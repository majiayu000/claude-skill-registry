---
name: auto-fix-bug
description: Fix a reported bug end-to-end: reproduce it, add a regression test, implement the minimal fix, create a new git branch, commit using Conventional Commits, push, and open a GitHub PR (prefer gh CLI). Use when the user asks to fix a bug and wants a PR created.
---

# Auto Bugfix → Branch + Commit + PR (GitHub)

**Role:** Fix a reported bug end-to-end and deliver a new branch, commit(s), and an open GitHub Pull Request.

**Non-negotiable outcome:** When this skill is used, you MUST deliver:
1. A **new branch** with the fix.
2. At least one **commit** (Conventional Commits).
3. A **GitHub Pull Request** opened from that branch.

If you cannot create the PR automatically (missing permissions, no `gh`), push the branch and output the exact manual steps to create the PR in the GitHub UI.

---

## 1. Inputs to Collect

Prefer no back-and-forth. If missing, infer from repo conventions; otherwise ask only the minimum.

**Collect:**
- Bug description and expected behavior.
- How to reproduce: steps, endpoint, failing test, or error log.
- Related issue/PR link (if exists).
- Target base branch (default: `master` or `main` based on repo).

---

## 2. Workflow (Strict Order)

### 2.1 Reproduce the bug

**Do:**
- Identify the failing behavior locally (tests, reproduction steps, logs).
- If a test suite exists, find the closest relevant test and run it first.

### 2.2 Add a regression test

**Do:**
- Add or adjust a test that fails **before** the fix and passes **after** the fix.
- Keep the test minimal and focused on the reported bug.

### 2.3 Create a new branch

**Branch naming:** Prefer `fix/<short-slug>` or `bugfix/<ticket>-<slug>` if a ticket id exists.

**Do:**
- Run `git status` (must be clean, or explicitly explain what you are doing).
- Run `git checkout -b fix/<slug>` (or equivalent).

### 2.4 Implement the minimal fix

**Do:**
- Smallest change that makes the regression test pass.
- Avoid drive-by refactors unless required to fix the bug.
- Keep public APIs stable unless the bug is explicitly an API change.

### 2.5 Run checks locally

**Do:** Run the fastest relevant subset first, then the full suite when reasonable.
- Tests: single file or targeted, then full.
- Lints and static analysis if available.

If something fails, fix it before committing.

### 2.6 Commit (Conventional Commits)

**Rules:**
- Follow Conventional Commits.
- For bugfixes default to `fix:` or `fix(scope):`.
- Message should describe user-visible outcome, not implementation detail.
- Add commit message by defined rules and GitHub automatically creates a link to the mentioned issue. For example, if your issue number is 123 , you can mention it in your PR like this: #123

**Examples:**
- `fix(auth): prevent token refresh race condition`
- `fix: handle null customer id in webhook handler`

**Do:**
- `git add -A`
- `git commit -m "fix(<scope>): <summary>"`

### 2.7 Push branch

**Do:**
- `git push -u origin fix/<slug>`

Do not force-push unless the user explicitly asks.

### 2.8 Create PR in GitHub

**Prefer GitHub CLI:**
- `gh pr create --base <base> --head fix/<slug> --title "<title>" --body "<body>"`

**PR title:** Same as commit subject (without scope is ok); keep it short.

**PR body template (fill it):**
- **What/Why:** 1–3 bullets.
- **Repro:** Steps or link to failing case.
- **Fix:** What changed.
- **Tests:** Exact commands run.
- **Risk:** Any edge cases or migration notes.
- **Links:** `closes #ID` (if applicable).

### 2.9 Final verification

**Do:**
- Ensure the PR is open and points to the correct base branch.
- Ensure the branch contains commit(s) and CI can run.

---

## 3. Guardrails

**Do not:**
- Commit secrets, tokens, or credentials.
- Change formatting project-wide.
- “Fix” unrelated warnings opportunistically.

**Do:** If you touch production-critical paths, add extra tests.

---

## 4. If `gh` Is Unavailable

**Do:**
1. Push the branch.
2. Print instructions: PR URL format hint (repo + compare branch), base branch to select, title/body to paste.
