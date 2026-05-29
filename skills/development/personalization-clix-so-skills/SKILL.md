---
name: clix-personalization
display-name: Personalization
short-description: Personalization templates
description: Helps developers author and debug Clix personalization templates
  (Liquid-style) for message content, deep links/URLs, and audience targeting.
  Use when the user mentions personalization variables, Liquid, templates,
  conditional logic, loops, filters, deep links, message logs, or when the user
  types `clix-personalization`.
user-invocable: true
---

# Clix Personalization

Use this skill to help developers write **personalized Clix campaigns** using
template-based variables and light logic in:

- **Message content** (title, body, subtitle)
- **Links** (dynamic URL or deep link params)
- **Audience targeting** (conditional include/exclude rules)

## What the official docs guarantee (high-signal)

- **Data namespaces**:
  - `user.*` (user traits/properties)
  - `event.*` (event payload properties)
  - `trigger.*` (custom properties passed via API-trigger)
  - Device/system vars: `device.id`, `device.platform`, `device.locale`,
    `device.language`, `device.timezone`, plus `user.id`, `event.name`
- **Missing variables** render as an **empty string**.
- **Output**: print values with `{{ ... }}`.
- **Conditionals**: `{% if %}`, `{% else %}`, `{% endif %}` with operators
  `== != > < >= <= and or not`. Invalid conditions evaluate to `false`.
- **Loops**: `{% for x in y %}` / `{% endfor %}` (use guards for empty lists).
- **Filters**: `upcase`, `downcase`, `capitalize`, `default`, `join`, `split`,
  `escape`, `strip`, `replace` (chain with `|`).
- **Errors**: template rendering errors show up in **Message Logs**.

## MCP-first (source of truth)

If the Clix MCP tools are available, treat them as the source of truth:

- `clix-mcp-server:search_docs` for personalization behavior and supported
  syntax

If MCP tools are not available, use the bundled references in `references/`.

## Workflow (copy + check off)

```
Personalization progress:
- [ ] 1) Identify where the template runs (message / URL / audience rule)
- [ ] 2) Identify trigger type (event-triggered vs API-triggered)
- [ ] 3) Confirm available inputs (user.*, event.*, trigger.*, device.*)
- [ ] 4) Draft templates with guards/defaults
- [ ] 5) Validate template structure (balance tags, avoid missing vars)
- [ ] 6) Verify in Clix (preview/test payloads, check Message Logs)
```

## 1) Confirm the minimum inputs

Ask only what’s needed:

- **Where used**: title/body/subtitle vs URL/deep link vs audience targeting
  rule
- **Campaign trigger**:
  - Event-triggered → `event.*` is available
  - API-triggered → `trigger.*` is available
- **Inputs**:
  - Which `user.*` properties are set by the app
  - Which `event.*` / `trigger.*` properties are passed (include example
    payload)
- **Fallback policy**: what to show when data is missing (default strings,
  guards)

## 2) Produce a “Template Plan” (before tweaking lots of templates)

Return a compact table the user can approve:

- **field** (title/body/url/audience)
- **template** (Liquid)
- **required variables** (and their source: user/event/trigger/device)
- **fallbacks** (default filter and/or conditional guards)
- **example payload** + **expected rendered output**

## 3) Authoring guidelines (what to do by default)

- Prefer **simple variables + `default`** over complex branching.
- Add **guards** for optional data and for arrays (`size > 0`) before looping.
- Prefer **pre-formatted** properties from your app (e.g., `"7.4 miles"`,
  `"38m 40s"`) instead of formatting inside templates.
- Keep logic minimal; complex branching belongs in the app or segmentation
  setup.

## 4) Validation (fast feedback loop)

If you have a template file (recommended for review), run:

```bash
bash <skill-dir>/scripts/validate-template.sh path/to/template.liquid
```

This script does lightweight checks (matching `{% if %}`/`{% endif %}`,
`{% for %}`/`{% endfor %}`, and brace balancing). It can’t guarantee the
variables exist — you still need a payload + console verification.

## 5) Verification checklist

- **Missing data**: does the template still read well with empty strings?
- **Trigger type**: API triggers use `trigger.*` (not `event.*`).
- **Message Logs**: check rendering errors and fix syntax issues first.
- **Upstream data**:
  - If `user.*` is missing → fix user property setting (see
    `clix-user-management`)
  - If `event.*` is missing → fix event tracking payload (see
    `clix-event-tracking`)

## Progressive Disclosure

- **Level 1**: This `SKILL.md` (always loaded)
- **Level 2**: `references/` (load when writing/debugging templates)
- **Level 3**: `scripts/` (execute directly, do not load into context)

## References

- `references/template-syntax.md` - Variables, output, conditionals, loops,
  filters
- `references/common-patterns.md` - Copy/paste patterns for messages + URLs +
  guards
- `references/debugging.md` - Troubleshooting missing variables and Message Logs
