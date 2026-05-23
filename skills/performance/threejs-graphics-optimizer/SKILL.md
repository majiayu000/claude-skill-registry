---
name: threejs-graphics-optimizer
description: Performance optimization rules for THREE.js and graphics programming. Covers mobile-first optimization, fallback patterns, memory management, render loop efficiency, and general graphics best practices for smooth 60fps experiences across devices.
---

# THREE.js Graphics Optimizer

**Version**: 1.0  
**Focus**: Performance optimization for THREE.js and graphics applications  
**Purpose**: Build smooth 60fps graphics experiences across all devices including mobile

---

## Philosophy: Performance-First Graphics

### The 16ms Budget

**Target**: 60 FPS = 16.67ms per frame

**Frame budget breakdown**:
- JavaScript logic: ~5-8ms
- Rendering (GPU): ~8-10ms
- Browser overhead: ~2ms

**If you exceed 16ms**: Frames drop, stuttering occurs.

### Mobile vs Desktop Reality

**Desktop**: Powerful GPU, lots of VRAM, high pixel ratios  
**Mobile**: Constrained GPU, limited VRAM, battery concerns, thermal throttling

**Design philosophy**: Optimize for mobile, scale up for desktop (not vice versa).

---

## Part 1: Core Optimization Principles

### 1. Minimize Draw Calls

**The Problem**: Each object = one draw call. 1000 objects = 1000 calls = slow.

**Solution: Geometry Merging**

```javascript
// ❌ Bad: 100 draw calls for 100 cubes
for (let i = 0; i < 100; i++) {
  const geometry = new THREE.BoxGeometry(1, 1, 1)
  const material = new THREE.MeshBasicMaterial({ color: 0xff0000 })
  const cube = new THREE.Mesh(geometry, material)
  cube.position.set(i * 2, 0, 0)
  scene.add(cube)
}

// ✅ Good: 1 draw call via InstancedMesh
const geometry = new THREE.BoxGeometry(1, 1, 1)
const material = new THREE.MeshBasicMaterial({ color: 0xff0000 })
const instancedMesh = new THREE.InstancedMesh(geometry, material, 100)

for (let i = 0; i < 100; i++) {
  const matrix = new THREE.Matrix4()
  matrix.setPosition(i * 2, 0, 0)
  instancedMesh.setMatrixAt(i, matrix)
}

instancedMesh.instanceMatrix.needsUpdate = true
scene.add(instancedMesh)
```

**When to use**:
- Many similar objects (particles, trees, enemies)
- Static or semi-static positioning
- Shared material/geometry

### 2. Level of Detail (LOD)

Render simpler geometry when objects are far away:

```javascript
const lod = new THREE.LOD()

// High detail (near camera)
const highDetailGeo = new THREE.IcosahedronGeometry(1, 3) // Many faces
const highDetailMesh = new THREE.Mesh(
  highDetailGeo,
  new THREE.MeshStandardMaterial({ color: 0x00d9ff })
)
lod.addLevel(highDetailMesh, 0) // Distance 0-10

// Medium detail
const medDetailGeo = new THREE.IcosahedronGeometry(1, 1)
const medDetailMesh = new THREE.Mesh(
  medDetailGeo,
  new THREE.MeshBasicMaterial({ color: 0x00d9ff })
)
lod.addLevel(medDetailMesh, 10) // Distance 10-50

// Low detail (far from camera)
const lowDetailGeo = new THREE.IcosahedronGeometry(1, 0)
const lowDetailMesh = new THREE.Mesh(
  lowDetailGeo,
  new THREE.MeshBasicMaterial({ color: 0x00d9ff })
)
lod.addLevel(lowDetailMesh, 50) // Distance 50+

scene.add(lod)

// Update LOD in render loop
function animate() {
  lod.update(camera)
  renderer.render(scene, camera)
}
```

### 3. Frustum Culling (Automatic)

THREE.js automatically skips objects outside camera view. Help it:

```javascript
// ❌ Bad: Unnecessarily large bounding volumes
mesh.geometry.computeBoundingSphere()
mesh.geometry.boundingSphere.radius = 1000 // Too large!

// ✅ Good: Accurate bounding volumes
mesh.geometry.computeBoundingSphere() // Uses actual geometry size
mesh.geometry.computeBoundingBox()
```

