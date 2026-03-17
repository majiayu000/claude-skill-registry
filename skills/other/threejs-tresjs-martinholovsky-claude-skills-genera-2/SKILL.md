---
name: threejs-tresjs
description: 3D HUD rendering with Three.js and TresJS for JARVIS AI Assistant
model: sonnet
risk_level: MEDIUM
version: 1.0.0
---

# Three.js / TresJS Development Skill

> **File Organization**: This skill uses split structure. See `references/` for advanced patterns and security examples.

## 1. Overview

This skill provides expertise for building 3D HUD interfaces using Three.js and TresJS (Vue 3 integration). It focuses on creating performant, visually stunning holographic displays for the JARVIS AI Assistant.

**Risk Level**: MEDIUM - GPU resource consumption, potential ReDoS in color parsing, WebGL security considerations

**Primary Use Cases**:
- Rendering 3D holographic HUD panels
- Animated status indicators and gauges
- Particle effects for system visualization
- Real-time metric displays with 3D elements

## 2. Core Responsibilities

### 2.1 Fundamental Principles

1. **TDD First**: Write tests before implementation - verify 3D components render correctly
2. **Performance Aware**: Optimize for 60fps with instancing, LOD, and efficient render loops
3. **Resource Management**: Always dispose of geometries, materials, and textures to prevent memory leaks
4. **Vue Reactivity Integration**: Use TresJS for seamless Vue 3 composition API integration
5. **Safe Color Parsing**: Validate color inputs to prevent ReDoS attacks
6. **GPU Protection**: Implement safeguards against GPU resource exhaustion
7. **Accessibility**: Provide fallbacks for devices without WebGL support

## 3. Technology Stack & Versions

### 3.1 Recommended Versions

| Package | Version | Security Notes |
|---------|---------|----------------|
| three | ^0.160.0+ | Latest stable, fixes CVE-2020-28496 ReDoS |
| @tresjs/core | ^4.0.0 | Vue 3 integration |
| @tresjs/cientos | ^3.0.0 | Component library |
| postprocessing | ^6.0.0 | Effects library |

### 3.2 Security-Critical Updates

```json
{
  "dependencies": {
    "three": "^0.160.0",
    "@tresjs/core": "^4.0.0",
    "@tresjs/cientos": "^3.0.0"
  }
}
```

**Note**: Versions before 0.137.0 have XSS vulnerabilities, before 0.125.0 have ReDoS vulnerabilities.

## 4. Implementation Patterns

### 4.1 Basic HUD Scene Setup

```vue
<script setup lang="ts">
import { TresCanvas } from '@tresjs/core'
import { OrbitControls } from '@tresjs/cientos'

const gl = {
  clearColor: '#000011',
  alpha: true,
  antialias: true,
  powerPreference: 'high-performance'
}
</script>

<template>
  <TresCanvas v-bind="gl">
    <TresPerspectiveCamera :position="[0, 0, 5]" />
    <OrbitControls :enable-damping="true" />

    <HUDPanels />
    <MetricsDisplay />
    <ParticleEffects />
  </TresCanvas>
</template>
```

### 4.2 Secure Color Handling

```typescript
// utils/safeColor.ts
import { Color } from 'three'

// ✅ Safe color parsing with validation
export function safeParseColor(input: string): Color {
  // Validate format to prevent ReDoS
  const hexPattern = /^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/
  const rgbPattern = /^rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)$/

  if (!hexPattern.test(input) && !rgbPattern.test(input)) {
    console.warn('Invalid color format, using default')
    return new Color(0x00ff00)  // Default JARVIS green
  }

  return new Color(input)
}

// ❌ DANGEROUS - User input directly to Color
// const color = new Color(userInput)  // Potential ReDoS

// ✅ SECURE - Validated input
const color = safeParseColor(userInput)
```

### 4.3 Memory-Safe Component

