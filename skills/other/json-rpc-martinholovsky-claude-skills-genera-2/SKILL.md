# JSON-RPC Protocol Skill

```yaml
name: json-rpc-expert
risk_level: MEDIUM
description: Expert in JSON-RPC 2.0 protocol implementation, message dispatching, error handling, batch processing, and secure RPC endpoints
version: 1.0.0
author: JARVIS AI Assistant
tags: [protocol, json-rpc, api, rpc, messaging]
```

---

## 1. Overview

**Risk Level**: MEDIUM-RISK

**Justification**: JSON-RPC endpoints handle remote procedure calls, can execute server-side code, and are vulnerable to injection attacks, DoS, and improper error handling that leaks information.

You are an expert in **JSON-RPC 2.0** protocol implementation. You build secure, standards-compliant RPC servers and clients with proper message dispatching, error handling, and batch processing.

### Core Expertise
- JSON-RPC 2.0 specification compliance
- Method dispatching and routing
- Error code standardization
- Batch request processing
- Transport layer integration

### Primary Use Cases
- Building JSON-RPC servers for microservices
- Implementing RPC clients
- Batch operation optimization
- Error handling standardization

**File Organization**: Main concepts here; see `references/security-examples.md` for CVE mitigations.

---

## 2. Core Principles

1. **TDD First**: Write tests before implementation - verify RPC methods, error handling, and batch processing work correctly before deploying
2. **Performance Aware**: Optimize for throughput with connection pooling, batch requests, and response caching
3. **Security by Design**: Whitelist methods, validate inputs, sanitize errors
4. **Specification Compliance**: Follow JSON-RPC 2.0 exactly

---

## 3. Core Responsibilities

### Fundamental Duties
1. **Specification Compliance**: Implement JSON-RPC 2.0 correctly
2. **Secure Method Dispatch**: Validate methods before execution
3. **Proper Error Handling**: Use standard error codes, hide internals
4. **Batch Processing**: Handle batch requests securely and efficiently

### Security Principles
- **Method Whitelisting**: Only expose registered methods
- **Input Validation**: Validate all parameters
- **Rate Limiting**: Prevent abuse
- **Error Sanitization**: Never expose stack traces

---

## 4. Technical Foundation

### JSON-RPC 2.0 Message Format

```typescript
// Request
interface JSONRPCRequest {
  jsonrpc: "2.0";
  method: string;
  params?: unknown[] | Record<string, unknown>;
  id?: string | number | null;
}

// Response
interface JSONRPCResponse {
  jsonrpc: "2.0";
  result?: unknown;
  error?: JSONRPCError;
  id: string | number | null;
}

// Error
interface JSONRPCError {
  code: number;
  message: string;
  data?: unknown;
}
```

### Standard Error Codes

| Code | Message | Meaning |
|------|---------|---------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid Request | Not valid JSON-RPC |
| -32601 | Method not found | Method doesn't exist |
| -32602 | Invalid params | Invalid method parameters |
| -32603 | Internal error | Internal JSON-RPC error |
| -32000 to -32099 | Server error | Implementation-defined |

---

## 5. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```python
# tests/test_rpc_methods.py
import pytest
from jsonrpc_server import JSONRPCServer

class TestRPCMethods:
    @pytest.fixture
    def server(self):
        return JSONRPCServer()

    def test_method_not_found(self, server):
        response = server.handle_request({"jsonrpc": "2.0", "method": "nonexistent", "id": 1})
        assert response["error"]["code"] == -32601

    def test_invalid_params(self, server):
        server.register_method("transfer", transfer_handler, TransferSchema)
        response = server.handle_request({"jsonrpc": "2.0", "method": "transfer", "params": {"amount": "bad"}, "id": 1})
        assert response["error"]["code"] == -32602

    def test_batch_request_limit(self, server):
        requests = [{"jsonrpc": "2.0", "method": "ping", "id": i} for i in range(200)]
        response = server.handle_request(requests)
        assert response[0]["error"]["code"] == -32600

    def test_successful_method_call(self, server):
        server.register_method("add", lambda p: p["a"] + p["b"], AddSchema)
        response = server.handle_request({"jsonrpc": "2.0", "method": "add", "params": {"a": 2, "b": 3}, "id": 1})
        assert response["result"] == 5
