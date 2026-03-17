---
name: planning-guide
agent: explore
context: fork
description: "Planning philosophy, patterns, and practices for implementation planning. Use when planning features, architectural changes, or refactoring. Provides L'Entonnoir, 2-3 task rule, and verification practice. Not for execution - use native Plan agent with this guide for context."
---

<mission_control>
<objective>Create actionable implementation plans through L'Entonnoir, quality-first breakdown, and evidence-based verification.</objective>
<success_criteria>Plan created with 2-3 tasks max, file:line evidence, and executable prompts</success_criteria>
</mission_control>

# Planning Guide

**Philosophy and patterns for creating actionable implementation plans**

## What This Provides

This guide contains planning philosophy that the native Plan agent lacks:

- **L'Entonnoir (The Funnel)**: Iterative narrowing through recognition-based questions
- **2-3 Task Rule**: Quality-first planning with aggressive atomicity
- **Verification Practice**: Evidence-based planning with file:line claims
- **Plan Format**: Standard template for executable prompts

## Quick Start

**Apply planning philosophy for actionable implementation plans:**

1. **If you need scope definition:** Use L'Entonnoir → Ask recognition-based questions → Result: Clear boundaries
2. **If you need task breakdown:** Apply 2-3 task rule → Split if exceeds 3 → Result: Atomic, executable tasks
3. **If you need verification:** Trace actual code → Provide file:line evidence → Result: Evidence-based claims

**Why:** Quality-first planning with aggressive atomicity prevents scope creep and maintains peak quality throughout execution.

## L'Entonnoir (The Funnel) Pattern

**Iterative narrowing through exploration and inference:**

```
EXPLORE → INFER → NARROW → VERIFY → CONTINUE
```

**How it works:**

1. **EXPLORE first** - Read files, analyze codebase, check git history
2. **INFER** - Trust ability to understand from exploration
3. **NARROW** - Refine scope based on findings
4. **VERIFY** - Confirm understanding through additional exploration
5. **CONTINUE** - Proceed when scope is clear

**Sequential focus:** Explore → Infer → Narrow → Verify → Execute. Trust native inference capabilities.

## Planning Principles

## Navigation

| If you need...        | Read...                                             |
| :-------------------- | :-------------------------------------------------- |
| Scope definition      | ## Quick Start → scope definition                   |
| Task breakdown        | ## Quick Start → task breakdown                     |
| Evidence-based claims | ## Quick Start → verification                       |
| L'Entonnoir pattern   | ## L'Entonnoir (The Funnel) Pattern                 |
| 2-3 task rule         | ## Planning Principles → Quality Over Consolidation |
| Plan format template  | See Plan Format Template section                    |

### Quality Over Consolidation

- Maximum 3 tasks per plan
- Plans are executable prompts, not documentation
- Each task must have clear completion criteria
- Dependencies and risks documented upfront

### The 2-3 Task Rule

**Every plan SHOULD contain 2-3 tasks maximum.**

**Why quality degrades with scope:**

| Context Position | Quality Level                              |
| ---------------- | ------------------------------------------ |
| Task 1 (0-15%)   | Peak quality, comprehensive                |
| Task 2 (15-35%)  | Still peak zone, quality maintained        |
| Task 3 (35-50%)  | Beginning pressure, natural stopping point |
| Task 4+ (50%+)   | DEGRADATION ZONE - quality crash           |

**Split when exceeding:** If a plan exceeds 50% context or has 4+ tasks, break it into multiple plans.

**Examples:**

```
❌ 08-01-PLAN.md: "Complete Authentication" (8 tasks, 80% context)
✅ 08-01-PLAN.md: "Auth Database Models" (2 tasks)
✅ 08-02-PLAN.md: "Auth API Core" (3 tasks)
✅ 08-03-PLAN.md: "Auth UI Components" (2 tasks)
```

**Aggressive atomicity:** More plans, smaller scope, consistent quality.

## Planning Process

### 1. Requirements Analysis

- Understand the feature request completely
- Ask ONE clarifying question if needed
- Identify success criteria
- List assumptions and constraints

### 2. Architecture Review

- Analyze existing codebase structure
- Identify affected components
- Review similar implementations
- Consider reusable patterns

### 3. Step Breakdown

Create detailed steps with:

- Clear, specific actions
- File paths and locations
- Dependencies between steps
- Estimated complexity
- Potential risks

**Multiple plans if needed:** If more than 3 tasks are needed, create multiple plans.

### 4. Implementation Order

- Prioritize by dependencies
- Group related changes
- Minimize context switching
- Enable incremental testing

## Plan Format Template

```markdown
# Implementation Plan: [Feature Name]

## Overview

[2-3 sentence summary]

## Requirements

- [Requirement 1]
- [Requirement 2]

## Architecture Changes

- [Change 1: file path and description]
- [Change 2: file path and description]

## Implementation Steps

### Phase 1: [Phase Name]

1. **[Step Name]** (File: path/to/file.ts)
   - Action: Specific action to take
   - Why: Reason for this step
   - Dependencies: None / Requires step X
   - Risk: Low/Medium/High

2. **[Step Name]** (File: path/to/file.ts)
   ...

### Phase 2: [Phase Name]

...

## Testing Strategy

- Unit tests: [files to test]
- Integration tests: [flows to test]
- E2E tests: [user journeys to test]

## Risks & Mitigations

- **Risk**: [Description]
  - Mitigation: [How to address]

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2
```

