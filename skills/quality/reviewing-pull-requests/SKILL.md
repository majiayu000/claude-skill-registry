---
name: reviewing-pull-requests
description: Use this skill to run a comprehensive pull request review using multiple specialized agents. Each agent focuses on a different aspect of code quality, such as comments, tests, error handling, type design, and general code review. The skill aggregates results and provides a clear action plan for improvements. Triggers include "review PR", "analyze pull request", "code review", and "PR quality check".
user-invocable: false
metadata:
  version: "0.1.0"
context: fork
allowed-tools:
  - Bash
  - Glob
  - Grep
  - Read
  - Task
---

# Comprehensive PR Review

Run a comprehensive pull request review using multiple specialized agents, each focusing on a different aspect of code quality.

**Review Aspects (optional):** "$ARGUMENTS"

## Review Workflow:

1. **Determine Review Scope**
   - Check git status to identify changed files
   - Parse arguments to see if user requested specific review aspects
   - Default: Run all applicable reviews

2. **Available Review Aspects:**

   - **comments** - Analyze code comment accuracy and maintainability
   - **tests** - Review test coverage quality and completeness
   - **errors** - Check error handling for silent failures
   - **types** - Analyze type design and invariants (if new types added)
   - **code** - General code review for project guidelines
   - **simplify** - Simplify code for clarity and maintainability
   - **all** - Run all applicable reviews (default)

3. **Identify Changed Files**
   - Run `git diff --name-only` to see modified files
   - Check if PR already exists: `gh pr view`
   - Identify file types and what reviews apply

   **Error handling:**
   - If `git diff` fails (not a git repo): Report error clearly and stop
   - If `gh pr view` fails with "no PR found": Expected for pre-PR reviews, continue with git diff
   - If `gh pr view` fails with auth error: Note that GitHub CLI authentication is needed
   - If no changed files found: Report "No changes detected" and stop

4. **Determine Applicable Reviews**

   Based on changes:
   - **Always applicable**: kata-code-reviewer (general quality)
   - **If test files changed**: kata-pr-test-analyzer
   - **If comments/docs added**: kata-comment-analyzer
   - **If error handling changed**: kata-failure-finder
   - **If types added/modified**: kata-type-design-analyzer
   - **After passing review**: kata-code-simplifier (polish and refine)

5. **Launch Review Agents**

   **Sequential approach** (one at a time):
   - Easier to understand and act on
   - Each report is complete before next
   - Good for interactive review

   **Parallel approach** (user can request):
   - Launch all agents simultaneously
   - Faster for comprehensive review
   - Results come back together

   **Agent failure handling:**
   - If agent completes: Include results in aggregation
   - If agent times out: Report "[agent-name] timed out - consider running independently"
   - If agent fails: Report "[agent-name] failed: [error reason]"
   - If one agent fails, STILL proceed with remaining agents
   - **Never silently skip a failed agent** - always report its status

6. **Aggregate Results**

   After agents complete, summarize:
   - **Critical Issues** (must fix before merge)
   - **Important Issues** (should fix)
   - **Suggestions** (nice to have)
   - **Positive Observations** (what's good)

   **Edge cases:**
   - If no issues found: Celebrate with "All Checks Passed" summary
   - If agents conflict: Note the disagreement and let user decide
   - If agent output malformed: Note "[agent] output could not be parsed"
   - Always include count of agents completed vs failed

7. **Provide Action Plan**

   Organize findings:
   ```markdown
   # PR Review Summary

   ## Critical Issues (X found)
   - [agent-name]: Issue description [file:line]

   ## Important Issues (X found)
   - [agent-name]: Issue description [file:line]

   ## Suggestions (X found)
   - [agent-name]: Suggestion [file:line]

   ## Strengths
   - What's well-done in this PR

   ## Recommended Action
   1. Fix critical issues first
   2. Address important issues
   3. Consider suggestions
   4. Re-run review after fixes
   ```

## Usage Examples:

**Full review (default):**
```
/kata:review-pr
```

**Specific aspects:**
```
/kata:review-pr tests errors
# Reviews only test coverage and error handling

/kata:review-pr comments
# Reviews only code comments

/kata:review-pr simplify
# Simplifies code after passing review
```

**Parallel review:**
```
/kata:review-pr all parallel
# Launches all agents in parallel
```

## Agent Descriptions:

**kata-comment-analyzer**:
- Verifies comment accuracy vs code
- Identifies comment rot
- Checks documentation completeness

**kata-pr-test-analyzer**:
- Reviews behavioral test coverage
- Identifies critical gaps
- Evaluates test quality

**kata-failure-finder**:
- Finds silent failures
- Reviews catch blocks
- Checks error logging

**kata-type-design-analyzer**:
- Analyzes type encapsulation
- Reviews invariant expression
- Rates type design quality

**kata-code-reviewer**:
- Checks CLAUDE.md compliance
- Detects bugs and issues
- Reviews general code quality

**kata-code-simplifier**:
- Simplifies complex code
- Improves clarity and readability
- Applies project standards
- Preserves functionality

## Tips:

- **Run early**: Before creating PR, not after
- **Focus on changes**: Agents analyze git diff by default
- **Address critical first**: Fix high-priority issues before lower priority
- **Re-run after fixes**: Verify issues are resolved
- **Use specific reviews**: Target specific aspects when you know the concern

## Workflow Integration:

**Before committing:**
```
1. Write code
2. Run: /kata:review-pr code errors
3. Fix any critical issues
4. Commit
```

**Before creating PR:**
```
1. Stage all changes
2. Run: /kata:review-pr all
3. Address all critical and important issues
4. Run specific reviews again to verify
5. Create PR
```

**After PR feedback:**
```
1. Make requested changes
2. Run targeted reviews based on feedback
3. Verify issues are resolved
4. Push updates
```
