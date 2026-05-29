---
name: ta-assets-pipeline-optimization
description: 3D asset optimization and pipeline management for Vite 6. Use when optimizing models, compressing textures, reducing asset size.
category: asset
---

# 3D Asset Pipeline Optimization

## When to Use

- Optimizing FBX/GLB models for web deployment
- Setting up efficient texture workflows
- Managing audio asset compression
- Creating asset LOD systems
- Optimizing shader asset loading

## Quick Start

```markdown
## Asset Optimization Checklist

### Before Export
- [ ] FBX: Remove unused materials, animations, textures
- [ ] Textures: Compress to WebP/ASTC, power of 2 sizes
- [ ] Audio: Convert to OGG, 44.1kHz, < 1MB
- [ ] Models: Polygon count < 50k for main characters

### Vite Configuration
```typescript
// vite.config.ts
build: {
  assetsInlineLimit: 0, // Never inline binary assets
  rollupOptions: {
    output: {
      assetFileNames: 'assets/[name].[hash][extname]'
    }
  }
}
```

### Asset Loading
```typescript
// Optimized model loading with LOD
import { useGLTF, useFBX } from '@react-three/drei'

function OptimizedModel({ url, lod }) {
  const model = lod === 'low'
    ? useGLTF('/assets/low-poly/model.glb')
    : useFBX('/assets/high-poly/model.fbx')
  return <primitive object={model.scene} />
}
```

## Asset Optimization Strategies

### 1. Model Optimization

#### FBX Export Settings (Blender)
```markdown
**File Export Settings:**
- Format: FBX Binary
- Apply Modifiers: ✓
- Selection Only: ✗
- Include: Mesh, Materials, Armature, Animation
- Exclude: Cameras, Lights, Empty Objects

**Mesh Optimization:**
- Decimate modifier (50% polygon reduction)
- Remove duplicate vertices
- Clean mesh data
```

#### GLB Compression Tools
```markdown
**glTF Transform Pipeline:**
```bash
# Install
npm install -g @gltf-transform/cli

# Optimize GLB
gltf-transform input.glb output.glb \
  --prune \
  --texture-compress webp \
  --texture-size 2048 \
  --draco-compress
```

**Compression Settings:**
- Draco compression: ✓
- Texture compression: WebP
- Maximum texture size: 2048x2048
- Remove unused attributes
```

### 2. Texture Optimization

#### Texture Export Guidelines
```markdown
**Format Selection:**
- Albedo: WebP (lossy, 80% quality)
- Normal: ASTC (4x4) for mobile, PNG for desktop
- Roughness/Metallic: WebP (lossless)
- AO: WebP (lossy, 70% quality)

**Size Guidelines:**
- Character textures: 1024x1024
- Environment textures: 2048x2048
- UI textures: 512x512 (power of 2)

**Compression Workflow:**
```typescript
// Texture compression function
async function compressTexture(imagePath: string): Promise<Blob> {
  const image = await loadImage(imagePath)
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')

  canvas.width = 1024
  canvas.height = 1024

  ctx.drawImage(image, 0, 0)

  return new Promise((resolve) => {
    canvas.toBlob(
      (blob) => resolve(blob!),
      'webp',
      0.8 // 80% quality
    )
  })
}
```
```

### 3. Audio Optimization

#### Audio Compression Settings
```markdown
**Format Guidelines:**
- Sound effects: OGG, 44.1kHz, mono
- Music: OGG, 44.1kHz, stereo
- Voice: OGG, 44.1kHz, mono

**File Size Targets:**
- SFX: < 100KB per file
- Music: < 1MB per minute
- Voice: < 50KB per second

**Compression Tool:**
```bash
# Using oggenc
oggenc -q 5 -r 44100 input.wav -o output.ogg
```
```

## Asset Management System

### 1. Asset Organization
```
src/assets/
├── models/
│   ├── characters/
│   │   ├── high-poly/
│   │   ├── low-poly/
│   │   └── animations/
│   ├── environment/
│   │   ├── props/
│   │   └── terrain/
│   └── weapons/
├── textures/
│   ├── characters/
│   ├── environment/
│   ├── ui/
│   └── shared/
├── audio/
│   ├── sfx/
│   ├── music/
│   └── voice/
└── shaders/
    ├── materials/
    └── post-processing/
