---
name: brain-updater
description: Update .brain/ context files after completing tasks. Use when: updating project context, documenting changes, maintaining activeContext.md, updating systemPatterns.md, tracking session progress, documenting decisions.
---

# Brain Updater

Update .brain/ files to maintain session context.

## When to Update

| File | When |
|------|-----|
| `activeContext.md` | After major tasks |
| `systemPatterns.md` | New patterns discovered |
| `projectRules.md` | Rarely (source of truth) |
| `plans/{feature}.md` | During planning |

## activeContext.md Template

```markdown
## Recent Changes
- [Brief description]

**Files Modified**:
- `path/to/file.py` - What changed

## Active Tasks
- [x] Completed task
- [ ] Pending task

## Decisions Made
| Decision | Rationale | Impact |
|----------|-----------|--------|
| Text | Why | What it affects |
```

## systemPatterns.md Template

Only add when discovering new reusable patterns:

```markdown
## N. Pattern Name

### When to Use
- Situation description

### Implementation
```python
# Example code
```

### Examples in Codebase
- `path/to/file.py:123` - Usage
```

## Example Update

```markdown
## Recent Changes
- Implemented HTTPRequestNode for browser automation
- Added async HTTP client with connection pooling

**Files Modified**:
- `src/casare_rpa/nodes/browser/http_node.py` - New node
- `tests/nodes/browser/test_http_node.py` - Tests

## Active Tasks
- [x] Implement HTTPRequestNode
- [x] Create test suite
- [ ] Document API
```
