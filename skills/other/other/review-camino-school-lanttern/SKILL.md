---
description: Review the current branch locally against Lanttern's code quality standards before opening a PR. Usage: /review [base-branch] [--issues #12,#34]
---

## Your task

You are an expert code reviewer specializing in Phoenix/Elixir applications, with deep knowledge of the Lanttern educational assessment platform's codebase, patterns, and quality standards.

The user has invoked `/review`. This is a **pre-PR local review** — the goal is to catch issues before the PR is opened. Parse the user's input for:

- **Base branch** (optional): the branch to diff against. Defaults to `main` if not provided.
- **GitHub issues** (optional): one or more issue numbers passed via `--issues` (e.g. `--issues #12,#34` or `--issues 12 34`). These represent the issues this change intends to resolve.

**Display the review in the terminal only — do NOT post comments, create GitHub issues, or push/write to any remote repository.**

### Step 1 — Identify branches

Run:

```
git branch --show-current
```

This gives you `headBranch`. The base branch is either what the user provided or `main`.

### Step 2 — Fetch base branch

Ensure the base branch is up to date:

```
git fetch origin <baseBranch>
```

### Step 3 — Build diff context

```
git diff origin/<baseBranch>...<headBranch>
git diff origin/<baseBranch>...<headBranch> --name-only
git diff origin/<baseBranch>...<headBranch> --stat -- 'lib/**'
git log origin/<baseBranch>..<headBranch> --oneline
```

### Step 4 — GitHub issues context (if provided)

If the user supplied issue numbers, fetch each issue's title and body for context:

```
gh issue view <number> --json number,title,body
```

Use this to understand the intent behind the change and verify the implementation addresses the described problem or feature.

### Step 5 — Apply the review checklist

Read the shared checklist file at `.claude/skills/review-checklist.md` and apply it in full.

**Framing guidance for this skill**: The overall assessment in the Overview section should be framed as one of:
- "Ready to open as a PR"
- "Needs minor changes before opening"
- "Needs significant changes before opening"

**IMPORTANT**: Output the review to the terminal only. Do not use `gh` or `git` in write mode. Do not push, comment, or create anything on the remote.
