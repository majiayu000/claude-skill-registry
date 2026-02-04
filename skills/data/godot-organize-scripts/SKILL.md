---
name: godot-organize-scripts
version: 3.0.0
displayName: Organize Script Files
description: >
  Use when Godot project has scripts scattered without clear organization. Detects
  scripts and organizes them by category (characters, enemies, components, managers,
  utilities). Creates clear structure showing architectural layers and relationships.
  Preserves all references and class_name declarations.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: beginner
audience: [developers]
keywords:
  - godot
  - script-organization
  - gdscript
  - file-structure
  - code-architecture
  - components
  - managers
  - best-practices
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".gd"]
    write: ["*"]
    move: true
    delete: false
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "Organized script directories, moved files with preserved references, git commits"
requirements: "Git repository, Godot 4.x"
execution: "Fully automatic with reference preservation"
integration: "Part of godot-organize-project orchestrator, works with godot-split-scripts"
---

# Organize Script Files

## Core Principle

**Scripts organized by architectural layer and responsibility.** Code structure reveals design.

## What This Skill Does

Finds script directories like:
```
scripts/
├── player.gd
├── enemy.gd
├── health_component.gd
├── game_manager.gd
├── utility.gd
├── inventory.gd
├── ui_manager.gd
└── ... (50 more scripts)
```

Transforms to:
```
scripts/
├── characters/
│   ├── player.gd
│   └── character_base.gd
├── enemies/
│   ├── enemy.gd
│   ├── goblin.gd
│   └── enemy_ai.gd
├── components/
│   ├── health_component.gd
│   ├── movement_component.gd
│   └── combat_component.gd
├── managers/
│   ├── game_manager.gd
│   ├── ui_manager.gd
│   └── audio_manager.gd
├── systems/
│   └── inventory.gd
└── utility/
    ├── math_helper.gd
    └── constants.gd
```

## Detection Patterns

Identifies:
- Scripts by architectural role
- Base classes vs implementations
- Reusable components vs specific entities
- System/manager scripts
- Utility/helper scripts

## When to Use

### Growing Codebase
Scripts have multiplied and organization is lost.

### Understanding Architecture
Want folder structure to reflect design.

### Team Onboarding
New developers need to navigate code quickly.

### Before Major Refactoring
Clean organization makes refactoring safer.

## Process

1. **Scan** - Inventory all .gd files and analyze content
2. **Classify** - Determine category based on role and naming
3. **Group** - Find related scripts (inheritance, dependencies)
4. **Plan** - Create target directory structure
5. **Move** - Relocate scripts preserving references
6. **Update** - Fix paths in preload(), extends, scenes
7. **Validate** - Ensure all scripts load correctly
8. **Commit** - Git commit per category moved

## Organization Structure

### Characters
Scripts for player and NPCs.
```
characters/
├── player.gd
├── npc.gd
├── character_base.gd
└── character_state_machine.gd
```

### Enemies
Scripts for enemy entities and AI.
```
enemies/
├── enemy_base.gd
├── goblin.gd
├── orc.gd
├── ai/
│   ├── enemy_ai.gd
│   ├── patrol_ai.gd
│   └── chase_ai.gd
└── behaviors/
    ├── attack_behavior.gd
    └── flee_behavior.gd
```

### Components
Reusable component scripts.
```
components/
├── health_component.gd
├── movement_component.gd
├── combat_component.gd
├── inventory_component.gd
└── hitbox_component.gd
```

### Managers
Singleton-style manager scripts.
```
managers/
├── game_manager.gd
├── audio_manager.gd
├── scene_manager.gd
├── save_manager.gd
└── input_manager.gd
```

### Systems
Game systems (inventory, quests, dialog).
```
systems/
├── inventory_system.gd
├── quest_system.gd
├── dialog_system.gd
└── crafting_system.gd
```

### UI
UI-specific scripts.
```
ui/
├── main_menu.gd
├── pause_menu.gd
├── hud.gd
├── inventory_ui.gd
└── widgets/
    ├── health_bar.gd
    └── button_hover.gd
```

