---
name: qa
description: >-
  Executa validação de qualidade com 11 fases de QA e tiers de complexidade. Use quando precisar validar qualidade de código, rodar QA checks, ou garantir que o código está pronto para produção.
compatibility: Projetos Laravel
metadata:
  author: aronpc
  version: 1.0.0
  category: quality
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# qa

## Resumo
Sistema de validação de qualidade com 11 fases de QA, avaliação de complexidade e workflow de correção.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `testing` | Para execução de testes automatizados |
| `pr-review` | Para review de PR com foco em qualidade |
| `mcp` | Para validação visual da aplicação |
| `coder` | Para corrigir issues encontradas |
| `sprint` | Para atualizar status após validação |

## Quando usar

Use esta skill sempre que precisar:

- Validar qualidade de codigo antes de merge
- Executar revisao de pull requests
- Avaliar complexidade de mudancas
- Identificar e corrigir issues de codigo
- Verificar requisitos de teste por nivel de risco
- Preparar codigo para deploy em producao
- Analisar debt tecnico
- Implementar padroes de qualidade

**Nao use para:**
- Code review social (use github-pr-review)
- Planejamento de features (use spec-creation)
- Analise arquitetural (use codebase-ideation)

---

## Fluxo de Validacao

```
+------------------+     +------------------+     +------------------+
|  1. Avaliacao    |---->|  2. Execucao     |---->|  3. Correcao     |
|  de Complexidade |     |  das Fases QA    |     |  (se necessario) |
+------------------+     +------------------+     +------------------+
```

---

## Avaliacao de Complexidade

Antes de iniciar a validacao, determine o nivel de complexidade da mudanca.

### Tiers de Complexidade

| Tier | Score | Descricao | Testes Minimos | Aprovacao |
|------|-------|-----------|----------------|-----------|
| **Trivial** | 1 | Cosmetico, sem logica | Nenhum obrigatorio | Auto |
| **Low** | 2-3 | 1-2 arquivos, logica simples | 50% cobertura | Auto |
| **Medium** | 4-6 | 3-5 arquivos, moderada | 70% cobertura | 1 reviewer |
| **High** | 7-8 | 6-10 arquivos, complexa | 85% cobertura | 2 reviewers |
| **Critical** | 9-10 | 10+ arquivos, arquitetura | 90% cobertura | Tech Lead |

### Matriz de Avaliacao Rapida

```
Score = (Arquivos + Logica + DB + Impacto + Externos + Sensivel) / 6

Arquivos:     1=1-2 | 3=3-5 | 6=6-10 | 10=10+
Logica:       1=nenhuma | 3=simples | 5=moderada | 8=complexa | 10=muito complexa
DB:           0=nenhuma | 3=campos | 6=tabelas | 10=schema major
Impacto:      1=baixo | 4=medio | 7=alto | 10=critico
Externos:     0=nenhum | 5=opcional | 10=critico
Sensivel:     0=nenhum | 5=indireto | 10=critico
```

> **Detalhes completos:** `references/complexity-assessment.md`

---

## Fases de QA (0-10)

O processo de QA tem 11 fases sequenciais. Cada fase deve passar antes de prosseguir.

### Visao Geral

| Fase | Nome | Objetivo | Comando |
|------|------|----------|---------|
| 0 | Escopo | Entender mudancas e impacto | `git diff` |
| 1 | Sintaxe | Verificar compilacao | `php -l`, `npm run build` |
| 2 | Analise Estatica | PHPStan + Pint | `./vendor/bin/phpstan` |
| 3 | Seguranca | SQL injection, XSS, CSRF | `composer audit` |
| 4 | Testes Unitarios | Cobertura de unidades | `./vendor/bin/pest --filter=Unit` |
| 5 | Testes Integracao | Features e fluxos | `./vendor/bin/pest --filter=Feature` |
| 6 | Performance | N+1, queries, cache | Debugbar, Blackfire |
| 7 | Acessibilidade | WCAG (se frontend) | axe, WAVE |
| 8 | Documentacao | Docblocks, README | - |
| 9 | Compatibilidade | PHP, Laravel, browsers | - |
| 10 | Deploy Ready | Rollback, migrations | - |

### Fase 0: Analise de Escopo

