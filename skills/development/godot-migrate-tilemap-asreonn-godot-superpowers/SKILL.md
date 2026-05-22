---
name: godot-migrate-tilemap
version: 1.0.0
displayName: "Godot TileMap V2 Migration"
description: >
  Migrates legacy TileMap (Godot 4.0-4.2) to new TileMapLayer system (Godot 4.3+).
  Handles TileMap node conversion, API migration (set_cell to set_cells_terrain_connect),
  TileSet resource updates, physics layer mapping, navigation layer conversion, and
  custom data preservation. Essential for upgrading Godot 4.2 projects to 4.3+.
author: "Asreonn"
license: MIT
category: game-development
type: tool
difficulty: advanced
audience: [developers, migrators]
keywords:
  - godot
  - tilemap
  - tilemaplayer
  - migration
  - godot43
  - tileset
  - terrain
  - navigation
  - physics
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme
filesystem:
  read:
    - "${PROJECT_ROOT}/**/*.gd"
    - "${PROJECT_ROOT}/**/*.tscn"
    - "${PROJECT_ROOT}/**/*.tres"
    - "${PROJECT_ROOT}/project.godot"
  write:
    - "${PROJECT_ROOT}/**/*.gd"
    - "${PROJECT_ROOT}/**/*.tscn"
    - "${PROJECT_ROOT}/**/*.tres"
  deny:
    - "**/.env*"
    - "**/secrets*"
    - "**/*.key"
behavior:
  timeout: 600
  retry: 2
  cache: true
  interactive: true
---

# Godot TileMap V2 Migration

**Migrates legacy TileMap system to Godot 4.3+ TileMapLayer architecture.**

## Breaking Changes

Godot 4.3 introduced a new TileMap system with breaking changes:

| Legacy (4.0-4.2) | New (4.3+) |
|------------------|------------|
| Single `TileMap` node | Multiple `TileMapLayer` nodes |
| `set_cell()` method | `set_cells_terrain_connect()` |
| Cell-based coordinates | Layer-based organization |
| Single TileSet resource | Enhanced TileSet with layers |
| `update_bitmask_region()` | Terrain system |
| Manual physics setup | Physics layers per tile |

---

## UPON INVOCATION - START HERE

When this skill is invoked, IMMEDIATELY execute:

### 1. Verify Godot Project (5 seconds)

```bash
ls project.godot 2>/dev/null && echo "✓ Godot project detected" || echo "✗ Not a Godot project"
```

**If NOT a Godot project:**
- Inform user this skill only works on Godot projects
- STOP here

### 2. Detect TileMap Usage (10 seconds)

```bash
echo "=== Detecting TileMap Usage ==="

echo "TileMap nodes in scenes:"
grep -rn "type=\"TileMap\"" --include="*.tscn" . | wc -l

echo "TileMap references in scripts:"
grep -rn "TileMap" --include="*.gd" . | wc -l

echo "set_cell calls:"
grep -rn "set_cell\|get_cell" --include="*.gd" . | wc -l

echo "update_bitmask calls:"
grep -rn "update_bitmask" --include="*.gd" . | wc -l

echo "tile_set property access:"
grep -rn "\.tile_set" --include="*.gd" . | wc -l
```

### 3. Present Findings

Show the user:
```
=== TileMap V2 Migration Analysis ===

Project: [project name]
Current: Legacy TileMap (Godot 4.0-4.2 style)

TileMap usage detected:
- TileMap nodes: X
- TileMap references: X
- set_cell/get_cell calls: X
- update_bitmask calls: X
- tile_set access: X

Migration includes:
✓ TileMap → TileMapLayer node conversion
✓ set_cell() → set_cells_terrain_connect()
✓ TileSet resource upgrade
✓ Physics layer mapping
✓ Navigation layer conversion
✓ Custom data preservation
✓ Terrain system setup
✓ Git commit per layer
✓ Backup before changes

⚠️  WARNING: Godot 4.3+ required for new TileMapLayer system

Would you like me to:
1. Proceed with migration (recommended)
2. Show detailed breakdown first
3. Migrate specific TileMaps only
4. Cancel
```

