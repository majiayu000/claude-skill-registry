---
name: vfx-particles
description: Implements visual effects using GPUParticles, trails, screen effects, and procedural VFX. Use when creating particle systems and visual feedback.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot VFX & Particles

When implementing visual effects, use these patterns for impactful and performant VFX.

## GPU Particles

### Basic Particle Setup
```gdscript
extends GPUParticles2D

func setup_explosion() -> void:
    amount = 50
    lifetime = 1.0
    one_shot = true
    explosiveness = 1.0
    emitting = false

    var material := ParticleProcessMaterial.new()

    # Emission
    material.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_SPHERE
    material.emission_sphere_radius = 5.0

    # Direction
    material.direction = Vector3(0, -1, 0)
    material.spread = 180.0

    # Velocity
    material.initial_velocity_min = 100.0
    material.initial_velocity_max = 200.0

    # Gravity
    material.gravity = Vector3(0, 200, 0)

    # Scale
    material.scale_min = 0.5
    material.scale_max = 1.5
    material.scale_curve = create_scale_curve()

    # Color
    material.color = Color.ORANGE
    material.color_ramp = create_color_gradient()

    process_material = material

func create_scale_curve() -> Curve:
    var curve := Curve.new()
    curve.add_point(Vector2(0, 1))
    curve.add_point(Vector2(1, 0))
    return curve

func create_color_gradient() -> Gradient:
    var gradient := Gradient.new()
    gradient.set_color(0, Color.WHITE)
    gradient.add_point(0.3, Color.YELLOW)
    gradient.add_point(0.6, Color.ORANGE)
    gradient.set_color(1, Color(1, 0, 0, 0))
    return gradient

func play() -> void:
    restart()
    emitting = true
```

### 3D Particles
```gdscript
extends GPUParticles3D

func setup_fire() -> void:
    amount = 100
    lifetime = 2.0
    preprocess = 1.0  # Pre-warm

    var material := ParticleProcessMaterial.new()

    # Emission from mesh surface
    material.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_BOX
    material.emission_box_extents = Vector3(0.5, 0.1, 0.5)

    # Upward motion
    material.direction = Vector3(0, 1, 0)
    material.spread = 15.0
    material.initial_velocity_min = 2.0
    material.initial_velocity_max = 4.0

    # Turbulence
    material.turbulence_enabled = true
    material.turbulence_noise_strength = 2.0
    material.turbulence_noise_speed = Vector3(0.5, 1, 0.5)
    material.turbulence_influence_min = 0.1
    material.turbulence_influence_max = 0.3

    # Scale over lifetime
    material.scale_min = 0.2
    material.scale_max = 0.5

    # Disable gravity
    material.gravity = Vector3.ZERO

    process_material = material

    # Use billboard quad for particles
    var quad := QuadMesh.new()
    quad.size = Vector2(1, 1)
    draw_pass_1 = quad

    # Material for rendering
    var render_mat := StandardMaterial3D.new()
    render_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
    render_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
    render_mat.vertex_color_use_as_albedo = true
    render_mat.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
    render_mat.albedo_texture = preload("res://textures/fire_particle.png")

    material_override = render_mat
```

### Particle Sub-Emitters
```gdscript
extends GPUParticles2D

# Main explosion particles
func setup_with_sub_emitters() -> void:
    # Main particles
    amount = 20
    lifetime = 0.5
    one_shot = true

    var main_material := ParticleProcessMaterial.new()
    main_material.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_POINT
    main_material.direction = Vector3(0, -1, 0)
    main_material.spread = 180.0
    main_material.initial_velocity_min = 200.0
    main_material.initial_velocity_max = 400.0
    main_material.gravity = Vector3(0, 500, 0)

    # Sub-emitter spawns particles from main particles
    var sub_emitter := GPUParticles2D.new()
    sub_emitter.amount = 5
    sub_emitter.lifetime = 0.3
    sub_emitter.local_coords = false

    var sub_material := ParticleProcessMaterial.new()
    sub_material.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_POINT
    sub_material.spread = 45.0
    sub_material.initial_velocity_min = 50.0
    sub_material.initial_velocity_max = 100.0

    sub_emitter.process_material = sub_material

    # Connect sub-emitter
    main_material.sub_emitter = sub_emitter.get_path()
    main_material.sub_emitter_mode = ParticleProcessMaterial.SUB_EMITTER_CONSTANT
    main_material.sub_emitter_frequency = 30.0

    process_material = main_material
    add_child(sub_emitter)
```

