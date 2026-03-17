---
name: godot-modernize-gdscript
version: 1.0.0
displayName: "Godot GDScript 2.0 Modernizer"
description: >
  Modernizes GDScript 1.0 (Godot 3.x) code to GDScript 2.0 (Godot 4.x) syntax.
  Converts yield to await, onready to @onready, export to @export, setget to
  property syntax, and adds optional static typing. Essential for Godot 3.x
  to 4.x migration projects.
author: "Asreonn"
license: MIT
category: game-development
type: tool
difficulty: intermediate
audience: [developers, migrators]
keywords:
  - godot
  - gdscript
  - modernization
  - migration
  - godot3
  - godot4
  - yield
  - await
  - static-typing
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme
filesystem:
  read:
    - "${PROJECT_ROOT}/**/*.gd"
    - "${PROJECT_ROOT}/project.godot"
  write:
    - "${PROJECT_ROOT}/**/*.gd"
  deny:
    - "**/.env*"
    - "**/secrets*"
    - "**/*.key"
behavior:
  timeout: 300
  retry: 2
  cache: true
  interactive: true
---

# Godot GDScript 2.0 Modernizer

**Converts GDScript 1.0 (Godot 3.x) patterns to GDScript 2.0 (Godot 4.x) syntax.**

## Core Conversions

This skill performs five key modernizations:

| GDScript 1.0 | GDScript 2.0 | Pattern |
|-------------|--------------|---------|
| `yield(object, "signal")` | `await object.signal` | Async operations |
| `onready var` | `@onready var` | Node references |
| `export var` | `@export var` | Inspector variables |
| `var x setget set_x, get_x` | Property syntax | Getters/setters |
| `var health = 100` | `var health: int = 100` | Static typing |

---

## UPON INVOCATION - START HERE

When this skill is invoked, IMMEDIATELY execute:

### 1. Verify Godot Project (5 seconds)

```bash
ls project.godot 2>/dev/null && echo "✓ Godot project detected" || echo "✗ Not a Godot project"
```

**If NOT a Godot project:**
- Inform user this skill only works on Godot projects
- STOP here

**If IS a Godot project:**
- Proceed to step 2

### 2. Detect GDScript Version (10 seconds)

```bash
# Check for Godot 3.x patterns
echo "=== Detecting GDScript 1.0 Patterns ==="
echo "yield statements:"
grep -rn "yield(" --include="*.gd" . | wc -l

echo "onready declarations:"
grep -rn "^onready var" --include="*.gd" . | wc -l

echo "export declarations:"
grep -rn "^export var\|^export(int)\|^export(float)" --include="*.gd" . | wc -l

echo "setget properties:"
grep -rn "setget" --include="*.gd" . | wc -l

echo "untyped variables:"
grep -rn "^var [a-z]" --include="*.gd" . | grep -v ":" | wc -l
```

### 3. Present Findings

Show the user:
```
=== GDScript 2.0 Modernization Analysis ===

Project: [project name]
Current: GDScript 1.0 (Godot 3.x style)

Patterns to modernize:
- yield statements: X
- onready variables: X
- export variables: X
- setget properties: X
- untyped variables: X

Total: X modernizations needed

Modernization includes:
✓ yield → await conversion
✓ onready → @onready
✓ export → @export
✓ setget → property syntax
✓ Optional static typing
✓ Git commit per file
✓ Backup before changes

Would you like me to:
1. Modernize all files (recommended)
2. Show detailed breakdown first
3. Select specific conversions
4. Cancel
```

### 4. Wait for User Choice

- **If 1 (Proceed):** Start Phase 2 immediately
- **If 2 (Details):** Show file-by-file breakdown, then offer to proceed
- **If 3 (Selective):** Ask which conversions to apply
- **If 4 (Cancel):** Exit skill

---

## Phase 1: Analysis & Inventory

### 1.1 Create File Inventory

```bash
# Find all .gd files
find . -name "*.gd" -type f | sort > /tmp/gdscript_files.txt
wc -l /tmp/gdscript_files.txt
echo "files found"
```

