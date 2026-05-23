---
name: ta-vfx-postfx
description: Post-processing effects with React Three Fiber. Use when adding bloom, depth of field, effect composer, visual polish.
category: vfx
---

# Post-Processing Effects Skill

> "The final polish that makes your visuals pop – post-processing transforms good into great."

## When to Use This Skill

Use when:

- Adding visual flair to scenes
- Creating atmosphere and mood
- Implementing stylized looks
- Hiding rendering imperfections

## Quick Start

```tsx
import { EffectComposer, Bloom, Vignette, Noise } from '@react-three/postprocessing';

function PostProcessing() {
  return (
    <EffectComposer>
      <Bloom intensity={0.5} luminanceThreshold={0.8} />
      <Vignette offset={0.5} darkness={0.5} />
      <Noise opacity={0.05} />
    </EffectComposer>
  );
}
```

## Decision Framework

| Effect         | Use Case                     | Performance |
| -------------- | --------------------------- | ----------- |
| Bloom          | Glowing effects, bright areas | Medium      |
| Vignette       | Focus attention, cinematic   | Low         |
| Color grading  | Mood, style consistency      | Low         |
| Depth of Field | Cinematic focus              | High        |
| Chromatic Aberration | Glitch, distorted look  | Low         |
| Film Grain     | Retro feel, texture          | Low         |
| SMAA           | Anti-aliasing                | Medium      |
| SSR            | Realistic reflections        | Very High   |

## Effects Reference

### Bloom

```tsx
import { Bloom } from '@react-three/postprocessing';

<Bloom
  intensity={1.0}        // Bloom strength
  luminanceThreshold={0.9} // Only bright pixels glow
  luminanceSmoothing={0.025} // Smooth threshold
  mipmapBlur             // Higher quality blur
/>
```

**Use for:** Emissive materials, magical effects, sci-fi interfaces

### Vignette

```tsx
import { Vignette } from '@react-three/postprocessing';

<Vignette
  offset={0.5}    // Position of vignette center
  darkness={0.5}  // Darkness at edges
  goDark          // Fade to black instead of opacity
/>
```

**Use for:** Cinematic feel, focusing player attention

### Depth of Field

```tsx
import { DepthOfField } from '@react-three/postprocessing';

<DepthOfField
  focusDistance={0.02}  // Distance to focus plane
  focalLength={0.05}    // Lens focal length
  bokehScale={4}        // Blur amount
  height={480}          // Resolution of DOF pass
/>
```

**Use for:** Cutscenes, focusing on important objects

### Chromatic Aberration

```tsx
import { ChromaticAberration } from '@react-three/postprocessing';

<ChromaticAberration
  offset={0.002}  // RGB channel offset amount
/>
```

**Use for:** Glitch effects, distortion, retro look

### Color Grading

```tsx
import { HalfTone, TiltShift, HueShift } from '@react-three/postprocessing';

// Hue shift for mood
<HueShift hue={0.2} />

// Half-tone for comic/print look
<HalfTone
  blendFunction={BlendFunction.NORMAL}
  radius={1}
  smoothing={0.1}
/>
```

### Noise / Film Grain

```tsx
import { Noise } from '@react-three/postprocessing';

<Noise
  opacity={0.05}     // Grain intensity
  premultiply       // Premultiply alpha
/>
```

**Use for:** Film look, hiding banding, texture

### God Rays (Volumetric Light)

```tsx
import { GodRays } from '@react-three/postprocessing';

// First, create a light source
const sun = useRef<THREE.PointLight>(null!);

<GodRays
  sun={sun}
  exposure={0.34}
  decay={0.9}
  density={0.96}
  weight={0.4}
  samples={100}
/>
```

## Effect Chains

```tsx
import {
  EffectComposer,
  RenderPass,
  Bloom,
  Vignette,
  Noise,
  ChromaticAberration,
} from '@react-three/postprocessing';

function CinematicLook() {
  return (
    <EffectComposer>
      <RenderPass />
      <Bloom
        intensity={0.3}
        luminanceThreshold={0.8}
        luminanceSmoothing={0.9}
      />
      <ChromaticAberration offset={[0.001, 0.001]} />
      <Noise opacity={0.03} />
      <Vignette offset={0.3} darkness={0.3} />
    </EffectComposer>
  );
}
```

## Performance Tips

```tsx
// Disable expensive effects on mobile
const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent);

function AdaptivePostProcessing() {
  return (
    <EffectComposer>
      <Bloom intensity={isMobile ? 0.2 : 0.5} />
      {!isMobile && <DepthOfField focusDistance={0.02} />}
      <Vignette offset={0.5} darkness={0.5} />
    </EffectComposer>
  );
}
```

## Custom Shaders

```tsx
import { Effect } from '@react-three/postprocessing';

const CustomEffect = shaderMaterial(
  { uTime: 0, uIntensity: 0.5 },
  // Vertex shader (pass-through)
  `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  // Fragment shader
  `
    uniform float uTime;
    uniform float uIntensity;
    varying vec2 vUv;

    // Simple color shift effect
    void main() {
      vec2 uv = vUv;
      float shift = sin(uTime) * uIntensity;
      vec4 color = texture2D(tDiffuse, uv);
      color.r += shift * 0.1;
      color.b -= shift * 0.1;
      gl_FragColor = color;
    }
  `
);

extend({ CustomEffect });
```

## Anti-Patterns

❌ **DON'T:**

- Use all effects at once (looks overprocessed)
- Enable expensive effects on mobile without testing
- Use bloom with low threshold (everything glows)
- Forget that effects render at full resolution

✅ **DO:**

- Use effects intentionally for mood/style
- Adjust effect intensity with gameplay state
- Test on target hardware
- Use lower resolution buffers when possible

## Checklist

Before adding post-processing:

- [ ] Effect serves clear artistic purpose
- [ ] Intensity tested in different lighting
- [ ] Performance acceptable on target platform
- [ ] Effect doesn't interfere with gameplay visibility
- [ ] Mobile variant considered

## Common Looks

### Sci-Fi Interface

```tsx
<EffectComposer>
  <Bloom intensity={1.5} luminanceThreshold={0.2} />
  <ChromaticAberration offset={0.005} />
  <Noise opacity={0.1} />
</EffectComposer>
```

### Vintage Film

```tsx
<EffectComposer>
  <Noise opacity={0.15} premultiply />
  <Vignette offset={0.2} darkness={0.8} />
  <HueShift hue={-0.05} />
</EffectComposer>
```

### Dream Sequence

```tsx
<EffectComposer>
  <Bloom intensity={0.8} luminanceThreshold={0.5} />
  <DepthOfField focusDistance={0.01} bokehScale={3} />
  <HueShift hue={0.1} />
</EffectComposer>
```

## Related Skills

For material basics: `Skill("ta-r3f-materials")`
For custom shaders: `Skill("ta-shader-sdf")`

## External References

- [react-postprocessing docs](https://github.com/pmndrs/react-postprocessing)
