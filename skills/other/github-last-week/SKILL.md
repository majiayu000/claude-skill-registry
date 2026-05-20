---
name: github:last-week
description: Weekly repository report - deep issue analysis, PR health, CI trends, actionable recommendations
---

# Last Week Report

Deep weekly analysis of repository health: issue investigation, PR status, CI trends.

## When to Use

- Weekly standup preparation
- Sprint retrospective input
- Tracking project health over time

> **Auto-approved**: All `gh` read commands are auto-approved.

## Workflow

### Phase 0: Gather Data (MUST run first)

Run the data gathering script to get a consistent snapshot of all issues, PRs, and CI runs. This prevents stale data from long-running analysis.

```bash
./.github/scripts/reports/weekly-report-data.sh 7 kagenti/kagenti
```

This creates JSON files in `/tmp/kagenti/github/data/`:
- `merged-prs.json` — PRs merged in the period
- `open-prs.json` — Currently open PRs (live snapshot)
- `open-issues.json` — Currently open issues (live snapshot)
- `new-issues.json` — Issues created in the period
- `ci-runs.json` — CI runs on main
- `ci-runs-all.json` — All CI runs

**IMPORTANT**: All subsequent phases MUST read from these JSON files, NOT re-query `gh`. This ensures consistency — PRs won't change state mid-analysis.

### Phase 1: Quick Stats

Read from the gathered data:

```bash
echo "Merged PRs: $(jq length /tmp/kagenti/github/data/merged-prs.json)"
```

```bash
echo "Open PRs: $(jq length /tmp/kagenti/github/data/open-prs.json)"
```

```bash
echo "Open issues: $(jq length /tmp/kagenti/github/data/open-issues.json)"
```

```bash
echo "New issues: $(jq length /tmp/kagenti/github/data/new-issues.json)"
```

### Phase 2: Deep Issue Analysis

For EVERY open issue (from `open-issues.json`), investigate:

Read from gathered data (do NOT re-query `gh`):

```bash
cat /tmp/kagenti/github/data/open-issues.json | jq '.[].number'
```

For each issue, determine:

1. **Still relevant?** — Check if the bug still exists on upstream/main
   - Search codebase for the affected code/component
   - Check if a fix was merged since the issue was created
   - Check if a test covers this scenario

2. **Work in progress?** — Check if any PR references this issue
   ```bash
   gh pr list --repo kagenti/kagenti --state all --search "issue-number" --json number,title,state
   ```

3. **Severity classification**:
   - **Security**: Credential leaks, auth bypass, injection
   - **Blocking**: Breaks deployment, tests, or user workflow
   - **Bug**: Broken behavior but workaround exists
   - **Feature**: New capability request
   - **Epic**: Multi-PR initiative (track progress)
   - **Stale**: No activity >30 days, may be outdated

4. **Actionable recommendation**: Close, update, assign, or create PR

### Phase 3: Deep PR Analysis

For EVERY open PR (from `open-prs.json`), investigate:

```bash
cat /tmp/kagenti/github/data/open-prs.json | jq '.[].number'
```

For each PR, determine:

1. **CI status**: Does it pass all checks?
2. **Needs /run-e2e?**: Does it touch kagenti/charts/deployments/.github paths?
3. **Review status**: Approved, changes requested, or waiting?
4. **Health**: Is it stale (>14 days)? Has merge conflicts?
5. **Summary**: What does this PR do? (read the body)

Classify each PR:

| Health | Criteria | Next Step |
|--------|----------|-----------|
| Ready to merge | Approved + CI passing | Merge it |
| Needs review | CI passing, no review | Request review |
| Needs /run-e2e | Touches deploy paths, no HyperShift run | Comment /run-e2e |
| CI failing | Has failures | Investigate with `rca:ci` |
| Stale | No update >14 days | Ping author or close |
| Conflicts | Mergeable = CONFLICTING | Author needs to rebase |
| Changes requested | Reviewer asked for changes | Author needs to address |

### Phase 3b: CI Failure Timeline

Get all runs on main (last 7 days):

```bash
gh run list --repo kagenti/kagenti --branch main --limit 30 --json databaseId,conclusion,name,createdAt,headSha,displayTitle
```

