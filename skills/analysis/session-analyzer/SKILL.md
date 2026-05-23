---
name: session-analyzer
description: |
  Analisa sessoes do Claude Code para extrair learnings e persistir conhecimento.
  Le arquivos de sessao em ~/.claude/projects/ e extrai decisoes, bloqueios e resolucoes.
  Invocado automaticamente pelo gate-check e orchestrator.
  Use quando: fim de fase, retrospectiva, analise de progresso.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
user-invocable: true
version: "1.1.0"
---

# Session Analyzer Skill

## Proposito

Esta skill analisa sessoes do Claude Code para:

1. **Extrair decisoes** - Identificar escolhas feitas durante a sessao
2. **Capturar bloqueios** - Registrar problemas encontrados e como foram resolvidos
3. **Persistir learnings** - Salvar conhecimento em `.project/sessions/`
4. **Alimentar RAG** - Adicionar ao corpus para consultas futuras

## Scripts Disponíveis

**⚠️ v3.0.0 Update:** Wrapper `analyze.sh` removido (Natural Language First principle).

Use diretamente:

### extract_learnings.py

```bash
# Uso direto do Python
python3 .claude/skills/session-analyzer/scripts/extract_learnings.py

# Com opções
python3 .claude/skills/session-analyzer/scripts/extract_learnings.py \
  --session-id <uuid> \
  --persist \
  --project /path/to/project
```

## Integração Automática

### Com gate-check

O gate-check invoca session-analyzer automaticamente após aprovação:

```bash
# Em gate-check.md
if [ $RESULT -eq 0 ]; then
    # Extrair learnings
    python3 .claude/skills/session-analyzer/scripts/analyze.py --extract-learnings
fi
```

### Com orchestrator

O orchestrator invoca ao fim de cada fase:

```yaml
on_phase_complete:
  - call: session-analyzer
    when: phase_completed
    persist: true
```

### Com memory-manager

Learnings são persistidos automaticamente:

```yaml
on_learning_found:
  - persist_to: .project/corpus/learnings/
  - update: rag_index
```

## Localizacao das Sessoes

Claude Code armazena sessoes em:

```
~/.claude/projects/{path-encoded}/{session-uuid}.jsonl
```

Onde `{path-encoded}` e o path do projeto com `/` substituido por `-`.

Exemplo:
- Projeto: `/home/user/source/repos/meu-projeto`
- Encoded: `-home-user-source-repos-meu-projeto`

## Formato dos Arquivos de Sessao

Arquivos JSONL (uma linha JSON por evento):

```json
{"type": "user", "content": "mensagem do usuario"}
{"type": "assistant", "content": "resposta do Claude"}
{"type": "tool_use", "name": "Bash", "params": {...}}
{"type": "tool_result", "output": "..."}
{"type": "thinking", "content": "raciocinio interno"}
```

## Tipos de Eventos Relevantes

| Tipo | O que Extrair |
|------|---------------|
| `user` | Requisitos, perguntas, contexto |
| `assistant` | Decisoes, explicacoes, sugestoes |
| `tool_use` | Comandos executados, arquivos criados |
| `thinking` | Raciocinio, trade-offs considerados |

## Processo de Analise

```yaml
session_analysis_process:
  1_locate_session:
    - Encontrar diretorio do projeto em ~/.claude/projects/
    - Listar arquivos .jsonl
    - Ordenar por data de modificacao

  2_parse_session:
    - Ler arquivo JSONL linha por linha
    - Extrair eventos relevantes
    - Agrupar por tipo

  3_identify_patterns:
    - Buscar decisoes (palavras-chave: "decidi", "escolhi", "vou usar")
    - Buscar bloqueios (palavras-chave: "erro", "falhou", "problema")
    - Buscar resolucoes (palavras-chave: "resolvido", "funcionou", "corrigido")

  4_generate_summary:
    - Criar resumo da sessao
    - Listar decisoes tomadas
    - Listar learnings identificados

  5_persist_results:
    - Salvar em .project/sessions/
    - Atualizar RAG corpus se relevante
    - Vincular ao projeto/fase
```

## Formato de Output

