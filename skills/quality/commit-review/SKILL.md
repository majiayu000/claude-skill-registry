---
name: commit.review
description: "Reviews changed code for issues, DRY opportunities, naming clarity, and test coverage using a sub-agent. Use as the first step before testing."
user-invocable: false

---

# commit.review

**Step 1/4** in **full** workflow

> Full commit workflow: review, test, lint, and commit

> Reviews code, runs tests, lints, and commits changes. Use when ready to commit work with quality checks.


## Instructions

**Goal**: Reviews changed code for issues, DRY opportunities, naming clarity, and test coverage using a sub-agent. Use as the first step before testing.

# Code Review

## Objective

Review changed code for quality issues before running tests. This catches problems early and ensures code meets quality standards.

## Task

Use a sub-agent to review the staged/changed code and identify issues that should be fixed before committing.

### Process

**IMPORTANT**: Use the Task tool to spawn a sub-agent for this review. This saves context in the main conversation.

1. **Get the list of changed files**
   ```bash
   git diff --name-only HEAD
   git diff --name-only --staged
   ```
   Combine these to get all files that have been modified.

2. **Spawn a sub-agent to review the code**

   Use the Task tool with these parameters:
   - `subagent_type`: "general-purpose"
   - `prompt`: Instruct the sub-agent to:
     - Read the code review standards from `doc/code_review_standards.md`
     - Read each of the changed files
     - Review each file against the standards
     - Report issues found with file, line number, severity, and suggested fix

3. **Review sub-agent findings**
   - Examine each issue identified
   - Prioritize issues by severity

4. **Fix identified issues**
   - Address each issue found by the review
   - For DRY violations: extract shared code into functions/modules
   - For naming issues: rename to be clearer
   - For missing tests: add appropriate test cases
   - For bugs: fix the underlying issue

5. **Re-run review if significant changes made**
   - If you made substantial changes, consider running another review pass
   - Ensure fixes didn't introduce new issues

## Quality Criteria

- Changed files were identified
- Sub-agent read the code review standards and reviewed all changed files
- All identified issues were addressed or documented as intentional

## Context

This is the first step of the commit workflow. Code review happens before tests to catch quality issues early. The sub-agent approach keeps the main conversation context clean while providing thorough review coverage.


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
- `code_reviewed`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

**Before completing this step, you MUST have your work reviewed against the quality criteria below.**

Use a sub-agent (Haiku model) to review your work against these criteria:

**Criteria (all must be satisfied)**:
1. Changed files were identified
2. Sub-agent reviewed the code for general issues, DRY opportunities, naming clarity, and test coverage
3. All identified issues were addressed or documented as intentional
**Review Process**:
1. Once you believe your work is complete, spawn a sub-agent using Haiku to review your work against the quality criteria above
2. The sub-agent should examine your outputs and verify each criterion is met
3. If the sub-agent identifies valid issues, fix them
4. Have the sub-agent review again until all valid feedback has been addressed
5. Only mark the step complete when the sub-agent confirms all criteria are satisfied

## On Completion

1. Verify outputs are created
2. Inform user: "full step 1/4 complete, outputs: code_reviewed"
3. **Continue workflow**: Use Skill tool to invoke `/commit.test`

---

**Reference files**: `.deepwork/jobs/commit/job.yml`, `.deepwork/jobs/commit/steps/review.md`