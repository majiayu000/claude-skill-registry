---
name: metrics-pull
description: "Pull snapshots from all configured metric sources, compute deltas against prior snapshots, flag unexplained signals, and draft evidence entries for canvas files. One entry point for all external product/market metrics."
instruction_budget: 47
---

# Metrics Pull Skill

Unified pull across all metric sources configured in `.claude/jit-tooling/active-metrics.yml`. Dispatches to per-source adapters (starting with `github`), normalizes to a shared schema, computes deltas, and drafts canvas evidence entries.

This skill is the L0/L1/L2/L5 evidence-gathering loop. Replaces manual "I checked the dashboard" reports with timestamped, sourced, diffable data.

## When to Use

- Before `/diamond-assess` at L0/L1/L2/L5, if the newest snapshot is >7 days old.
- After any public activity (launch, post, conference mention) — typically 24-48h later to capture the bump.
- Weekly baseline, regardless of activity.
- Ad hoc when the user wants a fresh read.

## Precondition: active-metrics.yml exists

If `.claude/jit-tooling/active-metrics.yml` does NOT exist:

1. Tell the user: "No metric sources are configured. Running `/metrics-detect` first."
2. Invoke `/metrics-detect` (or follow `.claude/jit-tooling/metrics-detector.md`).
3. After detection completes, return to this skill.

## Workflow

### Step 1: Load configuration

Read `active-metrics.yml`. Filter to sources with `status: active`. For each, verify the adapter file exists at `metrics-adapters/<source>.md`. If missing, follow `metrics-adapters/GENERATING.md` to generate it.

If `confirmed_by_user: false`, ask the user to confirm the source list before proceeding.

### Step 2: Dispatch adapters in parallel

For each active source, follow its adapter's "Pull" and "Normalize" sections. Adapters are independent — run them in parallel (bash jobs, multiple tool calls in one message).

Per-source handling:
- Honor the adapter's `credential_requirement`. If missing, skip the source and report to user; do not fail the entire pull.
- Honor the adapter's rate-limit and retry rules.
- If the adapter returns `fetch_status: partial`, include partial data but mark the snapshot.

### Step 3: Save raw snapshots

For each source, write the normalized snapshot to:

```
.claude/evals/metrics/<source>/YYYY-MM-DD.json
```

Use today's date. If today's snapshot already exists, OVERWRITE (the skill is idempotent within a day). Create directories as needed.

### Step 4: Load prior snapshots

For each source, find the most recent snapshot in `.claude/evals/metrics/<source>/` that is NOT today's. If none exists, skip delta computation for that source and note "first snapshot" in the report.

### Step 5: Compute deltas

Apply the adapter's "Delta rules" section. Common patterns:

- **Cumulative counts** (stars, forks, total subscribers): current minus prior, plus days-elapsed.
- **Windowed metrics** (14-day views/clones): highlight the newest day not present in the prior window. Avoid raw window-to-window subtraction when windows overlap.
- **Ranked lists** (referrers, top_paths, top-reviewed items): report new entries, dropped entries, rank shifts ≥3 positions.
- **Ratios** (clone-to-star, view-to-clone, churn rate): report current vs prior, flag drift >20%.

### Step 6: Flag unexplained signals

Each adapter defines what "unexplained" means for its source. Typically this is:

- **traffic class**: referrers not in `known_referrers` with `unique >= 5`.
- **events class**: unusual spikes (>3x prior window), new event types.
- **reviews class**: sudden rating changes, new-language reviews.
- **support class**: ticket category shifts, volume spikes.

