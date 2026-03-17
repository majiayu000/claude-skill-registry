---
# VERSION: 2.88.0
name: loop
description: "Ralph Loop pattern with swarm mode: iterative execution until VERIFIED_DONE with multi-agent coordination. Use when: (1) iterative refinement needed, (2) quality gates must pass, (3) automated validation required. Triggers: /loop, 'loop until done', 'iterate', 'keep trying', 'fix until passing'."
argument-hint: "<task>"
user-invocable: true
context: fork
agent: general-purpose
allowed-tools:
  - LSP
  - Task
  - Read
  - Edit
  - Write
  - Bash
  - Glob
  - Grep
hooks:
  PreToolUse:
    - path: .claude/hooks/validate-lsp-servers.sh
      match_tool: LSP
---

# /loop - Ralph Loop Pattern (v2.88)

Execute tasks iteratively with automatic quality validation until VERIFIED_DONE signal.

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Iterations use the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

## v2.87 Key Changes (UNIFIED SKILLS MODEL)

- **Skills/Commands unification**: All commands now use SKILL.md format
- **Single source of truth**: Skills live in repo, symlinked globally
- **Version alignment**: All skills updated to v2.87.0
- **Documentation consolidated**: Architecture docs in `docs/architecture/`

## Overview

The Ralph Loop is a **continuous execution pattern** that iterates through EXECUTE -> VALIDATE -> QUALITY CHECK cycles until the task passes all quality gates or reaches the iteration limit.

```
+------------------------------------------------------------------+
|                    RALPH LOOP PATTERN                             |
+------------------------------------------------------------------+
|                                                                   |
|   +----------+    +--------------+    +-----------------+         |
|   | EXECUTE  |--->|   VALIDATE   |--->| Quality Passed? |         |
|   |   Task   |    | (hooks/gates)|    +--------+--------+         |
|   +----------+    +--------------+             |                  |
|                                          NO <--+--> YES           |
|                                           |         |             |
|                          +----------------+         |             |
|                          v                          v             |
|                   +------------+          +---------------+       |
|                   |  ITERATE   |          | VERIFIED_DONE |       |
|                   | (max 15/30)|          |   (output)    |       |
|                   +-----+------+          +---------------+       |
|                         |                                         |
|                         +----------> Back to EXECUTE              |
|                                                                   |
+------------------------------------------------------------------+
```

## When to Use

Use `/loop` when:
1. **Iterative refinement needed** - Code requires multiple passes to meet quality standards
2. **Quality gates must pass** - TypeScript, ESLint, tests, linting must all pass
3. **Automated validation** - Let the loop handle retries automatically
4. **Complex implementations** - Multi-file changes that need coordination
5. **Research tasks** - Gathering information until complete

**DO NOT use** for:
- Simple one-shot tasks (use direct claude call)
- Tasks already in orchestration flow (redundant)
- Spec refinement workflows (use /adversarial)

## Iteration Limits

| Model | Max Iterations | Cost vs Claude | Quality | Use Case |
|-------|----------------|----------------|---------|----------|
| Claude (Sonnet/Opus) | **15** | 100% (baseline) | 85-90% SWE-bench | Complex reasoning, high accuracy |
| GLM-5 | **30** | ~10% | 80%+ SWE-bench | Standard tasks (2x multiplier) |
| MiniMax M2.1 | **30** | ~8% | 74% SWE-bench | Standard tasks (2x multiplier) |

## Model Selection

### Default Mode (Claude)

```bash
ralph loop "implement OAuth2 authentication"
```

Uses Claude Sonnet with **15 iteration limit**:
- Best for: Complex features, security-critical code, architectural changes
- Cost: Standard Claude pricing
- Quality: 85%+ SWE-bench accuracy

### GLM-5 Mode (--with-glm5 flag)

```bash
ralph loop "implement OAuth2 authentication" --with-glm5
```

Uses GLM-5 with **30 iteration limit**:
- Best for: Standard features, refactoring, testing, documentation
- Cost: ~10% of Claude cost
- Quality: 80%+ SWE-bench accuracy

### MiniMax Mode (--mmc flag)

```bash
ralph loop --mmc "implement OAuth2 authentication"
```

Uses MiniMax M2.1 with **30 iteration limit**:
- Best for: Non-critical features, exploratory research
- Cost: ~8% of Claude cost
- Quality: 74% SWE-bench accuracy

## CLI Execution

```bash
# Claude mode (15 iterations)
ralph loop "implement user authentication with JWT"

# GLM-5 mode (30 iterations)
ralph loop "refactor database queries" --with-glm5

# MiniMax mode (30 iterations)
ralph loop --mmc "refactor database queries to use TypeORM"

# Complex task with specific requirements
ralph loop "add rate limiting to API endpoints with Redis"
```

