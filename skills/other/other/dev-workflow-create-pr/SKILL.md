---
name: dev-workflow-create-pr
description: Create a GitHub pull request using the gh CLI. Analyzes changes from base branch, generates a description following the PR template (jira or GitHub issue, what, why, who), and creates the PR if one doesn't exist. Use when the user asks to create a PR, open a pull request, or submit changes for review.
---

# Create Pull Request

Create a GitHub pull request with an auto-generated description that follows the PR template.

## Prerequisites

- GitHub CLI installed and authenticated (`gh auth status`)
- Changes committed and pushed to remote
- Current branch is not `main` or `master`

## Workflow

### Step 1: Check for Existing PR

```bash
gh pr view --json number,url 2>/dev/null
```

**If PR exists**: Report the existing PR URL and ask if the user wants to update the description.

### Step 2: Get Current Branch and Verify Remote

```bash
git branch --show-current
git status
```

**If branch is `main` or `master`**: STOP and warn the user.

**If changes are not pushed**: Push first:

```bash
git push -u origin HEAD
```

### Step 3: Determine Base Branch and Analyze Changes

The branch may have been created from `main` or from another feature branch. Determine the correct base branch:

```bash
# Option 1: Check git log for branch refs - other branch names appear in parentheses
# Example output: "8e6b394a (RNDCORE-12097) fix: update test"
# This indicates the branch was forked from RNDCORE-12097
git log --oneline --decorate HEAD | head -20

# Option 2: Check if there's an upstream tracking branch or PR target
gh pr view --json baseRefName --jq '.baseRefName' 2>/dev/null

# Option 3: Find the merge-base with main (may include unrelated commits if branch is stale)
git merge-base main HEAD
```

**Important:** Look for branch names in parentheses in the git log output. If you see a pattern like:

```
cd9c4c18 (HEAD -> RNDCORE-12097-suspense) refactor: migrate queries
8e6b394a (RNDCORE-12097) fix: update test
```

This means `RNDCORE-12097-suspense` was branched from `RNDCORE-12097`. The base branch is `RNDCORE-12097`, NOT main.

Once base branch is identified, run these commands:

```bash
# If parent branch is detected (e.g., RNDCORE-12097)
git diff PARENT_BRANCH..HEAD --stat
git log PARENT_BRANCH..HEAD --oneline
git diff PARENT_BRANCH..HEAD

# Example:
git diff RNDCORE-12097..HEAD --stat
```

**Fallback:** If no parent branch is detected in the log, use main:

```bash
git diff main...HEAD
git log main..HEAD --oneline
git diff main...HEAD --stat
```

### Step 4: Generate PR Description

Generate the PR description directly from the diff gathered in Step 3.

**4a. Extract ticket or issue** from the branch name:

- **Jira:** Pattern `[A-Z]+-\d+` (e.g. RNDCORE-12345, RETIRE-456). Link: RETIRE → `https://gustohq.atlassian.net/browse/TICKET`; else `https://internal.guideline.tools/jira/browse/TICKET`.
- **GitHub:** Pattern `issue-(\d+)` or leading `(\d+)-`. Link: `https://github.com/[owner]/[repo]/issues/N` (use current repo if not in branch).

