---
name: r3f-drei
description: @react-three/drei helper library—OrbitControls, Text, Environment, useTexture, useGLTF, Html, Billboard, and 50+ abstractions that simplify common R3F patterns. Use when implementing camera controls, loading assets, rendering text, or needing common 3D utilities.
---

# R3F Drei

Drei ("three" in German) provides production-ready abstractions for common R3F patterns—controls, loaders, helpers, and effects.

## Quick Start

```tsx
import { OrbitControls, Environment, Text, useGLTF } from '@react-three/drei';

function Scene() {
  const { scene } = useGLTF('/model.glb');
  
  return (
    <>
      <OrbitControls />
      <Environment preset="city" />
      <Text position={[0, 2, 0]} fontSize={0.5}>Hello World</Text>
      <primitive object={scene} />
    </>
  );
}
```

## Controls

### OrbitControls

```tsx
import { OrbitControls } from '@react-three/drei';

<OrbitControls
  // Rotation
  enableRotate={true}
  rotateSpeed={1}
  minPolarAngle={0}           // Vertical min (0 = top)
  maxPolarAngle={Math.PI}     // Vertical max (π = bottom)
  minAzimuthAngle={-Infinity} // Horizontal min
  maxAzimuthAngle={Infinity}  // Horizontal max
  
  // Zoom
  enableZoom={true}
  zoomSpeed={1}
  minDistance={1}             // Min zoom distance
  maxDistance={100}           // Max zoom distance
  
  // Pan
  enablePan={true}
  panSpeed={1}
  screenSpacePanning={true}
  
  // Damping
  enableDamping={true}
  dampingFactor={0.05}
  
  // Target
  target={[0, 0, 0]}
  
  // Events
  onChange={(e) => console.log('changed')}
  onStart={(e) => console.log('interaction start')}
  onEnd={(e) => console.log('interaction end')}
/>
```

### Other Controls

```tsx
// First-person controls
import { PointerLockControls } from '@react-three/drei';
<PointerLockControls />

// Fly controls
import { FlyControls } from '@react-three/drei';
<FlyControls movementSpeed={10} rollSpeed={0.5} />

// Trackball controls
import { TrackballControls } from '@react-three/drei';
<TrackballControls />

// Map controls (constrained orbit)
import { MapControls } from '@react-three/drei';
<MapControls />

// Transform controls (gizmo)
import { TransformControls } from '@react-three/drei';
<TransformControls object={meshRef} mode="translate" />
```

## Loading

### useGLTF (3D Models)

```tsx
import { useGLTF } from '@react-three/drei';

function Model() {
  const { scene, nodes, materials, animations } = useGLTF('/model.glb');
  
  return <primitive object={scene} />;
}

// Preload
useGLTF.preload('/model.glb');

// With Draco compression
const { scene } = useGLTF('/model.glb', '/draco/');
```

### useTexture

```tsx
import { useTexture } from '@react-three/drei';

function TexturedMesh() {
  // Single texture
  const colorMap = useTexture('/texture.jpg');
  
  // Multiple textures
  const [color, normal, roughness] = useTexture([
    '/color.jpg',
    '/normal.jpg', 
    '/roughness.jpg'
  ]);
  
  // Object syntax
  const textures = useTexture({
    map: '/color.jpg',
    normalMap: '/normal.jpg',
    roughnessMap: '/roughness.jpg'
  });
  
  return (
    <mesh>
      <boxGeometry />
      <meshStandardMaterial {...textures} />
    </mesh>
  );
}
```

### useCubeTexture (Environment Maps)

```tsx
import { useCubeTexture } from '@react-three/drei';

function EnvMappedMesh() {
  const envMap = useCubeTexture(
    ['px.jpg', 'nx.jpg', 'py.jpg', 'ny.jpg', 'pz.jpg', 'nz.jpg'],
    { path: '/cubemaps/sky/' }
  );
  
  return (
    <mesh>
      <sphereGeometry />
      <meshStandardMaterial envMap={envMap} metalness={1} roughness={0} />
    </mesh>
  );
}
```

## Environment & Lighting

### Environment

```tsx
import { Environment } from '@react-three/drei';

// Preset environments
<Environment preset="sunset" />  // city, sunset, dawn, night, warehouse, forest, apartment, studio, park, lobby

// Custom HDR
<Environment files="/env.hdr" />

// As background
<Environment background preset="sunset" />

// With blur
<Environment preset="city" blur={0.5} />

// Ground projection
<Environment preset="sunset" ground={{ height: 15, radius: 60 }} />
```

