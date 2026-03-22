---
name: shader-fundamentals
description: GLSL shader fundamentals—vertex and fragment shaders, uniforms, varyings, attributes, coordinate systems, built-in variables, and data types. Use when writing custom shaders, understanding the graphics pipeline, or debugging shader code. The foundational skill for all shader work.
---

# Shader Fundamentals

GLSL (OpenGL Shading Language) runs on the GPU. Vertex shaders transform geometry; fragment shaders color pixels.

## Quick Start

```glsl
// Vertex Shader
uniform mat4 projectionMatrix;
uniform mat4 modelViewMatrix;

attribute vec3 position;
attribute vec2 uv;

varying vec2 vUv;

void main() {
  vUv = uv;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}

// Fragment Shader
uniform float uTime;
varying vec2 vUv;

void main() {
  vec3 color = vec3(vUv, sin(uTime) * 0.5 + 0.5);
  gl_FragColor = vec4(color, 1.0);
}
```

## Graphics Pipeline

```
Vertex Data → [Vertex Shader] → Primitives → Rasterization → [Fragment Shader] → Pixels
     ↑              ↑                                              ↑
 attributes    transforms                                    per-pixel color
```

| Stage | Runs Per | Purpose |
|-------|----------|---------|
| Vertex Shader | Vertex | Transform positions, pass data to fragment |
| Fragment Shader | Pixel | Calculate final color |

## Data Types

### Scalars

```glsl
bool b = true;
int i = 42;
float f = 3.14;
```

### Vectors

```glsl
vec2 v2 = vec2(1.0, 2.0);
vec3 v3 = vec3(1.0, 2.0, 3.0);
vec4 v4 = vec4(1.0, 2.0, 3.0, 4.0);

// Integer vectors
ivec2 iv2 = ivec2(1, 2);
ivec3 iv3 = ivec3(1, 2, 3);

// Boolean vectors
bvec2 bv2 = bvec2(true, false);
```

### Swizzling

```glsl
vec4 color = vec4(1.0, 0.5, 0.2, 1.0);

vec3 rgb = color.rgb;      // (1.0, 0.5, 0.2)
vec2 rg = color.rg;        // (1.0, 0.5)
float r = color.r;         // 1.0

// Reorder
vec3 bgr = color.bgr;      // (0.2, 0.5, 1.0)

// Duplicate
vec3 rrr = color.rrr;      // (1.0, 1.0, 1.0)

// Position aliases (xyzw = rgba = stpq)
vec3 pos = v4.xyz;
vec2 uv = v4.st;
```

### Matrices

```glsl
mat2 m2;  // 2x2
mat3 m3;  // 3x3
mat4 m4;  // 4x4

// Access columns
vec4 col0 = m4[0];

// Access element
float val = m4[1][2];  // column 1, row 2
```

### Samplers

```glsl
uniform sampler2D uTexture;      // 2D texture
uniform samplerCube uCubemap;    // Cube map

// Sample texture
vec4 texColor = texture2D(uTexture, vUv);
vec4 cubeColor = textureCube(uCubemap, direction);
```

## Variable Qualifiers

### Uniforms (CPU → GPU, constant per draw)

```glsl
// Set from JavaScript, same for all vertices/fragments
uniform float uTime;
uniform vec3 uColor;
uniform mat4 uModelMatrix;
uniform sampler2D uTexture;
```

### Attributes (Per-vertex data)

```glsl
// Only in vertex shader
attribute vec3 position;    // Built-in: vertex position
attribute vec3 normal;      // Built-in: vertex normal
attribute vec2 uv;          // Built-in: texture coordinates
attribute vec3 color;       // Built-in: vertex color

// Custom attributes
attribute float aScale;
attribute vec3 aOffset;
```

### Varyings (Vertex → Fragment, interpolated)

```glsl
// Vertex shader: write
varying vec2 vUv;
varying vec3 vNormal;

void main() {
  vUv = uv;
  vNormal = normal;
}

// Fragment shader: read (interpolated across triangle)
varying vec2 vUv;
varying vec3 vNormal;

void main() {
  // vUv is interpolated between triangle vertices
}
```

## Built-in Variables

### Vertex Shader

```glsl
// Output (must write)
vec4 gl_Position;       // Clip-space position

// Output (optional)
float gl_PointSize;     // Point sprite size (for gl.POINTS)
```

### Fragment Shader

```glsl
// Input
vec4 gl_FragCoord;      // Window-space position (pixel coordinates)
bool gl_FrontFacing;    // True if front face
vec2 gl_PointCoord;     // Point sprite coordinates [0,1]

// Output
vec4 gl_FragColor;      // Final pixel color
```

## Coordinate Spaces

```
Local/Object Space
      ↓ modelMatrix
World Space
      ↓ viewMatrix
View/Eye/Camera Space
      ↓ projectionMatrix
Clip Space (-1 to 1)
      ↓ perspective divide
NDC (Normalized Device Coordinates)
      ↓ viewport transform
Screen Space (pixels)
```

### Common Matrices (Three.js/R3F)

