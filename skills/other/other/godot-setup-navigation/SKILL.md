---
name: godot-setup-navigation
version: 1.0.0
displayName: Setup Navigation System
description: >
  Use when setting up NavigationServer API, creating NavigationRegion2D/3D scenes,
  generating NavigationPolygon from TileMap, configuring NavigationAgent2D/3D,
  implementing obstacle avoidance with RVO, or creating pathfinding integration
  patterns. Supports 2D top-down, 3D navigation, and TileMap-based navigation.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: advanced
audience: [developers]
keywords:
  - godot
  - navigation
  - pathfinding
  - navmesh
  - navigationagent
  - obstacle-avoidance
  - a-star
  - 2d
  - 3d
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".gd", ".tscn", ".tres", ".tilemap"]
    write: [".tscn", ".tres", ".gd"]
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "NavigationRegion2D/3D scenes, NavigationPolygon resources, NavigationAgent2D/3D configurations, pathfinding integration scripts, git commits"
requirements: "Git repository, Godot 4.x, NavigationServer API"
execution: "Fully automatic with scene generation and script updates"
integration: "Works with godot-migrate-tilemap for TileMap-based navigation"
---

# Setup Navigation System

## Core Principle

**Navigation is a service, not a component.** Use NavigationServer for runtime updates, NavigationRegion for static navmesh, and NavigationAgent for pathfinding requests. Avoid embedding navigation logic directly in character controllers.

## What This Skill Does

Sets up complete navigation systems:

1. **NavigationRegion2D/3D** - Creates navigation mesh boundaries
2. **NavigationPolygon** - Generates walkable areas from TileMap or geometry
3. **NavigationAgent2D/3D** - Configures pathfinding agents with obstacle avoidance
4. **RVO Integration** - Implements Reciprocal Velocity Obstacles for dynamic avoidance
5. **Pathfinding Integration** - Creates patterns for character movement, AI, and click-to-move

## Navigation System Setup

### NavigationRegion2D Configuration

**Before (Manual Setup):**
```gdscript
# No navigation setup - characters move blindly
extends CharacterBody2D

func _physics_process(delta):
    var input = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    velocity = input * 200
    move_and_slide()
```

**After (Navigation Region):**
```gdscript
# navigation_world.gd - Scene root with navigation
extends Node2D

@onready var navigation_region: NavigationRegion2D = $NavigationRegion2D

func _ready():
    # Bake navigation mesh after level loads
    await get_tree().process_frame
    navigation_region.bake_navigation_polygon()
```

**Generated Scene:**
```ini
# navigation_world.tscn
[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://navigation_world.gd" id="1_abc123"]

[sub_resource type="NavigationPolygon" id="NavigationPolygon_abc123"]
vertices = PackedVector2Array(0, 0, 1024, 0, 1024, 768, 0, 768)
polygons = [PackedInt32Array(0, 1, 2, 3)]
outlines = [PackedVector2Array(0, 0, 1024, 0, 1024, 768, 0, 768)]

[node name="NavigationWorld" type="Node2D"]
script = ExtResource("1_abc123")

[node name="NavigationRegion2D" type="NavigationRegion2D" parent="."]
navigation_polygon = SubResource("NavigationPolygon_abc123")
```

### NavigationRegion3D Configuration

```gdscript
# navigation_world_3d.gd
extends Node3D

@onready var navigation_region: NavigationRegion3D = $NavigationRegion3D

func _ready():
    # Bake 3D navigation mesh
    await get_tree().process_frame
    navigation_region.bake_navigation_mesh()
```

**Generated Scene:**
```ini
# navigation_world_3d.tscn
[gd_scene load_steps=3 format=3]

[ext_resource type="Script" path="res://navigation_world_3d.gd" id="1_abc123"]

[sub_resource type="NavigationMesh" id="NavigationMesh_abc123"]
vertices = PackedVector3Array(-10, 0, -10, 10, 0, -10, 10, 0, 10, -10, 0, 10)
polygons = [PackedInt32Array(0, 1, 2), PackedInt32Array(0, 2, 3)]
cell_size = 0.25
cell_height = 0.25
agent_radius = 0.5
agent_height = 2.0

[node name="NavigationWorld3D" type="Node3D"]
script = ExtResource("1_abc123")

[node name="NavigationRegion3D" type="NavigationRegion3D" parent="."]
navigation_mesh = SubResource("NavigationMesh_abc123")
```