### Lightformer

```tsx
import { Environment, Lightformer } from '@react-three/drei';

<Environment>
  <Lightformer
    position={[0, 5, -5]}
    scale={[10, 1, 1]}
    intensity={2}
    color="white"
  />
  <Lightformer
    position={[5, 0, 0]}
    rotation={[0, Math.PI / 2, 0]}
    scale={[5, 5, 1]}
    intensity={1}
    color="orange"
  />
</Environment>
```

### Sky & Stars

```tsx
import { Sky, Stars } from '@react-three/drei';

<Sky
  distance={450000}
  sunPosition={[0, 1, 0]}
  inclination={0.5}
  azimuth={0.25}
/>

<Stars
  radius={100}
  depth={50}
  count={5000}
  factor={4}
  saturation={0}
  fade
  speed={1}
/>
```

## Text

### Text (Troika)

```tsx
import { Text } from '@react-three/drei';

<Text
  position={[0, 0, 0]}
  fontSize={1}
  color="white"
  font="/fonts/roboto.woff"
  anchorX="center"  // left, center, right
  anchorY="middle"  // top, top-baseline, middle, bottom-baseline, bottom
  maxWidth={10}
  lineHeight={1}
  letterSpacing={0}
  textAlign="center"
  outlineWidth={0.05}
  outlineColor="black"
>
  Hello World
</Text>
```

### Text3D (Extruded)

```tsx
import { Text3D, Center } from '@react-three/drei';

<Center>
  <Text3D
    font="/fonts/helvetiker_regular.typeface.json"
    size={0.75}
    height={0.2}
    curveSegments={12}
    bevelEnabled
    bevelThickness={0.02}
    bevelSize={0.02}
    bevelOffset={0}
    bevelSegments={5}
  >
    Hello
    <meshStandardMaterial color="hotpink" />
  </Text3D>
</Center>
```

## HTML Integration

### Html Component

```tsx
import { Html } from '@react-three/drei';

<mesh position={[0, 1, 0]}>
  <boxGeometry />
  <meshStandardMaterial />
  
  <Html
    position={[0, 1, 0]}
    center                    // Center on position
    distanceFactor={10}       // Scale with distance
    occlude                   // Hide when occluded
    transform                 // Use CSS3D transform
    sprite                    // Always face camera
    className="annotation"
    style={{ color: 'white' }}
  >
    <div className="label">Click me!</div>
  </Html>
</mesh>
```

### Billboard

```tsx
import { Billboard, Text } from '@react-three/drei';

// Always faces camera
<Billboard
  follow={true}      // Follow camera rotation
  lockX={false}      // Lock X rotation
  lockY={false}      // Lock Y rotation
  lockZ={false}      // Lock Z rotation
>
  <Text fontSize={0.5}>I face the camera</Text>
</Billboard>
```

## Helpers

### Bounds (Auto-fit Camera)

```tsx
import { Bounds, useBounds } from '@react-three/drei';

function FitContent() {
  const bounds = useBounds();
  
  useEffect(() => {
    bounds.refresh().fit();
  }, []);
  
  return <Model />;
}

<Canvas>
  <Bounds fit clip observe margin={1.2}>
    <FitContent />
  </Bounds>
</Canvas>
```

### Center

```tsx
import { Center } from '@react-three/drei';

<Center>
  <mesh>
    <boxGeometry args={[1, 2, 3]} />
    <meshStandardMaterial />
  </mesh>
</Center>
```

### Float

```tsx
import { Float } from '@react-three/drei';

<Float
  speed={1}           // Animation speed
  rotationIntensity={1}  // Rotation intensity
  floatIntensity={1}     // Float intensity
  floatingRange={[-0.1, 0.1]}  // Y-axis range
>
  <mesh>
    <boxGeometry />
    <meshStandardMaterial />
  </mesh>
</Float>
```

### Clone

```tsx
import { Clone, useGLTF } from '@react-three/drei';

function ClonedModels() {
  const { scene } = useGLTF('/model.glb');
  
  return (
    <>
      <Clone object={scene} position={[-2, 0, 0]} />
      <Clone object={scene} position={[0, 0, 0]} />
      <Clone object={scene} position={[2, 0, 0]} />
    </>
  );
}
```

## Shapes

### Premade Shapes

