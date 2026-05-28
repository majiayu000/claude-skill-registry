---
name: Visual Style Guide
description: |
  Reference for consistent visual style across procedurally generated assets.

  **Triggers:** "visual style", "art style", "color palette", "material", "PBR".

  **Before generating:** Check `.studio/visual-style.md` for project style.

  **Load references when:**
  - Style tokens → `references/style-tokens.md`
  - Color palettes → `references/color-palettes.md`
  - PBR materials → `references/material-database.md`
  - Metal materials → `references/materials-metals.md`
  - Natural materials → `references/materials-natural.md`
  - Generation recipes → `references/generation-recipes.md`
  - Quality assessment → `references/quality-heuristics.md`
version: 3.1.0
---

# Visual Style Guide

Maintain consistent visual style across procedurally generated assets through style tokens, color palettes, and material definitions.

## Core Concepts

| Concept | Purpose | Reference |
|---------|---------|-----------|
| Style Token | Modifies generation parameters (roughness, saturation, detail) | `style-tokens.md` |
| Color Palette | HSL ranges for consistent colors | `color-palettes.md` |
| Material | PBR parameters for surfaces | `material-database.md` |
| Recipe | Bundles token + palette + material + constraints | `generation-recipes.md` |

## Style Token Quick Reference

| Token | Roughness | Saturation | Detail | Use For |
|-------|-----------|------------|--------|---------|
| RUSTIC | +0.3 | 0.7x | Medium | Medieval, weathered |
| PRISTINE | -0.2 | 1.0x | High | Sci-fi, clean |
| CYBERPUNK | -0.1 | 1.3x | Extreme | Neon, tech |
| GOTHIC | +0.2 | 0.6x | High | Horror, ornate |
| ORGANIC | +0.1 | 0.9x | High | Natural, living |

See `references/style-tokens.md` for 15+ tokens with full parameters.

## Color Palette Quick Reference

| Palette | Hue Range | Saturation | Use For |
|---------|-----------|------------|---------|
| WarmEarthy | 15-45 (orange-brown) | 0.3-0.6 | Wood, leather |
| CoolMetal | 200-240 (blue-gray) | 0.1-0.3 | Steel, chrome |
| Neon | 280-320, 160-200 | 0.8-1.0 | Cyberpunk |
| Muted | Any | 0.1-0.3 | Stone, worn |
| Vibrant | Any | 0.7-1.0 | Fantasy, cartoon |

See `references/color-palettes.md` for 12 palettes with specifications.

## Material Quick Reference

Use dot notation: `category.variant`

| Category | Variants | Key Properties |
|----------|----------|----------------|
| metal | polished, brushed, rusted, chrome | High metallic |
| wood | fresh, weathered, painted, charred | Low metallic, high roughness |
| stone | polished, rough, mossy, marble | Varied roughness |
| fabric | cotton, silk, leather, velvet | Medium roughness |
| crystal | clear, colored, magical | Low roughness, optional emission |

See `references/material-database.md` for 40+ materials with PBR values.

## Semantic Description Examples

| Natural Language | Style Translation |
|------------------|------------------|
| "rusty old barrel" | Style: Rustic, Material: metal.rusted |
| "glowing crystal" | Style: Fantasy, Material: crystal.magical, Emission: 0.8 |
| "clean sci-fi panel" | Style: Pristine, Material: metal.brushed |
| "neon cyberpunk sign" | Style: Cyberpunk, Material: tech.hologram |

## Creative Workflow

```
1. DESCRIBE  →  "weathered medieval barrel"
2. INTERPRET →  Style: Rustic, Palette: WarmEarthy, Material: wood.weathered
3. GENERATE  →  Produce mesh + textures
4. ASSESS    →  Run quality heuristics
5. ITERATE   →  Adjust based on feedback
```

## Quality Heuristics Summary

**Texture:**
- Contrast > 0.15
- Noise coherence > 0.4
- Histogram balance > 0.3

**Mesh:**
- Triangle count within budget
- Degenerate triangles = 0
- UV coverage > 0.95

See `references/quality-heuristics.md` for measurement code.

## Game Type Recommendations

| Game Type | Recipe |
|-----------|--------|
| Medieval RPG | Rustic + WarmEarthy + wood/stone |
| Sci-Fi | Pristine + CoolMetal + metal/tech |
| Horror | Gothic + Muted + stone/organic |
| Cartoon | Stylized + Vibrant + any |
| Cyberpunk | Cyberpunk + Neon + metal/tech |

See `references/generation-recipes.md` for complete recipe code.
