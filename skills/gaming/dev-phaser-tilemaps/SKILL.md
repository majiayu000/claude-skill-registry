---
name: dev-phaser-tilemaps
description: Tilemap loading, parsing, layers, and collision detection
---

# Phaser Tilemaps

> "Build expansive worlds with tile-based maps from Tiled."

## Before/After: Manual Level Building vs Tiled Integration

### ❌ Before: Manual Level Data Management

```typescript
// Manual tilemap without Tiled integration
interface Tile {
  x: number;
  y: number;
  type: string;
  solid: boolean;
}

interface Level {
  tiles: Tile[];
  width: number;
  height: number;
  spawn: { x: number; y: number };
}

// Hardcoded level data
const level1: Level = {
  tiles: [
    { x: 0, y: 0, type: 'grass', solid: false },
    { x: 1, y: 0, type: 'grass', solid: false },
    { x: 2, y: 0, type: 'wall', solid: true },
    // ... hundreds more entries
  ],
  width: 50,
  height: 50,
  spawn: { x: 100, y: 100 }
};

class LevelRenderer {
  private tileImages: Map<string, HTMLImageElement> = new Map();

  constructor(private canvas: HTMLCanvasElement) {
    // Load tile images manually
    this.loadTile('grass', 'assets/tiles/grass.png');
    this.loadTile('wall', 'assets/tiles/wall.png');
    this.loadTile('water', 'assets/tiles/water.png');
  }

  async loadTile(type: string, path: string) {
    const img = new Image();
    img.src = path;
    await new Promise(resolve => img.onload = resolve);
    this.tileImages.set(type, img);
  }

  render(level: Level, cameraX: number, cameraY: number) {
    const ctx = this.canvas.getContext('2d')!;

    // Manual culling - only draw visible tiles
    for (const tile of level.tiles) {
      const screenX = tile.x * 32 - cameraX;
      const screenY = tile.y * 32 - cameraY;

      // Culling check
      if (screenX < -32 || screenX > this.canvas.width ||
          screenY < -32 || screenY > this.canvas.height) {
        continue;
      }

      const img = this.tileImages.get(tile.type);
      if (img) {
        ctx.drawImage(img, screenX, screenY);
      }
    }
  }

  // Manual collision detection
  getTileAt(x: number, y: number, level: Level): Tile | null {
    const tileX = Math.floor(x / 32);
    const tileY = Math.floor(y / 32);
    return level.tiles.find(t => t.x === tileX && t.y === tileY) || null;
  }

  isSolid(x: number, y: number, level: Level): boolean {
    const tile = this.getTileAt(x, y, level);
    return tile?.solid || false;
  }
}

// Problems:
// - Hardcoded level data is unmaintainable
// - No visual editor for level design
// - Manual tile culling is error-prone
// - No layer support (parallax, foreground)
// - Manual collision detection for each tile
// - No object layer support (spawn points, enemies)
// - Hard to add new tiles or change layouts
```

### ✅ After: Tiled + Phaser Tilemap System

```typescript
// Tiled + Phaser handles everything automatically
export class GameScene extends Phaser.Scene {
  private map!: Phaser.Tilemaps.Tilemap;

  preload() {
    // Load Tiled JSON export - ONE line!
    this.load.tilemapTiledJSON('dungeon', 'assets/tilemaps/dungeon.json');
    this.load.image('dungeon_tiles', 'assets/tilesets/dungeon.png');
  }

  create() {
    // Create tilemap from Tiled - ONE line!
    this.map = this.make.tilemap({ key: 'dungeon' });

    // Add tileset - matches Tiled project name!
    const tileset = this.map.addTilesetImage('Dungeon Tiles', 'dungeon_tiles');

    // Create layers automatically from Tiled layers!
    const bgLayer = this.map.createLayer('Background', tileset);
    const wallsLayer = this.map.createLayer('Walls', tileset);
    const fgLayer = this.map.createLayer('Foreground', tileset);

    // Set collision from Tiled properties - ONE line!
    wallsLayer.setCollisionByProperty({ collides: true });

    // Player collides with walls - ONE line!
    this.physics.add.collider(this.player, wallsLayer);

    // Spawn player from Tiled object layer
    const spawnPoint = this.map.findObject('Objects', obj => obj.type === 'player');
    this.player.setPosition(spawnPoint.x, spawnPoint.y);

    // Spawn enemies from object layer
    this.map.createFromObjects('Objects', 'enemy', {
      key: 'enemy',
      frame: 0
    });

    // Parallax with scrollFactor - built-in!
    bgLayer.setScrollFactor(0.5);  // Background
    wallsLayer.setScrollFactor(1);  // Main layer
    fgLayer.setScrollFactor(1.2);   // Foreground

    // Camera bounds from map size - ONE line!
    this.cameras.main.setBounds(
      0, 0,
      this.map.widthInPixels,
      this.map.heightInPixels
    );
  }
}

// Benefits:
// - Visual level editor (Tiled)
// - JSON export for easy version control
// - Automatic culling and rendering
// - Multiple layers with depth sorting
// - Built-in collision detection
// - Object layers for entities
// - Tile properties for custom behavior
// - Supports isometric, hexagonal, orthogonal
```

