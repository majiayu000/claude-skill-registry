---
name: python-notebooks-async
description: "Use when writing or reviewing asyncio code in Jupyter notebooks or '#%%' cell workflows — structuring event-loop ownership, orchestrating async tasks, or choosing compatibility strategies. Also use when hitting RuntimeError: This event loop is already running, asyncio.run() failures in cells, or tasks silently never completing."
---

# Python Notebooks Async

## Overview

Notebook kernels own the event loop; async code must cooperate with that ownership rather than fight it.
This skill covers orchestration patterns, top-level `await`, and compatibility constraints for `.ipynb` and `#%%` workflows.

Treat these recommendations as preferred defaults.
When project constraints require deviation, call out tradeoffs and compensating controls.

## When to Use

- `asyncio.run()` raises `RuntimeError` inside a notebook cell.
- Event-loop conflicts when mixing async libraries in Jupyter.
- Porting async scripts into notebook workflows.
- Orchestrating concurrent tasks (`gather`, `TaskGroup`) in IPython kernels.
- Deciding where to place reusable async logic across notebook/module boundaries.

### When NOT to Use

- Pure script or service code with no notebook involvement — see `python-concurrency-performance`.
- Synchronous notebook workflows with no async needs.
- General asyncio API design outside notebook contexts — see `python-runtime-operations`.

## Quick Reference

- Treat notebook kernels as loop-owned environments; never create a competing loop.
- Use top-level `await` instead of `asyncio.run()` in notebook cells.
- Orchestrate concurrent work with `asyncio.gather()` or `asyncio.TaskGroup`.
- Keep reusable async logic in regular `.py` modules, imported into notebooks.
- Use `nest_asyncio` only as a constrained compatibility fallback, not a default.
- Avoid fire-and-forget tasks — always `await` or collect results explicitly.

## Common Mistakes

- **Calling `asyncio.run()` in a notebook cell.**
  The kernel already runs a loop; `asyncio.run()` tries to start a second one and raises `RuntimeError`.
  Use `await` directly instead.
- **Applying `nest_asyncio` globally by default.**
  It patches the loop to allow reentrant calls but masks design problems and can hide subtle concurrency bugs.
  Reserve it for legacy compatibility.
- **Defining async helpers inline in cells instead of modules.**
  Inline definitions are lost on kernel restart and cannot be tested outside the notebook.
  Extract to `.py` files.
- **Ignoring returned tasks or coroutines.**
  Calling an async function without `await` silently produces a never-executed coroutine object, with no error until results are missing downstream.
- **Mixing blocking I/O with async in the same cell.**
  Synchronous calls like `requests.get()` block the event loop, starving concurrent tasks.
  Use `aiohttp`, `httpx`, or `asyncio.to_thread()`.

## Scope Note

- Treat these recommendations as preferred defaults for common cases, not universal rules.
- If a default conflicts with project constraints or worsens the outcome, suggest a better-fit alternative and explain why it is better for this case.
- When deviating, call out tradeoffs and compensating controls (tests, observability, migration, rollback).

## Invocation Notice

- Inform the user when this skill is being invoked by name: `python-design-modularity`.

## References

- `references/notebooks-async.md`
