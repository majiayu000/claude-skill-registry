---
name: godot-sync-camera-positions
version: 3.0.0
displayName: Sync Camera-Following Positions
description: >
  Use when Godot background layers or elements follow the camera at runtime but
  show incorrect position in editor. Detects camera-following patterns and syncs
  editor position to match typical runtime state. Makes editor preview accurately
  show what players will see during gameplay.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: intermediate
audience: [developers]
keywords:
  - godot
  - camera-follow
  - editor-preview
  - background-layers
  - runtime-position
  - camera2d
  - level-design
  - wysiwyg
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

outputs: "Synced camera-aware positions, updated .tscn files, runtime comments, git commits"
requirements: "Git repository, Godot 4.x"
execution: "Automatic detection with calculated editor positions"
integration: "Part of godot-fix-positions orchestrator, works with godot-sync-parallax"
---

# Sync Camera-Following Positions

## Core Principle

**Editor preview should show realistic gameplay view.** Camera-following elements need special handling.

## What This Skill Does

Finds patterns like:
```gdscript
# background.gd
extends Sprite2D

func _process(delta):
    position = camera.position  # Follows camera at runtime

# background.tscn
[node name="Background" type="Sprite2D"]
position = Vector2(0, 0)  # Editor shows at origin

# RESULT: Editor shows background at (0,0)
# But in game, background is at camera position (e.g., 500, 300)
# Level designer sees wrong view!
```

Resolves to:
```gdscript
# background.gd (unchanged - runtime behavior same)
func _process(delta):
    position = camera.position

# background.tscn (updated to show typical camera position)
[node name="Background" type="Sprite2D"]
position = Vector2(500, 300)  # Camera starting position

# RESULT: Editor preview now shows realistic gameplay view
```

## Detection Patterns

Identifies camera-following code:

### Direct Camera Position Follow
```gdscript
func _process(delta):
    position = camera.position  # CAMERA FOLLOW
    position = camera.global_position
    position = get_viewport().get_camera_2d().position
```

### Player Position Follow (Indirect Camera)
```gdscript
func _process(delta):
    position = player.position  # Player follows camera
    # Background follows player → effectively follows camera
```

### Offset Camera Follow
```gdscript
func _process(delta):
    position = camera.position + offset  # CAMERA FOLLOW with offset
    position = player.position + Vector2(0, -100)
```

### Lerp Camera Follow
```gdscript
func _process(delta):
    position = position.lerp(camera.position, 0.1)  # Smooth camera follow
```

## When to Use

### Background Layers
Backgrounds that follow camera for infinite scrolling effect.

### UI Overlays
World-space UI that stays with camera.

### Level Design
Want to see what area looks like during gameplay.

### Camera-Relative Elements
Any element positioned relative to camera.

## Process

1. **Scan** - Find position assignments referencing camera/player
2. **Analyze** - Determine if it's camera-following pattern
3. **Calculate** - Determine typical camera position
4. **Update .tscn** - Set editor position to calculated position
5. **Document** - Add comments explaining runtime behavior
6. **Validate** - Ensure editor preview looks correct
7. **Commit** - Git commit per camera-follow sync

## Sync Strategies

### Strategy 1: Camera Start Position
Set editor position to where camera starts.

**Best for:** Most camera-following elements.

```gdscript
# background.gd
func _process(delta):
    position = camera.position

# Determine camera start position (from Level scene or project settings)
# Update background.tscn to position = camera_start_position
```

### Strategy 2: Player Start Position + Offset
Set editor position to player spawn + offset.

**Best for:** Elements following player with offset.

```gdscript
# cloud.gd
func _process(delta):
    position = player.position + Vector2(0, -200)  # Above player

# Find player spawn point
# Update cloud.tscn to position = player_spawn + Vector2(0, -200)
```

### Strategy 3: Metadata Annotation
Add metadata to scene explaining runtime behavior.

**Best for:** Complex camera following logic.

```gdscript
# Metadata in .tscn
[node name="Background"]
metadata/_editor_note = "Runtime: follows camera at camera.position"
```

## Smart Detection

**Identifies camera-following patterns:**
```gdscript
# CAMERA-FOLLOWING (syncs these)
position = camera.position
position = $"/root/Main/Camera".position
position = player.position  # If player has camera
position.x = camera.position.x  # Horizontal follow
```

**Skips non-camera patterns:**
```gdscript
# NOT CAMERA-FOLLOWING (skips these)
position = target_position  # Generic target
position = waypoints[index]  # Waypoint following
position = mouse_position  # Mouse following
```

