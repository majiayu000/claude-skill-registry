---
# VERSION: 2.88.0
name: orchestrator
description: "Full orchestration workflow with swarm mode: evaluate -> clarify -> classify -> persist -> plan mode -> spawn teammates -> execute -> validate -> retrospective. Use when: (1) implementing features, (2) complex refactoring, (3) multi-file changes, (4) tasks requiring coordination. Triggers: /orchestrator, /orch, 'orchestrate', 'full workflow', 'implement feature'."
argument-hint: "<task description>"
user-invocable: true
context: fork
agent: orchestrator
allowed-tools:
  - LSP
  - Task
  - AskUserQuestion
  - EnterPlanMode
  - ExitPlanMode
  - TodoWrite
  - Read
  - Edit
  - Write
  - Bash
  - Glob
  - Grep
  - mcp__plugin_claude-mem_*
hooks:
  PreToolUse:
    - path: .claude/hooks/validate-lsp-servers.sh
      match_tool: LSP
---

# Orchestrator - Multi-Agent Ralph v2.88

**Smart Memory-Driven Orchestration** with swarm mode, parallel memory search, RLM-inspired routing, and quality-first validation.

Based on @PerceptualPeak Smart Forking concept:
> "Why not utilize the knowledge gained from your hundreds/thousands of other Claude code sessions? Don't let that valuable context go to waste!!"

## Quick Start

```bash
# Via skill invocation
/orchestrator Implement OAuth2 authentication with Google

# Via CLI
ralph orch "Migrate database from MySQL to PostgreSQL"

# With specific teammates
/orchestrator "Refactor database layer" --teammates coder,reviewer
```

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: All teammates use the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

## v2.87 Key Changes (UNIFIED SKILLS MODEL)

- **Skills/Commands unification**: All commands now use SKILL.md format
- **Single source of truth**: Skills live in repo, symlinked globally
- **Version alignment**: All skills updated to v2.87.0
- **Documentation consolidated**: Architecture docs in `docs/architecture/`

## v2.81 Key Changes (SWARM MODE)

**Swarm mode is now ENABLED by default** using native Claude Code multi-agent features:

1. **Team Creation**: Orchestrator creates team "orchestration-team" with identity
2. **Teammate Spawning**: ExitPlanMode spawns 3 teammates (code-reviewer, test-architect, security-auditor)
3. **Shared Task List**: All teammates see same tasks via TeammateTool
4. **Inter-Agent Messaging**: Teammates can communicate via mailbox
5. **Plan Approval**: Leader can approve/reject teammate plans

## Core Workflow (10 Steps)

```
0. EVALUATE     -> Quick complexity assessment (trivial vs non-trivial)
1. CLARIFY      -> AskUserQuestion intensively (MUST_HAVE + NICE_TO_HAVE)
2. CLASSIFY     -> Complexity 1-10, model routing
2b. WORKTREE    -> Ask about worktree isolation
3. PLAN         -> Design detailed plan (orchestrator analysis)
3b. PERSIST     -> Write to .claude/orchestrator-analysis.md
4. PLAN MODE    -> EnterPlanMode (reads analysis as foundation)
5. DELEGATE     -> Route to appropriate model/agent
6. EXECUTE      -> Parallel subagents
7. VALIDATE     -> Quality gates + Adversarial
8. RETROSPECT   -> Analyze and improve
```

## Step 0: EVALUATE (3-Dimension Classification)

**Classification (RLM-inspired)**:
| Dimension | Values | Purpose |
|-----------|--------|---------|
| Complexity | 1-10 | Scope, risk, ambiguity |
| Information Density | CONSTANT / LINEAR / QUADRATIC | How answer scales |
| Context Requirement | FITS / CHUNKED / RECURSIVE | Decomposition needs |

**Workflow Routing**:
| Density | Context | Complexity | Route |
|---------|---------|------------|-------|
| CONSTANT | FITS | 1-3 | **FAST_PATH** (3 steps) |
| CONSTANT | FITS | 4-10 | STANDARD |
| LINEAR | CHUNKED | ANY | PARALLEL_CHUNKS |
| QUADRATIC | ANY | ANY | RECURSIVE_DECOMPOSE |

## Step 1: CLARIFY (Memory-Enhanced)

**MUST_HAVE Questions** (Blocking):
```yaml
AskUserQuestion:
  questions:
    - question: "What is the primary goal?"
      header: "Goal"
      options:
        - label: "New feature"
        - label: "Bug fix"
        - label: "Refactoring"
        - label: "Performance"
```

## Step 2: CLASSIFY (Model Routing)

