---
name: optimizing-smithery-score
description: Use when publishing an MCP server to Smithery and need to maximize the quality score - covers scoring categories, tool metadata requirements, deploy reliability, and known external deployment limitations
---

# Optimizing Smithery MCP Quality Score

## Overview

Smithery scores MCP servers on a 100-point scale across 4 categories. External deployments (non-hosted) have specific limitations. This skill covers proven techniques for maximizing score and avoiding common pitfalls.

## When to Use

- Publishing an MCP server to Smithery registry
- Score dropped unexpectedly after deploy
- Tools/prompts/resources not detected by scanner
- Investigating why specific scoring categories show partial credit

## Scoring Categories

| Category | Max Points | Components |
|----------|-----------|------------|
| Tool Quality | 55 | Descriptions (14pt), Parameter descriptions (12pt), Annotations (9pt), outputSchema (~10pt), unknown (~10pt) |
| Server Capabilities | 10 | Prompts (5pt), Resources (5pt) |
| Server Metadata | 50 | Description (10pt), Homepage (10pt), Icon (7pt), Display name (3pt), unknown (~20pt) |
| Configuration UX | 25 | Optional config (15pt), Config schema (10pt) |

## Quick Reference

### Must-Have for Each Tool

```typescript
server.registerTool('tool_name', {
  title: 'Human Title',           // Required
  description: '2-4 sentences.', // Descriptions score: all tools need descriptions
  inputSchema: {
    param: z.string().describe('Description here'), // ALL params need .describe()
  },
  outputSchema: jsonResult,       // Unlocks outputSchema points
  annotations: {                  // Annotations score: all tools need these
    readOnlyHint: true,
    destructiveHint: false,
    openWorldHint: true,
  },
}, async (args) => {
  const result = await doWork(args);
  return {
    content: [{ type: 'text' as const, text: JSON.stringify(result, null, 2) }],
    structuredContent: result as unknown as Record<string, unknown>, // Required when outputSchema is set
  };
});
```

### outputSchema Patterns

```typescript
// Dynamic API responses (unknown shape)
const jsonResult = z.object({}).passthrough();

// Text confirmation responses
outputSchema: { message: z.string().describe('Confirmation message') }
// Return: structuredContent: { message }

// Array responses
outputSchema: { items: z.array(z.object({}).passthrough()).describe('Array of items') }
// Return: structuredContent: { items: data as unknown as Record<string, unknown>[] }
```

**Critical**: MCP SDK enforces `structuredContent` when `outputSchema` is defined. Omitting it throws `McpError` at runtime.

### TypeScript Cast Pattern

TypeScript interfaces lack index signatures. Cast through `unknown`:

```typescript
// BAD - TS2352 error
structuredContent: result as Record<string, unknown>

// GOOD
structuredContent: result as unknown as Record<string, unknown>
```

## Parameterless Tools

Smithery scores parameter descriptions as a ratio (e.g., 32/37). Tools with no parameters count against you. Fix by adding meaningful optional parameters:

```typescript
// BAD - no inputSchema or empty inputSchema hurts param description ratio
server.registerTool('list_items', { inputSchema: {} }, ...)

// GOOD - add a real optional parameter
server.registerTool('list_items', {
  inputSchema: {
    limit: z.number().optional().describe('Maximum number of items to return'),
  },
}, ...)
```

## Deploy Reliability (GitHub Actions)

Smithery's scanner runs server-side from Smithery infrastructure, not from your CI runner. After deploying to Fly.io (or similar), instances need time to warm up.

### Proven GitHub Action Pattern

```yaml
deploy-smithery:
  needs: deploy  # Run AFTER server deploy, not just CI
  steps:
    - name: Wait for instances to warm up
      run: sleep 30

    - name: Verify MCP endpoint is ready
      run: |
        for i in $(seq 1 10); do
          STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
            https://your-api.example.com/mcp \
            -H "Content-Type: application/json" \
            -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"health-check","version":"1.0.0"}},"id":1}')
          if [ "$STATUS" = "200" ]; then break; fi
          sleep 5
        done

    - name: Publish with retry
      run: |
        for attempt in 1 2 3; do
          OUTPUT=$(npx @smithery/cli@latest publish \
            -u https://your-api.example.com/mcp \
            -n "org/server" \
            -k "$SMITHERY_API_KEY" \
            --config-schema path/to/config-schema.json 2>&1)
          echo "$OUTPUT"
          if echo "$OUTPUT" | grep -q "expected_capability"; then
            break
          fi
          sleep 15
        done
```

**Why retries matter**: Scanner queries `tools/list`, `prompts/list`, `resources/list` concurrently with timeouts. If any times out, those capabilities show 0 points. Score can fluctuate 48-83 between identical publishes.

## Known External Deployment Limitations

| Feature | Hosted | External | Notes |
|---------|--------|----------|-------|
| Config schema (10pt) | Works | Likely broken | `--config-schema` flag accepted but scoring may not credit it |
| Icon (7pt) | Upload via dashboard | Upload via dashboard | Same for both |
| Tool/param descriptions | Works | Works but flaky | Scanner timeout causes 0/0 detection |
| Prompts/Resources | Works | Flaky | Most common scan failure |

## Response Size Limits

Smithery's scanner has an effective tools/list response size limit of ~30KB. Beyond this, tools are not detected (shows 0/0 tools) while smaller responses like prompts/list and resources/list succeed.

