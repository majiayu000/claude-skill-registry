---
name: dev-phaser-scene-management
description: Scene transitions, data passing, and scene lifecycle management
---

# Phaser Scene Management

> "Orchestrating your game scenes with smooth transitions and data flow."

## Before/After: Manual Screen Management vs Phaser Scene System

### ❌ Before: Manual Screen Management

```typescript
// Manual scene management without Phaser
type ScreenType = 'title' | 'game' | 'pause' | 'gameover';
let currentScreen: ScreenType = 'title';

const screens: { [key in ScreenType]: HTMLElement } = {};

function showScreen(screen: ScreenType, data?: any) {
  // Hide current screen
  if (screens[currentScreen]) {
    screens[currentScreen].style.display = 'none';
  }

  // Show new screen
  if (!screens[screen]) {
    screens[screen] = document.getElementById(`screen-${screen}`)!;
  }
  screens[screen].style.display = 'block';

  // Manual data passing
  if (data && screen === 'game') {
    const levelElement = screens[screen].querySelector('.level')!;
    levelElement.textContent = data.level || '1';
  }

  // Manual cleanup
  if (currentScreen === 'game') {
    // Save game state manually
    saveGameState();
  }

  currentScreen = screen;
}

// Problems:
// - Manual DOM manipulation
// - No automatic lifecycle management
// - Data passing is manual
// - No transition effects built-in
// - Cleanup must be manual
// - No parallel scene support
```

### ✅ After: Phaser Scene System

```typescript
// Phaser handles scene lifecycle automatically
export class TitleScene extends Phaser.Scene {
  create() {
    // Start new scene - ONE line!
    // Data passed automatically, transition handled
    this.scene.start('GameScene', { level: 1, difficulty: 'normal' });
  }
}

export class GameScene extends Phaser.Scene {
  init(data: { level: number; difficulty: string }) {
    // Data received automatically in init()
    this.level = data.level || 1;
    this.difficulty = data.difficulty || 'normal';
  }

  create() {
    // Launch UI scene in parallel (not sequential)
    this.scene.launch('UIScene', { health: 100 });

    // Automatic cleanup on shutdown
    this.events.once('shutdown', () => {
      // Cleanup happens automatically
    });
  }

  pauseGame() {
    // Sleep game (keeps rendering), launch pause overlay
    this.scene.sleep('BackgroundScene');
    this.scene.launch('PauseScene');
  }

  levelComplete() {
    // Smooth fade transition - ONE line!
    this.cameras.main.fadeOut(300, 0, 0, 0);
    this.cameras.main.once('camerafadeoutcomplete', () => {
      this.scene.start('LevelCompleteScene', {
        level: this.level,
        score: this.score
      });
    });
  }
}

// Benefits:
// - Automatic lifecycle management (preload, create, update, shutdown)
// - Built-in data passing between scenes
// - Transition effects built-in
// - Parallel scene support (UI overlay)
// - Sleep/wake for background scenes
// - Automatic cleanup on shutdown
```

## When to Use This Skill

Use when:

- Managing multiple game scenes
- Passing data between scenes
- Implementing scene transitions
- Running parallel scenes (UI overlay)
- Pausing/resuming game state

## Quick Start

```typescript
// Start new scene
this.scene.start("GameScene", { level: 1, score: 0 });

// Launch scene in parallel
this.scene.launch("UIScene", { health: 100 });

// Sleep/scene (keeps rendering, stops update)
this.scene.sleep("BackgroundScene");
```

## Decision Framework

| Need                     | Use                |
| ------------------------ | ------------------ |
| Switch scenes            | `scene.start()`    |
| Parallel scene           | `scene.launch()`   |
| Pause scene              | `scene.pause()`    |
| Scene transition effects | Transition effects |
| Pass data to scene       | Data parameter     |

## Progressive Guide

### Level 1: Basic Scene Operations

```typescript
export class TitleScene extends Phaser.Scene {
  create() {
    // Start game scene
    this.input.on("pointerdown", () => {
      this.scene.start("GameScene", { difficulty: "normal" });
    });
  }
}

export class GameScene extends Phaser.Scene {
  private difficulty!: string;

  init(data: { difficulty: string }) {
    // Receive data from previous scene
    this.difficulty = data.difficulty || "normal";
  }

  create() {
    // Return to title
    this.events.on("shutdown", () => {
      console.log("Game scene shutting down");
    });

    this.input.keyboard!.on("keydown-ESC", () => {
      this.scene.start("TitleScene");
    });
  }
}
```

### Level 2: Scene Transitions with Data

