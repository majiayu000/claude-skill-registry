---
# VERSION: 2.88.0
name: create-task-batch
description: "Interactive wizard to create PRD or task lists for /task-batch. Uses /clarify and /ask-questions-if-underspecified for precise task definition. Use when: (1) preparing batch execution, (2) creating PRDs, (3) defining task lists with dependencies. Triggers: /create-task-batch, 'create tasks', 'new batch', 'prepare PRD'."
argument-hint: "[feature-name|project-description]"
user-invocable: true
context: fork
agent: orchestrator
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Glob
  - Grep
---

# /create-task-batch - Interactive Task List Creator (v2.88)

**Interactive wizard** for creating PRD documents and task lists optimized for `/task-batch` execution. Uses guided questioning to extract precise requirements, priorities, and dependencies.

## Quick Start

```bash
# Start interactive wizard
/create-task-batch

# With initial description
/create-task-batch "User authentication feature"

# For specific project area
/create-task-batch "API refactoring project"
```

## Workflow

```
+------------------------------------------------------------------+
|              CREATE-TASK-BATCH WORKFLOW                           |
+------------------------------------------------------------------+
|                                                                   |
|   +----------+    +-----------+    +---------------+              |
|   | GATHER   |--->| DECOMPOSE |--->| PRIORITIZE    |              |
|   | Context  |    | Into Tasks|    | & Dependencies|              |
|   +----------+    +-----------+    +-------+-------+              |
|                                                |                  |
|   +--------------------------------------------v---------------+ |
|   |                    VALIDATE                                 | |
|   |  - Each task has acceptance criteria                       | |
|   |  - Dependencies are resolvable                             | |
|   |  - Priorities are assigned                                 | |
|   +---------------------------+-------------------------------+ |
|                               |                                 |
|   +---------------------------v-------------------------------+ |
|   |                    OUTPUT                                   | |
|   |  - PRD file (.prq.md)                                      | |
|   |  - Task list (tasks.md)                                    | |
|   |  - JSON config (optional)                                  | |
|   +------------------------------------------------------------+ |
|                                                                   |
+------------------------------------------------------------------+
```

## Questioning Phases

### Phase 1: PROJECT CONTEXT

```yaml
AskUserQuestion:
  questions:
    - question: "What is the main goal of this batch?"
      header: "Goal"
      options:
        - label: "New Feature"
          description: "Implement a complete new feature"
        - label: "Bug Fixes"
          description: "Fix multiple related bugs"
        - label: "Refactoring"
          description: "Restructure existing code"
        - label: "Documentation"
          description: "Create or update documentation"

    - question: "What is the project area?"
      header: "Area"
      options:
        - label: "Backend API"
        - label: "Frontend UI"
        - label: "Database"
        - label: "Infrastructure"
        - label: "Full Stack"

    - question: "What is the target timeframe?"
      header: "Timeframe"
      options:
        - label: "Single session"
        - label: "1-2 days"
        - label: "1 week"
        - label: "Sprint (2 weeks)"
```

### Phase 2: FEATURE DETAILS

```yaml
AskUserQuestion:
  questions:
    - question: "Describe the main feature/functionality in detail"
      header: "Description"
      multiSelect: false
      # User provides free-form description

    - question: "What are the MUST-HAVE components?"
      header: "Must Have"
      multiSelect: true
      options:
        - label: "Authentication"
        - label: "Data validation"
        - label: "Error handling"
        - label: "Logging"
        - label: "Testing"
        - label: "Documentation"

    - question: "What are NICE-TO-HAVE components?"
      header: "Nice to Have"
      multiSelect: true
      options:
        - label: "Performance optimization"
        - label: "Caching"
        - label: "Rate limiting"
        - label: "Monitoring"
        - label: "CI/CD integration"
```

### Phase 3: TASK DECOMPOSITION

```yaml
# Automatic decomposition based on responses
Task Decomposition Rules:
  - Backend Feature:
    1. Create data models/schemas
    2. Implement business logic
    3. Create API endpoints
    4. Add validation
    5. Write tests
    6. Update documentation

  - Frontend Feature:
    1. Create UI components
    2. Implement state management
    3. Connect to API
    4. Add error handling
    5. Write tests
    6. Update documentation

  - Refactoring:
    1. Analyze current implementation
    2. Design new structure
    3. Create new modules
    4. Migrate existing code
    5. Update tests
    6. Remove deprecated code
```

