---
name: oss-evaluate-repo
description: |
  Evaluate whether an OSS repo is worth long-term investment before committing time.
  Assesses project health, governance, community, bus factor, and trajectory. Use when
  deciding whether to contribute to a specific repo, choosing between multiple repos,
  or evaluating a project's sustainability. Not for checking if a repo accepts
  contributions — use oss-find-issue for that.
---

# Evaluate Repo

Is this repo worth your time? Not every open source project deserves months of contribution effort. This skill evaluates project health, governance, community dynamics, and trajectory — so you invest in repos that will value your work and still exist in a year.

## Purpose

Contributing to OSS is an investment. A single meaningful PR takes 10-40 hours including learning the codebase. Before investing that time, you should know: Is this project actively maintained? Is the community healthy? Will your contributions be reviewed? Could the project be abandoned next month? This skill answers those questions with evidence, not vibes.

## When to Use

- Deciding whether to invest time in a specific OSS project
- Choosing between multiple repos to contribute to
- Evaluating a project before committing to a GSoC proposal
- **NOT** for checking if a repo accepts external contributions — `oss-find-issue` does that
- **NOT** for evaluating code quality — `oss-explore-repo` does that
- **NOT** for repos you're already contributing to — too late, you're invested

## Prerequisites

- A repo URL or name to evaluate
- `gh` CLI authenticated
- Clear goals for why you want to contribute (learning, career, community)

## Process

### 1. Check vital signs

These are binary health checks — if any fail, the repo is likely not worth investing in.

```bash
# Basic repo info
gh api repos/{owner}/{repo} --jq '{
  stars: .stargazers_count,
  forks: .forks_count,
  open_issues: .open_issues_count,
  archived: .archived,
  license: .license.spdx_id,
  created: .created_at,
  updated: .pushed_at,
  default_branch: .default_branch
}'

# Recent commit activity
git log --oneline -20 --since="6 months ago" 2>/dev/null || \
  gh api repos/{owner}/{repo}/commits --jq '.[0:10] | .[] | "\(.commit.author.date[:10]) \(.commit.message | split("\n")[0])"'

# Is the repo archived or in maintenance mode?
gh api repos/{owner}/{repo} --jq '.archived'
```

**Kill signals** (stop evaluation if any are true):
- Archived or read-only
- No commits in 6+ months
- README says "no longer maintained" or "looking for maintainers"
- License is missing or incompatible with your needs

### 2. Assess governance and bus factor

Who runs this project, and what happens if they leave?

```bash
# Top contributors (bus factor check)
gh api repos/{owner}/{repo}/contributors --jq '.[0:10] | .[] | "\(.contributions)\t\(.login)"'

# Recent committers (who's active NOW, not historically)
gh api repos/{owner}/{repo}/commits --jq '[.[0:50] | .[].author.login // "unknown"] | sort | group_by(.) | map({user: .[0], commits: length}) | sort_by(-.commits) | .[0:5] | .[] | "\(.commits)\t\(.user)"'

# Check if it's an org or personal project
gh api repos/{owner}/{repo} --jq '.owner.type'
```

Evaluate:
- **Bus factor**: How many people have committed in the last 3 months? If it's 1, the project dies if they stop.
- **Org vs personal**: Org-backed projects are more sustainable. Personal projects depend on one person's motivation.
- **Corporate backing**: Check if contributors have @company emails or if the org is a company. Corporate-backed OSS has resources but may shift priorities.
- **Governance model**: Is there a GOVERNANCE.md? A code of conduct? A clear decision-making process?

### 3. Evaluate community health

A healthy community means your contributions get reviewed, your questions get answered, and conflicts get resolved.

```bash
# Issue responsiveness — how quickly do issues get responses?
gh issue list -R {owner}/{repo} --state closed --limit 20 --json number,createdAt,closedAt,comments \
  --jq '.[] | {number, created: .createdAt[:10], closed: .closedAt[:10], comments: .comments}'

# PR review turnaround
gh pr list -R {owner}/{repo} --state merged --limit 20 --json number,createdAt,mergedAt,reviews \
  --jq '.[] | {number, created: .createdAt[:10], merged: .mergedAt[:10], reviews: (.reviews | length)}'

# Check for toxic interactions (look at recent closed issues/PRs)
gh issue list -R {owner}/{repo} --state closed --limit 5 --json number,comments \
  --jq '.[].number' | while read n; do
    echo "=== Issue #$n ==="
    gh issue view $n -R {owner}/{repo} --json comments --jq '.comments[-3:] | .[].body' | head -20
  done
```

**Healthy signals**:
- Issues get responses within a week
- PRs get reviewed within 2 weeks
- Maintainers are polite and constructive
- External contributors' PRs actually get merged
- Disagreements are resolved respectfully

