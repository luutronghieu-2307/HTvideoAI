# Operator Web UI

## Responsibility

`frontend/` is a React/Vite control surface for the local FastAPI service. It creates and reloads
projects, drives only valid workflow actions, shows state and artifacts, and keeps approval input
explicit. The workspace uses an eight-step progress rail, one primary action per state, compact
runtime status, and grouped settings. Business rules remain in the backend.

Project setup captures topic, duration, language, tone, audience, voice style, render mode,
preferred models, publish targets and manual approval mode. These values persist in SQLite through
Alembic revision `0003` and appear in the project summary after restart.

## Runtime

Development uses the Vite loopback proxy. Production build output is served by FastAPI on
`127.0.0.1:8765`, avoiding CORS and a second production process. `scripts/run.ps1` refuses to start
when the environment or frontend build is missing.

## Security and limits

The UI is not an authentication boundary and must not be exposed beyond loopback. The optional
Kaggle direct token is write-only: the API returns only whether it exists and the input is cleared
after saving. Multi-user mode requires authentication, authorization, CSRF/origin controls,
OS-backed per-user secret storage, and new threat-model review.

## Verification

TypeScript strict checking, Vitest, and Vite production build are part of `scripts/verify.ps1`.
Backend HTTP tests cover every action currently exposed by the UI. Final-video downloads use the
loopback API origin in Tauri rather than the application asset origin.
