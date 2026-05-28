---
name: phoenix-code-review
description: Reviews Phoenix code for controller patterns, context boundaries, routing, and plugs. Use when reviewing Phoenix apps, checking controllers, routers, or context modules.
---

# Phoenix Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Bounded contexts, Ecto integration | [references/contexts.md](references/contexts.md) |
| Actions, params, error handling | [references/controllers.md](references/controllers.md) |
| Pipelines, scopes, verified routes | [references/routing.md](references/routing.md) |
| Custom plugs, authentication | [references/plugs.md](references/plugs.md) |

## Review Checklist

### Controllers
- [ ] Business logic in contexts, not controllers
- [ ] Controllers return proper HTTP status codes
- [ ] Action clauses handle all expected patterns
- [ ] Fallback controllers handle errors consistently

### Contexts
- [ ] Contexts are bounded by domain, not technical layer
- [ ] Public functions have clear, domain-focused names
- [ ] Changesets validate all user input
- [ ] No Ecto queries in controllers

### Routing
- [ ] Verified routes (~p sigil) used, not string paths
- [ ] Pipelines group related plugs
- [ ] Resources use only needed actions
- [ ] Scopes group related routes

### Plugs
- [ ] Authentication/authorization via plugs
- [ ] Plugs are composable and single-purpose
- [ ] Halt called after sending response in plugs

### JSON APIs
- [ ] Proper content negotiation
- [ ] Consistent error response format
- [ ] Pagination for list endpoints

## Valid Patterns (Do NOT Flag)

- **Controller calling multiple contexts** - Valid for orchestration
- **Inline Ecto query in context** - Context owns its data access
- **Using `action_fallback`** - Centralized error handling pattern
- **Multiple pipelines per route** - Composition is intentional
- **`Plug.Conn.halt/1` without send** - May be handled by fallback

## Context-Sensitive Rules

| Issue | Flag ONLY IF |
|-------|--------------|
| Missing changeset validation | Field accepts user input AND no validation exists |
| Controller too large | More than 7 actions OR actions > 20 lines |
| Missing authorization | Route is not public AND no auth plug in pipeline |

## Gates (run in order; each step has a pass condition)

1. **Anchored evidence** — For every planned finding, open the source and note **file path + line number** from that read (not from memory or diff snippets alone). **Pass:** each finding cites `path:line` that you opened.
2. **“Handled elsewhere” sweep** — Before reporting “missing validation,” “missing auth,” or “wrong status,” search the router (pipelines/scopes), controller (`action_fallback`, `plug`), and relevant context for existing checks. **Pass:** you recorded whether handling exists elsewhere (yes + where, or no after search).
3. **Verification protocol** — Load and apply [review-verification-protocol](../review-verification-protocol/SKILL.md) for the issue type. **Pass:** that skill’s pre-report checks for that finding class are satisfied before you write the finding.
4. **Finding shape** — Emit each issue as `[FILE:LINE] ISSUE_TITLE` with a one-line rationale tied to the cited code. **Pass:** every line matches that pattern.

## Before Submitting Findings

Do not report until **Gates** above pass. For full anti-false-positive steps, follow [review-verification-protocol](../review-verification-protocol/SKILL.md).
