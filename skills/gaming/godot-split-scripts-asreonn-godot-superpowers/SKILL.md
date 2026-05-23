---
name: godot-split-scripts
version: 3.0.0
displayName: Split Monolithic Scripts
description: >
  Use when Godot scripts exceed 150 lines or have multiple responsibilities.
  Detects scripts doing too many things (player movement + combat + inventory + UI).
  Automatically splits into focused scripts following Single Responsibility Principle,
  preserves behavior exactly, and creates git commits per split.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: intermediate
audience: [developers]
keywords:
  - godot
  - script-splitting
  - refactoring
  - single-responsibility
  - component-pattern
  - gdscript
  - code-organization
  - monolithic-scripts
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

outputs: "Split scripts with single responsibilities, preserved behavior, git commits per split"
requirements: "Git repository, Godot 4.x"
execution: "Fully automatic with behavior validation"
integration: "Part of godot-refactor orchestrator, works with godot-add-signals"
---

# Split Monolithic Scripts

## Core Principle

**One script, one responsibility.** Scripts over 150 lines usually do too many things.

## What This Skill Does

Finds scripts like:
```gdscript
# player.gd - 500 lines
class_name Player
extends CharacterBody2D

# Movement (lines 1-100)
func _physics_process(delta): ...
func handle_input(): ...
func move(): ...

# Combat (lines 101-200)
func take_damage(amount): ...
func attack(): ...
func die(): ...

# Inventory (lines 201-350)
func add_item(item): ...
func remove_item(item): ...
func use_item(item): ...

# UI (lines 351-500)
func update_health_bar(): ...
func show_inventory(): ...
```

Transforms to:
```gdscript
# player.gd - 50 lines (orchestrator)
class_name Player
extends CharacterBody2D

@onready var movement = $MovementComponent
@onready var combat = $CombatComponent
@onready var inventory = $InventoryComponent
@onready var ui = $UIComponent

# Delegates to components
```

## Detection Patterns

Identifies scripts that:
- Exceed 150 lines
- Have multiple logical sections (comments like "# Movement", "# Combat")
- Handle unrelated concerns (physics + UI + data management)
- Have many exported variables for different systems
- Mix different levels of abstraction

## When to Use

### You're Building New Features
Adding new functionality to already-large script makes it worse.

### You're Debugging Complex Code
Large scripts are hard to reason about and test.

### You're Preparing for Team Work
Smaller scripts reduce merge conflicts and improve code review.

### You're Adding Tests
Single-responsibility scripts are easier to test in isolation.

## Process

1. **Scan** - Find scripts exceeding 150 lines
2. **Analyze** - Identify logical groupings and responsibilities
3. **Split** - Extract each responsibility to its own script
4. **Preserve** - Ensure behavior remains exactly the same
5. **Validate** - Run tests to confirm no regressions
6. **Commit** - Git commit per split operation

## Example Transformation

**Before (player.gd - 300 lines):**
```gdscript
extends CharacterBody2D

const SPEED = 300.0
const JUMP_VELOCITY = -400.0

var health = 100
var max_health = 100
var inventory = []

func _physics_process(delta):
    # Movement logic (50 lines)
    ...

func take_damage(amount):
    # Combat logic (30 lines)
    ...

func add_item(item):
    # Inventory logic (40 lines)
    ...

func update_ui():
    # UI logic (30 lines)
    ...
```

**After (player.gd - 30 lines):**
```gdscript
extends CharacterBody2D

@onready var movement: MovementComponent = $MovementComponent
@onready var combat: CombatComponent = $CombatComponent
@onready var inventory: InventoryComponent = $InventoryComponent
@onready var ui: UIComponent = $UIComponent

func _ready():
    combat.health_changed.connect(ui.update_health_bar)
    inventory.item_added.connect(ui.update_inventory)
```

**New Files Created:**
- `movement_component.gd` - Handles SPEED, JUMP_VELOCITY, _physics_process
- `combat_component.gd` - Handles health, take_damage, die
- `inventory_component.gd` - Handles inventory array, add_item, remove_item
- `ui_component.gd` - Handles update_health_bar, show_inventory

## Split Strategies

### By Domain
Split by game concepts (movement, combat, inventory).

### By Layer
Split by abstraction (input handling, state management, rendering).

### By Responsibility
Split by what changes for different reasons.

## What Gets Created

- Component scripts with single clear purpose
- Preserved @export variables in correct locations
- Signal connections for component communication
- Updated scene files with new component nodes
- Git commits documenting each split

## Smart Analysis

**Identifies clear boundaries:**
- Functions that operate on same variables
- Logical groupings indicated by comments
- Related functionality (all UI, all physics)

**Preserves integration:**
- Main script delegates to components
- Signals connect components when needed
- Public API remains compatible

## Integration

Works with:
- **godot-extract-to-scenes** - Split after extracting scenes
- **godot-add-signals** - Add signals for component communication
- **godot-refactor** (orchestrator) - Runs as part of full refactoring

## Safety

- Behavior preserved exactly (no functional changes)
- Validation tests run after each split
- Auto-rollback on test failure
- Git history preserves original script

## When NOT to Use

Don't split if:
- Script under 150 lines and focused
- Script has single clear responsibility
- Splitting would make code harder to understand
- Functions are tightly coupled and can't be separated

Keep simple things simple.

## Threshold Configuration

Default: 150 lines (Godot best practice)

Can be adjusted based on:
- Team preferences
- Script complexity
- Domain requirements

Scripts under threshold are skipped unless they have obvious multiple responsibilities.
