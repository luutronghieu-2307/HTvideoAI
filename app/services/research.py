"""Real ResearchBackend adapter backed by a local SearXNG instance or custom web search API.

SearXNG is a self-hosted metasearch engine exposing a free JSON API. This adapter
calls it to discover source candidates and retrieve evidence excerpts. It never
scrapes private endpoints; it uses the official SearXNG JSON API.
"""

from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Protocol

from pydantic import BaseModel, ConfigDict
from loguru import logger


class SourceCandidate(BaseModel):
    model_config = ConfigDict(frozen=True)

    source_id: str
    title: str
    url: str


class Evidence(BaseModel):
    model_config = ConfigDict(frozen=True)

    source_id: str
    excerpt: str
    checksum: str


class ResearchBackend(Protocol):
    def discover(self, query: str) -> list[SourceCandidate]: ...

    def retrieve(self, question: str) -> list[Evidence]: ...


class ResearchError(RuntimeError):
    """Raised when a research operation fails."""


class SearxngResearchBackend:
    """Discover and retrieve evidence from a local SearXNG JSON API."""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8080",
        *,
        timeout_seconds: int = 30,
        max_results: int = 10,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.max_results = max_results

    def discover(self, query: str) -> list[SourceCandidate]:
        logger.info(f"discovering research sources for query: {query}")
        results = self._search(query)
        candidates: list[SourceCandidate] = []
        for index, item in enumerate(results[: self.max_results], start=1):
            url = str(item.get("url", "")).strip()
            title = str(item.get("title", "")).strip()
            if not url or not title:
                continue
            candidates.append(
                SourceCandidate(
                    source_id=f"SRC-{index:03d}",
                    title=title,
                    url=url,
                )
            )
        logger.info(f"discovered {len(candidates)} research source candidates")
        return candidates

    def retrieve(self, question: str) -> list[Evidence]:
        logger.info(f"retrieving research evidence for question: {question}")
        results = self._search(question)
        evidence_list: list[Evidence] = []
        for index, item in enumerate(results[: self.max_results], start=1):
            url = str(item.get("url", "")).strip()
            excerpt = str(item.get("content", "")).strip()
            if not url or not excerpt:
                continue
            evidence_list.append(
                Evidence(
                    source_id=f"SRC-{index:03d}",
                    excerpt=excerpt,
                    checksum=hashlib.sha256(excerpt.encode("utf-8")).hexdigest(),
                )
            )
        logger.info(f"retrieved {len(evidence_list)} research evidence excerpts")
        return evidence_list

    def _search(self, query: str) -> list[dict[str, object]]:
        params = urllib.parse.urlencode({"q": query, "format": "json"})
        url = f"{self.base_url}/search?{params}"
        request = urllib.request.Request(url, method="GET")
        request.add_header("X-Forwarded-For", "127.0.0.1")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            logger.error(f"SearXNG request failed for url {url}: {exc}")
            raise ResearchError(f"SearXNG request failed: {exc}") from exc

        if not isinstance(payload, dict):
            raise ResearchError("SearXNG response must be a JSON object.")
        results = payload.get("results")
        if not isinstance(results, list):
            return []
        return [item for item in results if isinstance(item, dict)]
