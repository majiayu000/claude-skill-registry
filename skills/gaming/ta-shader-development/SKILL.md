---
name: ta-shader-development
description: GLSL/TSL shader creation, compilation, and testing for R3F. Use when writing custom shaders, implementing visual effects, optimizing shader performance.
category: shader
---

# Shader Development Skill

> "Shaders unlock visual effects impossible with standard materials."

## When to Use This Skill

Use when:

- Creating custom visual effects
- Implementing procedural patterns
- Optimizing material performance
- Building GPU-accelerated effects

## Shader Structure

```tsx
import { shaderMaterial } from '@react-three/drei';
import { extend } from '@react-three/fiber';

const CustomShaderMaterial = shaderMaterial(
  // Uniforms (variables passed from JS)
  {
    uTime: { value: 0 },
    uColor: { value: new THREE.Color(0.0, 0.5, 1.0) },
    uTexture: { value: null },
  },
  // Vertex shader
  vertexShader,
  // Fragment shader
  fragmentShader
);

extend({ CustomShaderMaterial });
```

## Vertex Shader Patterns

### Basic Vertex Shader

```glsl
uniform float uTime;
uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;

attribute vec3 position;
attribute vec2 uv;
attribute vec3 normal;

varying vec2 vUv;
varying vec3 vNormal;
varying vec3 vPosition;

void main() {
  vUv = uv;
  vNormal = normal;
  vPosition = position;

  // Basic displacement
  vec3 pos = position;
  pos.y += sin(pos.x * 4.0 + uTime) * 0.1;

  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

### SDF-based Displacement

```glsl
// Sphere SDF
float sdSphere(vec3 p, float r) {
  return length(p) - r;
}

