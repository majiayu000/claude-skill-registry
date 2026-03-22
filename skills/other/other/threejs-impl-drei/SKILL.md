---
name: threejs-impl-drei
description: >
  Use when using Drei helper components with React Three Fiber:
  controls, environment maps, text rendering, HTML overlays, or
  performance helpers. Prevents the common mistake of not wrapping
  useGLTF in Suspense, using wrong Environment preset name, or
  forgetting makeDefault on controls. Covers 150+ Drei components
  across controls, environment, text, materials, loaders, performance.
  Keywords: Drei, @react-three/drei, OrbitControls, Environment,
  useGLTF, useTexture, Html, Text, Stage, ContactShadows, Instances.
license: MIT
compatibility: "Designed for Claude Code. Requires @react-three/drei, @react-three/fiber 8.x+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-impl-drei

## Quick Reference

### Installation

```bash
npm install @react-three/drei @react-three/fiber three
```

### Critical Warnings

**ALWAYS** wrap components that use loader hooks (`useGLTF`, `useTexture`, `useFBX`, `useKTX2`, `useFont`) in `<Suspense fallback={...}>`. Omitting Suspense causes the entire React tree to crash.

**ALWAYS** add `makeDefault` to your primary camera controls (`<OrbitControls makeDefault />`). Without `makeDefault`, Drei controls do NOT integrate with R3F's event system and pointer events break.

**NEVER** use an invalid `Environment` preset name. The ONLY valid presets are: `apartment`, `city`, `dawn`, `forest`, `lobby`, `night`, `park`, `studio`, `sunset`, `warehouse`.

**NEVER** forget to call `.preload()` for critical assets. Use `useGLTF.preload('/model.glb')` at module scope to start loading before component mount.

**ALWAYS** use `<Instances>` for rendering more than 100 identical meshes. Individual meshes cause one draw call each; instances batch them into one.

---

## Controls

### OrbitControls

The most common camera control. Orbit, zoom, and pan around a target.

```jsx
import { OrbitControls } from '@react-three/drei'

<OrbitControls
  makeDefault           // ALWAYS add — integrates with R3F events
  enableDamping         // smooth movement
  dampingFactor={0.05}
  minDistance={2}
  maxDistance={20}
  minPolarAngle={0}
  maxPolarAngle={Math.PI / 2}  // prevent going below ground
/>
```

### Other Controls

| Component | Use Case |
|-----------|----------|
| `CameraControls` | Full-featured camera (recommended for complex scenes) |
| `MapControls` | Top-down map navigation (orbit restricted to vertical axis) |
| `PresentationControls` | Drag-to-rotate with spring physics (product viewers) |
| `ScrollControls` | Scroll-driven animation (`pages` prop sets scroll length) |
| `TransformControls` | Translate/rotate/scale gizmo on selected objects |
| `DragControls` | Drag objects in 3D space |
| `KeyboardControls` | Keyboard input as React context |
| `FaceControls` | Face-tracking camera movement |

### ScrollControls Pattern

```jsx
import { ScrollControls, useScroll } from '@react-three/drei'

<ScrollControls pages={3} damping={0.1}>
  <ScrollScene />
</ScrollControls>

function ScrollScene() {
  const scroll = useScroll()
  useFrame(() => {
    const offset = scroll.offset // 0 to 1
  })
  return <mesh />
}
```

---

## Environment and Staging

### Environment

Loads HDR environment maps for realistic reflections and lighting.

```jsx
import { Environment } from '@react-three/drei'

// Preset (downloads from polyhaven CDN)
<Environment preset="city" background blur={0.5} />

// Custom HDR file
<Environment files="/env.hdr" background />

// Custom environment with Lightformers
<Environment background>
  <Lightformer form="rect" intensity={2} position={[0, 5, -5]} scale={[10, 5, 1]} />
</Environment>
```

**Valid presets:** `apartment`, `city`, `dawn`, `forest`, `lobby`, `night`, `park`, `studio`, `sunset`, `warehouse`.

### Stage

Complete lighting and shadow setup in one component. Ideal for product viewers.

```jsx
import { Stage } from '@react-three/drei'

<Stage preset="rembrandt" intensity={0.5} environment="city" adjustCamera>
  <Model />
</Stage>
```

### Shadow Components

| Component | Use Case | Key Props |
|-----------|----------|-----------|
| `ContactShadows` | Soft ground shadows (no light needed) | `opacity`, `scale`, `blur`, `far`, `resolution`, `color` |
| `AccumulativeShadows` | High-quality baked soft shadows | `frames`, `alphaTest`, `scale`, `opacity` |
| `RandomizedLight` | Child of AccumulativeShadows | `amount`, `radius`, `intensity`, `position` |
| `BakeShadows` | Bake shadow maps once, stop updating | — |
| `SoftShadows` | PCSS soft shadows for real-time lights | — |

### AccumulativeShadows Pattern

```jsx
<AccumulativeShadows temporal frames={100} scale={10} position={[0, -0.5, 0]}>
  <RandomizedLight amount={8} radius={4} position={[5, 5, -10]} />
</AccumulativeShadows>
```

### Atmosphere

