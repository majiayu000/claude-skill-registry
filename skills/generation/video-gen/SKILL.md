---
name: video-gen
version: 1.0.0
description: |
  Video generation via fal.ai -- from quick one-off clips to multi-scene
  productions with keyframes, state tracking, and assembly. 10+ models
  including Kling 3.0, Veo 3.1, Sora 2, LTX-2.3. Two modes: light
  (fire-and-forget) and project (structured pipeline with gates).
tools_required:
  - python3 (+ requests library)
  - ffmpeg + ffprobe (project mode assembly)
triggers:
  - generate video, create video, make a clip, render animation
  - text to video, image to video, t2v, i2v
  - story video, multi-scene, video production, storyboard
  - assemble clips, combine scenes, video project
---

# video-gen

Video generation and multi-scene production via fal.ai. Two modes: light (fire-and-forget) and project (interactive pipeline with gates).

**Scripts:** `./scripts/generate.py`, `./scripts/preview.py`, `./scripts/project_init.py`, `./scripts/project_state.py`, `./scripts/decompose.py`, `./scripts/keyframe.py`, `./scripts/clip.py`, `./scripts/assemble.py`, `./scripts/character_sheet.py`
**Output dir:** `./output/`

## Setup

```bash
export FAL_KEY="your-fal-ai-key"
```

- **Claude Code:** copy this skill folder into `.claude/skills/video-gen/`
- **Codex CLI:** append this SKILL.md content to your project's root `AGENTS.md`

For the full installation walkthrough (prerequisites, API keys, verification, troubleshooting), see [references/installation-guide.md](references/installation-guide.md).

### Credential management

Three tiers for managing the `FAL_KEY` environment variable:

1. **Vault skill (recommended):** If you have a vault or secret-management skill, store the key there and export it before running scripts. Example: `export FAL_KEY=$(vault get FAL_KEY)`
2. **Custom secret manager:** Use your team's preferred secret manager (1Password CLI, AWS Secrets Manager, etc.)
3. **Plain export:** `export FAL_KEY='your-fal-ai-key'` in your shell profile

For project mode (keyframes + character sheets): also need `image-gen` peer skill.

## Staying Updated

This skill ships with an `UPDATES.md` changelog and `UPDATE-GUIDE.md` for your AI agent.

After installing, tell your agent: "Check `UPDATES.md` in the video-gen skill for any new features or changes."

When updating, tell your agent: "Read `UPDATE-GUIDE.md` and apply the latest changes from `UPDATES.md`."

Follow `UPDATE-GUIDE.md` so customized local files are diffed before any overwrite.

---

## Decision Tree

```text
Need video?
├── Quick one-off clip? ─────────── Light Mode (generate.py)
│   Single prompt, single output, no state
│
└── Multi-scene story/production? ── Project Mode
    ├── New project? ─────────────── project_init.py → G0
    ├── Existing project? ────────── project_state.py --status
    └── Resume at gate? ──────────── Check state, pick up where left off
```

---

## Quick Reference

### Light Mode

```bash
# Generate with default model (ltx-2.3)
python ./scripts/generate.py \
  --prompt "A red fox running through snow" \
  --output ./output/

# Generate with specific model and settings
python ./scripts/generate.py \
  --prompt "Tokyo skyline at sunset with dramatic clouds" \
  --model kling-v3 \
  --mode t2v \
  --duration 10 \
  --resolution 1080p \
  --aspect 16:9

# Image-to-video generation
python ./scripts/generate.py \
  --prompt "The character starts walking forward" \
  --mode i2v \
  --image ./path/to/keyframe.png \
  --model veo-3

# Quick preview (uses LTX fast, cheapest)
python ./scripts/preview.py \
  --prompt "Test scene" \
  --mode t2v
```

### Project Mode

```bash
# Initialize new project
python ./scripts/project_init.py \
  --name noir-detective \
  --scenes 5 \
  --output-dir ./projects \
  --style "cinematic, moody, film noir" \
  --tier standard \
  --logline "A detective investigates in a cyberpunk city"

# Check project status
python ./scripts/project_state.py --project ./projects/noir-detective

# Generate keyframe for scene
python ./scripts/keyframe.py \
  --project ./projects/noir-detective \
  --scene 1 \
  --style-keywords "cinematic, moody"

# Generate video clip for scene
python ./scripts/clip.py \
  --project ./projects/noir-detective \
  --scene 1 \
  --model kling-v3 \
  --duration 8

# Assemble final video
python ./scripts/assemble.py \
  --clips-dir ./projects/noir-detective/scenes \
  --output ./projects/noir-detective/output/final.mp4
```

---

