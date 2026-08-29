# Content Pipeline

## Responsibility

`ContentPipeline` coordinates source ingestion, research artifacts, immutable script v001 exports,
checksum-bound review, and deterministic critique. `ArtifactService` is the only writer for
versioned project artifacts and refuses different content at an existing path.

## Current modes

`demo-local` accepts user notes and never searches the web or calls an LLM. Every report and script
is labeled unverified. It exists so the complete application can be tested without credentials.

`llm` is used when a real `LLMBackend` is configured (see
[`ai-api.md`](ai-api.md)). `ContentPipeline` then calls the provider with the static
`SCRIPT_SYSTEM_PROMPT` plus a dynamic prompt built from the project fields and source notes, parses
the JSON response into a `ScriptDocument` with `mode="llm"`, and labels it as LLM-generated content
requiring human review. When no backend is configured, the pipeline falls back to `demo-local`.

`web` is used when a `ResearchBackend` (SearXNG) is configured (see
[`research.md`](research.md)). The pipeline discovers sources and retrieves evidence from the web
instead of user notes, then stores them as source notes with URLs for claim-to-source traceability.
Without a research backend, the pipeline falls back to user notes (`demo`).

Provider-backed research and generation must implement the same contracts and preserve source IDs,
checksums, and evidence metadata.

## Critique

When an `LLMBackend` is configured, `critique()` calls the provider with
`build_critique_prompt()` to review the script for factuality and structure, then maps the returned
`verdict` (`approved`/`rejected`) to `pass`/`fail`. If no source notes were supplied, a warning is
added because the LLM cannot cross-check facts. Without a backend, critique falls back to the
deterministic structural check (`demo-local`).

## Data and security

Canonical scripts are JSON; Markdown and DOCX are exports. Approval must match the latest SHA-256.
Source notes are length-bounded and recorded as `user_provided_unverified`. Artifact paths are
project-relative, traversal-resistant, atomic, immutable, and registered in SQLite.

## Tests and limits

Tests cover UTF-8, JSON/Markdown/DOCX output, no-source labeling, artifact idempotency, traversal,
conflict, checksum approval, critique, database persistence, and HTTP flow. Demo critique validates
structure and provenance flags; it does not establish factual accuracy.
