---
name: code-review-agent-team
args: "[PR_NUMBER] [--scope=security|performance|tests|quality]"
description: |
  Parallel multi-agent code review using Agent Teams with 4 specialized reviewers.
  Spawns a coordinated team of security, performance, test coverage, and code quality agents.
  Teammates can share findings with each other for cross-domain insights.
  Produces unified report with severity-ranked findings saved to /output/.

  Requires Claude Code with Agent Teams support (TeamCreate, TaskCreate, SendMessage).

  Use when asked to:
  - "review code", "code review", "check my changes", "review PR"
  - "security review", "performance review", "test coverage check"
  - "full code review", "multi-agent review", "parallel review"

  Examples:
  - `/code-review-team` -- review uncommitted changes (git diff)
  - `/code-review-team 42` -- review PR #42
  - `/code-review-team --scope=security` -- security-only review of uncommitted changes
  - `/code-review-team 42 --scope=performance,tests` -- specific reviewers for PR
---

# Multi-Agent Parallel Code Review (Agent Teams)

Spawns a coordinated team of 4 specialized code-reviewer agents using Agent Teams. Teammates can communicate findings to each other and the lead compiles a unified severity-ranked report.

## Step 1: Determine Review Target

Parse `$ARGUMENTS`:

- **No arguments**: Use AskUserQuestion to confirm target:

```
question: "What would you like to review?"
header: "Review Target"
options:
  - label: "Uncommitted changes"
    description: "Review current git diff (staged + unstaged)"
  - label: "Staged changes only"
    description: "Review only staged changes (git diff --cached)"
  - label: "Enter PR number"
    description: "Review a specific pull request"
  - label: "Last commit"
    description: "Review changes in the most recent commit"
```

- **Number provided** (e.g., `42`): Target is PR #42
- **`--scope` flag**: Limit to specific reviewer types (comma-separated)

---

## Step 2: Capture the Diff

**IMPORTANT:** Save diff to the scratchpad directory, not `/tmp`.

**For uncommitted changes (staged + unstaged):**
```bash
git diff HEAD > $SCRATCHPAD/code-review-diff.txt 2>&1 && echo "done"
```

**For staged changes only:**
```bash
git diff --cached > $SCRATCHPAD/code-review-diff.txt 2>&1 && echo "done"
```

**For PR number:**
```bash
gh pr diff $PR_NUMBER > $SCRATCHPAD/code-review-diff.txt 2>&1 && echo "done"
```

**For last commit:**
```bash
git diff HEAD~1..HEAD > $SCRATCHPAD/code-review-diff.txt 2>&1 && echo "done"
```

Also capture changed file list:
```bash
git diff HEAD --name-only > $SCRATCHPAD/code-review-files.txt 2>&1 && echo "done"
```

Read both files via Read tool. If diff is empty, inform user and stop.

---

## Step 3: Show Diff Summary

Display a brief summary before launching the team:

```markdown
## Code Review Target

**Source:** [uncommitted changes / PR #42 / last commit]
**Files Changed:** [n]
**Lines Added:** [+n]
**Lines Removed:** [-n]

### Changed Files

| # | File | Type |
|---|------|------|
| 1 | src/lib/auth.ts | Modified |
| 2 | components/Login.tsx | Added |
```

---

## Step 4: Confirm Review Scope

If `--scope` flag was NOT provided, use AskUserQuestion:

```
question: "Which reviewers should analyze these changes?"
header: "Review Scope"
options:
  - label: "All 4 reviewers (recommended)"
    description: "Security + Performance + Test Coverage + Code Quality"
  - label: "Security + Code Quality"
    description: "Focus on vulnerabilities and maintainability"
  - label: "Performance + Test Coverage"
    description: "Focus on efficiency and test completeness"
  - label: "Select specific"
    description: "Choose individual reviewers"
```

---

## Step 5: Spawn the Review Team

### 5a: Create the team

Use the Teammate tool to create a new team:

```
Teammate:
  operation: "spawnTeam"
  team_name: "code-review-team"
  description: "Parallel code review with specialized reviewers"
```

### 5b: Create tasks for each reviewer

