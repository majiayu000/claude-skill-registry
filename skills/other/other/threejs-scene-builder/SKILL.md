---
name: threejs-scene-builder
description: Comprehensive Three.js and React Three Fiber skill for creating 3D scenes, characters, NPCs, procedural generation, animation retargeting, and interactive experiences. Use when user asks to "create Three.js scene", "setup React Three Fiber", "add 3D character", "create NPC AI", "procedural 3D generation", "retarget animation", "setup avatar system", or "create 3D game".
allowed-tools: [Write, Read]
---

# Three.js & React Three Fiber - Complete 3D Development Skill

Comprehensive guide for creating advanced 3D web experiences using Three.js and React Three Fiber (R3F), covering scene setup, character systems, NPCs, procedural generation, animation retargeting, physics, and interactive gameplay.

## When to Use

- "Create Three.js scene" / "Setup 3D scene"
- "Setup React Three Fiber" / "Create R3F app"
- "Generate WebGL visualization" / "Create interactive 3D graphics"
- "Add 3D character" / "Setup avatar system"
- "Create NPC AI" / "Add game characters"
- "Procedural 3D generation" / "Generate 3D content"
- "Retarget animation" / "Mixamo to Three.js"
- "Setup character controller" / "Add physics"
- "Ready Player Me integration"
- "Create 3D game with Three.js"

## Instructions

### 1. Install Three.js

```bash
npm install three
# TypeScript types
npm install --save-dev @types/three
```

### 2. Basic Scene Setup

**TypeScript:**
```typescript
// scene.ts
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

export class SceneManager {
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private renderer: THREE.WebGLRenderer;
  private controls: OrbitControls;
  private animationId: number | null = null;

  constructor(container: HTMLElement) {
    // Scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x1a1a1a);
    this.scene.fog = new THREE.Fog(0x1a1a1a, 10, 50);

    // Camera
    this.camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    this.camera.position.set(5, 5, 5);
    this.camera.lookAt(0, 0, 0);

    // Renderer
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
    });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(this.renderer.domElement);

    // Controls
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.minDistance = 2;
    this.controls.maxDistance = 20;

    // Lights
    this.setupLights();

    // Handle resize
    window.addEventListener('resize', () => this.onWindowResize());

    // Start animation
    this.animate();
  }

  private setupLights() {
    // Ambient light
    const ambient = new THREE.AmbientLight(0xffffff, 0.4);
    this.scene.add(ambient);

    // Directional light (sun)
    const directional = new THREE.DirectionalLight(0xffffff, 0.8);
    directional.position.set(5, 10, 5);
    directional.castShadow = true;
    directional.shadow.camera.left = -10;
    directional.shadow.camera.right = 10;
    directional.shadow.camera.top = 10;
    directional.shadow.camera.bottom = -10;
    directional.shadow.mapSize.width = 2048;
    directional.shadow.mapSize.height = 2048;
    this.scene.add(directional);

    // Hemisphere light
    const hemisphere = new THREE.HemisphereLight(0xffffbb, 0x080820, 0.3);
    this.scene.add(hemisphere);
  }

  private onWindowResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  private animate() {
    this.animationId = requestAnimationFrame(() => this.animate());
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }

  public addObject(object: THREE.Object3D) {
    this.scene.add(object);
  }

  public dispose() {
    if (this.animationId !== null) {
      cancelAnimationFrame(this.animationId);
    }
    this.renderer.dispose();
    this.controls.dispose();
  }
}

// Usage
const container = document.getElementById('canvas-container')!;
const sceneManager = new SceneManager(container);

// Add a cube
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
cube.castShadow = true;
cube.receiveShadow = true;
sceneManager.addObject(cube);
```

### 3. Advanced Material Setup

```typescript
// materials.ts
import * as THREE from 'three';

export class MaterialLibrary {
  // PBR Material
  static createPBRMaterial(options: {
    color?: number;
    roughness?: number;
    metalness?: number;
    normalMap?: THREE.Texture;
    roughnessMap?: THREE.Texture;
  }) {
    return new THREE.MeshStandardMaterial({
      color: options.color ?? 0xffffff,
      roughness: options.roughness ?? 0.5,
      metalness: options.metalness ?? 0.5,
      normalMap: options.normalMap,
      roughnessMap: options.roughnessMap,
    });
  }

  // Glass Material
  static createGlassMaterial() {
    return new THREE.MeshPhysicalMaterial({
      color: 0xffffff,
      metalness: 0,
      roughness: 0,
      transmission: 1,
      thickness: 0.5,
    });
  }

  // Glowing Material
  static createGlowMaterial(color: number = 0x00ff00) {
    return new THREE.MeshBasicMaterial({
      color,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending,
    });
  }

  // Toon Material
  static createToonMaterial(color: number = 0x00ff00) {
    return new THREE.MeshToonMaterial({
      color,
      gradientMap: this.createGradientTexture(),
    });
  }

  private static createGradientTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 1;
    const ctx = canvas.getContext('2d')!;
    const gradient = ctx.createLinearGradient(0, 0, 256, 0);
    gradient.addColorStop(0, '#000000');
    gradient.addColorStop(0.5, '#808080');
    gradient.addColorStop(1, '#ffffff');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 256, 1);
    return new THREE.CanvasTexture(canvas);
  }
}
```

### 4. Geometry Helpers

```typescript
// geometries.ts
import * as THREE from 'three';

export class GeometryHelpers {
  static createGroundPlane(size: number = 20) {
    const geometry = new THREE.PlaneGeometry(size, size);
    const material = new THREE.MeshStandardMaterial({
      color: 0x808080,
      roughness: 0.8,
      metalness: 0.2,
    });
    const plane = new THREE.Mesh(geometry, material);
    plane.rotation.x = -Math.PI / 2;
    plane.receiveShadow = true;
    return plane;
  }

  static createSkybox(textureLoader: THREE.TextureLoader, path: string) {
    const loader = new THREE.CubeTextureLoader();
    const texture = loader.load([
      `${path}/px.jpg`, `${path}/nx.jpg`,
      `${path}/py.jpg`, `${path}/ny.jpg`,
      `${path}/pz.jpg`, `${path}/nz.jpg`,
    ]);
    return texture;
  }

  static createParticles(count: number = 1000) {
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(count * 3);

    for (let i = 0; i < count * 3; i++) {
      positions[i] = (Math.random() - 0.5) * 20;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const material = new THREE.PointsMaterial({
      size: 0.05,
      color: 0xffffff,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending,
    });

    return new THREE.Points(geometry, material);
  }
}
```

### 5. Animation System

