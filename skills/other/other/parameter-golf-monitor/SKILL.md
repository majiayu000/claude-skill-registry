---
name: parameter-golf-monitor
description: >
  Monitor the openai/parameter-golf competition leaderboard by fetching PR data from GitHub.
  Use this skill whenever the user asks about the parameter-golf competition, leaderboard standings,
  competitor scores, PR rankings, who's winning, what the current SOTA is, or wants to track
  competition progress. Also trigger when the user mentions "parameter golf", "val_bpb scores",
  "competition PRs", or asks to check/watch the leaderboard. Works for any competitor — not tied
  to a specific GitHub account.
---

# Parameter Golf Monitor

A skill for tracking the [openai/parameter-golf](https://github.com/openai/parameter-golf) competition leaderboard in real time by fetching open and merged PRs from GitHub's public API.

## What this skill does

The monitor script at `scripts/monitor.py` queries the GitHub API for PRs on `openai/parameter-golf`, extracts `val_bpb` scores from titles and bodies, classifies submissions (record vs non-record), and displays a ranked leaderboard table.

It requires **zero authentication** — it uses the unauthenticated GitHub API (60 requests/hour rate limit).

## When to use this skill

- User asks "what's the current leaderboard?" or "who's winning parameter golf?"
- User wants to check their ranking: "where do I stand?" or "how's my PR doing?"
- User asks about competitor scores or techniques
- User wants to monitor for new submissions or changes
- User says "check the competition" or "show me the standings"
- User wants to compare their score against the field

## How to run

The script is at `scripts/monitor.py` relative to this skill's directory. Run it with Python 3 (no dependencies beyond stdlib).

### One-shot leaderboard

```bash
python3 <skill-dir>/scripts/monitor.py
```

Shows all open PRs ranked by `val_bpb` (lower is better).

### Highlight a specific user

```bash
python3 <skill-dir>/scripts/monitor.py --me <github-username>
```

Marks the user's PR(s) with `<--` and shows their rank + gap to #1 in the summary. Ask the user for their GitHub username if they want highlighting and you don't already know it.

### Common flag combinations

| Goal | Command |
|------|---------|
| Full leaderboard | `python3 scripts/monitor.py` |
| Top 10 records only | `python3 scripts/monitor.py --top 10 --records-only` |
| Highlight a user | `python3 scripts/monitor.py --me USERNAME` |
| Merged records (SOTA history) | `python3 scripts/monitor.py --merged` |
| Everything (open + merged) | `python3 scripts/monitor.py --all` |
| Today's PRs only | `python3 scripts/monitor.py --since YYYY-MM-DD` |
| JSON for piping | `python3 scripts/monitor.py --json` |
| Live polling every 5 min | `python3 scripts/monitor.py --watch 5` |

### All flags

- `--me USER` — Highlight a GitHub username. Shows rank and gap to #1.
- `--top N` — Show only the top N scored entries (highlighted user always shown even if outside top N).
- `--records-only` — Exclude non-record submissions.
- `--merged` — Show only merged PRs.
- `--all` — Show both open and merged PRs.
- `--since YYYY-MM-DD` — Filter to PRs created on or after this date.
- `--json` — Output as JSON instead of a table (useful for piping to `jq` or other tools).
- `--watch MIN` — Poll every N minutes continuously (Ctrl+C to stop).

## Interpreting results

- **Rank** is by `val_bpb` ascending (lower = better). Only scored PRs get a numeric rank.
- **Status** shows `open`, `merged`, or `non-rec` (non-record submission).
- Scores marked `?` mean no `val_bpb` could be extracted from the PR title or body.
- Some very low scores (e.g. < 1.10) may be evaluation-only or use non-standard setups — check the PR for details.
- The **gap to #1** in the summary tells the highlighted user how far they are from the top.

## Rate limits

The GitHub API allows 60 unauthenticated requests per hour. Each `run_once` call makes 1 request (open PRs) or 2 requests (if `--merged` or `--all`). The `--watch` mode respects this — polling every 5 minutes uses ~12-24 requests/hour.

If you hit the rate limit, the script will show an error and retry on the next interval.

## Example output

```
[2026-03-20 02:17:15] Parameter Golf Leaderboard (open PRs)

Rank   val_bpb     PR  Status    Author              Date        Title
----------------------------------------------------------------------------------------------------
   1   1.15390  #135   open      unnir               2026-03-19  Record: OrthoInit + Int6 MLP3x + BigramHash + SmearGate
   2   1.15800  #106   open      krammnic            2026-03-19  record: 1.158
   3   1.15850  #122   open      mtybadger           2026-03-19  Record: Sliding Window Eval, 2048 Vocab Size
   4   1.16019  #156   open      dexhunter           2026-03-20  Int6 STE + NorMuon + SWA + Sliding Window  <--

Best: val_bpb=1.15390 (#135 by unnir)
Total: 56 PRs, 40 with scores

You (dexhunter): rank #4, val_bpb=1.16019, gap to #1: +0.00629
```
