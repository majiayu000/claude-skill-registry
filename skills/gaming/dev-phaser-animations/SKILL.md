---
name: dev-phaser-animations
description: Sprite animations, tweens, animation chains, and timeline sequences
---

# Phaser Animations

> "Bring your sprites to life with smooth animations and tweens."

## Before/After: Manual Animation vs Phaser Animation System

### ❌ Before: Manual Frame Animation

```typescript
// Manual sprite animation without Phaser
class SpriteAnimator {
  private currentFrame = 0;
  private frameTimer = 0;
  private frameDuration = 83; // ~12 FPS
  private isPlaying = false;
  private frames: HTMLImageElement[] = [];

  constructor(private sprite: HTMLElement) {
    // Load all frames manually
    for (let i = 0; i < 8; i++) {
      const img = document.createElement('img');
      img.src = `assets/walk/frame${i}.png`;
      this.frames.push(img);
    }
  }

  play(animationName: string) {
    this.isPlaying = true;
    this.currentFrame = 0;
  }

  update(dt: number) {
    if (!this.isPlaying) return;

    this.frameTimer += dt;

    if (this.frameTimer >= this.frameDuration) {
      this.frameTimer = 0;
      this.currentFrame = (this.currentFrame + 1) % this.frames.length;
      this.sprite.style.backgroundImage = `url(${this.frames[this.currentFrame].src})`;
    }
  }

  // Manual tween for position
  moveTo(targetX: number, targetY: number, duration: number) {
    const startX = parseFloat(this.sprite.style.left) || 0;
    const startY = parseFloat(this.sprite.style.top) || 0;
    const startTime = performance.now();

    const animate = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Linear interpolation only - no easing options
      this.sprite.style.left = (startX + (targetX - startX) * progress) + 'px';
      this.sprite.style.top = (startY + (targetY - startY) * progress) + 'px';

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    requestAnimationFrame(animate);
  }
}

// Problems:
// - Manual frame timing is error-prone
// - No built-in easing functions
// - Manual sprite sheet management
// - No animation state management
// - Chained animations require nested callbacks
// - No timeline support
```

### ✅ After: Phaser Animation System

```typescript
// Phaser handles all animation automatically
export class GameScene extends Phaser.Scene {
  create() {
    const player = this.add.sprite(400, 300, 'player');

    // Create sprite sheet animation - ONE config!
    this.anims.create({
      key: 'walk',
      frames: this.anims.generateFrameNumbers('player', {
        start: 0,
        end: 7
      }),
      frameRate: 12,
      repeat: -1 // Infinite loop
    });

    // Play animation - ONE line!
    player.play('walk');

    // Tween with easing - ONE call!
    this.tweens.add({
      targets: player,
      x: 600,
      y: 400,
      duration: 1000,
      ease: 'Power2', // Built-in easing!
      onComplete: () => {
        console.log('Movement complete!');
      }
    });

    // Timeline for sequences - ONE config!
    this.tweens.timeline({
      targets: player,
      tweens: [
        { alpha: 0, duration: 500, ease: 'Linear' },
        { x: 200, duration: 500, offset: '-=250' }, // Overlap!
        { scale: 2, duration: 300, ease: 'Back.easeOut' }
      ]
    });
  }
}

// Benefits:
// - Automatic frame timing
// - 20+ built-in easing functions
// - Sprite sheet generation helpers
// - Animation state management (isPlaying, currentAnim)
// - Timeline support for complex sequences
// - Event callbacks (onComplete, animationcomplete)
```

## When to Use This Skill

Use when:

- Creating sprite animations
- Building tween sequences
- Implementing timeline-based animations
- Animating UI elements
- Creating visual effects and transitions

## Quick Start

```typescript
create() {
  // Create animation from sprite sheet
  this.anims.create({
    key: 'walk',
    frames: this.anims.generateFrameNumbers('player', { start: 0, end: 7 }),
    frameRate: 12,
    repeat: -1
  });

  // Play animation
  const player = this.add.sprite(400, 300, 'player');
  player.play('walk');
}
```

## Decision Framework

