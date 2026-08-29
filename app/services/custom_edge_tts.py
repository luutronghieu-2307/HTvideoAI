import asyncio
import inspect
import os
import queue
import threading
import time
from typing import Union

import edge_tts
from edge_tts import SubMaker
from loguru import logger

from app.config import config


_DEFAULT_EDGE_TTS_TIMEOUT_SECONDS = 300.0


def convert_rate_to_percent(rate: float) -> str:
    """
    Convert float rate multiplier to edge-tts sign-prefixed percentage format (e.g. "+0%", "-20%").
    """
    try:
        rate = float(rate)
    except (TypeError, ValueError):
        rate = 1.0
    if rate <= 0:
        rate = 1.0
    percent = round((rate - 1.0) * 100)
    if percent >= 0:
        return f"+{percent}%"
    return f"{percent}%"


def ensure_file_path_exists(file_path: str) -> None:
    """
    Ensure output parent directory exists for TTS writing.
    """
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)


def create_edge_tts_communicate(
    text: str, voice_name: str, rate_str: str
) -> edge_tts.Communicate:
    """
    Construct Communicate object based on installed edge_tts version capabilities.
    """
    communicate_kwargs = {"rate": rate_str}
    communicate_signature = inspect.signature(edge_tts.Communicate)

    if "boundary" in communicate_signature.parameters:
        communicate_kwargs["boundary"] = "WordBoundary"

    return edge_tts.Communicate(text, voice_name, **communicate_kwargs)


def get_edge_tts_timeout_seconds() -> Union[float, None]:
    """
    Get edge_tts stream timeout from config. Default is 300s for long video speech synthesis.
    """
    raw_timeout = config.app.get(
        "edge_tts_timeout", _DEFAULT_EDGE_TTS_TIMEOUT_SECONDS
    )
    try:
        timeout_seconds = float(raw_timeout)
    except (TypeError, ValueError):
        logger.warning(
            "invalid edge_tts_timeout: "
            f"{raw_timeout}, fallback to {_DEFAULT_EDGE_TTS_TIMEOUT_SECONDS}s"
        )
        timeout_seconds = _DEFAULT_EDGE_TTS_TIMEOUT_SECONDS

    if timeout_seconds <= 0:
        return None

    return timeout_seconds


def _stream_edge_tts_sync_with_timeout(
    communicate, on_chunk, timeout_seconds: float
) -> None:
    """
    Consume edge_tts stream_sync with total timeout safety.
    """
    stream_queue = queue.Queue()
    done_marker = object()

    def _produce_chunks():
        try:
            for chunk in communicate.stream_sync():
                stream_queue.put(("chunk", chunk))
            stream_queue.put(("done", done_marker))
        except Exception as e:
            stream_queue.put(("error", e))

    thread = threading.Thread(target=_produce_chunks, daemon=True)
    thread.start()

    deadline = time.monotonic() + timeout_seconds
    while True:
        remaining_seconds = deadline - time.monotonic()
        if remaining_seconds <= 0:
            raise TimeoutError(
                f"edge_tts stream timed out after {timeout_seconds:g}s"
            )

        try:
            item_type, payload = stream_queue.get(
                timeout=min(0.5, remaining_seconds)
            )
        except queue.Empty:
            continue

        if item_type == "chunk":
            on_chunk(payload)
        elif item_type == "error":
            raise payload
        elif item_type == "done":
            return


def stream_edge_tts_chunks(
    communicate, on_chunk, timeout_seconds: Union[float, None] = None
) -> None:
    """
    Stream chunks from edge_tts supporting both synchronous and asynchronous versions.
    """
    if hasattr(communicate, "stream_sync"):
        if timeout_seconds:
            _stream_edge_tts_sync_with_timeout(
                communicate, on_chunk, timeout_seconds
            )
            return

        for chunk in communicate.stream_sync():
            on_chunk(chunk)
        return

    if not hasattr(communicate, "stream"):
        raise AttributeError("edge_tts communicate object has no stream method")

    async def _consume_async_stream():
        async for chunk in communicate.stream():
            on_chunk(chunk)

    loop = asyncio.new_event_loop()
    try:
        if timeout_seconds:
            loop.run_until_complete(
                asyncio.wait_for(_consume_async_stream(), timeout=timeout_seconds)
            )
        else:
            loop.run_until_complete(_consume_async_stream())
    finally:
        loop.close()


