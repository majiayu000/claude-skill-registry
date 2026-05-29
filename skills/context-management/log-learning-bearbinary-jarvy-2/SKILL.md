---
name: log-learning
description: "Log key learnings to progress.txt during PRD iteration. Use when you discover codebase patterns, encounter gotchas, make important decisions, or learn something that would help future work sessions. Triggers on: log learning, add to progress, capture insight, record pattern, note gotcha, save lesson."
---

# Log Learning

Capture key insights and learnings to progress.txt while iterating on PRD tasks. This file serves as session memory that is ingested at the start of subsequent work sessions.

## When to Use

Invoke this skill whenever you:
- Discover a codebase pattern that affects implementation
- Encounter a gotcha or unexpected behavior
- Make an architectural or design decision
- Find a workaround for a tricky problem
- Learn something about dependencies, APIs, or tooling
- Complete a task and want to capture what was learned

## Progress File Location

The progress file is at the project root: `progress.txt`

## Learning Categories

### 1. Codebase Patterns
Structural patterns discovered while working:

```markdown
## Codebase Patterns

- Middleware uses `MiddlewareParams` struct for dependency injection
- Echo RequestLoggerWithConfig used for custom request logging
- Request ID middleware should be early in chain
- slog is the standard library structured logger
```

### 2. Task Completion Notes
Append after completing work on a user story or task:

```markdown
---

## US-XXX: [Task Title]
Status: COMPLETE

### What was implemented:
- Specific change 1
- Specific change 2

### Files changed:
- path/to/file1.go
- path/to/file2.go

### Key learnings:
- Pattern discovered or reinforced
- Gotcha encountered
- Important decision made

---
```

### 3. Gotchas and Warnings
Issues to watch out for:

```markdown
### Gotchas:
- NATS JetStream requires explicit bucket creation before use
- Echo context must be cast for custom types
- Air hot-reload doesn't detect new files without restart
```

### 4. Decisions Made
Record why certain approaches were chosen:

```markdown
### Decision: [What was decided]
- Context: [situation]
- Options: [alternatives considered]
- Rationale: [why this choice]
```

## How to Log

### Quick Pattern Log
When you discover a pattern, append to the `## Codebase Patterns` section:

```bash
# Read current progress.txt first, then edit to add the pattern
```

### Task Completion Log
After completing a task:

1. Read the current progress.txt
2. Update the task status to COMPLETE
3. Add implementation notes under the task section
4. Append key learnings

### Session Summary
At the end of a work session, ensure progress.txt contains:
- Updated status for all worked tasks
- New patterns in the Codebase Patterns section
- Any gotchas discovered
- Important decisions made

## Format Guidelines

- Keep entries concise but informative
- Use bullet points for easy scanning
- Include file paths when relevant
- Link patterns to specific implementations
- Group related learnings together
- Use `---` separators between major sections

## Example Progress Entry

```markdown
---

## US-003: Add Request ID Middleware
Status: COMPLETE

### What was implemented:
- Created requestid.go middleware using X-Request-ID header
- Falls back to UUID generation when header not present
- Integrated with slog for trace correlation

### Files changed:
- services/api/middleware/requestid.go
- services/api/middleware/middleware.go
- services/api/middleware/slogger.go

### Key learnings:
- Request ID must be early in middleware chain for other middleware to use it
- Echo's c.Set() stores in request-scoped context
- Use c.Response().Header().Set() to echo ID back to caller

---
```

## Progress File Template

If starting fresh, initialize with:

```markdown
# Progress Log
Started: [date]

## Current Session - [Feature/PRD Name]
Source: [path to PRD or task file]

---

## Codebase Patterns (from this session)

[Patterns discovered during work]

---

[Task entries will be appended here]
```

## Key Principles

1. **Log immediately**: Capture learnings as they happen, not at the end
2. **Be specific**: Include file paths, function names, concrete details
3. **Think future-you**: Write what you'd want to know when resuming
4. **Compound knowledge**: Each learning should make future work easier
5. **Keep it scannable**: Bullet points and clear headers over paragraphs
