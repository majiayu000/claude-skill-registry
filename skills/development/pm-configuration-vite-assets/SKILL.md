---
name: pm-configuration-vite-assets
description: Vite 6 asset configuration patterns for React Three Fiber projects
category: configuration
---

# Vite 6 Asset Configuration Coordination

## When to Use

- Coordinating asset configuration between agents
- Reviewing asset loading implementations
- Resolving asset-related build issues
- Setting up new 3D asset workflows

## Quick Start

````markdown
## Asset Configuration Checklist

### Before Asset Loading Implementation

1. **Verify asset placement:**
   - FBX/GLB: Use `src/assets/` (processed by Vite)
   - Static assets: Use `public/` (served as-is)
   - Audio files: Use `src/assets/audio/` (spatial audio setup)

2. **Check vite.config.ts configuration:**
   ```typescript
   assetsInclude: ['**/*.fbx', '**/*.glb', '**/*.png', '**/*.ogg'];
   optimizeDeps: {
     exclude: ['*.fbx']; // Single wildcard for Vite 6
   }
   ```
````

3. **Verify asset plugin handles both URL patterns:**
   - `/assets/` (production)
   - `/src/assets/` (development)

````

## Key Configuration Patterns

### Wildcard Patterns

**❌ DON'T:**
```typescript
// Vite 6 doesn't support double wildcards in optimizeDeps.exclude
exclude: ['**/*.fbx']
````

**✅ DO:**

```typescript
// Vite 6 requires single wildcard in optimizeDeps.exclude
optimizeDeps: {
  exclude: ['*.fbx']; // Single asterisk only
}

// But double wildcards work in assetsInclude
assetsInclude: ['**/*.fbx', '**/*.glb', '**/*.png'];
```

### Asset URL Generation

**Development vs Production URLs:**

```typescript
// Development: Vite serves from /src/assets/
const modelUrl = '/src/assets/models/character.fbx';

// Production: Vite processes to /assets/ with hash
const modelUrl = '/assets/models/character.abc123.fbx';
```

### Asset Directory Strategy

| Asset Type     | Directory              | Processing   | URL Pattern                 | Use Case                            |
| -------------- | ---------------------- | ------------ | --------------------------- | ----------------------------------- |
| FBX/GLB Models | `src/assets/models/`   | ✅ Optimized | `/src/assets/` → `/assets/` | Game characters, props              |
| Audio Files    | `src/assets/audio/`    | ✅ Optimized | `/src/assets/` → `/assets/` | Sound effects, music                |
| Textures       | `src/assets/textures/` | ✅ Optimized | `/src/assets/` → `/assets/` | Material textures, decals           |
| Static Assets  | `public/`              | ❌ As-is     | `/filename.ext`             | Favicon, manifest, external scripts |
| UI Assets      | `src/assets/ui/`       | ✅ Optimized | `/src/assets/` → `/assets/` | UI sprites, icons                   |

## Common Pitfalls

### 1. Asset Path Resolution

**❌ Anti-Pattern:**

```typescript
// Using relative paths without alias
import model from '../../assets/models/character.fbx';
```

**✅ Best Practice:**

```typescript
// Using alias path resolution
import model from '@/assets/models/character.fbx';

// Using dynamic URL resolution
const modelPath = new URL('/assets/models/character.fbx', import.meta.url).href;
```

### 2. Binary File Handling

**❌ Anti-Pattern:**

```typescript
// Vite tries to inline large binary files
build: {
  assetsInlineLimit: 4096; // May inappropriately inline FBX files
}
```

**✅ Best Practice:**

```typescript
// Ensure binary files are served as separate files
build: {
  assetsInlineLimit: 0; // Never inline binary assets
}
```

### 3. Development Server Configuration

**❌ Anti-Pattern:**

```typescript
// Strict file serving prevents src/assets access
server: {
  fs: {
    strict: true;
  } // Blocks parent directory access
}
```

**✅ Best Practice:**

```typescript
server: {
  fs: {
    strict: false;
  } // Allow src/assets serving
}
```

## Agent Coordination Guidelines

### PM Coordination Tasks

1. **Asset Standardization:**
   - Define consistent asset directory structure
   - Establish naming conventions for assets
   - Coordinate asset format standards (FBX vs GLB)

2. **Build Process Oversight:**
   - Monitor build times with asset changes
   - Track asset bundle sizes
   - Coordinate asset optimization efforts

3. **Cross-Agent Communication:**
   - Ensure Developer and Tech Artist use compatible asset loading
   - Coordinate QA testing of asset loading in different environments
   - Document asset-related bugs for resolution

### Developer Implementation Notes

```typescript
// Proper asset loading pattern for React Three Fiber
import { useLoader } from '@react-three/fiber'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader'

