---
name: godot-organize-assets
version: 3.0.0
displayName: Organize Asset Files
description: >
  Use when Godot project has disorganized assets (sprites, audio, fonts, materials).
  Detects scattered asset files and organizes them into clear categories with
  consistent naming. Creates sprite atlases where beneficial, organizes audio by
  type, and groups related assets together.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: beginner
audience: [developers]
keywords:
  - godot
  - asset-organization
  - sprites
  - audio
  - sprite-atlases
  - file-structure
  - performance
  - assets
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".png", ".jpg", ".wav", ".ogg", ".ttf", ".glb", ".tres"]
    write: ["*"]
    move: true
    delete: false
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "Organized asset directories, moved files, sprite atlases, naming consistency, git commits"
requirements: "Git repository, Godot 4.x"
execution: "Fully automatic with reference preservation"
integration: "Part of godot-organize-project orchestrator, works with godot-organize-files"
---

# Organize Asset Files

## Core Principle

**Assets organized by type and purpose.** Easy to find, easy to maintain, easy to optimize.

## What This Skill Does

Finds asset directories like:
```
assets/
├── player_sprite.png
├── enemy1.png
├── enemy2.png
├── jump.wav
├── background_music.ogg
├── font.ttf
├── tile1.png
├── tile2.png
└── ... (100 more mixed assets)
```

Transforms to:
```
assets/
├── sprites/
│   ├── characters/
│   │   └── player_sprite.png
│   ├── enemies/
│   │   ├── enemy1.png
│   │   └── enemy2.png
│   └── environment/
│       ├── tiles/
│       │   ├── tile1.png
│       │   └── tile2.png
│       └── atlases/
│           └── environment_atlas.png  # Combined tiles
├── audio/
│   ├── music/
│   │   └── background_music.ogg
│   └── sfx/
│       └── jump.wav
└── fonts/
    └── font.ttf
```

## Detection Patterns

Identifies:
- Assets in wrong categories
- No subdirectory organization
- Inconsistent naming conventions
- Potential sprite atlas opportunities
- Unused/duplicate assets

## When to Use

### Building Asset-Heavy Game
Games with many sprites, sounds, or visual assets.

### Optimizing Performance
Creating sprite atlases reduces draw calls.

### Managing Large Asset Library
Finding specific asset becomes difficult.

### Preparing for Asset Pipeline
Clean structure enables automated processing.

## Process

1. **Scan** - Inventory all asset files by type
2. **Analyze** - Determine logical groupings
3. **Group** - Identify related assets (animation frames, tile sets)
4. **Optimize** - Create sprite atlases where beneficial
5. **Move** - Relocate assets to organized structure
6. **Update** - Fix all references in scenes and scripts
7. **Validate** - Ensure assets load correctly
8. **Commit** - Git commit per asset category

## Organization Strategies

### By Asset Type
Primary organization: sprites, audio, fonts, materials.

### By Domain
Secondary organization: characters, enemies, environment, ui.

### By Purpose
Tertiary organization: animations, icons, backgrounds, effects.

## Sprite Organization

```
sprites/
├── characters/
│   ├── player/
│   │   ├── idle/
│   │   │   ├── idle_01.png
│   │   │   ├── idle_02.png
│   │   │   └── idle_03.png
│   │   ├── run/
│   │   └── jump/
│   └── npc/
├── enemies/
│   ├── goblin/
│   ├── orc/
│   └── dragon/
├── items/
│   ├── weapons/
│   ├── consumables/
│   └── collectibles/
├── environment/
│   ├── tiles/
│   ├── props/
│   └── backgrounds/
└── ui/
    ├── icons/
    ├── buttons/
    └── panels/
```

## Audio Organization

