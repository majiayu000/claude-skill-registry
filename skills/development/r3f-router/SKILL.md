---
name: r3f-router
description: Routes to specialized R3F skills based on task requirements
category: development
keywords: [router, r3f, react-three-fiber, threejs, routing, skills, development]
---

# R3F Skill Router

> "Route to the right R3F skill based on what you're building."

## When to Use This Skill

Use when:

- Starting an R3F/Three.js related task
- Deciding which domain skills to load
- Combining multiple skills for complex tasks

## Quick Route

| Need               | Primary Skill      | Secondary Skills                     |
| ------------------ | ------------------ | ------------------------------------ |
| Basic scene setup  | `r3f-fundamentals` | —                                    |
| Custom materials   | `r3f-materials`    | `r3f-fundamentals`                   |
| Physics simulation | `r3f-physics`      | `r3f-fundamentals`                   |
| Performance issues | `r3f-performance`  | `r3f-fundamentals`                   |
| Game feature       | `r3f-fundamentals` | `r3f-physics`, `typescript-patterns` |

## Signal Matching

### Physics Signals

Keywords: `physics`, `collision`, `collider`, `rigid body`, `rapier`, `cannon`, `force`, `impulse`, `gravity`, `sensor`, `trigger`

→ Load: `agents/developer/skills/r3f-physics.md`

### Material Signals

Keywords: `material`, `shader`, `texture`, `PBR`, `matcap`, `GLSL`, `uniform`, `fragment`, `vertex`, `transparent`, `metalness`, `roughness`

→ Load: `agents/developer/skills/r3f-materials.md`

### Performance Signals

Keywords: `performance`, `FPS`, `optimize`, `mobile`, `instance`, `LOD`, `memory`, `dispose`, `lag`, `stuttering`, `draw calls`

→ Load: `agents/developer/skills/r3f-performance.md`

### Fundamentals Signals

Keywords: `scene`, `canvas`, `mesh`, `geometry`, `component`, `useFrame`, `useThree`, `drei`, `camera`, `light`, `render`

→ Load: `agents/developer/skills/r3f-fundamentals.md`

## Routing Algorithm

```javascript
function routeR3FSkills(task) {
  const text = `${task.title} ${task.description}`.toLowerCase();
  const skills = new Set();

  // Always start with fundamentals
  skills.add('r3f-fundamentals');

  // Check for physics
  if (
    /physics|collision|collider|rigid|rapier|cannon|force|impulse|gravity|sensor|trigger/i.test(
      text
    )
  ) {
    skills.add('r3f-physics');
  }

  // Check for materials/shaders
  if (
    /material|shader|texture|pbr|matcap|glsl|uniform|fragment|vertex|transparent|metalness|roughness/i.test(
      text
    )
  ) {
    skills.add('r3f-materials');
  }

  // Check for performance
  if (
    /performance|fps|optimize|mobile|instance|lod|memory|dispose|lag|stutter|draw.?call/i.test(text)
  ) {
    skills.add('r3f-performance');
  }

  return Array.from(skills);
}
```

## Common Combinations

### 1. Vehicle Implementation

**Signals**: vehicle, physics, controls, movement

**Skills**:

- `r3f-fundamentals` — Component structure
- `r3f-physics` — Rapier integration
- `typescript-patterns` — Type-safe controls

### 2. Environment/World Building

**Signals**: terrain, environment, world, lighting

**Skills**:

- `r3f-fundamentals` — Scene composition
- `r3f-materials` — Surface materials
- `r3f-performance` — Large scene optimization

### 3. Visual Effects

**Signals**: shader, effect, particles, post-processing

**Skills**:

- `r3f-materials` — Custom shaders
- `r3f-fundamentals` — useFrame for animation
- `r3f-performance` — GPU considerations

### 4. Mobile Game

**Signals**: mobile, touch, performance, optimization

**Skills**:

- `r3f-performance` — Mobile-first optimization
- `r3f-materials` — Lightweight materials
- `r3f-fundamentals` — Efficient components

### 5. Multiplayer Features

**Signals**: multiplayer, sync, network, colyseus

**Skills**:

- `r3f-fundamentals` — Component architecture
- `typescript-patterns` — State management
- `r3f-performance` — Network-aware updates

## Skill Dependencies

```
┌──────────────────┐
│ r3f-fundamentals │ ◀─── Required base for all R3F work
└────────┬─────────┘
         │
    ┌────┴────┬──────────┐
    ▼         ▼          ▼
┌────────┐ ┌────────┐ ┌────────────┐
│ physics│ │material│ │performance │
└────────┘ └────────┘ └────────────┘
```

## Research Guides (For Test-Fix Tasks)

**Before implementing R3F test-fix tasks, check research guides for technical specifications:**

| Guide | Topics | When to Use |
|-------|--------|-------------|
| `docs/research/terrain-shader-research.md` | Terrain raymarching, SDF functions, FBM noise | Working on terrain/heightmap shaders |
| `docs/research/paint-shader-research.md` | Wet paint effects, splat decals, fresnel | Working on paint/ink shaders |
| `docs/research/weapons-loading-research.md` | Weapon models, accessories, team colors | Working on weapon rendering |
| `docs/research/character-models-research.md` | Character skins, animations, blend states | Working on character models |

**Pattern:**
1. Check task for keywords (terrain, paint, weapon, character)
2. Read corresponding research guide
3. Extract shader code examples and technical specifications
4. Apply findings to R3F implementation

## Reference Files

| Skill            | Path                                           |
| ---------------- | ---------------------------------------------- |
| R3F Fundamentals | `agents/developer/skills/r3f-fundamentals.md`  |
| R3F Materials    | `agents/developer/skills/r3f-materials.md`     |
| R3F Physics      | `agents/developer/skills/r3f-physics.md`       |
| R3F Performance  | `agents/developer/skills/r3f-performance.md`   |
| Code Patterns    | `agents/developer/references/code-patterns.md` |

## External References

For deep-dive research, use these URLs:

- https://agent-skills.md/skills/Bbeierle12/Skill-MCP-Claude/r3f-fundamentals
- https://agent-skills.md/skills/Bbeierle12/Skill-MCP-Claude/r3f-materials
- https://agent-skills.md/skills/wollfoo/setup-factory/threejs
- https://agent-skills.md/skills/samhvw8/dot-claude/3d-graphics
- https://agent-skills.md/skills/ovachiever/droid-tings/threejs-graphics-optimizer