### NavigationPolygon Generation

**From Geometry (2D):**
```gdscript
# Generates NavigationPolygon from StaticBody2D collision shapes
func generate_from_collision_shapes():
    var navigation_polygon = NavigationPolygon.new()
    var outline = PackedVector2Array()
    
    # Collect all collision polygon points
    for body in get_tree().get_nodes_in_group("navigation_obstacles"):
        if body is StaticBody2D:
            for child in body.get_children():
                if child is CollisionPolygon2D:
                    for point in child.polygon:
                        outline.append(body.to_global(point))
    
    # Create navigation mesh avoiding obstacles
    navigation_polygon.add_outline(outline)
    navigation_polygon.make_polygons_from_outlines()
    
    $NavigationRegion2D.navigation_polygon = navigation_polygon
    $NavigationRegion2D.bake_navigation_polygon()
```

### Baking Navigation Mesh

**Editor-time Baking:**
```gdscript
@tool
extends EditorScript

func _run():
    var nav_region = get_scene().find_child("NavigationRegion2D")
    if nav_region:
        nav_region.bake_navigation_polygon()
        print("Navigation mesh baked successfully")
```

**Runtime Baking:**
```gdscript
# For dynamic levels or procedural generation
func bake_dynamic_navigation():
    var navigation_polygon = NavigationPolygon.new()
    
    # Define walkable area
    var walkable_outline = PackedVector2Array([
        Vector2(0, 0),
        Vector2(1024, 0),
        Vector2(1024, 768),
        Vector2(0, 768)
    ])
    
    navigation_polygon.add_outline(walkable_outline)
    
    # Cut out obstacles
    for obstacle in obstacles:
        var obstacle_outline = PackedVector2Array()
        for point in obstacle.shape:
            obstacle_outline.append(obstacle.global_position + point)
        navigation_polygon.add_outline(obstacle_outline)
    
    navigation_polygon.make_polygons_from_outlines()
    $NavigationRegion2D.navigation_polygon = navigation_polygon
```

### Runtime Navigation Updates

**Using NavigationServer:**
```gdscript
# For frequent updates without rebaking
func update_navigation_obstacle(obstacle: CollisionShape2D, enabled: bool):
    var map_rid = NavigationServer2D.get_maps()[0]
    var obstacle_rid = obstacle.get_rid()
    
    if enabled:
        NavigationServer2D.obstacle_set_map(obstacle_rid, map_rid)
    else:
        NavigationServer2D.obstacle_set_map(obstacle_rid, RID())
    
    NavigationServer2D.map_force_update(map_rid)
```

## NavigationAgent Setup

### 2D Agent Configuration

**Before (Direct Movement):**
```gdscript
# enemy.gd - No pathfinding
extends CharacterBody2D

@export var target: Node2D
@export var speed: float = 100.0

func _physics_process(delta):
    if target:
        var direction = (target.global_position - global_position).normalized()
        velocity = direction * speed
        move_and_slide()
```

**After (NavigationAgent):**
```gdscript
# enemy.gd - With pathfinding
extends CharacterBody2D

@export var target: Node2D
@export var speed: float = 100.0

@onready var nav_agent: NavigationAgent2D = $NavigationAgent2D

func _ready():
    # Configure agent
    nav_agent.path_desired_distance = 10.0
    nav_agent.target_desired_distance = 10.0
    nav_agent.radius = 20.0
    nav_agent.max_speed = speed
    nav_agent.avoidance_enabled = true
    
    # Connect signals
    nav_agent.velocity_computed.connect(_on_velocity_computed)

func _physics_process(delta):
    if not target:
        return
    
    if nav_agent.is_navigation_finished():
        velocity = Vector2.ZERO
        return
    
    # Update target position
    nav_agent.target_position = target.global_position
    
    # Get next path position
    var next_path_position = nav_agent.get_next_path_position()
    var direction = (next_path_position - global_position).normalized()
    
    # Set velocity (navigation server will compute avoidance)
    nav_agent.velocity = direction * speed

func _on_velocity_computed(safe_velocity: Vector2):
    velocity = safe_velocity
    move_and_slide()
```

