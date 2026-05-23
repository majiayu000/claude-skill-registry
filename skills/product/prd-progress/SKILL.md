---
name: prd-progress
description: Show implementation progress from linked tasks
argument-hint: <prd-file>
---

# prd-progress

**Category**: Product & Strategy

## Usage

```bash
prd-progress <prd-file> [--detailed] [--format <format>]
```

## Arguments

- `<prd-file>`: Required - Path to the PRD file
- `--detailed`: Optional - Show individual task status
- `--format`: Optional - Output format (simple, detailed, json). Default: simple

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. Read the PRD file and extract the task_file reference from metadata
2. If no task file is linked, check standard locations:
   - `./tasks/<prd-name>-tasks.md`
   - `../tasks/<prd-name>-tasks.md`
   - `product-docs/tasks/<prd-name>-tasks.md`
3. Read the linked task file and parse task structure
4. Count total tasks and completed tasks (marked with [x])
5. Calculate completion percentage and other metrics:
   - Tasks by priority (if specified)
   - Parent vs subtask completion
   - Estimated completion date (based on velocity)
6. Display progress information in requested format

## Task Parsing Rules

Recognize these task formats:
```markdown
- [ ] Task not started
- [x] Task completed
- [-] Task in progress (count as 0.5 for progress)
- [~] Task cancelled (exclude from totals)

Parent/Child structure:
- [ ] 1.0 Parent task
  - [x] 1.1 Subtask completed
  - [ ] 1.2 Subtask pending
```

## Output Formats

### Simple Format (default)
```
📊 PRD Progress: user-authentication-frd.md

Progress: ████████████░░░░░░░░ 60% (12/20 tasks)

✅ Completed: 12 tasks
🔄 In Progress: 2 tasks
⏳ Remaining: 6 tasks
❌ Blocked: 0 tasks

Estimated completion: 2025-01-10 (4 days)
```

### Detailed Format
```
📊 PRD Progress: user-authentication-frd.md

Overall: 60% complete (12/20 tasks)

By Section:
1. Database Setup      ██████████ 100% (3/3)
2. API Implementation  ████████░░ 80% (4/5)
3. Frontend UI         ████░░░░░░ 40% (2/5)
4. Testing            ██░░░░░░░░ 20% (1/5)
5. Documentation      ████░░░░░░ 40% (2/5)

Recent Progress:
- ✅ 2025-01-05: Completed "Create user model"
- ✅ 2025-01-05: Completed "Setup auth endpoints"
- 🔄 2025-01-06: Started "Build login form"

By Priority:
- High:   75% (6/8)
- Medium: 50% (4/8)
- Low:    50% (2/4)

Velocity: 3 tasks/day (last 7 days)
Est. Completion: 2025-01-10
```

### JSON Format
```json
{
  "prd_file": "user-authentication-frd.md",
  "task_file": "./tasks/user-authentication-frd-tasks.md",
  "progress": {
    "percentage": 60,
    "completed": 12,
    "total": 20,
    "in_progress": 2,
    "remaining": 6
  },
  "sections": [
    {
      "name": "Database Setup",
      "completed": 3,
      "total": 3,
      "percentage": 100
    }
  ],
  "estimated_completion": "2025-01-10",
  "velocity": 3.0,
  "last_updated": "2025-01-06"
}
```

## Progress Calculation

1. **Simple Progress**: (completed tasks / total tasks) * 100
2. **Weighted Progress**: Consider task hierarchy - parent tasks count more
3. **Velocity**: Average tasks completed per day over last 7 days
4. **Estimation**: remaining_tasks / velocity = days to complete

## Error Handling

- If PRD file not found: Exit with error
- If no task file linked: Search standard locations, report if not found
- If task file not found: Show 0% progress with warning
- If invalid task format: Skip line and note in detailed output

## Example

```bash
# Show simple progress
prd-progress user-authentication-frd.md

# Show detailed breakdown
prd-progress user-authentication-frd.md --detailed

# Get JSON output for automation
prd-progress inventory-prd.md --format json

# Check progress for PRD in another directory
prd-progress ../prds/active/feature-auth-frd.md
```

## Implementation Tips for Claude Code

1. **Task Counting**: Handle nested tasks correctly, don't double-count
2. **Progress Bar**: Use Unicode blocks for visual progress bars
3. **Velocity Calculation**: Only count last 7 days of activity
4. **Smart Search**: If task file not found, search relative to PRD location
5. **Date Parsing**: Extract completion dates from git history if available
6. **Section Detection**: Group tasks by top-level headings for section progress
