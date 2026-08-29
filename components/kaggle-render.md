# Kaggle Render Backend

## Responsibility

`KaggleRenderBackend` implements the `RenderBackend` protocol by driving a remote Kaggle kernel
through `KaggleExecutor`. It packages one scene's prompt and metadata into a payload, submits the
job, polls status, and collects the produced video back to the caller's `output_path`. It never
runs model inference locally and never exposes Kaggle credentials.

## Flow

1. `preflight(job)` — delegates to `KaggleExecutor.preflight()` and verifies the job's `model_id`
   matches the backend's configured model.
2. `submit(job)` — writes `scene.json` (project, scene, model, prompt, duration) plus a `kernel/`
   directory (kernel metadata + `main.py`) into a temporary payload, then calls
   `KaggleExecutor.submit(payload, idempotency_key)`. The idempotency key is
   `render-{project_id}-{scene_id}`.
3. `status(run)` — delegates to `KaggleExecutor.status(run)`.
4. `collect(run)` — calls `KaggleExecutor.collect(run, output_dir)`, finds the first video file
   (`.mp4`, `.webm`, `.mov`, `.mkv`) in the collected output, and copies it to the recorded
   `output_path`.
5. `cancel(run)` — no-op; `KaggleExecutor` has no cancel operation.

## Data and security

- The payload contains only the scene prompt and metadata; no credentials are embedded.
- The kernel script is a placeholder template. The concrete Wan2.1 inference code is supplied by
  the worker contract in a later step.
- `output_path` is tracked per run id in memory so `collect` knows where to write.

## Tests and limits

- Covered by `backend/tests/test_kaggle_render.py` with a deterministic fake executor: payload
  packaging, preflight blockers, model mismatch, status delegation, collect copy, unknown run,
  missing video, and no-op cancel.
- Real GPU inference and a real Kaggle smoke test are not covered here; they require a
  `KAGGLE_API_TOKEN` or proxy URL and are opt-in.
