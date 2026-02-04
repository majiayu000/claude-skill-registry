---
name: godot-sync-parallax
version: 3.0.0
displayName: Sync Parallax Layer Positions
description: >
  Use when Godot ParallaxBackground/ParallaxLayer nodes show incorrect positions
  in editor due to parallax multipliers. Calculates correct editor positions based
  on camera start position and parallax motion scale. Makes parallax layers preview
  realistically in editor, matching gameplay appearance.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: intermediate
audience: [developers]
keywords:
  - godot
  - parallax
  - parallax-background
  - parallax-layer
  - motion-scale
  - editor-preview
  - camera-position
  - gdscript
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".gd", ".tscn"]
    write: [".tscn"]
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "Synced parallax positions, corrected layer offsets, updated .tscn files, git commits"
requirements: "Git repository, Godot 4.x"
execution: "Automatic calculation based on parallax properties"
integration: "Part of godot-fix-positions orchestrator, specialized for parallax systems"
---

# Sync Parallax Layer Positions

## Core Principle

**Parallax layers need special math for correct editor preview.** Motion scale affects runtime position.

## What This Skill Does

Parallax systems in Godot are complex:
```gdscript
# Godot's parallax formula:
final_position = layer_position - (camera_position * motion_scale)
```

**The problem:**
- Editor shows layer at `layer_position`
- Runtime shows layer at `layer_position - (camera_position * motion_scale)`
- Editor preview doesn't match gameplay

**The solution:**
Calculate correct `layer_position` so runtime appearance matches intended design.

## Example Problem

```ini
# parallax_background.tscn
[node name="ParallaxBackground" type="ParallaxBackground"]

[node name="SkyLayer" type="ParallaxLayer" parent="."]
motion_scale = Vector2(0.2, 0.2)  # Slow parallax
position = Vector2(0, 0)

# Camera starts at (640, 360)
# Runtime position: 0 - (640 * 0.2) = -128 (WRONG!)
# Sky layer appears shifted left in game
```

**After sync:**
```ini
[node name="SkyLayer" type="ParallaxLayer" parent="."]
motion_scale = Vector2(0.2, 0.2)
position = Vector2(128, 72)  # Corrected!

# Runtime position: 128 - (640 * 0.2) = 0 (CORRECT!)
# Sky layer appears centered in game, matching editor
```

## Detection Patterns

Identifies parallax systems:

### ParallaxBackground Structure
```ini
[node name="ParallaxBackground" type="ParallaxBackground"]
scroll_offset = Vector2(0, 0)
scroll_base_scale = Vector2(1, 1)

[node name="Layer1" type="ParallaxLayer" parent="."]
motion_scale = Vector2(0.5, 0.5)
motion_offset = Vector2(0, 0)
```

### Multiple Layers with Different Scales
```ini
[node name="SkyLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.1, 0.1)  # Very slow (far away)

[node name="MountainsLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.3, 0.3)  # Slow (middle distance)

[node name="TreesLayer" parent="ParallaxBackground"]
motion_scale = Vector2(0.7, 0.7)  # Fast (close)
```

## When to Use

### Designing Parallax Backgrounds
Creating multi-layer parallax effect in editor.

### Debugging Parallax Issues
Layers appear at wrong positions in game.

### Visual Level Design
Want WYSIWYG for parallax systems.

### Multiple Parallax Layers
Complex parallax with many layers at different scales.

## Process

1. **Scan** - Find ParallaxBackground and ParallaxLayer nodes
2. **Detect Camera** - Find camera start position
3. **Calculate** - Apply inverse parallax formula
4. **Update Positions** - Correct layer positions in .tscn
5. **Update Offsets** - Adjust motion_offset if needed
6. **Validate** - Ensure layers align correctly
7. **Commit** - Git commit per parallax system

## Parallax Math

### Forward Formula (Godot's runtime calculation)
```
displayed_position = layer_position - (camera_position * motion_scale)
```

### Inverse Formula (What we need for editor)
```
layer_position = desired_position + (camera_position * motion_scale)
```

### Example Calculation

**Want sky layer centered at (0, 0) in game:**
- Camera starts at: (640, 360)
- Motion scale: (0.2, 0.2)
- Calculate: layer_position = 0 + (640 * 0.2) = 128
- Calculate: layer_position = 0 + (360 * 0.2) = 72
- **Set layer position in editor: (128, 72)**

## Example Transformations

### Example 1: Sky Layer

**Before (Broken):**
```ini
[node name="SkyLayer" type="ParallaxLayer"]
motion_scale = Vector2(0.2, 0.2)
position = Vector2(0, 0)
# Sprite at (0, 0) relative to layer

# Camera at (640, 360)
# Runtime: 0 - (640 * 0.2) = -128
# Sky appears -128 pixels left (WRONG)
```

**After (Fixed):**
```ini
[node name="SkyLayer" type="ParallaxLayer"]
motion_scale = Vector2(0.2, 0.2)
position = Vector2(128, 72)  # Corrected
# Sprite at (0, 0) relative to layer

# Runtime: 128 - (640 * 0.2) = 0
# Sky appears centered (CORRECT)
```

