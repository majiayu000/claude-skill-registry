---
name: session-audit
description: Audit Claude Code session logs (~/.claude/projects) for token waste and produce a ranked, attributed efficiency report (habit / skill_file / config). Use when the user asks to audit session efficiency, analyze token waste or cost blowups, review Claude Code usage cost, or asks "where are my tokens going".
model: inherit
---

# Session Efficiency Audit

You are the reasoning layer (L2/L3) of a layered audit engine. Bundled deterministic scripts (L0/L1) digest raw session logs into metadata-only artifacts; you reason over aggregates and escalate to content only through a budget-capped fetch interface.

`{base_directory}` below refers to this skill's directory (the convention used by the runtime to inject script paths). Set the workdir once and use it everywhere:

```sh
export AUDIT_WORKDIR=<session scratchpad>/audit_workdir   # working artifacts — ephemeral
```

**Two lifetimes.** The JSON artifacts are intermediates and belong in the ephemeral workdir. The **report is the deliverable and must outlive the session** — it goes to a dated file in a stable, project-independent archive:

```sh
mkdir -p ~/.claude/audit-reports
# final report -> ~/.claude/audit-reports/<YYYY-MM-DD>.md
```

Keeping past reports is also the only way to answer "am I improving?": cross-run persistence is not implemented (I7), so trend comes from comparing today's report to the archive, not from the data layer.

## Invariants (non-negotiable)

_The list below is canonical. Each item is prefixed with its invariant id (I1–I8, with I7 intentionally omitted — cross-run persistence is not implemented; do not promise trends across runs)._

1. **(I1)** **Never read a raw session JSONL directly** (no Read/cat/grep on `~/.claude/projects/**/*.jsonl`). All access goes through `run` and `fetch`.
2. **(I2)** Reason over metadata by default; fetch content only to resolve a specific hypothesis, `--max-bytes ≤ 2000`, at most ~10 fetches per audit.
3. **(I3)** Waste math never trusts raw `input_tokens`/`output_tokens` sums (streaming placeholders / thinking excluded). Anchor on `cache_read_input_tokens`, `cache_creation_input_tokens`, and content bytes.
4. **(I4)** All aggregation is deduped by `requestId` (the scripts do this — do not hand-roll parsing).
5. **(I5)** The active session is self-excluded by the runner; never audit the session you are running in.
6. **(I6)** Report the audit's own self-cost from `fetch_log.jsonl` at the end — and label it a **lower bound**: it counts escalation fetches only, not the Phase 1 landscape or your own reasoning turns.
7. **(I8)** **Write only to `$AUDIT_WORKDIR` and the report.** Never edit this skill's own files (`SKILL.md`, `bin/`, `src/`, `data/`) or the user's repo. You are an installed bundle: a relative path like `src/views.js` points at *your own running code*, not at the project that built you. An audit that patches its own renderer measures itself with something that changed mid-run, and the next install destroys the change without a word.

## Phase 0 — Digest (L0 + L1, zero LLM)

```sh
node {base_directory}/bin/audit.js run            # full directory
node {base_directory}/bin/audit.js run --max 50   # quick pass, newest 50 sessions
```

Writes to `$AUDIT_WORKDIR`: `manifest.json` (thresholds + `pricing`: priced models, unpriced models seen, and the share of waste that carries a price), `l1_findings.json` (rule findings: `{rule, severity, sessionId, turnPointers, evidenceStats, estWasteTokens, project}`), `overview.json` (aggregates: `projects`, `tools`, `models`, `gapBuckets`, `dates`, `skills`, `sessions` sorted by waste). Per-session and per-project rollups carry `wasteUsd` alongside `wasteTokens`, plus `models`, `usdPerMTok`, and `pricedShare`.

Rules emitted: `CACHE_TTL_EXPIRY`, `DUP_TOOL_CALL`, `BIG_TOOL_OUTPUT`, `RETRY_STORM`, `CACHE_MISS_RATE`, `CONTEXT_GROWTH`, `NO_SUBAGENT`.

## Phase 1 — Read the aggregate landscape

```sh
node {base_directory}/bin/audit.js views
```

One bounded block: totals (tokens **and** dollars), findings-by-rule with a sessions-affected count, cache hit-ratio distribution, projects and worst sessions by waste (full session ids, with the `fetch` command to inspect one), idle-gap cost curve, tools by bytes, peak-context and delegation, per-date trend, skill usage.

Do **not** read `overview.json` / `l1_findings.json` wholesale (>100KB), and do not hand-roll node one-liners for anything `views` already prints — every query and its output lands in your transcript, which is the audit's real self-cost.

