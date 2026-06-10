---
name: mcp-interface-design
description: |-
  Use when designing MCP servers with clear tools, strict schemas, scoped resources, and useful errors.
  Triggers:
skill_api_version: 1
user-invocable: false
hexagonal_role: domain
practices:
- pragmatic-programmer
- twelve-factor
consumes: []
produces:
- mcp-interface-design-spec
- tool-surface-audit
context_rel:
- kind: supplier-to
  with: cli-agent-ux-audit
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: topic
metadata:
  tier: judgment
  dependencies: []
  stability: experimental
output_contract: A design spec or audit (PASS/FAIL per principle) for an MCP server's tool/resource/auth surface, written to a durable artifact (markdown spec or a bead). No server code generated unless asked.
---

# mcp-interface-design — make MCP tools an agent can use without a human

A good MCP server is a *contract written for a model reader*, not an API written for a programmer. The agent never reads your source; it reads tool names, descriptions, and schemas, then guesses. Every ambiguity becomes a wrong call. This skill is the discipline for removing that ambiguity.

## ⚠️ Critical Constraints

- **The description IS the selection mechanism.** The model picks a tool from its name + description alone. A vague description silently routes to the wrong tool. **Why:** there is no embedding fallback — pure reasoning over text.
  - WRONG: `get_data` — "Gets data from the system."
  - CORRECT: `search_invoices` — "Find invoices by customer, date range, or status. Returns up to 50 matches with id, amount, and status. Use `get_invoice` for full line items."

- **Schemas must be strict and self-describing.** Loose schemas (`type: object` with no properties, free-form strings for enums) let the model send garbage that only fails at runtime. **Why:** validation at the boundary is cheaper than a failed tool call mid-reasoning.
  - WRONG: `{"status": {"type": "string"}}`
  - CORRECT: `{"status": {"type": "string", "enum": ["open","paid","void"], "description": "Invoice lifecycle state"}}`

- **Errors must teach the next action.** A bare `500` or `invalid argument` strands the agent. **Why:** the agent's only recovery signal is the error text — make it actionable.
  - WRONG: `{"error": "bad request"}`
  - CORRECT: `{"error": "date_from (2026-13-01) is not a valid ISO date. Expected YYYY-MM-DD."}`

- **Least-privilege, read-by-default.** Never expose a destructive tool (delete/send/pay) without an explicit, narrowly-scoped definition and an auth scope to match. **Why:** an agent will eventually call every tool you expose; surface area is liability.

- **Never overload one tool with a `mode`/`action` switch.** One tool = one job. **Why:** a `manage(action, ...)` god-tool defeats name-based selection and forces conditional schemas the model can't reason about.

## Why This Exists

MCP servers fail in production not because the transport breaks but because the *agent-facing contract* is built for humans. Humans read docs, infer intent, and retry by hand. A model gets one shot at name selection and one shot at argument filling per call, and recovers only from what the error text tells it. Teams ship 30 tools with terse names and `type: string` everywhere, then wonder why the agent picks `update_record` when it wanted `create_record`. This skill front-loads the design decisions that make the difference: tool granularity, schema strictness, error ergonomics, resource-vs-tool, and auth scoping — before any SDK code is written.

## Quick Start

1. List the **jobs** the agent needs done (verbs), not the entities you have (nouns). One job → one tool.
2. For each tool, write the **description first** — name, what it returns, when to use it, what to use instead.
3. Write a **strict JSON Schema**: every property typed, enums closed, required-list explicit, units in descriptions.
4. Define the **error contract**: every failure returns `{error, hint}` where `hint` names the fix.
5. Mark each tool **read | write | destructive** and assign the **minimal auth scope**.
6. Decide **tool vs resource**: stable, addressable, read-only context → resource; an action → tool.
7. Run the **Quality Rubric** below; write the result to a spec artifact.

## Methodology

### Phase 1 — Tool surface (granularity)
Enumerate jobs as verbs: `search_invoices`, `get_invoice`, `create_invoice`, `void_invoice`. Reject any tool whose description needs the word "and" between unrelated jobs, or whose arguments include an `action`/`mode` discriminator. Prefer 6 sharp tools over 2 overloaded ones; prefer parameters over near-duplicate tools (`search_invoices(status=)` not `search_open_invoices` + `search_paid_invoices`).

**Checkpoint:** every tool name is a single unambiguous verb-phrase the model could pick blind.

