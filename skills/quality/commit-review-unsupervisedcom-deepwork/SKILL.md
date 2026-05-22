---
name: commit.review
description: "Reviews changed code for issues, DRY opportunities, naming clarity, and test coverage using a sub-agent. Use as the first step before testing."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            Verify the code review is complete:
            1. Changed files were identified
            2. Sub-agent reviewed the code for general issues, DRY opportunities, naming clarity, and test coverage
            3. All identified issues were addressed or documented as intentional
            If ALL criteria are met, include `<promise>✓ Quality Criteria Met</promise>`.

  SubagentStop:
    - hooks:
        - type: prompt
          prompt: |
            Verify the code review is complete:
            1. Changed files were identified
            2. Sub-agent reviewed the code for general issues, DRY opportunities, naming clarity, and test coverage
            3. All identified issues were addressed or documented as intentional
            If ALL criteria are met, include `<promise>✓ Quality Criteria Met</promise>`.

---

# commit.review

**Step 1/4** in **commit** workflow

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
   - `prompt`: Include the list of changed files and the review criteria below

   The sub-agent should review each changed file for:

   **General Issues**
   - Logic errors or potential bugs
   - Error handling gaps
   - Security concerns
   - Performance issues

   **DRY Opportunities**
   - Duplicated code that should be extracted into functions
   - Repeated patterns that could be abstracted
   - Copy-pasted logic with minor variations

   **Naming Clarity**
   - Variables, functions, and classes should have clear, descriptive names
   - Names should reflect purpose and intent
   - Avoid abbreviations that aren't universally understood
   - Consistent naming conventions throughout

   **Test Coverage**
   - New functions or classes should have corresponding tests
   - New code paths should be tested
   - Edge cases should be covered
   - If tests are missing, note what should be tested

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

## Example Sub-Agent Prompt

```
Review the following changed files for code quality issues:

Files to review:
- src/module.py
- src/utils.py
- tests/test_module.py

For each file, check for:

1. **General issues**: Logic errors, bugs, error handling gaps, security concerns
2. **DRY opportunities**: Duplicated code, repeated patterns that should be extracted
3. **Naming clarity**: Are variable/function/class names clear and descriptive?
4. **Test coverage**: Does new functionality have corresponding tests?

Read each file and provide a structured report of issues found, organized by category.
For each issue, include:
- File and line number
- Description of the issue
- Suggested fix

If no issues are found in a category, state that explicitly.
```

## Quality Criteria

- Changed files were identified
- Sub-agent reviewed all changed files
- Issues were categorized (general, DRY, naming, tests)
- All identified issues were addressed or documented as intentional
- Sub-agent was used to conserve context
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Context

This is the first step of the commit workflow. Code review happens before tests to catch quality issues early. The sub-agent approach keeps the main conversation context clean while providing thorough review coverage.


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
- `code_reviewed`

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
2. Inform user: "Step 1/4 complete, outputs: code_reviewed"
3. **Continue workflow**: Use Skill tool to invoke `/commit.test`

---

**Reference files**: `.deepwork/jobs/commit/job.yml`, `.deepwork/jobs/commit/steps/review.md`