# Custom Voice Prompting & Script Generation Component

## Purpose

The **Custom Voice Prompting** component enables granular control over video narration tone, target audience, duration, and voice style prompt parameters (`voice_style: "nam trầm, bình tĩnh"`).

## Key Features

- **Static System Prompt Caching (`SCRIPT_SYSTEM_PROMPT`)**: Byte-for-byte static instruction block for provider prefix caching.
- **Dynamic Per-Project Prompt (`build_script_prompt`)**: Injects `voice_style`, `tone`, `audience`, `duration_seconds`, and research notes.
- **Script Critique (`CritiqueService`)**: Evaluates script structure (Hook, Body, Conclusion) and source evidence alignment.

## Usage

```python
from app.services.prompts import build_script_prompt
from app.services.llm import generate_script

prompt = build_script_prompt(
    topic="Vì sao con người mơ?",
    language="vi-VN",
    tone="khoa học, dễ hiểu",
    audience="người trưởng thành không chuyên",
    voice_style="nam trầm, bình tĩnh",
    duration_seconds=120,
)
```

## Testing

Covered in `test/services/test_prompts.py` and `test/services/test_critique.py`.
