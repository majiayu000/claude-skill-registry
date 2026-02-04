---
name: godot-refactor
version: 3.0.0
displayName: "Godot Refactoring Orchestrator"
description: >
  Use when Godot project has code-created objects, tight coupling via direct references,
  monolithic scripts over 150 lines, or needs scene-first architecture with signals and
  composition. Orchestrates all 5 code quality mini-skills: extract-to-scenes, split-scripts,
  add-signals, extract-resources, and clean-conflicts. Each operation runs independently
  with git commits and validation.
author: "Asreonn"
license: MIT
category: game-development
type: agent
difficulty: intermediate
audience: [developers, teams]
keywords:
  - godot
  - refactoring
  - code-quality
  - scene-architecture
  - signals
  - composition
  - gdscript
  - clean-code
  - godot4
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme
filesystem:
  read:
    - "${PROJECT_ROOT}/**/*.gd"
    - "${PROJECT_ROOT}/**/*.tscn"
    - "${PROJECT_ROOT}/project.godot"
    - "${PROJECT_ROOT}/**/*.tres"
  write:
    - "${PROJECT_ROOT}/**/*.gd"
    - "${PROJECT_ROOT}/**/*.tscn"
    - "${PROJECT_ROOT}/components/**"
    - "${PROJECT_ROOT}/resources/**"
  deny:
    - "**/.env*"
    - "**/secrets*"
    - "**/*.key"
    - "**/*.pem"
behavior:
  timeout: 600
  retry: 3
  cache: true
  interactive: true
use_cases:
  - "Building new features and code uses .new() instead of scenes"
  - "Scripts are over 150 lines and do too many things"
  - "Code has get_node() chains creating tight coupling"
  - "Game data is hardcoded in const arrays"
  - "Need clean architecture for team collaboration"
  - "Preparing code for review or testing"
  - "Want full project refactoring with all operations"
outputs: "Component library, split scripts, signal architecture, resource files, git commits per operation"
requirements: "Git repository, Godot 4.x, bash tools (grep, find, awk)"
execution: "Fully automatic with user approval after Phase 1 analysis"
auto_rollback: "Yes - auto-reverts on validation test failure"
integration: "Orchestrates: godot-extract-to-scenes, godot-split-scripts, godot-add-signals, godot-extract-resources, godot-clean-conflicts"
---

# Godot Refactor Orchestrator

**This orchestrator runs 5 code quality mini-skills in sequence. For individual operations, invoke mini-skills directly.**

## Core Principle: Scene-First, Signal-Based, Component Composition

**Iron Law**: NO functional or visual changes during refactoring. Period.

This skill automatically refactors Godot projects to cleaner, more modular architecture while preserving exact behavior. Every operation creates a git commit. Rollback is always available.

---

## UPON INVOCATION - START HERE

When this skill is invoked, IMMEDIATELY execute the following sequence:

### 1. Verify Godot Project (5 seconds)

```bash
# Check if this is a Godot project
ls project.godot 2>/dev/null && echo "✓ Godot project detected" || echo "✗ Not a Godot project"
```

**If NOT a Godot project:**
- Inform user this skill only works on Godot projects
- Ask if they want to navigate to the correct directory
- STOP here

**If IS a Godot project:**
- Proceed to step 2

### 2. Begin Phase 1: Analysis & Baseline (AUTOMATIC)

**Do NOT ask "What would you like me to do?" - Start analyzing immediately.**

Execute these commands in parallel:

```bash
# Detect code-created objects
grep -rn "\.new()" --include="*.gd" . | grep -E "(Node|Timer|Area|Sprite|Control|Collision)" | wc -l

# Detect monolithic scripts
find . -name "*.gd" -exec wc -l {} + | awk '$1 > 150' | wc -l

# Detect tight coupling
grep -rn "get_node\|has_method" --include="*.gd" . | wc -l

# Detect inline data
grep -rn "^[[:space:]]*const.*\[" --include="*.gd" . | wc -l
```

