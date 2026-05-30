---
name: jira-report-comment
description: >-
  This skill should be used when the user asks to "jira report", "post update to jira", "summarize commits for jira", "report to jira", "update the ticket", "comment on the ticket", "generate implementation report", "write a jira comment", "summarize my changes", or wants to notify PM/QA about completed work on a Jira ticket. Generates a business-friendly implementation report from git commits and saves it as a local markdown report.


allowed-tools: Read, Write, Bash, mcp__atlassian__getJiraIssue, AskUserQuestion
user-invocable: true
---

# Jira Report Comment

Generate a short Jira comment (60-100 words) describing what shipped on a ticket, and save it as a local markdown file.

**Announce at start:** "Using the jira-report-comment skill to generate an implementation report."

## What This Skill Produces

The reader is a PM, QA engineer, or architect who already has the Jira ticket open. They do not need a recap of the ticket. They need:

1. **The summary** - what shipped, in one or two sentences, framed as outcome. (Always present.)
2. **Root cause** - why the problem existed and the approach taken to fix it. (Present when the ticket fixes an existing problem.)
3. **Verify** - any non-obvious test path the ticket does not call out. (Usually omitted.)
4. **Deploy** - any non-routine deploy step. (Usually omitted.)

Default output:

- **Feature work:** summary only.
- **Bug fix:** summary + Root Cause.

Verify and Deploy appear only when a Decision Rule in Step 4 is triggered.

## Step 1: Resolve the Issue Key

Determine the Jira issue key using this priority:

1. If the user provided an issue key (e.g., "CX-4328"), use it directly.
2. Otherwise, extract from the current branch name:

   ```bash
   git branch --show-current
   ```

   Find the first match of `[A-Z]+-[0-9]+` (e.g., `feature/ABC-1234-description` yields `ABC-1234`).

3. If no key can be determined, ask the user.

**Confirm** the resolved key before proceeding: "I detected **CX-4328** from your branch. Use this issue key?"

### Reserve the Report File

After confirming the issue key, reserve the output file. This locks the filename for the session - all writes go to this file.

```bash
mkdir -p docs/jira-reports
touch "docs/jira-reports/$(date +%Y-%m-%d-%H%M%S)-<ISSUE_KEY>.md"
```

Store the full path in conversation context (e.g., `docs/jira-reports/2026-03-27-153012-ABC-123.md`). If the skill is invoked again in the same session for the same issue, reuse this path - do not create a new file.

## Step 2: Fetch Jira Issue Context

Retrieve the issue. Try the Atlassian MCP tool first:

```text
mcp__atlassian__getJiraIssue
  issueIdOrKey: "<ISSUE_KEY>"
```

If the MCP tool is unavailable or fails, ask the user: "Atlassian MCP is not available. Please paste the issue text (title, description, acceptance criteria) or provide an XML export."

Read and note:

- **Issue title** - what the ticket is about
- **Description** - acceptance criteria, requirements, business context
- **Issue type** - bug, story, task
- **Status** - current workflow state

This is what the reader already knows. **Do not paraphrase, quote, or restate any phrase from these in the comment.** Use this content as the reference for what to leave out, not as material for the report.

## Step 3: Gather Commits and Diffs

Find all commits referencing the issue key:

```bash
git log --grep="<ISSUE_KEY>" --format="%H %s" --reverse
```

If no commits found, widen the search:

```bash
git log --all --grep="<ISSUE_KEY>" --format="%H %s" --reverse
```

If still no commits, fall back to diffing the current branch against its base:

```bash
git merge-base HEAD main
git diff $(git merge-base HEAD main)..HEAD --stat
git diff $(git merge-base HEAD main)..HEAD
```

Try `main`, then `master`, then `develop` as the base branch. If no meaningful diff is found, inform the user and stop.

