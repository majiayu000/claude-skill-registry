---
name: godot-api-patterns
description: Provides Godot-specific API patterns, gotchas, best practices, and platform knowledge. Use when you need to understand Godot-specific behaviors and common pitfalls.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot API Patterns & Gotchas

When working with Godot APIs, be aware of these platform-specific behaviors and patterns.

## Common Gotchas

### Node Ready Order
```gdscript
# Children are ready BEFORE parents
# _ready() is called bottom-up in the tree

extends Node

func _ready() -> void:
    # Children are already ready here
    # Safe to access child nodes
    $ChildNode.do_something()

# But for siblings or parent references, use call_deferred
func _ready() -> void:
    call_deferred("_deferred_ready")

func _deferred_ready() -> void:
    # Now the entire tree is ready
    var sibling := get_parent().get_node("Sibling")
```

### @onready vs _ready()
```gdscript
# @onready runs BEFORE _ready()
# Use for node references that need to exist in _ready()

@onready var player: CharacterBody2D = $Player
@onready var health_bar: ProgressBar = $UI/HealthBar

func _ready() -> void:
    # player and health_bar are already set
    player.connect("health_changed", _on_health_changed)

# DON'T do this:
var player: CharacterBody2D  # Will be null in _ready()

func _ready() -> void:
    player = $Player  # Too late for other @onready vars that might need it
```

### Signal Connection Gotchas
```gdscript
# Connecting the same signal multiple times creates multiple calls
func _ready() -> void:
    # BAD: If _ready is called multiple times (scene reload)
    button.pressed.connect(_on_pressed)

# GOOD: Check or use CONNECT_ONE_SHOT
func _ready() -> void:
    if not button.pressed.is_connected(_on_pressed):
        button.pressed.connect(_on_pressed)

# Or use flags
button.pressed.connect(_on_pressed, CONNECT_ONE_SHOT)

# Disconnect on cleanup
func _exit_tree() -> void:
    if button.pressed.is_connected(_on_pressed):
        button.pressed.disconnect(_on_pressed)
```

### Process vs Physics Process
```gdscript
# _process: Variable timestep, every frame
# _physics_process: Fixed timestep (default 60Hz), before physics

# Use _physics_process for:
# - Movement that interacts with physics
# - Input that affects physics bodies
# - Anything that needs deterministic behavior

# Use _process for:
# - Visual updates (animations, particles)
# - UI updates
# - Non-physics game logic

func _physics_process(delta: float) -> void:
    # delta is constant (1/60 by default)
    velocity += gravity * delta
    move_and_slide()

func _process(delta: float) -> void:
    # delta varies based on frame rate
    $Sprite2D.rotation += spin_speed * delta
```

### Input Handling Priority
```gdscript
# Input flows: _input -> _gui_input -> _unhandled_input

func _input(event: InputEvent) -> void:
    # Called first, for all input
    # Call get_viewport().set_input_as_handled() to stop propagation
    pass

func _gui_input(event: InputEvent) -> void:
    # Only for Control nodes
    # Called after _input
    pass

func _unhandled_input(event: InputEvent) -> void:
    # Called if no GUI consumed the input
    # Best for game input
    if event.is_action_pressed("jump"):
        jump()

# Use _unhandled_key_input for keyboard shortcuts that shouldn't
# interfere with text input
func _unhandled_key_input(event: InputEvent) -> void:
    if event.is_action_pressed("pause"):
        toggle_pause()
```

### Dictionary and Array References
```gdscript
# Arrays and Dictionaries are passed by reference!

var original := [1, 2, 3]
var copy := original  # NOT a copy!
copy.append(4)
print(original)  # [1, 2, 3, 4] - original modified!

# Use duplicate() for actual copies
var actual_copy := original.duplicate()
actual_copy.append(5)
print(original)  # [1, 2, 3, 4] - unchanged

# Deep copy for nested structures
var nested := {"arr": [1, 2, 3]}
var deep_copy := nested.duplicate(true)
```