**Generated Scene:**
```ini
# enemy.tscn
[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://enemy.gd" id="1_abc123"]

[node name="Enemy" type="CharacterBody2D"]
script = ExtResource("1_abc123")

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("CircleShape2D_abc123")

[node name="NavigationAgent2D" type="NavigationAgent2D" parent="."]
path_desired_distance = 10.0
target_desired_distance = 10.0
radius = 20.0
max_speed = 100.0
avoidance_enabled = true
time_horizon = 5.0
path_postprocessing = 1
```

### 3D Agent Configuration

```gdscript
# enemy_3d.gd
extends CharacterBody3D

@export var target: Node3D
@export var speed: float = 5.0

@onready var nav_agent: NavigationAgent3D = $NavigationAgent3D

func _ready():
    nav_agent.path_desired_distance = 1.0
    nav_agent.target_desired_distance = 1.0
    nav_agent.radius = 0.5
    nav_agent.height = 2.0
    nav_agent.max_speed = speed
    nav_agent.avoidance_enabled = true
    nav_agent.velocity_computed.connect(_on_velocity_computed)

func _physics_process(delta):
    if not target or nav_agent.is_navigation_finished():
        velocity.x = 0
        velocity.z = 0
        return
    
    nav_agent.target_position = target.global_position
    var next_path_position = nav_agent.get_next_path_position()
    var direction = (next_path_position - global_position).normalized()
    
    nav_agent.velocity = direction * speed

func _on_velocity_computed(safe_velocity: Vector3):
    velocity.x = safe_velocity.x
    velocity.z = safe_velocity.z
    move_and_slide()
```

### Target Following

**Simple Follow:**
```gdscript
# follow_target.gd
extends CharacterBody2D

@export var target: Node2D
@export var follow_distance: float = 50.0

@onready var nav_agent: NavigationAgent2D = $NavigationAgent2D

func _physics_process(delta):
    if not target:
        return
    
    var distance_to_target = global_position.distance_to(target.global_position)
    
    if distance_to_target > follow_distance:
        nav_agent.target_position = target.global_position
        
        if not nav_agent.is_navigation_finished():
            var next_position = nav_agent.get_next_path_position()
            var direction = (next_position - global_position).normalized()
            velocity = direction * 100.0
            move_and_slide()
    else:
        velocity = Vector2.ZERO
```

**Predictive Following:**
```gdscript
# Predict where target will be
func get_predicted_target_position(look_ahead_time: float = 0.5) -> Vector2:
    if target is CharacterBody2D:
        return target.global_position + (target.velocity * look_ahead_time)
    return target.global_position
```

### Path Requests

**Manual Path Query:**
```gdscript
# Request path without NavigationAgent
func request_path(from: Vector2, to: Vector2) -> PackedVector2Array:
    var map_rid = NavigationServer2D.get_maps()[0]
    return NavigationServer2D.map_get_path(map_rid, from, to, true)

# Usage
var path = request_path(global_position, target_position)
for point in path:
    print("Path point: ", point)
```

**Path Query with Optimization:**
```gdscript
func request_optimized_path(from: Vector2, to: Vector2) -> PackedVector2Array:
    var map_rid = NavigationServer2D.get_maps()[0]
    
    # Query path with simplification
    var path = NavigationServer2D.map_get_path(
        map_rid, 
        from, 
        to, 
        true  # optimize path
    )
    
    return path
```

## Obstacle Avoidance

### Dynamic Obstacles

