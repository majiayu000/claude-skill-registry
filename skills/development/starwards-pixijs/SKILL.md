---
name: starwards-pixijs
description: PixiJS v8 patterns for Starwards - Containers, Sprites, Graphics, Textures, ticker integration, event handling, and testing with Playwright data-id selectors
version: 2025-12-02
related_skills:
  - starwards-tdd (test rendering with E2E)
  - starwards-debugging (debug rendering issues)
  - starwards-verification (verify visual output)
---

# PixiJS v8 Development for Starwards

## Overview

Starwards uses PixiJS v8 (^8.14.0) for 2D rendering in the browser module. This skill covers both the PixiJS v8 API reference and Starwards-specific patterns.

**Core principle:** Layered container composition with ticker-driven updates synced to Colyseus state changes.

## Table of Contents

1. [PixiJS v8 Reference](#pixijs-v8-reference)
   - [Application](#application)
   - [Containers & Scene Graph](#containers--scene-graph)
   - [Sprites](#sprites)
   - [Graphics (v8 API)](#graphics-v8-api)
   - [Text](#text)
   - [Textures & Assets](#textures--assets)
   - [Ticker](#ticker)
   - [Events / Interaction](#events--interaction)
   - [Performance Tips](#performance-tips)
   - [v8 Migration Guide](#v8-migration-highlights)
2. [Starwards Patterns](#starwards-patterns)
   - [CameraView Application](#cameraview-application)
   - [Layer System](#layer-system)
   - [Graphics Patterns](#starwards-graphics-patterns)
   - [Event Handling](#starwards-event-handling)
   - [Object Pooling](#object-pooling)
   - [Testing with Playwright](#testing-with-playwright)

---

# PixiJS v8 Reference

## Application

The `Application` class provides an extensible entry point for PixiJS projects.

### Async Initialization (v8 Required)

```typescript
import { Application } from 'pixi.js';

const app = new Application();

await app.init({
  width: 800,
  height: 600,
  backgroundColor: 0x1099bb,
});

document.body.appendChild(app.canvas);
```

### Key Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `width` | `number` | `800` | Initial width |
| `height` | `number` | `600` | Initial height |
| `backgroundColor` | `ColorSource` | `'black'` | Background color |
| `antialias` | `boolean` | - | Enable anti-aliasing |
| `resolution` | `number` | `1` | Pixel resolution |
| `resizeTo` | `Window \| HTMLElement` | - | Auto-resize target |
| `preference` | `'webgl' \| 'webgpu'` | `'webgl'` | Renderer type |

---

## Containers & Scene Graph

### Creating Containers

```typescript
import { Container } from 'pixi.js';

const container = new Container({
  x: 100,
  y: 100,
});

app.stage.addChild(container);
```

### Parent-Child Relationships

- Children inherit transforms, alpha, visibility from parents
- Render order: children render in insertion order (later = on top)
- Use `setChildIndex()` or `zIndex` with `sortableChildren` for reordering

### Coordinate Systems

```typescript
// Local to global
const globalPos = obj.toGlobal(new Point(0, 0));

// Global to local
const localPos = container.toLocal(new Point(100, 100));
```

### Culling

```typescript
container.cullable = true;        // Enable culling
container.cullableChildren = true; // Cull children recursively
container.cullArea = new Rectangle(0, 0, 400, 400); // Custom cull bounds
```

---

## Sprites

### Basic Usage

```typescript
import { Sprite, Assets } from 'pixi.js';

const texture = await Assets.load('bunny.png');
const sprite = new Sprite(texture);

sprite.anchor.set(0.5);  // Center anchor
sprite.x = 100;
sprite.y = 100;
sprite.tint = 0xff0000;  // Red tint
sprite.alpha = 0.8;
```

### Sprite Properties

| Property | Description |
|----------|-------------|
| `texture` | The texture to display |
| `anchor` | Origin point (0-1 range) |
| `tint` | Color tint |
| `blendMode` | Blend mode for compositing |
| `width`, `height` | Size (scales texture) |

---

## Graphics (v8 API)

**CRITICAL:** v8 uses a new fluent API. Build shapes first, then fill/stroke.

### v8 Fluent API

```typescript
import { Graphics } from 'pixi.js';

// Draw shape, then fill/stroke
const graphics = new Graphics()
  .rect(50, 50, 100, 100)
  .fill(0xff0000)
  .stroke({ width: 2, color: 'white' });

// Circle with fill and stroke
const circle = new Graphics()
  .circle(100, 100, 50)
  .fill({ color: 0x00ff00, alpha: 0.5 })
  .stroke({ width: 3, color: 0x000000 });
```

### Shape Methods

| v7 (OLD) | v8 (NEW) |
|----------|----------|
| `drawRect()` | `rect()` |
| `drawCircle()` | `circle()` |
| `drawEllipse()` | `ellipse()` |
| `drawRoundedRect()` | `roundRect()` |
| `drawPolygon()` | `poly()` |
| `drawStar()` | `star()` |

### Lines

```typescript
const lines = new Graphics()
  .moveTo(0, 0)
  .lineTo(100, 100)
  .lineTo(200, 0)
  .stroke({ width: 2, color: 0xff0000 });
```

### Holes (v8)

```typescript
const rectWithHole = new Graphics()
  .rect(0, 0, 100, 100)
  .fill(0x00ff00)
  .circle(50, 50, 20)
  .cut();  // Creates hole
```

### GraphicsContext (Sharing)

```typescript
import { GraphicsContext, Graphics } from 'pixi.js';

const context = new GraphicsContext()
  .rect(0, 0, 100, 100)
  .fill(0xff0000);

const g1 = new Graphics(context);
const g2 = new Graphics(context); // Shares same data
```

---

## Text

### Basic Text

```typescript
import { Text, TextStyle } from 'pixi.js';

const text = new Text({
  text: 'Hello World',
  style: {
    fontFamily: 'Arial',
    fontSize: 24,
    fill: 0xffffff,
    align: 'center',
  },
});
```

### TextStyle Properties

| Property | Description |
|----------|-------------|
| `fontFamily` | Font name |
| `fontSize` | Size in pixels |
| `fill` | Fill color |
| `stroke` | Stroke settings |
| `align` | Text alignment |
| `wordWrap` | Enable word wrapping |
| `wordWrapWidth` | Wrap width |

### BitmapText (Performance)

```typescript
import { BitmapText } from 'pixi.js';

const bitmapText = new BitmapText({
  text: 'Score: 1000',
  style: { fontFamily: 'MyBitmapFont', fontSize: 32 },
});
```

---

## Textures & Assets

### Loading Assets

```typescript
import { Assets, Sprite } from 'pixi.js';

// Single asset
const texture = await Assets.load('path/to/image.png');
const sprite = new Sprite(texture);

// Multiple assets
const textures = await Assets.load(['a.png', 'b.png']);

// With alias
await Assets.load({ alias: 'hero', src: 'images/hero.png' });
const heroTexture = Assets.get('hero');
```

### Asset Bundles

```typescript
Assets.addBundle('game', [
  { alias: 'player', src: 'player.png' },
  { alias: 'enemy', src: 'enemy.png' },
]);

const assets = await Assets.loadBundle('game');
```

### Manifest

```typescript
const manifest = {
  bundles: [
    {
      name: 'load-screen',
      assets: [{ alias: 'bg', src: 'background.png' }],
    },
    {
      name: 'game',
      assets: [{ alias: 'hero', src: 'hero.png' }],
    },
  ],
};

await Assets.init({ manifest });
await Assets.loadBundle('load-screen');
```

### SVGs

```typescript
// As texture
const svgTexture = await Assets.load('icon.svg');
const sprite = new Sprite(svgTexture);

// As Graphics (scalable)
const svgContext = await Assets.load({
  src: 'icon.svg',
  data: { parseAsGraphicsContext: true },
});
const graphics = new Graphics(svgContext);
```

### Texture Cleanup

```typescript
// Unload from cache and GPU
await Assets.unload('texture.png');

// Unload from GPU only (keep in memory)
texture.source.unload();

// Destroy texture
texture.destroy();
```

---

## Ticker

### Basic Usage

```typescript
import { Ticker, UPDATE_PRIORITY } from 'pixi.js';

// Using app ticker
app.ticker.add((ticker) => {
  sprite.rotation += 0.1 * ticker.deltaTime;
});

// One-time callback
app.ticker.addOnce((ticker) => {
  console.log('Called once');
});

// With priority (higher runs first)
app.ticker.add(updateFn, null, UPDATE_PRIORITY.HIGH);
```

### Priority Constants

- `UPDATE_PRIORITY.HIGH = 50`
- `UPDATE_PRIORITY.NORMAL = 0`
- `UPDATE_PRIORITY.LOW = -50`

### FPS Control

```typescript
app.ticker.maxFPS = 60;  // Cap framerate
app.ticker.minFPS = 30;  // Clamp deltaTime
```

### Ticker Properties

| Property | Description |
|----------|-------------|
| `deltaTime` | Scaled frame delta |
| `elapsedMS` | Raw milliseconds since last frame |
| `FPS` | Current frames per second |

---

## Events / Interaction

### Event Modes

```typescript
sprite.eventMode = 'static';  // Interactive, non-moving
sprite.eventMode = 'dynamic'; // Interactive, moving (receives idle events)
sprite.eventMode = 'passive'; // Default, children can be interactive
sprite.eventMode = 'none';    // No interaction
```

### Pointer Events

```typescript
sprite.eventMode = 'static';

sprite.on('pointerdown', (event) => {
  console.log('Clicked at', event.global.x, event.global.y);
});

sprite.on('pointermove', (event) => { /* ... */ });
sprite.on('pointerup', (event) => { /* ... */ });
sprite.on('pointerover', (event) => { /* ... */ });
sprite.on('pointerout', (event) => { /* ... */ });
```

### Hit Area

```typescript
import { Rectangle, Circle } from 'pixi.js';

sprite.hitArea = new Rectangle(0, 0, 100, 100);
// or
sprite.hitArea = new Circle(50, 50, 50);
```

### Custom Cursor

```typescript
sprite.cursor = 'pointer';
sprite.cursor = 'grab';
sprite.cursor = 'url(cursor.png), auto';
```

### Disable Children Interaction

```typescript
container.interactiveChildren = false; // Skip children hit testing
```

---

## Performance Tips

### Sprites
- Use spritesheets to minimize texture switches
- Sprites batch with up to 16 textures per batch
- Draw order matters for batching efficiency

### Graphics
- Graphics are fastest when not modified after creation
- Small Graphics (<100 points) batch like sprites
- Use sprites with textures for complex shapes

### Text
- Avoid updating text every frame (expensive)
- Use BitmapText for frequently changing text
- Lower `resolution` for less memory

### Masks
- Rectangle masks (scissor) are fastest
- Graphics masks (stencil) are second fastest
- Sprite masks (filters) are expensive

### Filters
- Release with `container.filters = null`
- Set `filterArea` for known dimensions
- Use sparingly - each filter adds draw calls

### General
- Enable culling for large scenes: `cullable = true`
- Use `RenderGroups` for static content
- Set `interactiveChildren = false` for non-interactive containers

---

## v8 Migration Highlights

### Key Changes

1. **Async Initialization Required**
```typescript
// OLD (v7)
const app = new Application({ width: 800 });

// NEW (v8)
const app = new Application();
await app.init({ width: 800 });
```

2. **Graphics API Changed**
```typescript
// OLD (v7)
graphics.beginFill(0xff0000).drawRect(0, 0, 100, 100).endFill();

// NEW (v8)
graphics.rect(0, 0, 100, 100).fill(0xff0000);
```

3. **Ticker Callback**
```typescript
// OLD (v7)
ticker.add((dt) => sprite.rotation += dt);

// NEW (v8)
ticker.add((ticker) => sprite.rotation += ticker.deltaTime);
```

4. **Application Canvas**
```typescript
// OLD (v7)
app.view

// NEW (v8)
app.canvas
```

5. **Leaf Nodes Can't Have Children**
- `Sprite`, `Graphics`, `Mesh` etc. can no longer have children
- Use `Container` as parent instead

6. **getBounds Returns Bounds**
```typescript
// OLD (v7)
const rect = container.getBounds();

// NEW (v8)
const rect = container.getBounds().rectangle;
```

---

# Starwards Patterns

## CameraView Application

Starwards extends `Application` for radar/tactical views.

**Location:** `modules/browser/src/radar/camera-view.ts`

```typescript
import { Application, ApplicationOptions, Container } from 'pixi.js';

export class CameraView extends Application {
  constructor(public camera: Camera) {
    super();
  }

  public async initialize(
    pixiOptions: Partial<ApplicationOptions>,
    container: WidgetContainer
  ) {
    await super.init(pixiOptions);

    // Limit FPS to prevent GPU heating
    this.ticker.maxFPS = 30;

    // Handle resize
    container.on('resize', () => {
      this.resizeView(container.width, container.height);
    });

    // Append canvas
    container.getElement().append(this.canvas);
  }

  // Coordinate transformations
  public worldToScreen = (w: XY) => this.camera.worldToScreen(this.renderer, w.x, w.y);
  public screenToWorld = (s: XY) => this.camera.screenToWorld(this.renderer, s.x, s.y);

  // Layer management
  public addLayer(child: Container) {
    this.stage.addChild(child);
  }
}
```

**Key patterns:**
- `ticker.maxFPS = 30` - Prevents excessive GPU usage
- Coordinate transforms: `worldToScreen()`, `screenToWorld()`
- Layer composition via `addLayer()`

---

## Layer System

Starwards uses a layer pattern where each layer has a `renderRoot` Container.

### GridLayer Example

**Location:** `modules/browser/src/radar/grid-layer.ts`

```typescript
import { Container, Graphics } from 'pixi.js';

export class GridLayer {
  private stage = new Container();
  private gridLines = new Graphics();

  constructor(private parent: CameraView) {
    this.parent.events.on('screenChanged', () => this.drawSectorGrid());
    this.stage.addChild(this.gridLines);
  }

  get renderRoot(): Container {
    return this.stage;
  }

  private drawSectorGrid() {
    // Clear and redraw
    this.gridLines.clear();

    // Draw lines using v8 API
    this.gridLines
      .moveTo(0, screen)
      .lineTo(this.parent.renderer.width, screen)
      .stroke({ width: 2, color: magnitude.color, alpha: 0.5 });
  }
}
```

**Pattern:**
- Each layer owns a `stage` Container
- Exposes via `renderRoot` getter
- Redraws on `screenChanged` event
- Uses `graphics.clear()` before redrawing

---

## Starwards Graphics Patterns

### v8 Fluent API Usage

```typescript
// Drawing selection rectangle
const graphics = new Graphics();
graphics
  .rect(min.x, min.y, width, height)
  .fill({ color: selectionColor, alpha: 0.2 })
  .stroke({ width: 1, color: selectionColor, alpha: 1 });

// Drawing grid lines
this.gridLines
  .moveTo(0, screenY)
  .lineTo(rendererWidth, screenY)
  .stroke({ width: 2, color: lineColor, alpha: 0.5 });
```

### Clear and Redraw Pattern

```typescript
private redraw() {
  this.graphics.clear();
  // ... draw new content
}
```

---

## Starwards Event Handling

**Location:** `modules/browser/src/radar/interactive-layer.ts`

### Setup

```typescript
import { Container, FederatedPointerEvent, Rectangle } from 'pixi.js';

export class InteractiveLayer {
  private stage = new Container();

  constructor(private parent: CameraView) {
    // Set cursor
    this.stage.cursor = 'crosshair';

    // Enable interaction
    this.stage.interactive = true;

    // Set hit area to full canvas
    this.stage.hitArea = new Rectangle(
      0, 0,
      this.parent.renderer.width,
      this.parent.renderer.height
    );

    // Register events
    this.stage.on('pointerdown', this.onPointerDown);
    this.stage.on('pointermove', this.onPointerMove);
    this.stage.on('pointerup', this.onPointerUp);

    // Update hit area on resize
    this.parent.events.on('screenChanged', () => {
      this.stage.hitArea = new Rectangle(
        0, 0,
        this.parent.renderer.width,
        this.parent.renderer.height
      );
    });
  }

  private onPointerDown = (event: FederatedPointerEvent) => {
    const screenPos = XY.clone(event.global);
    const worldPos = this.parent.screenToWorld(screenPos);
    // ... handle interaction
  };
}
```

**Key patterns:**
- `stage.interactive = true` enables events
- `stage.hitArea = new Rectangle(...)` defines clickable area
- Update hit area on resize
- Use `event.global` for screen coordinates
- Convert to world with `screenToWorld()`

---

## Object Pooling

**Location:** `modules/browser/src/radar/texts-pool.ts`

Starwards uses iterator-based pooling to reduce GC pressure.

```typescript
export class TextsPool {
  private texts: Text[] = [];

  constructor(private container: Container) {}

  *[Symbol.iterator]() {
    let index = 0;
    while (true) {
      if (index >= this.texts.length) {
        const text = new Text({ text: '', style: { ... } });
        this.texts.push(text);
        this.container.addChild(text);
      }
      const text = this.texts[index];
      text.visible = true;
      yield text;
      index++;
    }
  }

  return() {
    // Hide unused texts
    for (let i = this.usedCount; i < this.texts.length; i++) {
      this.texts[i].visible = false;
    }
  }
}

// Usage
const textsIterator = this.textsPool[Symbol.iterator]();
for (const item of items) {
  const text = textsIterator.next().value;
  text.text = item.label;
  text.x = item.x;
  text.y = item.y;
}
textsIterator.return(); // Hide unused
```

---

## Testing with Playwright

### Data Attributes

Add `data-id` to canvas elements for E2E testing:

```typescript
this.canvas.setAttribute('data-id', 'Tactical Radar');
```

### Playwright Selectors

```typescript
// Select canvas by data-id
const canvas = page.locator('[data-id="Tactical Radar"]');

// Get attribute values
const zoom = await canvas.getAttribute('data-zoom');
```

### RadarDriver Pattern

```typescript
class RadarDriver {
  constructor(private canvas: Locator) {}

  async getZoom() {
    return Number(await this.canvas.getAttribute('data-zoom'));
  }

  async setZoom(target: number) {
    await this.canvas.dispatchEvent('wheel', { deltaY: ... });
  }
}
```

### Testing Considerations

- No unit tests for PixiJS components (visual output)
- Use E2E tests with Playwright
- Test via data attributes, not rendered pixels
- Use `data-id` on Tweakpane panels: `page.locator('[data-id="Panel Name"]')`

---

## Quick Reference

| Task | Starwards Pattern |
|------|-------------------|
| Create layer | `class MyLayer { stage = new Container(); get renderRoot() { return this.stage; } }` |
| Draw graphics | `graphics.rect(...).fill({...}).stroke({...})` |
| Redraw | `graphics.clear(); // then draw` |
| Interactive | `stage.interactive = true; stage.hitArea = new Rectangle(...)` |
| Events | `stage.on('pointerdown', handler)` |
| Coords | `parent.worldToScreen(xy)`, `parent.screenToWorld(xy)` |
| FPS limit | `ticker.maxFPS = 30` |
| Test selector | `page.locator('[data-id="..."]')` |

---

## Common Pitfalls

1. **Using v7 Graphics API**
   - Wrong: `beginFill()`, `drawRect()`, `endFill()`
   - Right: `rect().fill().stroke()`

2. **Forgetting async init**
   - Wrong: `new Application({ width: 800 })`
   - Right: `await app.init({ width: 800 })`

3. **Adding children to Sprites**
   - v8 leaf nodes can't have children
   - Use Container as parent

4. **Not clearing Graphics**
   - Call `graphics.clear()` before redrawing

5. **Hit area not updated on resize**
   - Update `stage.hitArea` when canvas resizes

6. **SVGs not loading as textures**
   - Use `Texture.from()` for SVGs (GitHub issue #8694 workaround)
