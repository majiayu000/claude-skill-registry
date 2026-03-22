---
name: coder
description: >-
  Implementa código passo-a-passo com verificação obrigatória e autocrítica. Use quando precisar implementar features, fazer refatorações, ou desenvolver código seguindo um plano estruturado com quality checks.
compatibility: Git, ambiente de desenvolvimento
metadata:
  author: aronpc
  version: 1.0.0
  category: dev
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# coder

## Resumo
Implementa código passo-a-passo com verificação obrigatória e autocrítica.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `planner` | Para usar planos estruturados como input |
| `sprint` | Para executar tarefas de um sprint |
| `architecture` | Para seguir padrões arquiteturais |
| `standards` | Para seguir padrões de código |
| `testing` | Para criar testes durante implementação |
| `qa` | Para validação final do código |
| `workflow` | Para commits atômicos |

## Quando usar

Use esta skill sempre que precisar:

- Implementar código a partir de um plano ou especificação
- Transformar tarefas em código funcional
- Executar desenvolvimento passo-a-passo com verificação
- Trabalhar em features, refatorações ou investigações
- Garantir qualidade através de autocrítica e testes

## Environment Awareness

### Worktree Isolation

**IMPORTANTE**: Se você está em um worktree git, o isolamento é automático. Não é necessário criar branch.

Verifique sempre onde você está trabalhando:

```bash
# Verificar se está em worktree
git worktree list

# Verificar branch atual
git branch --show-current
```

### Path Confusion Prevention

**Nunca assuma caminhos**. Sempre verifique o CWD (Current Working Directory):

- Use caminhos absolutos para leitura/escrita
- Verifique o diretório antes de operações críticas
- Veja `references/path-confusion-prevention.md` para exemplos detalhados

## Workflow de Implementação (Steps 1-13)

### Step 1: Get Bearings

Antes de qualquer coisa, entenda onde você está:

```bash
# Verificar contexto
pwd
git status
git branch --show-current
git log -3 --oneline
```

Pergunte-se:
- Em que projeto/repo estou?
- Qual é o branch atual?
- Há alterações não commitadas?
- Qual é o contexto dos últimos commits?

### Step 2: Understand Plan

Leia e compreenda o plano de implementação:

1. Localize o arquivo de plano (ex: `plan.md`, `sprints/XXX.md`)
2. Identifique as tarefas a serem executadas
3. Liste dependências e pré-requisitos
4. Esclareça dúvidas ANTES de começar

**Checklist de Entendimento:**

- [ ] Li o plano completo
- [ ] Entendi o objetivo final
- [ ] Identifiquei todas as tarefas
- [ ] Sei quais arquivos serao modificados
- [ ] Conheco os criterios de aceitacao

### Step 3: Verify Environment

Confirme que o ambiente está pronto:

```bash
# Dependências instaladas?
composer install  # PHP
npm install       # JS

# Banco de dados acessível?
php artisan migrate --pretend

# Testes passando?
php artisan test --filter=existing
```

### Step 4: Create Implementation Branch

Se NAO estiver em worktree, crie um branch:

```bash
git checkout -b feat/nome-da-feature
# ou
git checkout -b fix/nome-do-fix
# ou
git checkout -b refactor/nome-da-refactor
```

### Step 5: Implement Core Changes

Implemente as mudanças principais:

1. **Siga o plano** - não improvise fora do escopo
2. **Um passo de cada vez** - não tente fazer tudo junto
3. **Commits atomicos** - cada mudança logica = um commit
4. **Teste incrementalmente** - não espere terminar para testar

### Step 6: Verify Implementation

**OBRIGATORIO**: Verifique que funciona:

```bash
# Testes automatizados
php artisan test
npm test

# Linting/Static Analysis
./vendor/bin/pint --test
./vendor/bin/phpstan

# Build (se aplicavel)
npm run build
```

### Step 7: Run Feature Tests

Teste a feature manualmente:

1. Suba o servidor local
2. Execute o fluxo completo da feature
3. Verifique edge cases
4. Confirme UX/UI conforme esperado

### Step 8: Self-Critique Checklist

**PARE e faça autocrítica** antes de prosseguir:

