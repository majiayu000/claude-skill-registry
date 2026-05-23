---
name: godot-extract-resources
version: 3.0.0
displayName: Extract Data to Resources
description: >
  Use when Godot code has hardcoded game data in const arrays, dictionaries, or
  embedded values. Detects inline data like enemy stats, item definitions, level
  configurations. Automatically extracts to .tres resource files, making data
  visible in editor, easily modifiable, and supports data-driven design.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: beginner
audience: [developers]
keywords:
  - godot
  - resources
  - data-driven
  - const-arrays
  - dictionaries
  - tres-files
  - gdscript
  - game-data
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".gd", ".tres"]
    write: [".gd", ".tres", ".tscn"]
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "Resource files (.tres), Resource script definitions, updated code using resources, git commits"
requirements: "Git repository, Godot 4.x"
execution: "Fully automatic with data preservation"
integration: "Part of godot-refactor orchestrator, creates data-driven architecture"
---

# Extract Data to Resources

## Core Principle

**Data belongs in resources, not code.** Hardcoded values make iteration slow and error-prone.

## What This Skill Does

Finds patterns like:
```gdscript
# enemy.gd
const ENEMY_DATA = {
    "goblin": {"health": 50, "speed": 100, "damage": 10},
    "orc": {"health": 100, "speed": 80, "damage": 20},
    "dragon": {"health": 500, "speed": 150, "damage": 50}
}
```

Transforms to:
```gdscript
# enemy_stats.gd
class_name EnemyStats
extends Resource

@export var enemy_name: String
@export var health: int
@export var speed: float
@export var damage: int
```

Creates resource files:
- `resources/enemies/goblin.tres`
- `resources/enemies/orc.tres`
- `resources/enemies/dragon.tres`

Updates code:
```gdscript
# enemy.gd
@export var stats: EnemyStats

func _ready():
    health = stats.health
    speed = stats.speed
    damage = stats.damage
```

## Detection Patterns

Identifies:
- `const` arrays with data structures
- Dictionaries with game data
- Embedded configuration values
- Hardcoded stats, properties, settings
- Switch statements on type strings

## When to Use

### You're Building Data-Heavy Games
Games with many items, enemies, levels, or configurations.

### You're Iterating on Balance
Want to tweak values quickly without code changes.

### You're Working with Designers
Non-programmers need to edit game data.

### You're Adding Moddability
External data files enable modding support.

## Process

1. **Scan** - Find const arrays, dictionaries with structured data
2. **Analyze** - Identify data schema and relationships
3. **Define** - Create Resource class definitions
4. **Extract** - Generate .tres files with data
5. **Update** - Modify code to load resources
6. **Validate** - Ensure data loads correctly
7. **Commit** - Git commit per resource type

## Example Transformation

**Before (Hardcoded Data):**
```gdscript
# item_manager.gd
const ITEMS = [
    {
        "id": "health_potion",
        "name": "Health Potion",
        "description": "Restores 50 HP",
        "heal_amount": 50,
        "icon": "res://icons/potion.png"
    },
    {
        "id": "sword",
        "name": "Iron Sword",
        "description": "A basic sword",
        "damage": 15,
        "icon": "res://icons/sword.png"
    }
]

func get_item(id: String):
    for item in ITEMS:
        if item.id == id:
            return item
    return null
```

**After (Resource-Based):**
```gdscript
# item_data.gd
class_name ItemData
extends Resource

@export var id: String
@export var item_name: String
@export_multiline var description: String
@export var icon: Texture2D
@export_group("Stats")
@export var heal_amount: int
@export var damage: int
```

```gdscript
# item_manager.gd
@export var items: Array[ItemData]

func get_item(id: String) -> ItemData:
    for item in items:
        if item.id == id:
            return item
    return null
```

**Created Files:**
- `resources/items/health_potion.tres`
- `resources/items/iron_sword.tres`

## Resource Patterns

### Simple Resources
Single values (stats, settings, constants).

### Composite Resources
Resources referencing other resources (weapon + stats + effects).

### Resource Libraries
Arrays of resources for different categories.

### Resource Inheritance
Base resource class with specialized variants.

## What Gets Created

- Resource class definitions in `resources/` or `scripts/resources/`
- .tres files in organized directory structure
- Updated code using @export var resource: ResourceType
- Documentation of resource schema
- Git commits per resource extraction

## Smart Analysis

**Identifies data types:**
- **Configuration** - Settings, constants, tuning values
- **Content** - Items, enemies, levels, abilities
- **Behavior** - AI patterns, state machines, rules

**Organizes by category:**
- `resources/items/` - Item data
- `resources/enemies/` - Enemy stats
- `resources/levels/` - Level configurations
- `resources/abilities/` - Ability definitions

## Integration

Works with:
- **godot-extract-to-scenes** - Scenes reference resources
- **godot-split-scripts** - Resources reduce script size
- **godot-refactor** (orchestrator) - Runs as part of full refactoring

## Safety

- Data preserved exactly during extraction
- Validation ensures resources load correctly
- Rollback on validation failure
- Original data preserved in git history

## When NOT to Use

Don't extract if:
- Data is truly constant (math constants, engine limits)
- Data changes at runtime (calculated values)
- Data is temporary state (not configuration)
- Extraction makes code more complex

Examples of valid hardcoded data:
- `const PI = 3.14159`
- `const MAX_PLAYERS = 4` (engine limitation)
- Calculated values based on other data

## Resource Organization

```
resources/
├── items/
│   ├── consumables/
│   │   ├── health_potion.tres
│   │   └── mana_potion.tres
│   └── weapons/
│       ├── iron_sword.tres
│       └── steel_axe.tres
├── enemies/
│   ├── goblin.tres
│   ├── orc.tres
│   └── dragon.tres
└── levels/
    ├── level_1.tres
    └── level_2.tres
```

## Benefits

- **Rapid iteration** - Change data without recompiling
- **Designer-friendly** - Edit values in Godot inspector
- **Type safety** - @export provides validation and autocomplete
- **Moddability** - External .tres files can be modified
- **Version control** - Data changes tracked separately from code
- **Hot reload** - Godot reloads resource changes automatically

## Common Transformations

| Before (Hardcoded) | After (Resource) |
|-------------------|------------------|
| `const STATS = {...}` | `@export var stats: Stats` |
| `var data = ITEMS[0]` | `var data = preload("item.tres")` |
| `if type == "fire":` | `if ability.element == Element.FIRE:` |
| `const CONFIG = {...}` | `@export var config: GameConfig` |

## Resource Types

### Built-in Resources
- Texture2D, Material, AudioStream
- Animation, Curve, Gradient
- Theme, StyleBox, Font

### Custom Resources
- EnemyStats, ItemData, LevelConfig
- AbilityDefinition, QuestData
- Any game-specific data structure

### Resource Collections
- Array[ItemData] for item databases
- Dictionary for lookup tables
- Resource library scenes
