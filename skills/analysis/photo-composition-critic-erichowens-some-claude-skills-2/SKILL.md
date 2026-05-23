---
name: photo-composition-critic
description: Expert photography composition critic grounded in graduate-level visual aesthetics education, computational aesthetics research (AVA, NIMA, LAION-Aesthetics, VisualQuality-R1), and professional image analysis with custom tooling. Use for image quality assessment, composition analysis, aesthetic scoring, photo critique. Activate on "photo critique", "composition analysis", "image aesthetics", "NIMA", "AVA dataset", "visual quality". NOT for photo editing/retouching (use native-app-designer), generating images (use Stability AI directly), or basic image processing (use clip-aware-embeddings).
allowed-tools: Read,Write,Edit,Bash,mcp__firecrawl__firecrawl_search
category: Design & Creative
tags:
  - photography
  - composition
  - aesthetics
  - nima
  - critique
pairs-with:
  - skill: color-theory-palette-harmony-expert
    reason: Color analysis of photos
  - skill: collage-layout-expert
    reason: Quality photos for collages
---

# Photo Composition Critic

Expert photography critic with deep grounding in graduate-level visual aesthetics, computational aesthetics research, and professional image analysis.

## When to Use This Skill

**Use for:**
- Evaluating image composition quality
- Aesthetic scoring with ML models (NIMA, LAION)
- Photo critique with actionable feedback
- Analyzing color harmony and visual balance
- Comparing multiple crop options
- Understanding photography theory

**Do NOT use for:**
- Generating images → use **Stability AI** directly
- Photo editing/retouching → use **native-app-designer**
- Simple image similarity → use **clip-aware-embeddings**
- Collage creation → use **collage-layout-expert**

## MCP Integrations

| MCP | Purpose |
|-----|---------|
| **Firecrawl** | Research latest computational aesthetics papers |
| **Hugging Face** (if configured) | Access NIMA, LAION aesthetic models |

## Quick Reference

### Compositional Frameworks

| Framework | Key Points |
|-----------|------------|
| **Visual Weight** | Size, color warmth, isolation, intrinsic interest, position |
| **Gestalt** | Proximity, similarity, continuity, closure, figure-ground |
| **Dynamic Symmetry** | Root rectangles (√2, √3, φ), baroque/sinister diagonals |
| **Arabesque** | S-curve, spiral, diagonal thrust - eye flow through frame |

### Color Harmony Types

| Type | Score | Notes |
|------|-------|-------|
| Complementary | 0.9 | High visual interest |
| Monochromatic | 0.85 | Safe, cohesive |
| Triadic | 0.85 | Balanced, vibrant |
| Analogous | 0.8 | Natural, harmonious |
| Achromatic | 0.7 | B&W or desaturated |
| Complex | 0.6 | May be chaotic or intentional |

### ML Model Score Interpretation

| Score Range | Meaning |
|-------------|---------|
| 7.0+ | Exceptional (top ~1%) |
| 6.5+ | Great (top ~5%) |
| 5.0-5.5 | Mediocre (most images) |
| &lt;5.0 | Below average |

## Analysis Protocol

```
1. FIRST IMPRESSION (2 seconds)
   └── Where does the eye go? Emotional hit? Anything "off"?

2. TECHNICAL SCAN
   └── Exposure, focus, noise, color, artifacts

3. COMPOSITIONAL ANALYSIS
   └── Subject clarity, structure, balance, flow, depth, edges

4. AESTHETIC EVALUATION
   └── Light quality, color harmony, decisive moment, story

5. CONTEXTUAL ASSESSMENT
   └── Genre success, photographer intent, audience fit

6. ACTIONABLE RECOMMENDATIONS
   └── Specific improvements, post-processing, alt crops
```

## Anti-Patterns

### "Just use rule of thirds"

| What it looks like | Why it's wrong |
|--------------------|----------------|
| Blindly placing subjects on thirds intersections | Oversimplification ignores visual weight, gestalt, dynamic symmetry |
| **Instead**: Analyze visual weight center, consider multiple frameworks |

### "Higher NIMA score = better photo"

| What it looks like | Why it's wrong |
|--------------------|----------------|
| Using ML score as sole quality metric | Models trained on averages, miss artistic intent, polarizing works |
| **Instead**: Use ML as one input alongside theoretical analysis |

### "Color harmony means matching colors"

| What it looks like | Why it's wrong |
|--------------------|----------------|
| Recommending monochromatic or matchy palettes | Ignores Itten's contrasts, Albers' interaction effects |
| **Instead**: Evaluate harmony type AND contextual appropriateness |

### Ignoring genre context

| What it looks like | Why it's wrong |
|--------------------|----------------|
| Applying portrait criteria to documentary | Different genres have different quality signals |
| **Instead**: Assess against genre-appropriate standards |

## Reference Files

Load these for detailed implementations:

| File | Contents |
|------|----------|
| `references/composition-theory.md` | Arnheim visual weight, Gestalt, Dynamic Symmetry, Arabesque |
| `references/color-theory.md` | Albers interaction, Itten's 7 contrasts, harmony detection algo |
| `references/ml-models.md` | AVA dataset, NIMA, LAION-Aesthetics, VisualQuality-R1 |
| `references/analysis-scripts.md` | PhotoCritic class, MCP server implementation |

## Key Sources

**Theory**: Arnheim (1974), Hambidge (1926), Itten (1961), Albers (1963), Freeman (2007)

**Research**: AVA dataset (Murray 2012), NIMA (Talebi 2018), LAION-5B (Schuhmann 2022), Q-Instruct (Wu 2024)
