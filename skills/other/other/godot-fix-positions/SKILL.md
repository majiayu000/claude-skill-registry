---
name: godot-fix-positions
version: 3.0.0
displayName: "Godot Position Sync Orchestrator"
description: >
  Use when Godot project has position conflicts between editor (.tscn) and code (.gd),
  camera-following backgrounds, or runtime positions don't match editor preview.
  Orchestrates all 3 position sync mini-skills: sync-static-positions, sync-camera-positions,
  and sync-parallax. Each operation targets specific position conflict types.
author: "Asreonn"
license: MIT
category: game-development
type: agent
difficulty: beginner
audience: [developers, level-designers]
keywords:
  - godot
  - positions
  - editor-sync
  - camera
  - parallax
  - wysiwyg
  - level-design
  - godot4
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme
filesystem:
  read:
    - "${PROJECT_ROOT}/**/*.gd"
    - "${PROJECT_ROOT}/**/*.tscn"
    - "${PROJECT_ROOT}/project.godot"
  write:
    - "${PROJECT_ROOT}/**/*.gd"
    - "${PROJECT_ROOT}/**/*.tscn"
  deny:
    - "**/.env*"
    - "**/secrets*"
    - "**/*.key"
behavior:
  timeout: 300
  retry: 2
  cache: true
  interactive: true
use_cases:
  - "Node position set in _ready() doesn't match editor preview"
  - "Background follows camera but editor shows wrong position"
  - "Parallax layers jump when game starts"
  - "Want What You See Is What You Get in editor"
  - "Position conflicts making level design confusing"
  - "Need to sync all position types at once"
outputs: "Synced positions, updated .tscn files, clear ownership documentation, git commits per sync type"
requirements: "Git repository, Godot 4.x"
execution: "Automatic detection with user-approved sync strategies"
auto_rollback: "Yes - reverts on validation failure"
integration: "Orchestrates: godot-sync-static-positions, godot-sync-camera-positions, godot-sync-parallax"
---

# Godot Fix Positions Orchestrator

**This orchestrator runs 3 position sync mini-skills in sequence. For individual operations, invoke mini-skills directly.**

## Core Principle: What You See Is What You Get (WYSIWYG)

**Iron Law**: Editor preview must match runtime behavior. No surprises.

This skill automatically detects and resolves position conflicts between editor-defined positions (.tscn files) and code-defined positions (.gd files). It handles static conflicts, camera-following backgrounds, parallax layers, and player-relative positioning.

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

### 2. Begin Phase 1: Detection & Analysis (AUTOMATIC)

**Do NOT ask "What would you like me to do?" - Start analyzing immediately.**

Execute these commands in parallel:

```bash
# Detect static position conflicts
find . -name "*.gd" -exec grep -l "position\s*=" {} \; | head -20

# Find camera-following patterns
grep -rn "position\s*=.*camera\|position\s*=.*player" --include="*.gd" . | head -20

# Find parallax backgrounds
find . -name "*parallax*.tscn" -o -name "*background*.tscn" | head -10

# Count potential conflicts
find . -name "*.gd" -exec grep -c "^\s*position\s*=" {} + | awk '{s+=$1} END {print s}'
```

### 3. Present Findings (30 seconds)

Show the user:
```
=== Editor Position Sync Analysis ===

Project: [project name from project.godot]

Conflicts detected:
- Static position assignments: X
- Camera-following elements: X
- Parallax backgrounds: X
- Player-relative positioning: X

Total: X position conflicts found

Sync includes:
✓ Detect editor vs code position conflicts
✓ Smart classification (intentional vs conflict)
✓ Camera-aware positioning
✓ Multiple sync strategies
✓ Git commit per operation
✓ Auto-rollback on test failure

Would you like me to:
1. Proceed with automatic sync (recommended)
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

**Static Position Conflicts:**
- `position = Vector2(x, y)` in `_ready()` or `_init()`
- Editor shows one position, runtime shows different position
- Nodes appear in wrong locations when game starts
- Visual debugging reveals position mismatches

**Camera-Following Elements:**
- Backgrounds that follow camera position
- UI elements that track player
- Parallax layers with camera sync
- `position = camera.position` patterns

**Player-Relative Positioning:**
- Nodes positioned relative to player
- `position = player.position + offset` patterns
- Elements that track player movement
- Camera-relative UI elements

**Editor Preview Mismatch:**
- "It looks right in the editor but wrong at runtime"
- "The background jumps when the game starts"
- "My UI elements are in the wrong place"
- "Camera-following nodes don't preview correctly"

### Decision Flowchart

```
User mentions position issues
    ↓
