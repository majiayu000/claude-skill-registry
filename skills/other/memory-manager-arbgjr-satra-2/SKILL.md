---
name: memory-manager
description: |
  Gerencia persistencia de contexto, decisoes e learnings do projeto.
  Armazena e recupera informacoes entre sessoes para manter continuidade.
  Use quando: salvar decisoes, recuperar contexto, persistir learnings.
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
user-invocable: false
---

# Memory Manager Skill

## Proposito

Esta skill gerencia a memoria persistente do projeto, incluindo:

1. **Contexto de projeto** - Estado atual, fase, configuracoes
2. **Decisoes** - ADRs, escolhas tecnicas, trade-offs
3. **Learnings** - Licoes aprendidas, padroes identificados
4. **Artefatos** - Referencias a documentos gerados

## Estrutura de Armazenamento

**IMPORTANTE:** A partir da v1.2.0, todos os artefatos devem ser salvos em `.agentic_sdlc/`.
O diretorio `.claude/memory/` e legado e sera migrado automaticamente.

```
.agentic_sdlc/
├── projects/
│   └── {project-id}/
│       ├── manifest.yml         # Estado do projeto (antigo project.yml)
│       ├── decisions/           # ADRs e decisoes
│       │   ├── adr-001.yml
│       │   ├── adr-002.yml
│       │   └── index.yml
│       ├── phases/              # Contexto por fase
│       │   ├── phase-0.yml
│       │   ├── phase-1.yml
│       │   └── ...
│       ├── specs/               # Especificacoes
│       ├── security/            # Threat models, scans
│       └── docs/                # Documentacao gerada
├── corpus/
│   ├── decisions/               # Decisoes indexadas para RAG
│   ├── learnings/               # Licoes aprendidas
│   ├── docs/                    # Documentacao pesquisavel
│   └── research/                # Pesquisas de dominio
├── sessions/                    # Historico de sessoes analisadas
├── references/                  # Documentos de referencia externos
└── templates/                   # Templates reutilizaveis
```

### Migracao Automatica

O hook `auto-migrate.sh` migra automaticamente de `.claude/memory/` para `.agentic_sdlc/` na primeira execucao de cada dia.

## Schema de Dados

### Project State

```yaml
# project.yml
project:
  id: string
  name: string
  created_at: datetime
  updated_at: datetime

  current_phase: number (0-8)
  complexity_level: number (0-3)
  status: [active | paused | completed]

  team:
    - name: string
      role: string

  metrics:
    phase_durations: object
    decisions_count: number
    odrs_count: number       # ODRs organizacionais
    learnings_count: number

  tags: list[string]
```

### Organizational Decision Record (ODR)

ODRs documentam decisões organizacionais/negócio, diferente de ADRs que são técnicos.
Veja `.docs/guides/adr-vs-odr.md` para guia completo.

```yaml
# decisions/odr-NNN.yml
odr:
  id: string               # ODR-001, ODR-002, etc
  title: string
  created_at: datetime
  updated_at: datetime
  status: [draft | pending_input | pending_approval | approved | rejected | superseded]
  deadline: datetime | null

  business_context: string

  stakeholders:
    decision_maker:
      name: string
      role: string
    consulted:
      - name: string
        role: string
        input_status: [pending | received | waived]
        input: string
    informed:
      - name: string
        role: string

  alternatives:
    - id: string           # A, B, C, etc
      title: string
      description: string
      pros: list[string]
      cons: list[string]
      estimated_cost: string
      risk_level: [low | medium | high]

  trade_offs:
    - description: string
      gain: string
      loss: string
      assessment: [acceptable | unacceptable | requires_mitigation]
      mitigation: string | null

  decision:
    chosen_alternative: string
    description: string
    rationale: string

  consequences:
    positive: list[string]
    negative: list[string]
    risks:
      - description: string
        probability: [low | medium | high]
        impact: [low | medium | high]
        mitigation: string

  approvals:
    - stakeholder: string
      approved: boolean | null
      approved_at: datetime | null
      comments: string

  relationships:
    related_odrs: list[string]
    derived_adrs: list[string]  # ADRs técnicos que derivam deste ODR
    related_issues: list[string]
    sdlc_phase: number | null

  metadata:
    category: [business | resource | timeline | scope | strategic]
    impact_level: [low | medium | high | critical]
    reversible: boolean
    project_id: string | null
    tags: list[string]
```

### Decision Record (ADR)

ADRs documentam decisões técnicas/arquiteturais.

```yaml
# decisions/adr-NNN.yml
decision:
  id: string
  type: [architectural | technical | process | tool]
  title: string
  created_at: datetime
  status: [proposed | accepted | rejected | superseded]

  context: string
  decision: string
  consequences:
    positive: list[string]
    negative: list[string]
    risks: list[string]

  related_decisions: list[string]
  phase: number
  author: string
  approvers: list[string]

  metadata:
    complexity: [low | medium | high]
    reversible: boolean
    cost_impact: string
```

