---
name: ipados
description: iPadOS platform-specific development with adaptive layouts, keyboard shortcuts, multitasking, and Stage Manager. Use when building iPad apps with split views, external keyboard support, or multi-window features.
versions:
  ipados: 26
user-invocable: false
references: references/adaptive-layouts.md, references/keyboard-shortcuts.md, references/multitasking.md
related-skills: swift-core, swiftui-core, ios, mcp-tools
---

# iPadOS Platform

iPadOS-specific development for tablet and productivity experiences.

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing iPad patterns
2. **fuse-ai-pilot:research-expert** - Verify latest iPadOS 26 docs via Context7/Exa
3. **mcp__apple-docs__search_apple_docs** - Check iPad multitasking patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Building iPad-optimized apps
- Implementing split views
- Supporting external keyboard
- Multi-window applications
- Stage Manager support
- Adaptive layouts

### Why iPadOS Skill

| Feature | Benefit |
|---------|---------|
| Split View | Side-by-side apps |
| Keyboard shortcuts | Productivity |
| Stage Manager | Desktop-like experience |
| Adaptive layouts | All iPad sizes |

---

## Reference Guide

| Need | Reference |
|------|-----------|
| Size classes, split views | [adaptive-layouts.md](references/adaptive-layouts.md) |
| External keyboard support | [keyboard-shortcuts.md](references/keyboard-shortcuts.md) |
| Slide Over, Stage Manager | [multitasking.md](references/multitasking.md) |

---

## Best Practices

1. **Size class adaptation** - Support compact and regular
2. **Keyboard shortcuts** - ⌘ shortcuts for productivity
3. **Drag and drop** - Enable data transfer
4. **Pointer support** - Mouse/trackpad cursors
5. **Multi-window** - Support multiple instances
6. **External display** - UIScreen support
