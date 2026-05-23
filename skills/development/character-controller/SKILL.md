---
name: character-controller
description: Implements character movement systems using CharacterBody2D/3D, including platformer physics, 3D FPS controllers, and advanced movement mechanics. Use when building player or NPC movement.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot Character Controllers

When implementing character movement, follow these patterns for responsive and polished controllers.

## CharacterBody2D Platformer

### Basic Platformer Movement
```gdscript
extends CharacterBody2D

@export var speed := 300.0
@export var jump_velocity := -400.0
@export var gravity := 980.0

func _physics_process(delta: float) -> void:
    # Apply gravity
    if not is_on_floor():
        velocity.y += gravity * delta

    # Handle jump
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    # Get horizontal input
    var direction := Input.get_axis("move_left", "move_right")

    if direction:
        velocity.x = direction * speed
    else:
        velocity.x = move_toward(velocity.x, 0, speed)

    move_and_slide()
```

### Advanced Platformer with Coyote Time and Jump Buffering
```gdscript
extends CharacterBody2D

@export var speed := 300.0
@export var acceleration := 2000.0
@export var friction := 1500.0
@export var air_friction := 200.0
@export var jump_velocity := -400.0
@export var gravity := 980.0
@export var max_fall_speed := 600.0

# Coyote time (allows jumping shortly after leaving platform)
@export var coyote_time := 0.1
var coyote_timer := 0.0

# Jump buffering (registers jump input before landing)
@export var jump_buffer_time := 0.1
var jump_buffer_timer := 0.0

# Variable jump height
@export var jump_cut_multiplier := 0.5
var is_jumping := false

func _physics_process(delta: float) -> void:
    var was_on_floor := is_on_floor()

    # Coyote time
    if was_on_floor:
        coyote_timer = coyote_time
    else:
        coyote_timer -= delta

    # Jump buffer
    if Input.is_action_just_pressed("jump"):
        jump_buffer_timer = jump_buffer_time
    else:
        jump_buffer_timer -= delta

    # Apply gravity
    if not is_on_floor():
        velocity.y += gravity * delta
        velocity.y = min(velocity.y, max_fall_speed)

    # Handle jump
    if jump_buffer_timer > 0 and coyote_timer > 0:
        velocity.y = jump_velocity
        is_jumping = true
        jump_buffer_timer = 0
        coyote_timer = 0

    # Variable jump height - cut jump short if button released
    if is_jumping and not Input.is_action_pressed("jump") and velocity.y < 0:
        velocity.y *= jump_cut_multiplier
        is_jumping = false

    if is_on_floor():
        is_jumping = false

    # Horizontal movement with acceleration
    var direction := Input.get_axis("move_left", "move_right")

    if direction:
        velocity.x = move_toward(velocity.x, direction * speed, acceleration * delta)
    else:
        var current_friction = friction if is_on_floor() else air_friction
        velocity.x = move_toward(velocity.x, 0, current_friction * delta)

    move_and_slide()
```

### Wall Jump and Wall Slide
```gdscript
extends CharacterBody2D

@export var wall_slide_speed := 50.0
@export var wall_jump_velocity := Vector2(300, -350)
@export var wall_jump_time := 0.15  # Time player can't control after wall jump

var wall_jump_timer := 0.0
var wall_direction := 0

func _physics_process(delta: float) -> void:
    wall_jump_timer -= delta

    # Detect wall
    wall_direction = 0
    if is_on_wall():
        wall_direction = get_wall_normal().x

    # Wall slide
    if is_on_wall() and not is_on_floor() and velocity.y > 0:
        velocity.y = min(velocity.y, wall_slide_speed)

    # Wall jump
    if Input.is_action_just_pressed("jump") and is_on_wall() and not is_on_floor():
        velocity = Vector2(wall_direction * wall_jump_velocity.x, wall_jump_velocity.y)
        wall_jump_timer = wall_jump_time

    # Normal movement (disabled briefly after wall jump)
    if wall_jump_timer <= 0:
        var direction := Input.get_axis("move_left", "move_right")
        if direction:
            velocity.x = direction * speed

    # Apply gravity and move
    if not is_on_floor():
        velocity.y += gravity * delta

    move_and_slide()
```

