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
3. Run `/evaluate-findings` skill
4. Run `/apply-findings` skill
5. Run `/finalize` skill
6. Draft replies
7. Post replies
8. Summary

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
            nodes { author { login } body path line }
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

## Step 3: Run `/evaluate-findings` Skill

Run the `/evaluate-findings` skill on the unresolved inline threads to assess each comment.

## Step 4: Run `/apply-findings` Skill

Run the `/apply-findings` skill on the evaluated results.

## Step 5: Run `/finalize` Skill

If `/apply-findings` reported any changes were made, run the `/finalize` skill to polish, test, review, and commit the changes. The commit SHA from finalize is needed for reply messages.

If no changes were made, skip to Step 6.

## Step 6: Draft Replies

Run `/github-voice` to load writing style rules before composing replies. Keep replies to one or two sentences. Avoid bullet-point reasoning or bolded labels.

**Review body comments** (top-level review comments with non-empty body) cannot be replied to via thread replies — they are not threads. Do not attempt to reply to them. Instead, report them in the summary (Step 8) with their triage status from Step 2.

For each processed **inline thread**, draft a reply.

**Reply format for fixes:**
```
Fixed in <commit-sha>.
```

Only add a brief description after the SHA if the fix meaningfully diverges from what the reviewer suggested. Otherwise, the commit SHA alone is enough.

**Reply format for skips:** Just state the reasoning for not changing it.

Output all drafted replies as text, grouped by file, showing the reviewer's comment and the drafted reply for each thread. Then use `AskUserQuestion` to confirm before posting.

## Step 7: Post Replies

After confirmation, check whether each thread was resolved between fetching and posting (e.g., CodeRabbit auto-resolves its own threads after a push). Skip resolved threads. Post each confirmed reply using:

```bash
gh api graphql -f query='
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $threadId, body: $body}) {
    comment { id }
  }
}' -f threadId="THREAD_ID" -f body="REPLY_BODY"
```

## Step 8: Summary

After processing all threads, present a summary table:

- Total unresolved inline threads found
- Number fixed (high + medium confidence)
- Number skipped (low confidence)
- Review body comments already addressed by commits (list author, state, one-line summary, and the addressing commit SHA)
- Review body comments requiring manual attention (list author, state, and a one-line summary of each)
- List of files modified

## Rules

- Never resolve or dismiss a review thread — only reply. Let the reviewer resolve.
- Process comments in file order to minimize context switching.
- Stale references and default-to-skip policy are handled by the `/evaluate-findings` skill.
- When a thread has multiple comments (discussion), read the full thread before deciding.
- The first comment in each thread is the original review comment; subsequent comments are replies.
