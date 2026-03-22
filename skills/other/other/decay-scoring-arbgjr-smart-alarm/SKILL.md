---
name: decay-scoring
description: |
  Sistema de scoring temporal para nodes de conhecimento do corpus RAG.
  Calcula scores de obsolescencia baseado em idade, validacao e acesso.
  Gera sugestoes de curadoria para conteudo desatualizado.
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
user-invocable: false
version: "1.0.0"
---

# Decay Scoring Skill

Sistema de pontuacao temporal automatica para nodes de conhecimento do corpus RAG.

## Objetivo

Explicitar obsolescencia, priorizar revisao e preferir conteudo recente ou validado recentemente.

## Algoritmo de Decay

```
decay_score = w_age * age_score + w_val * validation_score + w_access * access_score + w_type * type_bonus

Onde:
- w_age = 0.40 (peso da idade)
- w_val = 0.30 (peso da validacao)
- w_access = 0.20 (peso do acesso)
- w_type = 0.10 (bonus por tipo de conteudo)
```

### Componentes

1. **Age Score (Decaimento Exponencial):**
   ```
   age_score = exp(-lambda * dias_desde_criacao)
   lambda = ln(2) / half_life_dias
   ```

2. **Validation Score:**
   ```
   validation_score = exp(-lambda_val * dias_desde_validacao)
   lambda_val = ln(2) / 90  # Half-life de 90 dias
   ```

3. **Access Score:**
   ```
   access_score = min(1.0, log(1 + acessos_30d) / log(10)) * fator_recencia
   ```

4. **Type Bonus:**
   - concepts: 1.0 (mais estavel)
   - patterns: 0.9
   - decisions: 0.7
   - learnings: 0.5

### Thresholds de Status

| Score | Status | Acao |
|-------|--------|------|
| 0.70-1.00 | `fresh` | Nenhuma acao |
| 0.40-0.69 | `aging` | Considerar validacao |
| 0.20-0.39 | `stale` | Revisao recomendada |
| 0.00-0.19 | `obsolete` | Curadoria necessaria |

## Scripts

### decay_calculator.py

Calcula scores de decay para todos os nodes do corpus.

```bash
# Calcular scores
python3 .claude/skills/decay-scoring/scripts/decay_calculator.py

# Atualizar nodes com scores
python3 .claude/skills/decay-scoring/scripts/decay_calculator.py --update-nodes

# Output JSON
python3 .claude/skills/decay-scoring/scripts/decay_calculator.py --json
```

### decay_tracker.py

Rastreia acessos e validacoes de nodes.

```bash
# Registrar acesso
python3 .claude/skills/decay-scoring/scripts/decay_tracker.py access NODE_ID

# Registrar validacao
python3 .claude/skills/decay-scoring/scripts/decay_tracker.py validate NODE_ID

# Ver estatisticas
python3 .claude/skills/decay-scoring/scripts/decay_tracker.py stats
```

### decay_trigger.py

Gera sugestoes de curadoria baseadas nos scores.

```bash
# Gerar relatorio
python3 .claude/skills/decay-scoring/scripts/decay_trigger.py

# Filtrar por prioridade
python3 .claude/skills/decay-scoring/scripts/decay_trigger.py --priority critical
```

## Integracao

- **memory-manager**: Adiciona contexto de decay ao recuperar informacoes
- **rag-curator**: Usa triggers para sugerir acoes de curadoria
- **hybrid_search.py**: Aplica boost de decay nos resultados de busca
- **gate-evaluator**: Valida saude do corpus antes de releases

## Configuracao

Ver `config/decay_config.yml` para ajustar pesos, thresholds e half-lives.
