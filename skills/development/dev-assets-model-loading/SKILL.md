---
name: dev-assets-model-loading
description: FBX model loading patterns with sequential loading for React Three Fiber. Use when loading multiple FBX character models, implementing sequential loading to prevent memory overload, or creating character model components with proper error handling.
category: assets
---

# FBX Model Loading Patterns

## When to Use

- Loading multiple FBX character models
- Implementing sequential loading to prevent memory overload
- Creating character model components with proper error handling
- Working with React Three Fiber and @react-three/drei

## Quick Start

### Basic FBX Loader
```typescript
import { useFBX } from '@react-three/drei';

function CharacterModel({ characterType, position = [0, 0, 0] }: {
  characterType: string;
  position?: [number, number, number];
}) {
  const fbx = useFBX(`/assets/${characterType}.fbx`);

  return (
    <primitive
      object={fbx}
      position={position}
      scale={[1, 1, 1]}
    />
  );
}
```

### Sequential Loading for Multiple Characters
```typescript
import { useFBX, useProgress } from '@react-three/drei';
import { Suspense, useState, useEffect } from 'react';

function CharacterSpawner({ characters }: { characters: string[] }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loadedModels, setLoadedModels] = useState<any[]>([]);

  useEffect(() => {
    if (currentIndex < characters.length) {
      // Load one character at a time
      const timer = setTimeout(() => {
        setCurrentIndex(prev => prev + 1);
      }, 1000); // 1 second delay between loads

      return () => clearTimeout(timer);
    }
  }, [currentIndex, characters.length]);

  const loadNextCharacter = () => {
    if (currentIndex < characters.length) {
      const characterType = characters[currentIndex];
      const fbx = useFBX(`/assets/${characterType}.fbx`);
      setLoadedModels(prev => [...prev, { type: characterType, model: fbx }]);
    }
  };

  // Note: This is a simplified example. In practice, use a proper loading manager
  // or implement a custom loader that loads models sequentially.

  return (
    <Suspense fallback={<LoadingScreen />}>
      {characters.slice(0, currentIndex + 1).map((char, index) => (
        <CharacterModel key={index} characterType={char} />
      ))}
    </Suspense>
  );
}
```

## Anti-Patterns

❌ **DON'T:** Load all models simultaneously
```typescript
// Bad - Causes memory spike and long loading time
function AllCharactersAtOnce({ characters }: { characters: string[] }) {
  return (
    <>
      {characters.map(char => (
        <CharacterModel key={char} characterType={char} />
      ))}
    </>
  );
}
```

✅ **DO:** Load models sequentially with progress tracking
```typescript
function SequentialCharacterLoader({ characters }: { characters: string[] }) {
  const [loadingIndex, setLoadingIndex] = useState(0);
  const [loadedModels, setLoadedModels] = useState<string[]>([]);

  useEffect(() => {
    if (loadingIndex < characters.length) {
      const timer = setTimeout(() => {
        setLoadedModels(prev => [...prev, characters[loadingIndex]]);
        setLoadingIndex(prev => prev + 1);
      }, 500); // 500ms delay per model

      return () => clearTimeout(timer);
    }
  }, [loadingIndex, characters]);

  return (
    <Suspense fallback={<div>Loading characters...</div>}>
      {loadedModels.map((char, index) => (
        <CharacterModel key={index} characterType={char} />
      ))}
    </Suspense>
  );
}
```

❌ **DON'T:** Use useLoader with custom implementations without proper cleanup
```typescript
// Bad - Memory leaks and improper resource management
function BadLoader() {
  const [models, setModels] = useState<any[]>([]);

  // This will keep loading models without cleanup
  useEffect(() => {
    models.forEach(model => {
      // No cleanup of Three.js objects
    });
  }, [models]);
}
```

✅ **DO:** Proper resource management and cleanup
```typescript
import { useRef, useEffect } from 'react';

function CharacterModelWithCleanup({ characterType }: { characterType: string }) {
  const modelRef = useRef<THREE.Group>(null);
  const fbx = useFBX(`/assets/${characterType}.fbx`);

  useEffect(() => {
    // Cleanup when component unmounts
    return () => {
      if (modelRef.current) {
        // Dispose of Three.js objects to prevent memory leaks
        modelRef.current.traverse((child: any) => {
          if (child.isMesh) {
            child.geometry?.dispose();
            child.material?.dispose();
          }
        });
      }
    };
  }, []);

  return (
    <primitive
      ref={modelRef}
      object={fbx}
    />
  );
}
```