void main() {
  vec3 pos = position;

  // Animated SDF displacement
  float d = sdSphere(pos * 2.0, 1.0);
  pos += normal * d * 0.1;

  vUv = uv;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

### Vertex Animation

```glsl
uniform float uTime;
varying vec2 vUv;

// Simple noise function
float hash(vec2 p) {
  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

void main() {
  vUv = uv;
  vec3 pos = position;

  // Wave displacement
  pos.z += sin(pos.x * 2.0 + uTime) * cos(pos.y * 2.0 + uTime) * 0.2;

  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

## Fragment Shader Patterns

### Color Gradient

```glsl
uniform float uTime;
varying vec2 vUv;

void main() {
  // UV gradient
  vec3 color = vec3(vUv.x, vUv.y, 0.5);

  // Add time-based animation
  color.r += sin(uTime) * 0.2;

  gl_FragColor = vec4(color, 1.0);
}
```

### Circle/Shape Drawing

```glsl
varying vec2 vUv;

float sdCircle(vec2 p, float r) {
  return length(p) - r;
}

float sdBox(vec2 p, vec2 b) {
  vec2 d = abs(p) - b;
  return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
}

void main() {
  vec2 uv = vUv * 2.0 - 1.0;

  // Draw circle
  float circle = sdCircle(uv, 0.5);
  vec3 color = vec3(smoothstep(0.0, 0.01, circle));

  // Draw box border
  float box = sdBox(uv, vec2(0.4));
  float border = abs(box) - 0.05;
  color = mix(color, vec3(1.0, 0.0, 0.0), 1.0 - smoothstep(0.0, 0.01, border));

  gl_FragColor = vec4(color, 1.0);
}
```

### Noise Patterns

```glsl
// Simple noise
float hash(vec2 p) {
  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float noise(vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  f = f * f * (3.0 - 2.0 * f);

  float a = hash(i);
  float b = hash(i + vec2(1.0, 0.0));
  float c = hash(i + vec2(0.0, 1.0));
  float d = hash(i + vec2(1.0, 1.0));

  return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

float fbm(vec2 p) {
  float value = 0.0;
  float amplitude = 0.5;
  for (int i = 0; i < 5; i++) {
    value += amplitude * noise(p);
    p *= 2.0;
    amplitude *= 0.5;
  }
  return value;
}

void main() {
  vec2 uv = vUv * 3.0;
  float n = fbm(uv);
  vec3 color = vec3(n);

  gl_FragColor = vec4(color, 1.0);
}
```

### Fresnel Effect (Rim Lighting)

```glsl
varying vec3 vNormal;
varying vec3 vViewPosition;

void main() {
  // Calculate view direction
  vec3 viewDir = normalize(-vViewPosition);

  // Fresnel calculation
  float fresnel = pow(1.0 - dot(viewDir, vNormal), 3.0);

  // Apply fresnel
  vec3 color = vec3(0.0, 0.5, 1.0);
  color = mix(color, vec3(1.0), fresnel);

  gl_FragColor = vec4(color, 1.0);
}
```

### Glow Effect

```glsl
uniform float uTime;
varying vec2 vUv;

void main() {
  vec2 uv = vUv * 2.0 - 1.0;
  float dist = length(uv);

  // Glow calculation
  float glow = 0.02 / dist;
  glow = pow(glow, 1.5);

  // Animated color
  vec3 color = vec3(
    0.5 + 0.5 * sin(uTime),
    0.5 + 0.5 * sin(uTime + 2.0),
    0.5 + 0.5 * sin(uTime + 4.0)
  );

  color *= glow;

  gl_FragColor = vec4(color, 1.0);
}
```

## Complete Shader Example

```tsx
import { shaderMaterial } from '@react-three/drei';
import { extend, useFrame } from '@react-three/fiber';
import { useRef } from 'react';

const HologramMaterial = shaderMaterial(
  {
    uTime: 0,
    uColor: new THREE.Color(0.0, 1.0, 0.5),
    uScanLineDensity: 100.0,
    uScanLineSpeed: 2.0,
  },
  // Vertex shader
  `
    uniform float uTime;
    varying vec2 vUv;
    varying vec3 vPosition;
    varying vec3 vNormal;

    void main() {
      vUv = uv;
      vPosition = position;
      vNormal = normalize(normalMatrix * normal);

      // Holographic wobble
      vec3 pos = position;
      float wobble = sin(pos.y * 2.0 + uTime * 3.0) * 0.02;
      pos.x += wobble;

      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  // Fragment shader
  `
    uniform float uTime;
    uniform vec3 uColor;
    uniform float uScanLineDensity;
    uniform float uScanLineSpeed;
    varying vec2 vUv;
    varying vec3 vPosition;
    varying vec3 vNormal;

    void main() {
      // Scan lines
      float scanLine = sin(vPosition.y * uScanLineDensity + uTime * uScanLineSpeed);
      scanLine = smoothstep(-0.5, 0.5, scanLine);

      // Fresnel effect
      vec3 viewDir = normalize(cameraPosition - vPosition);
      float fresnel = pow(1.0 - abs(dot(viewDir, vNormal)), 2.0);

      // Combine effects
      vec3 color = uColor;
      color *= 0.5 + scanLine * 0.5;
      color += fresnel * 0.5;

      // Add grid pattern
      float grid = step(0.95, fract(vPosition.x * 10.0)) +
                   step(0.95, fract(vPosition.y * 10.0));
      color += grid * 0.2;

      gl_FragColor = vec4(color, 0.3 + fresnel * 0.5);
    }
  `
);

extend({ HologramMaterial });

function HologramMesh() {
  const materialRef = useRef();

  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uTime = state.clock.elapsedTime;
    }
  });

  return (
    <mesh>
      <boxGeometry args={[2, 2, 2]} />
      <hologramMaterial ref={materialRef} />
    </mesh>
  );
}
```

## ShaderToy MCP Integration

> "Shadertoy MCP enables querying thousands of community shaders for reference and learning."

The Shadertoy MCP server provides two tools for shader research and development:

### Available MCP Tools

| Tool                | Purpose                                | Usage                                                |
| ------------------- | -------------------------------------- | ---------------------------------------------------- |
| `get_shader_info()` | Retrieve full shader code and metadata | Get implementation details from any ShaderToy shader |
| `search_shader()`   | Search shaders by keywords             | Find reference shaders for specific effects          |

### Shader Research Workflow

```bash
# 1. Search for reference shaders
# Search for "terrain raymarching" shaders
search_shader("terrain raymarching")

# 2. Get shader details
# Get full code for a specific shader
get_shader_info("4tdSWr")  # Shader ID from search results
```

### Converting ShaderToy to R3F Format

ShaderToy uses a different entry point than Three.js/R3F:

**ShaderToy Format:**

```glsl
// ShaderToy - single pass, mainImage entry point
void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
  vec2 uv = fragCoord / iResolution.xy;
  fragColor = vec4(uv, 0.0, 1.0);
}
```

**R3F Format (Fragment Shader):**

```glsl
// R3F - standard vertex/fragment shader pairing
varying vec2 vUv;
uniform float uTime;
uniform vec2 uResolution;

void main() {
  vec2 uv = vUv;
  gl_FragColor = vec4(uv, 0.0, 1.0);
}
```

### Uniform Mapping Table

| ShaderToy     | R3F/Three.js    | Description                       |
| ------------- | --------------- | --------------------------------- |
| `iTime`       | `uTime`         | Elapsed time in seconds           |
| `iResolution` | `uResolution`   | Canvas resolution (width, height) |
| `iMouse`      | `uMouse`        | Mouse position                    |
| `iChannel0-3` | `uTexture0-3`   | Texture inputs                    |
| `iFrame`      | (compute in JS) | Frame counter                     |
| `iDate`       | (compute in JS) | Year, month, day, time            |

### Complete Conversion Example

```tsx
import { shaderMaterial } from '@react-three/drei';
import { extend, useFrame } from '@react-three/fiber';
import { useRef, useState } from 'react';
import * as THREE from 'three';

// 1. Research: Use Shadertoy MCP to find reference
// search_shader("ocean waves")
// get_shader_info("MsS2Wc")  # Example ocean shader

// 2. Convert: Create R3F shader material
const OceanWavesMaterial = shaderMaterial(
  {
    uTime: 0,
    uResolution: new THREE.Vector2(window.innerWidth, window.innerHeight),
    uColor: new THREE.Color(0.0, 0.5, 0.8),
  },
  // Vertex shader
  `
    varying vec2 vUv;
    varying vec3 vPosition;

    void main() {
      vUv = uv;
      vPosition = position;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  // Fragment shader (converted from ShaderToy)
  `
    uniform float uTime;
    uniform vec2 uResolution;
    uniform vec3 uColor;
    varying vec2 vUv;
    varying vec3 vPosition;

    // Noise function (from ShaderToy reference)
    float hash(vec2 p) {
      return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
    }

    float noise(vec2 p) {
      vec2 i = floor(p);
      vec2 f = fract(p);
      f = f * f * (3.0 - 2.0 * f);

      float a = hash(i);
      float b = hash(i + vec2(1.0, 0.0));
      float c = hash(i + vec2(0.0, 1.0));
      float d = hash(i + vec2(1.0, 1.0));

      return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
    }

    void main() {
      // ShaderToy: fragCoord / iResolution.xy
      vec2 uv = vUv;

      // Animate waves
      float wave = sin(uv.x * 10.0 + uTime) * 0.1;
      wave += sin(uv.y * 8.0 + uTime * 1.3) * 0.08;

      // Foam patterns
      float foam = noise(uv * 20.0 + uTime);
      foam = step(0.7, foam);

      // Combine
      vec3 color = uColor;
      color += vec3(wave);
      color += vec3(foam * 0.3);

      gl_FragColor = vec4(color, 0.8);
    }
  `
);

extend({ OceanWavesMaterial });

function OceanMesh() {
  const materialRef = useRef<{ uTime: number }>();
  const [resolution, setResolution] = useState(
    new THREE.Vector2(window.innerWidth, window.innerHeight)
  );

  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uTime = state.clock.elapsedTime;
    }
  });

  // Update resolution on resize
  useEffect(() => {
    const handleResize = () => {
      setResolution(new THREE.Vector2(window.innerWidth, window.innerHeight));
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]}>
      <planeGeometry args={[10, 10, 128, 128]} />
      <oceanWavesMaterial ref={materialRef} uResolution={resolution} />
    </mesh>
  );
}
```

### ShaderToy MCP Usage Pattern

```tsx
// When developing a new shader effect:

// 1. Search for reference implementations
// MCP Tool: search_shader("effect name")
// Examples:
// - "terrain raymarching" -> get terrain SDF patterns
// - "water caustics" -> get light refraction shaders
// - "particle explosion" -> get GPU particle patterns
// - "hologram scan" -> get scanline effects

// 2. Analyze promising shaders
// MCP Tool: get_shader_info("shaderId")
// Extract:
// - Noise functions
// - Color grading
// - SDF operations
// - Animation patterns

// 3. Convert to R3F format
// - Replace mainImage() with main()
// - Map iTime -> uTime
// - Map iResolution -> uResolution
// - Add vertex shader with varyings
// - Wrap in shaderMaterial()

// 4. Test and iterate
// - Debug with visualization helpers
// - Optimize performance
// - Add interactive uniforms
```

### Common Shader-to-R3F Conversions

**Terrain/Heightmap:**

```glsl
// ShaderToy
vec3 rayMarch(vec3 ro, vec3 rd) { ... }

// R3F - Add uniforms for camera position
uniform vec3 uCameraPos;
varying vec3 vWorldPosition;

// In vertex shader
vWorldPosition = (modelMatrix * vec4(position, 1.0)).xyz;
```

**Texture Sampling:**

```glsl
// ShaderToy
vec4 tex = texture(iChannel0, uv);

// R3F - Use proper texture uniform
uniform sampler2D uTexture0;
vec4 tex = texture2D(uTexture0, uv);
```

**Mouse Interaction:**

```glsl
// ShaderToy
vec2 mouse = iMouse.xy / iResolution.xy;

// R3F - Pass from React
uniform vec2 uMouse;
// In component: <material uMouse={[mouseX / width, mouseY / height]} />
```

### Attribution Protocol

When using ShaderToy shaders as reference:

```tsx
/**
 * [Effect Name] Shader
 * Based on "[Original Shader Name]" by [Author] on ShaderToy
 * Original: https://www.shadertoy.com/view/[shaderId]
 * Adapted for React Three Fiber by [Your Name]
 * Changes: [List modifications]
 */
```

### Search Strategy by Effect Type

| Want to Create | Search Terms                                    | Example Shaders |
| -------------- | ----------------------------------------------- | --------------- |
| Terrain        | `terrain raymarching`, `heightmap`, `mountains` | 4tdSWr, MdX3Rf  |
| Water          | `ocean waves`, `water caustics`, `ripple`       | MsS2Wc, Xts3DD  |
| Fire/Smoke     | `fire`, `smoke`, `particles`                    | 4sf3RN, XslGRr  |
| Hologram       | `hologram`, `scanline`, `glitch`                | 4tlSzl, WtBDWf  |
| Glow/Bloom     | `glow`, `bloom`, `neon`                         | 4sS3Wc, XtG3zw  |
| Clouds         | `clouds`, `sky`, `atmosphere`                   | 4dS3Wc, MtXS3S  |

## Shader Debugging

```glsl
// Debug UVs
gl_FragColor = vec4(vUv, 0.0, 1.0);

// Debug normals
gl_FragColor = vec4(vNormal * 0.5 + 0.5, 1.0);

// Debug position (normalized)
gl_FragColor = vec4(vPosition * 0.5 + 0.5, 1.0);

// Visualize value as grayscale
float value = /* your calculation */;
gl_FragColor = vec4(vec3(value), 1.0);

// Heat map visualization
vec3 heatmap(float t) {
  return mix(vec3(0.0, 0.0, 1.0),
             mix(vec3(0.0, 1.0, 0.0), vec3(1.0, 0.0, 0.0), t),
             t);
}
```

## Anti-Patterns

❌ **DON'T:**

- Create complex shaders without testing incrementally
- Use if/else for dynamic branching in shaders
- Forget to normalize vectors before dot products
- Use uniforms for static values (use const)

✅ **DO:**

- Build shaders step by step, test each addition
- Use mix() instead of if/else when possible
- Test on mobile hardware
- Add comments to complex shader math

## TSL Error Handling

### ⚠️ CRITICAL: TSL hash() Function Type Safety

**Learned from feat-tps-003 (2026-01-27):**

The TSL `hash()` function expects a **float** parameter, but passing `vec2` directly causes cryptic runtime errors:

```
TypeError: Cannot read properties of undefined (reading 'replace')
```

**ALWAYS use `dot()` to convert vec2 to float before passing to hash():**

```tsx
// ❌ WRONG - Causes TypeError at runtime
const hashValue = hash(position.xy);

// ✅ CORRECT - Use dot() for vec2 → float conversion
const hashValue = hash(dot(position.xy, vec2(1.0)));
```

**Why this happens:** TSL's `hash()` function internally calls `.toString()` on its argument for shader code generation. When passed a `vec2` node, the string representation doesn't match what `hash()` expects, causing the replace error.

**Files affected:** TerrainShader.ts, PaintMaterial.ts, PaintPatternShader.ts

---

### Problem: TypeError on .replace()

When using TSL (Three.js Shading Language) functions that may return undefined:

```glsl
// DANGEROUS - Can throw TypeError
const shaderCode = tslFunction().replace('pattern', 'replacement');
```

### Solution: Null-Check Before String Operations

```tsx
// SAFE - Check for undefined before string operations
function safeTslToString(tslNode: Node | undefined, fallback: string): string {
  if (!tslNode) return fallback;
  try {
    const str = tslNode.toString();
    return str || fallback;
  } catch {
    return fallback;
  }
}

// Usage in shader material creation
const vertexShader = safeTslToString(myTslNode, defaultVertexShader);
```

### TSL Hash Function Pattern

The `hash()` function requires explicit `vec2` handling:

```tsx
// WRONG - Implicit conversion can fail
const hashValue = hash(position.xy);

// CORRECT - Use dot() to explicitly convert vec2
const hashValue = hash(dot(position.xy, vec2(1.0)));
```

### Fn() for Conditional TSL Logic

```tsx
import { Fn } from 'three/examples/jsm/nodes/Nodes.js';

const conditionalNode = Fn(() => {
  const condition = /* your TSL logic */;
  return condition.select(valueA, valueB);
});
```

### Nullable Texture Uniforms

```tsx
import { texture, uniform } from 'three/examples/jsm/nodes/Nodes.js';

// Handle null textures safely
function createTextureUniform(initialValue: THREE.Texture | null) {
  return uniform(initialValue ?? nullTexture);
}
```

### Complete TSL Safe Pattern

```tsx
import { shaderMaterial } from '@react-three/drei';
import { Fn, hash, dot, vec2, uniform } from 'three/examples/jsm/nodes/Nodes.js';

const SafeTSLMaterial = shaderMaterial(
  {
    uTime: 0,
    uTexture: null, // Nullable texture
  },
  // Vertex shader
  `
    uniform float uTime;
    varying vec2 vUv;

    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  // Fragment shader - built from TSL with null checks
  safeTslToString(
    myTslFragmentNode,
    `
      uniform float uTime;
      varying vec2 vUv;

      void main() {
        vec3 color = vec3(0.5);
        gl_FragColor = vec4(color, 1.0);
      }
    `
  )
);
```

## Checklist

Before finalizing shader:

- [ ] Shader compiles without errors
- [ ] TSL functions null-checked before string conversion
- [ ] hash() uses dot() for vec2 arguments
- [ ] Uniforms properly typed
- [ ] Varyings match between vertex/fragment
- [ ] Performance tested on target hardware
- [ ] Fallback considered for low-end devices
- [ ] Complex shader sections documented

## Texture and Asset Loading

### Loading Textures with R3F

```tsx
import { useTexture } from '@react-three/drei';
import { useLoader } from '@react-three/fiber';
import { TextureLoader } from 'three';

// Option 1: Using useTexture hook (recommended)
function MyMesh() {
  const texture = useTexture('/assets/textures/MyTexture.png');
  return (
    <mesh>
      <meshStandardMaterial map={texture} />
    </mesh>
  );
}

// Option 2: Using useLoader with TextureLoader
function MyMesh2() {
  const texture = useLoader(TextureLoader, '/assets/textures/MyTexture.png');
  return (
    <mesh>
      <meshStandardMaterial map={texture} />
    </mesh>
  );
}

// Option 3: Loading multiple textures
function TexturedMesh() {
  const textures = useTexture({
    map: '/assets/textures/diffuse.png',
    normal: '/assets/textures/normal.png',
    roughness: '/assets/textures/roughness.png',
  });
  return (
    <mesh>
      <meshStandardMaterial {...textures} />
    </mesh>
  );
}
```

### Vite Asset Path Handling with Spaces

**CRITICAL**: When asset folder names contain spaces (e.g., "Splat Pack"), you must:

1. **URL-encode the paths** in your TypeScript code:

```tsx
// WRONG - Will fail to load
const texturePath = '/assets/Splat Pack/splat1.png';

// CORRECT - URL encoded
const texturePath = '/assets/Splat%20Pack/splat1.png';
```

2. **Extend Vite's assetsPlugin** to serve non-standard file types:

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { viteSingleFile } from 'vite-plugin-singlefile';

export default defineConfig({
  plugins: [
    react(),
    viteSingleFile(),
    {
      name: 'assets-plugin',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          // Serve image files from assets folder
          if (req.url?.startsWith('/assets/')) {
            next(); // Let Vite handle it
          } else {
            next();
          }
        });
      },
    },
  ],
  assetsInclude: ['**/*.png', '**/*.jpg', '**/*.jpeg', '**/*.webp', '**/*.gif'],
});
```

3. **Create a centralized texture manager**:

```tsx
// src/components/game/effects/SplatTextureManager.ts
const SPLAT_TEXTURE_BASE = '/assets/Splat%20Pack';