### 3. Present Findings (30 seconds)

Show the user:
```
=== Godot Refactoring Analysis ===

Project: [project name from project.godot]

Anti-patterns detected:
- Code-created objects: X
- Monolithic scripts: X
- Tight coupling: X
- Inline data: X
- Conflicting operations: (will be detected after refactoring)

Total: X anti-patterns found

Refactoring includes:
✓ Automatic testing after each operation
✓ Auto-rollback on test failure
✓ Git commit per operation
✓ Push to remote on demand

Would you like me to:
1. Proceed with automatic refactoring (recommended)
2. Show detailed breakdown first
3. Cancel
```

### 4. Wait for User Choice

- **If 1 (Proceed):** Start Phase 2 immediately
- **If 2 (Details):** Show detailed file-by-file breakdown, then offer to proceed
- **If 3 (Cancel):** Exit skill

**CRITICAL**: Do NOT stop after loading the skill. Do NOT ask "What would you like me to do?" Start with step 1 immediately.

---

## When to Use This Skill

Use this skill when you detect ANY of these symptoms:

**Code-Created Objects:**
- `.new()` calls in `_ready()`, `_process()`, or other lifecycle methods
- `add_child()` with programmatically created nodes
- Timers, Areas, Sprites created in code

**Monolithic Scripts:**
- Scripts >150 lines
- Multiple unrelated responsibilities in one file
- God objects that do everything

**Tight Coupling:**
- `get_node()` chains to access other nodes
- `has_method()` checks before calling
- Direct property access across nodes
- Parent-child dependencies for behavior

**Inline Data:**
- `const` arrays with game data
- Hardcoded configuration in scripts
- Data that should be resources

**Deep Inheritance:**
- More than 2 levels of script inheritance
- Inheritance used for code reuse instead of composition

### Decision Flowchart

```
User mentions Godot project
    ↓
Does it have ANY of the above symptoms?
    ↓ YES                    ↓ NO
Use this skill              Regular development
    ↓
Run Phase 1: Analysis
    ↓
Anti-patterns found?
    ↓ YES                    ↓ NO
Run Phases 2-4              Document clean state
```

---

## The Four Phases

### Phase 1: Analysis & Baseline (Automatic)

**Purpose**: Detect all anti-patterns and create safety baseline.

**Steps:**

1. **Scan Project Files**
```bash
# Find all Godot script files
find . -name "*.gd" -type f

# Find all scene files
find . -name "*.tscn" -type f
```

2. **Detect Anti-Patterns**

Use detection patterns from `anti-patterns-detection.md`:

```bash
# Code-created objects
grep -rn "\.new()" --include="*.gd" .

# Monolithic scripts (>150 lines)
find . -name "*.gd" -exec wc -l {} + | awk '$1 > 150 {print $2 " (" $1 " lines)"}'

# Tight coupling
grep -rn "get_node\|get_parent\|has_method" --include="*.gd" .

# Inline data
grep -rn "^[[:space:]]*const.*\[" --include="*.gd" .
```

3. **Create Git Baseline**

```bash
# Save current branch
current_branch=$(git branch --show-current)

# Create baseline tag
git tag baseline-$(date +%Y%m%d-%H%M%S)

# Initial commit if there are uncommitted changes
git add .
git commit -m "Baseline: Pre-refactoring state (on $current_branch)"
```

4. **Generate Refactoring Manifest**

Create a priority-ordered list:

| Priority | Anti-Pattern | File | Lines | Operation |
|----------|-------------|------|-------|-----------|
| 1 | Inline data | enemy_data.gd | 45-78 | Extract to .tres |
| 2 | Code-created Timer | laser_beam.gd | 38-45 | Extract to .tscn |
| 3 | Tight coupling | base_station.gd | 92 | Signal decoupling |
| 4 | Monolithic script | player_movement.gd | 287 lines | Split script |

