---
name: ln-910-community-engagement
description: "Analyzes community health and delegates engagement tasks. Use when managing GitHub issues, discussions, and announcements."
disable-model-invocation: true
license: MIT
allowed-tools: Read, Grep, Glob, Bash, Skill
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-910-community-engagement

**Type:** L2 Coordinator (active)
**Category:** 9XX Community Engagement

Analyzes current community health and repository state, consults the engagement strategy, and delegates to the appropriate worker. Each worker is also invocable standalone.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | `$ARGUMENTS` (optional): topic, action keyword, or empty for auto-analysis |
| **Output** | Situation report + delegated action via worker skill |
| **Workers** | ln-911 (triager), ln-912 (announcer), ln-913 (debater), ln-914 (responder) |

---

## Phase 0: GitHub Discovery

**MANDATORY READ:** Load `shared/references/community_github_discovery.md`

Execute the discovery protocol. Extract:
- `{owner}/{repo}` for all GitHub operations
- `repo.id` for GraphQL mutations (passed to workers)
- `maintainer` login (authenticated user)
- Discussion category IDs

**Gate checks:** gh authenticated? Discussions enabled?

Load strategy: check `docs/community_engagement_strategy.md` in target project, fallback to `shared/references/community_strategy_template.md`.

---

## Phase 1: Situation Analysis

If `$ARGUMENTS` contains a direct action keyword (`announce`, `debate`, `triage`, `respond`), skip analysis and jump to Phase 3 (Direct Delegation).

Otherwise, gather context from multiple sources in parallel:

### 1a. Community Health

Delegate to triager in summary mode (no interactive preview):

`Skill(skill: "ln-911-github-triager", args: "summary")`

Extract from triager output: red flags, priority counts (P0/P1/P2), health metrics.

### 1b. Unreleased Changes

```bash
# Last announcement date: most recent Announcements discussion
gh api graphql -f query='query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    discussions(first: 1, categoryId: "{categories.Announcements}", orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes { createdAt title }
    }
  }
}' -f owner="{owner}" -f name="{repo}"
```

Then check what changed since:
```bash
git log --oneline --since="{last_announcement_date}"
```

Read `CHANGELOG.md` — any entries newer than the last announcement?

### 1c. Cadence Check

From strategy Section 4:
- Days since last announcement → monthly digest overdue if >30 days?
- Any pending architectural decisions that need RFC?

---

## Phase 2: Decision Matrix

Apply strategy Section 1 (Announcement vs Debate) to the gathered context:

| Condition | Priority | Action | Worker |
|-----------|----------|--------|--------|
| Red flags: unanswered discussions >7d | **P0** | Respond to unanswered items | → ln-914 |
| Red flags: PRs needing review | **P0** | List PRs needing review | Recommendations only |
| Unreleased changes in CHANGELOG | **P1** | Announce: new features/fixes | → ln-912 |
| `$ARGUMENTS` contains RFC/debate topic | **P1** | Debate: launch RFC | → ln-913 |
| Monthly digest overdue (>30d) | **P2** | Monthly digest announcement | → ln-912 |
| Design questions identified in Phase 1 | **P2** | Debate: RFC for open decisions | → ln-913 |
| Community health OK, nothing unreleased | **—** | Report "all clear" | No delegation |

### Output: Situation Report

Present to user:

```
## Community Status — {YYYY-MM-DD}

**Repo:** {owner}/{repo}
**Last announcement:** {date} ({days} days ago)
**Open items:** {issues} issues, {prs} PRs, {discussions} discussions

### Red Flags
{list or "None"}

### Recommended Action
{One of: Announce / Debate / Respond to items / No action needed}

**Reason:** {brief explanation based on strategy criteria}
```

**Wait for user approval before proceeding.**

---

## Phase 3: Delegate

After user approves the recommended action:

### Direct Delegation (when `$ARGUMENTS` specifies action)

| Argument | Delegation |
|----------|-----------|
| `announce` or `announce {topic}` | `Skill(skill: "ln-912-community-announcer", args: "{topic}")` |
| `debate` or `debate {topic}` | `Skill(skill: "ln-913-community-debater", args: "{topic}")` |
| `triage` or `triage {scope}` | `Skill(skill: "ln-911-github-triager", args: "{scope}")` |
| `respond` or `respond {#number}` | `Skill(skill: "ln-914-community-responder", args: "{#number or batch}")` |

### Analysis-Based Delegation

| Recommended action | Delegation |
|-------------------|-----------|
| Announce | `Skill(skill: "ln-912-community-announcer")` — worker gathers its own context |
| Debate | `Skill(skill: "ln-913-community-debater", args: "{identified topic}")` |
| Respond to items | `Skill(skill: "ln-914-community-responder", args: "batch")` |
| No action needed | Report status, done |

---

## Shared References

| File | Purpose |
|------|---------|
| `shared/references/community_github_discovery.md` | Phase 0: dynamic repo/category/user discovery |
| `shared/references/community_strategy_template.md` | Default engagement strategy (fallback) |
| `shared/references/community_discussion_formatting.md` | GitHub Discussion formatting rules |

---

## Strategy Override

Each target project can override the default strategy by creating `docs/community_engagement_strategy.md`. All skills check project-local first, then fall back to the template in `shared/references/`.

---

## Phase 4: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `planning-coordinator`. Run after Phase 3 completes. Output to chat using the `planning-coordinator` format.

---

**TodoWrite format (mandatory):**
```
- GitHub discovery (in_progress)
- Situation analysis (pending)
- Apply decision matrix (pending)
- Invoke ln-911-github-triager (pending)
- Invoke ln-912-community-announcer (pending)
- Invoke ln-913-community-debater (pending)
- Invoke ln-914-community-responder (pending)
- Report outcome to user (pending)
```

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|---------|
| 1 | ln-911-github-triager | Shared (Skill tool) — community health summary |
| 3 | ln-912-community-announcer | Shared (Skill tool) — feature/release announcements |
| 3 | ln-913-community-debater | Shared (Skill tool) — RFC / architectural debates |
| 3 | ln-914-community-responder | Shared (Skill tool) — respond to unanswered items |

**All workers:** Invoke via Skill tool — workers see coordinator context.

## Definition of Done

- [ ] GitHub discovery complete (owner/repo, categories, maintainer extracted)
- [ ] Situation analyzed (health + unreleased changes + cadence) OR direct delegation triggered
- [ ] Decision matrix applied with priority-based action selection
- [ ] Worker delegated or recommendations shown to user
- [ ] User informed of outcome

---

**Version:** 1.0.0
**Last Updated:** 2026-03-13
