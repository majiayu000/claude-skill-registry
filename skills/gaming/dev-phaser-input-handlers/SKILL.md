---
name: dev-phaser-input-handlers
description: Keyboard, mouse, touch, and gamepad input management for Phaser
---

# Phaser Input Handlers

> "Responsive controls for every platform and input method."

## Before/After: Manual DOM Events vs Phaser Input System

### ❌ Before: Manual DOM Event Listeners

```typescript
// Manual input handling without Phaser
const keys: { [key: string]: boolean } = {};

// Setup key listeners
document.addEventListener('keydown', (e) => {
  keys[e.key] = true;
  keys[e.code] = true;

  // Manual input handling
  if (e.key === 'ArrowLeft') player.x -= 5;
  if (e.key === 'ArrowRight') player.x += 5;
  if (e.code === 'KeyW') player.y -= 5;
});

document.addEventListener('keyup', (e) => {
  keys[e.key] = false;
  keys[e.code] = false;
});

// Manual mouse/touch
canvas.addEventListener('mousedown', (e) => {
  shoot(e.clientX, e.clientY);
});

canvas.addEventListener('touchstart', (e) => {
  const touch = e.touches[0];
  shoot(touch.clientX, touch.clientY);
});

// Problems:
// - Different code paths for mouse vs touch
// - No key repeat prevention
// - No JustDown/JustUp tracking
// - Manual input state management
// - No gamepad support
// - Platform-specific issues
```

### ✅ After: Phaser Unified Input System

```typescript
// Phaser handles all input types uniformly
export class GameScene extends Phaser.Scene {
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private gamepadIndex = 0;
  private inputManager!: InputManager;

  create() {
    // Unified input setup - ONE system for all!
    this.cursors = this.input.keyboard!.createCursorKeys();
    this.inputManager = new InputManager(this);

    // Pointer works for mouse AND touch automatically
    this.input.on('pointerdown', (pointer: Phaser.Input.Pointer) => {
      this.shoot(pointer.x, pointer.y);
    });

    // Gamepad auto-detected
    this.input.gamepad!.on('connected', (pad) => {
      console.log('Gamepad connected:', pad.id);
    });
  }

  update() {
    // Input Manager abstracts all input methods
    const move = this.inputManager.getMovement(); // Works for keyboard, gamepad, or virtual joystick!

    this.player.setVelocity(move.x * 200, move.y * 200);

    if (this.inputManager.isJumpPressed()) {
      this.player.jump();
    }
  }
}

// Benefits:
// - Single API for all input types
// - Built-in JustDown/JustUp for triggers
// - Automatic mouse/touch unification
// - Native gamepad support
// - Virtual joystick for mobile
// - Platform-agnostic code
```

## When to Use This Skill

Use when:

- Implementing player controls
- Handling keyboard input
- Adding mouse/touch interaction
- Supporting gamepad controllers
- Creating virtual controls for mobile

## Quick Start

```typescript
create() {
  // Keyboard
  this.cursors = this.input.keyboard!.createCursorKeys();
  this.wasd = this.input.keyboard!.addKeys('W,A,S,D');

  // Mouse
  this.input.on('pointerdown', (pointer) => {
    this.spawnBullet(pointer.x, pointer.y);
  });
}

update() {
  if (this.cursors.left.isDown) {
    this.player.x -= 5;
  }
}
```

## Decision Framework

| Need       | Use                                   |
| ---------- | ------------------------------------- |
| Arrow keys | `createCursorKeys()`                  |
| WASD       | `addKeys('W,A,S,D')`                  |
| Click/tap  | `pointerdown` event                   |
| Drag       | `setInteractive({ draggable: true })` |
| Gamepad    | `gamepadpad` plugin                   |

## Progressive Guide

### Level 1: Keyboard Input

