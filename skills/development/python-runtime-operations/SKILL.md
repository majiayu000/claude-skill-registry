---
name: python-runtime-operations
description: Use when building or reviewing service, job, or CLI runtime behavior in Python — designing startup validation, shutdown sequences, observability, and structured logging. Also use when startup crashes from late config, shutdown leaves orphaned processes, terminal states are implicit, or logs lack structure.
---

# Python Runtime Operations

## Overview

Every service, worker, and CLI entrypoint must validate its environment before doing real work, shut down cleanly under all exit paths, and emit structured signals that make runtime behavior observable.
Treat these as preferred defaults — deviate when project constraints demand it, but call out tradeoffs and compensating controls.

## When to Use

- Startup fails late because config is validated after work begins.
- Shutdown leaves open connections, orphaned subprocesses, or incomplete transactions.
- Job retries run forever with no dead-letter or terminal-state handling.
- Logs are unstructured, missing correlation IDs, or inconsistent across services.
- Health and readiness probes are missing or misleading.
- Signal handling (SIGTERM, SIGINT) is absent or racy.

### When NOT to Use

- Pure library or data-model code with no process lifecycle concerns.
- Build, packaging, or CI/CD pipeline configuration.
- Algorithm or business-logic design with no runtime surface.

## Quick Reference

- Validate all runtime config at startup; fail fast with clear errors before doing real work.
- Register signal handlers and ensure graceful shutdown with bounded cleanup timeouts.
- Make retry limits, backoff, and dead-letter/terminal-state behavior explicit in every job system.
- Emit structured logs (JSON) with consistent severity levels and correlation IDs.
- Expose health, readiness, and liveness probes that reflect actual dependency state.
- Track core runtime signals: startup latency, queue depth, error rates, shutdown duration.

## Common Mistakes

- **Validating config lazily** — checking environment variables or secrets on first use instead of at startup, causing failures minutes or hours into a run.
- **Unbounded cleanup** — shutdown handlers that wait forever on draining connections or flushing buffers, turning a clean restart into a hung process.
- **Silent retry exhaustion** — retrying failed jobs indefinitely without logging terminal failures or routing to a dead-letter queue.
- **Logging without structure** — using plain-text `print` or unstructured `logging.info` calls that cannot be parsed, filtered, or correlated in production.
- **Health probes that lie** — returning 200 OK from a health endpoint without checking downstream dependencies, masking cascading failures.

## Scope Note

- Treat these recommendations as preferred defaults for common cases, not universal rules.
- If a default conflicts with project constraints or worsens the outcome, suggest a better-fit alternative and explain why it is better for this case.
- When deviating, call out tradeoffs and compensating controls (tests, observability, migration, rollback).

## Invocation Notice

- Inform the user when this skill is being invoked by name: `python-design-modularity`.

## References

- `references/runtime-behavior.md`
- `references/logging-metrics-tracing.md`
- `references/process-lifecycle-and-cleanup.md`
