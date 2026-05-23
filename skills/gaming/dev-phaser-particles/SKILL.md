---
name: dev-phaser-particles
description: Particle emitters for visual effects like fire, smoke, explosions, and magic
---

# Phaser Particles

> "Create stunning visual effects with particle systems."

## Before/After: Manual Particle System vs Phaser Particles

### ❌ Before: Manual Particle Management

```typescript
// Manual particle system without Phaser
class Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
  size: number;
  alpha: number;
  color: string;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
    const angle = Math.random() * Math.PI * 2;
    const speed = 50 + Math.random() * 200;
    this.vx = Math.cos(angle) * speed;
    this.vy = Math.sin(angle) * speed;
    this.life = 0;
    this.maxLife = 500 + Math.random() * 500;
    this.size = 2 + Math.random() * 4;
    this.alpha = 1;
    this.color = `hsl(${Math.random() * 60 + 10}, 100%, 50%)`;
  }

  update(dt: number): boolean {
    this.x += this.vx * dt / 1000;
    this.y += this.vy * dt / 1000;
    this.vy += 200 * dt / 1000; // Gravity
    this.life += dt;
    this.alpha = 1 - (this.life / this.maxLife);
    return this.life < this.maxLife;
  }

  render(ctx: CanvasRenderingContext2D) {
    ctx.globalAlpha = this.alpha;
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = 1;
  }
}

class ParticleSystem {
  private particles: Particle[] = [];

  explode(x: number, y: number, count: number) {
    for (let i = 0; i < count; i++) {
      this.particles.push(new Particle(x, y));
    }
  }

  update(dt: number) {
    // Filter out dead particles - creates garbage!
    this.particles = this.particles.filter(p => p.update(dt));
  }

  render(ctx: CanvasRenderingContext2D) {
    for (const p of this.particles) {
      p.render(ctx);
    }
  }

  // No built-in emit zones
  // No death zones
  // No onEmit callbacks
  // No texture/animated particles
  // No blend modes (ADD, MULTIPLY)
}

// Problems:
// - Manual array filtering creates GC pressure
// - No built-in particle lifecycle management
// - Manual render loop for each particle
// - No texture support (only circles/rects)
// - No blend modes (ADD for fire/magic)
// - No emit zones (circle, rectangle, edge)
// - No death zones
// - No onEmit/onDeath callbacks
// - Performance degrades with many particles
```

### ✅ After: Phaser Particle System

```typescript
// Phaser handles particles automatically
export class GameScene extends Phaser.Scene {
  create() {
    // Explosion emitter - ONE config!
    const explosion = this.add.particles(0, 0, 'explosion', {
      speed: { min: 100, max: 400 },
      angle: { min: 0, max: 360 },
      scale: { start: 0.5, end: 2 },
      alpha: { start: 1, end: 0 },
      lifespan: 600,
      quantity: 30,
      emitting: false, // Don't auto-emit
      blendMode: 'ADD' // Built-in blend modes!
    });

    // Trigger explosion anywhere - ONE line!
    explosion.explode(30, 400, 300);

    // Fire effect - continuous emitter
    const fire = this.add.particles(400, 500, 'fire', {
      speed: { min: 50, max: 100 },
      angle: { min: 240, max: 300 },
      scale: { start: 0.5, end: 0 },
      alpha: { start: 0.8, end: 0 },
      blendMode: 'ADD',
      lifespan: 800,
      frequency: 50, // Emit every 50ms
      quantity: 3
    });

    // Trail following player - ONE line!
    const trail = this.add.particles(0, 0, 'trail', {
      speed: 0,
      scale: { start: 0.8, end: 0 },
      alpha: { start: 0.5, end: 0 },
      lifespan: 300,
      quantity: 1,
      frequency: 50,
      emitZone: {
        type: 'edge', // Circle edge emission!
        source: new Phaser.Geom.Circle(0, 0, 20),
        quantity: 3
      }
    });
    trail.startFollow(this.player); // Auto-follow!

    // Custom per-particle behavior
    const sparkles = this.add.particles(400, 300, 'sparkle', {
      speed: { min: 50, max: 150 },
      scale: { start: 0, end: 0.5, ease: 'Back.easeOut' },
      alpha: { start: 1, end: 0 },
      lifespan: { min: 500, max: 1000 },
      onEmit: (particle: any) => {
        // Customize each particle!
        particle.tint = Phaser.Utils.Array.GetRandom([
          0xff0000, 0x00ff00, 0x0000ff
        ]);
      }
    });
  }
}

// Benefits:
// - Automatic object pooling (no GC!)
// - Built-in lifecycle management
// - GPU-accelerated rendering
// - Texture support + animation
// - Blend modes (ADD, MULTIPLY, SCREEN)
// - Emit zones (random, edge)
// - Death zones
// - Per-particle callbacks
// - Follow any game object
```

