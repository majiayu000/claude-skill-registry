---
name: oss-review-prs
description: |
  Review other contributors' PRs to learn the codebase and build maintainer trust.
  Guides structured diff reading, helps formulate review comments, and teaches
  how to distinguish blocking issues from nits. Use when you want to learn a
  codebase by reviewing PRs, build trust with maintainers before contributing code,
  or practice code review on OSS repos. Not for reviewing your own PR — use
  oss-submit-pr for that.
---

# Review PRs

Review other people's PRs to learn how the codebase evolves and earn maintainer trust. Thoughtful reviews are the fastest way from outsider to recognized contributor — maintainers notice reviewers who catch real issues.

## Purpose

Most contributors jump straight to writing code. But reviewing PRs teaches you things that reading source code doesn't: what maintainers care about, what patterns are enforced vs. aspirational, how the code changes over time, and what mistakes other contributors make. Regular reviewers build relationships with maintainers and earn trust that makes their own PRs get reviewed faster.

## When to Use

- You want to learn a codebase before contributing code
- You want to build trust with maintainers as a new contributor
- You've merged one PR and want to become a regular (see `oss-second-contribution`)
- You want to practice code review skills on real codebases
- **NOT** for reviewing your own PR before submission — use `oss-submit-pr` for self-review
- **NOT** if you don't understand the codebase at all — use `oss-explore-repo` first

## Prerequisites

- Repo explored enough to understand the general architecture (from `oss-explore-repo` or `oss-prep-to-contribute`)
- `gh` CLI authenticated
- Understanding of the language and frameworks used (or willingness to learn via `oss-learn-stack`)

## Process

### 1. Find PRs worth reviewing

Not every open PR needs your review. Pick ones where your review adds value.

```bash
# Open PRs, sorted by most recent
gh pr list -R {owner}/{repo} --state open --json number,title,author,labels,reviewDecision,createdAt,additions,deletions \
  --jq '.[] | "\(.number)\t\(.additions)+\(.deletions)\t\(.author.login)\t\(.title)"'

# PRs from first-time contributors (maintainers appreciate help reviewing these)
gh pr list -R {owner}/{repo} --state open --json number,title,author,authorAssociation \
  --jq '.[] | select(.authorAssociation == "FIRST_TIME_CONTRIBUTOR" or .authorAssociation == "FIRST_TIMER") | "\(.number)\t\(.author.login)\t\(.title)"'

# PRs without any reviews yet
gh pr list -R {owner}/{repo} --state open --json number,title,reviews \
  --jq '.[] | select(.reviews | length == 0) | "\(.number)\t\(.title)"'
```

**Good PRs to review**:
- From first-time contributors (maintainers need help with these)
- In areas you understand or want to learn
- Without existing reviews (your review adds the most value here)
- Small to medium size (under 500 lines) — you can review thoroughly

**PRs to skip**:
- Already has 3+ reviews — your review adds less value
- Draft PRs — the author isn't ready for feedback
- Massive refactors you don't understand — your review would be noise
- PRs from core maintainers with a clear LGTM — they don't need help

### 2. Read the PR description and linked issue

Before looking at any code, understand what the PR claims to do.

```bash
# Read the PR description
gh pr view {number} -R {owner}/{repo} --json title,body,labels,author,baseRefName,headRefName

# Read the linked issue (if any)
gh pr view {number} -R {owner}/{repo} --json body --jq '.body' | grep -oE '#[0-9]+' | head -5
# Then: gh issue view {issue-number} -R {owner}/{repo}
```

Before reading the diff, answer:
- What problem does this PR solve?
- What approach did the author take?
- What should the diff look like? (predict before you look)

### 3. Review the diff systematically

Read in this order — not top-to-bottom through the file list.

**Step 1: Tests first.** Tests tell you what the author thinks the code should do.

```bash
# Get the diff, filtered to test files
gh pr diff {number} -R {owner}/{repo} | grep -A 50 "^diff.*test\|^diff.*spec"
```

- What behaviors are tested?
- What edge cases are covered?
- What's NOT tested? (This is often the most valuable finding)

**Step 2: Implementation.** Now read the production code changes.

```bash
# Full diff
gh pr diff {number} -R {owner}/{repo}
```

Check for:
- Does the code do what the PR description says?
- Does it follow the repo's existing patterns?
- Are there error conditions not handled?
- Are there edge cases the tests don't cover?
- Is the scope right? (no unrelated changes sneaking in)

**Step 3: What's missing.** The hardest part of review — what SHOULD be in the diff but isn't.

- Related code that needs updating (callers, docs, types, configs)
- Missing test cases
- Migration or deployment concerns

### 4. Thinking gate — formulate your review

Before writing any comments, organize your findings:

