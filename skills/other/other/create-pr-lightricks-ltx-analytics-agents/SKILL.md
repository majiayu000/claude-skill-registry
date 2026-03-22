---
name: create-pr
description: This skill should be used when the user asks to "create a PR", "open a pull request", "ship it", "submit for review", "push and create PR", or wants to finalize changes into a pull request with Linear integration, Copilot review, and Slack notification.
---

# Create PR Workflow

Follow these steps in order. If a step fails, inform the user and stop unless noted otherwise.

## Step 1: Branch and Base Branch Detection

Detect the current branch and the repository's default base branch:

```bash
git branch --show-current
git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p'
```

- If the base branch detection fails, fall back to checking which of `main` or `master` exists on the remote.
- If currently on the base branch, ask the user what this PR is about and which Linear ticket it relates to (or none). Then create a branch named `{git-username}/{TICKET-ID}-short-description` if a ticket is provided (e.g., `dgang/CPDO-123-add-auth-flow`), or `{git-username}/short-description` if no ticket (e.g., `dgang/add-auth-flow`). Remember the ticket for Step 4.

## Step 2: Rebase on Latest Base Branch

Before rebasing, check for uncommitted changes using `git status --porcelain`.

If the working tree is dirty, stash before rebasing:

```bash
git stash push --include-untracked -m "create-pr-autostash"
```

If the working tree is clean, skip stashing entirely.

Then fetch and rebase:

```bash
git fetch origin
git rebase origin/{base-branch}
```

If rebase conflicts occur, stop immediately. Inform the user and let them resolve manually. Do NOT force-resolve or abort the rebase.

After a successful rebase, pop the stash **only if you stashed earlier**. If you did not stash, do NOT run `git stash pop` — it could apply an unrelated stash. If stash pop produces conflicts, stop and inform the user.

## Step 3: Squash and Clean Up Commits

Check how many commits exist on the branch ahead of the base branch:

```bash
git log origin/{base-branch}..HEAD --oneline
```

**If 0 commits:** Skip this step (nothing to squash).

**If 1 commit:** Skip this step (nothing to squash). The existing commit message will be reviewed during Step 6 (Stage and Commit) if needed.

**If 2+ commits:** Analyze all commit messages and the combined diff to decide how to proceed.

### Classifying commits

Read all commit messages and the full diff (`git diff origin/{base-branch}..HEAD`). Classify each commit message as either **meaningful** or **noise**.

**Noise** commits are those that don't describe a distinct, intentional unit of work. Examples:
- Generic fixups: `fix`, `fixes`, `fix typo`, `small fix`, `quick fix`
- Work-in-progress: `wip`, `continue`, `continue work`, `more work`, `progress`
- Gibberish or placeholders: `aaa`, `bbb`, `ccc`, `kuku`, `test`, `asdf`, `tmp`
- Iteration markers: `round`, `round 2`, `another round`, `try again`, `retry`
- Vague one-worders: `update`, `changes`, `stuff`, `done`, `ok`
- Repeated or near-duplicate messages of another commit **with the same or overlapping changes** (if multiple commits share the same meaningful message but each introduces different, non-overlapping work, treat them as meaningful)

**Meaningful** commits describe a distinct piece of work that someone would reasonably want as a separate commit in the final repo. Examples:
- `feat: add claude.md configuration`
- `fix: handle null pointer in auth middleware`
- `refactor: extract validation into shared module`
- `add terraform handling of cloudflare rate limit`

### Decision logic

**Auto-squash (no user prompt):** If there is only one meaningful commit message (or zero — all noise), squash everything into a single commit. Craft the commit message by analyzing the full diff and incorporating any useful context from the meaningful message. Briefly inform the user what you did (e.g., "Squashed 5 commits into one").

**Ask the user:** If there are 2+ semantically distinct meaningful commits, present them to the user and ask:
- **Option A: Squash all into one commit** — combine everything into a single well-crafted commit message.
- **Option B: Keep separate** — consolidate noise into their nearest meaningful commit, resulting in N clean commits.

### How to squash

Before rewriting any history, ensure the working tree is clean. If there are uncommitted changes (e.g., from a stash pop in Step 2), stash them first:

```bash
git stash push --include-untracked -m "create-pr-pre-squash"
```

Then create a backup branch as a safety net:

```bash
git branch {current-branch}-backup-$(date +%s)
```

If anything goes wrong during the rewrite, the backup branch preserves the original state. After your Step 7 push succeeds, clean up the backup branch: `git branch -D {backup-branch-name}`.

**For full squash (all into one commit):**

```bash
git reset --soft origin/{base-branch}
git commit -m "$(cat <<'EOF'
feat: short summary of the change

Detailed body explaining what changed and why.

CPDO-123
EOF
)"
```

**For partial consolidation (keep N meaningful commits):**