| Score | Complexity | Model | Adversarial |
|-------|------------|-------|-------------|
| 1-2 | Trivial | GLM-4.7 / glm-5 | No |
| 3-4 | Simple | GLM-4.7 / glm-5 | No |
| 5-6 | Medium | Sonnet | Optional |
| 7-8 | Complex | Opus | Yes |
| 9-10 | Critical | Opus (thinking) | Yes |

## Step 3: PLAN + PERSIST

Write plan to `.claude/orchestrator-analysis.md` with:
- Summary (informed by memory)
- Files to modify/create
- Dependencies
- Testing strategy
- Risks (include known issues from memory)

## Step 4: PLAN MODE

```yaml
EnterPlanMode: {}  # Claude Code reads orchestrator-analysis.md
```

Exit with `ExitPlanMode` when approved.

## Step 5: DELEGATE (Parallel-First with Swarm)

**PRIORITY: Parallel execution when possible**

```yaml
# With swarm mode (v2.81+)
Task:
  subagent_type: "orchestrator"
  description: "Full orchestration with swarm"
  prompt: "$ARGUMENTS"
  model: "sonnet"
  team_name: "orchestration-team"
  name: "orchestrator-lead"
  mode: "delegate"

# ExitPlanMode with swarm launch:
ExitPlanMode:
  launchSwarm: true
  teammateCount: 3
```

## Step 6: EXECUTE-WITH-SYNC

Nested loop with parallel substeps:

```
EXTERNAL RALPH LOOP (max 25)
└── For EACH step:
    ├── LSA-VERIFY (architecture check)
    ├── IMPLEMENT (parallel if independent)
    ├── PLAN-SYNC (drift detection)
    └── MICRO-GATE (max 3 retries)
```

**CRITICAL: model: "sonnet" for all subagents**

## Step 7: VALIDATE (Quality-First)

**Stage 1: CORRECTNESS (BLOCKING)**
- Meets requirements?
- Edge cases handled?

**Stage 2: QUALITY (BLOCKING)**
- Security verified? (semgrep + gitleaks)
- Performance OK?
- Tests adequate?

**Stage 3: CONSISTENCY (ADVISORY - not blocking)**
- Follows patterns?
- Style matches?

**Stage 4: ADVERSARIAL (if complexity >= 7)**
```bash
ralph adversarial "Design review"
```

## Step 8: RETROSPECTIVE (Mandatory)

```bash
ralph retrospective
```

**Save learnings to memory**:
```bash
ralph memvid save "Implemented OAuth2 successfully: [pattern details]"
ralph memvid save "AVOID: [error pattern] caused [issue]"
```

-> **VERIFIED_DONE**

## Model Routing

| Route | Primary | Secondary | Max Iter |
|-------|---------|-----------|----------|
| FAST_PATH | sonnet | - | 3 |
| STANDARD (1-4) | glm-5 | sonnet | 25 |
| STANDARD (5-6) | sonnet | opus | 25 |
| STANDARD (7-10) | opus | sonnet | 25 |
| PARALLEL_CHUNKS | sonnet (chunks) | opus (aggregate) | 15/chunk |
| RECURSIVE | opus (root) | sonnet (sub) | 15/sub |

## GLM-5 Teams Integration (--with-glm5)

When `$ARGUMENTS` contains `--with-glm5`:

**Step 1: Parse Arguments**
```
TASK=<everything before --with-glm5>
USE_GLM5=true
```

**Step 2: Spawn GLM-5 Teammates**
```bash
# GLM-5 Coder
.claude/scripts/glm5-teammate.sh "glm5-coder" "$CODER_TASK" "$TASK_ID-coder"

# GLM-5 Reviewer
.claude/scripts/glm5-teammate.sh "glm5-reviewer" "$REVIEW_TASK" "$TASK_ID-reviewer"

# GLM-5 Tester
.claude/scripts/glm5-teammate.sh "glm5-tester" "$TEST_TASK" "$TASK_ID-tester"
```

**Step 3: Wait for Completion**
```bash
cat .ralph/teammates/$TASK_ID-*/status.json
```

**Step 4: Aggregate Results**
- Collect outputs from `.ralph/reasoning/`
- Show thinking process for transparency
- Apply quality gates

## Available Teammates

| Teammate | Role | Best For |
|----------|------|----------|
| `coder` | Implementation | Writing code, fixing bugs |
| `reviewer` | Code Review | Quality checks, security |
| `tester` | Test Generation | Unit tests, coverage |
| `orchestrator` | Coordination | Complex multi-step tasks |

## Anti-Patterns

- Never start without smart memory search
- Never skip clarification
- Never use model: "haiku" for subagents
- Never skip retrospective
- Never attempt more than 3 fixes (3-Fix Rule)
- **Never block on consistency issues** (quality over consistency)
- **Never ignore memory context** (learn from history)

## Completion Criteria

