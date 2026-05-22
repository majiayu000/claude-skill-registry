---
name: style-consistency-enforcer
description: Analyze multiple assets and define a unified visual style guide. Use when images don't match, assets come from different sources, or need to regenerate consistent variants. Outputs style guides with line weight, shading, color saturation rules, and unified prompt templates for image generation.
---

# Style Consistency Enforcer (Stil-Wachter)

Analyze multiple assets and define a unified visual style guide.

## When to Use

- Multiple images that don't match
- Assets from different sources/generators
- Need to regenerate consistent variants
- Something feels "off" but can't pinpoint it

## Process

### 1. Catalog Each Asset

For each image, document:

| Attribute | Value |
|-----------|-------|
| Style | flat/detailed/painterly/3D |
| Line weight | thin/medium/thick/none |
| Color saturation | muted/moderate/vibrant |
| Color temperature | warm/neutral/cool |
| Shading | flat/soft gradient/hard shadows |
| Texture | smooth/grainy/noisy |
| Perspective | flat/isometric/realistic |
| Detail level | minimal/moderate/high |

### 2. Identify Conflicts

| Attribute | Asset A | Asset B | Conflict? |
|-----------|---------|---------|-----------|
| Style | flat minimal | detailed realistic | YES |
| Colors | muted teal | vibrant cyan | mild |
| Line weight | none | thick outlines | YES |

### 3. Choose Target Style

Pick the asset that:
- Best represents desired vibe
- Would be hardest to regenerate
- Has most screen presence

Document as the "style anchor."

### 4. Create Style Guide

```markdown
## Unified Style Guide

**Base Style:** [e.g., Flat minimalist illustration]
**Color Palette:** [e.g., Muted teals and navy]
**Line Weight:** [e.g., None (shapes only)]
**Shading:** [e.g., Soft gradients, no hard shadows]
**Texture:** [e.g., Smooth, no grain]
**Perspective:** [e.g., Slight depth, not fully flat]

### Do's
- [specific guidelines]

### Don'ts
- [things to avoid]
```

### 5. Asset-Specific Fixes

For each non-conforming asset:

```
Asset: [name]
Current: [current style]
Target: [target style]

Fixes needed:
- [specific change 1]
- [specific change 2]

Regeneration prompt:
"[subject], [style], [colors], [atmosphere]"
```

### 6. Unified Prompt Template

```
[SUBJECT DESCRIPTION]

Style: [e.g., flat minimalist vector illustration]
Colors: [specific hex codes]
Atmosphere: [mood descriptors]
Shading: [approach]
Details: [level]
Background: [treatment]

Negative: [things to exclude]
```

## Quick Comparison Checklist

- [ ] Same illustration style?
- [ ] Matching color temperature?
- [ ] Similar saturation levels?
- [ ] Consistent line treatment?
- [ ] Compatible perspectives?
- [ ] Unified shading approach?
- [ ] Matching detail density?

## Common Style Families

| Style | Characteristics | Good For |
|-------|-----------------|----------|
| Flat Minimal | No shadows, bold shapes, limited colors | Modern apps |
| Soft Gradient | Gentle shading, atmospheric | Premium feel |
| Line Art | Outlines, minimal fill | Technical, playful |
| Isometric | 30° angles, consistent depth | Data viz, gaming |
