---
name: n8n-syntax-expressions
description: >
  Use when writing n8n expressions, accessing node data, using JMESPath, or
  debugging expression errors. Prevents incorrect variable references and
  expression context mistakes. Covers all built-in variables ($json, $input,
  $node, $workflow, $execution, $env, $vars, $now, $today), JMESPath queries
  ($jmespath), paired items, static workflow data ($getWorkflowStaticData),
  utility functions ($ifEmpty), and expression context rules.
  Keywords: n8n, expressions, $json, $input, $node, JMESPath, $env, $vars,
  paired items, $getWorkflowStaticData.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n-syntax-expressions

## Quick Reference

### Expression Syntax

All n8n expressions use double-curly-brace syntax inside node parameter fields:

```
{{ expression }}
```

Expressions support standard JavaScript operations plus n8n-specific built-in variables.

### Current Node Input

| Variable | Returns | Description |
|----------|---------|-------------|
| `$json` | Object | Shorthand for `$input.item.json` — current item's JSON data |
| `$binary` | Object | Shorthand for `$input.item.binary` — current item's binary data |
| `$input.item` | Item | The input item currently being processed |
| `$input.all()` | Array\<Item\> | All input items from the current node |
| `$input.first()` | Item | First input item |
| `$input.last()` | Item | Last input item |
| `$input.params` | Object | Node configuration settings and operation parameters |

### Other Node Output

| Variable | Returns | Description |
|----------|---------|-------------|
| `$("node-name").all()` | Array\<Item\> | All items from named node output |
| `$("node-name").first()` | Item | First item from named node |
| `$("node-name").last()` | Item | Last item from named node |
| `$("node-name").item` | Item | Linked item via paired items tracking |
| `$("node-name").itemMatching(index)` | Item | Traces back to matching item (preferred in Code node) |
| `$("node-name").params` | Object | Query settings/parameters of named node |
| `$("node-name").context` | Object | Only available with Loop Over Items node |
| `$("node-name").isExecuted` | Boolean | True if the node has executed |

### Workflow & Execution Metadata

| Variable | Returns | Description |
|----------|---------|-------------|
| `$workflow.id` | String | Workflow ID |
| `$workflow.name` | String | Workflow name |
| `$workflow.active` | Boolean | Whether workflow is active |
| `$execution.id` | String | Unique execution ID |
| `$execution.mode` | String | `"test"`, `"production"`, or `"evaluation"` |
| `$execution.resumeUrl` | String | Webhook URL to resume at a Wait node |
| `$execution.resumeFormUrl` | String | URL for Wait node form |
| `$execution.customData` | CustomData | Get/set custom execution data |

### Environment & Configuration

| Variable | Returns | Description |
|----------|---------|-------------|
| `$env` | Object | Instance environment variables |
| `$vars` | Object | Active environment variables (all strings) |
| `$secrets` | Object | External secrets (**NOT available in Code node**) |

### Date & Time (Luxon DateTime)

| Variable | Returns | Description |
|----------|---------|-------------|
| `$now` | DateTime | Current moment, respects workflow timezone |
| `$today` | DateTime | Midnight at start of current day |

### Node Execution Context

| Variable | Returns | Description |
|----------|---------|-------------|
| `$prevNode.name` | String | Name of previous node |
| `$prevNode.outputIndex` | Number | Output connector index |
| `$prevNode.runIndex` | Number | Run of previous node |
| `$runIndex` | Number | How many times current node has executed (zero-based) |
| `$itemIndex` | Number | Current item position (**NOT available in Code node**) |
| `$parameter` | Object | Configuration settings of current node |
| `$nodeVersion` | Number | Current node version |
| `$pageCount` | Number | Results pages fetched (HTTP Request node only) |

### Utility Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `$ifEmpty(value, fallback)` | any | Returns `value` if non-empty, otherwise `fallback` |
| `$jmespath(object, searchString)` | any | JMESPath query on a JSON object |
| `$getWorkflowStaticData(type)` | Object | Persistent data. Type: `"global"` or `"node"` |

### HTTP Response (HTTP Request Node Only)

| Variable | Returns | Description |
|----------|---------|-------------|
| `$response.body` | Object | Response body from last HTTP call |
| `$response.headers` | Object | Response headers |
| `$response.statusCode` | Number | HTTP status code |
| `$response.statusMessage` | String | Optional status message |

---

## Critical Warnings

**NEVER** use `$itemIndex` in the Code node -- it is NOT available there. Use a loop counter or `items.indexOf()` instead.

**NEVER** use `$secrets` in the Code node -- it is NOT available there. Pass secret values via node parameters or use `$env` / `$vars` instead.