`VERIFIED_DONE` requires ALL:
1. Smart Memory Search complete
2. Task classified (3 dimensions)
3. MUST_HAVE questions answered
4. Plan approved
5. Implementation complete
6. CORRECTNESS passed (blocking)
7. QUALITY passed (blocking)
8. Adversarial passed (if complexity >= 7)
9. Retrospective done + learnings saved to memory

## CLI Commands

```bash
# Standard orchestration
ralph orch "task description"

# With GLM-5 teammates
ralph orch "task description" --with-glm5
ralph orch "complex feature" --with-glm5 --teammates coder,reviewer,tester

# Quality gates
ralph gates
ralph adversarial "spec"

# Memory
ralph memory-search "query"
ralph fork-suggest "Add authentication"
```

## Related Skills

- `/loop` - Iterative execution until VERIFIED_DONE
- `/gates` - Quality validation gates
- `/adversarial` - Spec refinement
- `/parallel` - Parallel subagent execution
- `/retrospective` - Post-task analysis
- `/clarify` - Requirement clarification

## Agent Teams Integration (v2.88)

**Optimal Scenario**: Integrated (Agent Teams + Custom Subagents)

This skill uses the INTEGRATED approach combining Agent Teams coordination with Custom Subagent specialization.

### Why Scenario C for This Skill
- **Multi-phase orchestration** requires tight coordination across evaluate, clarify, plan, execute, validate phases
- **Quality gates (TeammateIdle, TaskCompleted)** are essential for VERIFIED_DONE guarantee
- **Specialized ralph-* agents** for different task types (coder, reviewer, tester, researcher)
- **Shared task list** for progress tracking and dependency management
- **10-step workflow** benefits from both team coordination and agent specialization

### Configuration
1. **TeamCreate**: Create team "orchestration-team-{timestamp}" on skill invocation
2. **TaskCreate**: Create tasks for each orchestration phase (evaluate, clarify, plan, execute, validate)
3. **Spawn**: Use ralph-coder, ralph-reviewer, ralph-tester, ralph-researcher as needed
4. **Hooks**: TeammateIdle + TaskCompleted for VERIFIED_DONE guarantee
5. **Coordination**: Shared task list at ~/.claude/tasks/{team}/

### Workflow Pattern
```
TeamCreate(team_name, description)
  → TaskCreate(evaluate, clarify, classify, persist)
  → TaskCreate(plan-mode tasks)
  → Task(subagent_type="ralph-*", team_name) for execute phase
  → TaskUpdate(status="completed") as phases finish
  → Hooks validate quality at each stage
  → VERIFIED_DONE after retrospective
```

### Ralph Agent Types (v2.88)

| Agent | Role | Tools | Model |
|-------|------|-------|-------|
| `ralph-coder` | Code implementation | Read, Edit, Write, Bash | Inherited from settings.json |
| `ralph-reviewer` | Code review (security, quality) | Read, Grep, Glob | Inherited from settings.json |
| `ralph-tester` | Testing & QA | Read, Edit, Write, Bash(test) | Inherited from settings.json |
| `ralph-researcher` | Research & exploration | Read, Grep, Glob, WebSearch | Inherited from settings.json |

**Note**: All agents inherit their model from `~/.claude/settings.json` via `ANTHROPIC_DEFAULT_*_MODEL` environment variables (v2.88 model-agnostic architecture).

### VERIFIED_DONE Pattern with Hooks

The orchestrator ensures VERIFIED_DONE through these critical hooks:

| Hook | Event | Purpose | Exit 2 Behavior |
|------|-------|---------|-----------------|
| `teammate-idle-quality-gate.sh` | TeammateIdle | Quality check before idle | Keep working + feedback |
| `task-completed-quality-gate.sh` | TaskCompleted | Quality before task completion | Prevent completion + feedback |
| `ralph-subagent-stop.sh` | SubagentStop | Quality gate for ralph-* agents | Block if incomplete |

**Exit 2 Behavior**: When hooks return exit code 2, the agent continues working instead of completing/idling, ensuring continuous execution until VERIFIED_DONE.

### Team Coordination Example

