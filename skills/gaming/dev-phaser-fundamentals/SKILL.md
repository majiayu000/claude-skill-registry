---
name: dev-phaser-fundamentals
description: Phaser game configuration, scenes, and lifecycle management
---

# Phaser Fundamentals

> "2D web games made simple – scenes, sprites, and physics."

## When to Use This Skill

Use when:

- Setting up a new Phaser game
- Creating game scenes
- Implementing the scene lifecycle (preload/create/update)
- Configuring game settings (scale, physics, renderer)
- Setting up the game container and canvas

## Quick Start

```typescript
import Phaser from "phaser";
import { MainScene } from "./scenes/MainScene";

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: "game-container",
  backgroundColor: "#000000",
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
  physics: {
    default: "arcade",
    arcade: {
      gravity: { y: 300 },
      debug: false,
    },
  },
  scene: [MainScene],
};

new Phaser.Game(config);
```

## Before/After: Manual DOM vs Phaser Pattern

### ❌ Before: Manual DOM Manipulation

```typescript
// Manual game loop without Phaser
const canvas = document.getElementById("game") as HTMLCanvasElement;
const ctx = canvas.getContext("2d")!;

let playerX = 400;
let playerY = 300;

// Manual asset loading
const playerImg = new Image();
playerImg.src = "assets/player.png";
playerImg.onload = () => {
  gameLoop();
};

// Manual game loop
function gameLoop() {
  // Clear canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw player
  ctx.drawImage(playerImg, playerX, playerY);

  // Handle input manually
  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") playerX -= 5;
    // ... more manual input handling
  });

  requestAnimationFrame(gameLoop);
}
```

**Problems:**
- Manual asset loading (no preload queue)
- No sprite management
- Manual collision detection
- No physics engine
- Scene management is manual

### ✅ After: Phaser Pattern

```typescript
// Phaser handles everything
export class GameScene extends Phaser.Scene {
  private player!: Phaser.Physics.Arcade.Sprite;

  preload() {
    // Built-in asset loading with progress tracking
    this.load.image("player", "assets/player.png");
  }

  create() {
    // Physics-enabled sprite
    this.player = this.physics.add.sprite(400, 300, "player");

    // Built-in input handling
    this.cursors = this.input.keyboard!.createCursorKeys();
  }

  update() {
    // Frame-independent movement
    if (this.cursors.left!.isDown) {
      this.player.setVelocityX(-160);
    }
    // Built-in physics handles position updates
  }
}

const config = {
  // Phaser manages the game loop, canvas, rendering
  scene: [GameScene],
  physics: { default: "arcade" },
};

new Phaser.Game(config);
```

**Benefits:**
- Asset preloading with progress events
- Built-in physics engine
- Scene lifecycle management
- Input handling abstraction
- Optimized rendering pipeline

## Decision Framework

| Need               | Use                                   |
| ------------------ | ------------------------------------- |
| Basic 2D game      | `Phaser.AUTO` renderer type           |
| Physics platformer | Arcade physics with gravity           |
| Physics puzzle     | Matter physics for realism            |
| Responsive layout  | `Phaser.Scale.FIT` with `CENTER_BOTH` |
| Multiple scenes    | Array of scene classes in config      |

## Progressive Guide

### Level 1: Basic Scene Setup

```typescript
export class MainScene extends Phaser.Scene {
  constructor() {
    super({ key: "MainScene" });
  }

  preload() {
    // Load assets before create()
    this.load.image("player", "assets/player.png");
    this.load.image("background", "assets/bg.png");
  }

  create() {
    // Create game objects
    this.add.image(400, 300, "background");
    this.player = this.physics.add.sprite(400, 300, "player");
  }

  update(time: number, delta: number) {
    // Game loop (60fps)
    // delta = time since last frame in ms
  }
}
```

### Level 2: Scene Configuration with Data

```typescript
export class GameScene extends Phaser.Scene {
  constructor() {
    super({ key: "GameScene", active: false });
  }

  init(data: { level: number; score: number }) {
    // Receive data from previous scene
    this.level = data.level || 1;
    this.score = data.score || 0;
  }

  preload() {
    // Load level-specific assets
    this.load.image(`level${this.level}`, `assets/level${this.level}.png`);
  }

  create() {
    // Setup game objects
    this.createPlayer();
    this.createEnemies();
  }

  update(time: number, delta: number) {
    this.updatePlayer();
    this.updateEnemies();
  }
}
```

