---
name: ln-911-github-triager
description: "Produces prioritized triage report from open GitHub issues, PRs, and discussions. Use when reviewing community backlog."
license: MIT
allowed-tools: Bash, Read
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-911-github-triager

**Type:** L3 Worker (standalone)
**Category:** 9XX Community Engagement
**Invocation:** Standalone or as part of a broader community triage workflow

Scans all open issues, PRs, and discussions in the current repository. Categorizes by urgency. Produces an actionable triage report.

---

## Arguments

`$ARGUMENTS` controls scope and staleness threshold:

| Token | Effect | Default |
|-------|--------|---------|
| `issues` | Scan issues only | All three |
| `prs` | Scan PRs only | All three |
| `discussions` | Scan discussions only | All three |
| Number (e.g., `14`) | Staleness threshold in days | 7 |
| `issues 30` | Combine: scope + threshold | -- |
| `summary` | Compact output for coordinator: skip Phase 4 preview, return red flags + priority counts + metrics only | Full interactive report |

Parse `$ARGUMENTS`: extract scope tokens (`issues`, `prs`, `discussions`), numeric threshold, and `summary` flag. If no scope tokens, scan all three. If no number, default to 7 days.

---

## Phase 0: GitHub Discovery

**MANDATORY READ:** Load `shared/references/community_github_discovery.md`

Execute the discovery protocol. Extract:
- `{owner}/{repo}` for `--repo` flag and URLs
- `maintainer` login (authenticated user) for maintainer detection
- Verify `gh` is authenticated

Load strategy: check `docs/community_engagement_strategy.md` in target project, fallback to `shared/references/community_strategy_template.md`. Extract Section 5 (Engagement Metrics) for targets and red flags.

---

## Phase 1: Fetch Data

Run these `gh` commands based on scope. Execute all applicable fetches in parallel.

### 1a. Issues

```bash
gh issue list --repo {owner}/{repo} --state open --limit 100 --json number,title,labels,createdAt,updatedAt,author,comments,assignees
```

### 1b. Pull Requests

```bash
gh pr list --repo {owner}/{repo} --state open --limit 100 --json number,title,labels,createdAt,updatedAt,author,reviewDecision,reviewRequests,isDraft,comments,assignees
```

### 1c. Discussions (GraphQL)

```bash
gh api graphql -f query='
  query($owner: String!, $name: String!) {
    repository(owner: $owner, name: $name) {
      discussions(first: 100, states: OPEN) {
        nodes {
          number
          title
          category { name }
          createdAt
          updatedAt
          author { login }
          answerChosenAt
          labels(first: 5) { nodes { name } }
          comments(first: 20) {
            totalCount
            nodes {
              author { login }
              createdAt
            }
          }
        }
      }
    }
  }
' -f owner="{owner}" -f name="{repo}"
```

**Gate:** If all sources return zero items, report "No open items. Triage complete." and stop.

---

## Phase 2: Classify Each Item

For every fetched item, evaluate these conditions. An item can match multiple -- use highest priority.

### Priority Matrix

| Priority | Condition | Applies to |
|----------|-----------|------------|
| **P0 Critical** | Label contains `bug` AND no assignee | Issues |
| **P0 Critical** | Label contains `breaking` | Issues, PRs |
| **P1 Urgent** | Author != maintainer AND zero comments from maintainer | Issues, Discussions |
| **P1 Urgent** | Q&A discussion with `answerChosenAt` is null AND author != maintainer | Discussions |
| **P1 Urgent** | `reviewDecision` is null or `REVIEW_REQUIRED` | PRs |
| **P2 Stale** | No activity for > threshold days (`updatedAt` older than threshold) | All |
| **P3 Monitor** | PR marked as draft (`isDraft` is true) | PRs |
| **P3 Monitor** | Author == maintainer AND 0 community replies | Discussions |
| **P4 Info** | Items not matching any above condition | All |

### Maintainer Detection

The maintainer login comes from Phase 0 discovery (`viewer.login`). An item "has maintainer reply" if any comment's `author.login` equals the maintainer login.

For issues: check `comments` array authors. For discussions: check `comments.nodes[].author.login`.

### Staleness Calculation

Days since last activity: `(today - updatedAt)` in days. Compare against threshold (default 7, or from `$ARGUMENTS`).

### Label Urgency Signals

Labels that elevate priority: `bug`, `breaking`, `security`, `urgent`.

Labels that signal engagement opportunity (not urgency): `help wanted`, `good first issue`.

---