For each failed run, get the failing job and step:

```bash
gh run view <run-id> --repo kagenti/kagenti --json jobs --jq '.jobs[] | select(.conclusion == "failure") | "\(.name): \(.steps[] | select(.conclusion == "failure") | .name)"'
```

Get the commit that triggered the failure:

```bash
gh run view <run-id> --repo kagenti/kagenti --json headSha --jq '.headSha'
```

Check what that commit changed:

```bash
gh api repos/kagenti/kagenti/commits/<sha> --jq '.files[].filename'
```

Build a timeline of failures with root cause correlation:
- Map each failure to the triggering commit
- Identify if the same job/step fails repeatedly (infrastructure issue)
- Identify if failures started after a specific merge (regression)

Since E2E doesn't run on every merge, find candidate PRs that could have caused a failure:

```bash
gh pr list --repo kagenti/kagenti --state merged --json number,title,mergedAt,changedFiles --jq '.[] | select(.mergedAt > "LAST_SUCCESS_DATE" and .mergedAt < "FAILURE_DATE") | "#\(.number) \(.title) (\(.changedFiles) files)"'
```

For each candidate PR, check if it touched relevant paths:
- `charts/` or `deployments/` → likely deploy/config issue
- `kagenti/tests/` → test change may have introduced failure
- `.github/workflows/` or `.github/scripts/` → CI infrastructure change
- `kagenti/backend/` or `kagenti/auth/` → application logic change

Correlate the failure type with the PR changes to identify the most likely cause.

### Phase 4: Generate Report

Write the full report as markdown. Structure:

```markdown
# Weekly Report: [date range]

## Quick Stats
- Merged PRs: N
- New issues: N
- CI pass rate: X/Y on main

## Issue Analysis

### Security Issues
| # | Title | Status | Recommendation |
...

### Blocking Issues
| # | Title | Status | Recommendation |
...

### Bug Reports
| # | Title | Still affects main? | PR exists? | Recommendation |
...

### Feature Requests
| # | Title | Priority | Recommendation |
...

### Epics (track progress)
| # | Title | PRs merged/open | % done estimate |
...

### Issues to Close
| # | Title | Reason |
...
(Issues where fix was already merged, or issue is outdated)

## PR Analysis

### Ready to Merge
| # | Title | Author | Approved by |
...

### Needs Review (CI passing)
| # | Title | Author | Days waiting |
...

### Needs /run-e2e
| # | Title | Reason |
...

### Unhealthy PRs
| # | Title | Problem | Next step |
...

## CI Health

### Pass Rate
- Main branch: X/Y runs passed (Z%)
- HyperShift E2E: X/Y passed
- Kind E2E: X/Y passed
- Security/Lint/Build: X/Y passed

### Failure Timeline
| Date | Workflow | Job | Failure | Likely Cause |
|------|----------|-----|---------|-------------|
| ... | E2E HyperShift | Deploy & Test | timeout | Cluster creation slow |
| ... | CI | build | compile error | PR #N broke import |

### Failure Patterns
- **Recurring**: [failures that happen repeatedly — infrastructure, flaky tests]
- **One-off**: [failures tied to specific commits]
- **Trend**: [getting better/worse over time]

### Root Cause Correlation
For each failure, identify candidate PRs merged between last success
and the failure. Check which files they touched to find likely cause.

## Action Items

Single flat list, ordered by priority. No timescales.

| # | Action | Owner | Priority |
|---|--------|-------|----------|
| 1 | [Highest priority action] | [owner] | P0 |
| 2 | [Next action] | [owner] | P1 |
```

Save report:

```bash
# Save to /tmp/kagenti/github/weekly-report.md
```

### Phase 5: Ask User

After generating the report, ask:

> Weekly report ready. Want me to create a GitHub issue with this?
> Suggested title: "📊 Weekly Report [start-date] – [end-date]"
>
> You can also suggest a different title.

Only create the issue after user confirms title and content.

## Related Skills

- `github:issues` - Deep dive into individual issue triage
- `github:prs` - Deep dive into individual PR health
- `git:status` - Worktree and PR status overview
- `ci:status` - Detailed CI check analysis
- `rca:ci` - Investigate CI failures
- `repo:issue` - Issue creation format
