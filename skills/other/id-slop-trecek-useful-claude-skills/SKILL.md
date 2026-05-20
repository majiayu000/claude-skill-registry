---
name: id-slop
description: Identify AI-generated code slop in the codebase - useless comments, backward compatibility hacks, deprecation notices, dead code, and other technical debt left by AI assistants. Use when user says "id slop", "identify slop", "find slop", or "code cleanup scan". Generates a removal plan in temp/ and validates it with dry walkthrough.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '🧹 [SKILL: id-slop] Scanning for AI-generated slop...'"
          once: true
---

# Slop Identification Skill

Identify and catalog AI-generated code slop in the codebase. Slop is useless code patterns left behind by AI assistants during rapid development - comments that won't make sense to future readers, backward compatibility hacks, dead code, and other technical debt.

## When to Use

- User says "id slop", "identify slop", "find slop"
- User wants "code cleanup" or "cleanup scan"
- User mentions "AI-generated junk" or "leftover comments"
- User asks to "find useless comments" or "remove dead code"

## Critical Constraints

**NEVER:**
- Modify any source code files (this skill only IDENTIFIES slop)
- Remove code without creating a removal plan first
- Flag legitimate comments, documentation, or architectural patterns
- Flag TODO comments that describe actual future work

**ALWAYS:**
- Use subagents for parallel exploration
- Write the slop removal plan to `temp/id-slop/` directory
- Provide file paths and line numbers for each finding
- Run dry walkthrough on the generated plan
- Categorize slop by type for prioritized removal

## Slop Categories

### Category 1: Phase Reference Comments (HIGH PRIORITY)
Comments mentioning numbered phases from AI implementation plans that won't make sense to future readers.

**Patterns to detect:**
- `Phase [0-9]` in comments or docstrings
- `# Phase 1:`, `# Phase 2:`, etc.
- References to "implementation phase" or "migration phase" with numbers
- `Part of Phase X` comments

**Example slop:**
```python
# Phase 5: Migrate Checkpoint and Session Management
def migrate_session():  # Part of Phase 2 migration
```

### Category 2: Backward Compatibility Hacks (HIGH PRIORITY)
Parameters or code kept solely for "API compatibility" that's no longer needed.

**Patterns to detect:**
- `kept for API compatibility`
- `kept for backward compatibility`
- `unused but kept for`
- `ignored - kept for`
- Parameters that are documented as "unused" or "ignored"

**Example slop:**
```python
use_file_lock: bool = True,  # Ignored - kept for API compatibility
log_dir: Optional[Path] = None,  # Ignored - kept for API compatibility
```

### Category 3: Removed Code Comments (MEDIUM PRIORITY)
Comments explaining what was removed without explaining what replaced it.

**Patterns to detect:**
- `removed in Phase`
- `no longer needed`
- `NOTE: X removed`
- References to deleted features or functions

**Example slop:**
```python
# NOTE: test-and-log removed in Phase 4. Use simple 'test' task.
# baseline_manager removed - now handled by executor
```

### Category 4: Deprecation Notices (MEDIUM PRIORITY)
Comments marking code as deprecated without removal timeline or replacement guidance.

**Patterns to detect:**
- `deprecated` without clear migration path
- `@deprecated` decorators on live code
- `will be removed` without version/date
- Stale deprecation warnings

### Category 5: Fallback/Workaround Code (HIGH PRIORITY)
Fallback logic that masks errors instead of failing fast.

**Patterns to detect:**
- `try: ... except: pass` blocks that swallow all exceptions
- `# Silently ignore` comments
- Fallback methods that don't log the original error
- `ignore_errors=True` without logging

**Example slop:**
```python
try:
    result = risky_operation()
except:
    pass  # Silently ignore errors
```

### Category 6: Type System Bypasses (LOW PRIORITY)
Comments that bypass type checking instead of fixing the actual type issue.

**Patterns to detect:**
- `# type: ignore` without explanation
- `# noqa` without specific error code
- `cast()` calls that don't make type sense

**Example slop:**
```python
entry.status = status  # type: ignore
return wrapper  # type: ignore
```

### Category 7: Dead Placeholder Code (MEDIUM PRIORITY)
Stub implementations, placeholder nodes, or scaffolding never replaced.

**Patterns to detect:**
- Functions with only `pass` or `...` bodies
- `placeholder` or `stub` in function names
- `# TODO: implement` without implementation
- Test scaffolding left in production code

**Example slop:**
```python
def find_next_placeholder(state):
    """Placeholder node for testing."""
    pass
```

### Category 8: Unreachable Code Comments (LOW PRIORITY)
Comments explaining why code is unreachable or can't happen.

**Patterns to detect:**
- `# This should be unreachable`
- `# Acknowledge unused parameter`
- `# satisfies mypy` for dead code paths
- Defensive code for impossible states

**Example slop:**
```python
# This should be unreachable if retry_attempts > 0, but satisfies mypy
raise RuntimeError("Unreachable")
```

### Category 9: Commented-Out Code (HIGH PRIORITY)
Code blocks that are commented out instead of deleted.

**Patterns to detect:**
- Multi-line commented code blocks
- `# old_function()` style commented calls
- `# return old_value` commented returns

### Category 10: Dead Code (HIGH PRIORITY)
Unused functions, classes, methods, imports, variables, and constants that are never referenced anywhere in the codebase.

**Patterns to detect:**
- Functions/methods with no callers
- Classes never instantiated or subclassed
- Imports not used in the module
- Variables/constants assigned but never read
- Module-level code that serves no purpose

