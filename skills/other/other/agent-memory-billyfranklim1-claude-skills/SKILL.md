---
name: agent-memory
description: Persistent semantic memory for the agent. Use to save facts, patterns, and important decisions during interactions, and to retrieve relevant context. Always use when identifying a new pattern, a user decision, or a fact that must persist across sessions.
---

# Agent Memory — Memória Semântica

Banco SQLite em `~/.claude/memory/brain.db`. Busca por palavras-chave com ranking por importância e frequência de acesso.

## Quando usar

- **Salvar**: Ao detectar um padrão recorrente, decisão do the owner, gotcha técnico, ou fato crítico
- **Buscar**: Antes de agir em algo que pode ter histórico ("já vimos esse erro antes?")
- **Listar**: Para revisar o que sei sobre um projeto específico

## Comandos

```bash
# Salvar uma memória
python3 ~/.claude/memory/brain.py add "fato importante" \
  --tags "tag1,tag2" \
  --project "news|myapp|work8|infra|geral" \
  --importance 3  # 1=baixa, 2=média, 3=crítica

# Buscar por keywords
python3 ~/.claude/memory/brain.py search "horizon parou"
python3 ~/.claude/memory/brain.py search "deploy myapp"

# Listar por projeto
python3 ~/.claude/memory/brain.py list --project news
python3 ~/.claude/memory/brain.py list --tag padrão

# Remover memória obsoleta
python3 ~/.claude/memory/brain.py forget 42

# Estatísticas
python3 ~/.claude/memory/brain.py stats
```

## Tags recomendadas

| Tag | Quando usar |
|-----|-------------|
| `padrão` | Comportamento recorrente identificado |
| `decisão` | Escolha explícita do the owner |
| `crítico` | Regra que NUNCA deve ser violada |
| `erro` | Bug ou falha conhecida com solução |
| `deploy` | Procedimento de deploy específico |
| `segurança` | Configuração ou regra de segurança |
| `schema` | Estrutura de banco de dados |
| `incidente` | Problema que aconteceu em produção |

## Projetos

`news` | `myapp` | `work8` | `neuralnets` | `infra` | `geral`

## Importância

- **3 (🔴 crítica)**: Regras que não podem ser violadas, segurança, decisões imutáveis
- **2 (🟡 média)**: Padrões úteis, procedimentos, gotchas técnicos
- **1 (🔵 baixa)**: Preferências, notas, contexto auxiliar

## Comportamento automático

Ao final de qualquer sessão com aprendizados novos, salvar automaticamente usando `add`.
Ao iniciar trabalho em um projeto, buscar o contexto com `search "nome-do-projeto"`.
