---
name: commit.lint
description: "Formats and lints code with ruff using a sub-agent. Use after tests pass to ensure code style compliance."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            Verify the linting is complete:
            1. ruff format was run successfully
            2. ruff check was run successfully (with --fix)
            3. No remaining lint errors
            If ALL criteria are met, include `<promise>✓ Quality Criteria Met</promise>`.

  SubagentStop:
    - hooks:
        - type: prompt
          prompt: |
            Verify the linting is complete:
            1. ruff format was run successfully
            2. ruff check was run successfully (with --fix)
            3. No remaining lint errors
            If ALL criteria are met, include `<promise>✓ Quality Criteria Met</promise>`.

---

# commit.lint

**Step 3/4** in **commit** workflow

> Reviews code, runs tests, lints, and commits changes. Use when ready to commit work with quality checks.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/commit.test`

## Instructions

**Goal**: Formats and lints code with ruff using a sub-agent. Use after tests pass to ensure code style compliance.

# Lint Code

## Objective

Format and lint the codebase using ruff to ensure code quality and consistency.

## Task

Run ruff format and ruff check to format and lint the code. This step should be executed using a sub-agent to conserve context in the main conversation.

### Process

**IMPORTANT**: Use the Task tool to spawn a sub-agent for this work. This saves context in the main conversation. Use the `haiku` model for speed.

1. **Spawn a sub-agent to run linting**

   Use the Task tool with these parameters:
   - `subagent_type`: "Bash"
   - `model`: "haiku"
   - `prompt`: See below

   The sub-agent should:

   a. **Run ruff format**
      ```bash
      ruff format .
      ```
      This formats the code according to ruff's style rules.

   b. **Run ruff check with auto-fix**
      ```bash
      ruff check --fix .
      ```
      This checks for lint errors and automatically fixes what it can.

   c. **Run ruff check again to verify**
      ```bash
      ruff check .
      ```
      Capture the final output to verify no remaining issues.

2. **Review sub-agent results**
   - Check that both format and check completed successfully
   - Note any remaining lint issues that couldn't be auto-fixed

3. **Handle remaining issues**
   - If there are lint errors that couldn't be auto-fixed, fix them manually
   - Re-run ruff check to verify

## Example Sub-Agent Prompt

```
Run ruff to format and lint the codebase:

1. Run: ruff format .
2. Run: ruff check --fix .
3. Run: ruff check . (to verify no remaining issues)

Report the results of each command.
```

## Quality Criteria

- ruff format was run successfully
- ruff check was run with --fix flag
- No remaining lint errors (or all are documented and intentional)
- Sub-agent was used to conserve context
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Context

This step ensures code quality and consistency before committing. It runs after tests pass and before the commit step. Using a sub-agent keeps the main conversation context clean for the commit review.


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
- `code_formatted`

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
2. Inform user: "Step 3/4 complete, outputs: code_formatted"
3. **Continue workflow**: Use Skill tool to invoke `/commit.commit_and_push`

---

**Reference files**: `.deepwork/jobs/commit/job.yml`, `.deepwork/jobs/commit/steps/lint.md`