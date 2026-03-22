---
name: n8n-errors-expressions
description: >
  Use when debugging expression evaluation failures or undefined
  references in n8n workflows. Prevents data access errors by mapping
  every expression variable to its valid context. Covers undefined $json
  references, type mismatches, missing paired items, $itemIndex
  unavailability in Code node, $secrets restriction in Code node,
  JMESPath parameter order confusion, empty expression results, and
  context-dependent variable availability.
  Keywords: n8n, expression, error, $json, variable, type mismatch.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n Expression Error Diagnosis

> Diagnose and fix expression evaluation failures in n8n v1.x workflows.
> For error type details see [references/methods.md](references/methods.md).
> For before/after fixes see [references/examples.md](references/examples.md).
> For anti-patterns see [references/anti-patterns.md](references/anti-patterns.md).

---

## Quick Diagnostic Table

| Symptom | Cause | Fix |
|---------|-------|-----|
| `undefined` when accessing `$json.field` | Field does not exist on current item | Check field name spelling; use `$json?.field` or `$ifEmpty($json.field, fallback)` |
| `TypeError: Cannot read properties of undefined` | Accessing nested field on null/undefined parent | Chain optional access: `$json.parent?.child?.value` |
| `$itemIndex is not defined` in Code node | `$itemIndex` is NOT available in Code node | Use `items.indexOf(item)` or loop index variable instead |
| `$secrets is not defined` in Code node | `$secrets` is NOT available in Code node | Use `$env.SECRET_NAME` or pass secret via preceding Set node |
| `$response is not defined` | `$response` used outside HTTP Request node | ONLY use `$response` in HTTP Request node parameter fields |
| `Paired item not found` | Item linking broken between nodes | Use `$("<Node>").first()` or `$("<Node>").all()[index]` instead of `.item` |
| JMESPath returns unexpected result | Parameter order swapped | ALWAYS use `$jmespath(object, searchString)` — object first, search second |
| Expression returns empty string | Field exists but value is `null`, `""`, or `undefined` | Use `$ifEmpty($json.field, "default")` to provide fallback |
| `$getWorkflowStaticData` returns empty | Static data not available during manual test | ALWAYS test static data with active workflow (webhook/trigger), NEVER manual execution |
| `TypeError: X is not a function` | Calling n8n extension method on wrong type | Verify data type: `.extractEmail()` requires string, `.average()` requires array |
| `$("<Node>").item` returns wrong data | Expression evaluated in non-matching context | Use `$("<Node>").itemMatching(index)` in Code node; use `.first()` or `.all()` for explicit access |
| Python `AttributeError` on item access | Using dot notation in Python Code node | ALWAYS use bracket notation: `item["json"]["field"]` |
| `$pageCount is not defined` | Used outside HTTP Request node pagination | `$pageCount` is ONLY available in HTTP Request node |
| Number treated as string in comparison | n8n expression returned string type | Explicitly convert: `Number($json.price)` or use `parseInt()`/`parseFloat()` |
| Date comparison fails | Comparing string dates instead of DateTime | Convert with `.toDateTime()` then compare with `.diffTo()` or `.isBetween()` |

---

## Variable Availability Matrix

Use this matrix to determine which variables are available in each context.

| Variable | Expression Fields | Code Node (JS) | Code Node (Python) | HTTP Request Node |
|----------|:-:|:-:|:-:|:-:|
| `$json` / `$binary` | YES | YES | `_json` / `_binary` | YES |
| `$input.item` | YES | YES (each-item mode) | `_item` | YES |
| `$input.all()` | YES | YES | `_items` | YES |
| `$("<Node>").item` | YES | NO (use `.itemMatching()`) | NO | YES |
| `$("<Node>").itemMatching()` | YES | YES | YES (`_("<Node>")`) | YES |
| `$itemIndex` | YES | **NO** | **NO** | YES |
| `$runIndex` | YES | YES | YES | YES |
| `$secrets` | YES | **NO** | **NO** | YES |
| `$env` | YES | YES | `_env` | YES |
| `$vars` | YES | YES | `_vars` | YES |
| `$now` / `$today` | YES | YES | YES | YES |
| `$execution` | YES | YES | `_execution` | YES |
| `$workflow` | YES | YES | `_workflow` | YES |
| `$prevNode` | YES | YES | YES | YES |
| `$response` | NO | NO | NO | **YES** |
| `$pageCount` | NO | NO | NO | **YES** |
| `$parameter` | YES | YES | YES | YES |
| `$ifEmpty()` | YES | YES | YES | YES |
| `$jmespath()` | YES | YES | `_jmespath()` | YES |
| `$getWorkflowStaticData()` | YES | YES | `_getWorkflowStaticData()` | YES |
| `$execution.customData` | YES | YES | `_execution` | YES |

---

## Decision Tree: Expression Not Working

```
Expression returns unexpected result
|
+-- Is the variable available in this context?
|   +-- NO --> Check Variable Availability Matrix above
|   +-- YES --> Continue
|
+-- Does the field exist on the item?
|   +-- Check with: {{ Object.keys($json) }}
|   +-- Field missing --> Fix field name or check upstream node output
|   +-- Field exists --> Continue
|
+-- Is the value null/undefined/empty?
|   +-- YES --> Use $ifEmpty($json.field, fallback)
|   +-- NO --> Continue
|
+-- Is the type correct?
|   +-- String where number expected --> Number($json.field)
|   +-- Number where string expected --> String($json.field)
|   +-- String where date expected --> $json.field.toDateTime()
|   +-- Type is correct --> Continue
|
+-- Is item linking the problem?
|   +-- "Paired item not found" error --> See Paired Item Errors below
|   +-- Wrong item data --> Use explicit .first()/.all() instead of .item
|   +-- Correct linking --> Check expression syntax
```