```
audio/
├── music/
│   ├── main_theme.ogg
│   ├── battle_music.ogg
│   └── ambient/
│       ├── forest.ogg
│       └── cave.ogg
├── sfx/
│   ├── player/
│   │   ├── jump.wav
│   │   ├── land.wav
│   │   └── attack.wav
│   ├── enemies/
│   │   ├── hit.wav
│   │   └── death.wav
│   ├── ui/
│   │   ├── click.wav
│   │   └── hover.wav
│   └── environment/
│       ├── door_open.wav
│       └── chest_open.wav
└── voice/  # For games with voice acting
```

## Sprite Atlas Creation

**Detects atlas opportunities:**
- Multiple small sprites used together (UI icons)
- Animation frames (8+ frames in sequence)
- Tileset pieces (can be combined)
- Related sprites loaded simultaneously

**Creates atlases when:**
- 4+ sprites under 128x128 pixels
- Related sprites (same domain)
- Performance benefit (reduce draw calls)

**Example:**
```
# Before: 20 separate UI icon files (20 draw calls)
ui/icons/health_icon.png
ui/icons/mana_icon.png
... (18 more)

# After: 1 atlas texture (1 draw call)
ui/atlases/ui_icons_atlas.png
ui/atlases/ui_icons_atlas.png.import  # Atlas regions defined
```

## Naming Conventions

### Sprites
- `character_player_idle_01.png`
- `enemy_goblin_attack_03.png`
- `item_sword_iron.png`

### Audio
- `music_main_theme.ogg`
- `sfx_player_jump.wav`
- `ambient_forest_birds.ogg`

### Materials
- `mat_character_player.tres`
- `mat_environment_grass.tres`

Consistent naming enables:
- Alphabetical sorting groups related assets
- Easy searching and filtering
- Automated processing scripts

## What Gets Created

- Organized asset directories by type
- Subdirectories by domain/purpose
- Sprite atlases where beneficial
- Renamed files for consistency (optional)
- Updated references in all scenes/scripts
- Git commits per asset category

## Smart Analysis

**Detects usage patterns:**
- Frequently used together → group together
- Animation sequences → organize in frames
- UI elements → candidate for atlas
- Unused assets → flag for review

**Optimizes based on:**
- File size (small sprites → atlas)
- Load frequency (often used → optimize)
- Relationships (animation frames → folder)

## Integration

Works with:
- **godot-organize-files** - Base organization first
- **godot-organize-scripts** - Parallel script organization
- **godot-organize-project** (orchestrator) - Full project organization

## Safety

- All asset references preserved during moves
- Godot .import files regenerated correctly
- Sprite atlas creation validates regions
- Rollback on validation failure
- Original structure in git history

## When NOT to Use

Don't reorganize if:
- Assets already well organized
- External asset management tool in use
- Mid-production (bad timing for large changes)
- Custom organization required by pipeline

## Benefits

- **Performance** - Sprite atlases reduce draw calls
- **Organization** - Find assets quickly
- **Workflow** - Import new assets to correct location
- **Scalability** - Structure supports more assets
- **Collaboration** - Team knows where assets belong

## Atlas Performance

**Without atlases:**
- 20 UI icons = 20 separate textures = 20 draw calls
- 30 enemy sprites = 30 textures = 30 draw calls

**With atlases:**
- 20 UI icons = 1 atlas texture = 1 draw call
- 30 enemy sprites = 2-3 atlases = 2-3 draw calls

Significant performance improvement, especially for mobile.

## Common Transformations

| Before | After |
|--------|-------|
| `player.png` in root | `assets/sprites/characters/player/idle.png` |
| `sound.wav` mixed | `assets/audio/sfx/player/jump.wav` |
| 20 icons scattered | `assets/sprites/ui/atlases/ui_atlas.png` |
| `font.ttf` in assets | `assets/fonts/main_font.ttf` |

## Configuration Options

- Enable/disable sprite atlas creation
- Minimum atlas sprite count (default: 4)
- Maximum atlas size (default: 4096x4096)
- Naming convention style
- Organization depth (flat vs deep hierarchy)

Defaults follow Godot best practices and performance guidelines.
