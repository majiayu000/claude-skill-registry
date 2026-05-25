---
name: mission-orchestrator
description: "Lifecycle orchestrator that auto-detects project state and routes to the correct development phase."
alwaysApply: false
category: workflow-orchestration
tags:
- mission
- orchestrator
- lifecycle
- full-cycle
- automation
dependencies:
- attune:project-brainstorming
- attune:project-specification
- attune:project-planning
- attune:project-execution
- attune:war-room-checkpoint
- attune:war-room
- leyline:risk-classification
- leyline:damage-control
- leyline:additive-bias-defense
- imbue:justify
- imbue:vow-enforcement
- abstract:friction-detector
tools: []
provides:
  workflow:
  - mission-lifecycle
  - state-detection
  - phase-routing
  - session-recovery
  - reflexion-buffer
  - trust-tier
  - adaptive-constraints
usage_patterns:
- full-cycle-development
- mission-resume
- phase-routing
complexity: advanced
model_hint: deep
estimated_tokens: 600
progressive_loading: true
modules:
- modules/mission-types.md
- modules/state-detection.md
- modules/phase-routing.md
- modules/mission-state.md
- modules/plan-review.md
- modules/plan-versioner.md
- modules/feedback-collector.md
- modules/context-injector.md
- modules/iteration-governor.md
- modules/reflexion-buffer.md
- modules/trust-tier.md
- modules/adaptive-constraints.md
references:
- references/mission-charter.md
- references/progress-report.md
role: entrypoint
---
## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [Mission Lifecycle](#mission-lifecycle)
- [Interactive Plan Review](#interactive-plan-review)
- [Mission Types](#mission-types)
- [Phase-to-Skill Mapping](#phase-to-skill-mapping)
- [Session Recovery](#session-recovery)
- [Module Reference](#module-reference)
- [Related Skills](#related-skills)
- [Related Commands](#related-commands)
- [Exit Criteria](#exit-criteria)


# Mission Orchestrator

## Overview

Wraps the entire attune development lifecycle (brainstorm → specify → plan → execute) into a single mission with automatic state detection, type selection, and phase routing. Follows the "persistent presence lens" pattern from `spec-kit:speckit-orchestrator` — delegates entirely to existing skills via `Skill()` calls, never re-implements phase logic.

## When To Use

- Starting a new project from scratch (full lifecycle)
- Resuming an interrupted project workflow
- Running a focused tactical implementation from existing specs
- Quick-fixing from an existing implementation plan

## When NOT To Use

- Running a single phase directly (use `/attune:brainstorm`, `/attune:specify`, etc.)
- Non-project work (code review, debugging, research)
- When you need fine-grained control over phase transitions

## Mission Lifecycle

```
1. State Detection
   Scan for existing artifacts (project-brief.md, specification.md, etc.)
       |
2. Mission Type Selection
   Auto-detect type based on artifacts, or accept user override
       |
3. Phase Routing Loop
   For each phase in the mission type:
       a. Pre-phase validation (check prerequisites)
       b. Invoke Skill(attune:{phase-skill})
       c. Post-phase artifact check (verify output exists)
       d. Post-phase backlog triage (create GitHub issues
          for out-of-scope items after brainstorm/specify)
       e. Update mission state
       f. User checkpoint (skippable with --auto)
       g. Error handling via leyline:damage-control
       |
4. Completion
   All phases complete, final state saved
```

## Mission Types

| Type | Phases | Auto-detected When |
|------|--------|--------------------|
| `full` | brainstorm → specify → plan → execute | No artifacts exist |
| `standard` | specify → plan → execute | `docs/project-brief.md` exists |
| `tactical` | plan → execute | `docs/specification.md` exists |
| `quickfix` | execute | `docs/implementation-plan.md` exists |

See `modules/mission-types.md` for full type definitions and custom type support.

## Phase-to-Skill Mapping

| Phase | Skill Invoked | Artifact Produced |
|-------|--------------|-------------------|
| brainstorm | `Skill(attune:project-brainstorming)` | `docs/project-brief.md` |
| specify | `Skill(attune:project-specification)` | `docs/specification.md` |
| plan | `Skill(attune:project-planning)` | `docs/implementation-plan.md` |
| execute | `Skill(attune:project-execution)` | Implemented code + tests |

The orchestrator **never** re-implements phase logic. Each phase is a complete `Skill()` invocation that handles its own workflow.

## Session Recovery

Missions persist state to `.attune/mission-state.json`. On resume:

1. Load mission state file
2. Validate referenced artifacts still exist on disk
3. Identify last completed phase
4. Continue from next phase in sequence

See `modules/mission-state.md` for the state schema and recovery protocol.

## Interactive Plan Review

The plan-to-execute transition uses an interactive
review loop instead of a simple checkpoint. Plans are
reviewed section by section, revised based on feedback,
and must pass a mandatory war-room gate before execution.

**Key capabilities:**

- Section-by-section terminal review (architecture
  first, then phases)
- Approve/revise/reject verdicts with rationale
- Plan version tracking with diff summaries
- Context improvement from structured feedback
- Additive bias scanning before user review
- Maximum 3 revision rounds before forced decision
- Mandatory war-room approval with Prosecution Counsel

See `modules/plan-review.md` for the full protocol.

### Review Modules

- **plan-review.md**: Main orchestrator for the review loop
- **plan-versioner.md**: Version tracking and diff generation
- **feedback-collector.md**: Verdict capture and JSON output
- **context-injector.md**: Revision prompt construction
- **iteration-governor.md**: Round tracking and escalation

## User Directive Overrides

The orchestrator parses the user's command-args and
free-text at mission start for natural-language trust
signals. Phrases like "ignore scope guard", "ultrathink",
"don't keep asking", and "be autonomous" are recognized
as directive overrides that adjust the constraint
profile without requiring an explicit
`--constraints=` flag.

Directive overrides win over mission-type defaults but
never bypass the Safety Floor (pre-commit hooks,
proof-of-work evidence, destructive-operation
confirmation, external-facing actions). When a directive
is detected, the orchestrator acknowledges it once at
mission start and stops asking for the corresponding
checkpoints. Repeated approval-seeking after a directive
override is itself a workflow bug.

See `modules/adaptive-constraints.md` "User Directive
Override" section for the parsing table.

## Mission Charter

Define mission boundaries using the structured template from
`references/mission-charter.md`. A Mission Charter specifies:

- **Outcome**: What success looks like
- **Success metric**: Measurable completion criteria
- **Deadline**: Time boundary (session, date, or duration)
- **Constraints**: Token/time budgets, forbidden actions
- **Scope**: In-scope and out-of-scope areas
- **Stop criteria**: Conditions that halt the mission

See `references/mission-charter.md` for the full template and
examples.

## Progress Reports

Track progress with structured checkpoints using
`references/progress-report.md`. Generate reports at:

- Phase boundaries (between brainstorm→specify→plan→execute)
- Blocker identification
- Risk escalation
- Budget thresholds (50%, 75%, 90%)

See `references/progress-report.md` for the template and
checkpoint rhythm guidance.

## Module Reference

### Core modules (always loaded)

- **mission-types.md**: Type definitions, auto-detection logic,
  custom types
- **state-detection.md**: Artifact existence checks, quality
  validation, staleness
- **phase-routing.md**: Phase execution protocol, transition
  hooks, error handling
- **mission-state.md**: State schema, persistence, recovery
  protocol

### Plan-review modules (load when plan phase runs)

- **plan-review.md**: Interactive section-by-section review
  with bias scanning
- **plan-versioner.md**: Version tracking and diff summaries
- **feedback-collector.md**: Verdict capture and feedback files
- **context-injector.md**: Revision prompt construction from
  feedback
- **iteration-governor.md**: Round tracking, cap enforcement,
  escalation

### Conditional modules (load only when triggered)

- **reflexion-buffer.md**: Cross-session learning buffer; load
  when iteration count > 1 or after a failed revision round.
- **trust-tier.md**: Constraint-profile classifier; load when
  a user directive override is detected at mission start.
- **adaptive-constraints.md**: Constraint adaptation rules;
  load alongside `trust-tier.md` when directive overrides are
  active.

## Module Loading by Mission Type

This skill declares `progressive_loading: true`. To keep the
orchestrator's resident token cost minimal, load only the
subset of modules each mission type actually needs. The
orchestrator itself loads only the four core modules at
mission start; the rest are loaded on-demand when their
phase runs.

| Mission type | Core | Plan-review | Reflexion | Trust + adaptive |
|--------------|------|-------------|-----------|------------------|
| `quickfix` (execute only) | yes | -- | -- | if directive |
| `tactical` (plan -> execute) | yes | yes | if revising | if directive |
| `standard` (specify -> plan -> execute) | yes | yes | if revising | if directive |
| `full` (brainstorm -> specify -> plan -> execute) | yes | yes | yes | if directive |

Token cost (approximate, computed from `wc -w` on hub +
loaded modules and converted at ~1.3 tokens per word):

| Mission type | Loaded modules | Approx tokens |
|--------------|----------------|---------------|
| `quickfix`   | hub + core (4) | ~4,100 |
| `tactical`   | hub + core + plan-review (9) | ~6,900 |
| `standard`   | same as tactical (9) | ~6,900 |
| `full`       | hub + core + plan-review + reflexion (10) | ~7,900 |

The previous load-all pattern brought in roughly 10,100
tokens for every mission, including `quickfix` runs that
only need the execute phase. With per-type loading, quickfix
is ~60% lighter and the standard / tactical / full paths
save 22-32%.

When a directive override fires, the trust-tier +
adaptive-constraints pair adds ~2,200 tokens on top of the
mission-type baseline.

## Reference Modules

- **mission-charter.md**: Structured mission definition
  template (load only when defining a charter)
- **progress-report.md**: Checkpoint status report template
  (load only when emitting a progress report)

## Related Skills

- `Skill(attune:project-brainstorming)` - Brainstorm phase
- `Skill(attune:project-specification)` - Specify phase
- `Skill(attune:project-planning)` - Plan phase
- `Skill(attune:project-execution)` - Execute phase
- `Skill(attune:war-room-checkpoint)` - Risk assessment for RED/CRITICAL tasks
- `Skill(leyline:risk-classification)` - Task risk classification
- `Skill(leyline:damage-control)` - Error recovery during phases

## Related Commands

- `/attune:mission` - Invoke this skill
- `/attune:mission --resume` - Resume from saved state
- `/attune:mission --type tactical` - Override mission type

## Exit Criteria

- All phases in mission type completed successfully
- Artifacts exist for each completed phase
- Mission state saved to `.attune/mission-state.json`
- Risk summary generated (tier counts across all tasks)
- No unresolved errors or blockers
