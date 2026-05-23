---
name: dev-r3f-r3f-fundamentals
description: React Three Fiber core patterns for scene composition and game loop
category: r3f
---

# R3F Fundamentals

> "Declarative 3D – compose scenes like React components."

## When to Use This Skill

Use when:
- Setting up a new R3F scene
- Creating 3D components
- Implementing game loops with `useFrame`
- Managing canvas and renderer settings

## Quick Start

```tsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';

function App() {
  return (
    <Canvas camera={{ position: [0, 5, 10], fov: 50 }}>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <mesh>
        <boxGeometry />
        <meshStandardMaterial color="orange" />
      </mesh>
      <OrbitControls />
    </Canvas>
  );
}
```

## Decision Framework

| Need            | Use                                           |
| --------------- | --------------------------------------------- |
| Basic 3D scene  | `<Canvas>` with mesh + geometry + material    |
| Camera controls | `<OrbitControls>` or custom camera rig        |
| Animation loop  | `useFrame` hook                               |
| Access Three.js | `useThree` hook                               |
| Load assets     | `useLoader` or `<Suspense>` with drei loaders |
| Performance     | `<Instances>`, LOD, or `useInstancedMesh`     |

## Progressive Guide

### Level 1: Basic Components

```tsx
// Simple mesh component
export function Box({ position = [0, 0, 0] }) {
  return (
    <mesh position={position}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="royalblue" />
    </mesh>
  );
}
```

### Level 2: Animation with useFrame

```tsx
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';

export function SpinningBox() {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta;
      meshRef.current.rotation.y += delta * 0.5;
    }
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial color="hotpink" />
    </mesh>
  );
}
```

### Level 3: Accessing Three.js State

```tsx
import { useThree } from '@react-three/fiber';

export function CameraLogger() {
  const { camera, gl, scene, size } = useThree();

  useFrame(() => {
    // Access camera position
    console.log(camera.position.toArray());
  });

  return null;
}
```

### Level 4: Game Loop Pattern

```tsx
import { useGameStore } from '@/store/gameStore';

export function GameLoop() {
  const { phase, updatePhase } = useGameStore();

  useFrame((state, delta) => {
    // Fixed timestep update
    const fixedDelta = Math.min(delta, 1 / 30);

    // Update game logic
    updatePhase(fixedDelta);
  });

  return null;
}
```

### Level 5: Performance Optimization

```tsx
import { Instances, Instance } from '@react-three/drei';

export function ManyBoxes({ count = 1000 }) {
  return (
    <Instances limit={count}>
      <boxGeometry />
      <meshStandardMaterial />
      {Array.from({ length: count }, (_, i) => (
        <Instance
          key={i}
          position={[Math.random() * 100 - 50, Math.random() * 100 - 50, Math.random() * 100 - 50]}
        />
      ))}
    </Instances>
  );
}
```

## Anti-Patterns

**DON'T:**

- Create new objects inside `useFrame` (causes GC pressure)
- Use `useState` for rapidly changing values (use refs instead)
- Import entire Three.js (`import * as THREE`)
- Forget to dispose of geometries and materials
- Use `position={[x, y, z]}` with changing values (creates new array each render)
- **Use manual loaders like `FBXLoader.load()` in `useEffect`** – breaks R3F's suspense system

**DO:**

- Reuse Vector3/Quaternion instances in useFrame
- Use refs for animation state
- Import specific Three.js classes
- Clean up in useEffect return
- Use `position-x`, `position-y`, `position-z` for animated values
- **Use drei hooks (`useFBX`, `useGLTF`) for model loading** – integrates with R3F suspense

## Code Patterns

### Reusable Vector Pattern

```tsx
const tempVec = new THREE.Vector3();

function MovingObject() {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    tempVec.set(Math.sin(state.clock.elapsedTime), 0, Math.cos(state.clock.elapsedTime));
    meshRef.current?.position.copy(tempVec);
  });

  return <mesh ref={meshRef}>...</mesh>;
}
```

### Conditional Rendering

```tsx
function ConditionalMesh({ visible }) {
  // Don't render if not visible - saves GPU
  if (!visible) return null;

  return <mesh>...</mesh>;
}
```

