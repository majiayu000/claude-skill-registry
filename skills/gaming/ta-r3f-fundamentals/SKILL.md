---
name: ta-r3f-fundamentals
description: React Three Fiber core patterns for scene composition and game loop. Use when setting up R3F scenes, creating 3D components, implementing game loops.
category: r3f
---

# R3F Fundamentals Skill

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

❌ **DON'T:**

- Create new objects inside `useFrame` (causes GC pressure)
- Use `useState` for rapidly changing values (use refs instead)
- Import entire Three.js (`import * as THREE`)
- Forget to dispose of geometries and materials
- Use `position={[x, y, z]}` with changing values (creates new array each render)

✅ **DO:**

- Reuse Vector3/Quaternion instances in useFrame
- Use refs for animation state
- Import specific Three.js classes
- Clean up in useEffect return
- Use `position-x`, `position-y`, `position-z` for animated values

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

## Rendering Best Practices

### Depth Testing and Z-Fighting Prevention

**Z-fighting** (flickering between overlapping surfaces) occurs when two objects occupy the same depth or when depth testing is misconfigured.

```tsx
// ❌ WRONG - Causes flickering due to improper depth configuration
<mesh>
  <boxGeometry />
  <meshStandardMaterial color="blue" />
</mesh>

// ✅ CORRECT - Proper depth configuration for character models
<mesh renderOrder={10}>
  <boxGeometry />
  <meshStandardMaterial
    color="blue"
    depthTest={true}
    depthWrite={true}
  />
</mesh>
```

**Key Properties:**

| Property    | Type    | Purpose                              |
| ----------- | ------- | ------------------------------------ |
| `renderOrder` | number | Controls render order (higher = later) |
| `depthTest`  | boolean | Enable/disable depth buffer testing  |
| `depthWrite` | boolean | Enable/disable depth buffer writing |

**When to use:**

- **Character models**: `renderOrder={10}`, `depthTest={true}`, `depthWrite={true}`
- **Spawn points/overlays**: `renderOrder={10}`, `depthTest={true}`, `depthWrite={true}`
- **Transparent objects**: `renderOrder={1}`, `depthWrite={false}`, `transparent={true}`
- **Opaque geometry**: Default settings usually work

**Learned from bugfix-004 retrospective (2026-01-22):**
Flickering on character and spawn point models was resolved by setting `renderOrder=10`, `depthWrite=true`, and `depthTest=true`. This ensures proper Z-buffering and prevents depth conflicts.

### Material Rendering Order

```tsx
// For layered materials (e.g., character with equipment)
<CharacterModel renderOrder={10} />        // Renders last (on top)
<BodyArmor renderOrder={5} />
<Underlay renderOrder={0} />               // Renders first
```

## Checklist

Before implementing R3F component:

- [ ] Using refs for animated values (not useState)
- [ ] Not creating objects inside useFrame
- [ ] Proper cleanup in useEffect
- [ ] Using appropriate drei helpers
- [ ] Canvas has proper camera settings
- [ ] Lighting is set up correctly
- [ ] Depth testing configured for layered meshes (renderOrder, depthTest, depthWrite)
- [ ] No z-fighting visible on overlapping surfaces

## Related Skills

For materials: `Skill("ta-r3f-materials")`
For performance: `Skill("ta-r3f-performance")`
For physics: `Skill("ta-r3f-physics")`

## External References

- [drei documentation](https://github.com/pmndrs/drei) — Helper components
- [R3F documentation](https://docs.pmnd.rs/react-three-fiber) — Official docs

---

## State-Driven Visual Updates (NEW - 2026-01-28)

**Connecting game state to visual updates in R3F using Zustand selectors.**

### Pattern: Selective Re-renders

```tsx
// ❌ WRONG - Entire component re-renders on ANY state change
import { useGameStore } from '@/store/gameStore';

function HealthBar() {
  const { player, match, ui } = useGameStore(); // Unnecessary dependencies
  return <mesh scale={{ x: player.health / 100 }}>{/* ... */}</mesh>;
}

// ✅ CORRECT - Only re-renders when player.health changes
function HealthBar() {
  const health = useGameStore((state) => state.player.health);
  return <mesh scale={{ x: health / 100 }}>{/* ... */}</mesh>;
}
```

### Performance Pattern: useShallow

```tsx
import { useShallow } from '@/store/useShallow';
import { usePlayerStore } from '@/store/playerStore';

// Multiple related values - use shallow comparison
function PlayerStatus() {
  const { health, armor, weapon } = usePlayerStore(
    useShallow((state) => ({
      health: state.health,
      armor: state.armor,
      weapon: state.weapon,
    }))
  );
  // Only re-renders if health, armor, or weapon change
}
```

### Visual State Synchronization

```tsx
// State-driven material properties
function DamageIndicator() {
  const isDamaged = usePlayerStore((state) => state.health < 50);

  return (
    <mesh>
      <meshStandardMaterial
        color={isDamaged ? 'red' : 'blue'}
        emissive={isDamaged ? 'red' : undefined}
        emissiveIntensity={isDamaged ? 0.5 : 0}
      />
    </mesh>
  );
}

// State-driven animation
function PulsingEffect({ active }: { active: boolean }) {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    if (!meshRef.current || !active) return;
    const scale = 1 + Math.sin(clock.elapsedTime * 5) * 0.1;
    meshRef.current.scale.setScalar(scale);
  });

  return <sphereGeometry ref={meshRef} args={[0.5, 16, 16]} />;
}
```

### Anti-Patterns for State-Driven Visuals

❌ **DON'T:**
- Subscribe to entire store when only using one value
- Call setState inside useFrame (infinite loop)
- Update state on every frame (performance issue)
- Use deep selectors without memoization

✅ **DO:**
- Use specific selectors for each value
- Batch visual updates before state commits
- Use shallow comparison for multiple values
- Keep visual state separate from game state when possible

### State-Driven Texture Changes

```tsx
function WeaponModel() {
  const weaponType = usePlayerStore((state) => state.weapon);

  const textures = {
    blaster: useTexture('/weapons/blaster.png'),
    rocket: useTexture('/weapons/rocket.png'),
  };

  return (
    <mesh>
      <meshStandardMaterial map={textures[weaponType]} />
    </mesh>
  );
}
```

**Sources:**
- https://docs.pmnd.rs/zustand/guides/performance
- **Learned from arch-002 retrospective (2026-01-28)**
