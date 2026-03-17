---
name: address-pr-feedback
description: Walk through PR review comments one by one, spawn a subagent per comment to validate the concern and propose fixes, then explain each to the user and suggest fixes without replying on GitHub. Use when the user wants to address PR feedback, go through review comments, process PR comments interactively, or respond to code review.
---

# Address PR Feedback (Interactive)

Process every **review comment** on the current PR one by one (inline comments on the diff). If the user asks to go by **commits** instead, list commits with `git log $(gh pr view --json baseRefOid -q .baseRefOid)..HEAD --oneline` and process comments or changes per commit in the same interactive way. For each comment: (1) include a **clickable link** to the comment (`html_url`), (2) a subagent validates the concern and proposes a fix, (3) the **pr-comment-responder** subagent drafts a reply (with quoted original and link), (4) you explain and show the draft to the user; post the reply on GitHub only if the user explicitly asks.

## Prerequisites

- GitHub CLI installed and authenticated (`gh auth status`)
- Current directory is the repo, or PR number/URL is provided

## Workflow

### Step 1: Identify the PR and fetch comments

If the user did not specify a PR:

- Detect current branch and find its PR: `gh pr view --json number,url 2>/dev/null`
- If none: ask for PR number or URL

Then get repo and list **all review comments** (inline comments on the PR):

```bash
# Repo and PR number (from URL or current branch)
gh pr view --json number,baseRepository --jq '{number: .number, owner: .baseRepository.owner.login, repo: .baseRepository.name}'

# List all review comments (response includes id, html_url, path, line, body, user, etc.)
gh api "repos/{owner}/{repo}/pulls/{pull_number}/comments" --paginate
```

Optional: get the diff for context when explaining:

```bash
gh pr diff
```

### Step 2: Confirm scope with the user (interactive)

Before processing, **ALWAYS use the AskQuestion tool:**

- Title: "Review Comment Scope"
- Question: "Found [N] review comments on this PR. I'll go through them one by one, explain each, and propose fixes without replying on GitHub. Which comments would you like to process?"
- Options:
  - id: "all", label: "Process all comments"
  - id: "unresolved", label: "Only unresolved comments (if available)"
  - id: "abort", label: "Abort"

Based on the response:

- "all" → Process all comments one by one
- "unresolved" → Filter to unresolved comments if API supports it, otherwise process all
- "abort" → Stop the workflow

Then proceed one comment at a time.

### Step 3: For each comment (one by one)

For **each** review comment:

1. **Show the user which comment you’re on and include a clickable link**
   - e.g. “**Comment 2 of 7** — [View comment on GitHub](html_url)” and the file/line (and author if useful).
   - Use the comment’s `html_url` from the API so the user can open the thread in one click.

2. **Spawn the evaluation subagent** with a focused task. Pass:
   - The comment text
   - The file path and line (and surrounding code from the diff or from the repo)
   - Instruction: “Determine if this is a valid concern and whether the author should fix it. If yes, propose a concrete fix (code or steps). If no, explain why the comment is not valid or why we should not change code.”

3. **Explain to the user (the prompter)**:
   - What the reviewer said (short summary)
   - Whether the subagent considers it a **valid concern** and **should fix** (yes/no and brief reason)
   - **Proposed fix**: exact code or steps, or “No change recommended” with a short explanation

4. **Invoke the pr-comment-responder subagent** to draft the reply. Pass:
   - **comment_body**: the reviewer’s comment text
   - **comment_url**: the comment’s `html_url` from the API
   - **outcome**: e.g. “We applied the fix.” / “No code change; reason: …” / “Answer: …” (from the evaluation)
     The agent returns a formatted block with the link, quoted original, and **Reply:** text. Show that full block to the user.

5. **Show the draft reply** (the pr-comment-responder output) to the user, then **ALWAYS use the AskQuestion tool:**
   - Title: "Comment [N] of [M] - Next Steps"
   - Question: "Here's the proposed fix and draft reply. What would you like to do?"
   - Options:
     - id: "apply", label: "Apply the proposed fix"
     - id: "post", label: "Post the reply on GitHub"
     - id: "both", label: "Apply fix AND post reply"
     - id: "skip", label: "Skip this comment"
     - id: "adjust", label: "Let me adjust something"

   Based on the response:
   - "apply" → Apply the fix, then continue to next comment
   - "post" → Post only the reply body (the line after **Reply:** in the subagent output) via the API (see "Posting a reply" below), then continue
   - "both" → Apply fix AND post reply, then continue
   - "skip" → Move to next comment without changes
   - "adjust" → Wait for user guidance, then ask again

6. Repeat until all comments are processed.

### Step 4: Wrap-up

- Summarize: how many comments were processed, how many had proposed fixes, how many were “no change” or skipped, and how many replies were posted (if any)
- If any draft replies were not posted, remind the user they can copy them from the chat or ask to post later

## Subagent prompt (per comment)

When spawning the subagent, pass something like:

```
You are evaluating a single PR review comment.

Comment from reviewer:
---
<comment body>
---

Relevant code (file: <path>, line: <line>):
<snippet or link to file>

Tasks:
1. Decide if this is a valid concern (e.g. correct, relevant, and actionable).
2. Decide if the author should fix it (e.g. blocking vs nit vs out of scope).
3. If they should fix it: propose a concrete fix (code or clear steps).
4. If they should not: explain why in one or two sentences.

Output your conclusion and proposed fix (or “No change recommended” with reason) in a short, structured form for the main agent to relay to the user. Do not post anything to GitHub.
```

## Using the pr-comment-responder subagent

**Always use the pr-comment-responder subagent** to draft the reply for each comment. Invoke it with:

- **comment_body**: the reviewer's comment text (from the API `body` field)
- **comment_url**: the comment's `html_url` from the API
- **outcome**: one of: "We applied the fix." / "No code change; reason: <short reason>." / "Answer: <short answer>." (based on the evaluation subagent result)

The subagent returns a formatted block with a link to the comment, the original in a quote, and a **Reply:** line. Show that full block to the user. When posting via the API, use only the reply body (the text after **Reply:**).

## Posting a reply

Only when the user explicitly asks to post the reply, call the GitHub API (create a new comment that is a reply to the existing one):

```bash
# Reply to a specific review comment (need owner, repo, pull_number, comment_id from context)
gh api "repos/{owner}/{repo}/pulls/{pull_number}/comments" \
  --method POST \
  -f body="<reply body only: the line after **Reply:** from pr-comment-responder output>" \
  -f in_reply_to="<comment_id>"
```

If the user does not ask to post, do not call this API; just show the draft so they can copy or post manually.

## What not to do

- **Do not** post replies to comments unless the user explicitly asks to post.
- **Do not** batch multiple comments into one subagent call; do one comment per evaluation subagent and one per pr-comment-responder invocation.

## Optional: filter by “unresolved”

If the user only wants unresolved comments, check whether the API or `gh` supports it (e.g. some endpoints return `in_reply_to_id` or resolution status). If supported, filter the list before Step 3 so you only iterate over unresolved comments.

## Summary checklist

- [ ] PR identified (current branch or user-provided)
- [ ] All (or filtered) review comments fetched (include `id`, `html_url`, path, line, body)
- [ ] User informed of count and process (one by one; replies only if they ask to post)
- [ ] For each comment: show **[Comment N of M](html_url)** → evaluation subagent → explain + proposed fix → **pr-comment-responder** subagent → show draft (link + quote + reply) → pause (apply fix? post reply?)
- [ ] Post reply via API only when user explicitly asks
- [ ] Wrap-up summary given at the end
