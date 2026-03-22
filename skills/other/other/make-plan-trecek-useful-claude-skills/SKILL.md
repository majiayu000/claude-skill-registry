---
name: make-plan
description: Create implementation plans through deep codebase understanding. Use when user asks to create, devise, or write a plan. Leverages subagents to explore approaches, understand systems, and design aligned solutions.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '📋 [SKILL: plan] Creating implementation plan...'"
          once: true
---

# Implementation Plan Skill

Create focused, actionable implementation plans that recommend the technically best solution.

## When to Use

- User says "create a plan", "devise a plan", "write a plan"
- User wants an "implementation plan" for a feature or fix
- User asks to "plan out" a task or migration

## Core Values - CRITICAL

The ONLY criterion for choosing an approach is **technical quality and correctness of design**. A well-designed system is the goal. Nothing else matters.

**NEVER use these as reasons to choose or reject an approach:**
- Implementation effort or difficulty ("would require rewrite" is NOT a reason)
- Number of files changed
- Amount of existing code affected
- Number of tests that would need updating
- "Migration risk" or "rollback ease"
- "Preserves existing patterns" (existing patterns may be wrong)
- "Minimal changes needed"
- "Zero changes to X" (not a benefit - neutral at best)
- "Existing tests mostly pass" (tests validate desired behavior, they don't constrain design)

**Tests exist to validate that code works as intended.** When functionality changes, tests SHOULD change. "Would break tests" is never a reason to reject an approach.

**Git handles rollback.** Feature flags for rollback are unnecessary complexity.

**Existing code is not sacred.** If the existing architecture is flawed, the right answer is to fix it, not preserve it.

## Planning Steps

1. **Understand related systems and validate details** - Use subagents to study the architecture, how components work together, their purpose, patterns, and standards. Validate any details provided in the task description.

2. **Explore and design approaches** - Use subagents to investigate different ways to solve the problem. Use subagents with web search to research modern solutions, approaches, designs, and architectures relevant to the problem. For each approach, focus on:
   - Does it solve the problem correctly?
   - Is it the right abstraction?
   - Does it enable future evolution of the system?
   - Is the design clean and understandable?

3. **Design tests first** - For the chosen approach, define tests that capture the intended behavior. These tests should fail against the current codebase and pass once the implementation is complete. The implementation steps should be ordered to make these tests pass.

4. **Evaluate approaches on technical merit only** - Use subagents to assess each approach. Evaluation criteria:
   - **Correctness**: Does it fully solve the stated problem?
   - **Design quality**: Is this the right abstraction? Is it clean?
   - **Architectural fit**: Does it align with how the system SHOULD work (not how it currently works if current is flawed)?
   - **Maintainability**: Will future developers understand and extend it?

**DO NOT evaluate based on:** implementation effort, risk, number of changes, test breakage, or ease of rollback. These are not engineering criteria.

5. **Visualize with Architecture Lens** - After finalizing the plan, determine which architecture lens best illustrates the proposed changes, then create a mermaid diagram.

**Select the lens based on what the plan primarily affects:**

| If the plan primarily involves... | Use Lens |
|-----------------------------------|----------|
| Adding/modifying containers, services, or integrations | C4 Container |
| Changing workflow logic, state machines, or decision flow | Process Flow |
| Altering data storage, transformations, or information flow | Data Lineage |
| Restructuring modules, changing dependencies, or layering | Module Dependency |
| Adding/modifying parallel execution or thread handling | Concurrency |
| Changing error handling, retry logic, or recovery paths | Error/Resilience |
| Modifying repository patterns or data access | Repository Access |
| Changing CLI commands, config, or monitoring | Operational |
| Adding/modifying validation, trust boundaries, or isolation | Security |
| Changing build tools, test framework, or quality gates | Development |
| Affecting multiple user journeys or cross-component flows | Scenarios |
| Modifying state contracts, field lifecycles, or resume logic | State Lifecycle |
| Changing deployment topology or infrastructure | Deployment |

**MANDATORY: LOAD the appropriate arch-lens skill using the Skill tool:**

| Lens | Skill to LOAD |
|------|---------------|
| C4 Container | `/arch-lens-c4-container` |
| Process Flow | `/arch-lens-process-flow` |
| Data Lineage | `/arch-lens-data-lineage` |
| Module Dependency | `/arch-lens-module-dependency` |
| Concurrency | `/arch-lens-concurrency` |
| Error/Resilience | `/arch-lens-error-resilience` |
| Repository Access | `/arch-lens-repository-access` |
| Operational | `/arch-lens-operational` |
| Security | `/arch-lens-security` |
| Development | `/arch-lens-development` |
| Scenarios | `/arch-lens-scenarios` |
| State Lifecycle | `/arch-lens-state-lifecycle` |
| Deployment | `/arch-lens-deployment` |

**Create the diagram following the loaded skill's instructions:**
- Focus on the PROPOSED changes (use `newComponent` class for new elements)
- Show how new components integrate with existing architecture
- Use `●` prefix for modified existing components
- Use `★` prefix for new components

Include the diagram in the plan document under a "## Proposed Architecture" section.
More than one lens diagram is okay if it is complex plan (don't do more than 3, and make sure to load each appropriate skill).
---

## Skill Loading Checklist

Before writing the final plan, verify:

- [ ] Determined which architecture lens best fits the proposed changes
- [ ] LOADED the corresponding `/arch-lens-*` skill using the Skill tool
- [ ] The arch-lens skill LOADED the `/mermaid` skill for styling
- [ ] Diagram uses ONLY the classDef styles from the mermaid skill (no invented colors)
- [ ] Diagram includes a color legend table
- [ ] Every new component, class, or function is wired into the call chain — nothing is created but left unconnected

## Critical Constraints

**NEVER use EnterPlanMode.** This skill IS the planning process. Execute the planning steps directly — explore with subagents, design the approach, write the plan file to `temp/make-plan/`. Do not enter plan mode, do not call ExitPlanMode. Just do the work and deliver the plan.

**NEVER include:**
- Multiple alternative approaches (recommend ONE only)
- Stakeholder sections
- PR breakdown sections
- Backward compatibility considerations
- Fallback mechanisms
- Justifications based on effort, risk, or preserving existing code

**NEVER:**
- Change any code
- Choose an approach because it's easier
- Reject an approach because it's harder
- Create files outside `temp/make-plan/` directory
- Include `git cherry-pick` or `git checkout <branch> -- <file>` in plan steps — these bypass the worktree isolation model

**ALWAYS:**
- Write to `temp/make-plan/` directory
- Recommend the single best technical solution
- Ground decisions in design quality and correctness
- Include verification steps
- Be willing to recommend significant refactoring if that's the right answer

## Output

If the plan exceeds 500 lines, split it into multiple files (`_part_a`, `_part_b`, etc.) at natural section boundaries. Use as many parts as needed.

**CRITICAL — Multi-part plan rules:**
- **Never include file paths or guessable names for other parts.** No paths, no filenames, no references that allow an agent to locate other part files.
- Include only a brief plain-text note about what subsequent parts cover (e.g., "Part B will cover X and Y — implement as a separate task").
- The title of each part file MUST include `— PART A ONLY` (or B, C, etc.) so scope is immediately visible.
- Each part file MUST open with the scope warning block shown in the multi-part template below.

Save the plan to: `temp/make-plan/{task_name}_plan_{YYYY-MM-DD_HHMMSS}.md`

**Plan structure (single-part):**
```markdown
# Implementation Plan: {Task Name}

## Summary
{Brief overview of what will be implemented}

## Proposed Architecture
{Mermaid diagram showing the proposed changes using the selected lens}

**Lens Used:** {lens name} - {why this lens was chosen}

## Tests
{Tests to write first — should fail now, pass after implementation}

## Implementation Steps
{Ordered steps, each making one or more of the above tests pass}

## Verification
{How to verify the implementation is correct}
```

**Plan structure (multi-part — use for EACH part file):**
```markdown
# Implementation Plan: {Task Name} — PART {X} ONLY

> **PART {X} ONLY. Do not implement any other part. Other parts are separate tasks requiring explicit authorization.**

## Summary
{What THIS part covers. Explicitly note what is deferred: "Part B will cover X (separate task). Part C will cover Y (separate task)."}

## Proposed Architecture
{Mermaid diagram showing the proposed changes using the selected lens}

**Lens Used:** {lens name} - {why this lens was chosen}

## Tests
{Tests for THIS part only — should fail now, pass after THIS part's implementation}

## Implementation Steps
{Steps for THIS part only}

## Verification
{How to verify THIS part's implementation is correct}
```
