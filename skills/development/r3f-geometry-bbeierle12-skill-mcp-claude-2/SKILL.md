---
name: r3f-geometry
description: BufferGeometry creation, built-in geometries, custom geometry with buffer attributes, instanced meshes for rendering thousands of objects, and geometry manipulation. Use when creating custom shapes, optimizing with instancing, or working with vertex data directly.
---

# R3F Geometry

Geometry defines the shape of 3D objects via vertices, faces, normals, and UVs stored in buffer attributes.

## Quick Start

```tsx
// Built-in geometry
<mesh>
  <boxGeometry args={[1, 1, 1]} />
  <meshStandardMaterial />
</mesh>

// Custom geometry
<mesh>
  <bufferGeometry>
    <bufferAttribute
      attach="attributes-position"
      count={3}
      array={new Float32Array([0, 0, 0, 1, 0, 0, 0.5, 1, 0])}
      itemSize={3}
    />
  </bufferGeometry>
  <meshBasicMaterial side={THREE.DoubleSide} />
</mesh>
```

## Built-in Geometries

All geometries accept `args` array matching constructor parameters:

```tsx
// Box: [width, height, depth, widthSegments?, heightSegments?, depthSegments?]
<boxGeometry args={[1, 2, 1, 1, 2, 1]} />

// Sphere: [radius, widthSegments, heightSegments, phiStart?, phiLength?, thetaStart?, thetaLength?]
<sphereGeometry args={[1, 32, 32]} />

// Plane: [width, height, widthSegments?, heightSegments?]
<planeGeometry args={[10, 10, 10, 10]} />

// Cylinder: [radiusTop, radiusBottom, height, radialSegments?, heightSegments?, openEnded?]
<cylinderGeometry args={[0.5, 0.5, 2, 32]} />

// Cone: [radius, height, radialSegments?, heightSegments?, openEnded?]
<coneGeometry args={[1, 2, 32]} />

// Torus: [radius, tube, radialSegments, tubularSegments, arc?]
<torusGeometry args={[1, 0.3, 16, 100]} />

// TorusKnot: [radius, tube, tubularSegments, radialSegments, p?, q?]
<torusKnotGeometry args={[1, 0.3, 100, 16]} />

// Ring: [innerRadius, outerRadius, thetaSegments?, phiSegments?]
<ringGeometry args={[0.5, 1, 32]} />

// Circle: [radius, segments?, thetaStart?, thetaLength?]
<circleGeometry args={[1, 32]} />

// Dodecahedron/Icosahedron/Octahedron/Tetrahedron: [radius, detail?]
<icosahedronGeometry args={[1, 0]} />
```

## Buffer Attributes

Geometry data lives in typed arrays attached as attributes:

| Attribute | ItemSize | Purpose |
|-----------|----------|---------|
| `position` | 3 | Vertex positions (x, y, z) |
| `normal` | 3 | Surface normals for lighting |
| `uv` | 2 | Texture coordinates (u, v) |
| `color` | 3 | Per-vertex colors (r, g, b) |
| `index` | 1 | Triangle indices (optional) |

### Custom Geometry from Scratch

```tsx
import { useMemo } from 'react';
import * as THREE from 'three';

function Triangle() {
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry();
    
    // 3 vertices × 3 components (x, y, z)
    const positions = new Float32Array([
      -1, -1, 0,  // vertex 0
       1, -1, 0,  // vertex 1
       0,  1, 0   // vertex 2
    ]);
    
    // 3 vertices × 3 components (nx, ny, nz)
    const normals = new Float32Array([
      0, 0, 1,
      0, 0, 1,
      0, 0, 1
    ]);
    
    // 3 vertices × 2 components (u, v)
    const uvs = new Float32Array([
      0, 0,
      1, 0,
      0.5, 1
    ]);
    
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geo.setAttribute('normal', new THREE.BufferAttribute(normals, 3));
    geo.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));
    
    return geo;
  }, []);
  
  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial side={THREE.DoubleSide} />
    </mesh>
  );
}
```

