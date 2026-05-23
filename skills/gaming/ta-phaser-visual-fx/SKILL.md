---
name: ta-phaser-visual-fx
description: Adds post-processing and camera effects to Phaser games. Use proactively when implementing visual polish, camera effects, or post-processing.
category: techartist
---

# Phaser Visual FX

> "Add visual polish with camera effects, post-processing, and visual feedback."

## When to Use This Skill

Use when:

- Adding screen shake effects
- Implementing camera transitions
- Creating flash/fade effects
- Building visual feedback systems
- Adding post-processing effects

## Quick Start

```typescript
// Screen shake
this.cameras.main.shake(200, 0.01);

// Flash effect
this.cameras.main.flash(200, 255, 255, 255);

// Fade effect
this.cameras.main.fadeOut(300);
```

## Decision Framework

| Need              | Use                |
| ----------------- | ------------------ |
| Impact feedback   | Screen shake       |
| Scene transition  | Fade effect        |
| Damage indication | Red flash          |
| Hit confirmation  | Camera zoom        |
| Ambiance          | Tint/color grading |

## Progressive Guide

### Level 1: Basic Camera Effects

```typescript
export class GameScene extends Phaser.Scene {
  create() {
    // Screen shake
    const shakeEffect = (duration: number, intensity: number) => {
      this.cameras.main.shake(duration, intensity);
    };

    // Flash effect
    const flashEffect = (duration: number, color = 0xffffff) => {
      this.cameras.main.flash(duration, color);
    };

    // Fade effect
    const fadeOut = (duration: number) => {
      this.cameras.main.fadeOut(duration, 0, 0, 0);
    };

    const fadeIn = (duration: number) => {
      this.cameras.main.fadeIn(duration, 0, 0, 0);
    };

    // Usage examples
    this.input.on("pointerdown", () => {
      shakeEffect(200, 0.01);
    });
  }
}
```

### Level 2: Visual Feedback Systems

```typescript
export class GameScene extends Phaser.Scene {
  private cameraEffects!: CameraEffects;

  create() {
    this.cameraEffects = new CameraEffects(this);

    // Player hit feedback
    this.events.on("player-hit", (damage: number) => {
      this.cameraEffects.hitImpact(damage);
    });

    // Enemy death feedback
    this.events.on("enemy-death", (position: Phaser.Math.Vector2) => {
      this.cameraEffects.deathImpact(position);
    });

    // Level complete celebration
    this.events.on("level-complete", () => {
      this.cameraEffects.celebrate();
    });
  }
}

class CameraEffects {
  private mainCamera: Phaser.Cameras.Scene2D.Camera;

  constructor(private scene: Phaser.Scene) {
    this.mainCamera = scene.cameras.main;
  }

  hitImpact(damage: number) {
    // Red flash based on damage
    const intensity = Math.min(damage / 100, 1);
    this.mainCamera.flash(
      100,
      255,
      0,
      0,
      false,
      (camera: any, progress: number) => {
        return 1 - progress * intensity;
      },
    );

    // Screen shake
    this.mainCamera.shake(150, 0.005 + intensity * 0.01);
  }

  deathImpact(position: Phaser.Math.Vector2) {
    // Shake toward the position
    this.mainCamera.shake(200, 0.01);
  }

  celebrate() {
    // Zoom in/out pulse
    this.scene.tweens.add({
      targets: this.mainCamera,
      zoom: 1.1,
      duration: 200,
      yoyo: true,
      ease: "Sine.easeInOut",
    });

    // Confetti flash
    this.mainCamera.flash(500, 255, 255, 200);
  }
}
```

### Level 3: Advanced Camera Work