```glsl
uniform mat4 modelMatrix;       // Local → World
uniform mat4 viewMatrix;        // World → View
uniform mat4 projectionMatrix;  // View → Clip
uniform mat4 modelViewMatrix;   // Local → View (modelMatrix * viewMatrix)
uniform mat3 normalMatrix;      // For transforming normals

uniform vec3 cameraPosition;    // Camera world position
```

### Standard Vertex Transform

```glsl
void main() {
  // Full transform chain
  vec4 worldPosition = modelMatrix * vec4(position, 1.0);
  vec4 viewPosition = viewMatrix * worldPosition;
  vec4 clipPosition = projectionMatrix * viewPosition;
  gl_Position = clipPosition;
  
  // Or combined (more efficient)
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
```

## Built-in Functions

### Math

```glsl
// Trigonometry
sin(x), cos(x), tan(x)
asin(x), acos(x), atan(x)
atan(y, x)  // atan2

// Exponential
pow(x, y)   // x^y
exp(x)      // e^x
log(x)      // ln(x)
sqrt(x)     // √x
inversesqrt(x)  // 1/√x

// Common
abs(x)
sign(x)     // -1, 0, or 1
floor(x)
ceil(x)
fract(x)    // x - floor(x)
mod(x, y)   // x % y (floating point)
min(x, y)
max(x, y)
clamp(x, min, max)
mix(a, b, t)  // Linear interpolation: a*(1-t) + b*t
step(edge, x) // 0 if x < edge, else 1
smoothstep(e0, e1, x)  // Smooth Hermite interpolation
```

### Vector

```glsl
length(v)        // Vector magnitude
distance(a, b)   // length(a - b)
dot(a, b)        // Dot product
cross(a, b)      // Cross product (vec3 only)
normalize(v)     // Unit vector
reflect(I, N)    // Reflection vector
refract(I, N, eta)  // Refraction vector
faceforward(N, I, Nref)  // Flip normal if needed
```

## Common Patterns

### UV Coordinates

```glsl
// vUv ranges from (0,0) at bottom-left to (1,1) at top-right
varying vec2 vUv;

void main() {
  // Center UVs: -0.5 to 0.5
  vec2 centered = vUv - 0.5;
  
  // Aspect-corrected (assuming you pass uResolution)
  vec2 uv = vUv;
  uv.x *= uResolution.x / uResolution.y;
  
  // Tiling
  vec2 tiled = fract(vUv * 4.0);  // 4x4 tiles
  
  // Polar coordinates
  float angle = atan(centered.y, centered.x);
  float radius = length(centered);
}
```

### Color Operations

```glsl
// Grayscale (perceptual weights)
float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));

// Contrast
color = (color - 0.5) * contrast + 0.5;

// Brightness
color += brightness;

// Saturation
float gray = dot(color, vec3(0.299, 0.587, 0.114));
color = mix(vec3(gray), color, saturation);

// Gamma correction
color = pow(color, vec3(1.0 / 2.2));  // Linear to sRGB
color = pow(color, vec3(2.2));         // sRGB to linear
```

### Smooth Transitions

```glsl
// Hard edge
float mask = step(0.5, value);

// Soft edge
float mask = smoothstep(0.4, 0.6, value);

// Anti-aliased edge (screen-space)
float mask = smoothstep(-fwidth(value), fwidth(value), value);
```

## Debugging

### Visualize Values

```glsl
// Show UVs as color
gl_FragColor = vec4(vUv, 0.0, 1.0);

// Show normals
gl_FragColor = vec4(vNormal * 0.5 + 0.5, 1.0);

// Show depth
float depth = gl_FragCoord.z;
gl_FragColor = vec4(vec3(depth), 1.0);

// Show value range (red=negative, green=positive)
gl_FragColor = vec4(max(0.0, value), max(0.0, -value), 0.0, 1.0);
```

### Common Errors

| Issue | Likely Cause |
|-------|--------------|
| Black screen | gl_Position not set, or NaN values |
| Uniform not updating | Wrong name or type mismatch |
| Texture black | Texture not loaded, wrong UV |
| Flickering | Z-fighting, precision issues |
| Faceted look | Normals not interpolated |

## Precision

```glsl
// Declare precision (required in fragment shader for WebGL 1)
precision highp float;
precision mediump float;
precision lowp float;
```

| Precision | Range | Use Case |
|-----------|-------|----------|
| highp | ~10^38 | Positions, matrices |
| mediump | ~10^14 | UVs, colors |
| lowp | ~2 | Simple flags |

## File Structure

```
shader-fundamentals/
├── SKILL.md
├── references/
│   ├── glsl-types.md         # Complete type reference
│   ├── builtin-functions.md  # All built-in functions
│   └── coordinate-spaces.md  # Transform pipeline
└── scripts/
    └── templates/
        ├── basic.glsl        # Starter template
        └── fullscreen.glsl   # Fullscreen quad shader
```

## Reference

- `references/glsl-types.md` — Complete data type reference
- `references/builtin-functions.md` — All GLSL built-in functions
- `references/coordinate-spaces.md` — Transform pipeline deep-dive
