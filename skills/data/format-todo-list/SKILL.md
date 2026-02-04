---
name: format-todo-list
description: Generate properly formatted TodoWrite lists for orchestrator progress tracking. Use when creating phase checklists, updating task status, or ensuring consistent todo formatting.
---

# Format Todo List

Create properly structured todo lists for TodoWrite tool with correct status and activeForm fields.

## When to Use

- Creating initial phase checklists in orchestrators
- Updating todo list status
- Ensuring consistent todo formatting
- Generating progress tracking lists

## Instructions

### Step 1: Receive Todo Items

Accept array of todo items with status.

**Expected Input**:

```json
{
  "todos": [
    {
      "content": "Phase 1: Discovery",
      "status": "completed"
    },
    {
      "content": "Phase 2: Implementation",
      "status": "in_progress"
    },
    {
      "content": "Phase 3: Validation",
      "status": "pending"
    }
  ]
}
```

### Step 2: Generate Active Forms

Create activeForm for each todo based on content.

**Rules**:

- Convert imperative to present continuous
- "Run X" → "Running X"
- "Create X" → "Creating X"
- "Fix X" → "Fixing X"
- "Validate X" → "Validating X"

### Step 3: Validate Status

Ensure status is valid TodoWrite value.

**Valid Statuses**:

- `pending`: Not started
- `in_progress`: Currently active
- `completed`: Finished

### Step 4: Format for TodoWrite

Structure data for TodoWrite tool.

**Expected Output**:

```json
{
  "todos": [
    {
      "content": "Phase 1: Discovery",
      "status": "completed",
      "activeForm": "Discovering and analyzing"
    },
    {
      "content": "Phase 2: Implementation",
      "status": "in_progress",
      "activeForm": "Implementing changes"
    },
    {
      "content": "Phase 3: Validation",
      "status": "pending",
      "activeForm": "Validating results"
    }
  ]
}
```

## Error Handling

- **Invalid Status**: Return error listing valid statuses
- **Missing Content**: Return error for empty content
- **Empty Array**: Return error requesting at least one todo

## Examples

### Example 1: Phase Checklist

**Input**:

```json
{
  "todos": [
    { "content": "Phase 0: Pre-flight validation", "status": "completed" },
    { "content": "Phase 1: Bug detection", "status": "in_progress" },
    { "content": "Phase 2: Bug fixes", "status": "pending" },
    { "content": "Phase 3: Verification", "status": "pending" }
  ]
}
```

**Output**:

```json
{
  "todos": [
    {
      "content": "Phase 0: Pre-flight validation",
      "status": "completed",
      "activeForm": "Validating pre-flight checks"
    },
    {
      "content": "Phase 1: Bug detection",
      "status": "in_progress",
      "activeForm": "Detecting bugs"
    },
    {
      "content": "Phase 2: Bug fixes",
      "status": "pending",
      "activeForm": "Fixing bugs"
    },
    {
      "content": "Phase 3: Verification",
      "status": "pending",
      "activeForm": "Verifying fixes"
    }
  ]
}
```

### Example 2: Simple Task List

**Input**:

```json
{
  "todos": [
    { "content": "Run type check", "status": "completed" },
    { "content": "Run build", "status": "completed" },
    { "content": "Run tests", "status": "in_progress" }
  ]
}
```

**Output**:

```json
{
  "todos": [
    {
      "content": "Run type check",
      "status": "completed",
      "activeForm": "Running type check"
    },
    {
      "content": "Run build",
      "status": "completed",
      "activeForm": "Running build"
    },
    {
      "content": "Run tests",
      "status": "in_progress",
      "activeForm": "Running tests"
    }
  ]
}
```

### Example 3: Priority-Based List

**Input**:

```json
{
  "todos": [
    { "content": "Fix critical bugs", "status": "completed" },
    { "content": "Fix high-priority bugs", "status": "in_progress" },
    { "content": "Fix medium-priority bugs", "status": "pending" }
  ]
}
```

**Output**:

```json
{
  "todos": [
    {
      "content": "Fix critical bugs",
      "status": "completed",
      "activeForm": "Fixing critical bugs"
    },
    {
      "content": "Fix high-priority bugs",
      "status": "in_progress",
      "activeForm": "Fixing high-priority bugs"
    },
    {
      "content": "Fix medium-priority bugs",
      "status": "pending",
      "activeForm": "Fixing medium-priority bugs"
    }
  ]
}
```

## Validation

- [ ] Generates activeForm for all items
- [ ] Validates status values
- [ ] Handles various content formats
- [ ] Preserves original content
- [ ] Returns proper TodoWrite structure

## Supporting Files

- `template.json`: TodoWrite format template (see Supporting Files section)