### 4. Wait for User Choice

- **If 1 (Proceed):** Start Phase 2 immediately
- **If 2 (Details):** Show file-by-file breakdown
- **If 3 (Selective):** Ask which TileMaps to migrate
- **If 4 (Cancel):** Exit skill

---

## Phase 1: Analysis & Inventory

### 1.1 Create TileMap Inventory

```bash
# Find all TileMap nodes in .tscn files
grep -rn "type=\"TileMap\"" --include="*.tscn" . | while read line; do
    file=$(echo "$line" | cut -d: -f1)
    echo "Found TileMap in: $file"
done > /tmp/tilemap_scenes.txt

# Find all TileMap references in scripts
grep -rn "extends TileMap\|var.*TileMap\|: TileMap" --include="*.gd" . | while read line; do
    file=$(echo "$line" | cut -d: -f1)
    echo "TileMap usage in: $file"
done > /tmp/tilemap_scripts.txt
```

### 1.2 Analyze TileMap Structure

For each TileMap node:

```bash
# Extract TileMap configuration from .tscn
grep -A20 "type=\"TileMap\"" scene.tscn | grep -E "tile_set|format|cell|layer"
```

### 1.3 Create Migration Plan

```
TileMap V2 Migration Plan:
=========================

1. Node Structure Changes (X TileMaps)
   - Convert TileMap → TileMapLayer nodes
   - Preserve layer order and names
   - Update scene hierarchy

2. API Migration (X scripts)
   - set_cell() → set_cells_terrain_connect()
   - get_cell() → get_cell_alternative_tile()
   - update_bitmask() → terrain system

3. TileSet Updates (X resources)
   - Upgrade TileSet format
   - Map physics layers
   - Configure navigation layers
   - Preserve custom data

4. Script Updates (X files)
   - Update TileMap references
   - Fix method calls
   - Update signal connections

Total operations: X
Estimated time: Auto
Godot version required: 4.3+
Backup created: YES
Rollback available: YES
```

---

## Phase 2: TileMap Node Migration

### 2.1 Convert TileMap to TileMapLayer

**Legacy Structure:**
```ini
[node name="TileMap" type="TileMap"]
tile_set = ExtResource("1_qwerty")
format = 2

layer_0/name = "Ground"
layer_0/tile_data = PackedInt32Array(...)

layer_1/name = "Walls"  
layer_1/tile_data = PackedInt32Array(...)
```

**New Structure:**
```ini
[node name="Ground" type="TileMapLayer" parent="."]
tile_map_data = PackedByteArray(...)
tile_set = ExtResource("1_qwerty")

[node name="Walls" type="TileMapLayer" parent="."]
tile_map_data = PackedByteArray(...)
tile_set = ExtResource("1_qwerty")
```

**Transformation Process:**

1. **Parse legacy TileMap**
   - Extract layer names
   - Extract layer data
   - Extract TileSet reference
   - Extract position/z-index

2. **Generate TileMapLayer nodes**
   - One node per layer
   - Name from layer name
   - Convert tile_data format
   - Preserve TileSet reference

3. **Update scene hierarchy**
   - Remove TileMap node
   - Add TileMapLayer children
   - Update parent references

---

### 2.2 Tile Data Conversion

**Legacy Format:**
```ini
layer_0/tile_data = PackedInt32Array(0, 1, 0, 65536, 1, 0, ...)
```

**New Format:**
```ini
tile_map_data = PackedByteArray(0, 0, 0, 0, 1, 0, 0, 0, ...)
```

**Note:** Direct byte conversion requires Godot's internal format knowledge. Alternative approach:

```gdscript
# Migration script approach
# 1. Load scene with legacy TileMap in Godot 4.3
# 2. Run migration tool script
# 3. Save with new TileMapLayer format
```

---

