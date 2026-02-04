---
name: godot-setup-animationtree
version: 1.0.0
displayName: Setup AnimationTree State Machine
description: >
  Use when setting up AnimationTree nodes for state machine-driven animation,
  creating AnimationNodeStateMachine graphs, configuring BlendSpace2D/3D
  for locomotion blending, implementing state transition conditions,
  or creating animation blend trees for complex animation mixing.
  Supports player character animations, NPCs, and complex animation systems.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: advanced
audience: [developers]
keywords:
  - godot
  - animation
  - animationtree
  - state-machine
  - blendspace
  - blendspace2d
  - blendspace3d
  - transitions
  - animationtreeplayer
  - locomotion
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".gd", ".tscn", ".tres"]
    write: [".tscn", ".tres", ".gd"]
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "AnimationTree node configurations, AnimationNodeStateMachine graphs, BlendSpace2D/3D setups, transition conditions, animation controller scripts"
requirements: "Git repository, Godot 4.x, AnimatedSprite3D or Sprite2D with AnimationPlayer"
execution: "Fully automatic with scene generation and script updates"
integration: "Works with godot-add-signals for animation events and godot-extract-to-scenes for character scene organization"
---

# Setup AnimationTree State Machine

## Core Principle

**Animation is state-driven, not frame-driven.** Use AnimationTree to manage animation states, BlendSpaces for smooth parameter blending, and transitions for state changes. Avoid direct AnimationPlayer playback in gameplay code.

## What This Skill Does

Sets up complete AnimationTree systems:

1. **AnimationTree Node Structure** - Creates the tree node and animation player binding
2. **AnimationNodeStateMachine** - Builds state machine graphs with entry/exit states
3. **BlendSpace2D/3D** - Configures locomotion blending based on velocity/input
4. **State Transitions** - Defines conditions (bool, expression, time-based) for state changes
5. **Blend Trees** - Creates complex animation mixing with OneShot, Add2, Blend2 nodes

## AnimationTree Setup

### Basic AnimationTree Configuration

**Before (Direct AnimationPlayer):**
```gdscript
# player_animation.gd - Manual animation management
extends CharacterBody2D

@onready var anim_player: AnimationPlayer = $AnimationPlayer

func _physics_process(delta):
    var velocity = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    
    if velocity.length() > 0:
        if not anim_player.current_animation == "run":
            anim_player.play("run")
    else:
        if not anim_player.current_animation == "idle":
            anim_player.play("idle")
```

**After (AnimationTree):**
```gdscript
# player_animation.gd - State-driven animation
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
@onready var playback: AnimationNodeStateMachinePlayback

func _ready():
    animation_tree.active = true
    playback = animation_tree.get("parameters/playback")

func _physics_process(delta):
    var input_dir = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    
    # Update blend position for BlendSpace2D
    animation_tree.set("parameters/blend_position", input_dir)
    
    # Transition states
    if input_dir.length() > 0.1:
        playback.travel("Locomotion")
    else:
        playback.travel("Idle")
```

**Generated Scene:**
```ini
# player.tscn
[gd_scene load_steps=6 format=3]

[ext_resource type="Script" path="res://player_animation.gd" id="1_abc123"]

[sub_resource type="AnimationNodeAnimation" id="AnimationNodeAnimation_idle"]
animation = &"idle"

[sub_resource type="AnimationNodeBlendSpace2D" id="AnimationNodeBlendSpace2D_loco"]
blend_point_0/node = SubResource("AnimationNodeAnimation_idle")
blend_point_0/pos = Vector2(0, 0)
blend_point_1/node = SubResource("AnimationNodeAnimation_walk")
blend_point_1/pos = Vector2(0, 1)
blend_point_2/node = SubResource("AnimationNodeAnimation_run")
blend_point_2/pos = Vector2(0, 1.5)

[sub_resource type="AnimationNodeStateMachine" id="AnimationNodeStateMachine_main"]
states/Idle/node = SubResource("AnimationNodeAnimation_idle")
states/Idle/position = Vector2(300, 100)
states/Locomotion/node = SubResource("AnimationNodeBlendSpace2D_loco")
states/Locomotion/position = Vector2(500, 100)

[sub_resource type="AnimationNodeStateMachinePlayback" id="AnimationNodeStateMachinePlayback_main"]

[node name="Player" type="CharacterBody2D"]
script = ExtResource("1_abc123")

[node name="AnimationPlayer" type="AnimationPlayer" parent="."]

[node name="AnimationTree" type="AnimationTree" parent="."]
anim_player = NodePath("../AnimationPlayer")
tree_root = SubResource("AnimationNodeStateMachine_main")
parameters/playback = SubResource("AnimationNodeStateMachinePlayback_main")
parameters/blend_position = Vector2(0, 0)
```

