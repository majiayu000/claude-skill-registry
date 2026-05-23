---
name: animation-system
description: Implements animation systems using AnimationPlayer, AnimationTree, blend trees, and procedural animation. Use when creating character animations and visual effects.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot Animation System

When implementing animations, use these patterns for smooth and responsive character movement.

## AnimationPlayer Basics

### Playing Animations
```gdscript
extends CharacterBody2D

@onready var anim_player: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
    # Connect to animation finished signal
    anim_player.animation_finished.connect(_on_animation_finished)

func play_animation(anim_name: String, speed: float = 1.0) -> void:
    if anim_player.current_animation != anim_name:
        anim_player.play(anim_name)
        anim_player.speed_scale = speed

func play_backwards(anim_name: String) -> void:
    anim_player.play_backwards(anim_name)

func stop_animation() -> void:
    anim_player.stop()

func pause_animation() -> void:
    anim_player.pause()

func resume_animation() -> void:
    anim_player.play()

func _on_animation_finished(anim_name: String) -> void:
    match anim_name:
        "attack":
            play_animation("idle")
        "death":
            queue_free()
```

### Animation Blending
```gdscript
extends AnimationPlayer

func crossfade_to(anim_name: String, duration: float = 0.2) -> void:
    if current_animation == anim_name:
        return

    # Queue the new animation with crossfade
    queue(anim_name)
    advance(0)  # Start immediately

    # Use AnimationPlayer's built-in blending
    set_blend_time(current_animation, anim_name, duration)

# Manual crossfade using AnimationTree is preferred for complex blending
```

### Animation Callbacks
```gdscript
extends CharacterBody2D

@onready var anim_player: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
    # Add method track call in animation
    # Or use animation_finished signal

    pass

# Called from animation track
func spawn_projectile() -> void:
    var projectile := preload("res://projectile.tscn").instantiate()
    projectile.global_position = $ProjectileSpawn.global_position
    get_parent().add_child(projectile)

func play_sound(sound_name: String) -> void:
    var sound := $Sounds.get_node(sound_name) as AudioStreamPlayer2D
    if sound:
        sound.play()

func enable_hitbox() -> void:
    $Hitbox/CollisionShape2D.disabled = false

func disable_hitbox() -> void:
    $Hitbox/CollisionShape2D.disabled = true
```

## AnimationTree

### State Machine Setup
```gdscript
extends CharacterBody2D

@onready var anim_tree: AnimationTree = $AnimationTree
@onready var state_machine: AnimationNodeStateMachinePlayback = \
    anim_tree.get("parameters/playback")

func _ready() -> void:
    anim_tree.active = true

func travel_to_state(state_name: String) -> void:
    state_machine.travel(state_name)

func force_state(state_name: String) -> void:
    state_machine.start(state_name)

func get_current_state() -> String:
    return state_machine.get_current_node()

func is_playing(state_name: String) -> bool:
    return state_machine.get_current_node() == state_name

func _physics_process(_delta: float) -> void:
    update_animation_state()

func update_animation_state() -> void:
    if not is_on_floor():
        if velocity.y < 0:
            travel_to_state("Jump")
        else:
            travel_to_state("Fall")
    elif velocity.length() > 10:
        travel_to_state("Run")
    else:
        travel_to_state("Idle")
```

### Blend Tree Setup
```gdscript
extends CharacterBody2D

@onready var anim_tree: AnimationTree = $AnimationTree

func _physics_process(_delta: float) -> void:
    update_blend_parameters()

func update_blend_parameters() -> void:
    # For BlendSpace2D (8-directional movement)
    var input := Input.get_vector("left", "right", "up", "down")
    anim_tree.set("parameters/Move/blend_position", input)

    # For BlendSpace1D (speed-based)
    var speed_ratio := velocity.length() / max_speed
    anim_tree.set("parameters/Speed/blend_position", speed_ratio)

    # For animation transitions
    anim_tree.set("parameters/conditions/is_jumping", not is_on_floor() and velocity.y < 0)
    anim_tree.set("parameters/conditions/is_falling", not is_on_floor() and velocity.y > 0)
    anim_tree.set("parameters/conditions/is_grounded", is_on_floor())
```

### One-Shot Animations
```gdscript
extends CharacterBody2D

@onready var anim_tree: AnimationTree = $AnimationTree

func play_attack() -> void:
    # Trigger one-shot animation
    anim_tree.set("parameters/Attack/request", AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE)

func abort_attack() -> void:
    anim_tree.set("parameters/Attack/request", AnimationNodeOneShot.ONE_SHOT_REQUEST_ABORT)

func is_attacking() -> bool:
    return anim_tree.get("parameters/Attack/active")

func _on_attack_finished() -> void:
    # Called when one-shot completes
    pass
```

