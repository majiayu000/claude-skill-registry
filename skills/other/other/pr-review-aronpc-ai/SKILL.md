---
name: pr-review
description: >-
  Faz review de Pull Requests analisando segurança, qualidade e aderência a padrões. Use quando precisar revisar PRs, verificar qualidade de código, ou garantir conformidade com padrões do projeto.
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

# pr-review

## Resumo
Revisão sistemática de Pull Requests com análise multi-aspecto baseada em evidências.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `qa` | Para validação de qualidade antes do review |
| `standards` | Para verificar aderência aos padrões |
| `workflow` | Para verificar convenções de commit |
| `coder` | Para corrigir issues encontradas |

## Quando usar

Use esta skill quando precisar:
- Revisar Pull Requests de forma sistemática
- Identificar problemas de segurança em código
- Verificar qualidade e aderência a padrões
- Validar lógica e corretude de implementações
- Gerar feedback acionável para desenvolvedores

**Não use para:**
- Análise de codebase sem PR específico
- Sugestões de features (use codebase-ideation)
- Planejamento de implementação (use implementation-planner)

---

## Metodologia de Review

Esta skill segue uma metodologia **evidence-based** (baseada em evidências), não em confiança.

### Princípios Fundamentais

1. **Sempre verifique com código real** - Nunca reporte algo que não leu
2. **O diff é a pergunta, não a resposta** - Entenda o contexto antes de julgar
3. **Busque evidências, não padrões** - Confirme que o problema existe

### Estrutura de Review

```
Fase 0: Entender Intenção
├── Qual é a mudança proposta?
├── Qual problema está resolvendo?
└── Qual é o contexto da mudança?

Fase 1: Detecção de Triggers
├── Contrato de output mudou?
├── Contrato de input mudou?
├── Contrato comportamental mudou?
├── Side effects mudaram?
├── Contrato de falha mudou?
└── Contrato de null/undefined mudou?

Fase 2: Análise Especializada
├── Análise de Segurança
├── Análise de Qualidade
├── Lógica e Corretude
└── Aderência a Padrões

Fase 3: Validação de Findings
├── Verificar cada finding com código
├── Checar mitigações
└── Descartar falsos positivos

Fase 4: Síntese
├── Consolidar findings
├── Determinar veredito
└── Gerar itens de ação
```

---

## Análise de Segurança

### OWASP Top 10 - Áreas de Foco

| Categoria | O que buscar |
|-----------|--------------|
| Injection | SQL, command, LDAP injection |
| Auth failures | Session handling, weak passwords |
| Sensitive data | Exposed secrets, unencrypted data |
| XXE | XML parsing vulnerabilities |
| Access control | IDOR, privilege escalation |
| Misconfiguration | Debug mode, default credentials |
| XSS | Reflected, stored, DOM-based |
| Deserialization | Unsafe object deserialization |
| Vulnerabilities | Outdated dependencies |
| Logging | Missing audit trails |

### Checklist de Segurança

- [ ] Input validation presente
- [ ] Output encoding aplicado
- [ ] Auth checks corretos
- [ ] Secrets não hardcoded
- [ ] Dependencies atualizadas
- [ ] Error handling não vaza info

Veja `references/security-analysis.md` para detalhes.

---

## Análise de Qualidade de Código

### Dimensões de Qualidade

| Dimensão | Verificações |
|----------|--------------|
| Readability | Nomes claros, código autoexplicativo |
| Maintainability | Tamanho de funções, complexidade |
| Testability | Código testável, dependências injetáveis |
| Performance | Algoritmos eficientes, sem N+1 |
| Documentation | Comentários onde necessário |

### Checklist de Qualidade

- [ ] Funções < 50 linhas
- [ ] Complexidade ciclomática baixa
- [ ] DRY (não repetido)
- [ ] SOLID principles seguidos
- [ ] Testes para código novo/modificado

Veja `references/quality-checks.md` para detalhes.

---

## Lógica e Corretude

### Verificação de Lógica

1. **Trace the happy path** - Caminho principal funciona?
2. **Check edge cases** - Null, empty, boundary values
3. **Verify error handling** - Erros tratados corretamente?
4. **Check state management** - Estado consistente?

### Checklist de Corretude

- [ ] Lógica implementa o requisito
- [ ] Edge cases considerados
- [ ] Error paths tratados
- [ ] Race conditions evitadas
- [ ] State transitions corretas

---

## Pattern Adherence

### Verificações

- [ ] Segue padrões do codebase
- [ ] Estrutura consistente com código existente
- [ ] Naming conventions seguidas
- [ ] Arquitetura respeitada

Veja `references/specialist-agents.md` para padrões específicos.

---

## Tipos de Veredito

| Verdict | Quando usar |
|---------|-------------|
| `approved` | PR pronto para merge |
| `needs_changes` | Mudanças necessárias |
| `rejected` | PR não deve ser mergeado |

### Critérios de Aprovação

- Sem issues críticos ou high
- Testes passando
- Documentação atualizada
- Feedback de code review endereçado

### Critérios para Mudanças

- Issues encontrados que precisam fix
- Testes faltantes
- Documentação incompleta
- Violações de estilo/padrões

### Critérios de Rejeição

- Vulnerabilidades de segurança
- Breaking changes sem aprovação
- Arquitetura fundamentalmente errada
- Scope creep significativo

---

## Formato de Output

```markdown
## Resumo de Review do PR

**Verdict:** [approved | needs_changes | rejected]

### Visão Geral
[Breve descrição do que o PR faz]

### Issues Críticos (Obrigatório)
1. [Issue]: [Descrição] → [Ação]

### Alta Prioridade
1. [Issue]: [Descrição] → [Ação]

### Média Prioridade
1. [Suggestion]: [Descrição]

### Baixa Prioridade / Nitpicks
1. [Nit]: [Descrição]

### Pontos Positivos
- [Coisas positivas do PR]

### Testes
- [ ] Testes unitários adicionados/atualizados
- [ ] Testes de integração passando
- [ ] Testes manuais realizados

### Checklist para o Autor
- [ ] Resolver todos os issues críticos
- [ ] Atualizar documentação
- [ ] Adicionar testes para código novo
```

---

## Requisitos de Evidência

Todo finding DEVE incluir:

```json
{
  "finding": "Description of the issue",
  "severity": "critical|high|medium|low",
  "file": "path/to/file.ts",
  "line": 42,
  "evidence": "actual code snippet showing the issue",
  "recommendation": "How to fix it"
}
```

**Sem evidência de código real = Finding inválido**

---

## Referências

- `references/security-analysis.md` - OWASP Top 10 e security patterns
- `references/quality-checks.md` - Code quality patterns
- `references/specialist-agents.md` - Agentes especializados
- `references/pr-followup.md` - Follow-up process
- `references/fix-generation.md` - Estratégias de fix