```

### 2. Asset Metadata System
```typescript
// src/assets/metadata.ts
interface AssetMetadata {
  id: string
  name: string
  type: 'model' | 'texture' | 'audio' | 'shader'
  path: string
  size: number
  optimized: boolean
  lod?: 'high' | 'medium' | 'low'
  compression?: 'draco' | 'none'
  streaming?: boolean
}

export const assetRegistry: AssetMetadata[] = [
  {
    id: 'character-main',
    name: 'Main Character',
    type: 'model',
    path: '/assets/characters/main.fbx',
    size: 2048576, // 2MB
    optimized: true,
    lod: 'high',
    compression: 'draco'
  },
  // ... more assets
]
```

### 3. Asset Loader with Caching
```typescript
class AssetLoader {
  private cache = new Map<string, any>()
  private loading = new Map<string, Promise<any>>()

  async loadModel(url: string, lod?: string): Promise<THREE.Group> {
    const cacheKey = `${url}?lod=${lod}`

    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey)
    }

    if (this.loading.has(cacheKey)) {
      return this.loading.get(cacheKey)
    }

    const loadPromise = this.internalLoadModel(url, lod)
    this.loading.set(cacheKey, loadPromise)

    try {
      const model = await loadPromise
      this.cache.set(cacheKey, model)
      return model
    } finally {
      this.loading.delete(cacheKey)
    }
  }

  private async internalLoadModel(url: string, lod?: string) {
    if (url.endsWith('.glb')) {
      const gltf = await useGLTF(url)
      return gltf.scene
    } else if (url.endsWith('.fbx')) {
      const fbx = await useFBX(url)
      return fbx.scene
    }
    throw new Error('Unsupported model format')
  }
}
```

## LOD (Level of Detail) System

### 1. Asset Preparation
```markdown
**LOD Creation Workflow:**
1. Export high-poly model (100% detail)
2. Create medium-poly (50% detail)
3. Create low-poly (25% detail)
4. Create proxy (10% detail)

**Reduction Targets:**
- Character: High=50k, Medium=25k, Low=10k, Proxy=2k
- Environment: High=100k, Medium=50k, Low=20k, Proxy=5k
```

### 2. LOD Manager
```typescript
import { useFrame, useThree } from '@react-three/fiber'
import { useRef, useState } from 'react'