function Model({ url, type }: { url: string; type: 'glb' | 'fbx' }) {
  const model = type === 'glb'
    ? useLoader(GLTFLoader, url)
    : useLoader(FBXLoader, url)

  return <primitive object={model.scene} />
}
```

### Tech Artist Asset Preparation

```markdown
## Asset Preparation Guidelines

### FBX Models

- Use FBX 2020 format for compatibility
- Remove unused materials and textures
- Apply proper scale (1 unit = 1 meter)
- Include animations in FBX file
- Optimize polygon count (< 50k for main character)

### Audio Files

- Use OGG format for web compatibility
- Optimize sample rate (44.1kHz)
- Implement spatial audio positioning
- Compress files < 1MB where possible
```

### QA Testing Points

```markdown
## Asset Testing Checklist

### Build Tests

- [ ] FBX files copied to dist/assets/
- [ ] No "Cannot find version number" errors
- [ ] Assets load in both dev and production builds
- [ ] No 404 errors for asset URLs

### Performance Tests

- [ ] Asset loading time < 2 seconds
- [ ] Memory usage remains stable
- [ ] No asset memory leaks
- [ ] FPS maintained with asset loading

### Browser Tests

- [ ] Assets load in Chrome, Firefox, Safari
- [ ] Mobile device asset loading
- [ ] Slow network simulation
- [ ] Cache behavior verification
```

## Configuration Template

### vite.config.ts for R3F Projects

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import fs from 'fs';

// Custom asset plugin
function assetsPlugin() {
  return {
    name: 'assets-server',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const isAssetsPath = req.url?.startsWith('/assets/') || req.url?.startsWith('/src/assets/');
        if (!isAssetsPath) return next();

        let normalizedPath = req.url!;
        if (normalizedPath.startsWith('/assets/') && !normalizedPath.startsWith('/src/assets/')) {
          normalizedPath = '/src' + normalizedPath;
        }

        const urlPath = decodeURIComponent(normalizedPath);
        const filePath = path.join(__dirname, urlPath);

        fs.stat(filePath, (err, stats) => {
          if (err || !stats.isFile()) return next();

          const ext = path.extname(filePath).toLowerCase();
          const contentTypes = {
            '.fbx': 'application/octet-stream',
            '.glb': 'model/gltf-binary',
            '.ogg': 'audio/ogg',
            '.mp3': 'audio/mpeg',
            // ... other content types
          };

          res.setHeader('Content-Type', contentTypes[ext] || 'application/octet-stream');
          res.setHeader('Access-Control-Allow-Origin', '*');
          res.setHeader('Cache-Control', 'public, max-age=3600');

          fs.createReadStream(filePath).pipe(res);
        });
      });
    },
  };
}

export default defineConfig({
  plugins: [react(), assetsPlugin()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@assets': path.resolve(__dirname, './src/assets'),
    },
  },
  server: {
    port: 3000,
    fs: { strict: false },
  },
  build: {
    target: 'esnext',
    assetsInlineLimit: 0,
  },
  optimizeDeps: {
    include: ['three', '@react-three/fiber', '@react-three/drei'],
    exclude: ['*.fbx'], // Single wildcard for Vite 6
  },
  assetsInclude: [
    '**/*.fbx',
    '**/*.glb',
    '**/*.gltf',
    '**/*.png',
    '**/*.jpg',
    '**/*.jpeg',
    '**/*.ogg',
    '**/*.mp3',
    '**/*.wav',
  ],
  publicDir: 'public',
});
```

## Reference

- [Vite Static Asset Handling](https://vite.dev/guide/assets)
- [React Three Fiber Asset Loading](https://r3f.docs.pmnd.rs/tutorials/loading-models)
- [Three.js Asset Optimization](https://www.utsubo.com/blog/threejs-best-practices-100-tips)
