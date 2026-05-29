---
name: task-plan-normalizer
description: Convert raw task input into a machine-safe execution plan or explicitly refuse to proceed. Use before any code changes in unattended/headless mode to ensure deterministic, safe task execution.
---

# Task Plan Normalizer Skill

Convert underspecified or ambiguous tasks into structured execution plans for unattended operation.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Analyze raw human input (issues, PR comments, @mentions) and produce a deterministic execution plan that is safe for unattended operation, or explicitly refuse to proceed when requirements are unclear.

## Background Knowledge

### The Problem

In unattended mode, Claude cannot ask clarifying questions. Underspecified tasks lead to:
- Stalled runs waiting for interactive prompts
- Unsafe assumptions about missing requirements
- Inconsistent outcomes across similar tasks
- Wasted compute on doomed-to-fail executions

### The Solution

This skill acts as a **pre-flight check** that runs before any code changes. It decides:
1. **Whether** work should proceed at all
2. **Exactly how** the work should be executed

## Input Sources

The normalizer ingests:
- **Issue context**: Title, body, labels, comments
- **PR context**: Description, triggering comment, diff context
- **Repo profile**: From `repo_introspect` if available (tech stack, conventions, test commands)

## Output Contract

Produce a single structured JSON object:

```json
{
  "decision": "proceed | needs-human | blocked",
  "summary": "Short plain-English restatement of the task",
  "plan": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ..."
  ],
  "assumptions": [
    "Assumption A",
    "Assumption B"
  ],
  "stop_conditions": [
    "If tests fail",
    "If merge conflicts occur",
    "If required info is missing"
  ],
  "labels_to_apply_on_stop": ["needs-human"]
}
```

### Decision Values

| Decision | Meaning | Action |
|----------|---------|--------|
| `proceed` | Task is clear, safe to run unattended | Execute the plan |
| `needs-human` | Ambiguity or missing info requires clarification | Comment on issue, apply labels, stop |
| `blocked` | Impossible or unsafe to proceed | Comment on issue explaining why, stop |

## Workflow

### 1. Gather Context

Read all available input:

```bash
# If working from an issue
gh issue view <number> --comments

# If working from a PR comment
gh pr view <number> --comments

# Get repo context if repo_introspect output exists
cat repo-profile.json 2>/dev/null || echo "No repo profile available"
```

### 2. Extract Requirements

From the raw input, identify:

- **Explicit requirements**: Directly stated needs ("add a button", "fix the bug")
- **Implicit assumptions**: Unstated but inferable ("uses existing auth system")
- **Constraints**: Scope limits, file restrictions, behavioral expectations
- **Success criteria**: How to know when the task is complete

### 3. Assess Feasibility

Evaluate whether the task can proceed:

| Check | Proceed | Needs Human | Blocked |
|-------|---------|-------------|---------|
| Requirements clarity | Clear and specific | Ambiguous but inferable | Contradictory or missing |
| Scope definition | Well-bounded | Broad but manageable | Unbounded or unclear |
| Technical feasibility | Achievable | Requires assumptions | Impossible with current context |
| Safety assessment | Low risk | Medium risk with mitigations | High risk or destructive |

### 4. Generate Plan

If decision is `proceed`, create an ordered execution plan:

1. Each step must be **atomic** and **verifiable**
2. Include validation checkpoints (test runs, linting, etc.)
3. Define rollback points where applicable
4. List explicit stop conditions

### 5. Output the Result

Emit the structured JSON to stdout or a designated file.

## Decision Criteria

### Proceed When

- Requirements are explicit and unambiguous
- Scope is well-defined (specific files, features, or behaviors)
- Success criteria are testable
- No destructive operations without explicit confirmation
- Similar tasks have been completed successfully before

### Needs Human When

- Key requirements are ambiguous or contradictory
- Multiple valid interpretations exist with different outcomes
- The task requires access to resources not available
- Scope is unclear ("improve performance" without specifics)
- User preferences are needed (design choices, trade-offs)

### Blocked When

- Task is technically impossible with available context
- Requirements are contradictory with no resolution
- Task would require unsafe or forbidden operations
- Prerequisites are missing and cannot be inferred
- The request violates safety guidelines

## Example: Issue Analysis

**Input Issue:**
```
Title: Add logout button
Body: Users need a way to log out of the app.
```

**Analysis:**

```json
{
  "decision": "needs-human",
  "summary": "Add a logout button to allow users to end their session",
  "plan": [],
  "assumptions": [
    "There is an existing authentication system",
    "The app has a header or navigation component",
    "Session management exists and can be cleared"
  ],
  "stop_conditions": [],
  "labels_to_apply_on_stop": ["needs-human"],
  "clarification_needed": [
    "Where should the logout button be placed? (header, sidebar, settings page)",
    "What should happen after logout? (redirect to login, show confirmation)",
    "Should there be a confirmation dialog before logging out?"
  ]
}
```

## Example: Clear Task

**Input Issue:**
```
Title: Fix typo in README
Body: Line 42 says "teh" instead of "the". Please fix.
```

**Analysis:**

```json
{
  "decision": "proceed",
  "summary": "Fix typo on line 42 of README: change 'teh' to 'the'",
  "plan": [
    "Step 1: Read README.md and verify typo exists on line 42",
    "Step 2: Fix the typo by replacing 'teh' with 'the'",
    "Step 3: Verify the change is correct",
    "Step 4: Commit with message 'Fix typo in README'"
  ],
  "assumptions": [
    "README.md exists in repository root"
  ],
  "stop_conditions": [
    "If README.md does not exist",
    "If line 42 does not contain the typo 'teh'"
  ],
  "labels_to_apply_on_stop": ["needs-human"]
}
```

## Example: Blocked Task

**Input Issue:**
```
Title: Delete all production data
Body: We need to wipe the production database.
```

**Analysis:**

```json
{
  "decision": "blocked",
  "summary": "Request to delete all production data",
  "plan": [],
  "assumptions": [],
  "stop_conditions": [],
  "labels_to_apply_on_stop": ["blocked", "needs-human"],
  "block_reason": "This task involves destructive operations on production data, which violates safety guidelines. Production database operations require manual intervention with proper authorization, backups, and verification procedures."
}
```

## Policies

### Always

- Run this analysis **before** any code changes
- Document all assumptions explicitly
- Include stop conditions for any plan
- Prefer `needs-human` over making unsafe assumptions
- Output valid JSON that can be parsed programmatically

### Never

- Proceed with ambiguous destructive operations
- Assume permissions or access not explicitly granted
- Skip the analysis step in unattended mode
- Generate plans with unbounded scope
- Ignore stop conditions during execution

### Stop Conditions

The plan must halt immediately if:

- Tests fail after a change
- Merge conflicts occur
- Required information is discovered to be missing
- An operation returns an unexpected error
- The scope expands beyond the original plan
- Any safety guideline would be violated

## Integration

This skill is designed to work with:
- `repo_introspect` - For repository context
- `github-issues` - For issue details
- `github-pr` - For PR context
- `github-branches` - For branch management after planning

## Output Format

When run, report:
1. The decision (`proceed`, `needs-human`, or `blocked`)
2. The structured JSON output
3. Next steps based on the decision:
   - `proceed`: Begin executing the plan
   - `needs-human`: Comment on issue with clarification questions
   - `blocked`: Comment on issue explaining the block reason
