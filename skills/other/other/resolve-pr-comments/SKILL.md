---
name: resolve-pr-comments
description: "Evaluate, fix, answer, and reply to GitHub pull request review comments. Handles both change requests (fix or skip) and reviewer questions (explain using reasoning recalled from past Claude Code transcripts). Use when the user asks to \"resolve PR comments\", \"fix review comments\", \"address PR feedback\", \"handle review comments\", \"address review feedback\", \"respond to PR comments\", \"answer review questions\", or \"address code review\"."
---

# Resolve PR Review Comments

Fetch unresolved review comments from a GitHub PR (both inline threads and review-body observations), evaluate each one, fix or skip based on confidence, answer reviewer questions using recalled implementation reasoning, and reply to each thread. Review-body findings flow through the same evaluate-and-fix pipeline as inline threads; their outcomes land in the summary because they have no thread to reply to.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Fetch comments
2. Triage review bodies
3. Run `/interpret-feedback` skill
4. Split questions and change requests
5. Run `/evaluate-findings` skill
6. Resolve ambiguities
7. Run `/resolve-findings` skill
8. Verify fixes
9. Run `/answer-reviewer-questions` skill
10. Run `/reply-to-pr-threads` skill
11. Summary

## Step 1: Fetch Comments

Auto-detect owner, repo, and PR number from current branch if not provided. Then run `scripts/fetch-pr-data.sh`, which handles full pagination (reviews, review threads, inner comment pages for long threads, commits) and emits a single merged JSON document:

```bash
bash <skill-dir>/scripts/fetch-pr-data.sh <owner> <repo> <pr_number>
```

Output shape:

```jsonc
{
  "meta":          { "title", "url", "headRefName", "baseRefName" },
  "reviewThreads": [ { "id", "isResolved", "isOutdated", "comments": { "nodes": [ { "author", "body", "path", "line", "originalLine", "diffHunk" } ] } } ],
  "reviews":       [ { "author", "body", "state", "submittedAt" } ],
  "commits":       [ { "commit": { "oid", "abbreviatedOid", "message", "committedDate" } } ]
}
```

Filter review threads to unresolved only. Filter reviews to those with a non-empty body, excluding `PENDING` state (unsubmitted drafts).

## Step 2: Triage Review Bodies

Review bodies often pack multiple distinct concerns into one comment. Split each non-empty, non-PENDING review body into atomic observations, one per paragraph or bullet, so each can be evaluated on its own merits.

For every observation, check whether a subsequent commit already addresses it. Compare the review's `submittedAt` timestamp against each commit's `committedDate`; only commits after the review was submitted can address it. Start with commit messages; read `git show <oid>` only when the message is ambiguous. A commit addresses an observation when its changes clearly resolve that specific concern. Touching the same area is not enough.

Classify each observation:
- **Addressed**: A subsequent commit resolves it. Record the commit SHA for the Step 11 summary.
- **Unaddressed**: No subsequent commit resolves it. Carry into Step 3 as a review-body finding, tagged with the reviewer, review state, and the observation text.

Review-body findings have no `diffHunk`, file path, or line reference. The downstream pipeline handles findings without a code location.

## Step 3: Run `/interpret-feedback` Skill

Run the `/interpret-feedback` skill on the union of:
- Unresolved inline threads
- Unaddressed review-body findings from Step 2

Skip items from bot accounts (logins ending in `[bot]`, e.g., CodeRabbit, Copilot). AI reviewer feedback is structured and explicit enough for `/evaluate-findings` to handle directly.

For inline threads, include the `diffHunk` so the interpreters can see the code the reviewer was looking at. For outdated comments where `line` is null, use `originalLine`. For review-body findings, provide the observation text and the PR's changed-file list as context.

Tag each item with its `source` (`inline-thread` or `review-body`) so later steps can route replies correctly.

## Step 4: Split Questions and Change Requests

Classify each interpreted item as either a **question** or a **change request** based on the reconciled intent from Step 3.

- **Question** — the reviewer is asking for an explanation or wondering whether something is intentional. No code change requested. Examples: "Why this approach?", "Is this intentional?", "What is the benefit here?".
- **Change request** — the reviewer suggests a code change, flags a bug, or proposes an alternative. This includes soft-phrased suggestions ("could we ...", "consider ...") and rhetorical questions that imply a change ("Shouldn't this ...?", "Is there a reason this isn't ...?").

