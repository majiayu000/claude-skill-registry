---
name: resolve-pr-comments
description: "Evaluate, fix, and reply to GitHub pull request review comments. Use when the user asks to \"resolve PR comments\", \"fix review comments\", \"address PR feedback\", \"handle review comments\", \"address review feedback\", \"respond to PR comments\", or \"address code review\"."
---

# Resolve PR Review Comments

Fetch unresolved review comments from a GitHub PR, critically evaluate each one, fix or skip based on confidence, and reply to each thread.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Fetch comments
2. Triage review body comments
3. Run `/interpret-feedback` skill
4. Run `/evaluate-findings` skill
5. Resolve ambiguities
6. Choose implementation path
7. Implement and finalize
8. Verify fixes
9. Draft replies
10. Post replies
11. Summary

## Step 1: Fetch Comments

Fetch review threads, top-level review body comments, and PR commits from the PR:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      title url
      reviewThreads(first: 100) {
        nodes {
          id isResolved isOutdated
          comments(first: 50) {
            nodes { author { login } body path line originalLine diffHunk }
          }
        }
      }
      reviews(first: 50) {
        nodes {
          author { login }
          body state submittedAt
        }
      }
      commits(last: 50) {
        nodes {
          commit {
            oid abbreviatedOid message committedDate
          }
        }
      }
    }
  }
}' -f owner='{owner}' -f repo='{repo}' -F pr={pr_number}
```

Auto-detect owner, repo, and PR number from current branch if not provided. Filter review threads to unresolved only. Filter reviews to those with a non-empty body, excluding `PENDING` state (unsubmitted drafts).

## Step 2: Triage Review Body Comments

For each review body comment (non-empty body, non-PENDING), check whether a commit in the PR already addresses it. Compare the review's `submittedAt` timestamp against each commit's `committedDate`. Only commits **after** the review was submitted can address it.

To determine if a commit addresses a review body comment, start with commit messages. Only read the full diff (`git show <oid>`) when the message alone is ambiguous. A commit addresses a comment when its changes clearly resolve the specific issue described — not merely when it touches the same area.

Classify each review body comment as:
- **Addressed**: A subsequent commit clearly resolves the concern. Record the commit SHA.
- **Unaddressed**: No subsequent commit resolves the concern. Requires manual attention.

## Step 3: Run `/interpret-feedback` Skill

Run the `/interpret-feedback` skill on unresolved inline threads authored by humans. Skip threads from bot accounts (logins ending in `[bot]`, e.g., CodeRabbit, Copilot). AI reviewer feedback is structured and explicit enough for `/evaluate-findings` to handle directly.

Include each thread's `diffHunk` so the interpreters can see the code context the reviewer commented on. For outdated comments where `line` is null, use `originalLine` as the line reference.

## Step 4: Run `/evaluate-findings` Skill

Run the `/evaluate-findings` skill on the interpreted results to triage each comment.

## Step 5: Resolve Ambiguities

Collect items assigned an Escalate verdict by `/evaluate-findings`. If there are none, skip to Step 6.

Output all escalated items as a numbered list. For each item, show:

- The reviewer's original comment
- The competing interpretations or the reason for escalation
- The file and line reference

Then use `AskUserQuestion` to ask how to handle them. Per item, the options are:

- **Direct answer**: "Do X" — assign an Accept verdict with the user's clarified intent, and pass it to `/apply-findings`
- **Ask the reviewer**: "Ask them Y" — queue a clarification question to be drafted in Step 9
- **Skip**: Remove from processing

## Step 6: Choose Implementation Path

Present a summary of accepted findings: count by complexity (mechanical fixes vs. architectural or design changes). Then use `AskUserQuestion` to let the user choose:

- **Full** — Enter plan mode via `/plan-style` for review, approval, implementation, and finalize
- **Lightweight** — Apply directly via `/apply-findings`, then `/finalize`

Suggest Full when findings include complex or architectural changes. Suggest Lightweight when all findings are mechanical fixes.

If there are no accepted findings to implement, skip to Step 9.

## Step 7: Implement and Finalize

**Full path:**

Run the `/plan-style` skill. The plan should address each accepted finding from the evaluation, including any items reclassified in Step 5. After plan approval, implement the changes. `/finalize` is included as the plan's final step. The commit SHA from finalize is needed for reply messages.

**Lightweight path:**

1. Run the `/apply-findings` skill on the evaluated results, including any items reclassified in Step 5.
2. If changes were made, run the `/finalize` skill. The commit SHA from finalize is needed for reply messages.
3. If no changes were made, skip to Step 9.

## Step 8: Verify Fixes

For each finding that was fixed in Step 7, verify the fix actually addresses the reviewer's concern:

1. Read the current code at the relevant file and location
2. Compare against the reviewer's comment and `diffHunk` (the code the reviewer was looking at)
3. Confirm the specific concern is resolved

If the fix did not address the concern (wrong location, incomplete change, or the issue is still present), downgrade it to skipped. Draft a skip reply in Step 9 with the reason: the attempted fix did not resolve the reviewer's concern, with a brief explanation of what remains.

## Step 9: Draft Replies

Run `/github-voice` to load writing style rules before composing replies. Keep replies to one or two sentences. Avoid bullet-point reasoning or bolded labels.

**Review body comments** (top-level review comments with non-empty body) cannot be replied to via thread replies — they are not threads. Do not attempt to reply to them. Instead, report them in the summary (Step 11) with their triage status from Step 2.

For each processed **inline thread**, draft a reply.

**Reply format for fixes:**
```
Fixed in <commit-sha>.
```

Only add a brief description after the SHA if the fix meaningfully diverges from what the reviewer suggested. Otherwise, the commit SHA alone is enough.

**Reply format for skips:** Just state the reasoning for not changing it.

**Reply format for clarifications** (queued in Step 5): Draft the clarification question as directed by the user.

Output all drafted replies as text, grouped by file, showing the reviewer's comment and the drafted reply for each thread. Then use `AskUserQuestion` to confirm before posting.

## Step 10: Post Replies

After confirmation, check whether each thread was resolved between fetching and posting (e.g., CodeRabbit auto-resolves its own threads after a push). Skip resolved threads. Post each confirmed reply using:

```bash
gh api graphql -f query='
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $threadId, body: $body}) {
    comment { id }
  }
}' -f threadId="THREAD_ID" -f body="REPLY_BODY"
```

## Step 11: Summary

After processing all threads, present a summary table:

- Total unresolved inline threads found
- Number fixed (high + medium confidence)
- Number skipped (low confidence)
- Number of clarification questions posted
- Review body comments already addressed by commits (list author, state, one-line summary, and the addressing commit SHA)
- Review body comments requiring manual attention (list author, state, and a one-line summary of each)
- List of files modified

## Rules

- Never resolve or dismiss a review thread — only reply. Let the reviewer resolve.
- Process comments in file order to minimize context switching.
- Stale references and default-to-skip policy are handled by the `/evaluate-findings` skill.
- When a thread has multiple comments (discussion), read the full thread before deciding.
- The first comment in each thread is the original review comment; subsequent comments are replies.
