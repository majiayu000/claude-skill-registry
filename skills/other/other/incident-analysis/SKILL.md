---
name: incident-analysis
description: Use when analysing production logs, investigating incidents, writing postmortems, or reviewing error patterns from structured logs (JSONL, journal, HAProxy, PostgreSQL). Enforces source provenance, timezone discipline, hypothesis falsification, and evidence-graded findings. Prevents scope leakage, confidence flattening, and unreproducible counts.
---

# Incident Analysis

Analyse production incidents with falsificationist discipline. Every finding is a hypothesis. Every hypothesis has evidence with provenance. Every count has a reproducible command.

This skill exists because a 2026-03-16 afternoon analysis produced 10 errors caught by two peer reviewers — all caused by operating on data without verifying it matched the analytical assumptions. The errors are catalogued in `CREATION-LOG.md` in this directory.

## When to Use

- Analysing production log files (JSONL, systemd journal, HAProxy access logs, PostgreSQL logs)
- Writing or reviewing postmortem documents
- Investigating error patterns across multiple log sources
- Any task where counts, timelines, or causal claims are derived from log data

## Phase 1: Source Inventory

**Before any analysis, inventory every data source.** This is the single cheapest check that catches the most errors. (Lesson: the 2026-03-16 analysis operated on a 28-hour JSONL file believing it covered 2.5 hours.)

For each log file, record:

| Field | How to get it |
|-------|--------------|
| File path | The file you're analysing |
| Line count | `wc -l` |
| First timestamp | `head -1` or `jq -r '.timestamp' \| head -1` |
| Last timestamp | `tail -1` or `jq -r '.timestamp' \| tail -1` |
| Timestamp timezone | Read the format — PG logs say `UTC`, journal uses local, HAProxy uses local, JSONL uses UTC |
| File size | `ls -la` |

**Publish this table in the report before any findings.** It is the provenance manifest.

### Timezone Reference

Each source has its own timezone convention. State these explicitly per-source, never assume.

| Source | Typical timezone | How to verify |
|--------|-----------------|---------------|
| structlog JSONL | UTC (ISO 8601 with Z or +00:00) | Check first entry's timestamp suffix |
| systemd journal | Server local time | Check system timezone: `timedatectl` |
| PostgreSQL log | Configured in `postgresql.conf` (`log_timezone`), often UTC | Check timestamp suffix in log entries |
| HAProxy log | Server local time (syslog format) | Compare a known event across sources |

**Convert all timestamps to one reference timezone for cross-source comparison.** State which timezone you chose and why. Use a named timezone (e.g., `Australia/Sydney`, `America/New_York`) and derive the UTC offset from the date — never hardcode an offset like "AEDT" or "+11" because daylight saving boundaries shift. (Lesson: the 2026-03-16 analysis missed 13 PG errors because the analyst forgot that PG timestamps were UTC and grepped for local-time date prefixes.)

### Positive Control

After setting up your time filter, run a **positive control**: pick one event you know exists in the window (e.g., a restart, a known error). Run your filter. Confirm it appears. If a "no results" finding emerges from any filtered query, re-run the positive control to verify the filter is working before reporting zero. (Lesson: `grep "2026-03-16 15:" pglog` returned zero because PG logs were UTC, not local time. A positive control against the known 15:02 restart would have immediately revealed the timezone mismatch.)

## Phase 2: Enumerate Before Hypothesising

**Scan the full category space before searching for specific values.** Let the data define the categories, not your hypothesis. (Lesson: searching for `503` and `504` missed 500, 501, 502, 505, 506, 508 — yielding a 5xx total of 82 instead of 106.)

```bash
# Correct: enumerate all status codes first
grep -oE ' [0-9]{3} ' haproxy.log | sort | uniq -c | sort -rn

# Then drill into specific codes
grep ' 504 ' haproxy.log | ...
```

```bash
# Correct: enumerate all error events first
jq -r 'select(.level == "error") | .event' file.jsonl | sort | uniq -c | sort -rn

# Then drill into specific events
jq -r 'select(.event == "Database session error")' file.jsonl | ...
```