When in doubt, treat the item as a change request. The verdict from `/evaluate-findings` in Step 5 will catch genuine non-issues.

Produce two lists. Each entry retains the `source` tag, identifier (thread id for inline threads; a generated id for review-body findings), file path and line (use `originalLine` when `line` is null; omit for review-body findings), the reviewer's original text, and the reconciled intent from Step 3. Questions skip Step 5 and feed Step 9. Change requests feed Step 5.

## Step 5: Run `/evaluate-findings` Skill

Run the `/evaluate-findings` skill on the change requests from Step 4 to triage each one. Questions are not evaluated here.

Review-body findings have no file or line reference. Scope their assessment to the PR's changed files as a whole, and do not treat the absent code location as a "code has diverged" early exit.

## Step 6: Resolve Ambiguities

Collect items assigned an Escalate verdict by `/evaluate-findings`. If there are none, skip to Step 7.

Output all escalated items as a numbered list. For each item, show:

- The reviewer's original comment
- The competing interpretations or the reason for escalation
- The file and line reference

Then use `AskUserQuestion` to ask how to handle them. Per item, the options are:

- **Direct answer**: "Do X" — assign an Accept verdict with the user's clarified intent. Step 7 picks it up as an accepted finding.
- **Ask the reviewer**: "Ask them Y" — queue a clarification question to be drafted in Step 10
- **Skip**: Remove from processing

## Step 7: Run `/resolve-findings` Skill

If there are no accepted findings to implement, skip to Step 9.

Run the `/resolve-findings` skill on the accepted findings from Step 5, including any items reclassified in Step 6. The commit SHA from `/finalize` is needed for reply messages in Step 10.

## Step 8: Verify Fixes

For each finding that was fixed in Step 7, verify the fix actually addresses the reviewer's concern:

1. Read the current code. For inline threads, use the thread's file and line. For review-body findings, read the files touched during the fix.
2. Compare against the reviewer's comment (and `diffHunk` when available).
3. Confirm the specific concern is resolved.

If the fix did not address the concern (wrong location, incomplete change, or the issue is still present), downgrade the item to Skip. Record the reason (the attempted fix did not resolve the reviewer's concern, with a brief explanation of what remains) so Step 10 (for inline threads) and Step 11 (for review-body findings) report it correctly.

## Step 9: Run `/answer-reviewer-questions` Skill

Run the `/answer-reviewer-questions` skill on question items whose source is `inline-thread`. It produces raw answer text per thread.

Review-body questions (rare) have no thread to reply to. Carry them forward so Step 11 can list them for manual follow-up.

If there are no inline-thread questions, skip the skill invocation.

## Step 10: Run `/reply-to-pr-threads` Skill

Assemble the processed-thread list from inline-thread items only:

- **fix** — inline threads with Apply verdicts whose fix was verified in Step 8. Payload: the commit SHA from Step 7.
- **skip** — inline threads with Skip verdicts from `/evaluate-findings`, plus any downgraded in Step 8. Payload: the skip reasoning.
- **answer** — inline-thread questions with answers composed in Step 9. Payload: the raw answer text.
- **clarify** — inline threads reclassified as clarification questions in Step 6. Payload: the user-directed clarification question.

Review-body findings are not threads and cannot be replied to. Exclude them from this list. Their fixes are communicated by the commits from Step 7, and their triage status is reported in Step 11.

Run the `/reply-to-pr-threads` skill with the assembled list.

## Step 11: Summary

After processing all items, present a summary grouped by source.

**Inline threads:**
- Total unresolved threads found
- Fixed (change requests with accepted verdicts)
- Skipped (false positives or disproportionate changes)
- Questions answered (split into: answered from recalled transcript, answered from current code)
- Clarification questions posted

**Review-body findings:**
- Already addressed by commits (list author, state, one-line summary, addressing commit SHA)
- Fixed in this session (list observation, addressing commit SHA)
- Skipped (list observation, skip reasoning)
- Questions for manual follow-up (list observation; no thread to reply to)

**Overall:** list of files modified.

## Rules

- Process inline threads in file order to minimize context switching. Handle review-body findings after inline threads.
- Stale references and default-to-skip policy are handled by the `/evaluate-findings` skill.
- When a thread has multiple comments (discussion), read the full thread before deciding.
- The first comment in each thread is the original review comment; subsequent comments are replies.
