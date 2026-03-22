---
name: vvvv-editor-extensions
description: Helps create vvvv gamma editor extensions — .HDE.vl file naming, Command node registration with keyboard shortcuts, SkiaWindow/SkiaWindowTopMost window types, docking with WindowFactory, and API access to hovered/selected nodes via VL.Lang Session nodes. Use when building editor plugins, custom tooling windows, or automating editor workflows.
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with vvvv gamma development
metadata:
  author: Tebjan Halm
  version: "1.0"
---

# Editor Extensions

Extensions are standard VL patches saved with a `.HDE.vl` suffix. They run automatically when open in the editor.

## File Naming

| Context | Required Name |
|---|---|
| Standalone extension | `VL.MyExtension.HDE.vl` |
| Extension-only NuGet | `VL.MyExtension.HDE` (package ID) |
| Mixed NuGet main doc | `VL.MyPackage.vl` |
| Mixed NuGet extension doc | `VL.MyPackage.HDE.vl` |

## Required NuGet References

- **VL.HDE** — provides `Command` node, window types, `WindowFactory`
- **VL.Lang** — provides API nodes under the `Session` category

## Command Node

Registers a command in the editor menu:

| Pin | Purpose |
|---|---|
| `Label` | Menu text |
| `Visible` | Show/hide the command |
| `Shortcut` | Keyboard binding |
| Output | Triggers (bang) on activation |

Multiple `Command` nodes can live in one `.HDE.vl` document.

**Warning**: A runtime error in one command may affect all others in the same document.

## Window Types

| Type | Behavior |
|---|---|
| `SkiaWindow` | Slimmed-down Skia renderer window |
| `SkiaWindowTopMost` | Always-on-top, no focus steal |

## Docking

Wrap window with `WindowFactory` node. Connect `WindowContext` and `Window` pins.

Template: `VL.HDE/Template.HDE.vl`

## API Access

Access hovered/selected nodes, read/write pins via `VL.Lang` `Session` category nodes. Browse available API in the HelpBrowser's `API` section.

## Developer Shortcuts

- **Shift+F9** — restarts all extensions simultaneously

## Limitations

- Settings panel integration is not yet possible
- Extensions only run in the editor, not in exported applications
