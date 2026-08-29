# Publishing Safety

## Responsibility

`PublishingService` binds final video bytes, caption, targets, and privacy to one SHA-256 bundle.
Approval and publishing requests must reproduce the exact bundle. A changed video, caption, target,
or privacy setting fails closed.

## Demo publisher

The only implemented publisher writes a local JSON report containing
`published_publicly: false`. It records an idempotency operation and can safely return the same
result after retry. It never contacts a platform and cannot be mistaken for a successful public
post.

## Real platforms

Facebook Page and TikTok remain blocked by integration preflight. Their future adapters must query
live account capability, use official APIs, redact authorization, classify retryable errors, and
respect TikTok's unaudited `SELF_ONLY` restriction. Public mode needs user consent tied to the
current artifact and platform audit status.

## Tests

Tests cover non-video rejection, exact caption binding, idempotent retry, terminal state, and the
explicit non-public demo report. Media validation is a separate prerequisite before an artifact may
be registered as `final_video` in production mode.