**Obstacle Node Setup:**
```gdscript
# dynamic_obstacle.gd
extends StaticBody2D

@export var obstacle_radius: float = 30.0

@onready var obstacle: NavigationObstacle2D = $NavigationObstacle2D

func _ready():
    obstacle.radius = obstacle_radius
    obstacle.velocity = Vector2.ZERO
    
    # Connect to avoidance signals
    obstacle.avoidance_enabled = true

func set_avoidance_velocity(velocity: Vector2):
    obstacle.velocity = velocity
```

**Generated Scene:**
```ini
# moving_obstacle.tscn
[node name="MovingObstacle" type="StaticBody2D"]

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("CircleShape2D_abc123")

[node name="NavigationObstacle2D" type="NavigationObstacle2D" parent="."]
radius = 30.0
avoidance_enabled = true
```

### RVO (Reciprocal Velocity Obstacles)

**RVO Configuration:**
```gdscript
# Configure RVO parameters for realistic avoidance
func configure_rvo(agent: NavigationAgent2D):
    agent.avoidance_enabled = true
    agent.radius = 20.0  # Agent size
    agent.neighbor_distance = 100.0  # How far to look for neighbors
    agent.max_neighbors = 10  # Max agents to consider
    agent.time_horizon = 2.0  # How far ahead to predict collisions
    agent.time_horizon_obstacles = 1.0  # How far ahead for static obstacles
```

**RVO with Priority:**
```gdscript
# Some agents have right of way
func configure_priority_agent(agent: NavigationAgent2D, priority: int):
    agent.avoidance_enabled = true
    agent.avoidance_layers = 1
    agent.avoidance_mask = 1
    
    # Higher priority agents push lower priority ones
    # Use time_horizon to control this
    match priority:
        0: agent.time_horizon = 1.0  # Low priority - yields quickly
        1: agent.time_horizon = 2.0  # Normal priority
        2: agent.time_horizon = 5.0  # High priority - others yield
```

### Navigation Layers

**Layer Configuration:**
```gdscript
# Define different navigation layers
enum NavigationLayers {
    GROUND = 1,
    WATER = 2,
    AIR = 4
}

# Configure agent for specific layers
func configure_agent_layers(agent: NavigationAgent2D, layers: int):
    agent.navigation_layers = layers

# Configure region for specific layers
func configure_region_layers(region: NavigationRegion2D, layers: int):
    region.navigation_layers = layers
```

**Layer-based Pathfinding:**
```gdscript
# Ground units only walk on ground
configure_agent_layers($GroundUnit/NavigationAgent2D, NavigationLayers.GROUND)

# Flying units can use air paths
configure_agent_layers($FlyingUnit/NavigationAgent2D, NavigationLayers.AIR)

# Amphibious units can use ground and water
configure_agent_layers($AmphibiousUnit/NavigationAgent2D, 
    NavigationLayers.GROUND | NavigationLayers.WATER)
```

## Integration Patterns

### Character Movement

**State Machine Integration:**
```gdscript
# character_controller.gd
extends CharacterBody2D

enum State { IDLE, MOVING, ATTACKING }

@onready var nav_agent: NavigationAgent2D = $NavigationAgent2D
var current_state: State = State.IDLE
var target_position: Vector2

func set_target(pos: Vector2):
    target_position = pos
    nav_agent.target_position = pos
    current_state = State.MOVING

func _physics_process(delta):
    match current_state:
        State.IDLE:
            velocity = Vector2.ZERO
            
        State.MOVING:
            if nav_agent.is_navigation_finished():
                current_state = State.IDLE
                velocity = Vector2.ZERO
            else:
                var next_pos = nav_agent.get_next_path_position()
                var direction = (next_pos - global_position).normalized()
                nav_agent.velocity = direction * 150.0
                
        State.ATTACKING:
            # Attack logic here
            pass
    
    if current_state == State.MOVING:
        move_and_slide()

func _on_velocity_computed(safe_velocity: Vector2):
    velocity = safe_velocity
```

### AI Pathfinding

