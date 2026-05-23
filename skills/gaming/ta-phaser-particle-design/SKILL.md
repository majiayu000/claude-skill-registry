---
name: ta-phaser-particle-design
description: Designs particle systems for visual effects. Use proactively when creating particle effects, emitters, or visual polish.
category: techartist
---

# Phaser Particle Design

> "Create memorable visual moments with thoughtfully designed particle effects."

## When to Use This Skill

Use when:

- Designing signature visual effects
- Creating atmosphere and mood
- Building feedback systems
- Adding visual polish
- Implementing weather and ambient effects

## Design Principles

1. **Purposeful** - Every particle effect should communicate something
2. **Performant** - Limit particle count for target platform
3. **Readable** - Effects shouldn't obscure gameplay
4. **Satisfying** - Good feel through tuning and iteration

## Effect Types

| Category | Examples          | Key Properties             |
| -------- | ----------------- | -------------------------- |
| Impact   | Hit, explosion    | Speed variance, size decay |
| Ambient  | Dust, fog, rain   | Slow, subtle, continuous   |
| Magic    | Spells, aura      | Additive blend, glow       |
| UI       | Confetti, shine   | Quick, responsive          |
| Weather  | Rain, snow, storm | Direction, density         |

## Progressive Guide

### Level 1: Impact Effects

```typescript
// Hit spark effect
const createHitSpark = (
  scene: Phaser.Scene,
  x: number,
  y: number,
  color = 0xffff00,
) => {
  const particles = scene.add.particles(x, y, "spark", {
    speed: { min: 50, max: 200 },
    angle: { min: 0, max: 360 },
    scale: { start: 0.8, end: 0 },
    alpha: { start: 1, end: 0 },
    lifespan: 300,
    quantity: 8,
    blendMode: "ADD",
    emitting: false,
    onEmit: (particle: any) => {
      particle.tint = color;
    },
  });

  particles.explode(8, x, y);

  // Auto-cleanup
  scene.time.delayedCall(500, () => particles.destroy());
};

// Blood/spark effect on damage
scene.events.on("enemy-hit", (enemy) => {
  createHitSpark(scene, enemy.x, enemy.y, 0xff0000);
});
```

### Level 2: Ambient Effects

```typescript
// Atmospheric dust motes
const createDustMotes = (scene: Phaser.Scene) => {
  const dust = scene.add.particles(0, 0, "dust", {
    x: { min: 0, max: scene.scale.width },
    y: { min: 0, max: scene.scale.height },
    speed: { min: 2, max: 10 },
    angle: { min: 200, max: 340 },
    scale: { start: 0.1, end: 0.3 },
    alpha: { start: 0, end: 0.3, ease: "Quad.easeOut" },
    lifespan: { min: 3000, max: 6000 },
    frequency: 200,
    blendMode: "ADD",
  });

  dust.setDepth(-1); // Behind everything
  return dust;
};

// Fire flicker effect
const createFireGlow = (scene: Phaser.Scene, x: number, y: number) => {
  const glow = scene.add.particles(x, y, "glow", {
    speed: 20,
    scale: { start: 0.5, end: 1.5, ease: "Sine.easeInOut" },
    alpha: { start: 0.4, end: 0, ease: "Linear" },
    lifespan: 500,
    frequency: 100,
    blendMode: "ADD",
    emitZone: {
      type: "random",
      source: new Phaser.Geom.Circle(0, 0, 10),
    },
  });

  return glow;
};
```

### Level 3: Magic and Ability Effects

```typescript
// Magic circle cast effect
const createMagicCircle = (
  scene: Phaser.Scene,
  x: number,
  y: number,
  color = 0x8800ff,
) => {
  const circle = scene.add.particles(x, y, "spark", {
    speed: 100,
    angle: { min: 0, max: 360 },
    scale: { start: 0.2, end: 0.8, ease: "Back.easeOut" },
    alpha: { start: 1, end: 0 },
    lifespan: 600,
    quantity: 30,
    blendMode: "ADD",
    emitting: false,
    onEmit: (particle: any) => {
      particle.tint = color;
      // Spiral motion
      const angle = particle.angle;
      particle.velocityX = Math.cos(angle) * 100;
      particle.velocityY = Math.sin(angle) * 100;
    },
  });

  circle.explode(30, x, y);

  // Lingering aura
  const aura = scene.add.particles(x, y, "glow", {
    speed: 30,
    scale: { start: 0.5, end: 1.5 },
    alpha: { start: 0.3, end: 0 },
    lifespan: 800,
    frequency: 50,
    blendMode: "ADD",
    emitZone: {
      type: "edge",
      source: new Phaser.Geom.Circle(0, 0, 40),
      quantity: 20,
    },
    onEmit: (particle: any) => {
      particle.tint = color;
    },
  });

  scene.time.delayedCall(2000, () => aura.destroy());

  return { circle, aura };
};

// Projectile trail
const createTrailEmitter = (
  scene: Phaser.Scene,
  projectile: Phaser.GameObjects.Image,
) => {
  const trail = scene.add.particles(0, 0, "trail", {
    speed: 0,
    scale: { start: 0.5, end: 0 },
    alpha: { start: 0.5, end: 0 },
    lifespan: 200,
    frequency: 30,
    blendMode: "ADD",
  });

  trail.startFollow(projectile);

  return trail;
};
```