**Phase 1 Output:**
- ✓ Baseline git commit/tag created
- ✓ Anti-patterns detected and prioritized
- ✓ Manifest table generated
- ✓ Ready for automatic refactoring

---

### Phase 2: Automatic Refactoring (Five Operations)

Process anti-patterns in priority order: Data → Scenes → Signals → Scripts → Conflicts

**CRITICAL - After Each Operation:**
1. Git commit the changes
2. **Run automatic validation test**
3. If test fails: Auto-revert and report error
4. If test passes: **Continue automatically to next operation**
5. No user prompt unless test fails or user confirmation needed

**Automatic Testing Procedure:**
```bash
# Quick validation test (runs after each git commit)
echo "Running validation test..."
godot --headless --quit-after 5 project.godot 2>&1 | tee test_output.log

# Check for errors
if grep -q "ERROR\|SCRIPT ERROR\|Parse Error" test_output.log; then
    echo "⚠️  Tests failed - reverting operation"
    git reset --hard HEAD~1
    echo "❌ Operation reverted. Error details:"
    grep "ERROR\|SCRIPT ERROR\|Parse Error" test_output.log
    # STOP and report to user
else
    echo "✓ Tests passed - continuing"
    rm test_output.log
    # CONTINUE to next operation automatically
fi
```

**Note:** If test fails, STOP workflow and report to user. Otherwise, continue automatically through all operations.

#### Operation A: Extract Code-Created Objects to Modular Components

**Target**: Any `.new()` calls that create nodes

**Enhanced Process:**

1. **Detect and Analyze**
   - Find `.new()` calls for node types
   - Extract 30 lines of context (properties, methods, signals)
   - Analyze variable names, properties, methods
   - Consult `node-selection-guide.md` decision trees
   - Calculate confidence score for node type
   - Select optimal node from `godot-node-reference.md`

2. **Check Component Library**
   - Does `components/{category}/` exist? (e.g., `components/timers/`)
   - If YES: Reuse base component, skip to Step 4
   - If NO: Generate full component structure (Steps 2-3)

3. **Generate Component (First Time Only)**
   - Create `{type}_config.gd` (Resource class with @export properties)
   - Create `configurable_{type}.gd` (Script that extends node, applies config)
   - Create `configurable_{type}.tscn` (Base scene with script)
   - Creates modular, reusable foundation

4. **Generate Preset Resource**
   - Extract properties from analyzed code
   - Create `presets/{preset_name}.tres` (specific configuration)
   - Each detected instance gets unique preset
   - Presets reference the base component

5. **Update Parent Scene**
   - Add ext_resource entries for base scene and preset
   - Instance base component with preset resource
   - Same scene reused, different presets = ZERO duplication

6. **Update Parent Script**
   - Add @onready reference to component instance
   - Keep signal connections
   - Remove .new(), add_child(), static property assignments
   - Configuration now comes from preset resource

7. **Git Commit & Validate**
   - Commit all component files and parent changes
   - Run validation test
   - Ensure behavior unchanged

**Example Transformation:**

Before (Code-Created):
```gdscript
func _ready():
    _damage_timer = Timer.new()
    _damage_timer.wait_time = 0.5
    _damage_timer.one_shot = false
    add_child(_damage_timer)
    _damage_timer.timeout.connect(_on_damage)

    _cooldown_timer = Timer.new()
    _cooldown_timer.wait_time = 2.0
    _cooldown_timer.one_shot = true
    add_child(_cooldown_timer)
    _cooldown_timer.timeout.connect(_on_cooldown)
```

After (First Timer - Full Component Created):
```
Files created:
✓ components/timers/timer_config.gd (resource class)
✓ components/timers/configurable_timer.gd (reusable script)
✓ components/timers/configurable_timer.tscn (reusable base scene)
✓ components/timers/presets/damage_timer.tres (configuration preset)

parent.gd:
@onready var _damage_timer: ConfigurableTimer = $DamageTimer

func _ready():
    _damage_timer.timeout.connect(_on_damage)
```