## Example Transformations

### Example 1: Background Layer

**Before:**
```gdscript
# background.gd
extends Sprite2D
@onready var camera = $"/root/Main/Camera2D"

func _process(delta):
    position = camera.position

# background.tscn
[node name="Background" type="Sprite2D"]
position = Vector2(0, 0)
texture = preload("res://assets/sky.png")
```

**Editor view:** Background at origin (0, 0) - wrong!
**Game view:** Background at camera position (640, 360) - correct!

**After Sync:**
```gdscript
# background.gd (unchanged)
extends Sprite2D
@onready var camera = $"/root/Main/Camera2D"

func _process(delta):
    # Runtime: follows camera position
    position = camera.position

# background.tscn (updated)
[node name="Background" type="Sprite2D"]
position = Vector2(640, 360)  # Camera start position
texture = preload("res://assets/sky.png")
```

**Editor view:** Background at (640, 360) - matches gameplay!
**Game view:** Background at camera position - same as before!

### Example 2: Player-Relative Cloud

**Before:**
```gdscript
# cloud.gd
extends Sprite2D

func _process(delta):
    position = player.position + Vector2(0, -200)

# cloud.tscn
[node name="Cloud" type="Sprite2D"]
position = Vector2(0, 0)
```

**After Sync:**
```gdscript
# cloud.gd (unchanged)
func _process(delta):
    # Runtime: 200 pixels above player
    position = player.position + Vector2(0, -200)

# cloud.tscn (updated to show above player spawn)
[node name="Cloud" type="Sprite2D"]
position = Vector2(320, -20)  # Player spawns at (320, 180)
```

## Camera Position Detection

### Method 1: Find Camera2D in Scene
```bash
# Search for Camera2D nodes
grep -r "type=\"Camera2D\"" scenes/
# Find position value in camera's parent scene
```

### Method 2: Project Settings
```gdscript
# Check viewport size (camera typically starts at center)
# Default: 1280x720 → camera at (640, 360)
```

### Method 3: Ask User
If detection uncertain, ask:
"Where does your camera start? (e.g., center of viewport, player position)"

## What Gets Created

- Updated .tscn files with calculated positions
- Comments documenting runtime behavior
- Metadata annotations for complex patterns
- Validation ensuring editor preview looks correct
- Git commits per sync operation

## Integration

Works with:
- **godot-sync-static-positions** - Static position conflicts
- **godot-sync-parallax** - Parallax-specific camera following
- **godot-fix-positions** (orchestrator) - All position sync operations

## Safety

- Runtime behavior unchanged
- Only .tscn editor positions updated
- Code remains identical
- Rollback on validation failure
- Original positions in git history

## When NOT to Use

Don't sync if:
- Camera-following is complex (multiple cameras, switching)
- Position varies significantly during gameplay
- Editor position has specific meaning (not just default)
- Camera start position unknown/uncertain

## Benefits

- **Realistic Preview** - Editor shows gameplay view
- **Better Level Design** - See what players will see
- **Debug Friendly** - Obvious when positions are wrong
- **Team Communication** - Designers see accurate preview
- **WYSIWYG** - Preview matches gameplay

## Common Camera Patterns

### Infinite Scrolling Background
```gdscript
func _process(delta):
    position.x = camera.position.x
    # Vertical position fixed, horizontal follows camera
```

Sync: Set editor x to camera start x, keep y unchanged.

### Smooth Camera Follow
```gdscript
func _process(delta):
    position = position.lerp(camera.position, smoothness)
```

Sync: Set editor position to camera start (eventual position).

### Camera Bounds
```gdscript
func _process(delta):
    position = camera.position.clamp(min_bounds, max_bounds)
```

Sync: Set editor position to clamped camera start position.

## Validation

After syncing, validates:
- Editor position looks reasonable (not at 0,0)
- .tscn file parses correctly
- Scene loads without errors
- Visual appearance makes sense

## Documentation Pattern

```gdscript
# Runtime behavior:
# - Follows camera.position in _process
# - Editor position set to camera start: (640, 360)
# - During gameplay, position will match camera exactly
```

Clear documentation prevents confusion when code and editor positions differ intentionally.

## Camera Detection Hierarchy

1. Search for Camera2D in current scene
2. Search for Camera2D in parent scenes
3. Check project viewport size (assume center)
4. Ask user for camera start position

Intelligent detection minimizes user input needed.
