---
name: dev-phaser-sprite-management
description: Sprites, sprite sheets, texture atlases, and object pooling for Phaser
---

# Phaser Sprite Management

> "Efficient sprite handling – sheets, atlases, and object pools."

## Before/After: Manual Arrays vs Phaser Object Pooling

### ❌ Before: Manual Array Management

```typescript
// Manual sprite management without Phaser
interface Bullet {
  x: number;
  y: number;
  vx: number;
  vy: number;
  active: boolean;
}

const bullets: Bullet[] = [];
let lastShotTime = 0;

function shoot(x: number, y: number, dx: number, dy: number) {
  // Create new object every shot
  const bullet: Bullet = {
    x, y,
    vx: dx * 500,
    vy: dy * 500,
    active: true
  };
  bullets.push(bullet);
}

function updateBullets(dt: number) {
  for (let i = bullets.length - 1; i >= 0; i--) {
    const b = bullets[i];
    b.x += b.vx * dt;
    b.y += b.vy * dt;

    // Manual cleanup triggers GC pressure
    if (b.x < 0 || b.x > 800 || b.y < 0 || b.y > 600 || !b.active) {
      bullets.splice(i, 1); // Expensive operation
    }
  }
}

// Problems:
// - New objects every shot (GC pressure)
// - Array splice is expensive
// - No pre-allocation
// - Manual lifecycle management
```

### ✅ After: Phaser Object Pooling

```typescript
// Phaser handles pooling automatically
export class GameScene extends Phaser.Scene {
  private bulletPool!: Phaser.GameObjects.Group;

  create() {
    // Pre-allocate bullet pool
    this.bulletPool = this.add.group({
      defaultKey: 'bullet',
      maxSize: 50, // Never exceeds 50 objects
      createCallback: (bullet: Phaser.GameObjects.Image) => {
        bullet.setActive(false).setVisible(false);
      }
    });

    // Pre-fill pool for performance
    for (let i = 0; i < 20; i++) {
      this.bulletPool.get(0, 0);
    }
  }

  fireBullet(x: number, y: number, vx: number, vy: number) {
    const bullet = this.bulletPool.get(x, y) as Phaser.GameObjects.Image;

    if (bullet) {
      bullet.setActive(true).setVisible(true);

      // Animate and return to pool when done
      this.tweens.add({
        targets: bullet,
        x: x + vx * 2,
        y: y + vy * 2,
        duration: 500,
        onComplete: () => {
          this.bulletPool.killAndHide(bullet);
        }
      });
    }
  }
}

// Benefits:
// - Objects reused (no GC)
// - killAndHide is fast
// - Pre-allocated pool
// - Automatic lifecycle
```

## When to Use This Skill

Use when:

- Creating and managing game sprites
- Working with sprite sheets and texture atlases
- Implementing object pooling for performance
- Optimizing sprite rendering
- Managing sprite animations

## Quick Start

```typescript
// Load sprite sheet in preload()
this.load.spritesheet("player", "assets/player.png", {
  frameWidth: 32,
  frameHeight: 32,
  startFrame: 0,
  endFrame: 15,
});

// Create sprite in create()
const player = this.add.sprite(400, 300, "player", 0);
player.play("idle");
```

## Decision Framework

| Need                  | Use                            |
| --------------------- | ------------------------------ |
| Single image          | `load.image()` + `add.image()` |
| Animation frames      | `load.spritesheet()`           |
| Multiple sprites      | `load.atlas()`                 |
| Many reusable objects | Object pool                    |
| Physics body          | `physics.add.sprite()`         |

## Progressive Guide

### Level 1: Basic Sprite Loading

