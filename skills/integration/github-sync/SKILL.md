---
name: github-sync
description: |
  Skill base para sincronizacao com GitHub.
  Gerencia issues, labels e milestones de forma automatica.
  Use quando: criar issues, sincronizar milestones, gerenciar labels SDLC.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
user-invocable: false
version: "1.0.0"
---

# GitHub Sync Skill

Skill base que fornece utilitarios para sincronizacao com GitHub Issues, Labels e Milestones.

## Objetivo

Prover uma camada de abstracao sobre a API do GitHub para que outros agentes e skills
possam gerenciar issues, labels e milestones de forma consistente e automatizada.

## Scripts Disponiveis

### label_manager.py

Gerencia labels SDLC no repositorio.

```bash
# Criar todos os labels SDLC se nao existem
python3 .claude/skills/github-sync/scripts/label_manager.py ensure

# Listar labels existentes
python3 .claude/skills/github-sync/scripts/label_manager.py list

# Verificar se labels SDLC existem
python3 .claude/skills/github-sync/scripts/label_manager.py check
```

**Labels criados:**
- `phase:0` a `phase:8` - fase atual do SDLC
- `complexity:0` a `complexity:3` - nivel de complexidade
- `type:story`, `type:task`, `type:epic` - tipo de item
- `sdlc:auto` - criado automaticamente pelo SDLC

### milestone_sync.py

Gerencia milestones (sprints) no repositorio.

```bash
# Criar milestone
python3 .claude/skills/github-sync/scripts/milestone_sync.py create \
  --title "Sprint 1" \
  --description "Sprint goal" \
  --due-date "2026-01-28"

# Fechar milestone
python3 .claude/skills/github-sync/scripts/milestone_sync.py close --title "Sprint 1"

# Listar milestones
python3 .claude/skills/github-sync/scripts/milestone_sync.py list

# Obter milestone por titulo
python3 .claude/skills/github-sync/scripts/milestone_sync.py get --title "Sprint 1"
```

### issue_sync.py

Gerencia issues com integracao SDLC.

```bash
# Criar issue com labels SDLC
python3 .claude/skills/github-sync/scripts/issue_sync.py create \
  --title "[TASK-001] Implementar feature X" \
  --body-file task.md \
  --phase 5 \
  --type task \
  --milestone "Sprint 1"

# Atualizar issue
python3 .claude/skills/github-sync/scripts/issue_sync.py update \
  --number 123 \
  --phase 6 \
  --state open

# Sincronizar task YAML para issue
python3 .claude/skills/github-sync/scripts/issue_sync.py sync-task \
  --task-path .agentic_sdlc/projects/xxx/tasks/task-001.yml

# Buscar issue por titulo
python3 .claude/skills/github-sync/scripts/issue_sync.py find --title "[TASK-001]"
```

## Mapeamento SDLC <-> GitHub

| SDLC Agentico | GitHub |
|---------------|--------|
| Sprint | Milestone |
| Sprint goal | Milestone description |
| Sprint end date | Milestone due_on |
| Task | Issue |
| Story | Issue (type:story) |
| Epic | Issue (type:epic) |
| Phase | Label (phase:N) |
| Complexity | Label (complexity:N) |

## Labels por Cor

| Label | Cor | Descricao |
|-------|-----|-----------|
| `phase:0` | #0E8A16 | Preparation |
| `phase:1` | #1D76DB | Discovery |
| `phase:2` | #5319E7 | Requirements |
| `phase:3` | #FBCA04 | Architecture |
| `phase:4` | #F9D0C4 | Planning |
| `phase:5` | #C5DEF5 | Implementation |
| `phase:6` | #BFD4F2 | Quality |
| `phase:7` | #D4C5F9 | Release |
| `phase:8` | #0052CC | Operations |
| `complexity:0` | #C2E0C6 | Quick Flow |
| `complexity:1` | #FEF2C0 | Feature |
| `complexity:2` | #F9D0C4 | BMAD Method |
| `complexity:3` | #E99695 | Enterprise |
| `type:story` | #D93F0B | User Story |
| `type:task` | #0075CA | Task |
| `type:epic` | #7057FF | Epic |
| `sdlc:auto` | #EDEDED | Auto-generated |

## Integracao com Outros Skills

Esta skill e usada por:
- `github-projects` - Para criar issues e adicionar ao project
- `orchestrator` - Para sincronizar estado do SDLC com GitHub
- `delivery-planner` - Para criar milestones de sprints

## Pre-requisitos

- GitHub CLI (`gh`) instalado e autenticado
- Permissoes de escrita no repositorio
- Scope `project` para integracao com Projects V2

```bash
# Verificar autenticacao
gh auth status

# Adicionar scope project se necessario
gh auth refresh -s project
```

## Exemplos de Uso

### Preparar repositorio para SDLC

```bash
# 1. Criar labels
python3 .claude/skills/github-sync/scripts/label_manager.py ensure

# 2. Criar primeiro milestone
python3 .claude/skills/github-sync/scripts/milestone_sync.py create \
  --title "Sprint 1" \
  --description "Inicio do projeto" \
  --due-date "$(date -d '+14 days' +%Y-%m-%d)"
```

### Criar issue para task

```bash
python3 .claude/skills/github-sync/scripts/issue_sync.py create \
  --title "[TASK-001] Implementar autenticacao" \
  --body "## Descricao\n\nImplementar sistema de autenticacao OAuth2.\n\n## Acceptance Criteria\n\n- [ ] Login funcional\n- [ ] Logout funcional" \
  --phase 5 \
  --type task \
  --milestone "Sprint 1"
```

### Transicao de fase

```bash
# Atualizar issue para nova fase
python3 .claude/skills/github-sync/scripts/issue_sync.py update \
  --number 123 \
  --phase 6
```
