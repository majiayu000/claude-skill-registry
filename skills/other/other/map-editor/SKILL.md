---
name: Map Editor Tool
description: Comprehensive guide for using the visual map editor. Use when designing game worlds, placing buildings, NPCs, or managing map JSON files.
---

# Map Editor Tool

## Overview

The Map Editor is a visual tool for designing buildings and placing objects in your Babylon.js game world. It uses a grid-based system where each cell represents 1 unit in the 3D world.

**Location**: `tools/map-editor.html`  
**Access**: Open directly in web browser - no server needed!

## Getting Started

### 1. Open the Map Editor

Simply open `tools/map-editor.html` in your web browser:

```bash
# From your project root
open tools/map-editor.html
# or
firefox tools/map-editor.html
# or copy the full path and open in browser
/home/gianfiorenzo/Documents/Vs\ Code/babylon_fp/tools/map-editor.html
```

### 2. Using the Tools

**Available Tools:**
- 🧱 **Wall** - Create solid walls for buildings (2 units wide × 1 unit deep × 3 units tall)
- ⬜ **Floor** - Create floor tiles (thin, walkable)
- 🚪 **Door** - Create doorways (2 units wide × 1 unit deep × 2.2 units tall, interactive in-game)
- 🪟 **Window** - Create windows (2 units wide × 1 unit deep × 1.5 units tall)
- 👤 **NPC Spawn** - Mark NPC spawn points
- 🎮 **Player Spawn** - Mark player spawn points
- ❌ **Erase** - Remove tiles

**How to Use:**
1. Click a tool button to select it (it will highlight green)
2. Click on the grid to place tiles
3. Use the Rotation dropdown or press 'R' to rotate (0°, 90°, 180°, 270°)
4. Click on existing tiles with the Erase tool to remove them
5. Hover over the grid to see coordinates

### 3. Grid System

- **Grid Size**: 100x100 by default (adjustable)
- **Cell Size**: 1 unit per cell
- **World Size**: 100x100 units total
- **Origin**: Center of the grid is world position (0, 0, 0)

**Coordinate Conversion:**
- Grid (50, 50) = World (0, 0) (center)
- Grid (0, 0) = World (-50, -50) (top-left corner)
- Grid (100, 100) = World (50, 50) (bottom-right corner)

### 4. Visual Features

#### Cursor Preview 👁️
- Semi-transparent preview of the tile you're about to place
- Shows exactly what the tile will look like before clicking
- Preview follows your mouse cursor in real-time
- Changes instantly when you switch tools or rotation

#### Orientation Indicators 🧭
All rotatable items show a **bright green line** on their "front" edge:

**Walls, Doors, Windows:**
- **0° (Horizontal)**: Green line on **bottom** edge (facing south)
- **90° (Vertical)**: Green line on **left** edge (facing west)
- **180°**: Green line on **top** edge (facing north)
- **270°**: Green line on **right** edge (facing east)

**NPC & Player Spawns:**
- Default orientation facing **south** (down) with green line on bottom

Already-placed tiles show a **darker green line** (more subtle) to indicate their orientation.

#### Erase Tool Visual ❌
- Shows a red X under cursor when erase tool is selected
- Clear visual indication of what will be deleted

### 5. Building Types

#### Walls
- Default height: 3 units
- Blocks player movement
- Used for building exteriors and interiors
- Rotatable: 0°, 90°, 180°, 270°

#### Floors
- Thin tiles (0.1 units high)
- Create interior floors or platforms
- Collision enabled
- Walkable

#### Doors
- Height: 2.2 units
- Width: 1.0 units (can occupy 2 grid units with rotation)
- Can be made interactive with the DoorSystem
- Initially blocks movement in-game
- Rotatable for proper wall orientation

#### Windows
- Placed higher on walls (1.5 units from top)
- Semi-transparent
- Blocks movement (glass)
- Rotatable for proper wall orientation

#### Spawn Points
- **Player Spawn**: Where the player starts (only one per map)
- **NPC Spawn**: Where NPCs are placed (link to NPC id in JSON)
- Include `npcId` in the JSON to link to specific NPC data

## Advanced Features

### Drag Painting 🎨
- **Left-click and drag** to paint multiple tiles quickly
- Works with: Wall, Floor, Window, and Erase tools
- Perfect for creating large areas without clicking repeatedly
- Release mouse button to stop painting

### NPC Schedule Editor 📅
- Automatically opens when you select/place an NPC
- Edit waypoint times, positions, and npc type
- Add, edit, or remove waypoints
- Time validation ensures consistent schedules
- Export/import preserves all schedule data

### Map Import/Export

#### Exporting Your Map
Once you've designed your map:

1. **Copy JSON**: Copies the map data to your clipboard
2. **Download JSON**: Downloads as a `.json` file
3. Save the file to `/public/data/maps/your_map_name.json`

#### Importing Maps
1. Click **Import JSON** button
2. Select a `.json` file from your computer
3. Map and all schedule data are restored
4. Existing data is replaced

## Rotation & Building Walls

### Wall Placement

#### Horizontal Wall (0° or 180°)
Place walls at grid positions with X-spacing of 2:
```
Grid: (0,0) → (2,0) → (4,0) → (6,0)
World: x=-50, x=-48, x=-46, x=-44
```

