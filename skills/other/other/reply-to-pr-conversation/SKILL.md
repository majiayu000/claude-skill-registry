---
name: reply-to-pr-conversation
description: "Draft, confirm, and post a single conversational reply to GitHub PR conversation comments (issue comments). The reply addresses all tracked items in one natural-prose message. Use when the user asks to \"reply to PR conversation\", \"post PR conversation replies\", or \"draft PR conversation messages\"."
---

# Reply to PR Conversation

Draft a single reply that addresses a processed issue-comment list, confirm with the user, and post it as a new PR issue comment.

## Step 1: Run `/github-voice` Skill

Run the `/github-voice` skill to load voice rules and the insider-vs-outsider detection.

## Step 2: Compose the Reply

Use the processed-item list from conversation context. Each entry has: id, author, original comment body (to quote from selectively), category (`fix`, `skip`, `answer`, or `clarify`), and per-category payload.

Draft one reply that addresses every item as natural conversational prose. The output is a single piece of prose with flexible length and no rigid section structure.

**Use the category to interpret each payload:**

- **fix**: payload is a commit SHA. Mention "fixed in `<sha>`" where it fits the flow, plus a brief note when the fix diverges from what the commenter suggested.
- **skip**: payload is the skip reasoning. State it directly.
- **answer**: payload is answer text prepared upstream. Integrate it as the implementer's own words.
- **clarify**: payload is a user-directed question. Ask it as-is.

**Quote selectively.** Use `>` blockquotes only for the phrase being responded to. A single-topic reply quotes one sentence then responds; a multi-topic reply weaves quotes and responses together. Drop quotes entirely when @mentions plus context make the reply unambiguous.

**Quote handling:**

- Strip leading `>` from quoted lines so nested blockquotes don't misattribute.
- Replace fenced-code lines inside a quote with `> [code snippet]`.
- If the author login ends in `[bot]`, omit the suffix from the `@` mention.

Apply `/github-voice` rules. Match the conversation's length and tone. An acknowledgment with emoji is fine when the discussion calls for it; a multi-paragraph response is fine when the items warrant it.

## Step 3: Confirm

Output the drafted reply as text for review:

```
**Draft comment**

<full comment body as it will be posted>
```

Then use `AskUserQuestion` to ask whether to post. Offer:

- **Post** — post the comment
- **Cancel** — skip posting

## Step 4: Post the Comment

Auto-detect owner, repo, and PR number from the current branch if not provided. Post the drafted body once via the issue-comments REST endpoint:

```bash
gh api -X POST \
  "/repos/<owner>/<repo>/issues/<pr_number>/comments" \
  -f body="<comment-body>"
```

Report the posted comment's URL.

Then use the TaskList tool and proceed to any remaining task.

## Rules

- Never close the PR, resolve a thread, or edit existing comments. Only post a new issue comment.
- If the post fails, report the failure and leave the drafted body in the output so the user can post it manually.
