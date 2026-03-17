---
name: godot-clean-conflicts
version: 3.0.0
displayName: Clean Conflicting Operations
description: >
  Use when Godot code has operations that conflict with each other, creating
  undefined behavior. Detects same property set in multiple places (_ready, _process,
  code + editor), same signal connected multiple times, conflicting physics modes,
  competing animations. Automatically resolves conflicts with clear ownership.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: intermediate
audience: [developers]
keywords:
  - godot
  - conflicts
  - race-conditions
  - duplicate-signals
  - physics-modes
  - animation-conflicts
  - gdscript
  - undefined-behavior
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".gd", ".tscn", ".tres"]
    write: [".gd", ".tscn"]
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "Conflict resolution, clear ownership patterns, updated code/scenes, git commits"
requirements: "Git repository, Godot 4.x"
execution: "Automatic detection with user-approved resolution strategy"
integration: "Part of godot-refactor orchestrator, resolves architectural conflicts"
---

# Clean Conflicting Operations

## Core Principle

**One source of truth per property.** Conflicting operations create undefined behavior and debugging nightmares.

## What This Skill Does

Finds patterns like:
```gdscript
# player.gd
func _ready():
    position = Vector2(100, 100)  # Code sets position
    # BUT: .tscn also has position = Vector2(200, 200)
    # CONFLICT: Which position wins?

func _process(delta):
    rotation += delta  # Animation system ALSO modifying rotation
    # CONFLICT: Animation vs code control
```

Resolves to clear ownership:
```gdscript
# player.gd
# Position is set in .tscn (editor owns position)
# Rotation is controlled by animation (animation owns rotation)

func _process(delta):
    # Rotation conflict removed
    pass
```

## Detection Patterns

Identifies:

### Property Conflicts
- Same property set in code (_ready) and editor (.tscn)
- Same property modified in _process and _physics_process
- Property controlled by animation AND code simultaneously

### Signal Conflicts
- Same signal connected multiple times
- Duplicate lambda connections
- Signal connect without checking is_connected()

### Physics Conflicts
- RigidBody with code-controlled position (conflicts with physics)
- CharacterBody with physics_process AND animation control
- Conflicting collision layers/masks (code vs editor)

### Animation Conflicts
- AnimationPlayer and code both modifying same property
- Multiple AnimationPlayers controlling same nodes
- Tween and animation competing for control

## When to Use

### You're Debugging Unexpected Behavior
Properties have wrong values and you don't know why.

### You're Experiencing Race Conditions
Sometimes works, sometimes doesn't (timing-dependent).

### You're Seeing Duplicate Events
Signal fires twice, actions happen multiple times.

### You're Fighting the Physics Engine
Code tries to control physics body directly.

## Process

1. **Scan** - Find conflicting operations across code and scenes
2. **Analyze** - Determine which operation should own each property
3. **Resolve** - Apply conflict resolution strategy
4. **Document** - Add comments explaining ownership
5. **Validate** - Ensure behavior is now deterministic
6. **Commit** - Git commit per conflict resolution

## Example Transformations

### Conflict 1: Position Set in Both Code and Editor

**Before (Conflict):**
```gdscript
# enemy.gd
func _ready():
    position = Vector2(500, 300)  # Code says here

# enemy.tscn
[node name="Enemy" type="CharacterBody2D"]
position = Vector2(100, 100)  # Editor says here
# RESULT: Confusing! Editor shows one place, game uses another
```

**After (Resolved - Editor Wins):**
```gdscript
# enemy.gd
func _ready():
    # Position is set in scene file for editor visibility
    pass

# enemy.tscn
[node name="Enemy" type="CharacterBody2D"]
position = Vector2(500, 300)  # Updated to match intended position
# RESULT: What You See Is What You Get
```

### Conflict 2: Duplicate Signal Connections

**Before (Conflict):**
```gdscript
# ui.gd
func _ready():
    button.pressed.connect(_on_button_pressed)

func setup_ui():
    button.pressed.connect(_on_button_pressed)  # CONNECTED AGAIN!
    # RESULT: _on_button_pressed fires TWICE per click
```

**After (Resolved):**
```gdscript
# ui.gd
func _ready():
    if not button.pressed.is_connected(_on_button_pressed):
        button.pressed.connect(_on_button_pressed)

func setup_ui():
    # Connection already exists, skip
    pass
# RESULT: Fires exactly once per click
```

