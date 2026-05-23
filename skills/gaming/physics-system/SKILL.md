---
name: physics-system
description: Implements physics systems including RigidBody, collision detection, raycasting, joints, and custom physics behaviors. Use when building physics-driven gameplay.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot Physics System

When implementing physics-based gameplay, use these patterns for responsive and predictable physics.

## Physics Bodies

### RigidBody2D/3D Setup
```gdscript
extends RigidBody2D

@export var max_speed := 500.0
@export var push_force := 100.0

func _ready() -> void:
    # Physics material properties
    physics_material_override = PhysicsMaterial.new()
    physics_material_override.bounce = 0.5
    physics_material_override.friction = 0.8

    # Mass and gravity
    mass = 1.0
    gravity_scale = 1.0

    # Damping
    linear_damp = 0.1
    angular_damp = 0.1

    # Continuous collision detection for fast objects
    continuous_cd = RigidBody2D.CCD_MODE_CAST_RAY

func _physics_process(_delta: float) -> void:
    # Limit velocity
    if linear_velocity.length() > max_speed:
        linear_velocity = linear_velocity.normalized() * max_speed

func apply_impulse_toward(target: Vector2) -> void:
    var direction := (target - global_position).normalized()
    apply_central_impulse(direction * push_force)
```

### StaticBody with Moving Platform
```gdscript
extends StaticBody2D

@export var movement_speed := 100.0
@export var waypoints: Array[Marker2D]

var current_waypoint := 0
var velocity := Vector2.ZERO

func _physics_process(delta: float) -> void:
    if waypoints.is_empty():
        return

    var target := waypoints[current_waypoint].global_position
    var direction := (target - global_position).normalized()

    velocity = direction * movement_speed
    position += velocity * delta

    # Sync velocity for character riding platform
    constant_linear_velocity = velocity

    if global_position.distance_to(target) < 5:
        current_waypoint = (current_waypoint + 1) % waypoints.size()
```

### CharacterBody Physics Interactions
```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    # Apply movement
    move_and_slide()

    # Push RigidBodies
    for i in get_slide_collision_count():
        var collision := get_slide_collision(i)
        var collider := collision.get_collider()

        if collider is RigidBody2D:
            var push_direction := -collision.get_normal()
            var push_force := velocity.length() * 0.5
            collider.apply_central_impulse(push_direction * push_force)
```

## Collision Detection

### Area-Based Detection
```gdscript
extends Area2D

signal entity_entered(entity: Node2D)
signal entity_exited(entity: Node2D)

var entities_in_area: Array[Node2D] = []

func _ready() -> void:
    body_entered.connect(_on_body_entered)
    body_exited.connect(_on_body_exited)
    area_entered.connect(_on_area_entered)
    area_exited.connect(_on_area_exited)

func _on_body_entered(body: Node2D) -> void:
    if body.is_in_group("enemies"):
        entities_in_area.append(body)
        entity_entered.emit(body)

func _on_body_exited(body: Node2D) -> void:
    entities_in_area.erase(body)
    entity_exited.emit(body)

func _on_area_entered(area: Area2D) -> void:
    # For hitbox/hurtbox systems
    pass

func _on_area_exited(area: Area2D) -> void:
    pass

func get_closest_entity() -> Node2D:
    var closest: Node2D
    var closest_dist := INF

    for entity in entities_in_area:
        var dist := global_position.distance_to(entity.global_position)
        if dist < closest_dist:
            closest_dist = dist
            closest = entity

    return closest
```

### Hitbox/Hurtbox System
```gdscript
# hurtbox.gd
class_name Hurtbox
extends Area2D

signal hurt(hitbox: Hitbox, damage: float)

func _ready() -> void:
    collision_layer = 0
    collision_mask = 2  # Hitbox layer

# hitbox.gd
class_name Hitbox
extends Area2D

@export var damage := 10.0
@export var knockback_force := 200.0

var owner_node: Node2D

func _ready() -> void:
    collision_layer = 2
    collision_mask = 0  # Doesn't detect, only gets detected

    area_entered.connect(_on_area_entered)

func _on_area_entered(area: Area2D) -> void:
    if area is Hurtbox:
        area.hurt.emit(self, damage)

# Usage in character
extends CharacterBody2D

@onready var hurtbox: Hurtbox = $Hurtbox

func _ready() -> void:
    hurtbox.hurt.connect(_on_hurt)

func _on_hurt(hitbox: Hitbox, damage: float) -> void:
    health -= damage

    # Apply knockback
    var knockback_dir := (global_position - hitbox.global_position).normalized()
    velocity = knockback_dir * hitbox.knockback_force
```

## Raycasting