| Need                  | Use                                |
| --------------------- | ---------------------------------- |
| Frame-based animation | `anims.create()` + `sprite.play()` |
| Property animation    | `tweens.add()`                     |
| Sequenced animations  | `timeline`                         |
| Single tween          | `tweens.add()` once                |
| Delayed action        | `time.delayedCall()`               |

## Progressive Guide

### Level 1: Sprite Animations

```typescript
export class GameScene extends Phaser.Scene {
  create() {
    // Create animations from sprite sheet
    this.anims.create({
      key: "idle",
      frames: this.anims.generateFrameNumbers("player", {
        start: 0,
        end: 3,
      }),
      frameRate: 8,
      repeat: -1, // Infinite loop
      yoyo: false, // Don't play backwards
    });

    this.anims.create({
      key: "walk",
      frames: this.anims.generateFrameNumbers("player", {
        start: 4,
        end: 11,
      }),
      frameRate: 12,
      repeat: -1,
    });

    this.anims.create({
      key: "attack",
      frames: this.anims.generateFrameNumbers("player", {
        start: 12,
        end: 17,
      }),
      frameRate: 15,
      repeat: 0, // Play once
    });

    // Create sprite and play animation
    const player = this.add.sprite(400, 300, "player");
    player.play("idle");

    // Change animation
    player.play("walk", true); // true = ignore if playing
  }
}
```

### Level 2: Tweening Properties

```typescript
create() {
  const box = this.add.rectangle(400, 300, 50, 50, 0xff0000);

  // Basic tween
  this.tweens.add({
    targets: box,
    x: 600,
    duration: 1000,
    ease: 'Power2'
  });

  // Multiple properties
  this.tweens.add({
    targets: box,
    x: 200,
    y: 400,
    alpha: 0.5,
    angle: 180,
    scale: 2,
    duration: 2000,
    ease: 'Elastic.easeOut',
    onComplete: () => {
      console.log('Tween complete!');
    }
  });

  // Yoyo tween (ping-pong)
  this.tweens.add({
    targets: box,
    y: 100,
    duration: 1000,
    yoyo: true,
    repeat: -1
  });
}
```

### Level 3: Tween Chains and Callbacks

```typescript
create() {
  const sprite = this.add.sprite(400, 300, 'player');

  // Chain tweens
  this.tweens.add({
    targets: sprite,
    y: 200,
    duration: 500,
    ease: 'Linear',
    onComplete: () => {
      // Second tween
      this.tweens.add({
        targets: sprite,
        x: 600,
        duration: 500,
        ease: 'Linear',
        onComplete: () => {
          // Third tween
          this.tweens.add({
            targets: sprite,
            scale: 2,
            duration: 300,
            ease: 'Back.easeOut'
          });
        }
      });
    }
  });

  // Better approach: Timeline
  const timeline = this.tweens.timeline({
    targets: sprite,
    tweens: [
      {
        y: 200,
        duration: 500,
        ease: 'Linear'
      },
      {
        x: 600,
        duration: 500,
        ease: 'Linear'
      },
      {
        scale: 2,
        duration: 300,
        ease: 'Back.easeOut'
      }
    ]
  });

  // Timeline with delay
  this.tweens.timeline({
    tweens: [
      {
        targets: sprite,
        alpha: 0,
        duration: 500,
        offset: 0 // Start immediately
      },
      {
        targets: otherSprite,
        y: 400,
        duration: 500,
        offset: '-=250' // Start 250ms before previous ends
      }
    ]
  });
}
```

### Level 4: Animation State Management