### AnimationTree Activation

```gdscript
# Essential setup for AnimationTree
func _ready():
    # Activate the tree (must be done after node is ready)
    animation_tree.active = true
    
    # Get reference to state machine playback
    playback = animation_tree.get("parameters/playback")
    
    # Optional: Set initial state
    playback.start("Idle")
```

## AnimationNodeStateMachine

### State Machine Structure

**State Machine Graph:**
```ini
# State machine nodes in .tscn format
[sub_resource type="AnimationNodeStateMachine" id="AnimationNodeStateMachine_character"]
states/Start/position = Vector2(150, 100)
states/End/position = Vector2(800, 100)

# Idle state (single animation)
states/Idle/node = SubResource("AnimationNodeAnimation_idle")
states/Idle/position = Vector2(300, 100)

# Locomotion (blend space)
states/Locomotion/node = SubResource("AnimationNodeBlendSpace2D_loco")
states/Locomotion/position = Vector2(500, 100)

# Attack (one-shot animation)
states/Attack/node = SubResource("AnimationNodeOneShot_attack")
states/Attack/position = Vector2(500, 300)

# Death state
states/Death/node = SubResource("AnimationNodeAnimation_death")
states/Death/position = Vector2(700, 100)
```

### State Transitions

**Transition Configuration:**
```ini
# Transitions between states
[sub_resource type="AnimationNodeStateMachine" id="AnimationNodeStateMachine_character"]

# Idle -> Locomotion (auto on bool parameter)
transitions = ["Idle", "Locomotion", SubResource("AnimationNodeStateMachineTransition_idle_to_loco")]

# Locomotion -> Idle
transitions = ["Locomotion", "Idle", SubResource("AnimationNodeStateMachineTransition_loco_to_idle")]

# Any State -> Attack (using Attack trigger)
transitions = ["Start", "Attack", SubResource("AnimationNodeStateMachineTransition_attack")]

# Any State -> Death
transitions = ["Start", "Death", SubResource("AnimationNodeStateMachineTransition_death")]
```

**Transition Resource Definitions:**
```gdscript
# Transition with condition
var transition = AnimationNodeStateMachineTransition.new()
transition.switch_mode = AnimationNodeStateMachineTransition.SWITCH_MODE_IMMEDIATE
transition.advance_mode = AnimationNodeStateMachineTransition.ADVANCE_MODE_AUTO
transition.advance_condition = "is_moving"

# Transition with expression (Godot 4.1+)
transition.advance_expression = "velocity.length() > 0.1"

# Transition with time condition
transition.switch_mode = AnimationNodeStateMachineTransition.SWITCH_MODE_AT_END
```

### Playback Control

```gdscript
# State machine playback script
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
var playback: AnimationNodeStateMachinePlayback

func _ready():
    animation_tree.active = true
    playback = animation_tree.get("parameters/playback")

func _physics_process(delta):
    # Transition to locomotion state
    if velocity.length() > 0.1:
        playback.travel("Locomotion")
    else:
        playback.travel("Idle")
    
    # Trigger attack (OneShot)
    if Input.is_action_just_pressed("attack"):
        playback.travel("Attack")
    
    # Trigger death (immediate)
    if health <= 0:
        playback.travel("Death")

func stop_movement():
    # Stop at current state
    playback.stop()
    
func reset_to_idle():
    # Start over from Start node
    playback.start("Idle")
```

## BlendSpace2D Configuration

### Locomotion Blend Space

**Before (No Blending):**
```gdscript
# Discrete animations - jarring transitions
func update_animation():
    if velocity.length() < 0.1:
        anim_player.play("idle")
    elif velocity.length() < 100:
        anim_player.play("walk")
    else:
        anim_player.play("run")
```

