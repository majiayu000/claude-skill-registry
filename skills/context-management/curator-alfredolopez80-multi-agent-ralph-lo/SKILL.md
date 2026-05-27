---
# VERSION: 2.88.0
name: curator
description: "Full curator pipeline for autonomous learning from quality repositories. Executes: discovery → scoring → ranking → ingest → learn → inject. Use for: populating procedural memory with domain patterns, first-time domain learning, comprehensive knowledge building. Triggers: /curator full, 'learn patterns from repos', 'build knowledge base'."
argument-hint: "[full|quick|status] --type <domain> --lang <language>"
user-invocable: true
context: fork
allowed-tools:
  - Task
  - Bash
  - Read
  - Write
  - WebSearch
  - WebFetch
---

# Curator Pipeline Skill (v2.88)

**Full Autonomous Learning Pipeline** - Discovers, scores, and learns from quality repositories.

## Role & Priorities

**Priorities (ordered):** quality → coverage → relevance → performance → speed

**Scope:** Repository discovery, quality scoring, pattern extraction, procedural memory population.

## Agent Teams Integration (v2.88)

**Optimal Scenario**: C (Integrated)

### Why Scenario C for Curator

- **High coordination need**: 5+ sequential pipeline stages
- **Quality gates required**: Each stage needs validation before proceeding
- **Multi-tool operations**: GitHub API, git, file processing, JSON manipulation
- **Scalability**: Can process multiple repositories in parallel

### Scenario Analysis

| Criterion | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Coordination Need | 25% | 8/10 | Multi-stage pipeline requires orchestration |
| Specialization Need | 25% | 5/10 | General API/git skills sufficient |
| Quality Gate Need | 20% | 9/10 | Each stage needs validation |
| Tool Restriction Need | 15% | 3/10 | Needs broad tool access |
| Scalability | 15% | 8/10 | Can process many repos |
| **Total** | 100% | **6.9/10** | Scenario C optimal |

### Workflow (Scenario C)

```yaml
# Integrated Team Workflow
TeamCreate(team_name="curator-pipeline", description="Learning from ${DOMAIN} repos")

# Stage 1: Discovery
Task(subagent_type="ralph-researcher", prompt="Search GitHub for ${DOMAIN} repositories")
→ Returns candidate list

# Stage 2: Scoring (parallel)
Task(subagent_type="ralph-reviewer", prompt="Score ${REPO_1} quality")
Task(subagent_type="ralph-reviewer", prompt="Score ${REPO_2} quality")
→ Returns quality scores

# Stage 3: Ranking
Team lead aggregates scores and selects top N

# Stage 4: Ingest & Learn (parallel)
Task(subagent_type="ralph-coder", prompt="Clone and extract patterns from ${TOP_REPO}")
→ Returns extracted patterns

# Stage 5: Quality Gate
TeammateIdle hook validates pattern quality
TaskCompleted hook verifies manifest population

# Stage 6: Injection
Procedural memory updated automatically
```

## Pipeline Stages

### 1. Discovery (`curator-discovery.sh`)

```bash
# Search GitHub for repositories
--type <domain>    # backend, frontend, database, security, devops, testing
--lang <language>  # typescript, python, go, rust, java
--tier <tier>      # premium (1000+ stars), standard (500+), economic (100+)
```

**Output**: Candidate repository list with metadata.

### 2. Scoring (`curator-scoring.sh`)

Quality metrics:
- Star count and trend
- Recent commit activity
- Documentation quality
- Test coverage indicators
- Organization reputation

**Output**: Scored repository list (0-100).

### 3. Ranking (`curator-rank.sh`)

```bash
# Select top repositories
--max <n>         # Maximum repos to process (default: 3)
--diversity       # Ensure organization diversity
```

**Output**: Ranked candidate list.

### 4. Ingest (`curator-ingest.sh`)

```bash
# Clone and prepare repositories
--clone-depth 1   # Shallow clone for efficiency
```

**Output**: Cloned repositories in corpus/pending/.

### 5. Approve (`curator-approve.sh`)

```bash
# Manual or automatic approval
--auto            # Auto-approve based on score threshold
--threshold 75    # Minimum score for auto-approval
```

**Output**: Repositories moved to corpus/approved/.

### 6. Learn (`curator-learn.sh`) - **GAP FIXES v2.88**