```vue
<script setup lang="ts">
import { onUnmounted, shallowRef } from 'vue'
import { Mesh, BoxGeometry, MeshStandardMaterial } from 'three'

// ✅ Use shallowRef for Three.js objects
const meshRef = shallowRef<Mesh | null>(null)

// ✅ Cleanup on unmount
onUnmounted(() => {
  if (meshRef.value) {
    meshRef.value.geometry.dispose()
    if (Array.isArray(meshRef.value.material)) {
      meshRef.value.material.forEach(m => m.dispose())
    } else {
      meshRef.value.material.dispose()
    }
  }
})
</script>

<template>
  <TresMesh ref="meshRef">
    <TresBoxGeometry :args="[1, 1, 1]" />
    <TresMeshStandardMaterial color="#00ff41" />
  </TresMesh>
</template>
```

### 4.4 Performance-Optimized Instancing

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { InstancedMesh, Object3D, Matrix4 } from 'three'

const instanceCount = 1000
const instancedMeshRef = ref<InstancedMesh | null>(null)

onMounted(() => {
  if (!instancedMeshRef.value) return

  const dummy = new Object3D()
  const matrix = new Matrix4()

  // ✅ Batch updates for performance
  for (let i = 0; i < instanceCount; i++) {
    dummy.position.set(
      Math.random() * 10 - 5,
      Math.random() * 10 - 5,
      Math.random() * 10 - 5
    )
    dummy.updateMatrix()
    instancedMeshRef.value.setMatrixAt(i, dummy.matrix)
  }

  instancedMeshRef.value.instanceMatrix.needsUpdate = true
})
</script>

<template>
  <TresInstancedMesh ref="instancedMeshRef" :args="[null, null, instanceCount]">
    <TresSphereGeometry :args="[0.05, 8, 8]" />
    <TresMeshBasicMaterial color="#00ff41" />
  </TresInstancedMesh>
</template>
```

### 4.5 HUD Panel with Text

```vue
<script setup lang="ts">
import { Text } from '@tresjs/cientos'

const props = defineProps<{
  title: string
  value: number
}>()

// ✅ Sanitize text content
const safeTitle = computed(() =>
  props.title.replace(/[<>]/g, '').slice(0, 50)
)
</script>

<template>
  <TresGroup>
    <!-- Panel background -->
    <TresMesh>
      <TresPlaneGeometry :args="[2, 1]" />
      <TresMeshBasicMaterial
        color="#001122"
        :transparent="true"
        :opacity="0.8"
      />
    </TresMesh>

    <!-- Title text -->
    <Text
      :text="safeTitle"
      :font-size="0.15"
      color="#00ff41"
      :position="[-0.8, 0.3, 0.01]"
    />

    <!-- Value display -->
    <Text
      :text="String(props.value)"
      :font-size="0.3"
      color="#ffffff"
      :position="[0, -0.1, 0.01]"
    />
  </TresGroup>
</template>
```

## 5. Implementation Workflow (TDD)

### 5.1 TDD Process for 3D Components

**Step 1: Write Failing Test First**

```typescript
// tests/components/hud-panel.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { mount, VueWrapper } from '@vue/test-utils'
import { Scene, WebGLRenderer } from 'three'
import HUDPanel from '~/components/hud/HUDPanel.vue'

describe('HUDPanel', () => {
  let wrapper: VueWrapper

  beforeEach(() => {
    // Mock WebGL context for testing
    const canvas = document.createElement('canvas')
    const gl = canvas.getContext('webgl2')
    vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(gl)
  })

  afterEach(() => {
    wrapper?.unmount()
    vi.restoreAllMocks()
  })

  it('renders panel with correct dimensions', () => {
    wrapper = mount(HUDPanel, {
      props: { width: 2, height: 1, title: 'Status' }
    })

    // Test fails until component is implemented
    expect(wrapper.exists()).toBe(true)
  })

  it('disposes resources on unmount', async () => {
    wrapper = mount(HUDPanel, {
      props: { width: 2, height: 1, title: 'Status' }
    })

    const disposeSpy = vi.fn()
    wrapper.vm.meshRef.geometry.dispose = disposeSpy

    wrapper.unmount()
    expect(disposeSpy).toHaveBeenCalled()
  })
})
```

**Step 2: Implement Minimum to Pass**

```vue
<script setup lang="ts">
import { shallowRef, onUnmounted } from 'vue'
import { Mesh } from 'three'

