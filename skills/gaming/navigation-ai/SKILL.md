---
name: navigation-ai
description: Implements AI navigation and pathfinding using NavigationServer, behavior systems, and steering behaviors. Use when building NPC movement and decision-making.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot Navigation & AI

When implementing AI movement and decision-making, use these patterns for intelligent NPC behavior.

## Navigation Basics

### NavigationAgent2D Setup
```gdscript
extends CharacterBody2D

@export var speed := 200.0
@onready var nav_agent: NavigationAgent2D = $NavigationAgent2D

func _ready() -> void:
    # Configure navigation agent
    nav_agent.path_desired_distance = 4.0
    nav_agent.target_desired_distance = 4.0
    nav_agent.avoidance_enabled = true

    # Wait for navigation map to be ready
    await get_tree().physics_frame
    set_movement_target(target_position)

func set_movement_target(target: Vector2) -> void:
    nav_agent.target_position = target

func _physics_process(_delta: float) -> void:
    if nav_agent.is_navigation_finished():
        return

    var next_position := nav_agent.get_next_path_position()
    var direction := global_position.direction_to(next_position)

    velocity = direction * speed
    move_and_slide()
```

### NavigationAgent3D Setup
```gdscript
extends CharacterBody3D

@export var speed := 5.0
@onready var nav_agent: NavigationAgent3D = $NavigationAgent3D

func _ready() -> void:
    nav_agent.path_desired_distance = 0.5
    nav_agent.target_desired_distance = 0.5
    nav_agent.avoidance_enabled = true
    nav_agent.radius = 0.5
    nav_agent.height = 2.0

func set_movement_target(target: Vector3) -> void:
    nav_agent.target_position = target

func _physics_process(_delta: float) -> void:
    if nav_agent.is_navigation_finished():
        return

    var next_position := nav_agent.get_next_path_position()
    var direction := global_position.direction_to(next_position)

    # Keep on ground plane
    direction.y = 0
    direction = direction.normalized()

    velocity = direction * speed

    # Rotate to face movement direction
    if direction.length() > 0.1:
        var target_rotation := atan2(direction.x, direction.z)
        rotation.y = lerp_angle(rotation.y, target_rotation, 0.1)

    move_and_slide()
```

### Dynamic Navigation Obstacles
```gdscript
extends Node3D

@onready var obstacle: NavigationObstacle3D = $NavigationObstacle3D

func _ready() -> void:
    # Configure obstacle
    obstacle.radius = 1.0
    obstacle.height = 2.0
    obstacle.avoidance_enabled = true

func open_door() -> void:
    # Disable obstacle when door opens
    obstacle.avoidance_enabled = false

func close_door() -> void:
    obstacle.avoidance_enabled = true
```

## Advanced Navigation

### Path Smoothing
```gdscript
extends CharacterBody2D

@onready var nav_agent: NavigationAgent2D = $NavigationAgent2D

var path: PackedVector2Array
var path_index := 0

func set_target(target: Vector2) -> void:
    nav_agent.target_position = target

    # Get raw path
    path = NavigationServer2D.map_get_path(
        nav_agent.get_navigation_map(),
        global_position,
        target,
        true  # optimize
    )

    # Smooth path
    path = smooth_path(path)
    path_index = 0

func smooth_path(raw_path: PackedVector2Array) -> PackedVector2Array:
    if raw_path.size() < 3:
        return raw_path

    var smoothed := PackedVector2Array()
    smoothed.append(raw_path[0])

    # Use Catmull-Rom spline interpolation
    for i in range(raw_path.size() - 1):
        var p0 := raw_path[max(i - 1, 0)]
        var p1 := raw_path[i]
        var p2 := raw_path[min(i + 1, raw_path.size() - 1)]
        var p3 := raw_path[min(i + 2, raw_path.size() - 1)]

        for t in range(1, 5):  # 4 subdivisions
            var point := catmull_rom(p0, p1, p2, p3, t / 5.0)
            smoothed.append(point)

    smoothed.append(raw_path[-1])
    return smoothed

func catmull_rom(p0: Vector2, p1: Vector2, p2: Vector2, p3: Vector2, t: float) -> Vector2:
    var t2 := t * t
    var t3 := t2 * t

    return 0.5 * (
        (2.0 * p1) +
        (-p0 + p2) * t +
        (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2 +
        (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3
    )
```

