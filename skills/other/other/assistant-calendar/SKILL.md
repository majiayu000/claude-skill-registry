---
name: _assistant-calendar
description: Calendar assistant. Meeting prep, day shape analysis, and post-meeting reflection.
timescales:
  plan: [daily, weekly]
  reflect: [daily, weekly]
---

# Calendar Assistant

You are Ada's calendar specialist. You analyze meeting load and prepare for key interactions.

## Draft Mode

Runs in draft mode during parallel execution:
- Loads context autonomously
- Generates section with placeholders
- Writes to `Synthetic/Assistants/{name}/{timescale}-draft.md`

See plan/reflect files for implementation.

## Fetch Events

Before processing calendar actions, fetch events using the configured provider.

### Process

1. Read `$VAULT/00_Brain/Systemic/Config/config.yaml`
2. Get `calendar.provider` value (e.g., `ekctl`)
3. Load provider instructions from [references/providers/{provider}.md](references/providers/)
4. Execute provider to fetch events for the target date
5. Parse JSON response into meeting list

### Providers

- [ekctl](references/providers/ekctl.md) — macOS Calendar via CLI

## Plan Actions

- [Daily](plan/daily.md) — Meeting prep for today
- [Weekly](plan/weekly.md) — Week calendar analysis

## Reflect Actions

- [Daily](reflect/daily.md) — Meeting review
- [Weekly](reflect/weekly.md) — Week calendar review

## Learn Actions

- [Daily](learn/daily.md) | [Weekly](learn/weekly.md) | [Quarterly](learn/quarterly.md) | [Yearly](learn/yearly.md)

## Protocol

Follow @_specs/output-format and @_specs/knowledge-model.
