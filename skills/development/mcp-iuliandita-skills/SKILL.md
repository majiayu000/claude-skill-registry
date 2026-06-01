---
name: mcp
description: >
  · Build/review MCP servers, tools, resources, prompts, transports, OAuth, elicitation. Triggers: 'mcp', 'model context protocol', 'mcp server', 'tool handler', 'fastmcp', '@modelcontextprotocol/sdk'. Not for HTTP APIs (use backend-api).
license: MIT
compatibility: Requires Node.js or Python runtime
metadata:
  source: iuliandita/skills
  date_added: "2026-03-30"
  effort: high
  argument_hint: "<server-or-task>"
---

# MCP: Model Context Protocol Server Development

Build, review, and debug MCP servers that expose tools, resources, and prompts to AI coding
assistants. The goal is secure, well-structured servers that follow the protocol spec and don't
become yet another server with preventable injection vulnerabilities.

**Target versions** (May 2026):
- MCP specification: 2025-11-25 (current stable; 2026-03-15 in draft)
- TypeScript SDK: @modelcontextprotocol/sdk 1.29.0 (1.x stable; 2.0.0-alpha in dev)
- Python SDK: mcp 1.27.0 (v1.26.0+)
- Protocol transports: stdio, Streamable HTTP (the standalone HTTP+SSE transport was deprecated in spec 2025-03-26; SSE still streams inside Streamable HTTP)

## When to use

- Building a new MCP server (tools, resources, prompts)
- Adding tool handlers to an existing MCP server
- Configuring MCP transport (stdio for local, streamable HTTP for remote)
- Implementing MCP authentication (OAuth 2.1)
- Implementing MCP elicitation (interactive dialogs)
- Reviewing MCP server code for injection or tool poisoning vulnerabilities
- Debugging MCP connection issues between client and server
- Migrating from a custom tool integration to MCP

## When NOT to use

- General REST API development that doesn't use MCP - just write the API
- Claude API / Anthropic SDK usage in an application - use **ai-ml**
- Security auditing existing servers across a codebase - use **security-audit** (it has an MCP section)
- Using MCP browsing tools to browse or scrape web pages - use **browse**
- Writing prompts for LLMs (not MCP prompt resources) - use **prompt-generator**

---

## AI Self-Check

When generating or reviewing MCP server code, verify each item before presenting the result:

- [ ] All tool handler inputs validated server-side (no raw string interpolation into
  shell commands, SQL, file paths, or URLs)
- [ ] Tool descriptions accurate and concise (some clients truncate long descriptions)
- [ ] Resource URIs use a defined scheme and are validated before use
- [ ] Error responses use proper MCP error codes, not raw stack traces
- [ ] Authentication implemented for remote transports that handle user data (OAuth 2.1 with PKCE)
- [ ] No secrets hardcoded in tool handlers or server configuration
- [ ] `inputSchema` uses specific JSON Schema types with `required`, `maxLength`, constraints
- [ ] Server handles graceful shutdown (cleanup on SIGINT/SIGTERM)
- [ ] Streamable HTTP: binds to `127.0.0.1` (not `0.0.0.0`) when local
- [ ] Streamable HTTP: validates `Origin` header (DNS rebinding prevention)
- [ ] Rate limiting on tool invocations
- [ ] Tool annotations treated as untrusted by client-side code
- [ ] Elicitation does not request passwords, tokens, or secrets
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Spec version checked**: transports, auth, resources, tools, and prompts match current MCP docs and SDK behavior
- [ ] **Tool poisoning considered**: tool descriptions, dynamic metadata, and server updates cannot silently expand authority
- [ ] **SDK methods verified**: see Common Mistakes #8 - verify every API call against actual SDK docs rather than inventing method names

---

## Performance

- Keep tool schemas tight and responses small; large unstructured tool outputs waste model context.
- Use resources for reusable context instead of returning the same large payload from every tool call.
- Batch read-only lookups where latency matters, but keep side-effecting tools separate and auditable.


---

## Best Practices

- Treat MCP servers as security boundaries: authenticate, authorize, and log side effects explicitly.
- Make tool names and schemas stable; version breaking changes instead of changing semantics in place.
- Require user confirmation for tools that spend money, mutate infrastructure, delete data, or expose secrets.


## Workflow

**Build vs. Review:** Steps 1-6 are for building new servers. When reviewing existing MCP server code: (1) scope using Step 1 questions - what tools, transport, and auth does the server use; (2) audit each tool handler against Step 3 injection vectors and the AI Self-Check; (3) cross-reference the Common Mistakes section for patterns AI models frequently introduce.

### Step 1: Determine the server's purpose

Before writing code, clarify:
- **What tools will it expose?** Each tool = one operation the AI can invoke.
- **What resources will it serve?** Resources = read-only data the AI can access.
- **What transport?** stdio for local CLI integration, streamable HTTP for remote/production.
- **What authentication?** None for stdio. OAuth 2.1 recommended for remote servers handling user data.
- **What language?** TypeScript (most mature SDK) or Python (simpler, FastMCP).

