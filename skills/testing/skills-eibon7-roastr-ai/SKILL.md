---
name: skills
description: Archived skill guidance for skills.
---

---

name: dispatching-parallel-agents-skill
description: Use when facing 3+ independent failures that can be investigated without shared state or dependencies - dispatches multiple Claude agents to investigate and fix independent problems concurrently
triggers:

- "multiple failures"
- "independent problems"
- "parallel investigation"
- "3+ test failures"
  used_by:
- test-engineer
- orchestrator
  steps:
- paso1: "Verify: 3+ failures, independent domains, no shared state"
- paso2: "Identify independent domains by what's broken"
- paso3: "Create focused agent tasks: Specific scope, clear goal, constraints"
- paso4: "Dispatch agents in parallel"
- paso5: "Review summaries, verify fixes don't conflict"
- paso6: "Run full test suite, integrate changes"
  output: |
- Independent problems fixed in parallel
- Summary from each agent
- Full suite passing
- No conflicts between fixes
  when_to_use: "3+ test files failing with different root causes"
  when_not_to_use: "Failures related, need full context, shared state"
  pattern:
- "Group by what's broken (File A: tool approval, File B: batch completion)"
- "Each domain independent - fixing one doesn't affect others"
- "Dispatch concurrently, review when all return"
  agent_prompts:
- "Focused: One clear problem domain"
- "Self-contained: All context needed"
- "Specific output: What should agent return?"
  common_mistakes:
- "Too broad: 'Fix all tests' → agent lost"
- "No context: 'Fix race condition' → agent doesn't know where"
- "No constraints: Agent refactors everything"
- "Vague output: 'Fix it' → don't know what changed"
  referencias:
- "Fuente: superpowers-skills/dispatching-parallel-agents"
- "Roastr: Útil cuando múltiples tests fallando independientes"