```typescript
export class GameScene extends Phaser.Scene {
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private wasd!: {
    W: Phaser.Input.Keyboard.Key;
    A: Phaser.Input.Keyboard.Key;
    S: Phaser.Input.Keyboard.Key;
    D: Phaser.Input.Keyboard.Key;
  };
  private jumpKey!: Phaser.Input.Keyboard.Key;
  private shootKey!: Phaser.Input.Keyboard.Key;

  create() {
    // Arrow keys
    this.cursors = this.input.keyboard!.createCursorKeys();

    // WASD keys
    this.wasd = this.input.keyboard!.addKeys("W,A,S,D") as any;

    // Single key
    this.jumpKey = this.input.keyboard!.addKey("SPACE");
    this.shootKey = this.input.keyboard!.addKey(
      Phaser.Input.Keyboard.KeyCodes.X,
    );

    // Key combinations
    const shiftKey = this.input.keyboard!.addKey("SHIFT");
    this.input.keyboard!.on("keydown-SHIFT", () => {
      this.player.sprint = true;
    });
    this.input.keyboard!.on("keyup-SHIFT", () => {
      this.player.sprint = false;
    });
  }

  update() {
    // Arrow keys
    if (this.cursors.left.isDown) {
      this.player.setVelocityX(-160);
    } else if (this.cursors.right.isDown) {
      this.player.setVelocityX(160);
    } else {
      this.player.setVelocityX(0);
    }

    // Jump
    if (this.cursors.up.isDown && this.player.body!.touching.down) {
      this.player.setVelocityY(-330);
    }

    // WASD alternative
    if (this.wasd.A.isDown) {
      this.player.setVelocityX(-160);
    }

    // Single key check
    if (Phaser.Input.Keyboard.JustDown(this.jumpKey)) {
      this.player.jump();
    }

    // Shoot while held
    if (this.shootKey.isDown) {
      this.player.shoot();
    }
  }
}
```

### Level 2: Mouse and Touch Input

```typescript
create() {
  // Pointer (unified mouse/touch)
  this.input.on('pointermove', (pointer: Phaser.Input.Pointer) => {
    this.player.rotation = Phaser.Math.Angle.Between(
      this.player.x, this.player.y,
      pointer.x, pointer.y
    );
  });

  this.input.on('pointerdown', (pointer: Phaser.Input.Pointer) => {
    this.shoot(pointer.x, pointer.y);
  });

  // Dragging game objects
  const box = this.add.image(400, 300, 'box');
  box.setInteractive({ draggable: true });

  this.input.setDraggable([box]);

  this.input.on('drag', (pointer: any, gameObject: Phaser.GameObjects.Image, dragX: number, dragY: number) => {
    gameObject.x = dragX;
    gameObject.y = dragY;
  });

  // Click-specific detection
  this.input.on('gameobjectdown', (pointer: any, gameObject: any) => {
    gameObject.setTint(0xff0000);
  });

  // Zone interaction
  const zone = this.add.zone(400, 300, 200, 200);
  zone.setInteractive({ useHandCursor: true });
  zone.on('pointerover', () => {
    zone.setFillStyle(0x444444);
  });
  zone.on('pointerout', () => {
    zone.setFillStyle(0x000000);
  });
}
```

### Level 3: Virtual Joystick for Mobile