## Trail Effects

### Line2D Trail
```gdscript
extends Node2D

@export var trail_length := 20
@export var trail_width := 10.0

@onready var line: Line2D = $Line2D
@onready var target: Node2D = $Target

var points: Array[Vector2] = []

func _ready() -> void:
    line.width = trail_width
    line.gradient = create_trail_gradient()
    line.begin_cap_mode = Line2D.LINE_CAP_ROUND
    line.end_cap_mode = Line2D.LINE_CAP_ROUND

func create_trail_gradient() -> Gradient:
    var gradient := Gradient.new()
    gradient.set_color(0, Color(1, 1, 1, 1))
    gradient.set_color(1, Color(1, 1, 1, 0))
    return gradient

func _process(_delta: float) -> void:
    # Add current position
    points.push_front(target.global_position)

    # Limit length
    while points.size() > trail_length:
        points.pop_back()

    # Update line
    line.clear_points()
    for point in points:
        line.add_point(point)
```

### Trail with Width Curve
```gdscript
extends Line2D

@export var target: Node2D
@export var max_points := 30
@export var base_width := 20.0

var point_data: Array[Dictionary] = []

func _ready() -> void:
    width_curve = Curve.new()
    width_curve.add_point(Vector2(0, 1))
    width_curve.add_point(Vector2(1, 0))

func _process(delta: float) -> void:
    if not target:
        return

    # Add new point
    point_data.push_front({
        "position": target.global_position,
        "age": 0.0
    })

    # Update ages and remove old
    var new_data: Array[Dictionary] = []
    for data in point_data:
        data.age += delta
        if data.age < 1.0:  # 1 second lifetime
            new_data.append(data)

    point_data = new_data

    # Rebuild line
    clear_points()
    for data in point_data:
        add_point(data.position)

    # Adjust width based on segment
    width = base_width
```

### 3D Trail with Mesh
```gdscript
extends MeshInstance3D

@export var target: Node3D
@export var max_points := 50
@export var width := 0.5

var points: Array[Vector3] = []
var surface_tool := SurfaceTool.new()

func _process(_delta: float) -> void:
    if not target:
        return

    points.push_front(target.global_position)
    while points.size() > max_points:
        points.pop_back()

    rebuild_mesh()

func rebuild_mesh() -> void:
    if points.size() < 2:
        mesh = null
        return

    surface_tool.clear()
    surface_tool.begin(Mesh.PRIMITIVE_TRIANGLE_STRIP)

    var camera := get_viewport().get_camera_3d()
    if not camera:
        return

    for i in range(points.size()):
        var point := points[i]
        var t := float(i) / (points.size() - 1)

        # Calculate perpendicular to camera
        var to_camera := (camera.global_position - point).normalized()
        var direction: Vector3
        if i < points.size() - 1:
            direction = (points[i + 1] - point).normalized()
        else:
            direction = (point - points[i - 1]).normalized()

        var perpendicular := direction.cross(to_camera).normalized()
        var current_width := width * (1.0 - t)

        # Add vertices
        surface_tool.set_uv(Vector2(0, t))
        surface_tool.set_color(Color(1, 1, 1, 1 - t))
        surface_tool.add_vertex(point + perpendicular * current_width)

        surface_tool.set_uv(Vector2(1, t))
        surface_tool.set_color(Color(1, 1, 1, 1 - t))
        surface_tool.add_vertex(point - perpendicular * current_width)

    mesh = surface_tool.commit()
```

