---
name: ta-assets-workflow
description: Asset creation pipeline and integration workflow for Tech Artist. Use when creating new 3D/2D assets, importing external models, organizing project assets.
category: asset
---

# Asset Workflow Skill

> "A well-organized asset pipeline saves hours of frustration."

## When to Use This Skill

Use when:

- Creating new 3D/2D assets
- Importing external models
- Organizing project assets
- Setting up asset pipelines

## Asset Directory Structure

```
src/
├── assets/
│   ├── models/          # 3D models (.glb, .gltf)
│   │   ├── characters/
│   │   ├── vehicles/
│   │   ├── props/
│   │   └── environment/
│   ├── textures/        # Texture maps
│   │   ├── color/       # Albedo/diffuse
│   │   ├── normal/      # Normal maps
│   │   ├── roughness/   # Roughness/metalness
│   │   └── emission/    # Emissive/glow
│   ├── audio/           # Sound effects and music
│   │   ├── sfx/
│   │   └── music/
│   ├── shaders/         # GLSL shader files
│   └── fonts/           # Typefaces
└── components/
    └── assets/          # Asset wrapper components
```

## Asset Integration Workflow

### 1. Receive Task

```json
// From PM via current-task-techartist.json (state file)
{
  "id": "vis-002",
  "category": "visual",
  "title": "Vehicle PBR materials",
  "description": "Create realistic car paint materials",
  "acceptanceCriteria": ["Material loads correctly", "Follows art direction"],
  "assetType": "material"
}
```

### 2. Read GDD for Art Direction

**GDD research paths are managed in `ta-router`** - see "GDD Research" section for art direction, color palette, materials, and VFX specifications.

### 3. Request Additional References (if needed)

```json
// Send to Game Designer via message queue
{
  "type": "reference_request",
  "from": "techartist",
  "to": "gamedesigner",
  "payload": {
    "question": "What specific car paint finish? (matte, gloss, metallic)",
    "taskId": "vis-002",
    "assetType": "material"
  }
}
```

### 4. Create Asset

```tsx
// src/components/assets/VehiclePaint.tsx
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export function VehiclePaint({ color = '#FF6B35' }: { color?: string }) {
  const materialRef = useRef<THREE.MeshPhysicalMaterial>(null!);

  useFrame(({ clock }) => {
    // Subtle clearcoat animation
    if (materialRef.current) {
      materialRef.current.clearcoat = 0.8 + Math.sin(clock.elapsedTime * 0.5) * 0.1;
    }
  });

  return (
    <meshPhysicalMaterial
      ref={materialRef}
      color={color}
      metalness={0.9}
      roughness={0.3}
      clearcoat={1.0}
      clearcoatRoughness={0.1}
      envMapIntensity={1.5}
    />
  );
}
```

### 5. Test in Scene

```tsx
// Test component for development
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { VehiclePaint } from './components/assets/VehiclePaint';

function TestScene() {
  return (
    <Canvas camera={{ position: [0, 2, 5] }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <mesh>
        <boxGeometry args={[2, 1, 4]} />
        <VehiclePaint />
      </mesh>
      <OrbitControls />
    </Canvas>
  );
}
```

### 6. Run Feedback Loops

```bash
npm run type-check  # Must pass
npm run lint        # Must pass
npm run build       # Must pass
```

### 7. Commit Work

```bash
git add .
git commit -m "[ralph] [techartist] vis-002: Vehicle PBR materials

- Added metallic paint material with animated clearcoat
- Created reusable VehiclePaint component
- Material follows art direction

PRD: vis-002 | Agent: techartist | Iteration: 1"
```

### 8. Send to QA

```json
// Update current-task-techartist.json state file
{
  "state": {
    "status": "idle",
    "currentTaskId": null,
    "lastSeen": "{ISO_TIMESTAMP}"
  }
}

// Send implementation_complete message to PM
{
  "id": "msg-pm-{timestamp}-001",
  "from": "techartist",
  "to": "pm",
  "type": "implementation_complete",
  "payload": {
    "taskId": "vis-002",
    "success": true,
    "summary": "Asset created and validated"
  }
}
```

## Asset Naming Conventions

