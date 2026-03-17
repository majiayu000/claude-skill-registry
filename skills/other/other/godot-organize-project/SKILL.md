---
name: godot-organize-project
version: 3.0.0
displayName: "Godot Project Organization Orchestrator"
description: >
  Use when you need to reorganize project folder structure, consolidate similar files,
  organize resources by type, and create a clean project architecture from current folder
  chaos. Orchestrates all 3 organization mini-skills: organize-files, organize-assets,
  and organize-scripts. Each operation runs independently with reference preservation.
author: "Asreonn"
license: MIT
category: game-development
type: agent
difficulty: beginner
audience: [developers, teams]
keywords:
  - godot
  - organization
  - project-structure
  - folder-structure
  - assets
  - scripts
  - scenes
  - godot4
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme
filesystem:
  read:
    - "${PROJECT_ROOT}/**/*"
    - "${PROJECT_ROOT}/project.godot"
  write:
    - "${PROJECT_ROOT}/**/*"
  deny:
    - "**/.env*"
    - "**/secrets*"
    - "**/*.key"
    - "**/.git/**"
behavior:
  timeout: 300
  retry: 2
  cache: false
  interactive: true
use_cases:
  - "Project files scattered everywhere with no structure"
  - "Assets and scripts mixed in root directory"
  - "Can't find files because no organizational system"
  - "Want to prepare project for team collaboration"
  - "Need consistent structure across projects"
  - "Want to organize everything at once"
outputs: "Organized directory structure, moved files with preserved references, git commits per category"
requirements: "Git repository, Godot 4.x"
execution: "Fully automatic with reference preservation"
auto_rollback: "Yes - reverts on validation failure"
integration: "Orchestrates: godot-organize-files, godot-organize-assets, godot-organize-scripts"
---

# Godot Organize Project Orchestrator

**This orchestrator runs 3 organization mini-skills in sequence. For individual operations, invoke mini-skills directly.**

**Purpose**: Scan and intelligently reorganize Godot project folder structure for optimal organization and maintainability.

**Core Principle**: Automatic, non-destructive project reorganization with full git history preservation.

---

## UPON INVOCATION - START HERE

When this skill is invoked, IMMEDIATELY execute the following sequence:

### 1. Verify Godot Project (5 seconds)

```bash
ls project.godot 2>/dev/null && echo "✓ Godot project detected" || echo "✗ Not a Godot project"
```

**If NOT a Godot project:**
- Inform user this skill only works on Godot projects
- STOP here

**If IS a Godot project:**
- Proceed to step 2

### 2. Scan Project Structure (Automatic)

Execute in parallel:

```bash
# Directory tree
find . -type d -name "." -prune -o -type d -print | head -50

# File count by type
find . -type f \( -name "*.gd" -o -name "*.tscn" -o -name "*.tres" -o -name "*.png" -o -name "*.ogg" \) | wc -l

# Identify problem areas
find . -type f -name "*.gd" | wc -l  # Total scripts
find . -type f -name "*.tscn" | wc -l  # Total scenes
find . -type f -name "*.tres" | wc -l  # Total resources
find . -type d | wc -l  # Total directories

# Find orphaned files (files in root or misplaced)
find . -maxdepth 1 -type f \( -name "*.gd" -o -name "*.tscn" -o -name "*.tres" \)

# Detect unorganized directories
find . -type d -exec sh -c 'count=$(find "$1" -maxdepth 1 -type f | wc -l); [ $count -gt 10 ] && echo "$1 ($count files)"' _ {} \;
```

### 3. Analyze Current Structure

Detect patterns:
- All scripts in root? → Suggest scripts/ directory
- All scenes mixed with scripts? → Suggest scenes/ subdirectory
- All resources at top level? → Suggest resources/ or assets/ organization
- Textures, audio, fonts scattered? → Suggest assets/ with type subdirectories
- No organization at all? → Suggest comprehensive reorganization

### 4. Present Findings

Show the user:

```
=== Project Structure Analysis ===

Project: [project name]
Current state: DISORGANIZED

Statistics:
- Total directories: X
- Total scripts (.gd): Y
- Total scenes (.tscn): Z
- Total resources (.tres): W
- Orphaned files (root level): N

Issues Detected:
- [ ] Scripts scattered across project
- [ ] Scenes mixed with scripts
- [ ] Resources at top level
- [ ] Assets unorganized
- [ ] No clear hierarchy

Reorganization will:
✓ Create logical directory structure
✓ Group files by type and category
✓ Create components/ subdirectory structure
✓ Organize assets (sprites, audio, fonts, etc.)
✓ Improve IDE navigation
✓ Speed up compilation
✓ Make collaboration easier

Proposed structure:
res://
├─ scenes/
│  ├─ ui/
│  ├─ levels/
│  └─ entities/
├─ scripts/
│  ├─ ui/
│  ├─ gameplay/
│  ├─ utils/
│  └─ managers/
├─ assets/
│  ├─ sprites/
│  ├─ audio/
│  │  ├─ music/
│  │  └─ sfx/
│  ├─ fonts/
│  └─ shaders/
├─ resources/
│  ├─ configs/
│  ├─ data/
│  └─ materials/
└─ components/
   ├─ timers/
   ├─ areas/
   ├─ sprites/
   ├─ ui/
   └─ physics/

Would you like me to:
1. Reorganize project (recommended)
2. Show detailed breakdown first
3. Customize structure before proceeding
4. Cancel
```

### 5. Wait for User Choice

- **If 1 (Proceed):** Start automatic reorganization
- **If 2 (Details):** Show file-by-file breakdown, then offer to proceed
- **If 3 (Customize):** Ask about preferences for structure
- **If 4 (Cancel):** Exit skill

---

## Phase 1: Analysis & Planning

### 1.1 Detect Current Structure Type

```bash
# Analyze what kind of project this is

# Check for existing structure patterns
test -d "scripts" && echo "scripts/ exists"
test -d "scenes" && echo "scenes/ exists"
test -d "assets" && echo "assets/ exists"
test -d "components" && echo "components/ exists"

# Check if already organized
find . -maxdepth 1 -type f \( -name "*.gd" -o -name "*.tscn" \) | wc -l
# If 0: Already organized
# If >5: Needs organization
```

### 1.2 Map All Files

Create comprehensive file inventory:

```bash
# Create inventory of all files with their types
find . -type f \( -name "*.gd" -o -name "*.tscn" -o -name "*.tres" -o -name "*.png" -o -name "*.ogg" -o -name "*.mp3" \) > file_inventory.txt

# Analyze each file:
# - Current location
# - Type (script, scene, resource, asset)
# - Category (ui, gameplay, editor, utils, etc.)
# - Related files (dependencies)
```

### 1.3 Create Reorganization Plan

Generate step-by-step plan:

```
Reorganization Plan:
====================

1. Create directories (20 operations)
2. Move scripts (Y operations)
3. Move scenes (Z operations)
4. Move resources (W operations)
5. Move assets (A operations)
6. Update import settings
7. Verify all references
8. Commit changes

Total operations: X
Estimated time: Auto (user doesn't wait)
Rollback available: YES (complete git history)
```

---

## Phase 2: Create Directory Structure

### 2.1 Create Main Categories

```bash
mkdir -p res://scripts
mkdir -p res://scenes
mkdir -p res://assets
mkdir -p res://resources
mkdir -p res://components
```

### 2.2 Create Subcategories by Analysis

**Based on detected usage patterns:**

#### Scripts Organization

```
res://scripts/
├─ ui/                    # UI-related scripts
├─ gameplay/              # Game logic scripts
├─ entities/              # Entity scripts (player, enemy, etc.)
├─ managers/              # Singleton managers
├─ utils/                 # Utility/helper scripts
├─ editor/                # Editor scripts (if any)
└─ _autoload/             # Autoload scripts
```

#### Scenes Organization

```
res://scenes/
├─ ui/                    # UI screens, menus, HUD
│  ├─ menus/
│  ├─ hud/
│  └─ dialogs/
├─ levels/                # Level/map scenes
├─ entities/              # Reusable entity scenes
│  ├─ player/
│  ├─ enemies/
│  ├─ npcs/
│  └─ props/
└─ _debug/                # Debug/test scenes
```

#### Assets Organization

```
res://assets/
├─ sprites/               # 2D graphics
│  ├─ player/
│  ├─ enemies/
│  ├─ ui/
│  ├─ tiles/
│  └─ vfx/
├─ audio/                 # Sound files
│  ├─ music/
│  ├─ sfx/
│  └─ voice/
├─ fonts/                 # Font files
├─ shaders/               # Shader files
└─ 3d/                    # 3D models (if any)
```

#### Resources Organization

```
res://resources/
├─ configs/               # Configuration resources
├─ data/                  # Game data resources
│  ├─ enemies/
│  ├─ items/
│  └─ dialogue/
├─ materials/             # Material resources
├─ tilesets/              # TileSet resources
└─ theme/                 # UI theme resources
```

#### Components Organization

