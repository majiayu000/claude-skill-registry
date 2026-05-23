---
name: ta-phaser-camera-work
description: Implements camera controls, bounds, and follow behavior. Use proactively when setting up camera controls, camera bounds, or follow behavior.
category: techartist
---

# Phaser Camera Work

> "Cinematic camera controls that enhance gameplay and storytelling."

## When to Use This Skill

Use when:

- Setting up camera follow behavior
- Implementing camera bounds
- Creating cinematic sequences
- Building camera transitions
- Adding visual polish with camera

## Quick Start

```typescript
// Smooth follow
this.cameras.main.startFollow(this.player, true, 0.08, 0.08);

// Camera bounds
this.cameras.main.setBounds(0, 0, 2000, 2000);
```

## Decision Framework

| Need            | Use                       |
| --------------- | ------------------------- |
| Player tracking | `startFollow()` with lerp |
| Confined area   | `setBounds()`             |
| Cinematic pan   | `pan()` tween             |
| Zoom effect     | Camera zoom tween         |
| Letterboxing    | Custom camera for UI      |

## Progressive Guide

### Level 1: Basic Camera Setup

```typescript
export class GameScene extends Phaser.Scene {
  create() {
    // Get reference
    const camera = this.cameras.main;

    // Set background color
    camera.setBackgroundColor("#2d2d2d");

    // Set bounds (world limits)
    camera.setBounds(0, 0, 2000, 1500);

    // Follow player
    camera.startFollow(this.player, true, 0.1, 0.1);

    // Set zoom
    camera.setZoom(1.5);

    // Center camera on spawn
    camera.centerOn(this.player.x, this.player.y);
  }
}
```

### Level 2: Camera Follow Behaviors

```typescript
export class GameScene extends Phaser.Scene {
  create() {
    // Tight follow (no lag)
    this.cameras.main.startFollow(this.player, true, 1, 1);

    // Loose follow (smooth lag)
    this.cameras.main.startFollow(this.player, true, 0.05, 0.05);

    // Horizontal only (side-scroller)
    this.cameras.main.startFollow(this.player, true, 0.1, 0);

    // Locked Y, free X
    this.cameras.main.startFollow(this.player, true, 0, 0.1);

    // With deadzone (player can move without camera moving)
    this.cameras.main.startFollow(this.player, true, 0.08, 0.08);
    this.cameras.main.setDeadzone(
      this.scale.width * 0.3,
      this.scale.height * 0.3,
    );
  }
}
```

### Level 3: Cinematic Camera Moves

```typescript
export class CutsceneScene extends Phaser.Scene {
  create() {
    // Pan to location
    const panToLocation = (x: number, y: number, duration = 2000) => {
      this.tweens.add({
        targets: this.cameras.main,
        x: x,
        y: y,
        duration: duration,
        ease: "Power2.easeInOut",
      });
    };

    // Zoom in on object
    const focusOn = (target: Phaser.GameObjects.Sprite, duration = 1000) => {
      this.tweens.add({
        targets: this.cameras.main,
        x: target.x,
        y: target.y,
        zoom: 2,
        duration: duration,
        ease: "Power2.easeInOut",
      });
    };

    // Dramatic reveal
    const dramaticReveal = () => {
      const camera = this.cameras.main;

      // Start zoomed in
      camera.setZoom(3);
      camera.centerOn(this.boss.x, this.boss.y);

      // Zoom out to show arena
      this.tweens.add({
        targets: camera,
        zoom: 1,
        x: this.arenaCenter.x,
        y: this.arenaCenter.y,
        duration: 2000,
        ease: "Cubic.easeOut",
      });
    };

    // Tracking shot
    const trackingShot = (path: Phaser.Curves.Path, duration = 3000) => {
      this.tweens.add({
        targets: this.cameras.main,
        x: path.points[0].x,
        y: path.points[0].y,
        duration: duration,
        ease: "Linear",
        onUpdate: (tween: any) => {
          const progress = tween.progress;
          const point = path.getPoint(progress);
          this.cameras.main.centerOn(point.x, point.y);
        },
      });
    };
  }
}
```

### Level 4: Multi-Camera Setups

```typescript
export class GameScene extends Phaser.Scene {
  private gameCamera!: Phaser.Cameras.Scene2D.Camera;
  private uiCamera!: Phaser.Cameras.Scene2D.Camera;
  private minimapCamera!: Phaser.Cameras.Scene2D.Camera;

  create() {
    // Main game camera
    this.gameCamera = this.cameras.main;
    this.gameCamera.setName("game");
    this.gameCamera.setBounds(0, 0, 2000, 2000);
    this.gameCamera.startFollow(this.player);

    // UI camera (fixed, no scroll)
    this.uiCamera = this.cameras.add(0, 0, this.scale.width, this.scale.height);
    this.uiCamera.setName("ui");
    this.uiCamera.setScrollFactor(0);
    this.uiCamera.setBackgroundColor("rgba(0,0,0,0)");
    this.uiCamera.setZoom(1);

    // Minimap camera
    this.minimapCamera = this.cameras.add(this.scale.width - 220, 20, 200, 200);
    this.minimapCamera.setName("minimap");
    this.minimapCamera.setBounds(0, 0, 2000, 2000);
    this.minimapCamera.setZoom(0.1);

    // Minimap border
    this.add
      .rectangle(this.scale.width - 120, 120, 204, 204, 0xffffff)
      .setStrokeStyle(2, 0x000000)
      .setScrollFactor(0);

    // Add objects to specific cameras
    this.player.name = "player";

    // Minimap doesn't show everything
    this.minimapCamera.ignore(this.someObjects);
  }
}
```

### Level 5: Advanced Camera Controller

