---
name: kai-retro
description: Run a learning retrospective on the Kai harness. Mines gate-failure logs and 30-day performance results into lessons, triages candidate lessons (promote/keep/retire), and graduates repeated lessons into enforced gate checks with golden corpus cases. Use when "retro", "what have we learned", "triage lessons", "promote lessons", "why does this keep failing", "harness retrospective", or monthly / after any heavy content sprint.
---

Run the Kai learning retrospective. This is how the harness gets smarter: raw failure logs become lessons, repeated lessons become enforced checks. Read `memory/MEMORY.md` first for the graduation ladder.

## When to run

- Monthly, or after any sprint that produced 5+ gated pieces
- Whenever the same gate failure shows up twice in one session
- When a 30-day performance check grades new losers

## Step 1 — Mine the gate logs

```bash
python scripts/self_improvement/lesson_capture.py mine
```

This groups recurring failure signatures from `data/learning/gate_runs.jsonl`. Append candidates with `--write`. If the log is empty, note it and move on — the gates only log when they run.

## Step 2 — Diagnose losers

```bash
python scripts/self_improvement/lesson_capture.py losers
```

For each undiagnosed loser, read the piece and its `content_log.json` entry, write a one-line diagnosis (hook type, persona mismatch, seasonality, thin proof — name the cause, not the symptom), and add it to `memory/what-doesnt-work.md` under "Measured losers" with the piece id. Check seasonality and competitor moves before blaming the content (see `memory/edge-cases.md` EC-15).

## Step 3 — Triage every lesson

Go through `memory/lessons.md`:

| Verdict | Criteria | Action |
|---------|----------|--------|
| **Promote** | Fired 3+ times, or checkable by a regex/threshold | Graduate it (Step 4), mark `(promoted)` |
| **Keep** | True, useful, not yet recurring | Upgrade `candidate` → `active` if verified |
| **Merge** | Near-duplicate of another lesson | Combine into the more general one |
| **Retire** | No longer true (platform changed, gate fixed) | Mark `(retired)` with the reason — never delete |

## Step 4 — Graduate promoted lessons

Pick the strongest enforcement target, in this order:

1. **Lint rule / contract check** — new entry in a banned-word tier, a new overclaim regex in `scripts/quality_gates/seo_lint.py`, or a `deterministic_checks` line in the format's skill contract.
2. **Checklist line** — the relevant `knowledge/checklists/*.md`.
3. **CLAUDE.md / framework rule** — only for judgment calls code can't check.

**Non-negotiable:** any change to a gate script requires a matching case in `evals/golden/manifest.json` (one sample proving the new check fires, and confirm the existing pass samples still pass), then:

```bash
python scripts/quality_gates/golden_check.py
```

A gate change without a golden case is not a promotion — it's a regression waiting to happen.

## Step 5 — Refresh the memory index

- Update the "Current standing lessons" section of `memory/MEMORY.md` (keep the file under 200 lines).
- Cross-check `memory/edge-cases.md`: mark any entry whose `Enforcement: none` you just fixed; add new edge cases discovered this cycle.

## Step 6 — Report

Output a retro summary:

```
## Kai Retro — [date]

**Mined:** [N] recurring failure signatures ([gate]: [signature] ×[count], ...)
**Losers diagnosed:** [N] ([id]: [one-line diagnosis], ...)
**Promoted:** [lesson] → [enforcement target] (+ golden case [id])
**Retired:** [lesson] — [reason]
**Edge cases:** [new/closed entries]
**Open risks:** [lessons at 2 occurrences — one more and they must promote]
```

Commit the memory and gate changes together so the diff shows the lesson and its enforcement side by side. If a promotion changes publishing behavior (new hard block), flag it for human approval rather than applying silently.
