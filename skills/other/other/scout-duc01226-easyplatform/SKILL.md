---
name: scout
version: 1.0.0
description: "[Investigation] Fast codebase file discovery for task-related files. Use when quickly locating relevant files across a large codebase, beginning work on features spanning multiple directories, or before making changes that might affect multiple parts. Triggers on "find files", "locate", "scout", "search codebase", "what files"."

allowed-tools: Glob, Grep, Read, Task, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

## Quick Summary

**Goal:** Fast, parallel codebase file discovery to locate all files relevant to a task.

**Workflow:**

1. **Analyze Request** — Extract entity names, feature keywords, file types from prompt
2. **Parallel Search** — Spawn 3 agents searching backend core, backend infra, and frontend paths
3. **Synthesize** — Combine into numbered, prioritized file list with suggested starting points

**Key Rules:**

- Speed over depth -- return file paths only, no content analysis
- Target 3-5 minutes total completion time
- 3-minute timeout per agent; skip agents that don't return in time

# Scout - Fast Codebase File Discovery

Fast codebase search to locate files needed for a task. Token-efficient, parallel execution.

**KEY PRINCIPLE**: Speed over depth. Return file paths only - no content analysis. Target 3-5 minutes total.

---

## When to Use

- Quickly locating relevant files across a large codebase
- Beginning work on features spanning multiple directories
- Before making changes that might affect multiple parts
- Mapping file landscape before investigation or implementation
- Finding all files related to an entity, feature, or keyword

**NOT for**: Deep code analysis (use `feature-investigation`), debugging (use `debug`), or implementation (use `feature-implementation`).

> **UI Work Detected?** If the task involves updating UI, fixing UI, or finding a component from a screenshot/image, activate `visual-component-finder` skill FIRST before scouting. It uses a pre-built component index for fast visual-to-code matching.

---

## Quick Reference

| Input               | Description                                         |
| ------------------- | --------------------------------------------------- |
| `USER_PROMPT`       | What to search for (entity names, feature keywords) |
| `SCALE`             | Number of parallel agents (default: 3)              |
| `REPORT_OUTPUT_DIR` | Use `Report:` path from `## Naming` section         |

---

## Workflow

### Step 1: Analyze Search Request

Extract keywords from USER_PROMPT to identify:

- Entity names (e.g., Employee, Candidate, Survey)
- Feature names (e.g., authentication, notification)
- File types needed (backend, frontend, or both)

### Step 2: Execute Parallel Search

Spawn SCALE number of `Explore` subagents in parallel using `Task` tool.

#### Agent Distribution Strategy

- **Agent 1 - Backend Core**: `src/Services/*/Domain/`, `src/Services/*/UseCaseCommands/`, `src/Services/*/UseCaseQueries/`
- **Agent 2 - Backend Infra**: `src/Services/*/UseCaseEvents/`, `src/Services/*/Controllers/`, `src/Services/*/BackgroundJobs/`
- **Agent 3 - Frontend**: `{frontend-apps-dir}/`, `{frontend-libs-dir}/{domain-lib}/`, `{frontend-libs-dir}/{common-lib}/`

#### Agent Instructions

- **Timeout**: 3 minutes per agent
- Skip agents that don't return within timeout
- Use Glob for file patterns, Grep for content search
- Return only file paths, no content

### Step 3: Synthesize Results

Combine results into a **numbered, prioritized file list** (see Results Format below).

---

## Search Patterns by Priority

```
# HIGH PRIORITY - Core Logic
**/Domain/Entities/**/*{keyword}*.cs
**/UseCaseCommands/**/*{keyword}*.cs
**/UseCaseQueries/**/*{keyword}*.cs
**/UseCaseEvents/**/*{keyword}*.cs
**/*{keyword}*.component.ts
**/*{keyword}*.store.ts

# MEDIUM PRIORITY - Infrastructure
**/Controllers/**/*{keyword}*.cs
**/BackgroundJobs/**/*{keyword}*.cs
**/*Consumer*{keyword}*.cs
**/*{keyword}*-api.service.ts

# LOW PRIORITY - Supporting
**/*{keyword}*Helper*.cs
**/*{keyword}*Service*.cs
**/*{keyword}*.html
```

---

## Results Format

```markdown
## Scout Results: {USER_PROMPT}

### High Priority - Core Logic

1. `src/Services/{Service}/Domain/Entities/{Entity}.cs`
2. `src/Services/{Service}/UseCaseCommands/{Feature}/Save{Entity}Command.cs`
   ...

### Medium Priority - Infrastructure

10. `src/Services/{Service}/Controllers/{Entity}Controller.cs`
11. `src/Services/{Service}/UseCaseEvents/{Feature}/SendNotificationOn{Entity}CreatedEventHandler.cs`
    ...

### Low Priority - Supporting

20. `src/Services/{Service}/Helpers/{Entity}Helper.cs`
    ...

### Frontend Files

30. `{frontend-libs-dir}/{domain-lib}/src/lib/{feature}/{feature}-list.component.ts`
    ...

**Total Files Found:** {count}
**Search Completed In:** {time}

### Suggested Starting Points

1. `{most relevant file}` - {reason}
2. `{second most relevant}` - {reason}

### Unresolved Questions

- {any questions that need clarification}
```

---

## Quality Standards

| Standard       | Expectation                            |
| -------------- | -------------------------------------- |
| **Speed**      | Complete in 3-5 minutes                |
| **Accuracy**   | Return only relevant files             |
| **Coverage**   | Search all likely directories          |
| **Efficiency** | Minimize tool calls                    |
| **Structure**  | Always use numbered, prioritized lists |

---

## Report Output

Use naming pattern: `plans/reports/scout-{date}-{slug}.md`

**Output Standards:**

- Sacrifice grammar for concision
- List unresolved questions at end
- Always provide numbered file list with priority ordering

---

## See Also

- `feature-investigation` skill - Deep analysis of discovered files
- `feature-implementation` skill - Implementing features after scouting
- `planning` skill - Creating implementation plans from scouted files

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
