---
name: dev-phaser-physics-arcade
description: Arcade physics velocity, acceleration, collision, and bounds
---

# Phaser Arcade Physics

> "Fast, simple 2D physics for platformers and arcade games."

## Before/After: Manual Collision vs Phaser Arcade Physics

### ❌ Before: Manual AABB Collision

```typescript
// Manual physics without Phaser
interface Box {
  x: number;
  y: number;
  width: number;
  height: number;
  vx: number;
  vy: number;
}

const player: Box = { x: 100, y: 300, width: 32, height: 48, vx: 0, vy: 0 };
const platforms: Box[] = [
  { x: 0, y: 500, width: 800, height: 68 }
];

function checkCollision(a: Box, b: Box): boolean {
  return a.x < b.x + b.width &&
         a.x + a.width > b.x &&
         a.y < b.y + b.height &&
         a.y + a.height > b.y;
}

function updatePhysics(dt: number) {
  // Apply gravity
  player.vy += 1000 * dt;

  // Update position
  player.x += player.vx * dt;
  player.y += player.vy * dt;

  // Check collision with each platform
  for (const platform of platforms) {
    if (checkCollision(player, platform)) {
      // Resolve collision
      if (player.vy > 0 && player.y + player.height - player.vy * dt <= platform.y) {
        player.y = platform.y - player.height;
        player.vy = 0;
      }
    }
  }

  // World bounds
  if (player.x < 0) player.x = 0;
  if (player.x > 800 - player.width) player.x = 800 - player.width;
}

// Problems:
// - Manual collision detection is error-prone
// - No proper physics simulation
// - Tunneling at high speeds
// - No built-in platformer features
// - Manual state tracking
```

### ✅ After: Phaser Arcade Physics

```typescript
// Phaser handles physics automatically
export class GameScene extends Phaser.Scene {
  private player!: Phaser.Physics.Arcade.Sprite;

  create() {
    // Physics-enabled sprite with built-in collision
    this.player = this.physics.add.sprite(100, 450, 'player');
    this.player.setBounce(0); // No bounce
    this.player.setCollideWorldBounds(true);

    // Static platforms group
    const platforms = this.physics.add.staticGroup();
    platforms.create(400, 568, 'ground').setScale(2, 1).refreshBody();

    // One line to add collision
    this.physics.add.collider(this.player, platforms);
  }

  update() {
    // Simple velocity-based movement
    if (this.cursors.left.isDown) {
      this.player.setVelocityX(-160);
    } else if (this.cursors.right.isDown) {
      this.player.setVelocityX(160);
    } else {
      this.player.setVelocityX(0);
    }

    // Grounded check built-in
    if (this.cursors.up.isDown && this.player.body!.touching.down) {
      this.player.setVelocityY(-330);
    }
  }
}

// Benefits:
// - Built-in collision detection (no tunneling)
// - Touching detection (grounded, walls)
// - World bounds handling
// - Proper physics simulation
// - Easy platformer features
```

## When to Use This Skill

Use when:

- Implementing platformer games
- Creating collision detection
- Working with velocity and gravity
- Building arcade-style gameplay
- Need simple, performant physics

## Quick Start

```typescript
// Enable arcade physics in game config
physics: {
  default: 'arcade',
  arcade: {
    gravity: { y: 1000 },
    debug: false
  }
}

// Create physics sprite
const player = this.physics.add.sprite(400, 300, 'player');
player.setBounce(0.2);
player.setCollideWorldBounds(true);
```

## Decision Framework

| Need                | Use                              |
| ------------------- | -------------------------------- |
| Platformer          | Arcade with gravity              |
| Top-down            | Arcade without gravity           |
| Bouncing objects    | `setBounce(0.5)`                 |
| Static platforms    | `this.physics.add.staticGroup()` |
| Collision detection | `this.physics.add.collider()`    |

## Progressive Guide

### Level 1: Basic Physics Body

