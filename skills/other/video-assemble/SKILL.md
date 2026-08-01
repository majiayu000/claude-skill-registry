---
name: video-assemble
user-invocable: false
description: >
 Assemble a final recap video: mux narration audio over the source video, duck the original
 audio under the narration, render subtitles (SRT/ASS, optionally burned in), and loudness-
 normalize. Use as the last stage of the video-recap bundle. Consumes the source video +
 tts_meta.json (+ narration placement); produces recap_<name>.mp4 + subtitles.srt/.ass.
 触发词: 视频合成, 混音, 字幕, 压字幕, assemble video, mux, ducking, subtitles, 成片.
---

## What this does

1. Mixes the narration audio segments onto the source video at their placed times.
2. **Ducks** the original audio under narration (fixed / sidechain / zone modes).
3. Renders **subtitles** from the narration placement → `subtitles.srt` (+ `subtitles.ass`
   when burning, which is **on by default**; `--no-burn-subtitles` to disable).
4. Optional final **loudness normalization** to a target LUFS.

## Input contract

- `<video>` — the source video (the original, or `edited_source.mp4` in cut mode).
- `work_dir/tts_meta.json` — `{segments: [...]}` from **video-voiceover** (each segment carries
  `audio_path`, timing, `pause_after_ms`, and `overlaps_speech`/placement used for ducking + subtitles).

> **Running the scripts below** — the `scripts/…` paths are relative to this skill's own directory (the folder containing this `SKILL.md`). Claude Code runs commands from there, so they work as written. If your harness runs commands from the project root instead (opencode / Codex / OpenClaw commonly do), prefix this skill's absolute directory — e.g. `<skill-dir>/scripts/…`, using the directory your harness reports when it loads the skill. The scripts self-locate from their own path, so once started by the correct path they resolve their sibling skills and assets regardless of the working directory.

## Run

```bash
python3 scripts/assemble.py <video> --work-dir <work_dir> \
  [--recap-stem <name>] [--output-dir <dir>] [--no-burn-subtitles]
  [--subtitle-y-top <inclusive-y> --subtitle-y-bot <exclusive-y>]
  [--source-video <orig.mp4>] [--export-jianying [--jianying-out <dir>]]
```

## Output contract

- `recap_<stem>.mp4` — the final recap video (written to `--output-dir` or `work_dir`'s parent). It is the stable output alias, overwritten in place on every run so iterating on the narration refreshes the same file.
- `work_dir/output.mp4` — the in-place render.
- `subtitles.srt` — narration subtitles; `subtitles.ass` when burning subtitles (on by default).
- `timeline.json` — backend-neutral multi-track model (video / original-audio / narration / BGM / subtitle tracks with ducking automation). Always written.
- `assembly_manifest.json` — a slim render record: the input/source paths, the cut-mode source fingerprint (proving a stale ambient `SOURCE_VIDEO` did not leak into a full-mode export), the render settings, and the final output path.
- 剪映 draft folder (`recap_<stem>/draft_content.json` + `draft_info.json` + `draft_meta_info.json`) — only with `--export-jianying`.

## Notes
- Audio is mixed as tracks (like a cut-software timeline): the original audio, an optional BGM bed, and the narration.
- Optional 剪映/JianYing export: `--export-jianying` (or `EXPORT_JIANYING=1`) turns `timeline.json` into an editable draft with original clips, separate narration/BGM tracks, subtitle materials, native volume keyframes, and optional local photo overlays. It is fully decoupled and lazy-imported: the ffmpeg render never depends on it, and 剪映 need not be installed. In cut mode pass `--source-video <orig>` so the draft references real source ranges. Bundling is on by default and copies video/audio/photo to `Resources/local/{video,audio,image}`, writes placeholder paths plus `draft_meta_info.json` indexes, and keeps a cloned/moved draft self-contained; `--jianying-no-bundle-media` is only for reachable original paths. Overlapping overlays split onto numbered lanes, and a non-empty draft folder gets a numbered sibling instead of being overwritten. Constant speed, reverse, transforms, rich text, transition/mask/LUT, green-screen compound drafts, and explicit sound/sticker/text-template/video-effect/face-effect tracks are available through the documented timeline v2 authoring extensions. Resource-backed features require legal caller-supplied offline packages; no official catalog, demo credential, text-template adapter, or AutoJY desktop automation is bundled. The draft references the un-burned source, so its hardcoded subtitles remain visible (mask them in 剪映 if needed).
- Subtitle look: `SUBTITLE_FONT_SIZE`, `SUBTITLE_MARGIN_V`, `SUBTITLE_MAX_CHARS`, etc.
- Source-pinned subtitle look: `SUBTITLE_Y_TOP/BOT` places the ASS baseline on a measured source
  band using half-open display-pixel coordinates `[top, bot)`. With an explicit mask policy, the band defaults to `SUBTITLE_MASK_OPACITY=0.6` and
  `SOURCE_SUBTITLE_MASK_TIMING=narration`; `SUBTITLE_MASK_PADDING` controls pixel padding.
- Ducking / loudness: the original swells to `IDLE_ORIG_VOLUME` in the gaps and ducks to `SPEECH_DUCKING_VOLUME` under narration (`DUCK_FADE_SECONDS` smooths the transition); also `DUCKING_MODE`, `ZONE_DUCKING_VOLUME`, `FINAL_LOUDNORM`, `TARGET_LUFS`.
- BGM (optional): set `BGM_PATH` to any audio file; it loops to length and ducks under narration (`BGM_VOLUME` / `BGM_DUCKING_VOLUME`).
- Burning subtitles requires an ffmpeg with `subtitles`/libass support; assemble (and the
  recap orchestrator) preflight this and fail fast with a clear message if it is missing.
- During original-audio blocks (the narration gaps), original dialogue is burned only when the
  source mask actually covers those gaps, or when a user-supplied subtitle file explicitly asks
  for replacement text. Narration-only masking otherwise leaves the source hard subtitles visible.
  Replacement dialogue is wrapped in `「」` to set it apart from narration
  (`SUBTITLE_ORIGINAL_IN_GAPS`, default on). Preferred source is the agent-calibrated
  `original_subtitles.json` (OUTPUT-time `[{start,end,text}]`); without it, a conservative auto-ASR
  mapping is used (cut mode remaps ASR source→output via the clip plan, assigns each line to the one
  gap it lands in, and skips lines too dense to read).

## What this skill does NOT do
- Does NOT generate narration or synthesize TTS.
- Does NOT re-transcribe or alter timing decisions — it consumes placement from tts_meta.json.
- Burning subtitles is **on by default** (`--no-burn-subtitles` to turn it off); when on, it
  re-encodes the video to draw the subtitle band.