After (Second Timer - Reuses Base):
```
Files created:
✓ components/timers/presets/cooldown_timer.tres (NEW preset only!)

parent.gd:
@onready var _damage_timer: ConfigurableTimer = $DamageTimer
@onready var _cooldown_timer: ConfigurableTimer = $CooldownTimer

func _ready():
    _damage_timer.timeout.connect(_on_damage)
    _cooldown_timer.timeout.connect(_on_cooldown)
```

**Key Benefits:**

- ✅ Intelligent node selection (no arbitrary choices)
- ✅ Modular components (reusable across project)
- ✅ Zero duplication (same base, different presets)
- ✅ Inspector-configurable (edit presets in editor)
- ✅ Automatic library building (grows organically)
- ✅ Signal connections preserved
- ✅ Behavior unchanged (Iron Law maintained)

**Success Criteria:**
- Component structure created (if first of type)
- Preset resource created with extracted values
- Parent scene instances component with preset
- Parent script has @onready reference
- Signal connections work
- Old code removed
- Behavior unchanged

---

#### Operation B: Split Monolithic Scripts

**Target**: Scripts >150 lines with multiple responsibilities

**Detection:**
```bash
find . -name "*.gd" -exec wc -l {} + | awk '$1 > 150'
```

**For each detected script:**

1. **Analyze script structure**
   - Identify logical sections (look for comment headers, function groups)
   - Find responsibilities (input, physics, abilities, UI, etc.)
   - Determine dependencies between sections

2. **Plan split**
   - Main script keeps core responsibility
   - Extract secondary responsibilities to components
   - Define signal interface between components

3. **Create component scripts**

   Example: Split `player_movement.gd` (287 lines)

   Extract to `player_abilities.gd`:
   ```gdscript
   extends Node
   class_name PlayerAbilities

   signal ability_used(ability_name: String)
   signal cooldown_started(duration: float)

   # Ability-related functions moved here
   ```

4. **Update main script**
   ```gdscript
   @onready var abilities: PlayerAbilities = $Abilities

   func _ready():
       abilities.ability_used.connect(_on_ability_used)
   ```

5. **Implement signal communication**
   - Replace direct function calls with signals
   - Connect signals in _ready()
   - Remove tight coupling

6. **Git commit**
   ```bash
   git add player_movement.gd player_abilities.gd
   git commit -m "Refactor: Split abilities from player_movement.gd"
   ```

7. **Run automatic test** (see Phase 2 header for test procedure)

**Success criteria:**
- Main script <150 lines
- Component scripts focused (80-120 lines optimal)
- Signal-based communication
- No direct dependencies
- Behavior unchanged

---

#### Operation C: Implement Signal-Based Decoupling

**Target**: Direct coupling via get_node(), has_method(), direct calls

**Detection:**
```bash
grep -rn "get_node\|has_method" --include="*.gd" .
```

**For each detected coupling:**

1. **Identify the relationship**
   - What is being accessed?
   - What information is being exchanged?
   - Is this event-based or state query?

2. **Create/use Events autoload**

   If not exists, create `events.gd`:
   ```gdscript
   extends Node
   # Global event bus

   signal player_entered_safe_zone(zone: Node2D)
   signal enemy_spawned(enemy: Node2D)
   signal score_changed(new_score: int)
   ```

   Add to project settings: Project → Project Settings → Autoload

3. **Replace direct coupling with signals**

   Before:
   ```gdscript
   func _on_body_entered(body):
       if body.has_method("set_beam_enabled"):
           body.set_beam_enabled(false)
   ```

   After (emitter):
   ```gdscript
   func _on_body_entered(body):
       if body.is_in_group("player"):
           Events.player_entered_safe_zone.emit(self)
   ```

   After (receiver):
   ```gdscript
   func _ready():
       Events.player_entered_safe_zone.connect(_on_safe_zone)

   func _on_safe_zone(zone):
       set_beam_enabled(false)
   ```

