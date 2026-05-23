---
name: dev-phaser-ui-creation
description: UI containers, text objects, buttons, and DOM element integration
---

# Phaser UI Creation

> "Build responsive game UI with Phaser's UI components."

## Before/After: HTML DOM UI vs Phaser UI System

### ❌ Before: Pure HTML DOM UI

```typescript
// Pure HTML/CSS UI without Phaser integration
class GameUI {
  private container: HTMLElement;
  private scoreElement: HTMLElement;
  private healthFillElement: HTMLElement;
  private buttons: HTMLElement[] = [];

  constructor() {
    // Create UI container
    this.container = document.createElement('div');
    this.container.id = 'game-ui';
    this.container.style.position = 'absolute';
    this.container.style.top = '0';
    this.container.style.left = '0';
    this.container.style.width = '100%';
    this.container.style.pointerEvents = 'none'; // Let clicks pass through
    document.body.appendChild(this.container);

    // Score display
    this.scoreElement = document.createElement('div');
    this.scoreElement.className = 'score-display';
    this.scoreElement.textContent = 'Score: 0';
    this.container.appendChild(this.scoreElement);

    // Health bar
    const healthBar = document.createElement('div');
    healthBar.className = 'health-bar';
    healthBar.innerHTML = `
      <div class="health-bg">
        <div class="health-fill"></div>
      </div>
    `;
    this.container.appendChild(healthBar);
    this.healthFillElement = healthBar.querySelector('.health-fill')!;

    // Add CSS manually
    const style = document.createElement('style');
    style.textContent = `
      .score-display {
        position: absolute;
        top: 16px;
        left: 16px;
        font-size: 32px;
        font-family: Arial;
        color: white;
        text-shadow: 2px 2px 0 black;
      }
      .health-bar {
        position: absolute;
        top: 60px;
        left: 16px;
        width: 200px;
        height: 20px;
      }
      .health-bg {
        width: 100%;
        height: 100%;
        background: #333;
        border: 2px solid white;
      }
      .health-fill {
        width: 100%;
        height: 100%;
        background: #0f0;
        transition: width 0.2s;
      }
    `;
    document.head.appendChild(style);

    // Buttons need pointer events
    const startButton = document.createElement('button');
    startButton.textContent = 'Start Game';
    startButton.style.pointerEvents = 'auto';
    startButton.onclick = () => this.onStartGame();
    this.container.appendChild(startButton);
    this.buttons.push(startButton);

    // Manual sync with game state
    // Manual responsive positioning
    // No scene lifecycle integration
  }

  updateScore(score: number) {
    this.scoreElement.textContent = `Score: ${score}`;
  }

  updateHealth(current: number, max: number) {
    const percent = (current / max) * 100;
    this.healthFillElement.style.width = `${percent}%`;
  }

  // Manual cleanup required
  destroy() {
    this.container.remove();
  }

  // No integration with Phaser scenes
  // Manual positioning for camera
  // No depth sorting with game objects
}

// Problems:
// - No integration with Phaser scenes
// - Manual DOM manipulation
// - Separate CSS file or inline styles
// - No access to Phaser textures
// - Can't use Phaser tweens on UI
// - Manual sync with game state
// - No depth control vs game objects
// - Performance: separate render layer
```

### ✅ After: Phaser UI System

