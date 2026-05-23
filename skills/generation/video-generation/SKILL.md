---
name: video-generation
description: AI video generation with Sora, Veo, and Kling. Use when creating Reels, video prompts, or handling video generation workflows.
---

# AI Video Generation

## Quick Reference

| Model | Provider | Duration | Best For |
|-------|----------|----------|----------|
| Veo 3.1 | Google | 4-8s | Simple scenes, products |
| Sora 2 | OpenAI | 4-12s | Complex scenes |
| Kling Pro | fal.ai | 5-10s | Industrial, IoT |

## Model Selection

```python
# Auto-select based on complexity
from app.sora_helper import generate_video_smart

result = await generate_video_smart(prompt, topic, duration=8)
# Returns: {success, video_path, model_used}
```

**Complexity Keywords:**
- HIGH (Sora Pro): transformation, morphing, cinematic, epic
- MEDIUM (Sora): tracking, dolly, movement, transition
- LOW (Veo): static, simple, product

## Prompt Formula

```
[CINEMATOGRAPHY] + [SUBJECT] + [ACTION] + [CONTEXT] + [STYLE]
```

**Example:**
```
Slow dolly shot, IoT sensor on greenhouse shelf, LED blinking green,
morning sunlight through glass, professional documentary style
```

## Generation Functions

```python
# Veo (Google)
from app.veo_helper import generate_video_veo3
result = await generate_video_veo3(prompt, aspect_ratio="9:16", duration_seconds=8)

# Sora (OpenAI)
from app.sora_helper import generate_video_sora
result = await generate_video_sora(prompt, model="sora-2", size="720x1280")

# Kling (fal.ai)
from app.fal_helper import FalVideoGenerator
result = await FalVideoGenerator.generate_video(prompt, model="kling_pro", duration=10)
```

## Instagram Specs

| Spec | Value |
|------|-------|
| Aspect | 9:16 vertical |
| Resolution | 720x1280 |
| Codec | H.264/AAC |
| Max Duration | 90s |

## Environment Variables

```bash
GEMINI_API_KEY=...   # Veo
OPENAI_API_KEY=...   # Sora
FAL_API_KEY=...      # Kling
```

## Return Format

```python
# Success
{"success": True, "video_path": "/path/to.mp4", "model_used": "veo-3.1"}

# Error with fallback
{"success": False, "error": "...", "fallback": "veo3"}
```

## Best Practices

- Simple, comma-separated sentences
- Include camera movement + lighting
- Avoid complex physics (bouncing, running)
- Use: "cinematic", "professional", "documentary"
- Duration: 5-8s ideal for Reels

## Deep Links

- `app/sora_helper.py` - Sora + smart selection
- `app/veo_helper.py` - Veo generation
- `app/fal_helper.py` - Kling/Wan/Minimax
- `app/video_models.py` - Model configs
- `context/reels-prompts.md` - Prompt examples
