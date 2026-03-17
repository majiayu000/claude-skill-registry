---
name: immersive-visuals-router
description: Master router for immersive visual experiences combining React Three Fiber, shaders, particles, post-processing, GSAP animation, and audio. Use when building 3D web experiences, visualizers, creative coding projects, interactive installations, or any project requiring multiple visual technologies. Dispatches to 6 specialized domain routers covering 29 total skills.
---

# Immersive Visuals Router

Master router dispatching to 6 domain routers for comprehensive visual experiences.

## Routing Protocol

1. **Classify** — Identify primary domains from user request
2. **Route to Domain** — Select appropriate domain router(s)
3. **Combine Domains** — Most projects need 3-4 domains together
4. **Load Skills** — Domain routers will load specific skills

## Domain Overview

| Domain | Router | Skills | Focus |
|--------|--------|--------|-------|
| 3D Rendering | `r3f-router` | 6 | React Three Fiber, scenes, materials, camera |
| Shaders | `shaders-router` | 5 | GLSL, custom materials, visual effects |
| Particles | `particles-router` | 4 | Particle systems, physics, GPU optimization |
| Post-Processing | `postfx-router` | 3 | Bloom, effects, EffectComposer |
| Animation | `gsap-router` | 4 | GSAP tweens, timelines, scroll, React |
| Audio | `audio-router` | 3 | Playback, analysis, audio-reactive |

**Total: 6 routers, 25 specialized skills**

## Quick Route by Project Type

### 3D Scene (R3F Focus)
```
Primary:   r3f-router → Scene setup, components, materials
Secondary: postfx-router → Bloom, cinematic effects
Optional:  gsap-router → Camera animations
```

### Audio Visualizer
```
Primary:   audio-router → Playback, analysis, reactive
Secondary: r3f-router → 3D scene for visuals
Supporting: shaders-router → Custom visual effects
           postfx-router → Bloom, glow
           particles-router → Beat-reactive particles
```

### Creative Coding / Generative Art
```
Primary:   shaders-router → Custom fragment shaders
Secondary: r3f-router → Render pipeline
Supporting: postfx-router → Effects chain
```

### Interactive Experience
```
Primary:   r3f-router → 3D scene, interaction
Secondary: gsap-router → Smooth animations
Supporting: postfx-router → Visual polish
           audio-router → Sound feedback
```

### Countdown / Event Page
```
Primary:   gsap-router → Sequenced animations
Secondary: r3f-router → 3D elements
Supporting: postfx-router → Dramatic effects
           audio-router → Ambient, countdown audio
           particles-router → Celebration effects
```

### Particle-Heavy Effect
```
Primary:   particles-router → Particle systems
Secondary: r3f-router → Scene setup
Supporting: postfx-router → Bloom for particles
           shaders-router → Custom particle shaders
```

## Signal-Based Routing

### Domain Detection Signals

**r3f-router** (3D Rendering):
- "3D", "Three.js", "R3F", "React Three Fiber"
- "scene", "mesh", "geometry", "camera"
- "3D model", "GLTF", "environment"
- "orbit controls", "transform"

**shaders-router** (Custom Shaders):
- "shader", "GLSL", "fragment", "vertex"
- "custom material", "uniform"
- "procedural", "noise", "pattern"
- "ray marching", "SDF"

**particles-router** (Particle Systems):
- "particle", "emitter", "particle system"
- "dust", "sparks", "confetti", "stars"
- "instancing", "GPU particles"

**postfx-router** (Post-Processing):
- "bloom", "glow", "post-processing"
- "vignette", "chromatic aberration"
- "depth of field", "color grading"
- "EffectComposer"

**gsap-router** (Animation):
- "GSAP", "GreenSock", "animate"
- "timeline", "sequence", "tween"
- "scroll animation", "ScrollTrigger"
- "entrance animation"

**audio-router** (Audio):
- "audio", "music", "sound"
- "visualizer", "audio reactive"
- "beat", "frequency", "FFT"
- "Tone.js"

## Domain Combinations

### Cinematic 3D Scene
```
r3f-router     → Scene, camera, lighting
shaders-router → Custom materials
postfx-router  → Bloom, color grading, vignette
gsap-router    → Camera movements
```

### Music Visualizer
```
audio-router     → Load music, analyze frequencies
r3f-router       → 3D visualization geometry
shaders-router   → Audio-reactive shaders
particles-router → Beat-triggered particles
postfx-router    → Bloom, chromatic aberration
```

### Landing Page Hero
```
r3f-router     → Background 3D scene
gsap-router    → Text animations, scroll effects
postfx-router  → Subtle bloom, film grain
```

### Interactive Installation
```
r3f-router       → 3D environment
particles-router → Interaction feedback
gsap-router      → Transition animations
audio-router     → Sound feedback
postfx-router    → Immersive effects
```

### Product Showcase
```
r3f-router     → 3D product model
gsap-router    → Rotation, zoom animations
postfx-router  → Lighting effects, environment
```

## Temporal Collapse Stack

