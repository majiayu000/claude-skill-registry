---
name: video-content
description: "Three-tier video pipeline: ffmpeg Quick (5s, instant) → ffmpeg Enhanced with Ken Burns (15s, polished) → Remotion Animated (60-90s, production-grade). Takes static slides from Paper MCP or any PNGs and assembles them into platform-ready video. Make sure to use this skill whenever the user has slides, images, or PNGs and wants to turn them into video — even if they just say 'make a video from these', 'animate my slides', 'I have images and need a TikTok', or 'stitch these together'. Also use when they mention ffmpeg video assembly, Remotion-animated slide assembly, Ken Burns effects, or any slides-to-video pipeline. Owns the slides→MP4 assembly pipeline; for writing, debugging, or running `remotion render` on Remotion code itself, see /remotion-best-practices; for screen-recorded product demos, see /marketing-demo. Works with any PNG source — Paper exports, Canva, screenshots, anything."
category: creative
tier: nice-to-have
reads:
  - marketing/handoffs/*-handoff.yaml
  - marketing/content-specs/*.yaml
  - brand/creative-kit.md
  - brand/assets.md
writes:
  - marketing/video/*/
  - brand/assets.md
depends-on: []
triggers:
  - make video
  - video from slides
  - animate slides
  - render video
  - video content
  - assemble video
  - ffmpeg video
allowed-tools:
  - Bash(mktg status *)
  - Bash(ffmpeg *)
  - Bash(bun *)
  - Bash(bunx remotion *)
---

# /video-content — Video Assembly Pipeline

Three-tier video pipeline from static slides to platform-ready video. ffmpeg bookends every tier — slicing at the start, post-processing at the end.

For three-tier details, see [rules/three-tiers.md](rules/three-tiers.md).
For Remotion slide archetypes, see [references/remotion-archetypes.md](references/remotion-archetypes.md).
For ffmpeg recipes, see [references/ffmpeg-recipes.md](references/ffmpeg-recipes.md).

## ffmpeg Bookend Architecture

```
START (always): ffmpeg slice
  Input:  tall artboard PNG (e.g., 2160×26880 @ 2x) OR individual slide PNGs
  Output: individual slide PNGs at target resolution (1080×1920)
  Method: crop=W:H:0:Y per slide, scale to target

MIDDLE (tier-dependent):
  v1 Quick:    ffmpeg crossfade stitch
  v1.5 Enhanced: ffmpeg Ken Burns + audio
  v2 Full:     Remotion animate with spring physics

END (always): ffmpeg post-process
  - Audio mixing (background music, SFX from Remotion)
  - Two-pass H.264 encode (CRF 18, movflags +faststart)
  - Thumbnail extraction (best frame or slide 1)
  - GIF preview (first 3 seconds, 480px wide)
  - Platform-specific encode (TikTok, Instagram, YouTube presets)
```

## Workflow

### Phase 1: Detect Input

Check for these artifacts (in order of preference):

1. **Handoff YAML** at `marketing/handoffs/{name}-handoff.yaml` — written by /paper-marketing
2. **Content spec YAML** at `marketing/content-specs/{name}.yaml` — written by /slideshow-script
3. **Exported PNG** — user provides path to tall artboard export
4. **Slide directory** — user provides path to individual slide PNGs

If handoff YAML exists, read it for:
- `export_search_pattern` — filename pattern for the exported PNG
- `artboard.width`, `artboard.height`, `artboard.slide_count` — for ffmpeg slice coordinates
- `brand_snapshot` — full palette + fonts for Remotion `brand.ts` generation
- `content_spec` — path to the content spec YAML for slide types and animation hints
- `extracted_jsx` — optional HTML/CSS per slide for pixel-perfect Remotion reference

Both handoff YAML and content spec YAML are needed for v2 Full tier. Handoff provides export/brand info, content spec provides slide content and animation hints.

If no artifacts exist, ask the user:
```
"What slides should I turn into a video?"

Options:
1. "I have a Paper export PNG" — provide path
2. "I have individual slide PNGs" — provide directory
3. "Run /paper-marketing first" — go back to design phase
```

### Phase 2: ffmpeg Slice (START bookend)

If input is a tall artboard (not individual slides):

**Where does SLIDE_COUNT come from?**
- From `artboard.slide_count` in handoff YAML (preferred — exact value)
- From content spec YAML `slides` array length
- If neither exists, ask the user: "How many slides are in this image?"

