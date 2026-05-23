---
name: error-debugger
description: Analyzes errors, searches past solutions in memory, provides immediate fixes with code examples, and saves solutions for future reference. Use when user says "debug this", "fix this error", "why is this failing", or when error messages appear like TypeError, ECONNREFUSED, CORS, 404, 500, etc.
---

# Error Debugger

## Purpose

Context-aware debugging that learns from past solutions. When an error occurs:
1. Searches memory for similar past errors
2. Analyzes error message and stack trace
3. Provides immediate fix with code examples
4. Creates regression test via testing-builder
5. Saves solution to memory for future

**For ADHD users**: Eliminates debugging frustration - instant, actionable fixes.
**For SDAM users**: Recalls past solutions you've already found.
**For all users**: Gets smarter over time as it learns from your codebase.

## Activation Triggers

- User says: "debug this", "fix this error", "why is this failing"
- Error messages containing: TypeError, ReferenceError, SyntaxError, ECONNREFUSED, CORS, 404, 500, etc.
- Stack traces pasted into conversation
- "Something's broken" or similar expressions

## Core Workflow

### 1. Parse Error

Extract key information:

```javascript
{
  error_type: "TypeError|ReferenceError|ECONNREFUSED|...",
  message: "Cannot read property 'map' of undefined",
  stack_trace: [...],
  file: "src/components/UserList.jsx",
  line: 42,
  context: "Rendering user list"
}
```

### 2. Search Past Solutions

Query context-manager:

```
search memories for:
- error_type match
- similar message (fuzzy match)
- same file/component if available
- related tags (if previously tagged)
```

**If match found**:
```
🔍 Found similar past error!

📝 3 months ago: TypeError in UserList component
✅ Solution: Added null check before map
⏱️ Fixed in: 5 minutes
🔗 Memory: procedures/{uuid}.md

Applying the same solution...
```

**If no match**:
```
🆕 New error - analyzing...
(Will save solution after fix)
```

### 3. Analyze Error

See [reference.md](reference.md) for comprehensive error pattern library.

**Quick common patterns**:

- **TypeError: Cannot read property 'X' of undefined** → Optional chaining + defaults
- **ECONNREFUSED** → Check service running, verify ports
- **CORS errors** → Configure CORS headers
- **404 Not Found** → Verify route definition
- **500 Internal Server Error** → Check server logs

### 4. Provide Fix

**Format**:
```
🔧 Error Analysis

**Type**: {error_type}
**Location**: {file}:{line}
**Cause**: {root_cause_explanation}

**Fix**:

```javascript
// ❌ Current code
const users = data.users;
return users.map(user => <div>{user.name}</div>);
```

```javascript
// ✅ Fixed code
const users = data?.users || [];
return users.map(user => <div>{user.name}</div>);
```

**Explanation**: Added optional chaining and default empty array to handle case where data or data.users is undefined.

**Prevention**: Always validate API response structure before using.

**Next steps**:
1. Apply the fix
2. Test manually
3. I'll create a regression test
```

### 5. Save Solution

After fix confirmed working:

```bash
# Save to context-manager as PROCEDURE
remember: Fix for TypeError in map operations
Type: PROCEDURE
Tags: error, typescript, array-operations
Content: When getting "Cannot read property 'map' of undefined",
         add optional chaining and default empty array:
         data?.users || []
```

**Memory structure**:
```markdown
# PROCEDURE: Fix TypeError in map operations

**Error Type**: TypeError
**Message Pattern**: Cannot read property 'map' of undefined
**Context**: Array operations on potentially undefined data

## Solution

Use optional chaining and default values:

```javascript
// Before
const items = data.items;
return items.map(...)

// After
const items = data?.items || [];
return items.map(...)
```

## When to Apply

- API responses that might be undefined
- Props that might not be passed
- Array operations on uncertain data

## Tested

✅ Fixed in UserList component (2025-10-17)
✅ Regression test: tests/components/UserList.test.jsx

## Tags

error, typescript, array-operations, undefined-handling
```

### 6. Create Regression Test

Automatically invoke testing-builder:

```
create regression test for this fix:
- Test that component handles undefined data
- Test that component handles empty array
- Test that component works with valid data
```

## Tool Persistence Pattern (Meta-Learning)

**Critical principle from self-analysis**: Never give up on first obstacle. Try 3 approaches before abandoning a solution path.

### Debugging Tools Hierarchy

When debugging an error, try these tools in sequence:

**1. Search Past Solutions (context-manager)**
```bash
# First approach: Check memory
search memories for error pattern
```

If no past solution found → Continue to next approach

**2. GitHub Copilot CLI Search**
```bash
# Second approach: Search public issues
copilot "Search GitHub for solutions to: $ERROR_MESSAGE"
```

If Copilot doesn't find good results → Continue to next approach

**3. Web Search with Current Context**
```bash
# Third approach: Real-time web search
[Use web search for latest Stack Overflow solutions]
```

If web search fails → Then ask user for more context

### Real Example from Meta-Analysis

