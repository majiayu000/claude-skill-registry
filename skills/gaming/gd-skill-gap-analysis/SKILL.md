---
name: gd-skill-gap-analysis
description: Analyzes worker pain points to identify missing skills and create skill proposals. Use during playtest GDD review phase when workers report repeated struggles with specific patterns, retrospective pain points indicate missing knowledge, questions about implementation approaches recur, or technical decisions are delayed due to uncertainty.
---

# Skill Gap Analysis

## The Skill Gap Analysis Process

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SKILL GAP ANALYSIS WORKFLOW                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Step 1: COLLECT PAIN POINTS                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ • Read retrospective.txt pain point sections                          │   │
│  │ • Review worker message history                                       │   │
│  │ • Identify repeated questions                                         │   │
│  │ • Note "had to figure out" comments                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  Step 2: CATEGORIZE GAPS                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ • Pattern gaps (dev-patterns-*)                                      │   │
│  │ • Integration gaps (dev-integration-*)                               │   │
│  │ • Performance gaps (dev-performance-*)                               │   │
│  │ • Visual/Shader gaps (ta-shader-*, ta-r3f-*)                         │   │
│  │ • Reference gaps (gd-*, gamedesigner-reference)                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  Step 3: CHECK EXISTING SKILLS                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ • Search .claude/skills/ for similar skills                          │   │
│  │ • Check if gap is actually covered                                   │   │
│  │ • Determine if existing skill needs update vs new skill              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  Step 4: PROPOSE SKILL STRUCTURE                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ • Name following convention: {agent}-{category}-{specific}           │   │
│  │ • Description: Clear purpose statement                               │   │
│  │ • Category: gamedesign|developer|techartist|qa|shared               │   │
│  │ • Content: Outline with examples                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  Step 5: INCLUDE IN PLAYTEST REPORT                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Pain Point to Skill Mapping

### Developer Pattern Gaps

| Pain Point                                 | Skill Proposal                | Priority |
| ------------------------------------------ | ----------------------------- | -------- |
| "Unsure how to implement X pattern"        | dev-patterns-{x}              | HIGH     |
| "Don't know React Three Fiber way to do Y" | dev-r3f-{y}                   | HIGH     |
| "Had to guess state management approach"   | dev-patterns-state-management | MEDIUM   |
| "Unclear how to handle Z edge case"        | dev-patterns-{z}-edge-cases   | MEDIUM   |

### Tech Artist Visual Gaps

| Pain Point                               | Skill Proposal                       | Priority |
| ---------------------------------------- | ------------------------------------ | -------- |
| "Shader doesn't match visual spec"       | ta-shader-{effect}-examples          | HIGH     |
| "Don't know R3F material approach for X" | ta-r3f-materials-{x}                 | HIGH     |
| "Performance issues with particles"      | ta-performance-particle-optimization | MEDIUM   |
| "Unsure how to achieve visual style Y"   | ta-visual-{style}-patterns           | MEDIUM   |

### Game Designer Reference Gaps

| Pain Point                      | Skill Proposal           | Priority |
| ------------------------------- | ------------------------ | -------- |
| "Reference image unclear for X" | gd-visual-reference-{x}  | MEDIUM   |
| "Need examples of Y mechanic"   | gd-mechanic-examples-{y} | MEDIUM   |
| "Unclear design intent for Z"   | gd-design-rationale-{z}  | LOW      |

## Skill Proposal Template

````markdown
---
name: {agent}-{category}-{specific}
description: {Clear one-line description of skill purpose}
category: {gamedesign|developer|techartist|qa|shared}
---

# {Skill Title}

## Overview

{Describe what this skill enables workers to do}

## When to Use This Skill

Use when:

- {Trigger condition 1}
- {Trigger condition 2}
- {Trigger condition 3}

## Problem Being Solved

**Original Pain Point:**

> "{Quote from retrospective about the struggle}"

**Root Cause:**
{Analysis of why the struggle occurred}

**Solution:**
{How this skill solves the problem}

## Examples

### Example 1: {Context}

```typescript
// Before: Worker had to figure this out
// {What worker did before}

// After: Worker has clear pattern
// {What skill provides}
```
````

### Example 2: {Context}

{Another concrete example}

## Common Pitfalls

| Pitfall     | Why It's Bad  | Correct Approach |
| ----------- | ------------- | ---------------- |
| {Pitfall 1} | {Explanation} | {Solution}       |
| {Pitfall 2} | {Explanation} | {Solution}       |

## Related Skills

- {agent}-{related-skill-1}
- {agent}-{related-skill-2}

## Version

- 1.0.0 - Initial creation from playtest {taskId} retrospective

````

## Example Skill Proposals

### Example 1: Friction Transition Pattern

**Pain Point:** "Workers struggled with smooth transitions between friction surfaces. Character snapped between speeds."

**Skill Proposal:** `dev-patterns-friction-transition`

```markdown
---
name: dev-patterns-friction-transition
description: Smooth player movement transitions between surface friction types
category: developer
---

# Friction Transition Patterns

## Overview

Patterns for smooth player movement when transitioning between surfaces with different friction values (your paint, enemy paint, neutral).

## When to Use This Skill

Use when implementing:
- Paint friction system
- Surface-based movement modifiers
- Any friction/speed change on surface change

## The Smooth Transition Formula

```typescript
// Smooth friction transition over 100ms
interface FrictionTransition {
  from: SurfaceType;
  to: SurfaceType;
  startTime: number;
  duration: number; // 100ms
}

