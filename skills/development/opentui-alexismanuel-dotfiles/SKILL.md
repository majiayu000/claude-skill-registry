---
name: opentui
description: Comprehensive OpenTUI skill for building terminal user interfaces. Covers the core imperative API, React reconciler, and Solid reconciler. Use for any TUI development task including components, layout, keyboard handling, animations, and testing.
references:
  - core
  - react
  - solid
---

# OpenTUI Platform Skill

Consolidated skill for building terminal user interfaces with OpenTUI. Use decision trees below to find the right framework and components, then load detailed references.

## Critical Rules

**Follow these rules in all OpenTUI code:**

1. **Use `create-tui` for new projects.** See framework `README.md` quick starts.
2. **`create-tui` options must come before arguments.** `bunx create-tui -t react my-app` works, `bunx create-tui my-app -t react` does NOT.
3. **Never call `process.exit()` directly.** Use `renderer.destroy()` (see `core/gotchas.md`).
4. **Text styling requires nested tags in React/Solid.** Use modifier elements, not props (see `components/text-display.md`).

## How to Use This Skill

### Reference File Structure

Framework references follow a 5-file pattern. Cross-cutting concepts are single-file guides.

Each framework in `./references/<framework>/` contains:

| File | Purpose | When to Read |
|------|---------|--------------|
| `README.md` | Overview, when to use, quick start | **Always read first** |
| `api.md` | Runtime API, components, hooks | Writing code |
| `configuration.md` | Setup, tsconfig, bundling | Configuring a project |
| `patterns.md` | Common patterns, best practices | Implementation guidance |
| `gotchas.md` | Pitfalls, limitations, debugging | Troubleshooting |

Cross-cutting concepts in `./references/<concept>/` have `README.md` as the entry point.

### Reading Order

1. Start with `README.md` for your chosen framework
2. Then read additional files relevant to your task:
   - Building components -> `api.md` + `components/<category>.md`
   - Setting up project -> `configuration.md`
   - Layout/positioning -> `layout/README.md`
   - Troubleshooting -> `gotchas.md` + `testing/README.md`

### Example Paths

```
./references/react/README.md           # Start here for React
./references/react/api.md              # React components and hooks
./references/solid/configuration.md    # Solid project setup
./references/components/inputs.md      # Input, Textarea, Select docs
./references/core/gotchas.md           # Core debugging tips
```

### Runtime Notes

OpenTUI runs on Bun and uses Zig for native builds. Read `./references/core/gotchas.md` for runtime requirements and build guidance.

## Quick Decision Trees

### "Which framework should I use?"

```
Which framework?
├─ I want full control, maximum performance, no framework overhead
│  └─ core/ (imperative API)
├─ I know React, want familiar component patterns
│  └─ react/ (React reconciler)
├─ I want fine-grained reactivity, optimal re-renders
│  └─ solid/ (Solid reconciler)
└─ I'm building a library/framework on top of OpenTUI
   └─ core/ (imperative API)
```

### "I need to display content"

```
Display content?
├─ Plain or styled text -> components/text-display.md
├─ Container with borders/background -> components/containers.md
├─ Scrollable content area -> components/containers.md (scrollbox)
├─ ASCII art banner/title -> components/text-display.md (ascii-font)
├─ Code with syntax highlighting -> components/code-diff.md
├─ Diff viewer (unified/split) -> components/code-diff.md
└─ Line numbers with diagnostics -> components/code-diff.md
```

### "I need user input"

```
User input?
├─ Single-line text field -> components/inputs.md (input)
├─ Multi-line text editor -> components/inputs.md (textarea)
├─ Select from a list (vertical) -> components/inputs.md (select)
├─ Tab-based selection (horizontal) -> components/inputs.md (tab-select)
└─ Custom keyboard shortcuts -> keyboard/README.md
```

### "I need layout/positioning"

```
Layout?
├─ Flexbox-style layouts (row, column, wrap) -> layout/README.md
├─ Absolute positioning -> layout/patterns.md
├─ Responsive to terminal size -> layout/patterns.md
├─ Centering content -> layout/patterns.md
└─ Complex nested layouts -> layout/patterns.md
```

### "I need animations"

```
Animations?
├─ Timeline-based animations -> animation/README.md
├─ Easing functions -> animation/README.md
├─ Property transitions -> animation/README.md
└─ Looping animations -> animation/README.md
```

### "I need to handle input"

```
Input handling?
├─ Keyboard events (keypress, release) -> keyboard/README.md
├─ Focus management -> keyboard/README.md
├─ Paste events -> keyboard/README.md
├─ Mouse events -> components/containers.md
└─ Text selection -> components/text-display.md
```

### "I need to test my TUI"

```
Testing?
├─ Snapshot testing -> testing/README.md
├─ Interaction testing -> testing/README.md
├─ Test renderer setup -> testing/README.md
└─ Debugging tests -> testing/README.md
```

### "I need to debug/troubleshoot"

```
Troubleshooting?
├─ Runtime errors, crashes -> <framework>/gotchas.md
├─ Layout issues -> layout/README.md + layout/patterns.md
├─ Input/focus issues -> keyboard/README.md
└─ Repro + regression tests -> testing/README.md
```

### Troubleshooting Index

- Terminal cleanup, crashes -> `core/gotchas.md`
- Text styling not applying -> `components/text-display.md`
- Input focus/shortcuts -> `keyboard/README.md`
- Layout misalignment -> `layout/README.md`
- Flaky snapshots -> `testing/README.md`

For component naming differences and text modifiers, see `components/README.md`.

## Product Index

### Frameworks
| Framework | Entry File | Description |
|-----------|------------|-------------|
| Core | `./references/core/README.md` | Imperative API, all primitives |
| React | `./references/react/README.md` | React reconciler for declarative TUI |
| Solid | `./references/solid/README.md` | SolidJS reconciler for declarative TUI |

### Cross-Cutting Concepts
| Concept | Entry File | Description |
|---------|------------|-------------|
| Layout | `./references/layout/README.md` | Yoga/Flexbox layout system |
| Components | `./references/components/README.md` | Component reference by category |
| Keyboard | `./references/keyboard/README.md` | Keyboard input handling |
| Animation | `./references/animation/README.md` | Timeline-based animations |
| Testing | `./references/testing/README.md` | Test renderer and snapshots |

### Component Categories
| Category | Entry File | Components |
|----------|------------|------------|
| Text & Display | `./references/components/text-display.md` | text, ascii-font, styled text |
| Containers | `./references/components/containers.md` | box, scrollbox, borders |
| Inputs | `./references/components/inputs.md` | input, textarea, select, tab-select |
| Code & Diff | `./references/components/code-diff.md` | code, line-number, diff |

## Resources

**Repository**: https://github.com/anomalyco/opentui
**Core Docs**: https://github.com/anomalyco/opentui/tree/main/packages/core/docs
**Examples**: https://github.com/anomalyco/opentui/tree/main/packages/core/src/examples
**Awesome List**: https://github.com/msmps/awesome-opentui
