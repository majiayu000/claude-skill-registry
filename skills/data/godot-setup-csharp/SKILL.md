---
name: godot-setup-csharp
version: 3.0.0
displayName: Setup C# Integration
description: >
  Use when adding C# support to Godot 4.x projects or creating mixed GDScript/C# architectures.
  Sets up project structure, configures .csproj files, enables GDScript to C# communication,
  implements signal connections in C#, handles resource loading, and identifies performance-critical
  code candidates for C# optimization.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: intermediate
audience: [developers]
keywords:
  - godot
  - csharp
  - dotnet
  - csproj
  - gdscript-interop
  - signals
  - resource-loading
  - performance
  - mono
  - mixed-language
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".gd", ".cs", ".csproj", ".sln"]
    write: [".cs", ".csproj", ".sln"]
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "C# project files, .csproj configuration, C# script templates, signal bindings, resource loading code"
requirements: "Godot 4.x with .NET support, dotnet CLI, Git repository"
execution: "Semi-automatic with manual review points"
integration: "Works with godot-refactor, godot-extract-resources, godot-add-signals"
---

# Setup C# Integration

## Core Principle

**Use C# for performance-critical code, GDScript for rapid iteration.** Godot 4.x's .NET integration enables seamless mixed-language development.

## What This Skill Does

Transforms single-language projects into optimized mixed GDScript/C# architectures:

1. **Generates project structure** - .csproj, .sln, solution folders
2. **Enables cross-language communication** - GDScript calling C#, C# calling GDScript
3. **Implements signals in C#** - Type-safe signal connections and emissions
4. **Sets up resource loading** - Loading .tres, .tscn files from C#
5. **Identifies optimization candidates** - Code patterns that benefit from C#

## Detection Patterns

Identifies candidates for C# migration:
- Heavy mathematical operations (physics, pathfinding, AI)
- Complex data processing (inventory systems, save games)
- External library needs (NuGet packages, .NET ecosystem)
- Performance bottlenecks in GDScript profiling
- Systems requiring strong typing (networking, serialization)

## When to Use

### You're Starting a New Godot 4.x Project
Set up C# from the beginning for mixed-language flexibility.

### You Have Performance Bottlenecks
GDScript profiler shows heavy computation in hot paths.

### You Need .NET Libraries
Want to use Newtonsoft.Json, System.Text.Json, Math.NET, etc.

### You're Porting from Unity
Existing C# codebase to integrate with Godot.

### You Want Strong Typing
Large codebase where compile-time type checking prevents bugs.

## Process

1. **Analyze** - Profile GDScript, identify C# candidates
2. **Generate** - Create .csproj with Godot.NET.Sdk
3. **Configure** - Set up solution structure and references
4. **Migrate** - Convert selected scripts to C#
5. **Interop** - Set up GDScript ↔ C# communication
6. **Signals** - Implement signal connections in C#
7. **Resources** - Configure resource loading from C#
8. **Validate** - Test cross-language functionality
9. **Commit** - Git commit per major component

## Project Structure Generated

```
project-root/
├── project.godot
├── MyProject.csproj          # Auto-generated
├── MyProject.sln             # Solution file
├── scripts/
│   ├── gdscript/             # GDScript files
│   └── csharp/               # C# scripts
│       ├── Core/             # Performance-critical systems
│       ├── Utils/            # Helper classes
│       └── Resources/        # Resource loaders
└── .vscode/
    └── launch.json           # Debug configuration
```

## Example Transformations

### Project Setup

**Before (GDScript only):**
```gdscript
# No C# configuration
```

**After (Mixed setup):**
```xml
<!-- MyProject.csproj -->
<Project Sdk="Godot.NET.Sdk/4.2.0">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <EnableDynamicLoading>true</EnableDynamicLoading>
  </PropertyGroup>
  
  <ItemGroup>
    <!-- Godot already includes GodotSharp -->
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
  </ItemGroup>
</Project>
```

### GDScript Calling C#

**C# Class:**
```csharp
// scripts/csharp/Pathfinder.cs
using Godot;

namespace MyProject.Core;

[GlobalClass]
public partial class Pathfinder : Node
{
    [Export] public float CellSize { get; set; } = 32.0f;
    
    public Godot.Collections.Array<Vector2> FindPath(Vector2 start, Vector2 end)
    {
        // A* implementation in C#
        var path = new Godot.Collections.Array<Vector2>();
        // ... pathfinding logic
        return path;
    }
}
```

**GDScript Usage:**
```gdscript
# enemy.gd
@onready var pathfinder: Pathfinder = $"../Pathfinder"

func move_to_target(target_pos: Vector2):
    var path = pathfinder.find_path(global_position, target_pos)
    follow_path(path)
```

