import unittest

from app.services.prompts import (
    SCRIPT_SYSTEM_PROMPT,
    build_critique_prompt,
    build_script_prompt,
    parse_json_output,
)


class TestPromptsService(unittest.TestCase):
    def test_script_system_prompt_is_immutable_and_contains_rules(self):
        self.assertIn("QUY TẮC BẮT BUỘC", SCRIPT_SYSTEM_PROMPT)
        self.assertIn("sections", SCRIPT_SYSTEM_PROMPT)
        self.assertIn("Hook", SCRIPT_SYSTEM_PROMPT)

    def test_build_script_prompt_with_custom_voice_style_and_notes(self):
        prompt = build_script_prompt(
            topic="Vì sao con người mơ?",
            language="vi-VN",
            tone="khoa học, dễ hiểu",
            audience="người trưởng thành",
            voice_style="nam trầm, bình tĩnh",
            duration_seconds=120,
            source_notes="Nguồn A: Mơ giúp xử lý cảm xúc.",
        )

        self.assertIn("topic: Vì sao con người mơ?", prompt)
        self.assertIn("voice_style: nam trầm, bình tĩnh", prompt)
        self.assertIn("tone: khoa học, dễ hiểu", prompt)
        self.assertIn("audience: người trưởng thành", prompt)
        self.assertIn("duration_seconds: 120", prompt)
        self.assertIn("Nguồn A: Mơ giúp xử lý cảm xúc.", prompt)

    def test_build_critique_prompt(self):
        script_json = '{"sections": []}'
        prompt = build_critique_prompt(script_json)
        self.assertIn("Bạn là biên tập viên kiểm tra tính chính xác", prompt)
        self.assertIn(script_json, prompt)

    def test_parse_json_output_handles_raw_json_and_markdown_fences(self):
        raw_json = '{"key": "value"}'
        parsed = parse_json_output(raw_json)
        self.assertEqual(parsed, {"key": "value"})

        fenced_json = "```json\n{\"sections\": [1, 2, 3]}\n```"
        parsed_fenced = parse_json_output(fenced_json)
        self.assertEqual(parsed_fenced, {"sections": [1, 2, 3]})

    def test_parse_json_output_raises_value_error_on_invalid_json(self):
        with self.assertRaises(ValueError):
            parse_json_output("Not a json")


if __name__ == "__main__":
    unittest.main()
