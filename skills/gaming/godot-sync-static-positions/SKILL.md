---
name: godot-sync-static-positions
version: 3.0.0
displayName: Sync Static Positions
description: >
  Use when Godot nodes have position set in both .tscn (editor) and _ready() (code),
  creating confusion about actual runtime position. Detects static position assignments
  that conflict with editor values. Syncs to single source of truth, making editor
  preview match game behavior (WYSIWYG).
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: beginner
audience: [developers]
keywords:
  - godot
  - position-sync
  - editor-preview
  - wysiwyg
  - static-positions
  - node-position
  - level-design
  - tscn-files
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".gd", ".tscn"]
    write: [".gd", ".tscn"]
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "Synced positions, updated .tscn or .gd files, clear ownership documentation, git commits"
requirements: "Git repository, Godot 4.x"
execution: "Automatic detection with user-approved sync strategy"
integration: "Part of godot-fix-positions orchestrator, works with godot-clean-conflicts"
---

# Sync Static Positions

## Core Principle

**What You See Is What You Get.** Editor preview should match game behavior for static positions.

## What This Skill Does

Finds conflicts like:
```gdscript
# enemy.gd
func _ready():
    position = Vector2(500, 300)  # Code says here

# enemy.tscn
[node name="Enemy" type="CharacterBody2D"]
position = Vector2(100, 100)  # Editor says here

# RESULT: Confusing! Editor shows wrong position
```

Resolves to:
```gdscript
# enemy.gd
func _ready():
    # Position is set in scene file for editor visibility
    pass

# enemy.tscn
[node name="Enemy" type="CharacterBody2D"]
position = Vector2(500, 300)  # Updated to match intended position

# RESULT: Editor preview matches game
```

## Detection Patterns

Identifies:

### Direct Position Assignment in _ready()
```gdscript
func _ready():
    position = Vector2(100, 150)  # STATIC CONFLICT
    global_position = Vector2(500, 300)  # STATIC CONFLICT
```

### Node Property Assignment
```gdscript
func _ready():
    $Sprite.position = Vector2(10, 20)  # Child position conflict
    get_node("CollisionShape2D").position = Vector2(0, 0)
```

### Multiple Property Conflicts
```gdscript
func _ready():
    position = Vector2(100, 100)
    rotation = deg_to_rad(45)  # Also position-related
    scale = Vector2(2, 2)
```

## When to Use

### Level Design Workflow
Placing objects in editor but code overrides positions.

### Debugging Position Issues
"Why is this node in the wrong place?"

### Maintaining WYSIWYG
Want editor preview to be accurate.

### Preparing for Collaboration
Level designers need accurate editor preview.

## Process

1. **Scan** - Find position assignments in _ready()
2. **Compare** - Check against .tscn values
3. **Detect Conflicts** - Identify static conflicts (not dynamic)
4. **Choose Strategy** - User selects sync direction
5. **Apply** - Update .tscn or .gd files
6. **Document** - Add comments explaining ownership
7. **Validate** - Ensure positions match across editor/game
8. **Commit** - Git commit per conflict resolution

## Sync Strategies

### Strategy 1: Editor Wins (Recommended for Static Positions)
Move code value to .tscn, remove from code.

**When to use:**
- Position should be visible in editor
- Designer-controlled placement
- Static object positioning

**Example:**
```gdscript
# Before
func _ready():
    position = Vector2(500, 300)

# After
func _ready():
    # Position is set in scene file
    pass
```
```ini
# enemy.tscn updated
position = Vector2(500, 300)
```

### Strategy 2: Code Wins (Keep Dynamic)
Remove editor value, keep code assignment.

**When to use:**
- Position calculated at runtime
- Depends on other nodes/data
- Procedural positioning

**Example:**
```gdscript
# Before
func _ready():
    position = spawn_point.position + offset  # Dynamic!

# After
func _ready():
    # Position is dynamically calculated (see spawn_point)
    position = spawn_point.position + offset
```
```ini
# enemy.tscn - position removed or set to (0,0) as placeholder
```

### Strategy 3: Document Intent
Keep both but add clear comments.