For unexplained signals, attempt the investigation hooks defined in each adapter (e.g., GitHub's HN search) before presenting to the user.

### Step 7: Generate combined report

Write a markdown report to `.claude/evals/metrics/YYYY-MM-DD.md` (project-level, not per-source) with this structure:

```
# Metrics Pull: YYYY-MM-DD
Sources pulled: N active, M skipped (credential issue)

## <source 1 name>
Target: <target>
Prior snapshot: YYYY-MM-DD (N days ago)

### Summary
[primary_counts with deltas]

### [class-specific sections]
- traffic class: Traffic (windowed), Top Referrers, Top Paths
- events class: Event counts, ratios
- reviews class: Rating summary, new reviews, [repurposed fields under their declared interpretation]
- support class: Ticket volume, top tags

### Unexplained signals
[list or "none"]

### Notable patterns
[ratio drift, Goodhart flags, cross-source correlations]

## <source 2 name>
...

## Cross-source observations
[if applicable — e.g., "GitHub traffic up + Stripe new customers up on the same day"]

## Proposed Evidence Entries
[yaml blocks from Step 8]
```

Display the report to the user.

### Step 8: Draft evidence entries

For each source, consult the adapter's "Canvas routing" section. Draft a candidate evidence entry for each applicable canvas file. Never auto-write — always present for user confirmation.

Example entry (GitHub → purpose.yml):

```yaml
- type: "market_signal"
  summary: "GitHub owner/repo on 2026-04-16: 342 stars (+12), 47 forks (+2), 943 views / 286 unique, 693 clones / 240 unique over 14 days. Top referrers: reddit.com, news.ycombinator.com, linkedin.com. Clone-to-star ratio 2.03 — healthy private evaluation. No unexplained referrers."
  date: "2026-04-16"
  source_class: external_data
  provenance:
    snapshot: ".claude/evals/metrics/github/2026-04-16.json"
    adapter_version: 1
```

Ask the user: "Append these N evidence entries to [canvas files]?" Append only after explicit yes.

### Step 9: Update active-metrics.yml

For each source that pulled successfully, update `last_pulled_at` to the current timestamp. This is the only mutation `/metrics-pull` makes to `active-metrics.yml`.

## Parallel dispatch

For repos with multiple active sources, run adapter pulls in parallel in a single message. Each adapter is independent; serial pulls waste time and don't produce more accurate data.

Example for a project with GitHub + Plausible + Stripe:
- All three adapters' `gh api` / `curl` / `stripe` commands issued in one parallel batch.
- Wait for all, then proceed to delta + report.

## Partial success behavior

If SOME sources succeed and others fail:
- Save snapshots for successful sources.
- Report failures per source in the main report under "Skipped / failed sources" with the reason.
- Proceed with deltas and evidence entries for successful sources.
- Do NOT block evidence drafting on a partially-failed pull.

## Idempotency

- Multiple invocations on the same day overwrite the day's snapshot (no accumulation of intra-day noise).
- Evidence entries are drafted freshly each run — the user decides what to append.

## What NOT to Do

- Never auto-write to canvas files. Evidence requires human review.
- Never treat raw counts as success metrics without pairing with a ratio (Goodhart).
- Never compute or visualize beyond simple deltas. If the output starts to look like a dashboard, stop — that's feature creep. Mycelium is not an analytics platform.
- Never loop on rate limits. Single retry, then skip.
- Never leak credentials into reports, snapshots, or the decision log.

## Output

- Raw snapshots: `.claude/evals/metrics/<source>/YYYY-MM-DD.json`
- Combined report: `.claude/evals/metrics/YYYY-MM-DD.md`
- Drafted evidence entries (presented to user, appended on confirmation)
- Updated `last_pulled_at` in `active-metrics.yml`

## Theory Citations

- Gilad: Evidence-Guided. Confidence earned from observable signals, not asserted. Automated pulls lower the cost of evidence enough that users gather it without prompting.
- Goodhart: raw counts are gameable; pair every vanity metric with a ratio that pressures against manipulation.
- Torres: CDH / evidence-based progression. Canvas becomes a reflection of reality, not a snapshot from the last time someone remembered to update it.
- Forsgren: measure capabilities/outcomes, not vanity.
