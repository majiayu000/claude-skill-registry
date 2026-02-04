---
name: godot-organize-files
version: 3.0.0
displayName: Organize Project File Structure
description: >
  Use when Godot project has scattered files with no clear organization. Detects
  assets, scripts, scenes, and resources in root or inconsistent locations.
  Automatically creates organized directory structure following Godot best practices,
  moves files preserving references, and updates all dependencies.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: beginner
audience: [developers]
keywords:
  - godot
  - file-organization
  - directory-structure
  - project-cleanup
  - best-practices
  - asset-management
  - gdscript
  - godot-project
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: ["*"]
    write: ["*"]
    move: true
    delete: false
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "Organized directory structure, moved files with preserved references, git commits"
requirements: "Git repository, Godot 4.x"
execution: "Fully automatic with reference preservation"
integration: "Part of godot-organize-project orchestrator, works with organize-assets and organize-scripts"
---

# Organize Project File Structure

## Core Principle

**Clear structure = easy navigation.** Files should be where you expect them.

## What This Skill Does

Finds projects like:
```
my_game/
├── project.godot
├── player.gd
├── enemy.gd
├── sprite1.png
├── sound.wav
├── level1.tscn
├── main_menu.tscn
├── utility.gd
└── ... (50 more files in root)
```

Transforms to:
```
my_game/
├── project.godot
├── assets/
│   ├── sprites/
│   │   └── sprite1.png
│   └── audio/
│       └── sound.wav
├── scenes/
│   ├── levels/
│   │   └── level1.tscn
│   └── ui/
│       └── main_menu.tscn
└── scripts/
    ├── player.gd
    ├── enemy.gd
    └── utility.gd
```

## Detection Patterns

Identifies:
- Files in root directory that should be organized
- Inconsistent naming (CamelCase, snake_case mixed)
- Assets mixed with code
- No logical grouping by type or domain

## When to Use

### Starting New Project
Establish structure from the beginning.

### Inheriting Legacy Project
Project has grown organically without structure.

### Preparing for Collaboration
Team needs consistent file locations.

### Before Major Refactoring
Clean structure makes refactoring easier.

## Process

1. **Scan** - Inventory all project files and current structure
2. **Analyze** - Determine file types and relationships
3. **Plan** - Create target directory structure
4. **Move** - Relocate files preserving all references
5. **Update** - Fix paths in .tscn, .gd, project.godot
6. **Validate** - Ensure all references still work
7. **Commit** - Git commit per logical grouping moved

## Standard Structure

### Recommended Organization

```
project_root/
├── project.godot
├── assets/
│   ├── sprites/
│   │   ├── characters/
│   │   ├── enemies/
│   │   ├── items/
│   │   └── environment/
│   ├── audio/
│   │   ├── music/
│   │   ├── sfx/
│   │   └── voice/
│   ├── fonts/
│   ├── materials/
│   ├── shaders/
│   └── models/       # For 3D projects
├── scenes/
│   ├── characters/
│   ├── enemies/
│   ├── levels/
│   ├── ui/
│   └── components/
├── scripts/
│   ├── characters/
│   ├── enemies/
│   ├── components/
│   ├── managers/
│   └── utility/
├── resources/
│   ├── items/
│   ├── enemies/
│   └── abilities/
├── addons/           # Third-party plugins
└── docs/             # Documentation (optional)
```

## What Gets Created

- Organized directory structure
- Moved files with preserved references
- Updated .tscn files with new paths
- Updated script preload() paths
- Updated project.godot autoloads
- Git commits documenting organization

## Smart Analysis

**Detects file types:**
- **Assets** - .png, .jpg, .wav, .ogg, .ttf, .glb
- **Scenes** - .tscn, .scn
- **Scripts** - .gd, .cs
- **Resources** - .tres, .res
- **Config** - .cfg, .json, project.godot

**Determines grouping:**
- By type (sprites, scripts, scenes)
- By domain (characters, enemies, ui)
- By function (components, managers, utilities)

## Integration

Works with:
- **godot-organize-assets** - Further organizes asset files
- **godot-organize-scripts** - Further organizes script files
- **godot-organize-project** (orchestrator) - Runs as part of full organization

## Safety

- All file references preserved during moves
- Godot's .import files updated automatically
- Rollback on validation failure
- Original structure preserved in git history

## When NOT to Use

Don't reorganize if:
- Project already has clear structure
- Mid-development sprint (bad timing)
- Custom structure intentionally different
- External tools rely on current paths

## Path Updates

### Script Updates
```gdscript
# Before
var scene = preload("res://player.tscn")

# After
var scene = preload("res://scenes/characters/player.tscn")
```

### Scene Updates
```ini
# Before
[ext_resource path="res://player.gd" type="Script"]

# After
[ext_resource path="res://scripts/characters/player.gd" type="Script"]
```

### Autoload Updates
```ini
# Before
[autoload]
GameManager="*res://game_manager.gd"

# After
[autoload]
GameManager="*res://scripts/managers/game_manager.gd"
```

## Organization Strategies

### By Type (Simple Projects)
Group all sprites together, all scripts together.

### By Domain (Medium Projects)
Group by game concept (characters, enemies, levels).

### By Feature (Large Projects)
Group by feature (combat system, inventory system).

### Hybrid
Combine strategies (assets by type, scripts by domain).

## Benefits

- **Discoverability** - Find files where you expect them
- **Scalability** - Structure supports growth
- **Onboarding** - New team members navigate easily
- **Consistency** - Same structure across projects
- **Tooling** - Tools work better with organized projects

## Common Patterns

| Before | After |
|--------|-------|
| `player.gd` in root | `scripts/characters/player.gd` |
| `sprite.png` in root | `assets/sprites/characters/sprite.png` |
| `level.tscn` in root | `scenes/levels/level.tscn` |
| `item_data.tres` in root | `resources/items/item_data.tres` |

## Configuration

Can be customized for:
- Different naming conventions
- Alternative structures (src/ instead of scripts/)
- Project-specific requirements
- Team preferences

Default follows Godot best practices and community standards.