### FBX Model Loading Pattern

```tsx
import { useFBX } from '@react-three/drei';
import { Suspense } from 'react';

// ❌ WRONG - Manual loading breaks R3F suspense
// useEffect(() => {
//   new FBXLoader().load(url, (obj) => setFbx(obj));
// }, [url]);

// ✅ CORRECT - Use drei's useFBX hook
function CharacterModel({ url }: { url: string }) {
  const fbx = useFBX(url);
  return <primitive object={fbx} />;
}

// Wrap in Suspense for loading states
function Scene() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <CharacterModel url="/models/character.fbx" />
    </Suspense>
  );
}
```

## Checklist

Before implementing R3F component:

- [ ] Using refs for animated values (not useState)
- [ ] Not creating objects inside useFrame
- [ ] Proper cleanup in useEffect
- [ ] Using appropriate drei helpers
- [ ] Canvas has proper camera settings
- [ ] Lighting is set up correctly
- [ ] For FBX/GLTF models: using `useFBX`/`useGLTF` from drei (not manual loaders)

## Reference

- [drei documentation](https://github.com/pmndrs/drei) — Helper components
- [R3F documentation](https://docs.pmnd.rs/react-three-fiber) — Official docs
- [dev-r3f-r3f-physics](../dev-r3f-r3f-physics/SKILL.md) — Physics integration
- [dev-r3f-r3f-materials](../dev-r3f-r3f-materials/SKILL.md) — Materials and shaders

## Zustand + R3F Integration (NEW - 2026-01-28)

**State management for R3F scenes using Zustand with vanilla pattern.**

### Why Zustand for R3F

- **Zero boilerplate** - No wrapper components needed
- **Bundle efficient** - R3F already uses Zustand internally
- **TypeScript friendly** - Excellent type inference
- **DevTools support** - Easy state inspection

### Store Structure Pattern

```typescript
// src/store/types.ts - Shared types
export interface Vector3Like {
  x: number;
  y: number;
  z: number;
}

export interface PlayerState {
  position: Vector3Like;
  rotation: number;
  health: number;
  weapon: string;
}
```

```typescript
// src/store/playerStore.ts - Vanilla Zustand (no React dependencies)
import { mutate } from 'zustand/mutate';
import type { PlayerState, Vector3Like } from './types';

interface PlayerStore {
  state: PlayerState;
  setPosition: (position: Vector3Like) => void;
  setHealth: (health: number) => void;
  reset: () => void;
}

const initialState: PlayerState = {
  position: { x: 0, y: 0, z: 0 },
  rotation: 0,
  health: 100,
  weapon: 'blaster',
};

export const usePlayerStore = create<PlayerStore>((set) => ({
  state: initialState,
  setPosition: (position) =>
    set((store) => ({
      state: mutate(store.state, { position }),
    })),
  setHealth: (health) =>
    set((store) => ({
      state: mutate(store.state, { health }),
    })),
  reset: () => set({ state: initialState }),
}));
```

### R3F Component Integration

```tsx
// src/components/player/Player.tsx
import { usePlayerStore } from '@/store/playerStore';
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';

export function Player() {
  const { state, setPosition } = usePlayerStore();
  const meshRef = useRef<THREE.Mesh>(null);

  // Sync store position to mesh
  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.position.set(
        state.position.x,
        state.position.y,
        state.position.z
      );
    }
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[1, 2, 1]} />
      <meshStandardMaterial color="orange" />
    </mesh>
  );
}
```

### DevTools Setup

```typescript
// src/store/playerStore.ts
import { devtools } from 'zustand/middleware';

export const usePlayerStore = create<PlayerStore>()(
  devtools(
    (set) => ({
      state: initialState,
      // ... actions
    }),
    { name: 'PlayerStore' }
  )
);
```

### Anti-Patterns

❌ **DON'T:**
- Put React hooks inside store files (breaks vanilla pattern)
- Use `setState` directly in `useFrame` (causes infinite loops)
- Create new objects in store actions (use `mutate` from zustand/mutate)

✅ **DO:**
- Keep store files vanilla (no React imports)
- Use selectors for specific state slices
- Expose stores to `window.__ZUSTAND__` for debugging

### Testing Pattern

```typescript
// src/tests/store/playerStore.test.ts
import { renderHook, act } from '@testing-library/react';
import { usePlayerStore } from '@/store/playerStore';

describe('playerStore', () => {
  it('updates position', () => {
    const { result } = renderHook(() => usePlayerStore());

    act(() => {
      result.current.setPosition({ x: 10, y: 0, z: 5 });
    });

    expect(result.current.state.position).toEqual({ x: 10, y: 0, z: 5 });
  });
});
```

**Sources:**
- https://docs.pmnd.rs/zustand/guides/typescript
- https://github.com/pmndrs/zustand
- **Learned from arch-002 retrospective (2026-01-28)**

## TPS Camera Reference Values

**Validated working camera distances from feat-tps-003 (2026-01-27):**

| Mode         | Distance Value | Character Framing | Notes                          |
| ------------ | -------------- | ----------------- | ------------------------------ |
| Hipfire      | 3.5 units       | 30-40% of screen   | Character waist up visible    |
| Aim (ADS)    | 1.5 units       | Closer view       | For precision shooting         |

These values provide proper TPS (Third-Person Shooter) framing where the character is clearly visible on the left side of the screen with enough surrounding context.

## TPS Camera Shoulder Offset (feat-tps-004, 2026-01-27)

**⚠️ CRITICAL: Over-the-shoulder view requires BOTH position offset AND look-at offset.**

| Parameter          | Value (left shoulder view) | Notes                              |
| ------------------ | ------------------------- | ---------------------------------- |
| shoulderOffsetRight | 0.75 units                 | Camera position offset (right)     |
| shoulderOffsetLeft  | -0.75 units                | Camera position offset (left)      |
| look-at offset      | Same as position offset    | Often missed - REQUIRED for proper composition |

**Common anti-pattern from feat-tps-004:**
- ❌ Camera position offset but look-at at center (0, 0, 0)
- ✅ Look-at point must ALSO be offset by same shoulder amount

**Example implementation:**
```tsx
// Position offset (standard)
const _vec3_position = new Vector3(0, 1.6, 3.5)
  .add(_vec3_right.clone().multiplyScalar(shoulderOffset));

// Look-at offset (CRITICAL - often missed)
const _vec3_lookAt = targetPosition.clone()
  .add(_vec3_right.clone().multiplyScalar(shoulderOffset));

camera.position.copy(_vec3_position);
camera.lookAt(_vec3_lookAt);
```

**Acceptance criteria validation:**
- Exact numerical values must match acceptance criteria (0.75, not 0.85)
- Add code comments referencing acceptance criteria values
- E2E tests required for camera validation (20+ tests covering offset, distance, swap)

---

## UI Design System Integration for R3F (Added: ui-001 Playtest)

**Learned from ui-001:** Functional UI is insufficient - requires design system with tokens, aspect ratio, and professional styling.

### Design Token System Pattern

```typescript
// src/components/ui/tokens.ts - Single source of truth for UI values
export const UITokens = {
  // Base resolution for all calculations
  base: {
    width: 1920,
    height: 1080,
    aspectRatio: 16 / 9,
  },

  // Spacing scale (8px base unit)
  spacing: {
    xs: '8px',
    sm: '16px',
    md: '24px',
    lg: '32px',
    xl: '48px',
    xxl: '64px',
  },

  // Typography
  fontSize: {
    xs: '14px',
    sm: '16px',
    base: '18px',
    lg: '24px',
    xl: '32px',
    '2xl': '48px',
    '3xl': '64px',
    display: '128px',
  },

  // Get responsive scale factor
  getScale(windowWidth: number, windowHeight: number): number {
    const scale = Math.min(
      windowWidth / this.base.width,
      windowHeight / (this.base.width * 9 / 16)
    );
    return Math.max(0.5, Math.min(2, scale));
  },
};
```

### 16:9 Aspect Ratio Container Pattern

```tsx
// src/components/ui/AspectContainer.tsx
import React, { useEffect, useState } from 'react';

export function AspectContainer({ children }: { children: React.ReactNode }) {
  const [scale, setScale] = useState(1);

  useEffect(() => {
    const updateScale = () => {
      const s = UITokens.getScale(window.innerWidth, window.innerHeight);
      setScale(s);
    };

    updateScale();
    window.addEventListener('resize', updateScale);
    return () => window.removeEventListener('resize', updateScale);
  }, []);

  return (
    <div className="fixed inset-0 z-10 flex items-center justify-center bg-black">
      <div
        className="relative overflow-hidden"
        style={{
          aspectRatio: 16 / 9,
          transform: `scale(${scale})`,
          transformOrigin: 'center',
        }}
      >
        {children}
      </div>
    </div>
  );
}
```

### Using Design Tokens in Components

```tsx
import { UITokens } from '@/components/ui/tokens';

export function GameButton({ children, onClick }) {
  return (
    <motion.button
      onClick={onClick}
      style={{
        padding: UITokens.spacing.md,
        fontSize: UITokens.fontSize.lg,
        // Use token colors, not hardcoded values
        background: 'var(--color-primary-500)',
      }}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.97 }}
    >
      {children}
    </motion.button>
  );
}
```

### CSS Variables Approach (Recommended)

```css
/* src/index.css - Define CSS variables for design tokens */
:root {
  /* Base dimensions */
  --ui-base-width: 1920px;
  --ui-base-height: 1080px;
  --ui-aspect-ratio: 16 / 9;

  /* Spacing scale */
  --spacing-xs: 8px;
  --spacing-sm: 16px;
  --spacing-md: 24px;
  --spacing-lg: 32px;

  /* Typography */
  --font-display: 'Orbitron', sans-serif;
  --font-ui: 'Rajdhani', sans-serif;

  /* Colors - Orange/Cyan theme */
  --color-primary: #f97316;
  --color-secondary: #06b6d4;
  --color-metal-900: #0a0a0a;
  --color-metal-700: #262626;

  /* Glow effects */
  --glow-primary: rgba(249, 115, 22, 0.6);
}
```

### Button Component with Design System

```tsx
// src/components/ui/Button.tsx - Production-ready button
import { motion } from 'framer-motion';
import { UITokens } from './tokens';

interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
}: ButtonProps) {
  const sizeStyles = {
    sm: { height: '48px', padding: '0 24px', fontSize: UITokens.fontSize.sm },
    md: { height: '64px', padding: '0 32px', fontSize: UITokens.fontSize.lg },
    lg: { height: '80px', padding: '0 48px', fontSize: UITokens.fontSize.xl },
  };

  return (
    <motion.button
      className={`button button-${variant}`}
      style={sizeStyles[size]}
      onClick={onClick}
      whileHover={{ scale: 1.05, x: -4 }}
      whileTap={{ scale: 0.97, x: 2 }}
      transition={{
        type: 'spring',
        stiffness: 400,
        damping: 17,
      }}
    >
      {children}
    </motion.button>
  );
}
```

### Easing Curves for Game UI

```typescript
// src/components/ui/easing.ts
export const GameEasing = {
  snap: [0.22, 1, 0.36, 1] as const,
  reveal: [0.16, 1, 0.3, 1] as const,
  bounce: [0.34, 1.56, 0.64, 1] as const,
  press: [0.4, 0, 0.2, 1] as const,
};

// Usage with Framer Motion
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.4, ease: GameEasing.snap }}
/>
```

### R3F Canvas Integration with UI

```tsx
// App.tsx - Layered architecture
export function App() {
  return (
    <>
      {/* 3D Scene Layer */}
      <Canvas>
        <ambientLight />
        <GameScene />
      </Canvas>

      {/* UI Layer - 16:9 container ensures consistent layout */}
      <AspectContainer>
        <HUD />
      </AspectContainer>
    </>
  );
}
```

**Sources:**
- [React Three Fiber Aspect Ratio Discussion](https://github.com/pmndrs/react-three-fiber/discussions/711)
- [Framer Motion Easing Functions](https://motion.dev/docs/easing-functions)
- [The Easing Blueprint](https://www.reubence.com/articles/the-easing-blueprint)
- **Learned from ui-001 playtest (2026-01-28)**
