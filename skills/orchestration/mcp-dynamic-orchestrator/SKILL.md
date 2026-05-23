---
name: mcp-dynamic-orchestrator
description: Dynamic MCP server discovery and code-mode execution via central registry. Use for multiple MCP integrations, tool discovery, progressive disclosure, or encountering MCP context bloat, changing server sets, large tool sets.

  Keywords: MCP, code-mode, registry, dynamic tools, tool discovery, progressive disclosure
license: MIT
allowed-tools:
  - list_mcp_capabilities
  - describe_mcp
  - execute_mcp_code
---

## Overview

Use this skill to:
- Discover which MCP servers are available and what they are for.
- Inspect a specific MCP's capabilities without loading all tool schemas.
- Execute TypeScript/JavaScript that calls MCP tools via generated `mcp-clients/*` modules.

If no MCP servers are configured, `list_mcp_capabilities` will respond with an empty list
and a message pointing to `skills/mcp-dynamic-orchestrator/mcp.registry.json` so the user
can add MCP entries.

This skill reads from `mcp.registry.json`, so adding an MCP entry there (for example the
Cloudflare MCP) automatically makes it discoverable without changing tool wiring.

## Cloudflare MCP example

The Cloudflare MCP server can be configured in `mcp.registry.json` like this:

```json
{
  "id": "cloudflare",
  "title": "Cloudflare platform MCP",
  "summary": "Interact with Cloudflare's MCP endpoint for documentation, examples, and platform operations exposed via the official Cloudflare MCP server.",
  "mcp": {
    "transport": "stdio",
    "command": "npx",
    "args": [
      "mcp-remote",
      "https://docs.mcp.cloudflare.com/sse"
    ]
  },
  "domains": ["cloudflare", "workers", "kv", "r2", "queues", "zero_trust", "networking", "security", "observability"],
  "tags": ["cloudflare", "platform", "infra", "docs", "workers", "mcp"],
  "examples": [
    "Fetch Cloudflare Workers documentation for a specific API.",
    "Search Cloudflare platform docs for queues or KV usage patterns.",
    "Look up configuration guidance for Zero Trust or networking features."
  ],
  "sensitivity": "low",
  "visibility": "default",
  "priority": 10,
  "autoDiscoverTools": true
}
```

With this entry present:
- `list_mcp_capabilities` will return `cloudflare` when queries mention Cloudflare, Workers, KV, R2, Queues, etc.
- `describe_mcp` with `id: "cloudflare"` will surface concise tool summaries from the Cloudflare MCP server.
- `execute_mcp_code` lets the agent write TypeScript such as:

```ts
import * as cloudflare from "mcp-clients/cloudflare";

async function main() {
  const docs = await cloudflare.search_docs({ query: "Workers KV" });
  console.log(docs.summary);
}
```

The actual available functions under `mcp-clients/cloudflare` are generated dynamically
from the MCP tool definitions; the agent should always:
1. Discover via `list_mcp_capabilities`.
2. Inspect via `describe_mcp` to see available operations.
3. Use those operations via `execute_mcp_code`.

## How to use

1. Call `list_mcp_capabilities` with a natural language query or filters to see which MCPs exist.
2. For a chosen MCP (e.g. `cloudflare`), call `describe_mcp` to understand its operations.
3. Write TypeScript/JavaScript that imports from `mcp-clients/<id>` and calls the exported functions.
4. Run your code with `execute_mcp_code`, optionally restricting `allowedMcpIds` for safety.

## Rules

- Do not assume individual MCP tools are top-level tools.
- Always: discover → describe → generate code → `execute_mcp_code`.
- Request `detail: "schema"` in `describe_mcp` only when exact parameter shapes are required.

## Known Limitations

### Sandbox Security (CRITICAL)

⚠️ **The current sandbox implementation is NOT secure for untrusted code.**

- Uses `vm.createContext()` which is NOT a security boundary
- Can be escaped via prototype pollution, require() manipulation, etc.
- **Only enable for Claude-generated code** (trusted source)
- Requires `MCP_ORCH_ENABLE_SANDBOX=1` environment variable
- See `references/security-model.md` for complete security details

### Other Limitations

- **No TypeScript compilation**: User code in `.ts` format will fail
- **No module resolution**: Imports from `mcp-clients/*` don't resolve; use `$call()` API
- **Static registry**: Adding/removing MCPs requires restart
- **Limited error handling**: Generic errors for MCP connection failures

For detailed troubleshooting, see `references/troubleshooting.md`.

## Production Status

**What's Working** ✅:
- Discovery via `list_mcp_capabilities` (fully functional)
- Inspection via `describe_mcp` (fully functional)
- Registry management (16 MCPs configured)
- MCP clients (stdio + HTTP transports)
- Safety controls (visibility, sensitivity, policies)

**What's Limited** 🟡:
- Code execution (requires env flag, sandbox not secure)
- Testing (basic smoke tests only)

**What's Planned** 🔮:
- Secure sandbox with Worker threads (v1.1)
- TypeScript compilation support (v1.1)
- Module resolution (v1.1)
- Dynamic registry updates (v1.2)

For complete roadmap, see `plan.md` in repository root.