### Layered Animations
```gdscript
# AnimationTree structure:
# - AnimationNodeBlendTree
#   - Add2 (blend lower and upper body)
#     - Input 0: State Machine (lower body: idle, walk, run)
#     - Input 1: State Machine (upper body: idle, aim, shoot)
#     - Filter: Upper body bones only

extends CharacterBody2D

@onready var anim_tree: AnimationTree = $AnimationTree

func _ready() -> void:
    # Set up bone filter for upper body layer
    # This is usually done in editor, but can be done in code
    pass

func update_animations() -> void:
    # Lower body follows movement
    var move_state := "idle" if velocity.length() < 10 else "run"
    anim_tree.set("parameters/LowerBody/playback").travel(move_state)

    # Upper body independent
    if is_aiming:
        anim_tree.set("parameters/UpperBody/playback").travel("aim")
    elif is_shooting:
        anim_tree.set("parameters/UpperBody/playback").travel("shoot")
    else:
        anim_tree.set("parameters/UpperBody/playback").travel("idle")

    # Blend amount
    anim_tree.set("parameters/Add2/add_amount", 1.0 if is_aiming else 0.0)
```

## Procedural Animation

### Look At / Head Tracking
```gdscript
extends Node3D

@export var head_bone: String = "Head"
@export var max_angle := 70.0
@export var look_speed := 5.0

var skeleton: Skeleton3D
var head_bone_idx: int
var target: Node3D

func _ready() -> void:
    skeleton = $Skeleton3D
    head_bone_idx = skeleton.find_bone(head_bone)

func _process(delta: float) -> void:
    if not target or head_bone_idx < 0:
        return

    var head_transform := skeleton.get_bone_global_pose(head_bone_idx)
    var head_position := skeleton.to_global(head_transform.origin)

    var target_direction := (target.global_position - head_position).normalized()
    var local_direction := skeleton.global_transform.basis.inverse() * target_direction

    # Calculate rotation to look at target
    var target_rotation := Quaternion(Vector3.FORWARD, local_direction)

    # Clamp rotation
    var angle := target_rotation.get_euler()
    angle.x = clamp(angle.x, deg_to_rad(-max_angle), deg_to_rad(max_angle))
    angle.y = clamp(angle.y, deg_to_rad(-max_angle), deg_to_rad(max_angle))

    var clamped_rotation := Quaternion.from_euler(angle)

    # Apply smooth rotation
    var current := skeleton.get_bone_pose_rotation(head_bone_idx)
    var new_rotation := current.slerp(clamped_rotation, look_speed * delta)

    skeleton.set_bone_pose_rotation(head_bone_idx, new_rotation)
```

### Procedural Walk Cycle
```gdscript
extends CharacterBody2D

@export var leg_length := 20.0
@export var step_height := 10.0
@export var step_duration := 0.3

@onready var left_foot: Node2D = $LeftFoot
@onready var right_foot: Node2D = $RightFoot

var left_foot_target: Vector2
var right_foot_target: Vector2
var step_progress := 0.0
var is_left_stepping := true

func _physics_process(delta: float) -> void:
    if velocity.length() > 10:
        update_procedural_walk(delta)
    else:
        reset_feet()

func update_procedural_walk(delta: float) -> void:
    step_progress += delta / step_duration

    if step_progress >= 1.0:
        step_progress = 0.0
        is_left_stepping = not is_left_stepping
        calculate_next_step()

    # Interpolate foot positions
    var stepping_foot := left_foot if is_left_stepping else right_foot
    var grounded_foot := right_foot if is_left_stepping else left_foot
    var target := left_foot_target if is_left_stepping else right_foot_target

    # Arc motion for stepping foot
    var t := step_progress
    var horizontal := stepping_foot.position.lerp(target, t)
    var vertical_offset := sin(t * PI) * step_height

    stepping_foot.position = horizontal + Vector2(0, -vertical_offset)

func calculate_next_step() -> void:
    var forward := velocity.normalized()
    var step_distance := velocity.length() * step_duration

    if is_left_stepping:
        left_foot_target = left_foot.position + forward * step_distance
    else:
        right_foot_target = right_foot.position + forward * step_distance
```

