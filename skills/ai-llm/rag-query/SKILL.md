---
name: rag-query
description: |
  Consulta ao corpus RAG do projeto. Busca conhecimento em decisoes,
  documentacao, learnings e padroes armazenados.
  Use quando: buscar decisoes passadas, encontrar documentacao, recuperar padroes.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
user-invocable: false
---

# RAG Query Skill

## Proposito

Esta skill permite consultar o corpus de conhecimento do projeto para:

1. **Buscar decisoes** - Encontrar ADRs e decisoes tecnicas relevantes
2. **Encontrar documentacao** - Localizar docs oficiais e referencias
3. **Recuperar padroes** - Identificar padroes ja usados no projeto
4. **Acessar learnings** - Consultar licoes aprendidas

## Tipos de Consulta

### 1. Busca por Decisoes

```python
results = query_decisions(
    keywords=["database", "postgresql"],
    phase=3,
    type="architectural",
    limit=5
)
```

### 2. Busca por Documentacao

```python
results = query_docs(
    topic="authentication",
    source=["official", "internal"],
    limit=10
)
```

### 3. Busca por Padroes

```python
results = query_patterns(
    category="resilience",
    tags=["circuit-breaker", "retry"]
)
```

### 4. Busca por Learnings

```python
results = query_learnings(
    type="incident",
    keywords=["timeout", "performance"]
)
```

### 5. Busca Geral

```python
results = query(
    question="Como lidar com falhas de conexao ao banco?",
    sources=["decisions", "learnings", "patterns"],
    limit=5
)
```

## Estrutura do Corpus

O corpus RAG esta consolidado em `.project/corpus/`:

```
.project/corpus/
├── decisions/           # ADRs e decisoes
│   └── *.yml
├── docs/                # Documentacao oficial
│   ├── official/        # Docs de libs/frameworks
│   ├── internal/        # Docs do projeto
│   └── reference/       # Referencias externas
├── patterns/            # Padroes conhecidos
│   └── *.yml
├── learnings/           # Licoes aprendidas
│   └── *.yml
└── index.yml            # Indice do corpus
```

**Nota**: Por compatibilidade, o sistema tambem busca em:
- `.claude/knowledge/` (legado)
- `.claude/memory/` (legado)
- `.project/references/` (documentos externos via reference-indexer)

## Formato de Resultado

```yaml
query_result:
  query: string
  sources_searched: list[string]
  total_results: number

  results:
    - id: string
      type: [decision | doc | pattern | learning]
      title: string
      relevance_score: float (0-1)
      snippet: string
      source_path: string
      metadata:
        created_at: datetime
        tags: list[string]
        phase: number

  suggestions:
    - string
```

## Integracoes

### Com memory-manager

O rag-query le dados salvos pelo memory-manager:
- Decisoes em `.project/corpus/decisions/` (ou `.claude/memory/decisions/` legado)
- Learnings em `.project/corpus/learnings/` (ou `.claude/memory/learnings/` legado)
- Contextos em `.agentic_sdlc/projects/*/context/` (ou `.claude/memory/context/` legado)

### Com rag-curator

O rag-curator adiciona e organiza o corpus que o rag-query consulta.

## Scripts

### query_corpus.py

