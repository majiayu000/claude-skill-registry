---
name: requirements-gatherer
description: Use when gathering project requirements - asks structured questions about project type, scope, integrations, and constraints to populate project_state.md
version: 1.3.1
allowed-tools: Read, Write, Glob
---

# Requirements Gatherer

Ask structured questions to define project requirements.

## Activation

Activate when:
- Invoked by `project-initializer` after project setup
- User says "Gather requirements" or "Define requirements"
- Starting Phase 1 on a new project

## Workflow

### 1. Load Project Context

Use `Read` to get `{project_path}/project_state.md`. Extract:
- Project name
- Current scope (if any)
- Existing requirements (if resuming)

### 2. Ask Questions by Category

Ask one category at a time. Wait for response before proceeding.

**Category 1: Project Type & Scope**
```
What type of project is this?
- [ ] New Drupal module (starting from scratch)
- [ ] Feature for existing module
- [ ] Core issue/patch
- [ ] Theme or sub-theme
- [ ] Configuration/site building
- [ ] Other (Claude Code plugin, documentation, etc.)

What does this project include?
- [ ] A single Drupal module
- [ ] Multiple related modules
- [ ] A theme or sub-theme
- [ ] Configuration/site building
- [ ] Mix of the above

Please describe:
```

**Category 2: Core Functionality**
```
What is the main purpose?
1. What problem does it solve?
2. What are the must-have features?
3. What are nice-to-have features?
```

**Category 3: User Roles**
```
Who will use this?
1. Which user roles need access?
2. What permissions are needed?
3. Any role-specific features?
```

**Category 4: Data Requirements**
```
What data is involved?
1. New content types or entities needed?
2. New fields on existing types?
3. Configuration data to store?
4. Relationships to existing content?
```

**Category 5: Integrations**
```
What existing systems does this connect to?
1. Existing Drupal modules to integrate with?
2. External APIs or services?
3. ECA workflows needed?
4. Third-party libraries?
```

**Category 6: UI Requirements**
```
What interfaces are needed?
1. Admin forms or pages?
2. Frontend display requirements?
3. Specific UX patterns to follow?
4. Mobile considerations?
```

**Category 7: Constraints**
```
What limitations should we know about?
1. Drupal version (10.x, 11.x)?
2. Performance requirements?
3. Accessibility requirements (WCAG level)?
4. Browser support needs?
```

### 3. Handle Responses

For each category:
- Accept the answer
- Allow "skip" or "not sure yet" - mark as open question
- Summarize understanding back to user
- Proceed to next category

### 4. Update project_state.md

After all categories, use `Edit` tool to update the Requirements section:

```markdown
## Requirements

### Project Type
- {new module, existing feature, core issue, theme, config, other}

### Scope
- {what project includes}

### Core Functionality
- {requirement 1}
- {requirement 2}

### User Roles
| Role | Permissions | Features |
|------|-------------|----------|
| {role} | {perms} | {features} |

### Data Requirements
- {data type}: {storage approach}

### Integrations
- {module/service}: {integration type}

### UI Requirements
- {element}: {requirement}

### Constraints
- {constraint}: {details}

### Open Questions
- {questions marked as "not sure yet"}
```

### 5. Confirm Requirements

Show summary to user:
```
Requirements gathered for {project_name}:

Core: {1-2 sentence summary}
Roles: {list roles}
Integrations: {list integrations}
Open questions: {count}

Does this look complete? (yes/no/add more)
```

If "add more", ask what category to expand.

### 6. Transition to Task Definition

After user confirms requirements are complete:

```
Requirements complete!

Now let's define your first task. What feature or component do you want to work on first?

Examples:
- "Add settings form for API configuration"
- "Create custom entity for storing data"
- "Build admin dashboard"

Each task will go through:
1. Research (understand & find patterns)
2. Architecture (design the approach)
3. Implementation (build with TDD)

Enter your first task:
```

**IMPORTANT:** Do NOT suggest `/research` or `/design` at the project level. Tasks are what go through phases, not the project.

### 7. Create First Task

When user provides a task name:

1. **Validate task name** - convert to lowercase with underscores (e.g., "Add settings form" → `settings_form`)

2. **Confirm task creation:**
   ```
   Creating task: {task_name}

   Brief description (one sentence - what does this task accomplish?):
   ```

3. **Wait for user to provide description**

4. **Invoke research phase:**
   ```
   Starting research phase for: {task_name}
   ```
   Then invoke `/drupal-dev-framework:research {task_name}`

**CRITICAL:** Do NOT start research until:
- Task name is confirmed
- User provides a description
- Task creation is acknowledged

## Stop Points

STOP and wait for user after:
- Each category question
- Showing summary for confirmation
- Asking for first task
- After asking for task description (Step 7.2)
- User says "add more"
