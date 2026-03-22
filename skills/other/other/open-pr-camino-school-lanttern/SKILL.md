---
description: Run precommit checks, write a PR description, get approval, and open the PR on GitHub. Usage: /open-pr [base-branch] (e.g. /open-pr main)
---

## Your task

The user may have specified a base branch in their invocation (e.g. `/open-pr main` or `/open-pr develop`).

- If a base branch was provided, use it.
- If no base branch was provided, ask the user: "Which branch should this PR target? (e.g. main, develop)"

Do not proceed until you have the base branch confirmed.

Once you have the base branch, also confirm the current branch by running:

```
git branch --show-current
```

---

### Step 1 — Gather diff context

Using the confirmed base branch, run:

```
git log <base-branch>..HEAD --oneline
git diff <base-branch>..HEAD --name-only
git diff <base-branch>..HEAD
```

---

### Step 2 — Run precommit checks

Run `mix precommit` to verify the code compiles cleanly, passes Credo strict analysis, and all tests pass.

```
mix precommit
```

If `mix precommit` fails, **stop immediately** and report the failures to the user. Do not proceed to writing the PR description until all issues are resolved.

---

### Step 3 — Write the PR description

Using the diff context gathered in Step 1, extract:

- The main purpose of the changes
- Which parts of the system are affected
- Whether this is a feature, fix, refactor, or other type of change
- Any issue numbers referenced in commit messages or branch name (e.g. branch `452-link-staff-member-to-classes` → issue #452)

Craft a comprehensive PR description following these principles:

- Focus on WHAT was implemented and WHY, not HOW
- Write in present tense and active voice
- Be specific about functionality (e.g. "Adds support for linking staff members to classes" not "Updates staff members")
- Consider the educational domain (student/teacher/admin experience, assessment, learning management)

Use this structure:

```
### Summary

A brief 1-2 sentence overview of what this PR accomplishes.

### Related Issues

- Closes #[issue-number]

### What This PR Does

A clear explanation of the functionality added, changed, or fixed:

- New features or capabilities introduced
- Problems solved or bugs fixed
- Improvements to existing functionality
- User-facing changes

### Impact and Scope

- Which parts of the system are affected
- Which features or modules are touched
- Any breaking changes or migration requirements

### Testing Considerations

(Include if relevant)

- Key scenarios covered by tests
- Edge cases considered

### Additional Notes

(Include if relevant)

- Deployment considerations
- Follow-up tasks

---

Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

---

### Step 4 — Ask for approval

Present the full PR description to the user and ask:

> Does this PR description look good? Reply **yes** to open the PR, or provide feedback to revise it.

Do not proceed until the user approves. If they provide feedback, revise the description and ask again.

---

### Step 5 — Create the PR

Once approved, run:

```
gh pr create --base <base-branch> --title "<summary line>" --body "<approved description>"
```

Use the Summary line as the PR title. After the PR is created, display the PR URL to the user.