### Squash and Stretch
```gdscript
extends Sprite2D

@export var squash_amount := 0.3
@export var stretch_amount := 0.2
@export var return_speed := 10.0

var target_scale := Vector2.ONE

func squash() -> void:
    target_scale = Vector2(1 + squash_amount, 1 - squash_amount)

func stretch() -> void:
    target_scale = Vector2(1 - stretch_amount, 1 + stretch_amount)

func _process(delta: float) -> void:
    scale = scale.lerp(target_scale, return_speed * delta)
    target_scale = target_scale.lerp(Vector2.ONE, return_speed * delta)

# Usage with physics
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    var was_on_floor := is_on_floor()
    move_and_slide()

    # Landing squash
    if is_on_floor() and not was_on_floor:
        $Sprite2D.squash()

    # Jumping stretch
    if Input.is_action_just_pressed("jump") and is_on_floor():
        $Sprite2D.stretch()
```

### Screen Shake
```gdscript
extends Camera2D

var shake_amount := 0.0
var shake_decay := 5.0

func shake(amount: float, duration: float = 0.2) -> void:
    shake_amount = amount
    var tween := create_tween()
    tween.tween_property(self, "shake_amount", 0.0, duration)

func _process(delta: float) -> void:
    if shake_amount > 0:
        offset = Vector2(
            randf_range(-shake_amount, shake_amount),
            randf_range(-shake_amount, shake_amount)
        )
    else:
        offset = Vector2.ZERO
```

## Sprite Animation

### AnimatedSprite2D Controller
```gdscript
extends CharacterBody2D

@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D

func _physics_process(_delta: float) -> void:
    update_animation()
    update_facing()

func update_animation() -> void:
    if not is_on_floor():
        if velocity.y < 0:
            sprite.play("jump")
        else:
            sprite.play("fall")
    elif abs(velocity.x) > 10:
        sprite.play("run")
    else:
        sprite.play("idle")

func update_facing() -> void:
    if velocity.x > 0:
        sprite.flip_h = false
    elif velocity.x < 0:
        sprite.flip_h = true

func play_attack() -> void:
    sprite.play("attack")
    await sprite.animation_finished
    # Return to idle or movement animation
```

### Frame-Based Events
```gdscript
extends AnimatedSprite2D

signal attack_frame
signal step_frame

func _ready() -> void:
    frame_changed.connect(_on_frame_changed)

func _on_frame_changed() -> void:
    var current_anim := animation

    match current_anim:
        "attack":
            if frame == 3:  # Attack connects on frame 3
                attack_frame.emit()
        "run":
            if frame == 2 or frame == 6:  # Footstep frames
                step_frame.emit()
```

## Animation Tips

### Animation Speed Based on Movement
```gdscript
extends CharacterBody2D

@onready var anim_player: AnimationPlayer = $AnimationPlayer

@export var walk_speed := 100.0
@export var run_speed := 200.0

func _physics_process(_delta: float) -> void:
    var speed := velocity.length()

    if speed > 10:
        # Scale animation speed with movement speed
        var anim_speed := speed / walk_speed
        anim_player.speed_scale = clamp(anim_speed, 0.5, 2.0)
        anim_player.play("walk")
    else:
        anim_player.speed_scale = 1.0
        anim_player.play("idle")
```

### Root Motion
```gdscript
extends CharacterBody2D

@onready var anim_tree: AnimationTree = $AnimationTree

var root_motion_position := Vector2.ZERO

func _physics_process(delta: float) -> void:
    # Get root motion from animation
    var root_motion := anim_tree.get_root_motion_position()

    # Apply root motion as velocity
    if root_motion.length() > 0:
        velocity = Vector2(root_motion.x, root_motion.z) / delta
    else:
        # Normal movement when no root motion
        apply_movement_input()

    move_and_slide()
```

### Animation Retargeting
```gdscript
# When sharing animations between different skeletons
extends Skeleton3D

@export var source_skeleton: Skeleton3D
@export var bone_mapping: Dictionary  # {source_bone: target_bone}

func _process(_delta: float) -> void:
    if not source_skeleton:
        return

    for source_bone in bone_mapping:
        var target_bone: String = bone_mapping[source_bone]

        var source_idx := source_skeleton.find_bone(source_bone)
        var target_idx := find_bone(target_bone)

        if source_idx >= 0 and target_idx >= 0:
            var pose := source_skeleton.get_bone_pose(source_idx)
            set_bone_pose_rotation(target_idx, pose.basis.get_rotation_quaternion())
```