| Asset Type | Format                | Example                |
| ---------- | --------------------- | ---------------------- | ------------ |
| Models     | `{Name}_lod{0-3}.glb` | `sportsCar_lod0.glb`   |
| Textures   | `{name}_{type}.{ext}` | `vehicle_color.png`    |
| Materials  | `{Name}Material.tsx`  | `CarPaintMaterial.tsx` |
| Shaders    | `{name}.{vert         | frag}`                 | `water.vert` |
| Components | `{Name}.tsx`          | `VehicleMesh.tsx`      |

## Import Guidelines

```tsx
// ✅ DO: Use lazy loading for large assets
import { useGLTF } from '@react-three/drei';

function Vehicle() {
  const { scene } = useGLTF('/assets/models/vehicles/sportsCar.glb');
  return <primitive object={scene} />;
}

// ✅ DO: Use Suspense for asset loading
import { Suspense } from 'react';

function Scene() {
  return (
    <Suspense fallback={<LoadingIndicator />}>
      <Vehicle />
    </Suspense>
  );
}

// ❌ DON'T: Import large assets at module level
import vehicleModel from './assets/models/vehicle.glb'; // Bad!
```

## Asset Loading States and Patterns

### Progressive Loading with Suspense

**Problem**: Large assets cause long loading times with no feedback.

**Solution**: Use nested Suspense boundaries for progressive loading.

```tsx
import { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { useGLTF } from '@react-three/drei';

function Model({ url }: { url: string }) {
  const { scene } = useGLTF(url);
  return <primitive object={scene} />;
}

function App() {
  return (
    <Suspense fallback={<LoadingScreen />}>
      <Canvas>
        <Suspense fallback={<LowQualityModel />}>
          {/* High quality loads last */}
          <Model url="/assets/models/high-quality.glb" />
        </Suspense>
      </Canvas>
    </Suspense>
  );
}

// Initial low-quality placeholder
function LowQualityModel() {
  const { scene } = useGLTF('/assets/models/low-quality.glb');
  return <primitive object={scene} />;
}
```

### Loading States with useLoader

**Pattern**: Track loading progress for better UX.

```tsx
import { useLoader } from '@react-three/fiber';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

function ModelWithProgress({ url }: { url: string }) {
  // GLTFLoader is cached automatically by useLoader
  const gltf = useLoader(GLTFLoader, url);

  return <primitive object={gltf.scene} />;
}

// With Suspense, the fallback shows while loading
function Scene() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <ModelWithProgress url="/assets/models/character.glb" />
    </Suspense>
  );
}
```

### Asset Preloading Pattern

**Pattern**: Preload critical assets before they're needed.

```tsx
import { useEffect, useState } from 'react';
import { useGLTF } from '@react-three/drei';

function usePreloadGLTF(urls: string[]) {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let mounted = true;

    Promise.all(urls.map((url) => useGLTF.preload(url))).then(() => {
      if (mounted) setLoaded(true);
    });

    return () => {
      mounted = false;
    };
  }, urls);

  return loaded;
}

// Usage: preload assets before showing scene
function Game() {
  const assetsReady = usePreloadGLTF(['/assets/models/player.glb', '/assets/models/weapon.glb']);

  if (!assetsReady) {
    return <LoadingScreen progress="Loading assets..." />;
  }

  return <GameScene />;
}
```

### Cached Asset Loading

**Pattern**: `useLoader` and `useGLTF` automatically cache assets by URL.

```tsx
// First call loads and caches
const { scene: scene1 } = useGLTF('/assets/models/tree.glb');

// Subsequent calls use cached version - instant!
const { scene: scene2 } = useGLTF('/assets/models/tree.glb');

// Both share the same GPU memory
```

### Asset Loading Error Boundaries

**Pattern**: Handle loading failures gracefully.