**AI Controller with Navigation:**
```gdscript
# ai_controller.gd
extends CharacterBody2D

@export var patrol_points: Array[Marker2D]
@export var detection_range: float = 200.0

@onready var nav_agent: NavigationAgent2D = $NavigationAgent2D
@onready var vision: Area2D = $VisionArea

enum AIState { PATROL, CHASE, ATTACK, RETURN }

var current_state: AIState = AIState.PATROL
var current_patrol_index: int = 0
var home_position: Vector2
var target: Node2D

func _ready():
    home_position = global_position
    vision.body_entered.connect(_on_body_entered_vision)
    
    nav_agent.velocity_computed.connect(_on_velocity_computed)
    nav_agent.navigation_finished.connect(_on_navigation_finished)

func _physics_process(delta):
    match current_state:
        AIState.PATROL:
            process_patrol()
        AIState.CHASE:
            process_chase()
        AIState.ATTACK:
            process_attack()
        AIState.RETURN:
            process_return()

func process_patrol():
    if nav_agent.is_navigation_finished():
        current_patrol_index = (current_patrol_index + 1) % patrol_points.size()
        nav_agent.target_position = patrol_points[current_patrol_index].global_position
    
    var next_pos = nav_agent.get_next_path_position()
    var direction = (next_pos - global_position).normalized()
    nav_agent.velocity = direction * 80.0

func process_chase():
    if target:
        nav_agent.target_position = target.global_position
        var next_pos = nav_agent.get_next_path_position()
        var direction = (next_pos - global_position).normalized()
        nav_agent.velocity = direction * 150.0
        
        if global_position.distance_to(target.global_position) > detection_range * 1.5:
            current_state = AIState.RETURN

func process_return():
    nav_agent.target_position = home_position
    if nav_agent.is_navigation_finished():
        current_state = AIState.PATROL

func _on_body_entered_vision(body):
    if body.is_in_group("player"):
        target = body
        current_state = AIState.CHASE

func _on_velocity_computed(safe_velocity: Vector2):
    velocity = safe_velocity
    move_and_slide()
```

### Click-to-Move

**RTS-style Movement:**
```gdscript
# click_to_move.gd
extends CharacterBody2D

@export var speed: float = 150.0

@onready var nav_agent: NavigationAgent2D = $NavigationAgent2D
@onready var selection_indicator: Sprite2D = $SelectionIndicator

var is_selected: bool = false

func _ready():
    nav_agent.velocity_computed.connect(_on_velocity_computed)
    selection_indicator.visible = false

func _unhandled_input(event):
    if not is_selected:
        return
    
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
            var target = get_global_mouse_position()
            set_movement_target(target)

func set_movement_target(target: Vector2):
    nav_agent.target_position = target

func _physics_process(delta):
    if nav_agent.is_navigation_finished():
        velocity = Vector2.ZERO
        return
    
    var next_pos = nav_agent.get_next_path_position()
    var direction = (next_pos - global_position).normalized()
    nav_agent.velocity = direction * speed

func _on_velocity_computed(safe_velocity: Vector2):
    velocity = safe_velocity
    move_and_slide()

func select():
    is_selected = true
    selection_indicator.visible = true

func deselect():
    is_selected = false
    selection_indicator.visible = false
```

**Selection Manager:**
```gdscript
# selection_manager.gd
extends Node2D

var selected_units: Array[CharacterBody2D] = []

func _unhandled_input(event):
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
            if not Input.is_key_pressed(KEY_SHIFT):
                deselect_all()
            
            var click_pos = get_global_mouse_position()
            select_at_position(click_pos)
        
        elif event.button_index == MOUSE_BUTTON_RIGHT and event.pressed:
            var target_pos = get_global_mouse_position()
            move_selected_to(target_pos)

func select_at_position(pos: Vector2):
    var space_state = get_world_2d().direct_space_state
    var query = PhysicsPointQueryParameters2D.new()
    query.position = pos
    query.collide_with_areas = true
    
    var results = space_state.intersect_point(query)
    for result in results:
        var node = result.collider
        if node.has_method("select"):
            node.select()
            selected_units.append(node)

func deselect_all():
    for unit in selected_units:
        if is_instance_valid(unit) and unit.has_method("deselect"):
            unit.deselect()
    selected_units.clear()

func move_selected_to(target: Vector2):
    for unit in selected_units:
        if is_instance_valid(unit) and unit.has_method("set_movement_target"):
            unit.set_movement_target(target)
```

