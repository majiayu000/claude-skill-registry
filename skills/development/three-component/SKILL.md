---
name: three-component
description: Create a React Three Fiber 3D component for the Kardashev Network visualization
disable-model-invocation: true
argument-hint: "<ComponentName>"
---

# Create React Three Fiber Component

Create a new 3D component: **$ARGUMENTS**

## Project 3D Architecture (from IMPLEMENTATION_CHECKLIST.md)

```
src/components/three/
├── SunScene.tsx           # Main R3F canvas + scene setup
├── Sun.tsx                # 3D sun with corona shader
├── EnergyParticles.tsx    # Particle system for energy rays
├── CloudLayer.tsx         # Animated cloud coverage
├── Ground.tsx             # Ground plane receiving energy
├── InteractiveCamera.tsx  # Mouse parallax camera controls
└── StatsOverlay.tsx       # Click-to-reveal energy stats
```

## R3F Component Template

```tsx
// src/components/three/ComponentName.tsx
import React, { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

interface ComponentNameProps {
  // Data-driven props
  intensity?: number;
  color?: string;
  // Position/transform props
  position?: [number, number, number];
  scale?: number;
}

export function ComponentName({
  intensity = 1,
  color = "#ffffff",
  position = [0, 0, 0],
  scale = 1,
}: ComponentNameProps) {
  const meshRef = useRef<THREE.Mesh>(null);

  // Animation loop
  useFrame((state, delta) => {
    if (meshRef.current) {
      // Example: rotate based on time
      meshRef.current.rotation.y += delta * 0.5;
    }
  });

  return (
    <mesh ref={meshRef} position={position} scale={scale}>
      <sphereGeometry args={[1, 32, 32]} />
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={intensity} />
    </mesh>
  );
}
```

## Scene Setup Template

```tsx
// src/components/three/SunScene.tsx
import React, { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Environment } from "@react-three/drei";
import { EffectComposer, Bloom } from "@react-three/postprocessing";

interface SunSceneProps {
  ghi: number;        // Solar irradiance W/m²
  cloudCover: number; // 0-100%
  isDay: boolean;
}

export function SunScene({ ghi, cloudCover, isDay }: SunSceneProps) {
  return (
    <Canvas camera={{ position: [0, 0, 10], fov: 50 }}>
      <Suspense fallback={null}>
        <ambientLight intensity={0.2} />
        <pointLight position={[0, 0, 0]} intensity={ghi / 500} />

        {/* 3D Components */}
        <Sun intensity={ghi / 1000} />
        <EnergyParticles density={ghi / 100} />
        <CloudLayer opacity={cloudCover / 100} />
        <Ground />

        {/* Post-processing */}
        <EffectComposer>
          <Bloom luminanceThreshold={0.5} intensity={1.5} />
        </EffectComposer>

        {/* Controls */}
        <OrbitControls enableZoom={false} enablePan={false} />
      </Suspense>
    </Canvas>
  );
}
```

## Data-Driven Animation Bindings

| Data Point | Animation Effect |
|------------|------------------|
| `ghi` (irradiance) | Sun glow intensity, particle density |
| `cloudCover` | Cloud layer opacity, sun dimming |
| `isDay` | Day/night scene transition |
| `currentValue` | Energy beam thickness, particle speed |

## Interactive Features

```tsx
// Mouse parallax example
import { useThree } from "@react-three/fiber";

function InteractiveCamera() {
  const { camera } = useThree();

  useFrame(({ mouse }) => {
    camera.position.x = THREE.MathUtils.lerp(camera.position.x, mouse.x * 2, 0.05);
    camera.position.y = THREE.MathUtils.lerp(camera.position.y, mouse.y * 2, 0.05);
    camera.lookAt(0, 0, 0);
  });

  return null;
}
```

## Performance Guidelines

1. **Limit particle count** - Max 1000 particles on mobile
2. **Use instancing** - `useInstancedMesh` for many similar objects
3. **Lazy load** - Don't block initial render with 3D
4. **Reduce on mobile** - Check `window.innerWidth` for mobile optimizations
5. **Dispose properly** - Clean up geometries/materials in useEffect cleanup

## Checklist

- [ ] Create component in `src/components/three/`
- [ ] Use TypeScript with proper props interface
- [ ] Add `useFrame` for animations
- [ ] Bind visual properties to data props (ghi, cloudCover, etc.)
- [ ] Add proper lighting
- [ ] Consider post-processing effects (Bloom for glow)
- [ ] Test performance on mobile
- [ ] Add fallback for no WebGL support