```tsx
import { Component, ReactNode } from 'react';
import { useGLTF } from '@react-three/drei';

class AssetErrorBoundary extends Component<
  { children: ReactNode; fallback?: ReactNode },
  { hasError: boolean }
> {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <FallbackAsset />;
    }
    return this.props.children;
  }
}

// Wrap assets in error boundary
function SafeModel({ url }: { url: string }) {
  return (
    <AssetErrorBoundary fallback={<ErrorMesh />}>
      <Suspense fallback={<LoadingMesh />}>
        <Model url={url} />
      </Suspense>
    </AssetErrorBoundary>
  );
}

function Model({ url }: { url: string }) {
  const { scene } = useGLTF(url);
  return <primitive object={scene} />;
}
```

### Fallback Assets for Loading States

**Pattern**: Show placeholder while real asset loads.

```tsx
// Simple placeholder mesh
function LoadingMesh() {
  return (
    <mesh>
      <boxGeometry args={[1, 2, 0.5]} />
      <meshStandardMaterial color="#666" wireframe />
    </mesh>
  );
}

// Error fallback
function ErrorMesh() {
  return (
    <mesh>
      <sphereGeometry args={[0.5]} />
      <meshStandardMaterial color="red" />
    </mesh>
  );
}
```

**Learned from bugfix-005 retrospective (2026-01-22)**:

- Large weapon models may have load delays
- Always use Suspense boundaries for async asset loading
- Consider loading states for better UX during asset fetch

## Texture Optimization

```bash
# Optimize textures before importing
# Resize to power-of-2 dimensions
convert input.jpg -resize 512x512 output.png

# Compress to WebP
convert input.png -quality 80 output.webp

# Or use basis universal for GPU compression
basisu -q 1 input.png -output output.basis
```

## GLTF Export Settings (Blender)

```
Export Settings:
- Format: glTF Binary (.glb)
- Include: Selected Objects
- Mesh: + Apply Modifiers
- Mesh: - Tangents (compute at runtime)
- Mesh: - Blending: Obsolete
- LoD: Simplify disabled
- Armature: + Only Keyframes
- Animation: - Limit to Selected
- Geometry: - UV Map
- Geometry: - Normals
- Geometry: + Tangents
- Geometry: + Vertex Colors
- Objects: - PBR Ext
```

## Asset Component Template

````tsx
/**
 * {Asset Name}
 *
 * {Description of asset}
 *
 * @example
 * ```tsx
 * <MyAsset />
 * ```
 */
import { forwardRef, useMemo } from 'react';
import * as THREE from 'three';

export interface MyAssetProps {
  /** Description of prop */
  variant?: 'a' | 'b' | 'c';
  /** Another prop */
  intensity?: number;
}

export const MyAsset = forwardRef<THREE.Group, MyAssetProps>(
  ({ variant = 'a', intensity = 1.0 }, ref) => {
    // Create or load asset here
    const material = useMemo(
      () =>
        new THREE.MeshStandardMaterial({
          color: variant === 'a' ? 0xff0000 : 0x0000ff,
        }),
      [variant]
    );

    return (
      <group ref={ref}>
        <mesh>
          <boxGeometry />
          <meshStandardMaterial {...material} />
        </mesh>
      </group>
    );
  }
);

MyAsset.displayName = 'MyAsset';
````

## Checklist

Before marking asset ready:

- [ ] Asset follows naming conventions
- [ ] File is in correct directory
- [ ] textures are optimized (compressed, power-of-2)
- [ ] Component has TypeScript types
- [ ] Props documented with JSDoc
- [ ] Example usage in comments
- [ ] Tested in browser
- [ ] Feedback loops all pass

## Integration Smoke Test (CRITICAL)

**Before marking ANY task complete**, run this quick verification:

```bash
# Smoke Test Checklist - verify in browser
# 1. Character model visible? (not placeholder geometry)
# 2. Weapon model visible? (not placeholder box/cylinder)
# 3. Projectiles visible? (not debug-gated)
# 4. Audio plays? (if audio task)
# 5. Textures loaded? (not solid colors)
# 6. Animations playing? (if animated asset)
```

**CRITICAL: Debug Code Audit**

Before committing, search for debug-gated rendering:

```bash
# Search for debug conditionals that might hide features
grep -r "{debug &&" src/
grep -r "debug.*&&" src/
grep -r "if.*debug" src/
```

**Remove ALL debug conditionals from player-facing features:**

