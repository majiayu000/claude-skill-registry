---
name: ui-system
description: Implements UI systems using Control nodes, themes, responsive layouts, and UI animations. Use when building menus, HUDs, and interactive interfaces.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot UI System

When implementing user interfaces, use these patterns for responsive and polished UI.

## Layout Basics

### Container-Based Layout
```gdscript
# VBoxContainer - Vertical stack
# HBoxContainer - Horizontal stack
# GridContainer - Grid layout
# MarginContainer - Add margins
# CenterContainer - Center content
# PanelContainer - Background panel

extends Control

func setup_menu() -> void:
    # Create vertical menu
    var vbox := VBoxContainer.new()
    vbox.add_theme_constant_override("separation", 10)

    for option in ["Start", "Options", "Quit"]:
        var button := Button.new()
        button.text = option
        button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        vbox.add_child(button)

    add_child(vbox)
```

### Anchors and Margins
```gdscript
extends Control

func setup_anchors() -> void:
    # Full screen
    anchor_left = 0
    anchor_top = 0
    anchor_right = 1
    anchor_bottom = 1

    # Top-right corner
    anchor_left = 1
    anchor_top = 0
    anchor_right = 1
    anchor_bottom = 0
    offset_left = -100
    offset_right = 0
    offset_top = 0
    offset_bottom = 50

    # Center
    anchor_left = 0.5
    anchor_top = 0.5
    anchor_right = 0.5
    anchor_bottom = 0.5
    offset_left = -50
    offset_right = 50
    offset_top = -25
    offset_bottom = 25

func set_full_rect() -> void:
    set_anchors_preset(Control.PRESET_FULL_RECT)

func set_center() -> void:
    set_anchors_preset(Control.PRESET_CENTER)
```

### Responsive Layout
```gdscript
extends Control

@export var mobile_threshold := 600

func _ready() -> void:
    get_viewport().size_changed.connect(_on_viewport_resized)
    _on_viewport_resized()

func _on_viewport_resized() -> void:
    var viewport_size := get_viewport().get_visible_rect().size

    if viewport_size.x < mobile_threshold:
        apply_mobile_layout()
    else:
        apply_desktop_layout()

func apply_mobile_layout() -> void:
    # Stack vertically, larger touch targets
    $MainContainer.columns = 1
    for button in $MainContainer.get_children():
        button.custom_minimum_size.y = 60

func apply_desktop_layout() -> void:
    # Grid layout, normal sizes
    $MainContainer.columns = 3
    for button in $MainContainer.get_children():
        button.custom_minimum_size.y = 40
```

## Common UI Components

### Health Bar
```gdscript
extends Control

@onready var bar: ProgressBar = $ProgressBar
@onready var tween: Tween

@export var animate_duration := 0.3

var max_health := 100.0
var current_health := 100.0

func set_health(value: float) -> void:
    current_health = clamp(value, 0, max_health)

    if tween:
        tween.kill()

    tween = create_tween()
    tween.tween_property(bar, "value", current_health / max_health * 100, animate_duration)

func set_max_health(value: float) -> void:
    max_health = value
    bar.max_value = 100
    set_health(current_health)

# Segmented health bar
extends Control

@export var segment_count := 5
@export var segment_texture: Texture2D

var segments: Array[TextureRect] = []

func _ready() -> void:
    for i in range(segment_count):
        var segment := TextureRect.new()
        segment.texture = segment_texture
        $HBoxContainer.add_child(segment)
        segments.append(segment)

func set_health_segments(filled: int) -> void:
    for i in range(segments.size()):
        segments[i].modulate.a = 1.0 if i < filled else 0.3
```

### Inventory Grid
```gdscript
extends GridContainer

signal slot_clicked(slot_index: int)

@export var slot_scene: PackedScene
@export var slot_count := 20

var slots: Array[Control] = []

func _ready() -> void:
    columns = 5

    for i in range(slot_count):
        var slot := slot_scene.instantiate()
        slot.slot_index = i
        slot.clicked.connect(_on_slot_clicked)
        add_child(slot)
        slots.append(slot)

func set_item(slot_index: int, item_data: Dictionary) -> void:
    if slot_index < slots.size():
        slots[slot_index].set_item(item_data)

func clear_slot(slot_index: int) -> void:
    if slot_index < slots.size():
        slots[slot_index].clear()

func _on_slot_clicked(slot_index: int) -> void:
    slot_clicked.emit(slot_index)

# inventory_slot.gd
extends Control

signal clicked(slot_index: int)

@export var slot_index := 0

@onready var icon: TextureRect = $Icon
@onready var count_label: Label = $CountLabel

func _gui_input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.pressed:
        if event.button_index == MOUSE_BUTTON_LEFT:
            clicked.emit(slot_index)

func set_item(item_data: Dictionary) -> void:
    icon.texture = load(item_data.get("icon", ""))
    var count: int = item_data.get("count", 1)
    count_label.text = str(count) if count > 1 else ""
    count_label.visible = count > 1

func clear() -> void:
    icon.texture = null
    count_label.text = ""
```