```typescript
export class GameScene extends Phaser.Scene {
  private joystick!: {
    base: Phaser.GameObjects.Image;
    knob: Phaser.GameObjects.Image;
  };
  private joystickActive = false;
  private joystickPointerId: number | null = null;
  private joystickVector = { x: 0, y: 0 };

  create() {
    // Only show on touch devices
    if (this.sys.game.device.os.android || this.sys.game.device.os.iOS) {
      this.createVirtualJoystick();
    }
  }

  createVirtualJoystick() {
    const joyX = 100;
    const joyY = this.scale.height - 100;
    const radius = 50;

    // Joystick base
    const base = this.add.circle(joyX, joyY, radius, 0x444444, 0.5);
    base.setScrollFactor(0);
    base.setDepth(1000);

    // Joystick knob
    const knob = this.add.circle(joyX, joyY, 20, 0x888888, 0.8);
    knob.setScrollFactor(0);
    knob.setDepth(1001);

    this.joystick = { base, knob };

    // Touch input for joystick
    this.input.on("pointerdown", (pointer: Phaser.Input.Pointer) => {
      const dist = Phaser.Math.Distance.Between(
        pointer.x,
        pointer.y,
        joyX,
        joyY,
      );
      if (dist < radius && this.joystickPointerId === null) {
        this.joystickActive = true;
        this.joystickPointerId = pointer.id;
      }
    });

    this.input.on("pointermove", (pointer: Phaser.Input.Pointer) => {
      if (this.joystickActive && pointer.id === this.joystickPointerId) {
        const angle = Phaser.Math.Angle.Between(
          joyX,
          joyY,
          pointer.x,
          pointer.y,
        );
        const dist = Math.min(
          Phaser.Math.Distance.Between(joyX, joyY, pointer.x, pointer.y),
          radius,
        );

        this.joystick.knob.x = joyX + Math.cos(angle) * dist;
        this.joystick.knob.y = joyY + Math.sin(angle) * dist;

        // Normalized vector (-1 to 1)
        this.joystickVector.x = (this.joystick.knob.x - joyX) / radius;
        this.joystickVector.y = (this.joystick.knob.y - joyY) / radius;
      }
    });

    this.input.on("pointerup", (pointer: Phaser.Input.Pointer) => {
      if (pointer.id === this.joystickPointerId) {
        this.joystickActive = false;
        this.joystickPointerId = null;
        this.joystick.knob.x = joyX;
        this.joystick.knob.y = joyY;
        this.joystickVector = { x: 0, y: 0 };
      }
    });
  }

  update() {
    if (this.joystickActive) {
      this.player.setVelocity(
        this.joystickVector.x * this.player.speed,
        this.joystickVector.y * this.player.speed,
      );
    }
  }
}
```

### Level 4: Gamepad Support

```typescript
create() {
  // Gamepad is auto-enabled in Phaser 3

  // Check for gamepad connection
  this.input.gamepad!.on('connected', (gamepad: Phaser.Input.Gamepad.Gamepad) => {
    console.log('Gamepad connected:', gamepad.id);
  });

  this.input.gamepad!.on('disconnected', (gamepad: Phaser.Input.Gamepad.Gamepad) => {
    console.log('Gamepad disconnected:', gamepad.id);
  });
}

update() {
  const pads = this.input.gamepad!.gamepads;

  for (let i = 0; i < pads.length; i++) {
    const pad = pads[i];

    if (!pad || !pad.connected) continue;

    // Left stick
    if (pad.axes.length >= 2) {
      const axisX = pad.axes[0].getValue(); // -1 to 1
      const axisY = pad.axes[1].getValue();
      this.player.setVelocity(axisX * 200, axisY * 200);
    }

    // D-pad
    if (pad.buttons[12]?.isDown) this.player.setVelocityY(-160); // Up
    if (pad.buttons[13]?.isDown) this.player.setVelocityY(160);  // Down
    if (pad.buttons[14]?.isDown) this.player.setVelocityX(-160); // Left
    if (pad.buttons[15]?.isDown) this.player.setVelocityX(160);  // Right

    // Face buttons
    if (pad.buttons[0]?.isDown) this.player.jump();  // A/X
    if (pad.buttons[1]?.isDown) this.player.shoot(); // B/O

    // Shoulders
    if (pad.buttons[4]?.isDown) this.player.previousWeapon(); // L1
    if (pad.buttons[5]?.isDown) this.player.nextWeapon();     // R1
  }
}
```

### Level 5: Input Manager Class