Is it editor vs runtime mismatch?
    ↓ YES                    ↓ NO
Use this skill              Different issue
    ↓
Run Phase 1: Detection
    ↓
Conflicts found?
    ↓ YES                    ↓ NO
Run Phases 2-3              Document clean state
```

---

## The Three Phases

### Phase 1: Detection & Analysis (Automatic)

**Purpose**: Detect position conflicts and classify them intelligently.

**Steps:**

1. **Scan Project Files**
```bash
# Find all Godot script files
find . -name "*.gd" -type f

# Find all scene files
find . -name "*.tscn" -type f
```

2. **Detect Position Assignments**

Scan for position-setting patterns:

```bash
# Static position assignments
grep -rn "position\s*=\s*Vector2(" --include="*.gd" .

# Camera-following patterns
grep -rn "position\s*=.*camera" --include="*.gd" .

# Player-following patterns
grep -rn "position\s*=.*player" --include="*.gd" .

# Parallax patterns
grep -rn "ParallaxBackground\|ParallaxLayer" --include="*.gd" .
```

3. **Parse .tscn Files for Positions**

Extract position properties from scenes:

```bash
# Find position declarations in .tscn files
grep -rn "^position\s*=\s*Vector2(" --include="*.tscn" .
```

4. **Intelligent Classification**

For each detected position assignment, classify as:

- **CONFLICT**: Static position in `_ready()` differs from .tscn
- **INTENTIONAL_DYNAMIC**: Camera/player following (skip)
- **INTENTIONAL_ANIMATION**: Tweens/animations (skip)
- **PROCESS_ASSIGNMENT**: Every-frame in `_process()` (critical warning)

**Classification Logic:**

```python
def classify_position_assignment(context):
    # Context = 30 lines around assignment

    # SKIP: Animation/tween
    if "tween" in context or "create_tween" in context:
        return "INTENTIONAL_ANIMATION"

    # SKIP: Camera following
    if "camera.position" in context or "get_viewport().get_camera" in context:
        return "INTENTIONAL_DYNAMIC"

    # SKIP: Player following
    if "player.position" in context or "target.position" in context:
        return "INTENTIONAL_DYNAMIC"

    # CRITICAL: Every frame assignment
    if "_process(" in context:
        return "PROCESS_ASSIGNMENT"

    # CONFLICT: Static assignment in _ready
    if "_ready(" in context and "Vector2(" in line:
        return "CONFLICT"

    return "UNKNOWN"
```

5. **Create Conflict Manifest**

Generate a priority-ordered list:

| File | Node | Editor Position | Code Position | Classification | Sync Strategy |
|------|------|-----------------|---------------|----------------|---------------|
| background.gd | Background | (0, 0) | camera.position | DYNAMIC | Document intent |
| enemy.gd | Enemy | (500, 300) | (100, 150) | CONFLICT | Code → Editor |
| ui_label.gd | Label | (10, 10) | (50, 50) | CONFLICT | Editor → Code |

**Phase 1 Output:**
- ✓ All position assignments detected
- ✓ Conflicts classified intelligently
- ✓ Manifest table generated
- ✓ Ready for synchronization

---

### Phase 2: Position Synchronization (Three Strategies)

Process conflicts in priority order: Critical → Conflicts → Dynamic

**CRITICAL - After Each Operation:**
1. Git commit the changes
2. **Run automatic validation test**
3. If test fails: Auto-revert and report error
4. If test passes: **Continue automatically to next conflict**
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

#### Strategy A: Code → Editor Sync

**Target**: Static position conflicts where code position should be editor position

**When to use:**
- Code position is intentional final position
- Editor preview should match runtime
- Position set once in `_ready()` and never changes

**Process:**

1. **Detect Conflict**
```bash
# Example: enemy.gd sets position in _ready()
grep -A5 "_ready" enemy.gd
```

Example code:
```gdscript
# enemy.gd
func _ready():
    position = Vector2(100, 150)  # Conflict with .tscn
```

Example .tscn:
```ini
[node name="Enemy" type="CharacterBody2D"]
position = Vector2(500, 300)  # Different from code
```

2. **Update .tscn File**

Parse and update:
```python
# Read .tscn file
with open("enemy.tscn") as f:
    content = f.read()

# Find and replace position line
content = re.sub(
    r'position = Vector2\([^)]+\)',
    'position = Vector2(100, 150)',
    content
)

# Write back
with open("enemy.tscn", "w") as f:
    f.write(content)