```typescript
// animation.ts
import * as THREE from 'three';

export class AnimationController {
  private mixer: THREE.AnimationMixer;
  private actions: Map<string, THREE.AnimationAction> = new Map();

  constructor(model: THREE.Object3D, animations: THREE.AnimationClip[]) {
    this.mixer = new THREE.AnimationMixer(model);

    animations.forEach((clip, index) => {
      const action = this.mixer.clipAction(clip);
      this.actions.set(clip.name || `animation_${index}`, action);
    });
  }

  play(name: string, fadeIn: number = 0.5) {
    const action = this.actions.get(name);
    if (action) {
      action.reset().fadeIn(fadeIn).play();
    }
  }

  stop(name: string, fadeOut: number = 0.5) {
    const action = this.actions.get(name);
    if (action) {
      action.fadeOut(fadeOut);
    }
  }

  update(deltaTime: number) {
    this.mixer.update(deltaTime);
  }
}
```

### 6. Model Loading

```typescript
// loader.ts
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader';

export class ModelLoader {
  private gltfLoader: GLTFLoader;
  private textureLoader: THREE.TextureLoader;
  private loadingManager: THREE.LoadingManager;

  constructor(onProgress?: (progress: number) => void) {
    this.loadingManager = new THREE.LoadingManager();

    if (onProgress) {
      this.loadingManager.onProgress = (url, loaded, total) => {
        onProgress((loaded / total) * 100);
      };
    }

    // Setup DRACO loader for compressed models
    const dracoLoader = new DRACOLoader(this.loadingManager);
    dracoLoader.setDecoderPath('/draco/');

    this.gltfLoader = new GLTFLoader(this.loadingManager);
    this.gltfLoader.setDRACOLoader(dracoLoader);

    this.textureLoader = new THREE.TextureLoader(this.loadingManager);
  }

  async loadGLTF(url: string): Promise<THREE.Group> {
    return new Promise((resolve, reject) => {
      this.gltfLoader.load(
        url,
        (gltf) => {
          gltf.scene.traverse((child) => {
            if (child instanceof THREE.Mesh) {
              child.castShadow = true;
              child.receiveShadow = true;
            }
          });
          resolve(gltf.scene);
        },
        undefined,
        reject
      );
    });
  }

  async loadTexture(url: string): Promise<THREE.Texture> {
    return new Promise((resolve, reject) => {
      this.textureLoader.load(url, resolve, undefined, reject);
    });
  }
}
```

### 7. Post-Processing

```typescript
// post-processing.ts
import * as THREE from 'three';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass';
import { SSAOPass } from 'three/examples/jsm/postprocessing/SSAOPass';

export class PostProcessing {
  private composer: EffectComposer;

  constructor(
    renderer: THREE.WebGLRenderer,
    scene: THREE.Scene,
    camera: THREE.Camera
  ) {
    this.composer = new EffectComposer(renderer);

    // Render pass
    const renderPass = new RenderPass(scene, camera);
    this.composer.addPass(renderPass);

    // Bloom pass
    const bloomPass = new UnrealBloomPass(
      new THREE.Vector2(window.innerWidth, window.innerHeight),
      1.5,  // strength
      0.4,  // radius
      0.85  // threshold
    );
    this.composer.addPass(bloomPass);

    // SSAO pass
    const ssaoPass = new SSAOPass(scene, camera);
    ssaoPass.kernelRadius = 16;
    this.composer.addPass(ssaoPass);
  }

  render() {
    this.composer.render();
  }

  resize(width: number, height: number) {
    this.composer.setSize(width, height);
  }
}
```

### 8. Performance Optimization

```typescript
// optimization.ts
import * as THREE from 'three';

export class PerformanceOptimizer {
  static optimizeGeometry(geometry: THREE.BufferGeometry) {
    // Merge vertices
    geometry.computeVertexNormals();
    geometry.normalizeNormals();
    return geometry;
  }

  static createLOD(geometries: THREE.BufferGeometry[], distances: number[]) {
    const lod = new THREE.LOD();

    geometries.forEach((geometry, index) => {
      const material = new THREE.MeshStandardMaterial();
      const mesh = new THREE.Mesh(geometry, material);
      lod.addLevel(mesh, distances[index]);
    });

    return lod;
  }

  static enableInstancing(
    geometry: THREE.BufferGeometry,
    material: THREE.Material,
    count: number,
    positions: THREE.Vector3[]
  ) {
    const mesh = new THREE.InstancedMesh(geometry, material, count);

    const matrix = new THREE.Matrix4();
    positions.forEach((pos, i) => {
      matrix.setPosition(pos);
      mesh.setMatrixAt(i, matrix);
    });

    mesh.instanceMatrix.needsUpdate = true;
    return mesh;
  }

  static setupFrustumCulling(camera: THREE.Camera, objects: THREE.Object3D[]) {
    const frustum = new THREE.Frustum();
    const projScreenMatrix = new THREE.Matrix4();

    return () => {
      camera.updateMatrixWorld();
      projScreenMatrix.multiplyMatrices(
        camera.projectionMatrix,
        camera.matrixWorldInverse
      );
      frustum.setFromProjectionMatrix(projScreenMatrix);

      objects.forEach((obj) => {
        obj.visible = frustum.intersectsObject(obj);
      });
    };
  }
}
```

### 9. React Integration

```typescript
// ThreeCanvas.tsx
import React, { useEffect, useRef } from 'react';
import { SceneManager } from './scene';

export const ThreeCanvas: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneManagerRef = useRef<SceneManager | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Initialize scene
    sceneManagerRef.current = new SceneManager(containerRef.current);

    // Cleanup
    return () => {
      sceneManagerRef.current?.dispose();
    };
  }, []);

  return (
    <div
      ref={containerRef}
      style={{ width: '100vw', height: '100vh' }}
    />
  );
};
```

### 10. Complete Example

```typescript
// main.ts
import * as THREE from 'three';
import { SceneManager } from './scene';
import { GeometryHelpers } from './geometries';
import { MaterialLibrary } from './materials';
import { ModelLoader } from './loader';

async function main() {
  const container = document.getElementById('app')!;
  const scene = new SceneManager(container);

  // Add ground plane
  const ground = GeometryHelpers.createGroundPlane();
  scene.addObject(ground);

  // Add particles
  const particles = GeometryHelpers.createParticles(5000);
  scene.addObject(particles);

  // Load model
  const loader = new ModelLoader((progress) => {
    console.log(`Loading: ${progress.toFixed(0)}%`);
  });

  try {
    const model = await loader.loadGLTF('/models/scene.gltf');
    model.scale.set(2, 2, 2);
    scene.addObject(model);
  } catch (error) {
    console.error('Failed to load model:', error);
  }

  // Add rotating cube with PBR material
  const cubeGeo = new THREE.BoxGeometry();
  const cubeMat = MaterialLibrary.createPBRMaterial({
    color: 0x2194ce,
    roughness: 0.3,
    metalness: 0.8,
  });
  const cube = new THREE.Mesh(cubeGeo, cubeMat);
  cube.position.y = 1;
  scene.addObject(cube);

  // Animation loop
  function animate() {
    requestAnimationFrame(animate);
    cube.rotation.y += 0.01;
  }
  animate();
}

main();
```

