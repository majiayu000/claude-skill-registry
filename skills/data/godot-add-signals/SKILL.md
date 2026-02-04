---
name: godot-add-signals
version: 3.0.0
displayName: Replace Coupling with Signals
description: >
  Use when Godot code has tight coupling via get_node(), get_parent(), or direct
  references creating brittle dependencies. Detects coupling patterns and transforms
  to signal-based communication. Components become independent, testable, and reusable.
  Preserves exact behavior while improving architecture.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: intermediate
audience: [developers]
keywords:
  - godot
  - signals
  - decoupling
  - get-node
  - get-parent
  - architecture
  - gdscript
  - loose-coupling
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

outputs: "Signal definitions, signal connections, decoupled components, git commits"
requirements: "Git repository, Godot 4.x"
execution: "Fully automatic with behavior preservation"
integration: "Part of godot-refactor orchestrator, works with godot-split-scripts"
---

# Replace Coupling with Signals

## Core Principle

**Components communicate via signals, not direct references.** Coupling makes code brittle and hard to test.

## What This Skill Does

Finds patterns like:
```gdscript
# player.gd
func take_damage(amount):
    health -= amount
    get_node("../UI/HealthBar").update(health)  # TIGHT COUPLING
    get_parent().get_node("ScoreManager").reduce_score()  # FRAGILE PATH
```

Transforms to:
```gdscript
# player.gd
signal health_changed(new_health)

func take_damage(amount):
    health -= amount
    health_changed.emit(health)  # SIGNAL - NO COUPLING
```

```gdscript
# main.gd (or scene setup)
func _ready():
    player.health_changed.connect(ui.health_bar.update)
    player.health_changed.connect(score_manager.on_player_damaged)
```

## Detection Patterns

Identifies:
- `get_node("../path")` - Upward path navigation
- `get_parent().something` - Parent dependencies
- `find_child("name")` - Runtime searches
- `has_method()` - Tight interface coupling
- Direct owner references creating circular dependencies

## When to Use

### You're Refactoring Legacy Code
Old code has spaghetti dependencies via get_node chains.

### You're Building Testable Systems
Want to test components in isolation without full scene tree.

### You're Creating Reusable Components
Components should work in different contexts without modification.

### You're Experiencing Brittle Code
Changes to scene structure break unrelated functionality.

## Process

1. **Scan** - Find all get_node(), get_parent(), find_child() usage
2. **Analyze** - Identify what information flows between nodes
3. **Define Signals** - Create signal definitions for communication
4. **Replace** - Convert direct calls to signal emissions
5. **Connect** - Wire signals in appropriate orchestration points
6. **Validate** - Ensure behavior preserved exactly
7. **Commit** - Git commit per coupling removal

## Example Transformation

**Before (Tight Coupling):**
```gdscript
# enemy.gd
extends CharacterBody2D

func die():
    var player = get_node("../Player")  # FRAGILE PATH
    player.add_score(100)

    var audio = get_parent().get_node("AudioManager")  # TIGHT COUPLING
    audio.play_sound("enemy_death")

    queue_free()
```

**After (Signal-Based):**
```gdscript
# enemy.gd
extends CharacterBody2D

signal died(score_value: int)
signal death_sound_requested(sound_name: String)

func die():
    died.emit(100)
    death_sound_requested.emit("enemy_death")
    queue_free()
```

```gdscript
# main.gd (orchestrator)
func _ready():
    for enemy in enemies:
        enemy.died.connect(player.add_score)
        enemy.death_sound_requested.connect(audio_manager.play_sound)
```

## Signal Patterns

### One-to-Many
One emitter, multiple listeners (health changed → update UI + save game + achievement check).

### Event Broadcasting
Announce something happened without knowing who cares.

### Request-Response
Request service without knowing provider (request_ammo → whoever handles ammo).

### State Change Notification
Notify when state changes (entered_water, jumped, landed).

## What Gets Created

- Signal definitions with typed parameters
- Signal emission at appropriate points
- Signal connections in orchestrator scripts
- Documentation of signal purpose and parameters
- Git commits documenting each decoupling

## Smart Analysis

**Identifies coupling types:**
- **Structural coupling** - Depends on scene tree structure
- **Interface coupling** - Calls specific methods on other nodes
- **Data coupling** - Accesses data from other nodes

**Chooses appropriate solution:**
- Signals for events and notifications
- Dependency injection for services
- Scene composition for reusable components

## Integration

Works with:
- **godot-split-scripts** - Split first, then decouple
- **godot-extract-to-scenes** - Extract scenes, then add signals
- **godot-refactor** (orchestrator) - Runs as part of full refactoring

## Safety

- Behavior preserved exactly
- Signal connections tested automatically
- Rollback on validation failure
- Original coupling preserved in git history

## When NOT to Use

Don't add signals if:
- Parent-child relationship is intentional design
- Component genuinely needs specific parent type
- Coupling is within same responsibility boundary
- Adding signals makes code more complex, not simpler

Examples of valid coupling:
- UI button calling parent dialog's close method
- Child node accessing parent's exported properties
- Component accessing owner's public API

## Signal Naming Conventions

**Events (past tense):**
- `health_changed`
- `item_collected`
- `enemy_died`

**Requests (imperative):**
- `damage_requested`
- `play_sound`
- `spawn_particle`

**State Changes:**
- `entered_state`
- `exited_state`
- `state_changed`

## Benefits

- **Testability** - Test components without full scene tree
- **Reusability** - Components work in different contexts
- **Flexibility** - Add/remove listeners without changing emitter
- **Maintainability** - Changes don't break distant code
- **Clarity** - Signal connections show system architecture

## Common Transformations

| Before (Coupled) | After (Signal-Based) |
|------------------|---------------------|
| `get_node("../Player").damage()` | `damage_dealt.emit()` → player listens |
| `get_parent().update_ui()` | `ui_update_requested.emit()` → UI listens |
| `owner.score += 10` | `score_changed.emit(10)` → owner listens |
| `find_child("Camera").shake()` | `screen_shake_requested.emit()` → camera listens |