### 1.2 Analyze Each File

For each .gd file, detect patterns:

```bash
# Analyze patterns per file
for file in $(cat /tmp/gdscript_files.txt); do
    echo "=== $file ==="
    grep -c "yield(" "$file" 2>/dev/null || echo 0
    grep -c "^onready var" "$file" 2>/dev/null || echo 0
    grep -c "^export" "$file" 2>/dev/null || echo 0
    grep -c "setget" "$file" 2>/dev/null || echo 0
done
```

### 1.3 Create Modernization Plan

```
Modernization Plan:
===================

1. yield → await conversions (X files)
2. onready → @onready (X files)
3. export → @export (X files)
4. setget → properties (X files)
5. Static typing (X files)

Total files to modify: X
Estimated time: Auto (user doesn't wait)
Backup created: YES (git tag)
Rollback available: YES
```

---

## Phase 2: Modernization Operations

### Conversion A: yield → await

**Detection:**
```bash
grep -rn "yield(" --include="*.gd" .
```

**Common Patterns:**

| Old Pattern | New Pattern |
|-------------|-------------|
| `yield(get_tree().create_timer(1.0), "timeout")` | `await get_tree().create_timer(1.0).timeout` |
| `yield(timer, "timeout")` | `await timer.timeout` |
| `yield(animation_player, "animation_finished")` | `await animation_player.animation_finished` |
| `yield(get_tree(), "idle_frame")` | `await get_tree().process_frame` |

**Transformation Process:**

1. **Extract yield statement**
   ```gdscript
   # Before
   yield(get_tree().create_timer(2.0), "timeout")
   ```

2. **Convert to await**
   ```gdscript
   # After
   await get_tree().create_timer(2.0).timeout
   ```

3. **Handle variable assignment**
   ```gdscript
   # Before
   var result = yield(async_function(), "completed")
   
   # After
   var result = await async_function()
   ```

**Implementation:**
```python
# Pseudo-code for replacement
def convert_yield_to_await(line):
    # Pattern: yield(object, "signal_name")
    # Convert to: await object.signal_name
    
    import re
    pattern = r'yield\(([^,]+),\s*"([^"]+)"\)'
    replacement = r'await \1.\2'
    return re.sub(pattern, replacement, line)
```

---

### Conversion B: onready → @onready

**Detection:**
```bash
grep -rn "^onready var" --include="*.gd" .
```

**Transformation:**

```gdscript
# Before
onready var player = $Player
onready var health_bar = $UI/HealthBar

# After
@onready var player: Node = $Player
@onready var health_bar: ProgressBar = $UI/HealthBar
```

**Process:**
1. Replace `onready` with `@onready`
2. Add type hints where detectable
3. Keep variable name and initialization

**Type Inference (Optional):**
```gdscript
# If $Player is CharacterBody2D in scene
@onready var player: CharacterBody2D = $Player

# If $Timer is Timer node
@onready var _timer: Timer = $Timer
```

---

### Conversion C: export → @export

**Detection:**
```bash
grep -rn "^export" --include="*.gd" .
```

**Transformation:**

```gdscript
# Before
export var speed = 200
export(int) var max_health = 100
export(float) var jump_force = 500.0
export(String) var character_name = "Player"
export(NodePath) var target_path

# After
@export var speed: float = 200.0
@export var max_health: int = 100
@export var jump_force: float = 500.0
@export var character_name: String = "Player"
@export var target_path: NodePath
```

**Export Types Mapping:**

| Old Export | New Export | Type |
|------------|------------|------|
| `export(int)` | `@export var x: int` | Integer |
| `export(float)` | `@export var x: float` | Float |
| `export(String)` | `@export var x: String` | String |
| `export(bool)` | `@export var x: bool` | Boolean |
| `export(Color)` | `@export var x: Color` | Color |
| `export(Vector2)` | `@export var x: Vector2` | Vector2 |
| `export(Vector3)` | `@export var x: Vector3` | Vector3 |
| `export(NodePath)` | `@export var x: NodePath` | NodePath |
| `export var` | `@export var x: Type` | Inferred |