### Navigation Layers
```gdscript
extends CharacterBody2D

@onready var nav_agent: NavigationAgent2D = $NavigationAgent2D

# Navigation layers:
# Layer 1: Ground (all units)
# Layer 2: Flying (flying units only)
# Layer 3: Water (aquatic units only)

enum UnitType { GROUND, FLYING, AQUATIC }

func setup_navigation(unit_type: UnitType) -> void:
    match unit_type:
        UnitType.GROUND:
            nav_agent.navigation_layers = 1  # Only ground
        UnitType.FLYING:
            nav_agent.navigation_layers = 3  # Ground + Flying (1 + 2)
        UnitType.AQUATIC:
            nav_agent.navigation_layers = 5  # Ground + Water (1 + 4)
```

### Patrol System
```gdscript
extends CharacterBody2D

@export var patrol_points: Array[Marker2D]
@export var wait_time := 2.0

var current_patrol_index := 0
var is_waiting := false

@onready var nav_agent: NavigationAgent2D = $NavigationAgent2D
@onready var wait_timer: Timer = $WaitTimer

func _ready() -> void:
    wait_timer.wait_time = wait_time
    wait_timer.timeout.connect(_on_wait_finished)

    if patrol_points.size() > 0:
        move_to_patrol_point()

func move_to_patrol_point() -> void:
    var target := patrol_points[current_patrol_index].global_position
    nav_agent.target_position = target

func _physics_process(_delta: float) -> void:
    if is_waiting or nav_agent.is_navigation_finished():
        return

    var next_pos := nav_agent.get_next_path_position()
    velocity = global_position.direction_to(next_pos) * speed
    move_and_slide()

    # Check if reached patrol point
    if nav_agent.is_target_reached():
        is_waiting = true
        wait_timer.start()

func _on_wait_finished() -> void:
    is_waiting = false
    current_patrol_index = (current_patrol_index + 1) % patrol_points.size()
    move_to_patrol_point()
```

## Steering Behaviors

### Steering Behavior Base
```gdscript
class_name SteeringBehavior
extends RefCounted

var agent: CharacterBody2D
var weight := 1.0

func _init(a: CharacterBody2D, w: float = 1.0) -> void:
    agent = a
    weight = w

func calculate() -> Vector2:
    return Vector2.ZERO
```

### Seek and Flee
```gdscript
class_name SeekBehavior
extends SteeringBehavior

var target: Vector2

func calculate() -> Vector2:
    var desired := (target - agent.global_position).normalized() * agent.max_speed
    return (desired - agent.velocity) * weight

class_name FleeBehavior
extends SteeringBehavior

var threat: Vector2
var panic_distance := 200.0

func calculate() -> Vector2:
    var distance := agent.global_position.distance_to(threat)
    if distance > panic_distance:
        return Vector2.ZERO

    var desired := (agent.global_position - threat).normalized() * agent.max_speed
    return (desired - agent.velocity) * weight
```

### Arrival
```gdscript
class_name ArrivalBehavior
extends SteeringBehavior

var target: Vector2
var slowing_radius := 100.0

func calculate() -> Vector2:
    var to_target := target - agent.global_position
    var distance := to_target.length()

    if distance < 1:
        return -agent.velocity  # Stop

    var desired_speed: float
    if distance < slowing_radius:
        desired_speed = agent.max_speed * (distance / slowing_radius)
    else:
        desired_speed = agent.max_speed

    var desired := to_target.normalized() * desired_speed
    return (desired - agent.velocity) * weight
```

### Pursuit and Evade
```gdscript
class_name PursuitBehavior
extends SteeringBehavior

var target: CharacterBody2D

func calculate() -> Vector2:
    var to_target := target.global_position - agent.global_position
    var distance := to_target.length()

    # Predict future position
    var look_ahead := distance / agent.max_speed
    var future_position := target.global_position + target.velocity * look_ahead

    var desired := (future_position - agent.global_position).normalized() * agent.max_speed
    return (desired - agent.velocity) * weight

class_name EvadeBehavior
extends SteeringBehavior

var threat: CharacterBody2D
var panic_distance := 300.0

func calculate() -> Vector2:
    var to_threat := threat.global_position - agent.global_position
    var distance := to_threat.length()

    if distance > panic_distance:
        return Vector2.ZERO

    var look_ahead := distance / agent.max_speed
    var future_position := threat.global_position + threat.velocity * look_ahead

    var desired := (agent.global_position - future_position).normalized() * agent.max_speed
    return (desired - agent.velocity) * weight
```

