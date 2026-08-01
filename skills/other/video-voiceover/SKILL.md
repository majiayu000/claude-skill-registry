---
name: video-voiceover
user-invocable: false
description: >
 Synthesize Chinese narration audio (TTS voiceover) from a timestamped narration.json.
 Use to turn a written narration script into per-segment speech audio, with MiMo TTS
 (mimo-v2.5-tts), dynamic speed fitting, and loudness handling. Part of the video-recap bundle:
 consumes narration.json (output-timeline time), produces tts_segments + tts_meta.json.
 In the legacy direct-cut path, narration_mapped.json may be passed explicitly instead.
 触发词: 配音, 语音合成, TTS, 解说配音, voiceover, text to speech, 旁白配音.
---

## What this does

Reads a timestamped narration script and synthesizes one audio clip per segment, fitting speech
to each segment's time slot (dynamic rate), then records placement metadata. The only engine is
MiMo TTS (`mimo-v2.5-tts`).

## Requirements

```bash
export MIMO_API_KEY=***         # MiMo TTS (or a TTS-specific MIMO_TTS_API_KEY)
```

## Input contract

`work_dir/narration.json` — segments with `start` / `end` / `narration` (+ optional `pause_after_ms`,
`overlaps_speech`). Times are the **output-timeline** seconds the audio will be placed at.
In the orchestrated cut-mode flow, the agent writes `narration.json` directly against the output
timeline, and the orchestrator passes it here. In the legacy direct-cut path,
`narration_mapped.json` may be passed explicitly instead.

> **Running the scripts below** — the `scripts/…` paths are relative to this skill's own directory (the folder containing this `SKILL.md`). Claude Code runs commands from there, so they work as written. If your harness runs commands from the project root instead (opencode / Codex / OpenClaw commonly do), prefix this skill's absolute directory — e.g. `<skill-dir>/scripts/…`, using the directory your harness reports when it loads the skill. The scripts self-locate from their own path, so once started by the correct path they resolve their sibling skills and assets regardless of the working directory.

## Run

```bash
python3 scripts/voiceover.py --work-dir <work_dir> --narration <narration.json> \
  [--mimo-voice 冰糖 | --voice-ref <reference-audio>]
```

For direct one-off use, omitting `--narration` reads `work_dir/narration.json`.
Pass `--narration work_dir/narration_mapped.json` explicitly only for the legacy direct-cut path;
the video-recap orchestrator always passes `narration.json`.

## Output contract

- `tts_segments/*.wav` — one synthesized clip per narration segment.
- `tts_meta.json` — `{segments: [...], engine, narration}` where each segment carries its
  `audio_path`, timing, `pause_after_ms`, and placement fields consumed by **video-assemble**.
  When `--allow-partial-tts` lets a run continue past failed segments it also carries
  `partial: true` and `failures: [{index,start,end,text,error}]` so missing lines stay visible
  (a clean run carries `partial: false` and `failures: []`).

## Notes
- Re-runs safely reuse only matching per-segment audio; edited narration or TTS settings regenerate the affected WAVs.
- `--voice-ref` (full/cut recap only) switches narration to `mimo-v2.5-tts-voiceclone`; the reference
  is normalized lazily once when fresh synthesis is needed, and its content/preparation fingerprint
  invalidates stale cached segments. Use only with authorization; the reference is sent to MiMo.
- `TTS_WORKERS`, `TTS_TIMEOUT`, `TTS_RETRIES`, `ALLOW_PARTIAL_TTS` tune throughput/robustness.
- Dub mode has its own deterministic gate: `dub_lint.json` blocks empty/overlapping/out-of-range
  translation lines BEFORE voiceclone spend, and `dub_review.json` scaffolds fidelity/tone/timing/
  platform-fit review. `dub.py --stage lint|review` and `dub.py --print-schema` expose them directly.

## What this skill does NOT do
- Does NOT write or edit narration text.
- Does NOT mux, duck, or render subtitles — that is video-assemble.
- Does NOT analyze the video or choose timestamps — it voices the segments it is given.