### Learning Record

```yaml
# learnings/learning-NNN.yml
learning:
  id: string
  type: [incident | retrospective | discovery | pattern]
  title: string
  created_at: datetime

  source:
    type: [incident | project | research]
    reference: string

  insight: string
  actions:
    - action: string
      status: [pending | in_progress | completed]
      owner: string

  applicable_to: list[string]
  tags: list[string]
```

### Phase Context

```yaml
# context/phase-N.yml
phase_context:
  phase: number
  name: string
  started_at: datetime
  completed_at: datetime

  inputs:
    - type: string
      source: string

  outputs:
    - type: string
      path: string

  decisions: list[string]
  blockers: list[string]
  notes: string

  gate_result:
    passed: boolean
    score: float
    issues: list[string]
```

## Operacoes

### Salvar Contexto

```python
save_context(
    phase=2,
    data={
        "inputs": [...],
        "outputs": [...],
        "decisions": ["adr-001"],
        "notes": "Requisitos definidos com stakeholders"
    }
)
```

### Recuperar Contexto

```python
context = load_context(phase=2)
# Retorna o contexto completo da fase 2
```

### Registrar Decisao

```python
decision_id = save_decision(
    type="architectural",
    title="Usar PostgreSQL como banco principal",
    context="Precisamos de um banco relacional com suporte a JSON",
    decision="PostgreSQL com extensao JSONB",
    consequences={
        "positive": ["Flexibilidade de schema", "Boa performance"],
        "negative": ["Curva de aprendizado"],
        "risks": ["Lock-in no PostgreSQL"]
    }
)
```

### Registrar Learning

```python
learning_id = save_learning(
    type="incident",
    title="Timeout em queries complexas",
    source={"type": "incident", "reference": "INC-123"},
    insight="Queries com mais de 3 joins precisam de indices compostos",
    actions=[
        {"action": "Criar indice composto", "owner": "DBA"}
    ]
)
```

### Buscar Decisoes

```python
decisions = search_decisions(
    phase=3,
    type="architectural",
    status="accepted"
)
```

### Buscar Learnings

```python
learnings = search_learnings(
    type="incident",
    tags=["performance"]
)
```

## Integracao com RAG

O memory-manager alimenta o corpus RAG:

1. Novas decisoes sao indexadas automaticamente
2. Learnings sao adicionados ao corpus
3. Contexto de fases fica disponivel para consulta

## Scripts Utilitarios

### memory_ops.py

