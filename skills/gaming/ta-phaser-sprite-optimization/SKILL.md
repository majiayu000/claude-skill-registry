---
name: ta-phaser-sprite-optimization
description: Optimizes sprite atlases and textures for Phaser. Use proactively when optimizing sprite workflows or managing texture memory.
category: techartist
---

# Phaser Sprite Optimization

> "Maximize performance and minimize memory with optimized sprite workflows."

## When to Use This Skill

Use when:

- Creating sprite atlases
- Optimizing texture memory
- Reducing draw calls
- Managing sprite memory
- Preparing assets for production

## Quick Start

```typescript
// Load atlas instead of individual images
this.load.atlas("game", "assets/atlas.png", "assets/atlas.json");

// Create from atlas
const sprite = this.add.image(400, 300, "game", "player.png");
```

## Optimization Principles

1. **Minimize Draw Calls** - Use atlases to batch sprites
2. **Reduce Texture Swaps** - Group related sprites
3. **Optimize Memory** - Use appropriate texture formats
4. **Cache Smartly** - Preload, reuse, pool
5. **Target Platform** - Mobile vs desktop considerations

## Progressive Guide

### Level 1: Texture Atlas Creation

```
Using TexturePacker:
1. Import all sprite images
2. Set settings:
   - Algorithm: MaxRects
   - Padding: 2px (prevent bleeding)
   - Extrude: 1px (prevent seams)
   - Rotate: Disabled (Phaser compatible)
3. Export format: JSON (Hash)
```

```typescript
// Load atlas
preload() {
  this.load.atlas('characters', 'assets/characters.png', 'assets/characters.json');
  this.load.atlas('ui', 'assets/ui.png', 'assets/ui.json');
  this.load.atlas('tiles', 'assets/tiles.png', 'assets/tiles.json');
}

create() {
  // Use atlas
  const player = this.add.image(400, 300, 'characters', 'player/idle.png');
  const coin = this.add.image(400, 300, 'tiles', 'items/coin.png');
  const button = this.add.image(400, 300, 'ui', 'buttons/start.png');
}
```

### Level 2: Texture Format Optimization

```typescript
// Recommended texture formats by platform
const TEXTURE_CONFIG = {
  // Desktop: PNG for quality, WebP for size
  desktop: {
    format: 'png',
    quality: 1.0
  },

  // Mobile: WebP or compressed PNG
  mobile: {
    format: 'webp', // or 'png'
    quality: 0.8,
    maxTextureSize: 2048
  },

  // iOS: PVRTC (if supported)
  ios: {
    format: 'pvr',
    compression: 'PVRTC_4BPP'
  },

  // Android: ETC2 (if supported)
  android: {
    format: 'etc2',
    compression: 'ETC2_RGB'
  }
};

// Load with platform detection
preload() {
  const isMobile = this.sys.game.device.os.android ||
                   this.sys.game.device.os.iOS;

  if (isMobile) {
    this.load.atlas('game', 'assets/game.webp', 'assets/game.json');
  } else {
    this.load.atlas('game', 'assets/game.png', 'assets/game.json');
  }
}
```

### Level 3: Sprite Sheet Best Practices

```typescript
// Efficient sprite sheet setup
class SpriteSheetConfig {
  // 2x scale for pixel art (nearest neighbor)
  static readonly PIXEL_ART = {
    scale: 2,
    filterMode: Phaser.Textures.FilterMode.NEAREST
  };

  // Smooth scaling for HD art
  static readonly HD_ART = {
    scale: 1,
    filterMode: Phaser.Textures.FilterMode.LINEAR
  };

  static setupPixelArt(scene: Phaser.Scene) {
    scene.textures.setDefaultFilterModes(
      Phaser.Textures.FilterMode.NEAREST,
      Phaser.Textures.FilterMode.NEAREST
    );
  }

  static setupHDArt(scene: Phaser.Scene) {
    scene.textures.setDefaultFilterModes(
      Phaser.Textures.FilterMode.LINEAR,
      Phaser.Textures.FilterMode.LINEAR
    );
  }
}

// Usage
preload() {
  SpriteSheetConfig.setupPixelArt(this);
  this.load.spritesheet('player', 'assets/player.png', {
    frameWidth: 16,  // Source size (before scale)
    frameHeight: 16,
    margin: 0,
    spacing: 0
  });
}
```

