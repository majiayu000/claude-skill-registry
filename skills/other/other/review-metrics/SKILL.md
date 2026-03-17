---
name: review-metrics
description: |
  Analyze team code review activity and performance metrics from GitHub PRs.
  Use when: (1) User asks about team review statistics or performance,
  (2) User wants to see who reviewed what PRs, (3) User asks about review
  response times or approval rates, (4) User mentions "review metrics",
  "review stats", "review activity", or "レビュー分析",
  (5) User asks about review bottlenecks, stuck PRs, or review load.
argument-hint: "[week|last-week|month] [comments|reviewed|approved|response-time|fix-time|bottleneck|stuck|reviewer-load|cycles|pr-size]"
allowed-tools:
  - Bash
allowed-prompts:
  - tool: Bash
    prompt: "gh repo view"
  - tool: Bash
    prompt: "gh api graphql"
  - tool: Bash
    prompt: "gh api repos"
  - tool: Bash
    prompt: "gh pr list"
  - tool: Bash
    prompt: "gh pr view"
---

# Review Metrics

Collect and analyze team review metrics from GitHub pull requests.

## Invocation

Run via the unified dispatch script:

```bash
../../scripts/dispatch.sh $0 $1
```

Where `$0` is the period (default: `week`) and `$1` is the command.
If no command is provided, all rankings are shown.

## Examples

| Command | Dispatch |
|---------|----------|
| `/review-metrics` | `../../scripts/dispatch.sh week` |
| `/review-metrics last-week` | `../../scripts/dispatch.sh last-week` |
| `/review-metrics month comments` | `../../scripts/dispatch.sh month comments` |
| `/review-metrics last-week response-time` | `../../scripts/dispatch.sh last-week response-time` |
| `/review-metrics last-week fix-time` | `../../scripts/dispatch.sh last-week fix-time` |
| `/review-metrics last-week bottleneck` | `../../scripts/dispatch.sh last-week bottleneck` |
| `/review-metrics stuck` | `../../scripts/dispatch.sh week stuck` |
| `/review-metrics last-week reviewer-load` | `../../scripts/dispatch.sh last-week reviewer-load` |
| `/review-metrics last-week cycles` | `../../scripts/dispatch.sh last-week cycles` |
| `/review-metrics last-week pr-size` | `../../scripts/dispatch.sh last-week pr-size` |

## Available Scripts

### Ranking Scripts (Top 3)

| Script | Description |
|--------|-------------|
| `collect-metrics.sh` | All rankings combined |
| `ranking-comments.sh` | Review comments ranking only |
| `ranking-reviewed.sh` | Reviewed PRs ranking only |
| `ranking-approved.sh` | Approved PRs ranking only |
| `ranking-response-time.sh` | Response time ranking only |
| `ranking-fix-time.sh` | Fix time ranking (comment to commit) |

### Analysis Scripts (Team-wide)

| Script | Description |
|--------|-------------|
| `analysis-bottleneck.sh` | PR lifecycle phase breakdown (wait/review/merge) with p50/p90 |
| `analysis-stuck-prs.sh` | Currently stuck PRs needing attention |
| `analysis-reviewer-load.sh` | Full team review workload distribution |
| `analysis-review-cycles.sh` | Review round counts and change-request patterns |
| `analysis-pr-size.sh` | PR size vs review speed correlation |

## Period Options

| Period | Description |
|--------|-------------|
| `week` | Current week (Monday-Friday) - default |
| `last-week` | Previous week (Monday-Friday) |
| `month` | Last 30 days |

Note: `stuck` ignores period — it always shows current state.

## Metrics Collected

### Rankings
- **Review Comments**: Number of review comments left
- **Reviewed PRs**: Number of PRs reviewed
- **Approved PRs**: Number of PRs approved
- **Avg Response Time**: Time from review request to first review
- **Avg Fix Time**: Time from review comment to next commit (fix response)

### Analysis
- **Bottleneck**: PR lifecycle decomposition (Wait for Review / Review Cycles / Merge Delay) with Avg, p50, p90
- **Stuck PRs**: Open PRs waiting >24h for review, unaddressed change requests, long-running PRs >5 days
- **Reviewer Load**: Per-member requests/completions/rates/response times/pending counts
- **Review Cycles**: Round distribution (1-round vs multi-round), top change-requesters
- **PR Size**: Size bucket (XS/S/M/L/XL) correlation with cycle time and review rounds

## Requirements

- GitHub CLI (`gh`) installed and authenticated
- `jq` for JSON processing
