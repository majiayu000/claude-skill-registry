---
name: openskills-dev-orchestrator
description: Route OpenSkills development tasks to the right project skill or subagent, including sequencing rules for debugging, feature work, regression checks, and release readiness.
---

# OpenSkills Dev Orchestrator

Use this skill to decide which OpenSkills project skill or subagent to invoke first, and in what order, for the fastest safe outcome.

## Routing Rules

### 1) Runtime failures or sandbox regressions

1. Start with `openskills-runtime-debug`.
2. If issue spans multiple execution paths or platforms, use `runtime-sandbox-auditor` subagent.
3. Re-run runtime tests before concluding.

### 2) Plugin/build feature changes

1. Start with `openskills-plugin-separation`.
2. If dependency topology is unclear, use `wasm-plugin-build-specialist` subagent.
3. Validate runtime default-feature behavior and binding impact.

### 3) Binding breakages (TS/Python)

1. Start with `openskills-bindings-maintainer`.
2. If both bindings are affected or unclear, use `bindings-compatibility-agent` subagent.
3. Return a compatibility matrix and migration notes if needed.

### 4) Skill package authoring or updates

1. Start with `openskills-skill-authoring`.
2. Use `skill-spec-conformance-agent` subagent when multiple skills or ambiguous triggers are involved.
3. Validate discovery and activation behavior.

### 5) End-to-end confidence checks

1. Start with `openskills-e2e-test-runbook`.
2. Use `examples-e2e-agent` subagent for scenario-heavy or flaky behavior investigations.
3. Capture scenario-by-scenario pass/fail and tool-call evidence.

### 6) Release preparation

1. Start with `openskills-release-ops`.
2. Use `release-gatekeeper-agent` subagent for final GO/NO-GO judgment.
3. Output blockers, risks, and rollback notes explicitly.

## Escalation Heuristics

- Use a skill first when the workflow is deterministic and repeatable.
- Escalate to a subagent when the task needs deep cross-file reasoning, ambiguity handling, or parallel analysis.
- If a task is unresolved after one full skill pass, escalate to the corresponding subagent.

## Output Contract

Always return:

1. Selected path (skill and/or subagent)
2. Why this path was chosen
3. Ordered execution plan
4. Success criteria