### Level 4: Memory Management

```typescript
class AssetManager {
  private cache: Map<string, boolean> = new Map();
  private references: Map<string, number> = new Map();

  constructor(private scene: Phaser.Scene) {}

  preloadAtlas(key: string, textureUrl: string, jsonUrl: string) {
    if (!this.cache.has(key)) {
      this.scene.load.atlas(key, textureUrl, jsonUrl);
      this.cache.set(key, false); // Not loaded yet
      this.references.set(key, 0);
    }
    this.references.set(key, (this.references.get(key) || 0) + 1);
  }

  // Unload when no longer needed
  unloadAtlas(key: string) {
    const refCount = this.references.get(key) || 0;
    if (refCount <= 1) {
      this.scene.textures.remove(key);
      this.cache.delete(key);
      this.references.delete(key);
    } else {
      this.references.set(key, refCount - 1);
    }
  }

  // Unload all assets from a scene
  unloadSceneAssets(sceneKey: string) {
    const sceneAssets = this.getSceneAssets(sceneKey);
    sceneAssets.forEach((key) => this.unloadAtlas(key));
  }

  private getSceneAssets(sceneKey: string): string[] {
    // Return list of assets used by scene
    return [];
  }
}

// Texture memory monitoring
class TextureMonitor {
  private textures: Map<
    string,
    { width: number; height: number; format: string }
  > = new Map();

  trackTexture(key: string, texture: Phaser.Textures.Texture) {
    const source = texture.source[0];
    this.textures.set(key, {
      width: source.width,
      height: source.height,
      format: source.format || "rgba",
    });
  }

  getMemoryUsage(): number {
    let total = 0;
    this.textures.forEach((tex) => {
      total += tex.width * tex.height * 4; // 4 bytes per pixel (RGBA)
    });
    return total;
  }

  getMemoryUsageMB(): number {
    return this.getMemoryUsage() / (1024 * 1024);
  }

  report() {
    console.log("Texture Memory Usage:");
    this.textures.forEach((tex, key) => {
      const size = (tex.width * tex.height * 4) / 1024;
      console.log(
        `  ${key}: ${size.toFixed(2)} KB (${tex.width}x${tex.height})`,
      );
    });
    console.log(`  Total: ${this.getMemoryUsageMB().toFixed(2)} MB`);
  }
}
```

### Level 5: Advanced Optimization Techniques

