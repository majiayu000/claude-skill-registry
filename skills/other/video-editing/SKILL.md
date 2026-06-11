---
name: video-editing
description: "Video editing pipeline: cut footage, assemble clips via FFmpeg and Remotion."
user-invocable: false
agent: python-general-engineer
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
  - Skill
routing:
  category: video-creation
  triggers:
    - edit video
    - cut footage
    - make vlog
    - screen recording
    - video workflow
    - ffmpeg
    - remotion
    - demo video
    - make a clip
    - assemble clips
    - video editing
  pairs_with:
    - typescript-frontend-engineer
---

# Video Editing Skill

## Overview

This skill implements a **6-layer pipeline** where AI handles judgment tasks (what to keep, what to cut, highlight selection) and FFmpeg/Remotion handle mechanical execution deterministically.

| Layer | Name | Mechanism | Primary Tool |
|-------|------|-----------|-------------|
| 1 | CAPTURE | Inventory source footage | Bash + Glob |
| 2 | AI STRUCTURE | Transcript to EDL | LLM judgment |
| 3 | FFMPEG CUTS | EDL to segment files | FFmpeg (deterministic) |
| 4 | REMOTION COMPOSITION | Segments to TSX composition | Remotion + TypeScript |
| 5 | AI GENERATION | Fill gaps with generated assets | ElevenLabs / fal.ai (conditional) |
| 6 | FINAL POLISH | Human taste layer | Human + NLE |

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| `references/preflight.md` | `preflight.md` | Before Phase 1 |
| `references/phase-commands.md` | `phase-commands.md` | Each phase |
| `references/errors.md` | `errors.md` | Error Handling |
| `references/ffmpeg-commands.md` | `ffmpeg-commands.md` | Phase 3, Proxy |
| `references/remotion-scaffold.md` | `remotion-scaffold.md` | Phase 4 |

## Instructions

### Preflight (Run before Phase 1)

**Hard requirements** (BLOCK if missing): `ffmpeg` (all phases), `node` (Remotion / npx).
**Soft requirements** (WARN if missing): `remotion` (only required for Phase 4).

Preflight script (dependency checks, install hints, exit codes): `references/preflight.md`.

---

## Phase 1: CAPTURE

**Goal**: Inventory all source footage and confirm files exist on disk before any processing.

**Constraint**: Source files are read-only. All FFmpeg commands write to new files only. Never overwrite source footage.

Steps: locate source files (find), inspect each with `ffprobe`, generate proxies for files >10 min (see `references/ffmpeg-commands.md` -> Proxy Generation), create working directories (`segments/`, `assembled/`). Full command block: `references/phase-commands.md` -> Phase 1.

**Gate**: Source files confirmed on disk. File list written to `source-inventory.txt`. Proceed only when gate passes.

---

## Phase 2: AI STRUCTURE

**Goal**: Analyze content and produce a written EDL (`cuts.txt`) that drives all downstream cutting.

**Constraint**: `cuts.txt` is the contract. The EDL file is the only source of truth for downstream phases. Do not hand-edit FFmpeg commands — generate them from the EDL.

**Constraint**: Before writing the EDL manually, run FFmpeg scene/silence detection. Detection output informs judgment, not replaces it.

Steps: transcribe with whisper/AssemblyAI, run scene/silence detection, apply judgment (what advances narrative, what is filler, target duration), write `cuts.txt` in EDL format `START_TIME,END_TIME,LABEL`, review for overlap and total duration. Full command block and EDL format example: `references/phase-commands.md` -> Phase 2.

**Gate**: `transcript.txt` exists. `cuts.txt` written to disk. Proceed only when both files exist.

---

## Phase 3: FFMPEG CUTS

**Goal**: Execute the EDL deterministically — one FFmpeg cut per segment in `cuts.txt`.

**Constraint**: Batch-cut from EDL using a loop. Do not create individual FFmpeg commands per cut. This ensures reproducibility and review capability as a list.