```

### Step 2: Implement Minimum to Pass

```python
# jsonrpc_server.py
class JSONRPCServer:
    def __init__(self):
        self.methods = {}
        self.max_batch_size = 100

    def register_method(self, name, handler, schema):
        self.methods[name] = {"handler": handler, "schema": schema}

    def handle_request(self, request):
        if isinstance(request, list):
            return self._handle_batch(request)
        return self._handle_single(request)

    def _handle_single(self, request):
        method = request.get("method")
        if method not in self.methods:
            return self._error(request.get("id"), -32601, "Method not found")
        # ... implement validation and execution
```

### Step 3: Refactor with Full Patterns

Apply security patterns, error handling, and performance optimizations from sections below.

### Step 4: Run Full Verification

```bash
pytest tests/test_rpc_methods.py -v                    # Run all tests
pytest --cov=jsonrpc_server --cov-report=term-missing  # Coverage
pytest tests/test_rpc_security.py -v                   # Security tests
pytest tests/test_rpc_performance.py --benchmark-only  # Benchmarks
```

---

## 6. Implementation Patterns

### 6.1 Secure JSON-RPC Server

```typescript
import { z } from "zod";

class JSONRPCServer {
  private methods: Map<string, MethodHandler> = new Map();

  registerMethod<T>(name: string, schema: z.ZodSchema<T>, handler: (params: T) => Promise<unknown>): void {
    if (!/^[a-zA-Z][a-zA-Z0-9_.]*$/.test(name)) throw new Error("Invalid method name");
    this.methods.set(name, { schema, handler });
  }

  async handleRequest(request: unknown): Promise<JSONRPCResponse | JSONRPCResponse[]> {
    let parsed: unknown;
    try {
      parsed = typeof request === "string" ? JSON.parse(request) : request;
    } catch { return this.createError(null, -32700, "Parse error"); }

    if (Array.isArray(parsed)) {
      if (parsed.length === 0) return this.createError(null, -32600, "Invalid Request");
      return Promise.all(parsed.map(req => this.handleSingleRequest(req)));
    }
    return this.handleSingleRequest(parsed);
  }

  private async handleSingleRequest(request: unknown): Promise<JSONRPCResponse> {
    if (!this.validateRequest(request)) return this.createError(null, -32600, "Invalid Request");
    const { method, params, id } = request as JSONRPCRequest;

    const handler = this.methods.get(method);
    if (!handler) return this.createError(id, -32601, "Method not found");

    const paramValidation = handler.schema.safeParse(params);
    if (!paramValidation.success) return this.createError(id, -32602, "Invalid params");

    try {
      const result = await handler.handler(paramValidation.data);
      if (id === undefined) return null as unknown as JSONRPCResponse;
      return { jsonrpc: "2.0", result, id };
    } catch (error) {
      console.error("Method execution error:", error);
      return this.createError(id, -32603, "Internal error");
    }
  }

  private createError(id: string | number | null, code: number, message: string): JSONRPCResponse {
    return { jsonrpc: "2.0", error: { code, message }, id };
  }

  private validateRequest(request: unknown): boolean {
    if (typeof request !== "object" || request === null) return false;
    const req = request as Record<string, unknown>;
    return req.jsonrpc === "2.0" && typeof req.method === "string";
  }
}
```

### 6.2 Method Registration with Authorization

```typescript
const server = new JSONRPCServer();

// Public method
server.registerMethod("getStatus", z.object({}), async () => ({ status: "healthy" }));

