---
name: roadmap
description: >-
  Cria estratégia de produto com features priorizadas usando método MoSCoW. Use quando precisar definir roadmap, priorizar features, ou planejar a evolução do produto.
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

# roadmap

## Resumo
Define estratégia de produto com roadmap, features priorizadas (MoSCoW) e análise competitiva.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `spec` | Para transformar features do roadmap em specs técnicas |
| `sprint` | Para criar sprints a partir do roadmap |
| `codebase` | Para descobrir melhorias técnicas |
| `ui-ux` | Para descobrir melhorias de interface |

## Quando usar

Use esta skill quando precisar:
- Descobrir e documentar o propósito de um projeto
- Gerar features estratégicas priorizadas
- Analisar concorrentes
- Criar roadmap estruturado

**Não use para:**
- Especificações técnicas (use spec-creation)
- Melhorias de código (use codebase-ideation)

---

## Roadmap Discovery

### Objetivo
Entender o projeto profundamente para informar decisões de roadmap.

### Estrutura de Descoberta

```json
{
  "project_name": "Nome",
  "project_type": "web-app|mobile-app|cli|library|api",
  "tech_stack": {
    "primary_language": "language",
    "frameworks": ["framework1"],
    "key_dependencies": ["dep1"]
  },
  "target_audience": {
    "primary_persona": "Quem é o usuário principal?",
    "pain_points": ["Problemas que enfrentam"],
    "goals": ["O que querem alcançar"]
  },
  "product_vision": {
    "one_liner": "Uma frase descrevendo o produto",
    "problem_statement": "Que problema isso resolve?",
    "value_proposition": "Por que alguém usaria isso?"
  },
  "current_state": {
    "maturity": "idea|prototype|mvp|growth|mature",
    "existing_features": ["Feature 1"],
    "known_gaps": ["Capacidade faltante"]
  }
}
```

---

## Geração de Features

### Priorização MoSCoW

| Prioridade | Definição |
|------------|-----------|
| **Must** | Crítico para MVP |
| **Should** | Importante mas não crítico |
| **Could** | Nice to have |
| **Wont** | Não planejado |

### Estrutura de Feature

```json
{
  "id": "feature-1",
  "title": "Nome da feature",
  "description": "O que esta feature faz",
  "rationale": "Por que isso importa",
  "priority": "must",
  "complexity": "medium",
  "impact": "high",
  "acceptance_criteria": ["Critério 1"],
  "user_stories": ["Como [usuário], quero [ação]"]
}
```

---

## Análise Competitiva

### Processo

1. Identificar concorrentes (WebSearch)
2. Pesquisar feedback de usuários
3. Identificar pain points
4. Encontrar gaps de mercado

### Estrutura

```json
{
  "competitors": [
    {
      "name": "Competitor",
      "url": "https://...",
      "pain_points": ["Issue 1"],
      "strengths": ["Strength 1"]
    }
  ],
  "market_gaps": [
    {
      "description": "Gap in the market",
      "opportunity_size": "high"
    }
  ]
}
```

---

## Output: roadmap.json

```json
{
  "project_name": "Nome",
  "vision": "One-liner",
  "phases": [
    {
      "id": "phase-1",
      "name": "Foundation",
      "features": ["feature-1", "feature-2"]
    }
  ],
  "features": [
    {
      "id": "feature-1",
      "title": "Feature",
      "priority": "must"
    }
  ]
}
```

---

## Referências

- `references/roadmap-discovery.md` - Agent de discovery
- `references/feature-generator.md` - Brainstorming MoSCoW
- `references/competitor-analysis.md` - Análise competitiva
