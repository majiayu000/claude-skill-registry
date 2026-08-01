---
name: video-understanding
user-invocable: false
description: >
 Analyze a video into a structured understanding index: scene detection, ASR transcript,
 per-scene visual (VLM) analysis, silence windows, a fused timeline, and a narration-writing
 brief. Use to understand / index / summarize what happens in a video, or as the first stage
 of the video-recap bundle before writing narration. Input: a video file. Output: scenes.json,
 asr_result.json, vlm_analysis.json, silence_periods.json, timeline_fusion.json,
 agent_narration_brief.md. 触发词: 视频理解, 视频分析, 视频索引, video understanding, analyze video, 看懂视频.
---

## What this does

Turns a source video into an **understanding index** an agent (or a downstream stage) can read:
1. **Scene detection** — `scenes.json` (cut points, durations) + junk-scene filtering.
2. **Frame extraction** — sampled frames for the visual analysis.
3. **ASR** — `asr_result.json` (timestamped dialogue) via MiMo `mimo-v2.5-asr`.
4. **Silence detection** — `silence_periods.json` (quiet windows, `has_speech` flag).
5. **VLM analysis** — `vlm_analysis.json` (per-scene description, depth analysis, `frame_facts`).
6. **Timeline fusion + brief** — `timeline_fusion.json`, `asr_writing_chunks.json`, `agent_narration_brief.md`.

Stateless: reusable stages are skipped only when their output and provenance sidecar match
the current source video plus output-affecting settings. `--force` recomputes.

## Requirements

```bash
# ffmpeg: brew install ffmpeg | apt install ffmpeg | choco install ffmpeg
export MIMO_API_KEY=***          # one key drives ASR (mimo-v2.5-asr) + VLM (mimo-v2.5)
```

ASR uses MiMo `mimo-v2.5-asr`; pass `--skip-asr` to skip dialogue transcription. The full understanding run still requires `MIMO_API_KEY` for VLM scene analysis.
Optional MiMo scene-chunk video understanding: `--mimo-video-overview`.

If `work_dir/background_research.json` exists (story research the agent did first, see
`references/research-guide.md`), its synopsis and named characters are folded into the VLM
context, so scene descriptions can name people and read scenes with plot knowledge. Combine with
`--context` for a quick inline hint.

> **Running the scripts below** — the `scripts/…` paths are relative to this skill's own directory (the folder containing this `SKILL.md`). Claude Code runs commands from there, so they work as written. If your harness runs commands from the project root instead (opencode / Codex / OpenClaw commonly do), prefix this skill's absolute directory — e.g. `<skill-dir>/scripts/…`, using the directory your harness reports when it loads the skill. The scripts self-locate from their own path, so once started by the correct path they resolve their sibling skills and assets regardless of the working directory.

## Run

```bash
python3 scripts/understand.py <video> --work-dir <work_dir> \
  [--context "节目名/角色名"] [--scene-threshold 0.1] [--skip-asr] [--mimo-video-overview] [--force]
```

## Output contract

| File | Content |
|------|---------|
| `scenes.json` | scene cut list (start/end/duration) |
| `asr_result.json` | `[{start, end, text}]` timestamped transcript |
| `vlm_analysis.json` | per-scene description / depth / `frame_facts` |
| `silence_periods.json` | `[{start, end, duration, has_speech}]` quiet windows |
| `timeline_fusion.json` | VLM + ASR + silence overlap, unified timeline |
| `asr_writing_chunks.json` | ASR split at sentence boundaries, scene-aligned |
| `agent_narration_brief.md` | the human/agent-facing writing brief (read this first) |

Downstream, **video-script** reads the brief + index to write `narration.json`.

## References
- Background research before writing: `references/research-guide.md` (writes `background_research.json`).
- Output JSON shapes: `references/data-schema.md`.

## What this skill does NOT do
- Does NOT write narration / 解说词 or score it — that is video-script.
- Does NOT cut, edit, voice, or render video.
- Does NOT invent plot the signal doesn't support — it emits a substrate warning when ASR/VLM are thin, rather than fabricating.
- Does NOT publish or schedule anything; it writes artifacts to work_dir and stops.
