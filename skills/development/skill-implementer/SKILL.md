---
name: skill-implementer
description: Execute general implementation tasks following a plan. Invoke for non-Lean implementation work.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
context:
  - core/standards/code-patterns.md
  - core/formats/summary-format.md
  - core/standards/git-integration.md
---

# Implementer Skill

Execute implementation plans for general (non-Lean) tasks.

## Trigger Conditions

This skill activates when:
- Task language is "general", "meta", or "markdown"
- /implement command is invoked
- Plan exists and task is ready for implementation

## Implementation Strategy

### 1. Plan Loading

Load and parse the implementation plan:
- Find latest plan version
- Extract phases and their statuses
- Identify resume point (first non-completed phase)

### 2. Phase Execution

For each phase:
1. Mark phase [IN PROGRESS]
2. Execute each step
3. Verify completion
4. Mark phase [COMPLETED]
5. Commit changes

### 3. Verification

After each step/phase:
- Check files were created/modified correctly
- Run relevant tests if applicable
- Verify no regressions

## Execution Flow

```
1. Receive task context with plan path
2. Load and parse plan
3. Find resume point
4. For each remaining phase:
   a. Update phase status to IN PROGRESS
   b. Execute steps
   c. Verify results
   d. Update phase status to COMPLETED
   e. Git commit
5. Create implementation summary
6. Return results
```

## Step Execution Patterns

### Creating Files
```
1. Determine file path
2. Write content using Write tool
3. Verify file exists and content is correct
```

### Modifying Files
```
1. Read existing file
2. Apply changes using Edit tool
3. Verify changes applied correctly
```

### Running Commands
```
1. Execute command via Bash
2. Check exit code
3. Handle errors appropriately
```

## Summary Format

Create summary at `.claude/specs/{N}_{SLUG}/summaries/implementation-summary-{DATE}.md`:

```markdown
# Implementation Summary: Task #{N}

**Completed**: {date}
**Duration**: {time}

## Changes Made

{Overview of what was implemented}

## Files Modified

- `path/to/file` - {change description}

## Verification

- {What was verified}
- {Test results if any}

## Notes

{Any important notes or follow-ups}
```

## Return Format

```json
{
  "status": "completed|partial",
  "summary": "Implementation complete/partial",
  "artifacts": [
    {
      "path": ".claude/specs/{N}_{SLUG}/summaries/...",
      "type": "summary",
      "description": "Implementation summary"
    }
  ],
  "phases_completed": 3,
  "phases_total": 3,
  "files_modified": [
    "path/to/file1",
    "path/to/file2"
  ]
}
```

## Error Handling

### On Step Failure
- Log error details
- Keep phase as [IN PROGRESS]
- Return partial status
- Include error in response

### On Timeout
- Commit partial progress
- Mark phase [PARTIAL]
- Return with resume information