## Investigation Workflow

### Step 1: Launch Parallel Subagents

Spawn 4-6 Explore subagents to scan different slop categories simultaneously:

```
Subagent 1: Phase References & Deprecation
- Search for "Phase [0-9]" patterns in comments
- Search for "deprecated" markers
- Search for "removed in" comments

Subagent 2: Backward Compatibility & Fallbacks
- Search for "kept for" compatibility patterns
- Search for "ignored" parameters
- Search for silent error handling

Subagent 3: Dead Code & Placeholders
- Search for placeholder/stub functions
- Search for unused imports with noqa
- Search for pass-only function bodies

Subagent 4: Type Bypasses & Unreachable Code
- Search for "type: ignore" without explanation
- Search for "noqa" suppressions
- Search for "unreachable" comments

Subagent 5: Commented-Out Code
- Search for multi-line comment blocks that look like code
- Search for commented function calls
- Search for # old_ patterns

Subagent 6: Dead Code
- Search for functions/classes with no callers
- Search for unused imports
- Search for assigned-but-never-read variables
```

### Step 2: Consolidate Findings

After subagents complete, organize findings by:
1. **File path**
2. **Line number(s)**
3. **Slop category**
4. **Priority** (HIGH/MEDIUM/LOW)
5. **Removal action** (delete line, delete block, refactor)

### Step 3: Generate Removal Plan

Write a structured removal plan to: `temp/id-slop/slop_removal_plan_{YYYY-MM-DD_HHMMSS}.md`

The plan should follow this format:

```markdown
# Slop Removal Plan

**Date:** {YYYY-MM-DD}
**Scope:** {directories scanned}
**Total Findings:** {count}

## Summary by Category

| Category | Count | Priority |
|----------|-------|----------|
| Phase References | X | HIGH |
| Backward Compatibility | X | HIGH |
| ... | ... | ... |

## Phase 1: High Priority - Phase Reference Comments

### Objective
Remove all phase reference comments that won't make sense to future readers.

### Files to Modify

- `path/to/file.py:LINE`: Remove comment "# Phase 5: ..."
- `path/to/file.py:LINE-LINE`: Remove docstring section mentioning phases

### Implementation Steps
1. Delete line X in file.py containing "Phase 5" comment
2. Delete lines X-Y in file2.py containing phase docstring
...

### Success Criteria
- [ ] No "Phase [0-9]" patterns remain in comments
- [ ] Code still functions correctly

### Verification
```bash
grep -rn "Phase [0-9]" src/ --include="*.py" | grep -v "test"
```

## Phase 2: High Priority - Backward Compatibility Hacks

### Objective
Remove unused parameters kept for backward compatibility.

### Files to Modify
...

## Phase N: Final Verification

### Verification Commands
```bash
# Run linting/formatting checks and full test suite
```

### Success Criteria
- [ ] All tests pass
- [ ] No linting errors
- [ ] No functional regressions
```

### Step 4: Run Dry Walkthrough

After generating the removal plan, invoke the dry walkthrough skill:

```
Now running dry walkthrough on the slop removal plan...
```

### Step 5: Report Summary

Output to terminal:

```
## Slop Identification Complete

**Plan:** temp/id-slop/slop_removal_plan_{YYYY-MM-DD_HHMMSS}.md
**Total Findings:** {count}

### By Priority
- HIGH: {count} items (should fix immediately)
- MEDIUM: {count} items (fix when touching these files)
- LOW: {count} items (fix opportunistically)

### By Category
1. Phase References: {count}
2. Backward Compatibility: {count}
3. Removed Code Comments: {count}
4. Fallback/Workaround Code: {count}
5. Dead Placeholder Code: {count}
6. Type Bypasses: {count}
7. Dead Code: {count}

### Next Steps
1. Review the plan at temp/id-slop/slop_removal_plan_{YYYY-MM-DD_HHMMSS}.md
2. Dry walkthrough has been run - check for any issues
3. Implement the plan phase by phase
```

## Search Patterns Reference

Use these regex patterns for searching:

```bash
# Phase references
grep -rn "Phase [0-9]" --include="*.py"
grep -rn "# Phase" --include="*.py"

# Backward compatibility
grep -rn "kept for.*compatibility" --include="*.py"
grep -rn "ignored.*kept for" --include="*.py"

# Removed code
grep -rn "removed in Phase" --include="*.py"
grep -rn "no longer needed" --include="*.py"

# Fallbacks
grep -rn "except:.*pass" --include="*.py"
grep -rn "ignore_errors=True" --include="*.py"
grep -rn "Silently ignore" --include="*.py"

# Type bypasses
grep -rn "# type: ignore$" --include="*.py"
grep -rn "# noqa$" --include="*.py"

# Placeholders
grep -rn "placeholder" --include="*.py"
grep -rn "def.*stub" --include="*.py"

# Unreachable
grep -rn "should be unreachable" --include="*.py"
grep -rn "satisfies mypy" --include="*.py"
```

## Exclusions

Do NOT flag as slop:

1. **Architecture documentation** - Comments explaining design decisions
2. **API documentation** - Docstrings explaining parameters and return values
3. **Legitimate TODOs** - TODOs with clear descriptions of future work
4. **Test-specific code** - Mocks, fixtures, and test utilities
5. **Intentional type ignores** - Type ignores with explanatory comments
6. **Error handling with logging** - Exception handlers that log errors
7. **Feature flags** - Conditional code controlled by configuration