## When to Use This Skill

Use when:

- Creating explosion effects
- Adding fire/smoke effects
- Building magic spells
- Implementing weather effects
- Adding visual polish to actions

## Quick Start

```typescript
create() {
  const particles = this.add.particles(0, 0, 'flare', {
    speed: 100,
    scale: { start: 1, end: 0 },
    blendMode: 'ADD'
  });

  particles.startFollow(this.player);
}
```

## Decision Framework

| Need                | Use                        |
| ------------------- | -------------------------- |
| Trail effect        | `startFollow()` + emitting |
| Explosion           | One-time burst emitter     |
| Continuous effect   | Always-on emitter          |
| Zone-based emission | Emitter zone               |
| Texture animation   | Animated particle frames   |

## Progressive Guide

### Level 1: Basic Particle Emitter

```typescript
export class GameScene extends Phaser.Scene {
  create() {
    // Simple particle emitter
    const particles = this.add.particles(400, 300, "flare", {
      speed: 100,
      scale: { start: 1, end: 0 },
      blendMode: "ADD",
      lifespan: 1000,
      quantity: 1,
    });

    // Particle at mouse position
    this.input.on("pointermove", (pointer: Phaser.Input.Pointer) => {
      particles.emitParticleAt(pointer.x, pointer.y);
    });
  }
}
```

### Level 2: Common Effects

```typescript
create() {
  // Fire effect
  const fire = this.add.particles(400, 500, 'fire', {
    speed: { min: 50, max: 100 },
    angle: { min: 240, max: 300 },
    scale: { start: 0.5, end: 0 },
    blendMode: 'ADD',
    lifespan: 800,
    frequency: 50,
    quantity: 3
  });

  // Smoke effect
  const smoke = this.add.particles(400, 480, 'smoke', {
    speed: 30,
    angle: { min: 250, max: 290 },
    scale: { start: 0.3, end: 1 },
    alpha: { start: 0.5, end: 0 },
    lifespan: 2000,
    frequency: 100
  });

  // Explosion
  const createExplosion = (x: number, y: number) => {
    const explosion = this.add.particles(x, y, 'explosion', {
      speed: { min: 100, max: 300 },
      angle: { min: 0, max: 360 },
      scale: { start: 0.5, end: 2 },
      alpha: { start: 1, end: 0 },
      lifespan: 500,
      quantity: 30,
      emitting: false
    });

    explosion.explode(30, x, y);
  };

  // Trigger explosion on click
  this.input.on('pointerdown', (pointer: Phaser.Input.Pointer) => {
    createExplosion(pointer.x, pointer.y);
  });
}
```

### Level 3: Following Emitters

```typescript
export class GameScene extends Phaser.Scene {
  private trailEmitter!: Phaser.GameObjects.Particles.ParticleEmitter;

  create() {
    // Create player
    this.player = this.add.image(400, 300, "player");

    // Trail emitter
    this.trailEmitter = this.add.particles(0, 0, "trail", {
      speed: 0,
      scale: { start: 0.8, end: 0 },
      alpha: { start: 0.5, end: 0 },
      lifespan: 300,
      quantity: 1,
      frequency: 50,
      emitZone: {
        type: "edge",
        source: new Phaser.Geom.Circle(0, 0, 20),
        quantity: 3,
      },
    });

    // Follow player
    this.trailEmitter.startFollow(this.player);

    // Engine exhaust effect
    const exhaust = this.add.particles(0, 20, "exhaust", {
      speedX: { min: -20, max: 20 },
      speedY: { min: 50, max: 100 },
      scale: { start: 0.3, end: 0 },
      alpha: { start: 0.8, end: 0 },
      lifespan: 400,
      frequency: 30,
    });

    exhaust.startFollow(this.player);
  }
}
```

