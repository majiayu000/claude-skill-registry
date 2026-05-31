---
name: contributor
description: "End-to-end open source contribution workflow: from scanning issues to submitting PRs. Use this skill whenever the user wants to contribute to an open source project, find issues to fix, submit a pull request, fork a repo to contribute, fix a GitHub issue, or mentions 'open source contribution'. Also trigger when they provide a GitHub repo URL and ask about contributing, say things like 'help me submit a PR', 'find good first issues', 'I want to contribute to X', or mention fixing bugs in someone else's project."
---

# Contributor

Automated open source contribution workflow that takes you from a GitHub repo URL to merged PRs, with built-in safeguards against common contribution failures.

## Why this skill exists

Open source contributions fail for predictable reasons: fixing in the wrong layer (your PR gets closed because the maintainer preferred an upstream fix), colliding with other contributors, not following project conventions, or over-engineering a simple fix. This workflow prevents each of those failures through systematic pre-checks.

## Phase 1: Reconnaissance

Before writing any code, gather intelligence about the project and its contribution landscape.

### 1.1 Identify the target

Ask the user for:
- The GitHub repo URL (e.g., `pydantic/pydantic-ai`)
- Their GitHub username and email for commits
- Any specific issue they want to work on (or ask to scan for available ones)

### 1.2 Scan for available issues

Use `gh` CLI to find issues worth contributing to:

```bash
# Get open issues with metadata
gh issue list -R <owner>/<repo> --state open --limit 50 \
  --json number,title,labels,assignees,comments

# Check for competing PRs on each candidate
gh pr list -R <owner>/<repo> --state open \
  --search "<issue_number> in:title,body"
```

**Filter criteria** (apply in order):
1. No assignee
2. No open PR already fixing it (check both linked PRs and title/body search)
3. Fewer than 5 competing PRs
4. Prefer labels: `bug`, `good first issue`, `help wanted`
5. Prefer issues with maintainer comments suggesting a fix direction

### 1.3 Deep-read issue comments

For each candidate issue, read the full comment thread:

```bash
gh issue view <number> -R <owner>/<repo> --json body,comments
```

Extract:
- **Maintainer fix direction**: Do they prefer fixing here or in an upstream dependency?
- **Suggested approach**: Any code pointers, file references, or architectural guidance?
- **Blockers**: Is this waiting on another PR or release?
- **Who's working on it**: Even without assignment, someone might have commented "I'll take this"

### 1.4 Check for upstream redirection

This is the single most common failure mode. Before committing to any fix:

```bash
# Check if maintainers reference another repo
gh issue view <number> -R <owner>/<repo> --json comments \
  | grep -i "upstream\|genai-prices\|separate repo\|other repo"

# Check related repos for recent PRs mentioning this issue
gh pr list -R <owner>/<related-repo> --state open --limit 10 \
  --json title,body | grep -i "<issue_number>\|<issue_keywords>"
```

If there's any signal the fix belongs elsewhere, stop and ask the user before proceeding.

## Phase 2: Pre-communication

Never submit a PR cold. Always communicate your intent first.

### 2.1 Post a solution outline on the issue

Before writing code, leave a comment on the issue with your proposed approach. This serves two purposes: it claims the work (politely), and it gives maintainers a chance to redirect you before you waste effort.

**Template:**
```
Hi, I've been looking into this and traced the root cause to <X>.

Before I open a PR, I wanted to confirm the preferred approach:
A) <approach A — e.g., fix in this repo by modifying X>
B) <approach B — e.g., upstream fix in related-repo>

I can implement either direction. Happy to adjust based on your preference.
```

Wait for maintainer response before proceeding to code. If no response after 24-48 hours on an active project, proceed with the most conservative approach (smallest scope fix in the current repo).

### 2.2 Draft PR strategy

Plan to open as a Draft PR first. Convert to ready-for-review only after:
- CI passes
- Maintainer acknowledges the approach (via issue comment or PR review)

## Phase 3: Repository Setup

### 3.1 Fork and clone

```bash
gh repo fork <owner>/<repo> --clone --remote
cd <repo>
```

### 3.2 Determine the development branch

Don't assume `main`. Check what recent merged PRs target:

```bash
gh pr list -R <owner>/<repo> --state merged --limit 10 \
  --json baseRefName,mergedAt
```

Use the most common `baseRefName` from recent merges.

### 3.3 Read contribution guidelines

Check these files in order (read whichever exist):

```
CONTRIBUTING.md
.github/CONTRIBUTING.md
.github/PULL_REQUEST_TEMPLATE.md
.github/PULL_REQUEST_TEMPLATE/
```

Extract:
- Required commit message format
- Test requirements
- Pre-commit hooks or linting requirements
- DCO/CLA requirements
- Branch naming conventions

