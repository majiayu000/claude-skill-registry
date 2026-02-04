---
name: invokeai-image-gen
description: Generate images using InvokeAI's local API. Use when asked to generate, create, or make images with InvokeAI, FLUX.2 Klein, Z-Image Turbo, FLUX, or SDXL models. Supports text-to-image generation, automatic model detection, image download, and parameter selection based on model architecture.
# model: inherit
# context: fork
# user-invocable: true
# allowed-tools: Read,Bash
---

# InvokeAI Image Generation

Generate images via InvokeAI's REST API. Supports FLUX.2 Klein (default), Z-Image Turbo, FLUX.1, and SDXL.

## Quick Start

Simply call the script with your prompt and the output file name:

```bash
python scripts/generate.py -p "A dramatic sunset over snow-capped mountains, warm orange light reflecting off a still alpine lake in the foreground. Soft clouds catch the fading light." -o sunset.png
```

## Overriding The Default Model

If the user asks you to use a specific model, first find the model key, then use it in the command:

```bash
python scripts/generate.py --list-models | grep -i 'flux'

python scripts/generate.py -p "A tabby cat with bright green eyes sits on a weathered wooden windowsill, soft afternoon light streaming through lace curtains. Cosy, intimate mood." --model MODEL_KEY -o cat.png
```

## Options

| Option | Description |
|--------|-------------|
| `--prompt, -p` | Generation prompt (required) |
| `--negative, -n` | Negative prompt (SDXL only) |
| `--model, -m` | Model key (UUID) or partial name match |
| `--width, -W` / `--height, -H` | Dimensions |
| `--steps, -s` | Denoising steps |
| `--cfg, -c` | CFG scale |
| `--guidance, -g` | Guidance strength (FLUX.1 only) |
| `--scheduler` | Sampling scheduler |
| `--seed` | Random seed |
| `--output, -o` | Output path (default: invokeai-{seed}.png) |
| `--list-models` | List installed models |
| `--json` | JSON output |

## Model Defaults

Note: FLUX.2 Klein is the latest model which is used by default.

| Model | Steps | Guidance | CFG | Scheduler |
|-------|-------|----------|-----|-----------|
| FLUX.2 Klein | 4 | 3.5 | 1.0 | euler |
| Z-Image Turbo | 9 | - | 1.0 | euler |
| **FLUX.1 dev** | 28 | 3.5 | 1.0 | euler |
| **FLUX.1 Krea dev** | 28 | 4.5 | 1.0 | euler |
| **FLUX.1 Kontext dev** | 28 | 2.5 | 1.0 | euler |
| **FLUX.1 schnell** | 4 | 0.0 | 1.0 | euler |
| SDXL | 25 | - | 6.0 | dpmpp_2m_k |
| SDXL Turbo | 8 | - | 1.0 | dpmpp_sde |

All models default to 1024x1024. FLUX requires dimensions divisible by 16, SDXL by 8.

### FLUX.1 Variant Notes

- **FLUX.1 dev**: Standard text-to-image model, balanced quality/speed
- **FLUX.1 Krea dev**: Fine-tuned for aesthetic photography, use higher guidance (4.5)
- **FLUX.1 Kontext dev**: Image editing model, use lower guidance (2.5)
- **FLUX.1 schnell**: Distilled fast model, 4 steps, no guidance needed

## Model Selection

Auto-priority: Klein > Z-Image > FLUX > SDXL

Detection by name/base:
- **flux2_klein**: "klein" in name or "flux2" in base
- **flux_krea**: "krea" in name (FLUX.1 base)
- **flux_kontext**: "kontext" in name (FLUX.1 base)
- **flux_schnell**: "schnell" in name (FLUX.1 base)
- **flux**: "flux" in base (standard dev)
- **zimage**: "z-image" in base or "z-image/zimage" in name
- **sdxl**: "sdxl" in base (turbo/lightning variants auto-detect)

## Prompting (general information, but especially useful for FLUX.2 Klein)

Write prose, not keywords. Structure: **Subject -> Setting -> Details -> Lighting -> Atmosphere**

```
A weathered fisherman in his late sixties stands at the bow of a wooden boat,
wearing a salt-stained wool sweater. Golden hour sunlight filters through
morning mist, creating quiet determination and solitude.
```

**Key techniques:**
1. Front-load critical elements (word order matters)
2. Specify lighting: source, quality, direction, temperature
3. Include sensory texture: materials, reflections, atmosphere

**Good:** "A woman with short blonde hair poses against a light neutral background wearing colourful earrings, resting her chin on her hand."

**Bad:** "woman, blonde, short hair, neutral background, earrings"

Append style tags: `Style: Country chic. Mood: Serene, romantic.`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Check InvokeAI is running |
| Model not found | Use `--list-models` for valid keys |
| Dimensions error | FLUX: multiples of 16, SDXL: 8 |
| Black images (macOS) | Set `precision: bfloat16` in invokeai.yaml |

If the script fails to find the URL or authentication token, you can set or ask the user to set environment variables:

```bash
export INVOKEAI_API_URL='http://localhost:9090'
export INVOKEAI_AUTH_TOKEN='your-token'  # Optional
```

## Resources

- `scripts/generate.py` - Main generation script
