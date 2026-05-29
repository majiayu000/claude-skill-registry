---
name: dag-typesafe
description: >-
  Analyze a repository's type system and generate type-safe DAG execution pipelines
  with GraphSentry-style certificate verification. This skill should be used when
  building LLM-driven workflows that need deterministic type safety, when composing
  typed operations into validated execution graphs, or when adding contract-checked
  pipeline orchestration to any codebase. Supports Python (Pydantic) and TypeScript (Zod).
argument-hint: "[analyze|compose|compile|validate|registry] [args...]"
---

# dag-typesafe

Deterministic type safety via directed acyclic graphs for reasoning language models.

Analyze any repo's public API surface, extract a typed node registry, compose validated
execution DAGs from natural language, and compile them into native pipeline code with
GraphSentry-style `(artifact, certificate)` verification at every node boundary.

## Category

Code Scaffolding & Templates

## Core Concepts

Three layers compose into a single architecture:

1. **Typed Node Registry** — the repo's public functions/classes extracted as typed nodes
   with JSON Schema input/output contracts. The LLM selects from this registry; it never
   generates arbitrary code.

2. **DAG Plan** — a language-neutral execution graph where nodes reference registry entries
   and edges are schema-validated. No cycles, all inputs satisfied, all types compatible.

3. **Certificates** — each node emits an `(artifact, certificate)` pair. Certificates are
   deterministic predicates evaluated from logged evidence. Failed certificates halt the
   pipeline with diagnostic context. Based on GraphSentry (Li et al., 2026).

## Commands

Parse `$ARGUMENTS` to determine which command to run:

### `analyze`

Extract a typed node registry from the current repository.

```bash
python3 ~/.claude/skills/dag-typesafe/scripts/analyze.py [--language python|typescript|auto] [--output dag-registry.json]
```

1. Detect repo language(s) from file extensions and config files
2. Run the appropriate extractor(s) from `extractors/`
3. Walk the AST for public API surface only (exported functions, public classes, API endpoints)
4. Convert type annotations to JSON Schema
5. Output `dag-registry.json` at repo root

### `compose`

Generate a DAG plan from natural language using the typed registry.

The compose phase is **endpoint-agnostic** — it works with any OpenAI-compatible API
(OpenRouter, Groq, Subq Code, local models) or in-session via Claude Code.

**In-session mode (default):** Build a structured prompt from the registry and task
description, then use the current Claude Code session to generate the DAG plan.

**Headless mode:** Set `DAG_LLM_BASE_URL` and `DAG_LLM_API_KEY` environment variables
to point at any OpenAI-compatible endpoint.

```bash
python3 ~/.claude/skills/dag-typesafe/scripts/compose.py "task description" --registry dag-registry.json [--output dag-plan.json] [--provider session|openai]
```

1. Load registry from `dag-registry.json`
2. Build structured prompt constraining LLM to node selection and parameterization
3. Generate DAG plan conforming to `schemas/dag-plan.schema.json`
4. Validate the plan (type compatibility, no cycles, all inputs satisfied)
5. Generate certificate predicates for each node
6. Output `dag-plan.json`

### `compile`

Compile a validated DAG plan into native executable code.

```bash
python3 ~/.claude/skills/dag-typesafe/scripts/compile.py dag-plan.json [--target python|typescript] [--output pipeline.py]
```

1. Read validated `dag-plan.json` and `dag-registry.json`
2. Topologically sort nodes
3. Generate native pipeline code via inline code generation
4. Wrap each node call in schema validation (Pydantic `.model_validate()` / Zod `.parse()`)
5. Inject certificate predicate evaluation at every node boundary
6. Output executable pipeline file with zero runtime dependencies beyond standard validation libs

### `validate`

Type-check an existing DAG plan against a registry.

```bash
python3 ~/.claude/skills/dag-typesafe/scripts/validate.py dag-plan.json --registry dag-registry.json
```

Checks: cycle detection, edge type compatibility, required input satisfaction, certificate
predicate well-formedness, registry reference integrity.

### `registry`

Inspect, filter, and query the typed node registry.

```bash
python3 ~/.claude/skills/dag-typesafe/scripts/registry.py [--filter "pattern"] [--show-schemas] [--stats]
```

## Schemas

All schemas live in `schemas/` as JSON Schema (draft 2020-12):

- `dag-plan.schema.json` — DAG plan format (nodes, edges, metadata)
- `registry.schema.json` — typed node registry format
- `certificate.schema.json` — GraphSentry certificate format

Read these schemas before generating or validating any DAG artifacts.

## Extractors

Language-specific type extractors in `extractors/`:

| Extractor | Source Types | Output |
|-----------|-------------|--------|
| `python_extractor.py` | Pydantic BaseModel, dataclass, TypedDict, function annotations | JSON Schema |
| `typescript_extractor.py` | Zod schemas, interfaces, type aliases, function signatures | JSON Schema |

Each extractor walks the AST, identifies public API surface, and converts type definitions
to JSON Schema for the registry. Internal/private symbols are excluded.

## Code Generation

The compiler generates pipeline code inline (no external templates). Both Python and TypeScript
targets produce complete executable files with:

- Certificate/CertificateError classes
- Topologically sorted node execution
- Per-node certificate emission and predicate evaluation
- Predicate expression sandboxing (AST-validated safe subset only)

## LLM Provider Configuration

For headless/CI use, configure via environment variables:

```bash
export DAG_LLM_BASE_URL="https://openrouter.ai/api/v1"  # or Groq, Subq, local
export DAG_LLM_API_KEY="your-key"
export DAG_LLM_MODEL="anthropic/claude-sonnet-4-20250514"  # model identifier
```

When these are unset, compose mode generates a structured prompt for in-session use.

## Research Basis

This skill synthesizes patterns from:

- **GraphSentry** (Li et al., 2026) — certificate-driven typed DAGs, contract-checked graph surgery
- **ChopChop** (Nagy et al., POPL 2026) — semantic constrained decoding via coinductive realizability
- **PlanCompiler** (prnvh, 2026) — LLM confined to typed node registry selection
- **PlanAI** (Provos, 2026) — Pydantic-typed DAG orchestration with automatic routing
- **Agint** (Chivukula et al., 2025) — type floors (text→data→spec→code) in agentic graph compilation

Full source list: `references/research-sources.md`
