---
name: vigilante-issue-implementation
description: Implement a GitHub issue end-to-end when Vigilante dispatches work for a watched repository. Use the provided worktree, respect repository instructions, comment on the issue as work progresses, and report failures back to GitHub.
---

# Vigilante Issue Implementation

## Overview
Implement one GitHub issue from Vigilante dispatch through validated code changes, a pushed branch, and an opened pull request from the provided worktree. Always work inside the assigned worktree, always respect repository instructions, and always keep the GitHub issue updated with start, plan, progress, PR, and failure comments.

## Inputs
Require these inputs from Vigilante:

- issue number
- issue title and URL
- repository slug
- local repository path
- assigned worktree path
- branch name

## Workflow
1. Inspect issue and repository constraints
- Read the issue details supplied by Vigilante and confirm the issue scope before coding.
- Read development constraints from repository markdown files before making changes:
  - `AGENTS.md` when present
  - `README.md`
  - other root or area-specific docs that affect touched files
- If repository instructions conflict, follow the more specific instruction.

2. Announce session start on GitHub
- Post a comment on the issue as soon as work begins using `vigilante gh issue comment`.
- Include that Vigilante launched the session, the working branch, and that implementation is in progress.

3. Post an implementation plan early
- After inspecting the issue and repository constraints, post a concise implementation plan to the issue using `vigilante gh issue comment`.
- The plan comment should describe the intended development steps before substantial code changes begin.
- Keep the plan concrete and short so readers can understand what will happen next.

4. Implement inside the assigned worktree only
- Use only the provided worktree path.
- Never edit the root checkout when a worktree was assigned.
- Keep changes scoped to the issue.
- Prefer native repository tooling and avoid unnecessary new dependencies.
- Preserve existing coding patterns unless the issue requires a different approach.

Service dependencies:
- If app startup, migrations, or tests need local services, call the bundled `vigilante-local-service-dependencies` skill before inventing ad hoc setup steps.
- Prefer the skill's repository-native path first, and use its structured output to decide which env vars, commands, or cleanup steps the rest of the implementation should use.

5. Validate incrementally
- Run relevant tests, builds, or linters for the changed area before concluding work.
- Prefer targeted validation first, then broader validation when necessary.
- If a command fails, determine whether the problem is in the code, test setup, or environment before retrying.

6. Commit and push the branch
- Commit only issue-relevant changes in the assigned branch.
- Push the assigned branch to the remote with `vigilante git push`.
- Do not leave completed implementation work only in the local worktree.

7. Open a pull request
- Always create a pull request for the completed change set.
- Target the repository default branch unless repository instructions say otherwise.
- Include `Closes #<issue-number>` in the PR body as a required invariant.
- Include concise validation notes in the PR description.

8. Post progress comments at meaningful milestones
- Use `vigilante gh issue comment` for progress updates.
- Comment when investigation is complete and implementation starts.
- Comment when major milestones are reached, such as a core fix landing or tests passing.
- Comment when the branch has been pushed and the PR has been opened.
- Keep comments concise and factual.
- Do not spam the issue with low-signal updates.

9. Handle failures and blockers explicitly
- If tool setup fails, validation fails, or the issue is blocked, comment on the issue with the concrete problem using `vigilante gh issue comment`.
- Include enough detail for a human maintainer to understand the current state and next step.
- If work cannot proceed safely, stop and report the blocker instead of guessing.

10. Finish with a clear terminal state
- Leave the worktree in a coherent state.
- Ensure any executed validations are accurately reported.
- If the task completed successfully, summarize what changed, what was validated, and which PR was opened.
- If the task failed, summarize the failure clearly in the issue comment.

## GitHub Commenting Rules
- Use `vigilante gh issue comment` for all issue updates.
- Always comment when the session starts.
- For the coding-agent start comment, use a distinct launch title such as `## 🕹️ Coding Agent Launched: Codex` instead of a generic `Session Start` header.
- Always add a short implementation plan comment before substantial coding work begins.
- Add progress comments for non-trivial implementations as milestones are reached.
- Comment when the PR is opened.
- Comment immediately on any execution failure or blocking condition.
- Comments should be concise, concrete, and tied to real progress.
- Avoid generic status text that does not help the issue reader.

## Guardrails
- Never work outside the assigned worktree.
- Never ignore `AGENTS.md` or repository documentation that constrains implementation.
- Never make unrelated refactors unless they are required to complete the issue safely.
- Never silently fail; report errors or blockers back to the issue.
- Never claim validation passed unless the corresponding command actually succeeded.
- Never stop at local-only code changes when the task is complete; push the branch and create the PR.

## Completion Criteria
- The issue received a start comment.
- The issue received a plan comment describing the intended development steps.
- Progress or failure comments were posted as appropriate for the work performed.
- Code changes are scoped to the issue and live in the assigned worktree.
- Relevant validation was run and accurately reported.
- The branch was pushed to the remote.
- A pull request was opened for the change.
- Final session state is clear to both Vigilante and the GitHub issue reader.

## Output Expectations
When using this skill, the agent should leave:

- code changes in the assigned worktree
- a pushed branch containing those changes
- an opened pull request for those changes
- a clear issue comment trail produced through `vigilante gh issue comment`
- accurate success or failure reporting