```typescript
export class LevelSelectScene extends Phaser.Scene {
  selectLevel(level: number) {
    // Pass player progress to game scene
    const sceneData = {
      level: level,
      stars: this.getPlayerStars(level),
      unlocked: this.isLevelUnlocked(level),
    };

    // Fade transition
    this.cameras.main.fadeOut(300, 0, 0, 0);
    this.cameras.main.once("camerafadeoutcomplete", () => {
      this.scene.start("GameScene", sceneData);
    });
  }
}

export class GameScene extends Phaser.Scene {
  private level!: number;
  private stars!: number;
  private unlocked!: boolean;
  private score = 0;

  init(data: any) {
    this.level = data.level || 1;
    this.stars = data.stars || 0;
    this.unlocked = data.unlocked || true;
  }

  levelComplete() {
    // Return to level select with updated data
    const returnData = {
      level: this.level,
      stars: this.calculateStars(),
      score: this.score,
    };

    this.scene.start("LevelSelectScene", returnData);
  }
}
```

### Level 3: Parallel Scenes (UI Overlay)

```typescript
export class GameScene extends Phaser.Scene {
  create() {
    // Launch UI scene on top
    this.scene.launch("UIScene", { maxHealth: 100 });

    // Get reference to UI scene
    const uiScene = this.scene.get("UIScene") as UIScene;

    // Listen for UI events
    this.scene.get("UIScene").events.on("pause", () => {
      this.scene.pause();
    });

    this.scene.get("UIScene").events.on("resume", () => {
      this.scene.resume();
    });
  }

  update() {
    // Update UI with game data
    const uiScene = this.scene.get("UIScene") as UIScene;
    uiScene.updateHealth(this.player.health);
    uiScene.updateScore(this.score);
  }
}

export class UIScene extends Phaser.Scene {
  private healthBar!: Phaser.GameObjects.Graphics;
  private scoreText!: Phaser.GameObjects.Text;

  create(data: { maxHealth: number }) {
    // Create persistent UI elements
    this.healthBar = this.add.graphics();
    this.scoreText = this.add.text(16, 16, "Score: 0");

    // Pause button
    const pauseBtn = this.add.text(this.scale.width - 80, 16, "Pause");
    pauseBtn.setInteractive();
    pauseBtn.on("pointerdown", () => {
      this.events.emit("pause");
    });

    // Prevent UI scene from receiving pointer events first
    this.scene.bringToTop();
  }

  updateHealth(current: number) {
    this.healthBar.clear();
    this.healthBar.fillStyle(0x00ff00);
    this.healthBar.fillRect(16, 50, current * 2, 20);
  }

  updateScore(score: number) {
    this.scoreText.setText(`Score: ${score}`);
  }
}
```

### Level 4: Scene Sleep and Wake

```typescript
export class BackgroundScene extends Phaser.Scene {
  private stars!: Phaser.GameObjects.Group;

  create() {
    this.stars = this.add.group();

    for (let i = 0; i < 100; i++) {
      const star = this.add.image(
        Phaser.Math.Between(0, this.scale.width),
        Phaser.Math.Between(0, this.scale.height),
        "star",
      );
      star.setScrollFactor(0.1);
      this.stars.add(star);
    }

    // Listen for sleep/wake
    this.events.on("sleep", () => {
      console.log("Background scene paused");
    });

    this.events.on("wake", () => {
      console.log("Background scene resumed");
    });
  }

  update() {
    // Parallax scrolling
    this.stars.children.entries.forEach((star: any) => {
      star.x -= 0.5;
      if (star.x < -10) star.x = this.scale.width + 10;
    });
  }
}

export class PauseScene extends Phaser.Scene {
  create() {
    // Sleep the game scene (keeps rendering)
    this.scene.sleep("GameScene");

    // Create pause menu
    const overlay = this.add.rectangle(
      this.scale.width / 2,
      this.scale.height / 2,
      this.scale.width,
      this.scale.height,
      0x000000,
      0.5,
    );

    const resumeBtn = this.add.text(this.scale.width / 2, 300, "Resume");
    resumeBtn.setOrigin(0.5);
    resumeBtn.setInteractive();
    resumeBtn.on("pointerdown", () => {
      this.scene.stop();
      this.scene.wake("GameScene");
    });

    const quitBtn = this.add.text(this.scale.width / 2, 350, "Quit");
    quitBtn.setOrigin(0.5);
    quitBtn.setInteractive();
    quitBtn.on("pointerdown", () => {
      this.scene.stop("GameScene");
      this.scene.stop();
      this.scene.start("TitleScene");
    });
  }
}
```

### Level 5: Advanced Scene Manager