```typescript
export class GameScene extends Phaser.Scene {
  private player!: Phaser.Physics.Arcade.Sprite;

  create() {
    // Create physics sprite
    this.player = this.physics.add.sprite(400, 300, "player");

    // Physics properties
    this.player.setBounce(0.2); // Bounciness (0-1)
    this.player.setCollideWorldBounds(true); // Don't leave screen
    this.player.setDrag(0.1, 0); // Air resistance
    this.player.setFriction(0.1); // Ground friction
    this.player.setMaxVelocity(400); // Speed cap

    // Velocity control
    this.player.setVelocityX(200);
    this.player.setVelocityY(-300);
    this.player.setVelocity(100, 100);

    // Acceleration
    this.player.setAccelerationX(50);
  }
}
```

### Level 2: Collision Detection

```typescript
create() {
  const player = this.physics.add.sprite(400, 300, 'player');
  const platforms = this.physics.add.staticGroup();

  // Create platforms
  platforms.create(400, 568, 'ground').setScale(2, 1).refreshBody();
  platforms.create(600, 400, 'platform');

  // Player collides with platforms
  this.physics.add.collider(player, platforms);

  // Overlap detection (trigger, no collision response)
  const coins = this.physics.add.group({
    defaultKey: 'coin',
    bounceX: 0.5,
    bounceY: 0.5
  });

  this.physics.add.overlap(player, coins, this.collectCoin, undefined, this);
}

collectCoin(player: Phaser.Types.Physics.Arcade.GameObjectWithBody, coin: any) {
  coin.disableBody(true, true); // Disable and hide
}
```

### Level 3: Platformer Controls

```typescript
export class GameScene extends Phaser.Scene {
  private player!: Phaser.Physics.Arcade.Sprite;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private jumpKey!: Phaser.Input.Keyboard.Key;

  create() {
    this.player = this.physics.add.sprite(100, 450, "player");
    this.player.setBounce(0);
    this.player.setCollideWorldBounds(true);

    // Setup inputs
    this.cursors = this.input.keyboard!.createCursorKeys();
    this.jumpKey = this.input.keyboard!.addKey("SPACE");

    // Platforms
    const platforms = this.physics.add.staticGroup();
    platforms.create(400, 568, "ground").setScale(2).refreshBody();

    this.physics.add.collider(this.player, platforms);
  }

  update() {
    // Left/Right movement
    if (this.cursors.left.isDown) {
      this.player.setVelocityX(-160);
    } else if (this.cursors.right.isDown) {
      this.player.setVelocityX(160);
    } else {
      this.player.setVelocityX(0);
    }

    // Jump only if touching ground
    if (this.jumpKey.isDown && this.player.body!.touching.down) {
      this.player.setVelocityY(-330);
    }
  }
}
```

### Level 4: Advanced Collision Callbacks

```typescript
create() {
  // Collision with process callback (custom collision logic)
  this.physics.add.collider(
    this.player,
    this.enemies,
    this.playerHitEnemy,
    this.checkEnemyVulnerable,
    this
  );
}

// Called to check if collision should happen
checkEnemyVulnerable(
  player: Phaser.Types.Physics.Arcade.GameObjectWithBody,
  enemy: any
): boolean {
  const enemySprite = enemy as Phaser.Physics.Arcade.Sprite;
  // Only collide if enemy is vulnerable
  return !enemySprite.getData('invincible');
}

// Called when collision occurs
playerHitEnemy(
  player: Phaser.Types.Physics.Arcade.GameObjectWithBody,
  enemy: any
) {
  const enemySprite = enemy as Phaser.Physics.Arcade.Sprite;

  // If player is above enemy, kill enemy
  if (player.body!.velocity.y > 0 && player.y < enemySprite.y - 10) {
    enemySprite.destroy();
    player.setVelocityY(-200); // Bounce
  } else {
    // Player dies
    this.handlePlayerDeath();
  }
}
```

### Level 5: Custom Physics Components