```typescript
// Phaser UI is fully integrated
export class UIScene extends Phaser.Scene {
  private scoreText!: Phaser.GameObjects.Text;
  private healthBar!: Phaser.GameObjects.Graphics;

  create() {
    // Score text - ONE line!
    this.scoreText = this.add.text(16, 16, 'Score: 0', {
      fontSize: '32px',
      fontFamily: 'Arial',
      color: '#ffffff',
      fontStyle: 'bold',
      stroke: '#000000',
      strokeThickness: 4
    });

    // Health bar with Phaser graphics
    this.healthBar = this.add.graphics();
    this.updateHealth(100, 100);

    // Button with built-in interaction
    const startBtn = this.add.text(400, 300, 'Start Game', {
      backgroundColor: '#4444ff',
      color: '#ffffff',
      fontSize: '24px',
      padding: { x: 20, y: 10 }
    });
    startBtn.setOrigin(0.5);
    startBtn.setInteractive({ useHandCursor: true }); // Built-in cursor!

    // Hover effects with tweens!
    startBtn.on('pointerover', () => {
      this.tweens.add({
        targets: startBtn,
        scale: 1.05,
        duration: 100
      });
      startBtn.setStyle({ backgroundColor: '#6666ff' });
    });

    startBtn.on('pointerout', () => {
      this.tweens.add({
        targets: startBtn,
        scale: 1,
        duration: 100
      });
      startBtn.setStyle({ backgroundColor: '#4444ff' });
    });

    startBtn.on('pointerdown', () => {
      this.scene.start('GameScene');
    });

    // Fixed HUD - doesn't move with camera!
    this.cameras.main.ignore([this.scoreText, this.healthBar, startBtn]);
    // Or use setScrollFactor(0) for individual elements
  }

  updateHealth(current: number, max: number) {
    this.healthBar.clear();

    // Background
    this.healthBar.fillStyle(0x333333);
    this.healthBar.fillRect(16, 60, 200, 20);

    // Fill with color based on health
    const percent = current / max;
    const color = percent > 0.5 ? 0x00ff00 :
                  percent > 0.25 ? 0xffff00 : 0xff0000;

    this.healthBar.fillStyle(color);
    this.healthBar.fillRect(16, 60, 200 * percent, 20);

    // Border
    this.healthBar.lineStyle(2, 0xffffff);
    this.healthBar.strokeRect(16, 60, 200, 20);
  }

  // Method called from game scene
  updateScore(score: number) {
    this.scoreText.setText(`Score: ${score}`);

    // Score pop effect!
    this.tweens.add({
      targets: this.scoreText,
      scale: 1.2,
      duration: 100,
      yoyo: true
    });
  }
}

// Benefits:
// - Full Phaser scene integration
// - Uses Phaser rendering (no separate DOM)
// - Access to all Phaser features (tweens, cameras)
// - Can use game textures in UI
// - Built-in interactive states
// - Automatic cleanup on scene shutdown
// - Depth control with game objects
// - Single render pass (better performance)
```

## When to Use This Skill

Use when:

- Creating game HUDs and menus
- Building interactive buttons
- Displaying score and health
- Implementing dialog boxes
- Integrating HTML/CSS UI overlays

## Quick Start

```typescript
create() {
  // Text object
  const score = this.add.text(16, 16, 'Score: 0', {
    fontSize: '32px',
    color: '#fff'
  });

  // Interactive button
  const button = this.add.text(400, 300, 'Start', {
    backgroundColor: '#00f',
    padding: { x: 10, y: 5 }
  });
  button.setOrigin(0.5);
  button.setInteractive();
  button.on('pointerdown', () => this.startGame());
}
```

## Decision Framework

| Need            | Use                           |
| --------------- | ----------------------------- |
| Simple text     | `add.text()`                  |
| Styling text    | Text style config             |
| Interactive UI  | `setInteractive()`            |
| Complex layouts | Container or HTML overlay     |
| Responsive UI   | Scale manager + resize events |

## Progressive Guide

### Level 1: Text and Basic UI

```typescript
export class UIScene extends Phaser.Scene {
  private scoreText!: Phaser.GameObjects.Text;
  private healthBar!: Phaser.GameObjects.Graphics;
  private health = 100;
  private maxHealth = 100;

  create() {
    // Score display
    this.scoreText = this.add.text(16, 16, "Score: 0", {
      fontSize: "32px",
      fontFamily: "Arial",
      color: "#ffffff",
      fontStyle: "bold",
    });

    // Health bar background
    this.healthBar = this.add.graphics();
    this.updateHealthBar();

    // Timer text
    const timerText = this.add.text(this.scale.width - 16, 16, "Time: 60", {
      fontSize: "24px",
      color: "#ffff00",
    });
    timerText.setOrigin(1, 0);
  }

  updateScore(score: number) {
    this.scoreText.setText(`Score: ${score}`);
  }

  updateHealthBar() {
    this.healthBar.clear();

    // Background
    this.healthBar.fillStyle(0x333333);
    this.healthBar.fillRect(16, 60, 200, 20);

    // Health fill
    const healthPercent = this.health / this.maxHealth;
    const color =
      healthPercent > 0.5
        ? 0x00ff00
        : healthPercent > 0.25
          ? 0xffff00
          : 0xff0000;

    this.healthBar.fillStyle(color);
    this.healthBar.fillRect(16, 60, 200 * healthPercent, 20);

    // Border
    this.healthBar.lineStyle(2, 0xffffff);
    this.healthBar.strokeRect(16, 60, 200, 20);
  }
}
```