## Phase 3: API Migration

### 3.1 Method Call Updates

**Detection:**
```bash
grep -rn "set_cell\|get_cell\|update_bitmask" --include="*.gd" .
```

**Common Mappings:**

| Legacy API | New API |
|------------|---------|
| `set_cell(layer, coords, source_id)` | `set_cells_terrain_connect(coords_array, terrain_set, terrain)` |
| `get_cell(layer, coords)` | `get_cell_alternative_tile(coords)` |
| `get_cell_source_id(layer, coords)` | `get_cell_source_id(coords)` |
| `update_bitmask_region(start, end)` | Terrain system (set terrain bits) |
| `clear_layer(layer)` | `clear()` on TileMapLayer |
| `erase_cell(layer, coords)` | `erase_cell(coords)` |

### 3.2 Script Transformations

**Example 1: Setting a cell**

Before:
```gdscript
# Legacy TileMap API
tilemap.set_cell(0, Vector2i(5, 3), 1)
tilemap.set_cell(0, Vector2i(5, 4), 1)
tilemap.set_cell(0, Vector2i(6, 3), 1)
```

After:
```gdscript
# New TileMapLayer API - Using terrain for multiple cells
ground_layer.set_cells_terrain_connect(
    [Vector2i(5, 3), Vector2i(5, 4), Vector2i(6, 3)],
    0,  # terrain_set
    1   # terrain_id
)
```

**Example 2: Getting cell data**

Before:
```gdscript
var source_id = tilemap.get_cell_source_id(0, coords)
var atlas_coords = tilemap.get_cell_atlas_coords(0, coords)
```

After:
```gdscript
var source_id = ground_layer.get_cell_source_id(coords)
var atlas_coords = ground_layer.get_cell_atlas_coords(coords)
```

**Example 3: Autotile/Bitmask**

Before:
```gdscript
tilemap.set_cell(0, coords, 1)
tilemap.update_bitmask_region(Rect2i(0, 0, 20, 20))
```

After:
```gdscript
# Using terrain system
ground_layer.set_cells_terrain_connect([coords], 0, 1)
# Terrain automatically connects - no update_bitmask needed!
```

---

## Phase 4: TileSet Resource Migration

### 4.1 Physics Layers

**Legacy:** Physics setup per tile in TileSet

**New:** Dedicated physics layers

```gdscript
# New TileSet setup in Godot 4.3
tileset.set_physics_layer_collision_layer(0, 1)
tileset.set_physics_layer_collision_mask(0, 1)
tileset.set_physics_layer_physics_material_override(0, physics_material)
```

### 4.2 Navigation Layers

**Legacy:** Navigation polygons per tile

**New:** Navigation layers system

```gdscript
# Enable navigation layer
tileset.set_navigation_layer_enabled(0, true)

# Set navigation polygon for specific tile
var source_id = 1
var atlas_coords = Vector2i(0, 0)
tileset.set_navigation_polygon(0, source_id, atlas_coords, navigation_polygon)
```

### 4.3 Custom Data Layers

**New in 4.3:** Custom data per tile

```gdscript
# Define custom data layer
tileset.add_custom_data_layer()
tileset.set_custom_data_layer_name(0, "tile_health")
tileset.set_custom_data_layer_type(0, TYPE_INT)

# Set data on specific tile
tileset.set_custom_data(0, source_id, atlas_coords, 100)
```

---

## Phase 5: Execution & Safety

### 5.1 Create Git Baseline

```bash
# Create backup tag
git tag tilemap-v1-baseline-$(date +%Y%m%d-%H%M%S)

# Commit any current changes
git add .
git commit -m "Baseline: Pre-TileMap V2 migration" || echo "No changes to commit"
```

### 5.2 Migration Execution

For each TileMap:

1. **Backup scene file**
   ```bash
   cp scene.tscn scene.tscn.backup
   ```

2. **Parse TileMap data**
   - Extract layers
   - Extract tile data
   - Note TileSet reference