**Constraint**: Always generate concat-list.txt from cuts.txt order, not from shell glob. Shell glob (`segments/*.mp4`) sorts alphabetically, not by EDL order.

Steps: batch-cut from EDL with while loop (libx264/aac, `-avoid_negative_ts make_zero`), verify segments, generate `concat-list.txt` in EDL order, concat with `-f concat -safe 0 -c copy`. Full command block: `references/phase-commands.md` -> Phase 3. See also `references/ffmpeg-commands.md` -> Batch Cutting.

**Gate**: All segment files exist. `assembled/rough-cut.mp4` written to disk. Proceed only when gate passes.

---

## Phase 4: REMOTION COMPOSITION

**Goal**: Wrap segments in a Remotion TSX composition for programmatic overlays, titles, or transitions.

**When to use**: Only when rough-cut.mp4 requires programmatic elements (animated titles, lower thirds, caption tracks, brand overlays). If rough-cut.mp4 is sufficient, skip to Phase 6.

**Constraint**: Layer 4 requires TypeScript/React. Hand off to `typescript-frontend-engineer` for TSX work; return to `python-general-engineer` for Phase 5 onward.

Steps: initialize Remotion (`npm create video@latest` first time; otherwise `npm install @remotion/cli @remotion/player remotion`), scaffold composition (see `references/remotion-scaffold.md`), render with `npx remotion render`. Full command block: `references/phase-commands.md` -> Phase 4.

**Gate**: `assembled/remotion-output.mp4` exists. Proceed only when gate passes.

---

## Phase 5: AI GENERATION

**Goal**: Fill genuine gaps in source material with generated assets — only when needed.

**Constraint**: Check whether existing footage covers the gap before generating anything. Generate only what doesn't exist.

Decision tree: cut around the gap → update cuts.txt and re-run Phase 3; voiceover → ElevenLabs (authorization required); music → fal.ai (defer to fal-ai-media); b-roll → fal.ai (defer to fal-ai-media). ElevenLabs Python helper, authorization pattern, and save-to-disk flow: `references/phase-commands.md` -> Phase 5.

**Gate**: All required generated assets saved to `assets/` directory before proceeding.

---

## Phase 6: FINAL POLISH

**Goal**: Deliver assembled output and hand off taste-layer work to human.

**Constraint**: Layer 6 is human territory. The skill assembles; the human finishes. The following require human judgment and should not be attempted programmatically:

- Color grading and color matching between clips
- Music timing and volume ducking
- Caption style, font, positioning
- Transition timing and style
- Final audio mix levels

Handoff template (`handoff-notes.txt` with source list, EDL, rough-cut path, remaining-for-human checklist): `references/phase-commands.md` -> Phase 6.

**Gate**: `assembled/rough-cut.mp4` (or `assembled/remotion-output.mp4`) exists. `handoff-notes.txt` written to disk.

---

## Error Handling

Common errors (missing source files, FFmpeg codec errors, Remotion composition-not-found, concat-order bugs, ElevenLabs 401) and fixes: `references/errors.md`.

---

## References

| Reference | When to Load | Content |
|-----------|-------------|---------|
| `references/preflight.md` | Before Phase 1 | Dependency check script: ffmpeg, node, remotion |
| `references/phase-commands.md` | Each phase | Full shell command blocks for Phases 1-6 and gate checks |
| `references/errors.md` | Error Handling | Error matrix with causes and fixes |
| `references/ffmpeg-commands.md` | Phase 3, Proxy | FFmpeg recipes: timestamp extraction, batch cutting, concatenation, proxy generation, audio normalization, scene/silence detection, social reframing |
| `references/remotion-scaffold.md` | Phase 4 | TSX composition scaffold, render command, reuse patterns |

- [Remotion docs](https://www.remotion.dev/docs) -- TSX composition API
- [FFmpeg docs](https://ffmpeg.org/documentation.html) -- Flag reference