**If a stat you need is missing, say so in the report — do not add it to `views.js`.** You are running from an installed bundle, so `src/views.js` is *your own code*, and editing it mid-audit means the run measures itself with a renderer that changed partway through; the next install silently wipes the change anyway (I8). Record the gap under a "stats this report wanted and could not get" note, and a human ports it to the repo. Where a missing stat blocks a specific claim, a single narrow query is acceptable — but state in the report that you ran it, because the transcript cost is real and unlogged.

Two traps the view exists to prevent:

- **Finding counts are not population counts.** Every rule has entry gates — `CACHE_MISS_RATE` needs ratio < 0.5 *and* ≥5 turns — so "1 finding" never means "1 session with that property". Read the distribution block, never the rule count.
- **Raw vs. cost-equivalent tokens.** `gapBuckets.cacheCreation` is raw; rule waste is cost-equivalent (`creation × 1.15`, `rules.js:118`). The view prints the gap curve in both units. Compare like with like before claiming two methods corroborate.

## Phase 2 — L2 hypothesis loop

1. From the landscape, form candidate patterns. Recurring high-value ones: TTL expiry after idle gaps (check `gapBuckets` — cost per resume vs the `lt_1m` baseline), large-file re-read loops (DUP + BIG on `Read` in the same sessions), marathon sessions near the context ceiling, image-heavy low-cache sessions, snapshot-happy browser loops, scan-heavy sessions with `hasSubagents: false`.
2. Confirm or dismiss with narrower queries over per-session `findingsByRule` and per-session finding details.
3. Where metadata cannot resolve intent, escalate with fetch:

```sh
node {base_directory}/bin/audit.js fetch <session-id> --kind <kind> [--limit N] [--max-bytes B] [--uuid U] [--radius K]
```

| kind | returns | use to judge |
|---|---|---|
| `user_text` | user messages | intent vs agent behavior |
| `error_head` | head of errored results | transient vs deterministic failure |
| `tool_input` | tool call params | which file/command was duplicated |
| `assistant_head` | head of assistant text | verbosity / narration |
| `turn_window` | metadata around `--uuid` | sequence reconstruction |

4. Write `$AUDIT_WORKDIR/l2_hypotheses.json`:

```json
[{ "pattern": "NAME", "evidence": ["stat or fetch ref", "..."], "confidence": "high|medium|low",
   "escalation_fetches": ["..."], "resolution": "resolved|escalate", "interpretation": "one sentence" }]
```

## Phase 3 — L3 attribution

Reason over the hypotheses plus fetched snippets only. Write `$AUDIT_WORKDIR/attribution.json`, ranked by waste:

```json
[{ "rank": 1, "finding": "...", "attribution": "habit|skill_file|config",
   "estWasteShare": "~N% (xK of yK)", "trend": "improving|worsening|steady",
   "fix": "concrete behavior change, named skill edit, or config change" }]
```

Attribution guide: **habit** = working style (resuming big sessions after breaks, no /clear at pivots, inline scanning, whole-file re-reads); **skill_file** = a named skill drives the pattern (say which file and what to change); **config** = MCP bloat, model default, thinking budget, CLAUDE.md size.

## Phase 4 — Report

Write **`~/.claude/audit-reports/<YYYY-MM-DDTHHMMSSZ>.md`** (create the directory if absent). Generate the timestamp with `date -u +%Y-%m-%dT%H%M%SZ` (UTC, second-precision). No sequence suffix: the timestamp disambiguates, and a same-second collision would mean two simultaneous audits — outside this skill's pacing.

The report is read by a developer deciding **whether to spend an afternoon on this, and on what**. A finding they cannot price, verify, or check off later is a finding they will not act on. Every requirement below exists to close one of those three gaps.

**Header.** `projectsDir`, session count, and date window, so a later comparison knows its scope. Nothing else — keep tool-internal notes (artifact disagreements, re-renders, workdir paths) out of the deliverable; they read as "this tool contradicts itself" directly above the numbers. Put them in the workdir if you need them.

**Required content:**

1. **Totals in dollars *and* tokens.** `views` prints both. The dollar figure is what makes the report decidable; a token count alone is a unit nobody budgets in. Carry through both disclosures `views` prints — the unpriced-model share, and that thinking tokens and compaction are unmeasured — and label the totals a heuristic floor.
2. **Findings-by-rule table** with the **sessions-affected** column. 200 findings across 4 sessions is one bad week; across 60 it is a habit. The finding count alone cannot distinguish them, and the fix differs.
3. **Per-project breakdown** (`views` → Projects by waste). A dev acts on one repo at a time; the directory total tells them nothing about where to start. Note where the dollar and token rankings disagree — that means a pricier model, and it changes the priority.
4. **Ranked fixes**, each carrying all five of:
   - **Evidence** — real file names, real behaviors, the user's own quoted words where fetched.
   - **Full session ids**, never truncated, plus the command to check one:
     `node {base_directory}/bin/audit.js fetch <session-id> --kind user_text --limit 3 --max-bytes 500`
     An 8-char prefix cannot be resumed or fetched, so it makes the claim unverifiable.
   - **Cost** — dollars and tokens, with the share of headline.
   - **Attribution** — habit / skill_file / config.
   - **A target metric** — the exact row and number that should move by the next audit ("`CACHE_TTL_EXPIRY` 4,202K / $21 → under 1,500K"). Without one, "step away less" is unfalsifiable and next month's report has nothing to compare.