## Task Tool Invocation (Swarm Mode)

**IMPORTANT**: /loop uses swarm mode by default with full multi-agent coordination.

```yaml
Task:
  subagent_type: "general-purpose"
  model: "sonnet"
  run_in_background: true
  max_iterations: 15
  description: "Loop execution with swarm mode"
  team_name: "loop-execution-team"
  name: "loop-lead"
  mode: "delegate"
  prompt: |
    Execute the following task iteratively until VERIFIED_DONE:

    Task: $ARGUMENTS

    Ralph Loop pattern:
    1. EXECUTE - Implement the task
    2. VALIDATE - Run quality gates (tsc, eslint, tests)
    3. CHECK - Did all gates pass?
       - YES -> VERIFIED_DONE
       - NO -> ITERATE (max 15)

    Output: Final implementation + quality report
```

## Agent Teams Integration (v2.88)

**Optimal Scenario**: Integrated (Agent Teams + Custom Subagents)

This skill uses the INTEGRATED approach combining Agent Teams coordination with Custom Subagent specialization.

### Why Scenario C for This Skill
- **Iterative execution** requires tight coordination between implementation and validation phases
- **Quality gates (TeammateIdle, TaskCompleted)** are essential for VERIFIED_DONE guarantee on each iteration
- **Specialized ralph-coder agents** for implementation, ralph-tester for validation
- **Shared task list** tracks iteration progress and blockers
- **Multi-phase iteration** (EXECUTE -> VALIDATE -> CHECK) benefits from team coordination

### Configuration
1. **TeamCreate**: Create team "loop-{task-hash}" on loop invocation
2. **TaskCreate**: Create iteration tasks for each loop cycle
3. **Spawn**: Use ralph-coder for implementation, ralph-tester for validation
4. **Hooks**: TeammateIdle + TaskCompleted for quality validation on each iteration
5. **Coordination**: Shared task list at ~/.claude/tasks/{team}/

### Workflow Pattern
```
TeamCreate(team_name, description)
  → TaskCreate(iteration_n, "Implement iteration {n}")
  → Task(subagent_type="ralph-coder", team_name) for implementation
  → Task(subagent_type="ralph-tester", team_name) for validation
  → TaskUpdate(status="completed") when iteration passes gates
  → Hooks validate quality before marking complete
  → VERIFIED_DONE when all iterations pass
```

### Team Creation Pattern

When `/loop` is invoked, it automatically creates a dedicated team for the iteration:

```bash
# Automatic team creation
TeamCreate(
  team_name: "loop-{task-hash}",
  description: "Iterative execution: {task}"
)

# Spawn implementation teammate
Task(
  subagent_type: "ralph-coder",
  team_name: "loop-{task-hash}"
)

# Spawn validation teammate
Task(
  subagent_type: "ralph-tester",
  team_name: "loop-{task-hash}"
)
```

### Iteration Execution Flow

Each iteration follows this pattern:

1. **Phase 1: Implementation**
   - Spawn `ralph-coder` teammate
   - Execute task implementation
   - Teammate reports progress via TaskUpdate

2. **Phase 2: Validation**
   - Spawn `ralph-tester` teammate
   - Run quality gates
   - Collect validation results

3. **Phase 3: Hook Verification**
   - `TeammateIdle` hook triggers quality checks
   - `task-completed-quality-gate.sh` validates before completion
   - Exit 2 from hook = keep working with feedback
   - Exit 0 = proceed to next phase

4. **Phase 4: Decision**
   - All gates pass → `VERIFIED_DONE`
   - Any gate fails → Iterate (max 15/30)

### Hook Integration Points

| Hook | Trigger | Purpose |
|------|---------|---------|
| `teammate-idle-quality-gate.sh` | TeammateIdle | Quality checks before idle |
| `task-completed-quality-gate.sh` | TaskCompleted | Final validation before completion |
| `ralph-subagent-start.sh` | SubagentStart | Load Ralph context into teammates |
| `glm5-subagent-stop.sh` | SubagentStop | Quality gates when teammate stops |

### Team Composition

When /loop is invoked, it automatically spawns:

| Role | Purpose | Count |
|------|---------|-------|
| **Leader** | Loop coordinator, iteration management | 1 |
| **ralph-coder** | Implementation specialist | 1 |
| **ralph-tester** | Quality validation specialist | 1 |

**Total**: 3 agents working in parallel (1 leader + 2 teammates)

### Task Coordination

