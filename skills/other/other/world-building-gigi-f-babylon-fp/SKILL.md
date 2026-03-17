---
name: World Building & Grid System
description: Understanding the game world structure, grid-based building system, NPC definitions, and spatial organization. Use when working with maps, buildings, spawns, or world layout.
---

# World Building & Grid System

## Overview
Babylon FP uses a grid-based world system where buildings, NPCs, and spawns are placed on a precise coordinate grid. The world is designed in a top-down 2D grid that translates to 3D space in Babylon.js.

## Grid System Architecture

### Coordinate System
```typescript
// Grid coordinates (2D editor view)
gridX: number  // Horizontal position (0-99 default)
gridY: number  // Vertical position (0-99 default)

// World coordinates (3D game space)
worldX: number  // X position in 3D (gridX - gridSize/2)
worldZ: number  // Z position in 3D (gridY - gridSize/2)
worldY: number  // Height (usually 0 for ground level)

// Conversion formulas
worldX = (gridX - gridSize / 2) * CELL_SIZE
worldZ = (gridY - gridSize / 2) * CELL_SIZE
```

### Grid Properties
```typescript
GRID_CELL_SIZE = 1.0    // Each cell = 1 unit in world space
DEFAULT_GRID_SIZE = 100  // 100x100 grid
WORLD_SIZE = 100        // 100x100 units in 3D space
```

### Center Point
```
Grid (50, 50) = World (0, 0, 0)
Grid origin (0, 0) = World (-50, 0, -50)
Grid max (99, 99) = World (49, 0, 49)
```

## Building Types

### 1. Walls (`type: "wall"`)
**Properties**:
- Size: 1x1 grid cell
- Rotation: 0°, 90°, 180°, 270°
- Color: #666 (gray)
- Collision: Solid, blocks movement
- Height: Full height (blocks line of sight)

**Placement**:
```json
{
  "type": "wall",
  "position": {"x": 10, "y": 0, "z": 5},
  "gridPosition": {"x": 60, "y": 55},
  "rotation": 0
}
```

### 2. Floors (`type: "floor"`)
**Properties**:
- Size: 1x1 grid cell
- No rotation (flat surface)
- Color: #ddd (light gray)
- Collision: Walkable
- Visual: Ground plane

**Purpose**: Define walkable areas, rooms, paths

### 3. Doors (`type: "door"`)
**Properties**:
- Size: 2x1 grid cells (wide enough for player)
- Rotation: Determines which direction it spans
- Color: #8B4513 (brown)
- Interactive: Can open/close
- Width: 2.0 units

**Door System** (`src/systems/doorSystem.ts`):
```typescript
- Proximity detection (1.5 unit range)
- Automatic open when player approaches
- Smooth animation (pivot rotation)
- Collision updates (passable when open)
```

### 4. Windows (`type: "window"`)
**Properties**:
- Size: 1x1 grid cell
- Rotation: 0°, 90°, 180°, 270°
- Color: #87CEEB (sky blue)
- Collision: Solid
- Visual: Semi-transparent

**Purpose**: Visual detail, natural light, line of sight

### 5. Player Spawn (`type: "player-spawn"`)
**Properties**:
- Size: 1x1 grid cell
- Rotation: Initial facing direction
  - 0° = South (down)
  - 90° = West (left)
  - 180° = North (up)
  - 270° = East (right)
- Color: #FF4444 (red)
- Unique: Only one per map

**Default Spawn**: Center of map (gridX: 50, gridY: 50)

### 6. NPC Spawn (`type: "npc-spawn"`)
**Properties**:
- Size: 1x1 grid cell
- Rotation: Initial facing direction
- Color: Dynamic based on NPC type
- Has `npcId` property
- Has optional `schedule` property

**NPC Colors**:
```typescript
baker: #D2691E  (tan/brown)
guard: #4169E1  (royal blue)
thief: #8B8B8B  (gray)
// Custom colors from NPC editor
```

## Map Structure

### Map JSON Format
```json
{
  "metadata": {
    "gridSize": 100,
    "cellSize": 1,
    "worldSize": 100,
    "version": "1.0.0"
  },
  "buildings": [
    {
      "type": "wall",
      "position": {"x": 10, "y": 0, "z": 5},
      "gridPosition": {"x": 60, "y": 55},
      "rotation": 0
    }
  ],
  "spawns": {
    "player": [
      {"x": 0, "y": 0, "z": 0, "rotation": 0}
    ],
    "npcs": [
      {
        "x": 10, "y": 0, "z": 10,
        "npcId": "baker",
        "rotation": 0,
        "schedule": {
          "21600": {"x": 10, "y": 0, "z": 10},
          "28800": {"x": 15, "y": 0, "z": 15}
        }
      }
    ]
  }
}
```

### Map Files
```
public/data/maps/
  └── world.json          - Main game world
```

## NPC System

### NPC Definition Format
NPCs are defined in individual JSON files:

```json
{
  "id": "baker",
  "name": "Bread Baker",
  "color": [0.82, 0.41, 0.12],      // Skin color RGB (0-1)
  "shirtColor": [1.0, 1.0, 1.0],    // Shirt color RGB
  "height": 1.8,
  "hasHat": true,
  "hatColor": [1.0, 1.0, 1.0],
  "dialogue": {
    "greeting": "Fresh bread today!",
    "investigation": "I saw someone near the bakery last night..."
  }
}
```

### NPC Files
```
public/data/npcs/
  ├── baker.json
  ├── guard.json
  ├── beggar.json
  └── [custom NPCs]
```

### NPC Visual Properties
```typescript
// Body
- Height: 1.5 - 2.0 units
- Width: 0.5 units
- Color: Skin tone from color array

// Clothing
- Shirt: Covers torso
- Color: shirtColor array

// Accessories
- Hat: Optional (hasHat: true/false)
- Hat Color: Custom or white default
- Hat Style: Cylinder on top of head
```