function LODManager({ models }: { models: { high: string; medium: string; low: string } }) {
  const [currentLOD, setCurrentLOD] = useState<'high' | 'medium' | 'low'>('high')
  const camera = useThree((state) => state.camera)
  const [distance, setDistance] = useState(0)

  useFrame(() => {
    const dist = camera.position.distanceTo([0, 0, 0])
    setDistance(dist)

    if (dist < 10) {
      setCurrentLOD('high')
    } else if (dist < 30) {
      setCurrentLOD('medium')
    } else {
      setCurrentLOD('low')
    }
  })

  const currentModel = models[currentLOD]

  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Model url={currentModel} />
    </Suspense>
  )
}
```

## Performance Monitoring

### 1. Asset Performance Tracker
```typescript
function AssetPerformanceTracker() {
  const [stats, setStats] = useState({
    loadedAssets: 0,
    totalSize: 0,
    loadTimes: [] as number[],
    memoryUsage: 0
  })

  useEffect(() => {
    const interval = setInterval(() => {
      const assets = performance.getEntriesByType('resource')
      const modelAssets = assets.filter(a =>
        a.name.includes('.fbx') ||
        a.name.includes('.glb') ||
        a.name.includes('.png') ||
        a.name.includes('.jpg')
      )

      const totalSize = modelAssets.reduce((sum, asset) => {
        return sum + (asset as any).transferSize || 0
      }, 0)

      setStats({
        loadedAssets: modelAssets.length,
        totalSize,
        loadTimes: modelAssets.map(a => a.duration),
        memoryUsage: performance.memory?.usedJSHeapSize || 0
      })
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="asset-stats">
      <h3>Asset Performance</h3>
      <p>Loaded: {stats.loadedAssets}</p>
      <p>Total Size: {formatBytes(stats.totalSize)}</p>
      <p>Load Time: {stats.loadTimes.reduce((a, b) => a + b, 0).toFixed(2)}ms</p>
      <p>Memory: {formatBytes(stats.memoryUsage)}</p>
    </div>
  )
}
```

## Anti-Patterns

### 1. Asset Loading Issues

**❌ DON'T:**
```typescript
// Loading multiple high-poly models at once
function Scene() {
  const char = useFBX('/assets/character.fbx')
  const weapon = useFBX('/assets/weapon.fbx')
  const env = useGLTF('/assets/environment.glb')

  return (
    <>
      <primitive object={char.scene} />
      <primitive object={weapon.scene} />
      <primitive object={env.scene} />
    </>
  )
}
```

**✅ DO:**
```typescript
// Lazy load assets based on camera distance
function Scene() {
  const [characterLoaded, setCharacterLoaded] = useState(false)

  useFrame(() => {
    if (camera.position.distanceTo([0, 0, 0]) < 20 && !characterLoaded) {
      setCharacterLoaded(true)
    }
  })

  return (
    <>
      {characterLoaded ? (
        <Suspense fallback={<LoadingSpinner />}>
          <CharacterModel />
        </Suspense>
      ) : (
        <PlaceholderCharacter />
      )}
    </>
  )
}
```

### 2. Memory Management

**❌ DON'T:**
```typescript
// Not disposing of loaded assets
useEffect(() => {
  const model = useFBX('/assets/character.fbx')
  return () => {} // No cleanup
}, [])
```

**✅ DO:**
```typescript
useEffect(() => {
  let mounted = true

  const loadModel = async () => {
    const model = useFBX('/assets/character.fbx')
    return model
  }

  const model = loadModel()

  return () => {
    mounted = false
    // Dispose of geometries, materials, textures
    if (model?.scene) {
      model.scene.traverse(disposeObject)
    }
  }
}, [])

function disposeObject(object: THREE.Object3D) {
  if (object.geometry) object.geometry.dispose()
  if (object.material) {
    if (Array.isArray(object.material)) {
      object.material.forEach(mat => mat.dispose())
    } else {
      object.material.dispose()
    }
  }
}
```

### 3. Texture Memory Leaks

**❌ DON'T:**
```typescript
// Creating textures without cleanup
const texture = new THREE.TextureLoader().load('texture.png')
texture.needsUpdate = true // Updates cause memory leaks
```

**✅ DO:**
```typescript
const textureRef = useRef<THREE.Texture>()

useEffect(() => {
  textureRef.current = new THREE.TextureLoader().load('texture.png')

  return () => {
    if (textureRef.current) {
      textureRef.current.dispose()
      textureRef.current = null
    }
  }
}, [])

// Only update when necessary
if (textureRef.current && needsUpdate) {
  textureRef.current.needsUpdate = true
}
```

## Optimization Workflow

### 1. Asset Analysis
```typescript
function analyzeAssetPerformance() {
  const resources = performance.getEntriesByType('resource')

  const assetAnalysis = {
    totalAssets: resources.length,
    byType: {
      models: resources.filter(r => r.name.includes('.fbx') || r.name.includes('.glb')).length,
      textures: resources.filter(r => r.name.includes('.png') || r.name.includes('.jpg')).length,
      audio: resources.filter(r => r.name.includes('.ogg') || r.name.includes('.mp3')).length
    },
    avgLoadTime: resources.reduce((sum, r) => sum + r.duration, 0) / resources.length,
    largestAssets: resources
      .sort((a, b) => (b as any).transferSize - (a as any).transferSize)
      .slice(0, 5)
  }

  return assetAnalysis
}
```

### 2. Optimization Report
```typescript
function generateOptimizationReport() {
  const analysis = analyzeAssetPerformance()

  return {
    suggestions: [
      ...(analysis.avgLoadTime > 1000 ? ['Consider texture compression'] : []),
      ...(analysis.largestAssets[0]?.transferSize > 1000000 ? ['Optimize large assets'] : []),
      ...(analysis.byType.models > 10 ? ['Implement LOD system'] : [])
    ],
    recommendations: {
      compression: analysis.byType.textures > 5 ? true : false,
      lod: analysis.byType.models > 3 ? true : false,
      streaming: analysis.totalAssets > 20 ? true : false
    }
  }
}
```

## Related Skills

For asset creation workflow: `Skill("ta-assets-workflow")`
For Vite 6 specific handling: `Skill("ta-assets-workflow-vite-6")`

## External References

- [glTF Transform Documentation](https://gltf-transform.donmccurdy.com/)
- [Blender FBX Export Guidelines](https://docs.blender.org/manual/en/latest/files/importexport/fbx.html)
- [WebP Compression Guide](https://developers.google.com/speed/webp/docs/cwebp)
- [Three.js Memory Management](https://threejs.org/docs/#manual/en/introduction/How-to-dispose-of-objects)