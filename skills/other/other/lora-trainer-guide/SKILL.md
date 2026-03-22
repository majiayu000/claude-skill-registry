---
name: lora-trainer-guide
description: Use when helping users configure LoRA training — select presets, understand parameters, and pick the right settings for their model type. Covers SD1.5, SDXL, SD3, and Flux1 with real-world presets.
---

# LoRA Trainer Guide

## Overview

Help users pick the right training configuration and understand what the parameters actually do. Ships with 38 real-world presets covering SD1.5, SDXL, SD3, and Flux1 — standard LoRA, LyCORIS variants (LoHA, LoKR, LoCon, iA3), finetuning, and dreambooth.

The presets live in the `presets/` folder as JSON files. They're directly usable with Kohya SS, sd-scripts, and the Ktiseos-Nyx-Trainer.

## When to Use

- User wants to train a LoRA and needs help picking settings
- User has a preset and wants to understand what the params mean
- User is troubleshooting training results ("my outputs look fried, what do I change?")
- User wants to compare LoRA types (standard vs LoHA vs LoKR etc.)

## Opening Behavior

**Always start by asking:** "How familiar are you with LoRA training?"

Adjust your responses based on their answer:
- **New to it** — explain concepts, define terms, walk them through choices step by step
- **Done it a few times** — skip basics, focus on "which preset fits your use case" and key params to tweak
- **Experienced** — be concise, jump straight to recommendations, reference specific params

## Preset Selection Flow

Walk the user through these questions to find the right preset:

### 1. What model architecture?

| Architecture | Resolution | Key differences |
|-------------|-----------|-----------------|
| SD 1.5 | 512x512 | Oldest, most presets available, clip_skip=2 common |
| SDXL | 1024x1024 | Dual text encoder, needs `sdxl: true`, more VRAM |
| SD3 | Varies | Newer architecture, limited preset support |
| Flux1 | 512x512+ | Requires fp8, T5 text encoder, different LoRA type |

### 2. What training type?

| Type | Use when | File size | Flexibility |
|------|----------|-----------|-------------|
| Standard LoRA | General purpose, good balance of quality and size | Medium | High |
| LoHA | Easier concepts, multi-concept, want better generalization | Medium | Very high |
| LoKR (small, factor=-1) | Want tiny file size (<2.5MB) | Very small | Lower (model-specific) |
| LoKR (large, factor~8) | Want LoRA-like quality with Kronecker math | Medium-large | High |
| LoCon | Need convolution layer training specifically | Medium | Medium |
| iA3 | Style learning, want ultra-tiny files (<1MB) | Tiny | Low (hard to transfer) |
| Finetune | Full model training, best possible quality | Very large | Highest |
| Dreambooth | Subject-specific training | Very large | High |

### 3. Recommend a preset

Filter the `presets/` folder by `model_type` and `LoRA_type` from the JSON files. Each preset has this structure:

```json
{
  "name": "Human-readable name",
  "description": "What this preset is optimized for",
  "model_type": "SDXL",
  "config": {
    "LoRA_type": "Standard",
    "optimizer": "AdamW8bit",
    "network_dim": 32,
    "network_alpha": 32,
    "learning_rate": 0.0001,
    ...
  }
}
```

Present matching presets as numbered options with a brief explanation of what makes each one different (usually the optimizer and dim/alpha choices).

## What to Tweak

After selecting a preset, highlight the params the user is most likely to want to adjust. Don't dump every parameter — focus on what actually matters.

### Always worth checking

| Parameter | What it does | Typical range | Watch out for |
|-----------|-------------|---------------|---------------|
| `network_dim` | LoRA rank — higher = more expressive, bigger file | 8–128 | Higher isn't always better; 32 is a solid default |
| `network_alpha` | Scales the learning rate relative to dim | 1 to same-as-dim | alpha=1 vs alpha=dim behave VERY differently — see pitfalls |
| `learning_rate` | How fast the model learns | 1e-5 to 1e-3 | Depends heavily on optimizer choice |
| `train_batch_size` | Images per step | 1–8 | Higher = more VRAM, may need to adjust LR |
| `max_train_epochs` / `max_train_steps` | When to stop | Varies | More isn't better — watch for overtraining |
| `optimizer` | Learning algorithm | See reference.md | Each optimizer wants different LR ranges |
| `save_every_n_epochs` | Checkpoint frequency | 1–5 | Save often so you can pick the best epoch |

### Per-architecture specifics

**SD 1.5:**
- `clip_skip`: usually 2 for anime models, 1 for realistic
- `max_resolution`: 512,512
- `mixed_precision`: fp16 or bf16

**SDXL:**
- `sdxl`: must be `true`
- `max_resolution`: 1024,1024
- `sdxl_no_half_vae`: usually `true` (prevents NaN)
- `clip_skip`: usually 1
- Consider `min_snr_gamma`: 5 helps stabilize training

**Flux1:**
- `fp8_base`: must be `true` (Flux needs fp8)
- `flux1_checkbox`: `true`
- `LoRA_type`: must be "Flux1"
- `t5xxl_max_token_length`: 512
- `timestep_sampling`: "sigmoid"
- `discrete_flow_shift`: 3
- `model_prediction_type`: "raw"
- Cache text encoder outputs to disk (saves VRAM)

## Common Pitfalls

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| Loss goes NaN | LoHA + high dim, or LR too high | Lower LR, reduce dim, or switch to LoRA |
| Output looks nothing like training data | Undertrained or LR too low | More epochs, higher LR, check captions |
| Output is copy-paste of training images | Overtrained | Fewer epochs, lower dim, use an earlier checkpoint |
| Style bleeds into everything | Model learned style too hard | Use LoHA (dampens style), lower dim, add regularization images |
| Colors are washed out / wrong | VAE issues on SDXL | Set `sdxl_no_half_vae: true` |
| Flux training OOMs immediately | Not using fp8 | Set `fp8_base: true`, cache text encoder outputs |
| alpha=1 trains differently than expected | alpha scales effective LR | alpha=1 with dim=32 means effective LR is multiplied by 1/32. Set alpha=dim for "normal" behavior, or adjust LR accordingly |
| Increasing batch size makes results worse | LR wasn't scaled | When you increase batch size, increase LR proportionally |

## See Also

- `reference.md` in this skill folder — full parameter definitions, algorithm comparison tables, optimizer reference
- Presets are in `presets/` — each is a self-contained JSON file ready to load