## Examples

### 2D Top-Down Navigation

**Complete Setup:**
```gdscript
# player_topdown.gd
extends CharacterBody2D

@export var speed: float = 200.0

@onready var nav_agent: NavigationAgent2D = $NavigationAgent2D

func _ready():
    nav_agent.path_desired_distance = 8.0
    nav_agent.target_desired_distance = 8.0
    nav_agent.radius = 12.0
    nav_agent.max_speed = speed
    nav_agent.avoidance_enabled = true
    nav_agent.velocity_computed.connect(_on_velocity_computed)

func _input(event):
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_RIGHT and event.pressed:
            nav_agent.target_position = get_global_mouse_position()

func _physics_process(delta):
    if nav_agent.is_navigation_finished():
        velocity = Vector2.ZERO
        return
    
    var next_pos = nav_agent.get_next_path_position()
    var direction = (next_pos - global_position).normalized()
    nav_agent.velocity = direction * speed

func _on_velocity_computed(safe_velocity: Vector2):
    velocity = safe_velocity
    move_and_slide()
```

**Scene Structure:**
```ini
# topdown_level.tscn
[gd_scene load_steps=4 format=3]

[sub_resource type="NavigationPolygon" id="NavigationPolygon_level"]
vertices = PackedVector2Array(0, 0, 1024, 0, 1024, 768, 0, 768)
polygons = [PackedInt32Array(0, 1, 2, 3)]

[sub_resource type="CircleShape2D" id="CircleShape2D_player"]
radius = 12.0

[node name="TopdownLevel" type="Node2D"]

[node name="NavigationRegion2D" type="NavigationRegion2D" parent="."]
navigation_polygon = SubResource("NavigationPolygon_level")

[node name="Player" type="CharacterBody2D" parent="."]
position = Vector2(512, 384)

[node name="CollisionShape2D" type="CollisionShape2D" parent="Player"]
shape = SubResource("CircleShape2D_player")

[node name="NavigationAgent2D" type="NavigationAgent2D" parent="Player"]
radius = 12.0
max_speed = 200.0
avoidance_enabled = true

[node name="Obstacles" type="Node2D" parent="."]

[node name="Wall1" type="StaticBody2D" parent="Obstacles"]

[node name="CollisionPolygon2D" type="CollisionPolygon2D" parent="Obstacles/Wall1"]
polygon = PackedVector2Array(200, 200, 300, 200, 300, 300, 200, 300)
```

### 3D Navigation

**3D Character Controller:**
```gdscript
# player_3d.gd
extends CharacterBody3D

@export var speed: float = 5.0
@export var jump_velocity: float = 4.5

@onready var nav_agent: NavigationAgent3D = $NavigationAgent3D
@onready var camera: Camera3D = $Camera3D

var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")

func _ready():
    nav_agent.path_desired_distance = 0.5
    nav_agent.target_desired_distance = 0.5
    nav_agent.radius = 0.3
    nav_agent.height = 1.8
    nav_agent.max_speed = speed
    nav_agent.avoidance_enabled = true
    nav_agent.velocity_computed.connect(_on_velocity_computed)

func _input(event):
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
            var mouse_pos = event.position
            var from = camera.project_ray_origin(mouse_pos)
            var to = from + camera.project_ray_normal(mouse_pos) * 1000
            
            var space_state = get_world_3d().direct_space_state
            var query = PhysicsRayQueryParameters3D.new()
            query.from = from
            query.to = to
            
            var result = space_state.intersect_ray(query)
            if result:
                nav_agent.target_position = result.position

func _physics_process(delta):
    if not is_on_floor():
        velocity.y -= gravity * delta
    
    if Input.is_action_just_pressed("ui_accept") and is_on_floor():
        velocity.y = jump_velocity
    
    if nav_agent.is_navigation_finished():
        velocity.x = 0
        velocity.z = 0
        return
    
    var next_pos = nav_agent.get_next_path_position()
    var direction = (next_pos - global_position).normalized()
    
    nav_agent.velocity = direction * speed

func _on_velocity_computed(safe_velocity: Vector3):
    velocity.x = safe_velocity.x
    velocity.z = safe_velocity.z
    move_and_slide()
```