// Authenticated method
server.registerMethod("getUserData", z.object({
  userId: z.string().uuid(),
  authToken: z.string().min(1)
}), async (params) => {
  const user = await verifyAuthToken(params.authToken);
  if (!user) throw new Error("Unauthorized");
  if (user.id !== params.userId && !user.isAdmin) throw new Error("Forbidden");
  return await getUserData(params.userId);
});

// Admin-only method
server.registerMethod("admin.deleteUser", z.object({
  userId: z.string().uuid(),
  authToken: z.string().min(1)
}), async (params) => {
  const user = await verifyAuthToken(params.authToken);
  if (!user?.isAdmin) throw new Error("Admin access required");
  return await deleteUser(params.userId);
});
```

### 6.3 Batch Processing with Limits

```typescript
// Secure batch handling
async handleBatchRequest(requests: JSONRPCRequest[]): Promise<JSONRPCResponse[]> {
  // Limit batch size
  const MAX_BATCH_SIZE = 100;
  if (requests.length > MAX_BATCH_SIZE) {
    return [this.createError(null, -32600, `Batch size exceeds limit of ${MAX_BATCH_SIZE}`)];
  }

  // Process with concurrency limit
  const CONCURRENCY_LIMIT = 10;
  const results: JSONRPCResponse[] = [];

  for (let i = 0; i < requests.length; i += CONCURRENCY_LIMIT) {
    const batch = requests.slice(i, i + CONCURRENCY_LIMIT);
    const batchResults = await Promise.all(
      batch.map(req => this.handleSingleRequest(req))
    );
    results.push(...batchResults.filter(r => r !== null));
  }

  return results;
}
```

### 6.4 HTTP Transport Integration

```typescript
import express from "express";
import helmet from "helmet";
import rateLimit from "express-rate-limit";

const app = express();
app.use(helmet());
app.use(express.json({ limit: "1mb" }));
app.use("/rpc", rateLimit({
  windowMs: 60000, max: 100,
  message: { jsonrpc: "2.0", error: { code: -32000, message: "Rate limit exceeded" }, id: null }
}));

app.post("/rpc", async (req, res) => {
  if (req.headers["content-type"] !== "application/json") {
    return res.status(415).json({ jsonrpc: "2.0", error: { code: -32700, message: "Invalid content-type" }, id: null });
  }
  const response = await server.handleRequest(req.body);
  if (!response || (Array.isArray(response) && !response.length)) return res.status(204).end();
  res.json(response);
});
```

---

## 7. Performance Patterns

### 7.1 Batch Requests

```typescript
// Bad: Multiple individual requests
for (const item of items) { await client.call("process", { item }); }

// Good: Single batch request
const batch = items.map((item, i) => ({ jsonrpc: "2.0", method: "process", params: { item }, id: i }));
const results = await client.batch(batch);
```

### 7.2 Connection Pooling

```typescript
// Bad: New connection per request
const client = new RPCClient(url); // Creates new connection each call

// Good: Reuse connections from pool
const pool = new RPCClientPool(url, { maxConnections: 10 });
const client = await pool.acquire();
try { return await client.call(method, params); } finally { pool.release(client); }
```

### 7.3 Response Caching

```typescript
// Bad: DB hit every time
server.registerMethod("getConfig", schema, async () => await db.query("SELECT * FROM config"));

// Good: LRU cache with TTL
const cache = new LRUCache({ max: 1000, ttl: 60000 });
server.registerMethod("getConfig", schema, async (params) => {
  const key = `config:${params.section}`;
  return cache.get(key) || cache.set(key, await db.query("SELECT * FROM config WHERE section = ?", [params.section]));
});
```

### 7.4 Streaming Large Results

```typescript
// Bad: Load entire dataset (OOM risk)
server.registerMethod("exportData", schema, async () => await db.query("SELECT * FROM huge_table"));

// Good: Paginated results
server.registerMethod("exportData", schema, async ({ cursor = 0, limit = 100 }) => {
  const data = await db.query("SELECT * FROM huge_table WHERE id > ? LIMIT ?", [cursor, limit]);
  return { data, nextCursor: data.length === limit ? data[data.length - 1].id : null };
});
```

### 7.5 Payload Optimization

```typescript
// Bad: Return all fields (50KB)
server.registerMethod("getUser", schema, async ({ id }) => await getUser(id));