### Dialogue Box
```gdscript
extends Control

signal dialogue_finished

@onready var name_label: Label = $Panel/NameLabel
@onready var text_label: RichTextLabel = $Panel/TextLabel
@onready var continue_indicator: Control = $Panel/ContinueIndicator

@export var characters_per_second := 30.0

var dialogue_queue: Array[Dictionary] = []
var is_typing := false
var skip_typing := false

func show_dialogue(dialogues: Array[Dictionary]) -> void:
    dialogue_queue = dialogues.duplicate()
    show()
    show_next()

func show_next() -> void:
    if dialogue_queue.is_empty():
        hide()
        dialogue_finished.emit()
        return

    var dialogue := dialogue_queue.pop_front()
    name_label.text = dialogue.get("speaker", "")
    text_label.text = dialogue.get("text", "")
    text_label.visible_characters = 0
    continue_indicator.hide()

    is_typing = true
    skip_typing = false

    var duration := text_label.text.length() / characters_per_second
    var tween := create_tween()
    tween.tween_property(text_label, "visible_characters", text_label.text.length(), duration)
    tween.tween_callback(_on_typing_finished)

func _on_typing_finished() -> void:
    is_typing = false
    continue_indicator.show()

func _gui_input(event: InputEvent) -> void:
    if event.is_action_pressed("ui_accept"):
        if is_typing:
            # Skip to end
            text_label.visible_characters = text_label.text.length()
            is_typing = false
            continue_indicator.show()
        else:
            show_next()
```

### Tooltip System
```gdscript
# tooltip_manager.gd (Autoload)
extends CanvasLayer

@onready var tooltip: Control = $Tooltip
@onready var tooltip_label: Label = $Tooltip/Label

var follow_mouse := true

func _ready() -> void:
    tooltip.hide()

func _process(_delta: float) -> void:
    if tooltip.visible and follow_mouse:
        tooltip.global_position = get_viewport().get_mouse_position() + Vector2(15, 15)

        # Keep on screen
        var viewport_size := get_viewport().get_visible_rect().size
        if tooltip.global_position.x + tooltip.size.x > viewport_size.x:
            tooltip.global_position.x = viewport_size.x - tooltip.size.x
        if tooltip.global_position.y + tooltip.size.y > viewport_size.y:
            tooltip.global_position.y = viewport_size.y - tooltip.size.y

func show_tooltip(text: String) -> void:
    tooltip_label.text = text
    tooltip.show()

func hide_tooltip() -> void:
    tooltip.hide()

# Usage on any control
extends Button

@export var tooltip_text := "Click me!"

func _ready() -> void:
    mouse_entered.connect(_on_mouse_entered)
    mouse_exited.connect(_on_mouse_exited)

func _on_mouse_entered() -> void:
    TooltipManager.show_tooltip(tooltip_text)

func _on_mouse_exited() -> void:
    TooltipManager.hide_tooltip()
```

## UI Animations

### Tweened Transitions
```gdscript
extends Control

func fade_in(duration: float = 0.3) -> void:
    modulate.a = 0
    show()
    var tween := create_tween()
    tween.tween_property(self, "modulate:a", 1.0, duration)

func fade_out(duration: float = 0.3) -> void:
    var tween := create_tween()
    tween.tween_property(self, "modulate:a", 0.0, duration)
    tween.tween_callback(hide)

func slide_in_from_left(duration: float = 0.3) -> void:
    var target_pos := position
    position.x = -size.x
    show()
    var tween := create_tween()
    tween.set_ease(Tween.EASE_OUT)
    tween.set_trans(Tween.TRANS_BACK)
    tween.tween_property(self, "position", target_pos, duration)

func scale_popup(duration: float = 0.2) -> void:
    scale = Vector2.ZERO
    show()
    var tween := create_tween()
    tween.set_ease(Tween.EASE_OUT)
    tween.set_trans(Tween.TRANS_ELASTIC)
    tween.tween_property(self, "scale", Vector2.ONE, duration)
```

### Button Hover Effects
```gdscript
extends Button

@export var hover_scale := 1.1
@export var press_scale := 0.95
@export var animation_duration := 0.1

var base_scale := Vector2.ONE

func _ready() -> void:
    base_scale = scale
    mouse_entered.connect(_on_hover)
    mouse_exited.connect(_on_unhover)
    button_down.connect(_on_press)
    button_up.connect(_on_release)

func _on_hover() -> void:
    animate_scale(base_scale * hover_scale)

func _on_unhover() -> void:
    animate_scale(base_scale)

func _on_press() -> void:
    animate_scale(base_scale * press_scale)

func _on_release() -> void:
    if is_hovered():
        animate_scale(base_scale * hover_scale)
    else:
        animate_scale(base_scale)

func animate_scale(target: Vector2) -> void:
    var tween := create_tween()
    tween.tween_property(self, "scale", target, animation_duration)
```

