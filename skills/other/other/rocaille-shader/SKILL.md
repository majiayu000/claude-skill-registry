---
name: rocaille-shader
description: Generate Rocaille-style domain warping shaders with sinusoidal displacement, and mouse-reactive liquid logo effects on image/SVG textures. This skill should be used when building WebGL/GLSL visualizations, shader art, procedural backgrounds, organic swirling light effects, or when applying a rippling, bending, chromatically-refracting liquid hover effect to a logo or hero image. Creates characteristic flowing patterns through iterative coordinate warping using the formula v += sin(v.yx + t) / amplitude, and extends the same domain-warp family to texture-sampling pointer-driven effects.
argument-hint: [--mode rocaille|liquid-logo] [warp-count] [color-mode] [format]
---

# Rocaille Shader Skill

Generate organic, swirling light effects through progressive domain warping - a technique that creates increasingly complex patterns by iteratively displacing coordinates using sinusoidal functions.

## Core Technique

The Rocaille effect builds complexity through repeated application of:

```glsl
v += sin(v.yx + t) / amplitude;
```

Where:
- `v` is a 2D coordinate vector
- `v.yx` swaps x/y components creating characteristic swirl
- `t` is time for animation
- `amplitude` controls warp intensity (1.0 = strong, 4.0 = subtle)
- Each iteration adds more organic complexity

## Quick Reference

| Warps | Effect | Use Case |
|-------|--------|----------|
| 1-2 | Subtle wave | Backgrounds, subtle motion |
| 3-5 | Organic flow | Music visualizers, hero sections |
| 6-9 | Complex swirl | Psychedelic effects, main attraction |
| 10+ | Chaotic | Experimental, glitch art |

## Usage

To generate a shader, specify:
1. **Warp count** (1-15): Number of displacement iterations
2. **Color mode**: `basic`, `rainbow`, `monochrome`, `neon`, or custom RGB
3. **Output format**: `shadertoy`, `threejs`, `webgl`, `p5js`

### Generate Custom Shader

Run the generator script:

```bash
python3 scripts/rocaille_generator.py --warps 5 --color rainbow --format shadertoy
```

Options:
- `--warps N` - Number of warp iterations (default: 5)
- `--color MODE` - Color mode: basic, rainbow, monochrome, neon (default: rainbow)
- `--format FMT` - Output format: shadertoy, threejs, webgl, p5js, all (default: shadertoy)
- `--amplitude N` - Warp intensity divisor (default: 2.0)
- `--speed N` - Animation speed multiplier (default: 1.0)
- `--demo` - Generate interactive HTML demo page

### Asset Templates

Pre-built templates available in `assets/templates/`:

| Template | Description |
|----------|-------------|
| `shadertoy.glsl` | Shadertoy-compatible fragment shader |
| `threejs.js` | Three.js ShaderMaterial with uniforms |
| `vanilla-webgl.html` | Pure WebGL2, no dependencies |
| `p5js.js` | P5.js shader mode integration |
| `interactive.html` | Full demo with controls |
| `liquid-logo.glsl` | Shadertoy liquid-logo reference (reads iChannel0) |
| `liquid-logo.html` | Standalone liquid-logo runtime (drop `logo.png` beside it, or pass `?logo=…`) |

## Implementation Patterns

### Minimal Shadertoy

```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = (fragCoord - 0.5 * iResolution.xy) / iResolution.y;
    vec2 v = uv;

    for(int i = 0; i < 5; i++) {
        v += sin(v.yx + iTime) / 2.0;
    }

    float d = 1.0 / length(v);
    fragColor = vec4(vec3(d * 0.1), 1.0);
}
```

### Three.js Integration

```javascript
const material = new THREE.ShaderMaterial({
    uniforms: {
        uTime: { value: 0 },
        uWarpCount: { value: 5 },
        uAmplitude: { value: 2.0 }
    },
    vertexShader: vertexCode,
    fragmentShader: fragmentCode
});

// In animation loop
material.uniforms.uTime.value = performance.now() / 1000;
```

## Customization

### Base Shape Variations

Replace `1.0 / length(v)` with:
- `length(v)` - Inverted (dark center)
- `sin(length(v) * 10.0)` - Ripple rings
- `abs(v.x) + abs(v.y)` - Diamond shape
- `max(abs(v.x), abs(v.y))` - Square shape

### Color Mapping

```glsl
// Rainbow based on angle
vec3 color = 0.5 + 0.5 * cos(atan(v.y, v.x) + vec3(0, 2, 4));

// Neon glow
vec3 color = vec3(d * 0.2, d * 0.05, d * 0.3);

// Temperature gradient
vec3 color = mix(vec3(0.1, 0.2, 0.8), vec3(1.0, 0.3, 0.1), d);
```

## Liquid Logo Mode

Apply the domain-warp family to a texture instead of a procedural distance
field. A pointer-driven radial warp + chromatic aberration makes a static
image or SVG logo ripple, bend, and refract around the cursor, with an
optional Lissajous idle breathing when the pointer is inactive. Use for
hero sections, brand reveals, loading moments, or any hover state where
the logo should feel alive.

### Generate a self-contained HTML

```bash
python3 scripts/rocaille_generator.py \
    --mode liquid-logo \
    --input path/to/logo.svg \
    --output liquid.html
```

The output embeds the image as a base64 data URI — the generated HTML is a
single file with no external dependencies.

### Tuning parameters

| Flag | Default | Effect |
|------|---------|--------|
| `--distortion` | `0.40` | Peak UV pull toward the cursor |
| `--radius` | `0.25` | Gaussian falloff radius (smaller = tighter ripple) |
| `--decay` | `3.0` | Release decay rate (higher = snappier relax) |
| `--chroma` | `0.015` | RGB-channel UV split magnitude |
| `--idle` / `--no-idle` | on | Lissajous idle breathing when cursor is still |

The runtime respects `prefers-reduced-motion` (halves distortion and idle
amplitude) and pauses its RAF loop on `visibilitychange`, so the effect
consumes zero GPU when the tab is hidden.

For the shader math (radial Gaussian falloff, UV pull direction,
cursor-aligned chromatic offset), see `references/liquid-logo.md`.

## Reference Documentation

For deeper understanding:
- `references/rocaille-complete.md` - Full 8-step shader breakdown
- `references/domain-warping.md` - Theory from Inigo Quilez
- `references/glsl-patterns.md` - Common GLSL patterns used
- `references/liquid-logo.md` - Liquid logo math (falloff, pull, chromatic offset)

## Combining Effects

Layer with other techniques:
- **Bloom**: Apply gaussian blur to bright areas
- **Grain**: Add `fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453)`
- **Vignette**: Multiply by `1.0 - length(uv) * 0.5`
- **Chromatic aberration**: Sample RGB at slightly offset UVs

## Attribution

- **Rocaille domain-warp technique** — the core `v += sin(v.yx + t) / amplitude`
  formula and the theory behind it come from [Inigo Quilez's domain warping
  article](https://iquilezles.org/articles/warp/) (iq / Shadertoy).
- **Liquid Logo mode** — inspired by [**LiquidLogo**](https://gustavwf.supply/product/liquidlogo)
  by **Gustav WF** ([@gustavwf](https://x.com/gustavwf) / gustavwf.supply), a
  free Framer component. The liquid-logo shader here is **reimplemented from
  scratch** from first principles (radial Gaussian falloff, UV displacement,
  cursor-aligned chromatic offset) — it is not a port of Gustav's code and
  does not redistribute any of his files. If you want a drop-in Framer
  component, get it directly from him; if you want a standalone HTML file or
  a Shadertoy-compatible shader, this skill generates one.