## When to Use This Skill

Use when:

- Creating platformer levels
- Building isometric worlds
- Designing large game environments
- Working with Tiled Map Editor
- Implementing tile-based collision

## Quick Start

```typescript
preload() {
  this.load.tilemapTiledJSON('map', 'assets/level1.json');
  this.load.image('tiles', 'assets/tileset.png');
}

create() {
  const map = this.make.tilemap({ key: 'map' });
  const tileset = map.addTilesetImage('ground', 'tiles');
  const layer = map.createLayer('Ground', tileset);
  layer.setCollisionByExclusion([-1]);
}
```

## Decision Framework

| Need              | Use                             |
| ----------------- | ------------------------------- |
| Tiled JSON export | `load.tilemapTiledJSON()`       |
| Collision layer   | `setCollisionByExclusion([-1])` |
| Tile properties   | `setTileIndexCallback()`        |
| Isometric view    | Tiled isometric orientation     |
| Object layer      | `map.createFromObjects()`       |

## Progressive Guide

### Level 1: Basic Tilemap Loading

```typescript
export class GameScene extends Phaser.Scene {
  private map!: Phaser.Tilemaps.Tilemap;
  private tileset!: Phaser.Tilemaps.Tileset;
  private groundLayer!: Phaser.Tilemaps.DynamicTilemapLayer;
  private wallsLayer!: Phaser.Tilemaps.DynamicTilemapLayer;

  preload() {
    // Load tilemap JSON (exported from Tiled)
    this.load.tilemapTiledJSON("dungeon", "assets/tilemaps/dungeon.json");

    // Load tileset image
    this.load.image("dungeon_tiles", "assets/tilesets/dungeon.png");
  }

  create() {
    // Create tilemap
    this.map = this.make.tilemap({ key: "dungeon" });

    // Add tileset image (first param: name in Tiled, second: image key)
    this.tileset = this.map.addTilesetImage("Dungeon Tiles", "dungeon_tiles");

    // Create layers
    this.groundLayer = this.map.createLayer("Ground", this.tileset);
    this.wallsLayer = this.map.createLayer("Walls", this.tileset);
  }
}
```

### Level 2: Tile Collision

```typescript
create() {
  this.map = this.make.tilemap({ key: 'dungeon' });
  this.tileset = this.map.addTilesetImage('Dungeon Tiles', 'dungeon_tiles');

  // Create layer
  const walls = this.map.createLayer('Walls', this.tileset);

  // Set collision for ALL tiles
  walls.setCollisionByProperty({ collides: true });

  // Alternative: Set collision by exclusion (all except index -1)
  walls.setCollisionByExclusion([-1]);

  // Set collision for specific tile indices
  walls.setCollision([1, 2, 3, 4]);

  // Create player
  const player = this.physics.add.sprite(100, 100, 'player');
  player.setCollideWorldBounds(true);

  // Add collision between player and tilemap layer
  this.physics.add.collider(player, walls);

  // Visualize collision (debug)
  // walls.renderDebug(this.add.graphics());
}
```

### Level 3: Tile Properties and Callbacks