4. **Remove coupling code**
   - Delete get_node() calls
   - Delete has_method() checks
   - Delete direct property access

5. **Git commit**
   ```bash
   git add events.gd base_station.gd player_movement.gd
   git commit -m "Refactor: Decouple base_station from player via signals"
   ```

6. **Run automatic test** (see Phase 2 header for test procedure)

**Success criteria:**
- No get_node() for behavior access
- No has_method() checks
- Events.gd exists and is used
- Signal connections established
- Behavior unchanged

---

#### Operation D: Extract Data to .tres Resources

**Target**: `const` declarations with game data

**Detection:**
```bash
grep -rn "^[[:space:]]*const.*\[" --include="*.gd" .
```

**For each detected data constant:**

1. **Analyze data structure**
   ```gdscript
   const ENEMY_TYPES = [
       {"type": "basic", "health": 100, "speed": 200},
       {"type": "fast", "health": 50, "speed": 400}
   ]
   ```

2. **Create Resource class**

   Create `enemy_type_data.gd`:
   ```gdscript
   extends Resource
   class_name EnemyTypeData

   @export var type_name: String
   @export var health: int
   @export var speed: float
   ```

3. **Generate .tres files**

   Create `enemy_types/basic.tres`:
   ```ini
   [gd_resource type="EnemyTypeData" load_steps=2 format=3]

   [ext_resource type="Script" path="res://enemy_type_data.gd" id="1"]

   [resource]
   script = ExtResource("1")
   type_name = "basic"
   health = 100
   speed = 200.0
   ```

4. **Update script to use resources**
   ```gdscript
   @export var enemy_types: Array[EnemyTypeData]

   # In scene, assign resources via inspector
   ```

5. **Remove const declaration**

6. **Git commit**
   ```bash
   git add enemy_type_data.gd enemy_types/*.tres enemy_spawner.gd
   git commit -m "Refactor: Extract enemy data to .tres resources"
   ```

7. **Run automatic test** (see Phase 2 header for test procedure)

**Success criteria:**
- Resource class created
- .tres files generated with correct data
- Script updated to use resources
- Const declaration removed
- Behavior unchanged

---

#### Operation E: Clean Conflicting/Ineffective Operations

**Target**: Code that runs without errors but has no effect or conflicts with other code

**IMPORTANT**: This operation runs **after** Operations A-D are complete, as refactoring may introduce or remove conflicts.

**Detection:**
```bash
# Run comprehensive conflict detection
bash << 'EOF'
echo "=== Detecting Conflicting Operations ==="

# Self-assignments
echo "Self-assignments:"
grep -rn "position\s*=\s*position\|scale\s*=\s*scale\|rotation\s*=\s*rotation" --include="*.gd" .

# Redundant defaults
echo "Redundant defaults:"
grep -rn "modulate\s*=\s*Color\.WHITE\|scale\s*=\s*Vector2\.ONE" --include="*.gd" .

# Duplicate property assignments (common properties)
echo "Checking for duplicate assignments..."
for prop in "scale" "position" "rotation" "modulate" "visible"; do
    grep -rn "\.$prop\s*=" --include="*.gd" . | \
    awk -F: -v prop="$prop" '{
        file=$1; line=$2;
        if (file==prev_file && line-prev_line<20) {
            print file":"prev_line" and "line" - Duplicate "prop
        }
        prev_file=file; prev_line=line
    }'
done

# Conflicting tweens
echo "Conflicting tweens:"
grep -n "tween_property" --include="*.gd" -r . | \
awk -F: '{
    file=$1; line=$2;
    if (match($0, /tween_property.*"([^"]+)"/, arr)) {
        prop=arr[1];
        key=file":"prop;
        if (key in seen && line-seen[key]<15) {
            print file":"seen[key]" and "line" - Conflicting tweens on "prop
        }
        seen[key]=line
    }
}'

# Code after queue_free
echo "Code after queue_free:"
grep -A2 "queue_free()" --include="*.gd" . | grep -v "^--$"

EOF
```

