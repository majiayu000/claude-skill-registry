# WebGL Shader Gradient (Effect #1)

Fullscreen 2D aurora/nebula gradient via WebGL2 fragment shader. No 3D geometry — just a fullscreen quad + GLSL.

## Architecture

```
canvas (position: fixed, z-index: 1)
  → WebGL2 context
  → Fullscreen quad (2 triangles)
  → Fragment shader (6 noise layers, additive mixing)
```

## Setup

```js
const canvas = document.getElementById('shader-canvas');
const gl = canvas.getContext('webgl2');
if (!gl) { /* fallback to CSS gradient */ }
```

### Fullscreen Quad

```js
const positions = new Float32Array([-1,-1, 1,-1, -1,1, -1,1, 1,-1, 1,1]);
const buf = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, buf);
gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);
const vao = gl.createVertexArray();
gl.bindVertexArray(vao);
gl.enableVertexAttribArray(0);
gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
```

### Vertex Shader

```glsl
#version 300 es
in vec4 aPosition;
void main() { gl_Position = aPosition; }
```

## Fragment Shader: 6-Layer Aurora

Each layer: `fbm(uv * frequency + time * speed) * color_weight`

Layers blend additively for aurora depth:
- Layer 1: green, freq 1.2, speed 0.4
- Layer 2: lime, freq 1.8, speed -0.3
- Layer 3: blue, freq 2.5, speed 0.2
- Layer 4: purple, freq 0.8, speed 0.6
- Layer 5: teal, freq 3.0, speed -0.5
- Layer 6: pink, freq 1.5, speed 0.1

### Simplex 2D Noise (GLSL)

```glsl
vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec3 permute(vec3 x) { return mod289(((x * 34.0) + 1.0) * x); }

float snoise(vec2 v) {
    const vec4 C = vec4(0.211324865405187, 0.366025403784439,
                       -0.577350269189626, 0.024390243902439);
    vec2 i = floor(v + dot(v, C.yy));
    vec2 x0 = v - i + dot(i, C.xx);
    vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
    vec4 x12 = x0.xyxy + C.xxzz;
    x12.xy -= i1;
    i = mod289(i);
    vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0)) + i.x + vec3(0.0, i1.x, 1.0));
    vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
    m = m*m; m = m*m;
    vec3 x_ = 2.0 * fract(p * C.www) - 1.0;
    vec3 h = abs(x_) - 0.5;
    vec3 ox = floor(x_ + 0.5);
    vec3 a0 = x_ - ox;
    m *= 1.79284291400159 - 0.85373472095314 * (a0*a0 + h*h);
    vec3 g;
    g.x = a0.x * x0.x + h.x * x0.y;
    g.yz = a0.yz * x12.xz + h.yz * x12.yw;
    return 130.0 * dot(m, g);
}
```

### FBM (Fractal Brownian Motion)

```glsl
float fbm(vec2 p, float t) {
    float val = 0.0, amp = 0.5, freq = 1.0;
    for (int i = 0; i < 5; i++) {
        val += amp * snoise(p * freq + t * 0.3);
        freq *= 2.0; amp *= 0.5;
    }
    return val;
}
```

## DPR Clamping

```js
const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
canvas.width = window.innerWidth * dpr;
canvas.height = window.innerHeight * dpr;
```

Clamp at 1.5 to prevent GPU overload on Retina/4K displays.

## Resize Handler

```js
window.addEventListener('resize', () => {
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = window.innerWidth * dpr;
    canvas.height = window.innerHeight * dpr;
    gl.viewport(0, 0, canvas.width, canvas.height);
});
```

## prefers-reduced-motion Fallback

```css
@media (prefers-reduced-motion: reduce) {
    #shader-canvas { display: none; }
    body { background: linear-gradient(135deg, #0a1a00 0%, #141414 40%, #1a0a2a 100%); }
}
```

## Color Palettes

| Palette | Colors |
|---------|--------|
| Aurora | green, lime, blue, purple, teal, pink |
| Nebula | orange, coral, magenta, deep blue, warm white, amber |

## Cross-Reference

For Three.js ShaderMaterial integration, see `rocaille-shader` skill.
