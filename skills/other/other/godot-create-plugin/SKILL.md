---
name: godot-create-plugin
version: 3.0.0
displayName: Create Godot Editor Plugin
description: >
  Use when creating Godot Editor plugins with custom docks, panels, and tools.
  Generates plugin.cfg configuration, EditorPlugin script templates, custom
  editor UI components, and integrates with ProjectSettings. Creates complete
  plugin structure following Godot 4.x best practices.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: intermediate
audience: [developers]
keywords:
  - godot
  - editor-plugin
  - plugin.cfg
  - EditorPlugin
  - custom-dock
  - editor-panel
  - tool-script
  - gdscript
  - project-settings
  - editor-extension
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".gd", ".tscn", "project.godot"]
    write: [".cfg", ".gd", ".tscn", "project.godot"]
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "Complete plugin structure with plugin.cfg, EditorPlugin script, custom docks/panels, and settings integration"
requirements: "Godot 4.x project, Git repository"
execution: "Generates plugin files with templates and git commits"
integration: "Works with godot-refactor orchestrator, creates reusable editor tools"
---

# Create Godot Editor Plugin

## Core Principle

**Extend the editor, don't fight it.** Godot Editor plugins let you add custom tools, panels, and workflows directly into the editor interface.

## What This Skill Does

Creates complete Godot Editor plugins:
- **plugin.cfg** - Plugin metadata and configuration
- **EditorPlugin script** - Entry point with lifecycle hooks
- **Custom docks** - Side panels with custom UI
- **Bottom panels** - Bottom dock tabs like Animation/Shader editors
- **Tool scripts** - Scripts that run in editor
- **Settings integration** - ProjectSettings for plugin configuration

## Plugin Structure Created

```
addons/my_plugin/
├── plugin.cfg              # Plugin metadata
├── my_plugin.gd            # EditorPlugin entry point
├── docks/
│   ├── main_dock.gd        # Custom side dock logic
│   ├── main_dock.tscn      # Dock UI scene
│   └── bottom_panel.gd     # Bottom panel logic
├── ui/
│   ├── inspector_plugin.gd # Custom inspector controls
│   └── property_editor.gd  # Custom property editors
└── tools/
    ├── scene_tool.gd       # @tool script for editor functionality
    └── asset_processor.gd  # Import/Process automation
```

## When to Use

### You Need Custom Editor Tools
Creating level editors, terrain tools, or specialized workflows that integrate into Godot.

### You Want Inspector Extensions
Adding custom property editors for your custom resources or nodes.

### You're Building Asset Pipelines
Automating import workflows, batch processing, or custom exporters.

### You Need Project-Wide Utilities
Tools that operate across scenes, manage resources, or provide project insights.

## Process

1. **Generate plugin.cfg** - Create metadata file with name, description, version
2. **Create EditorPlugin script** - Implement `_enter_tree()` and `_exit_tree()`
3. **Build custom UI** - Design docks and panels as scenes
4. **Add tool scripts** - Create @tool scripts for editor functionality
5. **Integrate settings** - Add ProjectSettings entries for configuration
6. **Commit** - Git commit with complete plugin structure

## Example: Simple Dock Plugin

**Generated: addons/my_dock/plugin.cfg**
```ini
[plugin]
name="My Custom Dock"
description="Adds a custom dock panel to the editor"
author="Your Name"
version="1.0.0"
script="my_dock.gd"
```

**Generated: addons/my_dock/my_dock.gd**
```gdscript
@tool
extends EditorPlugin

const DOCK_SCENE = preload("res://addons/my_dock/dock.tscn")
var dock_instance: Control

func _enter_tree():
    # Add custom dock to left slot
    dock_instance = DOCK_SCENE.instantiate()
    add_control_to_dock(DOCK_SLOT_LEFT_BR, dock_instance)
    
    # Add custom settings
    _setup_project_settings()

func _exit_tree():
    # Remove dock when plugin is disabled
    if dock_instance:
        remove_control_from_docks(dock_instance)
        dock_instance.queue_free()

func _setup_project_settings():
    # Add custom project settings for plugin configuration
    if not ProjectSettings.has_setting("my_plugin/enabled_features"):
        ProjectSettings.set_setting("my_plugin/enabled_features", ["feature_a", "feature_b"])
        ProjectSettings.add_property_info({
            "name": "my_plugin/enabled_features",
            "type": TYPE_ARRAY,
            "hint": PROPERTY_HINT_TYPE_STRING,
            "hint_string": "24/17:Feature"
        })
```