Use a non-interactive, cherry-pick-based approach (since this skill is executed by an AI agent, not a human with an editor):

1. Identify the N meaningful commits and group surrounding noise commits with their nearest meaningful commit. Record these as ordered groups of SHAs.
2. Create a replay branch from the base:
   ```bash
   git checkout -b {current-branch}-replay origin/{base-branch}
   ```
3. For each group in order, apply the commits without committing and then create a single clean commit:
   ```bash
   git cherry-pick -n {sha1} {sha2} ...   # apply group without committing
   git commit -m "{clean message}"          # using HEREDOC pattern above
   ```
4. Replace the original branch with the replay (the backup branch from earlier preserves the original state):
   ```bash
   git checkout {current-branch}
   git reset --hard {current-branch}-replay
   git branch -D {current-branch}-replay
   ```

The result should be N clean commits, each with a good message, with all noise commits absorbed into the meaningful commit they followed.

**Fallback:** If cherry-pick produces conflicts that cannot be resolved automatically (e.g., heavily interleaved changes across the same files), abort the replay, switch back to the original branch, and fall back to a full squash into one commit. Inform the user why.

```bash
git cherry-pick --abort
git checkout {current-branch}
git reset --hard {backup-branch-name}   # restore from the exact backup branch created earlier
git branch -D {current-branch}-replay   # clean up failed replay
```

After any successful rewrite (squash or consolidation), pop the pre-squash stash if one was created. If there was no stash, do not pop.

### Crafting the squashed message

