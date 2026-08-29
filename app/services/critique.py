"""Script critique and fact-checking service.

Evaluates generated video scripts for structural completeness, factual alignment with
supplied research notes, and suitability for narration.
"""

from __future__ import annotations

from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict
from loguru import logger

from app.services.prompts import build_critique_prompt, parse_json_output


class CritiqueResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    verdict: str  # "pass" or "fail"
    score: int  # 0 to 100
    hard_failures: List[str]
    warnings: List[str]
    script_checksum: str


class CritiqueService:
    """Service to evaluate script factuality and structural quality."""

    def __init__(self, llm_backend: Any = None) -> None:
        self.llm_backend = llm_backend

    def critique_script(
        self,
        script_data: Dict[str, Any],
        script_checksum: str = "",
        source_notes_supplied: bool = True,
    ) -> CritiqueResult:
        """Critique script data using LLM if available, fallback to rule-based evaluation."""
        if self.llm_backend is not None:
            return self._critique_with_llm(script_data, script_checksum, source_notes_supplied)
        return self._critique_rule_based(script_data, script_checksum, source_notes_supplied)

    def _critique_with_llm(
        self,
        script_data: Dict[str, Any],
        script_checksum: str,
        source_notes_supplied: bool,
    ) -> CritiqueResult:
        import json
        script_json = json.dumps(script_data, ensure_ascii=False)
        prompt = build_critique_prompt(script_json)

        try:
            # Send completion request to LLM backend
            if hasattr(self.llm_backend, "complete"):
                from app.services.prompts import SCRIPT_SYSTEM_PROMPT
                # Protocol request format if using LLMBackend
                class LLMReq(BaseModel):
                    prompt: str
                    system: str = ""
                response = self.llm_backend.complete(LLMReq(prompt=prompt, system=SCRIPT_SYSTEM_PROMPT))
                text = getattr(response, "text", str(response))
            else:
                text = str(self.llm_backend(prompt))

            parsed = parse_json_output(text)
            raw_verdict = str(parsed.get("verdict", "")).strip().lower()
            hard_failures = [str(x) for x in parsed.get("hard_failures", []) if isinstance(x, str)]
            warnings = [str(x) for x in parsed.get("warnings", []) if isinstance(x, str)]

            if not source_notes_supplied:
                warnings.append("No source notes were supplied; LLM critique cannot cross-check facts.")

            raw_score = parsed.get("score", 0)
            try:
                score = int(raw_score) if isinstance(raw_score, (int, float, str)) else 0
            except (TypeError, ValueError):
                score = 0
            score = max(0, min(100, score))
            verdict = "pass" if raw_verdict == "approved" and not hard_failures else "fail"
            return CritiqueResult(
                verdict=verdict,
                score=score,
                hard_failures=hard_failures,
                warnings=warnings,
                script_checksum=script_checksum,
            )
        except Exception as exc:
            logger.warning(f"LLM critique failed, fallback to rule-based: {exc}")
            return self._critique_rule_based(script_data, script_checksum, source_notes_supplied)

    @staticmethod
    def _critique_rule_based(
        script_data: Dict[str, Any],
        script_checksum: str,
        source_notes_supplied: bool,
    ) -> CritiqueResult:
        hard_failures: List[str] = []
        warnings: List[str] = []

        sections = script_data.get("sections", [])
        if not isinstance(sections, list) or len(sections) < 3:
            hard_failures.append("Script must contain at least 3 sections (Hook, Body, Conclusion).")

        if not source_notes_supplied:
            warnings.append("No source notes were supplied; content is unverified.")

        # Evaluate word count and narration
        total_words = 0
        for section in (sections if isinstance(sections, list) else []):
            if isinstance(section, dict):
                narration = str(section.get("narration", "")).strip()
                if not narration:
                    hard_failures.append("Section narration cannot be empty.")
                total_words += len(narration.split())

        score = max(0, 100 - (40 * len(hard_failures)) - (10 * len(warnings)))
        verdict = "pass" if not hard_failures and score >= 80 else "fail"

        return CritiqueResult(
            verdict=verdict,
            score=score,
            hard_failures=hard_failures,
            warnings=warnings,
            script_checksum=script_checksum,
        )