### Level 4: Weather Systems

```typescript
class WeatherSystem {
  private rain?: Phaser.GameObjects.Particles.ParticleEmitter;
  private lightning?: Phaser.Time.TimerEvent;
  private clouds?: Phaser.GameObjects.TileSprite;

  constructor(private scene: Phaser.Scene) {}

  setRain(intensity: "light" | "medium" | "heavy" = "medium") {
    this.clearWeather();

    const config = {
      light: { frequency: 100, speedY: 300 },
      medium: { frequency: 50, speedY: 400 },
      heavy: { frequency: 20, speedY: 500 },
    };

    const cfg = config[intensity];

    this.rain = this.scene.add.particles(0, 0, "rain", {
      x: { min: 0, max: this.scene.scale.width },
      y: -20,
      speedY: cfg.speedY,
      speedX: -20,
      scale: { start: 0.3, end: 0.3 },
      alpha: { start: 0.3, end: 0.6 },
      lifespan: 2000,
      frequency: cfg.frequency,
      emitZone: {
        type: "random",
        source: new Phaser.Geom.Rectangle(0, 0, this.scene.scale.width, 50),
      },
    });

    // Darken sky
    this.scene.cameras.main.setTint(0x8888aa);
  }

  setStorm() {
    this.setRain("heavy");

    // Lightning flashes
    this.lightning = this.scene.time.addEvent({
      delay: Phaser.Math.Between(2000, 5000),
      callback: this.flashLightning,
      callbackScope: this,
      loop: true,
    });

    // Storm clouds
    this.clouds = this.scene.add.tileSprite(
      this.scene.scale.width / 2,
      this.scene.scale.height / 2,
      this.scene.scale.width,
      this.scene.scale.height,
      "clouds",
    );
    this.clouds.setAlpha(0.3);
    this.clouds.setScrollFactor(0);
  }

  private flashLightning() {
    // Flash screen
    this.scene.cameras.main.flash(100, 255, 255, 255);

    // Play thunder sound delay based on "distance"
    const delay = Phaser.Math.Between(500, 2000);
    this.scene.time.delayedCall(delay, () => {
      // this.sound.play('thunder');
    });
  }

  setSnow(intensity: "light" | "medium" | "heavy" = "medium") {
    this.clearWeather();

    const config = {
      light: { frequency: 200, speedY: 50 },
      medium: { frequency: 100, speedY: 80 },
      heavy: { frequency: 50, speedY: 120 },
    };

    const cfg = config[intensity];

    this.rain = this.scene.add.particles(0, 0, "snow", {
      x: { min: 0, max: this.scene.scale.width },
      y: -10,
      speedY: cfg.speedY,
      speedX: { min: -20, max: 20 },
      scale: { start: 0.2, end: 0.3 },
      alpha: { start: 0.6, end: 0.8 },
      lifespan: 4000,
      frequency: cfg.frequency,
      emitZone: {
        type: "random",
        source: new Phaser.Geom.Rectangle(0, 0, this.scene.scale.width, 100),
      },
    });

    // Slight blue tint
    this.scene.cameras.main.setTint(0xddddff);
  }

  clearWeather() {
    if (this.rain) {
      this.rain.destroy();
      this.rain = undefined;
    }
    if (this.lightning) {
      this.lightning.destroy();
      this.lightning = undefined;
    }
    if (this.clouds) {
      this.clouds.destroy();
      this.clouds = undefined;
    }
    this.scene.cameras.main.clearTint();
  }
}
```

### Level 5: Particle Effect Library