3. **Generate TileMapLayer nodes**
   - Create node entries
   - Convert data format
   - Set properties

4. **Update scripts**
   - Replace TileMap references
   - Update method calls
   - Fix signal connections

5. **Commit changes**
   ```bash
   git add scene.tscn modified_scripts.gd
   git commit -m "Migrate: TileMap to TileMapLayer in scene.tscn
   
   - Converted TileMap node to TileMapLayer nodes
   - Updated script references
   - Migrated set_cell() calls
   - Preserved layer data"
   ```

### 5.3 Validation After Each Migration

```bash
# Check scene loads in Godot
godot --headless --quit-after 5 project.godot 2>&1 | tee test.log

# Check for errors
if grep -q "ERROR\|SCRIPT ERROR" test.log; then
    echo "⚠️  Migration error detected!"
    git reset --hard HEAD~1
    echo "✓ Reverted to pre-migration state"
    exit 1
fi

rm test.log
```

---

## Phase 6: Post-Migration Setup

### 6.1 Terrain System Configuration

```gdscript
# Setup terrain for autotiling
tileset.add_terrain_set()
tileset.set_terrain_set_mode(0, TileSet.TerrainMode.CONNECT)

# Add terrain
tileset.add_terrain(0, 0)
tileset.set_terrain_name(0, 0, "Ground")

# Assign terrain to tiles
# (Configure in Godot editor for best results)
```

### 6.2 Physics Layer Setup

```gdscript
# Configure physics layers per tile type
tileset.set_physics_layer_collision_layer(0, 1)  # Layer 1
tileset.set_physics_layer_collision_mask(0, 1)   # Detect layer 1
```

### 6.3 Navigation Setup

```gdscript
# Enable navigation on specific tiles
navigation_layer.enabled = true
tileset.set_navigation_layer_enabled(0, true)
```

---

## Examples

### Example 1: Complete TileMap Migration

**Before (Godot 4.2):**
```gdscript
# level.tscn
[node name="TileMap" type="TileMap"]
tile_set = ExtResource("1_tileset")
format = 2
layer_0/name = "Ground"
layer_0/tile_data = PackedInt32Array(...)
layer_1/name = "Obstacles"
layer_1/tile_data = PackedInt32Array(...)

# level.gd
extends Node2D

@onready var tilemap: TileMap = $TileMap

func _ready():
    # Set some cells
    tilemap.set_cell(0, Vector2i(10, 5), 1)
    tilemap.set_cell(0, Vector2i(11, 5), 1)
    tilemap.update_bitmask_region(Rect2i(10, 5, 2, 1))
    
    # Get cell info
    var source_id = tilemap.get_cell_source_id(0, Vector2i(10, 5))
    print("Cell source: ", source_id)

func generate_level():
    for x in range(20):
        for y in range(15):
            tilemap.set_cell(0, Vector2i(x, y), randi() % 3)
    tilemap.update_bitmask_region(Rect2i(0, 0, 20, 15))
```

**After (Godot 4.3):**
```gdscript
# level.tscn
[node name="Ground" type="TileMapLayer" parent="."]
tile_set = ExtResource("1_tileset")
tile_map_data = PackedByteArray(...)

[node name="Obstacles" type="TileMapLayer" parent="."]
tile_set = ExtResource("1_tileset")
tile_map_data = PackedByteArray(...)

# level.gd
extends Node2D

@onready var ground_layer: TileMapLayer = $Ground
@onready var obstacles_layer: TileMapLayer = $Obstacles

func _ready():
    # Set cells using terrain
    ground_layer.set_cells_terrain_connect(
        [Vector2i(10, 5), Vector2i(11, 5)],
        0,  # terrain_set
        1   # terrain_id
    )
    
    # Get cell info
    var source_id = ground_layer.get_cell_source_id(Vector2i(10, 5))
    print("Cell source: ", source_id)

func generate_level():
    var coords_array = []
    for x in range(20):
        for y in range(15):
            coords_array.append(Vector2i(x, y))
    
    # Use terrain for efficient bulk placement
    ground_layer.set_cells_terrain_connect(coords_array, 0, randi() % 3)
```