export const SPLAT_TEXTURES = [
  `${SPLAT_TEXTURE_BASE}/Splat_A_01.png`,
  `${SPLAT_TEXTURE_BASE}/Splat_A_02.png`,
  // ... more textures
] as const;

export function getRandomSplatTexture(): string {
  return SPLAT_TEXTURES[Math.floor(Math.random() * SPLAT_TEXTURES.length)];
}
```

### Preloading Textures

```tsx
import { useLoader } from '@react-three/fiber';
import { TextureLoader } from 'three';

// Preload multiple textures before scene renders
function TexturePreloader({ urls, onLoaded }: { urls: string[]; onLoaded: () => void }) {
  useLoader(TextureLoader, urls, (loader) => {
    // All textures loaded
    onLoaded();
  });
  return null;
}
```

### Texture Best Practices

✅ **DO:**

- URL-encode paths with spaces (`%20` for space)
- Use relative paths from `/public` folder: `/assets/...`
- Preload textures before they're needed
- Use `useTexture` from `@react-three/drei` for automatic disposal
- Implement texture atlases for many small textures

❌ **DON'T:**

- Use un-encoded paths with spaces in URLs
- Import large textures directly in JSX (causes bundle bloat)
- Forget to dispose unused textures (memory leak)
- Load full-resolution textures for mobile devices
