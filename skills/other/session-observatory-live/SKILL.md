---
name: session-observatory-live
description: "Conversational guide for using tools/session-retro/observe.mjs to capture friction, wins, corrections, decisions, gaps, tool-use, and checkpoints as they happen during a session. Use at session start (to kick off the log), at inflection points (to record events), and at session end (to archive and feed the retrospective generator)."
format: 2025-10-02
version: 1.0.0
status: stable
updated: 2026-04-17
type: skill
category: gsd-meta
origin: tibsfox
modified: false
first_seen: 2026-04-17
first_path: examples/skills/gsd-meta/session-observatory-live/SKILL.md
superseded_by: null
---

# Session Observatory — Live Event Logging

Most session retrospectives are written from memory at the end. Memory is
lossy. This skill captures the habit of logging events as they happen, so the
retrospective has real data to work with.

## When to Activate

- **At session start** — log `start <mission-name>` as one of the first
  Bash tool calls, so the started_commit is recorded.
- **When friction hits** — hook fired repeatedly, tool failed, command took
  longer than expected, user corrected you.
- **When something works unusually well** — a technique that you'd recommend
  to future sessions.
- **Before and after irreversible actions** — commits, pushes, destructive ops.
- **On progress markers** — every ~10% through a long job.
- **At session close** — log `end`, then run `generate.mjs` to produce the
  SESSION-RETRO.md.

## Commands

```bash
# Start
node tools/session-retro/observe.mjs start "<mission-name>"

# Log an event
node tools/session-retro/observe.mjs event <kind> "<label>" '<json-payload>'

# Check in on the log
node tools/session-retro/observe.mjs status

# End (archives current.jsonl to a dated file)
node tools/session-retro/observe.mjs end
```

## Event Kinds (standard)

| Kind | When | Example label |
|------|------|---------------|
| `friction` | Something took more effort than it should have | `"read-before-edit hook fired N times"` |
| `win` | Something worked notably well | `"idempotent pipeline saved 3 re-runs"` |
| `correction` | User or hook corrected direction | `"user reminded: no Co-Authored-By"` |
| `tool-use` | Notable tool invocation | `"installed better-sqlite3 as optional dep"` |
| `decision` | Judgment call deserving review | `"committed 1,881 generated files"` |
| `gap` | Missing skill/agent/chipset | `"no batch-rewriter for N-script cascade"` |
| `checkpoint` | Progress marker for long-running work | `"Pass 2 chapters: 300/602"` |

Free-form kinds are allowed but less useful for aggregation. Prefer the
standard list.

## Payload Conventions

Payloads are free-form JSON. Common fields:

- `count` — numeric count of the occurrence
- `file` / `files` — paths involved
- `duration_min` — wall-clock time
- `cost` / `tokens` — resource spend
- `impact` — `"workflow"` | `"output"` | `"blocked"` | `"none"`
- `opportunity` — what skill/agent would have helped

## Retroactive Logging

If you didn't log live, you can backfill at session close by reviewing what
happened and calling `observe event` for each remembered moment. Better than
nothing. The timestamp will be session-end rather than event-time, but the
kinds and labels are still useful.

## Integration with Retrospective Generator

Events from `current.jsonl` are consumed by
`tools/session-retro/generate.mjs` and rendered in the SESSION-RETRO.md under
**Observations**, grouped by kind. The human-authored sections
(`What Worked`, `What Could Be Better`) then reference specific events as
evidence.

## Example — This Skill's First Use

The release-history feature session logged 33 events retroactively:
- 6 friction (read-before-edit fires, 11-script cascade, no checkpoint for
  LLM run, ghost-seeding cascade, over-eager regex, hidden drift)
- 4 wins (background Monitor, idempotent pipeline, recursive self-improvement,
  fresh-repo demo)
- 3 corrections (no Co-Authored-By, dev not main, link chapter files)
- 4 decisions (publish full tree, SQLite default, allowlist gates, Commits column)
- 4 gaps (batch-rewriter, portable-schema, decision-framework, session-token)
- 3 tool-uses (better-sqlite3, claude -p, git tags)
- 9 checkpoints (pass-by-pass progress)

Those 33 events became the concrete evidence for the retro's
"What Worked" / "What Could Be Better" / "Recommendations" sections.

## Anti-patterns

- **Logging every command.** Too noisy. Log inflection points.
- **Vague labels.** "Problem happened" is useless. "Retro extractor missed
  H3 headings — 57 files hid as a result" is useful.
- **Skipping at session close.** The log isn't useful if `end` never runs
  and the JSONL never archives. Generate the retro before context dies.

## Related

- `tools/session-retro/observe.mjs` — the logger itself
- `tools/session-retro/generate.mjs` — the retrospective generator
- `decision-framework-invoker` — often co-fires with `decision` events
