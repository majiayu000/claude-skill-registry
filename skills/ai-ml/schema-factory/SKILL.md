---
name: schema-factory
description: "Build, lint, ingest, compose Drescher-style schemas"
license: MIT
tier: 2
allowed-tools:
  - read_file
  - write_file
  - shell
related: [schema-mechanism, experiment, debugging, planning]
tags: [moollm, schemas, drescher, deterministic, reasoning]
credits:
  - "Gary Drescher — Schema Mechanism (1991)"
  - "Henry Minsky — Blocksworld examples"
---

# SCHEMA-FACTORY

> **"Deterministic checks first, LLM second."**

Build, lint, ingest, compose, and generate context for Drescher-style schemas.

---

## Why This Exists

Gary Drescher's schema mechanism is strongest when it has:

1. **Prescriptive schema-schema** — what valid schemas must look like
2. **Deterministic layer** — evaluate and refine before asking the LLM
3. **Context generator** — emit only needed patterns and evidence

The goal is **hybrid orchestration**: Python does deterministic work, Cursor/LLM handles synthesis, MOOLLM stays explicit about what came from where.

---

## Key Files

| File | Purpose |
|------|---------|
| `SCHEMA-SCHEMA.yml` | Drives linting and ingestion |
| `schema_tool.py` | CLI for all operations |
| `examples/schema-example.yml` | Compact schema set |
| `examples/henry-minsky-blocksworld.yml` | Classic microworld data |

---

## Quick Use

```bash
# Validate schemas
python3 schema_tool.py lint examples/schema-example.yml

# Compose action chain toward goal
python3 schema_tool.py compose --schemas examples/schema-example.yml --goal postgres-running

# Generate LLM context bundle
python3 schema_tool.py context --schemas examples/schema-example.yml --goal pyvision-running
```

---

## Methods

### LINT

Validate schema against schema-schema.

**Input:** One or more schema files (YAML)  
**Output:** Pass/fail + diagnostics  
**Emits:** `schema_lint`  
**Checks:** Required fields, type validation, reliability range, non-empty context/result

```bash
python3 schema_tool.py lint my-schemas.yml
```

### INGEST

Update schemas from experience logs or observed transitions.

**Input:** Experience logs  
**Output:** Updated schema set + evidence counts  
**Emits:** `schema_ingest`  
**Deterministic:** No LLM calls; only schema updates

```bash
python3 schema_tool.py ingest experience-log.yml --into my-schemas.yml
```

### COMPOSE

Build action chain toward goal.

**Input:** Schema set + goal  
**Output:** Composed action chain + rationale  
**Emits:** `schema_compose`

```bash
python3 schema_tool.py compose --schemas my-schemas.yml --goal target-state
```

### CONTEXT

Generate compact context bundle for LLM synthesis.

**Input:** Schema set + goal + optional focus items  
**Output:** Compact context bundle  
**Emits:** `context_generate`  
**Includes:** id, action, context, result, reliability, extended_context, extended_results

```bash
python3 schema_tool.py context --schemas my-schemas.yml --goal target-state --focus item1,item2
```

---

## Schema Structure

```yaml
schema:
  id: "unique-identifier"
  action: "what-the-schema-does"
  context:
    - precondition-1
    - precondition-2
  result:
    - postcondition-1
  reliability: 0.85  # 0.0-1.0
  
  # Optional
  extended_context: [...]
  extended_results: [...]
  evidence_count: 47
  marginal_attribution: {...}
```

---

## Principles

1. **Deterministic checks first, LLM second** — Python validates before synthesis
2. **Emit events for traceability** — Know what happened where
3. **Prefer small, explicit context bundles** — Don't dump everything
4. **Schema-schema can evolve** — Via the same learning loop it governs

---

## The Schema-Schema

The `SCHEMA-SCHEMA.yml` defines what valid schemas must look like:

- Required fields and their types
- Reliability range constraints
- Context/result non-empty rules
- Extension field patterns

This is **prescriptive** — schemas that don't match get lint errors.

---

## Integration with LLM

The factory provides **deterministic foundation** for LLM reasoning:

```yaml
# 1. Python validates and composes
schema_factory compose --goal postgres-running

# 2. Output becomes LLM context
"Here are the relevant schemas and a proposed action chain..."

# 3. LLM synthesizes and refines
"Based on these schemas, I recommend..."

# 4. Results feed back into ingest
schema_factory ingest --experience new-observations.yml
```

---

## Dovetails With

- [../schema-mechanism/](../schema-mechanism/) — Theoretical foundation (Drescher)
- [../experiment/](../experiment/) — Schemas drive experiment design
- [../debugging/](../debugging/) — Schema failures are bugs to investigate
- [../planning/](../planning/) — Schema composition is planning

---

*"Validate structure. Compose plans. Generate context. Let the LLM shine where it should."*
