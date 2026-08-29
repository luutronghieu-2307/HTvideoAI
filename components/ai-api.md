# AI API (OpenAI-backed LLM adapter)

## Purpose

Provide a typed, secret-safe adapter that calls an LLM through the official OpenAI SDK while
keeping SDK objects out of domain code. Domain services depend on the `LLMBackend` protocol in
[`adapters.py`](../../backend/src/video_pipeline/adapters.py), not on the OpenAI client.

## Behavior

- `LLMBackend.complete(request)` sends a chat completion and returns a normalized `LLMResponse`.
- The API key is read from the `API_KEY_AI` environment variable (or a local `.env` file) and is
  never logged or echoed.
- Prompts are built in [`prompts.py`](../../backend/src/video_pipeline/AI_api/prompts.py) and
  parsed into JSON with `parse_json_output`, which tolerates markdown code fences.

### Prompt split for prefix caching

Script prompts are split into two parts to reduce token cost and latency:

- **Static system prompt** (`SCRIPT_SYSTEM_PROMPT`): the fixed rules block (JSON contract, minimum
  sections, narration/visual guidance, source-factuality rule, word-per-minute target). It is
  byte-for-byte identical across requests and sent as the system message, so providers can cache
  the encoded prefix and avoid re-encoding the same human-language instructions on every call.
- **Dynamic user prompt** (`build_script_prompt`): the small per-project payload built from
  `topic`, `language`, `tone`, `audience`, `voice_style`, and `duration_seconds` (all fields exist
  on [`Project`](../../backend/src/video_pipeline/schemas.py)).

Callers should pass `SCRIPT_SYSTEM_PROMPT` as the `system` field and the dynamic prompt as the
`prompt` field of `LLMRequest` so the static prefix stays stable and cacheable.

### Integration with ContentPipeline

When `VIDEO_PIPELINE_LLM_BASE_URL`, `VIDEO_PIPELINE_LLM_MODEL`, and `API_KEY_AI` are all set,
[`api.py`](../../backend/src/video_pipeline/api.py) builds an `OpenAILLMBackend` and injects it into
[`ContentPipeline`](../../backend/src/video_pipeline/content.py). The pipeline then generates the
script through the LLM (`mode="llm"`) instead of demo content. Without a fully configured backend it
falls back to `demo-local`, so CI and credential-free runs keep working.

### Retry and correlation ID

`OpenAILLMBackend.complete()` retries transient failures (rate limit, timeout, connection) with
exponential backoff (`base_delay_seconds * 2**attempt`, default 3 retries). Authentication and
invalid-response errors are never retried because they cannot recover. Every request carries an
`X-Correlation-ID` header; the caller may supply `LLMRequest.correlation_id`, otherwise the backend
generates one for tracing.

## Files

| File | Role |
|---|---|
| [`adapters.py`](../../backend/src/video_pipeline/adapters.py) | `LLMBackend` protocol + `LLMRequest`/`LLMResponse` DTOs |
| [`AI_api/client.py`](../../backend/src/video_pipeline/AI_api/client.py) | `load_api_key`, `build_openai_client` |
| [`AI_api/openai_backend.py`](../../backend/src/video_pipeline/AI_api/openai_backend.py) | `OpenAILLMBackend` implementation |
| [`AI_api/prompts.py`](../../backend/src/video_pipeline/AI_api/prompts.py) | prompt templates + JSON parsing |
| [`AI_api/errors.py`](../../backend/src/video_pipeline/AI_api/errors.py) | domain-specific exceptions |
| [`AI_api/schemas.py`](../../backend/src/video_pipeline/AI_api/schemas.py) | re-exports DTOs from `adapters.py` |

## State / data changes

No persistent state is written by this component. It is a stateless adapter; any caller is
responsible for persisting generated content and recording correlation IDs.

## Failure modes

| Failure | Raised exception |
|---|---|
| Missing/blank API key | `LLMAuthenticationError` |
| Invalid/expired key | `LLMAuthenticationError` |
| Rate limit / quota | `LLMRateLimitError` |
| Request timeout | `LLMTimeoutError` |
| Connection failure | `LLMError` |
| Empty or malformed response | `LLMInvalidResponseError` |
| Non-JSON output | `LLMInvalidResponseError` |

## Security impact

- The API key is a new credential. It must be stored in the environment or an ignored local
  `.env` file and never committed. `.env.example` documents `API_KEY_AI=` with no value.
- SDK objects never cross into domain models; only Pydantic DTOs are returned.
- No retry policy is implemented inside the adapter yet; callers should add bounded retries with
  backoff and a correlation ID.

## Tests

Covered in [`test_ai_api.py`](../../backend/tests/test_ai_api.py) using fake clients (no network):
key loading, client construction, normalized responses, and mapping of every failure mode above.

## Known limits

- Uses a single default model (`gpt-4o-mini`); model selection is not yet configurable per call.
- No streaming, tool calls, or structured-output mode yet.
- No built-in retry/backoff; add at the caller boundary.