```
res://components/
├─ timers/                # Timer components (from godot-refactoring)
├─ areas/                 # Detection area components
├─ sprites/               # Visual component templates
├─ physics/               # Physics body templates
├─ ui/                    # UI component templates
└─ audio/                 # Audio components
```

### 2.3 Create Directory Structure

```bash
# Create all directories based on analysis
mkdir -p res://scripts/{ui,gameplay,entities,managers,utils,editor,_autoload}
mkdir -p res://scenes/{ui/{menus,hud,dialogs},levels,entities/{player,enemies,npcs,props},_debug}
mkdir -p res://assets/{sprites/{player,enemies,ui,tiles,vfx},audio/{music,sfx,voice},fonts,shaders,3d}
mkdir -p res://resources/{configs,data/{enemies,items,dialogue},materials,tilesets,theme}
mkdir -p res://components/{timers,areas,sprites,physics,ui,audio}

# Create .gitkeep files in empty directories
find res:// -type d -empty -exec touch {}/.gitkeep \;
```

---

## Phase 3: File Migration

### 3.1 Categorize Existing Files

```bash
# Analyze each file and determine category

# Scripts
for file in $(find . -maxdepth 1 -name "*.gd"); do
    # Read file content
    # Detect if it's ui, gameplay, manager, util, etc.
    # Assign to appropriate category
done

# Scenes
for file in $(find . -maxdepth 1 -name "*.tscn"); do
    # Analyze scene name and content
    # Assign to ui/levels/entities
done

# Resources
for file in $(find . -maxdepth 1 -name "*.tres"); do
    # Check resource type
    # Assign to configs/data/materials/etc
done

# Assets
for file in $(find . -maxdepth 1 -name "*.png"); do
    # Check dimensions and usage
    # Assign to sprites/ui/tiles/vfx
done
```

### 3.2 Move Files Intelligently

```bash
# Move scripts
mv player.gd res://scripts/entities/
mv ui_manager.gd res://scripts/managers/
mv utils.gd res://scripts/utils/
mv enemy.gd res://scripts/entities/

# Move scenes
mv menu.tscn res://scenes/ui/menus/
mv level_1.tscn res://scenes/levels/
mv player.tscn res://scenes/entities/player/
mv enemy.tscn res://scenes/entities/enemies/

# Move resources
mv game_config.tres res://resources/configs/
mv enemy_data.tres res://resources/data/enemies/
mv player_material.tres res://resources/materials/

# Move assets
mv player_sprite.png res://assets/sprites/player/
mv bg_music.ogg res://assets/audio/music/
mv explosion.png res://assets/sprites/vfx/
```

### 3.3 Update References

```bash
# Scan all .gd and .tscn files for hardcoded paths
grep -rn "res://" --include="*.gd" --include="*.tscn" . > path_references.txt

# Update path references in scripts
# Old: load("res://player.gd")
# New: load("res://scripts/entities/player.gd")

# Update path references in scenes
# Old: [ext_resource type="Script" path="res://ui_manager.gd"]
# New: [ext_resource type="Script" path="res://scripts/managers/ui_manager.gd"]
```

---

## Phase 4: Special Handling

### 4.1 Autoload Scripts

Detect and move to _autoload/:

```bash
# In project.godot:
# [autoload]
# EventBus="res://event_bus.gd"

# Move to:
# [autoload]
# EventBus="res://scripts/_autoload/event_bus.gd"

# Update project.godot references
```

### 4.2 Plugin Scripts (if any)

Keep in addons/ directory:

```bash
mkdir -p res://addons/
# Don't reorganize addons directory
```

### 4.3 Generated Files (if any)

```bash
# Don't reorganize:
# - .gd files in .godot/
# - Imported files
# - Cache files
```

---

## Phase 5: Integration with godot-refactoring

If component library detected (from godot-refactoring skill):

```bash
# Move existing components/ to new location
# components/ → res://components/

# Update parent .tscn files with new paths:
# Old: [ext_resource type="PackedScene" path="res://components/timers/..."]
# New: [ext_resource type="PackedScene" path="res://components/timers/..."]

# Ensure component library structure is respected
```

---

## Phase 6: Verify & Validate

### 6.1 Check File Counts

```bash
# Before reorganization
find . -maxdepth 1 -type f | wc -l

# After reorganization
find . -type f | wc -l

# Should be equal
```

### 6.2 Check All References

```bash
# Run Godot in headless mode to detect reference errors
godot --headless --quit-after 5 project.godot 2>&1 | grep -i "error\|not found"

# Should report 0 errors
```