**For each detected conflict:**

1. **Auto-fix** (no user input):
   - Self-assignments: Remove entirely
   - Code after `queue_free()`: Move code before queue_free
   - Obvious redundant defaults: Remove

2. **User confirmation** (ask user):
   - Duplicate assignments: Which value to keep?
   - Conflicting tweens: Which to keep or chain?
   - Multiple process calls: Final intended state?

3. **Example fixes:**

   **Self-assignment:**
   ```gdscript
   # Before
   position = position

   # After (remove line)
   ```

   **Duplicate assignment:**
   ```gdscript
   # Before
   sprite.scale = Vector2(2, 2)  # Line 45
   sprite.scale = Vector2(1, 1)  # Line 52

   # After (keep last)
   sprite.scale = Vector2(1, 1)  # Line 52
   ```

   **Conflicting tweens (user chose "chain"):**
   ```gdscript
   # Before
   var tween1 = create_tween()
   tween1.tween_property(self, "scale", Vector2(2,2), 1.0)
   var tween2 = create_tween()
   tween2.tween_property(self, "scale", Vector2(0.5,0.5), 1.0)

   # After
   var tween = create_tween()
   tween.tween_property(self, "scale", Vector2(2,2), 1.0)
   tween.tween_property(self, "scale", Vector2(0.5,0.5), 1.0)
   ```

4. **Git commit**
   ```bash
   git add <modified files>
   git commit -m "Refactor: Clean conflicting/ineffective operations

   - Removed self-assignments
   - Fixed duplicate property assignments
   - Resolved conflicting tweens
   - Cleaned up redundant operations

   No functional changes - code cleanup only"
   ```

5. **Run automatic test** (see Phase 2 header for test procedure)

**Success criteria:**
- No self-assignments remain
- No obvious duplicate assignments
- Conflicting tweens resolved
- Code after queue_free() moved
- Behavior unchanged

**Note:** See `conflicting-operations-detection.md` for comprehensive detection patterns and `refactoring-operations.md` Operation E for detailed procedures.

---

### Phase 3: Git Commits (Automatic)

**After each operation**, commit with clear message:

```bash
# Template
git add <files>
git commit -m "Refactor: <Operation> in <file> - <specific change>"

# Examples
git commit -m "Refactor: Extract Timer to scene in laser_beam.gd"
git commit -m "Refactor: Split abilities from player_movement.gd (287→142 lines)"
git commit -m "Refactor: Decouple base_station from player via signals"
git commit -m "Refactor: Extract enemy data to .tres resources"
git commit -m "Refactor: Clean conflicting/ineffective operations"
```

**After all operations:**
```bash
git tag refactor-complete-$(date +%Y%m%d)
```

**Commit history should show:**
- Baseline commit
- One commit per refactoring operation (A, B, C, D, E)
- Clear, descriptive messages
- Easy to review
- Easy to rollback individual changes

**Push on Demand:**

After all operations complete, ask user:
```
=== Refactoring Complete ===

All operations completed successfully!
5 operations performed, X commits created on current branch.

Would you like to push to remote?
1. Yes, push now
2. No, I'll push manually later
3. Show me the commit log first

Choice [1-3]:
```

**If user chooses 1 (push now):**
```bash
# Push to current branch's remote
git push origin $(git branch --show-current)
```

**If user chooses 3 (show log first):**
```bash
git log --oneline --graph baseline-*..HEAD
# Then ask again: Push now? [y/n]
```

**If user says "push" or "push et" at ANY time during the workflow:**
```bash
# Immediately push current branch
git push origin $(git branch --show-current)
echo "✓ Pushed to remote"
```

---

### Phase 4: Final Verification (Minimal, Automatic)

**Purpose**: Ensure no functional or visual regressions.

**Steps:**

1. **Open project in Godot**
   ```bash
   godot --editor path/to/project.godot
   ```