### Best Practices

**DO:**
- Use BufferGeometry
- Enable frustum culling
- Use instanced meshes for many objects
- Optimize textures
- Use LOD for distant objects
- Dispose geometries and materials
- Limit shadow maps
- Use post-processing sparingly

**DON'T:**
- Create objects in render loop
- Use high-poly models without LOD
- Forget to dispose resources
- Use too many lights
- Skip texture compression
- Render at native device pixel ratio on mobile
- Update uniforms every frame unnecessarily

---

## 🚀 PART 2: React Three Fiber (R3F)

React Three Fiber is a React renderer for Three.js that enables declarative, component-based 3D development.

### Installation

```bash
npm install three @react-three/fiber
# Ecosystem libraries
npm install @react-three/drei @react-three/postprocessing
npm install postprocessing
npm install --save-dev @types/three
```

### Basic R3F Scene

```tsx
// App.tsx
import { useRef, useState } from 'react';
import { Canvas, useFrame, MeshProps } from '@react-three/fiber';
import { OrbitControls, Environment, Sky } from '@react-three/drei';
import * as THREE from 'three';

function Box(props: MeshProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHover] = useState(false);
  const [active, setActive] = useState(false);

  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta;
    }
  });

  return (
    <mesh
      {...props}
      ref={meshRef}
      scale={active ? 1.5 : 1}
      onClick={() => setActive(!active)}
      onPointerOver={() => setHover(true)}
      onPointerOut={() => setHover(false)}
    >
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={hovered ? 'hotpink' : 'orange'} />
    </mesh>
  );
}

export default function App() {
  return (
    <Canvas camera={{ position: [0, 0, 5], fov: 75 }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <Box position={[0, 0, 0]} />
      <OrbitControls />
      <Sky sunPosition={[100, 20, 100]} />
      <Environment preset="sunset" />
    </Canvas>
  );
}
```

### Advanced R3F Scene Manager

```tsx
// Scene.tsx
import { useRef, useMemo } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import {
  OrbitControls,
  PerspectiveCamera,
  Environment,
  ContactShadows,
  useGLTF,
  useTexture,
  Html,
  Stats,
} from '@react-three/drei';
import {
  EffectComposer,
  Bloom,
  DepthOfField,
  Vignette,
  SSAO,
} from '@react-three/postprocessing';
import * as THREE from 'three';

// Scene configuration
interface SceneConfig {
  enablePostProcessing?: boolean;
  enableShadows?: boolean;
  enableStats?: boolean;
  toneMappingExposure?: number;
}

// Main scene component
function Scene({ config }: { config: SceneConfig }) {
  const { gl, scene } = useThree();

  // Configure renderer
  useMemo(() => {
    gl.shadowMap.enabled = config.enableShadows ?? true;
    gl.shadowMap.type = THREE.PCFSoftShadowMap;
    gl.toneMapping = THREE.ACESFilmicToneMapping;
    gl.toneMappingExposure = config.toneMappingExposure ?? 1;
    scene.background = new THREE.Color(0x1a1a1a);
  }, [gl, scene, config]);

  return (
    <>
      {config.enableStats && <Stats />}

      {/* Lighting */}
      <ambientLight intensity={0.3} />
      <directionalLight
        position={[10, 10, 5]}
        intensity={1}
        castShadow
        shadow-mapSize={[2048, 2048]}
        shadow-camera-left={-10}
        shadow-camera-right={10}
        shadow-camera-top={10}
        shadow-camera-bottom={-10}
      />
      <hemisphereLight args={[0xffffbb, 0x080820, 0.2]} />

      {/* Environment */}
      <Environment preset="city" background={false} />

      {/* Your 3D content here */}
    </>
  );
}

// App with Canvas wrapper
export default function App() {
  return (
    <Canvas shadows dpr={[1, 2]}>
      <Scene config={{ enablePostProcessing: true, enableShadows: true }} />
      <OrbitControls makeDefault />

      {/* Post-processing */}
      <EffectComposer>
        <Bloom luminanceThreshold={1} intensity={0.5} />
        <DepthOfField focusDistance={0.01} focalLength={0.2} bokehScale={3} />
        <SSAO />
        <Vignette opacity={0.5} />
      </EffectComposer>
    </Canvas>
  );
}
```

### R3F Hooks & Best Practices

```tsx
// hooks/useAnimatedModel.ts
import { useRef, useEffect } from 'react';
import { useGLTF, useAnimations } from '@react-three/drei';
import * as THREE from 'three';

export function useAnimatedModel(modelPath: string, animationName?: string) {
  const group = useRef<THREE.Group>(null);
  const { scene, animations } = useGLTF(modelPath);
  const { actions, names } = useAnimations(animations, group);

  useEffect(() => {
    if (animationName && actions[animationName]) {
      actions[animationName]?.play();
    } else if (names.length > 0 && actions[names[0]]) {
      actions[names[0]]?.play();
    }
  }, [actions, animationName, names]);

  return { group, scene, actions, names };
}

// Usage
function AnimatedCharacter() {
  const { group, scene } = useAnimatedModel('/models/character.glb', 'Idle');

  return (
    <group ref={group}>
      <primitive object={scene} />
    </group>
  );
}
```

### Drei Library - Essential Helpers

```tsx
import {
  // Cameras & Controls
  PerspectiveCamera, OrthographicCamera, OrbitControls,
  FlyControls, PointerLockControls, TrackballControls,

  // Staging
  Environment, Sky, Stars, Cloud, ContactShadows,
  BakeShadows, AccumulativeShadows, RandomizedLight,

  // Abstractions
  Box, Sphere, Plane, Cone, Cylinder, Torus,
  Text, Text3D, Html, Billboard,

  // Loaders
  useGLTF, useFBX, useTexture, useCubeTexture,

  // Performance
  Instances, Instance, Merged, Detailed,

  // Misc
  useHelper, Grid, GizmoHelper, Stats, PerformanceMonitor,
  Center, Bounds, Shadow, Reflector
} from '@react-three/drei';

// Example: Performance-optimized instances
function Trees({ count = 100 }) {
  const { nodes } = useGLTF('/models/tree.glb');

  return (
    <Instances limit={count} geometry={nodes.tree.geometry}>
      <meshStandardMaterial color="green" />
      {Array.from({ length: count }, (_, i) => (
        <Instance
          key={i}
          position={[
            (Math.random() - 0.5) * 50,
            0,
            (Math.random() - 0.5) * 50,
          ]}
          rotation={[0, Math.random() * Math.PI * 2, 0]}
          scale={0.5 + Math.random() * 0.5}
        />
      ))}
    </Instances>
  );
}
```