### Example 2: Multiple Layers

**Before (All at origin):**
```ini
[node name="Sky" type="ParallaxLayer"]
motion_scale = Vector2(0.1, 0.1)
position = Vector2(0, 0)

[node name="Mountains" type="ParallaxLayer"]
motion_scale = Vector2(0.3, 0.3)
position = Vector2(0, 0)

[node name="Trees" type="ParallaxLayer"]
motion_scale = Vector2(0.7, 0.7)
position = Vector2(0, 0)

# All layers shifted left at runtime
```

**After (Corrected):**
```ini
[node name="Sky" type="ParallaxLayer"]
motion_scale = Vector2(0.1, 0.1)
position = Vector2(64, 36)  # 640*0.1, 360*0.1

[node name="Mountains" type="ParallaxLayer"]
motion_scale = Vector2(0.3, 0.3)
position = Vector2(192, 108)  # 640*0.3, 360*0.3

[node name="Trees" type="ParallaxLayer"]
motion_scale = Vector2(0.7, 0.7)
position = Vector2(448, 252)  # 640*0.7, 360*0.7

# All layers centered correctly at runtime
```

## Advanced: Motion Offset

### Motion Offset vs Position
- **position**: Layer's base position
- **motion_offset**: Additional offset applied with motion_scale

Combined formula:
```
displayed_position = (layer_position + motion_offset) - (camera_position * motion_scale)
```

Syncing considers both properties.

## Smart Detection

**Identifies parallax systems:**
- ParallaxBackground node present
- ParallaxLayer children with motion_scale ≠ (1, 1)
- Sprite/TextureRect children of layers

**Detects camera:**
1. Camera2D in scene hierarchy
2. Camera position from parent scene
3. Viewport center (default: 640, 360 for 1280x720)

**Calculates corrections:**
- Per-layer based on motion_scale
- Accounts for motion_offset
- Handles ParallaxBackground scroll_offset

## What Gets Created

- Updated .tscn files with corrected layer positions
- Comments documenting parallax calculations
- Validation ensuring layers align correctly
- Git commits per parallax system

## Integration

Works with:
- **godot-sync-camera-positions** - Non-parallax camera following
- **godot-sync-static-positions** - Static position conflicts
- **godot-fix-positions** (orchestrator) - All position sync operations

## Safety

- Parallax behavior unchanged at runtime
- Only editor positions updated
- Original .tscn preserved in git
- Validation ensures layers align
- Rollback on validation failure

## When NOT to Use

Don't sync if:
- Parallax positions intentionally offset
- Custom parallax implementation (not ParallaxBackground)
- Dynamic parallax scaling at runtime
- Camera position highly variable

## Benefits

- **Visual Design** - Design parallax layers in editor
- **WYSIWYG** - Preview matches gameplay
- **Debugging** - Obvious when layers misaligned
- **Faster Iteration** - See results immediately
- **Team Friendly** - Level designers work in editor

## Common Parallax Patterns

### Infinite Scrolling Background
```ini
[node name="CloudsLayer" type="ParallaxLayer"]
motion_scale = Vector2(0.2, 0)  # Horizontal only
motion_mirroring = Vector2(1280, 0)  # Repeat horizontally
```

Sync: Correct horizontal position only.

### Vertical Parallax (Platformer)
```ini
[node name="SkyLayer" type="ParallaxLayer"]
motion_scale = Vector2(0, 0.1)  # Vertical only
```

Sync: Correct vertical position only.

### Full 2D Parallax
```ini
[node name="BackgroundLayer" type="ParallaxLayer"]
motion_scale = Vector2(0.3, 0.3)  # Both axes
```

Sync: Correct both x and y positions.

## Validation

After syncing, validates:
- All layers visible in editor
- Layer order preserved (back to front)
- Sprites aligned as intended
- No layer at negative positions (unless intentional)
- Editor preview looks realistic

## Camera Position Detection

### Priority Order
1. Camera2D in current scene → use position
2. Camera2D in parent scene → use position
3. Viewport size → assume center (width/2, height/2)
4. Project settings → get viewport size
5. Ask user if uncertain

## Documentation Pattern

```gdscript
# Parallax layer corrected for camera start: (640, 360)
# motion_scale: (0.2, 0.2)
# Formula: position = desired_runtime_position + (camera * motion_scale)
# Calculation: (0, 0) + (640 * 0.2, 360 * 0.2) = (128, 72)
```

Clear documentation shows calculation method.

## Common Issues Fixed

| Issue | Cause | Solution |
|-------|-------|----------|
| Layer shifted left in game | position = (0,0), motion_scale < 1 | Add offset: camera * motion_scale |
| Layer jumps at start | Editor position ≠ runtime position | Sync positions using formula |
| Layers misaligned | Different camera assumptions | Consistent camera start position |
| Preview doesn't match game | Parallax math not considered | Apply inverse parallax formula |

## Performance Considerations

Parallax systems are efficient but:
- Limit number of layers (typically 3-5)
- Use TextureRect for static backgrounds
- Consider motion_mirroring for infinite scrolling
- Avoid heavy shaders on parallax layers

Syncing positions doesn't affect performance, only editor usability.
