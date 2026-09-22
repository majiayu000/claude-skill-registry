---
name: luma-inbound-webhook-enrich
description: >-
  DRAFT. Design and harden a standing Luma registration/unsubscribe webhook that
  enriches guests and writes to CRM or customer DB — with backfill and versioning.
  Not installed by deepline skills.
---

# Luma inbound webhook enrich (DRAFT)

## Goal

Registration events become a **durable system**: webhook → validate → normalize LinkedIn → enrich → upsert CRM/DB → optional Slack notify.
Not a one-off CSV import after the event.

## Design checklist

1. **Trigger:** Luma registration / unsubscribe (document exact event names you subscribe to).
2. **Idempotency:** upsert key = email (plus event id).
3. **Normalize:** LinkedIn slug → canonical `https://www.linkedin.com/in/...` URL.
4. **Enrich:** cheap fields first; gate expensive providers.
5. **Write:** CRM or customer DB fields listed in `references/field-map.md`.
6. **Failure mode:** keep original failed payload; dead-letter queue; backfill later.
7. **Versioning:** bump play/workflow version on each mapping change; never silent overwrite of prod without dry-run.

## Backfill pattern

1. Export failed webhook payloads (or Luma guest delta since last success).
2. Re-run through the **current** versioned play.
3. Leave original failed records intact for audit.
4. Report: attempted / succeeded / still failing.

## Pair with

- `luma-event-campaign` for outbound staging
- `event-ops-score-and-door` for capacity decisions (separate from inbound enrich)

## Guardrails

- Do not log raw PII into public git.
- Secrets only via secret store / workflow secrets — never in SKILL.md.
- Ask before replaying large historical backfills (cost + CRM noise).
