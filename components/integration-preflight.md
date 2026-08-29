# Integration Preflight

## Responsibility

`IntegrationPreflightService` reports whether Kaggle, LLM research, media runtime, render models,
publishers, and Tauri have their required local prerequisites. It never returns credential values
and never treats credential presence as proof that a provider works.

## Kaggle connections

The probe reports `kaggle_proxy` and `kaggle_direct` independently. Proxy requires only a validated
HTTP(S) URL. Direct recognizes the official CLI's `KAGGLE_API_TOKEN`, `~/.kaggle/access_token`, or
legacy `~/.kaggle/kaggle.json` mechanisms. Auto routing prefers proxy and falls back to direct.
Presence checks never perform a job or prove remote availability.

## States

`missing_prerequisites` means the user must provide or install something. `configured_unverified`
means configuration exists but no live smoke test has passed. Only an integration-specific real
test may promote status to ready/healthy.

Tauri desktop readiness requires Rust/Cargo and the MSVC C++ Build Tools workload. WebView2 is a
Windows runtime prerequisite and is checked during installer/build verification.

The Windows run script prepends `.tools/ffmpeg/bin`, `.venv/Scripts`, and the user Cargo bin to
the process PATH. Verified tool versions and SHA-256 values are recorded in
`config/runtime-tools.yaml`; tool binaries remain ignored and are never committed.

## Security

No secret is read into API output, logs, project files, YAML, or test fixtures. Publisher status
remains blocked until official account/app configuration and platform restrictions are verified.
