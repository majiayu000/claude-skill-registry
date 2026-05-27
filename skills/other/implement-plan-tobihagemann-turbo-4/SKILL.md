---
name: implement-plan
description: "Execute an implementation plan file produced by $draft-plan, $turboplan, or $expand-shell. Runs pre-implementation prep, then runs $implement to execute the steps and finalize. Use when the user asks to \"implement plan\", \"implement the plan\", \"execute the plan\", \"run the plan\", \"implement plans/<slug>.md\", \"start implementing the plan\", or starts a fresh session to implement a previously drafted plan."
---

# Implement Plan

Execute an implementation plan file.

## Task Tracking

At the start, use `update_plan` to track each step:

1. Resolve and read the plan file
2. Read context files
3. Run `$implement` skill
4. Update plan status

## Step 1: Resolve and Read the Plan File

Determine which plan file to implement using these rules in order:

1. **Explicit path** — If an absolute or relative path was passed, use it
2. **Explicit slug** — If a slug was passed (e.g., `add-image-cache`), resolve to `.turbo/plans/<slug>.md` if that file exists; otherwise fall through to rule 5 before erroring
3. **Single file** — Glob `.turbo/plans/*.md`. If exactly one plan exists, use it
4. **Most recent** — If multiple plans exist, use the most recently modified
5. **Unexpanded shell** — If a slug or path was passed but resolved to no plan, derive `<slug>` from the basename (stripping `.md`) and check `.turbo/shells/<slug>.md`. If it exists, halt with: "`<slug>` is a shell that needs expansion first. Run `$pick-next-shell` to expand and implement it."
6. **Legacy fallback** — If `.turbo/plans/` does not exist but `.turbo/plan.md` exists, use it
7. **Nothing found** — If no plan matched any rule above, tell the user to run `$turboplan` (for a new task) or `$pick-next-shell` (for existing shells) and stop

If multiple plans exist and the most-recent choice is non-obvious (e.g., several plans were modified within the same minute), use `request_user_input` to let the user pick from the candidates.

State the resolved plan path before continuing, then read the file.

## Step 2: Read Context Files

Read in full:

- Every file listed in the plan's **Context Files** section
- Files the user referenced in their original request (if any)
- Every file path the plan references in the Context, Pattern Survey, and Implementation Steps sections

## Step 3: Run `$implement` Skill

Run the `$implement` skill. The plan file, its file references, and its Verification section are already in conversation context from Step 1.

## Step 4: Update Plan Status

After `$implement` completes, set the plan's frontmatter `status:` to `done`. If the plan is the legacy `.turbo/plan.md` without frontmatter, skip this step.

Then update or check the active plan and proceed to any remaining task.

## Rules

- The plan file is read-only during execution. If revisions are needed, run `$refine-plan` or `$draft-plan` separately.
- Never skip Step 2.
- Never enumerate or execute the plan's Implementation Steps inline. The work runs through `$implement`. Restating steps as a turn-level narration counts as inline execution and bypasses the delegation.
- If the plan's Implementation Steps or Verification include `git commit`, `git push`, or PR creation, halt before Step 3 and ask the user to remove them via `$refine-plan`.
