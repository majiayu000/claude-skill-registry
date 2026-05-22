---
name: debugging
description: Hypothesis-driven debugging with systematic investigation. Identifies root causes, creates minimal reproductions, and implements fixes. Use when investigating errors, bugs, crashes, or unexpected behavior.
---

# Debugging

Systematic debugging using hypothesis testing and root cause analysis.

## When to Use

- Error investigation (exceptions, crashes)
- Unexpected behavior diagnosis
- Performance issue root cause
- Integration/dependency failures

## MCP Workflow

```
# 1. Get code at error location
serena.find_symbol(name_path="ErrorClass/method", include_body=True)

# 2. Trace call chain
serena.find_referencing_symbols(name_path="ErrorClass/method")

# 3. Search for similar patterns (TOKEN CRITICAL - Always limit!)
serena.search_for_pattern(
    substring_pattern="null.*check",
    relative_path="src/",
    context_lines_after=1,
    max_answer_chars=3000
)

# 4. Check past similar issues
claude-mem.search(query="<error-type>", project="<project>")

# 5. Framework error handling
context7.get-library-docs("<framework>", topic="exception handling")
```

## Workflow

### 1. Observe
```
- Error message and stack trace
- Steps to reproduce
- When did it start? (recent changes?)
- Scope (one user? all?)
```

### 2. Hypothesize
```
Based on: [observation]
Hypothesis: [proposed cause]
Test: [how to verify]
```

### 3. Test
```
serena.find_symbol("SuspectedClass/method", include_body=True)
serena.find_referencing_symbols("SuspectedCause")
# Log analysis, local reproduction
```

### 4. Fix
```
1. Write failing test that reproduces bug
2. Implement minimal fix
3. Verify test passes
4. Run full test suite
```

### 5. Prevent
```
- Add edge case tests
- Improve validation
- Update documentation
```

## Common Patterns

### Null/Undefined
**Symptoms:** NullPointerException, "undefined is not a function"
**Investigate:**
- Find where null originates
- Trace back through call chain
- Check data presence assumptions

### Race Condition
**Symptoms:** Intermittent, works in debug mode
**Red flags:**
- Shared mutable state
- Missing synchronization
- Execution order assumptions

### Data Inconsistency
**Investigate:**
- Trace data flow source to error
- Check transformation logic
- Verify cache invalidation

## Investigation Techniques

### Git Bisect
```bash
git bisect start
git bisect bad
git bisect good <commit>
# Test middle commit, mark good/bad
git bisect reset
```

### Stack Trace Analysis
```
Start at bottom (entry point)
Move up to error line
Examine code at that line
Check what could be null/invalid
```

### Divide and Conquer
```
A -> B -> C -> D (output wrong)
Check B: correct? -> problem in C or D
        wrong?   -> problem in A or B
```

## Output Format

```markdown
## Bug: [Title]

### Symptoms
- Error: [message]
- Location: `file:line`

### Investigation
**Hypothesis 1:** [description]
- Test: [method]
- Result: Confirmed / Ruled Out

### Root Cause
[Identified cause] at `file:line`

### Fix
[Description]

### Prevention
- [ ] Test added
- [ ] Similar patterns checked
```

## Checklist

- [ ] Can reproduce consistently
- [ ] Stack trace analyzed
- [ ] Root cause identified (not just symptom)
- [ ] Failing test written
- [ ] Fix implemented
- [ ] Full test suite passes
