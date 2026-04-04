---
name: gource-visualizer
description: >
  Produce animated source control visualizations using Gource. This skill
  handles installation of Gource and ffmpeg, detection of repository metrics,
  preset-based configuration, single and multi-repo log generation, ffmpeg
  video encoding pipeline, headless rendering for server environments, caption
  generation from git tags, GitHub avatar resolution, and GSD output delivery.
  Use this skill whenever the user wants to visualize repository history,
  create a code evolution video, see project timeline animations, generate
  Gource videos, combine multiple repos into one visualization, or produce
  any kind of source control visualization. Also trigger when the user mentions
  "Gource", "repo visualization", "code history video", "project evolution
  animation", or asks to "show me what we built".
---

# Gource Visualizer

Gource is an open-source software version control visualization tool that renders repository history as an animated tree. This skill orchestrates the full pipeline from installation through rendering, producing MP4 or WebM video files, PNG thumbnails, and render summary reports. It activates when a user wants to visualize repository history, create a code evolution video, generate a Gource animation, see project timelines, or says "show me what we built."

All script paths below are relative to `skills/gource-visualizer/`.

## Quick Start

The 80% case: a single git repository, one video output.

1. **Install dependencies** (idempotent -- skips if already present):
   ```bash
   bash scripts/install-gource.sh
   ```

2. **Detect repository metrics** -- captures commit count, contributors, date range as JSON:
   ```bash
   bash scripts/detect-repo.sh <repo-path>
   ```

3. **Select a preset** based on user intent (default: `standard`):
   - "quick look" / "preview" --> `quick`
   - "presentation" / "demo" --> `standard`
   - "publication" / "YouTube" / "portfolio" --> `cinematic`
   - "thumbnail" / "screenshot" --> `thumbnail`

4. **Render the video**:
   ```bash
   bash scripts/render-video.sh --repo <repo-path> --preset standard --output <output-dir>/video.mp4
   ```
   The render script auto-calculates `--seconds-per-day` from repository metrics and preset target duration. It auto-detects headless environments and delegates to `scripts/render-headless.sh` when no display is available.

5. **Deliver output** to the user with a summary: video file path, duration, resolution, file size, repository metrics (commits, contributors, date range).

## Decision Tree

Route user intent through this tree to select the right workflow path.

```
User wants a visualization
  |
  +-- Single repo in current directory?
  |   +-- Yes --> Quick Start path (above)
  |   +-- No  --> Ask which repo, or detect workspace repos
  |
  +-- Multiple repos mentioned?
  |   +-- Yes --> Multi-Repository Workflow (below)
  |
  +-- Specific time range mentioned?
  |   +-- Yes --> Add --start-date YYYY-MM-DD --stop-date YYYY-MM-DD
  |
  +-- Quality or purpose mentioned?
  |   +-- "quick look" / "preview"              --> preset: quick
  |   +-- "presentation" / "demo"               --> preset: standard
  |   +-- "publication" / "YouTube" / "portfolio" --> preset: cinematic
  |   +-- "thumbnail" / "screenshot"            --> preset: thumbnail
  |
  +-- No display / CI / server environment?
      +-- Auto-detected by render-video.sh; --headless flag added automatically
```

## Multi-Repository Workflow

Combine multiple repositories into a single visualization with namespace prefixing and optional per-repo color coding.

1. Collect repository paths from the user.
2. Merge logs with color coding:
   ```bash
   bash scripts/merge-repos.sh --color --output combined.log <repo1> <repo2> ...
   ```
3. Render the combined log:
   ```bash
   bash scripts/render-video.sh --repo combined.log --preset <preset> --output <output-dir>/video.mp4
   ```

For detailed multi-repo configuration (namespace prefixing, color palette, chronological sorting), see `references/multi-repo-guide.md`.

## Enhancement Options

Optional enhancements to add to any render command:

- **Captions** (milestone markers from git tags):
  ```bash
  bash scripts/generate-captions.sh <repo-path> captions.txt
  ```
  Then pass `--caption-file captions.txt` to `render-video.sh`.