**NEVER** reverse the parameter order of `$jmespath()` -- it is `$jmespath(object, searchString)`, NOT `$jmespath(searchString, object)`. The n8n implementation differs from the JMESPath specification's `search(searchString, object)` pattern.

**NEVER** use `new Date()` in expressions -- ALWAYS use Luxon's `$now`, `$today`, `DateTime.fromISO()`, or `DateTime.fromFormat()` for consistent timezone handling.

**NEVER** rely on `$getWorkflowStaticData()` during manual test executions -- static data requires an active workflow with a trigger or webhook.

**NEVER** store large data objects in workflow static data -- keep it small. Large data causes performance degradation.

**ALWAYS** use `$json` as the primary way to access current item data -- it is shorthand for `$input.item.json`.

**ALWAYS** use `$("Node Name").item` in expressions for linked item access. In Code nodes, use `$("Node Name").itemMatching(index)` instead.

**ALWAYS** use `$ifEmpty(value, fallback)` for safe null/undefined handling -- it covers `""`, `[]`, `{}`, `null`, and `undefined`.

**ALWAYS** use bracket notation for dynamic property access: `$json["field-with-dashes"]`.

---

## Essential Patterns

### Pattern 1: Access Current Item Data

```
{{ $json.name }}
{{ $json.address.city }}
{{ $json["field-with-dashes"] }}
```

### Pattern 2: Access Other Node Output

```
{{ $("HTTP Request").item.json.data }}
{{ $("Get Users").first().json.email }}
{{ $("Webhook").all().length }}
```

### Pattern 3: Conditional Expressions

```
{{ $json.status === "active" ? "Yes" : "No" }}
{{ $ifEmpty($json.nickname, $json.fullName) }}
```

### Pattern 4: JMESPath Query

```
{{ $jmespath($json.data, "[*].name") }}
{{ $jmespath($("Code").all(), "[?json.active==`true`].json.id") }}
```

### Pattern 5: Date Operations (Luxon)

```
{{ $now.format("yyyy-MM-dd HH:mm:ss") }}
{{ $today.minus({days: 7}).toISO() }}
{{ $now.toRelative() }}
```

### Pattern 6: Static Workflow Data (Persistence)

```js
// In Code node — data persists across executions
const staticData = $getWorkflowStaticData('global');
const lastRun = staticData.lastExecution;
staticData.lastExecution = new Date().toISOString();
// n8n saves automatically on successful execution
```

### Pattern 7: IIFE for Multi-Statement Expressions

```
{{ (function() { const x = $json.price * 1.21; return x.toFixed(2); })() }}
```

### Pattern 8: Custom Execution Data

```js
// Set data
$execution.customData.set("user_email", "me@example.com");
$execution.customData.setAll({"key1": "val1", "key2": "val2"});

// Get data
const email = $execution.customData.get("user_email");
const all = $execution.customData.getAll();
```

### Pattern 9: Paired Items (Item Linking)

Every output item links back to the input items that produced it. This enables:

- Automatic item resolution in drag-and-drop mapping
- `$("Node").item` — access the linked item in expressions
- `$("Node").itemMatching(index)` — trace item origin in Code node

When a node processes multiple items, `{{ $json.fruit }}` dynamically resolves to each item's value during iteration.

---

## $ifEmpty Behavior

`$ifEmpty(value, fallback)` returns `fallback` when `value` is any of:

| Value | Considered Empty |
|-------|-----------------|
| `""` | Yes |
| `[]` | Yes |
| `{}` | Yes |
| `null` | Yes |
| `undefined` | Yes |
| `0` | No |
| `false` | No |

---

## Expression Context Rules

| Context | Available Variables |
|---------|-------------------|
| Node parameter fields | ALL `$` variables |
| Code node (JavaScript) | ALL except `$itemIndex` and `$secrets` |
| Code node (Python) | `_` prefix variants (e.g., `_json`, `_env`, `_vars`) |
| Credential fields | `$credentials` object only |
| HTTP Request node | ALL plus `$response` and `$pageCount` |
| Loop Over Items | ALL plus `$("Loop Node").context` |

---

## Reference Links

- [references/methods.md](references/methods.md) -- All $ variables with signatures, return types, descriptions
- [references/examples.md](references/examples.md) -- Expression patterns, JMESPath, static data, IIFE patterns
- [references/anti-patterns.md](references/anti-patterns.md) -- Expression mistakes, context confusion

### Official Sources

- https://docs.n8n.io/code/expressions/
- https://docs.n8n.io/code/builtin/overview/
- https://docs.n8n.io/code/builtin/current-node-input/
- https://docs.n8n.io/code/builtin/output-other-nodes/
- https://docs.n8n.io/code/builtin/n8n-metadata/
- https://docs.n8n.io/data/jmespath/