## Light Mode

### Model Selection

```text
What do you need?
├── Fast drafts + budget? ──────────── ltx-2.3 (fast) $0.04/s
├── Cinematic quality? ─────────────── kling-v3 $0.168/s
├── Dialogue/lip sync? ─────────────── veo-3 $0.20-0.40/s
├── Long clips (>10s)? ─────────────── sora-2 (up to 25s)
├── Budget with audio? ─────────────── wan $0.05-0.10/s
├── Anime/stylized? ────────────────── hailuo $0.045-0.08/s
└── Physics accuracy? ──────────────── cosmos $0.20/video
```

| Use Case | Model | Cost/5s | Why |
|----------|-------|---------|-----|
| Fast drafts | `ltx-2.3` | $0.20 | Open source, 4K capable, fastest iteration |
| Cinematic | `kling-v3` | $0.84 | Multi-shot narratives, character consistency |
| Dialogue/lip sync | `veo-3` | $2.00 | Best-in-class audio sync, natural performances |
| Long clips | `sora-2` | $2.50 | Up to 25s duration, complex scenes |
| Budget with audio | `wan` | $0.50 | Cheapest audio option, social media |
| Anime/stylized | `hailuo` | $0.40 | Anime support, micro-expressions |
| Physics | `cosmos` | $0.20 | RL-trained on physics, simulation-accurate |

### Script Reference: generate.py

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `ltx-2.3` | Model alias: ltx-2.3, kling-v3, veo-3, sora-2, wan, hailuo, cosmos, pixverse, grok |
| `--mode` | `t2v` | t2v (text-to-video) or i2v (image-to-video) |
| `--prompt` | required | Video description |
| `--image` | none | Source image path or URL (required for i2v) |
| `--duration` | `8` | Duration in seconds |
| `--resolution` | `1080p` | 720p, 1080p, 1440p, 4k |
| `--aspect` | `16:9` | 16:9, 9:16, 1:1 |
| `--fps` | `24` | Frames per second |
| `--seed` | none | Reproducibility seed |
| `--output` | `./output/` | Output directory or file path |
| `--no-preview` | false | Skip macOS QuickLook preview |
| `--no-audio` | false | Disable audio generation |
| `--quality` | `standard` | fast, standard, pro |
| `--dry-run` | false | Cost estimate only, no API call |
| `--timeout` | `300` | Queue timeout in seconds |
| `--negative-prompt` | none | What to exclude from generation |
| `--json` | false | Output JSON only (suppress stderr logs) |

### Script Reference: preview.py

```bash
# Preview existing video file
python ./scripts/preview.py /path/to/video.mp4

# Generate and preview (uses LTX fast, $0.04/s)
python ./scripts/preview.py \
  --prompt "Quick test scene" \
  --mode t2v \
  [--image path] \
  [--output path]
```

### Output JSON Contract

```json
{
  "success": true,
  "file": "/abs/path/to/20260308-143052-t2v-red-fox-snow.mp4",
  "model": "ltx-2.3",
  "mode": "t2v",
  "duration_sec": 8,
  "resolution": "1080p",
  "cost_usd": 0.32,
  "seed": 42,
  "fal_request_id": "abc123"
}
```

### Duration Constraints

| Model | Valid Durations | Notes |
|-------|----------------|-------|
| LTX-2.3 | 2, 4, 6, 8, 10s | Fixed increments only |
| Kling V3/2.6 | 5, 10s | Two options only |
| Veo 3.1 | 5-8s | Any value in range |
| Sora 2 | 5-20s (std), 5-25s (pro) | Any value in range |
| Hailuo | 4-6s | Any value in range |
| Wan | 3-5s | Any value in range |
| Cosmos | 5-9s | Any value in range |

### Cost Quick Reference

| Model | Video Only | With Audio | 4K Available |
|-------|-----------|-----------|-------------|
| `ltx-2.3` (fast) | $0.04/s | $0.04/s | Yes ($0.16/s) |
| `ltx-2.3` (std) | $0.06/s | $0.06/s | Yes ($0.24/s) |
| `wan` | $0.05/s | $0.10/s | No |
| `hailuo` | $0.045/s | N/A | No |
| `kling-v3` | $0.168/s | $0.336/s | No |
| `veo-3` (fast) | $0.10/s | $0.15/s | No |
| `veo-3` (std) | $0.20/s | $0.40/s | No |
| `sora-2` (720p) | $0.30/s | included | No |
| `sora-2` (1080p) | $0.50/s | included | No |

---

## Project Mode

### Gate Pipeline (G0-G5)

