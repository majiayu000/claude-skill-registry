---
name: sr
description: >-
  Conduct comprehensive code review before PR merge. Use when asked to
  'review code', 'start code review', 'review PR', 'check before merge',
  or 'pre-merge review'. NOT for addressing review comments (use /prc),
  NOT for code exploration (use /code-analysis).
argument-hint: [task-path or PR-url]
allowed-tools: Task, Skill, Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion
---

# Start Review Command

## PRIMARY OBJECTIVE

Professional code review using specialized agents. Ensure quality, architectural compliance, and requirements fulfillment before merge.

## WORKFLOW

### GATE 1: Task Identification

1. **AskUserQuestion**: "Which task to review? Provide task path or PR URL."

2. **Validate**:
   - Task document exists with "Implementation Complete" status
   - **STOP if**: "In Progress" or missing PR information
   - Linear issue referenced, steps marked complete

### GATE 2: Automated Quality Gate

**ACTION**: Invoke `automated-quality-gate` agent

```
Task directory: [path]
Run quality checks (format, lint, types, tests, build) and return structured results.
Agent returns data inline (no file created) - integrate into Code Review.
```

- **STOP if GATE_FAILED** → Return to developer with fixes list
- Agent returns JSON + markdown snippet for integration into Code Review

### GATE 3: Approach Review

**ACTION**: Invoke `senior-architecture-reviewer` agent

```
Task directory: [path]
Review approach, requirements fulfillment, architecture fit, TDD compliance (git history).
```

- **STOP if NEEDS_REWORK** → Return to developer with issues

### GATE 4: Parallel Code Review

**ACTION**: Invoke these 5 agents **IN PARALLEL**:

1. **`security-code-reviewer`**:
   ```
   Review security: OWASP, input validation, auth. Task: [path]
   ```

2. **`code-quality-reviewer`**:
   ```
   Review quality: SOLID, DRY, patterns, DDD layers. Task: [path]
   ```

3. **`test-coverage-reviewer`**:
   ```
   Review tests: coverage gaps, edge cases, quality. Task: [path]
   ```

4. **`documentation-accuracy-reviewer`**:
   ```
   Review docs: accuracy, completeness. Task: [path]
   ```

5. **`performance-reviewer`**:
   ```
   Review performance: bottlenecks, N+1 queries, efficiency. Task: [path]
   ```

### GATE 5: Synthesis & Decision

**TEMPLATE**: Use `@docs/product-docs/templates/code-review-template.md`

1. **Read template** from `docs/product-docs/templates/code-review-template.md`
2. **Aggregate findings** from all agents:
   - Quality Gate (GATE 2)
   - Approach Review (GATE 3)
   - All 5 Code Review agents (GATE 4)
3. **Apply severity markers** `[CRITICAL]`, `[MAJOR]`, `[MINOR]`, `[INFO]` within each agent section
4. **Consolidate issues** into severity categories with source agent attribution
5. **Apply decision matrix** (see below)
6. **Create** `Code Review - [Task].md` in task directory using template structure

### GATE 6: Codex Final Review (If APPROVED)

**CONDITION**: Only run if Decision Matrix result is APPROVED (0 Critical, 0-2 Major)

**ACTION**: Invoke `/codex-cli` skill for cross-AI final validation

**Verification focus:** Final pre-merge review as last reviewer before main
- All acceptance criteria implemented
- No regressions or breaking changes
- Code is production-ready
- No security issues missed by previous reviewers

**Process feedback:**
- **STOP if CRITICAL issues** → Change decision to NEEDS FIXES
- Add findings to Code Review document under "Cross-AI Validation" section

### GATE 7: Linear & Completion

1. **Update Linear status (end only)** using the `cc-linear` skill:
   - Do this as a **single atomic operation** (status update only).
   - Target status: `[Ready to Merge | Needs Fixes | In Review]`

2. **Add results comment (end only)** using the `cc-linear` skill:
   - Do this as a **separate atomic operation** (comment only).
   - Include status + issue counts + review doc path.

3. **Notify user** of outcome and next steps

## DECISION MATRIX

| Critical | Major | Decision |
|----------|-------|----------|
| 0 | 0-2 | APPROVED |
| 0 | 3+ | NEEDS FIXES |
| 1+ | any | NEEDS FIXES |

**Severity Levels**:
- `[CRITICAL]` - Must fix before merge (blocks approval)
- `[MAJOR]` - Should fix (3+ blocks approval)
- `[MINOR]` - Nice to fix (does not block)
- `[INFO]` - Observations (does not block)

**Status Mapping**:
- APPROVED → "Ready to Merge"
- NEEDS FIXES → "Needs Fixes"
- NEEDS DISCUSSION → Keep "In Review"

## OUTPUT

Single `Code Review - [Task].md` created in task directory using template from `@docs/product-docs/templates/code-review-template.md`.

**Important**: All review data is consolidated into this single file. No separate files are created for:
- Quality Gate Report (integrated into Pre-Review Validation section)
- Approach Review (integrated into Pre-Review Validation section)

**Contains**:
- Pre-Review validation (Quality Gate + Approach Review inline)
- Code Review findings from 5 specialized agents (with inline severity markers)
- Cross-AI Validation (Codex final review - if APPROVED)
- Consolidated issues checklist with agent attribution
- Decision with severity counts and next steps