**When to use:**
- Initial position in editor, overridden intentionally
- Default position with code override
- Both values have meaning

**Example:**
```gdscript
# Before
func _ready():
    position = start_position

# After
func _ready():
    # Editor position is default spawn, overridden to start_position
    position = start_position
```

## Smart Detection

**Identifies STATIC conflicts (fixes these):**
```gdscript
func _ready():
    position = Vector2(100, 100)  # Literal constant - STATIC
    position = Vector2(CONSTANT_X, CONSTANT_Y)  # Constants - STATIC
    $Child.position = Vector2(10, 10)  # Literal - STATIC
```

**Skips DYNAMIC positioning (intentional):**
```gdscript
func _ready():
    position = player.position  # Variable reference - DYNAMIC
    position = get_spawn_point()  # Function call - DYNAMIC
    if some_condition:
        position = Vector2(100, 100)  # Conditional - DYNAMIC

func _process(delta):
    position = target  # Every frame - DYNAMIC (skip)
```

**Key distinction: Static = same every time, Dynamic = varies at runtime**

## What Gets Created

- Synced .tscn files with correct positions
- Updated or cleaned code files
- Comments documenting position ownership
- Validation ensuring sync worked
- Git commits per sync operation

## Common Conflicts

### Conflict 1: Spawn Position
```gdscript
# Before: Code says (500, 300), editor says (0, 0)
func _ready():
    position = Vector2(500, 300)

# After: Editor updated, code removed
# enemy.tscn: position = Vector2(500, 300)
```

### Conflict 2: Child Node Offset
```gdscript
# Before: Child offset in code, not editor
func _ready():
    $Sprite.position = Vector2(0, -10)

# After: Sprite position moved in .tscn
# enemy.tscn: [node name="Sprite"] position = Vector2(0, -10)
```

### Conflict 3: Multiple Properties
```gdscript
# Before: Position, rotation, scale all in code
func _ready():
    position = Vector2(100, 100)
    rotation = deg_to_rad(45)
    scale = Vector2(1.5, 1.5)

# After: All properties in .tscn, code clean
# enemy.tscn has all three properties set
```

## Integration

Works with:
- **godot-sync-camera-positions** - Camera-following elements
- **godot-sync-parallax** - Parallax-specific syncing
- **godot-clean-conflicts** - General conflict resolution
- **godot-fix-positions** (orchestrator) - All position sync operations

## Safety

- Original positions preserved in git
- Validation ensures sync correctness
- Rollback on validation failure
- .tscn format preserved exactly

## When NOT to Use

Don't sync if:
- Position is calculated dynamically
- Position varies based on game state
- Intentional position override pattern
- Position set in _process() (every frame)

**Valid code-controlled positions:**
```gdscript
# These should NOT be synced to .tscn
func _ready():
    position = get_spawn_location_from_data()  # Data-driven
    position = player.position + offset  # Relative to player
    position = area.get_random_point()  # Procedural
```

## Benefits

- **WYSIWYG** - Editor shows accurate positions
- **Designer-Friendly** - Level design in editor, not code
- **Debugging** - Obvious where position comes from
- **Consistency** - Clear ownership pattern
- **Visualization** - Preview exactly matches game

## Position Ownership Patterns

After syncing, clear patterns emerge:

| Position Type | Owner | Example |
|---------------|-------|---------|
| Static spawn points | Editor (.tscn) | Enemy spawn locations |
| Child node offsets | Editor (.tscn) | Sprite relative to parent |
| Dynamic positions | Code (_ready, _process) | Follow player, procedural |
| Animation positions | AnimationPlayer | Animated movement |
| Physics positions | Physics engine | RigidBody2D |

## Validation

After syncing, validates:
- .tscn file parses correctly
- Position values match intended target
- References (@onready) still work
- Scene loads without errors
- Visual position matches code position

## Documentation Added

```gdscript
# Position is set in scene file at (500, 300)
# Rotation is controlled by AnimationPlayer "rotate"
# Scale is controlled by code (dynamic resizing based on health)
```

Clear ownership = clear code = fewer bugs.