### Level 4: Advanced Particle Configurations

```typescript
create() {
  // Magic sparkles
  const sparkles = this.add.particles(400, 300, 'sparkle', {
    speed: { min: 50, max: 150 },
    angle: { min: 0, max: 360 },
    scale: { start: 0, end: 0.5, ease: 'Back.easeOut' },
    alpha: { start: 1, end: 0, ease: 'Linear' },
    lifespan: { min: 500, max: 1000 },
    quantity: 2,
    frequency: 100,
    blendMode: 'ADD',
    rotate: { start: 0, end: 180 },
    emitting: true
  });

  // Rain effect
  const rainZone = new Phaser.Geom.Rectangle(0, 0, this.scale.width, 20);
  const rain = this.add.particles(0, 0, 'rain', {
    x: { min: 0, max: this.scale.width },
    y: -20,
    speedY: 400,
    speedX: 0,
    scale: { start: 0.3, end: 0.3 },
    alpha: { start: 0.5, end: 0.8 },
    lifespan: 2000,
    quantity: 5,
    frequency: 20,
    emitZone: { source: rainZone }
  });

  // Radial burst
  const burstEmitter = this.add.particles(400, 300, 'particle', {
    speed: 200,
    scale: { start: 1, end: 0 },
    alpha: { start: 1, end: 0 },
    lifespan: 1000,
    quantity: 50,
    emitting: false,
    onEmit: (particle: any) => {
      // Set custom color per particle
      particle.tint = Phaser.Utils.Array.GetRandom([0xff0000, 0x00ff00, 0x0000ff]);
    }
  });

  this.input.on('pointerdown', (pointer: Phaser.Input.Pointer) => {
    burstEmitter.explode(50, pointer.x, pointer.y);
  });
}
```

### Level 5: Particle System Manager

```typescript
class ParticleManager {
  private emitters = new Map<
    string,
    Phaser.GameObjects.Particles.ParticleEmitter
  >();

  constructor(private scene: Phaser.Scene) {
    this.createPresets();
  }

  private createPresets() {
    // Fire preset
    this.createEmitter("fire", {
      key: "fire",
      config: {
        speed: { min: 50, max: 100 },
        angle: { min: 240, max: 300 },
        scale: { start: 0.5, end: 0 },
        alpha: { start: 0.8, end: 0 },
        blendMode: "ADD",
        lifespan: 800,
        frequency: 50,
      },
    });

    // Explosion preset
    this.createEmitter("explosion", {
      key: "explosion",
      config: {
        speed: { min: 100, max: 400 },
        angle: { min: 0, max: 360 },
        scale: { start: 0.3, end: 1 },
        alpha: { start: 1, end: 0 },
        lifespan: 600,
        quantity: 30,
        emitting: false,
      },
    });

    // Trail preset
    this.createEmitter("trail", {
      key: "trail",
      config: {
        speed: 50,
        scale: { start: 0.5, end: 0 },
        alpha: { start: 0.6, end: 0 },
        lifespan: 400,
        frequency: 50,
      },
    });
  }

  createEmitter(name: string, { key, config }: any) {
    const emitter = this.scene.add.particles(0, 0, key, config);
    this.emitters.set(name, emitter);
    return emitter;
  }

  emit(name: string, x: number, y: number) {
    const emitter = this.emitters.get(name);
    if (emitter) {
      emitter.explode(emitter.config.quantity || 10, x, y);
    }
  }

  follow(name: string, target: Phaser.GameObjects.GameObject) {
    const emitter = this.emitters.get(name);
    if (emitter) {
      emitter.startFollow(target);
    }
  }

  stop(name: string) {
    const emitter = this.emitters.get(name);
    if (emitter) {
      emitter.stop();
    }
  }

  start(name: string) {
    const emitter = this.emitters.get(name);
    if (emitter) {
      emitter.start();
    }
  }

  destroy(name: string) {
    const emitter = this.emitters.get(name);
    if (emitter) {
      emitter.destroy();
      this.emitters.delete(name);
    }
  }
}

// Usage in scene
export class GameScene extends Phaser.Scene {
  private particles!: ParticleManager;

  create() {
    this.particles = new ParticleManager(this);

    // Use presets
    this.particles.follow("trail", this.player);

    // Trigger explosion
    this.input.on("pointerdown", (pointer: Phaser.Input.Pointer) => {
      this.particles.emit("explosion", pointer.x, pointer.y);
    });
  }
}
```

