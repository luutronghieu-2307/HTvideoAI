# Kaggle Connectivity

## Responsibility

Kaggle rendering supports two independent optional connection paths behind `KaggleExecutor`:
an intermediary HTTP(S) proxy URL and the official direct Kaggle CLI. Configuration mode is
`auto`, `proxy`, or `direct`. Auto mode prefers a configured proxy and falls back to direct.

## Local configuration

`GET/PUT /api/v1/configuration/kaggle` manages the allowlisted values in the ignored local `.env`:

- `VIDEO_PIPELINE_KAGGLE_MODE`
- `VIDEO_PIPELINE_KAGGLE_PROXY_URL`
- `VIDEO_PIPELINE_KAGGLE_NAMESPACE`
- optional `KAGGLE_API_TOKEN`

The response exposes only `direct_token_configured`; it never echoes the token. Proxy URLs must be
absolute HTTP(S), contain no embedded credentials, and have no fragment. Direct mode also accepts
official OAuth/access-token files detected by the Kaggle CLI preflight.

## Execution boundary

Configured means only that local prerequisites exist. It does not prove the proxy protocol,
Kaggle quota, GPU availability, notebook permission, or output correctness. A real opt-in smoke
test must verify the chosen endpoint before a model can be promoted.

## Failure behavior

Explicit proxy/direct modes fail closed when their selected path is unavailable. Auto may use the
other configured path. Submission retries must retain idempotency keys and must not switch backend
after an external run has been accepted.
