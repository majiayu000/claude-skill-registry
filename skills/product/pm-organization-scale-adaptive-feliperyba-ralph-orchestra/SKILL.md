---
name: pm-organization-scale-adaptive
description: Adjust planning depth and agent behavior based on PRD complexity level
category: organization
---

# Scale-Adaptive Planning Skill

> "Right-size the process – small projects need less ceremony, large projects need more structure."

## When to Use This Skill

Use at:

- Session initialization (determine project scale)
- Each retrospective (reassess based on progress)
- When PRD size changes significantly

## Quick Start

```javascript
// Determine project scale (reads both PRD files since v3.1.0)
const prd = readJson("prd.json");
const backlog = readJson(prd.backlogFile || "prd_backlog.json");
const allItems = [...prd.items, ...backlog.backlogItems];

const taskCount = allItems.filter((i) => !i.passes).length;
const scale =
  taskCount <= 3 ? 0 : taskCount <= 8 ? 1 : taskCount <= 15 ? 2 : taskCount <= 30 ? 3 : 4;

// Apply scale-appropriate process
const config = SCALE_CONFIG[scale];
```

**Note:** Since v3.1.0, tasks are split between `prd.json` (active queue: 5 tasks) and `prd_backlog.json` (backlog: ~70 tasks). PM must read both files to get accurate task counts for scale detection.

## Decision Framework

| Scale          | Task Count | Process Depth    | Retrospective | Skill Updates      |
| -------------- | ---------- | ---------------- | ------------- | ------------------ |
| 0 - Micro      | 1-3        | Minimal          | Brief notes   | None               |
| 1 - Small      | 4-8        | Light            | Quick review  | Anti-patterns only |
| 2 - Medium     | 9-15       | Standard         | Full process  | Update relevant    |
| 3 - Large      | 16-30      | Comprehensive    | Deep analysis | Create new skills  |
| 4 - Enterprise | 31+        | Full methodology | Multi-phase   | Full skill suite   |

## Progressive Guide

### Level 0: Micro (1-3 tasks)

Minimal ceremony for tiny projects:

```markdown
## Process Adjustments

- Skip formal retrospective file
- Use inline progress notes
- No skill improvement phase
- Simple task → implement → validate → done

## State Files

- prd.json.session (minimal session state)
- prd.json.items[{taskId}] (task details)
- Skip: retrospective.txt, handoff-log.json
```

### Level 1: Small (4-8 tasks)

Light process for small projects:

```markdown
## Process Adjustments

- Brief retrospective (inline in progress.txt)
- Quick learnings capture
- Anti-pattern documentation only
- Single-pass validation

## Retrospective Format (Inline)

### [TIMESTAMP] Task Complete: {{TASK_ID}}

- Done: {{what}}
- Learned: {{key insight}}
- Watch out: {{anti-pattern if any}}
```

### Level 2: Medium (9-15 tasks)

Standard process for typical projects:

```markdown
## Process Adjustments

- Full file-based retrospective
- Agent contributions required
- Skill updates for gaps
- Risk identification

## Full Process

1. Create retrospective.txt
2. Wait for Developer + QA input
3. PM synthesis
4. Update skills if gaps found
5. Proceed to next task
```

### Level 3: Large (16-30 tasks)

Comprehensive process for complex projects:

```markdown
## Process Adjustments

- Deep retrospective analysis
- Milestone reviews every 5 tasks
- Create new skill files
- Reference folder documentation
- Risk heat map tracking

## Additional Steps

1. Milestone review at 25%, 50%, 75%
2. Create domain-specific skill files
3. Build reference documentation
4. Track technical debt
5. Velocity monitoring
```

### Level 4: Enterprise (31+ tasks)

Full methodology for large projects:

```markdown
## Process Adjustments

- Multi-phase planning
- Sprint boundaries
- Full skill suite creation
- Architectural decision records
- Quality gates

## Enterprise Features

1. Sprint planning (5-8 tasks per sprint)
2. Architectural retrospectives
3. Full skill documentation
4. Integration testing phases
5. Release milestones
```

## Scale Detection Algorithm

```javascript
function detectScale(prd, backlog) {
  // Read both files for complete task picture (v3.1.0+)
  const prd = readJson("prd.json");
  const backlog = readJson(prd.backlogFile || "prd_backlog.json");
  const allItems = [...prd.items, ...backlog.backlogItems];

  const remaining = allItems.filter((i) => !i.passes).length;
  const total = allItems.length;
  const complexity = allItems.reduce(
    (sum, i) => sum + (i.category === 'architectural' ? 3 : i.category === 'integration' ? 2 : 1),
    0
  );

  // Base scale on task count
  let scale =
    remaining <= 3 ? 0 : remaining <= 8 ? 1 : remaining <= 15 ? 2 : remaining <= 30 ? 3 : 4;

  // Adjust for complexity
  if (complexity / total > 2) scale = Math.min(4, scale + 1);

  // Adjust for dependencies
  const depCount = allItems.reduce((sum, i) => sum + i.dependencies.length, 0);
  if (depCount / total > 1.5) scale = Math.min(4, scale + 1);

  return scale;
}
```

## Anti-Patterns

❌ **DON'T:**

- Apply enterprise process to 3-task projects
- Skip retrospectives for large projects
- Ignore scale changes during project
- Use fixed process regardless of size

✅ **DO:**

- Reassess scale at each retrospective
- Adjust process depth dynamically
- Right-size documentation effort
- Scale skill updates to project size

## Checklist

At session start:

- [ ] Count remaining tasks
- [ ] Calculate complexity score
- [ ] Determine initial scale (0-4)
- [ ] Configure process depth
- [ ] Document scale in prd.json.session

At each retrospective:

- [ ] Reassess remaining tasks
- [ ] Check if scale changed
- [ ] Adjust process if needed
- [ ] Update scale in prd.json.session

## Reference

- [pm-retrospective-facilitation](../pm-retrospective-facilitation/SKILL.md) — Retrospective process
- [pm-improvement-skill-research](../pm-improvement-skill-research/SKILL.md) — Skill updates
- https://github.com/bmad-code-org/BMAD-METHOD — Scale-adaptive methodology