```tsx
// ❌ WRONG - Feature hidden behind debug flag
{
  debug &&
    projectiles.map((proj) => (
      <mesh key={proj.id}>
        <sphereGeometry args={[0.1]} />
        <meshStandardMaterial color={proj.color} />
      </mesh>
    ));
}

// ✅ CORRECT - Feature always visible in production
{
  projectiles.map((proj) => (
    <mesh key={proj.id}>
      <sphereGeometry args={[0.1]} />
      <meshStandardMaterial color={proj.color} />
    </mesh>
  ));
}

// ✅ CORRECT - Debug-only helpers use debug flag
{
  debug && <gridHelper args={[20, 20]} />;
}
{
  debug && <axesHelper args={[2]} />;
}
```

**Learned from polish-001 retrospective (2026-01-22):**
Paint projectiles were invisible because they were gated behind `debug &&` conditional. Player-facing features must NEVER be debug-gated.

## Asset Integration Verification

After integrating an asset, verify it actually appears in the scene:

```tsx
// Add a temporary dev-mode check during development
import { useHelper } from '@react-three/drei';

function MyAsset() {
  const meshRef = useRef<THREE.Mesh>(null);

  // Temporary: visual verification during development
  useEffect(() => {
    if (meshRef.current) {
      console.log('[ASSET CHECK]', {
        type: meshRef.current.geometry.type,
        vertices: meshRef.current.geometry.attributes.position.count,
        // This confirms the REAL asset loaded, not a placeholder
      });
    }
  }, []);

  return <mesh ref={meshRef}>...</mesh>;
}
```

## Bone-Based Attachment for Animated Models

When attaching objects (weapons, accessories, effects) to animated character models, use the skeleton bone system rather than direct parenting to meshes.

### Finding and Attaching to Bones

```tsx
import { useRef, useEffect } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';

function CharacterWithWeapon() {
  const { scene } = useGLTF('/assets/models/characterMedium.glb');
  const weaponGroupRef = useRef<THREE.Group>(null);
  const mixerRef = useRef<THREE.AnimationMixer | null>(null);

  useEffect(() => {
    // Traverse to find skinned mesh with skeleton
    scene.traverse((object) => {
      if (object.type === 'SkinnedMesh') {
        const skinnedMesh = object as THREE.SkinnedMesh;
        const skeleton = skinnedMesh.skeleton;

        // Find the specific bone by name
        const handBone = skeleton.bones.find(
          (bone) => bone.name === 'mixamorigRightHand'
          // Common bone names: 'RightHand', 'mixamorigRightHand', 'RHand', 'Hand.R'
          // Check in Blender or Three.js Inspector for exact bone names
        );

        if (handBone && weaponGroupRef.current) {
          // Parent weapon group to bone - weapon moves with animation
          handBone.add(weaponGroupRef.current);
          // Adjust position/rotation relative to bone
          weaponGroupRef.current.position.set(0, 0, 0);
          weaponGroupRef.current.rotation.set(0, 0, 0);
        }
      }
    });

    // Set up animation mixer
    mixerRef.current = new THREE.AnimationMixer(scene);
    const action = mixerRef.current.clipAction(
      scene.animations[0] // First animation
    );
    action.play();

    return () => {
      mixerRef.current?.stopAllAction();
    };
  }, [scene]);

  useFrame((state, delta) => {
    mixerRef.current?.update(delta);
  });

  return (
    <group>
      <primitive object={scene} />
      <group ref={weaponGroupRef}>
        {/* Weapon moves with hand bone */}
        <WeaponModel />
      </group>
    </group>
  );
}
```

### Bone Attachment Pattern

| Step | Action                           | Purpose                                    |
| ---- | -------------------------------- | ------------------------------------------ |
| 1    | Load GLTF with skeleton          | Character model with bone hierarchy        |
| 2    | Traverse to SkinnedMesh          | Find mesh containing skeleton              |
| 3    | Find bone by name                | Locate attachment point (hand, head, etc.) |
| 4    | Parent object to bone            | `bone.add(childObject)`                    |
| 5    | Position/rotate relative to bone | Fine-tune attachment                       |
| 6    | Animation moves attachment       | Bone animation moves attached object       |

