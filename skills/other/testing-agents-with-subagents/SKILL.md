---
name: testing-agents-with-subagents
description: "Test agents via subagents: known inputs, captured outputs, verification."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
routing:
  triggers:
    - "test agents"
    - "agent testing"
    - "subagent testing"
    - "validate agent"
    - "agent test harness"
  category: testing
  pairs_with:
    - agent-evaluation
    - subagent-driven-development
---

# Testing Agents With Subagents

## Overview

This skill applies **TDD methodology to agent development** — RED (observe failures), GREEN (fix agent definition), REFACTOR (edge cases and robustness) — with subagent dispatch as the execution mechanism.

Test what the agent DOES, not what the prompt SAYS. Evidence-based verification only: capture exact outputs from subagent dispatch, verify every prompt change through testing. Always test via the Task tool, always test via the Task tool rather than reading prompts.

Minimum test counts vary by agent type: Reviewer agents need 6 cases (2 real issues, 2 clean, 1 edge, 1 ambiguous), Implementation agents 5 cases (2 typical, 1 complex, 1 minimal, 1 error), Analysis agents 4 cases (2 standard, 1 edge, 1 malformed), Routing/orchestration 4 cases (2 correct route, 1 ambiguous, 1 invalid). No agent is simple enough to skip testing — get human confirmation before exempting any agent.

Each test runs in a fresh subagent to avoid context pollution. After any fix, re-run ALL test cases to catch regressions. One fix at a time — you cannot determine what changed the outcome with multiple simultaneous fixes.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| example-driven tasks, errors | `examples-and-errors.md` | Loads detailed guidance from `examples-and-errors.md`. |
| dispatch-and-capture, negative, consistency, A/B, and routing-verification test patterns | `testing-patterns.md` | Loads detailed guidance from `testing-patterns.md`. |

## Instructions

### Phase 0: PREPARE — Understand the Agent

**Goal**: Read the agent definition and understand what it claims to do before writing tests.

**Step 1: Read the agent file**

```bash
# Read agent definition
cat agents/{agent-name}.md

# Read any referenced skills
cat skills/{skill-name}/SKILL.md
```

**Step 2: Identify testable claims**

Extract concrete, testable behaviors from the agent definition:
- What inputs does it accept?
- What output structure does it produce?
- What routing triggers should activate it?
- What error conditions does it handle?
- What skills does it invoke?

**Step 3: Determine minimum test count**

| Agent Type | Minimum Tests | Required Coverage |
|------------|---------------|-------------------|
| Reviewer agents | 6 | 2 real issues, 2 clean, 1 edge, 1 ambiguous |
| Implementation agents | 5 | 2 typical, 1 complex, 1 minimal, 1 error |
| Analysis agents | 4 | 2 standard, 1 edge, 1 malformed |
| Routing/orchestration | 4 | 2 correct route, 1 ambiguous, 1 invalid |

No gate — this phase is preparation. Move directly to Phase 1.

### Phase 1: RED — Observe Current Behavior

**Goal**: Run agent with test inputs and document exact current behavior before any changes.

**Step 1: Define test plan**

Write the test plan to a file before executing — this creates a reproducible baseline. See `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md` for the Test Plan template.

**Step 2: Dispatch subagent with test inputs**

Use the Task tool to dispatch the agent (see dispatch template in `references/examples-and-errors.md`). Each test runs in a fresh subagent — this prevents context pollution from earlier tests affecting later ones.

**Step 3: Capture results verbatim**

Document exact agent outputs. See the verbatim result capture template in `references/examples-and-errors.md`.

**Step 4: Identify failure patterns**
- Which test categories fail (happy path, error, edge)?
- Are failures structural (missing sections) or behavioral (wrong answers)?
- Do failures correlate with input characteristics?

**Gate**: All test cases executed. Exact outputs captured verbatim. Failures documented with specific issues identified. Proceed only when gate passes.

### Phase 2: GREEN — Fix Agent Definition

**Goal**: Update agent definition until all test cases pass. One fix at a time.

**Step 1: Prioritize failures**

Triage failures by severity — see the Failure Severity table in `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md` (Critical/High/Medium/Low).

**Step 2: Diagnose root cause**

Map the failure type to a fix approach — see the Root Cause → Fix Approach table in `references/examples-and-errors.md`.

**Step 3: Make one fix at a time**

Change one thing in the agent definition. Re-run ALL test cases. Document which tests now pass/fail.

Make one fix at a time — you cannot determine which change was effective. Same debugging principle: one variable at a time.

**Step 4: Iterate until green**

Repeat Step 3 until all test cases pass. If a fix causes a previously passing test to fail, revert and try a different approach. Track fix iterations using the Fix Log template in `references/examples-and-errors.md`.

**Gate**: All test cases pass. No regressions from previously passing tests. Can explain what each fix changed and why. Proceed only when gate passes.

### Phase 3: REFACTOR — Edge Cases and Robustness

**Goal**: Verify agent handles boundary conditions and produces consistent outputs.

**Step 1: Add edge case tests**

See the Edge Case Categories table in `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md` (Empty / Large / Unusual / Ambiguous inputs).

**Step 2: Run consistency tests**

Run the same input 3 times. Outputs should be consistent:
- Same structure
- Same key findings (for analysis agents)
- Acceptable variation in phrasing only

If inconsistent: add more explicit instructions to the agent definition. Re-test.

**Step 3: Run regression suite**

Re-run ALL test cases (original + edge cases) to confirm nothing broke during refactoring.

**Step 4: Document final test report**

See the Test Report template in `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md`.

**Gate**: Edge cases handled. Consistency verified. Full suite green. Test report documented. Fix is complete.

---

## Error Handling

See `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md` for error cases: agent-type-not-found, inconsistent-outputs, subagent-timeout, agent-asks-questions.

---

## Examples

See `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md` for worked examples: testing a new reviewer agent, testing after agent modification, testing routing logic.

---

## References

### Integration
- `agent-comparison`: A/B test agent variants
- `agent-evaluation`: Structural quality checks
- `test-driven-development`: TDD principles applied to agents

### Reference Files
- `${CLAUDE_SKILL_DIR}/references/testing-patterns.md`: Dispatch patterns, test scenarios, eval harness integration
- `${CLAUDE_SKILL_DIR}/references/examples-and-errors.md`: Worked examples (new reviewer, modification, routing) and error handling (agent-not-found, inconsistency, timeout, question-asking)
