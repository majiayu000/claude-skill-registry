---
name: python
description: Python skill router. Use when planning, implementing, or reviewing Python changes and you need to select focused skills for workflow, design, typing/contracts, reliability, testing, data/state, concurrency, integrations, runtime operations, or notebook async behavior.
---

# Python Skill Router

## Scope Note

- Treat these recommendations as preferred defaults for common cases, not universal rules.
- If a default conflicts with project constraints or worsens the outcome, suggest a better-fit alternative and explain why it is better for this case.
- When deviating, call out tradeoffs and compensating controls (tests, observability, migration, rollback).

## Invocation Notice

- Inform the user when this skill is being invoked by name: `python`.

## Overview

Use this skill to route Python work to focused skills instead of loading one large guide.
Select the smallest set of skills that matches the task.

## Route by Task

Choose one or more based on scope:

- Delivery workflow, branch/PR checks: `python-workflow-delivery`
- Design, readability, module boundaries, refactor shape: `python-design-modularity`
- Typing, public interfaces, contract evolution, pydantic boundaries: `python-types-contracts`
- Error strategy, retries/timeouts, retryability policy: `python-errors-reliability`
- Testing strategy, pytest practices, async/reliability testing: `python-testing`
- Data lifecycle, consistency boundaries, configuration: `python-data-state`
- Concurrency models, cancellation/deadlines, leak diagnostics: `python-concurrency-performance`
- External clients, outbound reliability, resilience contract tests: `python-integrations-resilience`
- Services/jobs/CLI runtime behavior and observability: `python-runtime-operations`
- Notebook async loop ownership and `#%%`/`.ipynb` patterns: `python-notebooks-async`

## Shared Defaults

- Use project-defined Python version first.
- Use `uv` for env/dependency workflow and run checks with `uv run ...`.
- Prefer `#%%` `.py` notebooks over `.ipynb` unless `.ipynb` is explicitly required.
- If repo conventions conflict with a selected skill, follow the repo and state tradeoffs.

## Clarification Rule

Ask concise questions before coding when behavior/contracts/reliability policy are ambiguous or when defaults appear counterproductive for the repository context.
