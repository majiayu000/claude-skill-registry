---
name: things3-productivity
description: Provides Things3 task management workflows, organization patterns, and
  productivity methodologies. Includes personal taxonomy integration, priority systems,
  and automation patterns for effective task
---

---
name: things3-productivity
description: Provides Things3 task management workflows, organization patterns, and productivity methodologies. Includes personal taxonomy integration, priority systems, and automation patterns for effective task management. MANDATORY: Claude must read this skill file before using any Things3 MCP tools (read_tasks, create_task, edit_task, migrate_inbox_to_notion).
---

# Things3 Productivity & Task Management

## Overview

This skill provides comprehensive guidance for Things3 task management, including organizational patterns, workflow automation, and integration with personal productivity systems.

**CRITICAL REQUIREMENT**: Before using ANY Things3 MCP tools (read_tasks, create_task, edit_task, migrate_inbox_to_notion), Claude MUST read this entire skill file to understand the proper query strategies, tag inheritance rules, and organizational patterns. Failure to do this results in broken workflows and incorrect task organization.

**Keywords**: things3, task management, productivity, GTD, priority, areas, projects, scheduling, automation, applescript

## Pre-Flight Checklist for Things3 Operations

**MANDATORY**: Before ANY Things3 task/project operations, verify ALL items:

- [ ] **Skill loaded**: Confirm things3-productivity skill is active in this conversation
- [ ] **Change validation**: Present diff summary using validation protocol for bulk operations
- [ ] **Tool limitations checked**: Review "Tool Limitations & Workarounds" section for constraints
- [ ] **Verification plan**: Define how to verify operations succeeded (e.g., `get_project_tasks`, `read_tasks`)
- [ ] **Scheduling complete**: For projects, schedule with `edit_task` after `create_project` (workaround for missing `when`/`deadline`)

**For project breakdowns specifically**:
- [ ] Present breakdown plan to user before creating projects
- [ ] Create projects with proper area/tags
- [ ] Use `edit_task` to set project `when` and `deadline`
- [ ] Create all subtasks with `project` parameter
- [ ] Verify tasks landed in projects using `get_project_tasks`
- [ ] If verification fails, use `edit_task` to move tasks to correct projects

## Personal Organization System

### Task Taxonomy
Personal organization patterns are automatically loaded from `private-prefs/personal-taxonomy.json`:
- **Work tags**: Personal work identification tags (e.g., "WORK")
- **Work areas**: Professional focus areas (e.g., "Work")
- **Priority system**: 7+ for high priority tasks (1-9 scale)
- **Priority distribution**: Balanced allocation - 1 item in priority 1, 2 items in priority 2, 3 items in priority 3, etc. Only use "+" priority for non-organic urgent items
- **Common patterns**: Frequently used organizational structures

### Scheduling Philosophy
- **Today view**: Active tasks for current day focus
- **Someday/Maybe**: Future considerations and ideas
- **Anytime**: Available tasks without specific timing
- **Inbox**: Capture point for quick entry and processing

## Core Workflows

### Change Validation Protocol
Before making any reorganization changes (task lists, views, scheduling), present a natural language diff summary:

**Standard validation format**:
```
**Before**: [what currently exists/state]
**Completed/Removed**: [items being completed or removed]
**Moving/Keeping**: [items staying but changing location/category]
**New/Added**: [new items being added] → [where they're going]
**After**: [final organized state]
```

**When to use**: View cleanup, bulk rescheduling, area/project reorganization, tag restructuring

### Things3-Specific Workflows

#### View Cleanup/Reorganization
- Reorganize by areas, projects, and priority levels
- Apply personal taxonomy consistently
- Use change validation protocol before executing

#### Bulk Task Operations
- Reschedule multiple tasks between lists (Today/Someday/Anytime)
- Apply tags consistently across task groups
- Use change validation protocol before executing

### Daily Planning
1. **Morning review**: Check Today view for scheduled tasks
2. **Inbox processing**: Clear inbox items regularly
3. **Priority assessment**: Use 7+ priority for high-importance items, maintain distribution (1 item in priority 1, 2 in priority 2, etc.)
4. **Work focus**: Filter by personal work tags for professional tasks

### Task Creation Patterns
- **Quick capture**: Minimal title for speed, elaborate later
- **Contextual tagging**: Apply work tags and priority numbers
- **Proper scheduling**: Use list-based scheduling (Today/Someday/Anytime)
- **Project organization**: Group related tasks under projects

### Weekly/Monthly Reviews
- Review Someday items for potential activation
- Archive completed projects
- Update area focus based on changing priorities
- Maintain clean project and area structure

## MCP Tools Integration

### Available Tools
- **`read_tasks`**: View tasks with flexible filtering and project discovery (AppleScript-based)
- **`search_tasks`**: Search tasks by string query across titles and notes (SQLite-based via things.py)
- **`create_task`**: Add new tasks via AppleScript automation
- **`edit_task`**: Modify existing tasks including scheduling and properties
- **`create_project`**: Create new projects (NOTE: does NOT support `when` or `deadline` - use `edit_task` after creation)
- **`migrate_inbox_to_notion`**: Transfer inbox items to Notion for documentation

### Tool Limitations & Workarounds

#### `create_project` Limitations
**Missing parameters**: `when` (scheduling), `deadline` (due date)