**Generated: addons/my_dock/dock.gd**
```gdscript
@tool
extends Control

@onready var button: Button = $VBoxContainer/Button
@onready var label: Label = $VBoxContainer/Label

func _ready():
    button.pressed.connect(_on_button_pressed)

func _on_button_pressed():
    label.text = "Button clicked at %s" % Time.get_time_string_from_system()
    
    # Access plugin settings
    var features = ProjectSettings.get_setting("my_plugin/enabled_features", [])
    print("Enabled features: ", features)
```

**Generated: addons/my_dock/dock.tscn**
```ini
[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://addons/my_dock/dock.gd" id="1_script"]

[node name="MyDock" type="Control"]
layout_mode = 3
anchors_preset = 15
script = ExtResource("1_script")

[node name="VBoxContainer" type="VBoxContainer" parent="."]
layout_mode = 1
anchors_preset = 15

[node name="Button" type="Button" parent="VBoxContainer"]
text = "Click Me"

[node name="Label" type="Label" parent="VBoxContainer"]
text = "Ready"
```

## Example: Custom Inspector Plugin

**Generated: addons/inspector_plugin/plugin.cfg**
```ini
[plugin]
name="Custom Inspector"
description="Adds custom property editors"
author="Your Name"
version="1.0.0"
script="custom_inspector.gd"
```

**Generated: addons/inspector_plugin/custom_inspector.gd**
```gdscript
@tool
extends EditorPlugin

var inspector_plugin: EditorInspectorPlugin

func _enter_tree():
    inspector_plugin = preload("res://addons/inspector_plugin/my_inspector_plugin.gd").new()
    add_inspector_plugin(inspector_plugin)

func _exit_tree():
    remove_inspector_plugin(inspector_plugin)
```

**Generated: addons/inspector_plugin/my_inspector_plugin.gd**
```gdscript
@tool
extends EditorInspectorPlugin

func _can_handle(object: Object) -> bool:
    # Apply to any node with custom script
    return object is Node

func _parse_property(object: Object, type: Variant.Type, name: String, 
                     hint_type: PropertyHint, hint_string: String, 
                     usage_flags: int, wide: bool) -> bool:
    # Handle specific property types
    if name == "my_custom_property":
        add_property_editor(name, preload("res://addons/inspector_plugin/custom_property_editor.gd").new())
        return true  # Handled
    return false  # Use default editor
```

## Example: Tool Script Pattern

**Generated: addons/tools/scene_batch_processor.gd**
```gdscript
@tool
extends EditorScript

## Batch process scenes in editor
## Run via: Editor > Run > Run Script

@export var target_directory: String = "res://scenes"
@export var operation: String = "cleanup"

func _run():
    print("Starting batch processing...")
    
    var dir = DirAccess.open(target_directory)
    if dir:
        dir.list_dir_begin()
        var file_name = dir.get_next()
        
        while file_name != "":
            if file_name.ends_with(".tscn"):
                _process_scene(target_directory.path_join(file_name))
            file_name = dir.get_next()
    
    print("Batch processing complete!")

func _process_scene(path: String):
    var scene = load(path)
    if scene:
        print("Processing: ", path)
        # Perform operations on packed scene
```

## Dock Slot Options