```yaml
# .project/sessions/session-{date}-{uuid-short}.yml
session_analysis:
  id: string
  analyzed_at: datetime
  source_file: string
  project_path: string

  summary:
    duration_estimate: string
    messages_count: number
    tools_used: list[string]

  decisions:
    - type: [architectural | technical | process]
      description: string
      context: string
      confidence: [high | medium | low]

  blockers:
    - description: string
      resolution: string
      time_to_resolve: string (estimated)

  learnings:
    - type: [pattern | anti-pattern | best-practice | gotcha]
      description: string
      applicable_to: list[string]

  artifacts_created:
    - path: string
      type: string

  next_steps:
    - description: string
      priority: [high | medium | low]
```

## Palavras-chave para Deteccao

### Decisoes
```python
DECISION_KEYWORDS = [
    "decidi", "escolhi", "vou usar", "optei por",
    "a melhor opcao", "faz mais sentido", "vamos com",
    "prefiro", "recomendo", "sugiro"
]
```

### Bloqueios
```python
BLOCKER_KEYWORDS = [
    "erro", "falhou", "problema", "nao funcionou",
    "bug", "issue", "bloqueado", "travado",
    "nao consegui", "impossivel"
]
```

### Resolucoes
```python
RESOLUTION_KEYWORDS = [
    "resolvido", "funcionou", "corrigido", "sucesso",
    "consegui", "pronto", "finalizado", "ok"
]
```

### Learnings
```python
LEARNING_KEYWORDS = [
    "aprendi", "descobri", "percebi", "entendi",
    "importante notar", "lembre-se", "dica",
    "evite", "sempre", "nunca"
]
```

## Integracao

### Com Orchestrator
```yaml
on_phase_complete:
  - call: session-analyzer
    when: phase_completed
    persist: true
```

### Com Memory Manager
```yaml
on_learning_found:
  - persist_to: .project/corpus/learnings/
  - update: rag_index
```

### Com Gate Evaluator
```yaml
on_gate_pass:
  - analyze_session: true
  - extract_learnings: true
```

## Script Python

O script `extract_learnings.py` implementa a logica de extracao.

## Uso Manual

```bash
# Analisar sessao mais recente do projeto atual
python3 .claude/skills/session-analyzer/extract_learnings.py

# Analisar sessao especifica
python3 .claude/skills/session-analyzer/extract_learnings.py --session-id <uuid>

# Analisar e persistir
python3 .claude/skills/session-analyzer/extract_learnings.py --persist
```

## Limitacoes

- Sessoes grandes podem demorar para analisar
- Deteccao de patterns e heuristica, nao 100% precisa
- Informacoes sensiveis devem ser filtradas antes de persistir

## Session Handoff Summaries (v2.0)

### Propósito

Gera resumos estruturados ao fim de cada sessão para facilitar continuidade entre sessões.
Adaptado do claude-orchestrator para o SDLC Agêntico.

### Uso

```bash
# Gerar handoff da sessão mais recente
python3 .claude/skills/session-analyzer/scripts/handoff.py

# Especificar projeto
python3 .claude/skills/session-analyzer/scripts/handoff.py --project /path/to/project

# Especificar arquivo de saída
python3 .claude/skills/session-analyzer/scripts/handoff.py --output custom-summary.md

# Modo silencioso (sem preview)
python3 .claude/skills/session-analyzer/scripts/handoff.py --quiet
```

### Estrutura do Handoff

```markdown
# Session Summary: YYYY-MM-DD - repository

## Session Metadata
- Date, session file, repo, phase

## Completed
- [tasks that were completed]

## Pending
- [tasks still pending]

## Context for Next Session
- Current phase
- Files modified
- Tools used
- Decisions made
- Blockers
- Notes
```

### Integração Automática

O handoff é gerado automaticamente:
- **Hook**: `session-analyzer.sh` invoca `handoff.py` após gate-check
- **Timing**: Ao fim de cada fase (gate passage)
- **Output**: `.project/sessions/YYYYMMDD-HHMMSS-{repo}.md`

### Exemplo

Ver `.claude/skills/session-analyzer/templates/handoff-example.md`

## Checklist

### Antes da Analise
- [ ] Verificar se sessao existe
- [ ] Confirmar projeto correto
- [ ] Verificar espaco em disco para output

### Apos a Analise
- [ ] Revisar learnings extraidos
- [ ] Validar decisoes identificadas
- [ ] Adicionar ao RAG se relevante
- [ ] Revisar handoff summary para proxima sessao