### Phase 2 — Schemas
For each tool define `inputSchema` with: every property typed; enums for closed sets; `required` listing only truly-required keys; `description` on every property carrying **units, format, and bounds** (e.g. "amount in cents", "ISO 8601 date"). Set `additionalProperties: false` so stray keys fail loudly. Keep argument counts low (≤6); nest rarely. Return a documented, stable **output shape** — agents key off field names.

**Checkpoint:** a malformed call is rejected at the schema boundary with a precise message, never silently coerced.

### Phase 3 — Errors
Define one error envelope used everywhere: `{ "error": "<what went wrong, with the bad value>", "hint": "<the corrective next action>" }`. Distinguish *retryable* (rate-limit, transient) from *terminal* (bad auth, not-found) so the agent doesn't loop. Never leak stack traces or secrets. Return partial-success info when a batch half-fails.

**Checkpoint:** for each failure mode, the error text alone is enough for the agent to fix and retry.

### Phase 4 — Resources & auth
**Resource** if it's stable, addressable, and read-only (a file, a record, a config) — exposed via URI for the host to pull into context cheaply. **Tool** if it performs an action or needs parameters. Assign each tool a class (read/write/destructive) and the **narrowest credential scope** that lets it work. Default to read-only tokens; gate writes/deletes behind explicit scopes; never embed a broad master key. Make the auth failure mode an actionable error (Phase 3), not a silent empty result.

**Checkpoint:** the credential the server runs with cannot do more than its exposed tools require.

## Output Specification

Write a design spec to `mcp-interface-design-<server>.md` (or a bead) containing:
- **Tool table:** `| tool | verb/job | class (read/write/destructive) | auth scope |`
- **Per-tool schema sketch** (properties, types, enums, required, descriptions).
- **Error envelope** definition + the retryable/terminal split.
- **Resource list** with URI shapes (if any).
- **Rubric result** (below) with PASS/FAIL per line and the fixes for any FAIL.

## Quality Rubric

A design PASSES only if ALL hold:
- **Selectability:** every tool name + description is sufficient for blind selection; no two tools overlap; no `action`/`mode` god-tool.
- **Schema strictness:** every property typed, every closed set an enum, `additionalProperties: false`, units/format in descriptions, `required` minimal-and-correct.
- **Error ergonomics:** one error envelope, every error names the bad value AND the fix, retryable vs terminal distinguished.
- **Least privilege:** each tool classed read/write/destructive; auth scope is the minimum; destructive tools are explicit, never implicit.
- **Tool-vs-resource:** read-only addressable context is a resource, not a tool; actions are tools.
- **Output stability:** return shapes are documented and named, not free-form blobs.

## Examples

**Splitting a god-tool.** `manage_user(action, id, payload)` → `get_user(id)`, `create_user(profile)`, `update_user(id, changes)`, `deactivate_user(id)`. The model now selects by name and fills a schema specific to the job.

**Self-correcting error.** Call `get_invoice(id="INV-9")` → not found. Return `{"error":"No invoice with id 'INV-9'. Ids look like 'inv_01H...'.","hint":"Call search_invoices to find the id first."}`. The agent self-routes to `search_invoices` without a human.

**Resource not tool.** Exposing the org's price list as `get_prices()` forces a call every turn; exposing it as resource `catalog://prices/current` lets the host pull it into context once. Stable read-only context → resource.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent calls the wrong tool | overlapping/vague descriptions | sharpen names to single verbs; add "use X instead" cross-refs |
| Agent sends malformed args | loose schema (free-form strings) | add enums, types, `additionalProperties: false`, units in descriptions |
| Agent loops on a failure | error text not actionable / retryable-vs-terminal unclear | adopt the `{error, hint}` envelope; mark terminal errors |
| Tool surface feels bloated | near-duplicate tools | collapse into one tool with a parameter |
| Over-broad blast radius | one credential, all scopes | class tools read/write/destructive; scope auth to the minimum |
| Context bloat from repeated reads | action-shaped what is really static context | model it as a resource (URI), not a tool |

## See Also

- `agent-ergonomics-and-intuitiveness-maximization-for-cli-tools` — the same ergonomics discipline for CLI surfaces; the sibling lens for tool design.
- The official MCP specification + your language SDK docs for transport, lifecycle, and capability negotiation (this skill is the *design* layer above them).
