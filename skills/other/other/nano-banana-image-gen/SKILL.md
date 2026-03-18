---
name: nano-banana-image-gen
description: Use when generating images with Gemini models, choosing between Nano Banana 1/2/Pro, optimizing image generation costs, writing image prompts, or needing visual grounding with real-world reference images
---

# Nano Banana 2 image generation reference

Nano Banana (NB) is Google's Gemini image generation family. NB2 = Gemini 3.1 Flash.

## Model selection

| Model | Best for | Tradeoffs |
|-------|----------|-----------|
| NB1 | Existing workflows that already work, lowest cost, speed-critical | No thinking, no visual grounding, no extreme ratios |
| NB2 | Default for new projects (~95% of Pro quality) | ~15% slower than Pro at 2K, weaker arm/leg composition, spelling errors in infographics |
| Pro | Complex multi-layered prompts, extreme logical constraints, interior scale/logic | Most expensive |

**Decision:** Start with NB2. Step up to Pro only if NB2 consistently fails your specific prompt.

## Visual grounding (NB2 only)

NB2 searches the internet for reference images before generating. Useful for:
- Specific real-world locations (churches, bridges, city squares, niche buildings)
- Exact animal species, breeds, insects
- Historically accurate scenes

Example: "Generate a cinematic, golden-hour photograph of the main historical church in Voiron, France. Ensure the architectural details, the spire, the surrounding square, and the landscape (mountains) are accurate to reality."

## Cost optimization

**512px batch-to-upscale workflow:**
1. Use Batch API (50% discount) to generate dozens of 512px variations
2. Review and pick the best composition
3. Upscale that image to 1K/2K/4K

512px output runs faster and costs roughly the same as NB1.

## Parameters

| Parameter | Values | Notes |
|-----------|--------|-------|
| Resolution | 512px, 1K, 2K, 4K | 512px for drafts, upscale winners |
| Aspect ratio | Standard + 1:4, 1:8, 4:1, 8:1 | Extreme ratios for banners, comics, scrolling |
| Thinking mode | On/Off | Keep OFF by default. Enable for complex infographics or grounding + spatial reasoning |

## Prompt recipes

**3D character selfie** (requires image upload): Transform personal photos into stylized 3D characters interacting with real selves.

**Anime to photorealistic** (requires image upload): "Convert this uploaded animated still into an ultra-realistic, cinematic, and fully photorealistic scene. Transform the animated characters into real humans while perfectly preserving their original identities, facial structures, outfits, expressions, and overall likeness."

**Historical street view**: "Generate a hyper-realistic image of [event] perfectly replicating a Google Maps Street View capture. Include a 123-degree wide-angle barrel distortion..."

**Crayon filter**: "A child's crayon drawing on white lined notebook paper of [subject]. Use chunky wax-crayon strokes, wobbly outlines, and bright bold colors that messily overflow the lines. Include visible heavy pressure marks, waxy smudges, and uneven scribble shading."

**Comic strip**: "Create a 4-panel horizontal comic strip (aspect ratio 4:1). [Story]. Use a vibrant, Franco-Belgian comic book style. Keep the [character] design consistent across all panels."

## Known limitations

- Spelling mistakes in infographics (NB1 was better at this)
- Consistency across multiple generations is weaker than Pro
- Arm/leg composition issues more frequent than other models
- Knowledge cutoff prevents referencing very recent products even with search on
- No seed value support yet (style changes between generations)

## Attribution

Based on ["Getting the most out of Nano Banana 2"](https://x.com/AINanoBanana) by [@NanoBanana](https://x.com/AINanoBanana) on X (Mar 11, 2026). Original thread covers model comparisons, visual grounding, parameters, and prompt techniques for Google's Gemini image generation models.