```typescript
export class GameScene extends Phaser.Scene {
  create() {
    // Camera follow with smoothing
    this.cameras.main.startFollow(this.player, true, 0.1, 0.1);

    // Set camera bounds
    this.cameras.main.setBounds(
      0,
      0,
      this.map.widthInPixels,
      this.map.heightInPixels,
    );

    // Camera deadzone (player can move without camera moving)
    this.cameras.main.setDeadzone(
      this.scale.width * 0.3,
      this.scale.height * 0.3,
    );

    // Dynamic zoom
    const zoomOnSprint = () => {
      this.tweens.add({
        targets: this.cameras.main,
        zoom: 1.2,
        duration: 200,
        ease: "Power2",
      });
    };

    const zoomNormal = () => {
      this.tweens.add({
        targets: this.cameras.main,
        zoom: 1,
        duration: 200,
        ease: "Power2",
      });
    };
  }
}
```

### Level 4: Post-Processing Pipeline

```typescript
export class GameScene extends Phaser.Scene {
  create() {
    // Custom post-processing pipeline
    const pipeline = this.cameras.main.setPostPipeline(CustomPipeline);

    // Adjust pipeline properties
    pipeline.setFloat2("resolution", this.scale.width, this.scale.height);
    pipeline.setFloat1("time", 0);

    // Animate shader time
    this.events.on("update", () => {
      pipeline.setFloat1("time", this.time.now / 1000);
    });
  }
}

// Custom pipeline shader
class CustomPipeline extends Phaser.Renderer.WebGL.Pipelines.PostFXPipeline {
  constructor(game: Phaser.Game) {
    super({
      game: game,
      renderTarget: true,
      fragShader: `
        precision mediump float;
        uniform sampler2D uMainSampler;
        uniform vec2 uResolution;
        uniform float uTime;
        varying vec2 outTexCoord;

        void main() {
          vec2 uv = outTexCoord;

          // Scanline effect
          float scanline = sin(uv.y * uResolution.y * 0.5 + uTime * 5.0) * 0.02;

          // Vignette
          vec2 center = uv - 0.5;
          float vignette = 1.0 - dot(center, center) * 0.5;

          // Sample and apply effects
          vec4 color = texture2D(uMainSampler, uv);
          color.rgb -= scanline;
          color.rgb *= vignette;

          gl_FragColor = color;
        }
      `,
    });
  }
}
```

### Level 5: Visual FX Manager

```typescript
class VisualFXManager {
  private effects = new Map<string, () => void>();

  constructor(private scene: Phaser.Scene) {
    this.setupBuiltInEffects();
  }

  private setupBuiltInEffects() {
    // Hit effect
    this.effects.set("hit-light", () => {
      this.scene.cameras.main.shake(100, 0.005);
      this.scene.cameras.main.flash(50, 255, 100, 100);
    });

    this.effects.set("hit-heavy", () => {
      this.scene.cameras.main.shake(300, 0.02);
      this.scene.cameras.main.flash(200, 255, 0, 0);

      // Slow motion
      this.scene.time.timeScale = 0.5;
      this.scene.time.delayedCall(500, () => {
        this.scene.time.timeScale = 1;
      });
    });

    // Power-up effect
    this.effects.set("powerup", () => {
      const camera = this.scene.cameras.main;

      // Zoom burst
      this.scene.tweens.add({
        targets: camera,
        zoom: 1.3,
        duration: 100,
        yoyo: true,
        ease: "Back.easeOut",
      });

      // Color flash
      camera.flash(300, 100, 255, 255);
    });

    // Explosion effect
    this.effects.set("explosion", (x: number, y: number) => {
      const camera = this.scene.cameras.main;

      // Calculate intensity based on distance
      const distance = Phaser.Math.Distance.Between(
        camera.midPoint.x,
        camera.midPoint.y,
        x,
        y,
      );
      const intensity = Math.max(0.01, 0.1 - distance / 2000);

      camera.shake(300, intensity);
      camera.flash(200, 255, 200, 100);
    });

    // UI popup effect
    this.effects.set("popup", (target: Phaser.GameObjects.Container) => {
      this.scene.tweens.add({
        targets: target,
        scale: 1.1,
        duration: 100,
        yoyo: true,
        ease: "Back.easeOut",
      });
    });
  }

  play(effectName: string, ...args: any[]) {
    const effect = this.effects.get(effectName);
    if (effect) {
      effect.apply(this, args);
    }
  }

  // Create custom effect
  register(name: string, effect: Function) {
    this.effects.set(name, effect);
  }
}
```