5. **A "do this first" pick, chosen on effort × permanence — not on waste rank.** A `skill_file` or `config` fix is one edit that keeps paying; a `habit` fix is indefinite discipline with no enforcement. When the top-ranked item is a habit and a smaller one is a one-line skill edit, say plainly that the skill edit goes first and why. For any `skill_file` fix, name the file and the text to change — "instruct it to read less" is not executable.
6. **Trend.** Before writing, `ls ~/.claude/audit-reports/`. If prior reports exist, read the most recent totals table and state the direction — which rules grew, which shrank, whether a previously recommended fix stuck. If the archive is empty say "first audit — no baseline yet"; do not infer a trend from within-run date buckets alone.
7. **Audit self-cost** — fetch count + bytes from `fetch_log.jsonl`, labelled a lower bound (I6).
8. **ASCII charts** — four visualizations placed **inline with the table each summarizes** in the report (findings-by-rule table → rule chart immediately after, per-project breakdown → project chart, per-date trend → date chart, cache hit-ratio section → distribution histogram). Each chart is authored in **two versions**:
   - **Wide** (~100 cols) in the report file: full labels and session counts.
   - **Compact** (~40 cols) in the chat summary: shortened labels, no session counts.
   Chart data is plotted **only from values already pulled from `views` output** (I8) — never re-derived or hand-rolled. If a stat is missing, skip that chart and note it under "stats this report wanted and could not get".

   The chat summary carries **all four compact charts** (rule, project, date, cache-hit), placed right after the headline paragraph and before the trend story, so the visual precedes the prose explanation.

### Chart format

```text
Wide version (~100 cols, label ≤ 25 chars, bar 50 chars, numbers ~20 chars):

NO_SUBAGENT       ████████████████████████████████████████████  243 sess / $73.04
CACHE_TTL_EXPIRY  ██████████████████████                        119 sess / $35.26
BIG_TOOL_OUTPUT   ████                                         62 sess /  $7.58
DUP_TOOL_CALL     ████████                                     98 sess / $14.01

Compact version (~40 cols, label ≤ 15 chars, bar 20 chars, numbers ~8 chars):

NO_SUBAGENT    ████████████████████  $73
CACHE_TTL      ██████████           $35
DUP_TOOL_CALL  ████                 $14
BIG_TOOL       ██                    $8
```

- Wrap each chart in a fenced code block so monospace alignment survives rendering.
- **Bar character**: `█` (U+2588). Round bars to whole units — no fractional blocks.
- **Layout**: right-padded label · bar · numbers. Fixed label width so bars line up.
- **Scale**: auto-scale to the maximum value so the largest bar fills the bar column.
- **Sort**: rows ordered by value descending — the worst item leads.

Then summarize the top 3 changes in chat, in the user's own context, and say where the report was saved.

## Interpretation notes

- `CONTEXT_GROWTH` carries zero direct waste — treat it as an amplifier of everything else in that session.
- `CACHE_TTL_EXPIRY` findings carry `evidenceStats.gapKind`. Only `user_idle` gaps are priced as waste; `tool_runtime` gaps are reported at **zero waste by design** — the wait was a long-running command, not a habit, and attributing it to behaviour produces a fix the user cannot act on. Check `gapKind` before calling any TTL finding a habit.
- `NO_SUBAGENT` is **excluded from headline waste** and reported in its own section. It prices a different counterfactual (delegate the phase) than the rules it overlaps (read less, read once), so summing it into the total double-counts bytes. Never add it to the headline figure.
- Rank by **prefix persistence**: early, long-riding costs beat late one-offs of the same size.
- **Dollars are priced per session, from its own model mix** — so the token ranking and the dollar ranking can legitimately disagree (a project on a pricier model costs more per wasted token). Where they do, the dollar order is the one to act on, and worth calling out. Unpriced models contribute tokens but no dollars; `manifest.pricing.pricedWasteShare` says how much of the total is covered.
- Peak context can exceed 200K on 1M-context models; don't call it a bug.
- A healthy directory (hit ratio >0.95, near-linear growth) deserves a short report saying so — do not manufacture findings.