### Conflict 3: Animation vs Code Control

**Before (Conflict):**
```gdscript
# player.gd
func _process(delta):
    sprite.rotation += delta * rotation_speed  # Code controls rotation

# player.tscn has AnimationPlayer controlling sprite.rotation
# RESULT: Jittery rotation, both systems fighting
```

**After (Resolved - Animation Wins):**
```gdscript
# player.gd
func _process(delta):
    # Rotation is controlled by animation system
    # Code can trigger animations: animation_player.play("rotate")
    pass

# AnimationPlayer has full control of sprite.rotation
# RESULT: Smooth animation, clear ownership
```

### Conflict 4: Physics Body Position Control

**Before (Conflict):**
```gdscript
# enemy.gd
extends RigidBody2D

func _physics_process(delta):
    position = target_position  # CONFLICT with physics engine!
    # Physics engine wants to control position
    # Code also tries to control position
    # RESULT: Jittery movement, physics fighting code
```

**After (Resolved - Use Correct Body Type):**
```gdscript
# enemy.gd
extends CharacterBody2D  # Changed to CharacterBody for code control

func _physics_process(delta):
    position = target_position  # Now appropriate for CharacterBody
    # CharacterBody2D is designed for code-controlled movement
    # RESULT: Smooth movement, no conflict
```

**Alternative Resolution (Keep RigidBody):**
```gdscript
# enemy.gd
extends RigidBody2D

func _physics_process(delta):
    # Use forces instead of direct position control
    apply_force((target_position - position) * force_strength)
    # Work WITH physics engine, not against it
    # RESULT: Realistic physics-based movement
```

## Conflict Resolution Strategies

### 1. Editor Wins (Position/Rotation/Scale)
Move code-defined values to .tscn for editor visibility.

### 2. Code Wins (Dynamic State)
Remove editor values when code needs full control.

### 3. Animation Wins (Animated Properties)
Code triggers animations, doesn't modify properties directly.

### 4. Physics Wins (RigidBody)
Use forces/impulses instead of direct property control.

### 5. One-Time Initialization
Establish clear pattern: editor for initial, code for changes.

## What Gets Created

- Conflict resolution documentation
- Comments explaining ownership decisions
- Updated code removing conflicts
- Updated .tscn files with correct values
- Git commits per conflict type resolved

## Smart Analysis

**Detects conflict severity:**
- **Critical** - Causes crashes or data corruption
- **High** - Causes incorrect behavior
- **Medium** - Causes performance issues
- **Low** - Causes confusion but works

**Prioritizes resolution:**
1. Critical conflicts first
2. High-impact conflicts
3. Performance conflicts
4. Clarity conflicts

## Integration

Works with:
- **godot-sync-static-positions** - Resolves position conflicts specifically
- **godot-split-scripts** - Separation helps prevent conflicts
- **godot-refactor** (orchestrator) - Runs as part of full refactoring

## Safety

- Each resolution strategy validated
- Behavior preserved or intentionally changed with approval
- Rollback on validation failure
- Original code preserved in git history

## When NOT to Use

Don't "fix" if:
- Intentional override pattern (editor default, code overrides)
- Temporary value (code initializes, then releases control)
- State machine pattern (different modes own property at different times)
- Animation blending (intentional property sharing)

Not all conflicts are bugs - some are architectural patterns.

## Common Conflicts

| Conflict Type | Symptom | Resolution |
|--------------|---------|------------|
| Position in _ready + .tscn | Wrong position in game | Editor wins (move to .tscn) |
| Duplicate signal connection | Event fires multiple times | Check is_connected() first |
| Animation + code rotation | Jittery animation | Animation wins (remove code) |
| RigidBody position control | Physics glitches | Use forces instead |
| _process + _physics_process | Inconsistent behavior | Choose one based on need |

## Benefits

- **Predictability** - Behavior is deterministic
- **Debuggability** - Clear ownership makes issues obvious
- **Performance** - No redundant operations
- **Maintainability** - Clear patterns for future changes
- **WYSIWYG** - Editor preview matches game behavior

## Documentation Added

For each resolution, adds comments like:
```gdscript
# Position is controlled by .tscn (editor-visible)
# Rotation is controlled by AnimationPlayer "idle"
# Scale is controlled by code (dynamic resizing)
```

Clear ownership = clear code.