```typescript
create() {
  this.map = this.make.tilemap({ key: 'level' });
  this.tileset = this.map.addTilesetImage('tiles', 'tiles');
  const worldLayer = this.map.createLayer('World', this.tileset);

  // Set collision from tile properties
  worldLayer.setCollisionByProperty({ collides: true });

  // Tile index callback (trigger when tile touched)
  worldLayer.setTileIndexCallback(
    5, // Tile index
    this.lavaCallback,
    this
  );

  // Tile location callback
  worldLayer.setTileLocationCallback(
    10, 10, // x, y
    5, 5,   // width, height
    this.coinCallback,
    this
  );
}

lavaCallback(sprite: Phaser.Types.Physics.Arcade.GameObjectWithBody, tile: Phaser.Tilemaps.Tile) {
  // Player touched lava tile
  const player = sprite as Phaser.Physics.Arcade.Sprite;
  this.handlePlayerDeath(player);
}

coinCallback(sprite: Phaser.Types.Physics.Arcade.GameObjectWithBody, tile: Phaser.Tilemaps.Tile) {
  // Remove coin tile
  const layer = tile.tilemapLayer;
  layer.removeTileAt(tile.x, tile.y);

  // Add score
  this.score += 10;
}
```

### Level 4: Object Layers

```typescript
create() {
  this.map = this.make.tilemap({ key: 'level' });
  this.tileset = this.map.addTilesetImage('tiles', 'tiles');

  // Create from object layer
  const objects = this.map.getObjectLayer('Objects');

  if (objects) {
    // Create sprites from objects
    objects.objects.forEach((obj: any) => {
      if (obj.type === 'player') {
        this.spawnPlayer(obj.x, obj.y);
      } else if (obj.type === 'enemy') {
        this.spawnEnemy(obj.x, obj.y, obj.properties);
      } else if (obj.type === 'coin') {
        this.spawnCoin(obj.x, obj.y);
      }
    });
  }

  // Alternative: createFromObjects
  const coins = this.map.createFromObjects('Objects', 'coin', {
    key: 'coin',
    frame: 0
  });

  // Add physics to created objects
  this.physics.add.group(coins);
}
```

### Level 5: Advanced Tilemap Techniques

```typescript
export class GameScene extends Phaser.Scene {
  private map!: Phaser.Tilemaps.Tilemap;
  private layers: Phaser.Tilemaps.DynamicTilemapLayer[] = [];

  create() {
    this.map = this.make.tilemap({ key: "large_level" });
    this.tileset = this.map.addTilesetImage("tiles", "tiles");

    // Multiple layers
    const bgLayer = this.map.createLayer("Background", this.tileset);
    const decorLayer = this.map.createLayer("Decoration", this.tileset);
    const mainLayer = this.map.createLayer("Main", this.tileset);
    const fgLayer = this.map.createLayer("Foreground", this.tileset);

    // Layer depth for parallax
    bgLayer.setScrollFactor(0.5);
    decorLayer.setScrollFactor(0.75);
    mainLayer.setScrollFactor(1);
    fgLayer.setScrollFactor(1.25);

    // Set collision
    mainLayer.setCollisionByProperty({ collides: true });
    fgLayer.setCollisionByProperty({ collides: true });

    // Create player with tile collision
    const player = this.physics.add.sprite(100, 100, "player");
    this.physics.add.collider(player, mainLayer);
    this.physics.add.collider(player, fgLayer);

    // Dynamic tile replacement
    this.setupTileInteraction(mainLayer, player);

    // Camera bounds from tilemap size
    this.cameras.main.setBounds(
      0,
      0,
      this.map.widthInPixels,
      this.map.heightInPixels,
    );
  }

  setupTileInteraction(
    layer: Phaser.Tilemaps.DynamicTilemapLayer,
    player: any,
  ) {
    // Pointer to click tiles
    this.input.on("pointerdown", (pointer: Phaser.Input.Pointer) => {
      const tile = layer.getTileAtWorldXY(pointer.x, pointer.y);

      if (tile) {
        console.log("Tile:", tile.index, "Properties:", tile.properties);

        // Replace tile
        if (tile.properties.breakable) {
          layer.removeTileAt(tile.x, tile.y);
          this.spawnParticles(tile.pixelX, tile.pixelY);
        }
      }
    });

    // Tile animation
    const animatedTiles = [{ index: 10, frames: [10, 11, 12], frameRate: 5 }];

    animatedTiles.forEach((anim) => {
      this.map.tiles[anim.index] = {
        animation: anim.frames.map((frame) => ({
          frame,
          duration: anim.frameRate,
        })),
      };
    });
  }

  // Raycasting for visibility
  isTileVisibleFrom(
    fromX: number,
    fromY: number,
    toX: number,
    toY: number,
  ): boolean {
    const layer = this.layers[0];
    const line = new Phaser.Geom.Line(fromX, fromY, toX, toY);
    const tiles = layer.getTilesWithinShape(line);

    // Check if any blocking tile between points
    return !tiles.some((tile) => tile.properties.blocksSight);
  }

  // Procedural tile placement
  fillAreaWithTiles(
    layerIndex: number,
    x: number,
    y: number,
    w: number,
    h: number,
    tileIndex: number,
  ) {
    const layer = this.layers[layerIndex];
    for (let ty = y; ty < y + h; ty++) {
      for (let tx = x; tx < x + w; tx++) {
        layer.putTileAt(tileIndex, tx, ty);
      }
    }
  }
}
```

