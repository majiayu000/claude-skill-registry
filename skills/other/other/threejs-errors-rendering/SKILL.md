---
name: threejs-errors-rendering
description: >
  Use when a Three.js scene renders incorrectly: black screen, invisible
  objects, wrong colors, z-fighting, or broken shadows. Prevents the
  common mistake of wrong color space, missing material.side, or
  forgetting updateProjectionMatrix. Covers all common rendering errors
  with diagnosis steps and fix patterns.
  Keywords: black screen, invisible, wrong color, z-fighting, shadow
  artifact, rendering error, debug, nothing visible, dark, broken.
license: MIT
compatibility: "Designed for Claude Code. Requires Three.js r160+."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# threejs-errors-rendering

## Debugging Workflow Checklist

When a Three.js scene does not render correctly, ALWAYS follow this sequence:

1. Open the browser console -- check for WebGL errors or Three.js warnings
2. Verify the renderer has a non-zero size (`renderer.getSize(new THREE.Vector2())`)
3. Confirm the canvas is in the DOM and visible (not `display: none`)
4. Check that `renderer.render(scene, camera)` is called (in a loop or at least once)
5. Verify the camera is looking at the scene (position, target, near/far)
6. Confirm at least one light exists for lit materials
7. Check material `side`, `visible`, `opacity`, and `transparent` properties
8. Verify object `visible`, `layers`, and `frustumCulled` properties
9. Inspect color space settings on renderer and textures

---

## Symptom 1: Black Screen (Nothing Visible)

### Cause A: Renderer has zero size

The canvas has 0x0 dimensions. This happens when `setSize()` is called before the container is in the DOM or when the container has no CSS dimensions.

**Fix:**
```javascript
// ALWAYS ensure the container is in the DOM and has dimensions before setSize
document.body.appendChild(renderer.domElement);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
```

### Cause B: Camera is inside the object or facing away

The camera is at `(0, 0, 0)` and the object is also at `(0, 0, 0)`, so the camera is inside the mesh. Or the camera is pointing in the wrong direction.

**Fix:**
```javascript
camera.position.set(0, 2, 5); // ALWAYS move camera away from origin
camera.lookAt(0, 0, 0);
```

### Cause C: Near/far clipping planes exclude the object

Objects closer than `near` or farther than `far` are clipped. Default PerspectiveCamera near is `0.1`, far is `2000`.

**Fix:**
```javascript
const camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
// NEVER set near to 0 -- causes z-fighting and depth buffer issues
// ALWAYS keep far/near ratio below 100000 for stable depth precision
```

### Cause D: No light in the scene

`MeshStandardMaterial`, `MeshPhongMaterial`, and `MeshLambertMaterial` require lights. Without light, they render black. `MeshBasicMaterial` does NOT require lights.

**Fix:**
```javascript
scene.add(new THREE.AmbientLight(0xffffff, 0.5));
scene.add(new THREE.DirectionalLight(0xffffff, 1));
```

### Cause E: render() is never called

The animation loop is not started, or `renderer.render(scene, camera)` is missing.

**Fix:**
```javascript
function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
animate(); // ALWAYS call the function to start the loop
```

### Cause F: Scene or camera is wrong reference

Passing an empty scene or an uninitialized camera to `render()`.

**Diagnosis:** Log `scene.children.length` and `camera.type` before the render call.

---

## Symptom 2: Invisible Objects

### Cause A: Wrong material side

Back faces are culled by default (`FrontSide`). If the camera sees the back of a plane or thin geometry, it is invisible.

**Fix:**
```javascript
const material = new THREE.MeshStandardMaterial({
  side: THREE.DoubleSide // ALWAYS use for planes, leaves, thin objects
});
```

### Cause B: opacity without transparent

Setting `opacity: 0.5` without `transparent: true` has NO effect.

**Fix:**
```javascript
const material = new THREE.MeshStandardMaterial({
  opacity: 0.5,
  transparent: true // ALWAYS pair with opacity < 1
});
```

### Cause C: Object on a different layer

The camera and the object MUST share at least one layer. By default both are on layer 0. If the object is moved to another layer, the camera must enable that layer too.