2. **Check for errors**
   - No red errors in console
   - No yellow warnings about missing nodes
   - All scenes load successfully

3. **Visual verification**
   - Run main scene
   - Quick visual check (30 seconds)
   - Compare against expected behavior

4. **Play test checklist** (from `verification-checklist.md`):
   - [ ] Player movement works
   - [ ] Abilities trigger correctly
   - [ ] Enemies spawn and behave normally
   - [ ] UI updates properly
   - [ ] No crashes or errors

5. **Performance baseline** (optional):
   ```bash
   # Compare FPS before/after
   # Should be identical ±2 FPS
   ```

**If verification fails:**

```bash
# Rollback procedure
git reset --hard baseline-YYYYMMDD-HHMMSS
git tag refactor-failed-$(date +%Y%m%d-%H%M%S)

# Report what broke
# Debug with systematic-debugging skill
```

**If verification succeeds:**

Report summary:
```
✓ Refactoring complete
✓ 8 operations performed
✓ 287 lines reduced to 142 across 3 files
✓ 4 .tscn scenes created
✓ 2 .tres resources created
✓ Signal-based architecture established
✓ No functional changes
✓ All tests passing
```

---

## Supporting Files

This skill uses modular reference files:

- **anti-patterns-detection.md**: All grep/find patterns for detection
- **refactoring-operations.md**: Detailed step-by-step procedures
- **godot-best-practices.md**: Clean patterns reference
- **tscn-generation-guide.md**: .tscn file format templates
- **verification-checklist.md**: Testing procedures

Read these files for detailed implementation guidance.

---

## Red Flags - STOP

These thoughts mean you're rationalizing away discipline:

| Rationalization | Reality | Fix |
|----------------|---------|-----|
| "While I'm here, let me add this feature" | Feature creep breaks Iron Law | Refactor only, no features |
| "This behavior is wrong, I'll fix it now" | Bug fixes are separate work | Note bug, refactor only |
| "I don't need to test this change" | Untested = broken | Always verify |
| "I'll commit after a few more changes" | Loses granularity | Commit per operation |
| "This .tscn format looks close enough" | Invalid scenes crash | Use exact format |
| "The user won't notice this visual change" | Iron Law has no exceptions | Revert and fix |
| "Signals are overkill for this" | Coupling creeps back | Use signals anyway |
| "I'll manually test later" | Later never comes | Test now |
| "This script is fine at 160 lines" | Arbitrary exceptions grow | Split at 150 |
| "I understand the pattern, no need to read" | Assumptions create bugs | Read the guide |

---

## Quick Reference: Anti-Pattern → Clean Pattern

| Anti-Pattern | Clean Pattern | Tool |
|-------------|---------------|------|
| `Timer.new()` in code | .tscn scene with Timer | Operation A |
| `get_node("../Player")` | Signal via Events | Operation C |
| `if has_method("take_damage"):` | Signal listener | Operation C |
| 287-line script | Split to 3 focused scripts | Operation B |
| `const WEAPONS = [...]` | .tres resources | Operation D |
| `add_child(sprite)` | Scene composition | Operation A |
| Direct method calls | Signal emit/connect | Operation C |
| Deep inheritance | Component composition | Operations A+B |

---

## File Operation Flow

```
1. Data Extraction
   .gd with const → Resource class .gd + .tres files

2. Scene Extraction
   .gd with .new() → .gd with @onready + new .tscn

3. Signal Decoupling
   .gd with get_node() → events.gd + updated .gd files

4. Script Splitting
   Large .gd → Multiple focused .gd files with signals
```

---

## Godot Naming Conventions

**Scenes (.tscn):**
- PascalCase for node names: `DamageTimer`, `AbilitySystem`
- snake_case for file names: `damage_timer.tscn`, `ability_system.tscn`

**Scripts (.gd):**
- snake_case for files: `player_movement.gd`, `enemy_spawner.gd`
- PascalCase for class_name: `class_name PlayerMovement`