### Type Coercion
```gdscript
# Godot auto-converts some types, which can cause bugs

var health: int = 100
health = 50.5  # Becomes 50, silently truncated!

# Use explicit typing to catch errors
var health: int = 100
# health = 50.5  # Error in strict mode

# Be careful with Vector math
var pos := Vector2(10, 20)
pos.x = 5  # OK
# pos.x = 5.5 / 2  # Result is float, assigned to float component, OK
# But int division:
var result := 5 / 2  # = 2, not 2.5!
var result := 5.0 / 2  # = 2.5
```

## Scene Tree Patterns

### Safe Node Access
```gdscript
# get_node() crashes if node doesn't exist
var player := get_node("Player")  # Crashes if missing

# get_node_or_null() returns null
var player := get_node_or_null("Player")
if player:
    player.do_something()

# has_node() for checking
if has_node("Player"):
    var player := get_node("Player")

# For waiting on nodes
func _ready() -> void:
    # Waits with timeout
    var player := await get_tree().process_frame
    player = get_node_or_null("Player")
```

### Reparenting Nodes
```gdscript
# Moving nodes between parents

func reparent_node(node: Node, new_parent: Node) -> void:
    # Preserve global transform for Node2D/Node3D
    var global_pos: Variant

    if node is Node2D:
        global_pos = node.global_position
    elif node is Node3D:
        global_pos = node.global_transform

    # Reparent
    node.get_parent().remove_child(node)
    new_parent.add_child(node)

    # Restore global position
    if node is Node2D:
        node.global_position = global_pos
    elif node is Node3D:
        node.global_transform = global_pos

# Or use reparent() in Godot 4
func move_node(node: Node, new_parent: Node) -> void:
    node.reparent(new_parent, true)  # true = keep global transform
```

### Scene Instantiation
```gdscript
# Preload for compile-time loading
const PlayerScene := preload("res://player.tscn")

# load() for runtime loading
var enemy_scene := load("res://enemy.tscn") as PackedScene

# Instantiate and configure BEFORE adding to tree
func spawn_enemy(position: Vector2) -> Node2D:
    var enemy := enemy_scene.instantiate() as Node2D
    enemy.global_position = position
    enemy.set_meta("spawn_time", Time.get_ticks_msec())

    # Add to tree LAST
    add_child(enemy)
    return enemy

# For expensive instantiation, use threading
func spawn_enemies_async(count: int) -> void:
    for i in range(count):
        var enemy := enemy_scene.instantiate()
        # Configure...
        call_deferred("add_child", enemy)
        await get_tree().process_frame  # Spread across frames
```

## Resource Patterns

### Resource Sharing
```gdscript
# Resources are shared by default!
# All instances of a scene share the same resource

# In scene:
@export var material: Material

# Problem: Changing material affects ALL instances

# Solution 1: Make unique in code
func _ready() -> void:
    material = material.duplicate()

# Solution 2: Make unique in editor
# Enable "Local to Scene" on the resource

# Solution 3: Create new resource
func _ready() -> void:
    var new_material := StandardMaterial3D.new()
    new_material.albedo_color = Color.RED
    $MeshInstance3D.material_override = new_material
```

### Custom Resources
```gdscript
# item_data.gd
class_name ItemData
extends Resource

@export var name: String
@export var description: String
@export var icon: Texture2D
@export var value: int
@export var stackable: bool = true
@export var max_stack: int = 99

# Create in code
var sword := ItemData.new()
sword.name = "Iron Sword"
sword.value = 100

# Or create .tres files in editor and load
var sword: ItemData = preload("res://items/iron_sword.tres")
```

## Coroutines and Async

### Using await
```gdscript
# Wait for signal
func wait_for_player() -> void:
    await $Player.ready
    print("Player is ready!")

# Wait for time
func delayed_action() -> void:
    await get_tree().create_timer(2.0).timeout
    print("2 seconds passed!")

# Wait for tween
func animate() -> void:
    var tween := create_tween()
    tween.tween_property($Sprite, "modulate:a", 0.0, 1.0)
    await tween.finished
    $Sprite.queue_free()

# Wait for next frame
func spread_work() -> void:
    for i in range(1000):
        do_work(i)
        if i % 100 == 0:
            await get_tree().process_frame
```

