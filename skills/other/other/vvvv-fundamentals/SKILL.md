---
name: vvvv-fundamentals
description: Explains vvvv gamma core concepts — data types, frame-based execution model, pins, pads, links, node browser, live compilation (source project vs binary reference workflows), .vl document structure, file types (.vl/.sdsl/.cs/.csproj), ecosystem overview, and AppHost runtime detection. Use when the user asks about vvvv basics, how vvvv works, the live reload model, when to patch vs code, or needs an overview of the visual programming environment.
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with vvvv gamma development
metadata:
  author: Tebjan Halm
  version: "1.0"
---

# vvvv gamma Fundamentals

## What Is vvvv gamma

vvvv gamma is a visual programming environment for .NET 8. It combines node-based patching with C# code generation, targeting Stride (3D engine) and .NET APIs. Programs are built by connecting nodes with links in a visual editor.

vvvv is a live programming environment — programs run continuously while you build them. Both visual patch edits and C# code changes take effect immediately without restarting. vvvv compiles C# source files itself via Roslyn into in-memory assemblies on every save.

## Document Structure

- **`.vl` files** — vvvv gamma documents (XML-based, version controlled)
- Each document contains **Patches** (visual programs) and **Definitions** (types, operations)
- Documents can reference NuGet packages and other `.vl` files
- The **Patch Explorer** shows the document's type hierarchy

## Execution Model

- **Frame-based evaluation** — the mainloop evaluates the entire graph every frame (~60 FPS)
- **Data flows left-to-right, top-to-bottom** through links between nodes
- **Process nodes** maintain state between frames (constructor → Update loop → Dispose)
- **Operation nodes** are pure functions evaluated each frame
- vvvv evaluates all connected nodes, skips disconnected subgraphs

## Live Compilation Model

vvvv runs your program continuously while you edit it. There is no edit-compile-run cycle for patches and shaders. For C#, live reload depends on how the code is referenced.

### Patch Changes

- Edits to visual patches apply immediately
- Node state (instance fields) is preserved across edits
- New nodes and links become active on the next frame

### Shader Changes

- `.sdsl` shader files always live-reload when saved
- vvvv recompiles shaders in the background and swaps them in the running program

### C# — Two Workflows

C# code can be integrated via source project reference or pre-compiled binary. The choice depends on project size and development phase.

**Source project reference** (live reload):

When a .vl document references a .csproj source project, vvvv compiles .cs files itself via Roslyn into in-memory assemblies. No `dotnet build` or external toolchain is involved.

- On .cs file save, vvvv detects the change and recompiles in the background
- Status indicator: gray = building symbols, orange = emitting C#
- On successful compilation, affected nodes restart their lifecycle:
  1. `Dispose()` called on old instance
  2. New constructor runs (with fresh `NodeContext`)
  3. `Update()` resumes on the next frame
- Static fields reset on reload — the entire in-memory assembly is replaced
- On compilation error, the program continues running with the last valid code

**Binary reference** (no live reload):

When a .vl document references a pre-compiled DLL or NuGet package, the assembly is loaded once at startup. To pick up changes, you must rebuild the DLL externally (e.g., `dotnet build`) and restart vvvv. This workflow is common for larger projects and stable libraries where live reload is not needed.

## Node Categories

### Process Nodes
- Have Create (constructor), Update (per-frame), and Dispose lifecycle
- Written in C# with `[ProcessNode]` attribute
- Maintain internal state between frames
- Use change detection to avoid redundant work

### Operation Nodes
- Pure functions: same input always produces same output
- Written as static C# methods (auto-discovered by vvvv)
- No state between frames
- No `[ProcessNode]` attribute needed

### Adaptive Nodes
- Nodes that adapt their implementation based on connected input types
- Example: `+` works with int, float, Vector3, string, etc.
- Resolved at link-time, not runtime

## Pins, Pads, and Links

- **Pins** — inputs and outputs on nodes and regions
- **Pads** — visual nodes for reading/writing Properties inside operation patches; all pads with the same name refer to the same property
- **Links** — connections between pins that define data flow and execution order
- **Spreading** — when a `Spread<T>` connects to a single-value input, the node auto-iterates

## When to Patch vs Write C#

| Use Patching | Use C# Code |
|---|---|
| Prototyping, data flow | Custom nodes, performance-critical code |
| Visual connections, UI composition | Complex algorithms |
| Real-time parameter tweaking | .NET library interop |
| Dataflow routing and spreading | Native/unmanaged resource management |

## Channels — Reactive Data Flow

- `IChannel<T>` — observable value container
- `IChannel<T>.Value` — read/write the current value
- `Channel.IsValid()` — check if connected
- Channels persist state across sessions
- Enable two-way data binding between UI and patch

For C# channel integration patterns (IChannelHub, PublicChannelHelper, [CanBePublished]), see vvvv-channels.

## Key Data Types

| Type | C# Equivalent | Usage |
|---|---|---|
| `Spread<T>` | `ImmutableArray<T>` | vvvv's immutable collection |
| `SpreadBuilder<T>` | `ImmutableArray<T>.Builder` | Build spreads efficiently |
| Float32, Int32, etc. | `float`, `int` | Primitives |
| `Vector2/3/4` | `Stride.Core.Mathematics` | Spatial math |
| `Color4` | `Stride.Core.Mathematics` | RGBA color |

## File Types

| Extension | Purpose |
|---|---|
| `.vl` | vvvv gamma documents (XML-based) |
| `.sdsl` | Stride shader files (SDSL language) |
| `.cs` | C# source files for custom nodes |
| `.csproj` | .NET project files |
| `.nuspec` | NuGet package spec |

## Ecosystem Overview

vvvv's functionality extends through NuGet packages that bundle .vl documents, C# nodes, and shaders.

| Domain | Key Packages |
|---|---|
| 3D Rendering | VL.Stride (Stride engine), VL.Fuse (GPU visual programming) |
| 2D Rendering | VL.Skia, ImGui, Avalonia, CEF/HTML |
| Hardware I/O | DMX/Art-Net, ILDA lasers, depth cameras (Azure Kinect, ZED), robotics (KUKA, Spot), Ultraleap, LiDAR |
| Networking | OSC, MIDI, MQTT, Redis, WebSocket, HTTP, TCP/UDP, ZeroMQ, Modbus, Ableton Link |
| Computer Vision | OpenCV, MediaPipe, YOLO (v8–v11), ONNX Runtime |
| Audio | NAudio, VST hosting, SuperCollider bridge |
| General .NET | Any of 100,000+ standard NuGet packages via .csproj reference |

To add a package: reference it in your `.vl` document's Dependencies, or add a `<PackageReference>` to your `.csproj`. See vvvv-dotnet for .csproj details.

## AppHost & Runtime Detection

```csharp
// Detect if running as exported .exe vs editor
bool isExported = nodeContext.AppHost.IsExported;

// Register per-app singleton services
nodeContext.AppHost.Services.RegisterService(myService);
```

For detailed reference, see [reference.md](reference.md).
