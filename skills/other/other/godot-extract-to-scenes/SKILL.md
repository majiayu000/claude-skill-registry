---
name: godot-extract-to-scenes
version: 3.0.0
displayName: Extract Code-Created Objects to Scenes
description: >
  Use when building Godot features and your code creates nodes with .new() instead
  of using scenes. Detects Timer.new(), Area2D.new(), Sprite2D.new() and other
  code-created objects. Automatically generates .tscn scene files, updates parent
  scripts with @onready references, and creates reusable component library.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: intermediate
audience: [developers]
keywords:
  - godot
  - scene-extraction
  - component-library
  - new-operator
  - node-creation
  - code-refactoring
  - tscn-generation
  - gdscript
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".gd", ".tscn", ".tres"]
    write: [".tscn", ".tres", ".gd"]
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "Component library with .tscn scenes, preset resources, updated parent scripts, git commits"
requirements: "Git repository, Godot 4.x"
execution: "Fully automatic with git commits per component"
integration: "Part of godot-refactor orchestrator, works with godot-split-scripts"
---

# Extract Code-Created Objects to Scenes

## Core Principle

**Every node should be a scene.** Code-created objects with `.new()` should be rare exceptions for truly dynamic content.

## What This Skill Does

Finds patterns like:
```gdscript
var timer = Timer.new()
timer.wait_time = 2.0
timer.one_shot = true
add_child(timer)
```

Transforms to:
```gdscript
@onready var timer: Timer = $Timer
# Timer is now a scene node, configured in editor
```

## Detection Patterns

Scans for:
- `Timer.new()`
- `Area2D.new()`, `CollisionShape2D.new()`
- `Sprite2D.new()`, `AnimatedSprite2D.new()`
- `AudioStreamPlayer.new()`, `AudioStreamPlayer2D.new()`
- `Control.new()`, `Label.new()`, `Button.new()`
- Any `Node*.new()` pattern

## When to Use

### You're Building New Features
Your code creates objects dynamically that should actually be scenes.

### You're Refactoring Legacy Code
Old code has `.new()` calls that make nodes invisible in editor.

### You Want Inspector Visibility
You want to configure properties in the Godot editor, not in code.

## Process

1. **Scan** - Find all `.new()` patterns in .gd files
2. **Analyze** - Determine node type, properties, parent relationships
3. **Generate** - Create .tscn scene files with proper configuration
4. **Update** - Replace code creation with @onready references
5. **Commit** - Git commit per component extracted

## Example Transformation

**Before:**
```gdscript
# player.gd
func _ready():
    var hitbox = Area2D.new()
    hitbox.name = "Hitbox"
    var collision = CollisionShape2D.new()
    var shape = RectangleShape2D.new()
    shape.size = Vector2(32, 48)
    collision.shape = shape
    hitbox.add_child(collision)
    add_child(hitbox)
```

**After:**
```gdscript
# player.gd
@onready var hitbox: Area2D = $Hitbox
# Hitbox is now configured as scene node in player.tscn
```

**Generated File:**
```ini
# components/hitbox_component.tscn
[gd_scene load_steps=2 format=3]

[sub_resource type="RectangleShape2D" id="1"]
size = Vector2(32, 48)

[node name="Hitbox" type="Area2D"]

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("1")
```

## What Gets Created

- Component library in `components/` directory
- .tscn scene files with proper node hierarchy
- Preset .tres files for reusable configurations
- Updated parent scripts with @onready references
- Git commits documenting each extraction

## Smart Detection

**Skips intentional dynamic creation:**
- Objects created in loops (spawning enemies)
- Objects created conditionally (different weapon types)
- Objects with variable types (plugin systems)

**Focuses on static objects:**
- Same object created every time
- Properties set to constant values
- Should exist in editor for visibility

## Integration

Works with:
- **godot-split-scripts** - Extract, then split large scripts
- **godot-add-signals** - Use signals with extracted components
- **godot-refactor** (orchestrator) - Runs as part of full refactoring

## Safety

- Every operation creates a git commit
- Validation tests run after extraction
- Auto-rollback on test failure
- Original code preserved in git history

## When NOT to Use

Don't extract if:
- Object is created dynamically (in loop, based on data)
- Object type varies at runtime
- Object is truly temporary (created and destroyed frequently)
- Code is already using PackedScene.instantiate()

These are legitimate uses of `.new()` and should remain as code.
