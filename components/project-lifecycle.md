# Project Lifecycle Component

## Responsibility

`video_pipeline.projects.ProjectService` owns project creation and reload. It coordinates
validated schemas, safe path construction, Alembic migration, SQLite persistence, and portable
file mirrors. No caller constructs project paths or writes lifecycle state directly.

## Storage contract

SQLite at `.state/pipeline.db` is authoritative. `project.yaml` and `logs/events.jsonl` are
human-readable mirrors. A project starts in `CREATED`; later state transitions must validate the
current state and append a durable database event in the same transaction.

Alembic revision `0003` adds `options_json` for typed tone, voice, audience, render strategy,
preferred models, publish targets and approval mode. `ProjectService.get` upgrades older project
databases before loading them, so existing projects remain usable after a desktop update.

## Failure and recovery

Input and path validation happen before file creation. A duplicate project ID fails without
overwriting. If mirror generation is interrupted after the database transaction, `repair_mirrors`
can be added in the next lifecycle milestone; consumers must never infer authority from a mirror.

## Security invariants

- IDs and slugs cannot contain path separators, control characters, or Windows reserved names.
- Resolved project paths must remain beneath the configured root.
- YAML uses safe serialization; JSONL records structured fields only.
- No request may supply a database path or arbitrary output path.
