---
name: create-pr
description: Create a GitHub PR with verification and Codex review. Runs verify.sh and code/doc review before PR creation.
argument-hint: "[focus] [--skip-verify] [--skip-review] [--base BRANCH] [--title TITLE] [--draft]"
allowed-tools: Bash, Read, Glob, Grep
---

# Create PR

Create a GitHub pull request with verification and Codex review. Runs `.workstream/verify.sh` (if available), auto-generates title and body from commits, runs Codex review (code or doc), and includes findings in the PR description.

## When to Use

- You're ready to open a pull request for your branch
- You want cross-model review included in the PR automatically
- You want consistent PR formatting with auto-generated title/body

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status` works)
- On a feature branch with commits ahead of base branch
- Git working tree clean (all changes committed)

## Arguments

| Argument | Example | Description |
|----------|---------|-------------|
| `focus` | `security` | Focus Codex review on specific area |
| `--skip-verify` | | Skip verification (`.workstream/verify.sh`) |
| `--skip-review` | | Skip Codex review entirely |
| `--base BRANCH` | `--base develop` | Base branch for PR (default: repo default) |
| `--title TITLE` | `--title "Add auth"` | Override auto-generated title |
| `--draft` | | Create as draft PR |

Additional `gh pr create` flags are passed through.

## Workflow

Copy this checklist and track progress:

```
Create PR Progress:
- [ ] Step 1: Pre-flight checks
- [ ] Step 2: Run verification
- [ ] Step 3: Gather branch context
- [ ] Step 4: Auto-generate title and body
- [ ] Step 5: Run Codex review
- [ ] Step 6: Show preview and confirm
- [ ] Step 7: Create PR
```

## Step 1: Pre-flight Checks

### Check gh CLI

```bash
gh auth status
```

If not authenticated:
```
gh CLI is not authenticated.

Run: gh auth login
```

### Check Branch State

```bash
CURRENT_BRANCH=$(git branch --show-current)
```

If on `main` or `master`:
```
CREATE PR: ABORTED
===================
You are on the main branch. Create a feature branch first.
```

### Check Clean Working Tree

```bash
git status --porcelain
```

If dirty:
```
CREATE PR: WARNING
==================
You have uncommitted changes. Commit or stash them first.

Uncommitted files:
{list of files}
```

Use AskUserQuestion:
```
Question: "You have uncommitted changes. How would you like to proceed?"
Header: "Dirty tree"
Options:
  - Label: "Commit all changes"
    Description: "Stage and commit everything before creating PR (Recommended)"
  - Label: "Continue anyway"
    Description: "Create PR with current commits only"
  - Label: "Cancel"
    Description: "Stop and handle changes manually"
```

If "Commit all changes": stage all, commit with auto-generated message, then continue.
If "Cancel": stop.

### Check Commits Ahead

```bash
# Detect base branch
BASE_BRANCH="${BASE:-$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name' 2>/dev/null || echo 'main')}"

# Count commits ahead
COMMITS_AHEAD=$(git rev-list --count $BASE_BRANCH..HEAD 2>/dev/null || echo "0")
```

If 0 commits ahead:
```
CREATE PR: ABORTED
===================
No commits ahead of {base_branch}. Nothing to create a PR for.
```

### Push to Remote

```bash
# Check if remote tracking branch exists and is up to date
git rev-parse --abbrev-ref @{upstream} 2>/dev/null
UNPUSHED=$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "all")
```

If unpushed commits (or no upstream):
```bash
git push -u origin $CURRENT_BRANCH
```

## Step 2: Run Verification

**If `--skip-verify` is set:** Skip this step entirely, continue to Step 3.

### Check for Verification Script

```bash
[[ -f .workstream/verify.sh ]]
```

**If `.workstream/verify.sh` does not exist:**
- Skip verification silently
- Continue to Step 3

### Run Verification

```bash
bash .workstream/verify.sh
```

This runs the project's verification gate (typically: typecheck → lint → test → build).

### Handle Results

**If verification passes (exit code 0):**
```
VERIFICATION: PASSED
====================
All checks passed (typecheck, lint, test, build).
```
Continue to Step 3.

**If verification fails (non-zero exit code):**
```
VERIFICATION: FAILED
====================

{verification output showing failures}

Fix the issues above before creating a PR.
```

Use AskUserQuestion:
```
Question: "Verification failed. How would you like to proceed?"
Header: "Verify failed"
Options:
  - Label: "Fix issues first"
    Description: "Stop PR creation, address the failures (Recommended)"
  - Label: "Create PR anyway"
    Description: "Proceed despite verification failures"
  - Label: "Cancel"
    Description: "Abort PR creation"
```

If "Fix issues first": stop and show what needs fixing.
If "Create PR anyway": continue to Step 3 (note failure in PR body).
If "Cancel": stop.

## Step 3: Gather Branch Context

```bash
# Commits on this branch
git log --oneline $BASE_BRANCH..HEAD

# Full diff stat
git diff $BASE_BRANCH...HEAD --stat

