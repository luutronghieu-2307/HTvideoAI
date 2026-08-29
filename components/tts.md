# TTS Backend (Edge TTS)

## Purpose

`EdgeTTSBackend` is the real adapter for the `TTSBackend` protocol in
[`adapters.py`](../../backend/src/video_pipeline/adapters.py). It synthesizes narration audio with
Microsoft Edge voices via `edge-tts` — free, local, and credential-free.

## Behavior

- `synthesize(text, voice_id, output_path)` writes an MP3 file and returns its path.
- Vietnamese projects use `vi-VN-NamMinhNeural`; English projects use `en-US-GuyNeural`.

When `DemoMediaService` has a `tts_backend`, `create_audio_previews()` generates real narration
(`mode="tts"`, `tts_used=true`) instead of tone WAV previews. Without a backend it falls back to
tone previews (`demo-local`).

## Files

| File | Role |
|---|---|
| [`tts.py`](../../backend/src/video_pipeline/tts.py) | `EdgeTTSBackend` implementation |
| [`adapters.py`](../../backend/src/video_pipeline/adapters.py) | `TTSBackend` protocol |

## Failure modes

| Failure | Raised exception |
|---|---|
| Synthesis error (network, voice) | `TTSError` |
| No output file produced | `TTSError` |

## Security impact

- No credentials involved; edge-tts uses Microsoft's public Edge voices.
- Output is written only to project-scoped paths.

## Tests

Covered in [`test_tts.py`](../../backend/tests/test_tts.py) with mocked synthesis: output writing,
error handling, and voice selection by language.

## Known limits

- Requires network access to Microsoft Edge TTS endpoints at runtime.
- No BGM/SFX mixing or loudness normalization yet; those are future work.
