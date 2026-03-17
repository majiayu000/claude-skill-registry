---
name: meshy
description: "Generate 3D models via the Meshy API. Supports text-to-3D (preview + refine pipeline), image-to-3D, text-to-texture, task management, model downloads, and batch generation from JSON manifests. Use this skill when creating 3D assets from text prompts, converting images to 3D models, texturing existing models, running batch 3D generation pipelines, or checking Meshy account balance."
---

# Meshy 3D Model Generation

Generate 3D models from text prompts, images, or apply textures to existing models via the Meshy API.

## Prerequisites

```bash
# API key in environment (already in ~/.config/env/secrets.env)
export MESHY_API_KEY="msy_xxx"
```

Get your API key at: https://www.meshy.ai/settings/api

## Quick Start

### Test Connection

```bash
uv run ~/.claude/skills/meshy/scripts/test_meshy.py --quick
```

### Generate a Model

```bash
uv run ~/.claude/skills/meshy/scripts/meshy_text_to_3d.py "a stealth fighter jet, delta wings" \
  --model-type lowpoly --format glb --output ./models
```

### Check Balance

```bash
uv run ~/.claude/skills/meshy/scripts/meshy_tasks.py balance
```

## Core Workflows

### 1. Text-to-3D Generation

Two-stage pipeline: Preview (geometry, ~2 min) then optional Refine (PBR textures, ~5 min).

```bash
# Full pipeline (preview + refine)
uv run ~/.claude/skills/meshy/scripts/meshy_text_to_3d.py \
  "a nuclear submarine, teardrop hull, conning tower" \
  --model-type lowpoly --filename submarine

# Preview only (saves credits)
uv run ~/.claude/skills/meshy/scripts/meshy_text_to_3d.py \
  "a red cube, game ready" --skip-refine --filename cube
```

### 2. Image-to-3D

```bash
# From local file
uv run ~/.claude/skills/meshy/scripts/meshy_image_to_3d.py ./reference.png --filename tank

# From URL
uv run ~/.claude/skills/meshy/scripts/meshy_image_to_3d.py https://example.com/photo.jpg
```

### 3. Text-to-Texture

```bash
uv run ~/.claude/skills/meshy/scripts/meshy_texture.py \
  https://cdn.meshy.ai/.../model.glb \
  --prompt "Military olive drab paint, worn metal, tactical" --enable-pbr
```

### 4. Batch Generation from Manifest

For generating multiple models (e.g., all 11 World War Watcher ordnance types):

```bash
# Generate all models from manifest
uv run ~/.claude/skills/meshy/scripts/meshy_batch.py manifest.json --output ./staging/

# Generate specific models only
uv run ~/.claude/skills/meshy/scripts/meshy_batch.py manifest.json --models fighter carrier

# Inspect manifest
uv run ~/.claude/skills/meshy/scripts/meshy_batch.py manifest.json --list
uv run ~/.claude/skills/meshy/scripts/meshy_batch.py manifest.json --dry-run

# Check status of last batch run
uv run ~/.claude/skills/meshy/scripts/meshy_batch.py manifest.json --status
```

### 5. Task Management

```bash
uv run ~/.claude/skills/meshy/scripts/meshy_tasks.py list                     # recent tasks
uv run ~/.claude/skills/meshy/scripts/meshy_tasks.py get TASK_ID              # task detail
uv run ~/.claude/skills/meshy/scripts/meshy_tasks.py get TASK_ID --watch      # poll until done
uv run ~/.claude/skills/meshy/scripts/meshy_tasks.py download TASK_ID         # download GLB
uv run ~/.claude/skills/meshy/scripts/meshy_tasks.py balance                  # credit balance
```

## Script Reference

### meshy_text_to_3d.py

| Flag | Default | Description |
|------|---------|-------------|
| `PROMPT` | required | Text description of 3D model |
| `--negative-prompt` | `""` | What to avoid |
| `--model-type` | `lowpoly` | `standard` / `lowpoly` / `ai_model` |
| `--skip-refine` | `False` | Preview only (saves credits) |
| `--enable-pbr` / `--no-pbr` | `True` | PBR textures in refine |
| `--format` | `glb` | `glb` / `gltf` / `usdz` / `fbx` |
| `--output` | `./output` | Output directory |
| `--filename` | derived | Output filename (no extension) |
| `--api-key` | env | Override MESHY_API_KEY |
| `--poll-interval` | `5` | Seconds between polls |
| `--timeout` | `600` | Max wait seconds |
| `--quiet` / `--json` | — | Output modes |

### meshy_image_to_3d.py

Same flags minus `--negative-prompt`, `--skip-refine`, `--enable-pbr`. Accepts local path (auto base64-encodes) or URL.

### meshy_texture.py

| Flag | Default | Description |
|------|---------|-------------|
| `MODEL_URL` | required | URL of existing 3D model |
| `--prompt` | required | Texture description |
| `--negative-prompt` | `""` | What to avoid |
| `--art-style` | `""` | Art style hint |
| `--enable-pbr` / `--no-pbr` | `True` | PBR textures |

### meshy_tasks.py

Subcommands: `list`, `get`, `download`, `balance`. All accept `--json`.

### meshy_batch.py

| Flag | Default | Description |
|------|---------|-------------|
| `MANIFEST` | required | Path to JSON manifest file |
| `--models` | all | Generate specific model IDs only |
| `--list` | — | List IDs and prompts |
| `--dry-run` | — | Preview without API calls |
| `--status` | — | Check last batch run status |
| `--skip-refine` | `False` | Override: preview only for all |
| `--output` | manifest | Override output directory |

## Batch Manifest Format

```json
{
  "version": 1,
  "defaults": {
    "model_type": "lowpoly",
    "skip_refine": false,
    "format": "glb",
    "enable_pbr": true,
    "output_dir": "./output"
  },
  "models": [
    {
      "id": "fighter",
      "prompt": "a modern stealth fighter jet, delta wings...",
      "negative_prompt": "organic, blurry...",
      "output_name": "fighter.glb"
    }
  ]
}
```

Per-model fields override `defaults`. Required per-model: `id`, `prompt`.

## World War Watcher Integration

```bash
cd ~/Desktop/Programming/worldwarwatcher

# Generate all 11 tactical models
uv run ~/.claude/skills/meshy/scripts/meshy_batch.py \
  scripts/models-manifest.json \
  --output scripts/models-staging/ \
  --quiet

# DRACO compress and deploy to public/models/
bash scripts/prepare-models.sh

# Verify in dev server
npm run dev
```

## Credit Costs

| Operation | Credits |
|-----------|---------|
| Text-to-3D Preview | ~5 |
| Text-to-3D Refine | ~10 |
| Image-to-3D | ~10 |
| Text-to-Texture | ~10 |

## DRACO Post-Processing

For web deployment, DRACO-compress GLBs to reduce file size 80-90%:

```bash
npx gltf-pipeline -i model.glb -o model-draco.glb -d --draco.compressionLevel 7
```

World War Watcher's `scripts/prepare-models.sh` automates this for all staged models.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `401 Unauthorized` | Check MESHY_API_KEY is set and valid |
| `429 Rate Limited` | Increase `--poll-interval`, wait between batch models |
| `Insufficient credits` | Check `meshy_tasks.py balance`, top up at meshy.ai |
| `Task FAILED` | Check task error via `meshy_tasks.py get TASK_ID` |
| `Timeout` | Increase `--timeout` (refine can take 10+ min) |
| `No GLB URL` | Task may not be complete, or format unavailable |

## API Reference

See `references/api-reference.md` for full Meshy v2 endpoint documentation.
