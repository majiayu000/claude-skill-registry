---
name: ai-video-production-master
description: Expert in script-to-video production pipelines for Apple Silicon Macs. Specializes in hybrid local/cloud workflows, LoRA training for character consistency, motion graphics generation, and artist commissioning. Activate on 'AI video production', 'script to video', 'video generation pipeline', 'character consistency', 'LoRA training', 'cloud GPU', 'motion graphics', 'Wan I2V', 'InVideo alternative'. NOT for real-time video editing, video compositing (use DaVinci/Premiere), audio production, or 3D modeling (use Blender/Maya).
allowed-tools: Read,Write,Edit,Bash(python:*,ffmpeg:*,npm:*),WebFetch,mcp__firecrawl__firecrawl_search
category: AI & Machine Learning
tags:
  - video
  - ai-generation
  - lora
  - cloud-gpu
  - motion-graphics
  - comfyui
pairs-with:
  - skill: sound-engineer
    reason: Audio for AI-generated videos
  - skill: voice-audio-engineer
    reason: Voice synthesis for narration
---

# AI Video Production Master

Expert in script-to-video production pipelines for Apple Silicon Macs. Specializes in:
- **Multiple video approaches**: Stock footage, T2V (Sora-style), I2V, hybrid
- Hybrid local/cloud workflows for cost optimization
- Style and character consistency (LoRA, IPAdapter, prompt discipline)
- Motion graphics and synthetic elements (title cards, data viz, lower thirds)
- Artist commissioning for training datasets
- Cloud GPU orchestration (Vast.ai, RunPod)

## When to Use

✅ **USE this skill for:**
- Script-to-video production pipelines
- Stock footage assembly (InVideo-style workflows)
- Text-to-video generation (Sora, Runway, Pika, Kling)
- Image-to-video animation (Wan I2V, ComfyUI)
- Cloud GPU orchestration (Vast.ai, RunPod, Lambda)
- Motion graphics generation (title cards, lower thirds, data viz)
- LoRA training for character/style consistency
- Artist commissioning for training datasets
- Cost optimization between local and cloud processing

❌ **DO NOT use for:**
- Real-time video editing → use DaVinci Resolve, Premiere Pro
- Video effects/compositing → use After Effects, Fusion
- Audio production/mixing → use `sound-engineer` skill
- 3D modeling/animation → use Blender, Maya, or `physics-rendering-expert` skill
- Static image generation → use `clip-aware-embeddings` or image gen tools

## Video Generation Approaches

Choose the right approach based on your content:

### Stock Footage (Invideo-style) - RECOMMENDED for most content
Best for: Educational, corporate, explainers, documentaries
- Uses curated stock libraries (Pexels, Pixabay, Storyblocks)
- Most professional, reliable results
- Fast turnaround (~30 min for full video)
- Script → AI selects matching clips → voiceover + music
```bash
python scripts/stock_video_generator.py --script script.txt --style documentary
```

### Text-to-Video (Sora-style) - For creative/artistic content
Best for: Abstract visuals, creative shorts, unique scenes
- True generative AI (no stock footage)
- Uses: Sora API, Runway Gen-3, Pika, Kling
- Cleaner than I2V (no weird image artifacts)
- Storyboard control for multi-shot narratives
```bash
python scripts/t2v_generator.py --prompt "A serene mountain lake at sunset" --provider sora
```

### Image-to-Video (I2V) - For animating specific images
Best for: Animating logos, concept art, specific compositions
- Animates existing images with subtle motion
- Can look "weird" if source images are AI-generated
- Best with clean, professional source images
```bash
python scripts/cloud_i2v_batch.py --images ./keyframes --provider vastai
```

### Hybrid Approach
Combine approaches per shot:
- Shot 1-3: Stock footage (b-roll, establishing)
- Shot 4-5: T2V (creative transitions)
- Shot 6-10: Stock footage (talking head, outro)

## Key Capabilities

### 1. Cost Optimization
Compare and recommend the optimal mix of local (M4 Max) vs cloud (H100/A100) processing:
```bash
python scripts/cost_calculator.py --shots 10 --duration 5
```

### 2. Cloud Batch Processing
Run I2V generation on cloud GPUs for 50x speedup:
```bash
python scripts/cloud_i2v_batch.py --images ./keyframes --provider vastai
```

### 3. Motion Graphics Generation
Create professional title cards, lower thirds, and data visualizations:
```bash
python scripts/motion_graphics_generator.py --type title --style deep_glow --title "Your Title"
```

### 4. Style Consistency
Provide guidance on:
- LoRA training parameters (rank, alpha, learning rate, steps)
- IPAdapter + FaceID for character consistency
- Prompt discipline and trigger words
- Reference image workflows

### 5. Artist Commissioning
Templates and guidance for:
- Finding artists (ArtStation, Fiverr, Upwork)
- Structuring commission requests
- AI training rights contracts
- Quality control and review processes

## Files in This Skill

```
ai-video-production-master/
├── README.md                          # Comprehensive guide
├── SKILL.md                           # This file
├── scripts/
│   ├── cost_calculator.py             # Cost comparison tool
│   ├── cloud_i2v_batch.py             # Cloud batch I2V (Vast.ai/RunPod)
│   ├── stock_video_generator.py       # Stock footage assembly (Invideo-style)
│   ├── t2v_generator.py               # Text-to-video (Sora/Runway/Pika)
│   └── motion_graphics_generator.py   # Title cards, lower thirds
├── workflows/
│   └── comfyui_i2v_optimized.json     # Optimized ComfyUI workflow
└── docs/
    ├── ARTIST_COMMISSIONING_GUIDE.md  # Hiring artists
    └── contracts/
        └── artist_commission_template.md  # Contract template
```

## Quick Reference

### Cost Comparison (10-shot video)
| Approach | Time | Cost | Best For |
|----------|------|------|----------|
| Stock Footage + AI | 30 min | Free-$20/mo | Educational, corporate |
| Sora (ChatGPT Plus) | 30 min | $20/mo | Creative, unique scenes |
| Full Local I2V (M4 Max) | 15+ hours | $0 | When you need specific images |
| Cloud I2V (RTX 4090) | 30 min | ~$0.50 | Batch I2V processing |
| InVideo Max | 30 min | $48/mo | Full automation |
| Runway Gen-3 | 30 min | ~$15-25 | High-quality T2V |

### Cloud GPU Pricing
| Provider | GPU | $/hr | I2V Time/Clip |
|----------|-----|------|---------------|
| Vast.ai | H100 80GB | $1.87 | ~2 min |
| RunPod | H100 80GB | $1.99 | ~2 min |
| RunPod | A100 80GB | $1.74 | ~3 min |
| Lambda | H100 | $2.99 | ~2 min |

### Motion Graphics Styles
- `neo_brutalist` - Raw, glitchy, utilitarian
- `deep_glow` - Intense light blooms, layered neons
- `liquid_motion` - Fluid, morphing typography
- `retro_revival` - 80s/90s grain and neon
- `glass_morphism` - Frosted glass, depth layers

## Dependencies

Python packages:
- httpx (for cloud API calls)
- argparse, json, subprocess (stdlib)

External tools:
- FFmpeg (video encoding)
- rsvg-convert or ImageMagick (SVG to PNG)
- ComfyUI (local generation)