Complete domain routing for the New Year countdown:

```
┌─────────────────────────────────────────────────┐
│           TEMPORAL COLLAPSE PROJECT             │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────┐  ┌─────────────┐              │
│  │ r3f-router  │  │gsap-router  │              │
│  │ - Scene     │  │ - Digit flip│              │
│  │ - Digits    │  │ - Sequences │              │
│  │ - Camera    │  │ - Countdown │              │
│  └──────┬──────┘  └──────┬──────┘              │
│         │                │                      │
│  ┌──────┴────────────────┴──────┐              │
│  │       postfx-router          │              │
│  │  - Bloom (cosmic glow)       │              │
│  │  - Chromatic aberration      │              │
│  │  - Vignette (void edge)      │              │
│  └──────────────┬───────────────┘              │
│                 │                               │
│  ┌──────────────┴───────────────┐              │
│  │      particles-router        │              │
│  │  - Time dilation particles   │              │
│  │  - Star field                │              │
│  │  - Celebration burst         │              │
│  └──────────────┬───────────────┘              │
│                 │                               │
│  ┌──────────────┴───────────────┐              │
│  │       audio-router           │              │
│  │  - Cosmic ambient loop       │              │
│  │  - Countdown ticks           │              │
│  │  - Beat-reactive visuals     │              │
│  │  - Celebration music         │              │
│  └──────────────────────────────┘              │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Domain Responsibilities

| Domain | Temporal Collapse Role |
|--------|------------------------|
| r3f | 3D countdown digits, camera orbit, environment |
| shaders | Digit morphing effect, custom glow material |
| particles | Time dilation particles, star field, celebration |
| postfx | Bloom on digits, vignette, chromatic on beat |
| gsap | Digit flip animation, intensity ramp, celebration |
| audio | Ambient loop, ticks, beat detection, celebration |

### Color Palette Reference

```javascript
const TEMPORAL_PALETTE = {
  void: '#050508',      // Background
  cyan: '#00F5FF',      // Primary glow
  magenta: '#FF00FF',   // Accent
  gold: '#FFD700',      // Celebration highlight
  white: '#FFFFFF'      // Text, bright elements
};
```

## Project Initialization Guide

### Step 1: Identify Core Requirements
- What is the primary visual experience?
- Is there audio involvement?
- Does it need animation/interaction?
- What level of visual fidelity?

### Step 2: Select Primary Domain
Choose the domain that represents the main technical challenge.

### Step 3: Add Supporting Domains
Based on secondary requirements:
- Need glow effects? → `postfx-router`
- Need smooth animations? → `gsap-router`
- Need particles? → `particles-router`
- Need audio? → `audio-router`
- Need custom materials? → `shaders-router`

### Step 4: Load Domain Skills
Each domain router will direct to specific skills.

## Performance Considerations

### By Domain

| Domain | Performance Impact | Optimization |
|--------|-------------------|--------------|
| r3f | Medium-High | LOD, frustum culling |
| shaders | Low-High* | Simplify math, reduce loops |
| particles | High | GPU instancing, LOD |
| postfx | Medium-High | Reduce passes, resolution |
| gsap | Low | Kill unused tweens |
| audio | Low | Appropriate FFT size |

*Depends on shader complexity

### Recommended Limits

- Particles: 10,000-50,000 with instancing
- Post-processing passes: 3-5 max
- Shader uniforms: Keep minimal
- Audio FFT: 128-256 for reactive, 1024+ for visualization

## Fallback Routing

- **"3D" mentioned** → Start with `r3f-router`
- **"Visualizer" mentioned** → `audio-router` + `r3f-router`
- **"Animation" only** → `gsap-router`
- **"Effect" unclear** → `postfx-router`
- **No clear signals** → Ask about project type

## Skill Dependencies

```
r3f-router
├── Independent (can use alone)
└── Enhanced by: shaders, postfx, particles

shaders-router
├── Requires: r3f (for Three.js context)
└── Enhanced by: postfx

particles-router
├── Requires: r3f (for scene)
└── Enhanced by: postfx (bloom), shaders (custom)

postfx-router
├── Requires: r3f (for scene)
└── Enhanced by: shaders (custom effects)

gsap-router
├── Independent (can use alone)
└── Enhanced by: r3f (3D animation)

audio-router
├── Independent (can use alone)
└── Enhanced by: all domains for reactive visuals
```

## Quick Reference Matrix

| Project Type | R3F | Shaders | Particles | PostFX | GSAP | Audio |
|--------------|-----|---------|-----------|--------|------|-------|
| 3D Scene | ● | ○ | ○ | ● | ○ | - |
| Visualizer | ● | ● | ● | ● | - | ● |
| Landing Page | ● | - | ○ | ● | ● | - |
| Particle Effect | ● | ○ | ● | ● | - | - |
| Countdown | ● | ○ | ● | ● | ● | ● |
| Product 3D | ● | - | - | ● | ● | - |
| Generative Art | ● | ● | ○ | ○ | - | - |

● Required  ○ Optional  - Not needed
