---
name: postfx-composer
description: EffectComposer setup and architecture for Three.js post-processing pipelines. Use when setting up multi-pass rendering, combining effects, creating custom passes, managing render targets, or building reusable effect stacks. Foundation skill for all post-processing work.
---

# Post-Processing Composer

EffectComposer architecture, render pipelines, and custom pass creation.

## Quick Start

```bash
npm install @react-three/postprocessing postprocessing three
```

```tsx
import { Canvas } from '@react-three/fiber';
import { EffectComposer, Bloom, Vignette } from '@react-three/postprocessing';

function App() {
  return (
    <Canvas>
      <Scene />
      <EffectComposer>
        <Bloom intensity={1} />
        <Vignette darkness={0.5} />
      </EffectComposer>
    </Canvas>
  );
}
```

## Core Concepts

### Render Pipeline Flow

```
Scene Render → EffectComposer → Effect 1 → Effect 2 → ... → Screen
                    ↓
              [Render Target A]  →  [Render Target B]  →  [Screen]
```

### EffectComposer Configuration

```tsx
import { EffectComposer } from '@react-three/postprocessing';
import { HalfFloatType } from 'three';

function PostProcessing() {
  return (
    <EffectComposer
      enabled={true}
      depthBuffer={true}
      stencilBuffer={false}
      multisampling={8}
      frameBufferType={HalfFloatType}
    >
      {/* Effects processed in order */}
    </EffectComposer>
  );
}
```

## Effect Ordering

### Recommended Order

```tsx
<EffectComposer>
  {/* 1. Scene modification (needs scene data) */}
  <SSAO />
  <DepthOfField />

  {/* 2. Lighting/color effects */}
  <Bloom />
  <ToneMapping />

  {/* 3. Color grading */}
  <HueSaturation />
  <BrightnessContrast />
  <LUT />

  {/* 4. Screen-space effects */}
  <ChromaticAberration />
  <Vignette />

  {/* 5. Noise/grain (always last) */}
  <Noise />
</EffectComposer>
```

### Why Order Matters

```tsx
// WRONG: Bloom after color grading reduces glow
<EffectComposer>
  <HueSaturation saturation={-0.5} />
  <Bloom intensity={2} />
</EffectComposer>

// CORRECT: Bloom before color grading
<EffectComposer>
  <Bloom intensity={2} />
  <HueSaturation saturation={-0.5} />
</EffectComposer>
```

## Conditional Effects

### Toggle Effects at Runtime

```tsx
function DynamicEffects({ enableBloom, enableDOF }) {
  return (
    <EffectComposer>
      {enableBloom && <Bloom luminanceThreshold={0.2} intensity={1.5} />}
      {enableDOF && <DepthOfField focusDistance={0.02} focalLength={0.05} />}
      <Vignette darkness={0.4} />
    </EffectComposer>
  );
}
```

### Effect Presets

```tsx
const PRESETS = {
  cinematic: {
    bloom: { intensity: 0.8, threshold: 0.3 },
    vignette: { darkness: 0.5, offset: 0.3 },
    grain: { opacity: 0.03 }
  },
  scifi: {
    bloom: { intensity: 2.0, threshold: 0.1 },
    chromatic: { offset: [0.003, 0.003] },
    vignette: { darkness: 0.6, offset: 0.2 }
  },
  minimal: { vignette: { darkness: 0.3, offset: 0.4 } }
};

function PresetEffects({ preset = 'cinematic' }) {
  const config = PRESETS[preset];
  return (
    <EffectComposer>
      {config.bloom && <Bloom {...config.bloom} />}
      {config.chromatic && <ChromaticAberration offset={config.chromatic.offset} />}
      {config.vignette && <Vignette {...config.vignette} />}
      {config.grain && <Noise {...config.grain} />}
    </EffectComposer>
  );
}
```

## Custom Effects

### Basic Custom Effect

