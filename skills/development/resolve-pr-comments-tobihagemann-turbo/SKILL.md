---
name: resolve-pr-comments
description: "Evaluate, fix, answer, and reply to GitHub pull request review comments and conversation comments. Handles both change requests (fix or skip) and reviewer questions (explain using reasoning recalled from past Claude Code transcripts). Use when the user asks to \"resolve PR comments\", \"fix review comments\", \"address PR feedback\", \"handle review comments\", \"address review feedback\", \"respond to PR comments\", \"answer review questions\", or \"address code review\"."
---

# Resolve PR Review Comments

Fetch unresolved review comments from a GitHub PR (inline threads, review-body observations, and issue-comment observations from the PR conversation), evaluate each one, fix or skip based on confidence, answer reviewer questions using recalled implementation reasoning, and reply. Inline threads are answered with thread replies; issue-comment findings are answered with new PR conversation comments. Review-body findings flow through the same evaluate-and-fix pipeline; their outcomes land in the summary because a review body has no destination to post to.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Fetch comments
2. Triage review bodies and issue comments
3. Run `/interpret-feedback` skill
4. Split questions and change requests
5. Run `/evaluate-findings` skill
6. Resolve ambiguities
7. Run `/resolve-findings` skill
8. Verify fixes
9. Run `/answer-reviewer-questions` skill
10. Run `/reply-to-pr-threads` skill
11. Run `/reply-to-pr-conversation` skill
12. Summary

## Step 1: Fetch Comments

Auto-detect owner, repo, and PR number from current branch if not provided. Then run `scripts/fetch-pr-data.sh`, which handles full pagination (reviews, review threads, inner comment pages for long threads, issue comments, commits) and emits a single merged JSON document:

```bash
bash <skill-dir>/scripts/fetch-pr-data.sh <owner> <repo> <pr_number>
```

Output shape:

```jsonc
{
  "meta":          { "title", "url", "headRefName", "baseRefName" },
  "reviewThreads": [ { "id", "isResolved", "isOutdated", "comments": { "nodes": [ { "author", "body", "path", "line", "originalLine", "diffHunk" } ] } } ],
  "reviews":       [ { "author", "body", "state", "submittedAt" } ],
  "issueComments": [ { "author", "body", "createdAt", "url" } ],
  "commits":       [ { "commit": { "oid", "abbreviatedOid", "message", "committedDate" } } ]
}
```

Filter review threads to unresolved only. Filter reviews to those with a non-empty body, excluding `PENDING` state (unsubmitted drafts). Filter issue comments to those with a non-empty body.

## Step 2: Triage Review Bodies and Issue Comments

Review bodies and PR conversation comments (issue comments) often pack multiple distinct concerns into one comment. Split each non-empty, non-PENDING review body and each non-empty issue comment into atomic observations, one per paragraph or bullet, so each can be evaluated on its own merits.

For every observation, check whether a subsequent commit already addresses it. Compare the source timestamp (`submittedAt` for review bodies, `createdAt` for issue comments) against each commit's `committedDate`; only commits after the source was posted can address it. Start with commit messages; read `git show <oid>` only when the message is ambiguous. A commit addresses an observation when its changes clearly resolve that specific concern. Touching the same area is not enough.

Classify each observation:
- **Addressed**: A subsequent commit resolves it. Record the commit SHA for the Step 12 summary.
- **Unaddressed**: No subsequent commit resolves it. Carry into Step 3, tagged with its `source` (`review-body` or `issue-comment`), the author, the observation text, and (for review bodies) the review state.

Review-body and issue-comment findings have no `diffHunk`, file path, or line reference. The downstream pipeline handles findings without a code location.

## Step 3: Run `/interpret-feedback` Skill

Run the `/interpret-feedback` skill on the union of:
- Unresolved inline threads
- Unaddressed review-body findings from Step 2
- Unaddressed issue-comment findings from Step 2

Skip AI-reviewer accounts — match by known login (e.g., `coderabbitai`, `copilot-pull-request-reviewer[bot]`), not the `[bot]` suffix alone. Their structured feedback routes directly to `/evaluate-findings`.

For inline threads, include the `diffHunk` so the interpreters can see the code the reviewer was looking at. For outdated comments where `line` is null, use `originalLine`. For review-body and issue-comment findings, provide the observation text and the PR's changed-file list as context.

Tag each item with its `source` (`inline-thread`, `review-body`, or `issue-comment`) so later steps can route replies correctly.

## Step 4: Split Questions and Change Requests

Classify each interpreted item as either a **question** or a **change request** based on the reconciled intent from Step 3.

- **Question** — the reviewer is asking for an explanation or wondering whether something is intentional. No code change requested. Examples: "Why this approach?", "Is this intentional?", "What is the benefit here?".
- **Change request** — the reviewer suggests a code change, flags a bug, or proposes an alternative. This includes soft-phrased suggestions ("could we ...", "consider ...") and rhetorical questions that imply a change ("Shouldn't this ...?", "Is there a reason this isn't ...?").

When in doubt, treat the item as a change request. The verdict from `/evaluate-findings` in Step 5 will catch genuine non-issues.

