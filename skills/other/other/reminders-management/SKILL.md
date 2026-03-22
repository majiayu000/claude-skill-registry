---
name: reminders-management
description: Use when managing Apple Reminders via MCP - covers list organization, reminder creation/updates, search patterns, and integration with other productivity workflows
---

# Apple Reminders Management via MCP

## When to Use This Skill

Invoke this skill when you need to:
- Create reminders for time-sensitive tasks or follow-ups
- Search existing reminders to check task status
- Update reminder priorities or due dates
- Organize reminders across different lists (Work, Personal, Projects)
- Mark reminders complete after task completion
- Integrate reminders with Obsidian @paia tags or task syncing workflows
- Set up recurring or time-based task tracking

## Core Principles

1. **List Organization**: Use appropriate reminder lists for different contexts (Work vs Personal)
2. **Priority Management**: Set priorities (high=1, medium=5, low=9) for task importance
3. **Due Date Discipline**: Set due dates for time-sensitive tasks, leave open for aspirational tasks
4. **Search First**: Check existing reminders before creating duplicates
5. **Completion Tracking**: Mark reminders complete to maintain clean lists
6. **Integration**: Link reminders to Obsidian notes for full context

## Available MCP Tools

### Core Operations

- **list_reminder_lists**: Get all available reminder lists (start here)
- **get_reminders**: Get reminders from specific list or all lists (with optional filtering)
- **search_reminders**: Search reminders by name or body content
- **create_reminder**: Create new reminder with priority, due date, and notes
- **update_reminder**: Update existing reminder (priority, due date, completion status)
- **delete_reminder**: Delete reminder by ID

## Reminder List Organization

### Typical List Structure

```
Work Lists:
- "Work" - General work tasks
- "LightForge Works" - Business Project business tasks
- "Partner Project" - Partnership development tasks
- "Projects" - Active project tasks

Personal Lists:
- "Reminders" - Default personal list
- "Shopping" - Shopping and errands
- "Reading" - Articles and books to read
- "Someday" - Aspirational tasks
```

### Pattern: Discover Available Lists

```
Use: mcp__reminders__list_reminder_lists

Result: Array of {id, name} for all available lists
```

**When to use**: Starting point before creating reminders, understanding organization

## Creating Reminders

### Pattern: Simple Task Reminder

```
Use: mcp__reminders__create_reminder

Parameters:
- name: "Follow up with Partner Contact on Partner Project partnership"
- listName: "Partner Project"
- priority: 1 (high priority)
- dueDate: "10/20/2025 09:00 AM"
```

### Pattern: Task with Context

```
Use: mcp__reminders__create_reminder

Parameters:
- name: "Update email campaign messaging for Business Project"
- listName: "LightForge Works"
- body: "Update remaining 6 emails in drip sequence. Reference: Obsidian note in Areas/Business/Business Project/Email Marketing Campaign.md"
- priority: 1
- dueDate: "10/22/2025 02:00 PM"
```

### Pattern: Recurring Task Placeholder

```
Note: MCP doesn't currently support recurring reminders via API
Workaround: Create individual instances with sequential due dates

Example - Weekly Review:
create_reminder(name: "Weekly Review", listName: "Work", dueDate: "10/20/2025 05:00 PM")
create_reminder(name: "Weekly Review", listName: "Work", dueDate: "10/27/2025 05:00 PM")
create_reminder(name: "Weekly Review", listName: "Work", dueDate: "11/03/2025 05:00 PM")
```

## Searching and Filtering Reminders

### Pattern: Search by Name or Content

```
Use: mcp__reminders__search_reminders

Parameters:
- searchTerm: "Partner Project"

Result: All reminders mentioning "Partner Project" in name or body
```

### Pattern: Get Reminders from Specific List

```
Use: mcp__reminders__get_reminders

Parameters:
- listName: "LightForge Works"
- completed: false (only show incomplete)

Result: All incomplete reminders in Business Project list
```

### Pattern: Find All Incomplete High Priority Tasks

```
Use: mcp__reminders__get_reminders

Parameters:
- completed: false

Then filter results where priority === 1 (high)
```

## Updating Reminders

### Pattern: Change Priority

```
# Step 1: Search for reminder
results = mcp__reminders__search_reminders(searchTerm: "market research")

# Step 2: Update priority
mcp__reminders__update_reminder(
  reminderId: results[0].id,
  priority: 1  # Escalate to high priority
)
```

