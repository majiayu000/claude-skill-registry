---
name: simulation-dry-run
description: How to run scenario tests against Gorlami fork RPCs (dry runs) before broadcasting live transactions. Covers config, seeding balances, runner flags, and safe script patterns.
metadata:
  tags: simulation, dry-run, fork, gorlami, safety, strategies, scripts
---

## When to use

Use this skill when you are:
- Writing or modifying a **fund-moving** script (swaps, lending, bridging, looping)
- Iterating on a strategy `deposit/update/withdraw/exit` flow
- Debugging approvals, units, calldata shapes, gas issues, or multi-step sequencing

## How to use

- [rules/quickstart.md](rules/quickstart.md) - Config + fastest way to run a fork scenario
- [rules/scenario-checklist.md](rules/scenario-checklist.md) - What to validate before “live”
- [rules/script-pattern.md](rules/script-pattern.md) - Recommended CLI + `gorlami_fork(...)` pattern
- [rules/gotchas.md](rules/gotchas.md) - Common fork-mode failures and mitigations


