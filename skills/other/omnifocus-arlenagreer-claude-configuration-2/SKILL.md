---
name: omnifocus
description: Manage OmniFocus projects and tasks programmatically. This skill should be used when creating, reading, updating, or listing OmniFocus tasks and projects. Supports all OmniFocus versions through intelligent automation method detection (Omni Automation → AppleScript → SQLite read-only fallback). Use for task management workflows, project queries, task completion tracking, and OmniFocus data operations.
---

# OmniFocus Task & Project Manager

## Overview

Manage OmniFocus tasks and projects programmatically with intelligent automation that works across all OmniFocus versions. The skill automatically detects and uses the best available method:

1. **Omni Automation** (OmniFocus 3+) - Modern JavaScript API
2. **AppleScript** (All versions) - Compatible fallback
3. **SQLite Read-Only** (Last resort) - For analytics when automation unavailable

## When to Use This Skill

Use this skill when users request to:

- **Create tasks**: "Add task 'Review PR' to project 'Development'"
- **Read tasks**: "Show me tasks in the 'Work' project"
- **Update tasks**: "Mark task 'Call client' as complete"
- **List projects**: "What projects do I have in OmniFocus?"
- **Query tasks**: "Show me all tasks tagged with '@urgent'"
- **Manage workflows**: "Create project tasks for new feature development"

## Core Capabilities

### 1. Create Tasks

Add new tasks to OmniFocus with full metadata support.

**Usage:**
```ruby
scripts/omnifocus_manager.rb --create \
  --name "Review pull request #42" \
  --project "Development" \
  --notes "Check for security issues and code quality"
```

**Claude Integration:**
```bash
# When user says: "Add task to OmniFocus to review the API documentation"
ruby ~/.claude/skills/omnifocus/scripts/omnifocus_manager.rb \
  --create \
  --name "Review API documentation" \
  --project "Documentation"
```