### 4. Texture Optimization

**Texture size matters**:
- 4K texture (4096x4096): 64MB VRAM (uncompressed)
- 2K texture (2048x2048): 16MB VRAM
- 1K texture (1024x1024): 4MB VRAM

**Rules**:
- Use smallest textures that look good
- Power-of-two dimensions (512, 1024, 2048)
- Compress textures (use basis/KTX2 format)

```javascript
const textureLoader = new THREE.TextureLoader()

// ❌ Bad: Loading 4K texture for small object
const texture = textureLoader.load('texture-4k.jpg')

// ✅ Good: Appropriate size for use case
const texture = textureLoader.load('texture-1k.jpg')

// ✅ Better: Set appropriate filtering
texture.minFilter = THREE.LinearFilter // No mipmaps (saves VRAM)
texture.anisotropy = renderer.capabilities.getMaxAnisotropy()

// ✅ Best: Dispose when done
function cleanup() {
  texture.dispose()
}
```

---

## Part 2: Mobile-Specific Optimization

### Mobile Detection & Adaptation

```javascript
/**
 * Detect mobile device.
 * @returns {boolean}
 */
export function isMobile() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile/i.test(navigator.userAgent)
    || window.innerWidth < 768
}

/**
 * Get optimal pixel ratio for device.
 * @returns {number}
 */
export function getOptimalPixelRatio() {
  const mobile = isMobile()
  const deviceRatio = window.devicePixelRatio
  
  // Cap pixel ratio on mobile to save performance
  return mobile 
    ? Math.min(deviceRatio, 1.5)  // Max 1.5x on mobile
    : Math.min(deviceRatio, 2)    // Max 2x on desktop
}

// Apply to renderer
renderer.setPixelRatio(getOptimalPixelRatio())
```

### Mobile Performance Settings

```javascript
/**
 * Configure renderer for mobile performance.
 */
function setupMobileOptimizations(renderer, scene, camera) {
  const mobile = isMobile()
  
  if (mobile) {
    // Disable expensive features
    renderer.shadowMap.enabled = false
    renderer.antialias = false
    
    // Lower pixel ratio
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5))
    
    // Simpler tone mapping
    renderer.toneMapping = THREE.NoToneMapping
    
    // Remove fog (expensive pixel shader)
    scene.fog = null
    
    // Reduce lights (expensive)
    // Keep only 1-2 lights max on mobile
    
    console.log('[Mobile] Performance optimizations applied')
  } else {
    // Desktop: enable high-quality features
    renderer.shadowMap.enabled = true
    renderer.shadowMap.type = THREE.PCFSoftShadowMap
    renderer.antialias = true
    renderer.toneMapping = THREE.ACESFilmicToneMapping
    
    console.log('[Desktop] High-quality features enabled')
  }
}
```

### Fallback Pattern

```javascript
/**
 * Create geometry with fallback for low-end devices.
 */
export function createOptimizedGeometry(options = {}) {
  const { size = 1, mobile = false } = options
  
  if (mobile) {
    // Simple geometry for mobile
    return new THREE.SphereGeometry(size, 8, 8) // Low poly
  } else {
    // Detailed geometry for desktop
    return new THREE.IcosahedronGeometry(size, 2) // High poly
  }
}

// Usage
const mobile = isMobile()
const geometry = createOptimizedGeometry({ size: 1, mobile })
const material = new THREE.MeshBasicMaterial({ color: 0x00d9ff })
const mesh = new THREE.Mesh(geometry, material)
```

---

## Part 3: Render Loop Optimization

### Efficient Animation Loop