### C# Calling GDScript

**GDScript with Methods:**
```gdscript
# ui_manager.gd
class_name UIManager

func show_damage_number(amount: int, position: Vector2):
    var label = preload("res://ui/damage_label.tscn").instantiate()
    label.text = str(amount)
    label.position = position
    add_child(label)
```

**C# Calling GDScript:**
```csharp
// scripts/csharp/CombatSystem.cs
using Godot;

public partial class CombatSystem : Node
{
    private Node _uiManager;
    
    public override void _Ready()
    {
        _uiManager = GetNode("../UIManager");
    }
    
    public void ApplyDamage(Node target, int damage)
    {
        // Call GDScript method from C#
        var pos = ((Node2D)target).GlobalPosition;
        _uiManager.Call("show_damage_number", damage, pos);
    }
}
```

### Signals in C#

**Defining and Emitting:**
```csharp
// scripts/csharp/HealthComponent.cs
using Godot;

namespace MyProject.Core;

[GlobalClass]
public partial class HealthComponent : Node
{
    [Signal] public delegate void HealthChangedEventHandler(int newHealth, int maxHealth);
    [Signal] public delegate void DiedEventHandler();
    
    [Export] public int MaxHealth { get; set; } = 100;
    
    private int _currentHealth;
    public int CurrentHealth 
    { 
        get => _currentHealth;
        set
        {
            _currentHealth = Mathf.Clamp(value, 0, MaxHealth);
            EmitSignal(SignalName.HealthChanged, _currentHealth, MaxHealth);
            
            if (_currentHealth <= 0)
                EmitSignal(SignalName.Died);
        }
    }
}
```

**Connecting in GDScript:**
```gdscript
# player.gd
@onready var health: HealthComponent = $HealthComponent

func _ready():
    health.health_changed.connect(_on_health_changed)
    health.died.connect(_on_died)

func _on_health_changed(new_health: int, max_health: int):
    update_health_bar(new_health, max_health)

func _on_died():
    play_death_animation()
```

**Connecting in C#:**
```csharp
// scripts/csharp/HealthBarUI.cs
using Godot;

public partial class HealthBarUI : ProgressBar
{
    public override void _Ready()
    {
        var healthComponent = GetNode<HealthComponent>("../HealthComponent");
        healthComponent.HealthChanged += OnHealthChanged;
    }
    
    private void OnHealthChanged(int newHealth, int maxHealth)
    {
        MaxValue = maxHealth;
        Value = newHealth;
    }
}
```

### Resource Loading in C#

**Loading Custom Resources:**
```csharp
// scripts/csharp/WeaponLoader.cs
using Godot;

namespace MyProject.Utils;

[GlobalClass]
public partial class WeaponLoader : Node
{
    public WeaponData LoadWeapon(string weaponId)
    {
        string path = $"res://resources/weapons/{weaponId}.tres";
        return GD.Load<WeaponData>(path);
    }
    
    public PackedScene LoadScene(string scenePath)
    {
        return GD.Load<PackedScene>(scenePath);
    }
}

// Custom resource class
[GlobalClass]
public partial class WeaponData : Resource
{
    [Export] public string WeaponName { get; set; }
    [Export] public int Damage { get; set; }
    [Export] public float AttackSpeed { get; set; }
    [Export] public Texture2D Icon { get; set; }
}
```

**GDScript Resource Definition:**
```gdscript
# resources/weapon_data.gd
class_name WeaponData
extends Resource

@export var weapon_name: String
@export var damage: int
@export var attack_speed: float
@export var icon: Texture2D
```

## Performance-Critical Code Identification

### Migrate to C# When You See:

| Pattern | GDScript Cost | C# Benefit |
|---------|--------------|------------|
| Heavy loops (1000+ iterations) | Interpreted overhead | Compiled, JIT-optimized |
| Complex math operations | Slower float math | Vectorized operations |
| String manipulation | Allocations | StringBuilder, spans |
| Dictionary lookups | Hash overhead | Generic Dictionary<T,T> |
| JSON serialization | Manual parsing | Newtonsoft.Json/System.Text.Json |
| Physics calculations | Per-frame interpreted | Native performance |
| Pathfinding/AI | Algorithm overhead | A* in C#, multithreading |

### Examples of Good C# Candidates:

```gdscript
# BAD: Heavy computation in GDScript
func process_voxels():
    for x in range(64):
        for y in range(64):
            for z in range(64):
                var voxel = calculate_voxel(x, y, z)  # 262k iterations!

# BETTER: Call C# for heavy work
@onready var voxel_processor: VoxelProcessor = $VoxelProcessor

func process_voxels():
    var result = voxel_processor.process_chunk(position)  # C# handles loops
```