### Level 2: Interactive Buttons

```typescript
export class MenuScene extends Phaser.Scene {
  create() {
    // Button background style
    const buttonStyle = {
      backgroundColor: "#4444ff",
      color: "#ffffff",
      fontSize: "24px",
      padding: { x: 20, y: 10 },
      borderRadius: 5,
    };

    const hoverStyle = {
      backgroundColor: "#6666ff",
      color: "#ffff00",
    };

    // Create buttons
    const startBtn = this.createButton(400, 200, "Start Game", buttonStyle);
    startBtn.on("pointerdown", () => {
      this.scene.start("GameScene");
    });

    const optionsBtn = this.createButton(400, 280, "Options", buttonStyle);
    optionsBtn.on("pointerdown", () => {
      this.scene.launch("OptionsScene");
    });

    const quitBtn = this.createButton(400, 360, "Quit", buttonStyle);
    quitBtn.on("pointerdown", () => {
      this.game.destroy(true);
    });
  }

  createButton(
    x: number,
    y: number,
    text: string,
    style: any,
  ): Phaser.GameObjects.Text {
    const button = this.add.text(x, y, text, style);
    button.setOrigin(0.5);
    button.setInteractive({ useHandCursor: true });

    // Hover effect
    button.on("pointerover", () => {
      button.setStyle({ backgroundColor: "#6666ff", color: "#ffff00" });
      button.setScale(1.05);
    });

    button.on("pointerout", () => {
      button.setStyle({ backgroundColor: "#4444ff", color: "#ffffff" });
      button.setScale(1);
    });

    // Click effect
    button.on("pointerdown", () => {
      button.setScale(0.95);
    });

    button.on("pointerup", () => {
      button.setScale(1.05);
    });

    return button;
  }
}
```

### Level 3: UI Containers

```typescript
export class UIScene extends Phaser.Scene {
  create() {
    // Container for HUD elements
    const hudContainer = this.add.container(0, 0);

    // Health display
    const healthBg = this.add.rectangle(20, 20, 200, 20, 0x333333);
    const healthFill = this.add.rectangle(20, 20, 180, 16, 0x00ff00);
    healthFill.setOrigin(0, 0.5);

    const healthText = this.add.text(120, 20, "100/100", {
      fontSize: "14px",
      color: "#fff",
    });
    healthText.setOrigin(0.5);

    // Score display
    const scoreLabel = this.add.text(20, 50, "Score:", {
      fontSize: "16px",
      color: "#aaa",
    });

    const scoreValue = this.add.text(80, 50, "0", {
      fontSize: "16px",
      color: "#fff",
    });

    // Add to container
    hudContainer.add([
      healthBg,
      healthFill,
      healthText,
      scoreLabel,
      scoreValue,
    ]);

    // Make container fixed (doesn't move with camera)
    hudContainer.setScrollFactor(0);
  }
}
```

### Level 4: Dialog Box