```javascript
class SceneManager {
  constructor() {
    this.clock = new THREE.Clock()
    this.animationId = null
    this.lastFrameTime = 0
    this.fps = 60
    this.frameInterval = 1000 / this.fps
  }
  
  /**
   * Main render loop with delta time.
   */
  animate() {
    this.animationId = requestAnimationFrame(() => this.animate())
    
    const now = performance.now()
    const delta = now - this.lastFrameTime
    
    // Throttle to target FPS if needed
    if (delta < this.frameInterval) return
    
    this.lastFrameTime = now - (delta % this.frameInterval)
    
    // Update logic with delta
    const deltaSeconds = this.clock.getDelta()
    this.update(deltaSeconds)
    
    // Render
    this.renderer.render(this.scene, this.camera)
  }
  
  /**
   * Update scene objects.
   * @param {number} delta - Time since last frame (seconds)
   */
  update(delta) {
    // Update animations, physics, etc.
    this.animatedObjects.forEach(obj => {
      if (obj.update) obj.update(delta)
    })
  }
  
  /**
   * Cleanup and stop animation.
   */
  dispose() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId)
    }
  }
}
```

### Conditional Rendering

```javascript
/**
 * Only render when something changed (for static scenes).
 */
class ConditionalRenderer {
  constructor(renderer, scene, camera) {
    this.renderer = renderer
    this.scene = scene
    this.camera = camera
    this.needsRender = true
  }
  
  /**
   * Mark scene as needing re-render.
   */
  invalidate() {
    this.needsRender = true
  }
  
  /**
   * Render only if needed.
   */
  render() {
    if (this.needsRender) {
      this.renderer.render(this.scene, this.camera)
      this.needsRender = false
    }
  }
  
  /**
   * Use with controls.
   */
  connectControls(controls) {
    controls.addEventListener('change', () => this.invalidate())
  }
}

// Usage
const conditionalRenderer = new ConditionalRenderer(renderer, scene, camera)
conditionalRenderer.connectControls(controls)

function animate() {
  requestAnimationFrame(animate)
  controls.update()
  conditionalRenderer.render() // Only renders if camera moved
}
```

---

## Part 4: Memory Management

### Dispose Pattern

```javascript
/**
 * Properly dispose THREE.js resources.
 */
export function disposeObject(object) {
  if (!object) return
  
  // Traverse and dispose children
  object.traverse((child) => {
    // Dispose geometry
    if (child.geometry) {
      child.geometry.dispose()
    }
    
    // Dispose materials
    if (child.material) {
      if (Array.isArray(child.material)) {
        child.material.forEach(material => disposeMaterial(material))
      } else {
        disposeMaterial(child.material)
      }
    }
    
    // Dispose textures
    if (child.texture) {
      child.texture.dispose()
    }
  })
  
  // Remove from parent
  if (object.parent) {
    object.parent.remove(object)
  }
}

/**
 * Dispose material and its textures.
 */
function disposeMaterial(material) {
  material.dispose()
  
  // Dispose textures
  Object.keys(material).forEach(key => {
    const value = material[key]
    if (value && typeof value === 'object' && 'minFilter' in value) {
      value.dispose() // It's a texture
    }
  })
}
```

### Memory Leak Prevention

```javascript
class SafeSceneManager {
  constructor() {
    this.scene = new THREE.Scene()
    this.renderer = new THREE.WebGLRenderer()
    this.objects = new Set()
  }
  
  /**
   * Add object and track it.
   */
  add(object) {
    this.scene.add(object)
    this.objects.add(object)
  }
  
  /**
   * Remove and dispose object.
   */
  remove(object) {
    this.scene.remove(object)
    this.objects.delete(object)
    disposeObject(object)
  }
  
  /**
   * Cleanup all resources.
   */
  dispose() {
    // Dispose all tracked objects
    this.objects.forEach(obj => disposeObject(obj))
    this.objects.clear()
    
    // Dispose renderer
    this.renderer.dispose()
    
    // Clear scene
    this.scene.clear()
  }
}
```

---

## Part 5: Material Optimization

### Material Sharing

```javascript
// ❌ Bad: New material for each object
for (let i = 0; i < 100; i++) {
  const material = new THREE.MeshBasicMaterial({ color: 0xff0000 })
  const mesh = new THREE.Mesh(geometry, material)
  scene.add(mesh)
}

// ✅ Good: Share single material
const sharedMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 })

for (let i = 0; i < 100; i++) {
  const mesh = new THREE.Mesh(geometry, sharedMaterial)
  scene.add(mesh)
}
```

### Cheaper Material Types

Performance ranking (fastest to slowest):

