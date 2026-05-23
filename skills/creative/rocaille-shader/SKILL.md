---
name: rocaille-shader
description: Generate Rocaille-style domain warping shaders with sinusoidal displacement. This skill should be used when building WebGL/GLSL visualizations, shader art, procedural backgrounds, or adding organic swirling light effects. Creates characteristic flowing patterns through iterative coordinate warping using the formula v += sin(v.yx + t) / amplitude.
argument-hint: [warp-count] [color-mode] [format]
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

## Reference Documentation

For deeper understanding:
- `references/rocaille-complete.md` - Full 8-step shader breakdown
- `references/domain-warping.md` - Theory from Inigo Quilez
- `references/glsl-patterns.md` - Common GLSL patterns used

## Combining Effects

Layer with other techniques:
- **Bloom**: Apply gaussian blur to bright areas
- **Grain**: Add `fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453)`
- **Vignette**: Multiply by `1.0 - length(uv) * 0.5`
- **Chromatic aberration**: Sample RGB at slightly offset UVs