```typescript
class AnimationController {
  private sprite: Phaser.GameObjects.Sprite;
  private currentAnim = '';

  constructor(sprite: Phaser.GameObjects.Sprite) {
    this.sprite = sprite;

    // Listen for animation completion
    this.sprite.on('animationcomplete', this.onAnimComplete, this);
  }

  play(animKey: string, ignoreIfPlaying = false) {
    if (ignoreIfPlaying && this.currentAnim === animKey) {
      return;
    }

    // Don't interrupt non-looping animations
    const current = this.sprite.anims.currentAnim;
    if (current && !current.repeat && current.isPlaying) {
      return;
    }

    this.sprite.play(animKey);
    this.currentAnim = animKey;
  }

  onAnimComplete(event: any) {
    if (event.key === 'attack') {
      this.play('idle');
    } else if (event.key === 'death') {
      this.sprite.setVisible(false);
    }
  }

  isPlaying(animKey: string): boolean {
    return this.sprite.anims.isPlaying && this.sprite.anims.currentAnim?.key === animKey;
  }

  getProgress(): number {
    return this.sprite.anims.getProgress();
  }
}

// In scene
create() {
  this.player = this.add.sprite(400, 300, 'player');
  this.animController = new AnimationController(this.player);
  this.animController.play('idle');
}

update() {
  if (this.cursors.left.isDown || this.cursors.right.isDown) {
    this.animController.play('walk');
  } else {
    this.animController.play('idle');
  }

  if (this.attackKey.isDown && !this.animController.isPlaying('attack')) {
    this.animController.play('attack');
  }
}
```

### Level 5: Advanced Animation Systems

```typescript
export class GameScene extends Phaser.Scene {
  private animManager!: AnimationManager;

  create() {
    this.animManager = new AnimationManager(this);

    // Define animation states
    this.animManager.registerState("player", "idle", {
      frames: { start: 0, end: 3 },
      frameRate: 8,
      loop: true,
    });

    this.animManager.registerState("player", "walk", {
      frames: { start: 4, end: 11 },
      frameRate: 12,
      loop: true,
    });

    this.animManager.registerState("player", "jump", {
      frames: { start: 12, end: 15 },
      frameRate: 10,
      loop: false,
      next: "idle",
    });

    this.animManager.registerState("player", "attack", {
      frames: { start: 16, end: 21 },
      frameRate: 15,
      loop: false,
      next: "idle",
      callback: this.onAttackComplete,
    });

    // Set up state transitions
    this.animManager.addTransition("player", "idle", "walk", () =>
      this.isMoving(),
    );
    this.animManager.addTransition(
      "player",
      "walk",
      "idle",
      () => !this.isMoving(),
    );
    this.animManager.addTransition("player", "walk", "jump", () =>
      this.justJumped(),
    );

    // Initialize player
    this.player = this.add.sprite(400, 300, "player");
    this.animManager.attach("player", this.player);
  }

  update() {
    this.animController.update("player");
  }

  isMoving() {
    return this.cursors.left.isDown || this.cursors.right.isDown;
  }

  justJumped() {
    return Phaser.Input.Keyboard.JustDown(this.jumpKey);
  }

  onAttackComplete() {
    console.log("Attack finished");
  }
}

class AnimationManager {
  private states = new Map<string, Map<string, AnimationState>>();
  private sprites = new Map<string, Phaser.GameObjects.Sprite>();
  private transitions: Array<{
    sprite: string;
    from: string;
    to: string;
    condition: () => boolean;
  }> = [];

  constructor(private scene: Phaser.Scene) {}

  registerState(sprite: string, key: string, config: any) {
    if (!this.states.has(sprite)) {
      this.states.set(sprite, new Map());
    }

    const stateConfig = {
      ...config,
      key: `${sprite}_${key}`,
    };

    // Create Phaser animation
    this.scene.anims.create({
      key: stateConfig.key,
      frames: this.scene.anims.generateFrameNumbers(sprite, config.frames),
      frameRate: config.frameRate,
      repeat: config.loop ? -1 : 0,
      yoyo: config.yoyo || false,
    });

    this.states.get(sprite)!.set(key, stateConfig);
  }

  attach(spriteKey: string, sprite: Phaser.GameObjects.Sprite) {
    this.sprites.set(spriteKey, sprite);
    sprite.play(`${spriteKey}_idle`);
  }

  addTransition(
    sprite: string,
    from: string,
    to: string,
    condition: () => boolean,
  ) {
    this.transitions.push({ sprite, from, to, condition });
  }

  update(spriteKey: string) {
    const sprite = this.sprites.get(spriteKey);
    if (!sprite) return;

    const currentAnim = sprite.anims.currentAnim?.key.replace(
      `${spriteKey}_`,
      "",
    );
    const states = this.states.get(spriteKey);

    // Check transitions
    for (const transition of this.transitions) {
      if (
        transition.sprite === spriteKey &&
        transition.from === currentAnim &&
        transition.condition()
      ) {
        this.play(spriteKey, transition.to);
        break;
      }
    }
  }

  play(spriteKey: string, stateKey: string) {
    const sprite = this.sprites.get(spriteKey);
    const state = this.states.get(spriteKey)?.get(stateKey);
    if (sprite && state) {
      sprite.play(state.key);
      if (state.callback) {
        sprite.once("animationcomplete-" + state.key, state.callback);
      }
    }
  }
}
```

