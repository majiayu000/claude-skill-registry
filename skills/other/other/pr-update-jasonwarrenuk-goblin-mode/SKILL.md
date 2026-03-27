---
name: pr-update
description: "{{ ƔƔƔ }} Update a PR description to account for commits made since it was last written"
model: sonnet
disable-model-invocation: true
allowed-tools: ["Bash(git:*)", "Bash(gh:*)", "Read", "Glob", "Grep"]
argument-hint: "<pr-number>"
---

Update the description of PR #$ARGUMENTS.

## Steps

### 1. Fetch current PR state

Run:
```
gh pr view $ARGUMENTS --json body,title,headRefName,baseRefName
```

### 2. Find the watermark

Look in the PR body for a comment in this exact format:
```
<!-- pr-update-watermark: <commit-sha> -->
```

If found, note the SHA — this is where the last update stopped. Call it `$WATERMARK_SHA`.

If not found, treat the entire commit history on the branch as new.

### 3. Get new commits

Run:
```
git log <baseRefName>..<headRefName> --oneline
```

If a watermark was found, filter to only commits **after** `$WATERMARK_SHA`:
```
git log ${WATERMARK_SHA}..HEAD --oneline
```

If there are no new commits since the watermark, tell me and stop — the description is already up to date.

### 4. Analyse the new commits

For each new commit, run:
```
git show <sha> --stat
```

Understand what changed and why. Group related commits into coherent change categories.

### 5. Produce the updated PR body

Take the existing PR body and update it:

- **Do not rewrite from scratch.** Preserve existing content unless it is now inaccurate.
- Update the `## Changes` section to incorporate the new commits. If collapsible `<details>` blocks already exist, add new entries or update existing ones as appropriate.
- If the description references behaviour that has changed, correct it.
- Insert or replace the watermark comment at the very end of the body, using the SHA of the **most recent commit on the branch**:

```
<!-- pr-update-watermark: <latest-sha> -->
```

### 6. Show me the diff

Display:
- The updated PR body in full
- A brief summary of what changed vs the previous description

Wait for my approval.

### 7. Apply the update

Once approved, run:
```
gh pr edit $ARGUMENTS --body "<updated body>"
```

Confirm success.