## Anti-Patterns

❌ **DON'T:**

- Create tilemap without adding tileset
- Forget to set collision on tiles
- Use wrong tileset name from Tiled
- Assume tilemap coordinate system matches pixel coordinates
- Create large tilemaps without culling
- Load tilemaps without compression

✅ **DO:**

- Match tileset name to Tiled project
- Set collision properties in Tiled or code
- Use `tile.pixelX/Y` for pixel positions
- Enable camera culling for large maps
- Use JSON compression for tilemaps
- Cache tilemap lookups when possible

## Code Patterns

### Tile Properties from Tiled

```
In Tiled, set tile properties:
- collides: true
- dangerous: true
- animates: true
- frameRate: 5
```

```typescript
// Access properties
layer.setCollisionByProperty({ collides: true });

// Custom property callback
layer.setTileLocationCallback(
  0,
  0,
  map.width,
  map.height,
  (sprite, tile) => {
    if (tile.properties.dangerous) {
      this.hurtPlayer(sprite);
    }
  },
  this,
);
```

### Parallax Tilemap Layers

```typescript
create() {
  const bgLayer = map.createLayer('Background', tileset);
  const midLayer = map.createLayer('Midground', tileset);
  const fgLayer = map.createLayer('Foreground', tileset);

  // Parallax scrolling
  bgLayer.setScrollFactor(0.2); // Far background
  midLayer.setScrollFactor(0.5); // Mid ground
  fgLayer.setScrollFactor(1);   // Foreground (normal)
}
```

### Tilemap Bounds

```typescript
create() {
  // Set camera bounds to tilemap size
  this.cameras.main.setBounds(
    0, 0,
    this.map.widthInPixels,
    this.map.heightInPixels
  );

  // Set world bounds
  this.physics.world.setBounds(
    0, 0,
    this.map.widthInPixels,
    this.map.heightInPixels
  );
}
```

## Tilemap Methods Reference

| Method                             | Description                    |
| ---------------------------------- | ------------------------------ |
| `createLayer(name, tileset)`       | Create layer from tilemap      |
| `setCollisionByProperty(props)`    | Set collision from properties  |
| `setCollisionByExclusion(indices)` | Set collision except specified |
| `setTileIndexCallback(index, fn)`  | Callback when tile touched     |
| `getTileAt(x, y)`                  | Get tile at grid coordinates   |
| `getTileAtWorldXY(x, y)`           | Get tile at pixel coordinates  |
| `putTileAt(index, x, y)`           | Place tile at grid coordinates |
| `removeTileAt(x, y)`               | Remove tile                    |
| `swapTiles(indexA, indexB)`        | Swap all tiles of two types    |

## Checklist

- [ ] Tileset image loaded before tilemap
- [ ] Tileset name matches Tiled project
- [ ] Collision set on appropriate tiles
- [ ] Camera bounds set for large maps
- [ ] Object layers processed
- [ ] Tile callbacks configured
- [ ] Layer depth set for parallax

## Reference

- [Tiled Map Editor](https://www.mapeditor.org/) — Tilemap creation tool
- [Phaser Tilemaps](https://photonstorm.github.io/phaser3-docs/Phaser.Tilemaps.Tilemap.html) — Tilemap API
- [Tiled JSON Format](https://doc.mapeditor.org/en/stable/reference/json-map-format/) — Export format
