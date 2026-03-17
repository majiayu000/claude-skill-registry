---
name: convex
description: |
  Build and operate Convex backends: functions (queries/mutations/actions/http actions), schemas,
  auth patterns, scheduling (cron/scheduled/workflows), file storage, testing, and debugging.
  Triggers: "convex", "query", "mutation", "action", "httpAction", "schema", "validator",
  "cron", "schedule", "workflow", "workpool", "ctx.db", "ctx.auth", "convex dev".
license: MIT
compatibility: Works best with Convex MCP (recommended) or Convex CLI (npx convex). Targets repos with a `convex/` directory.
metadata:
  version: "1.0"
---

# Convex

Convex backend skill with a bias toward safety, observability, and index-backed queries.

## Docs-First Rule (Blocking)

Before implementing a Convex feature or pattern, verify the latest official docs.

Primary sources:

- https://docs.convex.dev/
- https://stack.convex.dev/

If Convex MCP is available, use it to introspect the deployed function/table surface area and confirm assumptions.

## Environments (Dev / Preview / Prod)

Convex projects typically have:

- Dev deployments (your local `npx convex dev` sync target)
- Preview deployments (branch/PR deployments, beta feature)
- Production deployment

Use MCP `status` (if available) or the CLI to confirm which deployment you are connected to before making changes.

## Components-First Rule

Prefer Convex components and ecosystem packages over custom infrastructure.

Start at:

- https://docs.convex.dev/components
- `references/ecosystem.md`

## Core Rule (Blocking)

Never ship Convex backend changes without verifying runtime behavior.

Preferred verification order:

1) Convex MCP logs (structured, diffable)
2) `npx convex dev` terminal logs
3) Convex Dashboard logs

## Project Conventions (Preferred)

- Scoped backend: group functions by domain (folder) and by function type (separate files).
- Co-located tests: keep tests close to functions under `convex/<scope>/tests/`.
- Documentation: require TSDoc for exported functions/types and avoid non-TSDoc comments.

See `references/style.md` and `references/testing.md`.

## Router

| User says | Load reference | Do |
|---|---|---|
| help / cli help / usage | `references/cli-help.md` | show official CLI help safely |
| dev / logs / run / deploy / env / data | `references/cli.md` | common CLI workflows |
| mcp / tools / introspect / logs | `references/mcp.md` | use Convex MCP tools |
| tsdoc / docs / style | `references/style.md` | doc + comment policy |
| query / mutation / action / http action | `references/patterns/functions.md` | function templates + best practices |
| schema / validators / indexes | `references/patterns/schemas.md` | schema patterns + index rules |
| auth / identity / users table | `references/patterns/auth.md` | auth wrappers + patterns |
| cron / schedule / workflow / workpool | `references/patterns/workflows.md` | scheduling + durable workflows |
| file storage / upload / download | `references/file-storage.md` | file storage patterns |
| http / webhook | `references/patterns/http.md` | httpRouter/httpAction patterns |
| testing | `references/testing.md` | testing patterns |
| ecosystem / components | `references/ecosystem.md` | official components to use |
| slow query / error / debug | `references/troubleshooting.md` | troubleshooting + anti-patterns |
| validate / checklist | `checklists/validation.md` | blocking checks before shipping |

## MCP Integration (Recommended)

If Convex MCP is available, use it first.

If Convex MCP is not available, this skill still works:

- Use the Convex CLI (`npx convex ...`) and the dashboard.
- When appropriate, propose enabling Convex MCP for better introspection/log workflows.

- Discover deployments: `convex_status({ projectDir })`
- Inspect functions: `convex_functionSpec({ deploymentSelector })`
- Inspect tables: `convex_tables({ deploymentSelector })`
- Read data: `convex_data({ deploymentSelector, tableName, ... })`
- Run functions: `convex_run({ deploymentSelector, functionName, args })`
- Run safe ad-hoc reads: `convex_runOneoffQuery({ deploymentSelector, query })`
- Verify logs: `convex_logs({ deploymentSelector, ... })`

Full workflow: `references/mcp.md`.

## Critical Rules (7)

1) Always use validators (`args` + `returns`) for functions.
2) Always use explicit table names with `ctx.db.get/patch/replace`.
3) Prefer index-backed queries (`withIndex`) and bounded reads (`take`/pagination).
4) User identity comes from `ctx.auth`, never from args.
5) Use `internal*` functions for sensitive operations.
6) Schedule only internal functions.
7) Use `v.null()` for void returns (return `null`).

## References

- Patterns:
  - `references/patterns/schemas.md`
  - `references/patterns/functions.md`
  - `references/patterns/auth.md`
  - `references/patterns/workflows.md`
  - `references/patterns/http.md`
- Other:
  - `references/mcp.md`
  - `references/cli.md`
  - `references/cli-help.md`
  - `references/style.md`
  - `references/file-storage.md`
  - `references/testing.md`
  - `references/ecosystem.md`
  - `references/troubleshooting.md`
- Checklist:
  - `checklists/validation.md`