**After (BlendSpace2D):**
```gdscript
# Smooth blending between all animations
func _physics_process(delta):
    # Normalize velocity for blend position (-1 to 1)
    var blend_pos = velocity / max_speed
    animation_tree.set("parameters/Locomotion/blend_position", blend_pos)
```

**Generated BlendSpace2D:**
```ini
# BlendSpace2D resource
[sub_resource type="AnimationNodeBlendSpace2D" id="AnimationNodeBlendSpace2D_loco"]

# Center - Idle
blend_point_0/node = SubResource("AnimationNodeAnimation_idle")
blend_point_0/pos = Vector2(0, 0)

# Up - Walk North
blend_point_1/node = SubResource("AnimationNodeAnimation_walk_north")
blend_point_1/pos = Vector2(0, -1)

# Down - Walk South
blend_point_2/node = SubResource("AnimationNodeAnimation_walk_south")
blend_point_2/pos = Vector2(0, 1)

# Left - Walk West
blend_point_3/node = SubResource("AnimationNodeAnimation_walk_west")
blend_point_3/pos = Vector2(-1, 0)

# Right - Walk East
blend_point_4/node = SubResource("AnimationNodeAnimation_walk_east")
blend_point_4/pos = Vector2(1, 0)

# Diagonal blends (automatically interpolated)
blend_point_5/node = SubResource("AnimationNodeAnimation_walk_northeast")
blend_point_5/pos = Vector2(0.707, -0.707)

# Blend mode
blend_mode = 1  # BLEND_MODE_INTERPOLATED
min_space = Vector2(-1.5, -1.5)
max_space = Vector2(1.5, 1.5)
```

### BlendSpace2D Setup Script

```gdscript
# Programmatically create BlendSpace2D
func create_locomotion_blend_space() -> AnimationNodeBlendSpace2D:
    var blend_space = AnimationNodeBlendSpace2D.new()
    
    # Add idle animation at center
    var idle_node = AnimationNodeAnimation.new()
    idle_node.animation = "idle"
    blend_space.add_blend_point(idle_node, Vector2.ZERO)
    
    # Add directional walks
    var walk_north = AnimationNodeAnimation.new()
    walk_north.animation = "walk_north"
    blend_space.add_blend_point(walk_north, Vector2(0, -1))
    
    var walk_south = AnimationNodeAnimation.new()
    walk_south.animation = "walk_south"
    blend_space.add_blend_point(walk_south, Vector2(0, 1))
    
    var walk_east = AnimationNodeAnimation.new()
    walk_east.animation = "walk_east"
    blend_space.add_blend_point(walk_east, Vector2(1, 0))
    
    var walk_west = AnimationNodeAnimation.new()
    walk_west.animation = "walk_west"
    blend_space.add_blend_point(walk_west, Vector2(-1, 0))
    
    # Configure blend triangles for proper interpolation
    blend_space.add_triangle(0, 1, 4)  # Idle, North, East
    blend_space.add_triangle(0, 4, 2)  # Idle, East, South
    blend_space.add_triangle(0, 2, 3)  # Idle, South, West
    blend_space.add_triangle(0, 3, 1)  # Idle, West, North
    
    return blend_space
```

### Parameter-Driven Blend Space

```gdscript
# Update blend space based on input/velocity
func update_locomotion_blend():
    var input_dir = Input.get_vector("move_left", "move_right", "move_up", "move_down")
    
    # Calculate blend position based on input
    var blend_position = input_dir
    
    # Apply to AnimationTree
    animation_tree.set("parameters/Locomotion/blend_position", blend_position)
    
    # Also update speed scale for walk/run distinction
    var speed = velocity.length()
    var speed_scale = clamp(speed / base_speed, 0.5, 2.0)
    animation_tree.set("parameters/Locomotion/speed_scale", speed_scale)
```

## BlendSpace3D Configuration

### 3D Locomotion Blend Space