### Dash Mechanic
```gdscript
extends CharacterBody2D

@export var dash_speed := 800.0
@export var dash_duration := 0.15
@export var dash_cooldown := 0.5

var is_dashing := false
var dash_timer := 0.0
var dash_cooldown_timer := 0.0
var dash_direction := Vector2.ZERO

func _physics_process(delta: float) -> void:
    dash_cooldown_timer -= delta

    # Start dash
    if Input.is_action_just_pressed("dash") and dash_cooldown_timer <= 0 and not is_dashing:
        start_dash()

    # During dash
    if is_dashing:
        dash_timer -= delta
        velocity = dash_direction * dash_speed

        if dash_timer <= 0:
            is_dashing = false
            velocity = dash_direction * speed  # Keep some momentum
    else:
        # Normal movement
        apply_normal_movement(delta)

    move_and_slide()

func start_dash() -> void:
    is_dashing = true
    dash_timer = dash_duration
    dash_cooldown_timer = dash_cooldown

    # Get dash direction from input or facing direction
    var input_dir := Vector2(
        Input.get_axis("move_left", "move_right"),
        Input.get_axis("move_up", "move_down")
    )

    if input_dir != Vector2.ZERO:
        dash_direction = input_dir.normalized()
    else:
        dash_direction = Vector2.RIGHT if $Sprite2D.flip_h == false else Vector2.LEFT
```

## CharacterBody3D Controllers

### First Person Controller
```gdscript
extends CharacterBody3D

@export var speed := 5.0
@export var sprint_speed := 8.0
@export var jump_velocity := 4.5
@export var mouse_sensitivity := 0.002

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")

@onready var head: Node3D = $Head
@onready var camera: Camera3D = $Head/Camera3D

func _ready() -> void:
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
        # Rotate head (up/down)
        head.rotate_x(-event.relative.y * mouse_sensitivity)
        head.rotation.x = clamp(head.rotation.x, deg_to_rad(-90), deg_to_rad(90))

        # Rotate body (left/right)
        rotate_y(-event.relative.x * mouse_sensitivity)

    if event.is_action_pressed("ui_cancel"):
        Input.mouse_mode = Input.MOUSE_MODE_VISIBLE

func _physics_process(delta: float) -> void:
    # Gravity
    if not is_on_floor():
        velocity.y -= gravity * delta

    # Jump
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    # Movement
    var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

    var current_speed := sprint_speed if Input.is_action_pressed("sprint") else speed

    if direction:
        velocity.x = direction.x * current_speed
        velocity.z = direction.z * current_speed
    else:
        velocity.x = move_toward(velocity.x, 0, current_speed)
        velocity.z = move_toward(velocity.z, 0, current_speed)

    move_and_slide()
```

### Third Person Controller
```gdscript
extends CharacterBody3D

@export var speed := 5.0
@export var sprint_speed := 8.0
@export var jump_velocity := 4.5
@export var rotation_speed := 10.0

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")
var target_rotation := 0.0

@onready var camera_pivot: Node3D = $CameraPivot
@onready var spring_arm: SpringArm3D = $CameraPivot/SpringArm3D
@onready var model: Node3D = $Model

func _physics_process(delta: float) -> void:
    # Gravity
    if not is_on_floor():
        velocity.y -= gravity * delta

    # Jump
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    # Get input direction relative to camera
    var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")

    # Transform input to camera space
    var camera_basis := camera_pivot.global_transform.basis
    var direction := (camera_basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
    direction.y = 0
    direction = direction.normalized()

    var current_speed := sprint_speed if Input.is_action_pressed("sprint") else speed

    if direction:
        velocity.x = direction.x * current_speed
        velocity.z = direction.z * current_speed

        # Rotate model to face movement direction
        target_rotation = atan2(direction.x, direction.z)
        model.rotation.y = lerp_angle(model.rotation.y, target_rotation, rotation_speed * delta)
    else:
        velocity.x = move_toward(velocity.x, 0, current_speed)
        velocity.z = move_toward(velocity.z, 0, current_speed)

    move_and_slide()
```

### Smooth Camera Follow
```gdscript
extends Node3D

@export var target: Node3D
@export var offset := Vector3(0, 2, 5)
@export var follow_speed := 5.0
@export var rotation_speed := 3.0
@export var mouse_sensitivity := 0.003

var camera_rotation := Vector2.ZERO

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
        camera_rotation.x -= event.relative.y * mouse_sensitivity
        camera_rotation.y -= event.relative.x * mouse_sensitivity
        camera_rotation.x = clamp(camera_rotation.x, deg_to_rad(-80), deg_to_rad(80))

func _physics_process(delta: float) -> void:
    if not target:
        return

    # Calculate desired position
    var target_pos := target.global_position

    # Apply rotation
    var offset_rotated := offset.rotated(Vector3.UP, camera_rotation.y)
    offset_rotated = offset_rotated.rotated(Vector3.RIGHT, camera_rotation.x)

    var desired_position := target_pos + offset_rotated

    # Smoothly interpolate position
    global_position = global_position.lerp(desired_position, follow_speed * delta)

    # Look at target
    look_at(target_pos, Vector3.UP)
```

