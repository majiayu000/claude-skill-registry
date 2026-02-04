---
name: godot-modernize-input
version: 2.0.0
displayName: Modernize Input Handling
description: >
  Use when handling input in Godot 4.x projects and need to modernize patterns.
  Generates Input Map configurations from hardcoded key checks, sets up joypad
  rumble (Godot 4.x feature), implements gyroscope/accelerometer input on mobile,
  creates context-sensitive input handling for different game states, and adds
  input buffering for responsive gameplay. Converts old InputEvent patterns to
  modern Godot 4.x best practices.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: intermediate
audience: [developers]
keywords:
  - godot
  - input-handling
  - input-map
  - joypad
  - rumble
  - haptic
  - gyroscope
  - accelerometer
  - mobile-input
  - input-buffering
  - gdscript
  - gamepad
  - controller
platforms: [macos, linux, windows, android, ios]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".gd", ".tscn", ".tres", "project.godot"]
    write: [".gd", ".tscn", "project.godot"]
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "Modernized input scripts, Input Map configurations, device support scripts, input buffering systems"
requirements: "Git repository, Godot 4.x, input handling code to modernize"
execution: "Semi-automatic with detection prompts and git commits"
integration: "Works with godot-modernize-gdscript for complete codebase updates"
---

# Modernize Input Handling

## Core Principle

**Input handling should be device-agnostic, responsive, and context-aware.** Hardcoded key checks, missing device support, and unbuffered input create poor player experiences across platforms.

## What This Skill Does

### 1. Input Map Generation from Code

Converts hardcoded key detection to Input Map actions:

**Before:**
```gdscript
# Hardcoded key checks - NOT recommended
func _input(event):
    if event is InputEventKey:
        if event.keycode == KEY_SPACE:
            jump()
        if event.keycode == KEY_ESCAPE:
            pause_game()
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_LEFT:
            shoot()
```

**After:**
```gdscript
# Modern Input Map usage
func _input(event: InputEvent) -> void:
    if event.is_action_pressed("jump"):
        jump()
    if event.is_action_pressed("pause"):
        pause_game()
    if event.is_action_pressed("shoot"):
        shoot()
```

**Generated Input Map (project.godot):**
```ini
[input]

jump={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":32,"key_label":0,"unicode":32,"echo":false,"script":null)
, Object(InputEventJoypadButton,"resource_local_to_scene":false,"resource_name":"","device":-1,"button_index":0,"pressure":0.0,"pressed":false,"script":null)
]
}

shoot={
"deadzone": 0.5,
"events": [Object(InputEventMouseButton,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"button_mask":0,"position":Vector2(0, 0),"global_position":Vector2(0, 0),"factor":1.0,"button_index":1,"canceled":false,"pressed":false,"double_click":false,"script":null)
, Object(InputEventJoypadMotion,"resource_local_to_scene":false,"resource_name":"","device":-1,"axis":5,"axis_value":1.0,"script":null)
]
}
```

### 2. Joypad Rumble Setup (Godot 4.x)

Implements haptic feedback for controllers:

```gdscript
# InputRumbler.gd - Autoload singleton
extends Node

const WEAK_RUMBLE: float = 0.3
const MEDIUM_RUMBLE: float = 0.6
const STRONG_RUMBLE: float = 1.0
const SHORT_DURATION: float = 0.1
const MEDIUM_DURATION: float = 0.3
const LONG_DURATION: float = 0.8

var current_device: int = 0

func _ready() -> void:
    Input.joy_connection_changed.connect(_on_joy_connection_changed)

func _on_joy_connection_changed(device: int, connected: bool) -> void:
    if connected:
        current_device = device
        print("Controller connected: ", Input.get_joy_name(device))

func rumble(weak_magnitude: float, strong_magnitude: float, duration: float) -> void:
    if Input.get_joy_name(current_device).is_empty():
        return
    
    Input.start_joy_vibration(current_device, weak_magnitude, strong_magnitude, duration)

func rumble_impact() -> void:
    rumble(WEAK_RUMBLE, STRONG_RUMBLE, SHORT_DURATION)

func rumble_damage() -> void:
    rumble(MEDIUM_RUMBLE, MEDIUM_RUMBLE, MEDIUM_DURATION)

func rumble_explosion() -> void:
    rumble(STRONG_RUMBLE, STRONG_RUMBLE, LONG_DURATION)

func rumble_heartbeat() -> void:
    rumble(WEAK_RUMBLE, 0.0, 0.5)
    await get_tree().create_timer(0.6).timeout
    rumble(WEAK_RUMBLE, 0.0, 0.5)
```

### 3. Gyroscope/Accelerometer Input (Mobile)

Implements motion controls for mobile devices:

```gdscript
# MotionController.gd
extends Node

@export var tilt_sensitivity: float = 2.0
@export var shake_threshold: float = 15.0

signal tilt_detected(direction: Vector2)
signal shake_detected

var accelerometer_enabled: bool = false
var gyroscope_enabled: bool = false

func _ready() -> void:
    # Check if running on mobile
    if OS.has_feature("mobile") or OS.has_feature("android") or OS.has_feature("ios"):
        enable_motion_sensors()

func enable_motion_sensors() -> void:
    if DisplayServer.has_feature(DisplayServer.FEATURE_TOUCHSCREEN):
        # Enable accelerometer (gravity + user acceleration)
        if DisplayServer.has_feature(DisplayServer.FEATURE_SENSOR_ACCELEROMETER):
            DisplayServer.accelerometer_set_mode(DisplayServer.ACCELEROMETER_MODE_COMBINED)
            accelerometer_enabled = true
        
        # Enable gyroscope for rotation rate
        if DisplayServer.has_feature(DisplayServer.FEATURE_SENSOR_GYROSCOPE):
            gyroscope_enabled = true

func _process(delta: float) -> void:
    if not (accelerometer_enabled or gyroscope_enabled):
        return
    
    # Handle tilt-based movement
    if accelerometer_enabled:
        var accel: Vector3 = Input.get_accelerometer()
        var tilt: Vector2 = Vector2(accel.x, -accel.y) * tilt_sensitivity
        
        if tilt.length() > 0.1:
            tilt_detected.emit(tilt)
    
    # Handle shake detection
    if gyroscope_enabled:
        var gyro: Vector3 = Input.get_gyroscope()
        if gyro.length() > shake_threshold:
            shake_detected.emit()

func get_tilt_direction() -> Vector2:
    if not accelerometer_enabled:
        return Vector2.ZERO
    
    var accel: Vector3 = Input.get_accelerometer()
    # Normalize for device orientation
    return Vector2(accel.x, -accel.y).normalized()

func calibrate_center() -> void:
    # Store current orientation as neutral position
    var current_accel: Vector3 = Input.get_accelerometer()
    # Implementation: Store offset and apply to future readings
```

### 4. Context-Sensitive Input Handling

Manages different input contexts (gameplay, menu, dialogue, etc.):

```gdscript
# InputContextManager.gd - Autoload singleton
extends Node

enum Context {
    GAMEPLAY,
    MENU,
    DIALOGUE,
    PAUSED,
    INVENTORY
}

var current_context: Context = Context.GAMEPLAY
var context_stack: Array[Context] = []

# Context-specific action mappings
var context_actions: Dictionary = {
    Context.GAMEPLAY: ["move_left", "move_right", "jump", "shoot", "interact"],
    Context.MENU: ["ui_up", "ui_down", "ui_accept", "ui_cancel", "ui_left", "ui_right"],
    Context.DIALOGUE: ["ui_accept", "ui_cancel", "skip_dialogue"],
    Context.PAUSED: ["ui_accept", "ui_cancel", "resume"],
    Context.INVENTORY: ["inventory_navigate", "inventory_use", "inventory_close"]
}

func set_context(new_context: Context) -> void:
    context_stack.push_back(current_context)
    current_context = new_context
    _update_input_processing()
    print("Input context changed to: ", Context.keys()[new_context])

func restore_previous_context() -> void:
    if context_stack.size() > 0:
        current_context = context_stack.pop_back()
        _update_input_processing()

func reset_to_gameplay() -> void:
    context_stack.clear()
    current_context = Context.GAMEPLAY
    _update_input_processing()

func _update_input_processing() -> void:
    # Enable/disable action processing based on context
    var enabled_actions: Array = context_actions.get(current_context, [])
    
    # This works with built-in UI actions too
    match current_context:
        Context.GAMEPLAY:
            get_tree().paused = false
        Context.PAUSED:
            get_tree().paused = true
        Context.MENU, Context.INVENTORY:
            get_viewport().set_input_as_handled()

func is_action_allowed(action: StringName) -> bool:
    var enabled_actions: Array = context_actions.get(current_context, [])
    return action in enabled_actions or action.begins_with("ui_")

# Example usage in player controller
func _input(event: InputEvent) -> void:
    if not InputContextManager.is_action_allowed("jump"):
        return
    
    if event.is_action_pressed("jump"):
        jump()
```

### 5. Input Buffering

Adds input buffering for responsive gameplay:

```gdscript
# InputBuffer.gd - Component for responsive input
extends Node

@export var buffer_duration: float = 0.15  # 150ms buffer window

var buffered_actions: Dictionary = {}

func _ready() -> void:
    # Initialize buffer for common actions
    buffered_actions = {
        "jump": 0.0,
        "shoot": 0.0,
        "dash": 0.0,
        "interact": 0.0
    }

func _process(delta: float) -> void:
    # Decay buffer timers
    for action in buffered_actions.keys():
        if buffered_actions[action] > 0:
            buffered_actions[action] -= delta

func _input(event: InputEvent) -> void:
    for action in buffered_actions.keys():
        if event.is_action_pressed(action):
            buffer_action(action)

func buffer_action(action: StringName) -> void:
    if action in buffered_actions:
        buffered_actions[action] = buffer_duration

func is_buffered(action: StringName) -> bool:
    return action in buffered_actions and buffered_actions[action] > 0

func consume_buffer(action: StringName) -> bool:
    if is_buffered(action):
        buffered_actions[action] = 0.0
        return true
    return false

# Example usage in player controller
func _physics_process(delta: float) -> void:
    # Check buffered jump (allows jump before hitting ground)
    if input_buffer.is_buffered("jump") and is_on_floor():
        input_buffer.consume_buffer("jump")
        velocity.y = jump_velocity
```

## Detection Patterns

### Hardcoded Input Detection

Scans for:
- `InputEventKey` with specific `keycode` values
- `InputEventMouseButton` with specific `button_index` values
- `Input.is_key_pressed()` calls
- Direct joypad button checks without action mapping

### Legacy Patterns to Modernize

**Old Godot 3.x Pattern:**
```gdscript
if event is InputEventKey and event.scancode == KEY_SPACE:
    jump()
```

**Modern Godot 4.x:**
```gdscript
if event.is_action_pressed("jump"):
    jump()
```

## Device Support Matrix

| Input Type | Desktop | Mobile | Console | Implementation |
|------------|---------|--------|---------|----------------|
| Keyboard | ✅ | ❌ | ❌ | Input Map |
| Mouse | ✅ | ⚠️ Touch | ❌ | Input Map + Touch emulation |
| Touch | ❌ | ✅ | ❌ | Touch events + Virtual joystick |
| Gamepad | ✅ | ✅ (MFi) | ✅ | Input Map with deadzone |
| Gyroscope | ❌ | ✅ | ❌ (PS only) | MotionController singleton |
| Rumble | ✅ | ❌ | ✅ | InputRumbler singleton |

## When to Use

### You're Adding Controller Support
Your game only supports keyboard/mouse and needs gamepad compatibility.

### You're Porting to Mobile
Need to add touch controls, motion sensors, and adapt input for mobile devices.

### Input Feels Unresponsive
Players complain about missed inputs; need buffering for precise timing.

### Context Conflicts Exist
Menu navigation interferes with gameplay; need context-sensitive handling.

## Modern Input Best Practices

### 1. Always Use Input Map Actions
Never hardcode key checks in gameplay code. Use actions for:
- Remapping support
- Localization (different keyboard layouts)
- Accessibility (adaptive controllers)
- Multiple device types

### 2. Implement Deadzones
```gdscript
# In Input Map configuration (project.godot)
move_left={
"deadzone": 0.2,
"events": [Object(InputEventJoypadMotion,"resource_local_to_scene":false,"resource_name":"","device":-1,"axis":0,"axis_value":-1.0,"script":null)
]
}
```

### 3. Support Multiple Input Types Simultaneously
```gdscript
func _input(event: InputEvent) -> void:
    # Handle keyboard/controller
    if event.is_action_pressed("jump"):
        jump()
    
    # Handle touch (mobile)
    if event is InputEventScreenTouch and event.pressed:
        if _is_touch_in_jump_zone(event.position):
            jump()
```

### 4. Use InputEvent for One-Shots, _process for Continuous
```gdscript
# One-shot actions (button presses)
func _input(event: InputEvent) -> void:
    if event.is_action_pressed("shoot"):
        shoot()

# Continuous actions (held buttons)
func _process(delta: float) -> void:
    var move_direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")
    velocity.x = move_direction.x * speed
```

## Integration

Works with:
- **godot-modernize-gdscript** - Converts legacy GDScript patterns
- **godot-setup-multiplayer** - Synchronizes input across network
- **godot-extract-to-scenes** - Extracts input components as reusable scenes

## Safety

- Git commit per input modernization step
- Detection review before applying changes
- Rollback capability for each transformation
- Preserves manual Input Map entries

## When NOT to Use

Don't modernize if:
- Input handling is already using Input Map actions properly
- You're implementing platform-specific input (raw access needed)
- Legacy input is intentional for compatibility reasons

## Examples

### Complete Mobile Setup
```gdscript
# MobileInputHandler.gd
extends Node

@onready var virtual_joystick: VirtualJoystick = $VirtualJoystick
@onready var touch_buttons: Control = $TouchButtons

func _ready() -> void:
    # Only show touch UI on mobile
    var is_mobile: bool = OS.has_feature("mobile") or OS.has_feature("android") or OS.has_feature("ios")
    virtual_joystick.visible = is_mobile
    touch_buttons.visible = is_mobile

func get_movement_input() -> Vector2:
    # Combine gamepad and touch input
    var input := Input.get_vector("move_left", "move_right", "move_up", "move_down")
    
    if virtual_joystick.visible:
        input += virtual_joystick.output
    
    return input.normalized()
```

### Input Remapping UI
```gdscript
# RemapButton.gd
extends Button

@export var action: StringName

func _ready() -> void:
    pressed.connect(_on_pressed)
    update_display()

func _on_pressed() -> void:
    text = "Press any key..."
    set_process_input(true)

func _input(event: InputEvent) -> void:
    if event.is_pressed() and not event.is_echo():
        # Clear existing events for this action
        InputMap.action_erase_events(action)
        InputMap.action_add_event(action, event)
        set_process_input(false)
        update_display()

func update_display() -> void:
    var events: Array[InputEvent] = InputMap.action_get_events(action)
    if events.size() > 0:
        text = events[0].as_text()
    else:
        text = "Not assigned"
```