### Common Bone Names by Rig Format

| Rig Format | Hand Bone                   | Head Bone                   | Spine Bone                  |
| ---------- | --------------------------- | --------------------------- | --------------------------- |
| Mixamo     | `mixamorigRightHand`        | `mixamorigHead`             | `mixamorigSpine`            |
| Blender    | `RightHand`, `Hand.R`       | `Head`, `HeadTop`           | `Spine`, `Hips`             |
| VRM        | `rightHand`                 | `head`                      | `spine`                     |
| Custom     | Check in Three.js Inspector | Check in Three.js Inspector | Check in Three.js Inspector |

### Debugging Bone Attachments

```tsx
// During development, visualize bone positions
useEffect(() => {
  scene.traverse((object) => {
    if (object.type === 'SkinnedMesh') {
      const skinnedMesh = object as THREE.SkinnedMesh;
      const { bones } = skinnedMesh.skeleton;

      bones.forEach((bone, index) => {
        console.log(`Bone ${index}: ${bone.name}`, bone.position);
      });
    }
  });
}, [scene]);
```

**Learned from bugfix-004 retrospective (2026-01-22):**
Weapon attachment to character hand requires using `skeleton.bones.find()` to locate the bone, then `bone.add(weaponGroup)` to parent the weapon. Direct mesh parenting doesn't work with animated skeletons.

## Variable Asset Scales and Pivots

### Problem: Different Asset Packs Use Different Scales

When combining assets from multiple sources (Blender Market, Sketchfab, vendor packs), each may use different unit systems and scale conventions.

### Solution: Asset Configuration with Normalized Transforms

```tsx
// assets/config/weapon-config.ts
export interface WeaponConfig {
  name: string;
  modelPath: string;
  // Scale normalization
  scale: number; // Overall scale multiplier
  // Pivot correction (asset origin offset)
  position: [number, number, number];
  rotation: [number, number, number];
  // Optional: per-axis scale for non-uniform correction
  scaleVector?: [number, number, number];
}

export const weaponConfigs: Record<string, WeaponConfig> = {
  // Blaster Kit assets (small scale, ~0.15)
  blaster_rifle: {
    name: 'Blaster Rifle',
    modelPath: '/assets/models/blaster-kit/rifle.glb',
    scale: 0.15,
    position: [0, 0, 0],
    rotation: [0, 0, 0],
  },
  // Weapon Pack assets (default scale, ~1.0)
  plasma_gun: {
    name: 'Plasma Gun',
    modelPath: '/assets/models/weapon-pack/plasma.glb',
    scale: 1.0,
    position: [0, 0, 0],
    rotation: [0, Math.PI, 0], // May need rotation flip
  },
  // Accessories pack (tiny scale, ~0.01)
  scope_attachment: {
    name: 'Scope',
    modelPath: '/assets/models/accessories/scope.glb',
    scale: 0.01,
    position: [0, 0.5, 0], // Offset to attach point
    rotation: [0, 0, 0],
  },
};
```

### Normalized Asset Component

```tsx
import { useGLTF } from '@react-three/drei';
import type { WeaponConfig } from './weapon-config';

interface NormalizedAssetProps {
  config: WeaponConfig;
  attachTo?: THREE.Object3D; // Optional parent attachment
}

export function NormalizedAsset({ config, attachTo }: NormalizedAssetProps) {
  const { scene } = useGLTF(config.modelPath);
  const groupRef = useRef<THREE.Group>(null);

  // Apply configured transforms
  useEffect(() => {
    if (!groupRef.current) return;

    const { scale, position, rotation, scaleVector } = config;

    // Apply scale correction
    if (scaleVector) {
      groupRef.current.scale.set(...scaleVector);
    } else {
      groupRef.current.scale.setScalar(scale);
    }

    // Apply position offset (pivot correction)
    groupRef.current.position.set(...position);

    // Apply rotation correction
    groupRef.current.rotation.set(...rotation);

    // Attach to parent if provided (e.g., hand bone)
    if (attachTo) {
      attachTo.add(groupRef.current);
    }

    return () => {
      if (attachTo && groupRef.current) {
        attachTo.remove(groupRef.current);
      }
    };
  }, [config, attachTo]);

  return (
    <group ref={groupRef}>
      <primitive object={scene} />
    </group>
  );
}
```

