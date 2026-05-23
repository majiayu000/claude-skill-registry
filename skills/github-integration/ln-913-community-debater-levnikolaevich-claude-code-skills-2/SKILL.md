---
name: ln-913-community-debater
description: "Launches RFC and debate discussions on GitHub. Use when proposing changes that need community input or voting."
disable-model-invocation: true
license: MIT
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-913-community-debater

**Type:** L3 Worker (standalone)
**Category:** 9XX Community Engagement
Launches structured debate discussions in GitHub Discussions for decisions that benefit from community input.

---

## Phase 0: GitHub Discovery

**MANDATORY READ:** Load `shared/references/community_github_discovery.md`

Execute the discovery protocol. Extract:
- `{owner}/{repo}` for URLs and codebase context
- `repo.id` for GraphQL mutation
- `categories["Ideas"]` for RFC/Proposal discussions
- `categories["Polls"]` for Prioritization polls
- Verify required categories exist

Load strategy: check `docs/community_engagement_strategy.md` in target project, fallback to `shared/references/community_strategy_template.md`. Extract Section 3 (Debate Triggers) and Section 1 (Decision Matrix).

**MANDATORY READ:** Load `shared/references/community_discussion_formatting.md`
**MANDATORY READ:** Load `shared/references/humanizer_checklist.md`

---

## Phase 1: Define the Topic

If `$ARGUMENTS` provided, use as the topic seed. Otherwise, ask the user what they want to debate.

Gather context:
1. Read strategy Section 3 -- verify this qualifies as a debate
2. Grep the codebase for files related to the topic
3. Read relevant SKILL.md files, docs, or shared references
4. Identify existing patterns that the proposal might change

---

## Phase 2: Classify Debate Type

| Type | Prefix | Category | When to use |
|------|--------|----------|-------------|
| **Maintainer RFC** -- design mostly done, seeking validation | `[RFC]` | Ideas | End of design process, soft announcement |
| **Community RFC** -- early stage, genuinely open to alternatives | `[RFC]` | Ideas | Beginning of design, kickstart discussion |
| **Proposal** -- new feature or restructuring | `[Proposal]` | Ideas | Concrete idea with use case |
| **Workflow Change** -- pipeline, task flow, or conventions | `[RFC]` | Ideas | Affects multiple areas or user workflows |
| **Prioritization** -- what to build next, feature ranking | `[Poll]` | Polls | Multiple options, need community vote |

If type is **Prioritization**, switch to Polls flow (Phase 4).

---

## Phase 3: Compose RFC Discussion

Use the **RFC Structure Pattern** from `discussion_formatting.md` (loaded in Phase 0).

**Skill-specific additions beyond the shared pattern:**
- Add `## Unresolved Details` section after Open Questions — implementation details not yet decided, to be resolved during development
- Add `## Decision Criteria` section — how the decision will be made (metrics, feedback threshold)
- Minimum 2 alternatives in the Alternatives table

---

## Phase 4: Compose Poll (for Prioritization type)

GitHub Discussions Polls are created via UI only. Instead, compose a reaction-based voting discussion:

```
## {Topic}

{1-2 sentence context}

**Vote by reacting to the options below** (each option is posted as a separate comment -- use :+1: to vote).

### Context
{Why this decision matters now}
```

After creating the discussion, post each option as a separate comment for reaction-based voting.

---

## Phase 5: Fact-Check

Before presenting to user, verify every verifiable claim in the draft:

1. **File paths & links** -- verify each linked file exists: `ls {path}`. Remove or fix broken links.
2. **Code references** -- verify mentioned functions/patterns exist: `grep -r "{name}"`.
3. **Alternatives accuracy** -- re-read source files to confirm the Alternatives table accurately describes tradeoffs. No hallucinated pros/cons.
4. **Names** -- verify skill names, directory names, config keys match actual repo state.
5. **Humanizer audit** -- run the audit protocol from `humanizer_checklist.md`. If 3+ AI patterns found, rewrite flagged sections.

**Gate:** If any check fails, fix the draft before proceeding.

---

## Phase 6: Review and Publish

Present the composed title + body to the user. **Wait for explicit approval before publishing.**

After approval, publish via GraphQL using discovery context:

```bash
gh api graphql -f query='
  mutation($title: String!, $body: String!, $repoId: ID!, $catId: ID!) {
    createDiscussion(input: {
      repositoryId: $repoId,
      categoryId: $catId,
      title: $title,
      body: $body
    }) {
      discussion { url id }
    }
  }
' -f title="TITLE_HERE" -f body="BODY_HERE" -f repoId="{repo.id}" -f catId="{categories.Ideas or categories.Polls}"
```

For **Polls**, after creating the discussion, post each option as a comment:

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
' -f discussionId="DISCUSSION_NODE_ID" -f body="**Option N:** {description}"
```

Report the discussion URL to the user.

---

## Rules

- Always present the full composed text for user approval before publishing
- Never publish without explicit user confirmation
- Title: descriptive, under 80 chars, prefixed with [RFC], [Proposal], or [Poll]
- Body: factual, not persuasive -- present options neutrally
- Include links to relevant code/docs in the repository
- Set a decision timeline when applicable
- Minimum 2 alternatives in the Alternatives table
- Tone: "We're considering X. Here are the tradeoffs. What's your take?"

---

## Definition of Done

- [ ] Topic defined with codebase context gathered
- [ ] Debate type classified (RFC/Proposal/Workflow/Prioritization)
- [ ] RFC or poll composed with minimum 2 alternatives
- [ ] Fact-checked (links, code references, alternatives accuracy, names)
- [ ] Humanizer audit passed (< 3 AI patterns)
- [ ] User approved final draft
- [ ] Published via GraphQL mutation, URL reported

---

**Version:** 1.0.0
**Last Updated:** 2026-03-13
