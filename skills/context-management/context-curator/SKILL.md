---
name: context-curator
description: Use when starting a complex task to load relevant context from Memory MCP and suggest appropriate skills based on task type.
---

# Context Curator Skill

## Purpose

Dynamically load relevant context based on the current task type. This skill implements the "Curation Layer" from context engineering principles.

## When to Use

- Starting a new complex task
- Resuming work on a feature after a break
- Need to recall past decisions or patterns
- Want to ensure consistent patterns with previous work

## Task Type Detection

Analyze the user's request to determine task type:

| Keywords                              | Task Type              | Relevant Skills                                        |
| ------------------------------------- | ---------------------- | ------------------------------------------------------ |
| bug, error, fix, broken, debug        | debugging              | bug-diagnosis, tasks-bug-diagnosis                     |
| command, save, create, update, delete | backend-cqrs           | backend-cqrs-command, backend-entity-development       |
| query, list, get, search, filter      | backend-query          | backend-cqrs-query, backend-entity-development         |
| component, UI, frontend, Angular      | frontend               | frontend-angular-component, frontend-angular-store     |
| form, validation, input               | frontend-form          | frontend-angular-form, frontend-angular-component      |
| API, service, http                    | api-integration        | frontend-angular-api-service, backend-cqrs-command     |
| review, refactor, improve             | code-review            | code-review, tasks-code-review                         |
| test, spec, coverage                  | testing                | test-generation, tasks-test-generation                 |
| message, event, bus, sync             | cross-service          | backend-message-bus, arch-cross-service-integration    |
| migration, schema, database           | data-migration         | backend-data-migration, db-migrate                     |
| job, background, scheduled, recurring | background-job         | backend-background-job                                 |
| security, auth, permission            | security               | arch-security-review                                   |
| performance, slow, optimize           | performance            | arch-performance-optimization                          |
| implement, feature, add, build        | feature-implementation | feature-implementation, tasks-feature-implementation   |
| document, readme, docs                | documentation          | documentation, tasks-documentation, readme-improvement |
| branch, compare, diff, changes        | branch-comparison      | branch-comparison, tasks-spec-update                   |

## Execution Steps

### Step 1: Detect Task Type

Analyze user request keywords to identify task type from the table above.

### Step 2: Load Memory Context

Search Memory MCP for relevant entities:

```
mcp__memory__search_nodes({ query: "[task-type] [feature-name]" })
```

Key entities to query:

- `ProjectContext` - Overall codebase structure
- `FeatureProgress_[branch]` - Current feature status
- `PatternHistory` - Successfully used patterns
- `RecentDecisions` - Recent architectural decisions

### Step 3: Suggest Relevant Skills

Based on detected task type, recommend specific skills from the table.

### Step 4: Load Reference Files

For each task type, suggest key reference files:

**Backend CQRS:**

- `src/PlatformExampleApp/PlatformExampleApp.TextSnippet.Application/UseCaseCommands/` - Command examples
- `.github/skills/backend-cqrs-command/SKILL.md` - Patterns guide

**Frontend Angular:**

- `src/PlatformExampleAppWeb/apps/playground-text-snippet/` - Component examples
- `.github/skills/frontend-angular-component/SKILL.md` - Patterns guide

**Debugging:**

- `.github/AI-DEBUGGING-PROTOCOL.md` - Full debugging protocol
- `.github/instructions/debugging.instructions.md` - Quick reference

### Step 5: Output Context Summary

Provide formatted summary:

```markdown
## Context Loaded

**Task Type:** [detected type]
**Suggested Skills:** [skill-1], [skill-2]
**Memory Context:** [relevant entities found]
**Reference Files:** [key files to read]

**Previous Work:**

- [Relevant past decisions]
- [Patterns used successfully]
- [Current feature progress]

**Next Steps:**

1. [Recommended first action]
2. [Recommended second action]
```

## Memory Integration

After completing significant work, store learnings:

```
mcp__memory__create_entities({
  entities: [{
    name: "Decision_[timestamp]",
    entityType: "ArchitecturalDecision",
    observations: ["Chose X because Y", "Pattern used: Z"]
  }]
})
```

## Example Usage

User: "I need to add a new endpoint for task management"

Context Curator Output:

```markdown
## Context Loaded

**Task Type:** backend-cqrs + api-integration
**Suggested Skills:** backend-cqrs-command, backend-cqrs-query, frontend-angular-api-service
**Memory Context:** Found FeatureProgress_task-management with 3 observations

**Previous Work:**

- Task entity already created (TaskItemEntity.cs)
- Using SaveTaskItemCommand pattern

**Next Steps:**

1. Check existing TaskItemController for patterns
2. Use backend-cqrs-command skill for new command
3. Update frontend API service
```