### Asset Scale Detection Helper

```tsx
import { useEffect, useRef } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';

/**
 * Helper to detect asset scale and bounding box
 * Use during development to populate config values
 */
function useAssetInfo(url: string) {
  const { scene } = useGLTF(url);
  const info = useRef<{
    boundingBox: THREE.Box3;
    size: THREE.Vector3;
    center: THREE.Vector3;
  } | null>(null);

  useEffect(() => {
    const box = new THREE.Box3().setFromObject(scene);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());

    info.current = { boundingBox: box, size, center };

    // Log for config development
    console.log(`[Asset Info] ${url}`, {
      size: { x: size.x.toFixed(3), y: size.y.toFixed(3), z: size.z.toFixed(3) },
      center: { x: center.x.toFixed(3), y: center.y.toFixed(3), z: center.z.toFixed(3) },
    });
  }, [scene]);

  return info.current;
}
```

### Pivot Point Correction Pattern

**Problem**: Asset origin is not at the attachment point (e.g., gun grip vs. gun center).

**Solution**: Wrapper group with offset correction.

```tsx
interface PivotCorrectedProps {
  modelPath: string;
  // The point that should align with parent (e.g., hand position)
  gripOffset: [number, number, number];
  scale: number;
}

function PivotCorrectedAsset({ modelPath, gripOffset, scale }: PivotCorrectedProps) {
  const { scene } = useGLTF(modelPath);

  return (
    <group scale={scale}>
      {/* Offset wrapper shifts the model so grip point is at origin */}
      <group position={gripOffset}>
        <primitive object={scene} />
      </group>
    </group>
  );
}
```

### Common Scale Conversions

| Source System     | Three.js Units   | Scale Factor |
| ----------------- | ---------------- | ------------ |
| Blender (default) | 1 unit = 1 meter | 1.0          |
| Unreal Engine     | 1 unit = 1 cm    | 0.01         |
| Unity             | 1 unit = 1 meter | 1.0          |
| Maya (cm)         | 1 unit = 1 cm    | 0.01         |
| 3ds Max (inches)  | 1 unit = 1 inch  | 0.0254       |

### Asset Integration Checklist for Multi-Source Projects