**Fix:**
```javascript
object.layers.set(1);
camera.layers.enable(1); // camera must see layer 1
```

### Cause D: visible is false (inherited)

`visible = false` on a parent makes ALL descendants invisible. Check the full parent chain.

**Diagnosis:**
```javascript
let node = object;
while (node) {
  if (!node.visible) console.log('Hidden ancestor:', node.name || node.type);
  node = node.parent;
}
```

### Cause E: frustumCulled incorrectly

If the bounding sphere is wrong (e.g., after manual vertex changes without `computeBoundingSphere()`), the object may be culled even when visible.

**Fix:**
```javascript
geometry.computeBoundingSphere(); // ALWAYS call after modifying positions
// Or disable frustum culling for objects that must always render:
mesh.frustumCulled = false;
```

### Cause F: Object at wrong position or scale 0

Object is at a position far from the camera, or `scale.set(0, 0, 0)`.

**Diagnosis:** Log `object.position`, `object.scale`, `object.matrixWorld`.

---

## Symptom 3: Wrong Colors

### Cause A: Color space mismatch

This is the MOST COMMON color error in Three.js r160+.

**Rules:**
- Color/diffuse/emissive textures: ALWAYS set `texture.colorSpace = THREE.SRGBColorSpace`
- Data textures (normal, roughness, metalness, AO, displacement): ALWAYS leave as `THREE.LinearSRGBColorSpace`
- Renderer output: `renderer.outputColorSpace = THREE.SRGBColorSpace` (default in r160+)

**Symptoms of wrong color space:**
- Washed-out colors: data texture incorrectly set to `SRGBColorSpace` (double gamma)
- Over-saturated colors: color texture left in `LinearSRGBColorSpace` (no gamma applied)

**Fix:**
```javascript
const texture = await loader.loadAsync('diffuse.png');
texture.colorSpace = THREE.SRGBColorSpace; // for color textures

const normalMap = await loader.loadAsync('normal.png');
// NEVER set SRGBColorSpace on normal maps -- corrupts surface data
```

### Cause B: Tone mapping not configured

Without tone mapping, HDR values are clamped, producing flat or incorrect colors.

**Fix:**
```javascript
renderer.toneMapping = THREE.ACESFilmicToneMapping; // or AgXToneMapping
renderer.toneMappingExposure = 1.0;
```

### Cause C: Material color set after construction ignored

`material.color.set()` works, but `material.color = new THREE.Color()` after construction also works. The common mistake is setting color as a hex number directly: `material.color = 0xff0000` does NOT work.

**Fix:**
```javascript
material.color.set(0xff0000);      // Correct
material.color = new THREE.Color(0xff0000); // Correct
// material.color = 0xff0000;      // WRONG -- silently fails
```

---

## Symptom 4: Z-Fighting (Flickering Surfaces)

Z-fighting occurs when two surfaces overlap at nearly the same depth, causing the depth buffer to alternate between them.

### Fix A: Polygon offset

```javascript
const material = new THREE.MeshStandardMaterial({
  polygonOffset: true,
  polygonOffsetFactor: -1,
  polygonOffsetUnits: -1
});
```

### Fix B: Logarithmic depth buffer

```javascript
const renderer = new THREE.WebGLRenderer({ logarithmicDepthBuffer: true });
// Trades performance for better depth precision across large near/far ranges
// NEVER use with EffectComposer post-processing -- causes artifacts
```

### Fix C: Position offset

Move one surface slightly:
```javascript
decalMesh.position.z += 0.01; // small offset to prevent overlap
```

### Fix D: Reduce near/far ratio

```javascript
// ALWAYS keep the near plane as large as possible
camera.near = 1;    // not 0.001
camera.far = 1000;  // not 1000000
camera.updateProjectionMatrix();
```

---

## Symptom 5: Shadow Artifacts

For complete shadow configuration, see the `threejs-impl-shadows` skill. Common quick fixes:

- **No shadows at all:** `renderer.shadowMap.enabled = true`, `light.castShadow = true`, `mesh.castShadow = true`, `ground.receiveShadow = true`
- **Shadow acne (stripes):** Increase `light.shadow.bias` (e.g., `-0.005`)
- **Peter panning (shadow detached):** `light.shadow.bias` is too large, reduce it
- **Low-res shadows:** Increase `light.shadow.mapSize.set(2048, 2048)`