### Callable Patterns
```gdscript
# Creating callables
var my_callable := Callable(self, "my_function")
var my_callable := my_function  # Shorthand

# Binding arguments
var bound := my_callable.bind(arg1, arg2)
bound.call()  # Calls my_function(arg1, arg2)

# Useful for signals
button.pressed.connect(handle_button.bind(button_id))

func handle_button(id: int) -> void:
    print("Button %d pressed" % id)

# Deferred calls
call_deferred("my_function", arg1)
my_callable.call_deferred()
```

## Common Patterns

### Singleton/Autoload Pattern
```gdscript
# game_manager.gd (add as Autoload named "GameManager")
extends Node

signal score_changed(new_score: int)

var score := 0
var high_score := 0

func add_score(points: int) -> void:
    score += points
    if score > high_score:
        high_score = score
    score_changed.emit(score)

func reset() -> void:
    score = 0

# Usage anywhere:
GameManager.add_score(100)
GameManager.score_changed.connect(_on_score_changed)
```

### Observer Pattern with Groups
```gdscript
# Add nodes to groups for broadcasting

# enemy.gd
func _ready() -> void:
    add_to_group("enemies")

func take_damage(amount: int) -> void:
    health -= amount

# game_manager.gd
func damage_all_enemies(amount: int) -> void:
    get_tree().call_group("enemies", "take_damage", amount)

# Or get all in group
func get_all_enemies() -> Array[Node]:
    return get_tree().get_nodes_in_group("enemies")
```

### State Pattern with Enums
```gdscript
enum State { IDLE, WALKING, JUMPING, ATTACKING }

var current_state: State = State.IDLE:
    set(value):
        if current_state != value:
            exit_state(current_state)
            current_state = value
            enter_state(current_state)

func enter_state(state: State) -> void:
    match state:
        State.IDLE:
            $AnimationPlayer.play("idle")
        State.WALKING:
            $AnimationPlayer.play("walk")
        State.JUMPING:
            velocity.y = jump_force
        State.ATTACKING:
            $AnimationPlayer.play("attack")

func exit_state(state: State) -> void:
    match state:
        State.ATTACKING:
            $Hitbox.disabled = true
```

## Performance Gotchas

### String Concatenation
```gdscript
# BAD: Creates many intermediate strings
var result := ""
for i in range(1000):
    result += str(i)  # Slow!

# GOOD: Use Array and join
var parts: Array[String] = []
for i in range(1000):
    parts.append(str(i))
var result := "".join(parts)

# Or use StringName for comparisons
var action: StringName = &"jump"
if event.is_action(action):  # Faster than string comparison
    pass
```

### Type Hints for Performance
```gdscript
# Type hints help the compiler optimize

# Slower (dynamic typing)
func process_items(items):
    for item in items:
        item.process()

# Faster (static typing)
func process_items(items: Array[Item]) -> void:
    for item: Item in items:
        item.process()
```

### Avoiding Allocation in Hot Paths
```gdscript
# BAD: Allocates every frame
func _process(delta: float) -> void:
    var direction := Vector2(
        Input.get_axis("left", "right"),
        Input.get_axis("up", "down")
    )

# GOOD: Reuse objects
var direction := Vector2.ZERO

func _process(delta: float) -> void:
    direction.x = Input.get_axis("left", "right")
    direction.y = Input.get_axis("up", "down")
```

## Debugging Tips

### Print Debugging
```gdscript
# Basic print
print("Value: ", value)

# Formatted print
print("Position: %s, Health: %d" % [position, health])

# Print to specific output
push_warning("This might be a problem")
push_error("This is definitely wrong")

# Print with stack trace
print_stack()

# Breakpoint in code
breakpoint  # Pauses execution in debugger
```

### Assertions
```gdscript
# Debug-only checks (stripped in release)
func set_health(value: int) -> void:
    assert(value >= 0, "Health cannot be negative")
    assert(value <= max_health, "Health exceeds maximum")
    health = value

# Check that runs in release too
func divide(a: float, b: float) -> float:
    if b == 0:
        push_error("Division by zero!")
        return 0
    return a / b
```
