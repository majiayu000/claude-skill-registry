---
name: issue-implementation-review
description: Reviews code changes from a completed task implementation for correctness, completeness, and simplicity. Use when asked to "review implementation", "review task code", "code review", "verify implementation", or after completing an issue implementation.
context: fork
agent: general-purpose
allowed-tools:
  - Glob
  - Grep
  - LS
  - Read
  - WebFetch
  - WebSearch
  - TodoWrite
  - mcp__perplexity-ask__perplexity_ask
  - mcp__task-trellis__get_issue
  - mcp__task-trellis__list_issues
---

# Issue Implementation Review

Review the code changes from a completed task implementation to verify correctness, completeness, and adherence to simplicity principles.

## Goal

Provide a thorough code review of task implementation changes, ensuring the code correctly and completely solves the issue without over-engineering.

## Required Inputs

- **Task ID**: The Trellis task ID that was implemented (e.g., "T-add-user-validation")
- **Additional Context** (optional): Any decisions or constraints from implementation

## When You Need Clarification

This skill runs as a subagent and cannot ask the user questions directly. If you encounter situations where clarification is needed before proceeding effectively, **return early** with:

1. **Questions**: List each question that needs to be answered
2. **Context Collected**: Summarize what you've learned so far (task details, files examined, findings to date)
3. **Instructions for Caller**: Tell the caller to:
   - Get answers to the listed questions from the user
   - Re-invoke this skill with the original inputs plus the answers

### Example Early Return Format

```
## Clarification Needed

I need additional information before I can complete this review effectively.

### Questions
1. [First question that needs an answer]
2. [Second question if applicable]

### Context Collected So Far
- **Task**: [Task ID and title if retrieved]
- **Files Identified**: [List of files found]
- **Preliminary Findings**: [Any observations made before hitting the blocker]

### Next Steps
To continue this review:
1. Get answers to the questions above from the user
2. Re-run this skill with: `/issue-implementation-review [Task ID] --context "[answers and any additional context]"`
```

### When to Return Early

- Task ID is missing or invalid
- Multiple tasks match ambiguous criteria
- Implementation approach is unclear and critical to the review
- You find conflicting requirements that need human judgment

## Review Process

### 1. Gather Issue Context

Retrieve the full context for the implemented task:

- **Get the task**: Use `get_issue` to retrieve the task details, including:
  - Task description and requirements
  - Modified files list (tracked during implementation)
  - Implementation log entries
- **Get parent context**: Retrieve the parent feature (and epic/project if relevant) to understand broader requirements and acceptance criteria
- **Note the scope**: Understand what was requested vs. what should have been delivered

### 2. Review Changed Files

For each file listed in the task's modified files:

- **Read the file**: Examine the actual code changes
- **Understand the changes**: What was added, modified, or removed?
- **Check related files**: Look at imports, tests, and integration points

### 3. Correctness Review

Verify the implementation is technically correct:

- **Logic correctness**: Does the code do what it's supposed to do?
- **Error handling**: Are edge cases and errors handled appropriately?
- **Integration**: Does it integrate correctly with existing code?
- **Pattern consistency**: Does it follow codebase conventions and patterns?
- **Type safety**: Are types correct and complete (no `any` abuse)?
- **Security**: No obvious vulnerabilities (injection, XSS, etc.)?

### 4. Completeness Review

Verify all requirements are addressed:

- **Functional requirements**: All requirements from the task are implemented
- **Acceptance criteria**: Parent feature/epic criteria that apply are satisfied
- **Test coverage**: Tests exist for the new functionality (see [Testing Guidelines](testing-guidelines.md))
- **Quality checks**: Code passes linting, formatting, and type checks

### 5. Simplicity Review

Evaluate for over-engineering:

- **YAGNI violations**: Features or abstractions not required by the task
- **Premature optimization**: Performance optimizations without evidence of need
- **Unnecessary complexity**: Could this be simpler while still meeting requirements?
- **Scope creep**: Changes beyond what was requested (unless explicitly justified)
- **Dead code**: Unused imports, variables, or functions
- **Over-abstraction**: Helpers or utilities for one-time operations

**Guideline**: Three similar lines of code is often better than a premature abstraction.

### 6. Documentation Review

Evaluate code documentation against the [Code Documentation Guidelines](code-documentation-guidelines.md):

- **Over-documentation**: JSDoc/docstrings on private or internal functions
- **Redundant documentation**: Comments that restate what the code shows (parameter types, return types, obvious behavior)
- **Verbose documentation**: Multi-paragraph docs where one sentence would suffice
- **Missing public docs**: Public interfaces without any documentation

**Guideline**: Documentation is for AI agents who have already read the code. If the documentation just restates what's visible in the signature and implementation, flag it for removal.

## Output

Return only actionable findings. Skip positive assessments, status indicators, and "everything looks good" observations. The output is consumed by AI agents that need to act on findings.

### Output Format

```
## Review Findings

### Critical (must fix)
- [file:line] [Specific issue that must be addressed before proceeding]

### Recommendations
- [file:line] [Suggested improvement with rationale]

### Gaps
- [Missing requirement or functionality from the task description]

### Questions
- [Item needing user clarification before review can complete]
```

### Output Rules

- **Omit empty sections**: If a section has no items, do not include it
- **No findings = approved**: If there are no findings, return only: `No issues found.`
- **No verdict section**: Empty output implicitly means approved
- **Always include file:line**: Reference specific code locations for all findings
- **Skip positive observations**: Do not report things that are correct or working well

### Examples

**When issues are found:**
```
## Review Findings

### Critical (must fix)
- src/auth/login.ts:45 Missing null check before accessing user.email
- src/auth/login.ts:78 SQL query vulnerable to injection, use parameterized query

### Recommendations
- src/auth/login.ts:23 Consider extracting validation logic to separate function for testability
```

**When no issues are found:**
```
No issues found.
```

## Review Standards

- **Evidence-based**: Support findings with specific code references (file:line)
- **Actionable**: Recommendations should be specific and implementable
- **Proportionate**: Don't nitpick style when substance matters more
- **Concise**: Only report items that require action or decision