---

## Symptom 6: WebGL Context Lost

The browser reclaims the WebGL context under memory pressure or GPU reset.

### Recovery pattern

```javascript
renderer.domElement.addEventListener('webglcontextlost', (event) => {
  event.preventDefault(); // ALWAYS prevent default to allow restoration
  cancelAnimationFrame(animationId);
}, false);

renderer.domElement.addEventListener('webglcontextrestored', () => {
  // Re-initialize materials, textures, render targets
  initScene();
  animate();
}, false);
```

**NEVER** ignore context loss -- the canvas goes black permanently. ALWAYS add both event listeners.

---

## Symptom 7: needsUpdate Missing

### BufferAttribute

After modifying vertex data, the GPU buffer is stale:
```javascript
positions.array[0] = newX;
positions.needsUpdate = true; // ALWAYS set after modifying attribute data
```

### Material

After changing structural properties (adding/removing maps, changing `defines`):
```javascript
material.map = newTexture;
material.needsUpdate = true; // triggers shader recompilation
// NEVER set needsUpdate = true every frame -- causes constant recompilation
```

### Texture

After modifying texture image data:
```javascript
texture.image = newImage;
texture.needsUpdate = true; // triggers GPU re-upload
```

### InstancedMesh

After `setMatrixAt()` or `setColorAt()`:
```javascript
mesh.instanceMatrix.needsUpdate = true; // ALWAYS after setMatrixAt
mesh.instanceColor.needsUpdate = true;  // ALWAYS after setColorAt
```

---

## Symptom 8: updateProjectionMatrix Required

ALWAYS call `camera.updateProjectionMatrix()` after changing:

- `camera.fov`
- `camera.aspect`
- `camera.near`
- `camera.far`
- `camera.zoom`
- `camera.left/right/top/bottom` (OrthographicCamera)

```javascript
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix(); // NEVER forget this
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

---

## Symptom 9: Transparent Object Rendering Issues

Transparent objects render in the wrong order (back-to-front sorting fails).

### Fix A: renderOrder

```javascript
// Force specific rendering order
backgroundMesh.renderOrder = 0;
transparentMesh.renderOrder = 1;
frontMesh.renderOrder = 2;
```

### Fix B: depthWrite

```javascript
const material = new THREE.MeshStandardMaterial({
  transparent: true,
  opacity: 0.5,
  depthWrite: false // prevents transparent objects from writing to depth buffer
});
```

### Fix C: alphaTest instead of transparency

For textures with hard alpha edges (foliage, fences):
```javascript
const material = new THREE.MeshStandardMaterial({
  map: leafTexture,
  alphaTest: 0.5, // discards fragments below threshold
  side: THREE.DoubleSide
  // NEVER set transparent: true for hard-edge alpha -- use alphaTest instead
});
```

---

## Common Console Warnings

| Warning | Cause | Fix |
|---------|-------|-----|
| `THREE.WebGLRenderer: Texture is not power of two` | NPOT texture with repeat wrapping | Use power-of-two textures or `ClampToEdgeWrapping` |
| `THREE.WebGLProgram: shader error` | GLSL compilation failure | Check custom shader code for syntax errors |
| `THREE.PropertyBinding: Can not bind to...` | Animation targets missing property | Ensure skeleton/morph targets match the animation clip |
| `THREE.BufferGeometry: .addAttribute() removed` | Using deprecated API | Use `setAttribute()` instead |
| `GL_INVALID_OPERATION: Feedback loop` | Reading from a texture that is also a render target | Use separate textures for reading and writing |

---

## Reference Links

- [references/methods.md](references/methods.md) -- Fix-related API signatures
- [references/examples.md](references/examples.md) -- Complete fix patterns
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do

### Official Sources

- https://threejs.org/docs/#api/en/renderers/WebGLRenderer
- https://threejs.org/docs/#api/en/cameras/PerspectiveCamera
- https://threejs.org/docs/#api/en/materials/Material
- https://threejs.org/docs/#api/en/core/Object3D
- https://threejs.org/docs/#api/en/core/BufferAttribute