| Gate | Stage | What | Scripts | JSON Output |
|------|-------|------|---------|-------------|
| **G0** | Project Setup | Initialize project structure, manifest, state | `project_init.py` | project_dir, manifest, state paths |
| **G1** | Shot Prompts | Story decomposition into scene prompts | `decompose.py` | LLM prompt for story breakdown |
| **G2** | Reference Images | Generate keyframe images per scene | `keyframe.py` | keyframe image paths, costs |
| **G3** | Sequence Review | Review and lock shot sequence | `project_state.py --lock-sequence` | sequence lock confirmation |
| **G4** | Video Generation | Generate video clips per scene | `clip.py` | video clip paths, costs |
| **G5** | Assembly | Combine clips into final video | `assemble.py` | final video path, metadata |

### Detailed Gate Instructions

**G0 - Project Setup**: Use `project_init.py` to create project folder with `scenes/`, `characters/`, `audio/`, `output/` subdirectories, `manifest.md` template, and `state.json` tracking file. Define style, tier, budget, aspect ratio.

**G1 - Shot Prompts**: Use `decompose.py` to generate LLM prompt for story decomposition. Coordinator runs this against LLM to get scene-by-scene breakdown. Update `state.json` with scene prompts.

**G2 - Reference Images**: Run `keyframe.py` for each scene to generate keyframe images. These anchor the visual style and serve as I2V inputs. Requires `image-gen` peer skill.

**G3 - Sequence Review**: Use `project_state.py --lock-sequence` to freeze the shot sequence. No more scene additions/deletions after this gate. Review keyframes before locking.

**G4 - Video Generation**: Run `clip.py` for each scene to generate video clips using keyframes as I2V input. Outputs `shot_NN.mp4` files in `scenes/NN-name/` directories.

**G5 - Assembly**: Use `assemble.py` to discover clips and combine them with `ffmpeg`. Supports crossfades, audio overlay, and story.json metadata for timing.

### Script Reference: project_init.py

| Flag | Default | Description |
|------|---------|-------------|
| `--name` | required | Project name (kebab-case) |
| `--scenes` | required | Number of scenes (int >= 1) |
| `--output-dir` | required | Parent directory for project |
| `--aspect` | `16:9` | 16:9, 9:16, 1:1 |
| `--style` | `cinematic` | Style keywords (comma-separated) |
| `--tier` | `standard` | budget, standard, premium, ultra |
| `--logline` | none | One-line story description |
| `--budget` | `50.0` | Max spend in USD |

### Script Reference: project_state.py

```bash
# Display status table
python ./scripts/project_state.py --project /path/to/project

# Update gate status
python ./scripts/project_state.py \
  --project /path \
  --scene 1 \
  --gate prompt \
  --status locked \
  --path scenes/01-intro/prompt.md

# Add new scene
python ./scripts/project_state.py \
  --project /path \
  --add-scene \
  --scene-name climax \
  --scene-number 6

# Lock sequence (G3)
python ./scripts/project_state.py --project /path --lock-sequence

# Invalidate downstream gates
python ./scripts/project_state.py \
  --project /path \
  --scene 1 \
  --invalidate prompt
```

### Script Reference: decompose.py

| Flag | Default | Description |
|------|---------|-------------|
| `--idea` | required | Story concept description |
| `--style` | required | Visual style keywords |
| `--aspect-ratio` | `16:9` | Video aspect ratio |
| `--duration` | `30` | Total target duration (seconds) |
| `--tier` | `standard` | Generation tier |
| `--output` | none | Save LLM prompt to file |

### Script Reference: keyframe.py

| Flag | Default | Description |
|------|---------|-------------|
| `--project` | required | Project directory path |
| `--scene` | required | Scene number |
| `--style-keywords` | none | Override style keywords |
| `--model` | from tier | Image generation model |
| `--no-state-update` | false | Don't update state.json |

### Script Reference: clip.py

| Flag | Default | Description |
|------|---------|-------------|
| `--project` | required | Project directory path |
| `--scene` | required | Scene number |
| `--model` | from tier | Video generation model |
| `--duration` | `6` | Clip duration in seconds |
| `--quality` | `standard` | fast, standard, pro |
| `--bridge` | false | Use temporal bridging |
| `--seed` | none | Reproducibility seed |
| `--no-state-update` | false | Don't update state.json |

### Script Reference: assemble.py

| Flag | Default | Description |
|------|---------|-------------|
| `--clips-dir` | required | Directory containing scene clips |
| `--output` | required | Output video file path |
| `--story` | none | story.json for timing metadata |
| `--audio` | none | Voiceover track path |
| `--music` | none | Background music path |
| `--crossfade` | `0.5` | Crossfade duration between clips |

