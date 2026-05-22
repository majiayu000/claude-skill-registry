---
name: Art Vision
description: This skill should be used when the user asks about "art direction", "visual style", "color palette", "aesthetic", "visual coherence", "art style guide", "visual identity", "character design style", "environment style", "UI style", or discusses establishing or reviewing visual direction. Provides art direction framework for visual coherence.
version: 1.0.0
---

# Art Vision

Establish and maintain visual coherence through systematic art direction.

## Visual Hierarchy

Three levels every scene communicates through:
1. **Primary Focus** - Player's eye (characters, interactives)
2. **Secondary Context** - Navigation, environmental storytelling
3. **Tertiary Atmosphere** - Background, mood reinforcement

## Style Spectrum Positioning

| Spectrum | Left ←→ Right |
|----------|---------------|
| Fidelity | Stylized ←→ Realistic |
| Detail | Simplified ←→ Complex |
| Saturation | Desaturated ←→ Vibrant |
| Contrast | Low-key ←→ High-key |
| Form | Geometric ←→ Organic |
| Line | Hard-edge ←→ Painterly |

Document position for each. All assets should align.

## Color Theory

**Primary Palette (60/30/10 rule):**
- Dominant (60%): Sets tone
- Secondary (30%): Creates interest
- Accent (10%): Draws attention

**Functional Colors:**
- Player/friendly: Consistent hue
- Enemy/danger: Distinct, high recognition
- Interactive: Subtle affordance cue
- UI: Readable on all backgrounds

**Emotional Mapping:**
- Safe zones: Warmer, saturated
- Danger zones: Cooler, desaturated, high contrast

## Style Bible Sections

1. **Visual Pillars** - 3-5 non-negotiable style principles
2. **Reference Board** - Target aesthetic by category
3. **Color Keys** - Paintings for major environments/moods
4. **Material Definitions** - Surface treatments, normal map intensity
5. **Character Design Language** - Proportions, silhouettes
6. **Environment Design Language** - Scale, architecture

## Normal Map Aesthetic Guidelines

Normal maps add surface detail. Use consistently with visual style:

| Style | Normal Map Intensity | Recommendation |
|-------|---------------------|----------------|
| Stylized/Toon | 0.3-0.5 | Subtle or skip |
| PS1/N64 Retro | 0.5-0.8 | Subtle detail |
| PS2/Dreamcast | 0.8-1.2 | Standard detail |
| Realistic | 1.0-2.0 | Full detail |

**When to use normal maps:**
- Hero characters requiring close-up detail
- Architecture with visible surface texture
- Materials that rely on micro-detail (metal, fabric, stone)

**When to skip normal maps:**
- Flat-shaded stylized aesthetics
- Memory-constrained scenarios
- Distant or fast-moving objects
- When geometry provides sufficient form

**Material-specific intensity:**
| Material | Intensity Range |
|----------|----------------|
| Smooth plastic | 0.2-0.4 |
| Fabric/cloth | 0.5-0.8 |
| Stone/concrete | 0.8-1.2 |
| Metal (brushed) | 1.0-1.5 |
| Organic (bark, skin) | 0.6-1.0 |

## Coherence Checklist

- [ ] Fidelity matches other assets?
- [ ] Detail density appropriate for hierarchy role?
- [ ] Palette used correctly?
- [ ] Shape language consistent?
- [ ] Integrates with intended environment?

Store in `.studio/art-direction.md` or `.studio/creative-direction.md`.

## References

- **`references/color-theory.md`** - Advanced palette building
- **`references/composition.md`** - Visual hierarchy principles
- **`references/style-spectrums.md`** - Detailed spectrum definitions
