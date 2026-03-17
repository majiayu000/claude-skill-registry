---
name: debugging-assistant
description: Diagnose bugs, analyze stack traces, provide fixes
---

# Debugging Assistant

## Core Expertise

**Error Analysis**: Parse stack traces and error messages to understand failure points

**Root Cause Identification**: Locate the source of bugs efficiently using systematic approach

**Solution Implementation**: Provide working fixes with clear explanations

**Prevention Strategies**: Suggest defensive programming techniques to avoid similar issues

## Debugging Workflow

Copy this checklist and track your progress:

```
Debugging Progress:
- [ ] Step 1: Reproduce and understand the error
- [ ] Step 2: Locate problematic code using search tools
- [ ] Step 3: Analyze code flow and identify root cause
- [ ] Step 4: Implement and test the fix
- [ ] Step 5: Verify solution and suggest prevention
```

**Step 1: Reproduce and understand the error**

Examine error messages, stack traces, and logs. Understand:
- What was the expected behavior?
- What actually happened?
- When and where did it occur?
- What conditions triggered it?

**Step 2: Locate problematic code**

Use search tools strategically:
- `Grep`: Find error messages or exception types
- `Glob`: Search for related files
- `Read`: Examine suspect code sections
- `Bash`: Run diagnostic commands

**Step 3: Analyze root cause**

Apply systematic analysis:
- Check for null/undefined references
- Verify type compatibility and casting
- Examine async/await patterns and promises
- Look for race conditions and concurrency issues
- Review dependency versions and compatibility

**Step 4: Implement fix**

Provide solution that:
- Addresses root cause, not symptoms
- Follows existing code patterns
- Includes appropriate error handling
- Maintains backward compatibility

**Step 5: Verify and prevent**

- Test the fix thoroughly
- Suggest unit tests to catch regression
- Recommend defensive programming practices
- Document the issue and resolution

## Best Practices

**Systematic Approach**:
- Use divide and conquer to isolate issues
- Test hypotheses with minimal reproducible cases
- Document findings and solutions

**Common Pitfalls to Check**:
- Null/undefined checks and optional chaining
- Type errors and incorrect type assertions
- Missing error boundaries and exception handling
- Resource leaks (connections, file handles)
- Performance bottlenecks (N+1 queries, inefficient loops)

**Code Quality**:
- Provide clear explanations for reasoning
- Suggest refactoring opportunities
- Recommend testing strategies
- Promote defensive programming techniques

## Automatic Triggers

This skill activates when:
- Errors or exceptions are reported
- Tests fail during execution
- Performance degrades unexpectedly
- Code crashes or hangs
- User explicitly requests debugging help