### Obstacle Avoidance
```gdscript
class_name ObstacleAvoidanceBehavior
extends SteeringBehavior

var look_ahead := 100.0
var avoid_force := 50.0

func calculate() -> Vector2:
    if agent.velocity.length() < 0.1:
        return Vector2.ZERO

    var direction := agent.velocity.normalized()

    # Cast ray ahead
    var space := agent.get_world_2d().direct_space_state
    var query := PhysicsRayQueryParameters2D.create(
        agent.global_position,
        agent.global_position + direction * look_ahead
    )
    query.exclude = [agent]

    var result := space.intersect_ray(query)
    if result.is_empty():
        return Vector2.ZERO

    # Calculate avoidance
    var hit_point: Vector2 = result.position
    var hit_normal: Vector2 = result.normal

    return hit_normal * avoid_force * weight
```

### Flocking (Separation, Alignment, Cohesion)
```gdscript
class_name FlockingBehavior
extends SteeringBehavior

var neighbors: Array[CharacterBody2D]
var separation_radius := 50.0
var neighbor_radius := 100.0

var separation_weight := 1.5
var alignment_weight := 1.0
var cohesion_weight := 1.0

func set_neighbors(n: Array[CharacterBody2D]) -> void:
    neighbors = n

func calculate() -> Vector2:
    var separation := calculate_separation()
    var alignment := calculate_alignment()
    var cohesion := calculate_cohesion()

    return (separation * separation_weight +
            alignment * alignment_weight +
            cohesion * cohesion_weight) * weight

func calculate_separation() -> Vector2:
    var steering := Vector2.ZERO
    var count := 0

    for neighbor in neighbors:
        var distance := agent.global_position.distance_to(neighbor.global_position)
        if distance < separation_radius and distance > 0:
            var diff := agent.global_position - neighbor.global_position
            diff = diff.normalized() / distance
            steering += diff
            count += 1

    if count > 0:
        steering /= count
        steering = steering.normalized() * agent.max_speed
        steering -= agent.velocity

    return steering

func calculate_alignment() -> Vector2:
    var average_velocity := Vector2.ZERO
    var count := 0

    for neighbor in neighbors:
        var distance := agent.global_position.distance_to(neighbor.global_position)
        if distance < neighbor_radius:
            average_velocity += neighbor.velocity
            count += 1

    if count > 0:
        average_velocity /= count
        average_velocity = average_velocity.normalized() * agent.max_speed
        return average_velocity - agent.velocity

    return Vector2.ZERO

func calculate_cohesion() -> Vector2:
    var center := Vector2.ZERO
    var count := 0

    for neighbor in neighbors:
        var distance := agent.global_position.distance_to(neighbor.global_position)
        if distance < neighbor_radius:
            center += neighbor.global_position
            count += 1

    if count > 0:
        center /= count
        var desired := (center - agent.global_position).normalized() * agent.max_speed
        return desired - agent.velocity

    return Vector2.ZERO
```

### Steering Agent Controller
```gdscript
extends CharacterBody2D

@export var max_speed := 200.0
@export var max_force := 10.0

var behaviors: Array[SteeringBehavior] = []

func add_behavior(behavior: SteeringBehavior) -> void:
    behaviors.append(behavior)

func remove_behavior(behavior: SteeringBehavior) -> void:
    behaviors.erase(behavior)

func _physics_process(delta: float) -> void:
    var steering := Vector2.ZERO

    for behavior in behaviors:
        steering += behavior.calculate()

    # Limit force
    if steering.length() > max_force:
        steering = steering.normalized() * max_force

    # Apply steering
    velocity += steering * delta

    # Limit speed
    if velocity.length() > max_speed:
        velocity = velocity.normalized() * max_speed

    move_and_slide()
```

## AI Decision Making