### Pattern: Reschedule Due Date

```
# Step 1: Find reminder
results = mcp__reminders__get_reminders(listName: "Partner Project", completed: false)

# Step 2: Update due date
mcp__reminders__update_reminder(
  reminderId: results[0].id,
  dueDate: "10/25/2025 10:00 AM"  # Push out deadline
)
```

### Pattern: Mark Complete

```
# Step 1: Search for completed task
results = mcp__reminders__search_reminders(searchTerm: "email campaign setup")

# Step 2: Mark complete
mcp__reminders__update_reminder(
  reminderId: results[0].id,
  completed: true
)
```

### Pattern: Add Context to Existing Reminder

```
# Step 1: Find reminder
results = mcp__reminders__search_reminders(searchTerm: "partnership proposal")

# Step 2: Add body text with context
mcp__reminders__update_reminder(
  reminderId: results[0].id,
  body: "Draft partnership terms. Reference market research in Obsidian: Areas/Companies/Partner Project/market_research/"
)
```

## Integration Workflows

### Integration: Obsidian → Reminders

**Goal**: Create reminders from Obsidian @paia tags or action items

```markdown
Workflow:
1. Process @paia tag in Obsidian: mcp__obsidian__search_notes(searchTerm: "@paia")
2. Parse action items from note content
3. For each time-sensitive action:
   mcp__reminders__create_reminder(
     name: "[action from Obsidian]",
     listName: "[appropriate list]",
     body: "Source: [Obsidian note path]",
     priority: [based on @paia context],
     dueDate: [if specified in note]
   )
4. Update Obsidian note: append_to_note("Reminder created: [reminder_id]")
```

### Integration: Reminders → Obsidian

**Goal**: Sync reminder completion back to Obsidian task tracking

```markdown
Workflow:
1. Get completed reminders: mcp__reminders__get_reminders(completed: true)
2. Filter for reminders with "Source: [Obsidian path]" in body
3. For each completed reminder:
   - Extract Obsidian note path from body
   - Update note: mcp__obsidian__update_note_section
   - Mark task as complete with completion date
4. Archive or delete synced reminders: mcp__reminders__delete_reminder
```

### Integration: Task Sync Workflow (syncing-task-completions skill)

```markdown
Workflow: Two-agent sync pattern

@sync-scanner agent:
1. Get all incomplete reminders: mcp__reminders__get_reminders(completed: false)
2. Get all Obsidian action items: mcp__obsidian__search_notes(searchTerm: "TODO")
3. Cross-reference to find:
   - Reminders without Obsidian entries (orphaned)
   - Obsidian TODOs without reminders (untracked)
4. Generate sync report

@sync-updater agent:
1. For orphaned reminders: create Obsidian action items
2. For untracked TODOs: create reminders
3. Update master task list in Obsidian with completion dates
4. Mark synced reminders complete
```

### Integration: Time-Based Task Delegation

**Goal**: Create reminders for delegated sub-agent tasks

```markdown
Workflow:
1. Coordinator Claude delegates task to sub-agent
2. Create reminder for follow-up:
   mcp__reminders__create_reminder(
     name: "Check @implementer progress on [task]",
     listName: "Work",
     body: "Delegated to @implementer at [time]. Expected completion: [estimate]",
     priority: 5,
     dueDate: "[estimated completion + 1 hour]"
   )
3. When reminder triggers: check sub-agent output
4. Mark reminder complete when sub-agent finishes
```

## Priority Management Guidelines

### Priority Levels

- **High (1)**: Time-sensitive, blocking other work, high-impact
  - Example: "Follow up with client before deadline"
  - Example: "Fix production bug affecting users"

- **Medium (5)**: Important but not urgent, scheduled work
  - Example: "Update email campaign messaging"
  - Example: "Review market research findings"

- **Low (9)**: Nice-to-have, aspirational, low-priority
  - Example: "Read article about new AI framework"
  - Example: "Organize project files"

- **None (0)**: No specific priority, informational
  - Example: "Remember to check MJ's draft later"

### Pattern: Triage Existing Reminders

```markdown
Workflow:
1. Get all incomplete reminders: mcp__reminders__get_reminders(completed: false)
2. For each reminder:
   - Evaluate urgency and impact
   - Update priority: mcp__reminders__update_reminder(reminderId, priority)
   - Add or update due dates for time-sensitive items
3. Focus on high-priority items first
```