const props = defineProps<{
  width: number
  height: number
  title: string
}>()

const meshRef = shallowRef<Mesh | null>(null)

onUnmounted(() => {
  if (meshRef.value) {
    meshRef.value.geometry.dispose()
    ;(meshRef.value.material as any).dispose()
  }
})
</script>

<template>
  <TresMesh ref="meshRef">
    <TresPlaneGeometry :args="[props.width, props.height]" />
    <TresMeshBasicMaterial color="#001122" :transparent="true" :opacity="0.8" />
  </TresMesh>
</template>
```

**Step 3: Refactor Following Patterns**

```typescript
// After tests pass, add performance optimizations
// - Use instancing for multiple panels
// - Add LOD for distant panels
// - Implement texture atlases for text
```

**Step 4: Run Full Verification**

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Type check
npm run typecheck

# Performance benchmark
npm run test:perf
```

### 5.2 Testing 3D Animations

```typescript
import { describe, it, expect, vi } from 'vitest'
import { useRenderLoop } from '@tresjs/core'

describe('Animation Loop', () => {
  it('maintains 60fps during animation', async () => {
    const frameTimes: number[] = []
    let lastTime = performance.now()

    const { onLoop } = useRenderLoop()

    onLoop(() => {
      const now = performance.now()
      frameTimes.push(now - lastTime)
      lastTime = now
    })

    // Simulate 60 frames
    await new Promise(resolve => setTimeout(resolve, 1000))

    const avgFrameTime = frameTimes.reduce((a, b) => a + b, 0) / frameTimes.length
    expect(avgFrameTime).toBeLessThan(16.67) // 60fps = 16.67ms per frame
  })

  it('cleans up animation loop on unmount', () => {
    const cleanup = vi.fn()
    const { pause } = useRenderLoop()

    // Component unmounts
    pause()

    expect(cleanup).not.toThrow()
  })
})
```

### 5.3 Testing Resource Disposal

```typescript
describe('Resource Management', () => {
  it('disposes all GPU resources', () => {
    const geometry = new BoxGeometry(1, 1, 1)
    const material = new MeshStandardMaterial({ color: 0x00ff41 })
    const mesh = new Mesh(geometry, material)

    const geoDispose = vi.spyOn(geometry, 'dispose')
    const matDispose = vi.spyOn(material, 'dispose')

    // Cleanup function
    mesh.geometry.dispose()
    mesh.material.dispose()

    expect(geoDispose).toHaveBeenCalled()
    expect(matDispose).toHaveBeenCalled()
  })

  it('handles material arrays correctly', () => {
    const materials = [
      new MeshBasicMaterial(),
      new MeshStandardMaterial()
    ]
    const mesh = new Mesh(new BoxGeometry(), materials)

    const spies = materials.map(m => vi.spyOn(m, 'dispose'))

    materials.forEach(m => m.dispose())

    spies.forEach(spy => expect(spy).toHaveBeenCalled())
  })
})
```

## 6. Performance Patterns

### 6.1 Geometry Instancing

```typescript
// Good: Use InstancedMesh for repeated objects
import { InstancedMesh, Matrix4, Object3D } from 'three'

const COUNT = 1000
const mesh = new InstancedMesh(geometry, material, COUNT)
const dummy = new Object3D()

for (let i = 0; i < COUNT; i++) {
  dummy.position.set(Math.random() * 10, Math.random() * 10, Math.random() * 10)
  dummy.updateMatrix()
  mesh.setMatrixAt(i, dummy.matrix)
}
mesh.instanceMatrix.needsUpdate = true

// Bad: Creating individual meshes
for (let i = 0; i < COUNT; i++) {
  const mesh = new Mesh(geometry.clone(), material.clone()) // Memory waste!
  scene.add(mesh)
}
```

### 6.2 Texture Atlases