```typescript
export class DialogScene extends Phaser.Scene {
  private dialogBox!: Phaser.GameObjects.Container;
  private dialogText!: Phaser.GameObjects.Text;
  private continueText!: Phaser.GameObjects.Text;
  private isTyping = false;
  private typingSpeed = 30;

  create() {
    // Semi-transparent overlay
    const overlay = this.add.rectangle(
      this.scale.width / 2,
      this.scale.height / 2,
      this.scale.width,
      this.scale.height,
      0x000000,
      0.5,
    );

    // Dialog background
    const dialogBg = this.add.rectangle(
      this.scale.width / 2,
      this.scale.height - 100,
      this.scale.width - 40,
      180,
      0x333344,
    );
    dialogBg.setStrokeStyle(3, 0x666677);

    // Dialog text
    this.dialogText = this.add.text(
      this.scale.width / 2,
      this.scale.height - 130,
      "",
      {
        fontSize: "18px",
        color: "#ffffff",
        align: "left",
        wordWrap: { width: this.scale.width - 80 },
      },
    );
    this.dialogText.setOrigin(0.5, 0);

    // Continue prompt
    this.continueText = this.add.text(
      this.scale.width / 2,
      this.scale.height - 40,
      "Press SPACE to continue",
      {
        fontSize: "14px",
        color: "#aaaaaa",
      },
    );
    this.continueText.setOrigin(0.5);
    this.continueText.setVisible(false);

    // Group into container
    this.dialogBox = this.add.container(0, 0);
    this.dialogBox.add([dialogBg, this.dialogText, this.continueText]);
    this.dialogBox.setScrollFactor(0);

    // Input to continue
    const spaceKey = this.input.keyboard!.addKey("SPACE");
    spaceKey.on("down", () => this.advanceDialog());
  }

  showDialog(text: string) {
    this.dialogText.setText("");
    this.continueText.setVisible(false);
    this.isTyping = true;

    let index = 0;
    const timer = this.time.addEvent({
      delay: this.typingSpeed,
      repeat: text.length - 1,
      callback: () => {
        index++;
        this.dialogText.setText(text.substring(0, index));

        if (index >= text.length) {
          this.isTyping = false;
          this.continueText.setVisible(true);
          timer.destroy();
        }
      },
    });
  }

  advanceDialog() {
    if (this.isTyping) {
      // Skip typing animation
      this.time.removeAllEvents();
      this.isTyping = false;
      this.continueText.setVisible(true);
    } else {
      // Show next dialog (or close)
      this.scene.stop();
    }
  }
}
```

### Level 5: HTML DOM Integration

```typescript
export class GameScene extends Phaser.Scene {
  private domElement!: HTMLElement;

  create() {
    // Create HTML overlay
    this.domElement = this.add
      .dom(this.scale.width / 2, this.scale.height / 2)
      .createElement("div");

    this.domElement.setHTML(`
      <div class="ui-overlay">
        <h1>Game Paused</h1>
        <button id="resume-btn">Resume</button>
        <button id="quit-btn">Quit</button>
      </div>
    `);

    // Add CSS
    this.domElement.setStyle(`
      .ui-overlay {
        background: rgba(0, 0, 0, 0.8);
        padding: 40px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-family: Arial, sans-serif;
      }
      h1 { margin: 0 0 20px 0; }
      button {
        padding: 10px 20px;
        margin: 5px;
        font-size: 16px;
        cursor: pointer;
        background: #4444ff;
        color: white;
        border: none;
        border-radius: 5px;
      }
      button:hover {
        background: #6666ff;
      }
    `);

    // Hide initially
    this.domElement.setVisible(false);

    // Button handlers
    this.domElement.addListener("resume-btn").on("click", () => {
      this.resumeGame();
    });

    this.domElement.addListener("quit-btn").on("click", () => {
      this.quitGame();
    });
  }

  showPauseMenu() {
    this.domElement.setVisible(true);
    this.scene.pause();
  }

  resumeGame() {
    this.domElement.setVisible(false);
    this.scene.resume();
  }

  quitGame() {
    this.scene.start("TitleScene");
  }
}
```

## Anti-Patterns

❌ **DON'T:**

- Create UI elements in update()
- Forget to set scrollFactor(0) for HUD
- Use hardcoded positions for responsive UI
- Ignore touch sizes on mobile
- Create too many DOM elements
- Mix coordinate systems arbitrarily

✅ **DO:**