### Phase 4: PRIORITY & DEPENDENCIES

```yaml
AskUserQuestion:
  questions:
    - question: "How should tasks be prioritized?"
      header: "Priority"
      options:
        - label: "Auto (by dependencies)"
        - label: "Manual (I will specify)"
        - label: "By effort (easiest first)"
        - label: "By importance (critical first)"

    - question: "Should execution stop on first failure?"
      header: "Stop on Fail"
      options:
        - label: "Yes - Stop entire batch"
        - label: "No - Continue with remaining"
```

### Phase 5: ACCEPTANCE CRITERIA (MANDATORY FOR EACH TASK)

**CRITICAL: Every task MUST have explicit completion validation criteria.**
**No task can be executed without defined acceptance criteria.**

```yaml
# MANDATORY: For EACH generated task, ask completion criteria
FOR EACH task IN task_list:
  AskUserQuestion:
    questions:
      - question: "Define MANDATORY completion criteria for '[TASK_NAME]':"
        header: "Criteria"
        # MANDATORY - Cannot proceed without answer

      - question: "How will we VERIFY this task is complete?"
        header: "Verification"
        options:
          - label: "Tests pass"
            description: "Unit/integration tests must pass"
          - label: "File exists"
            description: "Specific file(s) created/modified"
          - label: "Command succeeds"
            description: "Specific command runs without error"
          - label: "Manual review"
            description: "Human reviews and approves"

      - question: "What files/modules are affected by '[TASK_NAME]'?"
        header: "Files"
        # Optional but recommended

# VALIDATION CHECK
IF any_task_missing_criteria:
  BLOCK: "Cannot create batch - all tasks MUST have completion criteria"
  ASK: Request missing criteria before proceeding
```

#### Task Completion Criteria Template

Each task in the output MUST include:

```yaml
task:
  id: "task-001"
  description: "Create OAuth2 service module"
  priority: 1
  completion_criteria:  # MANDATORY
    - criteria: "File src/auth/oauth2.service.ts exists"
      verification: "file_exists"
    - criteria: "Google OAuth client configured"
      verification: "code_contains"
      pattern: "GoogleAuthProvider"
    - criteria: "Unit tests pass"
      verification: "command"
      command: "npm test -- oauth2.service.spec.ts"
    - criteria: "No TypeScript errors"
      verification: "command"
      command: "tsc --noEmit"
  dependencies: []
```

## Output Templates

### Template 1: PRD Format (.prq.md)

```markdown
# Feature: {FEATURE_NAME}

**Created**: {TIMESTAMP}
**Version**: 2.88
**Timeframe**: {TIMEFRAME}

## Priority: {PRIORITY}

## Overview
{DESCRIPTION}

## Tasks

{#for task in tasks}
- [ ] {task.priority}: {task.description}
{#endfor}

## Dependencies
{#for dep in dependencies}
- {dep.task} depends on {dep.depends_on}
{#endfor}

## Acceptance Criteria
{#for task in tasks}
### {task.name}
{#for criteria in task.criteria}
- {criteria}
{#endfor}
{#endfor}

## Technical Notes
{TECHNICAL_NOTES}

## Risks
{#for risk in risks}
- {risk}
{#endfor}
```

### Template 2: Task List Format (tasks.md)

```markdown
# Batch: {BATCH_NAME}

**Created**: {TIMESTAMP}
**Config**: stop_on_failure={STOP_ON_FAILURE}, auto_commit=true

## Tasks

{#for task in tasks}
{task.number}. [{task.priority}] {task.description}
   - Files: {task.files}
   - Criteria: {task.criteria}
{#endfor}

## Execution Order
{EXECUTION_ORDER}
```

### Template 3: JSON Format

```json
{
  "batch_name": "{BATCH_NAME}",
  "created": "{TIMESTAMP}",
  "config": {
    "stop_on_failure": {STOP_ON_FAILURE},
    "auto_commit": true,
    "teammates": ["coder", "reviewer"]
  },
  "tasks": [
    {
      "id": "task-001",
      "description": "{description}",
      "priority": 1,
      "dependencies": [],
      "acceptance_criteria": ["{criteria}"],
      "files": ["{files}"]
    }
  ]
}
```

## CLI Usage

```bash
# Interactive mode (all questions)
ralph create-batch

# With initial description
ralph create-batch "Implement user authentication"

# Quick mode (minimal questions)
ralph create-batch --quick "Add API rate limiting"

# Output format selection
ralph create-batch --format json
ralph create-batch --format prd
ralph create-batch --format tasks

# Save to specific location
ralph create-batch --output docs/prd/auth.prq.md
```

