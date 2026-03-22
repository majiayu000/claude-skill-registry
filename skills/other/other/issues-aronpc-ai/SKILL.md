---
name: issues
description: >-
  Analisa e classifica issues com detecção de duplicados. Use quando precisar gerenciar issues do GitHub/GitLab, classificar bugs, ou organizar backlog de tarefas.
compatibility: GitHub, GitLab
metadata:
  author: aronpc
  version: 1.0.0
  category: github
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# issues

## Resumo
Analisa e classifica issues do GitHub com detecção de duplicados, spam e priorização.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `spec` | Para converter issues válidos em specs |
| `sprint` | Para adicionar issues a sprints |
| `planner` | Para planejar implementação de bugs |
| `pr-review` | Para relacionar issues com PRs |

## Quando usar

Use esta skill quando precisar:
- Classificar issues do GitHub
- Detectar issues duplicados
- Identificar spam ou issues de baixa qualidade
- Priorizar issues por severidade
- Extrair requisitos de issues para specs

**Não use para:**
- Code review (use github-pr-review)
- Planejamento de features (use spec-creation)

---

## Issue Classification

### Primary Categories

| Categoria | Descrição |
|-----------|-----------|
| `bug` | Algo está quebrado |
| `feature` | Request de nova funcionalidades |
| `documentation` | Melhorias na documentação |
| `question` | Dúvida ou suporte |
| `duplicate` | Duplicado de issue existente |
| `spam` | Conteúdo promocional ou irrelevante |
| `feature_creep` | Múltiplas features em um issue |

### Output Format

```json
{
  "category": "bug",
  "confidence": 0.92,
  "priority": "high",
  "labels_to_add": ["type:bug", "priority:high"],
  "is_duplicate": false,
  "duplicate_of": null,
  "is_spam": false,
  "is_feature_creep": false,
  "comment": null
}
```

---

## Bug Detection

### Bug Report Patterns

**Indicadores de bug:**
- "não funciona", "broken", "error", "crash"
- Stack traces
- Expected vs Actual
- Passos para reproduzir
- Screenshots de erros

### Análise de Bug

```json
{
  "issue_type": "bug",
  "title": "Concise task title",
  "summary": "One paragraph summary",
  "requirements": ["Fix the authentication timeout"],
  "acceptance_criteria": ["Sessions persist correctly"],
  "affected_áreas": ["src/auth/session.ts"],
  "complexity": "standard",
  "risks": ["May affect existing sessions"]
}
```

---

## Duplicate Detection

### Similarity Indicators

| Força | Indicadores |
|-------|-------------|
| **Alta** | Mensagens de erro idênticas, stack traces iguais |
| **Média** | Descrição similar, mesma área |
| **Baixa** | Mesmas labels, mesmo autor |

### Confidence Thresholds

| Threshold | Ação |
|-----------|------|
| 90%+ | Quase certamente duplicado |
| 80-89% | Provável duplicado, verificar |
| 70-79% | Possível duplicado, revisar |
| <70% | Não é duplicado |

---

## Spam Detection

### Spam Categories

| Tipo | Sinais |
|------|--------|
| Promocional | Links externos, marketing |
| Abuso | Linguagem ofensiva |
| Gibberish | Texto aleatório |
| Bot | Template, massa |

### Spam Signals

- Links externos não relacionados
- Conteúdo sem relação com o projeto
- Linguagem abusiva
- Texto sem sentido

---

## Priority Assessment

### High Priority
- Vulnerabilidades de segurança
- Perda de dados potencial
- Funcionalidade core quebrada
- Afeta muitos usuários

### Medium Priority
- Features com caso de uso claro
- Bugs não críticos
- Performance issues

### Low Priority
- Melhorias menores
- Edge cases
- Cosmético

---

## Label Taxonomy

### Type Labels
- `type:bug`
- `type:feature`
- `type:docs`
- `type:question`

### Priority Labels
- `priority:high`
- `priority:medium`
- `priority:low`

### Triage Labels
- `triage:potential-duplicate`
- `triage:needs-review`
- `triage:needs-breakdown`
- `triage:needs-info`

---

## Referências

- `references/issue-classification.md` - Classificação detalhada
- `references/bug-detection.md` - Padrões de bug report
- `references/duplicate-detection.md` - Algoritmo de similaridade
- `references/spam-detection.md` - Sinais de spam
