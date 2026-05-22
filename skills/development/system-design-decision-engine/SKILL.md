---
name: system-design-decision-engine
description: >
  Motor de decisão para System Design. Use quando a pessoa usuária pedir para
  desenhar, decidir, revisar ou defender uma arquitetura. O foco é identificar
  padrões recorrentes, exigir perguntas obrigatórias, forçar decisões explícitas,
  explicitar trade offs e consolidar uma proposta coerente para entrevista ou produção.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
user-invocable: true
---

# System Design Decision Engine

## Objetivo

Você não vai responder apenas explicando conceitos. Você vai conduzir uma decisão
arquitetural com rigor. A saída final deve seguir o contrato em
[reference-output-contract.md](reference-output-contract.md).

## Regras obrigatórias

1. Não assumir requisitos não declarados.
2. Ambiguidade gera pergunta objetiva, não inferência.
3. Toda decisão deve estar ligada a pelo menos um padrão ativado.
4. Todo padrão ativado exige ao menos uma decisão explícita.
5. Não listar tecnologias sem justificar com requisitos e trade offs.
6. Se a pessoa usuária pedir evidência, use o RAG local e cite a fonte do trecho.

## Como esta Skill trabalha

Esta Skill usa 7 padrões recorrentes. A definição de sinais, perguntas e decisões
está em JSON em `data/patterns/`. Veja o resumo em
[reference-patterns.md](reference-patterns.md).

Fluxo de trabalho.

Etapa 1. Detectar padrões a partir do enunciado
Execute:
python3 .claude/skills/system-design-decision-engine/scripts/detect_patterns.py "<texto do problema>"

Etapa 2. Gerar perguntas obrigatórias por padrão ativado
Execute:
python3 .claude/skills/system-design-decision-engine/scripts/generate_questions.py "<lista de ids de padrões>"

Etapa 3. Conduzir perguntas até reduzir ambiguidade
Você deve perguntar primeiro as perguntas obrigatórias. Se a pessoa usuária não souber,
ofereça 2 ou 3 cenários e explique o que muda nas decisões.

Etapa 4. Consolidar arquitetura
Você vai produzir a resposta final seguindo o contrato em
[reference-output-contract.md](reference-output-contract.md).
Você deve incluir, para cada padrão ativado:
- por que ativou
- decisões tomadas
- alternativas descartadas
- trade offs assumidos
- riscos e falhas comuns

## RAG local

O RAG é opcional e só pode ser usado nestes casos:
- pessoa usuária pediu fonte ou evidência
- subagent tradeoff-challenger sinalizou justificativa fraca

Política completa em:
[reference-rag-policy.md](reference-rag-policy.md)

Ingestão do corpus local:
python3 .claude/skills/system-design-decision-engine/scripts/rag_ingest.py

Busca no corpus:
python3 .claude/skills/system-design-decision-engine/scripts/rag_search.py "<consulta>"

## Arquivos de referência

- Padrões e como ativam: [reference-patterns.md](reference-patterns.md)
- Contrato de saída: [reference-output-contract.md](reference-output-contract.md)
- Política de RAG: [reference-rag-policy.md](reference-rag-policy.md)
- Trade-offs consolidados: [tradeoffs.md](tradeoffs.md)
- Fontes e materiais: [reference.md](reference.md)

## Referencias do Engineering Playbook

Decisoes devem considerar:
- `\.agentic_sdlc/docs/engineering-playbook/manual-desenvolvimento/principios.md` - Principios orientadores
- `\.agentic_sdlc/docs/engineering-playbook/stacks/devops/security.md` - Threat modeling (STRIDE)

## Padrões Detalhados (Markdown)

Para explicações detalhadas de cada padrão, consulte:

| Padrão | Sinais | Arquivo |
|--------|--------|---------|
| Contencao | Concorrência, estoque, reservas | [patterns/contention.md](patterns/contention.md) |
| Scaling Reads | Alta leitura, latência sensível | [patterns/scaling-reads.md](patterns/scaling-reads.md) |
| Scaling Writes | Alta escrita, picos | [patterns/scaling-writes.md](patterns/scaling-writes.md) |
| Real-time | Notificações, estado compartilhado | [patterns/real-time-updates.md](patterns/real-time-updates.md) |
| Large Files | Upload/download grandes | [patterns/large-files.md](patterns/large-files.md) |
| Long Running | Operações demoradas | [patterns/long-running-tasks.md](patterns/long-running-tasks.md) |
| Multi-step | Fluxos com etapas | [patterns/multi-step-processes.md](patterns/multi-step-processes.md) |

## Scripts Utilitários

### Detecção e Perguntas (Workflow)

```bash
# Detectar padrões no problema
python scripts/detect_patterns.py "sistema de reserva de ingressos"

# Gerar perguntas obrigatórias
python scripts/generate_questions.py "contention,scaling-writes"
```

### Estimativas, Diagramas e Checklists

**⚠️ v3.0.0 Update:** Scripts de geração removidos (Natural Language First principle).

Use natural language para:
- **Estimativas**: Peça a Claude para calcular capacidade, bandwidth, QPS baseado em requisitos
- **Diagramas Mermaid**: Peça a Claude para gerar diagramas específicos do seu contexto
- **Checklists**: Peça a Claude para criar checklist de decisões baseado em padrões ativados

Claude faz melhor que scripts estáticos porque adapta ao contexto específico do projeto.

## Subagents Disponíveis

Esta skill trabalha com 4 subagents especializados em `.claude/agents/`:

| Agent | Função | Quando usar |
|-------|--------|-------------|
| `requirements-interrogator` | Elimina ambiguidade | Faltam números, limites, requisitos |
| `tradeoff-challenger` | Ataca decisões fracas | Escolhas sem justificativa |
| `failure-analyst` | Analisa resiliência | Filas, jobs, pontos de falha |
| `interview-simulator` | Simula entrevista | Treinar defesa do design |