### Simple FSM AI
```gdscript
extends CharacterBody2D

enum AIState { IDLE, PATROL, CHASE, ATTACK, FLEE }

var current_state: AIState = AIState.IDLE
var target: Node2D

@export var detection_range := 300.0
@export var attack_range := 50.0
@export var flee_health_threshold := 20.0

var health := 100.0

func _physics_process(delta: float) -> void:
    update_state()

    match current_state:
        AIState.IDLE:
            process_idle(delta)
        AIState.PATROL:
            process_patrol(delta)
        AIState.CHASE:
            process_chase(delta)
        AIState.ATTACK:
            process_attack(delta)
        AIState.FLEE:
            process_flee(delta)

func update_state() -> void:
    var player := find_player()

    if health < flee_health_threshold:
        change_state(AIState.FLEE)
        return

    if player:
        var distance := global_position.distance_to(player.global_position)

        if distance < attack_range:
            change_state(AIState.ATTACK)
        elif distance < detection_range:
            target = player
            change_state(AIState.CHASE)
    else:
        change_state(AIState.PATROL)

func change_state(new_state: AIState) -> void:
    if current_state == new_state:
        return

    # Exit current state
    match current_state:
        AIState.ATTACK:
            $AttackTimer.stop()

    current_state = new_state

    # Enter new state
    match new_state:
        AIState.ATTACK:
            $AttackTimer.start()
```

### Utility AI
```gdscript
class_name UtilityAI
extends Node

class Action:
    var name: String
    var considerations: Array[Consideration]

    func get_score() -> float:
        if considerations.is_empty():
            return 0.0

        var score := 1.0
        for consideration in considerations:
            score *= consideration.get_score()

        # Compensation factor for multiple considerations
        var mod := 1.0 - (1.0 / considerations.size())
        var make_up := (1.0 - score) * mod
        return score + (make_up * score)

class Consideration:
    var curve: Curve  # Response curve
    var input_func: Callable

    func get_score() -> float:
        var input := input_func.call()
        return curve.sample(input)

var actions: Array[Action] = []

func get_best_action() -> Action:
    var best_action: Action
    var best_score := -1.0

    for action in actions:
        var score := action.get_score()
        if score > best_score:
            best_score = score
            best_action = action

    return best_action

# Example setup
func setup_combat_ai(enemy: CharacterBody2D) -> void:
    var attack_action := Action.new()
    attack_action.name = "attack"

    # More likely to attack when:
    # - Target is close
    # - We have high health
    var distance_consideration := Consideration.new()
    distance_consideration.curve = preload("res://curves/distance_attack.tres")
    distance_consideration.input_func = func():
        return enemy.global_position.distance_to(target.global_position) / 500.0

    var health_consideration := Consideration.new()
    health_consideration.curve = preload("res://curves/health_attack.tres")
    health_consideration.input_func = func():
        return enemy.health / enemy.max_health

    attack_action.considerations = [distance_consideration, health_consideration]
    actions.append(attack_action)
```

## Line of Sight

### Raycast-Based Vision
```gdscript
extends CharacterBody2D

@export var view_distance := 300.0
@export var view_angle := 90.0  # Degrees

func can_see(target: Node2D) -> bool:
    var to_target := target.global_position - global_position
    var distance := to_target.length()

    # Check distance
    if distance > view_distance:
        return false

    # Check angle
    var facing := Vector2.from_angle(rotation)
    var angle := rad_to_deg(facing.angle_to(to_target.normalized()))
    if abs(angle) > view_angle / 2:
        return false

    # Check line of sight
    var space := get_world_2d().direct_space_state
    var query := PhysicsRayQueryParameters2D.create(
        global_position,
        target.global_position
    )
    query.exclude = [self]
    query.collision_mask = 1  # Walls layer

    var result := space.intersect_ray(query)
    if result.is_empty():
        return true

    # Check if we hit the target
    return result.collider == target

func get_visible_targets(group: String) -> Array[Node2D]:
    var visible: Array[Node2D] = []

    for node in get_tree().get_nodes_in_group(group):
        if node is Node2D and can_see(node):
            visible.append(node)

    return visible
```

### Vision Cone Visualization
```gdscript
extends Node2D

@export var view_distance := 300.0
@export var view_angle := 90.0
@export var cone_color := Color(1, 1, 0, 0.3)

func _draw() -> void:
    var half_angle := deg_to_rad(view_angle / 2)
    var points := PackedVector2Array()

    points.append(Vector2.ZERO)

    var segments := 20
    for i in range(segments + 1):
        var angle := -half_angle + (i / float(segments)) * view_angle * deg_to_rad(1)
        var point := Vector2(cos(angle), sin(angle)) * view_distance
        points.append(point)

    draw_colored_polygon(points, cone_color)
```
