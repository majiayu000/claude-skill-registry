---
name: code-audit
description: Audits the entire codebase for bugs, security vulnerabilities, CLAUDE.md violations, dead code, duplicate code, and test quality issues. Use when asked to "audit code", "find bugs", "review codebase", "check for security issues", or "find dead code". Writes prioritized findings to TODO.md without suggesting fixes.
argument-hint: [optional: specific area like "services" or "tests"]
allowed-tools: Read, Edit, Write, Glob, Grep, Task
disable-model-invocation: true
---

Perform a comprehensive code audit and write findings to TODO.md.

## Pre-flight

1. **Read CLAUDE.md** - Load project rules to audit against
2. **Read TODO.md** - Preserve existing items (will be renumbered)

## Audit Process

Copy this checklist and track progress:

```
Audit Progress:
- [ ] Step 1: Explore codebase systematically
- [ ] Step 2: Check CLAUDE.md compliance
- [ ] Step 3: Collect and categorize findings
- [ ] Step 4: Write TODO.md with priority ordering
```

### Step 1: Systematic Exploration

Use Task tool with `subagent_type=Explore` to examine each area. If `$ARGUMENTS` specifies a focus area, prioritize that.

**Areas to examine:**
- `src/services/` - Core services
- `src/processing/` - Processing pipeline
- `src/routes/` - API routes
- `src/gemini/` - Gemini integration
- `src/utils/` - Utilities
- `src/bank/` - Bank logic
- `src/**/*.test.ts` - Tests

**For each area, look for:**
- Logic errors, null handling, race conditions
- Security vulnerabilities (injection, missing auth, exposed secrets)
- Unhandled edge cases and boundary conditions
- Dead or duplicate code
- Test quality issues (no assertions, always-pass, duplicates)

### Step 2: CLAUDE.md Compliance

Check project-specific rules. See [references/compliance-checklist.md](references/compliance-checklist.md) for the complete list.

### Step 3: Categorize Findings

| Tag | Description | Priority |
|-----|-------------|----------|
| `[security]` | Injection, exposed secrets, missing auth | Critical |
| `[bug]` | Logic errors, data corruption | Critical/High |
| `[edge-case]` | Unhandled scenarios | Medium |
| `[convention]` | CLAUDE.md violations | Medium |
| `[type]` | Unsafe casts, missing guards | Medium |
| `[dead-code]` | Unused functions, unreachable code | Low |
| `[duplicate]` | Repeated logic | Low |
| `[test]` | Useless/duplicate tests | Low |
| `[practice]` | Anti-patterns | Low |

**For each issue, document:**
- File path and approximate location
- Clear problem description
- Category tag

**Do NOT document solutions.** Identify problems only.

### Step 4: Write TODO.md

**Handle Existing Items:**
1. If TODO.md already has items, extract them first
2. Reformat each existing item to follow `## item #N [tag]` format
   - If item lacks a tag, infer appropriate tag from content
   - If item is a simple bullet, convert to proper format
3. Keep existing items in their original order

**Write Final TODO.md:**

```markdown
# TODO

## item #1 [tag]
First existing item (reformatted if needed)

## item #2 [tag]
Second existing item (reformatted if needed)

---

# Code Audit Findings

## item #3 [security]
Description of the security issue.

## item #4 [bug]
Description of the bug.

## item #5 [convention]
Description of the CLAUDE.md violation.
```

**Rules:**
- Each item: `## item #N [tag]`
- Content: Simple paragraph explaining the problem
- NO solutions
- Existing items stay at top in original order (items #1-N)
- Separator line (`---`) between existing and new items
- New audit findings below separator, ordered by priority (items #N+1 onwards)
- All items numbered sequentially

## Rules

- **Analysis only** - Do NOT modify source code
- **No solutions** - Document problems, not fixes
- **Be thorough** - Check every file in scope
- **Be specific** - Include file paths
- **No time wasting** - Don't analyze how to fix

## Termination

Output this message and STOP:

```
✓ Code audit complete. Findings written to TODO.md.

Found N issues:
- X critical/high priority
- Y medium priority
- Z low priority

Next step: Review TODO.md and use `plan-todo` to create implementation plans.
```

Do not ask follow-up questions. Do not offer to fix issues.
