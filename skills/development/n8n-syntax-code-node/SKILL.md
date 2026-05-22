---
name: n8n-syntax-code-node
description: >
  Use when writing Code node logic in n8n workflows with JavaScript or Python.
  Prevents misuse of unavailable variables ($itemIndex, $secrets) or restricted
  modules (fs, http). Covers runOnceForAllItems vs runOnceForEachItem execution,
  available variables ($input, $json, items), binary data handling, built-in
  modules, $() node access, Python _ prefix convention, and restrictions.
  Keywords: n8n, Code node, JavaScript, Python, $input, $json, items.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n Code Node

> Complete reference for the n8n v1.x Code node — JavaScript and Python modes, execution models, available variables, binary data, restrictions, and return format.

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Languages | JavaScript (Node.js) — always available; Python — requires `N8N_PYTHON_ENABLED=true` (stable v1.111.0+) |
| Default mode | Run Once for All Items |
| Return format | MUST return `[{json: {...}}]` (all-items) or `{json: {...}}` (each-item) |
| Environment | Sandboxed — no filesystem, no HTTP, no `$itemIndex`, no `$secrets`, no `$parameter` |

## CRITICAL: 5 Restrictions

These restrictions apply to ALL Code node executions. Violating them causes runtime errors.

1. **NO filesystem access** — NEVER use `fs`, `path`, or any file I/O. Use Read/Write Files From Disk nodes instead.
2. **NO HTTP requests** — NEVER use `fetch`, `axios`, or `http`. Use the HTTP Request node instead.
3. **NO `$itemIndex`** — This variable is NOT available in the Code node. Track index manually with a loop counter.
4. **NO `$secrets`** — External secrets are NOT accessible in Code node. Pass secret values through preceding node output.
5. **NO `$parameter`** — Node configuration parameters are NOT available. Hardcode values or pass them as input data.

## Execution Mode Decision Tree

```
Need to write Code node logic?
├── Processing items independently (filter, transform, enrich)?
│   └── Use "Run Once for Each Item"
│       ├── JS: access current item via $input.item.json
│       └── Python: access current item via _item["json"]
├── Need to compare/aggregate across ALL items (sort, deduplicate, summarize)?
│   └── Use "Run Once for All Items" (default)
│       ├── JS: access all items via items array
│       └── Python: access all items via _items list
└── Can a native node do this instead (Set, Filter, Sort, Merge)?
    └── ALWAYS prefer native nodes — they are faster and maintain item linking
```

## Return Format

### Run Once for All Items — MUST Return Array

```javascript
// JavaScript — ALWAYS return an array of {json: {...}} objects
return items.map(item => ({
  json: { name: item.json.name, processed: true }
}));
```

```python
# Python — ALWAYS return a list of {"json": {...}} dicts
return [{"json": {"name": item["json"]["name"], "processed": True}} for item in _items]
```

### Run Once for Each Item — Return Single Object

```javascript
// JavaScript — return ONE {json: {...}} object
return { json: { name: $input.item.json.name, processed: true } };
```

```python
# Python — return ONE {"json": {...}} dict
return {"json": {"name": _item["json"]["name"], "processed": True}}
```

> **NEVER** return raw data without the `json` wrapper. The format `{json: {...}}` is mandatory.

## Available Variables

### JavaScript Variables

| Variable | Mode | Description |
|----------|------|-------------|
| `items` | All Items | Array of all input items |
| `$input.item` | Each Item | Current item being processed |
| `$input.all()` | Both | All input items from current node |
| `$input.first()` | Both | First input item |
| `$input.last()` | Both | Last input item |
| `$json` | Each Item | Shorthand for `$input.item.json` |
| `$binary` | Each Item | Shorthand for `$input.item.binary` |
| `$("<node>").all()` | Both | All items from named node |
| `$("<node>").first()` | Both | First item from named node |
| `$("<node>").itemMatching(i)` | Both | Trace back to matching item in named node |
| `$execution.id` | Both | Current execution ID |
| `$execution.mode` | Both | `"test"`, `"production"`, or `"evaluation"` |
| `$execution.customData` | Both | Get/set custom execution metadata |
| `$workflow.id` | Both | Workflow ID |
| `$workflow.name` | Both | Workflow name |
| `$workflow.active` | Both | Whether workflow is active |
| `$now` | Both | Current DateTime (Luxon), respects timezone |
| `$today` | Both | Midnight today (Luxon) |
| `$env` | Both | Instance environment variables |
| `$vars` | Both | User-defined variables (all strings) |
| `$prevNode.name` | Both | Name of previous node |
| `$runIndex` | Both | How many times current node has executed |
| `$jmespath(obj, query)` | Both | JMESPath query function |
| `$ifEmpty(val, fallback)` | Both | Null-safe fallback |
| `$getWorkflowStaticData(type)` | Both | Persistent data (`"global"` or `"node"`) |

