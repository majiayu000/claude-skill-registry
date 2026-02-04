---
name: visionos
description: visionOS platform-specific development with spatial computing, RealityKit, immersive spaces, and volumes. Use when building Vision Pro apps, 3D experiences, or mixed reality features.
versions:
  visionos: 26
user-invocable: false
references: references/spatial-computing.md, references/realitykit.md, references/ornaments.md
related-skills: swift-core, swiftui-core, mcp-tools
---

# visionOS Platform

visionOS-specific development for Apple Vision Pro spatial computing.

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing visionOS patterns
2. **fuse-ai-pilot:research-expert** - Verify latest visionOS 26 docs via Context7/Exa
3. **mcp__apple-docs__search_apple_docs** - Check spatial computing patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Building Vision Pro applications
- Creating 3D spatial experiences
- Mixed reality features
- Immersive environments
- Hand and eye tracking

### Why visionOS Skill

| Feature | Benefit |
|---------|---------|
| Spatial computing | 3D interaction |
| RealityKit | 3D content rendering |
| Immersive spaces | Full environment |
| Volumes | 3D bounded content |

---

## Scene Types

| Scene | Description |
|-------|-------------|
| WindowGroup | 2D windows in space |
| Volume | 3D bounded content |
| ImmersiveSpace | Full immersive experience |

---

## Reference Guide

| Need | Reference |
|------|-----------|
| Windows, volumes, spaces | [spatial-computing.md](references/spatial-computing.md) |
| RealityView, 3D content | [realitykit.md](references/realitykit.md) |
| Attachments, UI ornaments | [ornaments.md](references/ornaments.md) |

---

## Best Practices

1. **Start with windows** - Familiar 2D first
2. **Add depth gradually** - Volumes for 3D
3. **Use ornaments** - Attach 2D UI to 3D
4. **Respect space** - Don't overwhelm user
5. **Hand tracking** - Natural interactions
6. **Eye comfort** - Avoid rapid movements