**What happened**: Tried GitHub MCP → Got auth error → Immediately gave up

**What should have happened**:
1. Try GitHub MCP → Auth error
2. Try `gh` CLI → Check if authenticated
3. Try direct GitHub API → Use personal token
4. Then create manual instructions if all fail

**Outcome**: The `gh` CLI WAS authenticated and worked perfectly. We gave up too early.

### Applying This to Error Debugging

When fixing an error:

```javascript
// Pattern: Try 3 fix approaches
async function debugError(error) {
  // Approach 1: Past solution
  const pastFix = await searchMemories(error);
  if (pastFix?.success_rate > 80%) {
    return applyPastFix(pastFix);
  }

  // Approach 2: Pattern matching
  const commonFix = matchErrorPattern(error);
  if (commonFix) {
    return applyCommonFix(commonFix);
  }

  // Approach 3: External search (Copilot/Web)
  const externalSolution = await searchExternalSolutions(error);
  if (externalSolution) {
    return applyExternalSolution(externalSolution);
  }

  // Only NOW ask for more context
  return askUserForMoreContext(error);
}
```

### Integration Tool Persistence

When integrations are available, use them in this order:

**For Error Search**:
1. GitHub Copilot CLI → Search issues in your repos and similar projects
2. Local memory → Past solutions you've saved
3. Web search → Latest Stack Overflow/docs

**For Solutions**:
1. Past solution from memory (fastest)
2. Codegen-ai agent (if complex bug) → Automated PR
3. Jules CLI async task (if time-consuming fix)
4. Manual fix with code examples

### Metrics

Track debugging approach success:

```json
{
  "error_id": "uuid",
  "approaches_tried": [
    {"type": "memory_search", "result": "no_match"},
    {"type": "copilot_search", "result": "success", "time": "5s"},
    {"type": "applied_fix", "verified": true}
  ],
  "total_time": "30s",
  "lesson": "Copilot found solution on second try"
}
```

**Key insight**: Most "failed" approaches are actually "didn't try enough" approaches.

## Context Integration

### Query Past Solutions

Before analyzing new error:

```javascript
// Search context-manager
const pastSolutions = searchMemories({
  type: 'PROCEDURE',
  tags: [errorType, language, framework],
  content: errorMessage,
  fuzzyMatch: true
});

if (pastSolutions.length > 0) {
  // Show user the past solution
  // Ask if they want to apply it
  // If yes, apply and test
  // If no, analyze fresh
}
```

### Learning Over Time

Track which solutions work:

```javascript
{
  solution_id: "uuid",
  error_pattern: "TypeError.*map.*undefined",
  times_applied: 5,
  success_rate: 100%,
  last_used: "2025-10-15",
  avg_fix_time: "2 minutes"
}
```

Sort solutions by success rate when multiple matches found.

### Project-Specific Patterns

Some errors are project-specific:

```javascript
// BOOSTBOX-specific
Error: "Boost ID not found"
→ Solution: Check boost exists before processing

// Tool Hub-specific
Error: "Tool not installed"
→ Solution: Run tool installer first

// Save these as PROJECT-specific procedures
```

## Integration with Other Skills

### Testing Builder

After providing fix:
```
Automatically invoke: testing-builder
Create regression test for: {error_scenario}
Ensure test fails without fix, passes with fix
```

### Context Manager

Query for similar errors:
```
search memories for:
- PROCEDURE type
- Error tag
- Similar message
- Same file/component
```

Save new solutions:
```
Save as PROCEDURE:
- Error pattern
- Solution
- Code examples
- Tested timestamp
```

### Rapid Prototyper

For complex fixes:
```
If fix requires significant refactoring:
→ Invoke rapid-prototyper
→ Create isolated example showing fix
→ User validates before applying to codebase
```

## Additional Resources

- **[Error Pattern Library](reference.md)** - Comprehensive patterns for JavaScript, Network, Database, React errors
- **[Debugging Examples](examples.md)** - Step-by-step debugging workflow examples

## Quick Reference

### Common Error Patterns

| Error | Quick Fix |
|-------|-----------|
| `undefined.map` | `data?.array || []` |
| `X is not a function` | Check function exists |
| `ECONNREFUSED` | Check service running |
| `CORS` | Configure CORS headers |
| `404` | Verify route exists |
| `500` | Check server logs |
| `Timeout` | Increase timeout value |
| `Cannot find module` | Install dependency |

### Trigger Phrases

- "debug this"
- "fix this error"
- "why is this failing"
- "something's broken"
- [paste error message]
- [paste stack trace]

### File Locations

- **Past solutions**: `~/.claude-memories/procedures/` (Linux/macOS) or `%USERPROFILE%\.claude-memories\procedures\` (Windows)
- **Error patterns**: Tagged with "error" in memory index

### Success Criteria

✅ Common errors fixed instantly (<30 seconds)
✅ Past solutions automatically recalled
✅ All fixes include code examples
✅ Regression tests created automatically
✅ Solutions saved for future reference
✅ Debugging gets faster over time