## Verification Practice

- Always explore codebase before planning
- Trace actual patterns, never assume
- Provide specific file:line evidence for architectural decisions
- Mark claims as VERIFIED/INFERRED/UNCERTAIN

## Refactoring Planning

When planning refactors:

1. Identify code smells and technical debt
2. List specific improvements needed
3. Preserve existing functionality
4. Create backwards-compatible changes when possible
5. Plan for gradual migration if needed

## Red Flags to Check

- Large functions (>50 lines)
- Deep nesting (>4 levels)
- Duplicated code
- Missing error handling
- Hardcoded values
- Missing tests
- Performance bottlenecks

## Operational Patterns

This guide follows these behavioral patterns:

- **Planning**: Switch to planning mode for architectural work
- **Delegation**: Add guide context when delegating to specialized workers
- **Tracking**: Maintain a visible task list for planning phases

Trust native tools to fulfill these patterns. The System Prompt selects the correct implementation.

## Progressive Disclosure

**Tier 1: Quick Planning** (simple changes)

- Basic step breakdown
- File locations
- Testing checklist

**Tier 2: Detailed Planning** (complex features)

- Full architecture review
- Risk assessment
- Dependency mapping
- Rollback strategy

**Tier 3: Comprehensive Planning** (major refactors)

- Migration strategy
- Backwards compatibility
- Performance impact
- Documentation updates

---

## Common Mistakes to Avoid

### Mistake 1: More Than 3 Tasks

❌ **Wrong:**
"Plan has 10 tasks covering 5 features" → Context overflow, confusion

✅ **Correct:**
"Plan has 2-3 tasks for one feature" → Clear scope, focused execution

### Mistake 2: Vague Task Descriptions

❌ **Wrong:**
"Implement authentication" → Unclear what exactly to do

✅ **Correct:**
"Create auth service with login/logout, add unit tests" → Specific, measurable

### Mistake 3: Skipping Evidence

❌ **Wrong:**
"Changes look complete" → No file:line verification

✅ **Correct:**
"Modified auth.ts:47-89, verified tests at auth.test.ts:23-156"

### Mistake 4: Ignoring Verification Criteria

❌ **Wrong:**
Tasks without completion criteria → Never know when done

✅ **Correct:**
Each task has explicit verification criteria (test passes, type check succeeds)

### Mistake 5: Scattered Questions

❌ **Wrong:**
"Ask multiple unrelated questions at once" → User overwhelmed

✅ **Correct:**
ONE focused question at a time using L'Entonnoir pattern

---

## Validation Checklist

Before claiming plan complete:

**Scope:**
- [ ] Feature scope clearly defined with boundaries
- [ ] L'Entonnoir applied for scope narrowing
- [ ] Out-of-scope items documented

**Tasks:**
- [ ] Maximum 3 tasks (2-3 task rule)
- [ ] Each task atomic and independently verifiable
- [ ] Task descriptions specific and actionable
- [ ] Each task has clear completion criteria

**Evidence:**
- [ ] File locations identified with file:line references
- [ ] Code changes traced to specific locations
- [ ] Existing patterns identified for consistency

**Quality:**
- [ ] Dependencies documented between tasks
- [ ] Risks identified upfront
- [ ] Verification criteria explicit for each task

**Format:**
- [ ] Plan uses standard template
- [ ] Tasks are executable prompts
- [ ] Progressive disclosure appropriate to complexity

---

## Best Practices Summary

✅ **DO:**
- Apply L'Entonnoir for iterative scope narrowing
- Limit plans to 2-3 tasks maximum
- Provide file:line evidence for all claims
- Define clear completion criteria for each task
- Document dependencies and risks upfront
- Use recognition-based questions (2-4 options)

❌ **DON'T:**
- Create plans with >3 tasks
- Use vague task descriptions without specifics
- Skip verification criteria
- Ask scattered questions without focus
- Ignore evidence-based claims
- Create documentation instead of executable prompts

---

## Genetic Code

This component carries essential Seed System principles for context fork isolation:

<critical_constraint>
**System Physics:**

1. Zero external dependencies (portability invariant)
2. Description uses What-When-Not-Includes format in third person
3. Progressive disclosure - core in SKILL.md, details in references/
4. XML for control (mission_control, critical_constraint), Markdown for data
   </critical_constraint>

## Recognition Questions

| Question | Recognition |
| :------- | :---------- |
| Would Claude know this without being told? | Delete (zero delta) |
| Can this work standalone? | Fix if no (non-self-sufficient) |
| Did I read the actual file, or just see it in grep? | Verify before claiming |

---

## Validation Checklist

Before claiming planning complete:

- [ ] Architecture creates dependency graph
- [ ] Phases identified with 2-3 tasks each
- [ ] Parallel opportunities identified
- [ ] Verification strategy defined

---

<critical_constraint>
