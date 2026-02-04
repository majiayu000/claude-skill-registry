---
name: threejs-geometry
description: Three.js geometry creation - built-in shapes, BufferGeometry, custom geometry, instancing. Use when creating 3D shapes, working with vertices, building custom meshes, or optimizing with instanced rendering.
---

# Three.js Geometry

## Built-in Geometries

```javascript
// Basic shapes
new THREE.BoxGeometry(1, 1, 1);
new THREE.SphereGeometry(1, 32, 32);
new THREE.PlaneGeometry(10, 10);
new THREE.CylinderGeometry(1, 1, 2, 32);
new THREE.ConeGeometry(1, 2, 32);
new THREE.TorusGeometry(1, 0.4, 16, 100);

// Advanced
new THREE.IcosahedronGeometry(1, 0);
new THREE.CapsuleGeometry(0.5, 1, 4, 8);
```

## Custom BufferGeometry

```javascript
const geometry = new THREE.BufferGeometry();

// Vertices
const vertices = new Float32Array([
  -1, -1, 0,  1, -1, 0,  1, 1, 0,  -1, 1, 0
]);
geometry.setAttribute("position", new THREE.BufferAttribute(vertices, 3));

// Indices
const indices = new Uint16Array([0, 1, 2, 0, 2, 3]);
geometry.setIndex(new THREE.BufferAttribute(indices, 1));

// Normals and UVs
geometry.setAttribute("normal", new THREE.BufferAttribute(normals, 3));
geometry.setAttribute("uv", new THREE.BufferAttribute(uvs, 2));

geometry.computeVertexNormals();
```

## InstancedMesh

```javascript
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const count = 1000;
const instancedMesh = new THREE.InstancedMesh(geometry, material, count);

const dummy = new THREE.Object3D();
for (let i = 0; i < count; i++) {
  dummy.position.set(Math.random() * 20 - 10, Math.random() * 20 - 10, Math.random() * 20 - 10);
  dummy.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);
  dummy.updateMatrix();
  instancedMesh.setMatrixAt(i, dummy.matrix);
}
instancedMesh.instanceMatrix.needsUpdate = true;
```

## Points and Lines

```javascript
// Points
const points = new THREE.Points(geometry, new THREE.PointsMaterial({ size: 0.1 }));

// Lines
const line = new THREE.Line(geometry, new THREE.LineBasicMaterial({ color: 0xff0000 }));
```

## Performance Tips
1. Use indexed geometry
2. Merge static meshes with `BufferGeometryUtils.mergeGeometries`
3. Use InstancedMesh for many identical objects
4. Call `geometry.dispose()` when done