# Changed files list (for review type detection)
git diff $BASE_BRANCH...HEAD --name-only
```

### Detect Review Type

Check changed files to determine whether to use `/codex-review` (code) or `/codex-consult` (docs):

```bash
# Get list of changed file extensions
git diff $BASE_BRANCH...HEAD --name-only
```

**Code file extensions:** `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.rb`, `.php`, `.swift`, `.kt`, `.c`, `.cpp`, `.h`, `.cs`, `.sh`, `.bash`, `.zsh`, `.sql`, `.graphql`, `.vue`, `.svelte`

**Doc file extensions:** `.md`, `.txt`, `.json`, `.yaml`, `.yml`, `.toml`, `.xml`, `.csv`, `.env`, `.conf`, `.cfg`, `.ini`

**Rules:**
- If ANY code files are in the diff: use `/codex-review`
- If ONLY doc/config files changed: use `/codex-consult`
- Default to `/codex-review` if unsure

## Step 4: Auto-generate Title and Body

### Title Generation

If `--title` not provided, generate from branch name and commit log:

1. Parse branch name: `feature/add-auth` -> `Add auth`
2. If branch name is unhelpful (e.g., `fix-123`), use the first commit subject
3. Keep under 70 characters

### Body Generation

Generate PR body from commit log:

```bash
# Get commit subjects and bodies
git log --format="- %s%n%n%b" $BASE_BRANCH..HEAD
```

Structure the body:

```markdown
## Summary
{2-4 bullet points summarizing the changes from commit messages}

## Changes
{For each commit:}
- {commit subject}

## Test plan
- [ ] {Inferred testing steps based on changes}
```

## Step 5: Run Codex Review

**If `--skip-review` is set:**
- Skip this step entirely
- Add to PR body: `**Codex Review:** SKIPPED (--skip-review)`
- Continue to Step 6

**If running inside Codex (CODEX_SANDBOX set):**
- Skip this step
- Add to PR body: `**Codex Review:** SKIPPED (running inside Codex)`
- Continue to Step 6

### Check Codex Availability

```bash
codex --version 2>/dev/null
```

**If Codex not available:**
- Skip review silently
- Add to PR body: `**Codex Review:** SKIPPED (Codex CLI not available)`
- Continue to Step 6

### Run Review

Based on review type detected in Step 2:

**For code changes:** Invoke `/codex-review` with the optional focus area.
The review runs against the current branch vs base branch.

**For doc-only changes:** Invoke `/codex-consult` on the diff content.

### Handle Results

Parse the Codex output for severity levels (see [EVALUATION_PRACTICES.md](../codex-review/EVALUATION_PRACTICES.md)):

**If critical issues found:**
```
CODEX REVIEW: CRITICAL ISSUES
==============================

{List of critical issues}

Critical issues must be addressed before creating the PR.
```

Use AskUserQuestion:
```
Question: "Codex found critical issues. How would you like to proceed?"
Header: "Critical"
Options:
  - Label: "Fix issues first"
    Description: "Stop PR creation, address the issues (Recommended)"
  - Label: "Create PR anyway"
    Description: "Proceed with critical issues noted in PR body"
  - Label: "Cancel"
    Description: "Abort PR creation"
```

If "Fix issues first": stop and list what needs fixing.
If "Create PR anyway": continue with issues in body.

**If no critical issues (pass or pass_with_notes):** Continue with findings in body.

### Format Findings for PR Body

Append a Codex Review section to the PR body:

```markdown
## Codex Review
**Status:** {PASS | PASS WITH NOTES | NEEDS ATTENTION}
**Model:** {model used}

{If recommendations:}
### Recommendations
{numbered list of recommendations}

{If positive findings:}
### Positive Findings
{bulleted list}
```

## Step 6: Show Preview and Confirm

Display the complete PR before creating:

```
PR PREVIEW
==========

Title: {title}
Base:  {base_branch} <- {current_branch}
Type:  {regular | draft}

Body:
---
{full PR body}
---
```

Use AskUserQuestion:
```
Question: "Create this PR?"
Header: "Confirm PR"
Options:
  - Label: "Yes, create PR"
    Description: "Create the pull request as shown (Recommended)"
  - Label: "Edit title"
    Description: "Change the PR title before creating"
  - Label: "Cancel"
    Description: "Abort PR creation"
```

If "Edit title": ask for new title via AskUserQuestion, then re-preview.
If "Cancel": stop.

## Step 7: Create PR

```bash
gh pr create --title "$TITLE" --body "$(cat <<'EOF'
{full PR body}

---
Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Add flags as needed:
- `--base $BASE_BRANCH` if non-default base
- `--draft` if draft mode requested

### Report Success

```
PR CREATED
==========

{PR URL from gh output}

Title: {title}
Base:  {base_branch} <- {current_branch}
Review: {PASS | PASS WITH NOTES | NEEDS ATTENTION | SKIPPED}
```

## Error Handling

| Failure | Action |
|---------|--------|
| `gh` not installed | Report and stop |
| `gh` not authenticated | Suggest `gh auth login` |
| Not on a feature branch | Report and stop |
| No commits ahead | Report and stop |
| Push fails | Report error and stop |
| Verification unavailable | Skip verification silently |
| Verification fails | Ask user (fix, continue, or cancel) |
| Codex unavailable | Skip review, note in PR body |
| Codex times out | Skip review, note in PR body |
| Codex critical issues | Ask user (fix, continue, or cancel) |
| `gh pr create` fails | Report error with full output |

## Configuration

Codex review uses existing configuration from `.claude/settings.local.json`:

```json
{
  "codexReview": {
    "enabled": true,
    "codeModel": "gpt-5.3-codex"
  },
  "codexConsult": {
    "enabled": true,
    "researchModel": "gpt-5.2"
  }
}
```

If both `codexReview.enabled` and `codexConsult.enabled` are `false`, Codex review is skipped entirely.

## Examples

**Basic PR:**
```
/create-pr
```

**Skip verification (e.g., for doc-only changes):**
```
/create-pr --skip-verify
```

**Skip Codex review:**
```
/create-pr --skip-review
```

**Skip both verification and review (fastest):**
```
/create-pr --skip-verify --skip-review
```

**Security-focused review with custom base:**
```
/create-pr security --base develop
```

**Draft PR with custom title:**
```
/create-pr --draft --title "WIP: Add authentication"
```
