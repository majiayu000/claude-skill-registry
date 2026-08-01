---
name: video-recap
description: >
 Generate a Chinese-narration recap video from an input video, end to end. Use when the user
 gives a video file (.mp4 / .mov / .mkv / .webm) and asks to add narration, generate voiceover,
 dub, summarize, or produce a recap (短剧 / 电视剧 / 电影 / 纪录片 / 科普). Orchestrates the
 video-* skill bundle: understanding → (agent writes narration) → cut → voiceover → assemble.
 触发词: 视频解说, 视频旁白, 生成解说, 视频recap, video recap, voiceover, narration, auto-dub, recap.
---

## What this is

A thin orchestrator over five independent, self-contained skills (each in `skills/`, sharing only
JSON/MP4 artifacts in a `work_dir` — no shared code):

```
video-understanding ─▶ (agent writes narration.json per video-script) ─▶ [video-cut] ─▶ video-voiceover ─▶ video-assemble
```

It is resume-safe: rerun the same command after writing `narration.json` to continue.
Phase B validates `recap_run_manifest.json` so an old `work_dir` from another source video or
different run settings is rejected instead of silently reusing stale narration. Understanding
artifacts are reused only when their provenance matches. For per-stage detail, read each skill's own SKILL.md.

## Install / env

```bash
# ffmpeg: brew install ffmpeg | apt install ffmpeg | choco install ffmpeg
export MIMO_API_KEY=***          # ONE key drives ASR + VLM + TTS (all MiMo)
```

The whole pipeline runs on ffmpeg + a single MiMo key: ASR (`mimo-v2.5-asr`), VLM (`mimo-v2.5`),
TTS (`mimo-v2.5-tts`). `tp-*` Token Plan keys default to the cn cluster (`MIMO_TOKEN_PLAN_CLUSTER`).
Optional MiMo scene-chunk video understanding: `--mimo-video-overview`.
Optional advisory final-stage review: `--mimo-qc pre-assemble|post-render|both`.
It is off by default, makes at most one request per selected stage, writes
`mimo_qc.json`, and is permanently fail-open/non-blocking.

Overridable defaults (zero-config otherwise): see `references/config-playbook.md`.

> **Running the scripts below** — the `scripts/…` paths are relative to this skill's own directory (the folder containing this `SKILL.md`). Claude Code runs commands from there, so they work as written. If your harness runs commands from the project root instead (opencode / Codex / OpenClaw commonly do), prefix this skill's absolute directory — e.g. `<skill-dir>/scripts/…`, using the directory your harness reports when it loads the skill. The scripts self-locate from their own path, so once started by the correct path they resolve their sibling skills and assets regardless of the working directory.

## Use

### 0. Research first (recommended)

If you can identify the source (show, film, topic), research it **before** analyzing and write
`work_dir/background_research.json` (see `video-understanding/references/research-guide.md`).
video-understanding folds it into the VLM context, so scene analysis can name characters and read
scenes with plot knowledge instead of labelling everyone "黑衣男子". Skip it when you can't research.

### 1. Analyze → pause for narration

```bash
python3 scripts/recap.py <video> --work-dir <work_dir> --context "背景"
```

Runs video-understanding (using `background_research.json` if you wrote it), writes
`agent_narration_brief.md`, and pauses. Then **write `work_dir/narration.json`** following the
**video-script** skill (read the brief first).
Cut mode (`--edit-mode cut --target-duration 10m`) also requires `clip_plan.json`.

Multi-video is cut-only. Use multiple positional videos plus `--edit-mode cut`; the generated project brief lists stable `source_id` values, and every `clip_plan.json` clip must include the chosen `source_id`:

```bash
python3 scripts/recap.py ep1.mp4 ep2.mp4 --edit-mode cut --target-duration 10m --work-dir work_dir_multi_ep
```

Optional filesystem material library:

```bash
python3 scripts/recap.py ep1.mp4 --material-library-dir .video-materials --save-materials
python3 scripts/recap.py ep1.mp4 ep2.mp4 --edit-mode cut --material-library-dir .video-materials --use-materials
```

Search is plain grep over JSON/MD/JSONL (for example `grep -R "keyword" .video-materials`). No raw media, DB, embeddings, or semantic search are part of the MVP.

### 2. Continue → produce the recap

