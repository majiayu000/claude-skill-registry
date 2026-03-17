---
name: countdown
description: "Countdown - pre-implementation validation. Runs oracle (Opus) for planning, then Go Poll with review agents (Haiku) to validate before coding starts."
---

# Countdown

The pre-launch sequence for validating a plan before implementation begins.

## Usage

```
/countdown [issue-number]
```

## What This Does

Countdown is the pre-implementation workflow:

1. **Plan** - Oracle creates/refines implementation plan
2. **Go Poll** - Review agents validate the plan
3. **Iterate** - Fix issues until all agents report GO
4. **Launch** - Begin implementation only when validated

## Sequence

### Phase 1: Oracle Planning

Oracle creates the implementation plan at:
```
~/.claude/plans/reovim/{issue_number}-{subject}.md
```

### Phase 2: Go Poll

Review agents validate the plan:

| Agent | Model | Focus |
|-------|-------|-------|
| **mission-control** | Haiku | Plan completeness, phases, acceptance criteria |
| **telemetry** | Haiku | Test strategy, coverage targets |
| **flight-director** | Sonnet | Architecture, Unix philosophy, layer boundaries |

## A+ Skip Rule

**If an agent gives ALL A+ in round N, skip that agent in round N+1.**

## Output Structure

```
tmp/{ISSUE}/
└── countdown/
    └── round-{N}/
        ├── mission-control.md
        ├── telemetry.md
        └── flight-director.md
```

## Grading Scale

| Grade | Meaning |
|-------|---------|
| **A+** | Exemplary plan (skip next round) |
| **A** | Ready for implementation |
| **B** | Minor gaps - refine plan |
| **C** | Significant gaps - more planning needed |
| **F** | Major issues - rethink approach |

## Success Criteria

**Must achieve GO (A or A+) from ALL THREE review agents** before implementation.

- **A+** = Exemplary, skip this agent in next round
- **A** = Ready for implementation, GO
- **B or below** = NO-GO, refine plan

If any agent gives below A:
1. Refine the plan based on feedback
2. Re-run `/countdown`
3. Repeat until all agents report GO (A or A+)

## Instructions

When invoked, you MUST:

1. Determine the issue number from context (git branch, user input, or ask)
2. Check if a plan exists at `~/.claude/plans/reovim/{issue}-*.md`
3. If no plan exists or plan needs refinement:
   - Launch `oracle` agent (Opus) to create/refine the plan
4. Determine the round number (start at 1, increment for re-reviews)
5. Check previous round grades - skip agents with A+ from prior rounds
6. Create the output directory: `tmp/{ISSUE}/countdown/round-{N}/`
7. Launch review agents IN PARALLEL using Task tool with `model: "haiku"`
8. After all agents complete, summarize the grades in a table
9. If any grade is below A, list what needs to be fixed in the plan

**Phase 1: Oracle (if needed)**
```
Create/refine implementation plan for issue #{ISSUE}.

You are Oracle - the far-seeing architect.

1. Understand the requirements from the issue
2. Explore the codebase to understand current architecture
3. Design a phased implementation plan

Write the plan to: ~/.claude/plans/reovim/{ISSUE}-{subject}.md

Include:
- Summary and approach
- Phases with specific files and changes
- Risks and mitigations
- Test strategy
- Acceptance criteria
```

**Phase 2: Review Agents**

**Agent 1 (mission-control):**
```
Countdown review for issue #{ISSUE} (Round {N}).

You are Mission Control validating the plan before launch.

Focus: Plan completeness and clarity.

1. Read the plan at ~/.claude/plans/reovim/{ISSUE}-*.md
2. Verify all phases have clear acceptance criteria
3. Check dependencies between phases
4. Ensure scope is well-bounded

Write your report to: tmp/{ISSUE}/countdown/round-{N}/mission-control.md

End with: "Mission Control: GO / NO-GO" and grade (A+/A/B/C/F).
```

**Agent 2 (telemetry):**
```
Countdown review for issue #{ISSUE} (Round {N}).

You are Telemetry validating the test strategy.

Focus: Test coverage planning.

1. Read the plan at ~/.claude/plans/reovim/{ISSUE}-*.md
2. Verify test strategy covers happy paths, errors, edge cases
3. Check that critical functionality has test targets
4. Identify any testing gaps

Write your report to: tmp/{ISSUE}/countdown/round-{N}/telemetry.md

End with: "Telemetry: GO / NO-GO" and grade (A+/A/B/C/F).
```

**Agent 3 (flight-director):**
```
Countdown review for issue #{ISSUE} (Round {N}).

You are Flight Director validating the architecture.

Focus: Unix philosophy and layer boundaries.

1. Read the plan at ~/.claude/plans/reovim/{ISSUE}-*.md
2. Verify mechanism vs policy separation
3. Check layer boundaries are respected
4. Assess complexity and simplicity

Write your report to: tmp/{ISSUE}/countdown/round-{N}/flight-director.md

End with: "Flight Director: GO / NO-GO" and grade (A+/A/B/C/F).
```

CRITICAL:
- Launch `oracle` with `model: "opus"` for planning
- Launch review agents with `model: "{model}"` for validation
  - `model: "haiku"` for fast, efficient reviews
  - `model: "sonnet"` for comprehensive, precise reviews
- Skip agents that received ALL A+ in previous rounds
- Do NOT start implementation until all agents report GO