### Example 2: Multiple Layer Management

**Before:**
```gdscript
# Access different layers
func set_ground_cell(coords: Vector2i, tile: int):
    tilemap.set_cell(0, coords, tile)

func set_wall_cell(coords: Vector2i, tile: int):
    tilemap.set_cell(1, coords, tile)

func clear_all():
    tilemap.clear_layer(0)
    tilemap.clear_layer(1)
```

**After:**
```gdscript
# Access different layers
func set_ground_cell(coords: Vector2i, tile: int):
    ground_layer.set_cells_terrain_connect([coords], 0, tile)

func set_wall_cell(coords: Vector2i, tile: int):
    obstacles_layer.set_cell(coords, tile)

func clear_all():
    ground_layer.clear()
    obstacles_layer.clear()
```

---

## Success Criteria

Migration complete when:

- ✓ Zero TileMap nodes remain (converted to TileMapLayer)
- ✓ Zero `set_cell(layer, ...)` calls remain
- ✓ Zero `update_bitmask` calls remain
- ✓ All scripts use TileMapLayer references
- ✓ TileSet resources upgraded to new format
- ✓ Physics layers configured (if used)
- ✓ Navigation layers configured (if used)
- ✓ Custom data preserved (if any)
- ✓ All scenes load without errors
- ✓ Runtime behavior identical

---

## Common Issues & Solutions

### Issue 1: Layer index confusion

**Problem:** Old code used layer indices (0, 1, 2)

**Solution:** Replace with explicit layer references
```gdscript
# Before
tilemap.set_cell(0, coords, tile)  # Layer 0

# After
ground_layer.set_cell(coords, tile)  # Named layer
```

### Issue 2: Bulk cell updates

**Problem:** `update_bitmask_region()` no longer exists

**Solution:** Use terrain system or set_cells_terrain_connect()
```gdscript
# Before
for x in range(width):
    for y in range(height):
        tilemap.set_cell(0, Vector2i(x, y), source_id)
tilemap.update_bitmask_region(Rect2i(0, 0, width, height))

# After
var coords_array = []
for x in range(width):
    for y in range(height):
        coords_array.append(Vector2i(x, y))
ground_layer.set_cells_terrain_connect(coords_array, 0, source_id)
```

### Issue 3: Cell coordinate systems

**Problem:** Coordinate system differences between TileMap and TileMapLayer

**Solution:** Both use Vector2i, but ensure local vs global coordinates
```gdscript
# Both work similarly
var local_coords = tilemap.local_to_map(position)  # Legacy
var local_coords = layer.local_to_map(position)    # New
```

---

## Rollback Procedure

If migration causes issues:

```bash
# Find baseline tag
git tag | grep "tilemap-v1-baseline"

# Reset to pre-migration
git reset --hard <baseline-tag>

# Or restore individual scene from backup
cp scene.tscn.backup scene.tscn
```

---

## Godot Version Requirements

**Minimum:** Godot 4.3+

**Check version:**
```bash
godot --version
# Should show 4.3 or higher
```

**Upgrade notes:**
- Open project in Godot 4.3 first (converts project.godot)
- Then run this migration skill
- Test thoroughly before committing

---

## Integration with Other Skills

**Use with:**
- `godot-modernize-gdscript` - Update syntax before TileMap migration
- `godot-refactor` - Clean up code after migration
- `godot-setup-navigation` - Configure navigation on new TileMapLayer

**Best practice workflow:**
1. Run godot-modernize-gdscript (update syntax)
2. Run godot-migrate-tilemap (this skill)
3. Run godot-refactor (clean architecture)
4. Manual testing in Godot 4.3+

---

**This skill handles the complex TileMap API changes in Godot 4.3, preserving your level data while upgrading to the modern TileMapLayer system.**
