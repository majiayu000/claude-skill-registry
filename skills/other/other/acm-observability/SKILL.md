---
name: acm-observability
description: Agent-actionable reference for ACM-AI's 6-tool observability stack. Teaches how to query traces, inspect graph state, debug Pydantic failures, and analyze costs programmatically.
---

# ACM-AI Observability Skill

## Decision Tree — Which Tool for Which Problem?

| Problem | Tool | Action |
|---------|------|--------|
| Wrong extraction data | Langfuse | Query trace by `session_id=extraction-{source_id}`, examine LLM input/output spans |
| Prompt iteration | LangSmith | Open Playground, edit prompt, re-run side-by-side |
| Pipeline costing | Langfuse | Aggregate GENERATION observations by model, sum tokens/cost |
| Pydantic parse failure | Logfire (via Langfuse) | Search OTel spans for `pydantic.validate_*` with error status |
| Graph stuck / wrong state | LangGraph API | `GET /threads/{id}/state` at `:2024` |
| Model relationships | erdantic | Run `scripts/generate_model_diagrams.py` -> `docs/diagrams/*.svg` |
| Nested JSON exploration | JSON Crack | Paste JSON at `localhost:8888` |
| Pipeline healthy across runs? | Langfuse | Historical traces, score trends, session list |

## Langfuse Query Patterns

### Authentication

```bash
# All Langfuse API calls use HTTP Basic auth
curl -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_BASE_URL/api/public/traces?sessionId=extraction-{source_id}"
```

Default `LANGFUSE_BASE_URL` is `http://localhost:3000` (self-hosted) or `https://cloud.langfuse.com`.

### Python SDK

```python
from langfuse import Langfuse

client = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_BASE_URL", "http://localhost:3000"),
)

# List traces for an extraction
traces = client.fetch_traces(session_id=f"extraction-{source_id}")

# Get a specific trace with observations
trace = client.fetch_trace(trace_id)
```

### Common Filters

| Filter | API Parameter | Example |
|--------|--------------|---------|
| By source | `sessionId` | `extraction-source:abc123` |
| By tag | `tags` | `acm-extraction` |
| By date | `fromTimestamp` | `2026-03-01T00:00:00Z` |
| By name | `name` | `acm_extraction` |

### Session ID Convention

From `langfuse_config.py:135`:
```python
"langfuse_session_id": f"extraction-{clean_source_id}"
```

All extraction traces for a source are grouped under `session_id=extraction-{source_id}`.

## LangGraph API Patterns

The LangGraph dev server runs at `http://127.0.0.1:2024`.

### Start the Server

```bash
uv run langgraph dev --no-browser
```

Registered graphs (from `langgraph.json`):
- `acm_extraction` — ACM extraction pipeline
- `supervisor` — Multi-agent supervisor

### Common Endpoints

```bash
# List registered graphs
curl -s http://127.0.0.1:2024/assistants | python -m json.tool

# List threads
curl -s "http://127.0.0.1:2024/threads?limit=10" | python -m json.tool

# Get thread state
curl -s http://127.0.0.1:2024/threads/{thread_id}/state | python -m json.tool

# Get thread history (checkpoints)
curl -s http://127.0.0.1:2024/threads/{thread_id}/history | python -m json.tool

# Dump state to JSON file for JSON Crack
uv run python scripts/dump_state_json.py {thread_id}
```

### Swagger UI

Full API documentation at `http://127.0.0.1:2024/docs`.

## Logfire Safety Guardrails

### NEVER Call instrument_pydantic() Without include={}

Blanket `logfire.instrument_pydantic()` creates an OTel span for EVERY `model_validate()` call. Docling creates 1 `PdfTextCell` per PDF character, causing ~48K traces per extraction.

### Safe Instrumentation Set

```python
import logfire

logfire.instrument_pydantic(
    include={
        "ACMExtractionRecord",
        "BuildingRoomContext",
        "ACMItemRecord",
        "ACMExtractionResult",
        "ACMItemExtractionResult",
        "NormalizedExtractionResult",
    }
)
```

This instruments only ACM domain models (~10-50 traces per run).

### OTel Span Nesting

`langfuse_tracing()` pre-injects OTel trace context via `_try_inject_otel_trace_context()` so Logfire Pydantic validation spans nest under the Langfuse trace (not as orphan top-level traces).

## Wiring Patterns

### Pattern 1: Context Manager (Routers)

Used in FastAPI router endpoints:

```python
from open_notebook.observability.langfuse_config import (
    langfuse_tracing,
    merge_langfuse_into_config,
)

with langfuse_tracing("acm_extraction", source_id=source_id) as (cb, meta):
    config = merge_langfuse_into_config(base_config, cb, meta)
    result = await graph.ainvoke(input_state, config=config)
```

### Pattern 2: Manual Handler (Commands)

Used in background command handlers:

```python
from open_notebook.observability.langfuse_config import (
    get_langfuse_handler,
    build_langfuse_metadata,
    append_langfuse_callback,
    flush_langfuse_handler,
)

handler = get_langfuse_handler()
callbacks = append_langfuse_callback([], handler)
metadata = build_langfuse_metadata(source_id=source_id)
config = {"callbacks": callbacks, "metadata": metadata}
try:
    result = graph.invoke(input_state, config=config)
finally:
    flush_langfuse_handler(handler)
```

### Critical Rule: Callback Placement

Callbacks belong at the **invocation site** (routers, commands), NEVER inside graph node functions. Graph nodes receive callbacks automatically via LangGraph's config propagation.

### Do NOT Modify Pre-Existing Wiring

`acm_extraction.py` and `source_commands.py` have working Langfuse wiring. Do not alter it.

## Cross-Tool Workflow Recipes

### Recipe 1: Debug a Failed Extraction

1. Query Langfuse: `session_id=extraction-{source_id}`
2. Find the trace with errors (look for spans with `statusCode: ERROR`)
3. Examine the LLM input/output in the GENERATION span
4. Check Logfire Pydantic spans for validation failures
5. If graph state needed: `GET /threads/{thread_id}/state` at `:2024`
6. Cross-reference with SurrealDB: `SELECT * FROM acm_record WHERE source_id = "{source_id}"`

### Recipe 2: Compare Costs Across Models

1. Fetch GENERATION observations from Langfuse filtered by date range
2. Group by `model` field
3. Sum `totalCost`, `promptTokens`, `completionTokens`
4. Compare cost-per-record: `totalCost / records_extracted`

### Recipe 3: Debug Pydantic Validation

1. Verify Logfire is initialized: check `LOGFIRE_ENABLED=true` and Langfuse keys set
2. Search Langfuse for OTel spans with name pattern `pydantic.validate_*`
3. Filter for spans with error status
4. Examine the span attributes for validation error details
5. Cross-reference with the LLM output that produced the invalid data

### Recipe 4: Inspect Graph Execution Flow

1. Start LangGraph dev server: `uv run langgraph dev --no-browser`
2. Find thread: `GET /threads?limit=10`
3. Get current state: `GET /threads/{id}/state`
4. View checkpoint history: `GET /threads/{id}/history`
5. Dump to JSON Crack: `uv run python scripts/dump_state_json.py {thread_id}`
6. Open `localhost:8888`, paste JSON for visual exploration

## Environment Variables Reference

| Variable | Purpose | Default |
|----------|---------|---------|
| `LANGFUSE_ENABLED` | Enable Langfuse tracing | `false` |
| `LANGFUSE_PUBLIC_KEY` | Langfuse auth | (required if enabled) |
| `LANGFUSE_SECRET_KEY` | Langfuse auth | (required if enabled) |
| `LANGFUSE_BASE_URL` | Langfuse host | `https://cloud.langfuse.com` |
| `LOGFIRE_ENABLED` | Enable Logfire -> Langfuse bridge | `false` |
| `LANGCHAIN_TRACING_V2` | Enable LangSmith auto-tracing | `false` |
| `LANGCHAIN_API_KEY` | LangSmith auth | (required if tracing enabled) |

## Key Source Files

| File | Purpose |
|------|---------|
| `open_notebook/observability/langfuse_config.py` | `langfuse_tracing()`, `get_langfuse_handler()`, `merge_langfuse_into_config()` |
| `open_notebook/observability/logfire_config.py` | `init_logfire()`, instrument_pydantic guidance |
| `open_notebook/observability/langfuse_bridge.py` | `emit_pipeline_event()` for custom LangChain events |
| `scripts/dump_state_json.py` | Dump LangGraph thread state to JSON file |
| `scripts/generate_model_diagrams.py` | Generate erdantic ER diagrams |
| `scripts/observability/setup_langfuse_datasets.py` | Langfuse dataset/prompt setup |
| `docs/development/observability.md` | Comprehensive reference (1026 lines) |