#### Vertical Wall (90° or 270°)
Place walls at grid positions with Y-spacing of 2:
```
Grid: (0,0) → (0,2) → (0,4) → (0,6)
World: z=-50, z=-48, z=-46, z=-44
```

#### Creating Corners
```
Horizontal wall at (0,0) rotation=0°
Vertical wall at (0,0) rotation=90°
Creates an L-shaped corner
```

### How Rotation Works

- **0°**: Horizontal (default) - 2 units wide along X-axis, 1 unit deep along Z-axis
- **90°**: Vertical - 1 unit wide along X-axis, 2 units deep along Z-axis
- **180°**: Horizontal (flipped)
- **270°**: Vertical (flipped)

## Loading Maps in Game

To load your map in the game:

1. Save your JSON file to `/public/data/maps/`
2. In `src/Game.ts`, uncomment and modify the map loading line:

```typescript
// In the init() method
await this.mapBuilder.loadMapFromFile('/data/maps/your_map_name.json');
```

## Tips for Organization

### Version Control
- Save maps as JSON files in `/public/data/maps/`
- Commit maps to git for team collaboration
- Use descriptive filenames

### Map Organization
Create separate maps for different areas:
- `town_center.json` - Main plaza
- `residential_01.json` - House group 1
- `bakery.json` - Bakery building
- `police_station.json` - Police station

### Naming Conventions
```
{area}_{building_type}_{variant}.json

Examples:
- downtown_shop_general.json
- downtown_shop_bakery.json
- residential_house_01.json
- plaza_fountain.json
```

### Map Metadata
Include metadata in your maps:

```json
{
  "metadata": {
    "gridSize": 100,
    "cellSize": 1,
    "worldSize": 100,
    "version": "1.0.0",
    "description": "Town bakery - single story building",
    "author": "Your Name",
    "created": "2025-10-15"
  },
  "tiles": [...],
  "spawns": [...],
  "schedules": [...]
}
```

## JSON Structure

### Complete Map Format
```json
{
  "metadata": {
    "gridSize": 100,
    "cellSize": 1,
    "description": "Bakery"
  },
  "tiles": [
    {
      "gridX": 10,
      "gridY": 15,
      "type": "wall",
      "rotation": 0
    }
  ],
  "spawns": [
    {
      "gridX": 20,
      "gridY": 25,
      "type": "npcSpawn",
      "npcId": "baker"
    }
  ],
  "schedules": [
    {
      "npcId": "baker",
      "waypoints": [
        {"time": "06:00", "gridX": 20, "gridY": 25},
        {"time": "09:00", "gridX": 15, "gridY": 20}
      ]
    }
  ]
}
```

## Advanced Usage

### Multi-Story Buildings
To create multi-story buildings:
1. Create multiple floor plans as separate map files
2. Load them with different Y offsets in code
3. Or modify positions before building in code

### Complex Structures
For complex buildings:
1. Start with the outer walls
2. Add interior walls to create rooms
3. Place floors
4. Add doors and windows
5. Mark spawn points for NPCs

### Performance Tips
- Keep maps under 500 tiles for best performance
- Use floor tiles sparingly (they add geometry)
- Group related structures in separate map files
- Reuse maps with position offsets for similar buildings

## Example Workflow

1. **Sketch**: Draw your building layout on paper
2. **Design**: Open map editor and create the structure
3. **Place NPCs**: Click NPC Spawn, edit schedule in modal
4. **Export**: Download JSON file
5. **Save**: Move to `/public/data/maps/`
6. **Test**: Load in game and walk through
7. **Iterate**: Adjust and refine
8. **Commit**: Save to version control

## Troubleshooting

**Map doesn't load in game:**
- Check browser console for errors
- Verify JSON syntax is valid
- Ensure file path in Game.ts is correct
- Check the file exists in `/public/data/maps/`

**Walls overlap or look wrong:**
- Remember spacing: horizontal walls use X-spacing of 2, vertical use Y-spacing of 2
- Check grid coordinates vs world coordinates
- Verify rotation settings (green line should face outward)

**Player gets stuck:**
- Add doors where needed
- Check for overlapping collision geometry
- Verify spawn points are in valid, open locations

**Schedule editor not showing:**
- Make sure you've selected an NPC spawn point
- Click on the NPC spawn to select it
- The editor should appear automatically

## Keyboard Shortcuts

- `R` - Rotate selected tool by 90°
- `E` - Select Erase tool
- `D` - Select Floor tool
- `W` - Select Wall tool

## Development Commands

### List all maps
```bash
ls -1 /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp/public/data/maps/*.json
```

### Validate map JSON
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
for f in public/data/maps/*.json; do
  echo "Checking $f..."
  node -e "JSON.parse(require('fs').readFileSync('$f'))" && echo "✓ Valid"
done
```

### Count buildings in a map
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
cat public/data/maps/example.json | grep -c '"type"'
```

## Future Enhancements

Planned features:
- [ ] Undo/Redo functionality
- [ ] Copy/Paste regions
- [ ] Prefab buildings (templates)
- [ ] Height adjustments
- [ ] Texture selection
- [ ] 3D preview panel
- [ ] Multi-map management
- [ ] Collision layer visualization
