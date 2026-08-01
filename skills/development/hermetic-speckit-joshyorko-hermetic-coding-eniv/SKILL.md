---
name: hermetic-speckit
description: Build software using isolated container-use environments with SpecKit
  workflow. Use when user needs to build a feature, application, or complex task that
  benefits from spec-driven development. Keyword
---

---
name: Hermetic SpecKit
description: Build software using isolated container-use environments with SpecKit workflow. Use when user needs to build a feature, application, or complex task that benefits from spec-driven development. Keywords: build, create, implement, feature, app, application, spec, plan, hermetic, isolated, dagger.
---

# Hermetic SpecKit Skill

This skill provides hermetic, isolated development environments using Dagger container-use with GitHub SpecKit workflow for spec-driven development.

## Architecture

```
User Prompt → Main Claude (Orchestrator)
                    │
                    ├─► Create container-use environment
                    │
                    └─► Spawn subagents for SpecKit phases:
                        1. /speckit.specify → spec.md
                        2. /speckit.clarify → (orchestrator responds)
                        3. /speckit.plan → plan.md
                        4. /speckit.tasks → tasks.md
                        5. /speckit.analyze → validation
                        │
                        └─► Report to user for approval
                              │
                              └─► Fan out implementation to parallel envs
```

## Variables

- **REPO_SOURCE**: The absolute path to the current repository
- **ENVIRONMENT_PREFIX**: `speckit-` (prefix for environment names)

## Prerequisites

container-use MCP server must be configured:
```bash
claude mcp add container-use -- container-use stdio
```

## MCP Tools (container-use)

| Tool | Purpose |
|------|---------|
| `environment_create` | Create isolated git worktree environment |
| `environment_config` | Configure base image and setup commands |
| `environment_run_cmd` | Execute commands in container |
| `environment_file_write` | Write files (auto-committed) |
| `environment_file_read` | Read files from environment |
| `environment_list` | List existing environments |
| `environment_open` | Open existing environment |

## Critical Rules

1. **ALWAYS use container-use MCP for ALL file/code operations** - Never use local filesystem tools
2. **DO NOT use git CLI** - container-use handles git automatically
3. **Capture environment ID** - Store in context, use for all subsequent operations
4. **Report access commands** - Always tell user: `container-use checkout <env_id>`

## Workflow

### Phase 1: Environment Setup

When user requests a complex build task:

1. **Create environment**:
   ```
   environment_create(
       environment_source=REPO_SOURCE,
       title="<descriptive task name>"
   )
   ```

2. **Configure for Python** (if needed):
   ```
   environment_config(
       environment_id=<env_id>,
       config={
           "base_image": "python:3.12-slim",
           "setup_commands": ["pip install --upgrade pip"]
       }
   )
   ```

3. **Capture the environment ID** in your context

### Phase 2: SpecKit Specification

Spawn a subagent (or run inline) to execute SpecKit phases:

**Step 2.1: Specify**
- Generate `.specify/spec.md` with the feature specification
- Include: What, Why, User Stories, Success Metrics
- Write using `environment_file_write`

**Step 2.2: Clarify (Self-Response)**
- Read the spec and identify ambiguities
- Generate clarifying questions
- **Orchestrator responds** to questions (not user)
- Update spec with clarifications

**Step 2.3: Plan**
- Generate `.specify/plan.md` with implementation plan
- Include: Architecture, Data Model, API Contracts, File Structure
- Reference the constitution if it exists

**Step 2.4: Tasks**
- Generate `.specify/tasks.md` with atomic tasks
- Mark parallel-safe tasks with `[P]`
- Ensure each task is < 4 hours of work
- Include file paths and dependencies

**Step 2.5: Analyze**
- Cross-check spec.md, plan.md, tasks.md for consistency
- Flag any gaps or conflicts
- Update artifacts as needed

### Phase 3: User Checkpoint

**STOP and report to user:**

```
SpecKit artifacts ready for review:

Environment: <env_id>
Branch: container-use/<env_id>

To review:
- container-use checkout <env_id>
- container-use diff <env_id>

Generated artifacts:
- .specify/spec.md - Feature specification
- .specify/plan.md - Implementation plan
- .specify/tasks.md - Task breakdown

Proceed with implementation? [Y/n]
```

Wait for user approval before implementation.

### Phase 4: Implementation (Fan-Out)

For each task in tasks.md:

1. **Identify parallel tasks** (marked with `[P]`)

2. **Create environment per task**:
   ```
   environment_create(
       environment_source=REPO_SOURCE,
       title="Task: <task description>"
   )
   ```

3. **Execute task** via subagent:
   - Read task details from tasks.md
   - Write code using `environment_file_write`
   - Run tests using `environment_run_cmd`
   - Iterate until tests pass

4. **Mark complete** in tasks.md when tests pass

5. **Report environment** to user:
   ```
   Task complete: <task description>
   View: container-use checkout <task_env_id>
   ```

### Phase 5: Final Report

After all tasks complete:

```
Implementation complete!

Environments created:
- <main_env_id> (SpecKit artifacts)
- <task1_env_id> (Task 1 implementation)
- <task2_env_id> (Task 2 implementation)
...

To merge all work:
1. container-use checkout <main_env_id>
2. Review each task branch
3. Merge as desired

To clean up:
- Environments persist until manually deleted
```

## Examples

### Example 1: Build a REST API

**User**: "Build a REST API for user authentication with JWT"

**Orchestrator**:
1. Creates environment: `speckit-auth-api`
2. Spawns subagent for SpecKit phases
3. Generates spec.md, plan.md, tasks.md
4. Reports to user for approval
5. Fans out to: `task-1-models`, `task-2-routes`, `task-3-jwt`
6. Each subagent implements in parallel
7. Reports all environments to user

### Example 2: Refactor a Module

**User**: "Refactor the payment module to use the strategy pattern"

**Orchestrator**:
1. Creates environment: `speckit-payment-refactor`
2. Reads existing code via `environment_file_read`
3. Generates refactoring spec and plan
4. Tasks breakdown by component
5. Implements with tests

## Troubleshooting

**"Container not found"**:
- Verify environment exists: `environment_list`
- Re-create if needed: `environment_create`

**"Python not found"**:
- Configure base image: `environment_config` with `python:3.12-slim`

**"Changes not showing"**:
- All changes auto-commit to branch
- Use `container-use checkout <env_id>` to view

## References

- [Container-Use Architecture](../../../docs/container-use-architecture.md)
- [Architecting Robust Agentic Systems](../../../docs/Architecting%20Robust%20Agentic%20Systems%3A%20Integrating%20S....md)
- [dagger/container-use](https://github.com/dagger/container-use)
- [github/spec-kit](https://github.com/github/spec-kit)