### Level 3: Game Config with Multiple Scenes

```typescript
const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: "game-container",
  backgroundColor: "#2d2d2d",
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
    width: 800,
    height: 600,
  },
  physics: {
    default: "arcade",
    arcade: {
      gravity: { x: 0, y: 1000 },
      debug: false,
    },
  },
  scene: [BootScene, PreloadScene, TitleScene, GameScene, UIScene],
  pipeline: { CustomPipeline: CustomPipeline },
};
```

### Level 4: Custom Game Config Extension

```typescript
interface ExtendedGameConfig extends Phaser.Types.Core.GameConfig {
  customSettings: {
    maxPlayers: number;
    gameMode: "deathmatch" | "capture";
  };
}

class CustomGame extends Phaser.Game {
  constructor(config: ExtendedGameConfig) {
    super(config);
    this.customSettings = config.customSettings;
  }
}
```

### Level 5: Scene Manager Control

```typescript
export class MainScene extends Phaser.Scene {
  create() {
    // Scene transitions
    this.scene.start("GameScene", { level: 1 });

    // Launch parallel scene (UI overlay)
    this.scene.launch("UIScene");

    // Pause current scene
    this.scene.pause();

    // Sleep scene (stops update but keeps rendering)
    this.scene.sleep("BackgroundScene");

    // Stop and remove scene
    this.scene.stop("OldScene");
  }
}
```

## Anti-Patterns

❌ **DON'T:**

- Load assets in `create()` - use `preload()`
- Create new objects in `update()` - causes GC pressure
- Use `this.scene.restart()` frequently - expensive operation
- Forget to call `super()` in scene constructor
- Use hardcoded screen dimensions - use scale manager
- Mix physics and non-physics objects without planning

✅ **DO:**

- Preload all assets in `preload()` before use
- Reuse objects with object pooling in `update()`
- Use scene data for passing values between scenes
- Clean up event listeners in `shutdown()` method
- Use `scale.manager` for responsive sizing
- Group related game objects with `this.add.group()`

## Code Patterns

### Scene Lifecycle Management

```typescript
export class GameScene extends Phaser.Scene {
  private player!: Phaser.Physics.Arcade.Sprite;
  private enemies!: Phaser.GameObjects.Group;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;

  constructor() {
    super({ key: "GameScene" });
  }

  create() {
    // Always setup shutdown for cleanup
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, this.shutdown, this);
  }

  shutdown() {
    // Clean up listeners
    this.input.keyboard!.off("keydown-ESC");
  }

  update(time: number, delta: number) {
    // Use delta for frame-independent movement
    const dt = delta / 1000; // Convert to seconds
  }
}
```

### Scale Manager Pattern

```typescript
const config: Phaser.Types.Core.GameConfig = {
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
    width: 800,
    height: 600,
  },
};

// In scene, get scale info
this.scale.width; // Actual canvas width
this.scale.height; // Actual canvas height
```

## Checklist

Before completing Phaser setup:

- [ ] Game config has proper scale settings
- [ ] Physics configured correctly (arcade or matter)
- [ ] Scene keys are unique
- [ ] Assets preloaded before use in create()
- [ ] Update loop is performant (no object creation)
- [ ] Shutdown handlers for cleanup
- [ ] Responsive scaling configured
- [ ] Scene transitions use proper data passing

## Common Issues

| Issue               | Solution                                 |
| ------------------- | ---------------------------------------- |
| Assets not loading  | Check `preload()` runs before `create()` |
| Physics not working | Verify physics config and body type      |
| Scene not updating  | Check scene is `active: true`            |
| Canvas size wrong   | Configure scale manager                  |
| Memory leaks        | Clean up in `shutdown()`                 |

## Reference

- [Phaser 3 Documentation](https://photonstorm.github.io/phaser3-docs/) — Official API docs
- [Phaser Examples](https://phaser.io/examples) — Code examples
- [Phaser TypeScript Types](https://github.com/photonstorm/phaser/tree/master/types) — Type definitions