```ini
# BlendSpace3D for 3D characters
[sub_resource type="AnimationNodeBlendSpace3D" id="AnimationNodeBlendSpace3D_loco3d"]

# Idle at center
blend_point_0/node = SubResource("AnimationNodeAnimation_idle_3d")
blend_point_0/pos = Vector3(0, 0, 0)

# Cardinal directions
blend_point_1/node = SubResource("AnimationNodeAnimation_walk_forward")
blend_point_1/pos = Vector3(0, 0, 1)

blend_point_2/node = SubResource("AnimationNodeAnimation_walk_backward")
blend_point_2/pos = Vector3(0, 0, -1)

blend_point_3/node = SubResource("AnimationNodeAnimation_strafe_left")
blend_point_3/pos = Vector3(-1, 0, 0)

blend_point_4/node = SubResource("AnimationNodeAnimation_strafe_right")
blend_point_4/pos = Vector3(1, 0, 0)

# Run variants at higher magnitude
blend_point_5/node = SubResource("AnimationNodeAnimation_run_forward")
blend_point_5/pos = Vector3(0, 0, 1.5)
```

**3D Character Animation Script:**
```gdscript
# character_3d.gd
extends CharacterBody3D

@onready var animation_tree: AnimationTree = $AnimationTree

func _physics_process(delta):
    # Get local velocity relative to character rotation
    var local_velocity = transform.basis.inverse() * velocity
    
    # Normalize for blend position
    var blend_pos = Vector3(
        clamp(local_velocity.x / max_speed, -1, 1),
        0,
        clamp(local_velocity.z / max_speed, -1, 1)
    )
    
    # Update blend space
    animation_tree.set("parameters/Locomotion3D/blend_position", blend_pos)
    
    # Update animation speed based on actual velocity
    var speed_factor = velocity.length() / max_speed
    animation_tree.set("parameters/Locomotion3D/speed_scale", clamp(speed_factor, 0.5, 1.5))
```

## State Transitions

### Boolean Condition Transitions

```gdscript
# Setup boolean condition in AnimationTree
func setup_conditions():
    # Set condition values
    animation_tree.set("parameters/conditions/is_moving", velocity.length() > 0.1)
    animation_tree.set("parameters/conditions/is_attacking", Input.is_action_pressed("attack"))
    animation_tree.set("parameters/conditions/is_grounded", is_on_floor())
    animation_tree.set("parameters/conditions/is_dead", health <= 0)
```

**Corresponding Scene Configuration:**
```ini
[sub_resource type="AnimationNodeStateMachineTransition" id="AnimationNodeStateMachineTransition_idle_to_move"]
advance_mode = 1  # ADVANCE_MODE_AUTO
advance_condition = "is_moving"

[sub_resource type="AnimationNodeStateMachineTransition" id="AnimationNodeStateMachineTransition_move_to_idle"]
advance_mode = 1
advance_condition = "is_moving"
negated = true

[sub_resource type="AnimationNodeStateMachineTransition" id="AnimationNodeStateMachineTransition_attack"]
advance_mode = 1
advance_condition = "is_attacking"
```

### Expression-Based Transitions

```gdscript
# Godot 4.1+ expression transitions
# No need for manual condition setting

# Transition expression examples:
# "velocity.length() > 0.1"
# "health <= 0"
# "is_on_floor() and Input.is_action_pressed(\"jump\")"
# "anim_time >= 0.8" (requires anim_time parameter tracking)
```

**Setting up Expression Transitions:**
```gdscript
func create_expression_transition(expression: String) -> AnimationNodeStateMachineTransition:
    var transition = AnimationNodeStateMachineTransition.new()
    transition.advance_mode = AnimationNodeStateMachineTransition.ADVANCE_MODE_AUTO
    transition.advance_expression = expression
    return transition

# Usage
var jump_transition = create_expression_transition("is_on_floor() and Input.is_action_pressed('jump')")
state_machine.add_transition("Idle", "Jump", jump_transition)
```

### Time-Based Transitions

```gdscript
# Transition at end of animation
var end_transition = AnimationNodeStateMachineTransition.new()
end_transition.switch_mode = AnimationNodeStateMachineTransition.SWITCH_MODE_AT_END
end_transition.advance_mode = AnimationNodeStateMachineTransition.ADVANCE_MODE_AUTO

# Transition after specific time
var time_transition = AnimationNodeStateMachineTransition.new()
time_transition.switch_mode = AnimationNodeStateMachineTransition.SWITCH_MODE_AT_END
time_transition.advance_mode = AnimationNodeStateMachineTransition.ADVANCE_MODE_AUTO
# Add custom wait time via expression
```

