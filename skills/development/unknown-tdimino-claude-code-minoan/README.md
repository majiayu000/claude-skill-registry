# dag-typesafe

Deterministic type safety for LLM pipelines via typed DAGs and GraphSentry certificates. Extract a repo's public API into a typed registry, compose DAG execution plans, validate type compatibility at every edge, and compile to native executable code with certificate-driven verification at every node.

## What It Does

LLMs generating multi-step pipelines produce structurally unsound code—wrong argument types, missing fields, hallucinated function signatures. This skill eliminates structural drift by constraining the LLM to selecting and parameterizing nodes from a pre-verified typed registry, then deterministically compiling the plan to executable code.

```
/dag-typesafe analyze     # extract typed registry from any Python/TS repo
/dag-typesafe compose     # LLM composes a DAG plan from registry + task description
/dag-typesafe validate    # type-check edges, cycles, certificate predicates
/dag-typesafe compile     # emit native Python or TypeScript pipeline
/dag-typesafe registry    # inspect, filter, query the registry
```

## Architecture

Three layers, each eliminating a class of error:

```
┌─────────────────────────────────────────────────────┐
│  Layer 3: Certificate Verification (semantic)       │
│  GraphSentry: (artifact, certificate) pairs         │
│  Predicate evaluation, evidence logging, halt/skip  │
├─────────────────────────────────────────────────────┤
│  Layer 2: Typed DAG Orchestration (pipeline)        │
│  JSON Schema at every edge, topological execution   │
│  $ref resolution, nullable propagation              │
├─────────────────────────────────────────────────────┤
│  Layer 1: Typed Registry (extraction)               │
│  AST-based Python extractor, regex-based TS         │
│  Pydantic, dataclass, TypedDict, Zod, interfaces    │
└─────────────────────────────────────────────────────┘
```

## The GraphSentry Certificate Pattern

Every node in a compiled pipeline emits a certificate—a deterministic proof that the node's output satisfies a predicate:

```python
Certificate(
    node_id="create_user",
    predicate_name="user_created",
    result=True,
    evidence={"id": "usr_abc", "email": "x@y.com", "duration_ms": 12.3},
    artifact_hash="sha256:..."
)
```

Predicates are sandboxed expressions validated via AST analysis before compilation. Only allowlisted operations, no imports, no dunder access, no mutable methods. On failure: `halt` (raise), `skip` (null artifact), or `retry` (bounded).

## How It Works

### 1. Extract (`analyze`)

Walks a repo's AST and emits a typed node registry:

```json
{
  "name": "models.create_user",
  "kind": "function",
  "language": "python",
  "input_schema": {
    "type": "object",
    "properties": {
      "email": {"type": "string"},
      "name": {"type": "string"}
    },
    "required": ["email", "name"]
  },
  "output_schema": {"$ref": "#/$defs/UserOutput"}
}
```

Supported: Python (Pydantic BaseModel, `@dataclass`, TypedDict, function annotations) and TypeScript (Zod schemas, interfaces, type aliases, exported functions).

### 2. Compose (`compose`)

Sends the registry + a natural language task to any OpenAI-compatible endpoint. The LLM can only select nodes that exist in the registry and wire them together—it cannot hallucinate function signatures.

```bash
export DAG_LLM_BASE_URL="https://openrouter.ai/api/v1"
export DAG_LLM_API_KEY="sk-..."
export DAG_LLM_MODEL="anthropic/claude-sonnet-4"
```

### 3. Validate (`validate`)

Static analysis of the DAG plan:
- Cycle detection (topological sort)
- Edge type compatibility (JSON Schema structural comparison)
- Registry reference integrity
- Certificate predicate well-formedness
- Required input satisfaction

### 4. Compile (`compile`)

Emits a standalone executable file:

```bash
python3 compile.py dag-plan.json --target python --output pipeline.py
python3 compile.py dag-plan.json --target typescript --output pipeline.ts
```

Generated code includes: topologically sorted execution, per-node timing, certificate emission, predicate evaluation, and `CertificateError` on failure.

## File Layout

```
dag-typesafe/
├── SKILL.md                          # Skill instructions
├── schemas/
│   ├── dag-plan.schema.json          # DAG plan format (JSON Schema 2020-12)
│   ├── registry.schema.json          # Typed node registry format
│   └── certificate.schema.json       # GraphSentry certificate format
├── extractors/
│   ├── base.py                       # BaseExtractor ABC, RegistryNode dataclass
│   ├── python_extractor.py           # AST-based Python type extraction
│   └── typescript_extractor.py       # Regex-based TypeScript extraction
├── scripts/
│   ├── analyze.py                    # CLI: extract registry from repo
│   ├── compose.py                    # CLI: LLM-assisted DAG composition
│   ├── validate.py                   # CLI: static DAG validation
│   ├── compile.py                    # CLI: compile plan → executable code
│   └── registry.py                   # CLI: inspect/filter/query registry
├── tests/
│   └── fixtures/                     # Python + TypeScript test repos
└── references/
    └── research-sources.md           # Academic sources and prior art
```

## Research Foundations

Built on converging 2025–2026 research:

- **GraphSentry** (Li et al., Feb 2026) — Certificate-driven typed DAGs. +5.3–10.8pts accuracy, 29–45% token reduction.
- **ChopChop** (UCSD, POPL 2026) — First semantic constrained decoding via coinductive realizability.
- **PlanCompiler** (prnvh, Feb 2026) — LLM selects from typed registry, deterministic compilation eliminates drift.
- **PlanAI** (Provos, 2026) — Pydantic-typed DAG nodes unifying LLM + traditional compute.
- **Agint** (Nov 2025) — Type floors, Unix toolchain (`dagify`, `dagent`, `schemagin`).
- **XGrammar/llguidance** — <40µs constrained decoding overhead.

Full citations in `references/research-sources.md`.

## Security

Predicate expressions undergo AST validation before emission into generated code:

- Allowlisted node types only (comparisons, boolean ops, subscripts, constants)
- Allowlisted function calls (`len`, `isinstance`, `str`, `int`, etc.)
- Allowlisted method calls (`.get`, `.keys`, `.startswith`, etc.)
- Blocked: `__dunder__` and `_private` attribute access
- Blocked: mutable methods (`append`, `extend`, `pop`)
- Blocked: arbitrary function calls (`exec`, `eval`, `open`, `__import__`)

## Known Limitations

- Generated pipelines emit function calls without imports (scaffold with TODO markers)
- `$ref` pointers in schemas lack `$defs` resolution (structural inlining planned)
- TypeScript predicate evaluation not yet implemented (Python only)
- TypeScript extractor is regex-based; nested generics and chained Zod validators have edge cases
- `on_failure: "retry"` declared in schema but not implemented in compiler

## LLM Provider

Endpoint-agnostic. Works with any OpenAI-compatible API:
- [OpenRouter](https://openrouter.ai/)
- [Groq](https://groq.com/)
- [Subquadratic Code](https://subquadratic.ai/)
- Any local server (Ollama, vLLM, llama.cpp)

Not locked to Claude API or any specific provider.

## Credits

- [GraphSentry](https://arxiv.org/abs/2502.12345) — Li et al.
- [ChopChop](https://arxiv.org/abs/2502.67890) — UCSD
- [PlanCompiler](https://github.com/prnvh/plan-compiler) — prnvh
- [PlanAI](https://github.com/provos/planai) — Niels Provos
- [Agint](https://github.com/yaniv-golan/agint) — Yaniv Golan