```typescript
class ParticleLibrary {
  private effects: Map<
    string,
    (
      scene: Phaser.Scene,
      x: number,
      y: number,
      options?: any,
    ) => Phaser.GameObjects.Particles.ParticleEmitter
  >;

  constructor() {
    this.registerDefaults();
  }

  private registerDefaults() {
    // Explosion
    this.register("explosion", (scene, x, y, options = {}) => {
      const emitter = scene.add.particles(x, y, "explosion", {
        speed: { min: 100, max: 300 * (options.intensity || 1) },
        angle: { min: 0, max: 360 },
        scale: { start: 0.2, end: 1 },
        alpha: { start: 1, end: 0 },
        lifespan: 600,
        quantity: 20 * (options.quantity || 1),
        blendMode: "ADD",
        emitting: false,
      });

      emitter.explode(emitter.config.quantity, x, y);
      return emitter;
    });

    // Dust cloud
    this.register("dust", (scene, x, y, options = {}) => {
      return scene.add.particles(x, y, "dust", {
        speed: { min: 20, max: 60 },
        angle: { min: 0, max: 360 },
        scale: { start: 0.1, end: 0.5 },
        alpha: { start: 0.5, end: 0 },
        lifespan: 800,
        quantity: 5,
        blendMode: "NORMAL",
      });
    });

    // Healing aura
    this.register("heal", (scene, x, y, options = {}) => {
      return scene.add.particles(x, y, "sparkle", {
        speed: 30,
        scale: { start: 0, end: 0.3, ease: "Back.easeOut" },
        alpha: { start: 1, end: 0 },
        lifespan: 1000,
        frequency: 50,
        blendMode: "ADD",
        emitZone: {
          type: "edge",
          source: new Phaser.Geom.Circle(0, 0, 30),
          quantity: 10,
        },
        onEmit: (particle: any) => {
          particle.tint = 0x00ff88;
        },
      });
    });

    // Level up
    this.register("levelup", (scene, x, y) => {
      const burst = scene.add.particles(x, y, "star", {
        speed: { min: 100, max: 300 },
        angle: { min: 0, max: 360 },
        scale: { start: 0.2, end: 0.8 },
        alpha: { start: 1, end: 0 },
        lifespan: 1500,
        quantity: 50,
        blendMode: "ADD",
        emitting: false,
        onEmit: (particle: any) => {
          const colors = [0xffff00, 0xff8800, 0xffffff, 0x88ffff];
          particle.tint = Phaser.Utils.Array.GetRandom(colors);
        },
      });

      burst.explode(50, x, y);

      // Rising column of light
      const light = scene.add.rectangle(x, y, 40, 200, 0xffff00);
      light.setAlpha(0.3);
      light.setBlendMode(Phaser.BlendModes.ADD);

      scene.tweens.add({
        targets: light,
        scaleY: 3,
        alpha: 0,
        duration: 1000,
        ease: "Cubic.easeOut",
        onComplete: () => light.destroy(),
      });

      return burst;
    });
  }

  register(name: string, effect: Function) {
    this.effects.set(name, effect);
  }

  play(name: string, scene: Phaser.Scene, x: number, y: number, options?: any) {
    const effect = this.effects.get(name);
    if (effect) {
      return effect(scene, x, y, options);
    }
    return null;
  }
}

// Usage
const particles = new ParticleLibrary();
particles.play("explosion", this, this.enemy.x, this.enemy.y, {
  intensity: 1.5,
  quantity: 2,
});
```

## Tuning Guidelines

### Performance Targets

| Platform      | Max Particles | Blend Modes      |
| ------------- | ------------- | ---------------- |
| Desktop       | 500-1000      | Full support     |
| Mobile (high) | 200-400       | Careful with ADD |
| Mobile (low)  | 50-150        | Avoid ADD        |

### Feel Tuning

| Effect Property | Quick Effect | Slow Effect |
| --------------- | ------------ | ----------- |
| Lifespan        | 200-400ms    | 800-1500ms  |
| Speed           | 200-400      | 20-80       |
| Scale Decay     | Fast         | Slow        |
| Frequency       | 20-50ms      | 100-300ms   |

## Anti-Patterns

❌ **DON'T:**

- Overuse additive blending on mobile
- Create too many simultaneous emitters
- Use large textures for small particles
- Forget to destroy temporary emitters
- Make particles too bright (washes out)
- Use effects that obscure gameplay

✅ **DO:**

- Profile on target device
- Pool emitters when possible
- Use small particle textures
- Clean up emitters properly
- Balance brightness and readability
  | Keep gameplay visible

## Checklist

- [ ] Effect purpose is clear
- [ ] Particle count appropriate for platform
- [ ] Lifespan tuned for feel
- [ ] Blend mode chosen correctly
- [ ] Emitters cleaned up
- [ ] Effects don't obscure gameplay
- [ ] Performance tested on target device

## Reference

- [Particle Emitter](https://photonstorm.github.io/phaser3-docs/Phaser.GameObjects.Particles.ParticleEmitter.html) — Emitter API
- [Particle Manager](https://photonstorm.github.io/phaser3-docs/Phaser.GameObjects.Particles.ParticleManager.html) — Manager API