```yaml
# 1. Create team (automatic on skill invocation)
TeamCreate:
  team_name: "orchestration-team-20250214"
  description: "Orchestrating feature implementation"

# 2. Create tasks for teammates
TaskCreate:
  subject: "Implement OAuth2 flow"
  description: "Add OAuth2 authentication with Google provider"
  metadata:
    assigned_to: "ralph-coder"
    priority: "high"

TaskCreate:
  subject: "Review OAuth2 implementation"
  description: "Security and quality review of OAuth2 code"
  metadata:
    assigned_to: "ralph-reviewer"
    depends_on: ["implement-oauth2-flow"]

TaskCreate:
  subject: "Test OAuth2 authentication"
  description: "Unit and integration tests for OAuth2"
  metadata:
    assigned_to: "ralph-tester"
    depends_on: ["implement-oauth2-flow"]

# 3. Spawn teammates for parallel execution
Task:
  subagent_type: "ralph-coder"
  team_name: "orchestration-team-20250214"

Task:
  subagent_type: "ralph-reviewer"
  team_name: "orchestration-team-20250214"

Task:
  subagent_type: "ralph-tester"
  team_name: "orchestration-team-20250214"

# 4. Monitor progress and aggregate results
TaskList:
  status: "in_progress"

# 5. Mark tasks complete
TaskUpdate:
  taskId: "1"
  status: "completed"

# 6. Delete team when VERIFIED_DONE
TeamDelete:
  team_name: "orchestration-team-20250214"
```

### Quality Standards (All Ralph Agents)

1. **CORRECTNESS**: Syntax must be valid, logic must be sound
2. **QUALITY**: No console.log, no TODO/FIXME, proper types
3. **SECURITY**: No hardcoded secrets, proper input validation
4. **CONSISTENCY**: Follow project style guides

### Communication Pattern

Teammates communicate via the shared task list and SendMessage tool:

```yaml
SendMessage:
  type: "message"
  recipient: "ralph-reviewer"
  content: "OAuth2 implementation complete, ready for review"
  summary: "Implementation ready for review"
```

## Action Reporting (v2.93.0)

**El orchestrator genera reportes automáticos completos** para garantiza trazabilidad:

### Reporte Automático

Cuando `/orchestrator` completa, se genera automáticamente:

1. **En la conversación de Claude**: Reporte visible con todos los detalles
2. **En el repositorio**: `docs/actions/orchestrator/{timestamp}.md`
3. **Metadatos JSON**: `.claude/metadata/actions/orchestrator/{timestamp}.json`

### Contenido del Reporte

Cada reporte incluye:
- ✅ **Summary**: Descripción de la tarea ejecutada
- ✅ **Execution Details**: Duración, iteraciones, archivos modificados
- ✅ **Git State**: Branch, commit, archivos cambiados
- ✅ **Errors**: Errores encontrados (si aplicable)
- ✅ **Recommendations**: Próximos pasos sugeridos

### Generación Manual (Opcional)

Si necesitas control manual del reporte:

```bash
# Al inicio
source .claude/lib/action-report-lib.sh
start_action_report "orchestrator" "Implementing OAuth2 with Google"

# Durante ejecución
mark_iteration  # Cada iteración del loop
mark_file_modified "src/auth/oauth.ts"  # Cada archivo modificado
record_error "Type mismatch in config"  # Si hay errores

# Al completar
complete_action_report \
    "success" \
    "OAuth2 implementation completed" \
    "1. Run tests: npm test
     2. Security audit: /security src/
     3. Create PR: gh pr create"
```

### Ver Reportes Anteriores

```bash
# Listar todos los reportes del orchestrator
ls -lt docs/actions/orchestrator/

# Ver el reporte más reciente
cat $(ls -t docs/actions/orchestrator/*.md | head -1)

# Buscar reportes fallidos
grep -l "Status: FAILED" docs/actions/orchestrator/*.md
```

### Estadísticas

```bash
source .claude/lib/action-report-generator.sh
get_skill_stats "orchestrator"

# Output:
# Skill: orchestrator
# Total Reports: 45
# Completed: 42
# Failed: 3
# Success Rate: 93%
```

### Integración con Hooks

El sistema de reportes del orchestrator se integra con:

| Hook | Propósito | Ubicación |
|------|-----------|-----------|
| `action-report-tracker.sh` | Genera reportes automáticos | `.claude/hooks/` |
| `orchestrator-report.sh` | Reportes de sesión | `~/.ralph/reports/` |
| `progress-tracker.sh` | Tracking en tiempo real | `.claude/progress.md` |

**Nota**: Los reportes de acción (`docs/actions/`) son COMPLEMENTARIOS a los reportes de sesión (`~/.ralph/reports/`).

### Referencias del Sistema de Reportes

- [Action Reports System](docs/actions/README.md) - Documentación completa
- [action-report-lib.sh](.claude/lib/action-report-lib.sh) - Librería helper
- [action-report-generator.sh](.claude/lib/action-report-generator.sh) - Generador

### References

- [Unified Architecture v2.87](docs/architecture/UNIFIED_ARCHITECTURE_v2.87.md)
- [Skills/Commands Unification](docs/architecture/SKILLS_COMMANDS_UNIFICATION_v2.87.md)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Claude Code Agent Teams Documentation](https://code.claude.com/docs/en/agent-teams)