```bash
# Detect slide count from image height
SLIDE_HEIGHT=$((IMAGE_HEIGHT / SLIDE_COUNT))

# Slice each slide
for i in $(seq 0 $((SLIDE_COUNT - 1))); do
  Y=$((i * SLIDE_HEIGHT))
  ffmpeg -i input.png \
    -vf "crop=${IMAGE_WIDTH}:${SLIDE_HEIGHT}:0:${Y},scale=${TARGET_W}:${TARGET_H}" \
    slides/slide_$((i + 1)).png
done
```

If input is already individual slides, skip to Phase 3.

### Phase 3: Select Tier

Use AskUserQuestion:
```
"Which video tier?"

1. "v1 Quick" (~5 seconds) — ffmpeg crossfade, no animation. Good for draft review.
2. "v1.5 Enhanced" (~15 seconds) — ffmpeg Ken Burns + background audio. Good enough to post.
3. "v2 Full" (~90 seconds) — Remotion animated with spring physics, SFX, light leaks. Production quality.
```

### Phase 4: Assemble (tier-dependent)

#### v1 Quick — ffmpeg Crossfade

```bash
# 3.5s per slide, 0.5s crossfade, H.264 CRF 18
ffmpeg -loop 1 -t 3.5 -i slide_1.png \
       -loop 1 -t 3.5 -i slide_2.png \
       ... \
       -filter_complex "xfade=transition=fade:duration=0.5:offset=3.0,..." \
       -c:v libx264 -crf 18 -pix_fmt yuv420p \
       -movflags +faststart output_v1.mp4
```

#### v1.5 Enhanced — Ken Burns + Audio

```bash
# Ken Burns: zoompan with subtle zoom + pan per slide
ffmpeg -loop 1 -t 4 -i slide_1.png \
  -vf "zoompan=z='min(zoom+0.0015,1.3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=120:s=1080x1920:fps=30" \
  ...
# Then stitch with xfade + add background audio
```

See [references/ffmpeg-recipes.md](references/ffmpeg-recipes.md) for full Ken Burns and audio mixing commands.

#### v2 Full — Remotion Animate

1. **Scaffold Remotion project** (if not exists):
   ```bash
   mkdir -p marketing/video/{name}
   cd marketing/video/{name}
   bun init -y
   bun add remotion @remotion/cli @remotion/transitions @remotion/google-fonts @remotion/layout-utils
   ```

2. **Read content spec YAML** for slide content + archetypes

3. **Generate slide components** using archetypes from [references/remotion-archetypes.md](references/remotion-archetypes.md):
   - Map `type: stat` → StatSlide component
   - Map `type: anchor_word` → AnchorWordSlide component
   - Map `type: emotional_pivot` → EmotionalPivotSlide component
   - etc.

4. **Auto-include in every v2 project:**
   - SFX on transitions: `@remotion/sfx` (whoosh, switch, page-turn mapped to archetype)
   - Light leaks at emotional pivots: `@remotion/light-leaks` with `hueShift` for brand color
   - `calculateMetadata` for dynamic duration based on slide count
   - Zod parametrizable schema (colors, text editable in Studio)
   - `fitText()` from `@remotion/layout-utils` for auto-sizing hero text

5. **Opt-in features** (ask user):
   - ElevenLabs voiceover + auto-subtitles
   - Custom SFX beyond defaults

6. **Render:**
   ```bash
   bunx remotion render src/index.ts TikTokSlideshow output_v2.mp4
   ```

Read the remotion-best-practices skill at `~/.claude/skills/remotion-best-practices/SKILL.md` for animation rules, and load specific rule files as needed (transitions.md, timing.md, text-animations.md, etc.).

### Phase 5: ffmpeg Post-Process (END bookend)

Always runs, regardless of tier:

```bash
# 1. Audio mix (if background music provided)
ffmpeg -i video.mp4 -i music.mp3 \
  -filter_complex "[1:a]volume=0.15[bg];[0:a][bg]amix=inputs=2" \
  -c:v copy mixed.mp4

# 2. Two-pass encode for optimal quality/size
ffmpeg -i mixed.mp4 -c:v libx264 -b:v 4M -pass 1 -f null /dev/null
ffmpeg -i mixed.mp4 -c:v libx264 -b:v 4M -pass 2 -movflags +faststart final.mp4

# 3. Thumbnail (slide 1 or best frame)
ffmpeg -i final.mp4 -vf "select=eq(n\,0)" -frames:v 1 thumbnail.png

# 4. GIF preview (first 3 seconds, 480px wide)
ffmpeg -i final.mp4 -t 3 -vf "fps=12,scale=480:-1" preview.gif

# 5. Platform-specific encode
# TikTok: H.264, 1080x1920, 30fps, CRF 18, AAC 128k
# Instagram: H.264, 1080x1350 or 1080x1920, 30fps, max 60s
# YouTube: H.264, 1080x1920, 30fps, CRF 16 (higher quality)
```

### Phase 6: Output and Register

**Output directory:** `marketing/video/{name}/`
```
marketing/video/lumi-aida/
├── slides/           # Individual slide PNGs
├── output_v1.mp4     # Quick version (if made)
├── output_v1.5.mp4   # Enhanced version (if made)
├── output_v2.mp4     # Full version (if made)
├── thumbnail.png     # Best frame
├── preview.gif       # 3-second preview
└── src/              # Remotion project (v2 only)
```

Update `brand/assets.md` with new video asset entry.

Report:
```
Video ready:
  File: marketing/video/{name}/output_{tier}.mp4
  Duration: {seconds}s
  Size: {MB} MB
  Resolution: {width}x{height}
  Thumbnail: marketing/video/{name}/thumbnail.png
  Preview GIF: marketing/video/{name}/preview.gif
```

## Standalone Usage

This skill works independently:
- `/video-content` alone — provide any slide PNGs, get video
- `/paper-marketing` → `/video-content` — design + assemble (no scripting)
- `/slideshow-script` → `/video-content` — skip Paper, use existing images
- Any PNG source → `/video-content` — works with Canva exports, screenshots, anything

## Prerequisites

- `ffmpeg` installed (8.0+)
- `bun` installed (for Remotion v2)
- For v2: Remotion packages installed automatically during scaffold

## Anti-Patterns

- **Wrong pixel format** — Always use `-pix_fmt yuv420p` for H.264. Without it, some players show a green screen or won't play at all.
- **Missing faststart** — Always include `-movflags +faststart` for web/social video. Without it, the video won't play until fully downloaded.
- **Scaling after stitching** — Always scale individual slides BEFORE stitching. Scaling the final video degrades quality.
- **Skipping the slice step** — Even if the input "looks like" individual slides, verify dimensions. A tall artboard that isn't sliced will produce a single stretched frame.
- **CRF too high** — CRF 18 is the sweet spot. CRF 23+ looks muddy on mobile. CRF below 15 balloons file size for marginal quality gain.
- **Assuming Remotion packages exist** — Before importing `@remotion/sfx` or `@remotion/light-leaks`, check if they're real packages. If unavailable, implement SFX with standard `<Audio>` component and light leaks with CSS gradients + opacity animation.
- **No audio track** — Social platforms may reject videos without an audio track. For v1, add a silent audio track: `-f lavfi -i anullsrc=r=44100:cl=stereo -shortest`.

## Edge Cases

- **ffmpeg not installed** — Check with `which ffmpeg`. If missing, tell the user: "Install ffmpeg: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)." Do not proceed without it.
- **Image height not divisible by slide count** — Round down the slide height. Warn the user that the bottom few pixels may be cropped. This is usually imperceptible.
- **Remotion render fails** — Common causes: missing fonts (use `@remotion/google-fonts`), missing assets in `public/`, or TypeScript errors. Check the error output and fix before retrying.
- **Disk space** — Video rendering needs space. A 7-slide v2 project can use 500MB+. Check available space before rendering.
- **Background music sourcing** — For v1.5, the user must provide a music file. Suggest royalty-free sources: YouTube Audio Library, Pixabay Music, or Uppbeat. Never use copyrighted music.
- **Corrupted PNG input** — If ffmpeg fails on a specific slide, verify the PNG opens in an image viewer. Re-export from Paper if corrupted.

## Principles

- **ffmpeg bookends everything** — slice at start, post-process at end, regardless of tier
- **Tiers are progressive** — v1 is instant, v1.5 is better, v2 is production. User chooses speed vs quality.
- **Content spec drives everything** — slide types, animation hints, and voice constraints come from YAML
- **Remotion best practices** — always load the remotion-best-practices skill for v2 work
- **No hardcoded content** — all text, colors, and timing come from content spec + brand files