```typescript
export class MainScene extends Phaser.Scene {
  preload() {
    // Single image
    this.load.image("player", "assets/player.png");

    // Sprite sheet (horizontal strip)
    this.load.spritesheet("coin", "assets/coin.png", {
      frameWidth: 16,
      frameHeight: 16,
      endFrame: 7,
    });

    // Multi-row sprite sheet
    this.load.spritesheet("player", "assets/player.png", {
      frameWidth: 32,
      frameHeight: 48,
      startFrame: 0,
      endFrame: 47,
    });
  }

  create() {
    // Create sprite
    const player = this.add.sprite(400, 300, "player");

    // Set frame manually
    player.setFrame(5);

    // Flip sprite
    player.setFlipX(true);
    player.setFlipY(false);
  }
}
```

### Level 2: Texture Atlas Loading

```typescript
preload() {
  // Load atlas with JSON (from TexturePacker)
  this.load.atlas('game', 'assets/atlas.png', 'assets/atlas.json');

  // Load atlas with XML (from Shoebox)
  this.load.atlasXML('ui', 'assets/ui.png', 'assets/ui.xml');

  // Load atlas with hash array (Unity-style)
  this.load.atlas('items', 'assets/items.png', 'assets/items.json');
}

create() {
  // Create sprite from atlas
  const sword = this.add.image(400, 300, 'game', 'sword.png');
  const shield = this.add.image(400, 350, 'game', 'shield.png');
}
```

### Level 3: Sprite Animations

```typescript
create() {
  // Create animations from sprite sheet
  this.anims.create({
    key: 'idle',
    frames: this.anims.generateFrameNumbers('player', {
      start: 0,
      end: 3
    }),
    frameRate: 10,
    repeat: -1 // Infinite loop
  });

  this.anims.create({
    key: 'walk',
    frames: this.anims.generateFrameNumbers('player', {
      start: 4,
      end: 11
    }),
    frameRate: 12,
    repeat: -1
  });

  this.anims.create({
    key: 'attack',
    frames: this.anims.generateFrameNumbers('player', {
      start: 12,
      end: 17
    }),
    frameRate: 15,
    repeat: 0 // Play once
  });

  // Play animation on sprite
  const player = this.add.sprite(400, 300, 'player');
  player.play('idle');

  // Change animation
  player.play('walk', true); // true = ignore if playing
}
```

### Level 4: Object Pooling

```typescript
export class MainScene extends Phaser.Scene {
  private bulletPool!: Phaser.GameObjects.Group;
  private readonly MAX_BULLETS = 50;

  create() {
    // Pre-create bullet pool
    this.bulletPool = this.add.group({
      defaultKey: "bullet",
      maxSize: this.MAX_BULLETS,
      createCallback: (bullet: Phaser.GameObjects.Image) => {
        bullet.setActive(false).setVisible(false);
      },
    });

    // Pre-fill pool
    for (let i = 0; i < 20; i++) {
      this.bulletPool.get(0, 0);
    }

    this.input.on("pointerdown", this.fireBullet, this);
  }

  fireBullet() {
    const bullet = this.bulletPool.get(
      this.player.x,
      this.player.y,
    ) as Phaser.GameObjects.Image;

    if (bullet) {
      bullet.setActive(true).setVisible(true);

      // Animate bullet
      this.tweens.add({
        targets: bullet,
        x: bullet.x + 500,
        duration: 500,
        onComplete: () => {
          // Return to pool
          bullet.setActive(false).setVisible(false);
          this.bulletPool.killAndHide(bullet);
        },
      });
    }
  }
}
```

### Level 5: Advanced Sprite Management

