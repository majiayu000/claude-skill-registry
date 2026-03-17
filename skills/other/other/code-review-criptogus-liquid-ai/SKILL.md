---
name: code-review
description: Code Review sistemático - Checklist completo para revisão de código
version: 1.0.0
category: workflow
triggers:
  - code review
  - review
  - revisão
  - revisar código
  - pull request
  - pr review
  - merge request
  - mr
tools: []
author: liquid-ai
based_on: ComposioHQ/awesome-claude-skills
---

# Code Review - Revisão Sistemática de Código

Esta skill implementa um processo sistemático de code review para garantir qualidade, segurança e manutenibilidade do código.

## Princípios do Code Review

> **O objetivo não é encontrar erros, é melhorar o código e compartilhar conhecimento.**

### Mentalidade Correta

| Fazer | Evitar |
|-------|--------|
| Sugerir melhorias | Criticar o autor |
| Explicar o "porquê" | Apenas apontar problemas |
| Elogiar código bom | Focar só no negativo |
| Ser específico | Comentários vagos |
| Priorizar issues | Tratar tudo igual |

## Processo de Review (5 Fases)

### Fase 1: Contexto (2 min)

```
┌─────────────────────────────────────────┐
│  1. Leia a descrição do PR/MR           │
│  2. Entenda o objetivo da mudança       │
│  3. Verifique issues relacionadas       │
│  4. Revise o escopo das mudanças        │
└─────────────────────────────────────────┘
```

**Perguntas:**
- O que este PR resolve?
- Qual o impacto esperado?
- Há breaking changes?

### Fase 2: Visão Geral (5 min)

```
┌─────────────────────────────────────────┐
│  1. Revise a lista de arquivos mudados  │
│  2. Identifique padrões nas mudanças    │
│  3. Note arquivos críticos (auth, db)   │
│  4. Verifique tamanho do diff           │
└─────────────────────────────────────────┘
```

**Red Flags:**
- [ ] PR muito grande (>500 linhas) - pedir para dividir
- [ ] Mudanças em arquivos não relacionados
- [ ] Arquivos sensíveis modificados (auth, security)

### Fase 3: Análise Detalhada (15-30 min)

```
┌─────────────────────────────────────────┐
│  1. Revise cada arquivo metodicamente   │
│  2. Verifique lógica e edge cases       │
│  3. Analise tratamento de erros         │
│  4. Confirme cobertura de testes        │
└─────────────────────────────────────────┘
```

### Fase 4: Testes e Validação (5 min)

```
┌─────────────────────────────────────────┐
│  1. Testes unitários existem?           │
│  2. Testes cobrem casos importantes?    │
│  3. CI/CD passou?                       │
│  4. Testes manuais necessários?         │
└─────────────────────────────────────────┘
```

### Fase 5: Feedback (5 min)

```
┌─────────────────────────────────────────┐
│  1. Organize comentários por prioridade │
│  2. Sugira melhorias específicas        │
│  3. Reconheça código bem escrito        │
│  4. Dê veredicto claro                  │
└─────────────────────────────────────────┘
```

## Checklist de Review

### Funcionalidade

- [ ] O código faz o que deveria?
- [ ] Edge cases são tratados?
- [ ] Erros são capturados e tratados?
- [ ] Não há regressões óbvias?

### Código Limpo

- [ ] Nomes de variáveis são descritivos?
- [ ] Funções são pequenas e focadas?
- [ ] Não há código duplicado?
- [ ] Comentários são necessários e úteis?

### Segurança

- [ ] Inputs são validados?
- [ ] Não há SQL injection?
- [ ] Não há XSS?
- [ ] Secrets não estão hardcoded?
- [ ] Auth/authz são verificados?

### Performance

- [ ] Queries são eficientes?
- [ ] Não há N+1 queries?
- [ ] Loops são otimizados?
- [ ] Caching é usado onde apropriado?

### Testes

- [ ] Testes unitários existem?
- [ ] Testes cobrem happy path?
- [ ] Testes cobrem error cases?
- [ ] Testes são legíveis?

### Manutenibilidade

- [ ] Código segue padrões do projeto?
- [ ] TypeScript types estão corretos?
- [ ] Imports estão organizados?
- [ ] Não há TODOs sem tracking?