Rerun the **same command** (narration.json now exists):

```bash
python3 scripts/recap.py <video> --work-dir <work_dir>          # [--edit-mode cut] [--no-burn-subtitles]
```

This validates the narration, (cut: builds `edited_source.mp4`), synthesizes the voiceover, and
assembles `recap_<name>.mp4`.

To ask MiMo for agent/user-facing suggestions without gating the render:

```bash
python3 scripts/recap.py <video> --work-dir <work_dir> --mimo-qc both
```

The pre-assemble review sees scripts/plans/TTS metadata; post-render also sees up
to six temporary JPEG samples. Matching inputs use a content cache; add
`--mimo-qc-refresh` to refresh. Missing credentials, 401/429, timeout, malformed
output, or sampling failure only produce an `unavailable`/`failed` pointer and
the pipeline continues. Frame base64 and credentials are never written to disk.

For source-pinned subtitles, first run `python3 tools/measure_subtitle.py <video>` from the repo
root, then pass the measured `--subtitle-y-top/--subtitle-y-bot`; this explicitly enables a 60%
opacity narration-window mask for that band. Coordinates use ffmpeg's auto-rotated display canvas
as a half-open `[top, bot)` interval and require a bottom-aligned ASS style. For cloned recap narration, pass
`--voice-ref <audio>` (distinct from dub mode).

### Dub mode — English→Chinese, original voice (`--edit-mode dub`)

Translates an English video into Chinese and **replaces** the speech with the ORIGINAL
speaker's cloned voice (`mimo-v2.5-tts-voiceclone`, same MiMo key) — distinct from recap/解说,
which overlays Chinese commentary on ducked audio. Same one-pause shape:

```bash
python3 scripts/recap.py <video> --edit-mode dub --work-dir <work_dir>     # prepare → pauses
```

Prepare transcribes the English audio in timed windows and pulls one reference clip, then writes
`dub_brief.md` + `dub_transcript.json`. The agent does all the judgment (like recap's narration):
**write `work_dir/dub_script.json`** = `[{"start": s, "end": s, "zh": "译文"}, …]` (ascending by
`start`) — translate **every** utterance faithfully on the source timeline and give each its source
`[start, end]` so the dub tracks the original's rhythm (don't drop a hook, merge, or condense; if
the original repeats, the dub repeats in sync). Keep each line speakable within its span (~5
chars/s). Rerun the same command to render `dub_<name>.mp4` — each line is cloned in the original
voice and time-fit to its `[start, end]` (placed at its start; only sped up if it would overrun the
next line, never globally — so the voice tracks the picture). v1: single speaker, full-track
replace (no background-music separation).

### Self-check

```bash
python3 scripts/recap.py --doctor
```

## Output

- `recap_<video>.mp4` — final video · `subtitles.srt` / `.ass` — subtitles
- `work_dir/` — all intermediate artifacts (the inter-skill contract; see `references/data-schema.md`)
- `work_dir/mimo_qc.json` — optional aggregated advisory report for selected
  pre-assemble/post-render stages; never a release gate

## Options (passed through to the stage skills)
`--context`, `--scene-threshold`, `--style`, `--edit-mode {full,cut,dub}`, `--target-duration`,
`--skip-asr`, `--mimo-video-overview`, `--mimo-qc {off,pre-assemble,post-render,both}`,
`--mimo-qc-refresh`, `--consolidate`, `--consolidate-asr`, `--mimo-tts-voice`,
`--voice-ref`, `--subtitle-y-top`, `--subtitle-y-bot`, `--no-burn-subtitles` (burn is on by default),
`--output-dir`, `--material-library-dir`, `--use-materials`, `--save-materials`.

`--style` is freeform verbatim guidance for the agent to synthesize with evidence; do not treat it as an option list, preset, switch, or finite style taxonomy.

## What this skill does NOT do
- Does NOT write narration.json / clip_plan.json — the agent authors those (see the video-script skill).
- Does NOT hard-block on the narration review (advisory; validate.py is the hard gate).
- Does NOT let MiMo QC block, repair, or change the exit status; subjective
  findings are pointers for the agent/user only.
- Is NOT an unattended scheduler — it is human-in-the-loop and posts to no channel.
- Shares NO code between stage skills — they communicate only through work_dir artifacts.