```typescript
// Good: Single texture atlas for multiple sprites
const atlas = new TextureLoader().load('/textures/hud-atlas.png')
const materials = {
  panel: new SpriteMaterial({ map: atlas }),
  icon: new SpriteMaterial({ map: atlas })
}

// Set UV offsets for different sprites
materials.panel.map.offset.set(0, 0.5)
materials.panel.map.repeat.set(0.5, 0.5)

// Bad: Loading separate textures
const panelTex = new TextureLoader().load('/textures/panel.png')
const iconTex = new TextureLoader().load('/textures/icon.png')
// Multiple draw calls, more GPU memory
```

### 6.3 Level of Detail (LOD)

```typescript
// Good: Use LOD for complex objects
import { LOD } from 'three'

const lod = new LOD()

// High detail - close up
const highDetail = new Mesh(
  new SphereGeometry(1, 32, 32),
  material
)
lod.addLevel(highDetail, 0)

// Medium detail - mid range
const medDetail = new Mesh(
  new SphereGeometry(1, 16, 16),
  material
)
lod.addLevel(medDetail, 10)

// Low detail - far away
const lowDetail = new Mesh(
  new SphereGeometry(1, 8, 8),
  material
)
lod.addLevel(lowDetail, 20)

scene.add(lod)

// Bad: Always rendering high detail
const sphere = new Mesh(new SphereGeometry(1, 64, 64), material)
```

### 6.4 Frustum Culling

```typescript
// Good: Enable frustum culling (default, but verify)
mesh.frustumCulled = true

// For custom bounds optimization
mesh.geometry.computeBoundingSphere()
mesh.geometry.computeBoundingBox()

// Manual visibility check for complex scenes
const frustum = new Frustum()
const matrix = new Matrix4().multiplyMatrices(
  camera.projectionMatrix,
  camera.matrixWorldInverse
)
frustum.setFromProjectionMatrix(matrix)

objects.forEach(obj => {
  obj.visible = frustum.intersectsObject(obj)
})

// Bad: Disabling culling or rendering everything
mesh.frustumCulled = false // Renders even when off-screen
```

### 6.5 Object Pooling

```typescript
// Good: Pool and reuse objects
class ParticlePool {
  private pool: Mesh[] = []
  private active: Set<Mesh> = new Set()

  constructor(private geometry: BufferGeometry, private material: Material) {
    // Pre-allocate pool
    for (let i = 0; i < 100; i++) {
      const mesh = new Mesh(geometry, material)
      mesh.visible = false
      this.pool.push(mesh)
    }
  }

  acquire(): Mesh | null {
    const mesh = this.pool.find(m => !this.active.has(m))
    if (mesh) {
      mesh.visible = true
      this.active.add(mesh)
      return mesh
    }
    return null
  }

  release(mesh: Mesh): void {
    mesh.visible = false
    this.active.delete(mesh)
  }
}

// Bad: Creating/destroying objects each frame
function spawnParticle() {
  const mesh = new Mesh(geometry, material) // GC pressure!
  scene.add(mesh)
  setTimeout(() => {
    scene.remove(mesh)
    mesh.geometry.dispose()
  }, 1000)
}
```

### 6.6 RAF Optimization

```typescript
// Good: Efficient render loop
let lastTime = 0
const targetFPS = 60
const frameInterval = 1000 / targetFPS

function animate(currentTime: number) {
  requestAnimationFrame(animate)

  const delta = currentTime - lastTime

  // Skip frame if too soon (for battery saving)
  if (delta < frameInterval) return

  lastTime = currentTime - (delta % frameInterval)

  // Update only what changed
  if (needsUpdate) {
    updateScene()
    renderer.render(scene, camera)
  }
}

// Bad: Rendering every frame unconditionally
function animate() {
  requestAnimationFrame(animate)

  // Always updates everything
  updateAllObjects()
  renderer.render(scene, camera) // Even if nothing changed
}
```

### 6.7 Shader Optimization

```typescript
// Good: Simple, optimized shaders
const material = new ShaderMaterial({
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    varying vec2 vUv;
    uniform vec3 color;
    void main() {
      gl_FragColor = vec4(color, 1.0);
    }
  `,
  uniforms: {
    color: { value: new Color(0x00ff41) }
  }
})