## Screen Effects

### Screen Shake
```gdscript
extends Camera2D

var shake_intensity := 0.0
var shake_decay := 5.0

func shake(intensity: float, duration: float = 0.5) -> void:
    shake_intensity = intensity

    var tween := create_tween()
    tween.tween_property(self, "shake_intensity", 0.0, duration)

func _process(delta: float) -> void:
    if shake_intensity > 0.01:
        offset = Vector2(
            randf_range(-shake_intensity, shake_intensity),
            randf_range(-shake_intensity, shake_intensity)
        )
    else:
        offset = Vector2.ZERO

# Trauma-based shake (more organic)
extends Camera2D

var trauma := 0.0
var trauma_decay := 1.0
var max_offset := Vector2(100, 75)
var max_rotation := 15.0
var noise := FastNoiseLite.new()
var noise_y := 0.0

func _ready() -> void:
    noise.seed = randi()
    noise.frequency = 2.0

func add_trauma(amount: float) -> void:
    trauma = min(trauma + amount, 1.0)

func _process(delta: float) -> void:
    if trauma > 0:
        trauma = max(trauma - trauma_decay * delta, 0)
        apply_shake()

func apply_shake() -> void:
    var shake := trauma * trauma  # Quadratic for feel

    noise_y += 1
    offset.x = max_offset.x * shake * noise.get_noise_2d(0, noise_y)
    offset.y = max_offset.y * shake * noise.get_noise_2d(100, noise_y)
    rotation = deg_to_rad(max_rotation * shake * noise.get_noise_2d(200, noise_y))
```

### Flash Effect
```gdscript
extends CanvasLayer

@onready var flash_rect: ColorRect = $FlashRect

func flash(color: Color = Color.WHITE, duration: float = 0.1) -> void:
    flash_rect.color = color
    flash_rect.show()

    var tween := create_tween()
    tween.tween_property(flash_rect, "color:a", 0.0, duration)
    tween.tween_callback(flash_rect.hide)

# Hit flash on sprite
extends Sprite2D

@export var flash_material: ShaderMaterial

func flash_white(duration: float = 0.1) -> void:
    material = flash_material
    flash_material.set_shader_parameter("flash_amount", 1.0)

    var tween := create_tween()
    tween.tween_property(flash_material, "shader_parameter/flash_amount", 0.0, duration)
    tween.tween_callback(func(): material = null)
```

### Freeze Frame
```gdscript
extends Node

func freeze_frame(duration: float) -> void:
    Engine.time_scale = 0.0

    # Use a timer that ignores time scale
    await get_tree().create_timer(duration, true, false, true).timeout

    Engine.time_scale = 1.0

# Slow motion
func slow_motion(scale: float, duration: float) -> void:
    Engine.time_scale = scale

    var tween := create_tween()
    tween.set_ignore_time_scale(true)
    tween.tween_property(Engine, "time_scale", 1.0, duration)
```

## Procedural VFX

### Slash Effect
```gdscript
extends Node2D

@export var slash_arc := 120.0  # degrees
@export var slash_radius := 100.0
@export var slash_duration := 0.15
@export var slash_color := Color.WHITE

var slash_progress := 0.0
var is_slashing := false

func do_slash() -> void:
    slash_progress = 0.0
    is_slashing = true

    var tween := create_tween()
    tween.tween_property(self, "slash_progress", 1.0, slash_duration)
    tween.tween_callback(func(): is_slashing = false; queue_redraw())

func _process(_delta: float) -> void:
    if is_slashing:
        queue_redraw()

func _draw() -> void:
    if not is_slashing:
        return

    var start_angle := deg_to_rad(-slash_arc / 2)
    var current_angle := start_angle + deg_to_rad(slash_arc) * slash_progress

    var points := PackedVector2Array()
    var colors := PackedColorArray()

    # Create arc
    var segments := 20
    for i in range(int(segments * slash_progress) + 1):
        var t := float(i) / segments
        var angle := start_angle + deg_to_rad(slash_arc) * t
        var point := Vector2(cos(angle), sin(angle)) * slash_radius

        points.append(point)

        var alpha := 1.0 - (slash_progress - t)
        alpha = clamp(alpha, 0, 1)
        colors.append(Color(slash_color, alpha))

    if points.size() > 1:
        draw_polyline_colors(points, colors, 5.0)
```

