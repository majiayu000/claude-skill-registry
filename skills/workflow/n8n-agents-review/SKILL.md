---
name: n8n-agents-review
description: >
  Use when reviewing n8n workflows or validating workflow JSON before
  deployment. Prevents production errors by catching anti-patterns in
  node configuration, connection wiring, and expression syntax. Covers
  workflow JSON structure, node configuration, connection wiring,
  expression syntax, credential setup, error handling patterns,
  deployment configuration, and known anti-patterns.
  Keywords: n8n, review, validation, workflow, audit, anti-pattern.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n Workflow & Code Review Agent

> Run this checklist against ANY n8n workflow JSON, custom node code, or deployment configuration to catch errors before they reach production.

## Quick Reference — Review Areas

| Area | Critical Checks | Reference |
|------|----------------|-----------|
| Workflow JSON | IConnections 3-level nesting, unique node names, required fields | [methods.md](references/methods.md#1-workflow-json-validation) |
| Connection Wiring | Type matching, correct indices, no orphan nodes | [methods.md](references/methods.md#2-connection-wiring) |
| Expressions | Valid variable refs, context restrictions, JMESPath order | [methods.md](references/methods.md#3-expression-validation) |
| Credentials | ICredentialType completeness, authenticate method, test endpoint | [methods.md](references/methods.md#4-credential-validation) |
| Node Types | INodeType interface, execute return type, property types | [methods.md](references/methods.md#5-node-type-validation) |
| Error Handling | Error workflow, continueOnFail, retry config | [methods.md](references/methods.md#6-error-handling) |
| Deployment | Encryption key, queue mode, volume mounts, PostgreSQL | [methods.md](references/methods.md#7-deployment-validation) |
| Code Node | Return format, restricted variables, sandbox limits | [methods.md](references/methods.md#8-code-node-validation) |
| Security | No hardcoded secrets, encryption, task runners | [methods.md](references/methods.md#9-security-validation) |
| Anti-Patterns | Consolidated list from all skill areas | [anti-patterns.md](references/anti-patterns.md) |

---

## Decision Tree — Review Workflow

```
START: What are you reviewing?
├─ Workflow JSON file (.json)
│  ├─ Run: Workflow JSON checks (Section 1)
│  ├─ Run: Connection Wiring checks (Section 2)
│  ├─ Run: Expression checks on all parameter values (Section 3)
│  ├─ Run: Error Handling checks (Section 6)
│  └─ Run: Anti-Pattern scan (Section 10)
│
├─ Custom node code (.node.ts)
│  ├─ Run: Node Type checks (Section 5)
│  ├─ Run: Credential checks if node uses credentials (Section 4)
│  ├─ Run: Error Handling checks (Section 6)
│  └─ Run: Anti-Pattern scan (Section 10)
│
├─ Credential definition (.credentials.ts)
│  └─ Run: Credential checks (Section 4)
│
├─ Code node content
│  ├─ Run: Code Node checks (Section 8)
│  └─ Run: Anti-Pattern scan (Section 10)
│
├─ Deployment config (docker-compose.yml / env vars)
│  ├─ Run: Deployment checks (Section 7)
│  └─ Run: Security checks (Section 9)
│
└─ Full project audit
   └─ Run ALL sections sequentially
```

---

## 1. Workflow JSON Validation

ALWAYS verify these required fields on every node in `nodes[]`:

| Field | Type | Rule |
|-------|------|------|
| `id` | string | MUST be unique UUID |
| `name` | string | MUST be unique within the workflow |
| `type` | string | MUST match a registered node type (e.g., `n8n-nodes-base.httpRequest`) |
| `typeVersion` | number | MUST be a valid version for the node type |
| `position` | [number, number] | MUST be `[x, y]` coordinate array |
| `parameters` | object | MUST exist (can be empty `{}`) |

ALWAYS verify the workflow root object contains:
- `id` (string)
- `name` (string)
- `active` (boolean)
- `nodes` (array)
- `connections` (object)

NEVER accept a workflow where two nodes share the same `name` — connections reference nodes by name, so duplicates break wiring.

---

## 2. Connection Wiring Validation

IConnections uses **3-level nesting**:

```
connections[sourceNodeName][connectionType][outputIndex] = IConnection[]
```

ALWAYS verify:
1. Every key in `connections` matches a `name` in `nodes[]`
2. Every `IConnection.node` value matches a `name` in `nodes[]`
3. `IConnection.type` is a valid `NodeConnectionType` (usually `"main"`)
4. `IConnection.index` does not exceed the destination node's input count
5. Trigger nodes (`group: ['trigger']`) have NO incoming connections
6. Non-trigger nodes have at least one incoming connection (unless intentionally orphaned)
7. Multi-output nodes (IF, Switch) have the correct number of output arrays

**IF node pattern**: `connections["IF"].main` MUST have exactly 2 arrays — index 0 for true, index 1 for false.

---

## 3. Expression Validation

ALWAYS verify expressions (`{{ ... }}`) use correct variable references:

| Context | Available | NOT Available |
|---------|-----------|---------------|
| Any expression | `$json`, `$binary`, `$input`, `$execution`, `$workflow`, `$now`, `$today`, `$env`, `$vars`, `$prevNode`, `$runIndex`, `$parameter` | — |
| Code node | All `$` vars except `$itemIndex` and `$secrets` | `$itemIndex`, `$secrets` |
| Python Code node | `_` prefix versions (`_json`, `_items`) | `$` prefix, dot notation on items |

ALWAYS verify `$jmespath(object, searchString)` parameter order — object FIRST, search string SECOND. This differs from the JMESPath spec.

NEVER allow `$("<NodeName>")` to reference a node name that does not exist in the workflow.

---

## 4. Credential Validation

ALWAYS verify `ICredentialType` implementations include:

| Property | Required | Rule |
|----------|----------|------|
| `name` | YES | Internal identifier, matches node's credential reference |
| `displayName` | YES | Human-readable label |
| `properties` | YES | Array of `INodeProperties[]` defining input fields |
| `authenticate` | YES | Method with `type: 'generic'` and `properties` object |
| `test` | RECOMMENDED | `ICredentialTestRequest` with test endpoint |

ALWAYS verify `authenticate.type` is `'generic'` — other values are not supported.

ALWAYS verify credential expressions use `$credentials` prefix: `={{$credentials.apiKey}}`.

NEVER allow credentials to be hardcoded in node parameters — ALWAYS use credential references.

---

## 5. Node Type Validation

ALWAYS verify `INodeType` implementations:

| Check | Expected | Common Failure |
|-------|----------|----------------|
| `description` property | `INodeTypeDescription` with all required fields | Missing `inputs`, `outputs`, or `properties` |
| `execute()` return type | `Promise<INodeExecutionData[][]>` | Returning single array `[]` instead of `[[]]` |
| Trigger nodes | `inputs: []` and `group: ['trigger']` | Having inputs on trigger nodes |
| Property `type` values | Valid `NodePropertyTypes` | Using invalid type strings |
| `displayOptions` | References existing property names/values | Referencing non-existent parameters |
| `credentials` array | Each entry has `name` matching a credential type | Credential name mismatch |

ALWAYS verify `execute()` returns `[returnData]` (wrapped in outer array), NOT just `returnData`.

ALWAYS verify each item in the return array has a `json` property: `{ json: { ... } }`.

---

## 6. Error Handling Validation

ALWAYS verify:

1. **Error workflow configured** — `settings.errorWorkflow` is set in production workflows
2. **continueOnFail pattern** — nodes using `this.continueOnFail()` include error data in output:
   ```typescript
   returnData.push({ json: { error: error.message }, pairedItem: { item: i } });
   ```
3. **Retry on transient failures** — HTTP/API nodes set `retryOnFail: true`, `maxTries >= 2`, `waitBetweenTries >= 1000`
4. **Error node exists** — at least one Error Trigger workflow is available for the instance
5. **`onError` setting** — nodes specify behavior: `'continueErrorOutput'`, `'continueRegularOutput'`, or `'stopWorkflow'`

NEVER allow a production workflow without an error workflow — silent failures are unacceptable.

---

## 7. Deployment Validation

ALWAYS verify for production deployments:

| Check | Expected | Consequence of Missing |
|-------|----------|----------------------|
| `N8N_ENCRYPTION_KEY` | Explicitly set and backed up | Key regeneration locks out all credentials |
| `NODE_ENV` | `production` | Missing production optimizations |
| `N8N_PROTOCOL` | `https` | Credentials transmitted in cleartext |
| `WEBHOOK_URL` | Set to public URL | Webhooks unreachable externally |
| `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS` | `true` | Settings file readable by other users |
| `N8N_RUNNERS_ENABLED` | `true` | Code runs in main process (security risk) |
| Volume: `/home/node/.n8n` | Mounted to persistent volume | Data lost on container restart |

**Queue mode additional requirements**:

| Check | Expected | Consequence of Missing |
|-------|----------|----------------------|
| `DB_TYPE` | `postgresdb` | SQLite does NOT support queue mode |
| `EXECUTIONS_MODE` | `queue` | Workers will not process jobs |
| Redis configured | `QUEUE_BULL_REDIS_HOST` + port | Queue has no broker |
| Shared `N8N_ENCRYPTION_KEY` | Same key on main + all workers | Credential decryption fails |
| S3 binary storage | Configured for shared access | Binary data inaccessible across instances |

---

## 8. Code Node Validation

ALWAYS verify Code node content:

| Check | Rule |
|-------|------|
| Return format (all items) | MUST return `[{json: {...}}, ...]` — array of objects with `json` key |
| Return format (each item) | MUST return `{json: {...}}` — single object with `json` key |
| No `$itemIndex` | NEVER use `$itemIndex` in Code node — it is not available |
| No `$secrets` | NEVER use `$secrets` in Code node — it is not available |
| No HTTP requests | NEVER make HTTP calls in Code node — use HTTP Request node |
| No file system access | NEVER access files directly — use Read/Write Files nodes |
| Python bracket notation | ALWAYS use `item["json"]["field"]`, NEVER `item.json.field` in Python |
| Binary data access | ALWAYS use `this.helpers.getBinaryDataBuffer()`, NEVER direct buffer access |

---

## 9. Security Validation

ALWAYS verify:

1. **No hardcoded credentials** — API keys, tokens, passwords NEVER in node parameters or Code node
2. **Encryption key set** — `N8N_ENCRYPTION_KEY` is explicitly configured (not auto-generated)
3. **Task runners enabled** — `N8N_RUNNERS_ENABLED=true` (isolates Code node execution)
4. **File access restricted** — `N8N_RESTRICT_FILE_ACCESS_TO` limits filesystem paths
5. **Settings permissions** — `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true`
6. **Env access blocked** — `N8N_BLOCK_ENV_ACCESS_IN_NODE=true` if env vars contain secrets
7. **Webhook authentication** — production webhooks use Basic Auth, Header Auth, or JWT
8. **HTTPS enforced** — `N8N_PROTOCOL=https` with valid TLS termination
9. **Secure cookies** — `N8N_SECURE_COOKIE=true` in HTTPS deployments

---

## 10. Anti-Pattern Detection

Scan for ALL anti-patterns listed in [anti-patterns.md](references/anti-patterns.md). Key categories:

- **Expression anti-patterns**: Wrong variable context, reversed JMESPath args, `new Date()` instead of Luxon
- **Code node anti-patterns**: Restricted variables, wrong return format, direct binary access
- **Credential anti-patterns**: Hardcoded secrets, missing test endpoint, wrong authenticate type
- **Deployment anti-patterns**: Missing encryption key, SQLite in production, no volume mounts
- **Workflow anti-patterns**: No error workflow, duplicate node names, orphan nodes

---

## Review Report Template

After completing all applicable checks, produce a report:

```markdown
## n8n Review Report

**Target**: [filename or description]
**Type**: [Workflow JSON | Custom Node | Credential | Deployment Config | Code Node]
**Date**: [date]

### Summary
- Total checks: [N]
- Passed: [N]
- Failed: [N]
- Warnings: [N]

### Critical Failures
1. [Area] — [What failed] — [Expected state] — [How to fix]

### Warnings
1. [Area] — [What to improve] — [Recommendation]

### Anti-Patterns Detected
1. [AP-XXX] — [Description] — [Location in code/config]
```

---

## Reference Links

- [Validation Methods (Complete Checklist)](references/methods.md)
- [Review Examples (Good/Bad/Fix)](references/examples.md)
- [Anti-Pattern Catalog](references/anti-patterns.md)