```

3. **Update .gd File**

Remove static assignment, add comment:
```gdscript
# enemy.gd
func _ready():
    # Position moved to .tscn for editor visibility
    # Was: position = Vector2(100, 150)
    pass
```

4. **Git Commit**
```bash
git add enemy.tscn enemy.gd
git commit -m "Sync: Move enemy position from code to editor (.tscn)

- Updated enemy.tscn position to Vector2(100, 150)
- Removed static position assignment from enemy.gd
- Editor now matches runtime position"
```

5. **Run automatic test** (see Phase 2 header for test procedure)

**Success criteria:**
- .tscn position matches intended runtime position
- Code assignment removed
- Comment documents change
- Behavior unchanged

---

#### Strategy B: Editor → Code Sync

**Target**: Position should be set in code, remove .tscn position

**When to use:**
- Position is calculated/dynamic
- .tscn position is arbitrary/wrong
- Code position is source of truth

**Process:**

1. **Keep Code Assignment**

Code already correct:
```gdscript
func _ready():
    position = Vector2(100, 150)  # Correct position
```

2. **Reset .tscn to Default**

Update .tscn to neutral position:
```ini
[node name="Enemy" type="CharacterBody2D"]
# position removed (defaults to Vector2(0, 0))
```

Or explicitly set to origin:
```ini
position = Vector2(0, 0)
```

3. **Add Documentation**

Add comment explaining:
```gdscript
func _ready():
    # Position set in code (not in .tscn)
    # Editor shows (0,0), runtime shows calculated position
    position = Vector2(100, 150)
```

4. **Git Commit**
```bash
git commit -m "Sync: Keep enemy position in code, reset editor

- Removed position from enemy.tscn (defaults to origin)
- Kept code position assignment
- Runtime position calculated in _ready()"
```

5. **Run automatic test**

---

#### Strategy C: Camera-Aware Positioning (SPECIAL)

**Target**: Backgrounds, parallax layers, camera-following elements

**When to use:**
- Background follows camera
- Parallax layers
- Player-relative UI elements
- Dynamic camera positioning

**Special Case - User's Background Issue:**

**Problem**: Background positioned at (0, 0) in editor, but follows camera at runtime, causing confusion during level design.

**Solution**:

1. **Detect Camera-Following Pattern**

```gdscript
# background.gd
func _process(delta):
    position = camera.position  # Follows camera
```

2. **Calculate Expected Editor Position**

Find typical camera start position:
```bash
# Search for camera or player spawn position
grep -rn "camera.*position\|player.*position" --include="*.tscn" .
```

Example: Camera starts at (512, 300)

3. **Update .tscn to Camera Start Position**

```ini
[node name="Background" type="Sprite2D"]
position = Vector2(512, 300)  # Camera start position
```

4. **Document Camera-Relative Behavior**

```gdscript
# background.gd
func _process(delta):
    # EDITOR NOTE: Position in .tscn shows camera start position
    # for accurate level design preview. At runtime, follows camera.
    position = camera.position
```

5. **Create Editor Preview Tool (Optional)**

Generate editor plugin to show camera bounds:

```gdscript
# addons/camera_preview/camera_preview.gd
@tool
extends EditorPlugin

func _enter_tree():
    # Draw camera bounds in editor
    pass
```

**Result:**
- Editor shows realistic preview
- Background appears at expected camera position
- Level design is accurate
- Runtime behavior unchanged

6. **Git Commit**
```bash
git commit -m "Sync: Camera-aware background positioning

- Updated background.tscn to camera start position
- Added documentation for camera-following behavior
- Editor now shows accurate runtime preview"
```

7. **Run automatic test**

**Success criteria:**
- Editor preview shows realistic camera view
- Runtime behavior unchanged
- Level design is accurate
- Documentation explains dynamic behavior

---

### Phase 3: Verification & Reporting

**Purpose**: Ensure synchronization succeeded without regressions.

**Steps:**

1. **Open project in Godot**
```bash
godot --editor project.godot
```

2. **Visual verification**
- Open synced scenes in editor
- Compare editor positions with manifest
- Verify positions match expected

3. **Runtime verification**
```bash
# Run main scene for 10 seconds
godot --quit-after 10 project.godot
```

4. **Check for conflicts**
```bash
# Re-run detection to verify all conflicts resolved
grep -rn "position\s*=\s*Vector2(" --include="*.gd" . | wc -l
```

5. **Generate Report**

```
=== Position Sync Complete ===

Conflicts resolved: X
- Code → Editor: X
- Editor → Code: X
- Camera-aware: X

Files modified:
- X .tscn files updated
- X .gd files updated

