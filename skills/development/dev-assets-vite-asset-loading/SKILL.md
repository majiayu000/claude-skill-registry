---
name: dev-assets-vite-asset-loading
description: Vite 6 asset loading patterns that avoid '?import' query parameter pollution. Use when working with static assets (FBX models, images, fonts), dealing with Vite 6's new asset handling, or loading assets from public vs src/assets directories.
category: assets
---

# Vite 6 Asset Loading Patterns

## When to Use

- Working with static assets (FBX models, images, fonts)
- Dealing with Vite 6's new asset handling
- Avoiding '?import' query parameter pollution
- Loading assets from public directory vs src/assets

## Quick Start

### For FBX Models (public/ directory)
```typescript
import { useFBX } from '@react-three/drei';

// CORRECT - Uses public directory with absolute path
function CharacterModel({ characterType }: { characterType: string }) {
  const fbx = useFBX(`/assets/${characterType}.fbx`);
  return <primitive object={fbx} />;
}

// For public assets that need URL
const imageUrl = new URL('/assets/images/splash.png', import.meta.url);
```

### For CSS/JS Assets (src/assets/ directory)
```typescript
// For assets that need processing
import backgroundImage from '@/assets/images/background.jpg';

// For CSS imports
import '@/styles/global.css';
```

## Anti-Patterns

❌ **DON'T:** Use `import` statements for public directory assets
```typescript
import characterModel from '/assets/character.fbx'; // Creates '?import' query
```

✅ **DO:** Use absolute paths for public assets
```typescript
// In JSX
<img src="/assets/logo.png" alt="Logo" />

// Or with URL constructor
const assetUrl = new URL('/assets/data.json', import.meta.url);
```

❌ **DON'T:** Mix public and src/assets references arbitrarily
```typescript
// Bad - inconsistent approach
function MixedAsset() {
  // This should be in public/ with absolute path
  const localAsset = require('@/assets/icon.png');
  // This should be imported properly
  const publicAsset = '/assets/icon.png';
}
```

✅ **DO:** Consistent directory strategy
```typescript
// All public assets use absolute paths
function ConsistentAssets() {
  return (
    <div>
      <img src="/assets/public-image.jpg" alt="Public" />
      <Model assetUrl="/assets/model.fbx" />
    </div>
  );
}
```

## Asset Directory Strategy

### Public Directory (`public/`)
**Use for:**
- Static files that won't change (favicons, fonts)
- Third-party assets (Blaster Kit, Animated Characters)
- Files served as-is without processing

**Reference pattern:**
```typescript
// Always use absolute paths starting with /
const assetPath = '/assets/Blaster Kit/Models/FBX format/rifle.fbx';
const fbx = useFBX(assetPath);
```

### Src Assets Directory (`src/assets/`)
**Use for:**
- Application-specific assets
- Assets that need processing (images, CSS)
- Assets bundled with your code

**Import pattern:**
```typescript
import processedImage from '@/assets/images/hero.png';
import styles from '@/styles/component.module.css';
```

## Vite 6 Specific Considerations

### Base URL Configuration
```javascript
// vite.config.js
export default defineConfig({
  base: '/your-app-path/', // Important for public assets
  assetsInclude: ['**/*.fbx', '**/*.glb'],
  // ... other config
});
```

### Asset Optimization
- Vite 6 automatically optimizes images, fonts, and media
- Use modern formats (WebP, AVIF when supported)
- Consider lazy loading for non-critical assets

### Cache Busting
```typescript
// For cache busting on public assets
const versionedAsset = `/assets/image.jpg?v=${APP_VERSION}`;

// Or for dynamic assets
const dynamicAsset = new URL(`/assets/${assetId}.png?theme=${theme}`, import.meta.url);
```

## Environment-Specific Paths

### Development
```typescript
// Absolute paths work in dev
const devAsset = '/assets/development-only.json';
```

### Production
```typescript
// Ensure base path is correct for production deployment
const prodAsset = `${import.meta.env.BASE_URL}assets/production.json`;
```

## FBX Model Loading Pattern

### Sequential Loading (Recommended)
```typescript
import { useFBX, useProgress } from '@react-three/drei';
import { Suspense } from 'react';

function SequentialLoader({ characters }: { characters: string[] }) {
  return (
    <Suspense fallback={<LoadingScreen />}>
      {characters.map((char, index) => (
        <CharacterModel key={index} characterType={char} />
      ))}
    </Suspense>
  );
}

function CharacterModel({ characterType }: { characterType: string }) {
  const fbx = useFBX(`/assets/${characterType}.fbx`);

  // Process and return the model
  return (
    <primitive
      object={fbx}
      position={[0, 0, 0]}
      scale={[1, 1, 1]}
    />
  );
}
```

### Loading State Management
```typescript
function AssetLoader() {
  const { active, progress, errors, item } = useProgress();

  if (errors.length > 0) {
    return <div>Error loading assets</div>;
  }

  return (
    <div>
      {active && <div>Loading: {item} - {progress.toFixed(0)}%</div>}
    </div>
  );
}
```

## Reference

- [Vite Static Asset Handling](https://vite.dev/guide/assets) — Official documentation
- [React Three Fiber Loading Models](https://r3f.docs.pmnd.rs/tutorials/loading-models) — R3F model loading patterns
- [Vite 6 Public Directory Usage](https://stackoverflow.com/questions/78811027/when-to-use-public-vs-assets-for-images-and-files-in-a-vite-project) — Community best practices