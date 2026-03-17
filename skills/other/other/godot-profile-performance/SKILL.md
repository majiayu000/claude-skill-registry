---
name: godot-profile-performance
version: 1.0.0
displayName: Godot Performance Profiler
description: Detects performance bottlenecks in Godot projects including expensive _process functions, get_node() calls in loops, instantiations in _process, and provides optimization suggestions with Godot profiler integration
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: intermediate
audience:
  - developers
keywords:
  - godot
  - performance
  - profiler
  - optimization
  - _process
  - frame-time
  - bottleneck
  - memory
  - gdscript
platforms:
  - macos
  - linux
  - windows
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme
permissions:
  filesystem:
    - read: "**/*.gd"
    - read: "**/project.godot"
    - write: "**/*.gd"
    - write: "**/optimization_report.md"
---

# Godot Performance Profiler

## Overview

Analyzes Godot projects to detect performance bottlenecks in GDScript code. Identifies expensive operations in frame-critical functions like `_process`, `_physics_process`, and `_draw`. Provides actionable optimization suggestions with before/after code examples and integrates with Godot's built-in profiler for validation.

**Core principle:** Frame time is precious—expensive operations belong in `_ready` or signal handlers, not per-frame callbacks.

## When to Use

**Use when:**
- Frame rate drops or inconsistent performance
- CPU usage is unexpectedly high
- Game stutters during gameplay
- `_process` functions contain complex logic
- Memory usage grows over time
- Before releasing a game or major update