## Blend Trees

### Complex Animation Mixing

**OneShot for Actions:**
```ini
[sub_resource type="AnimationNodeOneShot" id="AnimationNodeOneShot_attack"]
animation = SubResource("AnimationNodeAnimation_attack")
fadein_time = 0.1
fadeout_time = 0.15
mix_mode = 0  # ONE_SHOT_MIX_MODE_BLEND
```

**Blend2 for Smooth Transitions:**
```ini
[sub_resource type="AnimationNodeBlend2" id="AnimationNodeBlend2_action"]
```

**Add2 for Layering:**
```ini
[sub_resource type="AnimationNodeAdd2" id="AnimationNodeAdd2_recoil"]
# Adds recoil on top of base animation
```

**TimeScale for Speed Control:**
```ini
[sub_resource type="AnimationNodeTimeScale" id="AnimationNodeTimeScale_run"]
scale = 1.0  # Modified at runtime
```

### Complete Blend Tree Example

```ini
# Complex blend tree with layering
[sub_resource type="AnimationNodeBlendTree" id="AnimationNodeBlendTree_complex"]

# Input animations
nodes/Animation/node = SubResource("AnimationNodeAnimation_idle")
nodes/Animation/position = Vector2(100, 100)

# Time scale for speed control
nodes/TimeScale/node = SubResource("AnimationNodeTimeScale_var")
nodes/TimeScale/position = Vector2(300, 100)
nodes/TimeScale/input_0 = SubResource("AnimationNodeAnimation_idle")

# OneShot for hit reaction (layered on top)
nodes/HitReaction/node = SubResource("AnimationNodeOneShot_hit")
nodes/HitReaction/position = Vector2(500, 100)
nodes/HitReaction/input_0 = SubResource("AnimationNodeTimeScale_var")

# Add2 for weapon sway
nodes/WeaponSway/node = SubResource("AnimationNodeAdd2_sway")
nodes/WeaponSway/position = Vector2(700, 100)
nodes/WeaponSway/input_0 = SubResource("AnimationNodeOneShot_hit")
nodes/WeaponSway/input_1 = SubResource("AnimationNodeAnimation_sway")

# Output
nodes/Output/position = Vector2(900, 100)
node_connections = [&"output", 0, &"WeaponSway"]
```

**Blend Tree Script Control:**
```gdscript
# Control blend tree parameters
func update_blend_tree():
    # Update time scale based on movement speed
    var speed = velocity.length()
    var time_scale = clamp(speed / base_speed, 0.5, 2.0)
    animation_tree.set("parameters/TimeScale/scale", time_scale)
    
    # Trigger OneShot
    if is_hit:
        animation_tree.set("parameters/HitReaction/active", true)
        animation_tree.set("parameters/HitReaction/internal_active", true)
    
    # Control Add2 amount (0.0 = no sway, 1.0 = full sway)
    var sway_amount = clamp(speed / max_speed, 0.0, 1.0)
    animation_tree.set("parameters/WeaponSway/add_amount", sway_amount)
```

## Examples

### 2D Character Animation System

**Complete Setup:**
```gdscript
# character_animator.gd
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
@onready var playback: AnimationNodeStateMachinePlayback

@export var max_speed: float = 200.0
@export var blend_smoothness: float = 5.0

var target_blend_position: Vector2 = Vector2.ZERO
var current_blend_position: Vector2 = Vector2.ZERO

func _ready():
    animation_tree.active = true
    playback = animation_tree.get("parameters/playback")

func _physics_process(delta):
    # Get input
    var input_dir = Input.get_vector("move_left", "move_right", "move_up", "move_down")
    
    # Calculate target blend position
    if input_dir.length() > 0.1:
        target_blend_position = input_dir
        playback.travel("Locomotion")
    else:
        target_blend_position = Vector2.ZERO
        playback.travel("Idle")
    
    # Smooth blend position transition
    current_blend_position = current_blend_position.lerp(target_blend_position, blend_smoothness * delta)
    animation_tree.set("parameters/Locomotion/blend_position", current_blend_position)
    
    # Handle actions
    if Input.is_action_just_pressed("attack"):
        playback.travel("Attack")
    
    if Input.is_action_just_pressed("interact"):
        playback.travel("Interact")

func take_damage():
    playback.travel("Hit")

func die():
    playback.travel("Death")
```

