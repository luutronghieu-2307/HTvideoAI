# Model Registry

## Responsibility

`config/models.yaml` is the versioned inventory for render backends. `ModelRegistry` validates the
schema and applies hard constraints before a model can be routed: enabled flag, task support,
Kaggle compatibility, explicit commercial-use review, healthy smoke-test status, and available
VRAM. An LLM preference can never override these checks.

## Initial safety state

The eligible list is empty until a model passes every hard gate. A repository URL or public
checkpoint is not evidence that the exact revision is safe, licensed for the intended use, or
runnable on Kaggle.

License review status:

- **Wan2.1 T2V 1.3B** — `commercial_use_reviewed: true` (Apache-2.0, permits commercial use). Still
  not eligible until a real Kaggle smoke test marks it `healthy`.
- All other planned models remain `commercial_use_reviewed: false` and `untested` or blocked.

## Promotion gate

Before enabling a record, pin the checkpoint revision, verify its license, record Kaggle GPU/VRAM,
run a real smoke test, validate the output, and update `last_smoke_test_at`. Store smoke-test logs
and hashes without embedding model credentials.
