import asyncio
import json
import unittest
from unittest.mock import MagicMock, patch

from app.services.research import ResearchError, SearxngResearchBackend, SourceCandidate, Evidence


class TestResearchBackend(unittest.TestCase):
    def setUp(self):
        self.backend = SearxngResearchBackend(base_url="http://127.0.0.1:8080", timeout_seconds=5, max_results=5)

    def test_discover_sources_success(self):
        fake_response = {
            "results": [
                {"title": "Why Humans Dream", "url": "https://example.com/dream"},
                {"title": "Sleep and Memory", "url": "https://example.com/sleep"},
                {"title": "", "url": "https://example.com/empty"},
            ]
        }

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps(fake_response).encode("utf-8")
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response

            candidates = self.backend.discover("Why do humans dream?")
            self.assertEqual(len(candidates), 2)
            self.assertEqual(candidates[0].source_id, "SRC-001")
            self.assertEqual(candidates[0].title, "Why Humans Dream")
            self.assertEqual(candidates[0].url, "https://example.com/dream")

    def test_retrieve_evidence_success(self):
        fake_response = {
            "results": [
                {"title": "Dreaming Study", "url": "https://example.com/study", "content": "Dreams help process emotions."},
            ]
        }

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps(fake_response).encode("utf-8")
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response

            evidence_list = self.backend.retrieve("Dreaming facts")
            self.assertEqual(len(evidence_list), 1)
            self.assertEqual(evidence_list[0].source_id, "SRC-001")
            self.assertEqual(evidence_list[0].excerpt, "Dreams help process emotions.")
            self.assertTrue(len(evidence_list[0].checksum) == 64)

    def test_search_failure_raises_research_error(self):
        with patch("urllib.request.urlopen", side_effect=Exception("Connection refused")):
            with self.assertRaises(ResearchError):
                self.backend.discover("failure test")


if __name__ == "__main__":
    unittest.main()