**Generated Scene:**
```ini
# animated_character.tscn
[gd_scene load_steps=10 format=3]

[ext_resource type="Script" path="res://character_animator.gd" id="1_anim123"]

# Animation nodes
[sub_resource type="AnimationNodeAnimation" id="AnimationNodeAnimation_idle"]
animation = &"idle"

[sub_resource type="AnimationNodeAnimation" id="AnimationNodeAnimation_attack"]
animation = &"attack"

[sub_resource type="AnimationNodeBlendSpace2D" id="AnimationNodeBlendSpace2D_loco"]
blend_point_0/node = SubResource("AnimationNodeAnimation_idle")
blend_point_0/pos = Vector2(0, 0)
# ... more blend points

# State machine
[sub_resource type="AnimationNodeStateMachine" id="AnimationNodeStateMachine_main"]
states/Start/position = Vector2(150, 100)
states/Idle/node = SubResource("AnimationNodeAnimation_idle")
states/Idle/position = Vector2(300, 100)
states/Locomotion/node = SubResource("AnimationNodeBlendSpace2D_loco")
states/Locomotion/position = Vector2(500, 100)
states/Attack/node = SubResource("AnimationNodeAnimation_attack")
states/Attack/position = Vector2(500, 300)
states/End/position = Vector2(700, 100)

# Transitions
[sub_resource type="AnimationNodeStateMachineTransition" id="AnimationNodeStateMachineTransition_to_loco"]
advance_condition = "is_moving"

[sub_resource type="AnimationNodeStateMachineTransition" id="AnimationNodeStateMachineTransition_to_idle"]
advance_condition = "is_moving"
negated = true

[node name="AnimatedCharacter" type="CharacterBody2D"]
script = ExtResource("1_anim123")

[node name="Sprite2D" type="Sprite2D" parent="."]

[node name="AnimationPlayer" type="AnimationPlayer" parent="."]

[node name="AnimationTree" type="AnimationTree" parent="."]
anim_player = NodePath("../AnimationPlayer")
tree_root = SubResource("AnimationNodeStateMachine_main")
parameters/playback = SubResource("AnimationNodeStateMachinePlayback_main")
parameters/Locomotion/blend_position = Vector2(0, 0)
parameters/conditions/is_moving = false
```

### Combat Animation System

**Attack Combo System:**
```gdscript
# combat_animator.gd
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
@onready var playback: AnimationNodeStateMachinePlayback

var combo_count: int = 0
var max_combo: int = 3
var combo_window: float = 0.5
var combo_timer: float = 0.0

func _ready():
    animation_tree.active = true
    playback = animation_tree.get("parameters/playback")

func _physics_process(delta):
    # Update combo timer
    if combo_timer > 0:
        combo_timer -= delta
        if combo_timer <= 0:
            combo_count = 0
    
    # Handle attack input
    if Input.is_action_just_pressed("attack"):
        perform_attack()
    
    # Update animation conditions
    animation_tree.set("parameters/conditions/in_combo", combo_count > 0)

func perform_attack():
    match combo_count:
        0:
            playback.travel("Attack1")
        1:
            playback.travel("Attack2")
        2:
            playback.travel("Attack3")
        _:
            combo_count = 0
            playback.travel("Attack1")
    
    combo_count = (combo_count + 1) % max_combo
    combo_timer = combo_window

func reset_combo():
    combo_count = 0
    combo_timer = 0.0
```