## Advanced Loading Patterns

### Progressive Loading with Priority
```typescript
type Priority = 'high' | 'medium' | 'low';

interface PriorityModel {
  type: string;
  priority: Priority;
  position: [number, number, number];
}

function PriorityLoader({ models }: { models: PriorityModel[] }) {
  const [loadingQueue, setLoadingQueue] = useState<PriorityModel[]>([]);
  const [activeModels, setActiveModels] = useState<PriorityModel[]>([]);

  // Sort by priority and load high priority first
  useEffect(() => {
    const sorted = [...models].sort((a, b) => {
      const priorityOrder = { high: 0, medium: 1, low: 2 };
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    });
    setLoadingQueue(sorted);
  }, [models]);

  useEffect(() => {
    if (loadingQueue.length > 0 && activeModels.length < 3) { // Max 3 concurrent
      const nextModel = loadingQueue[0];
      const timer = setTimeout(() => {
        setActiveModels(prev => [...prev, nextModel]);
        setLoadingQueue(prev => prev.slice(1));
      }, 1000);

      return () => clearTimeout(timer);
    }
  }, [loadingQueue, activeModels.length]);

  return (
    <Suspense fallback={<LoadingScreen />}>
      {activeModels.map((model, index) => (
        <CharacterModel
          key={index}
          characterType={model.type}
          position={model.position}
        />
      ))}
    </Suspense>
  );
}
```

### Loading Manager with State
```typescript
type LoadingState = 'idle' | 'loading' | 'loaded' | 'error';

interface LoadingManager {
  models: Record<string, LoadingState>;
  progress: number;
  errors: string[];
}

function useCharacterLoader(characters: string[]): LoadingManager {
  const [loadingState, setLoadingState] = useState<LoadingManager>({
    models: {},
    progress: 0,
    errors: []
  });

  useEffect(() => {
    const loadModels = async () => {
      setLoadingState(prev => ({
        ...prev,
        models: characters.reduce((acc, char) => ({ ...acc, [char]: 'loading' }), {})
      }));

      for (let i = 0; i < characters.length; i++) {
        const character = characters[i];
        try {
          const fbx = useFBX(`/assets/${character}.fbx`);
          setLoadingState(prev => ({
            ...prev,
            models: { ...prev.models, [character]: 'loaded' },
            progress: ((i + 1) / characters.length) * 100
          }));
        } catch (error) {
          setLoadingState(prev => ({
            ...prev,
            models: { ...prev.models, [character]: 'error' },
            errors: [...prev.errors, `Failed to load ${character}`]
          }));
        }
      }
    };

    loadModels();
  }, [characters]);

  return loadingState;
}
```

## Error Handling and Recovery

### Error Boundaries
```typescript
import { ErrorBoundary } from 'react-error-boundary';

function CharacterLoaderWithErrorHandling({ characters }: { characters: string[] }) {
  return (
    <ErrorBoundary
      FallbackComponent={({ error, resetErrorBoundary }) => (
        <div>
          <h2>Failed to load characters</h2>
          <p>{error.message}</p>
          <button onClick={resetErrorBoundary}>Try again</button>
        </div>
      )}
    >
      <Suspense fallback={<LoadingScreen />}>
        {characters.map(char => (
          <CharacterModel key={char} characterType={char} />
        ))}
      </Suspense>
    </ErrorBoundary>
  );
}
```

### Retry Mechanism
```typescript
function CharacterModelWithRetry({ characterType }: { characterType: string }) {
  const [retryCount, setRetryCount] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const loadCharacter = () => {
    try {
      const fbx = useFBX(`/assets/${characterType}.fbx`);
      return fbx;
    } catch (err) {
      setError(`Failed to load ${characterType}`);
      if (retryCount < 3) {
        setTimeout(() => {
          setRetryCount(prev => prev + 1);
        }, 2000);
      }
      throw err;
    }
  };

  const fbx = useRetry(loadCharacter, [characterType, retryCount]);

  if (error && retryCount >= 3) {
    return <div>Failed to load {characterType} after 3 attempts</div>;
  }

  return <primitive object={fbx} />;
}
```

## FBX Scale Validation

### Problem: Scale Confusion Causes 10x Size Errors

Asset pack FBX models often require dramatically different scale values than expected. The Blaster Kit requires 0.015 scale (not 0.15), causing weapons to appear 10x too large if incorrect.

### Solution: Scale Configuration with Documentation