```typescript
class InputManager {
  private keyboard: { cursors: Phaser.Types.Input.Keyboard.CursorKeys; wasd: any };
  private gamepadIndex = 0;
  private virtualJoystick = { active: false, x: 0, y: 0 };

  constructor(private scene: Phaser.Scene) {
    this.setupKeyboard();
    this.setupGamepad();
    this.setupVirtualControls();
  }

  private setupKeyboard() {
    this.keyboard = {
      cursors: this.scene.input.keyboard!.createCursorKeys(),
      wasd: this.scene.input.keyboard!.addKeys('W,A,S,D')
    };
  }

  private setupGamepad() {
    this.scene.input.gamepad!.on('connected', () => {
      this.gamepadIndex = 0;
    });
  }

  private setupVirtualControls() {
    if (this.scene.sys.game.device.os.android ||
        this.scene.sys.game.device.os.iOS) {
      // Setup virtual joystick (see Level 3)
    }
  }

  getMovement(): { x: number; y: number } {
    // Gamepad first
    const pad = this.scene.input.gamepad!.getPad(this.gamepadIndex);
    if (pad && pad.connected && pad.axes.length >= 2) {
      return {
        x: pad.axes[0].getValue(),
        y: pad.axes[1].getValue()
      };
    }

    // Virtual joystick second
    if (this.virtualJoystick.active) {
      return {
        x: this.virtualJoystick.x,
        y: this.virtualJoystick.y
      };
    }

    // Keyboard fallback
    let x = 0, y = 0;
    if (this.keyboard.cursors.left.isDown || this.keyboard.wasd.A.isDown) x = -1;
    if (this.keyboard.cursors.right.isDown || this.keyboard.wasd.D.isDown) x = 1;
    if (this.keyboard.cursors.up.isDown || this.keyboard.wasd.W.isDown) y = -1;
    if (this.keyboard.cursors.down.isDown || this.keyboard.wasd.S.isDown) y = 1;

    return { x, y };
  }

  isJumpPressed(): boolean {
    return this.keyboard.cursors.up.isDown ||
           this.keyboard.wasd.W.isDown ||
           (this.scene.input.gamepad!.getPad(this.gamepadIndex)?.buttons[0]?.isDown);
  }

  isAttackJustPressed(): boolean {
    return Phaser.Input.Keyboard.JustDown(
      this.scene.input.keyboard!.addKey('SPACE')
    ) || this.scene.input.gamepad!.getPad(this.gamepadIndex)?.buttons[1]?.justDown;
  }
}

// In scene
create() {
  this.inputManager = new InputManager(this);
}

update() {
  const move = this.inputManager.getMovement();
  this.player.setVelocity(move.x * 200, move.y * 200);

  if (this.inputManager.isJumpPressed()) {
    this.player.jump();
  }
}
```

## Anti-Patterns

❌ **DON'T:**

- Create new Key objects every frame - reuse from create()
- Ignore JustDown/JustUp for trigger actions
- Mix coordinate systems for input
- Forget pointer ID for multi-touch
- Hardcode only keyboard input
- Use polling for all input (use events when appropriate)

✅ **DO:**

- Create keys once in create()
- Use JustDown/JustUp for one-shot actions
- Normalize input vectors
- Track pointer IDs for multi-touch
- Support multiple input methods
- Combine event listeners with polling

## Code Patterns

### Key Combination Detection

```typescript
// Ctrl+Z to undo
this.input.keyboard!.on("keydown-Z", () => {
  const ctrlKey = this.input.keyboard!.checkDown(
    this.input.keyboard!.addKey("CTRL"),
    100,
  );

  if (ctrlKey) {
    this.undo();
  }
});

// Double tap detection
let lastTapTime = 0;
this.input.on("pointerdown", () => {
  const now = this.time.now;
  if (now - lastTapTime < 300) {
    this.doubleTap();
  }
  lastTapTime = now;
});
```

### Smooth Input Damping

```typescript
update() {
  // Smooth movement with lerp
  const targetX = this.input.activePointer.x;
  const targetY = this.input.activePointer.y;

  this.player.x = Phaser.Math.Linear(this.player.x, targetX, 0.1);
  this.player.y = Phaser.Math.Linear(this.player.y, targetY, 0.1);
}
```

## Checklist

- [ ] Keys created in create() not update()
- [ ] JustDown/JustUp used for triggers
- [ ] Multi-touch handled correctly
- [ ] Gamepad fallback to keyboard
- [ ] Virtual controls for mobile
- [ ] Input vectors normalized
- [ ] Dead zones applied to analog input

## Reference

- [Phaser Input](https://photonstorm.github.io/phaser3-docs/Phaser.Input.InputPlugin.html) — Input system
- [Keyboard Plugin](https://photonstorm.github.io/phaser3-docs/Phaser.Input.Keyboard.KeyboardPlugin.html) — Keyboard API
- [Gamepad Plugin](https://photonstorm.github.io/phaser3-docs/Phaser.Input.Gamepad.GamepadPlugin.html) — Gamepad API