---

## 🎮 PART 3: Character Systems & Animation

### Character Animation System

```typescript
// characterAnimation.ts
import * as THREE from 'three';

export class CharacterAnimationController {
  private mixer: THREE.AnimationMixer;
  private actions: Map<string, THREE.AnimationAction> = new Map();
  private currentAction: THREE.AnimationAction | null = null;

  constructor(model: THREE.Object3D, animations: THREE.AnimationClip[]) {
    this.mixer = new THREE.AnimationMixer(model);

    animations.forEach((clip) => {
      const action = this.mixer.clipAction(clip);
      this.actions.set(clip.name, action);
    });
  }

  play(name: string, fadeTime: number = 0.3) {
    const nextAction = this.actions.get(name);
    if (!nextAction) return;

    if (this.currentAction && this.currentAction !== nextAction) {
      this.currentAction.fadeOut(fadeTime);
    }

    nextAction.reset().fadeIn(fadeTime).play();
    this.currentAction = nextAction;
  }

  crossFade(fromName: string, toName: string, duration: number = 0.3) {
    const fromAction = this.actions.get(fromName);
    const toAction = this.actions.get(toName);

    if (fromAction && toAction) {
      fromAction.fadeOut(duration);
      toAction.reset().fadeIn(duration).play();
      this.currentAction = toAction;
    }
  }

  setWeight(name: string, weight: number) {
    const action = this.actions.get(name);
    if (action) action.setEffectiveWeight(weight);
  }

  update(deltaTime: number) {
    this.mixer.update(deltaTime);
  }

  getAction(name: string) {
    return this.actions.get(name);
  }
}
```

### Animation Retargeting with SkeletonUtils

```typescript
// retargeting.ts
import * as THREE from 'three';
import { SkeletonUtils } from 'three/examples/jsm/utils/SkeletonUtils';

export class AnimationRetargeter {
  /**
   * Retarget animation from one skeleton to another
   * Based on: https://github.com/upf-gti/retargeting-threejs
   */
  static retargetAnimation(
    sourceClip: THREE.AnimationClip,
    targetSkeleton: THREE.Skeleton,
    sourceSkeleton: THREE.Skeleton
  ): THREE.AnimationClip {
    // Use SkeletonUtils for retargeting
    const retargetedClip = SkeletonUtils.retargetClip(
      targetSkeleton.bones[0],
      sourceSkeleton.bones[0],
      sourceClip,
      {}
    );

    return retargetedClip;
  }

  /**
   * Load Mixamo animation and apply to custom character
   */
  static async loadMixamoAnimation(
    fbxPath: string,
    targetModel: THREE.Object3D,
    loader: any
  ): Promise<THREE.AnimationClip[]> {
    return new Promise((resolve, reject) => {
      loader.load(
        fbxPath,
        (fbx: any) => {
          // Extract animations
          const animations = fbx.animations;

          // Find skeletons
          const targetSkeleton = this.findSkeleton(targetModel);
          const sourceSkeleton = this.findSkeleton(fbx);

          if (!targetSkeleton || !sourceSkeleton) {
            reject(new Error('Skeleton not found'));
            return;
          }

          // Retarget all animations
          const retargetedClips = animations.map((clip: THREE.AnimationClip) =>
            this.retargetAnimation(clip, targetSkeleton, sourceSkeleton)
          );

          resolve(retargetedClips);
        },
        undefined,
        reject
      );
    });
  }

  private static findSkeleton(object: THREE.Object3D): THREE.Skeleton | null {
    let skeleton: THREE.Skeleton | null = null;

    object.traverse((child) => {
      if (child instanceof THREE.SkinnedMesh && child.skeleton) {
        skeleton = child.skeleton;
      }
    });

    return skeleton;
  }
}
```

### Mixamo Integration Workflow

```typescript
// mixamoIntegration.ts
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader';
import * as THREE from 'three';

export class MixamoCharacter {
  private model: THREE.Group;
  private mixer: THREE.AnimationMixer;
  private animations: Map<string, THREE.AnimationClip> = new Map();

  constructor(model: THREE.Group) {
    this.model = model;
    this.mixer = new THREE.AnimationMixer(model);
  }

  /**
   * Load character with embedded animations (GLB from Mixamo)
   */
  static async loadWithAnimations(url: string): Promise<MixamoCharacter> {
    const loader = new GLTFLoader();

    return new Promise((resolve, reject) => {
      loader.load(
        url,
        (gltf) => {
          const character = new MixamoCharacter(gltf.scene);

          // Add animations
          gltf.animations.forEach((clip) => {
            character.animations.set(clip.name, clip);
          });

          resolve(character);
        },
        undefined,
        reject
      );
    });
  }

  /**
   * Add separate animation file (FBX without skin)
   */
  async addAnimation(name: string, fbxPath: string): Promise<void> {
    const loader = new FBXLoader();

    return new Promise((resolve, reject) => {
      loader.load(
        fbxPath,
        (fbx) => {
          if (fbx.animations.length > 0) {
            this.animations.set(name, fbx.animations[0]);
          }
          resolve();
        },
        undefined,
        reject
      );
    });
  }

  play(name: string, loop: boolean = true) {
    const clip = this.animations.get(name);
    if (!clip) return;

    const action = this.mixer.clipAction(clip);
    action.loop = loop ? THREE.LoopRepeat : THREE.LoopOnce;
    action.play();

    return action;
  }

  update(deltaTime: number) {
    this.mixer.update(deltaTime);
  }

  getModel() {
    return this.model;
  }
}

// Usage Example
async function setupMixamoCharacter() {
  // Method 1: Load character with animations
  const character = await MixamoCharacter.loadWithAnimations(
    '/models/character-with-animations.glb'
  );

  // Method 2: Load character and add animations separately
  const character2 = await MixamoCharacter.loadWithAnimations(
    '/models/character.glb'
  );
  await character2.addAnimation('walk', '/animations/walking.fbx');
  await character2.addAnimation('run', '/animations/running.fbx');

  character2.play('walk');
}
```

### Ready Player Me Integration