```typescript
class CameraController {
  private states = new Map<string, CameraState>();
  private currentState: string = "default";
  private tween?: Phaser.Tweens.Tween;

  constructor(private camera: Phaser.Cameras.Scene2D.Camera) {
    this.setupStates();
  }

  private setupStates() {
    // Default follow state
    this.states.set("default", {
      follow: null,
      lerp: 0.08,
      zoom: 1,
      deadzone: { x: 0.3, y: 0.3 },
    });

    // Combat state
    this.states.set("combat", {
      follow: null,
      lerp: 0.12,
      zoom: 1.1,
      deadzone: { x: 0.2, y: 0.2 },
    });

    // Sprint state
    this.states.set("sprint", {
      follow: null,
      lerp: 0.15,
      zoom: 1.2,
      deadzone: { x: 0.1, y: 0.1 },
    });

    // Cinematic state
    this.states.set("cinematic", {
      follow: null,
      lerp: 1,
      zoom: 1,
      deadzone: { x: 0, y: 0 },
    });
  }

  setState(stateName: string, duration = 500) {
    const state = this.states.get(stateName);
    if (!state || stateName === this.currentState) return;

    this.currentState = stateName;

    // Kill existing tween
    if (this.tween) {
      this.tween.destroy();
    }

    // Transition to new state
    this.tween = this.camera.scene.tweens.add({
      targets: this.camera,
      zoom: state.zoom,
      duration: duration,
      ease: "Power2.easeOut",
      onUpdate: () => {
        this.camera.setLerp(state.lerp, state.lerp);
        if (state.deadzone) {
          const w = this.camera.width * state.deadzone.x;
          const h = this.camera.height * state.deadzone.y;
          this.camera.setDeadzone(w, h);
        }
      },
    });
  }

  setFollowTarget(target: Phaser.GameObjects.GameObject) {
    this.camera.startFollow(target, true, 0.08, 0.08);
  }

  lookAt(
    target: Phaser.Math.Vector2 | Phaser.GameObjects.GameObject,
    duration = 500,
  ) {
    const x =
      target instanceof Phaser.GameObjects.GameObject ? target.x : target.x;
    const y =
      target instanceof Phaser.GameObjects.GameObject ? target.y : target.y;

    this.tween = this.camera.scene.tweens.add({
      targets: this.camera,
      x: x,
      y: y,
      duration: duration,
      ease: "Power2.easeInOut",
    });
  }

  // Camera shake with decay
  shake(intensity: number, duration: number) {
    const startTime = Date.now();

    const update = () => {
      const elapsed = Date.now() - startTime;
      if (elapsed >= duration) {
        this.camera.resetFX();
        return;
      }

      const progress = elapsed / duration;
      const currentIntensity = intensity * (1 - progress);

      this.camera.shake(16, currentIntensity);

      this.camera.scene.time.delayedCall(16, update);
    };

    update();
  }

  // Smooth zoom to target
  zoomTo(targetZoom: number, duration = 500) {
    this.tween = this.camera.scene.tweens.add({
      targets: this.camera,
      zoom: targetZoom,
      duration: duration,
      ease: "Power2.easeOut",
    });
  }
}
```

## Camera Methods Reference

| Method                  | Parameters                    | Description           |
| ----------------------- | ----------------------------- | --------------------- |
| `startFollow(target)`   | target, roundPx, lerpX, lerpY | Follow game object    |
| `stopFollow()`          | -                             | Stop following        |
| `setZoom(level)`        | number                        | Set zoom level        |
| `setBounds(x, y, w, h)` | bounds                        | Set world bounds      |
| `setDeadzone(w, h)`     | size                          | Set no-move zone      |
| `pan(x, y, duration)`   | position, ms                  | Pan to position       |
| `setLerp(lerpX, lerpY)` | 0-1 values                    | Set follow smoothness |
| `setScrollFactor(x, y)` | 0-1 values                    | Set parallax          |
| `centerOn(x, y)`        | position                      | Center camera         |
| `ignore(objs)`          | array                         | Don't render objects  |

## Anti-Patterns

❌ **DON'T:**

- Set lerp too high (jittery) or too low (laggy)
- Forget camera bounds for open worlds
- Use zoom without considering gameplay impact
- Mix coordinate systems when panning
  | Ignore camera in multi-camera setups
  | Change camera during player input

✅ **DO:**
| Tune lerp for game feel
| Set bounds for world limits
| Test gameplay at different zoom levels
| Use consistent coordinate systems
| Name cameras for debugging
| Change camera between gameplay segments

## Camera Effect Presets

```typescript
const CAMERA_PRESETS = {
  // Platformer
  platformer: {
    followLerp: 0.08,
    zoom: 1,
    deadzone: { x: 0.3, y: 0.4 },
  },

  // Top-down action
  topdown: {
    followLerp: 0.1,
    zoom: 1.2,
    deadzone: { x: 0.2, y: 0.2 },
  },

  // Bullet hell
  bullethell: {
    followLerp: 0.05,
    zoom: 1,
    deadzone: { x: 0.1, y: 0.1 },
  },

  // Cinematic
  cinematic: {
    followLerp: 0.03,
    zoom: 1,
    deadzone: { x: 0.05, y: 0.05 },
  },
};
```

## Checklist

- [ ] Camera follow tuned for game feel
- [ ] World bounds set correctly
- [ ] Deadzone configured
- [ ] Multi-camera setup working
- [ ] Lerp values appropriate
- [ ] Camera effects don't break gameplay
- [ ] Minimap (if used) updating correctly

## Reference

- [Camera API](https://photonstorm.github.io/phaser3-docs/Phaser.Cameras.Scene2D.Camera.html) — Camera docs
- [Camera Manager](https://photonstorm.github.io/phaser3-docs/Phaser.Cameras.CameraManager.html) — Manager API