| Component | Purpose | Key Props |
|-----------|---------|-----------|
| `Sky` | Procedural sky dome | `sunPosition`, `turbidity`, `rayleigh` |
| `Stars` | Particle starfield | `radius`, `count`, `factor`, `fade` |
| `Sparkles` | Floating particles | `count`, `size`, `speed`, `color` |
| `Cloud` | Volumetric clouds | `opacity`, `speed`, `segments`, `bounds` |

---

## Text and HTML

### Text (SDF)

High-quality 2D text rendered with signed distance fields via troika-three-text.

```jsx
import { Text } from '@react-three/drei'

<Text
  fontSize={0.5}
  color="white"
  anchorX="center"
  anchorY="middle"
  maxWidth={2}
  font="/fonts/Inter-Bold.woff"
>
  Hello World
</Text>
```

### Text3D

Extruded 3D geometry text. Requires a JSON font file (use `facetype.js` to convert).

```jsx
import { Text3D, Center } from '@react-three/drei'

<Center>
  <Text3D font="/fonts/Inter_Bold.json" size={0.75} height={0.2} bevelEnabled bevelSize={0.02}>
    Hello
    <meshStandardMaterial color="orange" />
  </Text3D>
</Center>
```

### Html

Renders DOM elements positioned in 3D space.

```jsx
import { Html } from '@react-three/drei'

<mesh position={[0, 2, 0]}>
  <Html
    transform            // transforms with 3D position
    distanceFactor={10}  // scales with distance
    occlude              // hides behind 3D objects
    center               // centers the HTML element
    className="label"
  >
    <div style={{ color: 'white' }}>Annotation</div>
  </Html>
</mesh>
```

### Billboard

ALWAYS faces the camera. Use for labels and sprites.

```jsx
import { Billboard, Text } from '@react-three/drei'

<Billboard follow={true} lockX={false} lockY={false} lockZ={false}>
  <Text fontSize={0.5}>Always Visible</Text>
</Billboard>
```

### Hud

Renders a heads-up display in a separate orthographic scene.

```jsx
import { Hud, OrthographicCamera } from '@react-three/drei'

<Hud renderPriority={1}>
  <OrthographicCamera makeDefault position={[0, 0, 5]} />
  <Text position={[0, 0, 0]} fontSize={0.1}>HUD Text</Text>
</Hud>
```

---

## Materials

| Component | Purpose |
|-----------|---------|
| `MeshReflectorMaterial` | Reflective floors with blur, distortion, resolution |
| `MeshTransmissionMaterial` | Glass with chromatic aberration, distortion, thickness |
| `MeshRefractionMaterial` | Refraction using environment cube map |
| `MeshWobbleMaterial` | Animated wobble on MeshStandardMaterial |
| `MeshDistortMaterial` | Perlin noise distortion on MeshStandardMaterial |
| `MeshDiscardMaterial` | Renders nothing (shadow-only objects) |
| `shaderMaterial` | Helper to create custom ShaderMaterial as JSX |

### MeshReflectorMaterial Example

```jsx
<mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.5, 0]}>
  <planeGeometry args={[50, 50]} />
  <MeshReflectorMaterial
    blur={[300, 100]}
    resolution={1024}
    mixBlur={1}
    mixStrength={50}
    roughness={1}
    depthScale={1.2}
    minDepthThreshold={0.4}
    maxDepthThreshold={1.4}
    color="#151515"
    metalness={0.5}
  />
</mesh>
```

### shaderMaterial Helper

```jsx
import { shaderMaterial } from '@react-three/drei'
import { extend } from '@react-three/fiber'

const WaveMaterial = shaderMaterial(
  { uTime: 0, uColor: new THREE.Color(0.2, 0.0, 0.1) },
  /* vertex */ `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
  /* fragment */ `uniform float uTime; uniform vec3 uColor; varying vec2 vUv; void main() { gl_FragColor = vec4(vUv * uColor, 1.0); }`
)
extend({ WaveMaterial })
// Usage: <waveMaterial uTime={clock.elapsedTime} />
```

---

## Loaders

**ALWAYS** wrap loader-consuming components in `<Suspense>`.

| Hook | Returns | Preload |
|------|---------|---------|
| `useGLTF(url)` | `{ nodes, materials, scene, animations }` | `useGLTF.preload(url)` |
| `useTexture(url)` | `THREE.Texture` or map object | `useTexture.preload(url)` |
| `useFBX(url)` | `THREE.Group` | `useFBX.preload(url)` |
| `useKTX2(url)` | Compressed texture | `useKTX2.preload(url)` |
| `useFont(url)` | Font data for Text3D | `useFont.preload(url)` |
| `useAnimations(clips, ref)` | `{ actions, names, mixer, ref }` | — |
| `useVideoTexture(url)` | `THREE.VideoTexture` | — |

### useGLTF Pattern

```jsx
import { useGLTF } from '@react-three/drei'

