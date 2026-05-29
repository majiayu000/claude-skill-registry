---
name: ta-assets-workflow-vite-6
description: Vite 6 asset handling and optimization workflow for Tech Artists. Use when creating and optimizing assets for Vite 6 builds.
category: asset
---

# Vite 6 Asset Workflow for Tech Artists

## When to Use

- Creating and optimizing assets for Vite 6 builds
- Setting up texture atlases and sprite sheets
- Optimizing FBX models for web loading
- Configuring Vite plugins for asset processing

## Quick Start

### Vite 6 Asset Configuration
```javascript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/your-game-path/',

  // Asset handling
  assetsInclude: ['**/*.fbx', '**/*.glb', '**/*.png', '**/*.jpg', '**/*.webp', '**/*.svg'],

  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['three', '@react-three/fiber', '@react-three/drei'],
        }
      }
    }
  }
});
```

### Asset Organization Structure
```
public/
├── assets/
│   ├── characters/          # FBX models (static)
│   ├── weapons/             # Third-party assets
│   └── environments/        # Terrain, props
src/assets/
├── textures/               # For Vite processing
├── materials/              # Custom shaders/materials
└── ui/                     # UI assets
```

## Anti-Patterns

❌ **DON'T:** Put all assets in one directory
```
src/assets/
├── character.fbx
├── weapon.fbx
├── texture1.png
└── sound1.mp3
```

✅ **DO:** Organize by type and category
```
src/assets/
├── characters/
├── weapons/
├── textures/
└── audio/
```

❌ **DON'T:** Use uncompressed textures
```typescript
const highResTexture = new THREE.TextureLoader().load('1024px_texture.png');
```

✅ **DO:** Optimize textures for web
```typescript
function loadOptimizedTexture(path: string, size: number = 512) {
  const texture = new THREE.TextureLoader().load(path);
  texture.encoding = THREE.sRGBEncoding;
  texture.anisotropy = 4;
  texture.generateMipmaps = true;
  return texture;
}
```

## Asset Optimization

### Texture Optimization
- Use WebP or AVIF formats when supported
- Target 512px-1024px for most textures
- Use 80% quality compression
- Generate mipmaps for 3D assets

### Model Optimization
- Target under 5MB per FBX file
- Remove unused vertices and materials
- Optimize UV mapping
- Use LOD groups for complex models

### Progressive Loading
Load high-priority assets first, defer others:
```typescript
const priorityOrder = ['player', 'weapons', 'enemies', 'environment'];
```

## Advanced Topics

**Texture Atlas Creation:** See [Vite Asset Optimization Guide](https://vite.dev/guide/assets)

**FBX Model Optimization:** See [Three.js Performance](https://threejs.org/docs/#manual/en/introduction/Performance)

**Vite Plugin Configuration:** See [Vite Plugins](https://vite.dev/plugins/)

**Asset Validation:** Run `npm run build` and check bundle size

**Performance Monitoring:** Use Chrome DevTools Performance tab

## Related Skills

For general asset workflow: `Skill("ta-assets-workflow")`
For performance optimization: `Skill("ta-r3f-performance")`

## External References

- [Vite Asset Documentation](https://vite.dev/guide/assets)
- [Three.js Optimization](https://threejs.org/docs/#manual/en/introduction/Performance)
- [Image Optimization](https://github.com/imagemin/imagemin)