```typescript
export class MainScene extends Phaser.Scene {
  private spriteManager!: SpriteManager;

  create() {
    this.spriteManager = new SpriteManager(this);

    // Register sprite types
    this.spriteManager.registerType("enemy", {
      poolSize: 30,
      onCreate: (sprite) => this.setupEnemy(sprite),
      onActivate: (sprite, data) => this.spawnEnemy(sprite, data),
      onDeactivate: (sprite) => this.cleanupEnemy(sprite),
    });
  }

  update() {
    // Spawn enemy
    this.spriteManager.spawn("enemy", { x: 400, y: 100, type: "flying" });
  }
}

// Sprite Manager class
class SpriteManager {
  private pools = new Map<string, Phaser.GameObjects.Group>();

  constructor(private scene: Phaser.Scene) {}

  registerType(
    type: string,
    config: {
      poolSize: number;
      onCreate: Function;
      onActivate: Function;
      onDeactivate: Function;
    },
  ) {
    this.pools.set(
      type,
      this.scene.add.group({
        defaultKey: type,
        maxSize: config.poolSize,
        createCallback: config.onCreate,
        removeCallback: config.onDeactivate,
      }),
    );
  }

  spawn(type: string, data: any) {
    const pool = this.pools.get(type);
    if (!pool) return null;

    const sprite = pool.get(data.x, data.y);
    if (sprite) {
      sprite.setActive(true).setVisible(true);
      pool.config.onActivate(sprite, data);
    }
    return sprite;
  }

  despawn(type: string, sprite: Phaser.GameObjects.GameObject) {
    const pool = this.pools.get(type);
    if (pool) {
      pool.killAndHide(sprite);
    }
  }
}
```

## Anti-Patterns

❌ **DON'T:**

- Load individual images for sprite frames - use sprite sheets
- Create/destroy sprites every frame - use object pooling
- Use large atlases without grouping - organize by scene/use
- Forget to `killAndHide()` pooled objects before reuse
- Mix pixel densities in sprite sheets
- Use `add.sprite()` when physics needed - use `physics.add.sprite()`

✅ **DO:**

- Use TexturePacker or similar for atlas generation
- Pre-allocate pools during scene creation
- Group atlas textures by logical usage
- Set active/visible false when returning to pool
- Use consistent frame sizes in sprite sheets
- Cache frequently used sprites

## Code Patterns

### Object Pool with Custom Class

```typescript
class Bullet extends Phaser.GameObjects.Image {
  declare body: Phaser.Physics.Arcade.Body;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'bullet');
    scene.add.existing(this);
    scene.physics.add.existing(this);
  }

  fire(x: number, y: number, velocity: Phaser.Math.Vector2) {
    this.setPosition(x, y);
    this.body.setVelocity(velocity.x, velocity.y);
    this.setActive(true);
    this.setVisible(true);
  }

  reset() {
    this.body.setVelocity(0, 0);
    this.setActive(false);
    this.setVisible(false);
    this.setPosition(-1000, -1000); // Off-screen
  }
}

// In scene
create() {
  this.bullets = this.add.group({
    classType: Bullet,
    maxSize: 50,
    runChildUpdate: true
  });
}
```

### Sprite Sheet with Multi-Row Animation

```typescript
// 4x4 sprite sheet (16 frames)
// Row 1: Idle (0-3)
// Row 2: Walk (4-7)
// Row 3: Attack (8-11)
// Row 4: Die (12-15)

this.anims.create({
  key: "idle",
  frames: this.anims.generateFrameNumbers("player", {
    start: 0,
    end: 3,
  }),
  frameRate: 8,
  repeat: -1,
  yoyo: false,
});

this.anims.create({
  key: "walk",
  frames: this.anims.generateFrameNumbers("player", {
    start: 4,
    end: 7,
  }),
  frameRate: 12,
  repeat: -1,
});
```

## Checklist

- [ ] Using sprite sheets or atlases (not individual images)
- [ ] Object pools pre-allocated
- [ ] Sprites properly returned to pool
- [ ] Animations defined before use
- [ ] Frame sizes consistent
- [ ] Texture memory optimized
- [ ] Off-screen sprites culled

## Reference

- [Phaser Loader](https://photonstorm.github.io/phaser3-docs/Phaser.Loader.LoaderPlugin.html) — Loading assets
- [Phaser Animations](https://photonstorm.github.io/phaser3-docs/Phaser.Animations.AnimationManager.html) — Animation system
- [Phaser Groups](https://photonstorm.github.io/phaser3-docs/Phaser.GameObjects.Group.html) — Object grouping
