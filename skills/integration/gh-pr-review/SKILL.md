---
name: gh-pr-review
description: "Reviews GitHub PRs with multi-agent orchestration for comprehensive validation. Triggers on keywords: PR review, review PR, GitHub PR review, pull request review"
project-agnostic: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
  - Task
  - WebFetch
---

# GitHub PR Review

Review the GitHub pull request with comprehensive validation using multi-agent orchestration.

## Inputs

- **PR_LINK**: $1 (GitHub PR URL, e.g., `https://github.com/owner/repo/pull/123`)
- **EXPECTED_CHANGES**: $2 (Brief description of expected changes)
- **REPORT_PATH**: $3 (Optional; defaults to `tmp/mux/{date}-{uuid}/PR-{PR_NUMBER}-{UUID}.md`)

---

## Pre-Flight

1. Extract PR number from URL: `$1`
2. Generate UUID for this review session
3. Create output directory: `tmp/mux/{date}-{uuid}/`

---

## Step 1: Fetch PR Data

Use `gh` CLI to gather PR information:

```
gh pr view <PR_NUMBER> --json title,body,author,state,baseRefName,headRefName,files,additions,deletions,commits
gh pr diff <PR_NUMBER>
gh pr view <PR_NUMBER> --json comments,reviews
gh pr checks <PR_NUMBER>
```

Store PR metadata for agent context.

---

## Step 2: Launch Review Agents (PARALLEL)

Use the **Task tool** to spawn 5 agents in parallel. Each agent writes findings to its output file.

### Agent 1: Expected Changes Validation
**Subagent type**: `general-purpose`
**Task**: Compare PR diff against expected changes: `$2`
- Identify missing expected changes
- Identify unexpected/out-of-scope changes
- Report alignment score (1-10) and gaps
- Write summary to: `{OUTPUT_DIR}/01_expected_changes.md`

### Agent 2: Security Review
**Subagent type**: `general-purpose`
**Task**: Security review of PR diff
- Check for hardcoded secrets/credentials
- Check for SQL injection, command injection, XSS vulnerabilities
- Check for insecure dependencies
- Check for permission/auth issues
- Reference OWASP Top 10
- Write summary to: `{OUTPUT_DIR}/02_security.md`

### Agent 3: Code Quality Review
**Subagent type**: `general-purpose`
**Task**: Code quality review of PR diff
- Validate against project conventions (if documented)
- RUN project-configured linters and type checkers on changed files from PR diff
- REPORT any NEW violations introduced by this PR (ignore pre-existing issues)
- REPORT any pre-commit hook failures with remediation guidance (if hooks are configured)
- Check type annotations present and correct
- Check error handling (re-raise, no silent failures)
- Check function complexity and readability
- Check naming conventions and import organization
- Write summary to: `{OUTPUT_DIR}/03_code_quality.md`

### Agent 4: Test Discovery & Execution
**Subagent type**: `general-purpose`
**Task**: Discover and run tests from PR
- Find test files in diff
- Find CLI configurations (test.json, cli.py patterns)
- Execute discovered tests with pytest
- Report pass/fail with output
- Write summary to: `{OUTPUT_DIR}/04_tests.md`

### Agent 5: Logic & Bug Risk Analysis (CRITICAL)
**Subagent type**: `general-purpose`
**Model**: `opus` (requires deep reasoning)
**Task**: Critical evaluation of logic changes and bug introduction risk

#### Logic Correctness Review
- **Intent vs Implementation**: Does the code actually achieve what it's supposed to?
- **Edge Cases**: Identify unhandled edge cases (nulls, empty collections, boundary values)
- **State Management**: Check for race conditions, stale state, improper state transitions
- **Control Flow**: Verify branching logic, loop terminations, early returns are correct
- **Data Flow**: Trace data through the change - are transformations correct?

