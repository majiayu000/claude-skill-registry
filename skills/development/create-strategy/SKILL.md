---
name: Create Strategy (LEAN)
description: Use this skill when you need to add a new LEAN QCAlgorithm strategy in Python.
---

# Create Strategy (LEAN QCAlgorithm)

Use when adding a new strategy under the Strategy Lab `strategies/` workspace.

## Steps

1) Create the strategy file
- Path: `server/strategies/<StrategyName>.py`
- Must define a `QCAlgorithm` class with `Initialize` and `OnData`.

2) Use AERA-injected parameters
- Read with `GetParameter(...)` and provide safe defaults:
  - `symbol`, `resolution`, `cash`, `feeBps`, `slippageBps`

3) Keep it LEAN-safe
- No network I/O.
- Avoid writing files from the algorithm.
- Keep logs short (no spam).

4) Verify
- Run from the app: Strategy Lab -> Run (LEAN) and inspect job logs/results.
- Run standard validations: see `skills/verify_changes/SKILL.md`.

## Template

Start from `skills/create_strategy/template_strategy.py`.