```python
#!/usr/bin/env python3
"""
Consulta o corpus de conhecimento do projeto.
Suporta paths consolidados (.project/corpus/) e legados (.claude/).
"""
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
import re

# Paths consolidados (preferencia)
CORPUS_DIR = Path(".project/corpus")
PROJECTS_DIR = Path(".agentic_sdlc/projects")
REFERENCES_DIR = Path(".project/references")

# Paths legados (fallback)
KNOWLEDGE_DIR = Path(".claude/knowledge")
MEMORY_DIR = Path(".claude/memory")

def load_all_decisions() -> List[Dict]:
    """Carrega todas as decisoes de paths consolidados e legados."""
    decisions = []

    # Paths consolidados (preferencia)
    corpus_decisions = CORPUS_DIR / "decisions"
    if corpus_decisions.exists():
        for f in corpus_decisions.glob("adr-*.yml"):
            data = yaml.safe_load(f.read_text())
            if data and "decision" in data:
                decisions.append({
                    **data["decision"],
                    "source_path": str(f),
                    "type": "decision"
                })

    # Paths por projeto
    for project_dir in PROJECTS_DIR.glob("*/decisions"):
        for f in project_dir.glob("adr-*.yml"):
            data = yaml.safe_load(f.read_text())
            if data and "decision" in data:
                decisions.append({
                    **data["decision"],
                    "source_path": str(f),
                    "type": "decision"
                })

    # Paths legados (fallback)
    legacy_decisions = MEMORY_DIR / "decisions"
    if legacy_decisions.exists():
        for f in legacy_decisions.glob("adr-*.yml"):
            data = yaml.safe_load(f.read_text())
            if data and "decision" in data:
                decisions.append({
                    **data["decision"],
                    "source_path": str(f),
                    "type": "decision"
                })

    return decisions

def load_all_learnings() -> List[Dict]:
    """Carrega todos os learnings de paths consolidados e legados."""
    learnings = []

    # Paths consolidados (preferencia)
    corpus_learnings = CORPUS_DIR / "learnings"
    if corpus_learnings.exists():
        for f in corpus_learnings.glob("*.yml"):
            data = yaml.safe_load(f.read_text())
            if data and "learning" in data:
                learnings.append({
                    **data["learning"],
                    "source_path": str(f),
                    "type": "learning"
                })

    # Paths por projeto
    for project_dir in PROJECTS_DIR.glob("*/learnings"):
        for f in project_dir.glob("*.yml"):
            data = yaml.safe_load(f.read_text())
            if data and "learning" in data:
                learnings.append({
                    **data["learning"],
                    "source_path": str(f),
                    "type": "learning"
                })

    # Paths legados (fallback)
    legacy_learnings = MEMORY_DIR / "learnings"
    if legacy_learnings.exists():
        for f in legacy_learnings.glob("*.yml"):
            data = yaml.safe_load(f.read_text())
            if data and "learning" in data:
                learnings.append({
                    **data["learning"],
                    "source_path": str(f),
                    "type": "learning"
                })

    return learnings

def calculate_relevance(item: Dict, keywords: List[str]) -> float:
    """Calcula score de relevancia baseado em keywords."""
    text = " ".join([
        str(item.get("title", "")),
        str(item.get("context", "")),
        str(item.get("decision", "")),
        str(item.get("insight", "")),
        " ".join(item.get("tags", []))
    ]).lower()

    if not keywords:
        return 0.5

    matches = sum(1 for kw in keywords if kw.lower() in text)
    return min(matches / len(keywords), 1.0)

def search(
    keywords: List[str] = None,
    sources: List[str] = None,
    type_filter: str = None,
    phase_filter: int = None,
    limit: int = 10
) -> Dict[str, Any]:
    """Busca geral no corpus."""
    keywords = keywords or []
    sources = sources or ["decisions", "learnings"]

    all_items = []

    if "decisions" in sources:
        all_items.extend(load_all_decisions())

    if "learnings" in sources:
        all_items.extend(load_all_learnings())

    # Filtrar por tipo
    if type_filter:
        all_items = [i for i in all_items if i.get("type") == type_filter]

    # Filtrar por fase
    if phase_filter is not None:
        all_items = [i for i in all_items if i.get("phase") == phase_filter]

    # Calcular relevancia
    for item in all_items:
        item["relevance_score"] = calculate_relevance(item, keywords)

    # Ordenar por relevancia
    all_items.sort(key=lambda x: x["relevance_score"], reverse=True)

    # Limitar resultados
    results = all_items[:limit]

    return {
        "query": " ".join(keywords),
        "sources_searched": sources,
        "total_results": len(results),
        "results": [
            {
                "id": r.get("id"),
                "type": r.get("type"),
                "title": r.get("title"),
                "relevance_score": r.get("relevance_score"),
                "snippet": r.get("context", r.get("insight", ""))[:200],
                "source_path": r.get("source_path"),
                "metadata": {
                    "created_at": r.get("created_at"),
                    "tags": r.get("tags", []),
                    "phase": r.get("phase")
                }
            }
            for r in results
        ]
    }

def query_decisions(
    keywords: List[str] = None,
    phase: int = None,
    decision_type: str = None,
    limit: int = 5
) -> Dict:
    """Busca especifica em decisoes."""
    decisions = load_all_decisions()

    if phase is not None:
        decisions = [d for d in decisions if d.get("phase") == phase]

    if decision_type:
        decisions = [d for d in decisions if d.get("type") == decision_type]

    for d in decisions:
        d["relevance_score"] = calculate_relevance(d, keywords or [])

    decisions.sort(key=lambda x: x["relevance_score"], reverse=True)

    return {
        "query_type": "decisions",
        "filters": {"phase": phase, "type": decision_type},
        "results": decisions[:limit]
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--keywords", nargs="+", default=[])
    parser.add_argument("--sources", nargs="+", default=["decisions", "learnings"])
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    result = search(
        keywords=args.keywords,
        sources=args.sources,
        limit=args.limit
    )
    print(yaml.dump(result, default_flow_style=False))
```

## Uso no Fluxo SDLC

1. **Antes de decidir** - Buscar decisoes similares
2. **Ao pesquisar** - Consultar documentacao oficial
3. **Ao resolver problemas** - Verificar learnings relevantes
4. **Ao implementar** - Buscar padroes ja usados

## Pontos de Pesquisa

Para melhorar esta skill:
- "RAG retrieval augmented generation best practices"
- "semantic search for code documentation"
- "knowledge graph software engineering"
