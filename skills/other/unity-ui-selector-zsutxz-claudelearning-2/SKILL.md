---
name: Unity UI System Selector
description: Guides selection between UGUI and UI Toolkit for projects. Use when choosing UI framework or migrating UI systems.
---

# Unity UI System Selector

Helps you choose the appropriate UI system for your Unity project and provides implementation guidance for both UGUI and UI Toolkit.

## Two UI Systems

**UGUI (Legacy)** - GameObject-based (2014). Mature, works on all Unity versions, large community. Weaker: Complex UI performance, limited styling, no live reload.

**UI Toolkit (Modern)** - Retained mode, web-inspired UXML/USS (2021.2+). Better performance, live reload, data-binding. Weaker: Requires 2021.2+, smaller community, limited 3D world-space UI.

## Decision Framework

**Use UGUI if:**
- Unity < 2021.2
- Simple UI (menus, HUD)
- 3D world-space UI needed
- Team knows UGUI well / tight deadline
- Legacy project

**Use UI Toolkit if:**
- Unity 2021.2+ and new project (future-proof)
- Complex/data-driven UI (inventory, skill trees)
- Editor tools (inspectors, windows) - **strongly recommended**
- Web dev background (HTML/CSS)
- Large-scale UI (MMO, strategy games)

When in doubt: For new projects on Unity 2021.2+, **UI Toolkit is recommended**.

## Comparison

| Feature | UGUI | UI Toolkit |
|---------|------|-----------|
| **Version** | 4.6+ | 2021.2+ |
| **Performance** | Simple UIs | All UIs |
| **Styling** | Inspector | CSS-like USS |
| **Layout** | Manual/Groups | Flexbox-like |
| **Editor Tools** | Good | Excellent |
| **Runtime UI** | Excellent | Good |
| **3D World UI** | Excellent | Limited |

## Migration

See [migration-guide.md](migration-guide.md) for UGUI → UI Toolkit migration strategy (3-4 months for medium projects).

## UI System Support Matrix

| Unity Version | UGUI | UI Toolkit (Editor) | UI Toolkit (Runtime) |
|--------------|------|-------------------|---------------------|
| 2019.4 LTS | ✅ Full | ✅ Basic | ❌ No |
| 2020.3 LTS | ✅ Full | ✅ Good | ⚠️ Experimental |
| 2021.3 LTS | ✅ Full | ✅ Excellent | ✅ Production |
| 2022.3 LTS+ | ✅ Full | ✅ Primary | ✅ Full |

## When to Use vs Other Components

**Use this Skill when**: Choosing between UGUI and UI Toolkit, understanding UI system trade-offs, or planning UI migration

**Use @unity-scripter agent when**: Implementing UI components, writing custom UI scripts, or converting UI code

**Use @unity-architect agent when**: Designing complex UI architecture, planning UI data flow, or structuring large-scale UI systems

**Use /unity:new-script command when**: Generating Editor scripts with UI Toolkit or UGUI templates

## Related Skills

- **unity-uitoolkit**: Assists with UI Toolkit implementation (UXML, USS, VisualElement API)
- **unity-template-generator**: Generates Editor scripts using selected UI system
- **unity-script-validator**: Validates UI code patterns
