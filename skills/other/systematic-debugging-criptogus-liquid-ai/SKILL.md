---
name: systematic-debugging
description: Debugging sistemático - Análise de root cause em 4 fases
version: 1.0.0
category: workflow
triggers:
  - debug
  - debugging
  - bug
  - erro
  - error
  - não funciona
  - quebrou
  - broken
  - fix
  - root cause
  - investigar
tools: []
author: liquid-ai
based_on: obra/superpowers
---

# Systematic Debugging - Root Cause Analysis

Esta skill implementa um processo sistemático de debugging em 4 fases para encontrar e corrigir bugs de forma eficiente.

## Princípio Fundamental

> **Debugging não é adivinhar. É um processo científico de eliminação.**

```
┌─────────────────────────────────────────────────────────────┐
│  NUNCA:  "Acho que o problema é X, vou mudar e ver"        │
│  SEMPRE: "Vou coletar evidências para confirmar a causa"   │
└─────────────────────────────────────────────────────────────┘
```

## As 4 Fases do Debugging Sistemático

### Fase 1: REPRODUZIR (Obrigatório)

```
┌─────────────────────────────────────────────────────────────┐
│  🎯 OBJETIVO: Conseguir reproduzir o bug consistentemente   │
└─────────────────────────────────────────────────────────────┘
```

**Checklist:**
- [ ] Consigo reproduzir o bug?
- [ ] Quais são os passos exatos?
- [ ] É intermitente ou consistente?
- [ ] Em qual ambiente ocorre? (dev, staging, prod)
- [ ] Desde quando começou? (qual commit/deploy)

**Perguntas Críticas:**
1. O que o usuário estava fazendo?
2. Quais dados estavam envolvidos?
3. Qual era o estado do sistema?

**Output Esperado:**
```markdown
## Reprodução do Bug
- **Passos:** [1, 2, 3...]
- **Frequência:** [sempre | às vezes | raro]
- **Ambiente:** [dev | staging | prod]
- **Primeiro relato:** [data/commit]
```

### Fase 2: ISOLAR (Eliminar Variáveis)

```
┌─────────────────────────────────────────────────────────────┐
│  🎯 OBJETIVO: Reduzir o espaço de busca ao mínimo          │
└─────────────────────────────────────────────────────────────┘
```

**Técnicas de Isolamento:**

| Técnica | Quando Usar | Como |
|---------|-------------|------|
| Binary Search | Bug em fluxo longo | Divida o fluxo ao meio, teste cada metade |
| Git Bisect | Bug em commit recente | `git bisect` para encontrar commit culpado |
| Feature Flags | Bug em feature específica | Desabilite features até isolar |
| Simplificação | Bug em dados complexos | Reduza dados ao mínimo que reproduz |

**Perguntas para Isolamento:**
1. Frontend ou Backend?
2. Código ou Dados?
3. Novo código ou Regressão?
4. Ambiente específico ou todos?

**Comando Útil - Git Bisect:**
```bash
git bisect start
git bisect bad HEAD
git bisect good <commit-que-funcionava>
# Git vai fazer binary search nos commits
```

### Fase 3: DIAGNOSTICAR (Encontrar Root Cause)

```
┌─────────────────────────────────────────────────────────────┐
│  🎯 OBJETIVO: Entender POR QUE o bug acontece              │
└─────────────────────────────────────────────────────────────┘
```

**Ferramentas de Diagnóstico:**

| Ferramenta | Propósito |
|------------|-----------|
| Console.log / Print | Rastrear fluxo de execução |
| Debugger (breakpoints) | Inspecionar estado em tempo real |
| Stack trace | Entender cadeia de chamadas |
| Logs de produção | Contexto do erro real |
| Network tab | Verificar requests/responses |

**Framework de Análise:**

```
┌─────────────────────────────────────────────────────────────┐
│  1. WHAT: O que está acontecendo de errado?                │
│  2. WHERE: Onde no código o erro ocorre?                   │
│  3. WHEN: Quando/sob quais condições?                      │
│  4. WHY: Por que o código se comporta assim?               │
│  5. HOW: Como o estado chegou a esse ponto?                │
└─────────────────────────────────────────────────────────────┘
```