## Níveis de Severidade

### 🔴 Blocker (Deve Corrigir)

- Bugs que quebram funcionalidade
- Vulnerabilidades de segurança
- Vazamento de dados/secrets
- Performance crítica

**Template:**
```
🔴 **BLOCKER**: [Descrição]

**Problema:** [O que está errado]
**Impacto:** [Consequência]
**Sugestão:** [Como corrigir]
```

### 🟡 Warning (Deveria Corrigir)

- Code smells
- Falta de tratamento de erro
- Testes insuficientes
- Documentação faltando

**Template:**
```
🟡 **WARNING**: [Descrição]

**Problema:** [O que poderia melhorar]
**Sugestão:** [Melhoria proposta]
```

### 🟢 Suggestion (Nice to Have)

- Melhorias de estilo
- Refatorações opcionais
- Otimizações menores

**Template:**
```
🟢 **SUGGESTION**: [Descrição]

**Ideia:** [Sugestão de melhoria]
```

### 💬 Question (Pedido de Clarificação)

- Não entendi a lógica
- Preciso de contexto
- Decisão de design

**Template:**
```
💬 **QUESTION**: [Pergunta]

**Contexto:** [Por que está perguntando]
```

### 👍 Praise (Reconhecimento)

- Código bem escrito
- Boa solução
- Melhoria notável

**Template:**
```
👍 **NICE**: [O que gostou]
```

## Padrões de Comentário

### Bom Comentário

```markdown
🟡 **WARNING**: Possível race condition

**Linha 45:** A verificação `if (user)` e a atualização `user.update()`
não são atômicas. Em alta concorrência, outro request pode modificar
o user entre essas operações.

**Sugestão:** Use uma transação ou lock otimista:
\`\`\`typescript
await db.transaction(async (tx) => {
  const user = await tx.user.findUnique({ where: { id } });
  if (user) await tx.user.update({ where: { id }, data });
});
\`\`\`
```

### Comentário Ruim

```markdown
❌ "Isso está errado"
❌ "Não gosto desse código"
❌ "Por que você fez isso?"
```

## Veredictos

### ✅ Approve

> "Código revisado e aprovado. Ótimo trabalho no [aspecto específico]!"

Usar quando:
- Não há blockers
- Warnings são menores
- Testes passam

### 🔄 Request Changes

> "Há alguns pontos que precisam de ajuste antes do merge. Veja os comentários marcados como BLOCKER."

Usar quando:
- Há blockers de segurança
- Bugs críticos encontrados
- Testes falhando

### 💬 Comment

> "Deixei algumas sugestões e perguntas. Nada bloqueante, mas gostaria de discutir antes de aprovar."

Usar quando:
- Precisa de clarificação
- Mudanças de design questionáveis
- Quer discussão antes de decidir

## Template de Review Completo

```markdown
## Code Review: [Título do PR]

### Resumo
[1-2 frases sobre o que foi revisado]

### Pontos Positivos
- 👍 [Aspecto bem feito]
- 👍 [Outro aspecto]

### Issues Encontradas

#### Blockers (🔴)
1. [Issue 1]
2. [Issue 2]

#### Warnings (🟡)
1. [Warning 1]
2. [Warning 2]

#### Suggestions (🟢)
1. [Suggestion 1]

### Perguntas
1. 💬 [Pergunta sobre decisão de design]

### Veredicto
[✅ Approve | 🔄 Request Changes | 💬 Comment]

### Próximos Passos
- [ ] [Ação necessária]
```

## Anti-Patterns de Review

| Anti-Pattern | Problema | Solução |
|--------------|----------|---------|
| Nitpicking | Foco em detalhes irrelevantes | Priorize impacto real |
| Rubber Stamping | Aprovar sem revisar | Dedique tempo adequado |
| Gatekeeping | Bloquear por preferência pessoal | Siga padrões do projeto |
| Drive-by Review | Comentar sem contexto | Entenda o objetivo primeiro |
| Delayed Review | Demorar dias para revisar | Revise em 24h |

---

**Esta skill ativa AUTOMATICAMENTE quando:**
- Usuário menciona "code review" ou "PR review"
- Discussão sobre merge/pull requests
- Pedido para revisar código
- Análise de qualidade de código