1. **MeshBasicMaterial** - No lighting, flat shading
2. **MeshLambertMaterial** - Simple diffuse lighting
3. **MeshPhongMaterial** - Specular highlights
4. **MeshStandardMaterial** - PBR (expensive)
5. **MeshPhysicalMaterial** - Advanced PBR (very expensive)

```javascript
// Mobile: Use cheaper materials
const material = isMobile()
  ? new THREE.MeshBasicMaterial({ color: 0x00d9ff })
  : new THREE.MeshStandardMaterial({ 
      color: 0x00d9ff,
      roughness: 0.5,
      metalness: 0.1
    })
```

### Blending Modes

```javascript
// Additive blending for glows (cheaper than transparent)
material.blending = THREE.AdditiveBlending
material.transparent = true
material.depthWrite = false // Don't write to depth buffer
```

---

## Part 6: Post-Processing Optimization

### Selective Post-Processing

```javascript
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js'
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js'
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js'

function setupPostProcessing(renderer, scene, camera, mobile) {
  const composer = new EffectComposer(renderer)
  
  // Always add render pass
  composer.addPass(new RenderPass(scene, camera))
  
  // Bloom only on desktop
  if (!mobile) {
    const bloomPass = new UnrealBloomPass(
      new THREE.Vector2(window.innerWidth, window.innerHeight),
      1.5,  // strength
      0.4,  // radius
      0.85  // threshold
    )
    composer.addPass(bloomPass)
  }
  
  return composer
}
```

---

## Part 7: General Graphics Best Practices

### 1. Object Pooling

```javascript
/**
 * Object pool to reuse objects instead of creating/destroying.
 */
class ObjectPool {
  constructor(createFn, resetFn) {
    this.pool = []
    this.createFn = createFn
    this.resetFn = resetFn
  }
  
  /**
   * Get object from pool or create new one.
   */
  acquire() {
    if (this.pool.length > 0) {
      return this.pool.pop()
    }
    return this.createFn()
  }
  
  /**
   * Return object to pool.
   */
  release(obj) {
    this.resetFn(obj)
    this.pool.push(obj)
  }
}

// Usage: Particle pool
const particlePool = new ObjectPool(
  // Create function
  () => {
    const geometry = new THREE.SphereGeometry(0.1)
    const material = new THREE.MeshBasicMaterial({ color: 0xffffff })
    return new THREE.Mesh(geometry, material)
  },
  // Reset function
  (particle) => {
    particle.position.set(0, 0, 0)
    particle.visible = false
  }
)

// Spawn particle
const particle = particlePool.acquire()
particle.position.set(Math.random(), Math.random(), Math.random())
particle.visible = true
scene.add(particle)

// Later: Return to pool
scene.remove(particle)
particlePool.release(particle)
```

### 2. Visibility Culling

```javascript
/**
 * Hide objects far from camera.
 */
function updateVisibility(camera, objects, maxDistance = 50) {
  const cameraPos = camera.position
  
  objects.forEach(obj => {
    const distance = obj.position.distanceTo(cameraPos)
    obj.visible = distance < maxDistance
  })
}
```

### 3. Lazy Loading

```javascript
/**
 * Load textures on demand.
 */
class LazyTextureLoader {
  constructor() {
    this.loader = new THREE.TextureLoader()
    this.cache = new Map()
  }
  
  async load(url) {
    // Check cache
    if (this.cache.has(url)) {
      return this.cache.get(url)
    }
    
    // Load texture
    return new Promise((resolve, reject) => {
      this.loader.load(
        url,
        (texture) => {
          this.cache.set(url, texture)
          resolve(texture)
        },
        undefined,
        reject
      )
    })
  }
}
```

---

## Part 8: Performance Monitoring

### FPS Counter