**5 Whys Technique:**
```
Bug: Usuário não consegue salvar
  Why 1: API retorna 500
  Why 2: Database query falha
  Why 3: Coluna não existe
  Why 4: Migration não foi aplicada
  Why 5: Deploy script não roda migrations

ROOT CAUSE: Deploy script incompleto
```

### Fase 4: CORRIGIR (E Prevenir)

```
┌─────────────────────────────────────────────────────────────┐
│  🎯 OBJETIVO: Corrigir o bug E prevenir recorrência        │
└─────────────────────────────────────────────────────────────┘
```

**Checklist de Correção:**
- [ ] Fix resolve o root cause (não só o sintoma)?
- [ ] Fix não introduz novos bugs?
- [ ] Teste automatizado cobre o cenário?
- [ ] Documentação atualizada se necessário?

**Template de Fix:**
```markdown
## Bug Fix: [Título]

### Root Cause
[Explicação do que causava o bug]

### Solução
[O que foi mudado e por quê]

### Testes Adicionados
- [ ] Teste que reproduz o bug original
- [ ] Teste de regressão

### Prevenção Futura
[O que fazer para evitar bugs similares]
```

## Padrões Comuns de Bugs

### 1. Race Conditions
```
Sintoma: Bug intermitente, difícil de reproduzir
Causa: Operações assíncronas sem sincronização
Solução: Locks, transações, ou sequenciamento
```

### 2. Off-by-One
```
Sintoma: Funciona para maioria, falha em edge cases
Causa: Índices ou limites incorretos
Solução: Revisar loops, arrays, e condições de borda
```

### 3. Null/Undefined Reference
```
Sintoma: "Cannot read property X of undefined"
Causa: Dados ausentes não tratados
Solução: Validação defensiva, optional chaining
```

### 4. State Corruption
```
Sintoma: Estado inconsistente após operações
Causa: Mutação direta, falta de imutabilidade
Solução: Imutabilidade, transações
```

### 5. Environment Mismatch
```
Sintoma: Funciona local, falha em prod
Causa: Diferenças de ambiente (vars, versões, dados)
Solução: Padronizar ambientes, containerização
```

## Anti-Patterns de Debugging

| Anti-Pattern | Problema | Solução |
|--------------|----------|---------|
| Shotgun Debugging | Mudar coisas aleatoriamente | Seguir as 4 fases |
| Printf Everywhere | Logs sem estratégia | Logs direcionados pela hipótese |
| Blame Game | Culpar outros/libs | Assumir que o bug é seu até provar contrário |
| Quick Fix | Corrigir sintoma, não causa | Sempre buscar root cause |
| Solo Debugging | Debugar sozinho por horas | Pedir ajuda após 30min travado |

## Regra dos 30 Minutos

```
┌─────────────────────────────────────────────────────────────┐
│  Se você está travado no mesmo bug por mais de 30 minutos: │
│                                                             │
│  1. Pare e documente o que você sabe                       │
│  2. Peça uma segunda opinião (rubber duck ou colega)       │
│  3. Faça uma pausa de 10 minutos                           │
│  4. Volte com perspectiva fresca                           │
└─────────────────────────────────────────────────────────────┘
```

## Checklist Final

### Antes de Começar
- [ ] Bug está claramente definido?
- [ ] Tenho acesso aos logs/ambiente necessário?
- [ ] Sei quando o bug começou?

### Durante o Debugging
- [ ] Estou seguindo as 4 fases em ordem?
- [ ] Estou documentando minhas descobertas?
- [ ] Estou testando uma hipótese por vez?

### Depois do Fix
- [ ] Bug original está corrigido?
- [ ] Não introduzi novos bugs?
- [ ] Teste automatizado adicionado?
- [ ] Root cause documentado?

---

**Esta skill ativa AUTOMATICAMENTE quando:**
- Usuário menciona "bug", "erro", "debug", "não funciona"
- Discussão sobre investigação de problemas
- Análise de stack traces ou logs de erro
