---
name: commit.commit_and_push
description: "Verifies changed files, creates commit, and pushes to remote. Use after linting passes to finalize changes."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            Verify the commit is ready:
            1. Changed files list was reviewed by the agent
            2. Files match what was modified during this session (or unexpected changes were investigated)
            3. Commit was created with appropriate message
            4. Changes were pushed to remote
            If ALL criteria are met, include `<promise>✓ Quality Criteria Met</promise>`.

  SubagentStop:
    - hooks:
        - type: prompt
          prompt: |
            Verify the commit is ready:
            1. Changed files list was reviewed by the agent
            2. Files match what was modified during this session (or unexpected changes were investigated)
            3. Commit was created with appropriate message
            4. Changes were pushed to remote
            If ALL criteria are met, include `<promise>✓ Quality Criteria Met</promise>`.

---

# commit.commit_and_push

**Step 4/4** in **commit** workflow

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

   If changes match expectations, proceed to commit.

   If there are unexpected changes:
   - Investigate why (e.g., lint auto-fixes, generated files)
   - If they're legitimate side effects of your work, include them
   - If they're unrelated or shouldn't be committed, use `git restore` to discard them

3. **Stage all appropriate changes**
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

   ```bash
   git commit -m "commit message here"
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

- Changed files list was reviewed by the agent
- Files match what was modified during this session (or unexpected changes were investigated and handled)
- Commit message follows project conventions
- Commit was created successfully
- Changes were pushed to remote
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Context

This is the final step of the commit workflow. The agent verifies that the changed files match its own expectations from the work done during the session, then commits and pushes. This catches unexpected changes while avoiding unnecessary user interruptions.


### Job Context

A workflow for preparing and committing code changes with quality checks.

This job starts with a code review to catch issues early, runs tests until
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

Stop hooks will automatically validate your work. The loop continues until all criteria pass.



**To complete**: Include `<promise>✓ Quality Criteria Met</promise>` in your final response only after verifying ALL criteria are satisfied.

## On Completion

1. Verify outputs are created
2. Inform user: "Step 4/4 complete, outputs: changes_committed"
3. **Workflow complete**: All steps finished. Consider creating a PR to merge the work branch.

---

**Reference files**: `.deepwork/jobs/commit/job.yml`, `.deepwork/jobs/commit/steps/commit_and_push.md`