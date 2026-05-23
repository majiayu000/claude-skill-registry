---
name: ralph-router
description: Routes to appropriate Ralph skills based on agent role and task signals
category: orchestration
---

# Ralph Skill Router

> "Right skill for the right agent at the right time."

## When to Use This Skill

Use at:

- Agent startup to load appropriate skills
- Task assignment to determine required skills
- Retrospective to identify skill gaps

## Quick Route

### By Agent Role

| Agent        | Core Skills                                                                                                                                               | Checklists                                             |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| PM           | `task-selection`, `retrospective`, `skill-improvement`, `scale-adaptive`                                                                                  | `prd-validation`, `task-handoff`                       |
| Developer    | `r3f-fundamentals`, `feedback-loops`, `typescript-patterns`                                                                                               | `pre-commit`, `code-quality`                           |
| QA           | `validation-workflow`, `browser-testing`, `bug-reporting`                                                                                                 | `validation-checks`                                    |
| GameDesigner | `gdd-creation`, `thermite-integration`, `mechanic-design`, `level-design`, `character-design`, `weapon-design`, `game-loop-design`, `playtest-validation` | `gdd-review`, `design-validation`                      |
| TechArtist   | `r3f-fundamentals`, `r3f-materials`, `r3f-geometry`, `shader-sdf`, `postfx-effects`, `particles-gpu`, `feedback-loops`, `typescript-patterns`             | `asset-quality`, `shader-review`, `visual-consistency` |

### By Task Category

| Category        | Developer Skills                          | QA Focus              | TechArtist Skills                               |
| --------------- | ----------------------------------------- | --------------------- | ----------------------------------------------- |
| `architectural` | `typescript-patterns`, `r3f-fundamentals` | Full validation suite | `typescript-patterns`, `r3f-fundamentals`       |
| `integration`   | Domain-specific (physics, materials)      | Cross-browser testing | `r3f-materials`, shader integration             |
| `functional`    | `r3f-fundamentals`, `feedback-loops`      | Acceptance criteria   | -                                               |
| `visual`        | -                                         | Visual QA             | `r3f-materials`, `shader-sdf`, `postfx-effects` |
| `shader`        | -                                         | Shader testing        | `shader-sdf`, `glsl`, `gpu-cost-optimizer`      |
| `effects`       | -                                         | Effects testing       | `particles-gpu`, `postfx-effects`               |
| `ui-polish`     | -                                         | UI testing            | `r3f-materials`, `visual-polish`                |
| `polish`        | `r3f-materials`, `r3f-performance`        | Visual + performance  | `r3f-materials`, `postfx-effects`               |

### By Signal Keywords

| Signal in Task                       | Route To              |
| ------------------------------------ | --------------------- |
| "physics", "collision", "rigid body" | `r3f-physics`         |
| "shader", "material", "texture"      | `r3f-materials`       |
| "performance", "fps", "optimization" | `r3f-performance`     |
| "component", "scene", "canvas"       | `r3f-fundamentals`    |
| "type", "interface", "generic"       | `typescript-patterns` |

## Routing Protocol

### Step 1: Identify Agent Role

```javascript
const role =
  state.agents[agentName].terminal === 'coordinator'
    ? 'pm'
    : agentName === 'developer'
      ? 'developer'
      : 'qa';
```

### Step 2: Load Core Skills

```markdown
## Core Skills for {{ROLE}}

Load these skills for every session:

### PM Core

- agents/pm/skills/task-selection.md
- agents/pm/skills/retrospective.md
- agents/pm/skills/scale-adaptive.md
- agents/pm/checklists/prd-validation.md
- agents/pm/checklists/task-handoff.md
- agents/pm/references/state-files.md

### Developer Core

- agents/developer/skills/feedback-loops.md
- agents/developer/skills/typescript-patterns.md
- agents/developer/checklists/pre-commit.md
- agents/developer/checklists/code-quality.md

### QA Core

- agents/qa/skills/validation-workflow.md
- agents/qa/skills/browser-testing.md
- agents/qa/skills/bug-reporting.md
- agents/qa/checklists/validation-checks.md
```

### Step 3: Load Domain Skills (Developer Only)

Based on task signals:

```javascript
function getDomainSkills(task) {
  const skills = [];
  const text = `${task.title} ${task.description}`.toLowerCase();

  // R3F/Three.js signals
  if (/physics|collision|rapier|rigid/.test(text)) {
    skills.push('agents/developer/skills/r3f-physics.md');
  }
  if (/shader|material|texture|pbr/.test(text)) {
    skills.push('agents/developer/skills/r3f-materials.md');
  }
  if (/performance|fps|optimize|mobile/.test(text)) {
    skills.push('agents/developer/skills/r3f-performance.md');
  }
  if (/scene|component|canvas|drei/.test(text)) {
    skills.push('agents/developer/skills/r3f-fundamentals.md');
  }

  // Always include fundamentals for R3F tasks
  if (skills.length > 0 && !skills.includes('r3f-fundamentals.md')) {
    skills.unshift('agents/developer/skills/r3f-fundamentals.md');
  }

  return skills;
}
```

## Common Skill Combinations

### Game Feature Development

```
r3f-fundamentals + r3f-physics + feedback-loops + pre-commit
```

### Visual Polish

```
r3f-fundamentals + r3f-materials + r3f-performance + pre-commit
```

### Performance Optimization

```
r3f-performance + r3f-materials + pre-commit
```

### New Component

```
r3f-fundamentals + typescript-patterns + code-quality + pre-commit
```

## Skill Dependencies

```
r3f-materials ──────┐
                    ├──▶ r3f-fundamentals
r3f-physics ────────┤
                    │
r3f-performance ────┘

validation-workflow ──┬──▶ browser-testing
                      └──▶ bug-reporting

retrospective ────────────▶ skill-improvement
```

## Reference

- [agents/pm/AGENT.md](../../pm/AGENT.md) — PM full instructions
- [agents/developer/AGENT.md](../../developer/AGENT.md) — Developer full instructions
- [agents/qa/AGENT.md](../../qa/AGENT.md) — QA full instructions
- [agents/gamedesigner/AGENT.md](../../gamedesigner/AGENT.md) — Game Designer full instructions
- [agents/techartist/AGENT.md](../../techartist/AGENT.md) — Tech Artist full instructions
- [.claude/skills/r3f-router.md](../../../.claude/skills/r3f-router.md) — R3F-specific routing