For the aggregate diff across all found commits (first commit's parent to last commit):

```bash
git diff <FIRST_COMMIT>^..<LAST_COMMIT> --stat
git diff <FIRST_COMMIT>^..<LAST_COMMIT>
```

If the first commit is the initial repository commit (no parent), use `git diff $(git hash-object -t tree /dev/null)..<LAST_COMMIT>` instead.

This shows the **net result** across all commits, not incremental progress.

If the diff is very large (50+ files), focus on the stat summary and read only the most significant files. Configuration files, test files, and migration files often reveal intent better than implementation details.

For tickets that fix an existing problem, also read commit messages for cause clues. The diff itself shows before-vs-after - that is where root cause lives.

## Step 4: Decide What Goes in the Comment

Load the output skeleton:

- **`references/report-template.md`** - read this now for the structure

### Decision Rules

Default output:

- **Feature work:** summary section only.
- **Bug fix:** summary + Root Cause section.

Add a **Root Cause** section if the ticket fixes an existing problem - the description mentions broken behavior, an incorrect result, a defect, or a regression. Issue type Bug is a strong but not required signal; some Story or Task tickets also fix problems.

The section explains:

- What was wrong (the underlying cause, not the symptom the ticket already describes)
- The approach taken to fix it

Limit to 1 or 2 bullets, max 25 words each. Derive both from the diff and commit messages, not from the ticket description.

Add a **Verify** section if AT LEAST ONE is true:

- The diff adds a feature flag and the test path depends on its state
- The diff fires a side effect (email, webhook, log, metric) that the ticket does not mention
- The diff adds a code path triggered by an input value the ticket does not name
- The diff changes behavior for a user role or permission level the ticket does not call out

Add a **Deploy** section if AT LEAST ONE is true:

- The diff adds or renames an environment variable
- The diff adds a feature flag (state the flag name and its default)
- The diff adds a database migration that needs manual coordination (data backfill, lock-heavy schema change)
- The diff adds a queue, scheduled job, or cron entry
- The diff requires a config change in another system (CDN, IAM, DNS)

If neither set of triggers fires: write only the summary. Stop.

### Tone

- Outcomes, not implementation. "Verification now checks the NPI Registry" not "Added NpiRegistryService."
- Common IT terms only (API, endpoint, database, deploy). No file paths, class names, or method names.
- Read **`references/formatting-rules.md`** and follow it.

## Step 5: Draft, Audit, Save

Draft in this order:

1. **Identify the ticket type.** If the ticket fixes an existing problem, derive the root cause and fix approach from the diff and commit messages before drafting. The summary can then reference the outcome naturally; the Root Cause section explains why it broke and how the diff fixes it.
2. **Write the summary** - one or two sentences linking work to ticket goal.
3. **Walk the Decision Rules.** For each trigger that fires (Root Cause for bug fixes; Verify or Deploy if their triggers fire), add the matching bullets.
4. **Audit each section bullet.** Delete any bullet that just restates the ticket or describes routine work. Routine work includes: pushing code, restarting services, clearing caches, running standard migrations.
5. **Strip ticket paraphrases.** Re-read the whole comment. Remove any phrase that paraphrases the ticket title, description, or acceptance criteria.

If Root Cause, Verify, and Deploy are all empty after step 3, the comment is the summary line and nothing else.

### Example 1 - bug fix (with Root Cause)

- **Ticket:** `BUG-789` "Cancellation email sent twice when a user cancels their subscription"
- **Description:** "Users who cancel receive two identical cancellation emails. Should only receive one."
- **Diff summary:** removed the legacy `onCancellation` handler registration in `SubscriptionEvents`. The newer `onSubscriptionCancelled` handler now sends the email alone. Test added covering single-send behavior.

**Comment:**

> ## BUG-789
>
> Cancellation now sends a single confirmation email.
>
> ### Root Cause
>
> - Two handlers were subscribed to the cancellation event after a partial refactor - the new `onSubscriptionCancelled` and the legacy `onCancellation` were both firing.
> - Removed the legacy registration; the new handler is the single source of truth.

The ticket described the symptom; Root Cause explains the underlying duplication. No Verify (the test path matches the ticket); no Deploy (routine code change).

### Example 2 - with Deploy

- **Ticket:** `XYZ-456` "Send weekly digest email to active members"
- **Description:** "Email members on Mondays at 9am with their week's activity summary. Skip inactive members."
- **Diff summary:** new cron job, new feature flag `weekly_digest_enabled` (default off), new env var `DIGEST_SENDER_EMAIL`.

**Comment:**

> ## XYZ-456
>
> Weekly digest emails now ship every Monday at 9am to active members, skipping accounts with no activity in the last 7 days.
>
> ### Deploy
>
> - Set `DIGEST_SENDER_EMAIL` in production before enabling the feature
> - Toggle `weekly_digest_enabled` to on after a smoke test
> - First scheduled run lands the Monday after deploy

The test path matches what the ticket described, so no Verify section. Deploy fires because of the new env var, the new flag, and the new cron entry.

### Save

Write the report content to the reserved file path (overwriting the empty placeholder):

```text
Write tool -> file_path: <RESERVED_FILE_PATH>
              content: <REPORT_CONTENT>
```

Confirm to the user: "Report saved to `<RESERVED_FILE_PATH>`."

If the user requests changes, revise and overwrite the same file.

If the `humanize-text` skill is available, run the final report through it before presenting to the user.

## Error Handling

- **Jira issue not found:** Tell the user the key appears invalid. Ask them to double-check.
- **No commits found:** Report clearly. Suggest checking the branch or that commits may use a different key format.
- **MCP tool unavailable:** Ask the user to provide issue context manually.
- **File write fails:** Show the error. Check directory permissions and retry.

## Hard Rules

- Total comment length: 60-100 words for feature work, up to 150 words when Root Cause is present.
- Summary: 1 or 2 sentences. Never paraphrase the ticket title, description, or acceptance criteria.
- Root Cause: include when the ticket fixes an existing problem. Max 2 bullets, max 25 words per bullet. Derive from the diff and commit messages, not the ticket.
- Verify and Deploy: omit unless a Decision Rule in Step 4 fires. Each section: max 3 bullets, max 15 words per bullet.
- Write to the reserved file path from Step 1. Do not create another file.
- Never commit or stage the report file - leave it untracked.
- Never invent changes the diffs do not show.

## Additional Resources

### Reference Files

- **`references/report-template.md`** - Output skeleton. Load in Step 4.
- **`references/formatting-rules.md`** - Length and style rules. Load alongside the skeleton in Step 4.