```tsx
// ReadyPlayerMeAvatar.tsx
import { useEffect, useRef } from 'react';
import { useGLTF, useAnimations } from '@react-three/drei';
import * as THREE from 'three';

interface AvatarProps {
  avatarId: string;
  animationUrl?: string;
  position?: [number, number, number];
}

export function ReadyPlayerMeAvatar({
  avatarId,
  animationUrl,
  position = [0, 0, 0]
}: AvatarProps) {
  const group = useRef<THREE.Group>(null);
  const avatarUrl = `https://models.readyplayer.me/${avatarId}.glb`;

  const { scene, animations } = useGLTF(avatarUrl);
  const { actions, names } = useAnimations(animations, group);

  useEffect(() => {
    // Apply better lighting to RPM avatars
    scene.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        child.castShadow = true;
        child.receiveShadow = true;

        // Fix material issues
        if (child.material) {
          child.material.envMapIntensity = 1;
        }
      }
    });
  }, [scene]);

  useEffect(() => {
    // Play first animation or idle
    const actionName = names.includes('Idle') ? 'Idle' : names[0];
    if (actionName && actions[actionName]) {
      actions[actionName]?.play();
    }
  }, [actions, names]);

  return (
    <group ref={group} position={position}>
      <primitive object={scene} />
    </group>
  );
}

// Preload avatars for better performance
useGLTF.preload('https://models.readyplayer.me/your-avatar-id.glb');
```

---

## 🤖 PART 4: NPC AI & Game Behaviors

### Yuka.js Integration for Game AI

```bash
npm install yuka
```

```typescript
// npcAI.ts
import * as YUKA from 'yuka';
import * as THREE from 'three';

export class NPCController {
  private entityManager: YUKA.EntityManager;
  private time: YUKA.Time;
  private vehicle: YUKA.Vehicle;
  private mesh: THREE.Mesh;

  constructor(mesh: THREE.Mesh) {
    this.mesh = mesh;
    this.entityManager = new YUKA.EntityManager();
    this.time = new YUKA.Time();

    // Create vehicle (NPC)
    this.vehicle = new YUKA.Vehicle();
    this.vehicle.maxSpeed = 3;
    this.vehicle.maxForce = 10;
    this.vehicle.setRenderComponent(mesh, this.sync);

    this.entityManager.add(this.vehicle);
  }

  // Sync Three.js mesh with Yuka entity
  private sync(entity: YUKA.GameEntity, renderComponent: THREE.Object3D) {
    renderComponent.position.copy(entity.position as any);
    renderComponent.quaternion.copy(entity.rotation as any);
  }

  // Seek behavior - move towards target
  seekTarget(targetPosition: THREE.Vector3) {
    const seekBehavior = new YUKA.SeekBehavior(
      new YUKA.Vector3(targetPosition.x, targetPosition.y, targetPosition.z)
    );
    this.vehicle.steering.add(seekBehavior);
  }

  // Flee behavior - run away from threat
  fleeFrom(threatPosition: THREE.Vector3) {
    const fleeBehavior = new YUKA.FleeBehavior(
      new YUKA.Vector3(threatPosition.x, threatPosition.y, threatPosition.z)
    );
    this.vehicle.steering.add(fleeBehavior);
  }

  // Wander behavior - random movement
  enableWander() {
    const wanderBehavior = new YUKA.WanderBehavior();
    wanderBehavior.radius = 5;
    wanderBehavior.distance = 10;
    wanderBehavior.jitter = 2;
    this.vehicle.steering.add(wanderBehavior);
  }

  // Follow path behavior
  followPath(waypoints: THREE.Vector3[]) {
    const path = new YUKA.Path();
    waypoints.forEach((wp) => {
      path.add(new YUKA.Vector3(wp.x, wp.y, wp.z));
    });
    path.loop = true;

    const followPathBehavior = new YUKA.FollowPathBehavior(path, 0.5);
    this.vehicle.steering.add(followPathBehavior);
  }

  // Obstacle avoidance
  enableObstacleAvoidance(obstacles: YUKA.GameEntity[]) {
    const obstacleAvoidance = new YUKA.ObstacleAvoidanceBehavior(obstacles);
    this.vehicle.steering.add(obstacleAvoidance);
  }

  update() {
    const delta = this.time.update().getDelta();
    this.entityManager.update(delta);
  }

  getVehicle() {
    return this.vehicle;
  }
}
```

### Advanced NPC with State Machine

```typescript
// npcStateMachine.ts
import * as YUKA from 'yuka';

export class NPCWithStates extends YUKA.GameEntity {
  private stateMachine: YUKA.StateMachine<NPCWithStates>;
  private states: {
    idle: YUKA.State<NPCWithStates>;
    patrol: YUKA.State<NPCWithStates>;
    chase: YUKA.State<NPCWithStates>;
    attack: YUKA.State<NPCWithStates>;
    flee: YUKA.State<NPCWithStates>;
  };

  public target: YUKA.GameEntity | null = null;
  public health: number = 100;
  public detectionRadius: number = 10;
  public attackRange: number = 2;

  constructor() {
    super();
    this.stateMachine = new YUKA.StateMachine(this);
    this.states = this.setupStates();
    this.stateMachine.currentState = this.states.idle;
  }

  private setupStates() {
    // Idle State
    const idleState = new YUKA.State('idle');
    idleState.enter = () => console.log('NPC is idle');
    idleState.execute = (npc: NPCWithStates) => {
      // Check for nearby targets
      if (npc.detectTarget()) {
        npc.stateMachine.changeState(npc.states.chase);
      }
    };

    // Patrol State
    const patrolState = new YUKA.State('patrol');
    patrolState.execute = (npc: NPCWithStates) => {
      // Patrol logic
      if (npc.detectTarget()) {
        npc.stateMachine.changeState(npc.states.chase);
      }
    };

    // Chase State
    const chaseState = new YUKA.State('chase');
    chaseState.enter = () => console.log('NPC is chasing');
    chaseState.execute = (npc: NPCWithStates) => {
      if (!npc.target) {
        npc.stateMachine.changeState(npc.states.idle);
        return;
      }

      const distance = npc.position.distanceTo(npc.target.position);

      if (distance <= npc.attackRange) {
        npc.stateMachine.changeState(npc.states.attack);
      } else if (distance > npc.detectionRadius) {
        npc.stateMachine.changeState(npc.states.idle);
      }
    };

    // Attack State
    const attackState = new YUKA.State('attack');
    attackState.execute = (npc: NPCWithStates) => {
      if (!npc.target) {
        npc.stateMachine.changeState(npc.states.idle);
        return;
      }

      const distance = npc.position.distanceTo(npc.target.position);
      if (distance > npc.attackRange) {
        npc.stateMachine.changeState(npc.states.chase);
      }
    };

    // Flee State
    const fleeState = new YUKA.State('flee');
    fleeState.enter = () => console.log('NPC is fleeing');
    fleeState.execute = (npc: NPCWithStates) => {
      if (npc.health > 30) {
        npc.stateMachine.changeState(npc.states.idle);
      }
    };

    return {
      idle: idleState,
      patrol: patrolState,
      chase: chaseState,
      attack: attackState,
      flee: fleeState,
    };
  }

