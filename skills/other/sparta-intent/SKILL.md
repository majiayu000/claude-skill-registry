---
name: sparta-intent
description: '> This skill has been absorbed into /memory. All capabilities now live
  in graphmemory.:'
---

---
name: sparta-intent
deprecated: true
deprecated_by: "graph_memory.intent + graph_memory.classifiers + graph_memory.ambiguity + graph_memory.hybrid_search"
deprecated_date: "2026-02-19"
description: "DEPRECATED — Use /memory intent, /memory recall, /memory clarify instead. All capabilities absorbed into graph_memory."
triggers: []
composable:
  memory: true
provides:
  - sparta-intent
composes: [, task-monitor]
---

# Sparta Intent Mapper (DEPRECATED 2026-02-19)

> **This skill has been absorbed into `/memory`.** All capabilities now live in `graph_memory.*`:
>
> | Old (sparta-intent)         | New (graph_memory)                          |
> |----------------------------|---------------------------------------------|
> | `sparta_intent.inference`  | `graph_memory.intent.IntentMapper`          |
> | `sparta_intent.query_spec` | `graph_memory.intent.QuerySpec`             |
> | `classifiers/predictor.py` | `graph_memory.classifiers.AmbiguityPredictor` / `IntentPredictor` |
> | `ambiguity_oracle.py`      | `graph_memory.ambiguity.AmbiguityOracle`    |
> | `result_stats.py`          | `graph_memory.ambiguity.ResultStats`        |
> | `clarifier.py`             | `graph_memory.ambiguity.Clarifier`          |
> | `aql_compiler.py` + `arango_exec.py` | `graph_memory.hybrid_search.hybrid_search_sparta_qra()` |
>
> **Why deprecated**: This skill was a silo that bypassed `/memory`'s hybrid search (BM25+vector+graph), taxonomy extraction, multihop traversal, and RecallSource infrastructure. The stress test hit a B-grade ceiling (avg 0.784) because it retrieved individual QRAs without graph context.
>
> **Migration**: Replace `from sparta_intent.inference import IntentMapper` with `from graph_memory.intent import IntentMapper`. Replace raw AQL queries with `hybrid_search_sparta_qra()`.
>
> **Classifier models still used**: The trained DistilBERT models at `/mnt/storage12tb/media/agents/shared/sparta-intent/classifiers/models/` are still loaded by `graph_memory.classifiers`.

## Original Architecture (for reference)

```
Query → IntentMapper → QuerySpec → AQLLinter → AQLCompiler → PlanGate → ArangoExecutor → ResultStats → AmbiguityOracle → Clarifier
```

## Usage

### Query (rule-based, <5ms)

```bash
./run.sh query "How does firmware verification prevent attacks?"
./run.sh query "What controls mitigate T1071?" --json
./run.sh query "How do I detect RF jamming?" --execute  # runs against ArangoDB
```

### Query with LLM (scillm via Chutes.ai)

```bash
./run.sh query "How do I detect RF jamming?" --llm
```

### Diagnose ambiguity

```bash
./run.sh diagnose "spacecraft security"
```

### Training (delegates to create-intent-map)

```bash
./run.sh train-sft        # prints delegation instructions
./run.sh train-grpo       # prints delegation instructions
```

## Composability

| Integration | How |
|-------------|-----|
| **Memory** | `recall()` before inference for cached QuerySpecs, `learn()` after successful queries |
| **scillm** | LLM-based inference via `quick_completion()` when `--llm` flag is set |
| **Taxonomy** | Canonical `BRIDGE_KEYWORDS` imported from `taxonomy/taxonomy.py` for Tier0 bridge classification |
| **Embedding** | `graph_memory.embeddings.encode_texts()` for vector lane AQL queries |
| **Telemetry** | `track_skill("sparta-intent")` wraps query execution for outcome logging |

## Safety

- **7-template AQL allowlist** — no dynamic query construction
- **Path traversal prevention** — `os.path.realpath()` check on template paths
- **Bind parameters only** — no string interpolation in AQL
- **Depth cap** — max 2 hops in graph traversal
- **k cap** — max 25 results (1000 for diagnostics)
- **Plan gate** — rejects full collection scans before execution
- **AQL linter** — validates QuerySpec constraints pre-compilation

## Oracle Signals

| Signal | Threshold | Meaning |
|--------|-----------|---------|
| Margin | < 0.08 | Top results too close in score |
| Entropy | > 1.35 | Score distribution too flat |
| Tag disagreement | > 0.45 | Result set spans multiple tactics |
| Entity disagreement | > 0.55 | Result set spans multiple controls |

Decision: >= 2 triggers = ambiguous → generate clarification question.
