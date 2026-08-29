"""Prompt templates and output parsing for LLM-backed content generation and voice customization.

Prompts are split into static system prompt and dynamic per-project user prompt
to take advantage of provider prefix caching.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict

from loguru import logger

_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)

# Static, immutable rules block for prefix caching across LLM requests.
SCRIPT_SYSTEM_PROMPT = (
    "Bạn là trợ lý viết script video chuyên nghiệp, chuyên tạo nội dung dài dạng "
    "thuyết minh (documentary) cho video tự động.\n"
    "\n"
    "QUY TẮC BẮT BUỘC:\n"
    "\n"
    "1. LUÔN trả về JSON hợp lệ. KHÔNG kèm markdown, code block, hay text giải thích.\n"
    "\n"
    "2. Chỉ trả về đúng cấu trúc JSON sau, không thêm field nào khác:\n"
    '{"sections": [{"title": "string", "narration": "string", "visual_direction": "string"}]}\n'
    "\n"
    '3. "sections" phải có TỐI THIỂU 3 phần theo thứ tự:\n'
    "- Hook (mở đầu, gây chú ý)\n"
    "- Nội dung chính (giải thích chi tiết)\n"
    "- Kết luận (tóm tắt, nhấn mạnh)\n"
    "\n"
    '4. "narration" là lời đọc (thuyết minh) - viết tự nhiên, dễ nghe, đúng ngôn ngữ và giọng đọc (voice_style) yêu cầu.\n'
    "\n"
    '5. "visual_direction" là hướng dẫn hình ảnh cho scene - mô tả ngắn gọn cảnh quay hình ảnh.\n'
    "\n"
    '6. Mọi thông tin factual phải dựa trên "Ghi chú nguồn" được cung cấp. '
    "KHÔNG bịa thêm sự kiện, số liệu, hay nguồn không có trong ghi chú.\n"
    "\n"
    "7. Tổng độ dài narration phù hợp với thời lượng video yêu cầu "
    "(khoảng 150-160 từ mỗi phút)."
)


def build_script_prompt(
    *,
    topic: str,
    language: str = "vi-VN",
    tone: str = "khoa học, dễ hiểu",
    audience: str = "người trưởng thành không chuyên",
    voice_style: str = "nam trầm, bình tĩnh",
    duration_seconds: int = 60,
    source_notes: str = "",
) -> str:
    """Build the dynamic user prompt from project fields and research notes."""
    prompt_parts = [
        "Hãy viết script video cho thông tin sau:",
        f"- topic: {topic}",
        f"- language: {language}",
        f"- tone: {tone}",
        f"- audience: {audience}",
        f"- voice_style: {voice_style}",
        f"- duration_seconds: {duration_seconds}",
    ]
    if source_notes:
        prompt_parts.extend(["\nGhi chú nguồn (Research Notes):", source_notes])
    prompt_parts.append("\nHãy trả về JSON đúng cấu trúc quy định.")
    return "\n".join(prompt_parts)


def build_critique_prompt(script_json: str) -> str:
    """Build a prompt that asks the model to review a script for factuality and structure."""
    return (
        "Bạn là biên tập viên kiểm tra tính chính xác. Đánh giá kịch bản sau đây "
        "và trả về JSON: "
        '{"verdict": "approved|rejected", "score": 0-100, "hard_failures": [], "warnings": []}. '
        f"Kịch bản:\n{script_json}"
    )


def parse_json_output(text: str) -> Dict[str, Any]:
    """Parse JSON from an LLM response, tolerating markdown code fences."""
    stripped = (text or "").strip()
    match = _JSON_FENCE_RE.search(stripped)
    candidate = match.group(1).strip() if match else stripped
    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError as exc:
        logger.error(f"Failed to parse LLM JSON output: {text[:200]}")
        raise ValueError("LLM output is not valid JSON.") from exc

    if not isinstance(parsed, dict):
        raise ValueError("LLM output must be a JSON object.")
    return parsed