**Root cause**: MCP SDK v1.26+ adds `execution: { taskSupport: 'forbidden' }` to every tool, and `outputSchema` adds ~8KB for 37 tools. Combined with `_meta`, these fields push the response past the scanner's limit.

**Fix**: Strip `execution`, `outputSchema`, and `_meta` from the tools/list response only (keep them for tool call validation):

```typescript
import { ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';

// After registering all tools:
const handlers = (mcpServer.server as any)._requestHandlers;
const origHandler = handlers.get('tools/list');
mcpServer.server.setRequestHandler(ListToolsRequestSchema, async (req, extra) => {
  const result = await origHandler(req, extra);
  if (result?.tools) {
    result.tools = result.tools.map(t => {
      const { execution, outputSchema, _meta, ...clean } = t;
      return clean;
    });
  }
  return result;
});
```

This reduces the response from ~39KB to ~29KB without losing tool call functionality.

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Missing `.describe()` on params | Partial param score | Add `.describe()` to every parameter |
| No `annotations` on tools | 0/9 annotation points | Add all 4 annotation hints |
| No `outputSchema` | Missing ~10pt | Add outputSchema + structuredContent |
| `as Record<string, unknown>` | TS build failure | Cast through `unknown` first |
| Deploy Smithery before server is ready | Random low scores | Add warmup delay + health check + retry |
| `needs: ci` instead of `needs: deploy` | Publishes before deploy finishes | Chain deploy-smithery after deploy job |
| Empty `inputSchema: {}` | Doesn't fix param ratio | Add real optional parameters instead |
| Expanding descriptions for quality | No effect | 14pt is fixed max for presence, not quality |
| tools/list response > ~30KB | Scanner shows 0/0 tools | Strip execution, outputSchema, _meta from list response |
| MCP SDK v1.26+ execution field | Scanner rejects unknown fields | Delete from registered tools or override handler |
| CF DO `idFromName(sessionId)` | Session routes to wrong DO, 0 tools | Use `idFromString(sessionId)` for hex DO IDs |

## Cloudflare Durable Object Session Routing

When hosting MCP on Cloudflare Workers with Durable Objects for stateful sessions, the session routing MUST use `idFromString()` — not `idFromName()`.

**The bug**: The MCP transport returns `state.id.toString()` (a 64-char hex DO ID) as the `mcp-session-id` header. If the worker routes subsequent requests with `idFromName(sessionId)`, it hashes the hex string into a DIFFERENT DO ID, sending the request to an uninitialized DO. Result: `"Bad Request: Server not initialized"` (100 bytes), and Smithery sees 0 tools.

**Symptoms**:
- `tools/list warm-up returned 0 name fields (100 bytes)`
- `[scan] No capabilities found` in Smithery publish output
- Score drops to 55-60 (metadata + config UX still work since those don't need MCP protocol)
- `initialize` succeeds but ALL follow-up requests fail

**Fix**:
```typescript
// worker.ts — MCP session routing
app.all('/mcp', async (c) => {
  const sessionId = c.req.header('mcp-session-id');

  if (sessionId) {
    // CORRECT: idFromString() reverses state.id.toString()
    try {
      const doId = c.env.MCP_SESSION_DO.idFromString(sessionId);
      const stub = c.env.MCP_SESSION_DO.get(doId);
      return stub.fetch(c.req.raw);
    } catch {
      return c.json(
        { jsonrpc: '2.0', error: { code: -32000, message: 'Invalid or expired session' }, id: null },
        { status: 404 },
      );
    }
  }

  // New session
  const newSessionId = crypto.randomUUID();
  const doId = c.env.MCP_SESSION_DO.idFromName(newSessionId);
  const stub = c.env.MCP_SESSION_DO.get(doId);
  return stub.fetch(c.req.raw);
});
```

**Key distinction**:
- `idFromName(string)` — one-way hash, creates a NEW deterministic ID from any string
- `idFromString(hex)` — reverses `id.toString()`, returns the SAME DO ID

**Verification**: After fixing, test the full MCP handshake:
```bash
# 1. Initialize (creates session)
RESP=$(curl -s -D /tmp/h -X POST https://api.example.com/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}},"id":1}')

# 2. Get session ID
SID=$(grep -i 'mcp-session-id' /tmp/h | tr -d '\r' | awk '{print $2}')

# 3. Send initialized notification
curl -s -X POST https://api.example.com/mcp \
  -H "Mcp-Session-Id: $SID" -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'

# 4. Verify tools/list returns tools (NOT "Server not initialized")
curl -s -X POST https://api.example.com/mcp \
  -H "Mcp-Session-Id: $SID" -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":2}' | head -c 500
```

## Score Debugging

If score drops unexpectedly:
1. **Test the full MCP handshake** — initialize → tools/list with same session. If tools/list returns "Server not initialized", session routing is broken.
2. Re-publish manually — scanner is flaky, especially for external deployments
3. Check if Tool Quality shows 0/0 tools — means scanner timeout OR session routing broken
4. Check Server Capabilities — Prompts most likely to be missed
5. Verify the MCP endpoint responds to `initialize` + `tools/list` quickly (< 5s)
6. Check CI logs for `tools/list warm-up returned 0 name fields` — this is the session routing bug