### Script Reference: character_sheet.py

| Flag | Default | Description |
|------|---------|-------------|
| `--character-json` | required | Characters definition file |
| `--character-id` | required | Character ID from JSON |
| `--output-dir` | required | Output directory for images |
| `--views` | `front,profile,three_quarter` | Comma-separated view list |
| `--tier` | `standard` | Image generation tier |

### File Structure

```
project-name/
├── manifest.md                    # Human-readable project summary
├── state.json                     # Machine state tracking (G0-G5)
├── story.json                     # Scene decomposition (G1 output)
├── characters.json                # Character definitions
├── scenes/
│   ├── 01-intro/
│   │   ├── prompt.md              # Scene description
│   │   ├── keyframe.png           # Reference image (G2)
│   │   └── shot_01.mp4           # Generated clip (G4)
│   ├── 02-conflict/
│   │   ├── prompt.md
│   │   ├── keyframe.png
│   │   └── shot_02.mp4
│   └── ...
├── characters/                    # Character reference sheets
│   ├── detective-front.png
│   ├── detective-profile.png
│   └── ...
├── audio/                         # Voiceover and music
└── output/                        # Final assembled videos
    └── final.mp4
```

### Token Efficiency Rules

1. **Coordinator context management**: Load only current gate's requirements, not full project history
2. **Scene isolation**: Each scene script operates independently with minimal cross-references
3. **State checkpoints**: Use `state.json` as single source of truth, not file system scanning
4. **Selective loading**: Scripts load only required JSON sections, not entire project state

### Going Back / Cascade Rules

- **Upstream change**: Invalidates all downstream gates automatically
- **Prompt change (G1)**: Invalidates G2 (keyframes), G4 (clips), G5 (assembly)
- **Keyframe change (G2)**: Invalidates G4 (clips), G5 (assembly)
- **Sequence lock (G3)**: Prevents scene additions/deletions, allows content changes
- **Clip regeneration (G4)**: Invalidates G5 (assembly) only

### Style Control (3 Layers)

1. **Project tier**: Maps to default models (budget→ltx-2.3, standard→kling-v3, premium→kling-v3, ultra→veo-3)
2. **Project style keywords**: Applied to all keyframes and clips automatically
3. **Per-scene overrides**: `--style-keywords` flag on keyframe.py/clip.py for scene-specific variations

---

## Dependencies

### Required for Light Mode
- Python 3.10+
- `requests` library: `pip install requests`
- fal.ai API key (`FAL_KEY` environment variable)

### Required for Project Mode (additional)
- `ffmpeg` + `ffprobe` (video assembly): install via system package manager
- `image-gen` peer skill (keyframes + character sheets)

### Image-gen Peer Resolution

Scripts resolve image generation dependency in this order:

1. **Environment override**: `IMAGE_GEN_SCRIPT=/path/to/generate.py` (explicit path)
2. **Auto-discovery**: `../image-gen/scripts/generate.py` (peer skill in fieldwork layout)
3. **Actionable error**: "Image generation requires the image-gen skill. Install it as a peer skill or set IMAGE_GEN_SCRIPT env var."

---

## Anti-Patterns

| Anti-pattern | Why it fails | Do this instead |
|-------------|-------------|-----------------|
| Using `produce.py` when interactive mode is appropriate | Skips human review gates, produces lower quality | Use project mode (G0-G5 pipeline) for quality work |
| Skipping style checkpoint on first keyframe | Inconsistent visual style across scenes | Review and approve keyframe style before generating remaining scenes |
| Generating video before locking prompts and images | Wasted generation costs on changing requirements | Complete G1-G3 (prompts, keyframes, sequence lock) before G4 |
| Hardcoding model without considering budget | Cost overruns, especially with Sora/Veo | Use `--dry-run` first, choose model based on budget and use case |
| Generating clips out of order | Breaks temporal bridging between scenes | Generate clips sequentially: scene 1, 2, 3... |
| Loading full prompts into coordinator context | Token waste, context overflow | Load only current gate requirements, use state.json for coordination |
| Using `--duration 4` with LTX | API validation error (LTX minimum is 6s) | Use `--duration 6` or higher for LTX model |
| Forgetting `--image` flag for i2v mode | Generation fails with validation error | Always provide `--image` path/URL for image-to-video |
| Using Kling for 15s clips | Model constraint violation (max 10s) | Use Sora 2 for clips longer than 10s |
| Skipping `--lock-sequence` before G4 | Scene changes invalidate expensive video generation | Lock sequence at G3 before generating any videos |

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| FAL_KEY not set | Missing API credential | `export FAL_KEY='your-fal-ai-key'` |
| Image-gen not found | Missing peer skill dependency | Install image-gen skill or set `IMAGE_GEN_SCRIPT` env var |
| ffmpeg not found | Missing video assembly dependency | Install ffmpeg: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux) |
| Duration validation failure | Invalid duration for model | Check duration constraints table, use valid values |
| HTTP 429: Rate limit | Too many requests | Wait 30s and retry, or switch to different model |
| HTTP 402: No credits | fal.ai account balance | Top up fal.ai account balance |
| API timeout | Model overloaded or network issue | Increase `--timeout` or try `--quality fast` variant |
| No video URL in result | Malformed API response | Check fal.ai status, try different model |
| Downloaded file is empty | Network interruption during download | Retry generation, check network stability |
| Model not available | Model endpoint changed or deprecated | Check `references/models.md` for current endpoints |
| Invalid aspect ratio | Unsupported ratio for model | Use 16:9, 9:16, or 1:1 (universally supported) |
| Project directory exists | Name collision | Choose different `--name` or remove existing directory |
| Sequence already locked | Trying to add scenes after G3 | Use `project_state.py --unlock-sequence` or work with existing scenes |
| Clip discovery failed | Assembly can't find generated clips | Check clip naming pattern `shot_NN.mp4` in `scenes/*/` directories |