### Direct Raycast
```gdscript
extends Node2D

func raycast_to(target: Vector2) -> Dictionary:
    var space := get_world_2d().direct_space_state
    var query := PhysicsRayQueryParameters2D.create(
        global_position,
        target
    )

    # Configure query
    query.collision_mask = 1  # Specific layers
    query.collide_with_areas = true
    query.collide_with_bodies = true
    query.exclude = [self]  # Exclude self

    return space.intersect_ray(query)

func check_line_of_sight(target: Node2D) -> bool:
    var result := raycast_to(target.global_position)
    return result.is_empty() or result.collider == target

# 3D Raycast
func raycast_3d(from: Vector3, to: Vector3) -> Dictionary:
    var space := get_world_3d().direct_space_state
    var query := PhysicsRayQueryParameters3D.create(from, to)
    return space.intersect_ray(query)
```

### Shape Cast
```gdscript
extends Node2D

func sphere_cast(radius: float, direction: Vector2, distance: float) -> Array:
    var space := get_world_2d().direct_space_state

    var shape := CircleShape2D.new()
    shape.radius = radius

    var query := PhysicsShapeQueryParameters2D.new()
    query.shape = shape
    query.transform = global_transform
    query.motion = direction.normalized() * distance
    query.collision_mask = 1

    return space.intersect_shape(query)

func box_overlap(size: Vector2) -> Array:
    var space := get_world_2d().direct_space_state

    var shape := RectangleShape2D.new()
    shape.size = size

    var query := PhysicsShapeQueryParameters2D.new()
    query.shape = shape
    query.transform = global_transform
    query.collision_mask = 1

    return space.intersect_shape(query)
```

### Multiple Raycasts (Cone, Fan)
```gdscript
extends Node2D

@export var ray_count := 10
@export var ray_length := 200.0
@export var cone_angle := 60.0  # degrees

func cone_raycast() -> Array[Dictionary]:
    var results: Array[Dictionary] = []
    var space := get_world_2d().direct_space_state

    var half_angle := deg_to_rad(cone_angle / 2)
    var angle_step := cone_angle / (ray_count - 1)

    for i in range(ray_count):
        var angle := rotation - half_angle + deg_to_rad(angle_step * i)
        var direction := Vector2.from_angle(angle)
        var target := global_position + direction * ray_length

        var query := PhysicsRayQueryParameters2D.create(global_position, target)
        var result := space.intersect_ray(query)

        if not result.is_empty():
            results.append(result)

    return results
```

## Joints and Constraints

### Pin Joint (Hinge)
```gdscript
extends Node2D

func create_pin_joint(body_a: RigidBody2D, body_b: RigidBody2D, anchor: Vector2) -> PinJoint2D:
    var joint := PinJoint2D.new()
    joint.position = anchor
    joint.node_a = body_a.get_path()
    joint.node_b = body_b.get_path()

    # Optional: softness for some give
    joint.softness = 0.0

    add_child(joint)
    return joint
```

### Groove Joint (Slider)
```gdscript
extends Node2D

func create_groove_joint(body_a: RigidBody2D, body_b: RigidBody2D,
                         groove_start: Vector2, groove_end: Vector2) -> GrooveJoint2D:
    var joint := GrooveJoint2D.new()
    joint.node_a = body_a.get_path()
    joint.node_b = body_b.get_path()

    # Groove is relative to body_a
    joint.length = groove_start.distance_to(groove_end)
    joint.initial_offset = groove_start.distance_to(body_b.global_position)

    add_child(joint)
    return joint
```

### Damped Spring
```gdscript
extends Node2D

func create_spring(body_a: RigidBody2D, body_b: RigidBody2D,
                   rest_length: float, stiffness: float, damping: float) -> DampedSpringJoint2D:
    var joint := DampedSpringJoint2D.new()
    joint.node_a = body_a.get_path()
    joint.node_b = body_b.get_path()

    joint.rest_length = rest_length
    joint.stiffness = stiffness  # Spring constant
    joint.damping = damping      # Energy loss

    add_child(joint)
    return joint
```

### Rope/Chain Physics
```gdscript
extends Node2D

@export var segment_count := 10
@export var segment_length := 20.0
@export var segment_mass := 0.5

var segments: Array[RigidBody2D] = []

func create_rope(start: Vector2, end: Vector2) -> void:
    var direction := (end - start).normalized()

    for i in range(segment_count):
        var segment := create_segment()
        segment.position = start + direction * segment_length * i
        segments.append(segment)
        add_child(segment)

        if i > 0:
            # Connect to previous segment
            var joint := PinJoint2D.new()
            joint.node_a = segments[i - 1].get_path()
            joint.node_b = segment.get_path()
            joint.position = segment.position - direction * segment_length / 2
            add_child(joint)

func create_segment() -> RigidBody2D:
    var segment := RigidBody2D.new()
    segment.mass = segment_mass

    var shape := CapsuleShape2D.new()
    shape.radius = 3
    shape.height = segment_length

    var collision := CollisionShape2D.new()
    collision.shape = shape
    segment.add_child(collision)

    return segment

func attach_start(body: Node2D) -> void:
    if segments.is_empty():
        return

    var joint := PinJoint2D.new()
    joint.node_a = body.get_path()
    joint.node_b = segments[0].get_path()
    add_child(joint)
```