- [ ] Determine source unit system for each asset pack
- [ ] Create config file with scale factors for each asset type
- [ ] Test each asset in isolation to verify scale
- [ ] Measure bounding box to determine grip/handle offset
- [ ] Add rotation correction if asset faces wrong direction
- [ ] Test attachment to character hand bone
- [ ] Verify alignment with animation (weapon doesn't float or clip)

**Learned from bugfix-005 retrospective (2026-01-22)**:

- Asset packs have wildly different scales (0.01 to 1.0+)
- Per-weapon configuration is essential for consistent attachment
- Grip offset varies by model - cannot use universal values

## Asset Scale Validation Workflow (NEW - 2026-01-25)

### Problem: Asset Packs Have Wildly Different Scales

When combining assets from multiple sources (Blender Market, Sketchfab, vendor packs), each may use different unit systems and scale conventions. The Blaster Kit requires 0.015 scale (not 0.15), causing 10x size errors.

### Scale Validation Process

#### Step 1: Detect Asset Scale on Import

```tsx
// Use this helper when FIRST importing an asset
import { useEffect, useState } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';

function AssetScaleValidator({
  assetUrl,
  targetSize = 0.5,
}: {
  assetUrl: string;
  targetSize?: number; // Desired size in Three.js units
}) {
  const { scene } = useGLTF(assetUrl);
  const [scaleReport, setScaleReport] = useState<string | null>(null);

  useEffect(() => {
    const box = new THREE.Box3().setFromObject(scene);
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    const suggestedScale = targetSize / maxDim;

    const report = `
=== ASSET SCALE REPORT ===
URL: ${assetUrl}
Current Size: ${size.x.toFixed(3)} x ${size.y.toFixed(3)} x ${size.z.toFixed(3)}
Max Dimension: ${maxDim.toFixed(3)}
Suggested Scale: ${suggestedScale.toFixed(4)}

ADD TO CONFIG:
{
  scale: ${suggestedScale.toFixed(4)},
  source: 'ASSET_PACK_NAME',
  verifiedDate: '${new Date().toISOString().split('T')[0]}',
}
`;
    console.log(report);
    setScaleReport(report);
  }, [scene, assetUrl, targetSize]);

  return null; // Development-only helper, renders nothing
}
```

#### Step 2: Document in Asset Config

```typescript
// assets/config/scale-registry.ts
interface AssetScaleEntry {
  scale: number;
  source: string;
  verifiedDate: string;
  notes?: string;
}

export const ASSET_SCALE_REGISTRY: Record<string, AssetScaleEntry> = {
  blaster_rifle: {
    scale: 0.015,
    source: 'Blaster Kit',
    verifiedDate: '2026-01-25',
    notes: 'CRITICAL: 0.15 makes weapon 10x too large',
  },
};
```

#### Step 3: Create Scale Validation Test

```typescript
// tests/assets/scale-validation.test.ts
import { describe, it, expect } from 'vitest';
import { ASSET_SCALE_REGISTRY } from '@/assets/config/scale-registry';

describe('Asset Scale Validation', () => {
  it('should have documented scale for all registered assets', () => {
    Object.entries(ASSET_SCALE_REGISTRY).forEach(([name, config]) => {
      expect(config.scale).toBeGreaterThan(0);
      expect(config.scale).toBeLessThan(100); // Sanity check
      expect(config.source).toBeTruthy();
      expect(config.verifiedDate).toMatch(/\d{4}-\d{2}-\d{2}/);
    });
  });

  it('should warn about unusual scale values', () => {
    Object.entries(ASSET_SCALE_REGISTRY).forEach(([name, config]) => {
      // Values like 0.15 (when should be 0.015) are red flags
      if (config.source === 'Blaster Kit' && config.scale > 0.02) {
        throw new Error(
          `${name}: Blaster Kit scale ${config.scale} is too large! ` +
            `Expected ~0.015. Check asset pack requirements.`
        );
      }
    });
  });
});
```

### Asset Scale Reference

| Asset Pack         | Typical Scale | Unit System | Notes                           |
| ------------------ | ------------- | ----------- | ------------------------------- |
| Blaster Kit        | 0.015         | Unknown     | CRITICAL: 0.15 is 10x too large |
| Mixamo             | 1.0           | Meters      | Export at unit scale            |
| Unreal Marketplace | 0.01          | Centimeters | Multiply by 0.01                |
| Unity Asset Store  | 1.0           | Meters      | Usually unit scale              |
| Custom Blender     | 1.0           | Meters      | Depends on export settings      |

### Scale Validation Checklist

Before marking asset integration complete:

- [ ] Scale value measured and documented in ASSET_SCALE_REGISTRY
- [ ] Unit test created to validate scale against expected range
- [ ] Visual verification in browser confirms correct size
- [ ] Asset tested in actual scene (not isolated)
- [ ] Source and verification date recorded
- [ ] Any special notes added (e.g., scale sensitivity warnings)

**Learned from feat-tps-005 and bugfix-tps-001 retrospectives (2026-01-25)**:

- Blaster Kit FBX requires 0.015 scale (not 0.15) - 10x difference
- Missing scale documentation causes repeated confusion
- Scale validation tests catch regressions before browser testing

## Production Readiness Checklist

Before sending to QA:

- [ ] NO debug conditionals on player-visible features
- [ ] Asset loads from correct path (check browser Network tab)
- [ ] Asset renders visibly (check Three.js inspector or browser)
- [ ] Placeholder geometry replaced with actual asset
- [ ] Animations play (if applicable)
- [ ] Textures apply correctly (not solid colors/tints only)
- [ ] No console errors during asset loading
- [ ] Asset scales and positions correctly relative to scene

## Related Skills

For material setup: `Skill("ta-r3f-materials")`
For general workflow: `Skill("techartist-worflow")`

## External References

- [GLTF Best Practices](https://github.com/KhronosGroup/glTF-Sample-Models)
