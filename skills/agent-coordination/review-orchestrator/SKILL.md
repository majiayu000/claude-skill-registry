---
name: review-orchestrator
description: 'Dispatch review subagents, compile feedback, triage for human decision. Use after quality gates pass.'
---

# Review Orchestrator

Dispatches multiple review subagents in parallel, compiles and deduplicates their feedback, and presents a triaged list for human decision.

## When to Use

- Quality gates have passed (lint, typecheck, tests)
- Code changes are ready for review
- Before creating a PR

## Prerequisites

- CodeRabbit CLI installed: `which coderabbit`
- Authenticated: `coderabbit auth login`
- Pro tier allows 8 reviews/hour

## Workflow

### 1. Verify Readiness

```bash
# Check CodeRabbit installed
which coderabbit

# Check there are changes to review
git status --porcelain
git diff --stat HEAD~1  # or vs base branch
```

If no changes or CodeRabbit missing, stop and inform user.

### 2. Gather Context

Collect before dispatching subagents:

- List of changed files: `git diff --name-only HEAD~1`
- The run directory path (for saving review-comments.md)
- Ticket requirements from `ticket.json` if available
- Plan file if available

### 3. Dispatch Review Subagents

Use the Task tool to dispatch three parallel review subagents:

**Subagent 1: CodeRabbit Review**

```
Run CodeRabbit CLI review on the current changes.

Commands:
cd {REPO_PATH}
coderabbit --prompt-only --type uncommitted

Parse output and categorize findings by severity:
- Critical: Security, race conditions, data loss
- Major: Logic errors, performance, missing error handling
- Minor: Code style, naming
- Nitpick: Formatting preferences

Return structured list with file:line, issue, suggested fix.
```

**Subagent 2: Agent Code Review**

```
Perform comprehensive code review of the changes.

Files to review: {FILES_LIST}
Ticket requirements: {TICKET_REQUIREMENTS}

Review Checklist:
1. Functionality: Implements requirements, handles edge cases, proper error handling
2. Code Quality: TypeScript (no any), Vue (Composition API), Tailwind (no dark:), naming conventions
3. Architecture: Follows existing patterns, no over-engineering, clean separation
4. Testing: Tests added, behavioral not change detectors, edge cases covered
5. Security: No secrets exposed, input validation, no XSS/injection
6. Performance: No unnecessary re-renders, efficient data structures

Return findings with severity (Critical/Major/Minor), location (file:line), and fix suggestion.
```

**Subagent 3: Pattern Compliance Review**

```
Check code against target repository patterns and AGENTS.md guidelines.

Files to review: {FILES_LIST}

Check for violations:
- Vue: Reactive props destructuring (not withDefaults), separate type imports
- Tailwind: No dark: variants (use semantic themes), use cn() utility, no !important
- TypeScript: No any types, no as any assertions
- State: No unnecessary computed/watch when simpler works
- Testing: Behavioral tests, not change detectors or mock tests

Return violations with file:line and the correct pattern to use.
```

### 4. Compile and Deduplicate

After all subagents complete:

1. **Merge findings** from all three reviewers
2. **Remove duplicates**: Same issue found by multiple reviewers (note "Found by: CodeRabbit, Agent")
3. **Resolve conflicts**: If reviewers disagree, note both perspectives with recommendation
4. **Group by file**: Organize findings by file path
5. **Sort by severity**: Critical → Major → Minor → Nitpick

### 5. Generate Review Summary

Create structured output:

````markdown
# Code Review Summary

## Statistics

- Total findings: {count}
- Critical: {count}
- Major: {count}
- Minor: {count}
- Nitpicks: {count}
- Duplicates removed: {count}

## Critical Issues (Must Fix)

### [C1] {Title}

- **File:** `path/to/file.ts:42`
- **Source:** CodeRabbit / Agent / Pattern
- **Issue:** {description}
- **Fix:**

```typescript
// Suggested fix
```
````

## Major Issues (Should Fix)

### [M1] {Title}

- **File:** `path/to/file.ts:55`
- **Source:** {source}
- **Issue:** {description}
- **Fix:** {suggestion}

## Minor Issues (Consider)

### [m1] {Title}

- **File:** `path/to/file.ts:10`
- **Issue:** {description}
- **Fix:** {suggestion}

## Nitpicks (Optional)

- [N1] `file.ts:10` - {description}
- [N2] `file.ts:20` - {description}

## Conflicting Opinions

### {Topic}

- **CodeRabbit says:** {opinion}
- **Agent says:** {opinion}
- **Recommendation:** {which to follow and why}

```

### 6. Present Triage Interface

```

Review complete. {X} findings across {Y} files.

For each finding, respond with:

- Numbers to implement (e.g., "C1, M1, M3")
- "all critical" - implement all critical
- "all major" - implement all critical + major
- "all" - implement everything
- "skip N1, N2" - skip specific items
- "clarify M2" - need more info on item

Your response:

````

Wait for human decision.

### 7. Save Review

Save full review to `{run-dir}/review-comments.md`:
- Complete review summary
- All findings with full details
- Human's triage decisions
- Timestamp

Update `status.json`:
```json
{
  "stage": "review-complete",
  "reviewStats": {
    "critical": 0,
    "major": 2,
    "minor": 3,
    "nitpicks": 5
  },
  "selectedFixes": ["C1", "M1", "M2"],
  "skippedItems": ["N1", "N2"]
}
````

### 8. Handle Implementation

For selected items:

- Dispatch fix subagents for each selected item, OR
- Return to implementation phase with specific fix list

After fixes, re-run affected quality gates to verify.

## Severity Definitions

| Severity | Description                                                | Action             |
| -------- | ---------------------------------------------------------- | ------------------ |
| Critical | Security issues, race conditions, data loss, breaking bugs | Must fix before PR |
| Major    | Logic errors, performance issues, missing error handling   | Should fix         |
| Minor    | Code style, naming, documentation                          | Consider fixing    |
| Nitpick  | Formatting, personal preference                            | Optional           |

## Rate Limiting

CodeRabbit Pro: 8 reviews/hour. Track usage and warn if approaching limit.

## Fallback

If CodeRabbit is unavailable:

1. Skip CodeRabbit subagent
2. Note in review summary: "CodeRabbit review skipped: {reason}"
3. Continue with Agent and Pattern reviews

## Example Session

```
> Review the changes

Checking prerequisites...
✓ CodeRabbit installed
✓ 5 files changed

Dispatching review subagents...
  [1/3] CodeRabbit: Running...
  [2/3] Agent Review: Running...
  [3/3] Pattern Review: Running...

All reviews complete. Compiling findings...

# Code Review Summary

## Statistics
- Total findings: 8
- Critical: 0
- Major: 2
- Minor: 3
- Nitpicks: 3
- Duplicates removed: 2

## Major Issues (Should Fix)

### [M1] Missing error handling in API call
- **File:** `src/api/client.ts:42`
- **Source:** CodeRabbit, Agent
- **Issue:** API call doesn't handle network errors
- **Fix:** Wrap in try/catch, show user-friendly error

### [M2] Unnecessary re-render in computed
- **File:** `src/components/Panel.vue:15`
- **Source:** Agent
- **Issue:** Computed recalculates on every render
- **Fix:** Memoize or move to watchEffect

...

Review complete. 8 findings across 5 files.

For each finding, respond with:
- Numbers to implement (e.g., "M1, M2")
- "all major" - implement all critical + major
- "skip N1" - skip specific items

Your response:
```
