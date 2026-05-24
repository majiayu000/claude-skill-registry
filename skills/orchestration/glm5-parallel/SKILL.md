---
# VERSION: 2.88.0
name: glm5-parallel
description: Model-agnostic parallel execution with Agent Teams coordination
allowed-tools:
  - Bash
  - Read
  - Write
  - Task
  - TaskCreate
  - TaskList
  - TaskGet
  - TaskUpdate
  - TeamCreate
  - SendMessage
---

# GLM-5 Parallel Skill

Model-agnostic parallel execution with Agent Teams coordination for comprehensive task execution.

> **Note**: Despite the name, this skill is model-agnostic as of v2.88.0. It works with any model configured in Agent Teams.

## Usage

```
/glm5-parallel <task> [--roles coder,reviewer,tester]
```

## Example

```
/glm5-parallel "Implement OAuth2 authentication" --roles coder,reviewer,tester
```

This spawns 3 teammates:
1. **coder** - Implements OAuth2
2. **reviewer** - Reviews the implementation
3. **tester** - Generates tests

## Execution Pattern

```bash
# Generate task ID
TASK_ID="parallel-$(date +%s)"

# Parse roles
ROLES="coder,reviewer,tester"

# Spawn in parallel
for ROLE in $(echo $ROLES | tr ',' ' '); do
    .claude/scripts/glm5-teammate.sh "$ROLE" "<task>" "${TASK_ID}-${ROLE}" &
done

# Wait for all
wait

# Aggregate results
for ROLE in $(echo $ROLES | tr ',' ' '); do
    echo "=== $ROLE ==="
    cat .ralph/teammates/${TASK_ID}-${ROLE}/status.json | jq '.output_summary'
done
```

## Default Roles

If no `--roles` specified:
- `coder` - Implementation
- `reviewer` - Code review
- `tester` - Test generation

## Output

Creates parallel status files:
- `.ralph/teammates/{task_id}-coder/status.json`
- `.ralph/teammates/{task_id}-reviewer/status.json`
- `.ralph/teammates/{task_id}-tester/status.json`

Aggregated in `.ralph/team-status.json`

## Agent Teams Integration (v2.88)

**Optimal Scenario**: Pure Agent Teams (Native)

This skill uses Pure Agent Teams with native coordination - no custom subagent specialization needed.

### Why Scenario A for This Skill
- Parallel execution is a core Agent Teams capability
- Standard Task tool supports native parallel execution
- No specialized subagent configuration required
- Native agent types provide all needed tools (Read, Edit, Write, Bash)
- Lower complexity, faster setup

### Configuration
1. **TeamCreate**: Recommended for parallel execution coordination
2. **Task**: Use native agent types with parallel execution
3. **Hooks**: TeammateIdle + TaskCompleted for quality gates
4. **Simple**: Leverage built-in Agent Teams parallelism

### Workflow Pattern
```
TeamCreate
  → Task(prompt, subagent_type) for each parallel workstream
  → Native agents execute in parallel
  → Aggregate results
  → Complete
```

### Parallel Execution Pattern

```javascript
// Create team for coordination
TeamCreate(team_name="parallel-{timestamp}", description="Parallel execution for: {task}")

// Spawn native agents in parallel
const workstreams = [
  { task: "Implement feature X", files: ["src/a.ts"] },
  { task: "Implement feature Y", files: ["src/b.ts"] },
  { task: "Write tests", files: ["tests/*.test.ts"] }
];

workstreams.forEach(work => {
  Task(
    subagent_type="coder",  // Native agent type
    team_name="parallel-{timestamp}",
    input=work
  );
});
```

### When This Is Sufficient
- Parallel code execution across files
- Standard implementation tasks
- No specialized tool restrictions needed
- Leverage native Agent Teams parallelism


## Action Reporting (v2.93.0)

**Esta skill genera reportes automáticos completos** para trazabilidad:

### Reporte Automático

Cuando esta skill completa, se genera automáticamente:

1. **En la conversación de Claude**: Resultados visibles
2. **En el repositorio**: `docs/actions/glm5-parallel/{timestamp}.md`
3. **Metadatos JSON**: `.claude/metadata/actions/glm5-parallel/{timestamp}.json`

### Contenido del Reporte

Cada reporte incluye:
- ✅ **Summary**: Descripción de la tarea ejecutada
- ✅ **Execution Details**: Duración, iteraciones, archivos modificados
- ✅ **Results**: Errores encontrados, recomendaciones
- ✅ **Next Steps**: Próximas acciones sugeridas

### Ver Reportes Anteriores

```bash
# Listar todos los reportes de esta skill
ls -lt docs/actions/glm5-parallel/

# Ver el reporte más reciente
cat $(ls -t docs/actions/glm5-parallel/*.md | head -1)

# Buscar reportes fallidos
grep -l "Status: FAILED" docs/actions/glm5-parallel/*.md
```

### Generación Manual (Opcional)

```bash
source .claude/lib/action-report-lib.sh
start_action_report "glm5-parallel" "Task description"
# ... ejecución ...
complete_action_report "success" "Summary" "Recommendations"
```

### Referencias del Sistema

- [Action Reports System](docs/actions/README.md) - Documentación completa
- [action-report-lib.sh](.claude/lib/action-report-lib.sh) - Librería helper
- [action-report-generator.sh](.claude/lib/action-report-generator.sh) - Generador
