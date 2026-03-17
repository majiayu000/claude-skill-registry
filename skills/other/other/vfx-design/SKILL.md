---
name: vfx-design
description: Extract visual effects entities from narrative text. Use when analyzing particle systems, shaders, lighting, color palettes, and VFX for magic, combat, and environment.
---
# vfx-design

Domain skill for Visual Effects Artist. Specific extraction rules and expertise.

## Domain Expertise

- **Particle systems**: Fire, smoke, magic effects, weather particles
- **Shaders**: Post-processing, materials, visual styles
- **Lighting**: Dynamic lighting, shadows, ambient occlusion
- **Visual effects**: Explosions, magic auras, transitions, illusions
- **Color theory**: Palettes, color grading, mood lighting

## Entity Types (5 total)

- **visual_effect** - Visual effects and FX
- **particle** - Particle systems and emitters
- **shader** - Shaders and materials
- **lighting** - Lighting systems
- **color_palette** - Color palettes

## Processing Guidelines

When extracting visual entities from chapter text:

1. **Identify visual effect elements**:
   - Magic effects described (glowing, shimmering, auras)
   - Particles mentioned (sparks, smoke, dust)
   - Lighting conditions (bright, dim, colorful)
   - Shader-like effects (bloom, blur, distortion)
   - Color descriptions (golden, crimson, azure)

2. **Extract visual effect details**:
   - Effect types (fire, ice, lightning, shadow)
   - Particle behaviors and lifetimes
   - Lighting colors, intensities, sources
   - Shader effects (bloom, vignette, chromatic aberration)
   - Color palettes and grading

3. **Analyze visual effect context**:
   - Magical vs natural effects
   - Environmental lighting changes
   - Character aura or enhancement effects
   - Combat or exploration effects

4. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Performance**: Visual effects shouldn't overwhelm performance
- **Readability**: Effects shouldn't obscure gameplay
- **Consistency**: Similar effects should look consistent
- **Atmosphere**: VFX enhance mood and immersion
- **Magic vs tech**: Different visual languages for magic vs technology
