---
name: engineering-lifecycle
description: "Plan, implement, and verify software with TDD discipline and intelligent execution routing. Not for ad-hoc execution without a plan."
---

# Engineering Lifecycle

<mission_control>
<objective>Plan, implement, and verify software with TDD discipline and intelligent execution routing</objective>
<success_criteria>Every feature: 2-3 task plan, RED→GREEN→REFACTOR cycle, 80%+ coverage</success_criteria>
</mission_control>

<trigger>When starting a new feature, refactoring, or bug fix</trigger>

## Core Loop

PLANNING → IMPLEMENTATION (TDD) → EXECUTION → VERIFICATION

## Workflow Patterns

### Planning with Funnel

<funnel_step:explore>

- Investigate codebase, git history, constraints
  </funnel_step:explore>

<funnel_step:ask>

- One focused question with 2-4 recognition-based options
  </funnel_step:ask>

<funnel_step:refine>

- Next question if scope still unclear
  </funnel_step:refine>

<funnel_step:write>

- Generate PLAN.md with checkpoints and verification criteria
  </funnel_step:write>

<funnel_step:confirm>

- "Plan ready. Invoke /plan:execute?"
  </funnel_step:confirm>

### TDD Implementation

<funnel_step:explore>

- Identify test cases: happy path, edge cases, error scenarios
  </funnel_step:explore>

<funnel_step:write>

1. RED: Write failing test (one behavior, real code)
2. GREEN: Minimal code to pass (no features)
3. REFACTOR: Clean up while tests stay green
   </funnel_step:write>

<funnel_step:confirm>

- Verify 80%+ coverage achieved
  </funnel_step:confirm>

### Execution with Mode Routing

<mode:autonomous>
Plan has no checkpoints → Fresh subagent executes all tasks
</mode:autonomous>

<mode:segmented>
Plan has human-verify checkpoints → Subagent for segments, main for checkpoints
</mode:segmented>

<mode:main>
Plan has decision/action checkpoints → Sequential main context execution
</mode:main>

<mode:reviewed>
Quality gates requested → Fresh subagent + 2-stage review
</mode:reviewed>

## Quick Reference

<iron_law>
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
</iron_law>

<task_rule>
Target: 2-3 tasks per plan, 50% context maximum, 2-5 min per task
</task_rule>

## References

| If You Need...           | Read...                 |
| ------------------------ | ----------------------- |
| User interaction pattern | refs/funnel-pattern.md  |
| PLAN.md structure        | refs/plan-format.md     |
| Execution mode selection | refs/execution-modes.md |
| TDD cycle details        | refs/tdd-patterns.md    |
| CLI automation limits    | refs/cli-automation.md  |

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---

<critical_constraint>
MANDATORY: Apply <iron_law> before any production code
MANDATORY: Keep plans to <task_rule> (2-3 tasks, 50% context)
MANDATORY: Run quality-standards after TDD cycle completes
</critical_constraint>

---
