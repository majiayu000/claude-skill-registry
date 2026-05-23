---
name: workflow-coordinator
description: Use when coordinating handoffs between workflows (e.g., skill-editor to programming-pm). Provides universal handoff schema v3.0, validation rules, distributed tracing conventions, and workflow discovery via frontmatter metadata.

handoff:
  accepts_from:
    - "*"
  provides_to:
    - "*"
  schema_version: "3.0"
  schema_type: universal

categories:
  - coordination
  - integration
  - workflow-management

input_requirements:
  - handoff-payload
  - workflow-request

output_types:
  - handoff-payload
  - validation-result
  - discovery-result
---

# Workflow Coordinator

Universal cross-workflow handoff coordination using schema v3.0.

## When to Use

- Coordinating handoffs between independent workflows (e.g., skill-editor to programming-pm)
- Discovering available target workflows for a handoff
- Validating handoff payloads before transmission
- Debugging multi-hop handoff chains via distributed tracing
- Adding handoff support to a new or existing skill

## When NOT to Use

- Internal specialist handoffs within programming-pm (use internal v1.2 schema)
- Simple file passing between agents (no schema validation needed)
- Single-skill invocations (no coordination needed)
- Agent team coordination within a single task (use agent teams directly)

## Pilot Scope Limitations

This is v3.0 pilot (documentation + schema artifacts only):

- **Token counting**: Guidance-only (heuristic estimation via `characters / 4`, not tiktoken)
- **Schema validation**: Manual invocation required (`python3` one-liner)
- **Circular handoff detection**: Advisory, not automated
- **CLI tools**: Deferred to v1.1 (`claude-handoff validate`, etc.)
- **Adapter layer**: Deferred to v1.1 (cross-version schema translation)
- **Registry sync tool**: Deferred to v1.1 (`claude-handoff-registry sync`)

---

## Quick Start: Minimal Handoff

The absolute minimum v3.0 handoff (5 required top-level fields):

```json
{
  "handoff": {
    "version": "3.0",
    "schema_type": "universal",
    "timestamp": "2026-02-07T18:30:00Z",
    "trace_id": "550e8400-e29b-41d4-a716-446655440000",
    "source": {
      "skill": "skill-editor",
      "workflow_id": "session-20260207-183000",
      "session_path": "/tmp/skill-editor-session/session-20260207-183000",
      "phase": "Phase 3"
    },
    "target": {
      "skill": "programming-pm"
    },
    "context": {
      "summary": "Implement workflow coordination system",
      "problem_type": "implementation"
    },
    "payload": {
      "working": {
        "description": "Key implementation details here"
      }
    },
    "meta": {
      "token_count": 250,
      "confidence": "high"
    }
  }
}
```

Generate a trace_id:

```bash
python3 -c "import uuid; print(uuid.uuid4())"
```

Estimate token count:

```bash
wc -c < handoff.json | awk '{printf "Estimated tokens: %d\n", $1/4}'
```

---

## Handoff Lifecycle

### Sender (Source Workflow)

1. Determine that work should be handed off to another workflow
2. Discover available target workflows (see Reference Documents below)
3. Present target options to user for selection (or auto-select if only one match)
4. Generate `trace_id` (UUID v4) if this is a new trace, or propagate existing
5. Build handoff payload using tiered context structure:
   - `payload.working` (<500 tokens): Immediate context needed by target
   - `payload.session` (<1000 tokens): Session artifacts and state (optional)
   - `payload.references` (<500 tokens): File paths for on-demand loading (optional)
6. Estimate token count via `characters / 4` heuristic
7. If over 2000 tokens, apply compression strategies (see validation reference)
8. Validate against schema v3.0 (`python3 -c "import json, jsonschema; ..."`)
9. Write handoff file to `{session_path}/handoffs/{source}-to-{target}-{timestamp}.json`
10. Log handoff transmission event to `trace.jsonl`

### Receiver (Target Workflow)

1. Read handoff file from provided path
2. Validate `handoff.version` is `"3.0"` (or handle legacy gracefully)
3. Extract `trace_id` and propagate to own session state
4. Read `context.summary` and `context.problem_type` for initial orientation
5. Load `payload.working` into working context
6. Optionally load `payload.session` and `payload.references` as needed
7. Begin processing at `target.expected_phase` (if specified) or entry point

---

## Reference Documents

Load the relevant reference for your task:

| Task | Reference |
|------|-----------|
| Creating a handoff payload | `references/handoff-validation.md` |
| Debugging a handoff chain | `references/distributed-tracing.md` |
| Finding target workflows | `references/handoff-registry.md` |
| Adding handoff support to a skill | `references/frontmatter-metadata-standard.md` |
| Schema definition (JSON Schema) | `references/universal-handoff-schema-v3.0.json` |

Load only the reference you need -- progressive disclosure keeps context lean.

---

## Design Decisions

Key architectural decisions (captured from perspective-swarm analysis and synthesis):

1. **Hybrid distributed orchestration** (not master orchestrator) -- Each workflow is autonomous; coordinator provides schema and conventions, not control
2. **Extend perspective-swarm v2.0** (not start from scratch) -- v2.0 already implements research-recommended patterns (JSON Schema, workflow discovery)
3. **2000-token budget** (research-based, configurable) -- Research shows 3-5x cost multiplier for context bloat; fixed budget with tiered structure
4. **JSON Schema Draft 2020-12** (OpenAPI 3.1 compatible) -- Industry standard with `unevaluatedProperties` for extensibility
5. **File-based tracing** (not database-backed) -- Lightweight, no infrastructure dependencies, JSON Lines format
6. **`unevaluatedProperties: false`** for schema extensibility -- Recognizes properties from all subschemas unlike `additionalProperties`, enabling v2.0/v3.0 coexistence (Strangler Fig migration)

---

## Examples

Two complete example handoff files demonstrate the schema:

- `examples/skill-editor-to-programming-pm.json` -- Full v3.0 handoff with all sections (skill-editor hands off implementation work)
- `examples/programming-pm-to-skill-editor.json` -- Reverse direction (programming-pm requests new skill creation)

Both examples validate against `references/universal-handoff-schema-v3.0.json`.