**Workaround**: After creating project, use `edit_task` with project UUID to set:
- Scheduling: `edit_task(task_uuid=project_id, when="today")`
- Deadline: `edit_task(task_uuid=project_id, deadline="YYYY-MM-DD")`

**Example workflow**:
```python
# 1. Create project
result = create_project(name="Project Name", area="Area", tags=["tag"])
project_id = result["project"]["id"]

# 2. Set scheduling and deadline
edit_task(task_uuid=project_id, when="today")
# Note: deadline parameter may not be supported in edit_task - verify tool schema
```

#### `create_task` with `project` Parameter
**Potential issue**: Tasks may not properly nest under projects when using `project` parameter.

**Verification step**: After bulk task creation, always verify tasks are in correct projects:
```python
get_project_tasks(project_id="project_uuid")
```

**If tasks missing**: Use `edit_task` to move them:
```python
edit_task(task_uuid="task_id", project="Project Name")
```

### Tool Usage Patterns

#### Cardinality Reduction Strategy
**Core principle**: **ALWAYS default to `when="today"`** to reduce from thousands to manageable set

**CRITICAL**: NEVER use `when="anytime"` or omit the `when` parameter without explicit user request - these queries are extremely expensive. Always default to `when="today"` unless user specifically asks for other views (inbox, anytime, someday, upcoming).

#### Work View Query Strategy (Multi-part approach)
For complete work task coverage, use 3-part queries:

```
# Part 1: Direct work tags
read_tasks(when="today", tags=["WORK"])

# Part 2: Area inheritance (tasks in work areas inherit tags)
read_tasks(when="today", area="Work")

# Part 3: Project inheritance (discover work projects through exploration)
read_tasks(when="today", project="on-call")  # example work project
```

#### Other Common Patterns
```
# High priority work focus
read_tasks(when="today", tags=["WORK"], min_priority=7)
read_tasks(when="today", area="Work", min_priority=7)

# Inbox processing
read_tasks(when="inbox", limit=10)

# Context-specific work (combine filters as needed)
read_tasks(when="today", area="Work")
read_tasks(when="anytime", tags=["WORK"], project="on-call")
```

#### Tag Inheritance Rules
- **Direct tags**: Tasks explicitly tagged with WORK
- **Area inheritance**: Tasks in Work area automatically inherit WORK context
- **Project inheritance**: Tasks in projects tagged with WORK inherit work context
- **Tool limitation**: `read_tasks` with `tags=["WORK"]` only finds directly tagged tasks, NOT tasks inheriting through projects/areas. Use multi-part queries (Parts 1, 2, 3 above) or `search_tasks` to find all work tasks.

#### String Search for Task Discovery
**Use `search_tasks` when looking for specific tasks by partial title or content:**

```python
# Find task by partial title (e.g., finding "AMP-138806" task)
search_tasks(query="138806", when="today")

# Search across all tasks (no list filter)
search_tasks(query="meeting prep")

# Combine with filters
search_tasks(query="bug", area="Work", tags=["urgent"])
```

**Advantages over `read_tasks`**:
- Searches both titles AND notes
- Uses SQLite directly (faster, more comprehensive)
- No need to know exact title or list location

**When to use `search_tasks` vs `read_tasks`**:
- **`search_tasks`**: Finding tasks by partial title/content, don't know exact location
- **`read_tasks`**: Viewing all tasks in a specific list/area/project with filters

#### Project Discovery (New Capability)

Use `read_tasks(area="AreaName", list_projects=True)` to discover existing projects within areas:

```python
# Discover projects within any area before task organization
read_tasks(area="WorkArea", list_projects=True)

# Returns list of projects with names and IDs
# Example output: project names, administrative projects, feature-specific projects, etc.
```

**Critical for task organization**: Always discover existing project structure before moving tasks to avoid creating duplicates. This solves the problem of not knowing what projects exist within areas.

**Work area example**: When organizing work tasks, use `read_tasks(area="Work", list_projects=True)` to find existing work projects.

## AppleScript Automation

### List-Based Scheduling
Tasks move between scheduling lists:
- **Today**: Scheduled for current day
- **Someday**: Future scheduling (Someday/Maybe)
- **Anytime**: Available without specific timing
- **Upcoming**: Future dated scheduling

### Tag Management
- Auto-create tags if they don't exist
- Apply multiple tags for context and priority
- Use personal taxonomy for consistent tagging
- Combine work identification with priority numbers

### Task Properties
- **Title**: Clear, actionable descriptions
- **Notes**: Detailed context and requirements
- **Area/Project**: Organizational hierarchy
- **Tags**: Context and priority markers

## Integration Workflows

### Things3 ↔ Notion
- Use Things3 for task execution and scheduling
- Use Notion for detailed documentation and planning
- Migrate notes and context from Things3 inbox to Notion
- Maintain cross-references between systems

### Personal Context Awareness
This skill automatically considers:
- Personal work areas and professional context
- Priority level definitions and usage patterns
- Common tag combinations and organizational preferences
- Integration points with other productivity systems

## Productivity Methodologies

### Getting Things Done (GTD) Principles
- Inbox as universal capture point
- Context-based task organization
- Regular review cycles for maintenance
- Clear next action definitions

### Personal Adaptations
- Work/personal separation through area management
- Priority-based focus using numerical tags
- List-based scheduling for time management
- Project-based organization for complex work

Always reference personal taxonomy and organizational preferences when suggesting Things3 workflows or automation.