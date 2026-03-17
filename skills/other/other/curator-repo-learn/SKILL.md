---
# VERSION: 2.88.0
name: curator-repo-learn
description: "Learn patterns from a specific GitHub repository. Clones, analyzes code structure, extracts patterns, and populates procedural memory. Use for: targeted learning from known quality repos, quick knowledge acquisition, specific pattern extraction. Triggers: /repo-learn, /curator-repo-learn, 'learn from repo'."
argument-hint: "<github-url> [--domain <domain>]"
user-invocable: true
context: fork
allowed-tools:
  - Task
  - Bash
  - Read
  - Write
---

# Curator Repo-Learn Skill (v2.88)

**Single Repository Pattern Extraction** - Learn from a specific GitHub repository.

## Role & Priorities

**Priorities (ordered):** accuracy → relevance → speed → coverage

**Scope:** Clone repository, analyze structure, extract patterns, update procedural memory.

## Agent Teams Integration (v2.88)

**Optimal Scenario**: B (Custom Subagents)

### Why Scenario B for Repo-Learn

- **Independent operation**: Single repo, single task
- **High specialization need**: Pattern recognition requires expertise
- **Low coordination need**: No multi-stage pipeline
- **Efficient execution**: Direct spawn, no team overhead

### Scenario Analysis

| Criterion | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Coordination Need | 25% | 2/10 | Independent operation |
| Specialization Need | 25% | 9/10 | Requires pattern recognition |
| Quality Gate Need | 20% | 6/10 | Moderate validation needed |
| Tool Restriction Need | 15% | 3/10 | Standard tools sufficient |
| Scalability | 15% | 2/10 | Single repo focus |
| **Total** | 100% | **5.2/10** | Scenario B optimal |

### Workflow (Scenario B)

```yaml
# Direct Subagent Spawn
Task(subagent_type="ralph-researcher", prompt="""
Analyze repository ${REPO_URL}:

1. Clone repository (shallow)
2. Detect domain and language
3. Scan for:
   - Function/method patterns
   - Class/interface definitions
   - Configuration patterns
   - Error handling patterns
   - Testing patterns
4. Extract rules with:
   - domain: <detected>
   - category: <detected>
   - confidence: 0.75-0.95
   - source_repo: ${REPO_URL}
   - source_file: <path>
5. Update ~/.ralph/procedural/rules.json
6. Create manifest with files[] array

Return: patterns extracted, rules added, domain detected
""")
```

## Usage

### Basic Usage

```bash
/repo-learn https://github.com/owner/repo
```

### With Domain Override

```bash
/repo-learn https://github.com/nestjs/nest --domain backend
```

### With Language Hint

```bash
/repo-learn https://github.com/vercel/next.js --lang typescript
```

## Process Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    REPO-LEARN PIPELINE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. VALIDATE URL                                             │
│     ├── Check GitHub format                                  │
│     └── Verify repository exists                             │
│                                                              │
│  2. CLONE REPOSITORY                                         │
│     ├── Shallow clone (--depth 1)                           │
│     └── Store in ~/.ralph/curator/corpus/learning/          │
│                                                              │
│  3. DETECT METADATA                                          │
│     ├── Domain (backend, frontend, etc.)                    │
│     ├── Language (typescript, python, etc.)                 │
│     └── Framework indicators                                  │
│                                                              │
│  4. SCAN FILES                                               │
│     ├── Source files (*.ts, *.py, etc.)                     │
│     ├── Configuration files                                  │
│     └── Documentation files                                  │
│                                                              │
│  5. EXTRACT PATTERNS                                         │
│     ├── Function signatures                                  │
│     ├── Class structures                                     │
│     ├── Import patterns                                      │
│     ├── Error handling patterns                              │
│     └── Configuration patterns                               │
│                                                              │
│  6. CREATE RULES                                             │
│     ├── rule_id: unique identifier                          │
│     ├── domain: detected or specified                       │
│     ├── category: sub-domain                                 │
│     ├── confidence: 0.75-0.95                               │
│     ├── source_repo: repository URL                         │
│     ├── source_file: file path                              │
│     └── behavior: pattern description                       │
│                                                              │
│  7. UPDATE PROCEDURAL MEMORY                                 │
│     ├── Backup existing rules.json                          │
│     ├── Merge new rules (unique_by rule_id)                 │
│     └── Update manifest                                      │
│                                                              │
│  8. CREATE MANIFEST (GAP-C01 FIX)                            │
│     ├── files[]: processed file list                        │
│     ├── patterns_extracted: count                           │
│     ├── detected_domain: domain                             │
│     └── detected_language: language                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Domain Detection (GAP-C02 FIX)

