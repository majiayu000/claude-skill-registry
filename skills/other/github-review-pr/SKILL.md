---
name: github-review-pr
description: Review GitHub pull requests with detailed, multi-perspective code analysis using parallel subagents. Use this skill whenever the user wants to review a PR, asks for code review on a pull request, mentions "review PR", "check this PR", "look at pull request", or references a PR number or GitHub PR URL. Also trigger when the user wants feedback on code changes, wants to approve or request changes on a PR, or asks to review someone's contribution.
---

# Review GitHub Pull Request

A structured, multi-agent workflow for thorough code reviews on GitHub PRs. The approach uses parallel specialized reviewers, confidence scoring, and false positive filtering to produce high-signal, actionable feedback.

Use `gh` for all GitHub interactions. Do not use web fetch or attempt to build/typecheck the app — CI handles that separately.

## Workflow

### 1. Eligibility Check

Use a subagent to verify the PR is eligible for review. Skip the review if any of these are true:

- The PR is closed or merged
- The PR is a draft
- The PR doesn't need review (e.g., automated/bot PR, or trivially simple)
- You've already left a code review comment on it

If no PR number is provided, run `gh pr list` to show open PRs and ask which one to review.

### 2. Gather Context (parallel)

Launch two subagents in parallel:

**Subagent A — Project guidance discovery**: Find all relevant CLAUDE.md and AGENTS.md files — check the repo root and any directories whose files the PR modified. Return a list of file paths (not contents).

**Subagent B — PR summary**: View the PR with `gh pr view` and `gh pr diff`, then return a concise summary of what changed.

### 3. Parallel Code Review (5 specialized agents)

Launch 5 parallel subagents, each reviewing the PR from a different angle. Each agent should return a list of issues found, with a reason tag for why it was flagged (e.g., "CLAUDE.md adherence", "bug", "historical git context", "past PR feedback", "code comment violation").

| Agent | Focus | Approach |
|-------|-------|----------|
| **#1 CLAUDE.md / AGENTS.md compliance** | Check changes against project guidance | Read the CLAUDE.md and AGENTS.md files from step 2. Note that these files are guidance for AI agents as they write code, so not all instructions apply during code review. |
| **#2 Shallow bug scan** | Obvious bugs in the diff | Read only the changed lines (avoid extra context beyond the diff). Focus on significant bugs, not nitpicks. Ignore likely false positives. |
| **#3 Git history context** | Bugs visible through historical context | Read `git blame` and history of modified code. Identify issues that become apparent in light of how the code evolved. |
| **#4 Past PR feedback** | Recurring issues | Find previous PRs that touched these files. Check their comments for feedback that may also apply here. |
| **#5 Code comment compliance** | Respect inline guidance | Read code comments in modified files. Verify the PR changes comply with any guidance expressed in those comments. |

### 4. Confidence Scoring

For each issue found in step 3, launch a parallel subagent that receives the PR context, the issue description, and the CLAUDE.md/AGENTS.md file list. The subagent scores the issue on a 0-100 confidence scale:

| Score | Meaning |
|-------|---------|
| **0** | False positive that doesn't stand up to light scrutiny, or a pre-existing issue. |
| **25** | Might be real, but could be a false positive. Couldn't verify. If stylistic, not explicitly called out in CLAUDE.md or AGENTS.md. |
| **50** | Verified as real, but may be a nitpick or unlikely to hit in practice. Not very important relative to the rest of the PR. |
| **75** | Double-checked and very likely real. Will be hit in practice. The existing approach is insufficient. Important for functionality, or directly mentioned in CLAUDE.md/AGENTS.md. |
| **100** | Definitely real and confirmed. Will happen frequently. Evidence directly confirms the issue. |

For issues flagged due to CLAUDE.md/AGENTS.md instructions, the scoring agent should double-check that the relevant file actually calls out that issue specifically.

### 5. Filter

Discard any issues scoring below **80**. If no issues meet this threshold, skip to posting the "no issues found" comment.

### 6. Re-check Eligibility

Before posting, use a subagent to repeat the eligibility check from step 1. PRs can be closed or updated while the review runs.

### 7. Post Review Comment

Use `gh` to comment on the PR with findings. Follow these rules:

- Keep output brief
- No emojis
- Link and cite relevant code, files, and URLs
- You must provide the **full git SHA** in links (not `$(git rev-parse HEAD)` — the comment renders as Markdown)
- Provide at least 1 line of context before and after the issue line in link ranges

#### Comment format — issues found

```markdown
### Code review

Found 3 issues:

1. <brief description> (CLAUDE.md says "<quote>")

https://github.com/OWNER/REPO/blob/FULL_SHA/path/to/file.ts#L12-L16

2. <brief description> (AGENTS.md says "<quote>")

https://github.com/OWNER/REPO/blob/FULL_SHA/path/to/file.ts#L30-L35

3. <brief description> (bug due to <file and code snippet>)

https://github.com/OWNER/REPO/blob/FULL_SHA/path/to/file.ts#L50-L55

<sub>- If this code review was useful, please react with a thumbs up. Otherwise, react with a thumbs down.</sub>
```

#### Comment format — no issues found

```markdown
### Code review

No issues found. Checked for bugs, CLAUDE.md, and AGENTS.md compliance.
```

#### Link format

Links must follow this exact format for Markdown rendering to work:

```
https://github.com/OWNER/REPO/blob/FULL_SHA/path/to/file.ext#L[start]-L[end]
```

- Full 40-character git SHA (no shell expansion)
- Repo name must match the repo being reviewed
- `#` after the file name
- Line range as `L[start]-L[end]`
- Include at least 1 line of context before/after (e.g., commenting on lines 5-6 should link `L4-L7`)

## False Positive Examples

These should be filtered out during steps 3-5. Share this context with the review and scoring agents:

- Pre-existing issues (not introduced by this PR)
- Something that looks like a bug but isn't actually one
- Pedantic nitpicks a senior engineer wouldn't flag
- Issues a linter, typechecker, or compiler would catch (imports, types, formatting, test failures)
- General code quality concerns (test coverage, docs, broad security) unless explicitly required in CLAUDE.md or AGENTS.md
- Issues called out in CLAUDE.md/AGENTS.md but explicitly silenced in code (e.g., lint ignore comments)
- Intentional functionality changes directly related to the PR's purpose
- Real issues on lines the author did not modify

## gh Command Reference

```sh
# List open PRs
gh pr list

# View PR description and metadata
gh pr view 78

# View PR code changes
gh pr diff 78

# Get repo owner/name
gh repo view --json nameWithOwner --jq '.nameWithOwner'

# Get PR head commit SHA (full 40-char)
gh api repos/OWNER/REPO/pulls/78 --jq '.head.sha'

# Post a comment on the PR
gh pr comment 78 --body "### Code review ..."

# Post inline review comment on a specific file/line
gh api repos/OWNER/REPO/pulls/78/comments \
    --method POST \
    --field body="[your-comment]" \
    --field commit_id="[full-sha]" \
    --field path="path/to/file" \
    --field line=42 \
    --field side="RIGHT"
```
