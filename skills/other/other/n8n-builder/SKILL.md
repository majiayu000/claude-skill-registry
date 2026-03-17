---
name: n8n-builder
type: standard
depth: base
description: >-
    Generates production-ready n8n 2.0+ workflow JSON with nodes, connections, AI
    agents, RAG pipelines, Task Runners, MCP clients, and validation. Use when
    building workflow automations, scaffolding LangChain agents with tools/memory,
    implementing RAG retrieval systems, or converting requirements to n8n JSON.
---

# [H1][N8N-BUILDER]
>**Dictum:** *Schema compliance enables n8n import without runtime validation errors.*

<br>

Generate valid n8n workflow JSON.

**Tasks:**
1. Read [schema.md](./references/schema.md) — Root structure, settings
2. Read [nodes.md](./references/nodes.md) — Node definition, typeVersion
3. Read [connections.md](./references/connections.md) — Graph topology, AI types
4. (dynamic values) Read [expressions.md](./references/expressions.md) — Variables, functions
5. (specific nodes) Read [integrations.md](./references/integrations.md) — Node parameters
6. Generate JSON — Apply template from [workflow.template.md](./templates/workflow.template.md)
7. Validate — Run `uv run .claude/skills/n8n-builder/scripts/validate-workflow.py`

[REFERENCE]: [index.md](./index.md) — File listing.

---
## [0][N8N_2.0]
>**Dictum:** *Breaking changes invalidate pre-2025 patterns.*

<br>

**Breaking Changes (December 2025):**

| [INDEX] | [CHANGE]          | [DETAIL]                                                                   |
| :-----: | ----------------- | -------------------------------------------------------------------------- |
|   [1]   | Database          | PostgreSQL required; MySQL/MariaDB support dropped                         |
|   [2]   | Python            | `"language": "python"` removed; use `"pythonNative"` with Task Runners     |
|   [3]   | Security          | `ExecuteCommand` and `LocalFileTrigger` disabled by default                |
|   [4]   | Code Isolation    | Environment variable access blocked (`N8N_BLOCK_ENV_ACCESS_IN_NODE=true`)  |
|   [5]   | Agent Type        | Agent type selection removed (v1.82+); all agents are Tools Agent          |
|   [6]   | Task Runners      | Enabled by default for code execution isolation; external process sandbox  |
|   [7]   | MCP Client        | `mcpClient` standalone node for calling external MCP servers as AI tools   |
|   [8]   | HITL              | Human-in-the-loop for AI tool calls; agent pauses for human approval       |
|   [9]   | MCP OAuth         | MCP servers support OAuth 2.1 authentication for credential exchange       |
|  [10]   | Publish/Save      | Save preserves edits (draft); Publish updates live version (separate act)  |
|  [11]   | SQLite Pool       | High-performance pooling driver reduces "Database Locked" errors           |
|  [12]   | Sub-Workflow Wait | Sub-workflows pause, wait for external input (Slack approval), return data |
|  [13]   | Project Vars      | Project-level variables alongside global; override global per project      |

[CRITICAL]:
- [ALWAYS] Use Task Runners for Code node execution — default isolation mode since 2025.
- [ALWAYS] Use `mcpClient` node (not HTTP) for MCP server integration — handles protocol negotiation.
- [NEVER] Use deprecated `"language": "python"` — fails silently with Task Runners enabled.

---
## [1][SCHEMA]
>**Dictum:** *Root structure enables n8n parser recognition and execution.*

<br>

**Guidance:**
- `AI Workflows` — Require `executionOrder: "v1"` in settings; async node ordering fails without.
- `Portability` — Credential IDs and errorWorkflow UUIDs are instance-specific; expect reassignment post-import.
- `Optional Fields` — Include empty objects (`"pinData": {}`) over omission; prevents import edge cases.
- `Sub-Workflow Typing` — Use `workflowInputs` schema on trigger nodes to validate caller payloads before execution.
- `pinData Limits` — Keep under 12MB; large payloads slow editor rendering and cannot contain binary data.

**Best-Practices:**
- [ALWAYS] Set `"active": false` on generation; activation is a deployment decision.
- [NEVER] Hardcode credential IDs; use placeholder names for cross-instance transfer.

[REFERENCE]: [→schema.md](./references/schema.md)

---
## [2][NODES]
>**Dictum:** *Unique identity enables deterministic cross-node references.*

<br>

**Guidance:**
- `Name Collisions` — n8n auto-renames duplicates (Set→Set1); breaks `$('NodeName')` expressions silently.
- `Version Matching` — typeVersion must match target n8n instance; newer versions may lack backward compatibility.
- `Error Strategy` — Use `onError: "continueErrorOutput"` for fault-tolerant pipelines; default stops execution.
- `Node Documentation` — Use `notes` field for inline documentation; `notesInFlow: true` displays on canvas.

**Best-Practices:**
- [ALWAYS] Generate UUID per node before building connections; connections reference node.name.
- [ALWAYS] Space nodes 200px horizontal, 150px vertical for canvas readability.

[REFERENCE]: [→nodes.md](./references/nodes.md)

---
## [3][CONNECTIONS]
>**Dictum:** *Connection types enable workflow mode distinction at parse time.*

<br>

