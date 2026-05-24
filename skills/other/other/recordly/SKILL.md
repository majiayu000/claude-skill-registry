---
name: recordly
description: "Polish screen recordings with Recordly (open-source Screen Studio alternative) — auto-zooms, cursor animations, webcam overlays, styled backgrounds, timeline editing. Also includes Slant: browser-based 3D perspective renderer with 12 animation presets and MP4/GIF export. Triggers on screen recording, demo video, Recordly, screen capture polish, product walkthrough, 3D perspective, Slant."
argument-hint: "[install | launch | open <file> | slant]"
---

# Recordly

Open-source screen recorder and editor for polished product demos, walkthroughs, tutorials, and social clips. Records screen or window, then provides a timeline editor with auto-zoom, cursor effects, webcam overlays, styled backgrounds, and MP4/GIF export. All effects are 2D pan-and-zoom with motion blur — not 3D perspective transforms.

Fork of OpenScreen (`siddharthvaddem/openscreen`, 10.6K stars, MIT). Recordly adds: webcam zoom-reactive scaling, `.recordly` project persistence, auto-captions (Whisper), enhanced cursor effects (sway, click bounce, loop mode), native capture backends. AGPL 3.0.

## When to Use

- Recording polished screen demos for PRs, docs, or social media
- Post-processing raw screen recordings with auto-zoom, cursor smoothing, and styled frames
- Creating product walkthrough videos with webcam overlay
- Polishing recordings captured via `compound-engineering:feature-video`

**When not to use**: For raw screen capture without polish (use macOS screenshot, OBS, or QuickTime). For headless/batch video processing (use ffmpeg). For device frame mockups with phone/laptop bezels (use Rotato or Shots.so). For audio mixing or voiceover (use a dedicated audio editor).

## Quick Start

```bash
# Install Recordly (clone, build, handle macOS quarantine)
bash scripts/install_recordly.sh

# Launch Recordly (or open a file directly)
bash scripts/launch_recordly.sh
bash scripts/launch_recordly.sh path/to/recording.mp4
bash scripts/launch_recordly.sh path/to/project.recordly
```

## Installation

Run the install script to clone, install dependencies, and build:

```bash
bash scripts/install_recordly.sh
```

The script clones `webadderall/Recordly` to `~/tools/recordly/`, runs `npm install`, builds the platform-appropriate app, and handles macOS quarantine.

Alternatively, download prebuilt releases from `https://github.com/webadderall/Recordly/releases`. On Arch Linux: `yay -S recordly-bin`.

## Integration with feature-video

Raw screen captures from `compound-engineering:feature-video` look unprofessional without post-processing — jarring mouse movements, no zoom on key interactions, plain backgrounds. Recordly fixes this:

1. Launch Recordly: `bash scripts/launch_recordly.sh`
2. Open the raw recording file in Recordly
3. Apply auto-zoom, cursor effects, and background styling
4. Export as MP4 and use the polished video in the PR description

## 3D Perspective Mode (Slant)

Flat screen recordings look generic on social media. Rendering them on a 3D plane with camera animation, HDRI reflections, and depth of field makes them look like Slant it ($69) or Screen Studio output — for free.

```bash
# Open the 3D perspective renderer in any modern browser
open scripts/slant.html
```

1. Drop a screen recording onto the viewport (or use the file picker)
2. Pick an animation preset (12 built-in: Hero Float, Dramatic Tilt, Orbit, Slide In, Push/Pull, Isometric, Carousel, Cinematic Pan, etc.)
3. Adjust background (gradient, solid color, or HDRI environment), depth of field, screen reflections
4. Export as MP4 (Twitter-ready, H.264), WebM, or GIF (GitHub PRs where GIFs render inline)

Self-contained HTML file — Three.js r183 from CDN, no build step, no server, no local dependencies. See `README.md` for the full preset gallery, export format details, and browser support matrix.

## Links

- **Repo**: `github.com/webadderall/Recordly`
- **Releases**: `github.com/webadderall/Recordly/releases`
- **Upstream (OpenScreen)**: `github.com/siddharthvaddem/openscreen`
- **License**: AGPL 3.0