**Unhealthy signals**:
- Issues and PRs sit for months without response
- Maintainer tone is dismissive or aggressive
- External PRs get closed without explanation
- Community discussions are toxic or absent
- "Drive-by" maintainer activity (once a month, closes 20 issues, disappears)

### 4. Check release cadence and stability

```bash
# Recent releases
gh release list -R {owner}/{repo} --limit 10

# Release frequency
gh release list -R {owner}/{repo} --limit 10 --json tagName,publishedAt \
  --jq '.[] | "\(.publishedAt[:10])\t\(.tagName)"'
```

Evaluate:
- **Regular releases**: Monthly or quarterly releases signal active development
- **Stale releases**: Last release 2+ years ago means your contributions won't reach users
- **Breaking changes**: Frequent major versions suggest instability
- **Changelog quality**: Detailed changelogs signal mature project management

### 5. Evaluate CI and development practices

```bash
# CI configuration
ls .github/workflows/ 2>/dev/null
cat .github/workflows/ci.yml 2>/dev/null | head -30

# Code quality tools
ls .eslintrc* .prettierrc* pyproject.toml rustfmt.toml .editorconfig 2>/dev/null

# Test infrastructure
find . -name "*test*" -type d -maxdepth 3 2>/dev/null | head -10
```

**Mature project signals**:
- CI runs on PRs (not just main)
- Linting and formatting enforced
- Test suite exists and is maintained
- Code review is required (branch protection)

### 6. Thinking gate — user articulates the decision

Present all findings in a structured summary and ask:

> "Based on everything we've found:
> 1. What's the strongest argument FOR contributing to this repo?
> 2. What's the biggest risk? (Bus factor, community health, stale reviews?)
> 3. Does this repo align with YOUR goals? (What do you want to learn or achieve?)
> 4. If this project were abandoned in 6 months, would your contributions still have been worth it for the learning alone?"

Wait for their answer. The last question is the most important — if the answer is no, the repo isn't worth the investment regardless of current health.

### 7. Make the decision

Based on the evaluation, the user decides:

- **Go**: Project is healthy, community is welcoming, goals align → proceed to `oss-find-issue`
- **Wait**: Project has potential but some concerns → bookmark and re-evaluate in a month
- **Pass**: Project has kill signals or doesn't align with goals → look for a different repo

## Related Skills

- **Next step (if Go)**: → `oss-explore-repo` — explore the codebase before contributing
- **Next step (if Go)**: → `oss-find-issue` — find an issue to work on
- **Alternative**: → `oss-find-real-issues` — if the repo is healthy but has no labeled issues

## Common Rationalizations

| Shortcut | Why It Fails |
|----------|-------------|
| "It has 50k stars, it must be healthy" | Stars measure popularity, not health. Many starred repos are unmaintained, have toxic communities, or don't merge external PRs. |
| "The code is interesting, that's enough" | Interesting code with an absent maintainer means your PR sits for months. The maintainer relationship matters as much as the code. |
| "I'll just contribute and see what happens" | Contributing without evaluating wastes 10-40 hours when your PR gets ignored. 30 minutes of evaluation saves weeks of frustration. |
| "It's backed by a big company, so it's safe" | Companies shift priorities. Corporate OSS projects get abandoned when the sponsoring team pivots. Check the actual activity, not the logo. |
| "I don't have time to evaluate, I just want to code" | Evaluation IS the most valuable use of your time. A well-chosen repo multiplies the impact of every hour you spend contributing. |

## Red Flags

- All recent commits are from a single person — extreme bus factor risk
- Issues and PRs from 6+ months ago sit unanswered — maintainer has checked out
- README promises features that don't exist — project is aspirational, not real
- Frequent hostile interactions in issues/PRs — toxic community
- User can't articulate why THIS repo over alternatives — they're picking randomly

## Verification Checklist

- [ ] Vital signs checked — not archived, recent commits exist, license verified (step 1)
- [ ] Bus factor assessed — multiple active contributors, org vs personal (step 2)
- [ ] Community health evaluated — response times, tone, external PR merge rate (step 3)
- [ ] Release cadence checked — regular releases reaching users (step 4)
- [ ] CI and dev practices assessed — tests, linting, code review (step 5)
- [ ] User articulated go/wait/pass decision with reasoning (step 6-7)

## Anti-patterns

- **DO NOT** evaluate based on stars alone — stars measure awareness, not health
- **DO NOT** skip the community health check — a technically excellent project with a toxic community isn't worth contributing to
- **DO NOT** evaluate for the user — present the evidence and let them decide
- **DO NOT** recommend repos you haven't evaluated — every recommendation needs evidence
- **DO NOT** rush the evaluation to start coding faster — 30 minutes of evaluation saves weeks of wasted effort