```javascript
/**
 * Simple FPS monitor.
 */
class FPSMonitor {
  constructor() {
    this.frames = 0
    this.lastTime = performance.now()
    this.fps = 60
  }
  
  update() {
    this.frames++
    const now = performance.now()
    
    if (now >= this.lastTime + 1000) {
      this.fps = Math.round((this.frames * 1000) / (now - this.lastTime))
      this.frames = 0
      this.lastTime = now
      
      // Warn if FPS drops
      if (this.fps < 30) {
        console.warn(`Low FPS: ${this.fps}`)
      }
    }
  }
  
  getFPS() {
    return this.fps
  }
}

// Usage
const fpsMonitor = new FPSMonitor()

function animate() {
  requestAnimationFrame(animate)
  fpsMonitor.update()
  renderer.render(scene, camera)
}
```

### GPU Memory Monitoring

```javascript
/**
 * Monitor GPU memory usage.
 */
function logMemoryUsage(renderer) {
  const info = renderer.info
  
  console.log('GPU Memory:', {
    geometries: info.memory.geometries,
    textures: info.memory.textures,
    programs: info.programs.length,
    drawCalls: info.render.calls,
    triangles: info.render.triangles
  })
}

// Call periodically
setInterval(() => logMemoryUsage(renderer), 5000)
```

---

## Critical Optimization Checklist

### Before Optimizing
- [ ] Profile first (Chrome DevTools Performance tab)
- [ ] Identify bottleneck (CPU or GPU?)
- [ ] Set target FPS (usually 60fps = 16ms/frame)

### Geometry
- [ ] Use InstancedMesh for repeated objects
- [ ] Implement LOD for distant objects
- [ ] Merge static geometries
- [ ] Use BufferGeometry (not Geometry)
- [ ] Dispose unused geometries

### Textures
- [ ] Use smallest texture size needed
- [ ] Power-of-two dimensions
- [ ] Compress textures (basis/KTX2)
- [ ] Set minFilter = LinearFilter if no mipmaps
- [ ] Dispose unused textures

### Materials
- [ ] Share materials across objects
- [ ] Use cheaper material types on mobile
- [ ] Limit transparent objects
- [ ] Use additive blending for glows
- [ ] Dispose unused materials

### Lighting
- [ ] Limit lights (1-2 on mobile, 3-5 on desktop)
- [ ] Disable shadows on mobile
- [ ] Use baked lighting where possible
- [ ] Prefer directional/point over spot lights

### Rendering
- [ ] Cap pixel ratio (1.5x mobile, 2x desktop)
- [ ] Disable antialiasing on mobile
- [ ] Use conditional rendering for static scenes
- [ ] Implement frustum culling
- [ ] Limit post-processing on mobile

### Mobile-Specific
- [ ] Detect mobile devices
- [ ] Reduce geometry complexity
- [ ] Disable expensive features
- [ ] Lower pixel ratio
- [ ] Test on real devices (not just desktop browser)

---

## Common Performance Killers

1. **Too many draw calls** → Use InstancedMesh
2. **High-resolution textures** → Resize to 1K or 2K
3. **Too many lights** → Limit to 2-3
4. **Transparent objects** → Use sparingly, render last
5. **Post-processing on mobile** → Disable or simplify
6. **Memory leaks** → Always dispose geometries/materials/textures
7. **Unnecessary re-renders** → Use conditional rendering
8. **High pixel ratio on mobile** → Cap at 1.5x

---

## Performance Testing Workflow

### 1. Test on Target Devices

```javascript
// Detect and log device info
console.log('Device Info:', {
  userAgent: navigator.userAgent,
  pixelRatio: window.devicePixelRatio,
  screen: `${window.screen.width}x${window.screen.height}`,
  gpu: renderer.capabilities.getMaxAnisotropy()
})
```

### 2. Profile with Chrome DevTools

1. Open DevTools → Performance tab
2. Record 5-10 seconds of rendering
3. Look for:
   - Long frames (>16ms)
   - GPU bottlenecks
   - Memory leaks

### 3. A/B Test Optimizations

```javascript
// Feature flag for testing
const ENABLE_SHADOWS = !isMobile()
const ENABLE_BLOOM = !isMobile()
const MAX_PARTICLE_COUNT = isMobile() ? 100 : 500
```

---

## Resources

- **THREE.js Docs**: https://threejs.org/docs/
- **THREE.js Performance Tips**: https://discoverthreejs.com/tips-and-tricks/
- **WebGL Fundamentals**: https://webglfundamentals.org/
- **GPU Performance**: https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices
