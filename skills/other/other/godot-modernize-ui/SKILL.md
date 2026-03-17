---
name: godot-modernize-ui
version: 1.0.0
displayName: Godot UI Modernization
description: Modernize Godot 3.x UI to 4.x best practices with theme extraction, responsive layouts, hiDPI support, and RichTextLabel BBCode patterns
author: Godot Superpowers
license: MIT
category: ui
type: tool
difficulty: beginner
audience:
  - developers
  - ui-designers
keywords:
  - godot
  - ui
  - theme
  - responsive
  - hidpi
  - bbcode
  - anchoring
  - layout
  - control
  - modernize
platforms:
  - linux
  - macos
  - windows
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme
---

# Godot UI Modernization

Modernizes Godot 3.x UI scenes and scripts to Godot 4.x best practices.

## When to Use

- Migrating Godot 3.x projects to 4.x with UI scenes
- UI doesn't scale properly on hiDPI displays
- Hardcoded styles scattered across Control nodes
- Manual positioning instead of responsive anchoring
- RichTextLabel using deprecated BBCode tags
- Creating reusable custom controls

## Core Patterns

### 1. Theme Resource Extraction

**Before (Godot 3.x):**
```gdscript
# Hardcoded in each Control node
$Button.modulate = Color.red
$Button.get("custom_styles/normal").bg_color = Color.blue
$Label.add_font_override("font", preload("res://fonts/big.tres"))
```

**After (Godot 4.x):**
```gdscript
# Centralized in Theme resource
# Create: res://ui/themes/main_theme.tres
# Assign to root Control or project settings
```

**Theme.tres structure:**
```
Theme
├── Button/styles/normal (StyleBoxFlat)
├── Button/colors/font_color = Color(1, 1, 1, 1)
├── Button/fonts/font = preload("res://fonts/button_font.tres")
├── Label/fonts/font = preload("res://fonts/label_font.tres")
└── Panel/styles/panel (StyleBoxFlat)
```

### 2. Control Anchoring Standardization

**Before:**
```gdscript
# Manual positioning
$Panel.position = Vector2(100, 100)
$Panel.size = Vector2(400, 300)
```

**After:**
```
Control (root)
├── Layout Mode: Anchors
├── Anchor Left: 0.5, Anchor Top: 0.5
├── Anchor Right: 0.5, Anchor Bottom: 0.5
├── Grow Horizontal: Center
├── Grow Vertical: Center
└── Custom Minimum Size: (400, 300)
```

**Anchor Presets for Common Layouts:**

| Layout | Anchors | Offsets | Grow |
|--------|---------|---------|------|
| Fullscreen | 0,0 to 1,1 | 0 all sides | Both |
| Top Bar | 0,0 to 1,0 | Bottom: 60 | Horizontal |
| Bottom Bar | 0,1 to 1,1 | Top: 60 | Horizontal |
| Center Panel | 0.5,0.5 | Size defined | Both |
| Left Sidebar | 0,0 to 0,1 | Right: 250 | Vertical |
| Right Sidebar | 1,0 to 1,1 | Left: 250 | Vertical |

### 3. UI Scaling (hiDPI Support)

**Project Settings:**
```
Display > Window > Stretch
├── Mode: canvas_items (or viewport)
├── Aspect: expand
└── Scale: 1.0 (auto-detected)
```

**Script for Dynamic Scaling:**
```gdscript
func _ready():
    # Handle hiDPI on different displays
    var screen_dpi = DisplayServer.screen_get_dpi()
    if screen_dpi > 150:
        get_tree().root.content_scale_factor = 2.0
```

**Responsive Sizing:**
```gdscript
@export var base_width: float = 1920.0
@export var base_height: float = 1080.0

func _on_viewport_size_changed():
    var viewport_size = get_viewport().get_visible_rect().size
    var scale_x = viewport_size.x / base_width
    var scale_y = viewport_size.y / base_height
    scale = Vector2(min(scale_x, scale_y), min(scale_x, scale_y))
```

### 4. RichTextLabel BBCode Patterns

**Deprecated Godot 3.x:**
```
[color=red]Warning[/color]
[url=https://example.com]Link[/url]
[img]res://icon.png[/img]
```

**Godot 4.x BBCode:**
```
[color=ff0000]Warning[/color]
[color=#ff0000]Hex Color[/color]
[url=https://example.com]Link[/url]
[img=64x64]res://icon.png[/img]
[font=res://fonts/custom.tres]Custom font[/font]
[wave amp=50 freq=5]Animated text[/wave]
[tornado radius=5 freq=2]Spinning text[/tornado]
[shake rate=5 level=10]Shaking text[/shake]
[fgcolor=00ff00 bgcolor=000000]Background[/fgcolor]
[outline_color=ffffff]Outlined[/outline_color]
```

**Script Integration:**
```gdscript
@onready var rich_label: RichTextLabel = $RichTextLabel

func append_colored_text(text: String, color: Color):
    rich_label.append_text("[color=%s]%s[/color]" % [color.to_html(), text])

func append_url(text: String, url: String):
    rich_label.append_text("[url=%s]%s[/url]" % [url, text])
    
func _on_meta_clicked(meta):
    OS.shell_open(str(meta))
```

### 5. Custom Control Creation

**Custom Button with Built-in Theme:**
```gdscript
@tool
class_name ModernButton
extends Button

@export var button_style: ButtonStyle = ButtonStyle.PRIMARY:
    set(value):
        button_style = value
        _update_style()

enum ButtonStyle { PRIMARY, SECONDARY, DANGER }

func _ready():
    _update_style()

func _update_style():
    match button_style:
        ButtonStyle.PRIMARY:
            add_theme_color_override("font_color", Color(1, 1, 1))
            add_theme_stylebox_override("normal", preload("res://ui/styles/primary_normal.tres"))
        ButtonStyle.SECONDARY:
            add_theme_color_override("font_color", Color(0.2, 0.2, 0.2))
            add_theme_stylebox_override("normal", preload("res://ui/styles/secondary_normal.tres"))
        ButtonStyle.DANGER:
            add_theme_color_override("font_color", Color(1, 1, 1))
            add_theme_stylebox_override("normal", preload("res://ui/styles/danger_normal.tres"))
```

## Responsive Design Patterns

### Container Hierarchy

```
CanvasLayer (UI Layer)
└── Control (Full Rect anchor, Fullscreen preset)
    ├── MarginContainer (padding)
    │   ├── VBoxContainer (vertical layout)
    │   │   ├── HBoxContainer (top bar)
    │   │   │   ├── Label (title)
    │   │   │   └── Button (close)
    │   │   └── ScrollContainer (scrollable content)
    │   │       └── VBoxContainer
    │   │           └── (dynamic content)
    │   └── HBoxContainer (bottom bar)
    │       └── Button (action)
    └── Panel (overlay/popup)
```

### Safe Area Handling (Mobile)
```gdscript
func _ready():
    # Apply safe area insets for notched devices
    var safe_area = DisplayServer.get_display_safe_area()
    var window_size = DisplayServer.window_get_size()
    
    $MarginContainer.add_theme_constant_override("margin_left", safe_area.position.x)
    $MarginContainer.add_theme_constant_override("margin_top", safe_area.position.y)
    $MarginContainer.add_theme_constant_override("margin_right", 
        window_size.x - safe_area.end.x)
    $MarginContainer.add_theme_constant_override("margin_bottom", 
        window_size.y - safe_area.end.y)
```

## Common Mistakes

**Using RectPosition/RectSize directly:**
```gdscript
# ❌ Bad - breaks with different resolutions
$Control.rect_position = Vector2(100, 100)
$Control.rect_size = Vector2(200, 150)

# ✅ Good - use anchors and layout containers
# Set anchors in editor or use custom_minimum_size
$Control.custom_minimum_size = Vector2(200, 150)
```

**Hardcoding pixel values without scaling:**
```gdscript
# ❌ Bad - too small on hiDPI
var padding = 10

# ✅ Good - scale with content_scale_factor
var padding = 10 * get_tree().root.content_scale_factor
```

**Manual font size calculations:**
```gdscript
# ❌ Bad - inconsistent across displays
label.add_theme_font_size_override("font_size", 24)

# ✅ Good - use theme with dynamic fonts
# Set in Theme resource with multiple sizes
```

**Forgetting to handle window resize:**
```gdscript
# ✅ Good - subscribe to resize signal
func _ready():
    get_viewport().size_changed.connect(_on_viewport_size_changed)
    _on_viewport_size_changed()

func _on_viewport_size_changed():
    # Recalculate responsive layout
    pass
```

## Quick Reference

| Task | Godot 3.x | Godot 4.x |
|------|-----------|-----------|
| Theme override | `add_stylebox_override()` | `add_theme_stylebox_override()` |
| Font override | `add_font_override()` | `add_theme_font_override()` |
| Color override | `add_color_override()` | `add_theme_color_override()` |
| Constant override | `add_constant_override()` | `add_theme_constant_override()` |
| Size override | `rect_min_size` | `custom_minimum_size` |
| Position | `rect_position` | `position` |
| Size | `rect_size` | `size` |
| Global position | `rect_global_position` | `global_position` |
| BBCode color | `[color=red]` | `[color=ff0000]` or `[color=#ff0000]` |
| BBCode image | `[img]path[/img]` | `[img=widthxheight]path[/img]` |
| hiDPI setting | `ProjectSettings.display/window/dpi/allow_hidpi` | `Display > Window > Stretch > Mode` |

## Migration Checklist

- [ ] Extract all hardcoded styles to Theme resources
- [ ] Replace rect_* properties with position/size
- [ ] Update BBCode syntax (colors, images)
- [ ] Configure hiDPI in project settings
- [ ] Convert manual positioning to anchor/layout system
- [ ] Test on multiple resolutions and DPIs
- [ ] Add viewport resize handling
- [ ] Create custom controls for repeated patterns
