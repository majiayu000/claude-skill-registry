---
name: kpi-pr-throughput
description: KPI for measuring and improving PR throughput. Defines metrics, measurement methods, and improvement strategies. Use to optimize how many quality PRs get merged.
---

# KPI: PR Throughput

**Definition**: The rate at which quality PRs are merged to main.

## Why This Matters

PR throughput measures productive output. High throughput with maintained quality indicates efficient development. Low throughput suggests blockers in the development pipeline.

## Metrics

### Primary Metric
**PRs Merged Per Session** - Count of PRs successfully merged during an agent session.

### Supporting Metrics
| Metric | What It Measures |
|--------|------------------|
| Time to Merge | Latency from PR creation to merge |
| Review Cycles | Number of review rounds needed |
| First-Pass Approval Rate | PRs approved without changes requested |
| Revert Rate | PRs reverted due to issues |

## Measurement

### During Session

Track:
```bash
# Count merged PRs by this agent
gh pr list --state merged --author @me --json number | jq length
```

### Quality Gate

Throughput only counts if:
- PR was not reverted
- Main branch stayed green
- No follow-up fix PRs needed

## Target Benchmarks

| Performance | PRs/Session |
|-------------|-------------|
| Struggling | 0 |
| Normal | 1-2 |
| High | 3-5 |
| Exceptional | 5+ |

## Improvement Strategies

### 1. Scope Down Aggressively

Large PRs take longer to review and have higher failure rates. Target:
- <300 lines changed per PR
- Single logical change per PR
- Clear, focused description

### 2. Front-load Verification

Run `./verify.sh --ui=false` before creating PR. Catching issues early avoids review cycles.

### 3. Write Good PR Descriptions

Clear descriptions reduce review time:
- What changed and why
- How to test
- Any risks or trade-offs

### 4. Stack PRs When Possible

For dependent changes, create stacked PRs that can be reviewed in parallel.

### 5. Address Feedback Promptly

When review feedback arrives, address it immediately while context is fresh.

## Blockers to Watch

| Blocker | Detection | Mitigation |
|---------|-----------|------------|
| Review delay | PR open >1 hour | Request review explicitly |
| Verification failures | verify.sh fails | Fix before PR, not after |
| Scope creep | PR grows beyond original intent | Split into multiple PRs |
| Merge conflicts | Can't merge cleanly | Rebase frequently |

## Anti-Patterns

- **Quantity over quality** - Merging broken code destroys throughput
- **Mega-PRs** - One 1000-line PR is worse than five 200-line PRs
- **Skipping review** - Unreviewed code accumulates debt
- **Ignoring CI** - Broken verification means broken code