- Use conventional commits format (`feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `test:`)
- Base the message on the **actual diff**, not just the old commit messages
- Incorporate substance from any meaningful commit messages
- If a Linear ticket ID is visible in the branch name (e.g., `CPDO-123`), include it on its own line at the end of the commit message body (matching the format in Step 6). Otherwise, if a ticket is detected later (Step 4), amend the commit to add it in the same format
- The message should read as if a thoughtful developer wrote it in one shot

## Step 4: Linear Ticket Detection

Determine the associated Linear ticket:

1. Check the branch name for a pattern matching `[A-Z]+-\d+` (e.g., `CPDO-123`, `MLPD-456`).
2. If not found in the branch name, check recent commit messages for the same pattern.
3. If still not found, ask the user which Linear ticket this relates to, or whether there is none.

If a ticket ID is found, fetch its details using `mcp__linear__get_issue` to get the title and context. This context informs the PR title, body, and commit message.

## Step 5: Check for Changes

Check for uncommitted changes and unpushed commits:

```bash
git status
git diff HEAD
git log origin/{base-branch}..HEAD --oneline
```

- If there are no uncommitted changes AND `git log origin/{base-branch}..HEAD` shows no commits, inform the user there is nothing to submit and stop.
- If `git log origin/{base-branch}..HEAD` shows at least one commit and there are no additional uncommitted changes, skip Step 6 and proceed directly to Step 7 (push).

## Step 6: Stage and Commit

This step handles any remaining uncommitted changes that were not already included in the squash (Step 3).

If Step 3 already produced a clean squashed commit and there are no additional changes, skip this step.

Otherwise, review changes with `git status` and `git diff HEAD`.

Compose a commit message using conventional commits format:

- `feat:` — new feature or capability
- `fix:` — bug fix
- `chore:` — maintenance, config, dependency updates
- `refactor:` — code restructuring without behavior change
- `docs:` — documentation only
- `test:` — adding or updating tests

If a Linear ticket is associated, include the ticket ID on its own line at the end of the commit message body. Example:

```
feat: add OAuth2 authentication flow

Implement login with JWT token refresh and session management.

CPDO-123
```

Stage relevant files. Avoid staging `.env`, credentials, secrets, or large binaries. Create the commit.

**Note:** Only if Step 3 resulted in a single squashed commit (not if it intentionally preserved multiple meaningful commits): if there are now two commits on the branch (the squashed one + this new one) and the new changes are part of the same logical unit of work, amend the previous commit instead of creating a separate one.

## Step 7: Push and Create PR

Push the branch. If Step 3 rewrote commit history (squash or consolidation), a force push is required. Always use `--force-with-lease` to avoid overwriting someone else's work on the same branch:

```bash
git push -u origin {branch-name}                # if no history rewrite
git push --force-with-lease -u origin {branch-name}  # if Step 3 rewrote history
```

Construct the PR title: use the conventional commit subject line, optionally prefixed with the ticket ID (e.g., `CPDO-123: feat: add OAuth2 authentication flow`).

Create the PR with `gh pr create`. Use this body template:

```
## Summary
- [1-3 bullet points describing what changed and why]

## Linear Ticket
[TICKET-ID]({ticket URL from mcp__linear__get_issue}) — {ticket title}

## Test Plan
- [ ] [Steps to verify the changes work correctly]
```

If no Linear ticket, omit the Linear Ticket section.

## Step 8: Copilot Review (Optional Iterative Loop)

Ask the user: **"Do you want to run the Copilot review loop?"**

- If **no**: request a single Copilot review (see below) and continue to Step 9.
- If **yes**: run the iterative review loop described below.

### Requesting a Copilot review

Extract the owner, repo, and PR number. Then request a review using the GitHub API directly:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/requested_reviewers \
  -f "reviewers[]=copilot-pull-request-reviewer[bot]"
```

IMPORTANT: The reviewer name MUST be exactly `copilot-pull-request-reviewer[bot]` with the `[bot]` suffix. Do NOT use `gh pr edit --add-reviewer` — it will silently fail for bot accounts.

If this request fails, warn the user but continue with the remaining steps.

### Iterative review loop

Repeat the following cycle until diminishing returns are reached:

**1. Request Copilot review** using the API call above.

**2. Wait for results.** Before polling, capture the current commit SHA:

```bash
git rev-parse HEAD
```

Then poll for a review that matches this exact commit SHA:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews \
  --jq '[.[] | select(.user.login=="copilot-pull-request-reviewer[bot]" and .commit_id=="{current_sha}") | {id: .id, commit: .commit_id}] | sort_by(.id) | last'
```

Poll every 60 seconds, up to 10 attempts (~10 minutes total). If no review appears after all attempts, inform the user "Copilot didn't respond — continuing without it" and proceed to Step 9.

Once a review appears for the current commit SHA, extract the review ID (a number) and fetch its comments:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments \
  --jq '[.[] | select(.pull_request_review_id == 1234567890) | {line: .line, body: .body}]'
```

Replace `1234567890` with the actual numeric review ID from the previous query.

**3. Analyze and classify each comment.** For each comment, decide:

- **Accept**: the comment identifies a real issue (incorrect behavior, misleading wording, missing edge case, actual bug). Worth fixing.
- **Skip**: the comment is a nitpick, repeats a previously addressed concern, suggests over-engineering, or doesn't apply (e.g., suggesting interactive tools for an AI agent, adding error handling the AI naturally handles).

**4. Present to the user.** Show a numbered summary of all comments with your recommendation (accept/skip) and a brief explanation for each. Ask the user to confirm or override.

**5. Apply accepted fixes.** Edit the files, then commit and push:
- If the branch has a single commit (from a full squash), amend it (`git commit --amend --no-edit`) and force push with `--force-with-lease`.
- If the branch has multiple meaningful commits (from partial consolidation or no squash), amend only HEAD or create a small fix commit, and push normally.

**6. Assess diminishing returns.** After each round, evaluate whether to continue:

- **Continue** if the round produced 2+ accepted fixes that improved the PR.
- **Stop** if most comments were skipped, comments are repeating from prior rounds, or the fixes are purely cosmetic. Inform the user: "Copilot's feedback is getting repetitive — I think we're good."

When the loop ends (either by diminishing returns or user decision), proceed to Step 9.

## Step 9: Comment on Linear Ticket

If a Linear ticket was identified, post a comment on it using `mcp__linear__create_comment` with:

- The PR title
- The PR URL
- A one-line summary of the changes

## Step 10: Update Linear Ticket Status

Ask the user if they want to move the Linear ticket status from "In Progress" to "In Review".

If yes:
1. Use `mcp__linear__list_issue_statuses` to find the correct "In Review" status ID for the ticket's team.
2. Use `mcp__linear__update_issue` to update the status.

If the user declines or there is no ticket, skip this step.

## Step 11: Slack Notification

Ask the user if they want to post a review request to Slack.

**Channel selection:** Before asking which channel, check if a preferred Slack channel is already saved in your auto memory files for this repo.

If a saved channel is found, use it as the default (confirm with the user: "Posting to #channel — ok?"). If not found, ask which channel to post to, then save the choice to your auto memory for this repo.

Do NOT modify repo files (e.g., `CLAUDE.md`) to store the channel preference unless the user explicitly asks you to.

Find the channel ID using `mcp__plugin_slack_slack__slack_search_channels`. IMPORTANT: Always search with `channel_types: "public_channel,private_channel"` since team channels are often private.

Send a message using `mcp__plugin_slack_slack__slack_send_message`. IMPORTANT: Do NOT wrap URLs in angle brackets in any form — no `<URL|text>` and no `<URL>`. Both trigger broken rendering or "Double-check this link" security warnings for bot-sent messages. Instead, paste URLs as plain text on their own line so Slack auto-unfurls them with a rich preview.

```
*{PR title}*
{one-line summary}
Already reviewed by Copilot ✅
{PR_URL}
Linear: {TICKET_URL from mcp__linear__get_issue response}
May someone please review it? 🙏
```

If no Linear ticket, omit the Linear line.