```bash
# Leader creates iteration task
TaskCreate(
  subject: "Implement iteration {n}",
  description: "{task requirements}",
  activeForm: "Implementing iteration {n}"
)

# Assign to coder
TaskUpdate(
  taskId: "{id}",
  owner: "ralph-coder",
  status: "in_progress"
)

# Coder completes work
TaskUpdate(
  taskId: "{id}",
  status: "completed"
)

# Leader validates, then marks VERIFIED_DONE or iterates
```

### VERIFIED_DONE Guarantee

The Agent Teams system ensures VERIFIED_DONE through:

1. **TeammateIdle Hook**: Validates work quality before any teammate goes idle
2. **TaskCompleted Hook**: Final validation gate before task completion
3. **Exit 2 Feedback**: Hooks return exit 2 to request fixes with specific feedback
4. **Task Coordination**: TaskUpdate system tracks progress and blockers

This creates a quality feedback loop that prevents completion until all standards are met.

## Output Location

```bash
# Logs saved to ~/.ralph/logs/
ls ~/.ralph/logs/loop-*.log

# View last loop execution
tail -f ~/.ralph/logs/loop-latest.log
```

## Pattern Details

### Loop Structure

```bash
iteration=0
max_iterations=15  # or 30 for GLM-5/MiniMax

while [[ $iteration -lt $max_iterations ]]; do
    # Step 1: EXECUTE
    implement_task

    # Step 2: VALIDATE
    run_quality_gates  # tsc, eslint, tests, semgrep

    # Step 3: CHECK
    if all_gates_passed; then
        echo "VERIFIED_DONE"
        exit 0
    fi

    # Step 4: ITERATE
    ((iteration++))
    analyze_failures
    apply_fixes
done

# Max iterations reached without VERIFIED_DONE
exit 1
```

### Quality Gates Integration

Each iteration runs quality gates:

1. **TypeScript**: `tsc --noEmit`
2. **ESLint**: `eslint .`
3. **Tests**: `npm test` or `pytest`
4. **Security**: `semgrep --config=auto`
5. **Custom**: Project-specific gates

### Stop Hook Integration

The loop integrates with the Stop hook:

```bash
# Initialize state
.claude/scripts/ralph-state.sh init "$SESSION_ID" loop "$TASK"

# On VERIFIED_DONE
.claude/scripts/ralph-state.sh complete "$SESSION_ID" loop

# On failure
.claude/scripts/ralph-state.sh fail "$SESSION_ID" loop "$ERROR"
```

## Anti-Patterns

- Never use infinite loops (always set max_iterations)
- Never skip quality gates (defeats the purpose)
- Never use for one-shot tasks (use direct execution)
- Never nest loops (causes exponential iterations)

## Completion Criteria

`VERIFIED_DONE` requires ALL:
1. All quality gates passed
2. No TypeScript errors
3. No ESLint errors
4. Tests passing
5. Security scan clean (no P0/P1 findings)

## Related Skills

- `/orchestrator` - Full orchestration workflow
- `/gates` - Quality validation gates
- `/adversarial` - Spec refinement
- `/parallel` - Parallel subagent execution
- `/retrospective` - Post-task analysis


## Action Reporting (v2.93.0)

**Esta skill genera reportes automáticos completos** para trazabilidad:

### Reporte Automático

Cuando esta skill completa, se genera automáticamente:

1. **En la conversación de Claude**: Resultados visibles
2. **En el repositorio**: `docs/actions/loop/{timestamp}.md`
3. **Metadatos JSON**: `.claude/metadata/actions/loop/{timestamp}.json`

### Contenido del Reporte

Cada reporte incluye:
- ✅ **Summary**: Descripción de la tarea ejecutada
- ✅ **Execution Details**: Duración, iteraciones, archivos modificados
- ✅ **Results**: Errores encontrados, recomendaciones
- ✅ **Next Steps**: Próximas acciones sugeridas

### Ver Reportes Anteriores

```bash
# Listar todos los reportes de esta skill
ls -lt docs/actions/loop/

# Ver el reporte más reciente
cat $(ls -t docs/actions/loop/*.md | head -1)

# Buscar reportes fallidos
grep -l "Status: FAILED" docs/actions/loop/*.md
```

### Generación Manual (Opcional)

```bash
source .claude/lib/action-report-lib.sh
start_action_report "loop" "Task description"
# ... ejecución ...
complete_action_report "success" "Summary" "Recommendations"
```

### Referencias del Sistema

- [Action Reports System](docs/actions/README.md) - Documentación completa
- [action-report-lib.sh](.claude/lib/action-report-lib.sh) - Librería helper
- [action-report-generator.sh](.claude/lib/action-report-generator.sh) - Generador

- [Unified Architecture v2.88](docs/architecture/UNIFIED_ARCHITECTURE_v2.88.md)
- [Skills/Commands Unification](docs/architecture/COMMANDS_TO_SKILLS_MIGRATION_v2.88.md)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
