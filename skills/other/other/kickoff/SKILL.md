---
name: superspec:kickoff
description: |
  Fast-track from idea to implementation-ready plan in one session.
  Combines brainstorm (4 phases) + validate + plan into a single flow.
  Use for small-to-medium features that don't need separate review points.
---

# Kickoff: Idea to Plan in One Session

## Overview

A streamlined flow that takes you from initial idea to implementation-ready plan.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        /superspec:kickoff                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Phase 1: EXPLORE (interactive)                                             │
│   └─→ Understand problem, ask questions, visualize                          │
│                                                                              │
│   Phase 2: PROPOSE → proposal.md                                             │
│   └─→ Why + What Changes + Impact                                           │
│                                                                              │
│   Phase 3: DESIGN → design.md                                                │
│   └─→ Compare approaches, select solution                                   │
│                                                                              │
│   Phase 4: SPEC → specs/*.md                                                 │
│   └─→ Requirements + Scenarios (each becomes a test)                        │
│                                                                              │
│   ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│   AUTO: superspec validate --strict                                          │
│   └─→ Verify spec format and completeness                                   │
│                                                                              │
│   AUTO: Generate plan.md + tasks.md                                          │
│   └─→ TDD implementation plan ready for execute                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Announce at start:** "I'm using the kickoff skill to take this idea from concept to implementation-ready plan."

## When to Use

**Use kickoff for:**
- Small to medium features (1-3 day implementation)
- Clear requirements that don't need extensive review
- Solo development or quick iterations
- Features where you want to move fast

**Use separate brainstorm → validate → plan for:**
- Large features (1+ week)
- Complex architectural changes
- Team review required between phases
- Breaking changes needing stakeholder approval

## The Flow

### Phase 1: EXPLORE

**Goal:** Understand the problem deeply before proposing solutions.

**Actions:**
```bash
# Check existing context
superspec list --specs    # What specs exist?
superspec list            # Any in-progress changes?
```

- Ask clarifying questions (one at a time)
- Investigate relevant code
- Visualize with ASCII diagrams
- Challenge assumptions

**Transition:** When problem is clear, move to PROPOSE.

---

### Phase 2: PROPOSE → proposal.md

**Goal:** Define Why and What (not How).

**Create:** `superspec/changes/[change-id]/proposal.md`

```markdown
# Change: [Brief Description]

## Why
[1-2 sentences - problem/opportunity]

## What Changes
- [Change 1]
- [Change 2]
- [**BREAKING** if applicable]

## Capabilities

### New Capabilities
- [capability-name]: [brief description]

### Modified Capabilities
- [existing-capability]: [what changes]

## Impact
- Affected specs: [list]
- Affected code: [key files]
```

**Transition:** When scope is confirmed, move to DESIGN.

---

### Phase 3: DESIGN → design.md

**Goal:** Define How - compare approaches and select solution.

**Create:** `superspec/changes/[change-id]/design.md`

```markdown
# Design: [Feature Name]

## Context
[Background, constraints]

## Goals / Non-Goals
- Goals: [what this achieves]
- Non-Goals: [what this excludes]

## Approaches Considered

### Approach A: [Name]
**Pros:** [advantages]
**Cons:** [disadvantages]

### Approach B: [Name]
**Pros:** [advantages]
**Cons:** [disadvantages]

## Decision
**Chosen Approach:** [A/B]
**Rationale:** [why]

## Technical Details
[Architecture, key components, data flow]
```

**Transition:** When approach is confirmed, move to SPEC.

---

### Phase 4: SPEC → specs/*.md

**Goal:** Define testable behavior - each Scenario becomes a TDD test.

**Create:** `superspec/changes/[change-id]/specs/[capability]/spec.md`

```markdown
# [Capability] Specification

## Purpose
[What this capability provides]

## Requirements

### Requirement: [Name]
The system SHALL [behavior].

#### Scenario: [Scenario Name]
- **WHEN** [trigger condition]
- **THEN** [expected result]

#### Scenario: [Another Scenario]
- **WHEN** [different condition]
- **THEN** [different result]
```

**Key Rule:** Write Scenarios like test descriptions - specific and testable.

---

### AUTO: Validate

After specs are written, automatically run:

```bash
superspec validate [change-id] --strict
```

**If validation fails:** Fix issues before proceeding to plan.

**Validation checks:**
- Every Requirement has at least one Scenario
- Scenario format is correct (`#### Scenario:`)
- MODIFIED includes full content
- REMOVED includes Reason and Migration

---

### AUTO: Generate Plan

After validation passes, generate implementation plan:

**Create:** `superspec/changes/[change-id]/plan.md`

```markdown
# [Feature] Implementation Plan

> **For Claude:** REQUIRED SKILL: Use superspec:execute to implement this plan.

**Goal:** [One sentence]
**Architecture:** [2-3 sentences]
**Tech Stack:** [Key technologies]

**Related Specs:**
- `superspec/changes/[id]/specs/[capability]/spec.md`

---

## Task 1: [Component Name]

**Spec Reference:** `### Requirement: [Name]`

**Files:**
- Create: `path/to/new-file.ts`
- Test: `tests/path/to/test.ts`

### Step 1.1: Write failing test (RED)

**Scenario:** `#### Scenario: [Name]`

```typescript
test('[Scenario Name]', async () => {
  // WHEN [condition]
  const result = await action(input);

  // THEN [result]
  expect(result).toEqual(expected);
});
```

**Run:** `npm test -- --grep "[Scenario Name]"`
**Expected:** FAIL

### Step 1.2: Implement (GREEN)

[Minimal code to pass test]

**Run:** `npm test -- --grep "[Scenario Name]"`
**Expected:** PASS

### Step 1.3: Commit

```bash
git commit -m "feat([cap]): [scenario]

Refs: superspec/changes/[id]/specs/[cap]/spec.md
Requirement: [Name]
Scenario: [Name]"
```
```

**Create:** `superspec/changes/[change-id]/tasks.md`

```markdown
# Implementation Tasks for [Change ID]

## Status
- Total Tasks: X
- Completed: 0
- In Progress: 0
- Pending: X

---

## Phase 1: [Phase Name]

- [ ] 1.1 Write test for Scenario: [name]
- [ ] 1.2 Implement [component]
- [ ] 1.3 Commit

---

## Completion Tracking

| Phase | Tasks | Completed | Status |
|-------|-------|-----------|--------|
| Phase 1 | 3 | 0 | PENDING |
| **Total** | **3** | **0** | **0%** |
```

---

## Completion Output

When kickoff completes, announce:

```
Kickoff complete! Created:

📁 superspec/changes/[change-id]/
├── proposal.md    ✓ Why + What
├── design.md      ✓ Technical approach
├── specs/         ✓ Requirements + Scenarios
│   └── [cap]/
│       └── spec.md
├── plan.md        ✓ TDD implementation plan
└── tasks.md       ✓ Task checklist

Validation: ✓ Passed

Next step: /superspec:execute to start TDD implementation
```

---

## Comparison: Kickoff vs Separate Commands

| Aspect | `/superspec:kickoff` | Separate Commands |
|--------|----------------------|-------------------|
| **Speed** | Faster, one session | Multiple sessions |
| **Review Points** | None (continuous) | After each phase |
| **Best For** | Small-medium features | Large features, team review |
| **Output** | Same documents | Same documents |

---

## Red Flags

| Warning | Problem |
|---------|---------|
| Skipping EXPLORE | May miss requirements |
| Only one approach in DESIGN | Haven't explored alternatives |
| Vague Scenarios | Can't convert to tests |
| Validation fails | Don't proceed to plan |

---

## Integration

**This skill combines:**
- `superspec:brainstorm` - Phases 1-4
- `superspec validate` - Auto-run
- `superspec:plan` - Auto-generate

**Next step after kickoff:**
- `/superspec:execute` - Start TDD implementation

**Alternative for large features:**
- Use `/superspec:brainstorm` separately
- Run `superspec validate` with team review
- Use `/superspec:plan` after approval
