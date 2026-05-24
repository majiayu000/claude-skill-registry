---
name: ln-914-community-responder
description: "Responds to unanswered GitHub discussions and issues with codebase-informed replies. Use when clearing community question backlog."
disable-model-invocation: true
license: MIT
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-914-community-responder

**Type:** L3 Worker (standalone)
**Category:** 9XX Community Engagement
Responds to unanswered GitHub Discussions and Issues by analyzing the question, searching the codebase for answers, and composing a helpful reply. Supports single-item and batch modes.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | `$ARGUMENTS`: discussion/issue number (`#42`), `batch` (all unanswered P1), or empty (interactive) |
| **Output** | Response comment(s) published to GitHub |
| **Pattern** | Read question → Search codebase → Compose response → Fact-check → Publish |

---

## Phase 0: GitHub Discovery

**MANDATORY READ:** Load `shared/references/community_github_discovery.md`

Execute the discovery protocol. Extract:
- `{owner}/{repo}` for URLs and API calls
- `repo.id` for GraphQL mutations
- `maintainer` login (authenticated user)
- Discussion category IDs

Load strategy: check `docs/community_engagement_strategy.md` in target project, fallback to `shared/references/community_strategy_template.md`. Extract Section 5 (Engagement Metrics) and Section 6 (Tone Guide).

**MANDATORY READ:** Load `shared/references/community_discussion_formatting.md`
**MANDATORY READ:** Load [response_styles.md](references/response_styles.md)
**MANDATORY READ:** Load `shared/references/humanizer_checklist.md`

---

## Phase 1: Load Items

### Single Item Mode

If `$ARGUMENTS` contains a number (e.g., `42`, `#42`):

```bash
# For discussions
gh api graphql -f query='query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    discussion(number: {N}) {
      id number title body
      category { name }
      author { login }
      createdAt
      answerChosenAt
      comments(first: 20) {
        totalCount
        nodes { author { login } body createdAt }
      }
    }
  }
}' -f owner="{owner}" -f name="{repo}"
```

```bash
# For issues (if discussion not found)
gh issue view {N} --repo {owner}/{repo} --json number,title,body,author,createdAt,comments,labels
```

### Batch Mode

If `$ARGUMENTS` is `batch`:

1. Fetch recent discussions + issues via GraphQL (last 30 days, open, sorted by created DESC)
2. Filter to P1 items: author != maintainer AND zero maintainer comments
3. Fetch full context for each item (max 10 per batch)

### Interactive Mode

If `$ARGUMENTS` is empty, list recent unanswered items and ask the user which to respond to.

---

## Phase 2: Analyze Context

For each item:

### 2a. Understand the Question

1. Read the discussion/issue body — identify the core question or problem
2. Read existing comments — check if partially answered or if follow-ups changed the scope
3. Detect item type: Q&A question, bug report, feature request, configuration help, general feedback

### 2b. Search Codebase for Answer

Based on the question type, search for relevant information:

| Question Type | Search Strategy |
|---------------|----------------|
| "How do I..." | Grep for keywords in SKILL.md files, README.md, docs/ |
| Bug report | Grep for mentioned function/file, check git log for recent fixes |
| Configuration | Read .hex-skills/environment_state.json, CLAUDE.md, relevant SKILL.md |
| Feature request | Check if feature already exists, grep for related patterns |
| Installation | Read README.md installation section, plugin.json |

```
FOR each item:
  1. Extract keywords from question (function names, skill names, error messages)
  2. Grep codebase for keywords (max 5 searches)
  3. Read relevant files (max 3 files, prioritize SKILL.md and docs/)
  4. Check git log for recent changes related to the topic
  5. If answer found → proceed to Phase 3
  6. If not found → mark as "needs-manual" and suggest the user respond directly
```

### 2c. Detect First-Time Poster

```bash
gh api graphql -f query='query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    discussions(first: 100) {
      nodes { author { login } }
    }
  }
}' -f owner="{owner}" -f name="{repo}"
```

Count how many discussions the author has created. If 0 previous (this is their first) → flag for Welcome style.

---

## Phase 3: Classify Response Type

**MANDATORY READ:** Load [response_styles.md](references/response_styles.md) — use the classification matrix.

| Item Type | Response Style |
|-----------|---------------|
| Q&A question with answer found | **Technical Answer** |
| Bug report | **Bug Acknowledgment** |
| Feature request / idea | **Feature Acknowledgment** |
| Question already answered elsewhere | **Redirect** |
| First-time poster (any type) | **Welcome** + appropriate content style |
| Stale item with progress update | **Status Update** |
| Cannot find answer in codebase | Mark `needs-manual` — skip composition |

---

## Phase 4: Compose Response

Use the selected style template from `response_styles.md`.

### Required Elements (All Styles)

- **Thank the author** — by name if possible, acknowledge their contribution
- **Answer the question** — direct, clear, linked to source code/docs
- **Invite follow-up** — "Let us know if this helps" or similar
- **No jargon without context** — explain internal terms
- **Link to code** — at least one link to relevant file in the repo

### Batch Mode Composition

In batch mode, compose all responses first, then present ALL for user review before publishing any.

---

## Phase 5: Fact-Check

Before presenting to user, verify every claim:

1. **File paths & links** — verify each linked file exists: `ls {path}`
2. **Code references** — verify mentioned functions/classes exist: `grep -r "{name}"`
3. **Feature descriptions** — re-read source file, confirm accuracy
4. **Install/usage commands** — verify against README.md

5. **Humanizer audit** -- run the audit protocol from `humanizer_checklist.md`. If 3+ AI patterns found, rewrite flagged sections.

**Gate:** If any check fails, fix the response before proceeding.

---

## Phase 6: Review and Publish

### Single Item Mode

Present the composed response to the user. **Wait for explicit approval before publishing.**

### Batch Mode

Present ALL responses in a summary table:

```
### Batch Responses — {N} items

| # | Type | Title | Style | Status |
|---|------|-------|-------|--------|
| {number} | {Discussion/Issue} | {title} | {Technical/Bug/Welcome/...} | Ready |
| {number} | ... | ... | ... | needs-manual |
```

Then show each response body. User can approve all, approve selectively, or edit individual responses.

### Publish Discussion Comment

```bash
gh api graphql -f query='
  mutation($discussionId: ID!, $body: String!) {
    addDiscussionComment(input: {
      discussionId: $discussionId,
      body: $body
    }) {
      comment { url }
    }
  }
' -f discussionId="{discussion.id}" -f body="{response body}"
```

### Publish Issue Comment

```bash
gh issue comment {number} --repo {owner}/{repo} --body "{response body}"
```

Report the comment URL(s) to the user.

---

## Rules

- **Always require user approval** before publishing any response
- **Never close** discussions or issues — only respond
- **Never mark as answered** — let the author do it (for Q&A discussions)
- **Batch limit:** max 10 items per batch (prevent context overload)
- **needs-manual items:** report to user with GitHub URL + reason, do not attempt response
- **Tone:** per strategy Section 6 — respectful, helpful, link to code

---

## Definition of Done

- [ ] Items loaded (single, batch, or interactive selection)
- [ ] Question context analyzed + codebase searched for answers
- [ ] Response type classified per response_styles.md
- [ ] First-time posters detected and welcomed
- [ ] Response(s) composed with links to relevant code/docs
- [ ] Fact-checked (file paths, code references, commands verified)
- [ ] User approved response(s)
- [ ] Published via GraphQL/CLI, comment URL(s) reported
- [ ] needs-manual items reported to user with URLs

---

**Version:** 1.0.0
**Last Updated:** 2026-03-14