### 3.4 Understand CI

```bash
ls .github/workflows/
```

Read the CI config to know what checks will run on your PR. Identify the commands for:
- Linting / formatting
- Type checking
- Unit tests
- Integration tests
- Pre-commit hooks

### 3.5 Set up the environment

Follow the project's documented setup process. Run the full test suite once to establish a passing baseline before making any changes.

## Phase 4: Code Fix

### 4.1 Branch per issue

```bash
git checkout -b fix/issue-<number>-<short-desc> <base-branch>
```

### 4.2 Implementation principles

- **Adopt the maintainer's suggested approach** if one exists in the issue comments
- **Minimal fix**: change only what's necessary to fix the issue. Don't refactor surrounding code, add features, or "improve" things along the way
- **Match project style**: follow the existing code patterns, naming conventions, and architecture
- **No hardcoding**: avoid hardcoded values unless the project already uses them in the same context
- **Add tests**: every fix needs a corresponding test that would have caught the bug. Follow the project's existing test patterns

### 4.3 Test your changes

Run the project's test suite. All existing tests must pass. Your new test must also pass. If the project has type checking or linting, run those too.

Language-specific verification:
- **Python**: `pytest`, `mypy`, `ruff` (or whatever the project uses)
- **TypeScript**: `npx tsc --noEmit`, project test command
- **Rust**: `cargo check && cargo test`
- **Go**: `go build ./... && go test ./...`

## Phase 5: Commit and Submit

### 5.1 Pre-commit checks

If the project uses pre-commit hooks:
```bash
pre-commit run --all-files
```

Fix any issues before committing.

### 5.2 Commit conventions

```bash
# Configure author
git config user.name "<user's name>"
git config user.email "<user's email>"

# Commit with DCO sign-off
git commit -s -m "<type>: <description>

Fixes #<issue-number>"
```

Rules:
- Follow the project's commit message format (check recent commits for examples)
- Include `Fixes #<number>` or `Closes #<number>` to auto-link
- No `Generated by Claude`, `Co-Authored-By: claude`, or any AI attribution
- Use rebase to keep history clean, never force push

### 5.3 Push and create PR

```bash
git push -u origin fix/issue-<number>-<short-desc>
```

Create a Draft PR following the project's template:

```bash
gh pr create --draft --title "<type>: <short description>" \
  --body "$(cat <<'EOF'
## Summary
<1-2 sentences describing the fix>

Fixes #<issue-number>

## Changes
- <bullet points of what changed>

## Test plan
- <how this was tested>
EOF
)"
```

### 5.4 Handle CI results

- **CI passes**: Comment on PR that it's ready for review, convert from draft
- **CI fails due to your code**: Fix it, push new commit, don't amend
- **CI fails due to infrastructure** (network timeouts, flaky tests, service outages): Comment explaining the failure is unrelated to your changes and request a rerun

## Phase 6: After Submission

### 6.1 If PR is closed without merge

Don't panic. Common reasons and responses:

| Reason | Response |
|--------|----------|
| Fix moved upstream | Ask to contribute to the upstream repo instead |
| Approach rejected | Ask what approach they'd prefer, offer to redo |
| Duplicate | Acknowledge, offer to help review the other PR |
| Scope too large | Offer to split into smaller PRs |

**Template for closed PRs:**
```
Thanks for the feedback. I understand the fix direction has shifted to <X>.
Would it be helpful if I submitted a PR to <upstream-repo> instead?
Happy to contribute wherever it's most useful.
```

### 6.2 If changes are requested

Address review feedback promptly. Make each revision a new commit (don't squash during review — the maintainer may want to see the evolution). Only squash if the maintainer asks.

## Anti-patterns to avoid

These are real failure modes from production contributions:

1. **Fixing in the wrong layer**: You fix in repo A, but the maintainer creates a PR in repo B minutes before closing yours. Prevention: Phase 1.4 upstream check + Phase 2 pre-communication.

2. **PR pile-up**: 5 people submit PRs for the same issue. Prevention: Phase 1.2 competing PR check + Phase 2 claiming the work.

3. **Over-engineering**: Adding error handling, type annotations, refactoring, or "improvements" beyond the fix. Prevention: Phase 4.2 minimal fix principle.

4. **CI infrastructure confusion**: A flaky test or network timeout in CI gets mistaken for a code problem. Prevention: Phase 5.4 explicit CI failure triage.

5. **Silent submission**: Submitting a PR without any prior communication on the issue. Prevention: Phase 2 pre-communication is mandatory.

6. **Wrong base branch**: PRing against `main` when the project develops on `dev`. Prevention: Phase 3.2 branch detection.