#### Qualidade de Código
- [ ] Código legível e bem nomeado?
- [ ] Sem código morto ou comentado?
- [ ] Funções/métodos com responsabilidade unica?
- [ ] DRY - sem repetição desnecessária?

#### Seguranca
- [ ] Inputs validados?
- [ ] Queries parametrizadas (sem SQL injection)?
- [ ] Autorização verificada?
- [ ] Dados sensíveis protegidos?

#### Performance
- [ ] N+1 queries evitadas?
- [ ] Indices necessários criados?
- [ ] Cache utilizado quando apropriado?
- [ ] Paginacao implementada?

#### Manutenibilidade
- [ ] Testes escritos/atualizados?
- [ ] Documentação atualizada?
- [ ] Padrões do projeto seguidos?
- [ ] Types/PHPDoc corretos?

### Step 9: Fix Issues Found

Se encontrou problemas na autocrítica:

1. **Liste os problemas** - não tente resolver tudo de uma vez
2. **Priorize** - críticos primeiro, depois melhorias
3. **Corrija** - um problema por vez
4. **Re-teste** - confirme que a correção funciona
5. **Volte ao Step 8** - ate passar todos checks

### Step 10: Update Documentation

Atualize documentação relevante:

- [ ] README.md se adicionou nova funcionalidades
- [ ] CHANGELOG.md com mudanças
- [ ] Comentarios em código complexo
- [ ] API documentation se aplicavel

### Step 11: Final Verification

**Última verificação completa:**

```bash
# Suite de testes completa
php artisan test --parallel

# Static analysis
./vendor/bin/phpstan --memory-limit=2G

# Code style
./vendor/bin/pint --test

# Build de produção
npm run build
```

### Step 12: Commit Changes

Commits seguindo convencao:

```bash
# Adicionar arquivos específicos (evite git add .)
git add path/to/specific/files

# Commit com mensagem descritiva
git commit -m "feat: adiciona feature X

- Implementa funcionalidades A
- Adiciona testes para B
- Atualiza documentação de C"
```

**Convencao de Commits:**
- `feat:` - Nova funcionalidades
- `fix:` - Correção de bug
- `refactor:` - Refatoracao
- `test:` - Testes
- `docs:` - Documentação
- `chore:` - Manutencao

### Step 13: Completion Checks

**Verificacoes finais antes de considerar completo:**

- [ ] Todas as tarefas do plano executadas?
- [ ] Todos os testes passando?
- [ ] Autocrítica completa e sem pendências?
- [ ] Commits feitos com mensagens claras?
- [ ] Branch pronto para merge/PR?
- [ ] Documentação atualizada?

## Workflow Guidance por Tipo

Cada tipo de implementação tem particularidades. Veja detalhes em:

- **Feature**: `references/workflow-guidance.md#feature-workflow`
- **Investigation**: `references/workflow-guidance.md#investigation-workflow`
- **Refactor**: `references/workflow-guidance.md#refactor-workflow`

## Recovery Process

Se ficar preso ou encontrar bloqueios:

1. Marque onde parou
2. Documente o problema
3. Tente abordagem alternativa
4. Consulte `references/recovery-process.md`

Veja detalhes completos em `references/recovery-process.md`.

## Quick Reference

### Comandos Úteis

```bash
# Verificar status
git status
php artisan test
./vendor/bin/pint --test

# Criar branch
git checkout -b feat/nome

# Commit
git add arquivo.php
git commit -m "feat: descrição"

# Verificar testes específicos
php artisan test --filter=NomeDoTest
```

### Estrutura de Commits

```
tipo: descrição curta (max 50 chars)

- Detalhe 1
- Detalhe 2
- Detalhe 3
```

### Red Flags - PARE se:

- Testes falhando e não sabe consertar
- Código ficou muito complexo
- Precisa de mais contexto do negocio
- Algo não faz sentido no plano
- Esta improvisando muito fora do escopo

## Referências

- `references/recovery-process.md` - Loop de recuperação e stuck marking
- `references/path-confusion-prevention.md` - Prevencao de confusão de caminhos
- `references/workflow-guidance.md` - Guias específicos por tipo de trabalho
