---
name: mediamulti-speaker-orchestrator
description: 'Orchestrate multi-voice TTS production: assign speakers, chunk dialogue,
  dispatch to voices, sync timing, and mix into a final track. Use after dialogue-dramatizer
  produces script turns.'
---

---
name: media/multi-speaker-orchestrator
description: Orchestrate multi-voice TTS production: assign speakers, chunk dialogue, dispatch to voices, sync timing, and mix into a final track. Use after dialogue-dramatizer produces script turns.
---

# Multi-Speaker Orchestrator

Capabilities
- dispatch_tts_segment: send text chunks to specific voice models.
- sync_audio_timing: insert/align pauses between turns.
- mix_audio_track: merge per-speaker audio into a single output (MP3/WAV).

Dependencies
- hybrid-orchestrator (flow control)
- canary-orchestration (safe rollout of new voices/pipelines)

Inputs
- scripted turns with speaker labels and optional prosody tags.

Outputs
- final mixed audio + timing metadata.

Usage
- Route each turn to its assigned voice model, align timing, then mix into a single deliverable. Use canary to test new voices before full deployment.