### Utility
Helper and utility scripts.
```
utility/
├── constants.gd
├── math_helper.gd
├── vector_utils.gd
└── debug_draw.gd
```

### Resources (Script Definitions)
Custom Resource class definitions.
```
resources/
├── item_data.gd
├── enemy_stats.gd
├── ability_definition.gd
└── level_config.gd
```

## Classification Logic

### Character Scripts
- Names contain "player", "npc", "character"
- Extend CharacterBody2D or custom character base
- Handle player/NPC-specific logic

### Enemy Scripts
- Names contain "enemy", "monster", mob types
- Extend enemy base or have AI logic
- Handle hostile entity behavior

### Component Scripts
- Names end with "_component"
- Designed for reuse across entities
- Single responsibility (health, movement, etc.)

### Manager Scripts
- Names end with "_manager"
- Often autoloaded singletons
- Manage global state or services

### System Scripts
- Names end with "_system"
- Handle game mechanics (inventory, quests)
- Domain-specific logic

### Utility Scripts
- Names like "helper", "utils", "constants"
- Stateless helper functions
- Mathematical or string utilities

## What Gets Created

- Organized script directories by category
- Subdirectories for specialized groupings
- Moved scripts with preserved references
- Updated class_name references
- Updated autoload paths in project.godot
- Git commits per category

## Smart Analysis

**Detects relationships:**
- Inheritance (base classes with implementations)
- Dependencies (scripts that preload others)
- Naming patterns (conventions reveal purpose)

**Maintains cohesion:**
- Related scripts stay together
- Base + derived classes in same category
- Component families grouped

## Reference Updates

### Script Preloads
```gdscript
# Before
const EnemyScene = preload("res://enemy.gd")

# After
const EnemyScene = preload("res://scripts/enemies/enemy.gd")
```

### Class Extends
```gdscript
# Before
extends "res://character_base.gd"

# After
extends "res://scripts/characters/character_base.gd"
```

### Scene Script Attachments
```ini
# Before
[ext_resource path="res://player.gd" type="Script"]

# After
[ext_resource path="res://scripts/characters/player.gd" type="Script"]
```

## Integration

Works with:
- **godot-split-scripts** - Split first, then organize
- **godot-organize-files** - Base file organization
- **godot-organize-project** (orchestrator) - Full project organization

## Safety

- All script references preserved
- class_name declarations work correctly
- Autoload paths updated automatically
- Rollback on validation failure
- Original structure in git history

## When NOT to Use

Don't reorganize if:
- Scripts already well organized
- Custom structure required by architecture
- Mid-sprint (bad timing)
- External tools rely on current paths

## Benefits

- **Discoverability** - Find scripts by responsibility
- **Architecture Visibility** - Structure reflects design
- **Onboarding** - New developers navigate easily
- **Refactoring** - Clear boundaries for changes
- **Testing** - Easier to test by layer

## Naming Conventions

**Optional: Rename during organization**
- `PlayerController.gd` → `player_controller.gd` (snake_case)
- `EnemyAI.gd` → `enemy_ai.gd`

Godot convention prefers snake_case for file names.

## Architecture Layers

**Typical hierarchy:**
1. **Entities** - characters/, enemies/
2. **Components** - components/
3. **Systems** - systems/, managers/
4. **UI** - ui/
5. **Utilities** - utility/

Organization reflects dependency direction (utilities depend on nothing, entities depend on everything).

## Common Transformations

| Before | After |
|--------|-------|
| `player.gd` in scripts/ | `scripts/characters/player.gd` |
| `enemy_ai.gd` in scripts/ | `scripts/enemies/ai/enemy_ai.gd` |
| `health_component.gd` mixed | `scripts/components/health_component.gd` |
| `game_manager.gd` in root | `scripts/managers/game_manager.gd` |
| `utils.gd` scattered | `scripts/utility/math_helper.gd` |

## Configuration

Can be customized for:
- Different architectural patterns (MVC, ECS-like, etc.)
- Team-specific categories
- Domain-specific groupings
- Depth of organization (flat vs deep)

Defaults follow Godot component-based architecture patterns.