## Due Date Best Practices

### When to Set Due Dates

**Set specific due dates for**:
- Client follow-ups with deadlines
- Event-based tasks (meetings, presentations)
- Time-sensitive dependencies (blocking other work)
- Recurring reviews (weekly, monthly)

**Leave due dates unset for**:
- Aspirational learning tasks
- Exploratory research
- "Someday/Maybe" items
- Tasks with flexible timelines

### Due Date Format

```
Format: "MM/DD/YYYY HH:MM AM/PM"

Examples:
- "10/20/2025 09:00 AM"
- "11/15/2025 02:30 PM"
- "12/01/2025 05:00 PM"
```

## Common Use Case Workflows

### Use Case: Client Follow-Up System

```markdown
Scenario: Track follow-ups with Partner Project partnership

Step 1: Create initial reminder
mcp__reminders__create_reminder(
  name: "Follow up with Partner Contact on partnership terms",
  listName: "Partner Project",
  body: "Discuss equity structure and timeline. Reference: Obsidian Partner Project Master Command Center",
  priority: 1,
  dueDate: "10/22/2025 10:00 AM"
)

Step 2: After follow-up, create next reminder
mcp__reminders__create_reminder(
  name: "Send partnership proposal to partner contact",
  listName: "Partner Project",
  body: "Based on discussion on 10/22. Include market research findings.",
  priority: 1,
  dueDate: "10/25/2025 09:00 AM"
)

Step 3: Mark previous reminder complete
mcp__reminders__update_reminder(reminderId: [id], completed: true)
```

### Use Case: Project Milestone Tracking

```markdown
Scenario: Track Business Project email campaign milestones

Step 1: Create milestone reminders
mcp__reminders__create_reminder(
  name: "Complete email 2-3 messaging updates",
  listName: "LightForge Works",
  priority: 5,
  dueDate: "10/23/2025 03:00 PM"
)

mcp__reminders__create_reminder(
  name: "Complete email 4-7 messaging updates",
  listName: "LightForge Works",
  priority: 5,
  dueDate: "10/25/2025 03:00 PM"
)

Step 2: As milestones complete, mark done
mcp__reminders__update_reminder(reminderId: [id], completed: true)

Step 3: Update Obsidian with progress
mcp__obsidian__append_to_note(
  notePath: "Areas/Business/Business Project/Email Marketing Campaign.md",
  content: "\n\n## Update 10/23/2025\n- Emails 2-3 messaging completed\n"
)
```

### Use Case: Daily Review System

```markdown
Scenario: Morning review of priorities

Step 1: Get today's due reminders
results = mcp__reminders__get_reminders(completed: false)
Filter for dueDate === today

Step 2: Get all high-priority incomplete
Filter results for priority === 1

Step 3: Triage and reschedule if needed
For each reminder:
  if still_valid:
    keep or update due date
  else:
    mark complete or delete
```

### Use Case: Research Task Management

```markdown
Scenario: Track research tasks that don't have hard deadlines

Step 1: Create low-priority reminders
mcp__reminders__create_reminder(
  name: "Research AlphaFold competitors for Partner Project market analysis",
  listName: "Partner Project",
  body: "Use Perplexity API skill. Save results to Obsidian.",
  priority: 9,  # Low priority - do when time allows
  # No due date - flexible timing
)

Step 2: When starting research, escalate priority
mcp__reminders__update_reminder(
  reminderId: [id],
  priority: 5,  # Medium - actively working
  dueDate: "10/24/2025 05:00 PM"  # Set completion target
)

Step 3: Mark complete and link to Obsidian results
mcp__reminders__update_reminder(
  reminderId: [id],
  completed: true,
  body: "Research completed. Results: Obsidian Areas/Companies/Partner Project/market_research/Competitive Landscape Synthesis.md"
)
```

## Bulk Operations Patterns

### Pattern: Weekly Cleanup

```markdown
Workflow:
1. Get all completed reminders from last week
   results = mcp__reminders__get_reminders(completed: true)

2. Review and archive
   For each completed reminder:
     if important_context:
       Extract to Obsidian note
     if no_longer_relevant:
       mcp__reminders__delete_reminder(reminderId: [id])

3. Triage incomplete reminders
   incomplete = mcp__reminders__get_reminders(completed: false)
   For each:
     Evaluate: still relevant? Update priority? Reschedule?
```

