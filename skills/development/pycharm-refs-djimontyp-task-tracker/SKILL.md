---
name: pycharm-refs
description: This skill should be used when agents need to provide clickable code references to users in reports, investigations, or bug findings. It ensures file references use the simple path:line_number format that Claude Code automatically converts to clickable links. Do not use for general documentation or conceptual explanations.
---

# Clickable Code References for Claude Code

## Overview

When providing code references to users that require immediate action or investigation, use the simple `path:line_number` format. Claude Code automatically recognizes this pattern and converts it to clickable links that open directly in the IDE.

## Critical Format Rule

**Use simple relative or absolute paths with colon and line number:**

```
path/to/file.py:LINE_NUMBER
backend/app/services/task_service.py:45
```

**Working directory context:** `{{env.WORKING_DIRECTORY}}`

## How It Works

1. Use tools like `Grep` or `Read` with `-n: true` parameter to see line numbers
2. Reference code using `path/to/file:line_number` format in responses
3. Claude Code automatically detects this pattern and makes it clickable
4. User clicks the link and IDE opens the file at that exact line

**No need for file:// protocol or special formatting!**

## When to Use This Format

Apply clickable references in these contexts:

- **Investigation reports** - Locations of bugs, performance bottlenecks, or issues
- **Analysis results** - Findings from code analysis or audits
- **Bug reports** - Specific locations where errors originate
- **Code review findings** - Problematic code segments that need attention
- **Implementation summaries** - Key changes made during development
- **Error locations** - Where exceptions or failures occur

The common pattern: if the user needs to **look at specific code right now**, make it clickable.

## When NOT to Use This Format

Skip clickable links in these contexts:

- **General documentation** - Architectural overviews, concept explanations
- **Conceptual references** - Discussing patterns or approaches without specific implementation
- **File structure descriptions** - Listing directory organization
- **Non-actionable mentions** - References that don't require user inspection

The common pattern: if the reference is **conceptual or documentary**, omit clickable links.

## Format Specifications

### Single Line Reference (Clickable)
```
backend/app/services/task_service.py:45
```

### Line Range Reference
Claude Code supports range format:
```
backend/app/models/contract.py:120
frontend/src/features/agents/components/TaskForm.tsx:55-58
```

### In Natural Language
```
Found performance bottleneck in the task classification loop at
backend/app/services/classification.py:156
```

### Multiple References
```
The validation error chain:
1. frontend/src/features/agents/components/TaskForm.tsx:89
2. backend/app/api/routes/tasks.py:234
3. backend/app/services/validation.py:67
```

## Examples

### ✅ Good Usage (Actionable Report)

```markdown
## Performance Analysis Results

Identified slow database queries:

1. N+1 query in task fetching
   backend/app/services/task_service.py:156

2. Missing index on topic_messages join
   backend/app/models/topic.py:45

3. Inefficient serialization in API response
   backend/app/api/routes/topics.py:89
```

### ✅ Good Usage (Bug Report)

```markdown
## TypeError in Task Creation

The error originates from missing validation:
frontend/src/features/agents/components/TaskForm.tsx:127

Root cause in schema definition:
backend/app/schemas/task.py:34
```

### ❌ Bad Usage (Documentation Context)

```markdown
## Architecture Overview

The service layer is organized in backend/app/services/
with helper utilities in backend/app/services/utils.py
```

**Why bad:** This is architectural documentation, not an actionable reference. No need for clickable links.

### ❌ Bad Usage (Conceptual Reference)

```markdown
## Design Patterns

We use dependency injection throughout the codebase, see backend/app/api/dependencies.py for examples.
```

**Why bad:** This is a conceptual explanation. The specific lines aren't relevant to understanding the pattern.

## Implementation Guidelines

When writing reports or providing findings:

1. **Use tools with line numbers** - Run `Grep` or `Read` with `-n: true` to see line numbers
2. **Identify context** - Is this report/investigation or documentation/concept?
3. **Check actionability** - Does the user need to inspect this code now?
4. **Use simple format** - If actionable, use `path/to/file:line_number` (relative or absolute)
5. **Omit if conceptual** - If discussing general architecture or patterns, use simple paths without line numbers

**Claude Code automatically converts `path:line` format to clickable links!**

Keep references **contextual and actionable** - clickable links are for helping users navigate to code they need to see immediately, not for documenting general file locations.
