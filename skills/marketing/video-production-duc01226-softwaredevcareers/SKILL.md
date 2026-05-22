---
name: video-production
description: Activate for video marketing strategy, script writing, video specifications for YouTube/TikTok/Instagram Reels/LinkedIn, production workflows, video optimization, thumbnail creation, and video repurposing. Used by content-creator and social-media-manager agents.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Video Production

Video marketing strategy, scripting, AI video generation, and platform optimization.

## When to Use

- Video strategy planning
- Script writing for any format
- Storyboard creation
- AI video generation (Veo 3.1)
- Platform specifications lookup
- Production workflow guidance
- Video optimization
- Thumbnail creation
- Video repurposing
- Caption extraction

## Setup

This skill leverages the `ai-multimodal` skill for Veo/Imagen APIs. Ensure:

```bash
export GEMINI_API_KEY="your-key"  # Get from https://aistudio.google.com/apikey
pip install google-genai python-dotenv pillow
```

## Quick Start

**Generate video**: `node scripts/generate-video.cjs --prompt "product demo" --template product-demo`
**Create storyboard**: `node scripts/create-storyboard.cjs --script "path/to/script.md"`
**Analyze video**: `node scripts/analyze-video.cjs --video "path/to/video.mp4"`
**Optimize for platform**: `node scripts/optimize-for-platform.cjs --video "path/to/video.mp4" --platform tiktok`
**Extract captions**: `node scripts/extract-captions.cjs --video "path/to/video.mp4"`

## Core Capabilities

### Video Types & Platform Specs
Load: `references/video-types-specs.md`

### Art Directions
Load: `references/video-art-directions.md`

### Script Templates
Load: `references/script-templates.md`

### Production Workflow
Load: `references/production-workflow.md`

### Video Optimization
Load: `references/video-optimization.md`

### Veo Prompt Engineering
Load: `references/veo-prompt-guide.md`

### Storyboard Format
Load: `references/storyboard-format.md`

### Audio Directives
Load: `references/audio-directive-guide.md`

### Thumbnail Design
Load: `references/thumbnail-design-guide.md`

### Video SEO
Load: `references/video-seo-optimization.md`

### Quality Review Workflow
Load: `references/quality-review-workflow.md`

## Scripts

| Script | Purpose |
|--------|---------|
| `generate-video.cjs` | Veo 3.1 wrapper with templates |
| `create-storyboard.cjs` | Imagen 4 storyboard generator |
| `analyze-video.cjs` | Gemini video understanding |
| `optimize-for-platform.cjs` | FFmpeg aspect ratio converter |
| `extract-captions.cjs` | Caption/transcript extraction |

## Templates

| Template | Use Case |
|----------|----------|
| `product-demo.json` | Product showcase videos |
| `explainer.json` | Educational/explainer videos |
| `testimonial.json` | Customer testimonial format |
| `short-form.json` | TikTok/Reels/Shorts format |

## Quick Reference

| Platform | Ratio | Ideal Length | Max |
|----------|-------|--------------|-----|
| YouTube | 16:9 | 8-15 min | 12h |
| YouTube Shorts | 9:16 | 30-60 sec | 3 min |
| TikTok | 9:16 | 15-60 sec | 60 min |
| Reels | 9:16 | 15-30 sec | 3 min |
| LinkedIn | 16:9 | 1-2 min | 10 min |

**Video Types:** Tutorial, Demo, Testimonial, BTS, Short-form, Explainer

## Video Pipeline (Frame-Based with Reviews)

Best quality workflow using start/end frames with AI-powered review gates:

```
1. SCRIPT (Gemini 2.5) → Scene timing with start/end frame descriptions
         ↓
   [REVIEW 1] → Grammar, timing, brand voice, hooks (Gemini text)
         ↓
2. STORYBOARD → Frame prompts with visual continuity
         ↓
   [REVIEW 2] → Prompt clarity, style consistency, feasibility (Gemini text)
         ↓
3. VOICEOVER (Gemini TTS) → Generate narration with voice control
         ↓
4. MUSIC (Lyria) → Generate background track with mood control
         ↓
   [REVIEW 3] → Audio clarity, pronunciation, mood match (Gemini audio)
         ↓
5. START/END FRAMES (Imagen 4) → Generate keyframes per scene
         ↓
   [REVIEW 4] → Quality, abnormalities, prompt adherence (Gemini vision)
         ↓
6. VIDEO (Veo 3.1) → Generate video between reference frames
         ↓
   [REVIEW 5] → Motion quality, artifacts, temporal consistency (Gemini video)
         ↓
7. MIX (FFmpeg) → Combine video + voiceover + music + SFX
         ↓
   [REVIEW 6] → A/V sync, transitions, overall polish (Gemini video)
         ↓
8. OPTIMIZE → Platform-specific versions
```

**Key**: Every step reviewed by AI before proceeding. Catches typos, abnormal actions, AI artifacts.

**Review capabilities from ai-multimodal**:
- Text analysis: Script grammar, timing validation
- Vision: Frame quality, abnormality detection (extra limbs, distorted faces)
- Video: Motion quality, temporal consistency, artifact detection
- Audio: Speech clarity, pronunciation errors, mood matching

**Time:** 25-35 min | **Cost:** $5-15/video + $0.12 reviews

## Workflow

### Planning
1. Define goal and audience
2. Choose video type and platform
3. Write script using templates
4. Create storyboard

### Production (AI-Generated)
1. Generate prompts from script
2. Generate video clips (Veo 3.1)
3. Review and iterate
4. Assemble scenes

### Post-Production
1. Optimize for target platform
2. Extract/add captions
3. Create thumbnail
4. Publish

## Output Format

```markdown
## Video Brief: [Title]

**Platform:** [YouTube/TikTok/etc.]
**Type:** [Tutorial/Demo/etc.]
**Length:** [Duration]
**Aspect Ratio:** [16:9/9:16/1:1]

### Script
[Scene-by-scene breakdown]

### Storyboard
[Key frames with timing]

### Veo Prompts
[Per-scene prompts]

### Visual Notes
[Shot descriptions]
```

## Best Practices

1. Hook in first 3 seconds
2. Design for sound-off (captions)
3. Strong thumbnail with faces
4. Clear CTA at end
5. Repurpose for multiple platforms
6. Use trending audio when applicable
7. Optimize title/description for SEO
8. A/B test thumbnails

## Cost Estimation

| Component | Cost |
|-----------|------|
| Veo 3.1 (2-4 clips) | $2-5 |
| Imagen 4 storyboard | $0.04-0.20 |
| Gemini API calls | $0.50-1.00 |
| **Per video** | **$3-6** |

## Integration

This skill works with:
- `ai-multimodal` - Video generation and analysis
- `creativity` - Creative direction, style templates, color psychology, voiceover styles
- `media-processing` - FFmpeg optimization
- `content-marketing` - Content strategy
- `social-media` - Distribution planning

## Resources

- [Veo API Docs](https://ai.google.dev/gemini-api/docs/video)
- [Imagen API](https://ai.google.dev/gemini-api/docs/imagen)
- [Platform Guidelines](https://support.google.com/youtube/answer/4603579)