- Identificar arquivos modificados
- Mapear dependencias diretas e indiretas
- Avaliar risco de breaking changes
- Classificar nivel de complexidade

### Fase 1: Sintaxe e Compilacao

```bash
# PHP syntax check
find . -name "*.php" -not -path "./vendor/*" -exec php -l {} \; | grep -v "No syntax errors"

# Frontend build
npm run build
```

### Fase 2: Analise Estatica

```bash
# PHPStan
./vendor/bin/phpstan analyse

# Laravel Pint (code style)
./vendor/bin/pint --test
```

### Fase 3: Seguranca

- Verificar SQL injection (queries raw)
- Verificar XSS (dados nao escapados)
- Verificar CSRF em formularios
- Validar input de usuario
- Verificar exposicao de dados sensiveis

```bash
# Auditoria de dependencias
composer audit
```

### Fase 4: Testes Unitarios

```bash
# Pest PHP
./vendor/bin/pest --filter=Unit --parallel

# Com cobertura
./vendor/bin/pest --coverage --min=80
```

### Fase 5: Testes de Integracao

```bash
# Feature tests
./vendor/bin/pest --filter=Feature

# Browser tests (Dusk)
php artisan dusk
```

### Fase 6: Performance

- Verificar queries N+1
- Verificar uso de eager loading
- Verificar indices de banco
- Benchmark operacoes criticas

**Metricas alvo:**
- Tempo de resposta < 200ms (p95)
- Queries por requisicao < 20
- Memory < 128MB por requisicao

### Fase 7: Acessibilidade (se frontend)

- Contraste de cores
- Navegacao por teclado
- Atributos ARIA
- Alt text em imagens
- Labels em formularios

### Fase 8: Documentacao

- Docblocks em metodos publicos
- Comentarios em logica complexa
- Atualizacao de README/CHANGELOG se necessario

### Fase 9: Compatibilidade

- Versao PHP minima
- Versao Laravel minima
- Backward compatibility
- Browser support (frontend)

### Fase 10: Deploy Readiness

- Plano de deploy documentado
- Plano de rollback testado
- Migrations reversiveis (down method)
- Feature flags (se necessario)
- Monitoramento configurado

> **Detalhes de todas as fases:** `references/qa-phases.md`

---

## Requisitos de Teste por Risco

### Trivial (Score 1)
- Verificacao visual/manual suficiente
- Auto-aprovacao permitida
- Deploy direto em producao (apos CI)

### Low (Score 2-3)
- 1-2 testes unitarios
- Cobertura de caso feliz + 1 caso de borda
- Auto-aprovacao permitida

### Medium (Score 4-6)
- Testes unitarios para metodos publicos
- 1-2 testes de feature/integration
- Teste de caso de borda e erro
- Code review por 1 pessoa

### High (Score 7-8)
- Cobertura completa de testes unitarios
- Suite de testes de integration
- Testes de contrato para APIs
- Testes de segurança quando aplicavel
- Code review por 2 pessoas
- Teste em staging obrigatorio

### Critical (Score 9-10)
- Cobertura de testes >= 90%
- Testes de carga/stress
- Testes de seguranca completos
- Testes de rollback
- Code review obrigatorio por 2+ pessoas
- Aprovacao de Tech Lead
- Staging deployment obrigatorio
- Janela de deploy definida

---

## Workflow de Correcao

Quando issues sao encontradas, siga este processo:

### 1. Classificar Severidade

| Severidade | Descricao | Acao |
|------------|-----------|------|
| **Blocker** | Impede funcionamento basico | Correcao imediata obrigatoria |
| **Critical** | Vulnerabilidade de seguranca | Correcao antes de merge |
| **Major** | Funcionalidade quebrada | Correcao obrigatoria |
| **Minor** | Code style, documentacao | Recomendado corrigir |
| **Info** | Sugestao de melhoria | Opcional |

### 2. Priorizar

Ordene por prioridade: Blocker > Critical > Major > Minor > Info

### 3. Aplicar Correcoes

```bash
# Aplicar correcoes automaticas (safe mode)
./vendor/bin/pint

# Re-executar validacao
./vendor/bin/phpstan analyse
./vendor/bin/pest
```

### 4. Verificar Regressoes

- Todos os testes existentes passando
- Funcionalidades adjacentes nao afetadas
- Documentacao atualizada