```tsx
import { 
  Box, Sphere, Plane, Cylinder, Cone, Torus, 
  TorusKnot, Ring, Circle, Icosahedron 
} from '@react-three/drei';

<Box args={[1, 1, 1]} position={[0, 0, 0]}>
  <meshStandardMaterial color="hotpink" />
</Box>

<Sphere args={[1, 32, 32]} position={[2, 0, 0]}>
  <meshStandardMaterial color="royalblue" />
</Sphere>
```

### RoundedBox

```tsx
import { RoundedBox } from '@react-three/drei';

<RoundedBox args={[1, 1, 1]} radius={0.1} smoothness={4}>
  <meshStandardMaterial color="orange" />
</RoundedBox>
```

### Line

```tsx
import { Line } from '@react-three/drei';

<Line
  points={[[0, 0, 0], [1, 1, 1], [2, 0, 0]]}
  color="red"
  lineWidth={2}
  dashed={false}
/>
```

## Staging

### ContactShadows

```tsx
import { ContactShadows } from '@react-three/drei';

<ContactShadows
  position={[0, -0.5, 0]}
  opacity={0.5}
  scale={10}
  blur={2}
  far={4}
  resolution={256}
  color="#000000"
/>
```

### Reflector (Mirrors/Floors)

```tsx
import { Reflector } from '@react-three/drei';

<Reflector
  position={[0, -0.5, 0]}
  rotation={[-Math.PI / 2, 0, 0]}
  args={[10, 10]}
  resolution={512}
  mirror={0.5}
  mixBlur={1}
  mixStrength={1}
  blur={[400, 100]}
  minDepthThreshold={0.9}
  maxDepthThreshold={1}
  depthScale={1}
>
  {(Material, props) => <Material {...props} color="white" />}
</Reflector>
```

### Backdrop

```tsx
import { Backdrop } from '@react-three/drei';

<Backdrop
  floor={0.25}
  segments={20}
  receiveShadow
>
  <meshStandardMaterial color="#353540" />
</Backdrop>
```

## Cameras

### PerspectiveCamera

```tsx
import { PerspectiveCamera } from '@react-three/drei';

<PerspectiveCamera
  makeDefault
  position={[0, 5, 10]}
  fov={75}
  near={0.1}
  far={1000}
/>
```

### OrthographicCamera

```tsx
import { OrthographicCamera } from '@react-three/drei';

<OrthographicCamera
  makeDefault
  zoom={50}
  position={[0, 0, 100]}
/>
```

### CameraShake

```tsx
import { CameraShake } from '@react-three/drei';

<CameraShake
  maxYaw={0.01}
  maxPitch={0.01}
  maxRoll={0.01}
  yawFrequency={0.5}
  pitchFrequency={0.5}
  rollFrequency={0.5}
  intensity={1}
/>
```

## Performance Helpers

### Detailed (LOD)

```tsx
import { Detailed } from '@react-three/drei';

<Detailed distances={[0, 15, 30]}>
  <HighDetailMesh />
  <MediumDetailMesh />
  <LowDetailMesh />
</Detailed>
```

### Instances

```tsx
import { Instances, Instance } from '@react-three/drei';

<Instances limit={1000}>
  <boxGeometry />
  <meshStandardMaterial />
  
  {positions.map((pos, i) => (
    <Instance key={i} position={pos} color="red" />
  ))}
</Instances>
```

### Preload

```tsx
import { Preload } from '@react-three/drei';

<Canvas>
  <Suspense fallback={null}>
    <Scene />
    <Preload all />  {/* Preload all assets in scene */}
  </Suspense>
</Canvas>
```

## Dependencies

```json
{
  "dependencies": {
    "@react-three/drei": "^9.92.0",
    "@react-three/fiber": "^8.15.0",
    "three": "^0.160.0"
  }
}
```

## File Structure

```
r3f-drei/
├── SKILL.md
├── references/
│   ├── controls-reference.md   # All control types
│   ├── loaders-reference.md    # All loader hooks
│   ├── helpers-reference.md    # All helper components
│   └── staging-reference.md    # Environment, shadows, etc.
└── scripts/
    └── presets/
        ├── studio-setup.tsx    # Professional studio lighting
        ├── outdoor-setup.tsx   # Outdoor scene setup
        └── product-setup.tsx   # Product visualization
```

## Reference

- `references/controls-reference.md` — All control types and options
- `references/loaders-reference.md` — useGLTF, useTexture, etc.
- `references/helpers-reference.md` — Center, Bounds, Float, etc.
- `references/staging-reference.md` — Environment, shadows, reflections
