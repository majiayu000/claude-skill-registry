---
name: event-ops-score-and-door
description: >-
  DRAFT. Score Luma/RSVP lists, approve against capacity, produce host-hit shortlists
  and day-of door packs. Systems framing — not a marketing CSV dump.
  Not installed by deepline skills.
---

# Event ops: score, approve, door pack (DRAFT)

## Thesis

A full Luma page is demand. Pipeline starts at **who gets a seat**, **who hosts must meet**, and **show/no-show writeback** — not at another invite channel.

## Flow

1. **Ingest** pending/waitlist/approved export (`templates/guests.schema.csv`).
2. **Enrich** missing title/company/LinkedIn (pilot ≤10 first).
3. **Score** into hot/warm/low/skip (`references/scoring.md`).
4. **Capacity approve** — dry-run diff before any Luma status changes.
5. **Host-hit list** — top 20–40 with why + intro angle (optional dossier skill next).
6. **Door pack** — name, company, segment, check-in box, host flags.
7. **Closeout** — show/no-show column for CRM writeback within 24–48h.

## Outputs

- `scored.csv`
- `approve-dry-run.diff.md`
- `host-hits.csv`
- `door-list.csv` / printable PDF if available
- `#event-ops` checklist owner

## Guardrails

- Scoring that never changes seats is a dashboard. This skill must change seats or explicitly say why not.
- No mass approve without capacity number on screen/log.