### TileMap-Based Navigation

**Automatic Navigation Generation:**
```gdscript
# tilemap_navigation.gd
extends Node2D

@onready var tile_map: TileMap = $TileMap
@onready var navigation_region: NavigationRegion2D = $NavigationRegion2D

func _ready():
    generate_navigation_from_tilemap()

func generate_navigation_from_tilemap():
    var navigation_polygon = NavigationPolygon.new()
    var used_cells = tile_map.get_used_cells(0)  # Layer 0
    
    # Get tileset navigation polygons
    var tile_set = tile_map.tile_set
    
    for cell in used_cells:
        var atlas_coords = tile_map.get_cell_atlas_coords(0, cell)
        var tile_data = tile_map.get_cell_tile_data(0, cell)
        
        if tile_data and tile_data.get_navigation_polygon(0):
            var nav_poly = tile_data.get_navigation_polygon(0)
            var vertices = nav_poly.vertices
            
            # Transform vertices to world space
            var world_vertices = PackedVector2Array()
            for vertex in vertices:
                var world_pos = tile_map.map_to_local(cell) + vertex
                world_vertices.append(world_pos)
            
            # Add to navigation polygon
            navigation_polygon.add_polygon(world_vertices)
    
    navigation_region.navigation_polygon = navigation_polygon
    navigation_region.bake_navigation_polygon()
```

**Using TileMap V2 with Navigation Layers:**
```gdscript
# tilemap_v2_navigation.gd
extends Node2D

@onready var tile_map: TileMapLayer = $TileMapLayer
@onready var navigation_region: NavigationRegion2D = $NavigationRegion2D

func _ready():
    # For Godot 4.3+ TileMapLayer
    generate_navigation_from_layer()

func generate_navigation_from_layer():
    var navigation_polygon = NavigationPolygon.new()
    var used_cells = tile_map.get_used_cells()
    var tile_set = tile_map.tile_set
    
    for cell in used_cells:
        var tile_data = tile_map.get_cell_tile_data(cell)
        
        if tile_data:
            # Check if tile has navigation
            var nav_poly = tile_data.get_navigation_polygon()
            if nav_poly:
                var vertices = nav_poly.vertices
                var world_vertices = PackedVector2Array()
                
                for vertex in vertices:
                    var world_pos = tile_map.map_to_local(cell) + vertex
                    world_vertices.append(world_pos)
                
                navigation_polygon.add_outline(world_vertices)
    
    navigation_polygon.make_polygons_from_outlines()
    navigation_region.navigation_polygon = navigation_polygon
```

## TileMap Integration (from TileMap V2)

**Navigation-Enabled TileMap Setup:**
```gdscript
# Create a tileset with navigation polygons
func create_navigation_tileset() -> TileSet:
    var tile_set = TileSet.new()
    tile_set.tile_size = Vector2i(32, 32)
    
    # Add terrain atlas source
    var atlas_source = TileSetAtlasSource.new()
    atlas_source.texture = preload("res://assets/tiles.png")
    atlas_source.texture_region_size = Vector2i(32, 32)
    
    # Add ground tile with navigation
    var ground_atlas = Vector2i(0, 0)
    atlas_source.create_tile(ground_atlas)
    
    var ground_data = atlas_source.get_tile_data(ground_atlas, 0)
    var nav_poly = NavigationPolygon.new()
    nav_poly.vertices = PackedVector2Array([
        Vector2(0, 0), Vector2(32, 0), 
        Vector2(32, 32), Vector2(0, 32)
    ])
    nav_poly.add_polygon(PackedInt32Array([0, 1, 2, 3]))
    ground_data.set_navigation_polygon(0, nav_poly)
    
    # Add wall tile without navigation
    var wall_atlas = Vector2i(1, 0)
    atlas_source.create_tile(wall_atlas)
    # No navigation polygon = unwalkable
    
    tile_set.add_source(atlas_source, 0)
    return tile_set
```

