---
name: roadmap-backcast
description: Use when planning with fixed deadline or target outcome, working backward from future goal to present, defining milestones and dependencies, mapping critical path, identifying what must happen when, planning product launches with hard dates, multi-year strategic roadmaps, event planning, transformation initiatives, or when user mentions "backcast", "work backward from", "reverse planning", "we need to launch by", "target date is", or "what needs to happen to reach".
---

# Roadmap Backcast

## Table of Contents
1. [Purpose](#purpose)
2. [When to Use](#when-to-use)
3. [What Is It](#what-is-it)
4. [Workflow](#workflow)
5. [Dependency Mapping](#dependency-mapping)
6. [Critical Path Analysis](#critical-path-analysis)
7. [Common Patterns](#common-patterns)
8. [Guardrails](#guardrails)
9. [Quick Reference](#quick-reference)

## Purpose

Roadmap Backcast helps you plan backward from a fixed goal or deadline to the present, identifying required milestones, dependencies, critical path, and feasibility constraints. It transforms aspirational targets into actionable, sequenced plans.

## When to Use

**Invoke this skill when you need to:**
- Plan toward a fixed deadline (product launch, event, compliance date)
- Work backward from strategic goal to present steps
- Map dependencies and sequencing for complex initiatives
- Identify critical path (longest sequence that determines timeline)
- Assess feasibility of ambitious timeline
- Coordinate cross-functional work toward shared milestone
- Plan multi-year transformation with interim checkpoints
- Sequence initiatives that build on each other
- Allocate resources across dependent workstreams

**User phrases that trigger this skill:**
- "We need to launch by [date]"
- "Work backward from the goal"
- "What needs to happen to reach [outcome]?"
- "Reverse plan from target"
- "Fixed deadline, what's feasible?"
- "Backcast from [future state]"
- "Critical path to delivery"

## What Is It

A backcasting roadmap that:
1. **Defines end state** (specific, measurable target outcome and date)
2. **Works backward** (what must be true one step before? And before that?)
3. **Identifies milestones** (key checkpoints with clear deliverables)
4. **Maps dependencies** (what depends on what, what can be parallel)
5. **Finds critical path** (longest chain that determines minimum timeline)
6. **Assesses feasibility** (can we realistically achieve by target date?)

**Quick example (Product Launch by Q1 2025):**
- **Target**: Product live in production for 1000 customers by Jan 31, 2025
- **T-4 weeks** (Jan 3): Beta testing with 50 customers complete, critical bugs fixed
- **T-8 weeks** (Dec 6): Feature complete, internal QA passed
- **T-12 weeks** (Nov 8): MVP built, core features working
- **T-16 weeks** (Oct 11): Design finalized, API contracts defined
- **T-20 weeks** (Sep 13): Requirements locked, team staffed
- **Today** (Sep 1): Feasible if no scope creep and 20% time buffer included

## Workflow

Copy this checklist and track your progress:

```
Roadmap Backcast Progress:
- [ ] Step 1: Define target outcome precisely
- [ ] Step 2: Work backward to identify milestones
- [ ] Step 3: Map dependencies and sequencing
- [ ] Step 4: Identify critical path
- [ ] Step 5: Assess feasibility and adjust
```

**Step 1: Define target outcome precisely**

State specific outcome (not vague goal), target date, success criteria. See [Common Patterns](#common-patterns) for outcome definition examples. For straightforward backcasts → Use [resources/template.md](resources/template.md).

**Step 2: Work backward to identify milestones**

Start at end, ask "what must be true just before this?" iteratively. Create 5-10 major milestones. For complex multi-year roadmaps → Study [resources/methodology.md](resources/methodology.md).

**Step 3: Map dependencies and sequencing**

Identify what depends on what, what can run in parallel. See [Dependency Mapping](#dependency-mapping) for techniques.

**Step 4: Identify critical path**

Find longest sequence of dependent tasks (this determines minimum timeline). See [Critical Path Analysis](#critical-path-analysis).

**Step 5: Assess feasibility and adjust**

Compare required timeline to available time. Add buffers (20-30%), identify risks, adjust scope or date if needed. Self-check using `resources/evaluators/rubric_roadmap_backcast.json` before finalizing. Minimum standard: Average score ≥ 3.5.

## Dependency Mapping

**Dependency types:**

**Sequential (A → B)**: B cannot start until A completes
- Example: Design must complete before engineering starts
- Critical path impact: Extends timeline
- Mitigation: Start A as early as possible, parallelize where safe

**Parallel (A ∥ B)**: A and B can happen simultaneously
- Example: Backend and frontend development
- Critical path impact: None (if resourced)
- Benefit: Reduces overall timeline

**Converging (A, B → C)**: C requires both A and B to complete
- Example: Testing requires both code complete AND test environment ready
- Critical path impact: C waits for slower of A or B
- Mitigation: Monitor both paths, accelerate slower one

**Diverging (A → B, C)**: A enables both B and C
- Example: API contract defined enables frontend AND backend work
- Critical path impact: Delays in A delay everything downstream
- Mitigation: Prioritize A, ensure high quality to avoid rework

## Critical Path Analysis

**Critical path**: Longest sequence of dependent tasks (determines minimum project duration)

**Finding critical path:**
1. List all milestones with durations
2. Draw dependency graph (arrows from prerequisite to dependent)
3. Calculate earliest start/finish for each milestone (forward pass)
4. Calculate latest start/finish for each milestone (backward pass)
5. Milestones with zero slack (earliest = latest) are on critical path

**Example:**
```
Milestone A (4 weeks) → Milestone B (6 weeks) → Milestone D (2 weeks) = 12 weeks (critical path)
Milestone A (4 weeks) → Milestone C (3 weeks) → Milestone D (2 weeks) = 9 weeks (non-critical, 3 weeks slack)
```

**Critical path is 12 weeks** (A→B→D path)

**Managing critical path:**
- **Monitor closely**: Delays on critical path directly delay project
- **Add buffer**: 20-30% to critical path tasks (Murphy's Law)
- **Resource priority**: Staff critical path first
- **Fast-track**: Can non-critical work be delayed to help critical path?
- **Crash**: Add resources to shorten critical path (diminishing returns, Brook's Law applies)

## Common Patterns

**Pattern 1: Product Launch with Fixed Date**
- **Target**: Product live by date, serving customers
- **Key milestones (backward)**: GA launch, beta testing, feature freeze, alpha testing, MVP, design complete, requirements locked
- **Critical path**: Usually design → engineering → testing (sequential)
- **Buffer**: 20-30% on engineering (unknowns), 20% on testing (bugs)

**Pattern 2: Compliance Deadline (Regulatory)**
- **Target**: Compliant by regulatory deadline (cannot slip)
- **Key milestones**: Audit passed, controls implemented, policies updated, gap analysis complete
- **Critical path**: Gap analysis → remediation → validation
- **Buffer**: 40%+ (regulatory risk intolerant, build extra time)

**Pattern 3: Strategic Transformation (Multi-Year)**
- **Target**: Future state vision (e.g., "Cloud-native architecture by 2027")
- **Key milestones (annual)**: Year 3 (full migration), Year 2 (50% migrated), Year 1 (pilot complete), Year 0 (strategy approved)
- **Critical path**: Foundation work (pilot, learnings) enables scale
- **Buffer**: 30%+ per phase (unknowns compound over time)

**Pattern 4: Event Planning (Conference, Launch Event)**
- **Target**: Event happens on date, attendees have great experience
- **Key milestones**: Event day, rehearsal, content ready, speakers confirmed, venue booked, date announced
- **Critical path**: Venue booking (long lead time) often on critical path
- **Buffer**: 10-20% (events have hard deadlines, less flexible)

## Guardrails

**Feasibility checks:**
- **Available time ≥ required time**: If backward timeline reaches before today, goal is infeasible
- **Buffer included**: Add 20-30% to estimates (Hofstadter's Law: "It always takes longer than you expect, even when you account for Hofstadter's Law")
- **Dependencies realistic**: Can dependent work actually be done in sequence (handoff time, rework)?
- **Resource constraints**: Do we have people/budget to parallelize where needed?

**Common pitfalls:**
- **Optimistic sequencing**: Assuming perfect handoffs, no rework, no blockers
- **Ignoring dependencies**: "We can start everything at once" → actually highly sequential
- **No buffer**: Plans with 0% slack fail on first hiccup
- **Scope creep**: Target outcome expands during execution, invalidates backcast
- **Sunk cost fallacy**: When backcast shows infeasibility, adjust scope or date (don't plow ahead)

**Quality standards:**
- Milestones have clear deliverables (not "working on X")
- Dependencies explicitly mapped (not assumed)
- Critical path identified (know what determines timeline)
- Feasibility assessed honestly (not wishful thinking)
- Risks documented (what could extend timeline?)
- Owners assigned to each milestone (accountability)

## Quick Reference

**Resources:**
- **Quick backcast**: [resources/template.md](resources/template.md)
- **Complex roadmaps**: [resources/methodology.md](resources/methodology.md)
- **Quality rubric**: `resources/evaluators/rubric_roadmap_backcast.json`

**5-Step Process**: Define Target → Work Backward → Map Dependencies → Find Critical Path → Assess Feasibility

**Dependency types**: Sequential (A→B) | Parallel (A∥B) | Converging (A,B→C) | Diverging (A→B,C)

**Critical path**: Longest dependent sequence = minimum project duration

**Buffer rule**: Add 20-30% to estimates, 40%+ for high-uncertainty work

**Feasibility test**: Required time ≤ Available time (with buffer)