Git commits created: X

All tests passing ✓
No regressions detected ✓
Editor preview matches runtime ✓
```

---

## Supporting Files

This skill uses modular reference files:

- **position-detection-patterns.md**: All grep patterns for position detection
- **sync-strategies.md**: Detailed step-by-step procedures
- **camera-aware-positioning.md**: Camera/parallax handling
- **validation-tests.md**: Testing procedures

Read these files for detailed implementation guidance.

---

## Red Flags - STOP

These thoughts mean you're rationalizing away discipline:

| Rationalization | Reality | Fix |
|----------------|---------|-----|
| "This dynamic position is a conflict" | Misclassification breaks behavior | Use intelligent classifier |
| "I'll sync all positions" | Over-sync breaks intentional dynamic positioning | Only sync true conflicts |
| "Camera-following is a conflict" | Wrong - it's intentional | Skip dynamic patterns |
| "I don't need to test this change" | Untested = broken | Always verify |
| "Close enough in editor" | Iron Law has no exceptions | Exact positions only |
| "I'll manually fix .tscn" | Manual edits create errors | Parse programmatically |

---

## Quick Reference: Conflict → Strategy

| Conflict Type | Detection | Strategy |
|--------------|-----------|----------|
| Static in _ready() | `position = Vector2()` in _ready | Code → Editor |
| Calculated position | `position = calc_spawn()` | Editor → Code |
| Camera-following | `position = camera.position` | Camera-aware |
| Parallax layer | ParallaxLayer + scroll | Camera-aware |
| Player-relative | `position = player.position + offset` | Document dynamic |
| Animation/tween | `tween_property("position")` | SKIP (intentional) |
| Every frame (_process) | position in _process | CRITICAL warning |

---

## Camera-Aware Positioning - Special Features

### For User's Background Use Case

**Problem Statement:**
- Background layer positioned at (0, 0) in editor
- At runtime, background follows camera: `position = camera.position`
- Editor shows wrong position → confusing for level design
- Need: Show correct position in BOTH editor and runtime

**Solution:**

1. **Detect Camera Start Position**
```bash
# Find main camera or player spawn point
grep -rn "Camera2D\|player.*position" --include="*.tscn" .
```

2. **Calculate Editor Position**
```python
# Parse camera start position from main scene
camera_start = Vector2(512, 300)  # Example

# Set background .tscn to camera start
background_position = camera_start
```

3. **Update Background .tscn**
```ini
[node name="Background" type="Sprite2D"]
position = Vector2(512, 300)  # Camera start (was 0, 0)
```

4. **Document Behavior**
```gdscript
# background.gd
# EDITOR PREVIEW: Position set to camera start for accurate level design
# RUNTIME: Follows camera dynamically
func _process(delta):
    position = camera.position
```

5. **Create Parallax Handler (If Needed)**

For ParallaxBackground nodes:
```gdscript
# parallax_background.gd
@export var camera_start_position := Vector2(512, 300)

func _ready():
    # Set initial scroll to camera start
    scroll_offset = camera_start_position
```

**Result:**
- Editor shows background at camera start position
- Level design is accurate
- Runtime follows camera as intended
- WYSIWYG achieved ✓

---

## Execution Strategy

This skill runs **fully automatically**:

1. User invokes skill on Godot project
2. Phase 1: Scan and report findings
3. User approves synchronization
4. Phase 2: Execute all sync operations with commits
5. Phase 3: Verify and report results

**User input required:**
- Initial invocation
- Approval after Phase 1 analysis
- Strategy selection (if ambiguous)
- Final verification check

**Everything else is automatic:**
- Position conflict detection
- Intelligent classification
- .tscn file updates
- Script modifications
- Git commits
- Testing

---

## Success Criteria

Synchronization is complete when:

- ✓ All static position conflicts resolved
- ✓ Camera-following elements documented
- ✓ Editor preview matches runtime positions
- ✓ All scenes load without errors
- ✓ Behavior identical to baseline
- ✓ Visual appearance unchanged
- ✓ Clean git history with descriptive commits

---

## Integration with Other Skills

**Works well with:**
- **godot-refactoring**: Refactor before position sync
- **Scene Hierarchy Cleaner**: Organize backgrounds into groups
- **Scene Layout Organizer**: Align after position sync

**Best practice workflow:**
1. Run godot-refactoring (if needed)
2. Run editor-position-sync
3. Run scene-hierarchy-cleaner (if needed)
4. Continue development

---

**Remember**: Editor preview is your source of truth for visual design. Runtime must match what you see in the editor. No surprises.
