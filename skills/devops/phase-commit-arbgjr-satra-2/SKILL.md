---
name: phase-commit
description: |
  Gerencia commits automaticos ao final de cada fase do SDLC.
  Garante que artefatos de cada fase sejam commitados e rastreados.
  Use quando: transicao de fase, checkpoint de progresso.
allowed-tools:
  - Bash
  - Read
  - Glob
user-invocable: false
---

# Phase Commit Skill

## Proposito

Esta skill automatiza commits ao final de cada fase do SDLC, garantindo:

1. **Rastreabilidade** - Cada fase tem seu commit identificavel
2. **Checkpoint** - Facilita rollback para estado conhecido
3. **Revisao** - Artefatos separados por fase facilitam code review
4. **Historico** - Git history reflete o progresso do SDLC

## Quando Usar

Esta skill deve ser chamada:

1. Ao **passar um quality gate** com sucesso
2. Ao **finalizar uma fase** manualmente
3. Quando o **orchestrator** detecta transicao de fase

## Formato de Commit

```
<type>(phase-<N>): <descricao curta>

Fase: <nome da fase>
Projeto: <id do projeto>
Artefatos criados:
- <lista de arquivos>

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Tipos por Fase

| Fase | Tipo | Exemplo |
|------|------|---------|
| 0 - Preparation | docs | `docs(phase-0): preparacao e compliance inicial` |
| 1 - Discovery | docs | `docs(phase-1): pesquisa e descoberta de dominio` |
| 2 - Requirements | feat | `feat(phase-2): requisitos e user stories` |
| 3 - Architecture | feat | `feat(phase-3): arquitetura e ADRs` |
| 4 - Planning | docs | `docs(phase-4): planejamento de entrega` |
| 5 - Implementation | feat | `feat(phase-5): implementacao de codigo` |
| 6 - Quality | test | `test(phase-6): testes e validacao de qualidade` |
| 7 - Release | chore | `chore(phase-7): preparacao de release` |
| 8 - Operations | docs | `docs(phase-8): documentacao de operacoes` |

## Processo

```yaml
phase_commit_process:
  1_identify_phase:
    - Ler .claude/memory/project.yml ou .agentic_sdlc/projects/*/manifest.yml
    - Identificar fase atual
    - Identificar projeto

  2_collect_artifacts:
    - Listar arquivos criados/modificados na fase
    - Filtrar por patterns relevantes
    - Agrupar por tipo

  3_stage_files:
    - git add dos arquivos identificados
    - Verificar se ha algo para commitar

  4_create_commit:
    - Gerar mensagem seguindo formato
    - Incluir lista de artefatos
    - Executar commit

  5_update_state:
    - Atualizar timestamp no manifest
    - Registrar commit hash no contexto da fase
    - Notificar usuario
```

## Artefatos por Fase

### Fase 0 - Preparation
```
.agentic_sdlc/intake/**
.agentic_sdlc/projects/*/manifest.yml
.agentic_sdlc/corpus/decisions/compliance-*.yml
```

### Fase 1 - Discovery
```
.agentic_sdlc/corpus/research/**
.agentic_sdlc/corpus/docs/**
.agentic_sdlc/references/**
```

### Fase 2 - Requirements
```
.agentic_sdlc/projects/*/specs/**
.agentic_sdlc/projects/*/requirements/**
*.spec.md
```

### Fase 3 - Architecture
```
.agentic_sdlc/projects/*/decisions/adr-*.yml
.agentic_sdlc/projects/*/security/threat-model*.yml
.agentic_sdlc/corpus/decisions/**
docs/architecture/**
```

### Fase 4 - Planning
```
.agentic_sdlc/projects/*/planning/**
.github/ISSUE_TEMPLATE/**
```

### Fase 5 - Implementation
```
src/**
lib/**
app/**
tests/**
```

### Fase 6 - Quality
```
.agentic_sdlc/projects/*/security/sast-*.yml
.agentic_sdlc/projects/*/security/sca-*.yml
tests/**
```

### Fase 7 - Release
```
CHANGELOG.md
docs/**
.github/workflows/**
```

### Fase 8 - Operations
```
.agentic_sdlc/projects/*/ops/**
docs/runbooks/**
```

## Script de Commit

```bash
#!/bin/bash
# phase-commit.sh
# Commita artefatos da fase atual

set -e

PROJECT_ID="${1:-}"
PHASE="${2:-}"
MESSAGE="${3:-}"

# Obter fase atual se nao especificada
if [ -z "$PHASE" ]; then
  if [ -f ".claude/memory/project.yml" ]; then
    PHASE=$(grep "current_phase:" .claude/memory/project.yml | awk '{print $2}')
  elif [ -f ".agentic_sdlc/projects/${PROJECT_ID}/manifest.yml" ]; then
    PHASE=$(grep "current_phase:" .agentic_sdlc/projects/${PROJECT_ID}/manifest.yml | awk '{print $2}')
  fi
fi

if [ -z "$PHASE" ]; then
  echo "Erro: Nao foi possivel determinar a fase atual"
  exit 1
fi

# Mapear tipo de commit
case $PHASE in
  0|1|4|8) TYPE="docs" ;;
  2|3|5)   TYPE="feat" ;;
  6)       TYPE="test" ;;
  7)       TYPE="chore" ;;
  *)       TYPE="chore" ;;
esac

# Nomes das fases
PHASE_NAMES=(
  "Preparation"
  "Discovery"
  "Requirements"
  "Architecture"
  "Planning"
  "Implementation"
  "Quality"
  "Release"
  "Operations"
)

PHASE_NAME="${PHASE_NAMES[$PHASE]}"

# Verificar se ha mudancas
if git diff --cached --quiet && git diff --quiet; then
  echo "Nenhuma mudanca para commitar na fase ${PHASE} (${PHASE_NAME})"
  exit 0
fi

# Adicionar arquivos nao rastreados
git add -A

# Gerar lista de arquivos
FILES=$(git diff --cached --name-only | head -20)
FILE_COUNT=$(git diff --cached --name-only | wc -l)

# Mensagem de commit
if [ -z "$MESSAGE" ]; then
  MESSAGE="artefatos da fase ${PHASE_NAME}"
fi

# Criar commit
git commit -m "$(cat <<EOF
${TYPE}(phase-${PHASE}): ${MESSAGE}

Fase: ${PHASE_NAME}
Projeto: ${PROJECT_ID}
Arquivos: ${FILE_COUNT}

Artefatos:
${FILES}

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

echo ""
echo "============================================"
echo "  Commit da Fase ${PHASE} Criado"
echo "============================================"
echo "Fase: ${PHASE_NAME}"
echo "Arquivos: ${FILE_COUNT}"
echo ""
```

## Integracao com Orchestrator

O orchestrator deve chamar esta skill:

```yaml
post_gate_actions:
  - condition: gate_passed == true
    action: call_skill("phase-commit")
    params:
      project_id: current_project.id
      phase: current_phase
      message: "completar fase ${phase_name}"
```

## Integracao com Gate Evaluator

Adicionar ao gate-evaluator:

```yaml
on_gate_pass:
  actions:
    - type: suggest_commit
      message: "Fase ${phase} completada. Sugerido commitar artefatos."
    - type: call_skill
      skill: phase-commit
      auto: false  # Pedir confirmacao primeiro
```

## Checklist

### Antes do Commit
- [ ] Verificar se ha arquivos para commitar
- [ ] Confirmar fase atual
- [ ] Revisar lista de artefatos

### Apos o Commit
- [ ] Atualizar manifest com commit hash
- [ ] Notificar usuario
- [ ] Sugerir push se branch remota existe

## Notas

- ✅ Esta skill FAZ COMMIT **E PUSH** automaticamente (v1.7.15+)
- ✅ Push detecta se branch tem upstream e configura automaticamente
- ✅ Logs estruturados com Loki (skill="phase-commit")
- ✅ Atualiza manifest.yml com commit hash e timestamp
- ⚠️ Se push falhar, o commit local é mantido e erro é reportado
- Commits podem ser agrupados se varias fases forem completadas rapidamente
