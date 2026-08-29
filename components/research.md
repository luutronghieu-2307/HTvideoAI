# Research Backend (SearXNG)

## Purpose

`SearxngResearchBackend` is the real adapter for the `ResearchBackend` protocol in
[`adapters.py`](../../backend/src/video_pipeline/adapters.py). It discovers web sources and
retrieves evidence through a local SearXNG instance's JSON API. It never scrapes private endpoints;
it uses the official SearXNG JSON API.

## Behavior

- `discover(query)` returns `SourceCandidate` (source_id, title, url).
- `retrieve(question)` returns `Evidence` (source_id, excerpt, checksum).

When `VIDEO_PIPELINE_RESEARCH_BASE_URL` is set, [`api.py`](../../backend/src/video_pipeline/api.py)
injects the backend into [`ContentPipeline`](../../backend/src/video_pipeline/content.py). The
pipeline then discovers sources from the web (`mode="web"`) instead of user notes. Without it, the
pipeline falls back to user notes (`demo`).

## Setup

Run [`setup-searxng.ps1`](../../scripts/setup-searxng.ps1) to start a local SearXNG container, then
set in `.env`:

```env
VIDEO_PIPELINE_RESEARCH_BASE_URL=http://127.0.0.1:8080
```

## Files

| File | Role |
|---|---|
| [`research.py`](../../backend/src/video_pipeline/research.py) | `SearxngResearchBackend` implementation |
| [`adapters.py`](../../backend/src/video_pipeline/adapters.py) | `ResearchBackend` protocol + DTOs |

## Failure modes

| Failure | Raised exception |
|---|---|
| SearXNG HTTP/JSON error | `ResearchError` |
| Non-object response | `ResearchError` |

## Security impact

- Uses the official SearXNG JSON API with a local-only instance.
- Sends `X-Forwarded-For: 127.0.0.1` to satisfy local bot-detection.
- No credentials are involved.

## Tests

Covered in [`test_research.py`](../../backend/tests/test_research.py) with mocked HTTP: discover,
retrieve, skipping entries without url/title, and error handling.

## Known limits

- Evidence is the search snippet only; full-page retrieval (e.g. Trafilatura) is not yet wired in.
- No retry/backoff yet; add at the caller boundary.