- **Avatars** (GitHub profile pictures for contributors):
  ```bash
  bash scripts/resolve-avatars.sh <repo-path> avatars/
  ```
  Then pass `--avatar-dir avatars/` to `render-video.sh`.

- **Logo overlay:** `--logo path/to/logo.png`

- **Title overlay:** `--title "Project Name"`

- **Custom time range:** `--start-date YYYY-MM-DD --stop-date YYYY-MM-DD`

- **WebM format:** `--format webm` (VP9 codec instead of H.264)

- **Audio track:** Post-process with ffmpeg to add music (see `references/ffmpeg-pipeline.md`).

## Preset Reference

| Preset | Resolution | FPS | Use Case | Target Duration |
|--------|-----------|-----|----------|-----------------|
| quick | 720p (1280x720) | 30 | Fast preview, iteration | ~30s |
| standard | 1080p (1920x1080) | 60 | Presentations, demos | ~3 min |
| cinematic | 1080p (1920x1080) | 60 | YouTube, portfolio, publication | ~4 min |
| thumbnail | 1080p (1920x1080) | -- | Single frame capture | < 10s |

Preset configs are at `configs/preset-<name>.conf`. The render script auto-calculates `--seconds-per-day` to hit the target duration based on repository date range.

For preset customization and parameter details, see `references/presets.md`.

## Reference Documents

| Reference | When to Read | Purpose |
|-----------|-------------|---------|
| `references/installation-guide.md` | Installation fails or platform-specific issues | Detailed platform install procedures (apt, brew, manual) |
| `references/presets.md` | User wants to understand or customize presets | Preset breakdown, parameter tuning, config format |
| `references/ffmpeg-pipeline.md` | Video encoding issues, format conversion, audio | Complete ffmpeg recipe book for post-processing |
| `references/multi-repo-guide.md` | Combining multiple repositories | Step-by-step multi-repo workflow with examples |
| `references/custom-log-format.md` | Non-git sources, manual log creation | Gource custom log format specification |
| `references/option-reference.md` | Advanced customization beyond presets | Curated Gource option guide with examples |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "could not initialize SDL" | No display / headless environment | Use `--headless` flag or `scripts/render-headless.sh` |
| "Xvfb failed to start" | Xvfb not installed | `sudo apt-get install xvfb` |
| Black or corrupt video | ffmpeg framerate mismatch | Ensure ffmpeg `-r` matches Gource `--output-framerate` in preset config |
| No users visible | No commits in selected date range | Widen `--start-date` / `--stop-date` range |
| Very fast or slow video | Auto-timing miscalculation | Override with explicit `--seconds-per-day` value |
| "libx264 not found" | ffmpeg missing H.264 codec | `sudo apt-get install libx264-dev` or reinstall ffmpeg from package |

## GSD Integration

When running under a GSD workflow, output files go to the GSD output directory. The render summary includes: video path, duration, resolution, repo metrics, and contributor count.

For post-milestone visualization, read the milestone's git tag range to set `--start-date` and `--stop-date`, producing a video that covers exactly that milestone's development period.

The skill works with the gource-visualizer agent pipeline (see `agents/` directory) for fully automated multi-step workflows including installation, detection, rendering, and delivery.

## Script Inventory

| Script | Purpose |
|--------|---------|
| `scripts/install-gource.sh` | Idempotent installer for Gource, ffmpeg, Xvfb |
| `scripts/detect-repo.sh` | VCS detection and metrics extraction (JSON output) |
| `scripts/generate-log.sh` | Single-repo Gource custom log generation |
| `scripts/merge-repos.sh` | Multi-repo log merge with namespacing and color |
| `scripts/generate-captions.sh` | Git tags to Gource caption format |
| `scripts/resolve-avatars.sh` | GitHub API avatar fetcher with caching |
| `scripts/render-video.sh` | Gource-to-ffmpeg render pipeline orchestrator |
| `scripts/render-headless.sh` | Xvfb wrapper for headless environments |