## Anti-Patterns

❌ **DON'T:**

- Create animations in update() - do it once in create()
- Override playing animation without checking
- Use tweens for simple value changes
- Forget to clean up event listeners
- Use `tweens.chain()` for simple sequences - use timeline
- Ignore animation repeat/yoyo properties

✅ **DO:**

- Create animations once in create()
- Check current animation before changing
- Use tweens for property animation
- Clean up listeners on shutdown
- Use timeline for sequences
- Configure repeat and yoyo appropriately

## Code Patterns

### Animation Playback Control

```typescript
// Check if animation is playing
if (sprite.anims.isPlaying) {
  console.log("Playing:", sprite.anims.currentAnim?.key);
}

// Get animation progress (0-1)
const progress = sprite.anims.getProgress();

// Pause/resume animation
sprite.anims.pause();
sprite.anims.resume();

// Stop animation
sprite.anims.stop();

// Restart animation
sprite.anims.restart();
```

### Tween Easing Functions

```typescript
// Linear
this.tweens.add({ targets: obj, x: 100, ease: "Linear" });

// Power easing
this.tweens.add({ targets: obj, x: 100, ease: "Power0" }); // Linear
this.tweens.add({ targets: obj, x: 100, ease: "Power1" }); // Smooth
this.tweens.add({ targets: obj, x: 100, ease: "Power2" }); // Accelerating
this.tweens.add({ targets: obj, x: 100, ease: "Power3" }); // More accelerating
this.tweens.add({ targets: obj, x: 100, ease: "Power4" }); // Most accelerating

// Special easing
this.tweens.add({ targets: obj, x: 100, ease: "Elastic.easeOut" });
this.tweens.add({ targets: obj, x: 100, ease: "Bounce.easeOut" });
this.tweens.add({ targets: obj, x: 100, ease: "Back.easeOut" });
this.tweens.add({ targets: obj, x: 100, ease: "Cubic.easeOut" });
```

### Tween Controls

```typescript
const tween = this.tweens.add({
  targets: sprite,
  alpha: 0,
  duration: 1000,
});

// Pause tween
tween.pause();

// Resume tween
tween.resume();

// Stop tween
tween.stop();

// Complete tween immediately
tween.complete();
```

## Common Easing Functions

| Ease      | Description        |
| --------- | ------------------ |
| `Linear`  | Constant speed     |
| `Power0`  | Same as Linear     |
| `Power1`  | Gentle ease        |
| `Power2`  | Medium ease        |
| `Power3`  | Strong ease        |
| `Power4`  | Strongest ease     |
| `Elastic` | Bouncy effect      |
| `Bounce`  | Bounce at end      |
| `Back`    | Overshoot slightly |
| `Sine`    | Smooth sine curve  |

## Checklist

- [ ] Animations created in create()
- [ ] Frame rates appropriate for smoothness
- [ ] Repeat/yoyo configured correctly
- [ ] Transitions handled gracefully
- [ ] Tweens use proper easing
- [ ] Event listeners cleaned up
- [ ] Animation state managed properly

## Reference

- [Animation Manager](https://photonstorm.github.io/phaser3-docs/Phaser.Animations.AnimationManager.html) — Animation API
- [Tween Manager](https://photonstorm.github.io/phaser3-docs/Phaser.Tweens.TweenManager.html) — Tween API
- [Easing Functions](https://photonstorm.github.io/phaser3-docs/Phaser.Math.Easing.html) — Easing reference