### Declarative Buffer Attributes

```tsx
function Triangle() {
  const positions = useMemo(() => 
    new Float32Array([-1, -1, 0, 1, -1, 0, 0, 1, 0]), 
  []);
  
  return (
    <mesh>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={3}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <meshBasicMaterial side={THREE.DoubleSide} />
    </mesh>
  );
}
```

### Indexed Geometry

Use indices to share vertices between triangles:

```tsx
function Quad() {
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry();
    
    // 4 unique vertices
    const positions = new Float32Array([
      -1, -1, 0,  // 0: bottom-left
       1, -1, 0,  // 1: bottom-right
       1,  1, 0,  // 2: top-right
      -1,  1, 0   // 3: top-left
    ]);
    
    // 2 triangles, 6 indices
    const indices = new Uint16Array([
      0, 1, 2,  // first triangle
      0, 2, 3   // second triangle
    ]);
    
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geo.setIndex(new THREE.BufferAttribute(indices, 1));
    geo.computeVertexNormals();
    
    return geo;
  }, []);
  
  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial side={THREE.DoubleSide} />
    </mesh>
  );
}
```

## Dynamic Geometry Updates

```tsx
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

function WavingPlane() {
  const geometryRef = useRef<THREE.BufferGeometry>(null!);
  
  useFrame(({ clock }) => {
    const positions = geometryRef.current.attributes.position;
    const time = clock.elapsedTime;
    
    for (let i = 0; i < positions.count; i++) {
      const x = positions.getX(i);
      const y = positions.getY(i);
      const z = Math.sin(x * 2 + time) * Math.cos(y * 2 + time) * 0.5;
      positions.setZ(i, z);
    }
    
    positions.needsUpdate = true;  // Critical!
    geometryRef.current.computeVertexNormals();
  });
  
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]}>
      <planeGeometry ref={geometryRef} args={[10, 10, 50, 50]} />
      <meshStandardMaterial color="royalblue" side={THREE.DoubleSide} />
    </mesh>
  );
}
```

## Instanced Mesh

Render thousands of identical meshes with different transforms in a single draw call:

```tsx
import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

function Particles({ count = 1000 }) {
  const meshRef = useRef<THREE.InstancedMesh>(null!);
  
  // Pre-allocate transformation objects
  const dummy = useMemo(() => new THREE.Object3D(), []);
  
  // Initialize instance matrices
  useEffect(() => {
    for (let i = 0; i < count; i++) {
      dummy.position.set(
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10
      );
      dummy.rotation.set(
        Math.random() * Math.PI,
        Math.random() * Math.PI,
        0
      );
      dummy.scale.setScalar(0.1 + Math.random() * 0.2);
      dummy.updateMatrix();
      meshRef.current.setMatrixAt(i, dummy.matrix);
    }
    meshRef.current.instanceMatrix.needsUpdate = true;
  }, [count, dummy]);
  
  // Animate instances
  useFrame(({ clock }) => {
    for (let i = 0; i < count; i++) {
      meshRef.current.getMatrixAt(i, dummy.matrix);
      dummy.matrix.decompose(dummy.position, dummy.quaternion, dummy.scale);
      
      dummy.rotation.x += 0.01;
      dummy.rotation.y += 0.01;
      
      dummy.updateMatrix();
      meshRef.current.setMatrixAt(i, dummy.matrix);
    }
    meshRef.current.instanceMatrix.needsUpdate = true;
  });
  
  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="hotpink" />
    </instancedMesh>
  );
}
```

### Instance Colors

```tsx
function ColoredInstances({ count = 1000 }) {
  const meshRef = useRef<THREE.InstancedMesh>(null!);
  
  useEffect(() => {
    const color = new THREE.Color();
    
    for (let i = 0; i < count; i++) {
      color.setHSL(i / count, 1, 0.5);
      meshRef.current.setColorAt(i, color);
    }
    
    meshRef.current.instanceColor!.needsUpdate = true;
  }, [count]);
  
  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[0.1, 16, 16]} />
      <meshStandardMaterial />
    </instancedMesh>
  );
}
```