```typescript
class SceneManager {
  private scene: Phaser.Scene;
  private sceneData = new Map<string, any>();

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
  }

  // Transition with data persistence
  transition(targetKey: string, data?: any, transition?: string) {
    // Save current scene data
    this.sceneData.set(this.scene.scene.key, this.getCurrentSceneData());

    // Merge new data
    const combinedData = {
      ...this.sceneData.get(targetKey),
      ...data,
    };

    // Apply transition effect
    if (transition === "fade") {
      this.fadeTransition(targetKey, combinedData);
    } else if (transition === "slide") {
      this.slideTransition(targetKey, combinedData);
    } else {
      this.scene.scene.start(targetKey, combinedData);
    }
  }

  private fadeTransition(targetKey: string, data: any) {
    const camera = this.scene.cameras.main;
    camera.fadeOut(300, 0, 0, 0);

    camera.once("camerafadeoutcomplete", () => {
      this.scene.scene.start(targetKey, data);
    });
  }

  private slideTransition(targetKey: string, data: any) {
    const width = this.scene.scale.width;
    const camera = this.scene.cameras.main;

    // Slide out effect
    this.scene.tweens.add({
      targets: camera,
      x: -width,
      duration: 300,
      onComplete: () => {
        camera.x = width;
        this.scene.scene.start(targetKey, data);

        // Slide in new scene (handled by new scene)
      },
    });
  }

  private getCurrentSceneData(): any {
    return {
      // Extract relevant data from current scene
      score: (this.scene as any).score || 0,
      health: (this.scene as any).player?.health || 100,
    };
  }

  // Launch overlay scene
  launchOverlay(overlayKey: string, data?: any) {
    this.scene.scene.launch(overlayKey, data);
    this.scene.scene.pause();
  }

  // Close overlay and resume
  closeOverlay(overlayKey: string, returnData?: any) {
    this.scene.scene.stop(overlayKey);
    this.scene.scene.resume();

    if (returnData) {
      this.handleOverlayData(returnData);
    }
  }

  private handleOverlayData(data: any) {
    // Process data returned from overlay
    if (data.action === "quit") {
      this.transition("TitleScene");
    }
  }
}

// Usage in scene
export class GameScene extends Phaser.Scene {
  private sceneManager!: SceneManager;

  create() {
    this.sceneManager = new SceneManager(this);
  }

  pauseGame() {
    this.sceneManager.launchOverlay("PauseScene", {
      score: this.score,
      level: this.level,
    });
  }

  levelComplete() {
    this.sceneManager.transition(
      "LevelCompleteScene",
      { score: this.score, stars: 3 },
      "fade",
    );
  }
}
```

## Anti-Patterns

❌ **DON'T:**

- Use `start()` when you need `launch()` for UI
- Forget to handle scene shutdown cleanup
- Pass circular references in scene data
- Use `restart()` frequently - expensive
- Stop scenes before retrieving data
- Mix scene keys as strings (use constants)

✅ **DO:**

- Use `launch()` for parallel UI scenes
- Clean up in shutdown event handler
- Keep scene data serializable
- Use scene manager for complex flows
- Retrieve data before stopping scenes
- Define scene key constants

## Code Patterns

### Scene Key Constants

```typescript
// constants.ts
export const SCENE_KEYS = {
  BOOT: "BootScene",
  PRELOAD: "PreloadScene",
  TITLE: "TitleScene",
  GAME: "GameScene",
  UI: "UIScene",
  PAUSE: "PauseScene",
} as const;

// Usage
this.scene.start(SCENE_KEYS.GAME, { level: 1 });
```

### Global Scene Manager

```typescript
// game.ts
const config: Phaser.Types.Core.GameConfig = {
  scene: [BootScene, PreloadScene, TitleScene, GameScene, UIScene],
  // ...
};

// Access from any scene
const gameScene = this.scene.get(SCENE_KEYS.GAME);
```

## Scene Methods Reference

| Method              | Description                   | Data Passed |
| ------------------- | ----------------------------- | ----------- |
| `start(key, data)`  | Switch to scene, stop current | Yes         |
| `launch(key, data)` | Start scene in parallel       | Yes         |
| `sleep(key)`        | Pause scene updates           | No          |
| `wake(key, data)`   | Resume sleeping scene         | Optional    |
| `stop(key, data)`   | Stop and remove scene         | Optional    |
| `pause()`           | Pause current scene           | No          |
| `resume()`          | Resume current scene          | No          |
| `get(key)`          | Get scene reference           | No          |

## Checklist

- [ ] Scene keys defined as constants
- [ ] Data passed in init() method
- [ ] Shutdown handlers for cleanup
- [ ] Parallel scenes use launch()
- [ ] Transition effects complete before scene switch
- [ ] Scene manager for complex flows
- [ ] Global state managed properly

## Reference

- [Scene Manager](https://photonstorm.github.io/phaser3-docs/Phaser.Scenes.SceneManager.html) — Scene API
- [Scene Plugin](https://photonstorm.github.io/phaser3-docs/Phaser.Scenes.ScenePlugin.html) — Scene operations