Create one task per selected reviewer using TaskCreate. All tasks are independent (no blockedBy dependencies).

### 5c: Spawn teammates

For each selected reviewer, spawn a teammate using the Task tool with `team_name` and `name` parameters. Launch ALL selected teammates in parallel.

Each teammate gets `subagent_type: "general-purpose"` for full tool access.

**IMPORTANT:** Include the full diff content and file list directly in each teammate's prompt. Teammates do NOT have access to the lead's filesystem context.

#### Security Reviewer Teammate

```
Task:
  team_name: "code-review-team"
  name: "security-reviewer"
  subagent_type: "general-purpose"
  description: "Security code review"
  prompt: |
    You are a security-focused code reviewer on a review team.

    ## Your Task
    1. Read the file `.claude/skills/code-review-agent-team/review.md` for the full checklist and severity guide
    2. Review the diff below for security vulnerabilities
    3. When done, mark your task as completed via TaskUpdate
    4. Send your findings to the team lead via SendMessage

    ## Focus Areas
    - Authentication and authorization flaws
    - Input validation and sanitization gaps
    - SQL injection, XSS, CSRF vulnerabilities
    - Sensitive data exposure (API keys, tokens, PII in logs)
    - Insecure dependencies or configurations
    - OWASP Top 10 compliance
    - Rate limiting gaps on API endpoints
    - Secrets or credentials in code

    ## Changed Files
    [paste file list from $SCRATCHPAD/code-review-files.txt]

    ## Diff
    [paste diff content from $SCRATCHPAD/code-review-diff.txt]

    ## Output Format (STRICT)
    Send findings to the lead as a JSON array wrapped in ```json code block.
    Each finding:
    {
      "reviewer": "security",
      "severity": "Critical|High|Medium|Low",
      "file": "path/to/file.ts",
      "line": 42,
      "title": "Short title",
      "description": "Detailed explanation of the issue",
      "suggestion": "How to fix it",
      "category": "auth|injection|exposure|config|validation|dependencies"
    }

    If no issues found, send: []
```

#### Performance Reviewer Teammate

```
Task:
  team_name: "code-review-team"
  name: "performance-reviewer"
  subagent_type: "general-purpose"
  description: "Performance code review"
  prompt: |
    You are a performance-focused code reviewer on a review team.

    ## Your Task
    1. Read `.claude/skills/code-review-agent-team/review.md` for the full checklist
    2. Review the diff below for performance issues
    3. Send findings to the team lead via SendMessage

    ## Focus Areas
    - N+1 query patterns (queries in loops)
    - Missing database indexes for new query patterns
    - Unbounded data fetching (missing LIMIT, pagination)
    - Memory leaks (unclosed connections, listeners, subscriptions)
    - Unnecessary re-renders in React components
    - Large bundle imports (importing entire libraries)
    - Missing caching opportunities
    - Inefficient algorithms or data structures

    ## Changed Files
    [paste file list]

    ## Diff
    [paste diff content]

    ## Output Format (STRICT)
    JSON array of findings with: reviewer, severity, file, line, title, description, suggestion, category
    Categories: n+1|memory|rendering|bundling|caching|algorithm|database

    If no issues found, send: []
```

#### Test Coverage Reviewer Teammate

```
Task:
  team_name: "code-review-team"
  name: "test-coverage-reviewer"
  subagent_type: "general-purpose"
  description: "Test coverage code review"
  prompt: |
    You are a test-coverage-focused code reviewer on a review team.

    ## Your Task
    1. Read `.claude/skills/code-review-agent-team/review.md` for the full checklist
    2. Review the diff below for test coverage gaps
    3. Send findings to the team lead via SendMessage

    ## Focus Areas
    - New functions/endpoints missing corresponding tests
    - Edge cases not covered (null, undefined, empty, boundary values)
    - Missing error path testing
    - Assertion quality (testing behavior, not implementation)
    - Missing integration tests for API routes
    - Test isolation (no shared state between tests)
    - Regression coverage for bug fixes

    ## Changed Files
    [paste file list]

    ## Diff
    [paste diff content]

    ## Output Format (STRICT)
    JSON array of findings with: reviewer, severity, file, line, title, description, suggestion, category
    Categories: missing-test|edge-case|assertion|integration|e2e|mock-quality

    If no issues found, send: []