---

## Bundled Resources Index

| Path | What | When to Load |
|------|------|-------------|
| `./scripts/generate.py` | Core video generation script | Every light mode generation task |
| `./scripts/preview.py` | Quick preview wrapper (LTX fast) | Quick tests and iteration |
| `./scripts/project_init.py` | Project structure initialization | Starting new multi-scene project (G0) |
| `./scripts/project_state.py` | State management and status display | Managing project gates, checking progress |
| `./scripts/decompose.py` | Story decomposition LLM prompt | Breaking story into scenes (G1) |
| `./scripts/keyframe.py` | Keyframe image generation | Creating visual references (G2) |
| `./scripts/clip.py` | Scene video generation | Generating video clips (G4) |
| `./scripts/assemble.py` | Final video assembly via ffmpeg | Combining clips into final video (G5) |
| `./scripts/character_sheet.py` | Multi-view character reference sheets | Character consistency across scenes |
| `./references/models.md` | Complete model catalog with capabilities and pricing | Model selection and optimization |
| `./references/model-kling.md` | Kling 3.0 detailed reference card | Kling-specific generation parameters |
| `./references/model-veo.md` | Veo 3.1 detailed reference card | Veo-specific features and audio capabilities |
| `./references/model-sora.md` | Sora 2 detailed reference card | Sora-specific parameters and remix features |
| `./references/model-ltx.md` | LTX-2.3 detailed reference card | LTX-specific modes and 4K capabilities |
| `./references/model-wan.md` | Wan 2.5/2.6 detailed reference card | Wan-specific features and budget optimization |
| `./references/model-hailuo.md` | Hailuo-02 detailed reference card | Hailuo anime/stylization capabilities |
| `./references/fal-api.md` | fal.ai queue API reference | API integration and debugging |
| `./references/pricing.md` | Cost per model per second with scenarios | Budget planning and cost optimization |
| `./references/prompt-guide.md` | Video prompt engineering best practices | Writing effective video prompts |
| `./references/camera-vocabulary.md` | Camera movement and angle terminology | Cinematic prompt construction |
| `./references/style-keywords.md` | Visual style keyword reference | Style consistency across scenes |
| `./references/story-schema.md` | JSON schema for story.json structure | Story decomposition validation |
| `./references/scene-schema.md` | JSON schema for scene objects | Scene data structure validation |
| `./references/shot-schema.md` | JSON schema for shot objects | Shot-level metadata validation |
| `./references/character-schema.md` | JSON schema for character objects | Character definition validation |
| `./references/consistency-guide.md` | Visual consistency techniques across scenes | Multi-scene project quality |
| `./references/cost-reference.md` | Cost estimation for project mode workflows | Project budget planning |
| `./references/model-selection.md` | Model selection guide for project mode | Choosing optimal models per scene |
| `./references/prompt-assembly.md` | How prompts are assembled from components | Understanding prompt construction |
| `./prompts/enhance-animated.md` | LLM prompt template for animation enhancement | Animated content optimization |
| `./prompts/enhance-cinematic.md` | LLM prompt template for cinematic enhancement | Film-quality content optimization |
| `./prompts/enhance.md` | General LLM prompt enhancement template | General prompt improvement |
| `./prompts/decompose.md` | LLM prompt template for story decomposition | Story-to-scenes breakdown |