### Pattern: List-Specific Review

```markdown
Workflow: Review specific project list

Step 1: Get all reminders for project
reminders = mcp__reminders__get_reminders(listName: "Partner Project", completed: false)

Step 2: Sort by priority and due date
Sort results by: priority ASC, dueDate ASC

Step 3: Update or complete as needed
For each reminder:
  Evaluate status and update accordingly
```

## Error Handling and Edge Cases

### Handle: Reminder Not Found

```markdown
# Search returns no results
results = mcp__reminders__search_reminders(searchTerm: "obscure task")
if not results or len(results) == 0:
  # Create new reminder instead
  mcp__reminders__create_reminder(...)
```

### Handle: Duplicate Prevention

```markdown
# Before creating, search for existing
existing = mcp__reminders__search_reminders(searchTerm: "Follow up with partner")
if existing and len(existing) > 0:
  # Update existing instead of creating duplicate
  mcp__reminders__update_reminder(
    reminderId: existing[0].id,
    dueDate: "[new date]"
  )
else:
  # Create new
  mcp__reminders__create_reminder(...)
```

### Handle: List Doesn't Exist

```markdown
# Before creating, verify list exists
lists = mcp__reminders__list_reminder_lists()
list_names = [l.name for l in lists]

if "ProjectName" not in list_names:
  # Fall back to default list
  listName = "Work"
else:
  listName = "ProjectName"

mcp__reminders__create_reminder(listName: listName, ...)
```

## Reminders Management Checklist

Before creating or updating reminders:

- [ ] **Duplicate Check**: Have I searched for existing reminders on this topic?
- [ ] **List Selection**: Am I using the appropriate list for this task context?
- [ ] **Priority Setting**: Have I set priority based on urgency and impact?
- [ ] **Due Date Decision**: Does this task need a specific due date, or is it flexible?
- [ ] **Context Addition**: Have I added body text with links to Obsidian or other resources?
- [ ] **Integration Plan**: Should this reminder be synced to Obsidian or other systems?
- [ ] **Completion Tracking**: Will I remember to mark this complete when done?

## Common Patterns Summary

| Goal | Primary Tool | Parameters | Notes |
|------|-------------|------------|-------|
| Discover lists | list_reminder_lists | None | Start here |
| Create task | create_reminder | name, listName, priority, dueDate, body | Always set priority |
| Find reminders | search_reminders | searchTerm | Search name and body |
| Get list tasks | get_reminders | listName, completed | Filter by list |
| Change priority | update_reminder | reminderId, priority | 1=high, 5=med, 9=low |
| Reschedule | update_reminder | reminderId, dueDate | Format: MM/DD/YYYY HH:MM AM/PM |
| Mark complete | update_reminder | reminderId, completed: true | Always mark done |
| Add context | update_reminder | reminderId, body | Link to Obsidian |
| Delete reminder | delete_reminder | reminderId | Use sparingly |

## Integration with Other Skills

### With coordinating-sub-agents

```
Create reminders for follow-up on delegated tasks
Track sub-agent progress with time-based reminders
Mark reminders complete when sub-agent delivers
```

### With syncing-task-completions

```
Bi-directional sync between Reminders and Obsidian
Update master task lists with completion dates
Create reminders for untracked Obsidian TODOs
```

### With processing-paia-tags

```
Create reminders for time-sensitive @paia actions
Link reminders back to source Obsidian notes
Mark @paia complete when reminder is done
```

### With obsidian-vault-intelligence

```
Reference Obsidian notes in reminder body text
Create reminders from Obsidian action items
Update Obsidian when reminders complete
```

## Apple Reminders as Task Management Layer

Think of Apple Reminders as:
- **Time-Based Task Tracking**: Due dates and notifications for time-sensitive work
- **Priority Queue**: High/medium/low priority organization
- **Cross-Device Sync**: Tasks accessible on all Apple devices
- **Integration Hub**: Bridge between Obsidian, Claude, and daily workflow
- **Completion Tracking**: Clear record of what's done and when

Use it proactively for:
- Client follow-up tracking
- Project milestone reminders
- Weekly/monthly review triggers
- Time-sensitive task delegation
- Bi-directional sync with Obsidian task system
