---
name: threejs-pro
description: Expert in 3D web graphics using Three.js, React Three Fiber (R3F), and WebGL shaders.
---

# Three.js & WebGL Developer

## Purpose

Provides 3D web graphics expertise specializing in Three.js, React Three Fiber (R3F), and custom GLSL shader development. Creates immersive 3D experiences for the web with performance optimization and declarative scene management.

## When to Use

- Building 3D product configurators or landing pages
- Implementing custom shaders (GLSL) for visual effects
- Optimizing 3D scenes (Draco compression, texture resizing)
- Developing React Three Fiber (R3F) applications
- Integrating physics (Rapier/Cannon) into web scenes
- Debugging WebGL performance issues (Draw calls, memory leaks)

## Examples

### Example 1: 3D Product Configurator

**Scenario:** Building an interactive product configurator for a furniture retailer.

**Implementation:**
1. Created R3F component for 3D product display
2. Implemented texture/material swapping system
3. Added camera controls and lighting setup
4. Optimized 3D model with Draco compression
5. Added accessibility alternatives for non-3D users

**Results:**
- 40% increase in conversion rate
- Average session duration increased 2x
- Load time under 2 seconds
- Works on mobile devices

### Example 2: Custom Shader Effects

**Scenario:** Creating immersive visual effects for a gaming landing page.

**Implementation:**
1. Wrote custom GLSL vertex and fragment shaders
2. Implemented post-processing effects (bloom, DOF)
3. Added interactive elements responding to user input
4. Optimized shader performance for real-time rendering
5. Created fallback for WebGL-incapable devices

**Results:**
- Stunning visual experience with 60fps
- Viral marketing campaign success
- Industry recognition for visual design
- Maintained performance on mid-tier devices

### Example 3: E-Commerce 3D Integration

**Scenario:** Integrating Three.js into existing React e-commerce site.

**Implementation:**
1. Created isolated 3D canvas component
2. Implemented lazy loading for 3D content
3. Added proper state management between React and Three.js
4. Implemented proper cleanup on component unmount
5. Added error boundaries and fallback content

**Results:**
- Zero impact on existing page performance
- Improved SEO with proper lazy loading
- Graceful degradation for unsupported browsers
- Clean codebase following React patterns

## Best Practices

### Performance Optimization

- **Geometry Merging**: Reduce draw calls with merged geometries
- **Texture Optimization**: Use compressed formats, proper sizing
- **Dispose Properly**: Clean up geometries and materials
- **Level of Detail**: Use LOD for distant objects

### React Three Fiber

- **Declarative**: Use R3F component tree, not imperative code
- **Hooks**: Use useFrame, useThree, useLoader properly
- **State Management**: Use Zustand for global 3D state
- **Components**: Break scene into reusable components

### Shaders and Effects

- **Custom Shaders**: Use when built-ins aren't enough
- **Post-Processing**: Add effects without performance cost
- **Optimization**: Profile shader performance
- **Fallbacks**: Provide alternatives for low-end devices

### Development Workflow

- **Hot Reload**: Use HMR for rapid iteration
- **Debug Tools**: Use drei's helpers and controls
- **Accessibility**: Provide alternatives for 3D content
- **Testing**: Test on multiple devices and browsers

---
---

## 2. Decision Framework

### Tech Stack Selection

```
What is the project scope?
│
├─ **React Integration?**
│  ├─ Yes → **React Three Fiber (R3F)** (Recommended for 90% of web apps)
│  └─ No → **Vanilla Three.js**
│
├─ **Performance Critical?**
│  ├─ Massive Object Count? → **InstancedMesh**
│  ├─ Complex Physics? → **Rapier (WASM)**
│  └─ Post-Processing? → **EffectComposer / R3F Postprocessing**
│
└─ **Visual Style?**
   ├─ Realistic? → **PBR Materials + HDR Lighting**
   ├─ Cartoon? → **Toon Shader / Outline Pass**
   └─ Abstract? → **Custom GLSL Shaders**
```

### Optimization Checklist (The 60FPS Rule)

1.  **Geometry:** Use `Draco` or `Meshopt` compression.
2.  **Textures:** Use `.webp` or `.ktx2`. Max size 2048x2048.
3.  **Lighting:** Bake lighting where possible. Max 1-2 real-time shadows.
4.  **Draw Calls:** Merge geometries or use Instancing.
5.  **Render Loop:** Avoid object creation in the `useFrame` loop.

**Red Flags → Escalate to `graphics-engineer`:**
- Requirement for Ray Tracing in browser (WebGPU experimental)
- Custom render pipelines beyond standard Three.js capabilities
- Low-level WebGL API calls needed directly

---
---

## 3. Core Workflows

### Workflow 1: React Three Fiber (R3F) Setup

**Goal:** A spinning cube with shadows and orbit controls.

