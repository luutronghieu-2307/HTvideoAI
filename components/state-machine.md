# Workflow State Machine

## Responsibility

`state_machine.py` is the only transition policy. `ProjectService.transition` validates an edge,
updates SQLite and writes a canonical event in one transaction, then updates YAML/JSONL mirrors.
Callers and UI code cannot assign status directly.

## Flow

```text
CREATED -> RESEARCHING -> DRAFTING -> AWAITING_USER_REVIEW
  -> CRITIQUING -> STORYBOARDING -> RENDERING -> AUDIO_ASSEMBLY
  -> FINAL_QC -> AWAITING_PUBLISH_APPROVAL -> PUBLISHING -> DONE
```

Review and QC can route to revision/re-render. Active states can fail closed to `FAILED`. Terminal
states cannot restart implicitly; a future recovery feature must record an explicit new workflow
run rather than silently rewriting history.

## Failure and recovery

SQLite is canonical. `repair_mirrors` rebuilds `project.yaml` and `events.jsonl` after interrupted
file writes. A later worker milestone must also persist the last safe retry target and operation
idempotency key before external side effects.

## Tests

`test_state_machine.py` covers valid, skipped, and terminal edges. Project and API tests prove state
and events survive reload and that corrupted mirrors can be rebuilt.