**Guidance:**
- `AI vs Main` — AI nodes require specialized types (`ai_tool`, `ai_languageModel`); `main` causes silent tool invisibility.
- `Fan-out` — Single output to multiple nodes executes in parallel; order within array is non-deterministic.
- `Multi-output` — Array index maps to output port; IF node: index 0 = true branch, index 1 = false branch.
- `Single Model` — Agent accepts exactly one `ai_languageModel` connection; multiple models conflict silently.
- `Memory Scope` — `ai_memory` persists within single trigger execution only; no cross-session persistence.

**Best-Practices:**
- [ALWAYS] Match connection key AND `type` property; mismatches cause silent failures.
- [NEVER] Connect AI tools via `main` type; agent cannot discover them.
- [NEVER] Connect multiple language models to single agent; use Model Selector node for dynamic selection.

[REFERENCE]: [→connections.md](./references/connections.md)

---
## [4][EXPRESSIONS]
>**Dictum:** *Dynamic evaluation eliminates hardcoded parameters.*

<br>

**Guidance:**
- `Static vs Dynamic` — Prefix `=` signals evaluation; without it, value is literal string including `{{ }}`.
- `Pinned Data` — Test mode pins lack execution context; `.item` fails, use `.first()` or `.all()[0]` instead.
- `Complex Logic` — IIFE pattern `{{(function(){ return ... })()}}` enables multi-statement evaluation.
- `Scope Confusion` — `$json` accesses current node input only; use `$('NodeName').item.json` for other nodes.

**Best-Practices:**
- [ALWAYS] Use `$('NodeName')` for cross-node data; `$json` only accesses current node input.
- [ALWAYS] Escape quotes in JSON strings or use template literals to prevent invalid JSON.
- [NEVER] Assume `.item` works in all contexts; pinned data testing requires explicit accessors.

[REFERENCE]: [→expressions.md](./references/expressions.md)

---
## [5][INTEGRATIONS]
>**Dictum:** *Node type selection determines integration capability.*

<br>

**Guidance:**
- `Trigger Selection` — Webhook for external calls, scheduleTrigger for periodic; choose based on initiation source.
- `AI Tool Visibility` — Sub-workflow tools require `description` parameter; agent uses it for tool selection reasoning.
- `Code Language` — Use `"pythonNative"` for Python; `"python"` is deprecated.
- `Error Propagation` — Use `stopAndError` node for controlled failures; triggers designated error workflow.
- `MCP Client` — `mcpClient` standalone node connects to external MCP servers; discovers tools dynamically via `ai_tool` connection. Supports OAuth 2.1.
- `Guardrails` — `guardrails` node enforces AI output safety with configurable rules and actions.
- `HITL` — Human-in-the-loop approval for AI agent tool calls; agent pauses execution until human approves.
- `Output Parser` — `outputParserStructured` jsonSchema must be static; expressions in schema are ignored silently.
- `Batch Processing` — Use `splitInBatches` for large datasets to prevent memory exhaustion; process in chunks.

**Best-Practices:**
- [ALWAYS] Set `responseMode: "lastNode"` for webhook→response patterns; ensures output reaches caller.
- [ALWAYS] Include `description` on HTTP nodes used as AI tools; undocumented tools are invisible to agent.
- [ALWAYS] Include unique `webhookId` per workflow to prevent path collisions across workflows.

[REFERENCE]: [→integrations.md](./references/integrations.md)

---
## [6][RAG]
>**Dictum:** *RAG pipelines ground LLM responses in domain-specific knowledge.*

<br>

**Guidance:**
- `Vector Store Selection` — Simple for development; PGVector/Pinecone/Qdrant for production persistence.
- `Embedding Consistency` — Same embedding model required for insert and query; mismatch causes semantic drift.
- `Chunk Strategy` — Recursive Character splitter recommended; splits Markdown/HTML/code before character fallback.
- `Memory vs Chains` — Only agents support memory; chains are stateless single-turn processors.
- `Retriever Modes` — MultiQuery for complex questions; Contextual Compression for noise reduction.

**Best-Practices:**
- [ALWAYS] Match embedding model between document insert and query operations.
- [ALWAYS] Use `ai_memory` connection type for memory nodes; `main` silently fails.
- [NEVER] Use Simple Vector Store in production; data lost on restart, global user access.

[REFERENCE]: [→rag.md](./references/rag.md)

---
## [7][VALIDATION]
>**Dictum:** *Pre-export validation prevents n8n import failures.*

<br>

**Script:**
```bash
uv run .claude/skills/n8n-builder/scripts/validate-workflow.py workflow.json
uv run .claude/skills/n8n-builder/scripts/validate-workflow.py workflow.json --strict
```

**Checks (12 automated):**
- `root_required` — name, nodes, connections present
- `node_id_unique` / `node_name_unique` — no duplicates
- `node_id_uuid` — valid UUID format
- `conn_targets_exist` — connection targets reference existing nodes
- `conn_ai_type_match` — AI connection key matches type property
- `settings_exec_order_ai` — LangChain workflows require `executionOrder: "v1"`
- `settings_caller_policy` / `node_on_error` — enum value validation

**Guidance:**
- `API Deployment` — Use POST then PUT pattern; single POST may ignore settings due to API bug.
- `Performance` — `saveExecutionProgress: true` triggers DB I/O per node; disable for high-throughput (>1000 RPM).
- `Source Control` — Strip `instanceId` when sharing; credential files contain stubs only, not secrets.

[REFERENCE]: [→validation.md](./references/validation.md)

