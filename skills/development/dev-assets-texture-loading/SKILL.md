---
name: dev-assets-texture-loading
description: Texture loading and optimization for R3F. Use when loading image textures.
category: assets
---

# Texture Loading

Optimized texture loading patterns for React Three Fiber.

## When to Use

Use when:
- Loading textures for materials
- Optimizing texture memory usage
- Setting up texture filtering

## Quick Start

```typescript
import { useLoader } from '@react-three/fiber';
import { TextureLoader } from 'three';
import { useMemo } from 'react';

function TexturedMaterial({ textureUrl, color = '#ffffff' }) {
  const texture = useLoader(TextureLoader, textureUrl);

  // Optimize texture settings
  useMemo(() => {
    if (texture) {
      texture.colorSpace = THREE.SRGBColorSpace;
      texture.generateMipmaps = true;
      texture.minFilter = THREE.LinearMipmapLinearFilter;
      texture.magFilter = THREE.LinearFilter;
      texture.anisotropy = 4;
    }
  }, [texture]);

  return (
    <meshStandardMaterial
      map={texture}
      color={color}
    />
  );
}
```

## Vite Asset Import

```typescript
// Import texture with ?url suffix
import woodTexture from '@/assets/textures/wood.jpg?url';

// Use in material
function WoodMaterial() {
  const texture = useLoader(TextureLoader, woodTexture);
  return <meshStandardMaterial map={texture} />;
}
```

## Texture Optimization

```typescript
// Pre-compress textures before adding to src/assets/
// Use WebP format for better compression

const textureOptimization = {
  // Power of 2 dimensions for GPU
  width: 512,   // 512, 1024, 2048, 4096
  height: 512,

  // Compression
  format: 'webp', // WebP > PNG > JPEG

  // Mipmaps for distance
  generateMipmaps: true,
  minFilter: THREE.LinearMipmapLinearFilter,

  // Anisotropic filtering
  anisotropy: 4,  // Max: 16
};
```

## Multiple Textures

```typescript
function MultiTextureMaterial() {
  const [colorMap, normalMap, roughnessMap] = useLoader(TextureLoader, [
    '/textures/diffuse.jpg',
    '/textures/normal.jpg',
    '/textures/roughness.jpg',
  ]);

  return (
    <meshStandardMaterial
      map={colorMap}
      normalMap={normalMap}
      roughnessMap={roughnessMap}
    />
  );
}
```

## Environment Maps

```typescript
import { Environment, CubeCamera } from '@react-three/drei';

function SceneWithReflection() {
  return (
    <>
      {/* Pre-generated environment map */}
      <Environment preset="city" />

      {/* Or custom HDRI */}
      <Environment files="/hdr/studio.hdr" />
    </>
  );
}
```

## Texture Disposal

```typescript
useEffect(() => {
  const texture = textureLoader.load('/texture.jpg');

  return () => {
    // Always dispose textures when done
    texture.dispose();
  };
}, []);
```

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| Non-power-of-2 dimensions | Use 512, 1024, 2048 |
| Not setting colorSpace | Set to SRGBColorSpace |
| Large textures for mobile | Use smaller textures on mobile |
| Not disposing | Always dispose in cleanup |
| Using PNG unnecessarily | Use WebP for better compression |

## Mobile Optimization

```typescript
const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent);

const textureSize = isMobile ? 512 : 2048;
const textureFormat = isMobile ? 'webp' : 'jpg';
```

## Reference

- **[dev-assets-model-loading](../dev-assets-model-loading/SKILL.md)** — FBX model loading
- **[dev-assets-audio-loading](../dev-assets-audio-loading/SKILL.md)** — Audio loading
- **[dev-performance-performance-basics](../dev-performance-performance-basics/SKILL.md)** — Performance optimization