```tsx
// src/components/assets/WeaponModel.tsx
// CRITICAL: Document scale values with source and date

interface WeaponScaleConfig {
  scale: number;
  source: string;           // Asset pack name
  verifiedDate: string;     // When scale was tested
  notes?: string;           // Any special considerations
}

const FBX_SCALE_REGISTRY: Record<string, WeaponScaleConfig> = {
  // Blaster Kit - requires 0.015 scale
  blaster_rifle: {
    scale: 0.015,
    source: 'Blaster Kit',
    verifiedDate: '2026-01-25',
    notes: 'CRITICAL: 0.15 makes weapon GIGANTIC (10x too large)',
  },
  // Other asset packs - use 1.0 as default
  plasma_gun: {
    scale: 1.0,
    source: 'Weapon Pack',
    verifiedDate: '2026-01-25',
  },
};
```

### Unit Test for Scale Validation

```tsx
// src/components/assets/__tests__/WeaponModel.test.ts
import { describe, it, expect } from 'vitest';
import { FBX_SCALE_REGISTRY } from '../WeaponModel';

describe('WeaponModel Scale Validation', () => {
  it('should have documented scale for each weapon type', () => {
    const weaponTypes = ['blaster_rifle', 'plasma_gun', 'shotgun'];

    weaponTypes.forEach(type => {
      expect(FBX_SCALE_REGISTRY[type]).toBeDefined();
      expect(FBX_SCALE_REGISTRY[type].scale).toBeGreaterThan(0);
      expect(FBX_SCALE_REGISTRY[type].scale).toBeLessThan(10); // Sanity check
      expect(FBX_SCALE_REGISTRY[type].source).toBeTruthy();
      expect(FBX_SCALE_REGISTRY[type].verifiedDate).toMatch(/\d{4}-\d{2}-\d{2}/);
    });
  });

  it('should flag suspicious scale values (0.15 instead of 0.015)', () => {
    // Common mistake: 0.15 is too large for Blaster Kit
    Object.values(FBX_SCALE_REGISTRY).forEach(config => {
      if (config.source === 'Blaster Kit') {
        expect(config.scale).toBeLessThan(0.02); // Blaster Kit needs ~0.015
      }
    });
  });
});
```

### Scale Detection Helper for Development

```tsx
import { useEffect, useRef } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';

/**
 * Development helper to detect actual asset scale
 * Use during development to populate FBX_SCALE_REGISTRY
 */
function useAssetScaleDetection(assetUrl: string) {
  const { scene } = useGLTF(assetUrl);
  const scaleInfo = useRef<{ size: THREE.Vector3; suggestedScale: number } | null>(null);

  useEffect(() => {
    const box = new THREE.Box3().setFromObject(scene);
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);

    // For weapons, target size ~0.5 units (hand-held)
    const suggestedScale = 0.5 / maxDim;

    scaleInfo.current = { size, suggestedScale };

    // Log for config development
    console.log(`[Asset Scale Detection] ${assetUrl}`, {
      actualSize: { x: size.x.toFixed(3), y: size.y.toFixed(3), z: size.z.toFixed(3) },
      suggestedScale: suggestedScale.toFixed(4),
      // Use this suggestedScale value in FBX_SCALE_REGISTRY
    });
  }, [scene, assetUrl]);

  return scaleInfo.current;
}

// Usage during development:
// const scaleInfo = useAssetScaleDetection('/assets/models/blaster-rifle.fbx');
// Check console for suggested scale value
```

### Scale Validation Checklist

Before committing weapon/asset code:

- [ ] Scale value is documented in FBX_SCALE_REGISTRY
- [ ] Unit test exists to verify scale is within expected range
- [ ] Visual verification in browser confirms correct size
- [ ] Scale source and verified date are recorded
- [ ] Any special notes (e.g., "CRITICAL: 0.15 is 10x too large") are added

**Learned from bugfix-tps-001 and feat-tps-005 retrospectives (2026-01-25)**:
- Blaster Kit FBX models require 0.015 scale, not 0.15
- Missing scale documentation causes confusion and rework
- Unit tests catch scale regressions before browser testing

## Reference

- [React Three Fiber - Loading Models](https://r3f.docs.pmnd.rs/tutorials/loading-models) — Official R3F documentation
- [Three.js FBX Loader](https://threejs.org/docs/#examples/en/loaders/FBXLoader) — Three.js FBX documentation
- [Vite Asset Handling](https://vite.dev/guide/assets) — Vite static asset management