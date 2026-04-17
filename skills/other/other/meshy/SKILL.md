---
name: meshy
description: "Generate 3D models from text or images via 5 providers: Meshy (text-to-3D, texturing, batch), fal.ai Hunyuan3D Pro ($0.225, PBR), WaveSpeedAI Rapid ($0.0225, bulk), Trellis 2 (poly control), and Local Depth (free offline ONNX depth maps + mesh). Includes GLB viewer. Triggers on 3D model, image to 3D, GLB, depth map, text to 3D, texturing, 3D asset, Meshy, Hunyuan."
---

# 3D Model Generation (Multi-Provider)

Generate 3D models from text prompts, images, or apply textures to existing models. Four providers with different cost/quality tradeoffs.

## Provider Selection

| Provider | Script | Cost | Speed | Best for |
|----------|--------|------|-------|----------|
| **Meshy** (default) | `meshy_text_to_3d.py`, `meshy_image_to_3d.py` | 5-20 credits | 2-7 min | Text-to-3D, texturing, low-poly game assets, batch |
| **fal.ai Hunyuan3D** | `fal_hunyuan3d.py` | $0.225 | ~2 min | High-fidelity image-to-3D with PBR, text-to-3D |
| **WaveSpeedAI Rapid** | `wavespeed_rapid.py` | $0.0225 | ~1 min | Bulk iteration, concept validation (16x cheaper) |
| **Trellis 2** | `trellis2.py` | 15-55 credits | 30s-4 min | Precise poly count control, geometry-only fast runs |
| **Local Depth** | `depth_local.py` | Free | ~5s | Offline depth maps, local mesh gen, preprocessing |

**Decision guide:**
- Quick concept check → WaveSpeedAI ($0.02, fastest)
- Production image-to-3D → fal.ai Hunyuan3D (best PBR quality)
- Text-to-3D → Meshy (only provider with text prompt support + refine pipeline)
- Specific poly budget → Trellis 2 (`--decimation 5000` for low-poly)
- Batch generation → Meshy (`meshy_batch.py` with manifest)
- Free offline depth/mesh → Local Depth (zero API cost, ONNX on-device)
- Depth map as preprocessing → Local Depth + any cloud provider for texturing

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

## Alternative Providers

For full flags, API contracts, and credit costs, see the corresponding reference file:

- **fal.ai Hunyuan3D** → `references/fal-hunyuan3d.md` (credential: `FAL_KEY`)
- **WaveSpeedAI Rapid** → `references/wavespeed-rapid.md` (credential: `WAVESPEED_API_KEY`)
- **Trellis 2** → `references/trellis2.md` (credential: `THREEDAI_API_KEY`)
- **Local Depth** → `references/depth-local.md` (no credential needed — free, local ONNX inference)

All three accept local file paths (auto base64-encoded) or URLs. Run any script with `--help` for flags.

## GLB Viewer

Museum-quality standalone Three.js viewer for previewing generated .glb models. Open in browser — no server needed.

```bash
# Open with a model URL
open ~/.claude/skills/meshy/assets/glb-viewer.html?glb=https://cdn.example.com/model.glb

# Or drag-and-drop a local .glb file onto the page
open ~/.claude/skills/meshy/assets/glb-viewer.html
```

Features: 7-light PBR gallery rig, bloom/vignette post-processing, SMAA, auto-rotate with graceful pause, ground plane with shadow catcher.

Keyboard: `D` download, `R` toggle rotation, `F` fullscreen.

## API Reference

See `references/api-reference.md` for full Meshy v2 endpoint documentation.
