---
name: ta-router
description: Routes Tech Artist to domain skills based on task category and signal keywords. Use when starting Tech Artist tasks to determine which skills to load.
category: routing
---

# Tech Artist Skill Router

> "Right skill for the right visual task."

## Quick Route

### By Task Category

| Category        | Skills                                                          |
| --------------- | --------------------------------------------------------------- |
| `architectural` | `ta-r3f-fundamentals`, `ta-validation-typescript`               |
| `visual`        | `ta-r3f-materials`, `ta-shader-sdf`, `ta-vfx-postfx`            |
| `shader`        | `ta-shader-development`, `ta-shader-sdf`                        |
| `vfx`           | `ta-vfx-particles`, `ta-vfx-postfx`                             |
| `asset`         | `ta-assets-workflow`, `ta-assets-pipeline-optimization`         |
| `performance`   | `ta-r3f-performance`, `ta-r3f-physics`                          |
| `ui`            | `ta-ui-polish`, `ta-ui-debug-helpers`, `ta-ui-design-reference` |
| `figma`         | `ta-figma-integration`                                          |
| `camera`        | `ta-camera-tps`                                                 |
| `networking`    | `ta-networking-visual-feedback`                                 |

### By Signal Keywords

| Signal                                         | Route To                                         |
| ---------------------------------------------- | ------------------------------------------------ |
| "shader", "glsl", "tsl"                        | `ta-shader-development`, `ta-shader-sdf`         |
| "particle", "gpu", "instanced"                 | `ta-vfx-particles`, `ta-foliage-instancing`      |
| "postfx", "bloom", "effect"                    | `ta-vfx-postfx`                                  |
| "material", "pbr", "texture"                   | `ta-r3f-materials`                               |
| "physics", "collision", "rapier"               | `ta-r3f-physics`                                 |
| "water", "ocean", "gerstner"                   | `ta-water-shader`                                |
| "foliage", "grass", "vegetation"               | `ta-foliage-instancing`                          |
| "paint", "territory", "splat"                  | `ta-paint-territory`                             |
| **"terrain mesh", "heightmap"**                | `ta-terrain-mesh` (mesh component)               |
| **"procedural terrain", "perlin", "simplex"**  | `ta-procedural-terrain` (algorithms - RESEARCH)  |
| **"caldera", "crater", "volcano"**             | `ta-procedural-terrain` (radial terrain)         |
| **"territory grid", "cpu territory"**          | `ta-territory-grid-cpu` (server grid)            |
| **"terrain testing", "e2e terrain"**           | `ta-terrain-testing` (E2E patterns)              |
| **"figma", "design reference", "ui design"**   | `ta-figma-integration`, `ta-ui-design-reference` |
| **"ut3", "unreal tournament", "carbon fiber"** | `ta-ui-design-reference` (UT3 aesthetic)         |

### Common Combinations

| Task Type            | Skills                                                        |
| -------------------- | ------------------------------------------------------------- |
| Shader Development   | `ta-r3f-fundamentals` + `ta-shader-development`               |
| VFX Creation         | `ta-r3f-fundamentals` + `ta-vfx-particles` + `ta-vfx-postfx`  |
| Asset Pipeline       | `ta-r3f-fundamentals` + `ta-assets-workflow`                  |
| Material Creation    | `ta-r3f-fundamentals` + `ta-r3f-materials`                    |
| Terrain System (NEW) | `ta-r3f-fundamentals` + `ta-terrain-mesh` + `ta-water-shader` |

## Research Guides

**Before creating assets, check ./src/assets/index.md**

## GDD Research

**Before creating, always read the GDD specs**

## Skill Hierarchy

```
                    ta-r3f-fundamentals (BASE)
                              |
        +---------------------+---------------------+
        |                     |                     |
   ta-r3f-materials     ta-r3f-physics       ta-r3f-performance
        |                     |                     |
   ta-shader-*          ta-camera-tps         ta-vfx-*
   ta-ui-*
```