```bash
# Extract patterns and populate procedural memory
# GAP-C01 FIX: Manifest files[] now populated
# GAP-C02 FIX: Domain detection and assignment
```

**Output**:
- Updated `~/.ralph/procedural/rules.json`
- Manifest with `files[]` array
- Domain-categorized rules

## Commands

### Full Pipeline

```bash
/curator full --type backend --lang typescript
```

Executes all stages: discovery → scoring → ranking → ingest → approve → learn.

### Quick Pipeline

```bash
/curator quick --type security --lang python --repo owner/repo
```

Skips discovery, learns from specific repository.

### Status Check

```bash
/curator status
```

Shows:
- Approved repositories count
- Rules per domain
- Learning gaps

## Configuration

```json
// ~/.ralph/config/memory-config.json
{
  "curator": {
    "max_repos_per_run": 3,
    "min_stars": 100,
    "clone_depth": 1,
    "auto_approve_threshold": 75,
    "domains": ["backend", "frontend", "database", "security", "devops", "testing"]
  },
  "auto_learn": {
    "enabled": true,
    "blocking": false,
    "min_rules_domain": 3
  }
}
```

## Quality Gates (v2.88)

| Stage | Gate | Failure Action |
|-------|------|----------------|
| Discovery | Results > 0 | Retry with broader search |
| Scoring | Top score >= 60 | Lower threshold or expand search |
| Ingest | Clone success | Skip repo, continue |
| Learn | Patterns > 0 | Log warning, proceed |

## GAP Fixes Applied (v2.88)

### GAP-C01: Manifest Files[] Population

Before:
```json
{"files": [], "patterns_extracted": 0}
```

After:
```json
{
  "files": ["src/handler.ts", "src/middleware.ts"],
  "patterns_extracted": 5,
  "detected_domain": "backend",
  "detected_language": "typescript"
}
```

### GAP-C02: Domain Detection

Rules now automatically categorized:
- Keyword analysis of repository content
- File extension detection
- Configuration file inspection

## Related Skills

- `/curator-repo-learn` - Single repository learning (Scenario B)
- `/repo-learn` - Alias for curator-repo-learn
- `/smart-fork` - Pattern extraction from external repos

## Hooks Integration

| Hook | Trigger | Purpose |
|------|---------|---------|
| `orchestrator-auto-learn.sh` | PreToolUse (Task) | Detect learning gaps |
| `curator-suggestion.sh` | UserPromptSubmit | Suggest learning |
| `continuous-learning.sh` | SessionEnd | Extract from session |


## Action Reporting (v2.93.0)

**Esta skill genera reportes automáticos completos** para trazabilidad:

### Reporte Automático

Cuando esta skill completa, se genera automáticamente:

1. **En la conversación de Claude**: Resultados visibles
2. **En el repositorio**: `docs/actions/curator/{timestamp}.md`
3. **Metadatos JSON**: `.claude/metadata/actions/curator/{timestamp}.json`

### Contenido del Reporte

Cada reporte incluye:
- ✅ **Summary**: Descripción de la tarea ejecutada
- ✅ **Execution Details**: Duración, iteraciones, archivos modificados
- ✅ **Results**: Errores encontrados, recomendaciones
- ✅ **Next Steps**: Próximas acciones sugeridas

### Ver Reportes Anteriores

```bash
# Listar todos los reportes de esta skill
ls -lt docs/actions/curator/

# Ver el reporte más reciente
cat $(ls -t docs/actions/curator/*.md | head -1)

# Buscar reportes fallidos
grep -l "Status: FAILED" docs/actions/curator/*.md
```

### Generación Manual (Opcional)

```bash
source .claude/lib/action-report-lib.sh
start_action_report "curator" "Task description"
# ... ejecución ...
complete_action_report "success" "Summary" "Recommendations"
```

### Referencias del Sistema

- [Action Reports System](docs/actions/README.md) - Documentación completa
- [action-report-lib.sh](.claude/lib/action-report-lib.sh) - Librería helper
- [action-report-generator.sh](.claude/lib/action-report-generator.sh) - Generador

- [Learning System Audit](../../../docs/audits/LEARNING_SYSTEM_AUDIT_v2.88.md)
- [Learning System Scenarios](../../../docs/architecture/LEARNING_SYSTEM_SCENARIOS_v2.88.md)
- [MULTI_AGENT_SCENARIOS_v2.88](../../../docs/architecture/MULTI_AGENT_SCENARIOS_v2.88.md)
