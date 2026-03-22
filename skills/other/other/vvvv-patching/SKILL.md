---
name: vvvv-patching
description: Explains vvvv gamma visual programming patterns — dataflow, node connections, regions (ForEach/If/Switch/Repeat/Accumulator), channels for reactive data flow, event handling (Bang/Toggle/FrameDelay/Changed), patch organization, and common anti-patterns (circular dependencies, polling vs reacting, ignoring Nil). Use when the user asks about patching best practices, dataflow patterns, event handling, or how to structure visual programs.
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with vvvv gamma development
metadata:
  author: Tebjan Halm
  version: "1.0"
---

# vvvv Patching Patterns

## Dataflow Basics

- **Left-to-right, top-to-bottom** execution order
- **Links** carry data between pads (input/output connection points)
- **Spreading** — connecting a `Spread<T>` to a single-value input auto-iterates the node
- Every frame, the entire connected graph evaluates; disconnected subgraphs are skipped

Both visual patches and C# source projects operate in a live environment — edits take effect immediately while the program runs. Patch changes preserve node state; C# code changes trigger a node restart (Dispose → Constructor). You can adjust parameters, add connections, and restructure patches while seeing results in real-time.

## When to Patch vs Write C#

| Patch | Code (C#) |
|---|---|
| Data flow routing, visual connections | Performance-critical algorithms |
| Prototyping and parameter tweaking | Complex state machines |
| UI composition and layout | .NET library interop |
| Simple transformations | Native resource management |

As a rule: **patch the data flow, code the algorithms**.

## Regions

Regions are visual constructs that control execution flow:

| Region | Purpose | C# Equivalent |
|---|---|---|
| **ForEach** | Iterate over Spread elements | `foreach` loop |
| **If** | Conditional execution | `if/else` |
| **Switch** | Multi-branch selection | `switch` |
| **Repeat** | Loop N times | `for` loop |
| **Accumulator** | Running aggregation | `Aggregate/Fold` |

## Process Nodes in Patches

Process nodes are the primary way to add state to patches:
- They have a **Create** region (runs once) and an **Update** region (runs each frame)
- Internal state persists between frames
- Can contain sub-patches for complex logic

## Channels — Reactive Data Flow

Channels provide two-way data binding:
- `IChannel<T>` — observable value container
- `.Value` — read or write the current value
- Channels persist state across sessions
- Connect channels between nodes for reactive updates without explicit links

## Event Handling

- **Bang** — a one-frame `true` pulse (trigger)
- **Toggle** — alternates between `true` and `false`
- **FrameDelay** — delays a value by one frame (breaks circular dependencies)
- Use `Changed` node to detect when a value changes between frames

## Patch Organization

### Naming Conventions
- Use PascalCase for patch names and node names
- Group related operations under a common category
- Use descriptive names that indicate the operation (verb + noun)

### Structure
- Keep patches focused — one purpose per patch
- Extract reusable logic into sub-patches
- Use **IOBox** nodes for exposing parameters
- Add **Pad** nodes to create input/output pins on the patch boundary

## Common Anti-Patterns

1. **Circular dependencies** — use FrameDelay to break cycles
2. **Too many nodes in one patch** — extract sub-patches
3. **Polling instead of reacting** — use Channels for reactive updates
4. **Ignoring Nil** — always handle null/empty Spread inputs gracefully

For common patterns reference, see [patterns.md](patterns.md).
