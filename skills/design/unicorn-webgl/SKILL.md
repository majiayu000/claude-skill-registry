---
name: unicorn-webgl
description: |
  WebGL/3D web development with Unicorn Studio, Three.js, shaders, and scroll-driven interactions.
  TRIGGERS: Unicorn Studio, WebGL effects, Three.js, shaders, GLSL, scroll-driven 3D, GSAP ScrollTrigger, Lenis, hero animations, interactive visuals, distortion effects, blur effects, lighting effects, PBR materials, fragment shaders, vertex shaders, post-processing, Framer/Webflow embeds, immersive web experiences.
---

# Unicorn Studio + WebGL/3D Web Dev

## Unicorn Studio Overview

Browser-based no-code WebGL tool for interactive visuals, 2D/3D effects, animations. Export as images, videos, or embeddable WebGL scenes.

**Workflow:**
1. Create project (artboard canvas)
2. Import assets (images, videos, logos, shapes, 3D primitives)
3. Add/position layers (images, shapes, text, video)
4. Apply effects from Effects panel → adjust parameters → stack effects
5. Add motion (time-based) and interactivity (hover, scroll, cursor, timeline)
6. Export: static/video OR embeddable code/SDK for Framer, Webflow, Wix, Three.js

## Effects Taxonomy

| Category | What it does | Code equivalent |
|----------|--------------|-----------------|
| **Filters** | Color manipulation, tints, contrast, saturation, grading | Fragment shader color ops, post-processing |
| **Distortion** | Warps, displacements, waves, noise, refraction | Displacement shaders, vertex deformation |
| **Blur** | Gaussian, directional, zoom, bokeh | Multi-pass Gaussian blur nodes |
| **Lighting** | Simulated lights, glow, highlights, rim | PBR lighting, custom BRDF |
| **Stylize** | Halftone, posterize, grain, glitch, edge detect | Custom fragment shaders |
| **Misc** | Experimental effects | — |
| **Custom** | User-defined shaders | GLSL/TSL extensions |

## Integration Patterns

**Pattern 1: Visual shader editor for hero sections**
- Design in Unicorn → embed in React/Next/Framer/Webflow
- Use for cards, transitions, section backgrounds

**Pattern 2: 2D WebGL FX layer**
- Unicorn handles parallax, lighting, distortions on top of standard layout
- Deep 3D (full environments) stays in custom Three.js/R3F

**Pattern 3: Rapid prototyping**
- Designers iterate look in Unicorn
- Devs replicate/extend in GLSL/TSL/WebGPU where needed

## Three.js Core Concepts

**Scene structure:** Scene → Camera → Mesh (Geometry + Material) → Renderer

**Lighting types:**
- `AmbientLight`: Uniform fill, no shadows
- `DirectionalLight`: Parallel "sunlight", casts shadows
- `PointLight`: Omnidirectional from point, falloff
- `SpotLight`: Cone-shaped, focused highlights
- `HemisphereLight`: Sky/ground gradient

**Materials:**
- PBR: baseColor, metalness, roughness, normal, AO
- Unlit: Ignores scene lighting (UI, toon, FX)
- Custom: Your own BRDF/stylized lighting

## Shader Fundamentals

**Vertex shader:** Positions vertices, deforms geometry (waves, wobble, displacement)

**Fragment shader:** Computes pixel color (lighting, shading, effects)

**Common patterns:**
- Gaussian blur: Double render-pass softening
- Fresnel: View-angle rim highlight (glow, outlines)
- Cel/toon: Quantized light bands
- Displacement: Texture/math moves vertices

**Languages:**
- GLSL: C-like, WebGL standard
- TSL: Node-based, generates shaders (WebGPU)

## Scroll + Interaction Stack

**GSAP:**
- Timeline: Sequenced animations, scrubbed by scroll/time
- ScrollTrigger: Links scroll position to timeline progress
- Easing: Acceleration curves (power, easeInOut)

**Lenis:** Smooth scroll library, feeds delta to GSAP + render loop

**Scroll-driven camera:** Camera position/rotation/FOV updated by scroll progress

**Best practices:**
- Dedicated render loop + smooth scroll delta (Lenis)
- Drive shader uniforms (time, intensity, distortionAmount) from GSAP timelines
- Combine custom shaders + scroll camera + UI text animation in cohesive hero

## Quick Reference

See `references/glossary.json` for term definitions and code mappings.

See `references/workflows.md` for step-by-step implementation guides:
- Scroll-driven 3D hero
- Unicorn embed in Next.js
- Custom shader + GSAP integration
