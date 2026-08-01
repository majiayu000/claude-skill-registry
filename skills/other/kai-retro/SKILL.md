---
name: kai-retro
description: Run a learning retrospective on the Kai harness. Mines gate-failure logs and 30-day performance results into lessons, triages candidate lessons (promote/keep/retire), and graduates repeated lessons into enforced gate checks with golden corpus cases. Use when "retro", "what have we learned", "triage lessons", "promote lessons", "why does this keep failing", "harness retrospective", or monthly / after any heavy content sprint.
---

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

## Objective

The harness ends this cycle enforcing something it was only remembering at the start. Gate-failure logs and 30-day grades become diagnosed lessons; lessons that keep firing become lint rules, contract checks, or checklist lines with golden corpus cases behind them, and the memory index reflects what changed. Run it monthly, after any sprint that produced 5+ gated pieces, whenever the same gate failure appears twice in one session, or when a 30-day check grades new underperformers. Read `memory/MEMORY.md` first — the graduation ladder is the shape of the whole cycle.

## Done when

Work type `harness-change` — floor **E3/C3/O1** (`harness/eco-floors.yaml`).

- **E3** — `golden_check.py` passes on the changed tree and a named human approved the diff. Memory and gate changes commit together so the lesson and its enforcement read side by side.
- **C3** — every promotion into a gate script has a matching case in `evals/golden/manifest.json` (one sample proving the new check fires, plus confirmation existing pass samples still pass), reviewed by a non-author. A gate change without a golden case is not a promotion; it is a regression waiting to happen.
- **O1** — metric `lesson_recurrence_stopped`, read from `data/learning/gate_runs.jsonl` at 30 days: the promoted lesson's failure signature stops appearing.

The summary names: signatures mined with counts, underperformers diagnosed with their one-line causes, what was promoted and to which target with its golden case id, what was retired and why, edge cases opened or closed, and lessons sitting at two occurrences — one recurrence from mandatory promotion.

## Constraints

- **Diagnose the cause, not the symptom.** Name hook type, persona mismatch, seasonality, or thin proof — not "low traffic." Check seasonality and competitor moves before blaming the content (`memory/edge-cases.md` EC-15). Diagnoses are written against the piece and its `content_log.json` entry and land in `memory/what-doesnt-work.md` under "Measured losers" with the piece id.
- **Never delete a lesson.** Retired lessons are marked `(retired)` with the reason; git keeps history.
- **Any change to a gate script requires a golden case**, then a passing `golden_check.py` run. **A promotion that changes publishing behavior — any new hard block — is flagged for human approval, never applied silently.**
- **`memory/MEMORY.md` stays under 200 lines**; refresh its "Current standing lessons" section, and cross-check `memory/edge-cases.md` — mark entries whose `Enforcement: none` was just fixed, add ones found this cycle. An empty gate log is a finding, not a failure: note it and continue, since the gates only log when they run.

## Context

| Need | Load |
|---|---|
| Graduation ladder, standing lessons, lessons awaiting triage | `memory/MEMORY.md` + `memory/lessons.md` |
| Gotchas and their enforcement status; measured losers | `memory/edge-cases.md` + `memory/what-doesnt-work.md` |
| Golden corpus cases | `evals/golden/manifest.json` |
| Promotion targets, strongest first | `scripts/quality_gates/seo_lint.py` (overclaim regex, banned-word tier) → `harness/skill-contracts/` (`deterministic_checks`) → `knowledge/checklists/` → `CLAUDE.md`, for judgment calls code cannot check |

```bash
python scripts/self_improvement/lesson_capture.py mine     # recurring failure signatures from data/learning/gate_runs.jsonl; --write appends candidates
python scripts/self_improvement/lesson_capture.py losers   # 30-day underperformers with no diagnosis yet; grades are winner/average/underperformer (older docs said "loser")
python scripts/quality_gates/golden_check.py               # required after any gate-script change
```

| Verdict | Criteria | Action |
|---|---|---|
| Promote | Fired 3+ times, or checkable by a regex or threshold | Graduate it, mark `(promoted)` |
| Keep | True, useful, not yet recurring | Upgrade `candidate` → `active` if verified |
| Merge | Near-duplicate of another lesson | Combine into the more general one |
| Retire | No longer true (platform changed, gate fixed) | Mark `(retired)` with the reason — never delete |

## Escalate when

- A promotion would introduce a new hard block on publishing.
- A lesson has fired 3+ times but no regex, threshold, checklist line, or contract check can express it, or a golden case cannot be constructed for a proposed gate change.
- An underperformer's cause traces to a business or product decision rather than to the content.