---

## Paired Item Error Resolution

When you see "Paired item not found" or get wrong data from `$("<Node>").item`:

1. **Identify the break point** — Item linking breaks when a node changes item count (e.g., aggregation, split, filter removes items).
2. **Use explicit access instead:**
   - `$("<Node>").first()` — ALWAYS returns first item (safe fallback)
   - `$("<Node>").all()[index]` — Access by position
   - `$("<Node>").itemMatching(currentIndex)` — Trace back from current item (preferred in Code node)
3. **In Code node** — NEVER use `$("<Node>").item`. ALWAYS use `$("<Node>").itemMatching(index)`.

---

## JMESPath Parameter Order

n8n uses `$jmespath(object, searchString)` — this is the OPPOSITE of the JMESPath spec's `search(searchString, object)`.

```js
// CORRECT — object first, search string second
{{ $jmespath($json.data, "[*].name") }}

// WRONG — search string first (JMESPath spec order)
{{ $jmespath("[*].name", $json.data) }}
```

ALWAYS verify: first argument is the data object, second argument is the query string.

---

## Static Data Pitfalls

`$getWorkflowStaticData()` has specific constraints:

- **NOT available during manual test execution** — returns empty object `{}`
- ONLY populated when workflow runs via trigger/webhook in production
- Data persists across executions but ONLY after successful completion
- NEVER store large data — keep static data small (IDs, timestamps, counters)
- May be unreliable during high-frequency parallel executions

---

## Common Error Messages Reference

| Error Message | Meaning | Resolution |
|---------------|---------|------------|
| `Expression evaluation error` | Generic expression parse failure | Check syntax: matching `{{ }}`, valid JS |
| `Cannot read properties of undefined (reading 'X')` | Accessing property on null/undefined | Add null checks: `$json.parent?.child` |
| `X is not a function` | Wrong method for data type | Check type: strings have `.extractEmail()`, arrays have `.average()` |
| `Paired item information is missing` | Item link chain broken | Use `.first()`, `.all()`, or `.itemMatching()` |
| `ReferenceError: $itemIndex is not defined` | Used in Code node | Use loop index or `items.indexOf(item)` |
| `ReferenceError: $secrets is not defined` | Used in Code node | Use `$env` or pass via Set node |
| `Invalid left-hand side in assignment` | Assignment `=` inside expression | Expressions are read-only; use Code node for assignment |
| `Unexpected token` | Syntax error in expression | Check for unmatched brackets, quotes, or template literals |

---

## Code Node Specific Restrictions

ALWAYS remember these restrictions when writing Code node logic:

1. `$itemIndex` — **NOT available**. Use loop index or `items.indexOf(item)`.
2. `$secrets` — **NOT available**. Use `$env.SECRET_NAME` instead.
3. `$("<Node>").item` — **NOT recommended**. Use `$("<Node>").itemMatching(index)`.
4. No HTTP requests — use HTTP Request node before/after Code node.
5. No file system access — use Read/Write Files nodes.
6. Python: ALWAYS use bracket notation `item["json"]["field"]`, NEVER dot notation.
7. Python on Cloud: NEVER import external libraries.

---

## $response Context Restriction

`$response` is ONLY available in HTTP Request node parameter fields:

| Property | Returns | Context |
|----------|---------|---------|
| `$response.body` | Response body object | HTTP Request node ONLY |
| `$response.headers` | Response headers | HTTP Request node ONLY |
| `$response.statusCode` | HTTP status code | HTTP Request node ONLY |
| `$response.statusMessage` | Status message | HTTP Request node ONLY |

If you need HTTP response data in other nodes, the HTTP Request node automatically outputs the response as `$json` for downstream nodes.

---

## Null/Undefined Handling Strategy

ALWAYS handle potentially missing data with one of these approaches:

1. **`$ifEmpty(value, fallback)`** — Best for simple fallback values
2. **Optional chaining** — `$json.parent?.child?.value` for nested access
3. **Ternary** — `{{ $json.field ? $json.field : "default" }}` for conditional logic
4. **IIFE for complex logic:**
   ```js
   {{ (function() {
     const val = $json.field;
     if (val === null || val === undefined) return "N/A";
     return val.toString();
   })() }}
   ```

---

## Type Conversion Quick Reference

| From | To | Method |
|------|----|--------|
| String | Number | `Number($json.field)` or `parseInt()` / `parseFloat()` |
| String | Boolean | `$json.field.toBoolean()` |
| String | DateTime | `$json.field.toDateTime()` |
| Number | String | `String($json.field)` or `$json.field.format()` |
| Number | Boolean | `$json.field.toBoolean()` (0 = false, else true) |
| Number | DateTime | `$json.field.toDateTime()` (Unix ms or seconds) |
| Boolean | Number | `$json.field.toNumber()` (true=1, false=0) |
| Boolean | String | `$json.field.toString()` |
| Array | String | `$json.arr.toJsonString()` |
| Object | String | `$json.obj.toJsonString()` |

---

## Reference Files

- [references/methods.md](references/methods.md) — Expression error types and variable availability details
- [references/examples.md](references/examples.md) — Common expression errors with before/after fixes
- [references/anti-patterns.md](references/anti-patterns.md) — Expression anti-patterns to avoid
