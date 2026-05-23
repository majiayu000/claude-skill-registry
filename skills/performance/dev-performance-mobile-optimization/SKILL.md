---
name: dev-performance-mobile-optimization
description: Mobile-specific optimization for R3F/Three.js. Use when targeting mobile devices.
category: performance
---

# Mobile Optimization

Optimize R3F/Three.js for mobile devices with limited GPU/CPU.

## When to Use

Use when:
- Targeting mobile devices
- FPS drops on mobile
- Memory issues on phones

## Mobile vs Desktop Targets

| Feature         | Desktop | Mobile  |
| --------------- | ------- | ------- |
| Pixel Ratio     | 2.0     | 1.0-1.5 |
| Shadows         | On      | Off     |
| Anti-aliasing   | MSAA    | Off     |
| Post-processing | Full    | Minimal |
| Draw calls      | < 200   | < 50    |
| Polygons        | < 1M    | < 100K  |

## Mobile Detection

```tsx
const config = useMemo(() => {
  const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent);
  return {
    dpr: isMobile ? 1 : Math.min(window.devicePixelRatio, 2),
    shadows: !isMobile,
    antialias: !isMobile,
    maxDrawCalls: isMobile ? 50 : 200,
  };
}, []);
```

## Canvas Configuration

```tsx
<Canvas
  dpr={config.dpr}
  shadows={config.shadows}
  gl={{
    antialias: config.antialias,
    powerPreference: 'high-performance',
  }}
  performance={{
    min: 0.5,
    max: 1,
    debounce: 200,
  }}
>
  <Scene />
</Canvas>
```

## Texture Optimization

```tsx
// Compress textures for mobile
const textureLoader = new THREE.TextureLoader();

// Use WebP or JPEG (not PNG)
textureLoader.load('/textures/ground.webp');

// Resize textures to power-of-2
const MAX_TEXTURE_SIZE = isMobile ? 512 : 2048;

// Use texture compression
const gl = (canvas.getContext('webgl') || canvas.getContext('experimental-webgl'));
if (gl) {
  gl.getExtension('WEBGL_compressed_texture_s3tc');
  gl.getExtension('WEBGL_compressed_texture_astc');
}
```

## Geometry Optimization

```tsx
// Low-poly models for mobile
const MOBILE_SETTINGS = {
  treePolygons: 500,      // Desktop: 5000
  rockPolygons: 200,      // Desktop: 2000
  characterPolygons: 2000, // Desktop: 15000
};

// Simplified shapes
<mesh>
  {/* Mobile: 8 segments, Desktop: 32 */}
  <sphereGeometry args={[1, isMobile ? 8 : 32, isMobile ? 6 : 32]} />
  <meshStandardMaterial />
</mesh>
```

## Lighting Optimization

```tsx
// Mobile: minimize lights
<ambientLight intensity={isMobile ? 0.3 : 0.5} />
{isMobile ? (
  // Single directional light
  <directionalLight position={[10, 10, 5]} intensity={0.8} />
) : (
  // Desktop: full lighting
  <>
    <directionalLight position={[10, 10, 5]} intensity={1} castShadow />
    <pointLight position={[-10, 5, -5]} intensity={0.5} />
    <hemisphereLight args={['#ffffff', '#444444', 0.6]} />
  </>
)}
```

## Material Optimization

```tsx
// Mobile: simpler materials
<meshStandardMaterial
  // Disable expensive features on mobile
  roughness={isMobile ? 0.8 : 0.5}
  metalness={0}
  // Use single color instead of textures when possible
  color={isMobile ? '#8B4513' : undefined}
  map={isMobile ? undefined : woodTexture}
/>
```

## Post-Processing

```tsx
import { EffectComposer, RenderPass } from '@react-three/postprocessing';

function PostProcessing({ isMobile }) {
  if (isMobile) {
    // Mobile: minimal or no post-processing
    return null;
  }

  return (
    <EffectComposer>
      <RenderPass />
      {/* Add effects for desktop only */}
      <Bloom luminanceThreshold={0.5} intensity={0.5} />
    </EffectComposer>
  );
}
```

## Frustum Culling

```tsx
// Enable frustum culling (default: true)
<mesh frustumCulled={true}>
  <complexGeometry />
  <meshStandardMaterial />
</mesh>

// For large objects, manually set bounding sphere
<mesh
  frustumCulled={false}  // Disable auto-culling
  onPointerOver={(e) => {
    // Custom culling logic
    const distance = camera.position.distanceTo(e.object.position);
    if (distance < 100) {
      e.object.visible = true;
    } else {
      e.object.visible = false;
    }
  }}
>
```

## Performance Monitoring

```tsx
// Mobile-specific FPS target
const TARGET_FPS = isMobile ? 30 : 60;

useFrame(() => {
  const fps = 1 / clock.getDelta();
  if (isMobile && fps < 25) {
    // Reduce quality dynamically
    setQualityLevel(Math.max(0.5, qualityLevel - 0.1));
  }
});
```

## Common Mobile Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Overheating | Too many draw calls | Reduce instances, lower poly |
| Battery drain | 60 FPS on mobile | Cap at 30 FPS |
| Crashes | Memory leak | Dispose textures/geometries |
| Visual artifacts | Unsupported format | Use WebP, not PNG |

## Checklist

- [ ] DPR limited to 1.0-1.5
- [ ] Shadows disabled
- [ ] Anti-aliasing disabled
- [ ] Textures compressed (WebP)
- [ ] Draw calls under 50
- [ ] Polygon count under 100K
- [ ] FPS capped at 30 if needed
- [ ] Post-processing minimal

## Reference

- [performance-basics.md](./performance-basics.md) - Core optimization
- [lod-systems.md](./lod-systems.md) - LOD for mobile