### Notification Popup
```gdscript
extends Control

@onready var container: VBoxContainer = $VBoxContainer

var notification_scene := preload("res://ui/notification.tscn")

func show_notification(text: String, duration: float = 3.0, type: String = "info") -> void:
    var notification := notification_scene.instantiate()
    notification.setup(text, type)
    container.add_child(notification)

    # Slide in
    notification.position.x = size.x
    var tween := create_tween()
    tween.tween_property(notification, "position:x", 0, 0.3).set_ease(Tween.EASE_OUT)

    # Auto dismiss
    await get_tree().create_timer(duration).timeout

    tween = create_tween()
    tween.tween_property(notification, "modulate:a", 0, 0.3)
    tween.tween_callback(notification.queue_free)
```

## Input Handling

### Focus Navigation
```gdscript
extends Control

func _ready() -> void:
    # Set up focus neighbors programmatically
    var buttons := $VBoxContainer.get_children()

    for i in range(buttons.size()):
        var button: Button = buttons[i]

        if i > 0:
            button.focus_neighbor_top = buttons[i - 1].get_path()
        if i < buttons.size() - 1:
            button.focus_neighbor_bottom = buttons[i + 1].get_path()

        # Wrap around
        buttons[0].focus_neighbor_top = buttons[-1].get_path()
        buttons[-1].focus_neighbor_bottom = buttons[0].get_path()

    # Set initial focus
    buttons[0].grab_focus()
```

### Drag and Drop
```gdscript
# draggable_item.gd
extends Control

var drag_data: Dictionary

func _get_drag_data(_position: Vector2) -> Variant:
    # Create preview
    var preview := TextureRect.new()
    preview.texture = $Icon.texture
    preview.size = Vector2(32, 32)
    set_drag_preview(preview)

    return drag_data

# drop_target.gd
extends Control

signal item_dropped(data: Dictionary)

func _can_drop_data(_position: Vector2, data: Variant) -> bool:
    return data is Dictionary and data.has("item_id")

func _drop_data(_position: Vector2, data: Variant) -> void:
    item_dropped.emit(data)
```

### Input Rebinding
```gdscript
extends Control

var awaiting_input := false
var action_to_rebind := ""

func start_rebind(action: String) -> void:
    action_to_rebind = action
    awaiting_input = true
    $RebindLabel.text = "Press any key..."

func _input(event: InputEvent) -> void:
    if not awaiting_input:
        return

    if event is InputEventKey or event is InputEventJoypadButton:
        # Remove existing bindings
        InputMap.action_erase_events(action_to_rebind)

        # Add new binding
        InputMap.action_add_event(action_to_rebind, event)

        awaiting_input = false
        update_button_text()

func update_button_text() -> void:
    var events := InputMap.action_get_events(action_to_rebind)
    if events.size() > 0:
        $RebindLabel.text = events[0].as_text()
```

## Theming

### Custom Theme
```gdscript
extends Control

func apply_custom_theme() -> void:
    var custom_theme := Theme.new()

    # Button styling
    var button_normal := StyleBoxFlat.new()
    button_normal.bg_color = Color(0.2, 0.2, 0.2)
    button_normal.corner_radius_top_left = 5
    button_normal.corner_radius_top_right = 5
    button_normal.corner_radius_bottom_left = 5
    button_normal.corner_radius_bottom_right = 5

    var button_hover := button_normal.duplicate()
    button_hover.bg_color = Color(0.3, 0.3, 0.3)

    var button_pressed := button_normal.duplicate()
    button_pressed.bg_color = Color(0.1, 0.1, 0.1)

    custom_theme.set_stylebox("normal", "Button", button_normal)
    custom_theme.set_stylebox("hover", "Button", button_hover)
    custom_theme.set_stylebox("pressed", "Button", button_pressed)

    # Font
    var font := load("res://fonts/custom_font.ttf")
    custom_theme.set_font("font", "Button", font)
    custom_theme.set_font_size("font_size", "Button", 16)

    # Colors
    custom_theme.set_color("font_color", "Button", Color.WHITE)
    custom_theme.set_color("font_hover_color", "Button", Color.YELLOW)

    theme = custom_theme
```

### Dynamic Theme Switching
```gdscript
extends Node

var themes := {
    "light": preload("res://themes/light_theme.tres"),
    "dark": preload("res://themes/dark_theme.tres")
}

var current_theme := "dark"

func set_theme(theme_name: String) -> void:
    if not themes.has(theme_name):
        return

    current_theme = theme_name
    get_tree().root.theme = themes[theme_name]

func toggle_theme() -> void:
    set_theme("light" if current_theme == "dark" else "dark")
```

## Performance Tips

```gdscript
# Batch UI updates
extends Control

var pending_updates: Array[Callable] = []

func queue_update(update_func: Callable) -> void:
    pending_updates.append(update_func)

    if pending_updates.size() == 1:
        call_deferred("_process_updates")

func _process_updates() -> void:
    for update in pending_updates:
        update.call()
    pending_updates.clear()

# Use visibility to skip processing
extends Control

func _process(delta: float) -> void:
    if not visible:
        return
    # Update logic

# Preload commonly used scenes
var cached_scenes := {
    "button": preload("res://ui/button.tscn"),
    "slot": preload("res://ui/inventory_slot.tscn")
}
```
