---
name: checkpoint
description: "[Tooling & Meta] Save memory checkpoint to preserve analysis context"
infer: true
---

# Save Memory Checkpoint

Save current analysis, findings, and progress to an external memory file to prevent context loss during long-running tasks.

## Summary

**Goal:** Persist current task context, findings, and progress to a checkpoint file for recovery after context compaction.

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Determine location | Filename: `plans/reports/checkpoint-{YYMMDD-HHMM}-{slug}.md` |
| 2 | Gather context | Task, findings, files analyzed/modified, progress, decisions |
| 3 | Write checkpoint file | Structured markdown with recovery instructions |
| 4 | Update todo list | Mark checkpoint creation complete |

**Key Principles:**
- Save checkpoints every 30-60 minutes during complex tasks
- Include file paths, line numbers, and exact findings -- be specific
- Always include recovery instructions for easy task resumption

## Usage

Use this command when:
- Working on complex multi-step tasks (investigation, planning, implementation)
- Before expected context compaction
- At key milestones during feature development
- After completing significant analysis phases

## Checkpoint File Location

Files are saved to: `plans/reports/checkpoint-{timestamp}-{slug}.md`

## Instructions

**Create a checkpoint file with the following structure:**

### Step 1: Determine Checkpoint Location

```bash
# Get current date for filename
date +%y%m%d-%H%M
```

### Step 2: Gather Context

Collect and document:

1. **Current Task** - What are you working on?
2. **Key Findings** - What have you discovered?
3. **Files Analyzed** - Which files have been read/modified?
4. **Progress Summary** - What's completed vs remaining?
5. **Important Context** - Critical information to preserve
6. **Next Steps** - What should be done next?
7. **Open Questions** - Unresolved issues

### Step 3: Write Checkpoint File

Create a markdown file at `plans/reports/checkpoint-YYMMDD-HHMM-{task-slug}.md` with:

```markdown
# Memory Checkpoint: [Task Description]

> Checkpoint created to preserve analysis context during [task type].

## Session Info

- **Created:** [timestamp]
- **Task:** [description]
- **Branch:** [git branch]
- **Phase:** [current phase]

## Current Task Summary

[Brief description of what you're working on]

## Key Findings

### Analysis Results
- [Finding 1]
- [Finding 2]
- [Finding N]

### Patterns Discovered
- [Pattern 1]
- [Pattern 2]

### Dependencies Identified
- [Dependency 1]
- [Dependency 2]

## Files Context

### Analyzed Files
| File            | Purpose   | Relevance       |
| --------------- | --------- | --------------- |
| path/to/file.cs | [purpose] | High/Medium/Low |

### Modified Files
- `path/to/modified.ts` - [change description]

### Pending Files
- `path/to/pending.cs` - [why pending]

## Progress Summary

### Completed
- [x] [Completed item 1]
- [x] [Completed item 2]

### In Progress
- [ ] [Current item]

### Remaining
- [ ] [Remaining item 1]
- [ ] [Remaining item 2]

## Important Context

### Critical Information
[Information that must not be lost]

### Assumptions Made
- [Assumption 1]
- [Assumption 2]

### Decisions Made
- [Decision 1] - [rationale]
- [Decision 2] - [rationale]

## Next Steps

1. [Immediate next action]
2. [Following action]
3. [Subsequent action]

## Open Questions

- [ ] [Question 1]
- [ ] [Question 2]

## Recovery Instructions

To resume this task after context reset:
1. Read this checkpoint file
2. Review [specific files] for context
3. Continue from [specific point]

---

*Checkpoint saved by Claude Code at [timestamp]*
```

### Step 4: Update Todo List

Update your todo list to reflect checkpoint was created:
```
- [x] Create memory checkpoint at [timestamp]
```

## Best Practices

1. **Save checkpoints frequently** - Every 30-60 minutes during complex tasks
2. **Be specific** - Include file paths, line numbers, exact findings
3. **Document decisions** - Record why choices were made
4. **Link related files** - Reference other analysis documents
5. **Include recovery steps** - Make resumption easy

## Related Commands

- `/context` - Load project context
- `/compact` - Manually trigger context compaction
- `/watzup` - Generate progress summary

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