function updateFrictionTransition(
  current: FrictionTransition,
  deltaTime: number
): number {
  const elapsed = performance.now() - current.startTime;
  const t = Math.min(elapsed / current.duration, 1);
  // Cubic ease in-out for natural feel
  const ease = t < 0.5
    ? 4 * t * t * t
    : 1 - Math.pow(-2 * t + 2, 3) / 2;

  return lerp(getFriction(current.from), getFriction(current.to), ease);
}
````

## Momentum Preservation

When surface changes, preserve 80% of current momentum:

```typescript
const preservedVelocity = currentVelocity.clone().multiplyScalar(0.8);
const newDirection = getMovementDirection();
targetVelocity = preservedVelocity.add(
  newDirection.multiplyScalar(maxSpeed * surfaceSpeedModifier)
);
```

## Common Pitfalls

| Pitfall              | Why                            | Fix                                   |
| -------------------- | ------------------------------ | ------------------------------------- |
| Instant snap         | Jarring feel, breaks immersion | Use 100ms blend                       |
| Losing all momentum  | Player feels stuck             | Preserve 80%                          |
| No client prediction | Laggy feel                     | Predict on client, validate on server |

````

### Example 2: Visual Reference for Territory Colors

**Pain Point:** "Tech Artist unsure about exact territory colors and patterns. Multiple revisions needed."

**Skill Proposal:** `gd-visual-reference-territory`

```markdown
---
name: gamedesigner-visual-reference-territory
description: Visual specifications for territory colors and patterns
category: gamedesign
---

# Territory Visual Reference

## Color Specifications

| Team | Hex Color | RGB | Use Case |
|------|-----------|-----|----------|
| Orange | #FF6B35 | (255, 107, 53) | Orange paint, territory |
| Blue | #4A90D9 | (74, 144, 217) | Blue paint, territory |
| Neutral | #808080 | (128, 128, 128) | Unpainted surface |

## Pattern Specifications

### Orange Team Pattern
- Type: Diagonal stripes
- Angle: 45 degrees
- Spacing: 10px between lines
- Line width: 2px
- Opacity: 70% over base color

### Blue Team Pattern
- Type: Polka dots
- Dot radius: 5px
- Spacing: 15px between dots (grid)
- Opacity: 70% over base color

### Reference Images

See: `docs/design/images-references/territory/`
- `orange-stripes.png` - Diagonal stripe pattern
- `blue-dots.png` - Polka dot pattern
- `territory-comparison.png` - Side by side comparison

## Accessibility

Patterns are PRIMARY differentiation, colors are secondary. All modes playable without color.

## Implementation Example

```typescript
const TERRITORY_PATTERNS = {
  orange: {
    type: 'stripes',
    angle: 45,
    spacing: 10,
    color: '#FF6B35'
  },
  blue: {
    type: 'dots',
    radius: 5,
    spacing: 15,
    color: '#4A90D9'
  }
};
````

````

## Skill Gap Report Template

```json
{
  "skillGaps": [
    {
      "id": "gap-001",
      "agent": "developer",
      "category": "pattern",
      "painPoint": "Workers struggled with smooth friction transitions",
      "retrospectiveQuote": "Character snapped between speeds when surface changed",
      "proposedSkill": "dev-patterns-friction-transition",
      "priority": "HIGH",
      "affectedTasks": ["P1-001", "P1-002"],
      "proposal": {
        "name": "dev-patterns-friction-transition",
        "description": "Smooth player movement transitions between surface friction types",
        "category": "developer",
        "keyContent": ["100ms blend formula", "80% momentum preservation", "Client prediction pattern"]
      }
    }
  ],
  "existingSkillsNeedingUpdate": [
    {
      "skill": "dev-r3f-r3f-physics",
      "issue": "Missing friction surface integration example",
      "proposedAddition": "Add friction system integration section"
    }
  ]
}
````

## Priority Guidelines

| Priority | Criteria                               | Examples                    |
| -------- | -------------------------------------- | --------------------------- |
| CRITICAL | Blocks multiple tasks, safety/security | dev-multiplayer-anti-cheat  |
| HIGH     | Causes delays, repeated questions      | dev-patterns-{core-system}  |
| MEDIUM   | Improves quality, reduces revisions    | ta-visual-{style}-patterns  |
| LOW      | Nice to have, edge cases               | gd-mechanic-examples-{rare} |

## Integration with PM Skill Research

When skill gaps are identified:

1. **Document gaps** in playtest report
2. **PM reviews** during skill_research phase
3. **PM uses skill-researcher** to:
   - Verify gap isn't already covered
   - Research best practices
   - Create/update skill files
4. **Skills committed** before next task assignment

## Quality Gates

Before submitting skill gap proposal:

- [ ] Pain points clearly quoted from retrospective
- [ ] Root cause identified
- [ ] Existing skills checked for coverage
- [ ] Skill name follows convention
- [ ] Category correctly assigned
- [ ] At least 2 examples provided
- [ ] Common pitfalls documented
- [ ] Related skills referenced
- [ ] Priority justified by impact
