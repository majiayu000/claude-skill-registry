---
name: commit.test
description: "Pulls latest code and runs tests until all pass. Use after code review passes to verify changes work correctly."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            Verify the tests are passing:
            1. Latest code was pulled from the branch
            2. All tests completed successfully
            3. No test failures or errors remain
            4. Test output shows passing status
            If ALL criteria are met, include `<promise>✓ Quality Criteria Met</promise>`.

  SubagentStop:
    - hooks:
        - type: prompt
          prompt: |
            Verify the tests are passing:
            1. Latest code was pulled from the branch
            2. All tests completed successfully
            3. No test failures or errors remain
            4. Test output shows passing status
            If ALL criteria are met, include `<promise>✓ Quality Criteria Met</promise>`.

---

# commit.test

**Step 2/4** in **commit** workflow

> Reviews code, runs tests, lints, and commits changes. Use when ready to commit work with quality checks.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/commit.review`

## Instructions

**Goal**: Pulls latest code and runs tests until all pass. Use after code review passes to verify changes work correctly.

# Run Tests

## Objective

Run the project's test suite and fix any failing tests until all tests pass.

## Task

Execute the test suite for the project and iteratively fix any failures until all tests pass.

### Process

1. **Pull latest code from the branch**
   - Run `git pull` to fetch and merge any changes from the remote
   - If there are merge conflicts, resolve them before proceeding
   - This ensures you're testing against the latest code

2. **Detect or use the test command**
   - If a test command was provided, use that
   - Otherwise, auto-detect the project type and determine the appropriate test command:
     - Python: `pytest`, `python -m pytest`, `uv run pytest`
     - Node.js: `npm test`, `yarn test`, `bun test`
     - Go: `go test ./...`
     - Rust: `cargo test`
     - Check `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` for hints

3. **Run the tests**
   - Execute the test command
   - Capture the output

4. **Analyze failures**
   - If tests pass, proceed to output
   - If tests fail, analyze the failure messages
   - Identify the root cause of each failure

5. **Fix failing tests**
   - Make the necessary code changes to fix failures
   - This may involve fixing bugs in implementation code or updating tests
   - Re-run tests after each fix

6. **Iterate until passing**
   - Continue the fix/test cycle until all tests pass

## Quality Criteria

- Latest code was pulled from the branch
- Test command was correctly identified or used from input
- All tests are now passing
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Context

This step runs after code review. Tests must pass before proceeding to lint and commit. This ensures code quality and prevents broken code from being committed. If tests fail due to issues introduced by the code review fixes, iterate on the fixes until tests pass.


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


## Required Inputs

**User Parameters** - Gather from user before starting:
- **test_command**: Test command to run (optional - will auto-detect if not provided)


## Work Branch

Use branch format: `deepwork/commit-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/commit-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `tests_passing`

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
2. Inform user: "Step 2/4 complete, outputs: tests_passing"
3. **Continue workflow**: Use Skill tool to invoke `/commit.lint`

---

**Reference files**: `.deepwork/jobs/commit/job.yml`, `.deepwork/jobs/commit/steps/test.md`