Produce two lists. Each entry retains the `source` tag, identifier (thread id for inline threads; a generated id for review-body and issue-comment findings), file path and line (use `originalLine` when `line` is null; omit for review-body and issue-comment findings), the reviewer's original text, and the reconciled intent from Step 3. Questions skip Step 5 and feed Step 9. Change requests feed Step 5.

## Step 5: Run `/evaluate-findings` Skill

Run the `/evaluate-findings` skill on the change requests from Step 4 to triage each one. Questions are not evaluated here.

Review-body and issue-comment findings have no file or line reference. Scope their assessment to the PR's changed files as a whole, and do not treat the absent code location as a "code has diverged" early exit.

## Step 6: Resolve Ambiguities

Collect items assigned an Escalate verdict by `/evaluate-findings`. If there are none, skip to Step 7.

Output all escalated items as a numbered list. For each item, show:

- The reviewer's original comment
- The competing interpretations or the reason for escalation
- The file and line reference, when available

Then use `AskUserQuestion` to ask how to handle them. Per item, the options are:

- **Direct answer**: "Do X" — assign an Accept verdict with the user's clarified intent. Step 7 picks it up as an accepted finding.
- **Ask the reviewer**: "Ask them Y" — queue a clarification question to be drafted in Step 10 (inline threads) or Step 11 (issue comments)
- **Skip**: Remove from processing

## Step 7: Run `/resolve-findings` Skill

If there are no accepted findings to implement, skip to Step 9.

Run the `/resolve-findings` skill on the accepted findings from Step 5, including any items reclassified in Step 6. `/finalize` commits and pushes as part of its normal flow; Steps 10 and 11 replies reference the already-pushed commit SHA.

## Step 8: Verify Fixes

For each finding that was fixed in Step 7, verify the fix actually addresses the reviewer's concern:

1. Read the current code. For inline threads, use the thread's file and line. For review-body and issue-comment findings, read the files touched during the fix.
2. Compare against the reviewer's comment (and `diffHunk` when available).
3. Confirm the specific concern is resolved.

If the fix did not address the concern (wrong location, incomplete change, or the issue is still present), downgrade the item to Skip. Record the reason (the attempted fix did not resolve the reviewer's concern, with a brief explanation of what remains) so Step 10 (for inline threads), Step 11 (for issue-comment findings), and Step 12 (for review-body findings) report it correctly.

## Step 9: Run `/answer-reviewer-questions` Skill

Run the `/answer-reviewer-questions` skill on question items whose source is `inline-thread`. It produces raw answer text per thread.

Issue-comment questions are composed during Step 11's assembly and posted by `/reply-to-pr-conversation`. They have no file and line to ground with `/recall-reasoning`, so the composition draws on the reconciled intent and the PR's changed code. Review-body questions have no destination to post to and are listed for manual follow-up in Step 12.

If there are no inline-thread questions, skip the skill invocation.

## Step 10: Run `/reply-to-pr-threads` Skill

Assemble the processed-thread list from inline-thread items only:

- **fix** — inline threads with Apply verdicts whose fix was verified in Step 8. Payload: the commit SHA from Step 7.
- **skip** — inline threads with Skip verdicts from `/evaluate-findings`, plus any downgraded in Step 8. Payload: the skip reasoning.
- **answer** — inline-thread questions with answers composed in Step 9. Payload: the raw answer text.
- **clarify** — inline threads reclassified as clarification questions in Step 6. Payload: the user-directed clarification question.

Issue-comment findings go to Step 11; review-body findings have no destination to post to and surface only in Step 12.

Run the `/reply-to-pr-threads` skill with the assembled list.

## Step 11: Run `/reply-to-pr-conversation` Skill

Assemble the processed-item list from issue-comment items only. Each entry includes the generated id, the author, the original comment body (for quoting), the category, and the per-category payload:

- **fix** — issue-comment findings with Apply verdicts whose fix was verified in Step 8. Payload: the commit SHA from Step 7.
- **skip** — issue-comment findings with Skip verdicts from `/evaluate-findings`, plus any downgraded in Step 8. Payload: the skip reasoning.
- **answer** — issue-comment questions. Compose a one-or-two-sentence answer from the reconciled intent from Step 3 and the PR's changed code. Payload: the composed answer.
- **clarify** — issue-comment items reclassified as clarification questions in Step 6. Payload: the user-directed clarification question.

Review-body findings have no destination to post to. Exclude them from this list; their triage status is reported in Step 12.

If there are no issue-comment items to reply to, skip the skill invocation.

Run the `/reply-to-pr-conversation` skill with the assembled list.

## Step 12: Summary

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

**Issue-comment findings:**
- Already addressed by commits (list author, one-line summary, addressing commit SHA)
- Fixed in this session (list observation, addressing commit SHA)
- Skipped (list observation, skip reasoning)
- Questions answered (list observation)
- Clarification questions asked
- Reply URL (the posted issue comment, if any)

**Overall:** list of files modified.

## Rules

- Process inline threads in file order to minimize context switching. Handle review-body and issue-comment findings after inline threads.
- Stale references and default-to-skip policy are handled by the `/evaluate-findings` skill.
- When a thread has multiple comments (discussion), read the full thread before deciding.
- The first comment in each thread is the original review comment; subsequent comments are replies.