**Apply time filtering as the first transformation, before any grouping or aggregation.** Treat unfiltered data as untrusted. (Lesson: JSONL INVALIDATE events with `pool_size=5` from the morning contaminated the afternoon analysis because the JSONL was aggregated before filtering.)

## Phase 3: Findings as Hypotheses

Every finding follows this template. The template exists because the 2026-03-16 analysis mixed confirmed facts, inferred causes, and out-of-window corroboration in the same narrative without marking which was which (Codex critique: "scope leakage... a summary layer flattens them into one narrative").

### Well-Formed Finding Template

```markdown
## Finding N: [Specific, falsifiable claim]

**Hypothesis:** [What you believe happened, stated as testable]

**Evidence:**
- Source: [file path, timezone, filtered window]
- Command: [exact command that produced the number]
- Result: [what the command returned]

**Falsification attempts:**
- [What evidence would disprove this hypothesis]
- [Did you look for that evidence? What did you find?]

**Confidence:** [See calibration below]

**Scope:** [in-window-confirmed | out-of-window-corroboration | inference]
```

### Confidence Calibration

Confidence is earned by surviving falsification, not by feeling sure. (Framework: Popper — a hypothesis gains credibility by failing to be falsified, not by accumulating confirming instances.)

| Level | Criteria | Example |
|-------|----------|---------|
| **Confirmed** | Direct measurement from the correct time window, correct source, verified filter. The positive control passed. | "54 x 503 at 15:02" — HAProxy log, correct timezone, status code directly in log line |
| **Corroborated** | Multiple independent sources agree, but at least one link is indirect or from a different time window | "PG FATAL at 15:50 correlates with INVALIDATE spike" — two sources, same timeframe, but causal link inferred |
| **Inferred** | Plausible mechanism or temporal correlation, but not directly measured. State what additional evidence would promote this to Corroborated | "CancelledError churn caused by students navigating away" — CancelledError confirmed, student behaviour inferred from semantics |
| **Unverified** | Number reported without recording the command, or from an unfiltered/wrong-window source | Any count from an unfiltered JSONL file. Any "zero results" finding without a positive control |

**A finding derived from an unfiltered source is Unverified until re-run with correct filtering.** This is non-negotiable. (Lesson: "91 DB rollback errors" was reported as a finding; the afternoon-only count was 19.)

### Report Structure Separation

Separate findings into three sections. Mixing these is how scope leakage happens. (Codex: "mixes unfiltered JSONL duplicate counts, prior-day student-id errors, and post-window share-button evidence at the same confidence level.")

1. **In-window confirmed facts** — evidence from within the defined analysis window, from filtered sources, with provenance
2. **Out-of-window corroboration** — evidence from outside the window that supports or contextualises in-window findings. Clearly marked as such
3. **Inference and interpretation** — causal claims, mechanism hypotheses, recommendations. Clearly marked as interpretation, not fact

## Phase 4: Cross-Source Reconciliation

For each significant event (restarts, error spikes, stalls), trace it across all available sources. A finding is stronger when multiple independent sources confirm it. A finding that appears in only one source should note that limitation.

**Reference-point cross-check:** For each finding, compare timestamps against known reference events (restarts, deploys, config changes). If a timestamp resolves a question (e.g., "is this pre- or post-deploy?"), use it — don't hedge. (Lesson: 8 of 10 PG tag errors were at 16:11 AEDT, definitively after the 15:02 restart, but the analysis hedged about pre-restart origin because the analyst didn't check timestamps against the known restart time.)

## Phase 5: Causal Chain, Not Root Cause

Frame failure as a chain of contributing factors, each necessary but only jointly sufficient. (Allspaw/Cook: "Finding the root cause of a failure is like finding a root cause of a success.") Use contributing-factor framing, not Five Whys. (Salesforce Engineering: replace "why" with "how" to avoid the single-chain trap.)

For each link in the chain, mark whether it is:
- **Confirmed link:** Evidence directly demonstrates this step caused the next
- **Inferred link:** Temporal correlation or plausible mechanism, but not directly demonstrated
- **What would strengthen this link:** Specific evidence that would promote an inferred link to confirmed

## Phase 6: Provenance Discipline