## Anti-Patterns

❌ **DON'T:**

- Create too many particles per frame
- Use large particle textures for small effects
- Forget to stop emitters when done
- Overuse blend modes (can kill performance)
- Create particles in update() loop
- Ignore particle lifespan

✅ **DO:**

- Limit particle count for mobile
- Use appropriate particle sizes
- Stop/remove unused emitters
- Use blend modes sparingly
- Create emitters once in create()
- Tune lifespan for desired effect

## Code Patterns

### Emit Zones

```typescript
// Rectangle zone
const rectZone = new Phaser.Geom.Rectangle(x, y, width, height);
particles.setEmitZone({
  type: "random",
  source: rectZone,
});

// Edge zone (particles on perimeter)
const edgeZone = new Phaser.Geom.Circle(x, y, radius);
particles.setEmitZone({
  type: "edge",
  source: edgeZone,
  quantity: 20,
});

// Random point zone
const pointZone = new Phaser.Geom.Circle(x, y, radius);
particles.setEmitZone({
  type: "random",
  source: pointZone,
});
```

### Death Zones

```typescript
// Particles die when entering zone
const deathZone = new Phaser.Geom.Rectangle(300, 200, 200, 200);
particles.setDeathZone({
  type: "onEnter",
  source: deathZone,
});
```

### Particle Callbacks

```typescript
const particles = this.add.particles(400, 300, "spark", {
  speed: 100,
  lifespan: 1000,
  onEmit: (particle: any) => {
    // Customize each particle
    particle.tint = 0xff0000;
    particle.velocity.x *= Math.random();
  },
  onParticleEmit: (emitter, particle) => {
    // Called when particle emits
  },
  onParticleDeath: (emitter, particle) => {
    // Called when particle dies
  },
});
```

## Emitter Configuration Reference

| Property    | Type           | Description                 |
| ----------- | -------------- | --------------------------- |
| `speed`     | number/min/max | Particle velocity           |
| `angle`     | number/min/max | Emission angle              |
| `scale`     | start/end      | Size over life              |
| `alpha`     | start/end      | Opacity over life           |
| `lifespan`  | number/min/max | Particle duration (ms)      |
| `quantity`  | number         | Particles per emission      |
| `frequency` | number         | Time between emissions (ms) |
| `blendMode` | string         | Rendering blend mode        |
| `rotate`    | start/end      | Rotation over life          |
| `emitZone`  | object         | Zone for emission           |
| `deathZone` | object         | Zone for death              |

## Common Blend Modes

| Mode       | Description | Use For             |
| ---------- | ----------- | ------------------- |
| `NORMAL`   | Default     | Most effects        |
| `ADD`      | Additive    | Fire, sparks, magic |
| `MULTIPLY` | Multiply    | Shadows, smoke      |
| `SCREEN`   | Screen      | Glowing effects     |

## Checklist

- [ ] Particle textures loaded
- [ ] Emitter frequency tuned
- [ ] Particle lifespan appropriate
- [ ] Speed and angle configured
- [ ] Blend mode set correctly
- [ ] Emitters stopped/removed when done
- [ ] Particle count limited for performance

## Reference

- [Particle Emitter](https://photonstorm.github.io/phaser3-docs/Phaser.GameObjects.Particles.ParticleEmitter.html) — Emitter API
- [Particle Manager](https://photonstorm.github.io/phaser3-docs/Phaser.GameObjects.Particles.ParticleManager.html) — Manager API
