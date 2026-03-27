---
name: ln-912-community-announcer
description: "Composes and publishes announcements to GitHub Discussions. Use when sharing releases, updates, or news with the community."
disable-model-invocation: true
license: MIT
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-912-community-announcer

**Type:** L3 Worker (standalone)
**Category:** 9XX Community Engagement
Composes and publishes structured announcements to GitHub Discussions (Announcements category).

---

## Phase 0: GitHub Discovery

**MANDATORY READ:** Load `shared/references/community_github_discovery.md`

Execute the discovery protocol. Extract:
- `{owner}/{repo}` for URLs and git commands
- `repo.id` for GraphQL mutation
- `categories["Announcements"]` category ID for publishing
- Verify Announcements category exists

Load strategy: check `docs/community_engagement_strategy.md` in target project, fallback to `shared/references/community_strategy_template.md`. Extract Section 2 (Announcement Triggers) and Section 6 (Tone Guide).

**MANDATORY READ:** Load `shared/references/community_discussion_formatting.md`
**MANDATORY READ:** Load [announcement_styles.md](references/announcement_styles.md)
**MANDATORY READ:** Load `shared/references/humanizer_checklist.md`

---

## Phase 1: Gather Context

1. Read strategy Section 2 -- verify this qualifies as an announcement
2. Read `CHANGELOG.md` -- extract the latest entry (or the entry matching `$ARGUMENTS` date if provided)
3. Read `README.md` -- check current version badge, any WARNING/IMPORTANT callouts
4. Run: `git log --oneline -20` -- recent commits for context
5. If `$ARGUMENTS` contains a topic keyword (not a date), use it as the announcement subject
6. Run: `git diff --name-only` (uncommitted) or `git diff --name-only HEAD~1..HEAD` (last commit) -- build the list of changed files
7. Read key source files from the diff (max 5 files, prioritize by relevance to `$ARGUMENTS` topic):
   - Protocol/guide files in diff -> read full (the substance)
   - SKILL.md files in diff -> read only changed sections via `git diff -- {file}`
   - Reference files -> read if substantially changed
   - Goal: understand the "why" behind changes that CHANGELOG doesn't spell out

---

## Phase 2: Classify and Select Style

### 2a. Classify Announcement Type

| Type | Trigger | Emoji |
|------|---------|-------|
| **Release** | New version in CHANGELOG | :rocket: |
| **Breaking Change** | WARNING callout in README or "breaking" in CHANGELOG | :warning: |
| **New Features** | New feature entries in CHANGELOG | :sparkles: |
| **Architecture** | Structural changes (new categories, plugin splits) | :building_construction: |
| **Community** | Non-technical updates (events, milestones) | :people_holding_hands: |

### 2b. Select Style

Use the **Style Selection Matrix** from `announcement_styles.md` to pick a primary style based on announcement type. Check the last 3 announcements in Discussions — if they all used the same style, pick a different one for variety.

Optionally mix: use a hook from one style with the body from another (see Mixing Styles table in `announcement_styles.md`).

---

## Phase 3: Compose Announcement

Use the selected style template from `announcement_styles.md` as the structural basis, and `discussion_formatting.md` for GitHub markdown syntax.

**Required elements (all styles):**
- Add `### Contributors` section after `### What's Next` — thank contributors by @mention if applicable (skip for solo work)
- Add footer: `*Full changelog: [CHANGELOG.md](https://github.com/{owner}/{repo}/blob/{default_branch}/CHANGELOG.md)*`
- If breaking change: include migration steps with clear before/after in an `> [!IMPORTANT]` alert
- End with engagement question (per Writing Quality checklist in `announcement_styles.md`)

---

## Phase 4: Fact-Check

Before presenting to user, verify every verifiable claim in the draft:

1. **Commands & code blocks** -- grep `README.md` for each command/snippet in the draft. If command not found -> replace with the actual command. Never invent install/update commands.
2. **File paths & links** -- verify each linked file exists: `ls {path}`. Remove or fix broken links.
3. **Numbers** -- verify counts mentioned against actual data: `git diff --name-only | grep -c SKILL.md` or `ls -d ln-*/SKILL.md | wc -l`.
4. **Feature descriptions** -- re-read the key source file (from Phase 1 step 7) and confirm the draft accurately describes what changed. No hallucinated capabilities.
5. **Names** -- verify names match actual directory/file names in the repo.

6. **Humanizer audit** -- run the audit protocol from `humanizer_checklist.md`. If 3+ AI patterns found, rewrite flagged sections.

**Gate:** If any check fails, fix the draft before proceeding.

---

## Phase 5: Review and Publish

Present the composed announcement title + body to the user. **Wait for explicit approval before publishing.**

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
      discussion { url }
    }
  }
' -f title="TITLE_HERE" -f body="BODY_HERE" -f repoId="{repo.id}" -f catId="{categories.Announcements}"
```

Report the discussion URL to the user.

**Note:** Pinning is not available via API -- remind the user to pin manually in GitHub UI if the announcement is important.

---

## Phase 6: Cross-Post (Optional)

If the announcement is a release or breaking change, suggest:
1. Create a matching GitHub Release if a version tag exists: `gh release create vX.Y.Z --notes "See discussion: URL"`
2. Update the repo description if the announcement changes the project scope

---

## Definition of Done

- [ ] Context gathered (CHANGELOG, README, git log, key source files)
- [ ] Announcement type classified + style selected (different from last 3)
- [ ] Draft composed using selected style template + formatting rules
- [ ] Writing quality checklist passed (announcement_styles.md)
- [ ] Fact-checked (commands, paths, numbers, descriptions, names verified)
- [ ] User approved final draft
- [ ] Published via GraphQL mutation, URL reported

---

**Version:** 1.0.0
**Last Updated:** 2026-03-13
