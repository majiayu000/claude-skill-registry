---
name: github-projects
description: |
  Gerencia GitHub Projects V2 via GraphQL API.
  Cria projects, configura campos customizados e views.
  Use quando: iniciar projeto SDLC, mover issues entre fases.
allowed-tools:
  - Read
  - Write
  - Bash
user-invocable: false
version: "1.0.0"
---

# GitHub Projects Skill

Skill para gerenciamento de GitHub Projects V2 usando GraphQL API.

## Objetivo

Automatizar criacao e gerenciamento de GitHub Projects V2 para projetos SDLC,
incluindo configuracao de campos customizados, views e sincronizacao de issues.

## Pre-requisitos

- GitHub CLI (`gh`) instalado e autenticado
- Scope `project` habilitado: `gh auth refresh -s project`

## Scripts Disponiveis

### project_manager.py

Gerencia Projects V2 via GraphQL.

```bash
# Criar project
python3 .claude/skills/github-projects/scripts/project_manager.py create \
  --title "SDLC: Feature X" \
  --description "Projeto para feature X"

# Obter project por titulo
python3 .claude/skills/github-projects/scripts/project_manager.py get --title "SDLC: Feature X"

# Listar projects
python3 .claude/skills/github-projects/scripts/project_manager.py list

# Adicionar issue ao project
python3 .claude/skills/github-projects/scripts/project_manager.py add-item \
  --project-number 1 \
  --issue-url "https://github.com/owner/repo/issues/123"

# Atualizar campo de um item
python3 .claude/skills/github-projects/scripts/project_manager.py update-field \
  --project-number 1 \
  --item-id "PVTI_xxx" \
  --field "Phase" \
  --value "Implementation"

# Configurar campos customizados SDLC
python3 .claude/skills/github-projects/scripts/project_manager.py configure-fields \
  --project-number 1
```

### project_views.py

Gerencia views (Kanban, Timeline, Table) do Project.

```bash
# Criar view Kanban por fase
python3 .claude/skills/github-projects/scripts/project_views.py create-kanban \
  --project-number 1

# Criar view Timeline
python3 .claude/skills/github-projects/scripts/project_views.py create-timeline \
  --project-number 1

# Listar views
python3 .claude/skills/github-projects/scripts/project_views.py list \
  --project-number 1
```

## Campos Customizados SDLC

| Campo | Tipo | Valores |
|-------|------|---------|
| Phase | SingleSelect | Backlog, Requirements, Architecture, Planning, In Progress, QA, Release, Done |
| Sprint | Iteration | Sprints configurados |
| Story Points | Number | 1, 2, 3, 5, 8, 13, 21 |
| Priority | SingleSelect | Critical, High, Medium, Low |

## Colunas do Kanban (por fase SDLC)

1. **Backlog** - Phases 0-1 (Preparation, Discovery)
2. **Requirements** - Phase 2
3. **Architecture** - Phase 3
4. **Planning** - Phase 4
5. **In Progress** - Phase 5 (Implementation)
6. **QA** - Phase 6 (Quality)
7. **Release** - Phase 7
8. **Done** - Completed

## GraphQL Queries Utilizadas

### Criar Project
```graphql
mutation CreateProject($ownerId: ID!, $title: String!) {
  createProjectV2(input: {ownerId: $ownerId, title: $title}) {
    projectV2 { id number url }
  }
}
```

### Adicionar Item
```graphql
mutation AddItem($projectId: ID!, $contentId: ID!) {
  addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
    item { id }
  }
}
```

### Atualizar Campo
```graphql
mutation UpdateField($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: ProjectV2FieldValue!) {
  updateProjectV2ItemFieldValue(
    input: {projectId: $projectId, itemId: $itemId, fieldId: $fieldId, value: $value}
  ) { item { id } }
}
```

## Integracao SDLC

### Ao iniciar workflow (Phase 0)
```bash
# 1. Criar project
PROJECT=$(python project_manager.py create --title "SDLC: $FEATURE_NAME" --json)

# 2. Configurar campos
python project_manager.py configure-fields --project-number $PROJECT_NUMBER

# 3. Criar views
python project_views.py create-kanban --project-number $PROJECT_NUMBER
```

### Ao transicionar de fase
```bash
# Atualizar campo Phase de todas as issues do sprint
python project_manager.py update-phase \
  --project-number $PROJECT_NUMBER \
  --from-phase 5 \
  --to-phase 6
```

## Exemplo de Uso Completo

```bash
# Criar project para nova feature
python project_manager.py create \
  --title "SDLC: Sistema de Autenticacao" \
  --description "Implementacao de autenticacao OAuth2"

# Configurar campos SDLC
python project_manager.py configure-fields --project-number 1

# Adicionar issue existente
python project_manager.py add-item \
  --project-number 1 \
  --issue-url "https://github.com/arbgjr/sdlc_agentico/issues/123"

# Atualizar fase da issue
python project_manager.py update-field \
  --project-number 1 \
  --item-id "PVTI_xxx" \
  --field "Phase" \
  --value "In Progress"
```

## Limitacoes

- Projects V2 requer scope `project` no token
- Alguns campos (Iteration) tem API limitada
- Views customizadas tem suporte parcial via API