**State Machine for Combos:**
```ini
[sub_resource type="AnimationNodeStateMachine" id="AnimationNodeStateMachine_combat"]
states/Idle/position = Vector2(300, 100)
states/Attack1/position = Vector2(500, 100)
states/Attack2/position = Vector2(500, 200)
states/Attack3/position = Vector2(500, 300)

# Attack1 -> Attack2 transition
[sub_resource type="AnimationNodeStateMachineTransition" id="AnimationNodeStateMachineTransition_a1_a2"]
switch_mode = 1  # SWITCH_MODE_AT_END
advance_mode = 1
advance_condition = "in_combo"

# Attack2 -> Attack3 transition
[sub_resource type="AnimationNodeStateMachineTransition" id="AnimationNodeStateMachineTransition_a2_a3"]
switch_mode = 1
advance_mode = 1
advance_condition = "in_combo"

# All attacks -> Idle (when combo ends)
[sub_resource type="AnimationNodeStateMachineTransition" id="AnimationNodeStateMachineTransition_end"]
switch_mode = 1
advance_mode = 1
negated = true
advance_condition = "in_combo"
```

### NPC Animation with Random Idle Variations

```gdscript
# npc_animator.gd
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
@onready var playback: AnimationNodeStateMachinePlayback

var idle_variations: Array[String] = ["Idle", "Idle2", "Idle3"]
var idle_timer: float = 0.0
var next_idle_change: float = 5.0

func _ready():
    animation_tree.active = true
    playback = animation_tree.get("parameters/playback")
    pick_random_idle()

func _physics_process(delta):
    # Random idle variation
    idle_timer += delta
    if idle_timer >= next_idle_change and velocity.length() < 0.1:
        idle_timer = 0.0
        next_idle_change = randf_range(3.0, 8.0)
        pick_random_idle()
    
    # Movement
    if velocity.length() > 0.1:
        playback.travel("Walk")

func pick_random_idle():
    var random_idle = idle_variations[randi() % idle_variations.size()]
    playback.travel(random_idle)
```

## Common Patterns

### Animation Event Integration

```gdscript
# Connect animation events to gameplay
func _ready():
    animation_tree.animation_started.connect(_on_animation_started)
    animation_tree.animation_finished.connect(_on_animation_finished)

func _on_animation_started(anim_name: StringName):
    match anim_name:
        "attack":
            # Disable movement during attack
            can_move = false
        "dash":
            # Make invincible
            is_invincible = true

func _on_animation_finished(anim_name: StringName):
    match anim_name:
        "attack":
            can_move = true
        "dash":
            is_invincible = false
```

### Animation-Driven Movement

```gdscript
# Root motion implementation
func _on_animation_tree_animation_started(anim_name: StringName):
    if anim_name == &"attack":
        # Enable root motion tracking
        animation_tree.set("parameters/Attack/active", true)

func _physics_process(delta):
    # Apply root motion from animation
    var root_motion: Transform3D = animation_tree.get_root_motion()
    global_transform *= root_motion
```

### Smooth State Transitions

```gdscript
# Crossfade duration configuration
var transition = AnimationNodeStateMachineTransition.new()
transition.fade_duration = 0.2  # 200ms crossfade
```

## Safety

- Always check if AnimationTree is active before accessing parameters
- Verify AnimationPlayer has all required animations before setting up tree
- Handle missing blend positions gracefully (default to center)
- Reset AnimationTree when reparenting or changing scenes
- Disconnect signals before queue_free()

## When NOT to Use

Don't use AnimationTree when:
- Only 2-3 simple animations (overkill)
- Animation logic is extremely simple (just play/stop)
- Performance is critical on low-end devices
- You need direct frame-by-frame control

Use direct AnimationPlayer instead:
```gdscript
# Simple animation control
func _physics_process(delta):
    if is_moving:
        anim_player.play("walk")
    else:
        anim_player.play("idle")
```

## Integration

Works with:
- **godot-add-signals** - Connect animation events to gameplay systems
- **godot-extract-to-scenes** - Create reusable animated character scenes
- **godot-setup-navigation** - Navigation agents with movement animations
- **godot-migrate-tilemap** - Animated tilemap characters

## Performance Tips

1. **Limit Blend Points** - 4-8 points is usually enough
2. **Cache Parameters** - Store parameter paths as constants
3. **Disable Unused Trees** - Set `active = false` when off-screen
4. **Use TimeScale** - Instead of changing animation speeds
5. **Batch Transitions** - Group state changes when possible