> **Detalhes do workflow:** `references/fix-workflow.md`

---

## Formato de Output

### Relatorio Resumido

```
+===============================================================+
| QA VALIDATION REPORT                                          |
+===============================================================+
| Project: laravel-app                                          |
| Branch: feature/user-dashboard                                |
| Complexity: MEDIUM (Score: 6/10)                              |
+===============================================================+
| PHASE RESULTS                                                 |
+===============================================================+
| Phase 0: Scope Analysis     [PASS]                            |
| Phase 1: Syntax            [PASS]                            |
| Phase 2: Static Analysis   [FAIL]  (3 issues)                |
| Phase 3: Security          [PASS]                            |
| Phase 4: Unit Tests        [FAIL]  (2 failures)              |
| Phase 5: Integration       [SKIP]                            |
| Phase 6: Performance       [WARN]  (1 N+1 detected)          |
| Phase 7-10:                [SKIP]                            |
+===============================================================+
| ISSUES: 0 Blocker, 0 Critical, 5 Major, 3 Minor              |
| STATUS: BLOCKED                                               |
| ACTION: Fix 5 Major issues before proceeding                  |
+===============================================================+
```

### Issue Detalhada

```markdown
## Issue #1: Missing return type

**Fase:** 2 (Static Analysis)
**Severidade:** Major
**Arquivo:** app/Services/UserService.php:45

**Problema:**
Method "getUserName()" has no return type declaration.

**Solucao:**
public function getUserName(int $userId): string
{
    return User::findOrFail($userId)->name;
}

**Auto-fixable:** Sim
```

> **Detalhes do validador:** `references/validation-fixer.md`

---

## Prompt de Validacao QA

Use este prompt quando precisar validar codigo:

```
Voce e um QA Reviewer Agent. Execute validacao completa de QA.

## CONTEXTO

- Arquivos modificados: [lista de arquivos]
- Branch: [nome da branch]
- Tipo de mudanca: [feature/bugfix/refactor]

## SUA TAREFA

1. **Avaliar Complexidade**
   - Contar arquivos afetados
   - Avaliar complexidade logica
   - Determinar tier (trivial/low/medium/high/critical)

2. **Executar Fases de QA**
   - Fase 0-10 em sequencia
   - Parar em caso de FAIL blocker
   - Documentar cada resultado

3. **Reportar Issues**
   - Classificar por severidade
   - Sugerir correcoes
   - Indicar auto-fixable issues

4. **Gerar Relatorio**
   - Status final: PASS/FAIL/BLOCKED
   - Acao requerida
   - Proximos passos

## FORMATO DE OUTPUT

Use o formato padrao de relatorio QA.
```

---

## Comandos Rapidos

```bash
# Validacao completa
./vendor/bin/phpstan analyse && ./vendor/bin/pest && ./vendor/bin/pint --test

# Apenas sintaxe e analise estatica
find . -name "*.php" -not -path "./vendor/*" -exec php -l {} \; && ./vendor/bin/phpstan analyse

# Testes com cobertura
./vendor/bin/pest --coverage --min=80

# Correcao automatica de estilo
./vendor/bin/pint

# Auditoria de seguranca
composer audit && ./vendor/bin/phpstan analyse --level=8
```

---

## Integracao com Git Hooks

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running QA checks..."

# Syntax
php -l $(git diff --cached --name-only -- '*.php') 2>/dev/null

# Style
./vendor/bin/pint --dirty --test

# Quick tests
./vendor/bin/pest --parallel --stop-on-failure
```

### Pre-push Hook

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "Running full QA validation..."

# Full static analysis
./vendor/bin/phpstan analyse

# All tests
./vendor/bin/pest --coverage --min=70
```

---

## Referencias

- `references/complexity-assessment.md` - Tiers e criterios de complexidade detalhados
- `references/qa-phases.md` - Todas as fases de QA com checklists completos
- `references/fix-workflow.md` - Processo de correcao e templates
- `references/validation-fixer.md` - Agente de validacao e interface

---

## Convencoes

- Usar portugues brasileiro em relatorios
- Documentar todas as issues encontradas
- Manter rastreabilidade de correcoes
- Sempre verificar regressoes apos correcoes
- Priorizar issues por severidade