## Phase 3: Engagement Metrics

Calculate aggregate metrics per strategy Section 5:

| Metric | Calculation | Target | Red Flag |
|--------|-------------|--------|----------|
| Time to First Response | Avg(first maintainer comment - item created) for items WITH reply | <24h | >72h |
| Unanswered discussions | Count where author != maintainer AND no maintainer comment AND age > threshold | 0 | Any >7 days |
| Community-to-maintainer ratio | Non-maintainer comments / maintainer comments across all items | >0.3 | 0 |
| New discussions this month | Discussions created in last 30 days | >2 | 0 |
| Zero-engagement items | Items with 0 comments total | -- | -- |

---

## Phase 4: Preview Table

If `$ARGUMENTS` contains `summary` → skip this phase entirely. Output compact summary (red flags, priority counts per category, health metrics table) and stop. Do NOT compose the full Phase 5 report.

**Otherwise (standalone mode):** present a compact summary table of ALL classified items for user review. **Wait for user approval before proceeding to Phase 5.**

```
### Triage Preview -- {total count} items found

| # | Type | Title | Priority | Age | Key Signal |
|---|------|-------|----------|-----|------------|
| {number} | {Issue/PR/Discussion} | {title (truncated to 50 chars)} | {P0/P1/P2/P3/P4} | {days}d | {short reason} |
```

Sort by priority (P0 first), then by age (oldest first) within each priority group.

After presenting, ask the user:
- Confirm priorities look correct
- Whether to exclude any items from the full report
- Whether to adjust the staleness threshold

Proceed to Phase 5 only after user confirms.

---

## Phase 5: Compose Report

Present the full triage report in this format:

```
## GitHub Triage Report -- {YYYY-MM-DD}

**Scope:** {issues/PRs/discussions or "all"} | **Threshold:** {N} days | **Open items:** {total count}
```

### Red Flag Alerts

If any red flags from Phase 3 are triggered, add BEFORE Health Metrics:

```
> [!WARNING]
> **Red flags detected:**
> - {description, e.g., "2 unanswered discussions older than 7 days"}
```

### Health Metrics Table

```
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Unanswered (>{N}d) | {count} | 0 | {OK / RED FLAG} |
| Avg first response | {hours}h | <24h | {OK / RED FLAG} |
| Community:maintainer ratio | {ratio} | >0.3 | {OK / RED FLAG} |
| New discussions (30d) | {count} | >2 | {OK / RED FLAG} |
| Zero-engagement items | {count} | -- | {count} |
```

### Priority Tables

For each priority P0..P3, show header with count. If count is 0, show header `(0)` and skip table.

**P0 Critical:**

| # | Type | Title | Labels | Age | Action Needed |
|---|------|-------|--------|-----|---------------|

**P1 Urgent:**

| # | Type | Title | Author | Age | Why |
|---|------|-------|--------|-----|-----|

**P2 Stale:**

| # | Type | Title | Last Activity | Days Stale |
|---|------|-------|---------------|------------|

**P3 Monitor:**

| # | Type | Title | Note |
|---|------|-------|------|

**P4 Info:** Do NOT list individually -- only include in total count.

### Recommended Actions

```
### Recommended Actions

1. **Respond:** {items needing maintainer reply, with GitHub URLs}
2. **Review:** {PRs needing review, with GitHub URLs}
3. **Close or bump:** {stale items -- suggest close if resolved, bump if relevant}
4. **Engage:** {items that could benefit from community call-to-action}
```

### Formatting Rules

- Sort items within each priority group by age (oldest first)
- URL format: `https://github.com/{owner}/{repo}/{issues|discussions|pull}/{number}`
- Dates in `YYYY-MM-DD`, ages in days
- All items in Recommended Actions must have direct GitHub URLs

---

## Rules

- **Read-only:** this skill fetches and reports -- never create, modify, or close any GitHub item
- **No publishing:** do not create issues, comments, labels, or any other GitHub state change
- **Maintainer login:** from Phase 0 discovery (authenticated user)
- **Default threshold:** 7 days (per strategy Section 5)
- **Rate limits:** if GraphQL rate limit hit, report partial results with a warning

---

## Definition of Done

- [ ] GitHub data fetched for all scoped item types (issues/PRs/discussions)
- [ ] Every item classified by priority (P0-P4)
- [ ] Engagement metrics calculated per strategy targets
- [ ] Report composed (full interactive report OR compact summary for coordinator)

---

**Version:** 1.0.0
**Last Updated:** 2026-03-13
