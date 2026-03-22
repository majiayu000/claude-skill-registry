---
name: external-intel-provider-rollout
description: Replace mock intel providers with live external adapters and keep scheduler, status, tests, and docs aligned. Use when working on external market/news API integration, provider env vars, or rollout validation for `news_briefing`, `eod_summary`, and `watch_poll`.
---

# External Intel Provider Rollout

Read the contract first, then make the smallest change that moves one provider path closer to live operation.

Use this skill when the task touches any of these areas:

- `bot/intel/providers/news.py`
- `bot/intel/providers/market.py`
- `bot/features/intel_scheduler.py`
- `bot/app/settings.py`
- `docs/specs/external-intel-api-spec.md`
- provider status, job status, env vars, or rollout docs

## Quick Start

1. Read `docs/context/session-handoff.md`, `docs/context/goals.md`, and `docs/specs/external-intel-api-spec.md`.
2. Inspect the current provider interface and the scheduler path that consumes it.
3. Identify which one of `news_briefing`, `eod_summary`, or `watch_poll` is in scope.
4. Confirm the expected state updates, logs, tests, and docs before editing.

## Workflow

### 1. Fix the contract before the transport

- Normalize external data into the existing `NewsItem`, `Quote`, and `EodSummary` shapes.
- Keep vendor-specific fields out of the scheduler and policy layers.
- Preserve the spec's timeout, retry, and rate-limit expectations unless the user asks to change them.

### 2. Change one provider path at a time

- Prefer a new adapter or a narrow replacement over a broad rewrite.
- Keep the current scheduler semantics intact while swapping the data source.
- Do not couple `news_briefing`, `eod_summary`, and `watch_poll` rollout work unless the task explicitly requires it.

### 3. Preserve operational truth

- Make sure provider failures surface through `set_provider_status(...)`.
- Make sure job outcomes still distinguish `ok`, `failed`, `skipped`, and `no-target` style paths when applicable.
- Treat stale or partial external data as an operational risk, not just a parsing problem.

### 4. Validate the risky edge

- Add or update targeted tests around the changed provider path.
- Prefer tests that cover normalization, scheduler failure handling, and status recording.
- If live verification is not possible, leave a short note about what remains unverified.

### 5. Update runbooks and context

- Update `README.md` when env vars, run commands, or operating assumptions change.
- Update the relevant `docs/context/*.md` files before finishing.
- Record remaining vendor, auth, quota, or data freshness risks explicitly.

## Repo-Specific Checks

### News briefing

- Keep dedup behavior tied to fetched items, not post-success assumptions.
- Verify regional split (`domestic`, `global`) still matches the post body contract.

### EOD summary

- Keep the trading-day guard ahead of the external fetch when possible.
- Match `date_text`, index changes, and ranking rows to existing render expectations.

### Watch poll

- Watch quote freshness and cooldown behavior closely.
- Prefer batch-friendly adapter design even if the current interface is single-symbol.

## Done When

- The changed provider path matches `docs/specs/external-intel-api-spec.md`.
- Relevant tests or logical verification were performed and recorded.
- Operational docs and `docs/context/*` were updated when behavior changed.
- Remaining rollout risk is written down instead of implied.