## Custom Physics

### Custom Gravity Zones
```gdscript
extends Area2D

@export var gravity_direction := Vector2.DOWN
@export var gravity_strength := 980.0
@export var priority := 0

func _ready() -> void:
    gravity_space_override = Area2D.SPACE_OVERRIDE_REPLACE
    gravity_direction = gravity_direction.normalized()
    gravity = gravity_strength

# Alternative: Manual gravity application
extends Area2D

func _physics_process(_delta: float) -> void:
    for body in get_overlapping_bodies():
        if body is RigidBody2D:
            # Override built-in gravity
            body.gravity_scale = 0
            body.apply_central_force(gravity_direction * gravity_strength * body.mass)
```

### Buoyancy
```gdscript
extends Area2D

@export var water_density := 1.0
@export var drag := 0.1

func _physics_process(_delta: float) -> void:
    for body in get_overlapping_bodies():
        if body is RigidBody2D:
            apply_buoyancy(body)

func apply_buoyancy(body: RigidBody2D) -> void:
    # Calculate submerged percentage
    var body_top := body.global_position.y - 20  # Approximate
    var body_bottom := body.global_position.y + 20
    var water_surface := global_position.y

    var submerged := 0.0
    if body_bottom > water_surface:
        if body_top > water_surface:
            submerged = 1.0
        else:
            submerged = (body_bottom - water_surface) / 40.0

    # Buoyancy force
    var buoyancy := water_density * submerged * 980.0 * body.mass
    body.apply_central_force(Vector2.UP * buoyancy)

    # Drag
    body.linear_velocity *= 1.0 - (drag * submerged)
```

### Wind Force
```gdscript
extends Area2D

@export var wind_direction := Vector2.RIGHT
@export var wind_strength := 100.0
@export var turbulence := 0.2

var time := 0.0

func _physics_process(delta: float) -> void:
    time += delta

    for body in get_overlapping_bodies():
        if body is RigidBody2D:
            apply_wind(body)

func apply_wind(body: RigidBody2D) -> void:
    # Add turbulence
    var turb := Vector2(
        sin(time * 3.0 + body.global_position.x * 0.1),
        cos(time * 2.0 + body.global_position.y * 0.1)
    ) * turbulence

    var force := (wind_direction.normalized() + turb) * wind_strength
    body.apply_central_force(force)
```

### Magnet/Attraction Force
```gdscript
extends Node2D

@export var attraction_strength := 500.0
@export var max_range := 200.0
@export var attract_layer := 2

func _physics_process(_delta: float) -> void:
    var space := get_world_2d().direct_space_state

    var shape := CircleShape2D.new()
    shape.radius = max_range

    var query := PhysicsShapeQueryParameters2D.new()
    query.shape = shape
    query.transform = global_transform
    query.collision_mask = attract_layer
    query.collide_with_bodies = true

    var results := space.intersect_shape(query)

    for result in results:
        var body := result.collider as RigidBody2D
        if body:
            attract_body(body)

func attract_body(body: RigidBody2D) -> void:
    var direction := global_position - body.global_position
    var distance := direction.length()

    if distance < 1:
        return

    # Inverse square law
    var force := attraction_strength / (distance * distance)
    force = min(force, attraction_strength)  # Cap force

    body.apply_central_force(direction.normalized() * force * body.mass)
```

## Physics Layers Best Practices

```gdscript
# Recommended layer setup:
# Layer 1: World/Environment
# Layer 2: Player
# Layer 3: Enemies
# Layer 4: Projectiles
# Layer 5: Pickups
# Layer 6: Triggers
# Layer 7: Hitboxes
# Layer 8: Hurtboxes

# Set in code
func setup_collision_layers(body: CollisionObject2D, layer_name: String) -> void:
    var layers := {
        "world": 1,
        "player": 2,
        "enemy": 3,
        "projectile": 4,
        "pickup": 5,
        "trigger": 6,
        "hitbox": 7,
        "hurtbox": 8
    }

    body.collision_layer = 1 << (layers[layer_name] - 1)

func setup_collision_mask(body: CollisionObject2D, detect_layers: Array[String]) -> void:
    var mask := 0
    for layer_name in detect_layers:
        var layer := layers.get(layer_name, 0)
        mask |= 1 << (layer - 1)

    body.collision_mask = mask

# Example: Enemy that collides with world and player, detects projectiles
func setup_enemy(enemy: CharacterBody2D) -> void:
    enemy.collision_layer = 1 << 2  # Layer 3 (enemy)
    enemy.collision_mask = (1 << 0) | (1 << 1) | (1 << 3)  # Layers 1, 2, 4
```