> "What are the 2-3 most important things about this PR?
> 1. What's the biggest risk or potential issue you found?
> 2. Is there a missing test case or unhandled edge case?
> 3. Would you approve this if you were a maintainer? Why or why not?"

Wait for the user to articulate their assessment. If they say "it looks fine," push back: "What did the author change in {file}? What does the test at line N actually verify?"

### 5. Write review comments

Help the user draft comments that are helpful, specific, and appropriately scoped.

**Comment types** — label each one:

| Type | Prefix | When to use |
|------|--------|-------------|
| Blocking | `issue:` | Would cause a bug, security issue, or data loss |
| Suggestion | `suggestion:` | Better approach, but current code works |
| Nit | `nit:` | Style, naming, minor cleanup — not worth blocking |
| Question | `question:` | You're unsure and want to learn |
| Praise | (none) | Something clever or well-done — maintainers rarely hear this |

**Rules for good review comments**:
- Reference specific line numbers
- Explain WHY, not just WHAT — "this could cause X because Y"
- Suggest an alternative when pointing out problems
- Be direct — no hedging ("I think maybe perhaps this could potentially...")
- One thought per comment — don't write paragraphs

**What the LLM DOES**: Reviews the user's draft comments for tone, specificity, and accuracy. Points out if a comment is vague or could be misread.

**What the LLM DOES NOT DO**: Write comments for the user. The user must formulate their observations.

### 6. Submit the review

```bash
# Submit review with comments
gh pr review {number} -R {owner}/{repo} --comment --body "$(cat <<'EOF'
{user's review summary}
EOF
)"
```

**Use "Comment" — NOT "Approve" or "Request Changes."** You're not a maintainer. Even if you found blocking issues, use "Comment" and let the maintainer make the call.

Exception: If the repo explicitly invites community approvals (check CONTRIBUTING.md), then "Approve" is appropriate for clean PRs.

### 7. Thinking gate — reflect on what you learned

> "What did you learn about this codebase from reviewing this PR?
> 1. What patterns did the author follow? Were they consistent with the rest of the repo?
> 2. What would you do differently? (Not better — differently)
> 3. Did reviewing this PR change how you'd approach your own contribution?"

This reflection is what turns review from a chore into a learning activity.

## Related Skills

- **Preparation**: ← `oss-explore-repo` — understand the codebase before reviewing
- **Growth path**: ← `oss-second-contribution` — reviewing PRs is a key trust-building activity
- **Next contribution**: → `oss-find-issue` — after reviewing, you understand the codebase well enough to contribute
- **If knowledge gaps**: → `oss-learn-stack` — learn unfamiliar tech encountered in PRs

## Common Rationalizations

| Shortcut | Why It Fails |
|----------|-------------|
| "I'll just say 'LGTM' to build trust" | Rubber-stamp reviews are noise. Maintainers notice who actually reads the code. An "LGTM" from someone who hasn't contributed tells them nothing. |
| "I'll use 'Request Changes' to make my review count" | Using "Request Changes" as a non-maintainer is presumptuous. It blocks the PR and annoys the author. Use "Comment" — the maintainer decides what blocks. |
| "I'll review the massive 2000-line refactor" | You can't review 2000 lines effectively. Your comments will be surface-level. Pick small PRs where you can be thorough. |
| "I don't know enough to review" | You know enough to ask questions. A "question: why did you choose X over Y?" teaches you something and might surface an issue the author didn't consider. |
| "I'll skip the tests, they're boring" | Tests are the review's anchor. Without reading tests, you don't know what the author thinks the code should do, and you can't spot missing coverage. |

## Red Flags

- User submits "LGTM" without reading the diff — they're farming activity, not learning
- User writes comments about style only (variable naming, formatting) — they missed the substance
- User uses "Request Changes" on their first review — presumptuous for a non-maintainer
- Comments are vague ("this could be better") — not specific enough to be actionable
- User reviews PRs in repos they've never explored — they lack context to add value

## Verification Checklist

- [ ] PR chosen is in a codebase the user has explored or understands
- [ ] PR description and linked issue read before looking at the diff
- [ ] Tests reviewed first, then implementation, then checked for missing changes
- [ ] User articulated the 2-3 most important findings (step 4)
- [ ] Each comment is labeled (blocking/suggestion/nit/question) and references specific lines
- [ ] Review submitted as "Comment" not "Approve" or "Request Changes" (unless repo explicitly invites)
- [ ] User reflected on what they learned (step 7)

## Anti-patterns

- **DO NOT** write review comments for the user — they must formulate their own observations
- **DO NOT** submit empty "LGTM" reviews — every review must identify at least one substantive observation
- **DO NOT** use "Request Changes" unless the repo explicitly invites community-level approvals
- **DO NOT** review PRs in repos the user hasn't explored — context-free reviews add noise
- **DO NOT** focus only on style nits — substance (bugs, missing tests, logic errors) comes first