**Don't use for:**
- Network/server performance issues (use server profiling tools)
- GPU/shader optimization (use Godot's GPU profiler)
- Physics simulation tuning (use Godot's physics debug tools)

## Detection Patterns

### Heavy _process Functions

**Trigger:** Functions with >15 lines of code in `_process` or `_physics_process`

**Detection:**
```bash
# Count lines in process functions
rg "^func _process" -A 50 --glob "*.gd" | wc -l
```

**Thresholds:**
- Warning: >15 lines
- Critical: >30 lines

### get_node() in Loops

**Pattern:**
```gdscript
# ❌ BAD: get_node() in _process
func _process(delta):
    get_node("UI/HealthBar").value = health  # Called every frame!
    get_node("Player").position = position
```

**Detection regex:**
```regex
func _process.*\n(?:.*\n)*?\s+get_node\(
```

### Instantiation in _process

**Pattern:**
```gdscript
# ❌ BAD: Creating objects every frame
func _process(delta):
    var bullet = Bullet.new()  # Memory churn!
    add_child(bullet)
```

**Detection keywords:**
- `.new()` in `_process` or `_physics_process`
- `.instantiate()` in frame callbacks
- `add_child()` or `remove_child()` in loops

### Complex Operations in _physics_process

**Anti-patterns:**
- Heavy pathfinding calculations
- Complex AI state machines
- Large array operations
- File I/O or network calls

## Analysis Procedures

### Frame Time Analysis

**Steps:**
1. Enable Godot profiler (Debug > Profiler)
2. Run game for 60 seconds of typical gameplay
3. Identify functions with high "Time (ms)" values
4. Sort by "Time %" to find top offenders
5. Look for functions >0.1ms per frame

**Interpretation:**
- <0.01ms: Excellent
- 0.01-0.05ms: Good
- 0.05-0.1ms: Acceptable
- >0.1ms: Needs optimization

### Memory Usage Detection

**Indicators:**
- Continuous growth in Memory monitor
- Frequent garbage collection spikes
- Node count increasing over time

**Detection:**
```bash
# Check for object creation in process functions
rg "\.new\(\)|instantiate\(\)" -B 5 -A 2 --glob "*.gd" | \
  rg -A 10 "func _process|func _physics_process"
```

### Draw Call Optimization

**Check:**
- Godot's "Monitors" tab > "Draw Calls"
- Each unique material = additional draw call
- GPU skinning vs CPU skinning

**Optimization targets:**
- <100 draw calls for 2D games
- <500 draw calls for simple 3D
- Use texture atlases to reduce material switches

### Physics Performance

**Red flags:**
- High collision shape complexity
- Too many rigid bodies (>100)
- Complex polygon collisions
- `_physics_process` doing non-physics work

## Optimization Suggestions

### Cache Node References

**Before:**
```gdscript
extends CharacterBody2D

func _process(delta):
    get_node("UI/HealthBar").value = health
    get_node("UI/ManaBar").value = mana
    get_node("UI/LevelLabel").text = str(level)
```

**After:**
```gdscript
extends CharacterBody2D

@onready var health_bar = $UI/HealthBar
@onready var mana_bar = $UI/ManaBar
@onready var level_label = $UI/LevelLabel

func _process(delta):
    health_bar.value = health
    mana_bar.value = mana
    level_label.text = str(level)
```

**Impact:** Eliminates 3 node lookups per frame (~0.01ms each)

### Move Initialization to _ready

**Before:**
```gdscript
func _process(delta):
    var gravity = ProjectSettings.get("physics/2d/default_gravity")
    velocity.y += gravity * delta
```

**After:**
```gdscript
var gravity

func _ready():
    gravity = ProjectSettings.get("physics/2d/default_gravity")

func _process(delta):
    velocity.y += gravity * delta
```

### Object Pooling for Bullets/Particles

**Before:**
```gdscript
func shoot():
    var bullet = BulletScene.instantiate()
    bullet.position = global_position
    get_parent().add_child(bullet)
```

**After:**
```gdscript
var bullet_pool: Array[Bullet] = []

func _ready():
    # Pre-instantiate bullets
    for i in range(50):
        var bullet = BulletScene.instantiate()
        bullet.hide()
        bullet_pool.append(bullet)
        get_parent().add_child(bullet)

func shoot():
    for bullet in bullet_pool:
        if not bullet.visible:
            bullet.position = global_position
            bullet.show()
            bullet.activate()
            return
```

**Impact:** Eliminates instantiation overhead during gameplay

### Signal-Based Updates

**Before:**
```gdscript
func _process(delta):
    # Checking every frame if health changed
    if health != previous_health:
        update_health_bar()
        previous_health = health
```

**After:**
```gdscript
signal health_changed(new_health)

var health = 100:
    set(value):
        if health != value:
            health = value
            health_changed.emit(health)

func _ready():
    health_changed.connect(update_health_bar)
```

### Batch Array Operations

**Before:**
```gdscript
func _process(delta):
    for enemy in enemies:
        if enemy.position.distance_to(player.position) < 100:
            enemy.target_player()
```

**After:**
```gdscript
var check_timer = 0.0
const CHECK_INTERVAL = 0.1  # Check 10x per second, not 60x

func _process(delta):
    check_timer += delta
    if check_timer >= CHECK_INTERVAL:
        check_timer = 0
        update_enemy_targets()

func update_enemy_targets():
    for enemy in enemies:
        if enemy.position.distance_to(player.position) < 100:
            enemy.target_player()
```

## Godot Profiler Integration

### Enabling the Profiler

1. Run game with Debug > Start with Profiler
2. Or click the "Profiler" tab in the bottom panel while game runs
3. Enable specific monitors:
   - CPU Time
   - Function Time
   - Node Count
   - Memory
   - Draw Calls

### Key Metrics to Monitor

**Frame Time (ms):**
- Shows total time per frame
- Target: <16.67ms for 60 FPS, <33.33ms for 30 FPS
- Spikes indicate hitches

**Function Breakdown:**
- Lists all functions sorted by time
- Look for `_process`, `_physics_process`, `_draw`
- Click function name to see callers

**Memory Monitor:**
- Watch for continuous growth
- Sudden spikes indicate allocations
- Plateaus followed by drops = garbage collection

### Profiling Workflow

```
1. Establish baseline (unoptimized)
   └─ Record profiler data for 60 seconds

2. Identify top 3 time consumers
   └─ Sort by "Time %" in profiler

3. Apply optimization
   └─ Use patterns above

4. Validate improvement
   └─ Profile again, compare metrics
   └─ Verify frame time reduced

5. Repeat for next bottleneck
```

## Examples

### Example 1: UI Controller Optimization

**Problem:**
```gdscript
# ui_controller.gd
extends Control

func _process(delta):
    # Called every frame - 5 node lookups!
    get_node("HealthBar").value = player.health
    get_node("ManaBar").value = player.mana
    get_node("LevelLabel").text = "Level: " + str(player.level)
    get_node("XpBar").value = player.xp
    get_node("GoldLabel").text = "Gold: " + str(player.gold)
```

**Profiler Output:**
```
Function          | Time (ms) | Time %
----------------------------------------
_process          | 0.18      | 12.3%
get_node          | 0.15      | 10.2%  (x5)
```

**Optimized:**
```gdscript
# ui_controller.gd
extends Control

@onready var health_bar = $HealthBar
@onready var mana_bar = $ManaBar
@onready var level_label = $LevelLabel
@onready var xp_bar = $XpBar
@onready var gold_label = $GoldLabel

func _ready():
    # Connect to player signals instead of polling
    player.health_changed.connect(_on_health_changed)
    player.mana_changed.connect(_on_mana_changed)
    player.leveled_up.connect(_on_leveled_up)
    player.xp_changed.connect(_on_xp_changed)
    player.gold_changed.connect(_on_gold_changed)

func _on_health_changed(value): health_bar.value = value
func _on_mana_changed(value): mana_bar.value = value
func _on_leveled_up(level): level_label.text = "Level: " + str(level)
func _on_xp_changed(value): xp_bar.value = value
func _on_gold_changed(value): gold_label.text = "Gold: " + str(value)
```

**Result:**
```
Function          | Time (ms) | Time %
----------------------------------------
_process          | 0.00      | 0.0%   (removed!)
_on_health_changed| 0.01      | 0.7%   (event-driven)
```

### Example 2: Enemy Spawner Fix

**Problem:**
```gdscript
# spawner.gd
extends Node2D

func _process(delta):
    if enemies.size() < max_enemies:
        var enemy = EnemyScene.instantiate()  # Memory churn!
        enemy.position = random_position()
        add_child(enemy)
        enemies.append(enemy)
```

**Memory leak:** Continuous instantiation without pooling

**Optimized:**
```gdscript
# spawner.gd
extends Node2D

var spawn_timer = 0.0
const SPAWN_RATE = 2.0  # Check spawn every 2 seconds

func _process(delta):
    spawn_timer += delta
    if spawn_timer >= SPAWN_RATE:
        spawn_timer = 0
        try_spawn()

func try_spawn():
    if enemies.size() < max_enemies:
        spawn_enemy()

func spawn_enemy():
    # Consider object pool for frequent spawns
    var enemy = EnemyScene.instantiate()
    enemy.position = random_position()
    add_child(enemy)
    enemies.append(enemy)
```

**Additional improvement:** Use object pooling for frequently spawned enemies

### Example 3: Physics Optimization

**Problem:**
```gdscript
# player.gd
extends CharacterBody2D

func _physics_process(delta):
    # Heavy calculation every physics frame
    var nearby = get_tree().get_nodes_in_group("enemies")
    for enemy in nearby:
        if global_position.distance_to(enemy.global_position) < detection_radius:
            enemy.set_target(self)
    
    # Do physics
    velocity.y += gravity * delta
    move_and_slide()
```

**Profiler Output:**
```
Function              | Time (ms) | Time %
--------------------------------------------
_physics_process      | 0.45      | 28.5%
get_nodes_in_group    | 0.25      | 15.8%
distance_to           | 0.12      | 7.6%
```

**Optimized:**
```gdscript
# player.gd
extends CharacterBody2D

var detection_timer = 0.0
const DETECTION_RATE = 0.2  # 5x per second

func _physics_process(delta):
    # Separate physics from AI
    velocity.y += gravity * delta
    move_and_slide()
    
    # Run detection less frequently
    detection_timer += delta
    if detection_timer >= DETECTION_RATE:
        detection_timer = 0
        update_enemy_detection()

func update_enemy_detection():
    var nearby = get_tree().get_nodes_in_group("enemies")
    for enemy in nearby:
        if global_position.distance_to(enemy.global_position) < detection_radius:
            enemy.set_target(self)
```

**Result:** Physics frame time reduced by ~60%

## Success Criteria

A performance optimization is successful when:

### Quantitative Metrics
- [ ] Target function frame time reduced by >50%
- [ ] `_process` function line count <15 lines
- [ ] Zero `get_node()` calls in `_process` or `_physics_process`
- [ ] Zero `.new()` or `.instantiate()` calls in frame callbacks
- [ ] Profiler "Time %" for top 3 functions <30% combined
- [ ] Frame time stays <16.67ms for 60 FPS target
- [ ] Memory usage stable (no continuous growth)

### Qualitative Checks
- [ ] Node references cached in `_ready()` or `@onready`
- [ ] Complex logic moved to signals or timers
- [ ] Object pooling used for frequent instantiations
- [ ] `_physics_process` contains only physics-related code
- [ ] Profiler data shows improvement vs baseline

### Validation Steps
1. **Profile before:** Record baseline metrics
2. **Apply optimization:** Make targeted changes
3. **Profile after:** Compare metrics
4. **Verify in-game:** Test actual gameplay feels smoother
5. **Check edge cases:** Ensure optimization works in all scenarios

## Quick Reference

| Pattern | Detection | Fix | Impact |
|---------|-----------|-----|--------|
| get_node() in _process | Search: `get_node` after `_process` | Cache in `@onready` | ~0.01ms per call |
| .new() in _process | Search: `.new()` in frame functions | Use object pooling | Eliminates GC pressure |
| Heavy _process | Count lines >15 | Move to signals/timers | Reduces per-frame load |
| Physics + AI | AI in `_physics_process` | Separate with timer | 5-10x reduction |
| Uncached settings | `ProjectSettings.get()` in loop | Cache in `_ready` | One-time cost |

## Common Mistakes

### Mistake: "I'll optimize later"
**Problem:** Technical debt accumulates, harder to fix later
**Fix:** Profile early and often, fix bottlenecks as they appear

### Mistake: Premature optimization
**Problem:** Optimizing code that isn't a bottleneck
**Fix:** Always profile first, focus on top time consumers

### Mistake: Micro-optimizations
**Problem:** Spending hours to save 0.001ms
**Fix:** Target functions >0.1ms, ignore the rest

### Mistake: Not validating improvements
**Problem:** Assuming optimization worked without measuring
**Fix:** Always run profiler before and after

### Mistake: Optimizing release builds only
**Problem:** Debug builds have different performance characteristics
**Fix:** Profile release builds for accurate data
