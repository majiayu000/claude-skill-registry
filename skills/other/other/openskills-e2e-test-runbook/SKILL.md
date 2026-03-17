---
name: openskills-e2e-test-runbook
description: Run deterministic OpenSkills end-to-end validation across runtime tests and example agents, then report tool calls, activation behavior, and regressions.
---

# OpenSkills E2E Test Runbook

Use this skill for confidence checks before merging runtime, tooling, or example-agent changes.

## Test Layers

1. Runtime regression tests
2. Sandbox-focused tests
3. Example-agent behavior checks
4. Optional binding smoke tests

## Baseline Commands

```bash
cargo test -p openskills-runtime
```

Example-agent checks (from example directories):

```bash
npm install
npm start "What skills are available?"
npm start "Create a new skill called 'note-taker'."
```

## E2E Expectations

- Skills discover successfully.
- Skill activation occurs for matching prompts.
- Tool calls align with intent (activation, file reads/writes, script runs).
- No unexpected sandbox failures.

## Reporting Format

- What was run
- What passed
- What failed
- Repro command for each failure
- Suggested next fix