```typescript
// Physics component class
class PlatformerController {
  private speed = 160;
  private jumpForce = -330;
  private isGrounded = false;

  constructor(
    private sprite: Phaser.Physics.Arcade.Sprite,
    private cursors: Phaser.Types.Input.Keyboard.CursorKeys,
    private jumpKey: Phaser.Input.Keyboard.Key
  ) {
    this.enableDoubleJump();
  }

  update() {
    // Horizontal movement
    if (this.cursors.left.isDown) {
      this.sprite.setVelocityX(-this.speed);
      this.sprite.setFlipX(true);
    } else if (this.cursors.right.isDown) {
      this.sprite.setVelocityX(this.speed);
      this.sprite.setFlipX(false);
    } else {
      this.sprite.setVelocityX(0);
    }

    // Jump
    if (this.jumpKey.isDown && this.isGrounded) {
      this.sprite.setVelocityY(this.jumpForce);
      this.isGrounded = false;
    }
  }

  onGrounded() {
    this.isGrounded = true;
  }

  private enableDoubleJump() {
    this.jumpKey.on('down', () => {
      if (!this.isGrounded && this.sprite.body!.velocity.y > -200) {
        this.sprite.setVelocityY(this.jumpForce * 0.8);
      }
    });
  }
}

// In scene
create() {
  const controller = new PlatformerController(
    this.player,
    this.cursors,
    this.jumpKey
  );

  this.physics.add.collider(this.player, platforms, () => {
    controller.onGrounded();
  });
}

update() {
  controller.update();
}
```

## Anti-Patterns

❌ **DON'T:**

- Use Matter physics for simple platformers - Arcade is faster
- Set position directly on physics bodies - use velocity
- Forget to call `refreshBody()` after scaling static objects
- Use overlap when collider is needed
- Disable physics bodies instead of removing from scene
- Mix pixel and meter units arbitrarily

✅ **DO:**

- Use Arcade for platformers, top-down games
- Apply forces/velocity for movement
- Refresh body after scale/position changes
- Use proper collision types (collider vs overlap)
- Remove bodies from physics world when destroyed
- Keep units consistent (pixels)

## Code Patterns

### One-Way Platforms

```typescript
create() {
  const platforms = this.physics.add.staticGroup();

  // Create one-way platform
  const platform = platforms.create(400, 400, 'platform');
  platform.checkCollision.down = false; // Can jump through from below
  platform.checkCollision.up = true;    // Lands on top
}
```

### Body Size Adjustment

```typescript
const player = this.physics.add.sprite(400, 300, "player");

// Adjust body size (smaller than sprite)
player.body!.setSize(20, 40);
player.body!.setOffset(6, 8); // Center the body

// Disable body on one side
player.body!.checkCollision.up = false;
```

### Moving Platform

```typescript
export class MovingPlatform extends Phaser.Physics.Arcade.Image {
  constructor(
    scene: Phaser.Scene,
    x: number,
    y: number,
    texture: string,
    private startX: number,
    private endX: number,
  ) {
    super(scene, x, y, texture);
    scene.add.existing(this);
    scene.physics.add.existing(this, false); // false = static

    this.setVelocityX(50);
    this.scene.events.on("update", this.updatePlatform, this);
  }

  updatePlatform() {
    if (this.x >= this.endX) {
      this.setVelocityX(-50);
    } else if (this.x <= this.startX) {
      this.setVelocityX(50);
    }
  }
}
```

## Checklist

- [ ] Physics enabled in game config
- [ ] Bodies properly sized (offset from sprite)
- [ ] Static bodies use `staticGroup()`
- [ ] Dynamic bodies use `physics.add.sprite()`
- [ ] Colliders/overlaps configured
- [ ] World bounds enabled if needed
- [ ] Refresh body called after scale

## Physics Body Properties

| Property       | Type    | Description                  |
| -------------- | ------- | ---------------------------- |
| `velocity`     | Vector2 | Current velocity             |
| `acceleration` | Vector2 | Applied acceleration         |
| `drag`         | Vector2 | Deceleration over time       |
| `gravity`      | Vector2 | Applied gravity force        |
| `bounce`       | number  | Bounciness (0-1)             |
| `friction`     | number  | Surface friction             |
| `maxVelocity`  | Vector2 | Maximum speed cap            |
| `allowGravity` | boolean | Whether gravity affects body |
| `immovable`    | boolean | Body cannot be pushed        |

## Reference

- [Arcade Physics Docs](https://photonstorm.github.io/phaser3-docs/Phaser.Physics.Arcade.ArcadePhysics.html) — Official docs
- [Physics Body API](https://photonstorm.github.io/phaser3-docs/Phaser.Physics.Arcade.Body.html) — Body properties
