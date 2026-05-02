---
name: oss-find-issue
description: |
  Find unclaimed open source issues that match the user's skills and experience level.
  Searches for issues created by maintainers/org admins, checks contribution eligibility,
  and ranks by learning value. Use when looking for an issue to contribute to, starting
  OSS contributions, or finding GSoC-friendly issues.
---

# Find Issue

Find a real, unclaimed issue that matches your skills - from repos that actually want your contribution. This skill does the research; you decide what's worth your time.

## Purpose

Not every issue is worth picking up. Random issues filed by drive-by users often get closed without merging. Issues from maintainers and org members are the ones that get reviewed and merged. This skill finds those, checks if the repo accepts outside contributions, and matches issues to what you actually know - so you don't waste weeks on something that gets rejected or ignored.

## Prerequisites

- A GitHub account with `gh` CLI authenticated
- A target repo or area of interest (language, framework, domain)

## Process

### 1. Understand the contributor

Before searching for anything, understand who's contributing. Ask the user:

- "What languages and frameworks are you comfortable with?"
- "What's your experience level? (first contribution / a few PRs merged / experienced contributor)"
- "Any specific repos or domains you're interested in? (web, CLI tools, data, infra, etc.)"

Do NOT skip this. Issue matching without knowing the contributor is useless.

### 2. Check contribution eligibility

Before looking at a single issue, verify the repo accepts outside contributions:

```bash
# Fetch contribution guidelines
gh api repos/{owner}/{repo}/contents/CONTRIBUTING.md --jq '.content' | base64 -d 2>/dev/null
gh api repos/{owner}/{repo}/contents/.github/CONTRIBUTING.md --jq '.content' | base64 -d 2>/dev/null
gh api repos/{owner}/{repo}/contents/CODE_OF_CONDUCT.md --jq '.content' | base64 -d 2>/dev/null
```

Check for:
- **Explicit "we welcome contributions"** - if absent, that's a yellow flag
- **CLA requirements** - some orgs require signing a Contributor License Agreement before any PR
- **"Internal only" signals** - some repos state contributions are restricted to org members
- **Stale contribution docs** - if CONTRIBUTING.md references tools/processes from 3+ years ago, the repo may not be actively maintained
- **Recent external PRs merged** - strongest signal that outside contributions are welcome

```bash
# Check if external PRs actually get merged
gh pr list -R {owner}/{repo} --state merged --limit 20 --json author,mergedAt,authorAssociation | \
  jq '[.[] | select(.authorAssociation != "MEMBER" and .authorAssociation != "OWNER")]'
```

If the repo doesn't accept outside contributions, **tell the user immediately** and suggest alternatives. Don't waste their time.

### 3. Identify maintainers and core contributors

Issues filed by maintainers carry more weight - they represent actual project priorities.

```bash
# Get repo collaborators and recent committers
gh api repos/{owner}/{repo}/contributors --jq '.[0:10] | .[].login'

# Check issue author association
gh issue list -R {owner}/{repo} --state open --json number,title,author,labels,assignees,authorAssociation,createdAt --limit 50
```

Filter for issues where `authorAssociation` is `OWNER`, `MEMBER`, or `COLLABORATOR`. These are the issues maintainers actually care about.

### 4. Search for matching issues

```bash
# Good first issues from maintainers
gh issue list -R {owner}/{repo} --label "good first issue" --state open \
  --json number,title,labels,assignees,comments,createdAt,authorAssociation,author

# Help wanted
gh issue list -R {owner}/{repo} --label "help wanted" --state open \
  --json number,title,labels,assignees,comments,createdAt,authorAssociation,author

# GSoC-specific (if applicable)
gh issue list -R {owner}/{repo} --label "gsoc" --state open \
  --json number,title,labels,assignees,comments,createdAt,authorAssociation,author
```

For each candidate issue, verify:

```bash
# Read full issue with comments
gh issue view {number} -R {owner}/{repo} --json body,comments,assignees,labels,author,authorAssociation,createdAt,updatedAt

# Check for linked PRs (someone might already be working on it)
gh pr list -R {owner}/{repo} --search "#{number}" --state open --json number,title,author
```

### 5. Filter and rank

**Must-have filters** (skip issue if any fail):
- No assignee AND no "I'll take this" / "working on this" in recent comments
- No open PR linked to this issue
- Created or updated within last 6 months
- Clearly scoped - you can describe what needs to change in 2 sentences
- Filed by maintainer/member/collaborator (or explicitly endorsed by one in comments)

**Ranking criteria**:

| Criteria | Weight | What to check |
|----------|--------|---------------|
| Skill match | High | Does the issue require languages/frameworks the user knows? |
| Learning value | High | Will the user learn something non-trivial? |
| Clear scope | High | Is the expected outcome well-defined? |
| Maintainer engagement | Medium | Has a maintainer commented or labeled recently? |
| Impact | Medium | Does this affect real users or is it cosmetic? |
| Complexity fit | Medium | Not trivial (typo fix) but not overwhelming (full rewrite) |

### 6. Present recommendations

For each of the top 3 issues, present:

```
### #{number} - {title}
- **Filed by**: {author} ({authorAssociation})
- **Why this issue**: {one sentence - what makes it a good pick for THIS user}
- **What it involves**: {what needs to change, in plain language}
- **Skills exercised**: {what the user will learn/practice}
- **Complexity**: {low / medium / high - relative to user's stated experience}
- **Maintainer activity**: {last maintainer comment date, engagement level}
- **Link**: {url}
```

### 7. Thinking gate - user decides

**Do NOT let the user just say "number 1."** Ask:

> "Before you pick one - tell me:
> 1. Why does this issue interest you? (What about it matches your skills from step 1?)
> 2. What do you think the fix might involve? (Look at the 'What it involves' section above - does that match what you'd expect?)
> 3. Is the complexity right for you? (Not so easy you learn nothing, not so hard you get stuck for weeks)"

If the user can't articulate why, that's a signal to dig deeper or suggest a different issue.

### 8. Claim the issue

Once the user has chosen AND explained their reasoning:

**Check the repo's assignment workflow first.** Some repos require maintainer assignment rather than self-claiming. Look for:
- "Please request to be assigned" in CONTRIBUTING.md or issue templates
- Issues with an `assignees` field in their template YAML frontmatter
- Repos where maintainers assign work (check recent closed issues for the pattern)

If the repo uses **assignment-based workflow**:

```bash
gh issue comment {number} -R {owner}/{repo} --body "I'd like to be assigned to this issue."
```

If the repo allows **self-claiming**:

```bash
gh issue comment {number} -R {owner}/{repo} --body "I'd like to work on this issue. I'll submit a PR within [user-specified timeframe]."
```

**Keep the claim comment short.** One sentence is enough. Don't write a paragraph about your background, your approach, or how excited you are. Maintainers see dozens of these - concise signals competence.

## Related Skills

- **Next step**: → `oss-prep-to-contribute` - prepare to actually contribute (set up dev env, understand codebase, knowledge check)
- **Preparation**: → `oss-explore-repo` - explore the codebase broadly before committing to a specific issue
- **Alternative**: → `oss-find-real-issues` - if no existing issues match, find real code problems to file as new issues

## Anti-patterns

- **DO NOT** pick issues just because they look easy - pick ones that match skills AND teach something
- **DO NOT** skip the eligibility check - getting a PR rejected because the org doesn't accept outside contributions is demoralizing
- **DO NOT** claim multiple issues at once - claim one, ship it, then claim the next
- **DO NOT** present issues from random users as equal to maintainer-filed issues - they're not