```python
#!/usr/bin/env python3
"""
Operacoes de memoria para o SDLC.
v1.2.0 - Usa .agentic_sdlc como diretorio principal
"""
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
import os

# Diretorio principal (v1.2.0+)
AGENTIC_SDLC_DIR = Path(".agentic_sdlc")
# Diretorio legado (para compatibilidade)
LEGACY_MEMORY_DIR = Path(".claude/memory")

def get_project_dir(project_id: str = None) -> Path:
    """Retorna diretorio do projeto atual."""
    if project_id is None:
        # Tentar obter do manifest ou project.yml
        project_id = get_current_project_id()
    return AGENTIC_SDLC_DIR / "projects" / project_id

def get_current_project_id() -> str:
    """Obtem ID do projeto atual."""
    # Verificar .agentic_sdlc primeiro
    current_file = AGENTIC_SDLC_DIR / ".current-project"
    if current_file.exists():
        return current_file.read_text().strip()

    # Fallback para .claude/memory
    if (LEGACY_MEMORY_DIR / "project.yml").exists():
        with open(LEGACY_MEMORY_DIR / "project.yml") as f:
            data = yaml.safe_load(f)
            return data.get("project", {}).get("id", "default")

    return "default"

def get_memory_dir(project_id: str = None) -> Path:
    """Retorna diretorio de memoria do projeto."""
    return get_project_dir(project_id)

def ensure_structure():
    """Garante que a estrutura de diretorios existe."""
    dirs = ["decisions", "learnings", "context", "sessions"]
    for d in dirs:
        (MEMORY_DIR / d).mkdir(parents=True, exist_ok=True)

def load_project() -> Dict[str, Any]:
    """Carrega estado do projeto."""
    project_file = MEMORY_DIR / "project.yml"
    if not project_file.exists():
        return {
            "project": {
                "id": None,
                "current_phase": 0,
                "complexity_level": 2,
                "status": "active",
                "metrics": {}
            }
        }
    with open(project_file) as f:
        return yaml.safe_load(f)

def save_project(data: Dict[str, Any]):
    """Salva estado do projeto."""
    ensure_structure()
    data["project"]["updated_at"] = datetime.now().isoformat()
    with open(MEMORY_DIR / "project.yml", "w") as f:
        yaml.dump(data, f, default_flow_style=False)

def get_next_decision_id() -> str:
    """Gera proximo ID de decisao."""
    index_file = MEMORY_DIR / "decisions" / "index.yml"
    if index_file.exists():
        with open(index_file) as f:
            index = yaml.safe_load(f) or {"last_id": 0}
    else:
        index = {"last_id": 0}
    next_id = index["last_id"] + 1
    index["last_id"] = next_id
    with open(index_file, "w") as f:
        yaml.dump(index, f)
    return f"adr-{next_id:03d}"

def save_decision(
    type: str,
    title: str,
    context: str,
    decision: str,
    consequences: Dict[str, List[str]],
    phase: int,
    author: str = "claude"
) -> str:
    """Salva uma nova decisao."""
    ensure_structure()
    decision_id = get_next_decision_id()

    data = {
        "decision": {
            "id": decision_id,
            "type": type,
            "title": title,
            "created_at": datetime.now().isoformat(),
            "status": "proposed",
            "context": context,
            "decision": decision,
            "consequences": consequences,
            "phase": phase,
            "author": author,
            "related_decisions": [],
            "approvers": [],
            "metadata": {
                "complexity": "medium",
                "reversible": True
            }
        }
    }

    with open(MEMORY_DIR / "decisions" / f"{decision_id}.yml", "w") as f:
        yaml.dump(data, f, default_flow_style=False)

    return decision_id

def load_decision(decision_id: str) -> Optional[Dict]:
    """Carrega uma decisao por ID."""
    decision_file = MEMORY_DIR / "decisions" / f"{decision_id}.yml"
    if not decision_file.exists():
        return None
    with open(decision_file) as f:
        return yaml.safe_load(f)

def save_phase_context(phase: int, data: Dict[str, Any]):
    """Salva contexto de uma fase."""
    ensure_structure()
    context_file = MEMORY_DIR / "context" / f"phase-{phase}.yml"

    context = {
        "phase_context": {
            "phase": phase,
            "updated_at": datetime.now().isoformat(),
            **data
        }
    }

    with open(context_file, "w") as f:
        yaml.dump(context, f, default_flow_style=False)

def load_phase_context(phase: int) -> Optional[Dict]:
    """Carrega contexto de uma fase."""
    context_file = MEMORY_DIR / "context" / f"phase-{phase}.yml"
    if not context_file.exists():
        return None
    with open(context_file) as f:
        return yaml.safe_load(f)

def save_learning(
    type: str,
    title: str,
    insight: str,
    source: Dict[str, str],
    actions: List[Dict] = None,
    tags: List[str] = None
) -> str:
    """Salva um novo learning."""
    ensure_structure()

    learnings_dir = MEMORY_DIR / "learnings"
    existing = list(learnings_dir.glob("learning-*.yml"))
    next_num = len(existing) + 1
    learning_id = f"learning-{next_num:03d}"

    data = {
        "learning": {
            "id": learning_id,
            "type": type,
            "title": title,
            "created_at": datetime.now().isoformat(),
            "source": source,
            "insight": insight,
            "actions": actions or [],
            "applicable_to": [],
            "tags": tags or []
        }
    }

    with open(learnings_dir / f"{learning_id}.yml", "w") as f:
        yaml.dump(data, f, default_flow_style=False)

    return learning_id

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["init", "status", "list-decisions"])
    args = parser.parse_args()

    if args.action == "init":
        ensure_structure()
        print("Memory structure initialized")
    elif args.action == "status":
        project = load_project()
        print(yaml.dump(project, default_flow_style=False))
    elif args.action == "list-decisions":
        decisions_dir = MEMORY_DIR / "decisions"
        for f in decisions_dir.glob("adr-*.yml"):
            d = yaml.safe_load(f.read_text())
            print(f"{d['decision']['id']}: {d['decision']['title']}")
```

## Checklist de Uso

### Ao Iniciar Sessao
- [ ] Carregar project.yml
- [ ] Identificar fase atual
- [ ] Carregar contexto da fase

### Ao Tomar Decisao
- [ ] Registrar decisao com contexto
- [ ] Vincular a fase atual
- [ ] Notificar para aprovacao se necessario

### Ao Aprender Algo
- [ ] Registrar learning com fonte
- [ ] Definir acoes se aplicavel
- [ ] Adicionar tags para busca

### Ao Mudar de Fase
- [ ] Salvar contexto da fase atual
- [ ] Atualizar project.yml
- [ ] Inicializar contexto da nova fase

## Pontos de Pesquisa

Para melhorar esta skill:
- "knowledge management systems for software development"
- "organizational memory patterns"
- "decision tracking software engineering"
