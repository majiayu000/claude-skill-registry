---
name: ta-ui-debug-helpers
description: Debug visualization helpers using drei and Three.js. Use when adding debug gizmos, visual helpers, diagnostics.
category: ui
---

# Visual Debug Helpers Skill

> "Visual debugging saves hours – see what's happening, not guess."

## When to Use This Skill

Use **during development and debugging** to visualize:
- Input direction vectors
- Collision bounds
- Physics bodies
- Camera frustums
- Light coverage
- Player positions

## Quick Start

```bash
# Install drei if not present
npm install @react-three/drei

# Enable debug mode in gameStore
store.setDebugMode('input')  // Shows input helpers
store.setDebugMode('physics') // Shows physics bodies
store.setDebugMode('all')     // Shows everything
```

## The Debug Visualization Stack

```
┌─────────────────────────────────────────────────────────┐
│                    Debug Mode Toggle                    │
├─────────────┬─────────────┬─────────────┬───────────────┤
│ Input Arrow │ Bounding Box│ Gizmos      │ Stats         │
│ (Direction) │ (Colliders) │ (Transform) │ (FPS/Memory)  │
└─────────────┴─────────────┴─────────────┴───────────────┘
```

## Essential Helpers from @react-three/drei

### 1. ArrowHelper (Input Direction)

Visualize player input direction:

```typescript
import { ArrowHelper } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

function InputDebug({ direction }: { direction: Vector3 }) {
  return (
    <ArrowHelper
      dir={direction.clone().normalize()}
      origin={[0, 0, 0]}
      length={2}
      color={0x00ff00}
      headLength={0.2}
      headWidth={0.1}
    />
  );
}
```

### 2. BoundingBox (Colliders)

Show physics/collision bounds:

```typescript
import { BoundingBox, useHelper } from '@react-three/drei';
import { useRef } from 'react';

function PhysicsDebug({ children }: { children: React.ReactNode }) {
  const ref = useRef<Object3D>(null);

  return (
    <group ref={ref}>
      <BoundingBox
        wireframe
        color={0xff0000}
        opacity={0.3}
      >
        {children}
      </BoundingBox>
    </group>
  );
}
```

### 3. GridHelper (World Reference)

Show ground plane for position reference:

```typescript
import { Grid } from '@react-three/drei';

<Grid
  args={[100, 100]}  // Size, divisions
  cellColor="#6f6f6f"
  sectionColor="#9d4b4b"
  position={[0, -0.01, 0]}  // Slightly below zero
/>;
```

### 4. CameraHelper (View Frustum)

Visualize camera view:

```typescript
import { useHelper, CameraHelper } from '@react-three/drei';
import { PerspectiveCamera } from '@react-three/diber';

function DebugCamera() {
  const cameraRef = useRef<PerspectiveCamera>(null);
  useHelper(cameraRef, CameraHelper, 'cyan');

  return <perspectiveCamera ref={cameraRef} />;
}
```

### 5. PositionalAudioHelper (Sound Debug)

Visualize 3D audio range:

```typescript
import { PositionalAudioHelper } from '@react-three/drei';

<PositionalAudioHelper
  audio={audioRef}
  size={1}  // Helper scale
  color="#ff0000"
/>;
```

### 6. Stats (Performance Monitor)

Show FPS and memory:

```typescript
import { Stats } from '@react-three/drei';

<Stats
  className="stats-position"
  showGraph={true}
/>;
```

## Progressive Guide

### Level 1: Input Direction Debug

Create an input arrow that shows where player is trying to move:

```typescript
// components/debug/InputDirectionDebug.tsx
import { useAtom } from 'jotai';
import { debugModeAtom } from '@/store/debugStore';
import { ArrowHelper } from '@react-three/drei';

export function InputDirectionDebug({ inputDirection }: { inputDirection: Vector3 }) {
  const [debugMode] = useAtom(debugModeAtom);

  if (debugMode !== 'input' && debugMode !== 'all') return null;

  return (
    <>
      {/* Green arrow for input direction */}
      <ArrowHelper
        dir={inputDirection.clone().normalize()}
        origin={[0, 1, 0]}
        length={2}
        color={0x00ff00}
        headLength={0.2}
        headWidth={0.1}
      />

      {/* Blue arrow for camera forward */}
      <ArrowHelper
        dir={[0, 0, -1]}
        origin={[0, 1, 0]}
        length={2}
        color={0x0000ff}
        headLength={0.2}
        headWidth={0.1}
      />
    </>
  );
}
```

### Level 2: Physics Body Debug

Show collider boundaries:

```typescript
// components/debug/PhysicsDebug.tsx
import { CapsuleCollider, RigidBody } from '@react-three/rapier';
import { useHelper } from '@react-three/drei';
import { useRef } from 'react';

export function PhysicsDebug({ enabled }: { enabled: boolean }) {
  const colliderRef = useRef<Object3D>(null);

  useHelper(colliderRef, enabled ? BoxHelper : null, 'red');

  return (
    <RigidBody colliders={false}>
      <CapsuleCollider ref={colliderRef} args={[0.5, 1]} />
    </RigidBody>
  );
}
```