Automatic domain detection from repository content:

```bash
# Domain Keywords
backend:    api, server, rest, graphql, controller, service
frontend:   react, vue, angular, component, hook, state
database:   sql, query, schema, migration, orm, prisma
security:   auth, jwt, token, encrypt, hash, csrf
testing:    test, spec, jest, vitest, mock, coverage
devops:     docker, kubernetes, ci, deploy, pipeline
hooks:      hook, lifecycle, callback, trigger, event
general:    config, util, helper, common, shared
```

## Output Example

```json
{
  "repository": "https://github.com/nestjs/nest",
  "learned_at": "2026-02-14T22:00:00Z",
  "detected_domain": "backend",
  "detected_language": "typescript",
  "files": [
    "packages/core/nest-application.ts",
    "packages/core/nest-factory.ts",
    "packages/common/services/logger.service.ts"
  ],
  "patterns_extracted": 12,
  "rules_added": [
    {
      "rule_id": "rule-backend-1739566800-abc123",
      "domain": "backend",
      "category": "backend",
      "source_repo": "https://github.com/nestjs/nest",
      "source_file": "packages/core/nest-application.ts",
      "behavior": "Classes: class NestApplication. Functions: async initialize, async dispose.",
      "confidence": 0.85
    }
  ]
}
```

## Error Handling

| Error | Recovery |
|-------|----------|
| Invalid URL | Show usage, exit |
| Repository not found | Suggest alternatives, exit |
| Clone failure | Retry with different depth |
| No patterns found | Log warning, return empty |
| Rules merge failure | Restore from backup |

## Integration with Curator Pipeline

```bash
# Quick learning without full pipeline
/curator quick --repo owner/repo

# Full pipeline for comprehensive learning
/curator full --type backend --lang typescript

# Single repo learning (this skill)
/repo-learn https://github.com/owner/repo
```

## Related Skills

- `/curator` - Full pipeline (Scenario C)
- `/smart-fork` - Pattern extraction and forking
- `/research` - Repository research

## Files

| File | Purpose |
|------|---------|
| `.claude/scripts/curator-learn.sh` | Pattern extraction (GAP-C01, GAP-C02 fixed) |
| `.claude/scripts/curator-ingest.sh` | Repository cloning |
| `.claude/scripts/backfill-domains.sh` | Domain backfill for existing rules |
| `~/.ralph/procedural/rules.json` | Procedural memory |


## Action Reporting (v2.93.0)

**Esta skill genera reportes automáticos completos** para trazabilidad:

### Reporte Automático

Cuando esta skill completa, se genera automáticamente:

1. **En la conversación de Claude**: Resultados visibles
2. **En el repositorio**: `docs/actions/curator-repo-learn/{timestamp}.md`
3. **Metadatos JSON**: `.claude/metadata/actions/curator-repo-learn/{timestamp}.json`

### Contenido del Reporte

Cada reporte incluye:
- ✅ **Summary**: Descripción de la tarea ejecutada
- ✅ **Execution Details**: Duración, iteraciones, archivos modificados
- ✅ **Results**: Errores encontrados, recomendaciones
- ✅ **Next Steps**: Próximas acciones sugeridas

### Ver Reportes Anteriores

```bash
# Listar todos los reportes de esta skill
ls -lt docs/actions/curator-repo-learn/

# Ver el reporte más reciente
cat $(ls -t docs/actions/curator-repo-learn/*.md | head -1)

# Buscar reportes fallidos
grep -l "Status: FAILED" docs/actions/curator-repo-learn/*.md
```

### Generación Manual (Opcional)

```bash
source .claude/lib/action-report-lib.sh
start_action_report "curator-repo-learn" "Task description"
# ... ejecución ...
complete_action_report "success" "Summary" "Recommendations"
```

### Referencias del Sistema

- [Action Reports System](docs/actions/README.md) - Documentación completa
- [action-report-lib.sh](.claude/lib/action-report-lib.sh) - Librería helper
- [action-report-generator.sh](.claude/lib/action-report-generator.sh) - Generador

- [Learning System Audit](../../../docs/audits/LEARNING_SYSTEM_AUDIT_v2.88.md)
- [Learning System Scenarios](../../../docs/architecture/LEARNING_SYSTEM_SCENARIOS_v2.88.md)