```typescript
class SpriteOptimizer {
  // Multi-atlas system for large projects
  static organizeIntoAtlases(assets: string[]): {
    characters: string[];
    tiles: string[];
    ui: string[];
    effects: string[];
  } {
    return {
      characters: assets.filter((a) => /player|enemy|npc/.test(a)),
      tiles: assets.filter((a) => /tile|ground|wall/.test(a)),
      ui: assets.filter((a) => /button|panel|icon/.test(a)),
      effects: assets.filter((a) => /explosion|spark|smoke/.test(a)),
    };
  }

  // Dynamic texture resolution
  static getTextureScale(): number {
    const pixelRatio = window.devicePixelRatio || 1;

    if (pixelRatio >= 3) return 0.5; // 3x displays, use half res
    if (pixelRatio >= 2) return 0.66; // 2x displays
    return 1; // Standard displays
  }

  // Generate lower-res textures at runtime
  static createMipmaps(scene: Phaser.Scene, key: string) {
    const texture = scene.textures.get(key);
    const source = texture.source[0];

    // Create half-size version
    const halfSizeCanvas = document.createElement("canvas");
    halfSizeCanvas.width = source.width / 2;
    halfSizeCanvas.height = source.height / 2;

    const ctx = halfSizeCanvas.getContext("2d")!;
    ctx.drawImage(
      source.image as HTMLImageElement,
      0,
      0,
      source.width,
      source.height,
      0,
      0,
      halfSizeCanvas.width,
      halfSizeCanvas.height,
    );

    // Add as mipmap
    texture.addMipMap(1, halfSizeCanvas);
  }

  // Batch sprite rendering
  static batchSprites(
    sprites: Phaser.GameObjects.Sprite[],
  ): Phaser.GameObjects.Container {
    const container = sprites[0].scene.add.container(0, 0);

    // Group by texture to minimize draw calls
    const byTexture = new Map<string, Phaser.GameObjects.Sprite[]>();
    sprites.forEach((sprite) => {
      const key = (sprite as any).texture.key;
      if (!byTexture.has(key)) byTexture.set(key, []);
      byTexture.get(key)!.push(sprite);
    });

    // Add sprites in texture order
    byTexture.forEach((spriteList) => {
      spriteList.forEach((sprite) => container.add(sprite));
    });

    return container;
  }

  // Optimize sprite culling
  static setupCulling(
    camera: Phaser.Cameras.Scene2D.Camera,
    sprites: Phaser.GameObjects.Sprite[],
  ) {
    const bounds = new Phaser.Geom.Rectangle();

    sprites.forEach((sprite) => {
      sprite.setVisible(false); // Start hidden
    });

    camera.on("prerender", () => {
      camera.getWorldBounds(bounds);

      sprites.forEach((sprite) => {
        const inView = Phaser.Geom.Rectangle.Overlaps(
          bounds,
          sprite.getBounds(),
        );
        sprite.setVisible(inView);
      });
    });
  }
}
```

## Anti-Patterns

❌ **DON'T:**

- Load individual images for sprite frames
- Use textures larger than device max
- Forget to unload unused textures
- Mix pixel art scaling with HD art
- Create new textures at runtime without cleanup
- Overuse full-screen sprite sheets

✅ **DO:**

- Use atlases for related sprites
- Check device max texture size
- Unload textures between scenes
  | Keep filter modes consistent
  | Cache generated textures
  | Partition large sprite sheets

## Texture Size Guidelines

| Platform      | Max Size | Recommended |
| ------------- | -------- | ----------- |
| Desktop       | 4096+    | 2048        |
| Mobile (high) | 2048     | 1024-2048   |
| Mobile (low)  | 1024     | 512-1024    |
| WebGL1        | 2048     | 1024        |

## Memory Calculator

```typescript
// Estimate texture memory
function calculateTextureMemory(
  width: number,
  height: number,
  format: "rgba" | "rgb" | "pvrtc" = "rgba",
): number {
  const bytesPerPixel = {
    rgba: 4,
    rgb: 3,
    pvrtc: 0.5, // PVRTC 4bpp
    etc2: 0.5,
    s3tc: 0.5,
  };

  return width * height * bytesPerPixel[format];
}

// Examples
const texture1MB = calculateTextureMemory(512, 512, "rgba") / (1024 * 1024); // 1 MB
const textureCompressed =
  calculateTextureMemory(512, 512, "pvrtc") / (1024 * 1024); // 0.125 MB
```

## Checklist

- [ ] Using atlases instead of individual images
- [ ] Texture sizes appropriate for target platform
- [ ] Filter mode consistent (nearest/linear)
- [ ] Unused textures unloaded
- [ ] Memory usage monitored
- [ ] Sprite culling enabled for large scenes
- [ ] Padding added to prevent bleeding

## Reference

- [TexturePacker](https://www.codeandweb.com/texturepacker) — Atlas creation tool
- [Phaser Textures](https://photonstorm.github.io/phaser3-docs/Phaser.Textures.TextureManager.html) — Texture API
