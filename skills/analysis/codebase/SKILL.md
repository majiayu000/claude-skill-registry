---
name: codebase
description: >-
  Descobre melhorias e oportunidades de refatoração baseada em padrões existentes no código. Use quando quiser analisar o codebase para encontrar melhorias, inconsistências, ou áreas que precisam de atenção.
compatibility: Qualquer projeto
metadata:
  author: aronpc
  version: 1.0.0
  category: ideation
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
---

# codebase

## Resumo
Identifica oportunidades de melhoria no codebase baseada em padrões existentes.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `spec` | Para criar specs a partir das melhorias identificadas |
| `ui-ux` | Para combinar melhorias técnicas e visuais |
| `architecture` | Para identificar melhorias arquiteturais |
| `qa` | Para avaliar debt técnico |

## Quando usar

Use esta skill quando precisar:
- Descobrir oportunidades de melhoria no código
- Identificar padrões que podem ser estendidos
- Encontrar quick wins e melhorias de maior impacto
- Priorizar melhorias por esforço/impacto

**Não use para:**
- Planejamento estratégico de produto (use roadmap-strategy)
- Revisão de PR (use github-pr-review)

---

## Princípio Chave

**Encontre oportunidades que o código revela.**

Estas são features e melhorias que emergem naturalmente de entender:
- Que padrões existem
- Como podem ser estendidos
- Onde podem ser aplicados em outros lugares

---

## Níveis de Esforço

| Nível | Tempo | Descrição |
|-------|-------|-----------|
| trivial | 1-2h | Cópia direta com mudanças menores |
| small | 0.5 dia | Padrão claro, alguma lógica nova |
| medium | 1-3 dias | Padrão existe mas precisa adaptação |
| large | 3-7 dias | Padrão arquitetural habilita nova capacidade |
| complex | 1-2 semanas | Fundação suporta adição major |

---

## Categorias de Oportunidade

### A. Extensões de Padrão (trivial → medium)
- CRUD para entidade similar
- Filtros para mais campos
- Export para outros formatos

### B. Oportunidades de Arquitetura (medium → complex)
- Data model suporta feature X
- API structure habilita novo tipo de endpoint
- Component architecture suporta nova view

### C. Configuração/Settings (trivial → small)
- Valores hardcoded → configuráveis
- Missing preferences seguindo padrão existente

### D. Adições de Utilitários (trivial → medium)
- Validadores para mais casos
- Formatters para mais formatos
- Helpers relacionados

### E. Melhorias de UI (trivial → medium)
- Loading states seguindo padrão
- Empty states seguindo padrão
- Error states seguindo padrão

### F. Extensões de Infraestrutura (medium → complex)
- Plugin points não utilizados
- Event system com novos tipos

---

## Output Format

```json
{
  "code_improvements": [
    {
      "id": "ci-001",
      "title": "Add search to user list",
      "description": "Add search functionality to user list page",
      "rationale": "Search pattern exists in product list",
      "builds_upon": ["ProductList search component"],
      "estimated_effort": "trivial",
      "affected_files": ["src/pages/Users.tsx"],
      "existing_patterns": ["SearchBar component"],
      "implementation_approach": "Reuse SearchBar from ProductList"
    }
  ]
}
```

---

## Analysis Phases

1. **Load Context** - Ler project_index.json, ideation_context.json
2. **Discover Patterns** - Buscar padrões repetidos
3. **Identify Opportunities** - Categorizar por tipo
4. **Analyze Specific** - Deep dive em cada oportunidade
5. **Filter & Prioritize** - Remover duplicados, priorizar
6. **Generate Output** - Criar code_improvements_ideas.json

---

## Referências

- `references/improvement-categories.md` - Categorias detalhadas
- `references/insight-extractor.md` - Extração de insights
