---
name: plan-code-workflow
description: "Plan/Code workflow for moderate to complex tasks. Defines when to use Plan vs Code mode. Applied automatically for non-trivial implementations."
user-invocable: false
---

# Plan/Code Workflow

Two primary work modes: **Plan** and **Code**.

## Task Complexity Assessment

| Complexity | Characteristics | Strategy |
|------------|-----------------|----------|
| **Trivial** | Simple syntax, single API, <10 lines | Answer directly |
| **Moderate** | Non-trivial logic in single file, local refactoring | Use Plan/Code workflow |
| **Complex** | Cross-module design, concurrency, multi-step migrations | Must use Plan/Code workflow |

## Common Rules

- **When entering Plan mode**, briefly restate: mode, objective, key constraints, current state
- In Plan mode, **must read relevant code first** before proposing modifications
- Only restate when mode switches or constraints significantly change
- Don't unilaterally introduce new tasks beyond scope
- When user says "implement", "execute", "proceed", "start coding" → switch to Code mode immediately

## Plan Mode (Analysis / Alignment)

1. Analyze top-down, find root causes, not just patch symptoms
2. List key decision points and trade-offs
3. Provide **1–3 feasible options**, each including:
   - Summary approach
   - Impact scope (modules/interfaces involved)
   - Pros and cons
   - Potential risks
   - Verification methods

4. Only ask clarifying questions when missing info would block progress
5. Avoid providing essentially identical plans

### Exit Conditions

- User explicitly chooses an option, OR
- One option is clearly superior (explain reasoning, proactively choose)

Once conditions met → **enter Code mode directly**

## Code Mode (Execute Plan)

1. Main content must be concrete implementation, not continued planning
2. Before providing code, briefly state:
   - Which files/modules will be modified
   - Purpose of each modification

3. Prefer **minimal, reviewable changes**:
   - Local snippets/patches over complete files
   - Mark key change regions

4. Indicate how to verify:
   - Tests/commands to run
   - Draft new test cases if needed

5. If major problems discovered → pause, switch back to Plan mode

### Output Should Include

- What changes were made, where
- How to verify
- Known limitations or follow-up TODOs
