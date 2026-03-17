---
name: markdowntown-analytics
description: Use this when instrumenting analytics, reviewing event taxonomy, or handling privacy/redaction rules for markdowntown.
---

# Analytics + privacy

## When to use
- Adding new analytics events or UI telemetry.
- Auditing payloads for privacy and redaction.
- Updating monitoring/funnel definitions.

## Workflow
1. **Find existing events**
   - Check event taxonomy and funnels before adding new names.
   - Use existing event names where possible; add new ones only when needed.

2. **Instrument safely**
   - Client events flow through `track`/`trackError` in `src/lib/analytics.ts`.
   - Redaction happens in `redactAnalyticsPayload` before PostHog capture.

3. **Privacy expectations**
   - Never send raw file paths, cwd values, or repo names.
   - Use counts or booleans instead of raw content.

4. **Validate + monitor**
   - Update docs for event taxonomy and monitoring where needed.
   - Add/adjust tests for redaction and analytics utilities.

## References
- codex/skills/markdowntown-analytics/references/analytics.md
- codex/skills/markdowntown-analytics/references/redaction.md

## Guardrails
- Analytics should be optional (env controlled) and must not break UI.
- Never include secrets, file paths, cwd values, or raw content in analytics payloads.
- Always log follow-up tasks when you spot missing events or gaps.
