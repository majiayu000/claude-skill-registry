---
name: postfx-router
description: Router for Three.js post-processing effects domain. Use when implementing visual effects like bloom, glow, chromatic aberration, vignette, depth of field, color grading, or any screen-space effects. Routes to 3 specialized skills for bloom, effects, and composer setup.
---

# Post-Processing Router

Routes to 3 specialized skills based on post-processing requirements.

## Routing Protocol

1. **Classify** — Identify effect type from user request
2. **Match** — Apply signal matching rules below
3. **Combine** — Most production scenes need 2-3 skills together
4. **Load** — Read matched SKILL.md files before implementation

## Quick Route

### Tier 1: Core (Start Here)
| Need | Skill | Signals |
|------|-------|---------|
| Pipeline setup, effect ordering | `postfx-composer` | EffectComposer, setup, pipeline, render target, custom pass, multi-pass |
| Glow, luminance effects | `postfx-bloom` | bloom, glow, neon, emissive, luminance, UnrealBloom, selective bloom |
| Cinematic polish, color | `postfx-effects` | vignette, chromatic, DOF, grain, color grade, LUT, aberration |

## Signal Matching

### Primary Signals

**postfx-composer** (always start here for new projects):
- "set up post-processing"
- "configure effect pipeline"
- "create custom effect/pass"
- "render targets", "effect ordering"

**postfx-bloom**:
- "bloom", "glow", "luminance", "neon", "emissive"
- "selective bloom", "object glow", "UnrealBloomPass"

**postfx-effects**:
- "chromatic aberration", "vignette", "depth of field", "DOF"
- "film grain", "noise", "color grading", "LUT", "tone mapping"
- "scanlines", "CRT", "god rays"

### Confidence Scoring

- **High (3+ signals)** — Route directly to matched skill
- **Medium (1-2 signals)** — Route with composer as foundation
- **Low (0 signals)** — Start with `postfx-composer` for setup

## Common Combinations

### Basic Post-Processing Setup (2 skills)
```
postfx-composer → Pipeline architecture, effect ordering
postfx-bloom    → Basic glow effects
```

### Cinematic Scene (3 skills)
```
postfx-composer → Pipeline setup, tone mapping
postfx-bloom    → Subtle glow on lights
postfx-effects  → Vignette, grain, color grading
```

### Neon/Cyberpunk Aesthetic (2 skills)
```
postfx-bloom    → High-intensity selective bloom
postfx-effects  → Chromatic aberration, vignette
```

### Custom Effect Development (1-2 skills)
```
postfx-composer → Custom Effect class, shader writing
postfx-effects  → Reference existing effects
```

## Decision Table

| Effect Type | Complexity | Primary Skill | Supporting Skill |
|-------------|------------|---------------|------------------|
| Glow/bloom only | Simple | bloom | composer |
| Cinematic look | Medium | effects | composer + bloom |
| Custom effect | Complex | composer | - |
| Selective bloom | Medium | bloom | composer |
| Color grading | Simple | effects | composer |
| Full production | Complex | All three | - |

## Effect Categories

### Lighting Effects → postfx-bloom
- Bloom/glow, selective bloom, emissive enhancement, HDR luminance

### Camera Effects → postfx-effects
- Chromatic aberration, vignette, depth of field, lens distortion

### Color Effects → postfx-effects
- Tone mapping, color grading, LUT, hue/saturation

### Texture Effects → postfx-effects
- Film grain, noise, scanlines, CRT

### Architecture → postfx-composer
- EffectComposer setup, effect ordering, custom effects, render targets

## Integration with Other Domains

### With R3F (r3f-*)
```
r3f-fundamentals → Scene setup
postfx-composer  → Effect pipeline
postfx-bloom     → Object glow
```

### With Shaders (shaders-*)
```
shaders-glsl     → Custom effect shader code
postfx-composer  → Wrap in Effect class
```

### With Particles (particles-*)
```
particles-systems → Particle emitters
postfx-bloom      → Particle glow
postfx-effects    → Atmosphere
```

### With Audio (audio-*)
```
audio-analysis    → Frequency data
postfx-bloom      → Audio-reactive bloom
postfx-effects    → Audio-reactive aberration
```

## Quick Reference

| Effect | Skill |
|--------|-------|
| Bloom | `postfx-bloom` |
| Selective Bloom | `postfx-bloom` |
| Vignette | `postfx-effects` |
| Chromatic Aberration | `postfx-effects` |
| Depth of Field | `postfx-effects` |
| Film Grain/Noise | `postfx-effects` |
| Color Grading | `postfx-effects` |
| LUT | `postfx-effects` |
| Tone Mapping | `postfx-effects` |
| Custom Effects | `postfx-composer` |
| Render Targets | `postfx-composer` |

## Temporal Collapse Stack

```
postfx-composer → HDR pipeline, tone mapping, adaptive quality
postfx-bloom    → Cosmic glow on digits, particles, UI
postfx-effects  → Vignette (void edge), subtle chromatic, grain
```

## Fallback Behavior

- **No framework context** → Assume @react-three/postprocessing
- **Unclear effect type** → Start with `postfx-composer` + `postfx-bloom`
- **Performance concerns** → Prioritize `postfx-composer` optimization patterns
