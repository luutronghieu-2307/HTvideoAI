import unittest

from app.services.critique import CritiqueResult, CritiqueService


class TestCritiqueService(unittest.TestCase):
    def setUp(self):
        self.critique_service = CritiqueService()

    def test_rule_based_critique_valid_script_passes(self):
        valid_script = {
            "sections": [
                {"title": "Hook", "narration": "Welcome to our video about dreaming."},
                {"title": "Body", "narration": "Scientists believe dreams process emotions."},
                {"title": "Conclusion", "narration": "Thank you for watching."},
            ]
        }
        result = self.critique_service.critique_script(
            script_data=valid_script,
            script_checksum="a" * 64,
            source_notes_supplied=True,
        )
        self.assertEqual(result.verdict, "pass")
        self.assertGreaterEqual(result.score, 80)
        self.assertEqual(len(result.hard_failures), 0)

    def test_rule_based_critique_missing_sections_fails(self):
        invalid_script = {
            "sections": [
                {"title": "Hook", "narration": "Only one section here."},
            ]
        }
        result = self.critique_service.critique_script(
            script_data=invalid_script,
            script_checksum="b" * 64,
            source_notes_supplied=False,
        )
        self.assertEqual(result.verdict, "fail")
        self.assertTrue(len(result.hard_failures) > 0)
        self.assertTrue(len(result.warnings) > 0)


if __name__ == "__main__":
    unittest.main()
