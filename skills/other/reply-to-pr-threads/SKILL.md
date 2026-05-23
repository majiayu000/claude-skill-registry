---
name: reply-to-pr-threads
description: "Draft, confirm, and post replies to GitHub PR review threads. Handles per-category reply formatting, re-fetches thread resolution state so auto-resolved threads are skipped, and posts via GraphQL. Use when the user asks to \"reply to PR threads\", \"post PR thread replies\", or \"draft PR reply messages\"."
---

# Reply to PR Threads

Draft replies for a processed review-thread list, confirm with the user, and post the surviving drafts.

## Step 1: Run `$github-voice` Skill

Run the `$github-voice` skill to load voice rules and the insider-vs-outsider detection.

## Step 2: Re-fetch Thread State

Auto-detect owner, repo, and PR number from the current branch if not provided, then query the current resolution state:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes { id isResolved }
      }
    }
  }
}' -f owner='{owner}' -f repo='{repo}' -F pr={pr_number}
```

Drop threads whose `isResolved` is now true. Reviewers or bots such as CodeRabbit may resolve threads after the original fetch, and drafting replies for them is wasted work.

## Step 3: Draft Replies

Use the processed-thread list from conversation context. Each entry has: thread id, file path, line, category (`fix`, `skip`, `answer`, or `clarify`), and per-category payload.

Keep every reply to one or two sentences. No bullet-point reasoning. No bolded labels.

**fix**: payload is a commit SHA, optionally with a divergence note.

```
Fixed in <commit-sha>.
```

Only add a brief sentence after the SHA when the fix meaningfully diverges from what the reviewer suggested. Otherwise the SHA alone is enough.

**skip**: payload is the skip reasoning. State the reasoning directly. Do not apologize or hedge.

**answer**: payload is raw answer text from `$answer-reviewer-questions`. Tighten to one or two sentences and apply `$github-voice` rules (no em dashes, natural tone). Do not cite transcripts or mention Claude. The reply reads as the implementer's own explanation.

**clarify**: payload is a user-directed question. Draft it as directed.

## Step 4: Present Drafts and Confirm

Output all drafts as text, grouped by file:

```
### <file-path>

**Thread <id>** (<category>, line <line>)
Reviewer: <original comment, truncated if long>
Reply: <drafted reply>
```

Then use `request_user_input` to ask whether to post. Offer:

- **Post** — post all drafts as shown
- **Cancel** — skip posting

## Step 5: Post Replies

For each approved draft, post via the reply mutation:

```bash
gh api graphql -f query='
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $threadId, body: $body}) {
    comment { id }
  }
}' -f threadId="THREAD_ID" -f body="REPLY_BODY"
```

Substitute `THREAD_ID` with the thread's id and `REPLY_BODY` with the drafted reply text for each post. Report what was posted and what was skipped (due to auto-resolution between re-fetch and posting).

Then update or check the active plan and proceed to any remaining task.

## Rules

- Never resolve or dismiss a review thread. Only reply. Let the reviewer resolve.
- If a post mutation fails because the thread is already resolved, log the skip and continue with the rest.
