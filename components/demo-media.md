# Demo Media Component

## Responsibility

`DemoMediaService` exercises the complete media workflow without external models. It creates a
deterministic PNG for every storyboard scene, mono WAV tone previews, SRT timing, an H.264/AAC MP4
assembled by the bundled FFmpeg runtime, and JSON reports. Outputs are immutable and checksummed.

## Truthfulness boundary

PNG candidates are not AI-generated video. WAV tones are not TTS narration. Reports explicitly set
`ai_model_inference: false`, `tts_used: false`, and `preview_only: true`. The MP4 proves local
assembly and decoding only; it is not evidence of model or voice quality.

## Optional AI render integration

When a `RenderBackend` (e.g. `KaggleRenderBackend`) is injected, `render_previews` also submits each
scene to the remote backend and stores the returned video as an `ai_render_candidate`. The
deterministic demo PNG is still produced so local assembly and QC keep working. The render report
then sets `mode: ai-kaggle` and `ai_model_inference: true`. Without a backend, behavior is unchanged
and the report stays `demo-local`.

## QC behavior

Demo QC verifies required artifacts, runs ffprobe, requires MP4/H.264/AAC, 640x360 video and 48 kHz
audio, then advances to checksum-bound publish approval. The report always writes
`public_publish_allowed: false`. Missing tools, files or an invalid media profile fail closed.

## Tests

Tests use a typed fake media runtime for normal CI and cover the FFmpeg command/profile adapter.
The Windows desktop smoke uses the real bundled FFmpeg/ffprobe runtime.
