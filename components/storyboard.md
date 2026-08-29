# Storyboard Component

## Responsibility

`StoryboardService` turns the latest checksum-approved script into ordered durable scenes. Each
scene stores narration, visual prompt, target duration, status, and a stable ID in SQLite. The
portable JSON artifact binds the scene plan to the approved script checksum.

## Idempotency and failure behavior

Repeated calls return the same database scenes and immutable artifact. Storyboarding is refused
without an approved script or from an unrelated state. Artifact creation occurs before the scene
transaction so a retry can safely reuse identical content after interruption.

## Current limit

The demo creates one scene per script section and divides duration evenly. Production expansion
must add shot boundaries, dependencies, character/style references, critical-path scheduling, and
an explicit storyboard approval when creative control requires it.