---

### Conversion D: setget → Property Syntax

**Detection:**
```bash
grep -rn "setget" --include="*.gd" .
```

**Transformation:**

```gdscript
# Before (GDScript 1.0)
var health = 100 setget set_health, get_health

func set_health(value):
    health = clamp(value, 0, max_health)
    health_changed.emit(health)

func get_health():
    return health
```

```gdscript
# After (GDScript 2.0)
var health: int = 100:
    set(value):
        health = clamp(value, 0, max_health)
        health_changed.emit(health)
    get:
        return health
```

**Process:**
1. Remove `setget` from variable declaration
2. Add colon after type
3. Inline setter and getter
4. Use `set(value):` and `get:` syntax

**Complex Example:**
```gdscript
# Before
var score = 0 setget set_score

func set_score(value):
    score = max(0, value)
    update_ui()

# After
var score: int = 0:
    set(value):
        score = max(0, value)
        update_ui()
```

---

### Conversion E: Static Typing (Optional)

**Detection:**
```bash
grep -rn "^var [a-z_]* = " --include="*.gd" . | grep -v ":"
```

**Type Inference:**

| Value | Inferred Type |
|-------|--------------|
| `= 100` | `int` |
| `= 3.14` | `float` |
| `= "text"` | `String` |
| `= true` | `bool` |
| `= Vector2(x, y)` | `Vector2` |
| `= $Node` | Node type from scene |

**Transformation:**
```gdscript
# Before
var health = 100
var speed = 200.5
var name = "Player"
var active = true
var position = Vector2.ZERO

# After
var health: int = 100
var speed: float = 200.5
var name: String = "Player"
var active: bool = true
var position: Vector2 = Vector2.ZERO
```

---

## Phase 3: Execution & Safety

### 3.1 Create Git Baseline

```bash
# Create backup tag
git tag gdscript1-baseline-$(date +%Y%m%d-%H%M%S)

# Stage any current changes
git add .
git commit -m "Baseline: Pre-GDScript 2.0 modernization" || echo "No changes to commit"
```

### 3.2 Process Files Sequentially

For each .gd file:

```bash
# Process file
python3 << 'EOF'
import re

def modernize_gdscript(content):
    # Conversion 1: yield → await
    content = re.sub(
        r'yield\(([^,]+),\s*"([^"]+)"\)',
        r'await \1.\2',
        content
    )
    
    # Conversion 2: onready → @onready
    content = re.sub(
        r'^onready var',
        '@onready var',
        content,
        flags=re.MULTILINE
    )
    
    # Conversion 3: export → @export (simple)
    content = re.sub(
        r'^export var',
        '@export var',
        content,
        flags=re.MULTILINE
    )
    
    return content

# Read, process, write
with open("script.gd", "r") as f:
    content = f.read()

new_content = modernize_gdscript(content)

with open("script.gd", "w") as f:
    f.write(new_content)
EOF
```

### 3.3 Commit Per File

```bash
# After each file modification
git add "$file"
git commit -m "Modernize: $file to GDScript 2.0

- Converted yield to await
- Updated onready to @onready  
- Migrated export to @export
- Applied static typing"
```

### 3.4 Validation After Each File

```bash
# Validate syntax
godot --headless --quit-after 2 project.godot 2>&1 | grep -i "error" && {
    echo "Syntax error detected in $file"
    git reset --hard HEAD~1
    echo "Reverted changes to $file"
}
```

---

## Phase 4: Verification & Testing

### 4.1 Syntax Validation

```bash
# Check all modified files for syntax errors
for file in $(git diff --name-only HEAD~10..HEAD | grep "\.gd$"); do
    echo "Checking $file..."
    # Basic syntax check
    gdscript_tool --check "$file" 2>/dev/null || echo "Manual review needed: $file"
done
```

### 4.2 Pattern Verification