### Python Variables

Python uses `_` prefix instead of `$`:

| Python Variable | JavaScript Equivalent |
|----------------|----------------------|
| `_items` | `items` |
| `_item` | `$input.item` |
| `_input` | `$input` |
| `_execution` | `$execution` |
| `_workflow` | `$workflow` |
| `_env` | `$env` |
| `_vars` | `$vars` |
| `_jmespath(obj, query)` | `$jmespath(obj, query)` |
| `_getWorkflowStaticData(type)` | `$getWorkflowStaticData(type)` |
| `_prevNode` | `$prevNode` |
| `_now` | `$now` |
| `_today` | `$today` |

**Python-specific rules:**
- ALWAYS use bracket notation: `item["json"]["field"]` — dot notation fails
- On n8n Cloud: NEVER import external libraries
- Self-hosted: standard library + allowlisted third-party modules only
- `getBinaryDataBuffer()` is NOT supported in Python

## Binary Data Handling

```javascript
// Get binary buffer (JavaScript only, NOT available in Python)
const buffer = await this.helpers.getBinaryDataBuffer(itemIndex, 'data');

// Create new item with binary data from base64
return [{
  json: { fileName: 'output.txt' },
  binary: {
    data: await this.helpers.prepareBinaryData(
      Buffer.from('file content', 'utf-8'),
      'output.txt',
      'text/plain'
    )
  }
}];
```

> **NEVER** access binary data directly via `items[0].binary.data.data`. ALWAYS use `getBinaryDataBuffer()`.

## Built-in Modules

| Module | Availability |
|--------|-------------|
| Node.js `crypto` | Cloud + Self-hosted |
| `moment` (npm package) | Cloud + Self-hosted |
| Luxon (via expressions) | Cloud + Self-hosted |
| External npm modules | Self-hosted only (requires env config) |

## Item Linking in Code Node

ALWAYS use `$("<node>").itemMatching(index)` in Code node — NOT `$("<node>").item`:

```javascript
// Correct — Code node item tracing
const originalData = $("HTTP Request").itemMatching(0).json;

// Wrong — .item does not work reliably in Code node
// const originalData = $("HTTP Request").item.json;
```

## Error Handling

```javascript
// Try-catch pattern for Code node
try {
  const value = items[0].json.requiredField;
  if (!value) throw new Error('requiredField is missing');
  return [{ json: { result: value } }];
} catch (error) {
  // Return error as data (workflow continues)
  return [{ json: { error: error.message } }];
}
```

## When NOT to Use Code Node

ALWAYS prefer native nodes for these operations:

| Operation | Use Instead |
|-----------|-------------|
| Filter items | Filter node |
| Set/rename fields | Edit Fields (Set) node |
| Sort items | Sort node |
| Remove duplicates | Remove Duplicates node |
| Limit items | Limit node |
| Split arrays | Split Out node |
| Merge data | Merge node |
| Date/time formatting | Expressions with Luxon |
| Simple conditionals | IF / Switch node |

Native nodes are faster (no sandbox overhead) and maintain automatic item linking.

## Reference Files

- [references/methods.md](references/methods.md) — Complete variable reference per mode, built-in modules, return format details
- [references/examples.md](references/examples.md) — JavaScript and Python patterns: item manipulation, binary data, aggregation
- [references/anti-patterns.md](references/anti-patterns.md) — Common Code node mistakes with corrections

## Sources

- n8n Code node documentation: `n8n-io/n8n-docs` (main branch)
- n8n Code node source: `packages/nodes-base/nodes/Code/Code.node.ts`
- n8n Expression reference: `docs/data/expression-reference/`
- n8n Binary data reference: `docs/data/specific-data-types/binary-data.md`