### Instance Attributes (Custom Data)

```tsx
function CustomInstanceData({ count = 1000 }) {
  const meshRef = useRef<THREE.InstancedMesh>(null!);
  
  // Custom per-instance data
  const speeds = useMemo(() => {
    const arr = new Float32Array(count);
    for (let i = 0; i < count; i++) {
      arr[i] = 0.5 + Math.random();
    }
    return arr;
  }, [count]);
  
  useEffect(() => {
    // Attach as instanced buffer attribute
    meshRef.current.geometry.setAttribute(
      'aSpeed',
      new THREE.InstancedBufferAttribute(speeds, 1)
    );
  }, [speeds]);
  
  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <boxGeometry />
      <shaderMaterial
        vertexShader={`
          attribute float aSpeed;
          varying float vSpeed;
          void main() {
            vSpeed = aSpeed;
            gl_Position = projectionMatrix * modelViewMatrix * instanceMatrix * vec4(position, 1.0);
          }
        `}
        fragmentShader={`
          varying float vSpeed;
          void main() {
            gl_FragColor = vec4(vSpeed, 0.5, 1.0 - vSpeed, 1.0);
          }
        `}
      />
    </instancedMesh>
  );
}
```

## Geometry Utilities

### Compute Normals

```tsx
const geometry = useMemo(() => {
  const geo = new THREE.BufferGeometry();
  // ... set positions
  geo.computeVertexNormals();  // Auto-calculate smooth normals
  return geo;
}, []);
```

### Compute Bounding Box/Sphere

```tsx
useEffect(() => {
  geometry.computeBoundingBox();
  geometry.computeBoundingSphere();
  
  console.log(geometry.boundingBox);    // THREE.Box3
  console.log(geometry.boundingSphere); // THREE.Sphere
}, [geometry]);
```

### Center Geometry

```tsx
const geometry = useMemo(() => {
  const geo = new THREE.BoxGeometry(2, 3, 1);
  geo.center();  // Move to origin
  return geo;
}, []);
```

### Merge Geometries

```tsx
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils';

const merged = useMemo(() => {
  const box = new THREE.BoxGeometry(1, 1, 1);
  const sphere = new THREE.SphereGeometry(0.5, 16, 16);
  sphere.translate(0, 1, 0);
  
  return mergeGeometries([box, sphere]);
}, []);
```

## Performance Tips

| Technique | When to Use | Impact |
|-----------|-------------|--------|
| Instancing | 100+ identical meshes | Massive |
| Indexed geometry | Shared vertices | Moderate |
| Lower segments | Non-hero geometry | Moderate |
| Merge geometries | Static scene | Moderate |
| Dispose unused | Dynamic loading | Memory |

### Disposal

```tsx
useEffect(() => {
  return () => {
    geometry.dispose();  // Clean up GPU memory
  };
}, [geometry]);
```

## File Structure

```
r3f-geometry/
├── SKILL.md
├── references/
│   ├── buffer-attributes.md   # Deep-dive on attribute types
│   ├── instancing-patterns.md # Advanced instancing
│   └── procedural-shapes.md   # Algorithmic geometry
└── scripts/
    ├── procedural/
    │   ├── grid.ts            # Grid mesh generator
    │   ├── terrain.ts         # Heightmap terrain
    │   └── tube.ts            # Custom tube geometry
    └── utils/
        ├── geometry-utils.ts  # Merge, center, clone
        └── instancing.ts      # Instance helpers
```

## Reference

- `references/buffer-attributes.md` — All attribute types and usage
- `references/instancing-patterns.md` — Advanced instancing techniques
- `references/procedural-shapes.md` — Generating geometry algorithmically