function Model(props) {
  const { nodes, materials } = useGLTF('/model.glb')
  return (
    <group {...props}>
      <mesh geometry={nodes.Body.geometry} material={materials.Metal} />
    </group>
  )
}
useGLTF.preload('/model.glb')
```

### useTexture with Multiple Maps

```jsx
const textures = useTexture({
  map: '/color.jpg',
  normalMap: '/normal.jpg',
  roughnessMap: '/roughness.jpg',
  aoMap: '/ao.jpg',
})
// Spread directly onto material
<meshStandardMaterial {...textures} />
```

### useAnimations Pattern

```jsx
function AnimatedModel() {
  const group = useRef()
  const { nodes, animations } = useGLTF('/character.glb')
  const { actions } = useAnimations(animations, group)

  useEffect(() => {
    actions['Walk']?.play()
    return () => actions['Walk']?.stop()
  }, [actions])

  return <group ref={group}><primitive object={nodes.Scene} /></group>
}
```

---

## Performance

### Instances

ALWAYS use for large numbers of identical meshes (>100). Reduces draw calls from N to 1.

```jsx
import { Instances, Instance } from '@react-three/drei'

<Instances limit={1000} range={1000}>
  <boxGeometry />
  <meshStandardMaterial />
  {positions.map((pos, i) => (
    <Instance key={i} position={pos} color="orange" />
  ))}
</Instances>
```

### Merged

Merges different geometries into a single draw call.

```jsx
import { Merged } from '@react-three/drei'

function Furniture({ nodes }) {
  return (
    <Merged meshes={[nodes.Chair, nodes.Table, nodes.Lamp]}>
      {(Chair, Table, Lamp) => (
        <>
          <Chair position={[0, 0, 0]} />
          <Table position={[2, 0, 0]} />
          <Lamp position={[1, 1, 0]} />
        </>
      )}
    </Merged>
  )
}
```

### Performance Helpers

| Component | Purpose |
|-----------|---------|
| `Detailed` | LOD — switches geometry based on camera distance |
| `BakeShadows` | Bakes shadows once, stops updating |
| `AdaptiveDpr` | Lowers device pixel ratio during performance drops |
| `AdaptiveEvents` | Reduces event frequency during performance drops |
| `PerformanceMonitor` | Monitors FPS, triggers regression callbacks |
| `Bvh` | BVH-accelerated raycasting for complex meshes |
| `meshBounds` | Fast bounding-box raycasting (replaces per-triangle) |

### PerformanceMonitor Pattern

```jsx
<PerformanceMonitor
  onIncline={() => setDpr(2)}
  onDecline={() => setDpr(1)}
  flipflops={3}
  onFallback={() => setDpr(0.5)}
/>
```

---

## Staging and Layout

| Component | Purpose | Key Props |
|-----------|---------|-----------|
| `Center` | Centers children at origin | `top`, `right`, `bottom`, `left`, `front`, `back` |
| `Float` | Floating hover animation | `speed`, `rotationIntensity`, `floatIntensity` |
| `Bounds` | Auto-fit camera to content | `fit`, `clip`, `observe`, `margin` |
| `Resize` | Normalizes children to unit size | `width`, `height`, `depth` |

---

## Abstractions and Effects

| Component | Purpose |
|-----------|---------|
| `Edges` | Renders wireframe edges |
| `Outlines` | Screen-space outlines |
| `Trail` | Motion trail behind objects |
| `Decal` | Project texture onto mesh surface |
| `Splat` | Gaussian splatting renderer |
| `Clone` | Deep clone with shared geometry/materials |
| `Image` | Texture-mapped plane with shader effects |
| `MeshPortalMaterial` | Portal — renders scene inside mesh surface |
| `GradientTexture` | Procedural gradient texture |

---

## Gizmos

| Component | Purpose |
|-----------|---------|
| `GizmoHelper` | Viewport orientation widget |
| `PivotControls` | Interactive pivot gizmo (translate/rotate/scale) |
| `TransformControls` | Three.js TransformControls wrapper |
| `Grid` | Infinite configurable grid plane |
| `Helper / useHelper` | Visualize light/camera helpers |

---

## Component Selection Guide

| Scenario | Component |
|----------|-----------|
| Product viewer | `Stage` + `OrbitControls` + `Environment` |
| Architectural walkthrough | `CameraControls` + `Environment` + `ContactShadows` |
| Scrolling experience | `ScrollControls` + `useScroll` |
| Data visualization | `Instances` + `Html` + `Billboard` |
| Text labels in 3D | `Text` (2D) or `Text3D` (extruded) + `Billboard` |
| Glass/transparent objects | `MeshTransmissionMaterial` + `Environment` |
| Reflective floors | `MeshReflectorMaterial` |
| Large identical meshes | `Instances` (>100) or `Merged` (mixed geometries) |
| Model loading | `useGLTF` + `Suspense` + `.preload()` |
| HUD / overlay | `Hud` or `Html` with `fullscreen` |

---

## Reference Links

- [references/methods.md](references/methods.md) -- Key component props and hook signatures
- [references/examples.md](references/examples.md) -- Complete working examples
- [references/anti-patterns.md](references/anti-patterns.md) -- Common mistakes and fixes

### Official Sources

- https://drei.docs.pmnd.rs/
- https://github.com/pmndrs/drei
- https://r3f.docs.pmnd.rs/