## Integration with /task-batch

After creating the task list:

```bash
# Step 1: Create the batch
/create-task-batch "User authentication"

# Step 2: Review generated PRD
# File saved to: docs/prd/user-authentication.prq.md

# Step 3: Execute the batch
/task-batch docs/prd/user-authentication.prq.md

# Or with options
/task-batch docs/prd/user-authentication.prq.md --priority
```

## Example Session

```
User: /create-task-batch "User profile feature"

Assistant: I'll help you create a task batch for "User profile feature".

[Phase 1: PROJECT CONTEXT]
Q: What is the main goal of this batch?
A: New Feature

Q: What is the project area?
A: Full Stack

Q: What is the target timeframe?
A: 1-2 days

[Phase 2: FEATURE DETAILS]
Q: Describe the main feature in detail:
A: Users should be able to view and edit their profile, upload avatar, and set preferences

Q: What are the MUST-HAVE components?
A: Authentication, Data validation, Testing

[Phase 3: TASK DECOMPOSITION]
Based on your input, I've decomposed the feature into these tasks:

1. [P1] Create user profile data model
2. [P1] Implement profile API endpoints (GET, PUT)
3. [P2] Create profile UI page
4. [P2] Add avatar upload functionality
5. [P3] Implement user preferences
6. [P3] Write unit and integration tests

[Phase 4: PRIORITY & DEPENDENCIES]
Q: How should tasks be prioritized?
A: Auto (by dependencies)

Q: Should execution stop on first failure?
A: No - Continue with remaining

[Phase 5: ACCEPTANCE CRITERIA]
Q: Acceptance criteria for "Create user profile data model":
A: Schema exists, migrations run, validation works

[OUTPUT]
Created: docs/prd/user-profile-feature.prq.md

Ready to execute with:
/task-batch docs/prd/user-profile-feature.prq.md
```

## Anti-Patterns

- **NEVER** create tasks without acceptance criteria
- **NEVER** skip the dependency check
- **NEVER** create circular dependencies
- **NEVER** make tasks too large (should be 1-2 hours max)
- **NEVER** forget to validate the output before execution

## Related Skills

- `/task-batch` - Execute the created task list
- `/clarify` - Used internally for requirement gathering
- `/orchestrator` - Base orchestration workflow
- `/retrospective` - Post-batch analysis


## Action Reporting (v2.93.0)

**Esta skill genera reportes automáticos completos** para trazabilidad:

### Reporte Automático

Cuando esta skill completa, se genera automáticamente:

1. **En la conversación de Claude**: Resultados visibles
2. **En el repositorio**: `docs/actions/create-task-batch/{timestamp}.md`
3. **Metadatos JSON**: `.claude/metadata/actions/create-task-batch/{timestamp}.json`

### Contenido del Reporte

Cada reporte incluye:
- ✅ **Summary**: Descripción de la tarea ejecutada
- ✅ **Execution Details**: Duración, iteraciones, archivos modificados
- ✅ **Results**: Errores encontrados, recomendaciones
- ✅ **Next Steps**: Próximas acciones sugeridas

### Ver Reportes Anteriores

```bash
# Listar todos los reportes de esta skill
ls -lt docs/actions/create-task-batch/

# Ver el reporte más reciente
cat $(ls -t docs/actions/create-task-batch/*.md | head -1)

# Buscar reportes fallidos
grep -l "Status: FAILED" docs/actions/create-task-batch/*.md
```

### Generación Manual (Opcional)

```bash
source .claude/lib/action-report-lib.sh
start_action_report "create-task-batch" "Task description"
# ... ejecución ...
complete_action_report "success" "Summary" "Recommendations"
```

### Referencias del Sistema

- [Action Reports System](docs/actions/README.md) - Documentación completa
- [action-report-lib.sh](.claude/lib/action-report-lib.sh) - Librería helper
- [action-report-generator.sh](.claude/lib/action-report-generator.sh) - Generador

- [Task Decomposition Best Practices](https://agentic-patterns.com/patterns/task-decomposition/)
- [PRD Writing Guide](https://www.atlassian.com/agile/project-management/requirements)
- [Unified Architecture v2.88](docs/architecture/UNIFIED_ARCHITECTURE_v2.88.md)
