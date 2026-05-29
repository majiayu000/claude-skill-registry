---
name: clix-event-tracking
display-name: Event Tracking
short-description: Event tracking setup
description: Implements Clix event tracking (Clix.trackEvent) with consistent naming, safe
  property schemas, and campaign-ready validation. Use when adding, reviewing,
  or debugging event tracking; when configuring event-triggered campaigns; or
  when the user mentions events, tracking, funnels, or properties — or when the
  user types `clix-event-tracking`.
user-invocable: true
---

# Tracking Clix Events

Use this skill to help developers design and implement **Clix event tracking**
via `Clix.trackEvent(...)` so events can drive **event-triggered campaigns**,
**audience filters**, and **personalization**.

## What the official docs guarantee (high-signal)

- **When to track**: identify the user action/system event, then attach
  meaningful properties (funnel checkpoints, milestones, button taps).
- **Property normalization**: booleans/numbers/strings map directly; date-like
  values serialize to ISO 8601; unsupported objects become strings.
- **Error handling**: event tracking calls can throw—always handle errors so the
  app stays robust.

## MCP-first (source of truth)

If Clix MCP tools are available, treat them as the **source of truth**:

- `clix-mcp-server:search_docs` for conceptual behavior (campaign triggers,
  personalization)
- `clix-mcp-server:search_sdk` for exact SDK signatures per platform

If MCP tools are not available, use the bundled references:

- Event API contract + pitfalls → `references/trackevent-contract.md`
- Naming + schemas + privacy → `references/naming-and-schema.md`
- Implementation patterns → `references/implementation-patterns.md`
- Campaign mapping → `references/campaign-mapping.md`
- Debugging checklist → `references/debugging.md`

## Workflow (copy + check off)

```
Event tracking progress:
- [ ] 1) Confirm platform(s) and goals (analytics vs campaign triggers)
- [ ] 2) Propose event plan (names, when fired, properties, where in code)
- [ ] 3) Validate plan (names, keys, types, PII constraints)
- [ ] 4) Implement trackEvent calls (platform-correct)
- [ ] 5) Verify: events fire once, serialize cleanly, match campaign configs
```

## 1) Confirm the minimum inputs

Ask only what’s needed:

- **Platform**: iOS / Android / React Native / Flutter
- **Goal**: analytics only, event-triggered campaigns, or both
- **Top flows** (1–3): e.g., onboarding, checkout, subscription
- **PII policy**: what must never be sent (email/phone/name/free-text, etc.)

## 2) Propose an “Event Plan” (before touching code)

Return a compact table the user can approve:

- **event_name** (stable, `snake_case`)
- **when** (exact moment the event fires)
- **properties** (key + type, mark required vs optional)
- **location** (file/function/UI handler/network response)
- **purpose** (campaign trigger / analytics / both)

If campaigns are involved, remind: **event names and property keys must match
exactly** in the Clix console.

## 3) Validate the plan (fast feedback loop)

Create `event-plan.json` in `.clix/` directory (recommended) or project root:

**Recommended location**: `.clix/event-plan.json`

- Organized: keeps tooling configs together
- Hidden: doesn't clutter project root
- Committable: planning document for team review

**Alternative**: `event-plan.json` in project root (simpler, but less organized)

**For agents**: Locate `scripts/validate-event-plan.sh` in the installed skill
directory, then run it:

```bash
# From project root:
bash <skill-dir>/scripts/validate-event-plan.sh .clix/event-plan.json
# Or if in root:
bash <skill-dir>/scripts/validate-event-plan.sh event-plan.json
```

The skill directory is typically:

- `.cursor/skills/event-tracking/` (Cursor)
- `.claude/skills/event-tracking/` (Claude Code)
- `.vscode/skills/event-tracking/` (VS Code)
- `.agents/skills/event-tracking/` (Amp)
- Or check where this skill was installed

If validation fails: fix the plan first, then implement.

## 4) Implement tracking (platform-correct)

Use MCP to fetch the exact `trackEvent` signature for the platform; then:

- **Place calls at stable boundaries** (action confirmed, request succeeded,
  state updated)
- **Avoid duplicates** (don’t fire on every render; debounce where needed)
- **Avoid null/complex values** (prefer primitives; serialize dates to ISO)
- **Do not track PII by default**

See `references/implementation-patterns.md` for placement heuristics and code
patterns.

## 5) Verify

Minimum verification:

- Event fires **exactly once** per user action (or the intended cadence)
- Properties are **primitive + stable** (no null surprises)
- For campaigns: console trigger conditions match **exact names/keys**

For troubleshooting steps, see `references/debugging.md`.