#### Bug Introduction Risk
- **Behavioral Regressions**: Changes that might break existing functionality
- **Silent Failures**: Paths where errors could be swallowed or ignored
- **Type Coercion Issues**: Implicit conversions that might lose data or precision
- **Off-by-One Errors**: Index/range calculations
- **Null Reference Risks**: Accessing properties on potentially null/undefined values
- **Resource Leaks**: Unclosed connections, file handles, memory allocations

#### Logic Smell Detection
- **Inverted Conditions**: Logic that does the opposite of what variable names suggest
- **Dead Code Paths**: Unreachable branches introduced by the change
- **Contradictory Logic**: Conditions that can never be true together
- **Missing Validation**: Input assumptions not validated
- **Inconsistent Handling**: Similar cases handled differently without reason

#### Impact Analysis
- **Downstream Effects**: What other components rely on changed code?
- **Contract Violations**: Does the change break implicit contracts with callers?
- **Assumption Changes**: Are assumptions about data/state still valid?

#### Output Format
For each issue found:
```
[SEVERITY] - [Category]
Location: file:line
Issue: [description]
Why it's a bug: [reasoning]
Fix suggestion: [if applicable]
```

- Write summary to: `{OUTPUT_DIR}/05_logic_bugs.md`

---

## Step 3: Aggregate Results

After ALL agents complete:
1. Read all agent summaries from `{OUTPUT_DIR}/*.md`
2. Synthesize findings into consolidated report

---

## Step 4: Generate Review Report

Create report at: `$3` or `tmp/mux/{date}-{uuid}/PR-{PR_NUMBER}-{UUID}.md`

### Report Template

```markdown
# PR Review: #{PR_NUMBER}

**URL**: {PR_URL}
**Title**: {PR_TITLE}
**Author**: {AUTHOR}
**Branch**: {HEAD} -> {BASE}
**Review Session**: {UUID}
**Date**: {TIMESTAMP}

---

## Executive Summary

{Overall assessment: APPROVE / REQUEST_CHANGES / NEEDS_DISCUSSION}

### Scores
| Category | Score | Status |
|----------|-------|--------|
| Expected Changes Alignment | X/10 | {emoji} |
| Logic & Bug Risk | X/10 | {emoji} |
| Security | X/10 | {emoji} |
| Code Quality | X/10 | {emoji} |
| Tests | X/10 | {emoji} |

---

## Detailed Findings

### Expected Changes
{From Agent 1}

### Logic & Bug Risk (CRITICAL)
{From Agent 5 - This section requires careful review}

#### Logic Issues Found
{List of logic correctness problems}

#### Potential Bugs Introduced
{List of bug risks with severity and reasoning}

#### Impact Assessment
{Downstream effects and contract changes}

### Security
{From Agent 2}

### Code Quality
{From Agent 3}

### Test Results
{From Agent 4}

---

## PR Review Comments

| File | Line | Severity | Comment |
|------|------|----------|---------|
| path/file.py | 42 | ERROR | Issue description |

---

## PR Review Message

{Copy-paste ready message for GitHub PR comment}

### Recommendation
- APPROVE: Ready to merge
- REQUEST_CHANGES: Must address before merge
- COMMENT: No blocking issues

---

## Next Steps
{Actionable recommendations}
```

---

## Step 5: Present Results

Output summary to user:

```
PR REVIEW COMPLETE

PR: #{PR_NUMBER} - {TITLE}
Report: {REPORT_PATH}

Top Issues:
{Critical findings}

Proposed Actions:
1. Post review: gh pr review {PR_NUMBER} --comment --body-file {REPORT}
2. Request changes: gh pr review {PR_NUMBER} --request-changes
3. Approve: gh pr review {PR_NUMBER} --approve

Which action?
```

---

## Safety

- READ-ONLY GitHub operations (no automatic posting)
- All review comments require USER CONFIRMATION before posting
- Tests run in local environment only
- Sensitive data redacted from reports
