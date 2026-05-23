---
name: ta-phaser-fundamentals
description: Configures Phaser games and manages scene lifecycle. Use proactively when setting up Phaser scenes, creating game config, or managing scene transitions.
category: techartist
---

# Phaser Fundamentals for Tech Artists

> "2D web games made simple – scenes, sprites, and visual polish."

## When to Use This Skill

Use when:

- Setting up Phaser game configuration
- Creating and managing scenes
- Understanding the Phaser lifecycle (preload/create/update)
- Configuring rendering and visual settings
- Setting up scene transitions

## Quick Start

```typescript
// Game config with visual settings
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
  scene: [MainScene],
  // Pixel art settings
  render: {
    pixelArt: true,
  },
};

new Phaser.Game(config);
```

## Visual Configuration

### Pixel Art Mode

```typescript
// Enable pixel art rendering
const config: Phaser.Types.Core.GameConfig = {
  render: {
    pixelArt: true, // Disables smoothing
    antialias: false,
    roundPixels: false,
  },
  scene: [MainScene],
};
```

### Camera Setup

```typescript
create() {
  // Main camera
  const camera = this.cameras.main;

  // Background color
  camera.setBackgroundColor('#2d2d2d');

  // Bounds (for level boundaries)
  camera.setBounds(0, 0, 2000, 2000);

  // Zoom
  camera.setZoom(1);

  // Follow player
  camera.startFollow(this.player, true, 0.08, 0.08);
}
```

## Scene Visual Lifecycle

```typescript
export class MainScene extends Phaser.Scene {
  preload() {
    // Load all visual assets
    this.load.image("background", "assets/background.png");
    this.load.spritesheet("player", "assets/player.png", {
      frameWidth: 32,
      frameHeight: 32,
    });
    this.load.atlas("ui", "assets/ui.png", "assets/ui.json");
  }

  create() {
    // Setup visual layers
    this.setupBackground();
    this.setupPlayer();
    this.setupUI();
  }

  update(time: number, delta: number) {
    // Visual updates (60fps)
    this.updateParticles();
    this.updateAnimations();
  }

  private setupBackground() {
    // Tiling background
    this.bg = this.add.tileSprite(
      400,
      300,
      this.scale.width,
      this.scale.height,
      "background",
    );
    this.bg.setScrollFactor(0.5); // Parallax
  }

  private setupPlayer() {
    this.player = this.add.sprite(100, 300, "player");
    this.player.play("idle");
  }

  private setupUI() {
    // UI layer on top
    const uiContainer = this.add.container(0, 0);
    uiContainer.setScrollFactor(0); // Fixed position

    const healthBar = this.add.rectangle(20, 20, 200, 20, 0x00ff00);
    const healthText = this.add.text(120, 30, "100", {
      fontSize: "16px",
      color: "#ffffff",
    });
    healthText.setOrigin(0.5);

    uiContainer.add([healthBar, healthText]);
  }

  private updateParticles() {
    // Update particle emitters
  }

  private updateAnimations() {
    // Update sprite animations
  }
}
```

## Visual Best Practices

1. **Asset Organization**
   - Use texture atlases for sprites
   - Separate UI assets into own atlas
   - Organize by scene/function

2. **Performance**
   - Use object pooling for particles
   - Limit active game objects
   - Cull off-screen sprites

3. **Layering**
   - Background layer (parallax)
   - Game layer (main action)
   - Foreground layer (parallax)
   - UI layer (fixed, no scroll)

4. **Pixel Art**
   - Set `pixelArt: true` in config
   - Use `setFilterMode(Phaser.Textures.FilterMode.NEAREST)`
   - Keep original resolution

## Checklist

- [ ] Game config has proper visual settings
- [ ] Scenes have proper layering
- [ ] UI elements fixed with scrollFactor(0)
- [ ] Parallax configured for layers
- [ ] Asset atlases used instead of individual images
- [ ] Pixel art mode enabled when needed

## Reference

- [Phaser Scale Manager](https://photonstorm.github.io/phaser3-docs/Phaser.Scale.Manager.html) — Responsive scaling
- [Phaser Cameras](https://photonstorm.github.io/phaser3-docs/Phaser.Cameras.Scene2D.Camera.html) — Camera API
- [Phaser Renderer](https://photonstorm.github.io/phaser3-docs/Phaser.Renderer.Renderer.html) — Rendering settings
