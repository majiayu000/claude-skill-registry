---
name: spec
description: >-
  Escreve especificações técnicas com requisitos, design e critérios de teste. Use quando precisar criar specs técnicas, documentar requisitos, ou definir contratos de API.
compatibility: Qualquer projeto
metadata:
  author: aronpc
  version: 1.0.0
  category: planning
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - WebSearch
---

# spec

## Resumo
Cria especificações técnicas completas com requisitos, design, API e plano de testes.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `roadmap` | Para usar features do roadmap como input |
| `codebase` | Para descobrir melhorias baseadas no código |
| `ui-ux` | Para descobrir melhorias de interface |
| `planner` | Para transformar spec em plano de implementação |
| `sprint` | Para criar sprint a partir da spec |
| `issues` | Para converter issues em requisitos |

## Quando usar

Use esta skill quando precisar:
- Criar especificações técnicas para novas features
- Documentar requisitos de implementação
- Planejar arquitetura de soluções
- Coletar e organizar requisitos de stakeholders

**Não use para:**
- Planejamento estratégico de produto (use roadmap-strategy)
- Ideias de melhoria sem requisito claro (use codebase-ideation)
- Bug fixes simples (use quick-spec)

---

## Pipeline Overview

O pipeline de criação de specs tem 4 estágios:

```
1. Requirements Gatherer → Coleta requisitos
2. Research Agent → Pesquisa soluções
3. Spec Writer → Escreve spec.md
4. Spec Critic → Revisa e refina
```

### Quick Spec (Alternativa)

Para tarefas simples e diretas, use Quick Spec:
- Single file changes
- Bug fixes óbvios
- Config updates
- Typo fixes

Veja `references/requirements-gatherer.md` para detalhes do coletor.

---

## Requirements Gatherer

### Objetivo
Coletar e documentar requisitos de forma estruturada.

### Processo
1. Entender o problema/feature request
2. Identificar stakeholders
3. Coletar requisitos funcionais
4. Coletar requisitos não-funcionais
5. Identificar restrições
6. Definir critérios de aceitação

### Output
```json
{
  "title": "Feature Title",
  "problem_statement": "What problem does this solve?",
  "functional_requirements": [
    {"id": "FR-1", "description": "Requirement", "priority": "must"}
  ],
  "non_functional_requirements": [
    {"id": "NFR-1", "type": "performance", "description": "Requirement"}
  ],
  "constraints": ["Constraint 1"],
  "acceptance_criteria": ["AC-1: Criterion"],
  "open_questions": ["Question 1"]
}
```

Veja `references/requirements-gatherer.md` para detalhes.

---

## Research Agent

### Objetivo
Pesquisar soluções e tecnologias necessárias.

### Processo
1. Identificar integrações necessárias
2. Pesquisar APIs e bibliotecas
3. Avaliar alternativas
4. Documentar findings

### Output
```json
{
  "integrations_needed": [
    {
      "name": "Integration Name",
      "type": "API|Library|Service",
      "purpose": "Why needed",
      "documentation_url": "https://...",
      "notes": "Implementation notes"
    }
  ],
  "alternatives_considered": [
    {"name": "Alt 1", "pros": [], "cons": [], "decision": "rejected"}
  ],
  "technical_notes": "Important technical details"
}
```

Veja `references/research-agent.md` para detalhes.

---

## Spec Writer

### Objetivo
Criar documento de especificação completo.

### Estrutura spec.md
```markdown
# [Feature Name]

## Overview
[Brief description of the feature]

## Problem Statement
[What problem this solves]

## Goals
- Goal 1
- Goal 2

## Non-Goals
- What this feature will NOT do

## Technical Design

### Architecture
[Diagrams, flow descriptions]

### Data Model
[Schema, data structures]

### API Design
[Endpoints, contracts]

### UI/UX Design
[Mockups, user flows]

## Implementation Plan
[Phases, milestones]

## Testing Strategy
[Unit, integration, e2e tests]

## Risks & Mitigations
[Risk assessment]

## Open Questions
[Unresolved items]

## References
[Links to docs, resources]
```

Veja `references/spec-writer.md` para detalhes.

---

## Spec Critic

### Objetivo
Revisar e refinar a especificação.

### Checklist de Revisão
- [ ] Problema claramente definido?
- [ ] Goals e Non-goals claros?
- [ ] Design técnico completo?
- [ ] Edge cases considerados?
- [ ] Plano de testes adequado?
- [ ] Riscos identificados?
- [ ] Sem ambiguidades?

### Output
```json
{
  "overall_quality": "excellent|good|needs_work|poor",
  "issues": [
    {
      "section": "Technical Design",
      "issue": "Missing error handling",
      "severity": "major|minor",
      "suggestion": "Add error handling section"
    }
  ],
  "recommendations": ["Recommendation 1"]
}
```

Veja `references/spec-critic.md` para detalhes.

---

## Quick Spec

Para tarefas simples, crie uma spec minimalista:

```markdown
# Quick Spec: [Task Title]

## Task
[One-line description of what to do]

## Files to Modify
- `path/to/file1.ts` - [What to change]
- `path/to/file2.ts` - [What to change]

## Change Details
[Specific changes to make]

## Verification
- [ ] [How to verify it works]
```

### Quando usar Quick Spec
- Single file changes
- Obvious bug fixes
- Config updates
- Typo fixes
- Simple refactors

### Quando NÃO usar Quick Spec
- Multiple files
- New features
- API changes
- Database changes
- Architecture changes

---

## Workflow Completo

### 1. Iniciar com Requirements
```bash
# Criar diretório de spec
mkdir -p specs/[feature-name]

# Coletar requisitos
# Usar Requirements Gatherer
```

### 2. Pesquisar (se necessário)
```bash
# Pesquisar integrações
# Usar Research Agent
```

### 3. Escrever Spec
```bash
# Criar spec.md
# Usar Spec Writer
```

### 4. Revisar
```bash
# Criticar spec
# Usar Spec Critic
# Iterar se necessário
```

### 5. Finalizar
```bash
# Spec pronta para implementation planner
```

---

## Referências

- `references/requirements-gatherer.md` - Coleta de requisitos
- `references/research-agent.md` - Pesquisa de integrações
- `references/spec-writer.md` - Escrita de spec.md
- `references/spec-critic.md` - Crítica e refinamento