```csharp
// C# Implementation
using Godot;

public partial class VoxelProcessor : Node
{
    public byte[,,] ProcessChunk(Vector3I chunkPos)
    {
        var voxels = new byte[64, 64, 64];
        // Fast C# loops with compiler optimizations
        for (int x = 0; x < 64; x++)
            for (int y = 0; y < 64; y++)
                for (int z = 0; z < 64; z++)
                    voxels[x, y, z] = CalculateVoxel(chunkPos, x, y, z);
        return voxels;
    }
}
```

## Communication Patterns

### Pattern 1: C# Core with GDScript UI
- C#: Game logic, AI, physics, data processing
- GDScript: UI, animation, scene management, input handling

### Pattern 2: GDScript Gameplay with C# Utilities
- GDScript: Main gameplay loops, node interactions
- C#: Math utilities, save/load systems, external API calls

### Pattern 3: Shared Resources
- Both languages use same .tres resource files
- C# Resource classes with [GlobalClass] attribute
- GDScript resource definitions

## What Gets Created

- `.csproj` project file with Godot.NET.Sdk
- `.sln` solution file for IDE integration
- C# script templates in `scripts/csharp/`
- `[GlobalClass]` attributed classes for cross-language use
- Signal definitions with proper C# syntax
- Resource loader utilities
- `.vscode/launch.json` for debugging
- Documentation of interop boundaries

## Safety

- Gradual migration - one system at a time
- Git commits at each integration point
- Validation tests for cross-language calls
- Type safety prevents runtime errors
- Original GDScript preserved in git history

## When NOT to Use

Don't add C# if:
- Team has no C# experience
- Project is small (< 1000 lines)
- No performance issues exist
- Build complexity isn't worth benefit
- Target platform doesn't support .NET (some consoles)

## Best Practices

### Keep Interop Boundaries Clean
```csharp
// GOOD: Self-contained C# class
public partial class InventorySystem : Node
{
    public void AddItem(string itemId, int quantity) { }
    public bool RemoveItem(string itemId, int quantity) => true;
    public Godot.Collections.Array<string> GetItems() => null;
}
```

### Use Godot Types for Interop
```csharp
// GOOD: Godot types work across languages
public void MoveEntity(Node2D entity, Vector2 position) { }

// AVOID: Pure C# types require conversion
public void ProcessList(List<string> items) { }  // GDScript can't call easily
```

### Signal Naming Consistency
```csharp
// C# signals use PascalCase
[Signal] public delegate void ItemCollectedEventHandler(string itemId);

// Connect from GDScript (snake_case in GDScript)
inventory_system.item_collected.connect(_on_item_collected)
```

### Export Properties Work Both Ways
```csharp
// C# exports visible in editor
[Export] public float MovementSpeed { get; set; } = 200.0f;
[Export] public PackedScene ProjectileScene { get; set; }
```

## Integration

Works with:
- **godot-extract-resources** - C# Resource classes with [GlobalClass]
- **godot-add-signals** - Type-safe C# signal implementations
- **godot-refactor** (orchestrator) - Mixed-language architecture decisions

## Common Transformations

| Scenario | GDScript | C# |
|----------|----------|-----|
| Class declaration | `class_name MyClass` | `public partial class MyClass : Node` |
| Export variable | `@export var speed: float` | `[Export] public float Speed { get; set; }` |
| Signal | `signal health_changed` | `[Signal] public delegate void HealthChangedEventHandler(int health);` |
| Method call to GDScript | `node.method()` | `node.Call("method", args)` |
| Load resource | `load("path")` | `GD.Load<Resource>("path")` |
| Dictionary | `var dict = {}` | `new Godot.Collections.Dictionary()` |
| Array | `var arr = []` | `new Godot.Collections.Array<T>()` |

## Debugging Setup

```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Play",
            "type": "coreclr",
            "request": "launch",
            "program": "${config:godotEditorPath}",
            "args": ["--path", "${workspaceRoot}"],
            "cwd": "${workspaceRoot}",
            "stopAtEntry": false
        }
    ]
}
```

## Benefits

- **Performance** - Compiled C# runs 10-100x faster for heavy computation
- **Type Safety** - Compile-time error detection
- **Ecosystem** - Access to NuGet packages and .NET libraries
- **Tooling** - Visual Studio, VS Code, Rider with full IDE support
- **Debugging** - Full debugger support with breakpoints
- **Gradual** - Migrate systems incrementally