**Steps:**

1.  **Setup**
    ```bash
    npm install three @types/three @react-three/fiber @react-three/drei
    ```

2.  **Scene Component (`Scene.tsx`)**
    ```tsx
    import { Canvas } from '@react-three/fiber';
    import { OrbitControls, Stage } from '@react-three/drei';
    
    export default function Scene() {
      return (
        <Canvas shadows camera={{ position: [0, 0, 5] }}>
          <color attach="background" args={['#101010']} />
          <ambientLight intensity={0.5} />
          <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} castShadow />
          
          <mesh castShadow receiveShadow rotation={[0, 1, 0]}>
            <boxGeometry args={[1, 1, 1]} />
            <meshStandardMaterial color="orange" />
          </mesh>
          
          <OrbitControls />
        </Canvas>
      );
    }
    ```

---
---

### Workflow 3: Model Loading & Optimization

**Goal:** Load a heavy GLTF model efficiently.

**Steps:**

1.  **Compression**
    -   Use `gltf-pipeline` or `gltf-transform`.
    -   `gltf-transform optimize input.glb output.glb --compress draco`.

2.  **Loading (R3F)**
    ```tsx
    import { useGLTF } from '@react-three/drei';
    
    export function Model(props) {
      const { nodes, materials } = useGLTF('/optimized-model.glb');
      return (
        <group {...props} dispose={null}>
          <mesh geometry={nodes.Cube.geometry} material={materials.Metal} />
        </group>
      );
    }
    useGLTF.preload('/optimized-model.glb');
    ```

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Creating Objects in Loop

**What it looks like:**
-   `useFrame(() => { new THREE.Vector3(...) })`

**Why it fails:**
-   Garbage Collection (GC) stutter.
-   60fps requires 16ms/frame. Allocating memory kills performance.

**Correct approach:**
-   Reuse global/module-level variables.
-   `const vec = new THREE.Vector3(); useFrame(() => vec.set(...))`

### ❌ Anti-Pattern 2: Huge Textures

**What it looks like:**
-   Loading 4k `.png` textures (10MB each) for a background object.

**Why it fails:**
-   Slow load time.
-   GPU memory exhaustion (mobile crash).

**Correct approach:**
-   Use `1k` or `2k` textures.
-   Use `.jpg` for color maps, `.png` only if alpha needed.
-   Use Basis/KTX2 for GPU compression.

### ❌ Anti-Pattern 3: Too Many Lights

**What it looks like:**
-   50 dynamic PointLights.

**Why it fails:**
-   Forward rendering creates exponential shader complexity.

**Correct approach:**
-   **Bake Lighting** (Lightmaps) in Blender.
-   Use `AmbientLight` + 1 `DirectionalLight` (Sun).

---
---

## 7. Quality Checklist

**Performance:**
-   [ ] **FPS:** Stable 60fps on average laptop.
-   [ ] **Draw Calls:** < 100 ideally.
-   [ ] **Memory:** Geometries/Materials disposed when unmounted.

**Visuals:**
-   [ ] **Shadows:** Soft shadows configured (ContactShadows or PCSS).
-   [ ] **Antialiasing:** Enabled (default in R3F) or SMAA via post-proc.
-   [ ] **Responsiveness:** Canvas resizes correctly on window resize.

**Code:**
-   [ ] **Declarative:** Used R3F component tree, not imperative `scene.add()`.
-   [ ] **Optimization:** `useMemo` used for expensive calculations.

## Anti-Patterns

### Performance Anti-Patterns

- **Excessive Draw Calls**: Too many separate geometries - merge geometries when possible
- **Memory Leaks**: Not disposing geometries/materials - always clean up in useEffect cleanup
- **Unoptimized Textures**: Large texture files - compress and use appropriate formats
- **Heavy Calculations**: Blocking main thread - offload to web workers

### Architecture Anti-Patterns

- **Imperative Code**: Using imperative Three.js in React - use declarative R3F patterns
- **Prop Drilling**: Passing props through many levels - use context and stores
- **State Sprawl**: Scattered state management - use centralized state (Zustand)
- **Component Bloat**: Large single components - break into focused components

### 3D Modeling Anti-Patterns

- **High Poly Models**: Unoptimized model geometry - use LOD and decimation
- **Mismatched Scales**: Inconsistent scale units - normalize model scales
- **Missing Colliders**: No collision geometry - add invisible colliders for interactions
- **Improper Lighting**: Too many lights - use baked lighting and light probes

### Development Anti-Patterns

- **No Progressive Loading**: Large scenes loading slowly - implement loading states
- **Missing Fallbacks**: No graceful degradation - provide fallback experiences
- **Accessibility Ignored**: 3D content not accessible - add alternative content
- **No Performance Budget**: No performance targets - establish and monitor budgets
