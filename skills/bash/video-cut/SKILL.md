---
name: video-cut
user-invocable: false
description: >
 Cut a long video down to selected source ranges (montage / clip assembly). Part of the
 video-recap bundle: in the orchestrated (two-pass) flow, consumes clip_plan.json + the
 source video, produces edited_source.mp4; the agent then writes narration.json against
 the output timeline. When invoked standalone WITHOUT --no-narration-map, also remaps an
 existing narration.json → narration_mapped.json (legacy single-pass path).
 触发词: 视频剪辑, 剪辑式解说, video cut, clip plan, 拼剪.
---

## What this does

Takes an agent-authored **clip plan** (which source ranges to keep, in order) and:
1. Validates + enriches it into `clip_plan_validated.json` (clip ids, source/output times, total duration, overlap checks). Boundaries are then snapped to natural pauses (`SNAP_CLIP_LINE_END`) and nudged clear of the original footage's hard cuts (`SCENE_CUT_SNAP`, see below).
2. Concatenates those source ranges into a single `edited_source.mp4`.
3. **(Orchestrated path — default)** Stops here; the agent writes `narration.json` against the output timeline (0 .. total seconds). Invoked by `recap.py` with `--no-narration-map`.
4. **(Legacy single-pass path)** When invoked directly **without** `--no-narration-map`: maps narration written in original-video time onto the cut output timeline → `narration_mapped.json`.

It is stateless: given the same inputs it reproduces the same outputs. Caching is just
"reuse `edited_source.mp4` if it is newer than `clip_plan.json`".

## Input contract

`work_dir/clip_plan.json` — a JSON array, or `{"clips": [...]}`. Each clip:

```json
{"start": 12.0, "end": 28.5, "reason": "inciting incident"}
```

`start`/`end` are **original-video seconds** (aliases `source_start`/`source_end` or `in`/`out` accepted).
Optionally `target_duration` at the object top level (e.g. `"10m"`).

`work_dir/narration.json` (optional, legacy single-pass path only) — segments with original-video `start`/`end` + `narration` text, consumed only when `--no-narration-map` is NOT passed.
Each segment may carry `source_clip_id` to disambiguate when overlapping clips are allowed.

> **Running the scripts below** — the `scripts/…` paths are relative to this skill's own directory (the folder containing this `SKILL.md`). Claude Code runs commands from there, so they work as written. If your harness runs commands from the project root instead (opencode / Codex / OpenClaw commonly do), prefix this skill's absolute directory — e.g. `<skill-dir>/scripts/…`, using the directory your harness reports when it loads the skill. The scripts self-locate from their own path, so once started by the correct path they resolve their sibling skills and assets regardless of the working directory.

## Run

```bash
python3 scripts/cut.py <video> --work-dir <work_dir> \
  [--target-duration 10m] [--clip-padding 0] [--allow-overlap]
```

## Output contract

- `clip_plan_validated.json` — normalized clips with `clip_id`, `source_start/end`, `output_start/end`, `duration`.
- `edited_source.mp4` — the concatenated source video (the new shortened timeline).
- `narration_mapped.json` — **(legacy single-pass path only)** narration with `start`/`end` rewritten to output time and `source_clip_id` set. NOT produced in the orchestrated flow (`recap.py --no-narration-map`).

In the orchestrated flow, downstream (voiceover + assemble) treat `edited_source.mp4` as the video and `narration.json` (written by the agent against the output timeline) as the narration.

## Notes

- In the legacy single-pass path, timestamps in `clip_plan.json` and `narration.json` are **original-video time**; this tool does the source→output remap. In the orchestrated path, `narration.json` is written by the agent directly in **output-timeline time** — no remap is performed.
- Overlapping/duplicate source ranges raise an error unless `--allow-overlap` is set; with overlap, narration should set `source_clip_id`.
- Segments that fall outside every kept clip are dropped (logged).
- **Shot-change-aware boundaries (`SCENE_CUT_SNAP`, default on).** A clip boundary that lands a few tenths of a second from a hard cut in the *original* footage shows a brief sliver of the adjacent shot that then cuts again — a visible 闪烁/flicker at the edit point. After the natural-pause snap, each `source_start` is moved forward onto, and each `source_end` back onto, any original shot-change within `SCENE_CUT_SNAP_MARGIN` (default `0.5`s; detected with ffmpeg's scene metric at `SCENE_CUT_DETECT_THRESHOLD`, default `0.4`). Boundaries already on a cut, or with no nearby cut, are untouched; snaps that would shrink a clip below ~0.5s are skipped. Set `SCENE_CUT_SNAP=0` to disable.

## What this skill does NOT do
- Does NOT re-transcribe or re-analyze the video.
- Does NOT write narration, and does NOT pick clips for you — it consumes an agent-authored clip_plan.json.
- Does NOT re-encode beyond the concatenation/remap needed to build the cut source.