### Impact Effect
```gdscript
extends Node2D

func spawn_impact(position: Vector2, normal: Vector2) -> void:
    var impact := preload("res://effects/impact.tscn").instantiate()
    impact.global_position = position
    impact.rotation = normal.angle()
    get_tree().current_scene.add_child(impact)

# impact.gd
extends Node2D

@onready var particles: GPUParticles2D = $Particles
@onready var flash: Sprite2D = $Flash
@onready var ring: Sprite2D = $Ring

func _ready() -> void:
    particles.emitting = true

    # Flash animation
    var flash_tween := create_tween()
    flash_tween.tween_property(flash, "scale", Vector2(2, 2), 0.1)
    flash_tween.parallel().tween_property(flash, "modulate:a", 0.0, 0.1)

    # Ring expansion
    var ring_tween := create_tween()
    ring_tween.tween_property(ring, "scale", Vector2(3, 3), 0.2)
    ring_tween.parallel().tween_property(ring, "modulate:a", 0.0, 0.2)

    # Cleanup
    await get_tree().create_timer(particles.lifetime).timeout
    queue_free()
```

### Damage Numbers
```gdscript
extends Node2D

@export var float_speed := 50.0
@export var float_duration := 1.0

func spawn_damage_number(amount: int, position: Vector2, is_crit: bool = false) -> void:
    var label := Label.new()
    label.text = str(amount)
    label.global_position = position
    label.z_index = 100

    if is_crit:
        label.add_theme_color_override("font_color", Color.YELLOW)
        label.add_theme_font_size_override("font_size", 24)
    else:
        label.add_theme_color_override("font_color", Color.WHITE)
        label.add_theme_font_size_override("font_size", 16)

    add_child(label)

    # Random horizontal offset
    var offset := randf_range(-20, 20)

    var tween := create_tween()
    tween.set_parallel(true)
    tween.tween_property(label, "position:y", position.y - float_speed, float_duration)
    tween.tween_property(label, "position:x", position.x + offset, float_duration)
    tween.tween_property(label, "modulate:a", 0.0, float_duration).set_delay(float_duration * 0.5)

    tween.chain().tween_callback(label.queue_free)
```

## Effect Pooling

### VFX Pool Manager
```gdscript
class_name VFXPool
extends Node

var pools: Dictionary = {}  # scene_path -> Array[Node]

func get_effect(scene_path: String) -> Node:
    if not pools.has(scene_path):
        pools[scene_path] = []

    var pool: Array = pools[scene_path]

    # Find available effect
    for effect in pool:
        if not effect.is_inside_tree():
            return effect

    # Create new if none available
    var scene := load(scene_path) as PackedScene
    var effect := scene.instantiate()
    pool.append(effect)
    return effect

func play_at(scene_path: String, position: Vector2, parent: Node = null) -> Node:
    var effect := get_effect(scene_path)

    if parent:
        parent.add_child(effect)
    else:
        get_tree().current_scene.add_child(effect)

    effect.global_position = position

    if effect.has_method("play"):
        effect.play()

    return effect

# Pooled effect script
extends Node2D

signal finished

func play() -> void:
    $Particles.restart()
    $Particles.emitting = true

    await get_tree().create_timer($Particles.lifetime).timeout

    get_parent().remove_child(self)
    finished.emit()
```