def is_edge_tts_voice(voice_name: Union[str, None]) -> bool:
    """
    Check if the voice name specifies edge_tts custom provider (e.g. edge_tts:... or edge:...).
    """
    v = (voice_name or "").strip()
    return v.startswith("edge_tts:") or v.startswith("edge:")


def parse_edge_tts_voice_name(name: str) -> str:
    """
    Parse pure edge_tts voice name, stripping prefixes ('edge_tts:', 'edge:') and gender tags ('-Female', '-Male').
    """
    name = (name or "").strip()
    if name.startswith("edge_tts:"):
        name = name.split(":", 1)[1].strip()
    elif name.startswith("edge:"):
        name = name.split(":", 1)[1].strip()
    name = name.replace("-Female", "").replace("-Male", "").strip()
    return name


_AZURE_VOICES_DATA_FILE = os.path.join(
    os.path.dirname(__file__), "data", "azure_voices.json"
)


def get_edge_tts_voices(filter_locals=None) -> list[str]:
    """
    Get edge_tts voices list for dropdown selection.
    Prioritizes Vietnamese (vi-VN) voices at the top.
    """
    voices = []
    if os.path.exists(_AZURE_VOICES_DATA_FILE):
        try:
            import json
            with open(_AZURE_VOICES_DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    name = item["name"]
                    gender = item["gender"]
                    if "V2" in name:
                        continue
                    if filter_locals and not any(
                        name.lower().startswith(fl.lower()) for fl in filter_locals
                    ):
                        continue
                    voices.append(f"edge_tts:{name}-{gender}")
        except Exception as e:
            logger.warning(f"Failed to load azure_voices.json for edge_tts: {e}")

    if not voices:
        preset_voices = [
            "vi-VN-HoaiMyNeural-Female",
            "vi-VN-NamMinhNeural-Male",
            "zh-CN-XiaoxiaoNeural-Female",
            "zh-CN-YunxiNeural-Male",
            "zh-CN-YunjianNeural-Male",
            "zh-CN-XiaoyiNeural-Female",
            "zh-CN-YunyangNeural-Male",
            "en-US-AvaNeural-Female",
            "en-US-AndrewNeural-Male",
            "en-US-EmmaNeural-Female",
            "en-US-BrianNeural-Male",
        ]
        return [f"edge_tts:{v}" for v in preset_voices]

    vi_voices = [v for v in voices if "vi-VN" in v]
    other_voices = [v for v in voices if "vi-VN" not in v]
    vi_voices.sort()
    other_voices.sort()
    return vi_voices + other_voices


def custom_edge_tts(
    text: str,
    voice_name: str,
    voice_rate: float,
    voice_file: str,
    voice_volume: float = 1.0,
) -> Union[SubMaker, None]:
    """
    Generate speech using edge_tts.
    """
    clean_voice_name = parse_edge_tts_voice_name(voice_name)
    text = (text or "").strip()
    rate_str = convert_rate_to_percent(voice_rate)
    for i in range(3):
        try:
            logger.info(
                f"start edge_tts synthesis, voice name: {clean_voice_name}, try: {i + 1}"
            )

            ensure_file_path_exists(voice_file)
            communicate = create_edge_tts_communicate(text, clean_voice_name, rate_str)
            sub_maker = edge_tts.SubMaker()
            timeout_seconds = get_edge_tts_timeout_seconds()

            with open(voice_file, "wb") as file:
                def _handle_chunk(chunk):
                    chunk_type = chunk["type"]
                    if chunk_type == "audio":
                        file.write(chunk["data"])
                    elif chunk_type in ["WordBoundary", "SentenceBoundary"]:
                        sub_maker.feed(chunk)

                stream_edge_tts_chunks(
                    communicate, _handle_chunk, timeout_seconds=timeout_seconds
                )

            if not sub_maker.get_srt():
                logger.warning("failed, sub_maker.get_srt() is empty")
                continue

            logger.info(f"completed, output file: {voice_file}")
            return sub_maker
        except Exception as e:
            logger.error(f"failed edge_tts, error: {str(e)}")
            if os.path.exists(voice_file) and os.path.getsize(voice_file) == 0:
                try:
                    os.remove(voice_file)
                except Exception as remove_error:
                    logger.warning(
                        "failed to remove empty tts file: "
                        f"{voice_file}, error: {str(remove_error)}"
                    )
    return None