### 6.3 Verify Scene Integrity

```bash
# Check that all scene files are still valid
for scene in $(find . -name "*.tscn"); do
    godot --editor -e "$scene" 2>&1 | grep -q "ERROR" && echo "ERROR in $scene"
done

# Should report 0 errors
```

### 6.4 Verify Script Integrity

```bash
# Check that all scripts compile
for script in $(find . -name "*.gd"); do
    gdscript -c "$script" 2>&1 | grep -q "Error" && echo "ERROR in $script"
done

# Should report 0 errors
```

---

## Phase 7: Git & Finalization

### 7.1 Create Backup Commit

```bash
git add .
git commit -m "Backup: Pre-reorganization state

All files present before structure reorganization."
```

### 7.2 Move All Files

(Execute moves from Phase 3)

### 7.3 Update References

(Execute reference updates from Phase 3.3)

### 7.4 Final Verification

```bash
# Run Godot validation
godot --headless --quit-after 5 project.godot

# Check for errors
# Should see: "All scenes and scripts loaded successfully"
```

### 7.5 Create Final Commit

```bash
git add .
git commit -m "Refactor: Reorganize project structure for better organization

Project structure reorganization:
- Created logical directory hierarchy
- Organized scripts by category (ui, gameplay, entities, managers, utils)
- Organized scenes (ui, levels, entities)
- Organized assets (sprites, audio, fonts, shaders)
- Organized resources (configs, data, materials)
- Organized components (from godot-refactoring integration)
- Updated all internal path references
- Verified all scenes and scripts load without errors

Benefits:
- Improved IDE navigation and file organization
- Faster compilation and project loading
- Easier collaboration and code discovery
- Clear separation of concerns
- Integrated with godot-refactoring skill

Behavior: UNCHANGED
Visual: UNCHANGED
Performance: UNCHANGED (or improved)
"
```

### 7.6 Tag Completion

```bash
git tag reorganize-complete-$(date +%Y%m%d-%H%M%S)
```

---

## Result Metrics

After successful reorganization:

```
=== Project Reorganization Complete ===

Before:
- Structure: FLAT/CHAOTIC
- Navigation: DIFFICULT
- File discovery: SLOW

After:
- Structure: HIERARCHICAL & LOGICAL
- Navigation: FAST & INTUITIVE
- File discovery: INSTANT
- Build time: Potentially faster
- Collaboration: EASIER

Files organized:
- Scripts: X → scripts/
- Scenes: Y → scenes/
- Resources: Z → resources/
- Assets: W → assets/
- Components: V → components/ (if godot-refactoring detected)

Total migrations: X + Y + Z + W + V
Errors: 0
Warnings: 0

Status: ✓ SUCCESS

Next steps:
1. Reopen project in Godot editor
2. Verify folder structure matches
3. Check that all assets load correctly
4. Continue development on clean structure
```

---

## Integration with godot-refactoring

This skill **pairs perfectly with** the godot-refactoring skill:

1. **Run godot-refactoring first** → Extracts code-created nodes to modular components
   - Creates `res://components/` directory structure
   - Generates component base scenes and presets

2. **Run project-structure-organizer** → Recognizes component structure
   - Preserves component organization
   - Creates supporting directories
   - Organizes rest of project around component library
   - Updates all references

3. **Result** → Clean, modular, organized project

---

## Rollback

If reorganization causes issues:

```bash
# View commits
git log --oneline | head -5

# Find pre-reorganization commit
git log --oneline | grep "Pre-reorganization"

# Reset to before
git reset --hard <commit_hash>

# Project restored to previous state
```

---

## Use Cases

### Case 1: New Project - Organize From Start

User creates new Godot project, adds a few files, then invokes:
- Skill creates proper structure immediately
- User continues development on clean structure

### Case 2: Existing Project - Cleanup

User has 1-year-old project with 200 files scattered everywhere:
- Skill scans and auto-reorganizes
- All references updated
- Project is now maintainable

### Case 3: After godot-refactoring - Full Cleanup

User runs godot-refactoring skill, creates component library:
- Components are organized in `res://components/`
- Then runs this skill to organize rest of project
- Result: Fully organized, modular project

---

## Best Practices

1. **Run after godot-refactoring** → Complete project cleanup pipeline
2. **Create git commit before** → Always have rollback option
3. **Verify in editor after** → Open Godot and check file tree
4. **Run on main branch** → Don't do on feature branches
5. **Document structure** → Add README to res// with directory guide

---

**This skill provides complete project structure organization with zero data loss and full rollback capability.**