**Record the exact command next to every number.** If you cannot paste the command that produced a figure, mark the figure as Unverified. (Lesson: "1,967 errors" was reported but could not be reproduced from any query — it was a derived figure with no provenance chain.)

**Tag each datum with its source inline.** Use a consistent notation:
- `[JSONL, afternoon-filtered, UTC]`
- `[journal, full file, local time]`
- `[PG log, full file, UTC]`
- `[HAProxy, full file, local time]`
- `[Beszel, visual estimate]`

This makes confidence flattening visible on re-read. If a paragraph mixes `[JSONL, afternoon-filtered]` and `[JSONL, unfiltered]` tags, the scope leakage is immediately apparent.

## Phase 7: Self-Challenge Before Presenting

Before presenting findings, run your own adversarial review. (Etsy Debriefing Facilitation Guide: the facilitator role catches counterfactuals, premature convergence, and hindsight bias.)

For each finding, check:

1. **Does the evidence actually come from the claimed time window?** Re-verify the filter.
2. **Is the confidence level earned?** Check against the calibration table.
3. **Are there alternative explanations I haven't considered?**
4. **Am I describing what happened, or what should have happened?** Counterfactual claims ("they should have...") are unfalsifiable. Stick to observables. (Etsy: "a reality that didn't actually happen... the group is trying to fix things that are not the actual problem.")
5. **Would a reviewer with the raw logs reach the same conclusion?** If your finding requires trusting your narrative rather than checking the data, it is not well-formed.

## Quick Reference: Verification Order

Cheapest checks first. Steps 1–3 take under 5 minutes and would have caught 5 of the 10 errors in the 2026-03-16 analysis.

| Step | Action | Catches |
|------|--------|---------|
| 1 | **Source inventory** — first/last timestamp, timezone, line count per file | Window contamination, timezone mismatch |
| 2 | **Positive control** — pick a known event, confirm your filter finds it | False negatives from wrong filters |
| 3 | **Enumerate before drilling** — scan full category space first | Incomplete enumeration |
| 4 | **Provenance annotation** — paste the command next to every number | Unreproducible figures |
| 5 | **Source tagging in prose** — `[source, filter, timezone]` per datum | Confidence flattening, scope leakage |
| 6 | **Reference-point cross-check** — compare timestamps against known events | Confidence understatement, deploy boundary errors |
| 7 | **Self-challenge** — adversarial review of own findings | Counterfactuals, alternative explanations |

## Subagent Decomposition

When dispatching incident analysis to subagents, split by phase rather than giving one agent all 7 phases. A single agent runs out of turns doing thorough source verification AND finding construction AND self-challenge. (Lesson: a test agent used 59 turns on Phases 1–2 and never produced the final finding.)

**Recommended split:**

| Agent | Phases | Input | Output |
|-------|--------|-------|--------|
| **Inventory agent** | 1–2 (Source inventory, enumeration) | Log file paths, analysis window (local time + timezone), known reference events | Provenance manifest table, category breakdowns with commands, positive control results |
| **Finding agent** | 3–6 (Hypotheses, cross-source, causal chain, provenance) | Provenance manifest from agent 1, specific event to trace | Well-formed findings with evidence, causal chain, confidence levels |
| **Challenge agent** | 7 (Self-challenge) | Findings from agent 2, raw log file paths for spot-checking | Adversarial review: weaknesses, alternative explanations, unearned confidence |

Each agent gets the full turn budget for a smaller scope. The provenance manifest from agent 1 becomes the contract that agent 2 must honour — it cannot introduce numbers from unfiltered sources because the manifest documents the correct windows.

The challenge agent (Phase 7) should be a different model or at minimum a fresh agent with no shared context, to avoid confirmation bias from having constructed the finding.

## Applying to a Project

Create a project-specific incident analysis playbook that maps the methodology to your log sources. The playbook should document:
- Where each log source lives and how to collect it
- The timezone convention for each source (verify, don't assume)
- Common grep/jq patterns for your application's error types
- Known reference events (deploy process, restart mechanism)
- Triage order for your incident response

The methodology in this skill is source-agnostic. The playbook makes it concrete.