| Slot | Location | Best For |
|------|----------|----------|
| `DOCK_SLOT_LEFT_UL` | Left, upper | Main tools, frequent access |
| `DOCK_SLOT_LEFT_BL` | Left, lower | Secondary panels |
| `DOCK_SLOT_LEFT_UR` | Left, upper right | Inspector companions |
| `DOCK_SLOT_LEFT_BR` | Left, lower right | Debug/info panels |
| `DOCK_SLOT_RIGHT_UL` | Right, upper | Properties, settings |
| `DOCK_SLOT_RIGHT_BL` | Right, lower | Console, output |
| `DOCK_SLOT_RIGHT_UR` | Right, upper right | Less frequent tools |
| `DOCK_SLOT_RIGHT_BR` | Right, lower right | Bottom companions |

## EditorPlugin Lifecycle

```gdscript
func _enter_tree():
    # Called when plugin is enabled
    # Add docks, menus, inspectors here
    pass

func _exit_tree():
    # Called when plugin is disabled
    # Clean up everything added in _enter_tree
    pass

func _has_main_screen() -> bool:
    # Return true if plugin provides main screen (like 2D/3D/Script)
    return false

func _make_visible(visible: bool):
    # Called when main screen tab is selected/deselected
    pass

func _get_plugin_name() -> String:
    # Name shown in main screen tabs
    return "My Plugin"

func _get_plugin_icon() -> Texture2D:
    # Icon for main screen tab
    return get_editor_interface().get_base_control().get_theme_icon("Node", "EditorIcons")
```

## Settings Integration

Add custom ProjectSettings entries:

```gdscript
func _enter_tree():
    # Add setting if it doesn't exist
    if not ProjectSettings.has_setting("my_plugin/enable_debug"):
        ProjectSettings.set_setting("my_plugin/enable_debug", false)
        
        # Define property metadata
        ProjectSettings.add_property_info({
            "name": "my_plugin/enable_debug",
            "type": TYPE_BOOL,
            "hint": PROPERTY_HINT_NONE
        })
        
        # Set as basic setting (shows in Project Settings UI)
        ProjectSettings.set_initial_value("my_plugin/enable_debug", false)
        ProjectSettings.set_as_basic("my_plugin/enable_debug", true)
```

## Access Editor from Plugin

```gdscript
# Get the editor interface
var interface = get_editor_interface()

# Access editor features
var editor_selection = interface.get_selection()
var editor_settings = interface.get_editor_settings()
var resource_preview = interface.get_resource_previewer()

# Get current scene
var edited_scene_root = interface.get_edited_scene_root()

# Get selected nodes
var selected_nodes = editor_selection.get_selected_nodes()

# Open scene in editor
interface.open_scene_from_path("res://scene.tscn")

# Reload scene
interface.reload_scene_from_path("res://scene.tscn")

# Play scene
interface.play_current_scene()
```

## What Gets Created

- **Complete plugin structure** in `addons/plugin_name/`
- **plugin.cfg** with proper metadata
- **EditorPlugin script** with lifecycle hooks
- **Dock scenes** (UI) and scripts (logic)
- **Bottom panels** for specialized tools
- **Inspector plugins** for custom property editors
- **Tool scripts** for editor automation
- **ProjectSettings integration** for configuration
- **Git commits** documenting each component

## Integration

Works with:
- **godot-refactor** (orchestrator) - Create plugins as part of larger refactoring
- **godot-extract-to-scenes** - Use extracted components in plugin UI
- **godot-add-signals** - Connect plugin UI signals

## Safety

- Validates plugin.cfg syntax
- Checks for plugin name conflicts
- Ensures proper cleanup in `_exit_tree()`
- Auto-rollback on validation failure
- Git commits for each generated component

## When NOT to Use

Don't create a plugin for:
- One-off scripts (use EditorScript without plugin)
- Simple utilities (use Project > Tools > GDScript)
- Runtime game features (plugins are editor-only)
- Replacing existing Godot features

## Best Practices

1. **Clean up in `_exit_tree()`** - Remove all added UI/components
2. **Use `@tool` scripts** - Enable code to run in editor
3. **Check `Engine.is_editor_hint()`** - Distinguish editor vs runtime
4. **Prefix settings** - Use `plugin_name/setting_name` convention
5. **Save settings** - Call `ProjectSettings.save()` after changes
6. **Handle selection** - Update UI when editor selection changes
7. **Lazy loading** - Load heavy resources only when needed
