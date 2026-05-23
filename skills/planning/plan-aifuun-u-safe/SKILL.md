---
name: plan
description: |
  Create or update implementation plans for features, MVPs, and milestones.
  TRIGGER when: user wants to plan a feature ("create a plan for X", "plan this feature", "how should we implement Y", "break down this task").
version: "2.1.0"
  DO NOT TRIGGER when: user wants to start an issue (use /start-issue), or just wants quick advice without detailed planning.
---

# Plan - Strategic Feature Planning

Create detailed implementation plans by analyzing requirements, architecture, and dependencies.

## Overview

This skill generates structured implementation plans for features and milestones:

**What it does:**
1. Analyzes feature requirements and scope
2. Identifies dependencies and risks
3. Designs architectural approach
4. Breaks down into concrete tasks with phases
5. Estimates timeline and complexity
6. Creates actionable checklist

**Why it's needed:**
Ad-hoc feature development leads to missed requirements, overlooked dependencies, and scope creep. Strategic planning up-front ensures all aspects are considered and provides a roadmap for implementation.

**When to use:**
- Planning a new feature or MVP
- Breaking down complex work
- Estimating effort for a milestone
- Designing architectural approach
- Creating roadmap for multi-phase work

## Workflow

### Step 1: Create Todo List

**Initialize planning tracking** using TaskCreate:

```
Task #1: Gather feature requirements
Task #2: Analyze dependencies and risks (blocked by #1)
Task #3: Design architecture (blocked by #2)
Task #4: Break down into phases (blocked by #3)
Task #5: Create task checklist (blocked by #4)
Task #6: Generate final plan document (blocked by #5)
```

After creating tasks, proceed with planning execution.

## Planning Dimensions

### 1. Requirements Analysis

Understand what needs to be built:

**Questions to answer:**
```
- What problem does this solve?
- Who will use this feature?
- What are the must-have requirements?
- What's nice-to-have vs essential?
- What are the success criteria?
- What constraints exist (time, budget, tech)?
```

**Input sources:**
- User description or argument
- Issue body if linked
- Existing documentation
- Similar features in codebase

### 2. Scope Definition

Define clear boundaries (in-scope vs out-of-scope items). Prevents feature creep and sets realistic expectations.

### 3. Dependency Mapping

Identify what's needed first: technical (libraries, infrastructure), code (refactors, migrations), and external (approvals, assets) dependencies. Identify critical path tasks that block others.

### 4. Risk Assessment

Surface potential problems early with mitigations. Categorize as high/medium/low risk and include specific mitigation strategies for each.

### 5. Architectural Design

Make key technical decisions: define data flows, components, and technology stack. Ensure alignment with existing patterns and project Pillars (if framework installed).

### 6. Phase Breakdown

Organize work into manageable phases. Each phase should have: clear goal, task list, timeline, and deliverable. Phases build on each other and are independently testable.

### 7. Task Checklist

Create concrete actionable tasks organized by category (Setup, Database, Implementation, Testing, Documentation). Each task should be specific and verifiable.

## Estimation

Provide timeline estimate (optimistic/realistic/pessimistic) and complexity assessment (low/medium/high overall, with breakdown by component).

## Plan Output Format

Generate structured markdown with: title, metadata (date, duration, complexity), overview, scope (in/out), dependencies, risks, architecture, phases (with goals and deliverables), tasks, testing strategy, success criteria, and next steps.

Save to `.claude/plans/active/[feature-name]-plan.md`

## Smart Context Integration

Leverage project context: read architecture docs, check installed Pillars (.prot/), review similar features, consider ADRs, and identify reusable patterns. Adapt plan to match project standards.

## Usage Examples

**"create a plan for adding user authentication with OAuth"**
- Analyzes requirements, defines scope, identifies dependencies
- Assesses risks, designs architecture, breaks into phases
- Generates complete plan document in ~5 minutes

**"/plan 'implement real-time notifications'"**
- Parses argument, analyzes tech options (Socket.IO vs native)
- Creates 4-phase plan with deliverables
- Saves to `.claude/plans/active/realtime-notifications-plan.md`

**"help me plan an MVP for a task management app"**
- Gathers requirements, defines MVP scope
- Creates multi-phase plan with timeline estimate
- ~10 minutes for comprehensive planning

## Integration

Works with `/start-issue` (auto-plans from issues) and `/next` (gets tasks from plan). Plans saved to `.claude/plans/active/[feature]-plan.md`, archived when done.

## Best Practices

1. **Plan before coding** - Saves time overall
2. **Be realistic** - Optimistic estimates lead to delays
3. **Identify risks early** - Mitigation is easier upfront
4. **Break into phases** - Makes progress trackable
5. **Review with team** - Catch blind spots

## Task Management

**After each planning step**, update progress:

```
Requirements gathered → Update Task #1
Dependencies analyzed → Update Task #2
Architecture designed → Update Task #3
Phases defined → Update Task #4
Tasks created → Update Task #5
Plan document generated → Update Task #6
```

Provides visibility into planning progress.

## Final Verification

**Before finalizing plan**, verify:

```
- [ ] All 6 planning tasks completed
- [ ] Scope clearly defined (in/out)
- [ ] Dependencies identified
- [ ] Risks assessed with mitigations
- [ ] Architecture designed
- [ ] Phases with deliverables
- [ ] Complete task checklist
- [ ] Realistic timeline estimate
- [ ] Plan document saved
```

Missing items indicate incomplete planning.

## Related Skills

- **/start-issue** - Creates issue plan automatically
- **/next** - Get next task from plan
- **/review** - Review implementation quality

---

**Version:** 2.1.0
**Last Updated:** 2026-03-10
**Changelog:**
- v2.1.0 (2026-03-10): Create implementation plans for issues
**Pattern:** Tool-Reference (guides planning process)
**Compliance:** ADR-001 Section 4 ✅