## Anti-Patterns

❌ **DON'T:**

- Overuse camera shake (dizzying)
- Chain too many effects at once
- Use long fade durations (feels slow)
- Forget to reset time scale
- Apply effects to wrong camera
- Ignore camera bounds during effects

✅ **DO:**

- Keep effects short and punchy
- Layer effects carefully
- Use appropriate duration for action
- Always reset time scale
- Target specific cameras
- Maintain camera bounds

## Visual FX Guidelines

| Effect     | Duration  | Intensity      | Use Case      |
| ---------- | --------- | -------------- | ------------- |
| Light Hit  | 50-150ms  | Low            | Small damage  |
| Heavy Hit  | 200-400ms | High           | Big damage    |
| Explosion  | 200-500ms | Distance-based | Explosions    |
| Power-up   | 100-300ms | Medium         | Collectibles  |
| Death      | 300-800ms | High           | Player death  |
| Pickup     | 100-200ms | Low            | Items         |
| Transition | 300-600ms | N/A            | Scene changes |

## Code Patterns

### Camera Follow with Lerp

```typescript
// Smooth follow with custom lerp
this.cameras.main.startFollow(this.player, true, 0.08, 0.08);
```

### Multi-Camera Setup

```typescript
create() {
  // Main game camera
  const mainCam = this.cameras.main;
  mainCam.setName('game');
  mainCam.startFollow(this.player);

  // UI camera (fixed)
  const uiCam = this.cameras.add(0, 0, this.scale.width, this.scale.height);
  uiCam.setName('ui');
  uiCam.setScrollFactor(0);
  uiCam.setZoom(1);
}
```

### Screen Effects Combination

```typescript
// Dramatic entrance
const dramaticEntrance = () => {
  // Start black
  this.cameras.main.setBackgroundColor("#000000");

  // Zoom in while fading in
  this.cameras.main.setZoom(0.5);
  this.cameras.main.fadeIn(1000);

  this.tweens.add({
    targets: this.cameras.main,
    zoom: 1,
    duration: 1000,
    ease: "Power2.easeOut",
  });
};
```

## Camera Methods Reference

| Method                       | Description             |
| ---------------------------- | ----------------------- |
| `shake(duration, intensity)` | Shake the camera        |
| `flash(duration, r, g, b)`   | Flash screen color      |
| `fadeOut(duration, r, g, b)` | Fade to black           |
| `fadeIn(duration, r, g, b)`  | Fade from black         |
| `setZoom(level)`             | Set camera zoom         |
| `startFollow(target)`        | Follow game object      |
| `setDeadzone(w, h)`          | Set no-move zone        |
| `setBounds(x, y, w, h)`      | Set camera limits       |
| `pan(x, y, duration)`        | Move camera to position |
| `setScrollFactor(x, y)`      | Set parallax factor     |

## Checklist

- [ ] Effects have appropriate duration
- [ ] Camera bounds maintained
- [ ] Time scale reset after slow-mo
- [ ] Effects don't interfere with gameplay
- [ ] Multiple cameras handled correctly
- [ ] Effects are readable on screen
- [ ] Performance considered (many effects)

## Reference

- [Camera API](https://photonstorm.github.io/phaser3-docs/Phaser.Cameras.Scene2D.Camera.html) — Camera docs
- [PostFX Pipeline](https://photonstorm.github.io/phaser3-docs/Phaser.Renderer.WebGL.Pipelines.PostFXPipeline.html) — Post-processing