**Resources (.tres):**
- snake_case for files: `enemy_types/basic.tres`
- PascalCase for Resource class: `class_name EnemyTypeData`

**Signals:**
- snake_case: `signal ability_used`, `signal player_entered_safe_zone`
- Past tense for events: `signal enemy_spawned` (not `enemy_spawn`)

**@onready variables:**
- snake_case with type hint: `@onready var _damage_timer: Timer = $DamageTimer`
- Private with underscore: `_damage_timer`, `_ability_system`

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Invalid .tscn format | Scene won't load in Godot | Use exact template format |
| Missing node type in .tscn | Godot can't parse scene | Always specify `type="Timer"` |
| Forgetting @onready | Null reference at runtime | Add @onready for all node refs |
| Wrong signal signature | Connection fails silently | Match parameter types exactly |
| Removing necessary .new() | Some objects SHOULD be created | Only refactor scene nodes |
| Not testing after each op | Compounding errors | Test after every commit |
| Coupling through globals | Different coupling, same problem | Use Events for decoupling only |
| Over-splitting scripts | Too many tiny files | 80-120 lines is optimal |
| Async signals without checks | Race conditions | Verify node existence |
| Changing behavior "slightly" | Iron Law violation | Revert immediately |

---

## Signal Architecture Patterns

**Event Bus (Events.gd):**
```gdscript
# Use for global events
signal player_died
signal level_completed(level_num: int)
signal score_changed(new_score: int)
```

**Direct Node Signals:**
```gdscript
# Use for parent-child communication
signal health_depleted
signal ability_activated(ability_name: String)
```

**When to use which:**
- Events.gd: Cross-tree communication, global state changes
- Node signals: Parent-child, local behavior

---

## Real-World Impact

Expected improvements after refactoring:

**Code Quality:**
- 30-50% reduction in total lines of code
- Scripts average 80-120 lines (down from 150-300)
- Zero direct node dependencies
- Signal-based architecture throughout

**Maintainability:**
- Changes isolated to single files
- Components reusable across scenes
- Testing individual components possible
- New developers onboard faster

**Performance:**
- Identical to baseline (±2 FPS)
- Scene loading slightly faster
- Memory usage unchanged

---

## Execution Strategy

This skill runs **fully automatically**:

1. User invokes skill on Godot project
2. Phase 1: Scan and report findings
3. User approves refactoring
4. Phases 2-3: Execute all operations with commits on current branch
5. Phase 4: Verify and report results

**User input required:**
- Initial invocation
- Approval after Phase 1 analysis
- Final verification check (30 seconds)

**Everything else is automatic:**
- Anti-pattern detection
- .tscn file generation
- Script modifications
- Git commits on current branch
- Testing

---

## Success Criteria

Refactoring is complete when:

- ✓ Zero `.new()` calls for scene nodes
- ✓ All scripts <150 lines
- ✓ Signal-based architecture established
- ✓ No `get_node()` for behavior access
- ✓ Data in .tres resources
- ✓ Clean git history with descriptive commits on current branch
- ✓ All scenes load without errors
- ✓ Behavior identical to baseline
- ✓ Visual appearance unchanged
- ✓ Performance within ±2 FPS

---

## Post-Refactoring

After successful refactoring:

1. **Continue development**
   - Changes are already on current branch
   - Push to remote if not already pushed
   - Continue normal development workflow

2. **Document architecture**
   - Create architecture diagram
   - Document signal flows
   - List component responsibilities

3. **Establish standards**
   - Use this clean architecture as template
   - Apply patterns to new code
   - Prevent anti-pattern regression

4. **Consider further improvements** (separate tasks):
   - Add unit tests (use TDD skill)
   - Optimize performance (profile first)
   - Add new features (use brainstorming skill)

---

**Remember**: Refactoring changes HOW code works internally, not WHAT it does externally. The Iron Law is absolute.