### Step 2: Scaffold the server

**TypeScript** (recommended for production):

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "my-server", version: "1.0.0" });

// Current SDK API: `server.registerTool(name, { title, description, inputSchema }, handler)`.
// The older `server.tool(name, desc, schema, handler)` shorthand still works in v1.x.
server.registerTool(
  "search_docs",
  {
    title: "Search docs",
    description: "Search documentation by keyword",
    inputSchema: { query: z.string().max(200).describe("Search query"), limit: z.number().int().min(1).max(100).default(10) },
  },
  async ({ query, limit }) => {
    // If this tool reads files, apply path validation from Step 3 before any fs access.
    const sanitized = query.replace(/[^\w\s-]/g, "");
    const results = await searchIndex(sanitized, limit);
    return { content: [{ type: "text", text: JSON.stringify(results) }] };
  }
);

server.resource("config", "config://app/settings", async (uri) => ({
  contents: [{ uri: uri.href, mimeType: "application/json", text: JSON.stringify(config) }],
}));

const transport = new StdioServerTransport();
await server.connect(transport);
```

**Python** (FastMCP for quick prototyping):

```python
import json, re
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def search_docs(query: str, limit: int = 10) -> str:
    """Search documentation by keyword."""
    sanitized = re.sub(r"[^\w\s-]", "", query[:200])
    return str(search_index(sanitized, min(limit, 100)))

@mcp.resource("config://app/settings")
def get_config() -> str:
    """Application configuration."""
    return json.dumps(config)

if __name__ == "__main__":
    mcp.run()
```

### Step 3: Implement tools securely

Injection is the top MCP vulnerability class. Every tool handler is an attack surface.

**The #1 rule: never interpolate user input into commands, queries, or paths.**

**Common injection vectors in MCP tools:**

| Vector | Bad pattern | Safe pattern |
|--------|-----------|--------------|
| Shell | Interpolated command strings | `execFile` with argument arrays + path validation |
| SQL | String concatenation in queries | Parameterized queries with `$1` placeholders |
| File paths | Direct `readFile(userPath)` | Resolve path, validate prefix against allowlist |
| URLs | Direct `fetch(userUrl)` | Parse URL, validate scheme + host against allowlist |
| Templates | Dynamic code evaluation | Sandboxed template engine with no code execution |

**Path traversal prevention:**

```typescript
import path from "node:path";

function safePath(base: string, userInput: string): string {
  const resolved = path.resolve(base, userInput);
  if (!resolved.startsWith(path.resolve(base) + path.sep)) {
    throw new Error("Path traversal detected");
  }
  return resolved;
}
```

**Before/after - applying safePath() to a vulnerable tool handler:**

```typescript
// BEFORE (vulnerable - user controls path directly)
server.tool("read_file", "Read a project file",
  { path: z.string() },
  async ({ path: filePath }) => {
    const data = await readFile(filePath, "utf-8"); // path traversal
    return { content: [{ type: "text", text: data }] };
  }
);

// AFTER (safe - resolved path validated against allowed base)
server.tool("read_file", "Read a project file",
  { path: z.string().max(500) },
  async ({ path: filePath }) => {
    const safe = safePath("/srv/project", filePath);
    const data = await readFile(safe, "utf-8");
    return { content: [{ type: "text", text: data }] };
  }
);
```

**SSRF prevention** (when tools fetch URLs from user input):
- Block private IP ranges: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`
- Block link-local: `169.254.0.0/16` (includes cloud metadata at `169.254.169.254`)
- Block loopback: `127.0.0.0/8`
- Require HTTPS in production
- Pin DNS resolution between check and use (TOCTOU defense)

### Step 4: Configure transport

| Transport | Use case | Auth needed | Notes |
|-----------|----------|-------------|-------|
| **stdio** | Local tools, CLI integration | No | Runs as user's process. Most secure. |
| **Streamable HTTP** | Remote/multi-client servers | Recommended | Single endpoint, POST for messages, optional SSE streaming. |

The standalone HTTP+SSE transport (spec 2024-11-05) was deprecated in spec 2025-03-26; use Streamable HTTP for all remote servers (it still uses SSE internally for optional response streaming).
Auth is optional per spec but strongly recommended for servers handling user data. When
implementing auth, use OAuth 2.1 with PKCE. Prefer Client ID Metadata Documents over Dynamic
Client Registration (DCR is a fallback, not a requirement).

**Streamable HTTP security:**
- Bind to `127.0.0.1` for local servers (never `0.0.0.0`)
- Validate `Origin` header on all requests (DNS rebinding prevention)
- If using stateful sessions: `MCP-Session-Id` must be cryptographically random (UUID v4+)
- Client sends `MCP-Protocol-Version` header (e.g., `2025-11-25`)
- Consider using `createMcpExpressApp()` / `createMcpHonoApp()` for built-in DNS rebinding
  protection - these ship from the separate `@modelcontextprotocol/express` and
  `@modelcontextprotocol/hono` packages, not the core `@modelcontextprotocol/sdk`

