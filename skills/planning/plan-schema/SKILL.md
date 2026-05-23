---
name: plan-schema
description: Use when creating or validating Arc plans. Defines the 8 required sections, anti-patterns, and validation checklist.
invocation: agent
---

# Plan Schema

Define and enforce the required structure for all Arc plans. Every plan produced by the `plan-creator-default` agent or the `/plan` command must conform to this schema.

## Invocation Contract

Inputs:
- Feature intent and constraints
- Candidate implementation steps

Outputs:
- Plan document with all required sections
- Schema validation result with actionable failures

## Required Sections

### 1. Summary

A 2-3 sentence overview of what the plan accomplishes and why. Include the tier classification (Simple/Standard/Full) and the routing confidence from `router`.

### 2. Scope and Non-Goals

Explicitly list what is in scope and what is deliberately excluded. Non-goals prevent scope creep and set expectations. Be concrete: "authentication is out of scope" is better than "some features are deferred."

### 3. Code Context and Affected Files

List every file that will be created, modified, or deleted. For modifications, note which functions or sections are affected. This enables accurate impact assessment and conflict detection in team mode.

### 4. Implementation Plan

Ordered list of steps with enough detail to execute without further clarification. Each step should specify:
- What changes to make
- Which files are touched
- What the expected outcome is
- Any preconditions from earlier steps

### 5. Dependency Graph

Define ordering constraints between steps. Use explicit notation: "Step 3 depends on Step 1 and Step 2." Identify which steps can run in parallel. This graph directly feeds into bead decomposition.

### 6. Exit Criteria Commands

Concrete, runnable commands that verify the plan is complete:
- Test commands with expected pass counts
- Lint and typecheck commands
- Build commands
- Any manual verification steps (marked as such)

Never use vague criteria like "run tests." Specify: `npm test -- --filter=auth` or `pytest tests/test_auth.py -v`.

### 7. Risk and Rollback

Identify what could go wrong and how to recover. Include:
- Technical risks (breaking changes, data migration failures)
- Mitigation strategies for each risk
- Rollback procedure if the plan must be abandoned mid-execution

### 8. Phase Weights and Rationale

Assign relative weight (percentage) to each implementation phase. Weights guide effort estimation and progress tracking. Include a brief rationale for the distribution.

## Anti-Patterns

- Vague exit criteria without explicit commands
- References to external context without embedding needed details
- Missing dependency ordering between steps
- Steps too large to verify independently (should be decomposed further)
- Non-goals section absent or filled with trivia instead of genuine scope boundaries
- Dependency graph that is purely sequential when parallelism is possible

## Validation

After producing a plan, verify:
1. All eight sections are present and non-empty.
2. Every affected file in Section 3 appears in at least one step in Section 4.
3. Every step in Section 4 appears in the dependency graph in Section 5.
4. Exit criteria in Section 6 are runnable commands, not descriptions.
5. Phase weights in Section 8 sum to 100%.

## Related Skills

- `router` determines the tier and whether a plan is needed.
- `beads-schema` defines how plan steps decompose into executable beads.
- Execution skills (`loop`, `swarm`, `team`) consume the plan.