If neither found, **ALWAYS use the AskQuestion tool:** Title "Ticket or Issue", options: Jira (specify), GitHub (specify URL or #N), Skip (placeholder). If skip: use `RND***-xxxx` for jira or omit issue line.

**4b. Analyze changes** from the diff — what changed, why, who it impacts.

**4c. Generate the `[[[...]]]` block.** Use **either** jira **or** issue (not both):

Jira:
```
[[[
**jira:** [TICKET-123](<jira-browse-url>)
**what:** concise summary of changes
**why:** business justification
**who:** affected users/teams
]]]
```

GitHub:
```
[[[
**issue:** [#N](https://github.com/owner/repo/issues/N)
**what:** concise summary of changes
**why:** business justification
**who:** affected users/teams
]]]
```

**Description rules:**

- Put `[[[` and `]]]` on their own lines
- Keep what/why/who concise (1-2 sentences each)
- Use backticks for code references (class names, methods, files)
- Only use bullet points for "what" if there are multiple distinct changes
- No indentation inside the block
- No agent preamble or headers outside the block

**Examples:**

Simple change (no bullets):

```
[[[
**jira:** [RNDCORE-11727](https://internal.guideline.tools/jira/browse/RNDCORE-11727)
**what:** Fix null pointer in `TenantTransferPacket#process` when user has no address
**why:** Users without addresses were causing 500 errors during transfer
**who:** Participants transferring accounts
]]]
```

Multiple changes (use bullets):

```
[[[
**jira:** [RNDCORE-11728](https://internal.guideline.tools/jira/browse/RNDCORE-11728)
**what:**
- Add `BillingCalculator` service to handle fee computations
- Update `Invoice#generate` to use new calculator
- Remove deprecated `LegacyBilling` module

**why:** Legacy billing code was unmaintainable and causing calculation errors
**who:** Internal billing team, sponsors receiving invoices
]]]
```

RETIRE branch:

```
[[[
**jira:** [RETIRE-456](https://gustohq.atlassian.net/browse/RETIRE-456)
**what:** Remove unused `OldAuthenticator` class and related specs
**why:** Dead code cleanup after migration to new auth system
**who:** No user impact, internal cleanup
]]]
```

### Step 5: Create the PR

The PR body must include the `[[[...]]]` block and a screenshot placeholder.

```bash
gh pr create --title "<type>: <short description>" --body "$(cat <<'EOF'
<[[[...]]] block from Step 4>

---

### Screenshot(s):
_No visual changes_

EOF
)"
```

**Title format:** Use conventional commit style based on the change type:

- `feat:` for new features
- `fix:` for bug fixes
- `refactor:` for code restructuring
- `chore:` for maintenance

### Step 6: Report Success

Get the PR URL and format it as a clickable markdown link:

```bash
PR_URL=$(gh pr view --json url --jq '.url')
```

Then output a message with the URL as a clickable markdown link:

```
PR created successfully! 🎉

[View PR #<number>]($PR_URL)
```

Example output: "PR created successfully! 🎉\n\n[View PR #2640](https://github.com/guideline-app/mobile-app/pull/2640)"

### Step 7: Offer to Start Review

After reporting the clickable PR URL, **ALWAYS use the AskQuestion tool:**

- Title: "Start PR Review?"
- Question: "Would you like me to review the PR for code quality, security, and best practices?"
- Options:
  - id: "review", label: "Yes, review it"
  - id: "done", label: "No, I'm done"

Based on the response:

- "review" → Use the `dev-workflow-review-pr` skill to perform a comprehensive code review
- "done" → End the workflow

## Checklist

```
PR Creation Progress:
- [ ] Verified no existing PR
- [ ] Confirmed changes are pushed
- [ ] Determined correct base branch (may not be main)
- [ ] Analyzed diff from base branch
- [ ] Generated PR description with [[[...]]] block
- [ ] Created PR with gh CLI
- [ ] Reported PR URL as clickable markdown link
- [ ] Offered to start PR review
```

## Edge Cases

### Branch has no Jira ticket or GitHub issue

Use `N/A`, or ask the user for the Jira key or GitHub issue (URL or #N).

### Branch created from another feature branch (not main)

When a branch is created from another feature branch:

1. Run `git log --oneline --decorate HEAD` and look for branch names in parentheses
2. If you see `(PARENT-BRANCH-NAME)` on a commit that isn't HEAD, that's the parent branch
3. Diff against that branch name directly

Example:

```bash
# Git log shows:
# cd9c4c18 (HEAD -> RNDCORE-12097-suspense) refactor: migrate queries
# 8e6b394a (RNDCORE-12097) fix: update test
#
# The parent branch is RNDCORE-12097

git diff RNDCORE-12097..HEAD --stat  # Shows only this branch's changes
git log RNDCORE-12097..HEAD --oneline  # Shows only this branch's commits
```

This ensures the PR description only reflects changes in THIS branch, not inherited changes from the parent branch.

### Large diff (>1000 lines)

Focus summary on high-level changes. Group by feature area or file type.

### No commits ahead of main

STOP - nothing to create a PR for. Inform the user.

### Branch is stale (main has diverged significantly)

The diff against main may include many unrelated changes. Identify the actual fork point:

```bash
git merge-base main HEAD
```

And consider if the branch needs to be rebased before creating the PR.

## Notes

- Always push changes before creating PR
- Review the generated description for accuracy before the PR is created
- For visual changes, remind the user to add screenshots after PR creation
