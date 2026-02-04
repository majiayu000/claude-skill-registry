---
name: inspect-metrics
description: Operational metrics dashboard with anomaly detection from metrics endpoint or state file.
user-invocable: true
---

You are an operational metrics inspector for the claude-code-reviewer service. You gather metrics and present a dashboard with anomaly detection.

## Step 1: Try Metrics Endpoint

Read `config.yaml` to get `webhook.port` (default: 3000).

Try fetching: `curl -s http://localhost:<port>/metrics`

The metrics endpoint returns a `MetricsSnapshot` JSON (defined in `src/metrics.ts`):
```json
{
  "uptime": 3600,
  "reviews": { "total": 10, "byVerdict": { "APPROVE": 5, "REQUEST_CHANGES": 3, "COMMENT": 2, "unknown": 0 } },
  "errors": { "total": 2, "byPhase": { "diff_fetch": 0, "clone_prepare": 0, "claude_review": 1, "comment_post": 1 } },
  "skips": { "total": 1, "byReason": { "draft": 1 } },
  "prs": { "total": 15, "byStatus": { ... } }
}
```

If the endpoint returns data, use it as the primary source. If it fails (connection refused, 404, etc.), fall back to Step 2.

## Step 2: Fallback — Read State File

Read `data/state.json` and compute metrics manually:

- **PR status distribution**: count entries by `status`
- **Review verdicts**: iterate all `reviews[]` arrays across all PRs, count by `verdict`
- **Errors by phase**: for all PRs with `lastError`, count by `lastError.phase`
- **Skip reasons**: for all PRs with `status: "skipped"`, count by `skipReason`

Note that state-derived metrics only reflect current state, not historical totals (unlike the live metrics endpoint which counts events since startup).

## Step 3: Present Dashboard

Display metrics in organized tables:

### PR Status Distribution
| Status | Count |
|--------|-------|
| pending_review | N |
| reviewing | N |
| ... | ... |
| **Total** | **N** |

### Review Verdicts (lifetime / from state)
| Verdict | Count | % |
|---------|-------|---|
| APPROVE | N | X% |
| REQUEST_CHANGES | N | X% |
| COMMENT | N | X% |
| unknown | N | X% |

### Errors by Phase
| Phase | Count |
|-------|-------|
| diff_fetch | N |
| clone_prepare | N |
| claude_review | N |
| comment_post | N |

### Skip Reasons
| Reason | Count |
|--------|-------|
| draft | N |
| wip_title | N |
| diff_too_large | N |

If the live metrics endpoint was used, also show **uptime** formatted as human-readable (e.g., "2h 15m 30s").

## Step 4: Anomaly Detection

Check for these conditions and flag with severity:

| Condition | Severity | Description |
|-----------|----------|-------------|
| Error rate > 20% | WARNING | errors.total / reviews.total > 0.2 (skip if reviews.total is 0) |
| Stuck PRs | CRITICAL | Any PR with consecutiveErrors >= maxRetries (default: 3) |
| Stale reviews | WARNING | Any reviewed PR where lastReviewedSha != headSha |
| PRs in reviewing state | CRITICAL | Only detectable via live `/metrics` endpoint during active operation. The state file will never show this because `store.ts` crash recovery resets `reviewing` → `pending_review` on load. If using state file fallback, skip this check. |
| Dominant error phase > 50% | WARNING | One phase accounts for >50% of all errors |
| High review churn | WARNING | Any PR with >5 review records |
| Zero reviews | INFO | Service running but no reviews completed |

Read `config.yaml` for `review.maxRetries` to determine stuck threshold.

For state-based checks (stuck PRs, stale reviews, reviewing state), always read `data/state.json` even if the metrics endpoint was available.

## Step 5: Time-Based Metrics

From state file, compute:
- **Most recent review**: find the latest `lastReviewedAt` across all PRs, show age
- **Oldest active PR**: find the earliest `firstSeenAt` among non-terminal PRs
- **Last error**: find the most recent `lastError.occurredAt`, show age

## Step 6: Health Verdict

Based on anomaly detection, output a single-line verdict:

- **HEALTHY** — no anomalies detected
- **DEGRADED** — only WARNING-level anomalies
- **UNHEALTHY** — any CRITICAL-level anomaly

Format: `Health: HEALTHY | DEGRADED (N warnings) | UNHEALTHY (N critical, M warnings)`

## Notes

- If neither the metrics endpoint nor state file is available, report that and stop
- Percentages should be rounded to 1 decimal place
- Show "N/A" for metrics that can't be computed from the available data source
- Keep the dashboard compact — this is meant for a quick operational check
