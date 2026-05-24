# Audit output schema

The exact structure of the audit output. Follow this precisely. It is read both by the user and by the agent on future audits (for comparison + progress tracking).

## Folder layout (changed 2026-04-15)

Each audit run writes to a per-date folder, not a single file:

```
~/.flowhunt/audits/
  2026-04-15/
    audit.md                      # the human-readable report (schema below)
    raw/
      activitywatch.json          # top-100 AFK-filtered AW query output
      gmail.json                  # pruned Gmail search response
      calendar.json               # Calendar events list
      slack.json                  # Slack data if collected
      tasks.json                  # Live tracker output (Linear, Notion, ...)
      tasks.md                    # Copy of ~/.flowhunt/tasks.md if user is in manual mode
      user-proposed.md            # Raw user answers to "what would YOU automate?"
      intake.json                 # What the user answered during setup
```

**Always dump raw.** The audit.md is the narrative; `raw/` is the source of truth. Future re-analysis (same user with a different angle, or a different agent loading the same folder) depends on raw being there.

## audit.md structure

## Full template

```markdown
---
date: 2026-04-15
window_days: 30
data_sources:
  activitywatch: ok
  gmail: ok | unconnected | error:<msg>
  calendar: ok | unconnected | error:<msg>
  tasks: ok:<tracker> | manual | unconnected | skipped
  slack: ok | unconnected | error:<msg>
  imessage: ok | unconnected | skipped
  telegram: ok | unconnected | skipped
  discord: ok | unconnected | skipped
agent: claude-code | codex | opencode | gemini | unknown
language: pl | en | ...
goal_anchor: <one-line copy of workflow_context.goal — for diffing across audits>
---

# FlowHunt audit — 2026-04-15

## Kontekst

> Powtarzamy żeby user widział, że audit zna jego sytuację. Cztery linijki, kopie z `intake.json` → `workflow_context`. Jak `workflow_context` brak (legacy audit), pomiń tę sekcję.

- **Rola:** <workflow_context.role>
- **Główne bóle (TY je wskazałeś):** <workflow_context.time_drains, joined>
- **Święte / nie ruszamy:** <workflow_context.sacred, joined — albo "nic" jak puste>
- **Cel audytu:** <workflow_context.goal>

## Summary

<Two sentences max. #1 thing to automate first and why. If data is thin, say so here.>

**Estimated time saved:** <one short string, e.g. "4-6h / week">

## Patterns

- <pattern 1 — specific, tied to numbers from the data>
- <pattern 2>
- <pattern 3>
- ...

## Automation recommendations

### 1. <one-line title of the #1 thing to automate>

- **What:** <one sentence describing the specific thing to automate>
- **How:** <one sentence describing the concrete tool / integration / approach>
- **Estimated saved:** <hours per week>

### 2. <second title>

- **What:** ...
- **How:** ...
- **Estimated saved:** ...

### 3. <third title>

...

<Continue for as many recommendations as the data supports. 3-6 is typical.>

## Not worth automating

- <thing 1 — one line why not>
- <thing 2>
- ...

## User-proposed automations

<Populated in Step 6 of audit.md — after asking the user "what would YOU automate?".
Verbatim or lightly-edited user answers, each followed by your short suggestion for
how it could be built. If the user did not propose anything, write one line:
"(nic nie zgłoszono w tej sesji)".>

### <user's idea #1 as they phrased it>

- **What:** <their phrasing>
- **How (agent's suggestion):** <one-sentence stack / approach>
- **Estimated saved:** <their estimate or "user didn't say">

### <user's idea #2>

...

## Data sources used this run

| Source | Status | Volume |
|---|---|---|
| ActivityWatch | ok | <X days, Y top entries> |
| Gmail | ok/unconnected | <N messages scanned> |
| Google Calendar | ok/unconnected | <N events scanned> |
| Task tracker | ok:<name> / manual / unconnected | <N tasks, N completed, N recurring> |
| Slack | ok/unconnected | <N channels, N messages> |
| iMessage | skipped | - |
| Telegram | skipped | - |

## Change since last audit

<If a previous audit exists in ~/.flowhunt/audits/, add this section. Otherwise omit.>

- Recommendation #1 from previous audit: **built / in progress / abandoned / still recommended**
- New patterns since <previous_date>: ...
- Estimated time saved delta: <+/- Xh>
```

## Rules for writing the file

1. **Frontmatter is mandatory.** The next audit run reads it to understand what data was available last time. Never skip it.
2. **Section order is fixed.** Summary → Patterns → Recommendations → Not worth → Data sources → Change since last. Do not reorder, do not merge sections.
3. **Recommendations numbered in priority order.** #1 is the single most impactful thing to automate first. If you cannot defend that ordering in the Summary, the ordering is wrong.
4. **"Estimated saved" is honest.** If you cannot put a number on it, do not put one. Write "hard to estimate — depends on how often X happens" and move on.
5. **Data sources table is always present** even when only ActivityWatch was available. It communicates the shape of the audit transparently.
6. **"Change since last audit" is only included when a previous audit file exists.** Otherwise omit the section entirely — do not write "no previous audit".
7. **Language matches the user's language.** This file is a user-facing artifact, not an English-only log.

## Example (minimal, ActivityWatch only, thin data)

```markdown
---
date: 2026-04-15
window_days: 30
data_sources:
  activitywatch: ok
  gmail: unconnected
  calendar: unconnected
  slack: unconnected
  imessage: skipped
  telegram: skipped
agent: claude-code
language: pl
---

# FlowHunt audit — 2026-04-15

## Summary

Dane są cienkie — tylko 5 dni ActivityWatch, brak podpiętego Gmaila i Slacka.
Najpilniejsze: uruchom audit ponownie za 10 dni, a tymczasem podłącz Gmail
(najsilniejszy sygnał w twoim stacku skoro spędzasz 40% czasu w Gmailu w Brave).

**Estimated time saved:** depends on connectors — re-run after 14 days

## Patterns

- 42% czasu aktywnego spędzasz w przeglądarce, z czego ~18% to Gmail (tytuł "Inbox - Gmail")
- 3 okna Warp otwarte równolegle przez >2h dziennie, tytuły sugerują pracę w Claude Code
- ...

## Automation recommendations

### 1. Podłącz Gmail do flowhunt

- **What:** Włącz konektor Gmail w Claude, bo bez niego audit nie widzi twojej głównej osi pracy.
- **How:** Otwórz https://claude.ai/settings/connectors i kliknij Connect przy Gmail.
- **Estimated saved:** enables the rest of the audit

### 2. ...

## Not worth automating

- ...

## Data sources used this run

| Source | Status | Volume |
|---|---|---|
| ActivityWatch | ok | 5 days, 87 entries |
| Gmail | unconnected | - |
| Google Calendar | unconnected | - |
| Slack | unconnected | - |
| iMessage | skipped | - |
| Telegram | skipped | - |
```
