---
name: managing-context-window
description: Helps manage context window efficiently by summarizing, focusing, and pruning context to stay within token limits.
---

# Managing Context Window Skill

## When to Use

- Context is approaching token limits
- User asks to summarize conversation history
- Need to focus on specific task
- Working with large files or codebases

## What This Skill Does

1. Analyzes current context usage
2. Identifies non-essential information
3. Creates summaries of conversation history
4. Focuses context on current task
5. Prunes redundant or outdated information

## Strategies

### 1. Summarize Previous Work

```
Summary of work so far:
- Implemented activity recording service
- Added GPS tracking functionality
- Created activity list screen
- Working on: activity detail view

Current task: Add activity statistics calculation
```

### 2. Focus on Current Task

Keep only:

- Current implementation goal
- Relevant code files
- Recent error messages
- Specific questions to answer

### 3. Prune Redundant Information

- Remove completed sub-tasks
- Remove duplicate information
- Remove outdated context
- Remove exploratory messages

### 4. Use File References

Instead of pasting full file contents:

- Reference file paths
- Use Grep to find specific sections
- Read specific line ranges

## Implementation

```typescript
// Use TodoWrite to track progress instead of comments
const todos = [
  { id: "1", content: "Implement activity recording", status: "completed" },
  { id: "2", content: "Add GPS tracking", status: "completed" },
  { id: "3", content: "Create activity detail view", status: "in_progress" },
];

// When switching tasks, update context
function switchTask(newTask: string) {
  return {
    task: newTask,
    relevantFiles: getRelevantFiles(newTask),
    summary: summarizeCompletedWork(),
  };
}
```

## Best Practices

1. Use TodoWrite for tracking
2. Reference files instead of pasting
3. Summarize completed work
4. Focus on current task
5. Remove outdated context
6. Keep error messages relevant
7. Use specific line ranges when reading
