---
# VERSION: 2.88.1
name: code-reviewer
description: Automated code review using official Claude Code plugin with 4 parallel agents. Uses LSP for efficient code navigation.
allowed-tools: LSP,Read,Write,Bash,Glob,Grep
hooks:
  PreToolUse:
    - path: .claude/hooks/validate-lsp-servers.sh
      match_tool: LSP
---

# Code Reviewer (Official Plugin)

Integrates the official Claude Code code-review plugin.

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

## Quick Start

```bash
/code-review              # Review current changes
/code-review --comment    # Post review as PR comment
```

## Architecture

4 parallel agents with confidence scoring (≥80):

1. Agent #1: CLAUDE.md compliance
2. Agent #2: CLAUDE.md compliance (redundancy)
3. Agent #3: Bug detection (changes only)
4. Agent #4: Git blame/history analysis

## Features

- Multi-agent parallel review
- Confidence-based filtering
- Auto-skip closed/draft/trivial PRs
- Direct GitHub code links

## Integration

Official plugin: `~/.claude-sneakpeek/zai/config/plugins/cache/anthropics/code-review/`

**Author**: Boris Cherny (boris@anthropic.com)
**Version**: 1.0.0

## Agent Teams Integration (v2.88)

**Optimal Scenario**: Pure Custom Subagents

This skill uses Pure Custom Subagents (no Agent Teams) for focused code review operations.

### Why Scenario B for Code Review
- **Native multi-agent**: Already uses 4 parallel agents via official plugin
- **Read-only operation**: Review should not modify code (tool restrictions critical)
- **No coordination needed**: Analysis is independent per file/PR
- **Faster execution**: Direct spawn avoids team creation overhead

### Configuration
1. **No TeamCreate**: Official plugin already handles parallelism
2. **Direct Task**: Spawn ralph-reviewer for additional analysis if needed
3. **Tool Restrictions**: Review agents restricted to Read/Grep/Glob (no Write/Edit)
4. **Model Inheritance**: Use model configured in settings.json

### Workflow Pattern
```
# Official plugin runs 4 parallel agents natively
/code-review → Plugin spawns 4 agents with confidence scoring

# For extended analysis (optional):
Task(subagent_type="ralph-reviewer", prompt="Deep analysis of specific file...")
  → Agent executes with restricted tools
  → Returns detailed findings
  → Complete
```

### Tool Restrictions for Safety
| Agent | Allowed Tools | Purpose |
|-------|---------------|---------|
| `ralph-reviewer` | Read, Grep, Glob | Analysis only (no modifications) |
| `ralph-researcher` | Read, Grep, Glob | Context lookup only |

### When NOT to Use Agent Teams
- Official plugin already provides parallel review
- Read-only analysis doesn't need team coordination
- Tool restrictions prevent accidental changes more effectively than teams
- When review is a one-shot operation (not multi-phase workflow)


## Action Reporting (v2.93.0)

**Esta skill genera reportes automáticos completos** para trazabilidad:

### Reporte Automático

Cuando esta skill completa, se genera automáticamente:

1. **En la conversación de Claude**: Resultados visibles
2. **En el repositorio**: `docs/actions/code-reviewer/{timestamp}.md`
3. **Metadatos JSON**: `.claude/metadata/actions/code-reviewer/{timestamp}.json`

### Contenido del Reporte

Cada reporte incluye:
- ✅ **Summary**: Descripción de la tarea ejecutada
- ✅ **Execution Details**: Duración, iteraciones, archivos modificados
- ✅ **Results**: Errores encontrados, recomendaciones
- ✅ **Next Steps**: Próximas acciones sugeridas

### Ver Reportes Anteriores

```bash
# Listar todos los reportes de esta skill
ls -lt docs/actions/code-reviewer/

# Ver el reporte más reciente
cat $(ls -t docs/actions/code-reviewer/*.md | head -1)

# Buscar reportes fallidos
grep -l "Status: FAILED" docs/actions/code-reviewer/*.md
```

### Generación Manual (Opcional)

```bash
source .claude/lib/action-report-lib.sh
start_action_report "code-reviewer" "Task description"
# ... ejecución ...
complete_action_report "success" "Summary" "Recommendations"
```

### Referencias del Sistema

- [Action Reports System](docs/actions/README.md) - Documentación completa
- [action-report-lib.sh](.claude/lib/action-report-lib.sh) - Librería helper
- [action-report-generator.sh](.claude/lib/action-report-generator.sh) - Generador
