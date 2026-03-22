---
name: audit-defense-standards
description: Audit the codebase against defense standards derived from historical bug patterns. Standards accumulate over time as new patterns are discovered via audit-bugs and design-guards. Use when user says "audit defenses", "audit defense standards", "check defenses", or "defense audit".
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '[SKILL: audit-defense-standards] Auditing defense standards compliance...'"
          once: true
---

# Defense Standards Audit Skill

Audit the codebase against defense standards derived from historical bug pattern analysis. Each standard represents an architectural lesson learned from real bugs - a guard that prevents an entire class of bugs, not just one instance.

Standards are added here when `/design-guards` recommends them and the user approves.

## When to Use

- User says "audit defenses", "audit defense standards", "check defenses"
- As a periodic health check to catch regressions
- After major refactors to verify guards still hold

## Critical Constraints

**NEVER:**
- Modify any source code files
- Update an existing report - always generate new

**ALWAYS:**
- Use subagents for parallel exploration (one per standard or group)
- All output goes under `temp/audit-defense-standards/` (create if needed)
- Final report: `temp/audit-defense-standards/defense_audit_{YYYY-MM-DD_HHMMSS}.md`
- Subagents must NOT create their own files - they return findings in their response text only
- Provide file paths and line numbers for violations
- Categorize by severity

---

## Defense Standards Template

This skill requires project-specific defense standards. Define them in this section following the format below.

### Example Defense Standards

The following examples show common patterns applicable to many codebases. Replace these with project-specific standards derived from your bug pattern analysis.

---

### DS-1: Typed Boundaries Over Raw Data Access

**Rule:** Data crossing component boundaries must pass through typed accessors or validation. No raw `dict.get()` or unvalidated external input at boundary crossings.

**Audit Strategy:**
- Find raw dict/JSON access on data crossing component boundaries
- Check that boundary-crossing functions use typed parameters, not `Dict[str, Any]` or unvalidated strings
- Verify no mutation of caller's data (`.pop()` on function parameters)
- Look for direct external input consumption without schema validation

**Severity:** HIGH

---

### DS-2: Error Context Preservation

**Rule:** When error/failure data passes through transformations or wrappers, the error message/context must be explicitly preserved. Broad exception handlers must not swallow programmer errors.

**Audit Strategy:**
- Trace error context through transformation chains
- Verify all error factory methods preserve error messages when wrapping
- Find `except Exception` and `except BaseException` handlers; verify each is narrowed or justified
- Check that error logs include actionable context (not just "An error occurred")

**Severity:** HIGH

---

### DS-3: Validation at Construction Time

**Rule:** Domain objects must be validated at construction time, not only at persistence boundaries. Direct constructors must not bypass validators.

**Audit Strategy:**
- Find direct constructor calls for domain models; verify validators fire
- Check that validation happens before business logic operates on the data
- Verify validation errors propagate (not swallowed or logged-only)
- Look for late validation (only at save/persist) that allows invalid state in memory

**Severity:** HIGH

---

## Adding Project-Specific Standards

Defense standards come from the `/design-guards` pipeline:

1. `/audit-bugs` identifies recurring patterns
2. `/design-guards` investigates solutions and recommends standards
3. User approves which recommendations become permanent standards
4. Add the approved standards to this file following the format below

**Standard format:**
```markdown
### DS-N: {Short Name}

**Rule:** {One-sentence rule statement}

**Audit Strategy:**
{Concrete steps subagents should take to check compliance}

**Severity:** {CRITICAL / HIGH / MEDIUM / LOW}
```

**Before first use:** Replace the example standards above with your project's actual defense standards, or keep them as a starting point and add project-specific ones as they're discovered.

---

## Audit Workflow

1. **Launch parallel subagents** - one per standard or group of related standards
2. **Each subagent:** runs the audit strategy, reports violations with file paths and line numbers
3. **Consolidate findings** by standard and severity
4. Ensure `temp/audit-defense-standards/` exists (`mkdir -p`)
5. **Write report** to `temp/audit-defense-standards/defense_audit_{YYYY-MM-DD_HHMMSS}.md`
6. **Output summary** to terminal: violation count per standard, total by severity

## Report Structure

```markdown
# Defense Standards Audit

**Date:** {today}
**Standards Checked:** {count}

## Summary
| Standard | Violations | Severity |
|----------|-----------|----------|
| DS-1: Typed Boundaries | X | HIGH |
| DS-2: Error Context | X | HIGH |
| ... | ... | ... |

## DS-N: {Standard Name}

### Violations
- {file}:{line} - {description of violation}

### Compliant Patterns Found
{Brief note on good patterns found, if any}
```

---

## Severity Guidelines

**CRITICAL:** Violations that can cause silent data corruption or unrecoverable state
**HIGH:** Violations that cause crashes, validation bypass, or error masking
**MEDIUM:** Violations that cause incorrect behavior in edge cases
**LOW:** Violations that affect code quality but not correctness
