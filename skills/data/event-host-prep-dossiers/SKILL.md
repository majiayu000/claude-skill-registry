---
name: event-host-prep-dossiers
description: >-
  DRAFT. Build anonymizable host-prep one-pagers for must-meet guests at an
  in-person event: rank, enrich, light research, warm-intro angles, PDF pack.
  Not installed by deepline skills. No real customer data in repo samples.
---

# Event host-prep dossiers (DRAFT)

## When to use

Hosts need a printable pack: photo, role history, why they matter, 2–4 talk tracks.
Use after `event-ops-score-and-door` produces a host-hit shortlist.

## Pipeline

1. Take top N (default 40) from host-hit / hot segment.
2. Person enrich via LinkedIn URL when present (photo, experience).
3. Light web research: 3–8 bullets from public sources only; cite source names.
4. Warm-intro score 0–10 + `name_game_hooks` + `avoid` line.
5. Render one page per person → combined PDF.
6. Deliver folder locally; do not email externally unasked.

## Sample data

Only fictional rows in `templates/sample-shortlist.csv`.

## Guardrails

- Never invent employment or education.
- Cache photos; placeholder if missing.
- Ask before paid enrich > agreed pilot budget.
- Scrub real customer CSVs before committing anywhere public.