  detectTarget(): boolean {
    // Implement target detection logic
    return false; // Placeholder
  }

  update(delta: number): this {
    this.stateMachine.update();
    return this;
  }
}
```

### React Three Fiber NPC Component

```tsx
// NPCComponent.tsx
import { useRef, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import { useGLTF } from '@react-three/drei';
import { NPCController } from './npcAI';
import * as THREE from 'three';

interface NPCProps {
  modelPath: string;
  initialPosition: [number, number, number];
  behavior: 'wander' | 'patrol' | 'chase';
  waypoints?: [number, number, number][];
  target?: THREE.Vector3;
}

export function NPC({
  modelPath,
  initialPosition,
  behavior,
  waypoints,
  target
}: NPCProps) {
  const { scene } = useGLTF(modelPath);
  const groupRef = useRef<THREE.Group>(null);
  const npcController = useRef<NPCController | null>(null);

  useEffect(() => {
    if (!groupRef.current) return;

    // Find the first mesh in the scene hierarchy
    // For production, use scene.getObjectByName() or traverse to find specific mesh
    let mesh: THREE.Mesh | undefined;
    scene.traverse((child) => {
      if (!mesh && child instanceof THREE.Mesh) {
        mesh = child;
      }
    });

    if (!mesh) return;

    npcController.current = new NPCController(mesh);

    // Setup behavior
    switch (behavior) {
      case 'wander':
        npcController.current.enableWander();
        break;
      case 'patrol':
        if (waypoints) {
          const points = waypoints.map(wp => new THREE.Vector3(...wp));
          npcController.current.followPath(points);
        }
        break;
      case 'chase':
        if (target) {
          npcController.current.seekTarget(target);
        }
        break;
    }
  }, [behavior, waypoints, target, scene]);

  useFrame(() => {
    npcController.current?.update();
  });

  return (
    <group ref={groupRef} position={initialPosition}>
      <primitive object={scene} />
    </group>
  );
}
```

---

## 🎲 PART 5: Procedural Generation

### Procedural Character Generation

```typescript
// proceduralCharacter.ts
import * as THREE from 'three';

interface CharacterParameters {
  height: number;        // 0.5 - 1.5 (multiplier)
  bodyWidth: number;     // 0.7 - 1.3
  headSize: number;      // 0.8 - 1.2
  armLength: number;     // 0.8 - 1.2
  legLength: number;     // 0.9 - 1.1
  skinColor: THREE.Color;
  hairColor: THREE.Color;
}

export class ProceduralCharacterGenerator {
  /**
   * Generate a procedural humanoid character
   * Inspired by parametric models like SMPL
   */
  static generate(params: CharacterParameters): THREE.Group {
    const character = new THREE.Group();

    // Base measurements
    const baseHeight = 1.7 * params.height;
    const headHeight = 0.25 * params.headSize;
    const torsoHeight = 0.45 * baseHeight;
    const legHeight = 0.45 * baseHeight * params.legLength;
    const armLength = 0.35 * baseHeight * params.armLength;

    // Head
    const headGeo = new THREE.SphereGeometry(
      headHeight / 2,
      32,
      32
    );
    const headMat = new THREE.MeshStandardMaterial({
      color: params.skinColor
    });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.y = baseHeight - headHeight / 2;
    head.castShadow = true;
    character.add(head);

    // Torso
    const torsoGeo = new THREE.BoxGeometry(
      0.3 * params.bodyWidth,
      torsoHeight,
      0.2
    );
    const torso = new THREE.Mesh(torsoGeo, headMat);
    torso.position.y = baseHeight - headHeight - torsoHeight / 2;
    torso.castShadow = true;
    character.add(torso);

    // Arms
    const armGeo = new THREE.CylinderGeometry(0.04, 0.04, armLength, 8);
    const leftArm = new THREE.Mesh(armGeo, headMat);
    leftArm.position.set(
      -0.15 * params.bodyWidth - 0.04,
      baseHeight - headHeight - armLength / 2 - 0.05,
      0
    );
    leftArm.castShadow = true;
    character.add(leftArm);

    const rightArm = leftArm.clone();
    rightArm.position.x *= -1;
    character.add(rightArm);

    // Legs
    const legGeo = new THREE.CylinderGeometry(0.06, 0.05, legHeight, 8);
    const leftLeg = new THREE.Mesh(legGeo, headMat);
    leftLeg.position.set(
      -0.08,
      legHeight / 2,
      0
    );
    leftLeg.castShadow = true;
    character.add(leftLeg);

    const rightLeg = leftLeg.clone();
    rightLeg.position.x *= -1;
    character.add(rightLeg);

    // Hair (simple)
    const hairGeo = new THREE.SphereGeometry(headHeight / 2 + 0.02, 32, 32);
    const hairMat = new THREE.MeshStandardMaterial({
      color: params.hairColor
    });
    const hair = new THREE.Mesh(hairGeo, hairMat);
    hair.position.copy(head.position);
    hair.position.y += 0.02;
    hair.scale.set(1, 0.6, 1);
    character.add(hair);

    return character;
  }

  /**
   * Generate random character parameters
   */
  static randomParams(): CharacterParameters {
    return {
      height: 0.8 + Math.random() * 0.4,
      bodyWidth: 0.85 + Math.random() * 0.3,
      headSize: 0.9 + Math.random() * 0.2,
      armLength: 0.9 + Math.random() * 0.2,
      legLength: 0.95 + Math.random() * 0.1,
      skinColor: new THREE.Color().setHSL(
        0.08 + Math.random() * 0.05,
        0.3 + Math.random() * 0.3,
        0.4 + Math.random() * 0.3
      ),
      hairColor: new THREE.Color().setHSL(
        Math.random(),
        0.5 + Math.random() * 0.5,
        0.2 + Math.random() * 0.3
      ),
    };
  }
}

// Usage
const params = ProceduralCharacterGenerator.randomParams();
const character = ProceduralCharacterGenerator.generate(params);
scene.add(character);
```

### Procedural Terrain Generation

```bash
npm install simplex-noise
```

```typescript
// proceduralTerrain.ts
import * as THREE from 'three';
import { SimplexNoise } from 'simplex-noise';

export class TerrainGenerator {
  static generate(
    width: number,
    depth: number,
    segments: number,
    heightScale: number = 10
  ): THREE.Mesh {
    const geometry = new THREE.PlaneGeometry(
      width,
      depth,
      segments,
      segments
    );

    const noise = new SimplexNoise();
    const vertices = geometry.attributes.position.array;

    for (let i = 0; i < vertices.length; i += 3) {
      const x = vertices[i];
      const z = vertices[i + 1];

      // Multi-octave noise for realistic terrain
      let height = 0;
      height += noise.noise2D(x * 0.01, z * 0.01) * heightScale;
      height += noise.noise2D(x * 0.05, z * 0.05) * (heightScale * 0.25);
      height += noise.noise2D(x * 0.1, z * 0.1) * (heightScale * 0.125);

      vertices[i + 2] = height;
    }

    geometry.computeVertexNormals();
    geometry.rotateX(-Math.PI / 2);

    // Vertex coloring based on height
    const colors: number[] = [];
    for (let i = 0; i < vertices.length; i += 3) {
      const height = vertices[i + 2];
      const color = new THREE.Color();

      if (height < 0) {
        color.setHex(0x3a7bc8); // Water
      } else if (height < 2) {
        color.setHex(0xc2b280); // Sand
      } else if (height < 5) {
        color.setHex(0x567d46); // Grass
      } else {
        color.setHex(0x8b7355); // Mountain
      }

      colors.push(color.r, color.g, color.b);
    }

    geometry.setAttribute(
      'color',
      new THREE.Float32BufferAttribute(colors, 3)
    );

    const material = new THREE.MeshStandardMaterial({
      vertexColors: true,
      flatShading: true,
    });

    return new THREE.Mesh(geometry, material);
  }
}
```

### Procedural Buildings

```typescript
// proceduralBuilding.ts
import * as THREE from 'three';

export class BuildingGenerator {
  static generateBuilding(
    floors: number = 3 + Math.floor(Math.random() * 7),
    floorHeight: number = 3,
    width: number = 5 + Math.random() * 5,
    depth: number = 5 + Math.random() * 5
  ): THREE.Group {
    const building = new THREE.Group();

    // Building material
    const wallMaterial = new THREE.MeshStandardMaterial({
      color: new THREE.Color().setHSL(0, 0, 0.6 + Math.random() * 0.2),
      roughness: 0.8,
    });

    // Create floors
    for (let i = 0; i < floors; i++) {
      const floorGeo = new THREE.BoxGeometry(width, floorHeight, depth);
      const floor = new THREE.Mesh(floorGeo, wallMaterial);
      floor.position.y = i * floorHeight + floorHeight / 2;
      floor.castShadow = true;
      floor.receiveShadow = true;
      building.add(floor);

      // Add windows
      BuildingGenerator.addWindows(floor, width, depth, floorHeight);
    }

    // Roof
    const roofGeo = new THREE.ConeGeometry(
      Math.max(width, depth) * 0.7,
      floorHeight,
      4
    );
    const roofMat = new THREE.MeshStandardMaterial({ color: 0x8b4513 });
    const roof = new THREE.Mesh(roofGeo, roofMat);
    roof.position.y = floors * floorHeight + floorHeight / 2;
    roof.rotation.y = Math.PI / 4;
    roof.castShadow = true;
    building.add(roof);

    return building;
  }

  private static addWindows(
    floor: THREE.Mesh,
    width: number,
    depth: number,
    height: number
  ) {
    const windowMaterial = new THREE.MeshStandardMaterial({
      color: 0x87ceeb,
      emissive: 0x87ceeb,
      emissiveIntensity: 0.3,
    });

    const windowSize = 0.8;
    const windowDepth = 0.1;

    // Front and back windows
    for (let i = -1; i <= 1; i += 2) {
      const windowGeo = new THREE.BoxGeometry(
        windowSize,
        windowSize,
        windowDepth
      );
      const window = new THREE.Mesh(windowGeo, windowMaterial);
      window.position.set(0, 0, (depth / 2 + windowDepth / 2) * i);
      floor.add(window);
    }
  }
}
```

---

## ⚡ PART 6: Physics & Character Controllers

### Rapier Physics Integration

```bash
npm install @react-three/rapier
```

```tsx
// PhysicsScene.tsx
import { Physics, RigidBody, CuboidCollider } from '@react-three/rapier';
import { Canvas } from '@react-three/fiber';

function PhysicsScene() {
  return (
    <Canvas>
      <Physics gravity={[0, -9.81, 0]}>
        {/* Ground */}
        <RigidBody type="fixed">
          <mesh rotation={[-Math.PI / 2, 0, 0]}>
            <planeGeometry args={[100, 100]} />
            <meshStandardMaterial color="gray" />
          </mesh>
        </RigidBody>

        {/* Dynamic objects */}
        <RigidBody position={[0, 5, 0]}>
          <mesh castShadow>
            <boxGeometry />
            <meshStandardMaterial color="red" />
          </mesh>
        </RigidBody>
      </Physics>

      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} castShadow />
    </Canvas>
  );
}
```

### Character Controller with Physics

```tsx
// CharacterController.tsx
import { useRef, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import { RigidBody, CapsuleCollider, RapierRigidBody } from '@react-three/rapier';
import { useKeyboardControls } from '@react-three/drei';
import * as THREE from 'three';

interface CharacterControllerProps {
  position?: [number, number, number];
}

export function CharacterController({ position = [0, 2, 0] }: CharacterControllerProps) {
  const rigidBodyRef = useRef<RapierRigidBody>(null);
  const [, get] = useKeyboardControls();

  const velocity = useRef(new THREE.Vector3());
  const direction = useRef(new THREE.Vector3());

  const moveSpeed = 5;
  const jumpForce = 5;

  useFrame((state, delta) => {
    if (!rigidBodyRef.current) return;

    const { forward, backward, left, right, jump } = get();

    // Get current velocity
    const currentVel = rigidBodyRef.current.linvel();
    velocity.current.set(currentVel.x, currentVel.y, currentVel.z);

    // Calculate movement direction
    direction.current.set(0, 0, 0);
    if (forward) direction.current.z -= 1;
    if (backward) direction.current.z += 1;
    if (left) direction.current.x -= 1;
    if (right) direction.current.x += 1;

    direction.current.normalize();

    // Apply movement
    velocity.current.x = direction.current.x * moveSpeed;
    velocity.current.z = direction.current.z * moveSpeed;

    // Jump
    if (jump && Math.abs(currentVel.y) < 0.1) {
      velocity.current.y = jumpForce;
    }

    rigidBodyRef.current.setLinvel(velocity.current, true);
  });

  return (
    <RigidBody
      ref={rigidBodyRef}
      position={position}
      lockRotations={true}
    >
      <CapsuleCollider args={[0.5, 0.5]} />
      <mesh castShadow>
        <capsuleGeometry args={[0.5, 1]} />
        <meshStandardMaterial color="blue" />
      </mesh>
    </RigidBody>
  );
}

// Keyboard controls setup
import { KeyboardControls } from '@react-three/drei';

const keyboardMap = [
  { name: 'forward', keys: ['ArrowUp', 'KeyW'] },
  { name: 'backward', keys: ['ArrowDown', 'KeyS'] },
  { name: 'left', keys: ['ArrowLeft', 'KeyA'] },
  { name: 'right', keys: ['ArrowRight', 'KeyD'] },
  { name: 'jump', keys: ['Space'] },
];

function App() {
  return (
    <KeyboardControls map={keyboardMap}>
      <Canvas>
        {/* Your scene */}
        <CharacterController />
      </Canvas>
    </KeyboardControls>
  );
}
```

---

## 📚 PART 7: Academic References & Research

### Character Animation & Retargeting

**Key Concepts:**
- **IK (Inverse Kinematics)**: Calculate joint angles to reach target positions (e.g., hand placement)
- **FK (Forward Kinematics)**: Calculate end position from joint angles
- **Retargeting**: Transfer animations between different skeletal structures

**Research Areas:**
1. **Motion Retargeting Techniques**
   - Skeleton correspondence construction
   - Preserving motion characteristics during transfer
   - IK-based vs FK-based approaches

2. **Implementation References:**
   - SkeletonUtils (Three.js) for basic retargeting
   - upf-gti/retargeting-threejs - Open source retargeting solver
   - Mixamo workflow with Blender for manual retargeting

### Parametric Body Models

#### SMPL (Skinned Multi-Person Linear)

- Parametric model encoding body shape and pose with ~100 parameters
- Applications: avatar creation, virtual try-on, motion capture
- Web implementation possible with SMPL-X JavaScript libraries

**Modern Approaches:**
- **AvatarForge**: AI-driven multimodal avatar generation
- **SmartAvatar**: VLM-based parametric avatar creation
- **FaceMaker**: Procedural facial feature generation

**Academic Papers:**
1. "FaceMaker—A Procedural Face Generator to Foster Character Design Research"
2. "Parametric 3D human modeling with biharmonic SMPL"
3. "AvatarCraft: Transforming Text into Neural Human Avatars"

### Game AI & Pathfinding

**Steering Behaviors (Craig Reynolds):**
- Seek, Flee, Pursue, Evade
- Wander, Arrive, Obstacle Avoidance
- Path Following, Leader Following

**Pathfinding Algorithms:**
- A* (A-Star) for optimal paths
- Navigation meshes for 3D environments
- Dynamic pathfinding for moving obstacles

**State Machines:**
- Finite State Machines (FSM) for behavior control
- Hierarchical State Machines for complex NPCs
- Goal-Oriented Action Planning (GOAP)

**Implementation:**
- Yuka.js - Complete game AI library for web
- Integration with Three.js and React Three Fiber

### Procedural Generation

**Noise Functions:**
- Perlin Noise - Smooth, natural-looking randomness
- Simplex Noise - Improved performance, no directional artifacts
- Multi-octave noise for realistic terrain

**Procedural Techniques:**
- L-Systems for organic structures (trees, plants)
- Wave Function Collapse for level generation
- Marching Cubes for volumetric terrain
- Parametric models for character variation

---

## 🎯 Best Practices Summary

### React Three Fiber

**DO:**
- Use `useFrame` for animations, not `setInterval`
- Leverage drei helpers for common tasks
- Use `<Instances>` for repeated geometries
- Implement proper cleanup in useEffect
- Use Suspense for lazy loading models
- Enable `concurrent` mode for better performance

**DON'T:**
- Create Three.js objects in render (use useMemo)
- Forget to dispose of geometries/materials
- Use too many lights (performance impact)
- Skip `dpr` limiting on mobile devices

### Character Systems

**DO:**
- Use GLTFLoader for web (not FBX when possible)
- Implement animation blending with fadeIn/fadeOut
- Cache loaded models with useGLTF.preload()
- Use Mixamo for quick prototyping
- Implement proper skeleton hierarchy

**DON'T:**
- Mix incompatible skeletal structures
- Skip bone name verification in retargeting
- Forget to update animation mixer each frame
- Load uncompressed models in production

### NPC & Game AI

**DO:**
- Use Yuka.js for production-ready AI
- Implement state machines for complex behaviors
- Optimize AI update frequency (not every frame)
- Use spatial partitioning for large NPC counts
- Add perception systems (vision, hearing)

**DON'T:**
- Run pathfinding every frame
- Skip behavior priority systems
- Forget performance budgets for AI
- Hardcode behavior values (use configuration)

### Physics

**DO:**
- Use Rapier for best web performance
- Implement CCD for fast-moving objects
- Use compound colliders for complex shapes
- Limit physics updates to 60Hz
- Implement sleep states for static objects

**DON'T:**
- Use mesh colliders for everything
- Skip collision layers/masks
- Run physics at render framerate
- Forget to cleanup physics objects

---

## 🔗 Essential Resources

### Documentation
- [Three.js](https://threejs.org/docs/)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- [Drei](https://github.com/pmndrs/drei)
- [Yuka.js](https://mugen87.github.io/yuka/)
- [Rapier](https://rapier.rs/)

### Model Resources
- [Ready Player Me](https://readyplayer.me/)
- [Mixamo](https://www.mixamo.com/)
- [Sketchfab](https://sketchfab.com/)
- [Poly Haven](https://polyhaven.com/)

### Learning
- [Three.js Journey](https://threejs-journey.com/)
- [Discover Three.js](https://discoverthreejs.com/)
- [Bruno Simon's Portfolio](https://bruno-simon.com/)

---

## ✅ Complete Checklist

### Basic Setup
- [ ] Three.js or R3F installed
- [ ] Scene, camera, renderer configured
- [ ] Lighting system implemented
- [ ] Controls added (OrbitControls/PointerLock)
- [ ] Responsive canvas sizing

### Character System
- [ ] GLTF/GLB loader implemented
- [ ] Animation system working
- [ ] Character controller (if needed)
- [ ] Ready Player Me or Mixamo integration
- [ ] Animation blending functional

### Game Features (if applicable)
- [ ] NPC AI with Yuka.js
- [ ] Physics with Rapier
- [ ] Collision detection
- [ ] State management
- [ ] Input handling

### Procedural Generation (if applicable)
- [ ] Terrain generation
- [ ] Character variations
- [ ] Procedural buildings/props
- [ ] Noise-based systems

### Performance
- [ ] Instancing for repeated objects
- [ ] LOD system implemented
- [ ] Frustum culling enabled
- [ ] Texture optimization
- [ ] Shadow map optimization
- [ ] Post-processing optimized

### Production Ready
- [ ] Error boundaries added
- [ ] Loading states implemented
- [ ] Mobile optimization
- [ ] Proper cleanup/disposal
- [ ] Asset preloading
- [ ] Performance monitoring