```bash
# Verify no old patterns remain
echo "Checking for remaining GDScript 1.0 patterns..."

echo "yield statements remaining:"
grep -rn "yield(" --include="*.gd" . | wc -l

echo "onready remaining:"
grep -rn "^onready var" --include="*.gd" . | wc -l

echo "export remaining:"
grep -rn "^export var\|^export(" --include="*.gd" . | wc -l
```

### 4.3 Godot Project Test

```bash
# Open project in Godot to verify
godot --editor project.godot &
sleep 5

# Check for errors
# (User should visually verify no red errors in Output panel)
```

---

## Examples

### Example 1: Complete Script Modernization

**Before (GDScript 1.0):**
```gdscript
extends CharacterBody2D

export var speed = 200
export(int) var health = 100

onready var sprite = $Sprite
onready var animation = $AnimationPlayer

var damage = 10 setget set_damage

func set_damage(value):
    damage = clamp(value, 0, 100)

func _ready():
    yield(get_tree().create_timer(1.0), "timeout")
    start_game()

func take_damage(amount):
    health -= amount
    if health <= 0:
        yield(play_death_animation(), "completed")
        queue_free()

func play_death_animation():
    animation.play("death")
    yield(animation, "animation_finished")
```

**After (GDScript 2.0):**
```gdscript
extends CharacterBody2D

@export var speed: float = 200.0
@export var health: int = 100

@onready var sprite: Sprite2D = $Sprite
@onready var animation: AnimationPlayer = $AnimationPlayer

var damage: int = 10:
    set(value):
        damage = clamp(value, 0, 100)

func _ready():
    await get_tree().create_timer(1.0).timeout
    start_game()

func take_damage(amount: int) -> void:
    health -= amount
    if health <= 0:
        await play_death_animation()
        queue_free()

func play_death_animation() -> void:
    animation.play("death")
    await animation.animation_finished
```

### Example 2: Signal Connection Modernization

**Before:**
```gdscript
func _ready():
    button.connect("pressed", self, "_on_button_pressed")
    timer.connect("timeout", self, "_on_timeout")

func _on_button_pressed():
    pass

func _on_timeout():
    pass
```

**After:**
```gdscript
func _ready():
    button.pressed.connect(_on_button_pressed)
    timer.timeout.connect(_on_timeout)

func _on_button_pressed() -> void:
    pass

func _on_timeout() -> void:
    pass
```

---

## Success Criteria

Modernization complete when:

- ✓ Zero `yield(` statements remain (converted to await)
- ✓ Zero `onready var` remain (converted to @onready)
- ✓ Zero `export var` remain (converted to @export)
- ✓ Zero `setget` remain (converted to property syntax)
- ✓ All scripts compile without errors
- ✓ No functional changes (behavior identical)
- ✓ Git history shows clear modernization commits

---

## Common Issues & Solutions

### Issue 1: yield with function calls

**Problem:**
```gdscript
var result = yield(load_data(), "completed")
```

**Solution:**
```gdscript
var result = await load_data()
```

### Issue 2: Coroutines with state

**Problem:**
```gdscript
func process():
    yield(do_step_1(), "completed")
    yield(do_step_2(), "completed")
```

**Solution:**
```gdscript
func process() -> void:
    await do_step_1()
    await do_step_2()
```

### Issue 3: setget with only getter or setter

**Problem:**
```gdscript
var score = 0 setget , get_score  # Only getter
```

**Solution:**
```gdscript
var score: int = 0:
    get:
        return score
```

---

## Rollback Procedure

If modernization causes issues:

```bash
# Find baseline tag
git tag | grep "gdscript1-baseline"

# Reset to pre-modernization state
git reset --hard <baseline-tag>

# Or revert specific commits
git revert <modernization-commit-hash>
```

---

## Integration with Other Skills

**Use before:**
- `godot-refactor` - Modernize syntax first, then refactor architecture
- `godot-migrate-tilemap` - Update code before TileMap migration

**Use after:**
- Project conversion from Godot 3.x to 4.x
- `godot-organize-project` - Organize files first

---

**This skill automates the tedious parts of GDScript 1.0 → 2.0 migration while preserving exact functionality.**