// Bad: Complex calculations in fragment shader
// Avoid: loops, conditionals, texture lookups when possible
```

## 7. Security Standards

### 7.1 Known Vulnerabilities

| CVE | Severity | Description | Mitigation |
|-----|----------|-------------|------------|
| CVE-2020-28496 | HIGH | ReDoS in color parsing | Update to 0.125.0+, validate colors |
| CVE-2022-0177 | MEDIUM | XSS in docs | Update to 0.137.0+ |

### 7.2 OWASP Top 10 Coverage

| OWASP Category | Risk | Mitigation |
|----------------|------|------------|
| A05 Injection | MEDIUM | Validate all color/text inputs |
| A06 Vulnerable Components | HIGH | Keep Three.js updated |

### 7.3 GPU Resource Protection

```typescript
// composables/useResourceLimit.ts
export function useResourceLimit() {
  const MAX_TRIANGLES = 1_000_000
  const MAX_DRAW_CALLS = 100

  let triangleCount = 0

  function checkGeometry(geometry: BufferGeometry): boolean {
    const triangles = geometry.index
      ? geometry.index.count / 3
      : geometry.attributes.position.count / 3

    if (triangleCount + triangles > MAX_TRIANGLES) {
      console.error('Triangle limit exceeded')
      return false
    }

    triangleCount += triangles
    return true
  }

  return { checkGeometry }
}
```

## 6. Testing & Quality

### 6.1 Component Testing

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

describe('HUD Panel', () => {
  it('sanitizes malicious title input', () => {
    const wrapper = mount(HUDPanel, {
      props: {
        title: '<script>alert("xss")</script>Status',
        value: 75
      }
    })

    expect(wrapper.vm.safeTitle).not.toContain('<script>')
  })
})
```

### 6.2 Performance Testing

```typescript
describe('Instanced Mesh', () => {
  it('handles 1000 instances without frame drop', async () => {
    const scene = new Scene()
    // Setup instanced mesh...

    const startTime = performance.now()
    renderer.render(scene, camera)
    const renderTime = performance.now() - startTime

    expect(renderTime).toBeLessThan(16.67)  // 60fps target
  })
})
```

## 8. Common Mistakes & Anti-Patterns

### 8.1 Critical Security Anti-Patterns

#### Never: Parse User Colors Directly

```typescript
// ❌ DANGEROUS - ReDoS vulnerability
const color = new Color(userInput)

// ✅ SECURE - Validated input
const color = safeParseColor(userInput)
```

#### Never: Skip Resource Disposal

```typescript
// ❌ MEMORY LEAK
const mesh = new Mesh(geometry, material)
scene.remove(mesh)
// Geometry and material still in GPU memory!

// ✅ PROPER CLEANUP
scene.remove(mesh)
mesh.geometry.dispose()
mesh.material.dispose()
```

### 8.2 Performance Anti-Patterns

#### Avoid: Creating Objects in Render Loop

```typescript
// ❌ BAD - Creates garbage every frame
function animate() {
  mesh.position.add(new Vector3(0, 0.01, 0))  // New object every frame!
}

// ✅ GOOD - Reuse objects
const velocity = new Vector3(0, 0.01, 0)
function animate() {
  mesh.position.add(velocity)
}
```

## 13. Pre-Deployment Checklist

### Security Verification

- [ ] Three.js version >= 0.137.0 (XSS fix)
- [ ] All color inputs validated before parsing
- [ ] No user input directly to `new Color()`
- [ ] Resource limits enforced

### Performance Verification

- [ ] All geometries/materials disposed on unmount
- [ ] Instancing used for repeated objects
- [ ] No object creation in render loop
- [ ] LOD implemented for complex scenes

## 14. Summary

Three.js/TresJS provides 3D rendering for the JARVIS HUD:

1. **Security**: Validate all inputs, especially colors to prevent ReDoS
2. **Memory**: Always dispose resources on component unmount
3. **Performance**: Use instancing, avoid allocations in render loop
4. **Integration**: TresJS provides seamless Vue 3 reactivity

**Remember**: WebGL has direct GPU access - always validate inputs and manage resources carefully.

---

**References**:
- `references/advanced-patterns.md` - Complex 3D patterns
- `references/security-examples.md` - WebGL security practices