### Level 3: Scene Overview

Add omniscient camera for debugging:

```typescript
// components/debug/DebugCamera.tsx
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';

export function DebugCamera() {
  return (
    <>
      <PerspectiveCamera
        makeDefault
        position={[10, 10, 10]}
        fov={50}
      />
      <OrbitControls
        makeDefault
        enablePan={true}
        enableZoom={true}
        enableRotate={true}
      />
    </>
  );
}
```

### Level 4: Custom Gizmos

Create custom debug markers:

```typescript
// components/debug/SphereMarker.tsx
import { Sphere, MeshBasicMaterial } from '@react-three/drei';

export function SphereMarker({
  position,
  color = '#ff0000',
  size = 0.2,
}: {
  position: [number, number, number];
  color?: string;
  size?: number;
}) {
  return (
    <Sphere args={[size, 16, 16]} position={position}>
      <meshBasicMaterial color={color} wireframe />
    </Sphere>
  );
}

// Usage: Mark spawn points, cover positions, etc.
<SphereMarker position={spawnPoint} color="#00ff00" />;
<SphereMarker position={enemyPosition} color="#ff0000" />;
```

## Debug Store Pattern

Create centralized debug state:

```typescript
// store/debugStore.ts
import { atom } from 'jotai';

export type DebugMode = 'none' | 'input' | 'physics' | 'colliders' | 'all';

export const debugModeAtom = atom<DebugMode>('none');
export const showFPSAtom = atom<boolean>(false);
export const showWireframesAtom = atom<boolean>(false);
export const showGridAtom = atom<boolean>(false);

// UI Component
export function DebugPanel() {
  const [debugMode, setDebugMode] = useAtom(debugModeAtom);
  const [showFPS, setShowFPS] = useAtom(showFPSAtom);

  return (
    <div className="debug-panel">
      <h3>Debug Mode</h3>
      <select value={debugMode} onChange={(e) => setDebugMode(e.target.value as DebugMode)}>
        <option value="none">None</option>
        <option value="input">Input Direction</option>
        <option value="physics">Physics Bodies</option>
        <option value="colliders">Colliders</option>
        <option value="all">All</option>
      </select>

      <label>
        <input type="checkbox" checked={showFPS} onChange={(e) => setShowFPS(e.target.checked)} />
        Show FPS
      </label>
    </div>
  );
}
```

## Debug Color Convention

| Use Case | Color | Hex |
|----------|-------|-----|
| Input direction | Green | 0x00ff00 |
| Camera forward | Blue | 0x0000ff |
| Colliders/Obstacles | Red | 0xff0000 |
| Friendly units | Cyan | 0x00ffff |
| Enemy units | Orange | 0xff8800 |
| Spawn points | Yellow | 0xffff00 |
| Cover positions | Purple | 0xff00ff |

## Keyboard Toggles

Add hotkeys for quick debug access:

```typescript
// hooks/useDebugHotkeys.ts
import { useEffect } from 'react';
import { useSetAtom } from 'jotai';
import { debugModeAtom } from '@/store/debugStore';

export function useDebugHotkeys() {
  const setDebugMode = useSetAtom(debugModeAtom);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Shift + D toggles debug modes
      if (e.shiftKey && e.key === 'D') {
        setDebugMode((prev) => {
          const modes: DebugMode[] = ['none', 'input', 'physics', 'all'];
          const idx = modes.indexOf(prev);
          return modes[(idx + 1) % modes.length];
        });
      }

      // Shift + G toggles grid
      if (e.shiftKey && e.key === 'G') {
        setShowGrid((prev) => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [setDebugMode]);
}
```

## Anti-Patterns

❌ **DON'T:**

- Leave debug helpers enabled in production
- Use expensive helpers in hot loops
- Hardcode debug state (use a store)
- Create debug geometry manually (use helpers)

✅ **DO:**

- Wrap debug components in conditional rendering
- Use `process.env.NODE_ENV` checks
- Create reusable debug components
- Use helpers from @react-three/drei

## Production Safety

```typescript
// Never render debug in production
const isDev = process.env.NODE_ENV === 'development';

if (!isDev) return null;

// Or use explicit flag
const ENABLE_DEBUG = import.meta.env.VITE_ENABLE_DEBUG === 'true';
```

## Checklist

When adding debug visualization:

- [ ] Helper wrapped in debug mode check
- [ ] Disabled in production builds
- [ ] Color follows convention
- [ ] Keyboard toggle available
- [ ] Performance acceptable (< 1 FPS impact)
- [ ] Clean up helpers on unmount

## Related Skills

For UI polish: `Skill("ta-ui-polish")`

## External References

- [@react-three/drei Helpers](https://github.com/pmndrs/drei#helpers)
- [Three.js Helpers](https://threejs.org/docs/#api/en/helpers/)
- [React Three Fiber Debug](https://docs.pmnd.rs/react-three-fiber/debugging)
