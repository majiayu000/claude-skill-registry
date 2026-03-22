---
name: pr-feedback
description: Address PR review feedback including inline threads, general comments, bot-generated reviews, PR description findings, and CI failures. Use when asked to handle, address, resolve, respond to, or work through PR review comments, review feedback, or CI check failures. Triggers on requests like "address PR comments", "handle review feedback", "resolve PR reviews", "fix review comments", "go through PR feedback", "check CI failures".
---

# PR Feedback

Fetch all review feedback and CI status from the PR associated with the current branch, triage each item, implement fixes, and propose responses.

All commands auto-detect the repository and PR from the current branch.

## Step 1: Fetch All Review Feedback

Run the three fetch commands to collect all feedback:

```bash
python3 ~/.claude/skills/pr-feedback/scripts/pr_feedback.py threads    # unresolved inline review threads
python3 ~/.claude/skills/pr-feedback/scripts/pr_feedback.py ci         # CI check status and failures
python3 ~/.claude/skills/pr-feedback/scripts/pr_feedback.py comments   # general PR comments and PR description
```

If any fails (no PR for current branch, auth issues), report the error and stop.

`threads` returns `unresolved_threads` with thread_id, path, line, and comments (each with node_id, database_id, diff_hunk).

`ci` returns `ci_summary` (pass/fail/pending counts) and `failed_checks` (with run_id, job_id for log fetching).

`comments` returns `pr_body` (may contain bot-appended review content), `pr_comments` (each with node_id, database_id), and `pr_author`.

## Step 2: Triage and Process Review Comments

### Inline Review Threads

For each unresolved thread, read the file at the commented path and lines for context. Read the entire thread (including replies) to understand the final ask. Classify into one of three actions:

**Implement** when the comment is:
- A clear, unambiguous fix: bug, typo, missing import, null check, off-by-one
- A code style correction aligned with project conventions or linter rules
- Missing error handling at a system boundary
- A simple rename, refactor, or dead code removal with obvious improvement

**Dismiss** (with concise, respectful explanation) when:
- A stylistic preference not backed by project conventions or linter rules
- Suggesting over-engineering or premature abstraction
- Factually incorrect about what the code does
- Already addressed in a subsequent commit (verify via git log)
- Out of scope for the PR

**Ask** (escalate to user) when:
- The suggestion is ambiguous or has multiple valid interpretations
- It involves an architectural or design trade-off
- It requires domain or business knowledge to evaluate
- The scope extends significantly beyond the PR
- You are genuinely uncertain whether the concern is valid

When in doubt between Implement and Ask, prefer Ask.

### General PR Comments

Process comments from `pr_comments` that contain actionable review feedback. Skip CI status messages, merge bot noise, and other non-review content. Look for:
- Bot-generated code reviews (Greptile, CodeRabbit, etc.)
- Human reviewer comments left at the PR level rather than inline
- Specific concerns, suggestions, or questions that warrant a response

Triage these using the same Implement / Dismiss / Ask criteria. Since these are not tied to specific lines, read the relevant files mentioned in the comment for context.

### PR Description Bot Content

Scan `pr_body` for bot-appended review sections. Common patterns:
- Greptile: sections titled "Greptile Summary", "Greptile Overview", or containing "Confidence Score"
- Other bots: sections with "must-fix", "findings", "suggestions"

Extract actionable items and triage them. Pay particular attention to "must-fix" items -- they indicate merge-blocking concerns from the bot's perspective.

Flag any findings that are factually incorrect (hallucinations). These need correction in the response phase.

## Step 3: Address CI Failures

If `ci_summary.failed` is 0, skip this step.

For each entry in `failed_checks`, fetch the failed job logs:

```bash
gh run view {run_id} --log-failed 2>&1 | tail -200
```

Diagnose each failure and classify:

**Fix** when:
- A test failure caused by code changes in this PR
- A lint or formatting error introduced by this PR
- A pre-commit hook failure on files changed in this PR

**Skip** (with explanation) when:
- A flaky test unrelated to the PR's changes
- An infrastructure or CI configuration issue (timeout, runner failure, dependency fetch error)
- A pre-existing failure that also occurs on the base branch

When fixing, read the relevant test file and source file to understand the failure, then apply the fix.

## Step 4: Present Summary

After processing all feedback and CI failures, present results grouped by action:

1. **Implemented** -- each change with file path, line, and what was done
2. **Dismissed** -- each with the explanation
3. **Needs input** -- each with your questions
4. **CI fixes** -- each failure with diagnosis and what was fixed
5. **CI skipped** -- each with why it was skipped

Wait for user review of code changes before proceeding to Step 5.

## Step 5: Propose Responses

After the user approves the code changes, propose a response plan. Present the full plan and wait for approval before executing any of it.

### For Implemented Threads
- Resolve the thread: `python3 ~/.claude/skills/pr-feedback/scripts/pr_feedback.py resolve THREAD_ID`
- Optionally reply with a brief note about the fix: `python3 ~/.claude/skills/pr-feedback/scripts/pr_feedback.py reply DATABASE_ID "Fixed: ..."`

### For Dismissed Threads
- Reply with the dismissal explanation: `python3 ~/.claude/skills/pr-feedback/scripts/pr_feedback.py reply DATABASE_ID "Explanation..."`
- Or add a thumbs-up if acknowledged but no change needed: `python3 ~/.claude/skills/pr-feedback/scripts/pr_feedback.py react review DATABASE_ID`
- Skip replying if the comment is clearly noise (bot false positive)

### For General PR Comments and PR Body Findings

Draft a single follow-up PR comment addressing multiple non-threaded items together:
```bash
python3 ~/.claude/skills/pr-feedback/scripts/pr_feedback.py comment "Response text..."
```

Use this for:
- Responding to bot reviews with corrections for hallucinated findings
- Providing missing context that reviewers may not have
- Pointing reviewers to the right code if they misread the implementation
- Summarizing what was fixed vs. what was intentionally left as-is

To react to a general PR comment: `python3 ~/.claude/skills/pr-feedback/scripts/pr_feedback.py react issue DATABASE_ID`

## Guidelines

- Process threads in file order to keep edits coherent.
- When multiple comments touch the same file, read the file once and process them together.
- Do not commit changes or post responses automatically. Present everything for user review first.
- Outdated threads still deserve attention -- the underlying concern may still apply. Flag them as outdated in the summary.
- If a thread has back-and-forth discussion, focus on the latest unresolved ask.
- Respect the codebase's project instructions (CLAUDE.md) when evaluating comments.
- When drafting response text, keep it factual and concise. Do not be defensive or dismissive.
- When correcting hallucinated findings, be specific: quote what the reviewer claimed, explain what actually happens, and point to the relevant code.