- Create UI once in create()
- Fix HUD with scrollFactor(0)
- Use scale manager for positioning
- Make buttons large enough for touch
- Minimize DOM usage
- Keep UI coordinates consistent

## Code Patterns

### Responsive UI Positioning

```typescript
create() {
  // Position relative to screen size
  const scoreText = this.add.text(
    this.scale.width * 0.02,  // 2% from left
    this.scale.height * 0.02, // 2% from top
    'Score: 0'
  );

  // Handle resize
  this.scale.on('resize', (gameSize: Phaser.Structs.Size) => {
    scoreText.setPosition(
      gameSize.width * 0.02,
      gameSize.height * 0.02
    );
  });
}
```

### Text Styling Presets

```typescript
const TEXT_STYLES = {
  HEADER: {
    fontSize: "48px",
    fontFamily: "Arial",
    color: "#ffffff",
    fontStyle: "bold",
    stroke: "#000000",
    strokeThickness: 4,
  },
  BODY: {
    fontSize: "18px",
    fontFamily: "Arial",
    color: "#cccccc",
    align: "center",
  },
  BUTTON: {
    fontSize: "24px",
    fontFamily: "Arial",
    color: "#ffffff",
    backgroundColor: "#4444ff",
    padding: { x: 20, y: 10 },
  },
};
```

### Custom Button Class

```typescript
class Button extends Phaser.GameObjects.Container {
  private background: Phaser.GameObjects.Rectangle;
  private text: Phaser.GameObjects.Text;

  constructor(
    scene: Phaser.Scene,
    x: number,
    y: number,
    width: number,
    height: number,
    text: string,
    onClick: () => void,
  ) {
    super(scene, x, y);
    scene.add.existing(this);

    // Background
    this.background = scene.add.rectangle(0, 0, width, height, 0x4444ff);
    this.background.setStrokeStyle(2, 0x6666ff);
    this.background.setInteractive({ useHandCursor: true });

    // Text
    this.text = scene.add.text(0, 0, text, {
      fontSize: "20px",
      color: "#ffffff",
    });
    this.text.setOrigin(0.5);

    this.add([this.background, this.text]);

    // Events
    this.background.on("pointerover", () => this.onHover());
    this.background.on("pointerout", () => this.onOut());
    this.background.on("pointerdown", () => this.onDown());
    this.background.on("pointerup", () => {
      this.onUp();
      onClick();
    });
  }

  onHover() {
    this.background.setFillStyle(0x6666ff);
  }

  onOut() {
    this.background.setFillStyle(0x4444ff);
  }

  onDown() {
    this.setScale(0.95);
  }

  onUp() {
    this.setScale(1);
  }
}
```

## UI Text Style Properties

| Property          | Type   | Description                   |
| ----------------- | ------ | ----------------------------- |
| `fontFamily`      | string | Font name                     |
| `fontSize`        | string | Size with unit (e.g., '24px') |
| `color`           | string | Text color (hex)              |
| `fontStyle`       | string | 'bold', 'italic', etc.        |
| `align`           | string | 'left', 'center', 'right'     |
| `backgroundColor` | string | Background color              |
| `padding`         | object | { x, y } padding              |
| `lineSpacing`     | number | Space between lines           |
| `stroke`          | string | Outline color                 |
| `strokeThickness` | number | Outline width                 |
| `shadow`          | object | Shadow config                 |
| `wordWrap`        | object | { width } for wrapping        |

## Checklist

- [ ] UI created in create() not update()
- [ ] HUD elements have scrollFactor(0)
- [ ] Buttons are interactive
- [ ] Touch targets large enough (44px min)
- [ ] Text styles defined consistently
- [ ] Responsive positions handled
- [ ] DOM elements cleaned up on shutdown

## Reference

- [Game Objects](https://photonstorm.github.io/phaser3-docs/Phaser.GameObjects.GameObjectFactory.html) — Object creation
- [Text Object](https://photonstorm.github.io/phaser3-docs/Phaser.GameObjects.Text.html) — Text API
- [Container](https://photonstorm.github.io/phaser3-docs/Phaser.GameObjects.Container.html) — Container API
