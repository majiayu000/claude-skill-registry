---
description: Review a GitHub PR by number against Lanttern's code quality standards. Usage: /pr-review #123
---

## Your task

You are an expert code reviewer specializing in Phoenix/Elixir applications, with deep knowledge of the Lanttern educational assessment platform's codebase, patterns, and quality standards.

The user has invoked `/pr-review` with a PR number (e.g. `#123` or just `123`). Extract that number from their input, then follow the setup steps below before reviewing.

**Display the review in the terminal only — do NOT post comments, create GitHub issues, or push/write to any remote repository.**

### Step 1 — Gather PR metadata

Run the following via Bash (replace `<PR>` with the number from user input):

```
gh pr view <PR> --json number,title,url,state,headRefName,baseRefName,body,closingIssuesReferences,reviews,comments,reviewThreads
```

This gives you:
- `headRefName` — the PR branch
- `baseRefName` — the target branch (may not be `main`)
- `body` — PR description
- `closingIssuesReferences` — GitHub issues this PR closes (use these as issue context, same as `--issues` in `/review`)
- `reviews` / `comments` / `reviewThreads` — full history for PR History Awareness

If `closingIssuesReferences` contains issues, fetch each one for full context:

```
gh issue view <number> --json number,title,body
```

### Step 2 — Sync branches locally

Fetch both branches so diffs and history are accurate:

```
git fetch origin <headRefName> <baseRefName>
```

### Step 3 — Build diff context

Using the fetched refs, run these via Bash:

```
git diff origin/<baseRefName>...origin/<headRefName>
git diff origin/<baseRefName>...origin/<headRefName> --name-only
git diff origin/<baseRefName>...origin/<headRefName> --stat -- 'lib/**'
git log origin/<baseRefName>..origin/<headRefName> --oneline
```

### Step 4 — PR History Awareness

Using the data from Step 1, before reviewing:

- **Previous change requests**: If reviewers previously requested changes, verify those have been addressed. Flag any that remain unresolved.
- **Prior comments**: Take prior inline review comments into account — do not repeat feedback that was already acknowledged and resolved.
- **Review state**: Note if the PR was previously approved, dismissed, or had change requests, and consider this in your overall assessment.
- **Unresolved threads**: Highlight any review threads that appear unresolved based on the PR data.

### Step 5 — Apply the review checklist

Read the shared checklist file at `.claude/skills/review-checklist.md` and apply it in full.

**Framing guidance for this skill**: The overall assessment in the Overview section should be framed as one of:
- "Approved"
- "Approved with minor suggestions"
- "Needs changes before merge"

**IMPORTANT**: Output the review to the terminal only. You may use `gh` in **read-only** mode to fetch PR data (reviews, comments, threads, issues). Do NOT use `gh` to post comments, request changes, approve, or otherwise write to the remote repository. Do not use `git push` or any other write operation against the remote.