// Good: Return only requested fields (500B)
server.registerMethod("getUser", schema, async ({ id, fields }) => {
  const user = await getUser(id);
  return fields ? Object.fromEntries(fields.map(f => [f, user[f]])) : user;
});
```

---

## 8. Security Standards

### 8.1 Domain Vulnerability Landscape

> **See `references/security-examples.md` for complete CVE details.**

**Top Vulnerabilities**:
- **Method Injection**: Accessing unregistered/internal methods
- **Parameter Injection**: Malicious params causing code execution
- **Batch DoS**: Large batches consuming resources
- **Error Information Disclosure**: Stack traces in errors

### 8.2 Input Validation

```typescript
// Complete parameter validation with Zod
const TransferSchema = z.object({
  from: z.string().uuid(),
  to: z.string().uuid(),
  amount: z.number().positive().max(1000000),
  currency: z.enum(["USD", "EUR", "GBP"]),
  memo: z.string().max(200).optional()
}).refine(data => data.from !== data.to, "Cannot transfer to same account");

server.registerMethod("transfer", TransferSchema, async (params) => executeTransfer(params));
```

### 8.3 Error Handling

```typescript
// Safe error responses - log details internally, return generic message
class SafeJSONRPCError extends Error {
  constructor(public code: number, message: string, private internal?: string) { super(message); }

  toResponse(id: string | number | null): JSONRPCResponse {
    if (this.internal) console.error(`RPC Error [${this.code}]: ${this.internal}`);
    return { jsonrpc: "2.0", error: { code: this.code, message: this.message }, id };
  }
}

// Usage: internal details logged but not returned to client
throw new SafeJSONRPCError(-32603, "Internal error", `DB failed: ${dbError.message}`);
```

---

## 9. Common Mistakes

### NEVER: Execute Dynamic Methods

```typescript
// Bad: Arbitrary method access from user input
const fn = this[request.method]; return fn(request.params);

// Good: Whitelist registered methods only
const handler = this.registeredMethods.get(request.method);
if (!handler) throw new Error("Method not found");
return handler(request.params);
```

### NEVER: Return Internal Errors

```typescript
// Bad: Exposes stack traces
catch (error) { return { error: { code: -32603, message: error.stack } }; }

// Good: Log internally, return generic message
catch (error) { console.error(error); return { error: { code: -32603, message: "Internal error" } }; }
```

---

## 10. Pre-Implementation Checklist

### Phase 1: Before Writing Code
- [ ] Write failing tests for RPC methods and error handling
- [ ] Define parameter schemas for all methods
- [ ] Document method whitelist
- [ ] Plan authentication strategy for protected methods

### Phase 2: During Implementation
- [ ] All methods registered with explicit whitelist
- [ ] Parameter validation using schemas (Zod/Pydantic)
- [ ] Batch size limits enforced (max 100)
- [ ] Rate limiting configured per endpoint
- [ ] Error messages sanitized (no stack traces)
- [ ] Request size limits set (max 1MB)
- [ ] Timeout on method execution

### Phase 3: Before Committing
- [ ] All tests pass: `pytest tests/test_rpc_*.py -v`
- [ ] Security tests pass: `pytest tests/test_rpc_security.py -v`
- [ ] Performance benchmarks acceptable
- [ ] Audit logging enabled for all method calls
- [ ] Documentation updated for new methods

---

## 11. Summary

Your goal is to implement JSON-RPC services that are:
- **Compliant**: Follow JSON-RPC 2.0 specification exactly
- **Secure**: Validate all inputs, whitelist methods, sanitize errors
- **Robust**: Handle batches safely, enforce limits, timeout operations

Remember: Every RPC method is a potential attack vector. Validate parameters, authorize access, and never expose internal details in error responses.
