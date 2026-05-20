---
name: godot
cluster: game-dev
description: "Godot is an open-source game engine for 2D and 3D development using GDScript."
tags: ["godot","game-engine","gdscript"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "godot game engine 2d 3d gamedev gdscript scripting"
---

# godot

## Purpose
This skill enables the AI to assist with Godot game engine tasks, focusing on 2D and 3D game development using GDScript. Use it to generate, debug, or optimize Godot projects programmatically.

## When to Use
Apply this skill when building or modifying games in Godot, such as creating prototypes, scripting game logic, or exporting builds. Use it for tasks involving GDScript, scene management, or integration with Godot's node-based system, especially in game-dev workflows.

## Key Capabilities
Godot supports 2D/3D rendering via its scene tree, with GDScript for scripting. Key features include physics simulation (e.g., RigidBody2D for collisions), animation handling (e.g., AnimationPlayer node), and asset importing (e.g., .gltf for 3D models). It handles input via InputMap and signals for event-driven programming. Export options include platforms like HTML5 or Android using built-in exporters.

## Usage Patterns
To use Godot effectively, structure commands via CLI for automation or embed GDScript in projects. For CLI, run scripts from the project directory; for code, extend nodes and connect signals. Always specify the project path in commands. Pattern: Load scenes dynamically in GDScript, then handle updates in _process() or _physics_process(). For integration, wrap Godot functions in try-except blocks to catch runtime errors.

## Common Commands/API
Use the Godot CLI for project management. Example: `godot --path /path/to/project --run main.gd` to execute a script. For exporting: `godot --path . --export "Linux/X11" build/linux.zip --no-window`. In GDScript, use API like `extends Node2D` for base classes; connect signals with `signal my_signal(value)` and `emit_signal("my_signal", 42)`. Config formats: Edit project settings via project.godot file, e.g., set `application/config/name="MyGame"`. No auth keys required, as Godot is local.

## Integration Notes
Integrate Godot with tools like Git for version control (commit project.godot and scenes). For external scripts, import via `load("res://script.gd")` in GDScript. If combining with other engines, export Godot projects as standalone binaries. Use environment variables for custom paths, e.g., set $GODOT_PROJECT_PATH="/user/project" and reference in commands like `godot --path $GODOT_PROJECT_PATH`. Avoid mixing with other engines' APIs; stick to Godot's node system for compatibility.

## Error Handling
In GDScript, handle errors with assertions or checks, e.g., use `if not is_instance_valid(node): print("Node invalid")`. For CLI, check exit codes: if `godot --run script.gd` fails, parse output for messages like "Error: Script not found". Common issues: Missing resources; resolve by ensuring paths in project.godot are correct. Pattern: Wrap code in functions like `func safe_load(path): var res = load(path); if res == null: printerr("Load failed")`. Log errors via Godot's OS class: `OS.alert("Error occurred")`.

## Usage Examples
Example 1: Create a simple 2D scene with a moving sprite. Use CLI to run: `godot --path /path/to/project --editor`. In GDScript, add to a node: `extends Sprite; func _process(delta): position.x += 50 * delta; if position.x > 500: position.x = 0`. This script makes the sprite move horizontally and wrap around.

Example 2: Export a project for Windows. Command: `godot --path . --export "Windows Desktop" build/win.exe`. Then, in GDScript, handle input: `func _input(event): if event.is_action_pressed("jump"): velocity.y = -300`. This sets up a basic jump mechanic and automates the build process.

## Graph Relationships
- Related to: game-dev cluster (e.g., skills like unity for similar game development tasks)
- Connected via tags: godot (direct match), game-engine (links to other engines like unreal), gdscript (relates to scripting skills)
- Cross-cluster links: game-dev to tools like git for version control in projects