```tsx
import { Effect } from 'postprocessing';
import { Uniform } from 'three';
import { forwardRef, useMemo } from 'react';

class ColorShiftEffect extends Effect {
  constructor({ shift = 0.0 }) {
    super('ColorShiftEffect', /* glsl */`
      uniform float shift;

      void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
        vec3 color = inputColor.rgb;
        float hueShift = shift * uv.x;
        color.r = color.r * cos(hueShift) - color.g * sin(hueShift);
        color.g = color.r * sin(hueShift) + color.g * cos(hueShift);
        outputColor = vec4(color, inputColor.a);
      }
    `, {
      uniforms: new Map([['shift', new Uniform(shift)]])
    });
  }

  set shift(value) {
    this.uniforms.get('shift').value = value;
  }
}

const ColorShift = forwardRef(({ shift = 0 }, ref) => {
  const effect = useMemo(() => new ColorShiftEffect({ shift }), []);
  useEffect(() => { effect.shift = shift; }, [shift, effect]);
  return <primitive ref={ref} object={effect} />;
});
```

### Custom Effect with Time

```tsx
class PulseEffect extends Effect {
  constructor() {
    super('PulseEffect', /* glsl */`
      uniform float uTime;
      uniform float uIntensity;

      void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
        float pulse = sin(uTime * 2.0) * 0.5 + 0.5;
        float vignette = 1.0 - length(uv - 0.5) * pulse * uIntensity;
        outputColor = vec4(inputColor.rgb * vignette, inputColor.a);
      }
    `, {
      uniforms: new Map([
        ['uTime', new Uniform(0)],
        ['uIntensity', new Uniform(0.5)]
      ])
    });
  }

  update(renderer, inputBuffer, deltaTime) {
    this.uniforms.get('uTime').value += deltaTime;
  }
}
```

## Render Targets

### Manual Render Target Management

```tsx
import { useFBO } from '@react-three/drei';

function CustomRenderPipeline() {
  const { gl, scene, camera } = useThree();
  const targetA = useFBO({ width: 1024, height: 1024 });

  useFrame(() => {
    gl.setRenderTarget(targetA);
    gl.render(scene, camera);
    gl.setRenderTarget(null);
    gl.render(scene, camera);
  });

  return null;
}
```

## Performance Patterns

### Resolution Scaling

```tsx
function ScaledEffects() {
  const { size } = useThree();
  const scale = 0.5;

  return (
    <EffectComposer frameBufferType={HalfFloatType} multisampling={0}>
      <Bloom intensity={1.5} width={size.width * scale} height={size.height * scale} />
    </EffectComposer>
  );
}
```

### Adaptive Quality

```tsx
import { useDetectGPU } from '@react-three/drei';

function AdaptiveQuality() {
  const { tier } = useDetectGPU();

  const quality = useMemo(() => {
    if (tier >= 3) return { multisampling: 8, bloomLevels: 8 };
    if (tier >= 2) return { multisampling: 4, bloomLevels: 5 };
    return { multisampling: 0, bloomLevels: 3 };
  }, [tier]);

  return (
    <EffectComposer multisampling={quality.multisampling}>
      <Bloom levels={quality.bloomLevels} />
    </EffectComposer>
  );
}
```

## Temporal Collapse Setup

```tsx
import { EffectComposer, Bloom, ChromaticAberration, Vignette, Noise, ToneMapping } from '@react-three/postprocessing';
import { ToneMappingMode, BlendFunction } from 'postprocessing';
import { HalfFloatType } from 'three';

function TemporalCollapseComposer({ children }) {
  return (
    <EffectComposer multisampling={4} frameBufferType={HalfFloatType}>
      <ToneMapping mode={ToneMappingMode.ACES_FILMIC} />
      <Bloom luminanceThreshold={0.15} luminanceSmoothing={0.9} intensity={2.0} radius={0.85} mipmapBlur />
      <ChromaticAberration offset={[0.002, 0.001]} radialModulation modulationOffset={0.3} />
      <Vignette darkness={0.6} offset={0.25} />
      <Noise opacity={0.025} blendFunction={BlendFunction.OVERLAY} />
      {children}
    </EffectComposer>
  );
}
```

## Reference

- See `postfx-bloom` for bloom-specific techniques
- See `postfx-effects` for individual effect configurations
- See `shaders-glsl` for writing custom effect shaders