## Movement State Machine

### State-Based Character Controller
```gdscript
extends CharacterBody2D

enum State { IDLE, RUN, JUMP, FALL, WALL_SLIDE, DASH }

var current_state: State = State.IDLE

@export var speed := 300.0
@export var jump_velocity := -400.0
@export var gravity := 980.0

func _physics_process(delta: float) -> void:
    match current_state:
        State.IDLE:
            process_idle(delta)
        State.RUN:
            process_run(delta)
        State.JUMP:
            process_jump(delta)
        State.FALL:
            process_fall(delta)
        State.WALL_SLIDE:
            process_wall_slide(delta)
        State.DASH:
            process_dash(delta)

    move_and_slide()

func change_state(new_state: State) -> void:
    # Exit current state
    match current_state:
        State.DASH:
            exit_dash()

    current_state = new_state

    # Enter new state
    match new_state:
        State.JUMP:
            enter_jump()
        State.DASH:
            enter_dash()

func process_idle(delta: float) -> void:
    apply_gravity(delta)
    velocity.x = move_toward(velocity.x, 0, speed * delta * 10)

    if not is_on_floor():
        change_state(State.FALL)
    elif Input.is_action_just_pressed("jump"):
        change_state(State.JUMP)
    elif Input.get_axis("move_left", "move_right") != 0:
        change_state(State.RUN)

func process_run(delta: float) -> void:
    apply_gravity(delta)

    var direction := Input.get_axis("move_left", "move_right")
    velocity.x = direction * speed

    if not is_on_floor():
        change_state(State.FALL)
    elif Input.is_action_just_pressed("jump"):
        change_state(State.JUMP)
    elif direction == 0:
        change_state(State.IDLE)

func apply_gravity(delta: float) -> void:
    if not is_on_floor():
        velocity.y += gravity * delta
```

## Input Handling Best Practices

### Input Buffer System
```gdscript
class_name InputBuffer
extends RefCounted

var buffer: Dictionary = {}
var buffer_times: Dictionary = {}

func _init() -> void:
    pass

func update(delta: float) -> void:
    for action in buffer_times.keys():
        buffer_times[action] -= delta
        if buffer_times[action] <= 0:
            buffer.erase(action)
            buffer_times.erase(action)

func add(action: String, duration: float = 0.1) -> void:
    buffer[action] = true
    buffer_times[action] = duration

func consume(action: String) -> bool:
    if buffer.has(action):
        buffer.erase(action)
        buffer_times.erase(action)
        return true
    return false

func has(action: String) -> bool:
    return buffer.has(action)
```

### Action Queuing
```gdscript
extends CharacterBody2D

var action_queue: Array[String] = []
var max_queue_size := 3

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("attack"):
        queue_action("attack")
    elif event.is_action_pressed("special"):
        queue_action("special")

func queue_action(action: String) -> void:
    if action_queue.size() < max_queue_size:
        action_queue.append(action)

func process_action_queue() -> void:
    if action_queue.is_empty():
        return

    var next_action := action_queue[0]

    if can_perform_action(next_action):
        action_queue.pop_front()
        perform_action(next_action)

func can_perform_action(action: String) -> bool:
    # Check if current state allows this action
    return true

func perform_action(action: String) -> void:
    match action:
        "attack":
            do_attack()
        "special":
            do_special()
```

## Common Gotchas

### Floor Detection
```gdscript
# is_on_floor() is only valid AFTER move_and_slide()
func _physics_process(delta: float) -> void:
    # BAD: Checking before move_and_slide
    # if is_on_floor():  # This is stale from last frame

    move_and_slide()

    # GOOD: Check after move_and_slide
    if is_on_floor():
        # This is current
        pass

# For immediate floor check without moving
func is_grounded() -> bool:
    return test_move(global_transform, Vector3.DOWN * 0.1)
```

### Snapping to Slopes
```gdscript
extends CharacterBody3D

func _physics_process(delta: float) -> void:
    # Enable floor snapping for slopes
    floor_snap_length = 0.5 if is_on_floor() else 0.0

    # Adjust floor max angle for steep slopes
    floor_max_angle = deg_to_rad(45)

    move_and_slide()
```

### Delta Independence
```gdscript
# BAD: Frame-dependent movement
velocity.x += 10  # Faster at higher FPS

# GOOD: Delta-independent movement
velocity.x += acceleration * delta

# For velocity-based movement with move_and_slide
# velocity is already handled correctly by move_and_slide
velocity.x = speed  # This is fine, move_and_slide handles delta
```