**Supported Parameters:**
- `--name` (required): Task title
- `--project` (optional): Project name (creates if doesn't exist)
- `--notes` (optional): Task notes/description
- `--tag` (optional): Tag to assign (repeatable for multiple tags)
- `--due` (optional): Due date (ISO 8601 format)

### 2. Read Tasks

Query tasks with powerful filtering options.

**Usage:**
```ruby
# All incomplete tasks
scripts/omnifocus_manager.rb --read

# Tasks in specific project
scripts/omnifocus_manager.rb --read --project "Development"

# Tasks with specific tag
scripts/omnifocus_manager.rb --read --tag "@urgent"

# Include completed tasks
scripts/omnifocus_manager.rb --read --completed

# Limit results
scripts/omnifocus_manager.rb --read --limit 50
```

**Claude Integration:**
```bash
# When user says: "What tasks do I have in my Work project?"
ruby ~/.claude/skills/omnifocus/scripts/omnifocus_manager.rb \
  --read \
  --project "Work"
```

**Output Format (JSON):**
```json
[
  {
    "id": "abc123xyz",
    "name": "Review pull request #42",
    "completed": false,
    "note": "Check for security issues",
    "project": "Development",
    "dueDate": "2025-11-25T17:00:00Z",
    "tags": ["@code-review", "@high-priority"]
  }
]
```

### 3. Update Tasks

Modify existing tasks programmatically.

**Usage:**
```ruby
# Mark task complete
scripts/omnifocus_manager.rb --update TASK_ID --completed

# Update task name
scripts/omnifocus_manager.rb --update TASK_ID --name "New task title"

# Update notes
scripts/omnifocus_manager.rb --update TASK_ID --notes "Updated description"
```

**Claude Integration:**
```bash
# When user says: "Mark the task 'Call client' as done"
# First, find the task ID
TASK_ID=$(ruby ~/.claude/skills/omnifocus/scripts/omnifocus_manager.rb \
  --read | jq -r '.[] | select(.name == "Call client") | .id')

# Then mark it complete
ruby ~/.claude/skills/omnifocus/scripts/omnifocus_manager.rb \
  --update "$TASK_ID" \
  --completed
```

### 4. List Projects

View all OmniFocus projects.

**Usage:**
```ruby
scripts/omnifocus_manager.rb --list-projects
```

**Output Format (JSON):**
```json
[
  {
    "id": "proj123",
    "name": "Development",
    "status": "active",
    "note": "Software development tasks",
    "taskCount": 15
  },
  {
    "id": "proj456",
    "name": "Marketing",
    "status": "active",
    "note": "",
    "taskCount": 8
  }
]
```

## Automation Method Detection

The skill automatically detects and uses the best available automation method:

### Priority Order

1. **Omni Automation (Preferred)**
   - Modern JavaScript API
   - OmniFocus 3+ required
   - Cross-platform (Mac, iOS, iPad)
   - Full read/write capabilities
   - Fastest performance

2. **AppleScript (Compatible)**
   - Works with all OmniFocus versions
   - macOS only
   - Full read/write capabilities
   - Requires OmniFocus Pro for automation

3. **SQLite Read-Only (Fallback)**
   - Last resort when automation unavailable
   - Read operations only
   - No permissions required
   - Useful for analytics and reporting

**Detection is automatic** - no configuration needed. The manager checks availability in order and uses the first working method.

## Permission Requirements

### Omni Automation
- **Minimal**: Enable Automation in OmniFocus Preferences → Automation
- No system-level permissions required

### AppleScript
- **System Permission**: System Preferences → Security & Privacy → Privacy → Automation
- User prompted on first use
- Must grant permission for controlling application to control OmniFocus

### SQLite Read-Only
- **File System Access**: Read access to `~/Library/Caches/`
- No automation permissions needed
- Read-only operations only

### Setup Guidance

When encountering permission errors, guide users to:

1. Open **System Preferences** (or **System Settings** on macOS 13+)
2. Navigate to **Security & Privacy** → **Privacy** → **Automation**
3. Find the controlling application (e.g., Terminal, Ruby, Claude Code)
4. Enable checkbox for **OmniFocus**
5. Restart the application if needed

## Common Workflows

### Workflow 1: Create Project with Tasks

```bash
# Create project by adding first task
ruby scripts/omnifocus_manager.rb --create \
  --name "Set up database schema" \
  --project "New Feature Development"

# Add more tasks to the project
ruby scripts/omnifocus_manager.rb --create \
  --name "Implement API endpoints" \
  --project "New Feature Development"

ruby scripts/omnifocus_manager.rb --create \
  --name "Write unit tests" \
  --project "New Feature Development"
```

### Workflow 2: Daily Task Review

```bash
# Get all incomplete tasks
ruby scripts/omnifocus_manager.rb --read > /tmp/tasks.json

# Process with jq for specific queries
cat /tmp/tasks.json | jq '.[] | select(.dueDate != null) | {name, dueDate}'
```

### Workflow 3: Bulk Task Completion

```bash
# Find all tasks matching criteria
ruby scripts/omnifocus_manager.rb --read --project "Sprint 23" > /tmp/sprint_tasks.json

# Mark each as complete
cat /tmp/sprint_tasks.json | jq -r '.[].id' | while read task_id; do
  ruby scripts/omnifocus_manager.rb --update "$task_id" --completed
done
```

### Workflow 4: Task Analytics

```bash
# Count tasks by project (using read-only SQLite)
ruby scripts/omnifocus_manager.rb --read | \
  jq 'group_by(.project) | map({project: .[0].project, count: length})'
```

## Claude Usage Patterns

### Pattern 1: Natural Language Task Creation

**User Request**: "Add a task to call the client about Q4 planning to my Work project"

**Claude Response**:
```bash
ruby ~/.claude/skills/omnifocus/scripts/omnifocus_manager.rb \
  --create \
  --name "Call client about Q4 planning" \
  --project "Work"
```

### Pattern 2: Task Query with Formatting

**User Request**: "Show me my urgent tasks"

**Claude Response**:
```bash
# Query urgent tasks
ruby ~/.claude/skills/omnifocus/scripts/omnifocus_manager.rb \
  --read \
  --tag "@urgent" | \
  jq -r '.[] | "- \(.name) [\(.project // "Inbox")]"'
```

### Pattern 3: Task Status Updates

**User Request**: "I finished the code review task"

**Claude Response**:
```bash
# Find task ID
TASK_ID=$(ruby ~/.claude/skills/omnifocus/scripts/omnifocus_manager.rb \
  --read | \
  jq -r '.[] | select(.name | contains("code review")) | .id' | head -1)

# Mark complete
if [ -n "$TASK_ID" ]; then
  ruby ~/.claude/skills/omnifocus/scripts/omnifocus_manager.rb \
    --update "$TASK_ID" \
    --completed
  echo "✅ Task marked as complete"
else
  echo "❌ Task not found"
fi
```

### Pattern 4: Project Overview

**User Request**: "What's in my Development project?"

**Claude Response**:
```bash
ruby ~/.claude/skills/omnifocus/scripts/omnifocus_manager.rb \
  --read \
  --project "Development" | \
  jq -r '
    "Development Project Tasks:\n" +
    "Total: \(length)\n" +
    "Incomplete: \([.[] | select(.completed == false)] | length)\n\n" +
    "Tasks:\n" +
    (.[] | "- [\(if .completed then "x" else " " end)] \(.name)")
  '
```

## Troubleshooting

### Issue: "Omni Automation Error: Application isn't running"

**Solution**: Start OmniFocus application
```bash
open -a OmniFocus
sleep 2  # Wait for app to launch
# Retry operation
```

### Issue: "AppleScript Error: Not authorized"

**Solution**: Grant automation permissions
1. System Preferences → Security & Privacy → Privacy → Automation
2. Enable checkbox for controlling app → OmniFocus
3. Restart controlling application

### Issue: "Task not found" when updating

**Solution**: Verify task ID exists
```bash
# List all task IDs
ruby scripts/omnifocus_manager.rb --read | jq -r '.[].id'

# Or search for task by name
ruby scripts/omnifocus_manager.rb --read | jq '.[] | select(.name | contains("search term"))'
```

### Issue: "OmniFocus database not found"

**Solution**: Verify OmniFocus is installed and has been run at least once
```bash
ls -la ~/Library/Caches/com.omnigroup.OmniFocus*
```

### Issue: "Write operations not available"

**Explanation**: Only read-only SQLite access is available
**Solution**: Enable Omni Automation or grant AppleScript permissions for write operations

## Advanced Usage

### Programmatic Integration

Use the Ruby API directly for custom integrations:

```ruby
require_relative 'scripts/omnifocus_manager'

manager = OmniFocusManager.new
puts "Using automation: #{manager.automation_type}"

# Create task
result = manager.create_task(
  name: "Process expense report",
  project: "Finance",
  notes: "Q4 2025 expenses",
  tags: ["@admin", "@urgent"]
)

# Read tasks
tasks = manager.read_tasks(project: "Finance", completed: false)
tasks.each do |task|
  puts "#{task['name']} - #{task['completed'] ? '✓' : '○'}"
end
```

### JSON Output Processing

All commands output JSON for easy processing with `jq`:

```bash
# Tasks due this week
ruby scripts/omnifocus_manager.rb --read | \
  jq '.[] | select(.dueDate != null and (.dueDate | fromdateiso8601) < (now + 604800))'

# Group by project
ruby scripts/omnifocus_manager.rb --read | \
  jq 'group_by(.project) | map({project: .[0].project, tasks: map(.name)})'

# Export to CSV
ruby scripts/omnifocus_manager.rb --read | \
  jq -r '["Name","Project","Completed","Due Date"], (.[] | [.name, .project, .completed, .dueDate]) | @csv'
```

## Performance Considerations

- **Omni Automation**: Fastest, direct API access (~100-200ms per operation)
- **AppleScript**: Moderate speed (~200-500ms per operation)
- **SQLite**: Very fast for reads (~10-50ms), but read-only

For bulk operations (>100 tasks), consider:
1. Using SQLite read-only for queries
2. Batching write operations
3. Caching project IDs to avoid repeated lookups

## Resources

See `references/api_reference.md` for detailed API documentation including:
- Complete Omni Automation JavaScript API reference
- AppleScript object model and properties
- SQLite database schema details
- Advanced query examples

## Version Compatibility

- **OmniFocus 3+**: Full Omni Automation support
- **OmniFocus 2**: AppleScript only
- **OmniFocus 1**: AppleScript only
- **All versions**: SQLite read-only fallback

## Security & Privacy

- **No data transmission**: All operations are local
- **Read-only by default**: SQLite fallback is read-only to prevent corruption
- **Permission-gated**: Requires explicit user authorization for automation
- **Temporary database copies**: SQLite operations use copies, never modify live database
