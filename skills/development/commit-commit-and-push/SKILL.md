---
name: commit.commit_and_push
description: "Verifies changed files, creates commit, and pushes to remote. Use after linting passes to finalize changes."
user-invocable: false

---

# commit.commit_and_push

**Step 4/4** in **full** workflow

> Full commit workflow: review, test, lint, and commit

> Reviews code, runs tests, lints, and commits changes. Use when ready to commit work with quality checks.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/commit.lint`

## Instructions

**Goal**: Verifies changed files, creates commit, and pushes to remote. Use after linting passes to finalize changes.

# Commit and Push

## Objective

Review the changed files to verify they match the agent's expectations, create a commit with an appropriate message, and push to the remote repository.

## Task

Check the list of changed files against what was modified during this session, ensure they match expectations, then commit and push the changes.

### Process

1. **Get the list of changed files**
   ```bash
   git status
   ```
   Also run `git diff --stat` to see a summary of changes.

2. **Verify changes match expectations**

   Compare the changed files against what you modified during this session:
   - Do the modified files match what you edited?
   - Are there any unexpected new files?
   - Are there any unexpected deleted files?
   - Do the line counts seem reasonable for the changes you made?

   If changes match expectations, proceed to the next step.

   If there are unexpected changes:
   - Investigate why (e.g., lint auto-fixes, generated files)
   - If they're legitimate side effects of your work, include them
   - If they're unrelated or shouldn't be committed, use `git restore` to discard them

3. **Update CHANGELOG.md if needed**

   If your changes include new features, bug fixes, or other notable changes:
   - Add entries to the `## [Unreleased]` section of CHANGELOG.md
   - Use the appropriate subsection: `### Added`, `### Changed`, `### Fixed`, or `### Removed`
   - Write concise descriptions that explain the user-facing impact

   **CRITICAL: NEVER modify version numbers**
   - Do NOT change the version in `pyproject.toml`
   - Do NOT change version headers in CHANGELOG.md (e.g., `## [0.4.2]`)
   - Do NOT rename the `## [Unreleased]` section
   - Version updates are handled by the release workflow, not commits

4. **Stage all appropriate changes**
   ```bash
   git add -A
   ```
   Or stage specific files if some were excluded.

5. **View recent commit messages for style reference**
   ```bash
   git log --oneline -10
   ```

6. **Create the commit**

   Generate an appropriate commit message based on:
   - The changes made
   - The style of recent commits
   - Conventional commit format if the project uses it

   **IMPORTANT:** Use the commit job script (not `git commit` directly):
   ```bash
   .claude/hooks/commit_job_git_commit.sh -m "commit message here"
   ```

7. **Push to remote**
   ```bash
   git push
   ```
   If the branch has no upstream, use:
   ```bash
   git push -u origin HEAD
   ```

## Quality Criteria

- Changed files were verified against expectations
- CHANGELOG.md was updated with entries in [Unreleased] section (if changes warrant documentation)
- Version numbers were NOT modified (pyproject.toml version and CHANGELOG version headers unchanged)
- Commit was created with appropriate message
- Changes were pushed to remote

## Context

This is the final step of the commit workflow. The agent verifies that the changed files match its own expectations from the work done during the session, then commits and pushes. This catches unexpected changes while avoiding unnecessary user interruptions.


### Job Context

A workflow for preparing and committing code changes with quality checks.

The **full** workflow starts with a code review to catch issues early, runs tests until
they pass, formats and lints code with ruff, then reviews changed files
before committing and pushing. The review and lint steps use sub-agents
to reduce context usage.

Steps:
1. review - Code review for issues, DRY opportunities, naming, and test coverage (runs in sub-agent)
2. test - Pull latest code and run tests until they pass
3. lint - Format and lint code with ruff (runs in sub-agent)
4. commit_and_push - Review changes and commit/push



## Work Branch

Use branch format: `deepwork/commit-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/commit-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `changes_committed`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

**Before completing this step, you MUST have your work reviewed against the quality criteria below.**

Use a sub-agent (Haiku model) to review your work against these criteria:

**Criteria (all must be satisfied)**:
1. Changed files were verified against expectations
2. CHANGELOG.md was updated with entries in [Unreleased] section (if changes warrant documentation)
3. Version numbers were NOT modified (pyproject.toml version and CHANGELOG version headers unchanged)
4. Commit was created with appropriate message
5. Changes were pushed to remote
**Review Process**:
1. Once you believe your work is complete, spawn a sub-agent using Haiku to review your work against the quality criteria above
2. The sub-agent should examine your outputs and verify each criterion is met
3. If the sub-agent identifies valid issues, fix them
4. Have the sub-agent review again until all valid feedback has been addressed
5. Only mark the step complete when the sub-agent confirms all criteria are satisfied

## On Completion

1. Verify outputs are created
2. Inform user: "full step 4/4 complete, outputs: changes_committed"
3. **full workflow complete**: All steps finished. Consider creating a PR to merge the work branch.

---

**Reference files**: `.deepwork/jobs/commit/job.yml`, `.deepwork/jobs/commit/steps/commit_and_push.md`