```

#### Code Quality Reviewer Teammate

```
Task:
  team_name: "code-review-team"
  name: "code-quality-reviewer"
  subagent_type: "general-purpose"
  description: "Code quality review"
  prompt: |
    You are a code-quality-focused code reviewer on a review team.

    ## Your Task
    1. Read `.claude/skills/code-review-agent-team/review.md` for the full checklist
    2. Review the diff below for code quality issues
    3. Send findings to the team lead via SendMessage

    ## Focus Areas
    - Readability and clarity of code
    - Naming conventions (clear, descriptive, consistent)
    - DRY violations (duplicated logic)
    - SOLID principle violations
    - Excessive nesting or complexity
    - Dead code or unused imports
    - Missing TypeScript types (any usage, missing return types)
    - Error handling patterns
    - File organization and module boundaries

    ## Changed Files
    [paste file list]

    ## Diff
    [paste diff content]

    ## Output Format (STRICT)
    JSON array of findings with: reviewer, severity, file, line, title, description, suggestion, category
    Categories: naming|dry|solid|complexity|types|error-handling|style|organization

    If no issues found, send: []
```

### 5d: Assign tasks to teammates

After spawning all teammates, assign each task to its corresponding teammate using TaskUpdate.

---

## Step 6: Monitor Progress & Collect Results

The lead monitors progress by:

1. **Receiving messages** -- teammates send findings via SendMessage
2. **Checking TaskList** -- periodically check if all tasks are marked `completed`
3. **Redirecting if needed** -- if a teammate seems stuck, respond via SendMessage

Wait until all teammates have sent findings and marked tasks as completed.

For each teammate's message:
1. Extract the JSON array from the ```json code block
2. Merge all findings into a single array
3. Sort by severity: Critical > High > Medium > Low

---

## Step 7: Shutdown the Team

Send shutdown requests to all teammates, then clean up.

---

## Step 8: Present Unified Report

```markdown
## Code Review Report

**Target:** [uncommitted changes / PR #42 / last commit]
**Files Reviewed:** [n]
**Reviewers:** [Security, Performance, Test Coverage, Code Quality]
**Total Findings:** [n]

### Summary

| Severity | Count | Action |
|----------|-------|--------|
| Critical | [n] | Must fix before merge |
| High | [n] | Should fix before merge |
| Medium | [n] | Fix when possible |
| Low | [n] | Consider improving |

### Findings by Reviewer

| Reviewer | Critical | High | Medium | Low | Total |
|----------|----------|------|--------|-----|-------|
| Security | [n] | [n] | [n] | [n] | [n] |
| Performance | [n] | [n] | [n] | [n] | [n] |
| Test Coverage | [n] | [n] | [n] | [n] | [n] |
| Code Quality | [n] | [n] | [n] | [n] | [n] |

### Critical Findings

| # | Reviewer | File | Title | Category |
|---|----------|------|-------|----------|
| 1 | security | auth.ts:42 | SQL injection risk | injection |

**Details:**
> [description]
> **Fix:** [suggestion]
```

---

## Step 9: Ask About Next Steps

Options:
- Show all findings with details
- Show findings for specific file
- Save report to /output/ (JSON)
- Launch fix agents (auto-fix Critical/High issues)
- Done

---

## Step 10: Save Report

If requested, save full JSON report to `./output/code-review-TIMESTAMP.json`.

---

## Step 11: Optional Fix Agents

For selected findings, spawn one-shot Task agents (not team members) to auto-fix issues. Launch up to 3 in parallel. Each agent: reads the file, makes the minimum change, preserves all functionality.

---

## Error Handling

- **Empty diff**: Inform user, suggest checking `git status`
- **Invalid teammate JSON**: Skip reviewer, note in report
- **Unresponsive teammate**: 2 follow-ups, then skip
- **Missing `gh` CLI**: Suggest installation, offer uncommitted review instead