**Runtime TileMap Navigation Update:**
```gdscript
# Update navigation when tiles change
func update_navigation_at_position(map_pos: Vector2i):
    # Remove old navigation data
    var nav_poly = NavigationPolygon.new()
    
    # Rebuild from current tilemap state
    var used_cells = tile_map.get_used_cells(0)
    
    for cell in used_cells:
        var tile_data = tile_map.get_cell_tile_data(0, cell)
        if tile_data and tile_data.get_navigation_polygon(0):
            var local_nav = tile_data.get_navigation_polygon(0)
            var world_verts = PackedVector2Array()
            
            for vert in local_nav.vertices:
                world_verts.append(tile_map.map_to_local(cell) + vert)
            
            nav_poly.add_outline(world_verts)
    
    nav_poly.make_polygons_from_outlines()
    navigation_region.navigation_polygon = nav_poly
```

## Common Patterns

### Multi-Agent Coordination
```gdscript
# Group movement with formation
func move_formation_to(target: Vector2, units: Array[CharacterBody2D]):
    var leader = units[0]
    leader.nav_agent.target_position = target
    
    # Other units follow with offsets
    for i in range(1, units.size()):
        var offset = Vector2(i * 30, 0)
        units[i].nav_agent.target_position = target + offset
```

### Dynamic Path Cost
```gdscript
# Different terrain costs
func calculate_path_cost(path: PackedVector2Array, terrain_map: TileMap) -> float:
    var cost = 0.0
    for i in range(path.size() - 1):
        var terrain_type = get_terrain_at(path[i], terrain_map)
        match terrain_type:
            "grass": cost += 1.0
            "mud": cost += 2.0
            "road": cost += 0.5
    return cost
```

### Navigation Debug Visualization
```gdscript
# Draw path for debugging
func _draw():
    if nav_agent.is_navigation_finished():
        return
    
    var path = nav_agent.get_current_navigation_path()
    if path.size() > 0:
        var local_path = PackedVector2Array()
        for point in path:
            local_path.append(to_local(point))
        
        draw_polyline(local_path, Color.GREEN, 2.0)
        
        for point in local_path:
            draw_circle(point, 3.0, Color.RED)
```

## Safety

- Always check `is_navigation_finished()` before accessing path
- Use `velocity_computed` signal for RVO avoidance
- Verify NavigationServer map exists before queries
- Handle cases where no path exists (agent returns empty path)
- Bake navigation after level generation completes

## When NOT to Use

Don't use NavigationAgent when:
- Movement is simple and direct (no obstacles)
- Performance is critical (NavigationServer has overhead)
- You need custom pathfinding algorithms (use A* directly)
- Agents don't need obstacle avoidance

Use direct movement instead:
```gdscript
# Simple direct movement - no navigation needed
func _physics_process(delta):
    var direction = (target.global_position - global_position).normalized()
    velocity = direction * speed
    move_and_slide()
```

## Integration

Works with:
- **godot-migrate-tilemap** - Convert TileMap V1 to V2 with navigation
- **godot-refactor** - Full project refactoring including navigation
- **godot-add-signals** - Connect navigation events via signals

## Performance Tips

1. **Batch Navigation Updates** - Don't bake every frame
2. **Use NavigationLayers** - Separate agents by layer for efficiency
3. **Limit Max Neighbors** - RVO performance scales with neighbor count
4. **Static vs Dynamic** - Use NavigationRegion for static, Obstacles for dynamic
5. **Path Caching** - Cache paths that don't change frequently