### NPC Behavior
- Follow schedules (see Time System skill)
- Interpolate between waypoints
- Face direction of movement
- Can have dialogue trees
- Can be photographed for evidence

## Map Editor (`tools/map-editor.html`)

### Features
**Grid Canvas**:
- Visual 100x100 grid
- Zoom: 1x to 5x
- Pan: Middle mouse button
- Cell size: 10px per grid cell (base)

**Tools**:
1. **Select** (👆) - Click NPCs to edit schedules
2. **Wall** (🧱) - Place walls
3. **Floor** (⬜) - Place floor tiles
4. **Door** (🚪) - Place 2-cell doors
5. **Window** (🪟) - Place windows
6. **NPC Spawn** (👤) - Place NPCs with schedules
7. **Player Spawn** (🎮) - Place player start
8. **Erase** (❌) - Remove tiles

**Drag Painting**: Wall, Floor, Window, Erase support click-and-drag

**Rotation**: R key or dropdown (0°, 90°, 180°, 270°)

**Schedule Editor**:
- Opens automatically when NPC selected
- Click on grid to add waypoints
- Each waypoint has time (HH:MM format)
- Visual path between waypoints
- Editable times in list
- Save & Close button

**Import/Export**:
- Export: Generates JSON with all tiles and schedules
- Import: Load existing maps with full state restoration
- Copy to clipboard or download file

### Grid Rendering
```typescript
// Colors
Background: #1a1a1a (dark)
Grid lines: #333 (subtle)
Labels: Every 10 cells

// Tile display
- Colored squares for buildings
- Green arrow for rotation indicator
- Red tiles for schedule waypoints
- Dashed lines connecting waypoints
```

## World Building Workflow

### 1. Design Phase
```
1. Plan layout on paper/grid
2. Define rooms and spaces
3. Decide NPC locations and schedules
4. Plan crime/investigation locations
```

### 2. Map Creation
```
1. Open map-editor.html
2. Place walls to define rooms
3. Add floors inside rooms
4. Place doors for entrances
5. Add windows for detail
6. Place player spawn (center or custom)
```

### 3. NPC Placement
```
1. Click NPC Spawn tool
2. Select NPC type from modal
3. Click on grid to place
4. Schedule editor opens automatically
5. Add waypoints by clicking grid cells
6. Assign times to each waypoint
7. Save & Close
```

### 4. Testing
```
1. Export map JSON
2. Save to public/data/maps/world.json
3. Launch game (npm run dev)
4. Test player spawn location
5. Verify NPCs follow schedules
6. Test door interactions
7. Check collision/navigation
```

### 5. Iteration
```
1. Import existing map
2. Make adjustments
3. Re-export and test
4. Repeat until satisfied
```

## Spatial Organization

### Building Patterns

**Simple Room**:
```
WWWWW
W...W  (W=Wall, .=Floor, D=Door)
W...W
W.D.W
WWWWW
```

**House with Window**:
```
WWWWWW
W....W
W....W
W..#.W  (#=Window)
WW.DWW
```

**Street/Path**:
```
.......  (Floor tiles for walkable path)
.......
```

### NPC Spawn Placement
```
- Home locations: Inside buildings
- Work locations: Shops, workplaces
- Patrol routes: Streets, alleys
- Social spots: Town square, market
```

## Collision & Physics

### Collision Types
```typescript
Solid (blocks all):
- Walls
- Windows
- NPCs (soft collision)

Walkable:
- Floors
- Open doors
- Empty grid cells

Interactive:
- Doors (open/close)
- NPCs (dialogue)
```

### Player Movement
```typescript
- WASD/Arrow keys
- Mouse look
- Collision with walls
- Walk through open doors
- Cannot overlap NPCs
```

## Development Commands

### List all maps
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
ls -lh public/data/maps/*.json
```

### List all NPCs
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
ls -1 public/data/npcs/*.json | xargs -I {} basename {} .json
```

### Count buildings in map
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
node -e "const map = require('./public/data/maps/world.json'); console.log('Buildings:', map.buildings?.length || 0, '\nNPCs:', map.spawns?.npcs?.length || 0)"
```

### Validate map JSON
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
node -e "JSON.parse(require('fs').readFileSync('public/data/maps/world.json'))" && echo "✓ Valid JSON"
```

## Related Files
```
tools/map-editor.html           - Visual map editor (2000+ lines)
tools/npc-editor.html           - NPC creator/editor
public/data/maps/world.json     - Main game map
public/data/npcs/*.json         - NPC definitions
src/systems/doorSystem.ts       - Door interaction
src/systems/npcSystem.ts        - NPC movement/rendering
src/config/gameConfig.ts        - World constants
```

## Best Practices

### Map Design
- ✅ Leave open spaces for movement
- ✅ Create clear pathways with floors
- ✅ Use doors wide enough (2 cells)
- ✅ Place player spawn in accessible area
- ✅ Test NPC pathfinding routes
- ❌ Don't create isolated areas
- ❌ Don't place spawns inside walls

### NPC Schedules
- ✅ Start at 6:00 AM (morning)
- ✅ Use realistic time gaps (15+ min)
- ✅ Create logical routes (home→work→home)
- ✅ Avoid overlapping NPCs at same spot
- ✅ End near starting position
- ❌ Don't use times outside 6 AM - 10 PM
- ❌ Don't create impossible jumps (teleportation)

### Performance
- Limit total tiles to reasonable count (<1000)
- Reuse floor patterns rather than individual tiles
- Keep NPC count manageable (<20)
- Simple building shapes render faster