### Step 5: Handle elicitation safely

MCP elicitation lets servers request structured input from users mid-task.

**Schema restrictions** - elicitation schemas are limited to flat objects with primitive fields:
- `string` (with optional `format`: email, uri, date, date-time)
- `number` / `integer` (with `minimum`, `maximum`)
- `boolean`
- `enum` (string with `enum`; use `anyOf` with `title` for labeled choices)
- `array` of enum strings (for multi-select)

No nested objects. Keep schemas simple for broad client support.

**Security**: never request credentials via elicitation. Clients should show which server is
requesting input and allow decline/cancel at any time. Handle all three responses: `accept`
(with data), `decline`, and `cancel`.

### Step 6: Test the server

```bash
# Test with MCP Inspector (official debugging tool)
npx @modelcontextprotocol/inspector your-server-command

# Python alternative
uv run mcp dev server.py
```

Test each tool handler with: valid inputs (happy path), missing required fields,
malicious inputs (injection, path traversal, oversized payloads), concurrent requests.

Read `references/security.md` for specific injection test payloads.

---

## Tool Poisoning and Rug Pull Defense

These attacks target tool metadata, not tool execution.

**Tool poisoning**: malicious instructions hidden in tool `description` fields manipulate the
AI model into exfiltrating data or calling unintended tools. Descriptions are visible to the
model but often hidden from users in the UI.

**Rug pull attacks**: server changes tool definitions after initial approval - clean version
during onboarding, malicious version later.

**Server-side defenses:**
- Write clear, honest tool descriptions - no hidden instructions
- Do not include executable logic or injection payloads in descriptions
- Keep descriptions minimal and factual
- Treat `annotations` as advisory (untrusted on the client side)

**Client-side defenses** (document for consumers of your server):
- Display tool descriptions to users before granting access
- Hash tool schemas at approval time; alert on changes between sessions
- Limit cross-server tool access

---

## Common Mistakes

AI models consistently make these errors when generating MCP server code:

1. **Shell commands via string interpolation** - the #1 vulnerability. Always use
   argument arrays for system commands.
2. **Missing server-side validation** - generating `inputSchema` but never validating
   against it in the handler. The client may skip validation.
3. **Bare `"type": "string"` in schemas** - no `maxLength`, no `pattern`, no constraints.
   Accepts any string of any length.
4. **Binding HTTP to `0.0.0.0`** - exposes local servers to the network. Use `127.0.0.1`.
5. **No `Origin` header validation** - enables DNS rebinding against local servers.
6. **Leaking error details** - stack traces, file paths, or DB errors in tool responses.
7. **Token passthrough** - accepting OAuth tokens meant for other services without
   audience validation.
8. **Hallucinating SDK methods** - inventing API calls that don't exist. See AI Self-Check for the verification checklist item.
9. **Ignoring elicitation actions** - handling `accept` but crashing on `decline`/`cancel`.
10. **No graceful shutdown** - missing SIGINT/SIGTERM handlers on stdio servers.

---

## Reference Files

- `references/security.md` - OAuth 2.1 details, known CVEs, injection test payloads,
  SSRF prevention, session management, and tool poisoning defense

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** MCP
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/mcp/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **security-audit** - for auditing MCP servers as part of a broader security review. The
  security-audit skill's ASI and MCP sections cover vulnerability patterns; this skill covers
  building servers correctly from the start.
- **code-review** - for reviewing MCP server code for correctness beyond security.
- **docker** - for containerizing MCP servers with minimal capabilities.
- **ai-ml** - for Claude API / Anthropic SDK usage in the application that calls MCP tools. Use ai-ml, not this skill, for Anthropic SDK integration code.
- **backend-api** - for general REST/GraphQL API development that does not use the MCP protocol.
- **browse** - for using MCP browsing tools to scrape or interact with web pages; this skill builds the server, browse operates it.
- **prompt-generator** - for writing LLM prompts (not MCP prompt resources); route there when the request is about prompt engineering rather than MCP server construction.

---

## Rules

1. **Validate all tool inputs server-side.** Never trust the client or model. Use schema
   validation (Zod, Pydantic) with explicit types, ranges, and constraints.
2. **No shell execution with string interpolation.** Use argument arrays for system commands.
3. **Keep descriptions concise.** Some clients truncate long descriptions. A few sentences
   covering what the tool does and its parameters - not implementation details.
4. **Authenticate when handling user data.** Use OAuth 2.1 with PKCE for remote servers that
   access user data. Auth is optional per spec but strongly recommended.
5. **Return structured errors.** MCP error codes + human-readable messages. No stack traces.
6. **Test with malicious inputs.** Injection payloads, path traversal, oversized inputs.
7. **Bind local servers to 127.0.0.1.** Never `0.0.0.0` for local-only servers.
8. **Validate Origin headers** on all streamable HTTP requests.
9. **Handle shutdown gracefully.** Register signal handlers. Clean up resources.
10. **Run the AI Self-Check.** Every generated MCP server gets verified against the checklist.
