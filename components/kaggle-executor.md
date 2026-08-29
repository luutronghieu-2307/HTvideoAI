# Kaggle Executor

## Purpose

`KaggleExecutorBackend` is the real adapter for the `KaggleExecutor` protocol in
[`adapters.py`](../../backend/src/video_pipeline/adapters.py). It only *controls* Kaggle through the
official API/CLI; it never runs model inference locally. GPU work happens in a Kaggle kernel.

## Behavior

- `preflight()` reports blockers for the selected mode.
- `submit()` packages a payload directory and returns an `ExternalRun`.
- `status()` polls a run.
- `collect()` downloads and unpacks run output.

Two modes are supported:

- **Proxy** (`KaggleMode.PROXY`): calls an HTTP proxy contract at
  `{proxy_url}/submit`, `/status/{run_id}`, and `/output/{run_id}`. The proxy is responsible for
  talking to Kaggle. Uses `urllib` (stdlib), no extra dependency.
- **Direct** (`KaggleMode.DIRECT`): uses the official Kaggle CLI. `submit()` runs
  `kaggle kernels push` and reads the kernel slug from `kernel-metadata.json`; `status()` runs
  `kaggle kernels status <slug>`; `collect()` runs `kaggle kernels output <slug> -p <dir>`. Requires
  the CLI and an OAuth/API token (`KAGGLE_API_TOKEN` env or `~/.kaggle/` credentials).

## Files

| File | Role |
|---|---|
| [`kaggle_executor.py`](../../backend/src/video_pipeline/kaggle_executor.py) | `KaggleExecutorBackend` implementation |
| [`adapters.py`](../../backend/src/video_pipeline/adapters.py) | `KaggleExecutor` protocol + `ExternalRun` DTO |

## Failure modes

| Failure | Raised exception |
|---|---|
| Missing proxy URL / CLI / token | `KaggleExecutorError` (from `preflight`) |
| Proxy returns no `run_id` | `KaggleExecutorError` |
| Proxy HTTP/JSON error | `KaggleExecutorError` |
| Kaggle CLI non-zero exit | `KaggleExecutorError` |
| Direct mode missing `kernel/` dir | `KaggleExecutorError` |

## Security impact

- Proxy URL is validated as absolute HTTP(S) with no credentials/fragments (see
  [`configuration.py`](../../backend/src/video_pipeline/configuration.py)).
- Direct mode reads the official Kaggle token file; the token is never logged.
- CLI calls use fixed argv and `shell=False`.

## Tests

Covered in [`test_kaggle_executor.py`](../../backend/tests/test_kaggle_executor.py) with mocked
HTTP/CLI (no real network): preflight blockers, proxy submit/status/collect, direct submit, and
payload checksum.

## Known limits

- Direct `status()`/`collect()` require the kernel slug from `kernel-metadata.json` and a configured
  namespace for a fully qualified `<namespace>/<slug>` reference. A real Kaggle smoke test is still
  required to confirm the CLI output format for `kaggle kernels status`.
- No retry/backoff yet; add at the caller boundary.
