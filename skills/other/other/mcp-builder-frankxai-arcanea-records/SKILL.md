---
name: arcanea-mcp-builder
description: Guide for building MCP (Model Context Protocol) servers for the Arcanea ecosystem. Use when creating new MCP tools, extending packages/arcanea-mcp, adding Arcanea-branded tools, integrating external APIs as MCP endpoints, or building new MCP servers for the Arcanea AI toolkit. Triggers on: MCP server, MCP tool, model context protocol, mcp-builder, create tool, arcanea-mcp, new MCP. Sourced from Anthropic's official mcp-builder skill, adapted for Arcanea's TypeScript + Bun stack.
license: MIT (source: anthropics/skills/mcp-builder)
metadata:
  author: Arcanea (adapted from Anthropic)
  version: "1.0.0"
  stack: TypeScript strict, Bun, MCP TypeScript SDK, Hono
---

# Arcanea MCP Builder

> *"Shinkami guards the Source Gate at 1111 Hz — Meta-consciousness. MCP tools are the hands through which meta-consciousness acts. Build them with clarity and precision."*

Adapted from Anthropic's official MCP builder guide for the Arcanea ecosystem. Arcanea MCP servers live in `packages/arcanea-mcp/`.

## Architecture Overview

```
packages/arcanea-mcp/
├── src/
│   ├── index.ts              # Server entry point
│   ├── tools/                # Tool definitions (one file per domain)
│   │   ├── guardian-tools.ts
│   │   ├── lore-tools.ts
│   │   ├── prompt-tools.ts
│   │   └── academy-tools.ts
│   ├── skills/               # Skill rules engine (existing)
│   │   ├── skill-rules-engine.ts
│   │   └── feedback-bridge.ts
│   └── resources/            # MCP resources (read-only data)
│       └── canon-resource.ts
└── package.json
```

---

## Phase 1: Plan the MCP Server

### Define Tool Scope
Before writing code, answer:
1. **What does this tool enable the AI to do?** (action-oriented, not data-oriented)
2. **What's the minimal set of tools?** (prefer comprehensive coverage over abstractions)
3. **What auth does it need?** (Supabase JWT, API keys, or none)
4. **What should error messages say?** (actionable, guide toward solution)

### Tool Naming Convention (Arcanea)
```
arcanea_{domain}_{verb}_{noun}
arcanea_lore_get_guardian
arcanea_lore_search_texts
arcanea_academy_unlock_gate
arcanea_prompts_create
arcanea_prompts_list
arcanea_canon_validate
```

---

## Phase 2: Implement with TypeScript SDK

### Setup
```bash
cd packages/arcanea-mcp
# Already in monorepo — add SDK if needed
bun add @modelcontextprotocol/sdk zod
```

### Server Entry Point
```typescript
// packages/arcanea-mcp/src/index.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { registerGuardianTools } from './tools/guardian-tools.js'
import { registerLoreTools } from './tools/lore-tools.js'
import { registerAcademyTools } from './tools/academy-tools.js'

const server = new Server(
  {
    name: 'arcanea-mcp',
    version: '1.0.0',
  },
  {
    capabilities: { tools: {} },
  }
)

// Register all tool groups
registerGuardianTools(server)
registerLoreTools(server)
registerAcademyTools(server)

// Start with stdio transport (for Claude Code integration)
const transport = new StdioServerTransport()
await server.connect(transport)
```

### Tool Definition Pattern
```typescript
// packages/arcanea-mcp/src/tools/guardian-tools.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js'
import { z } from 'zod'
import { supabaseAdmin } from '../lib/supabase-admin.js'

const GetGuardianSchema = z.object({
  gate: z.enum([
    'foundation', 'flow', 'fire', 'heart', 'voice',
    'sight', 'crown', 'shift', 'unity', 'source'
  ]).describe('The gate name to retrieve guardian info for'),
})

const SearchGuardiansSchema = z.object({
  element: z.enum(['earth', 'water', 'fire', 'wind', 'void', 'spirit']).optional(),
  query: z.string().optional().describe('Free text search across guardian descriptions'),
  limit: z.number().int().min(1).max(10).default(5),
})

const GUARDIAN_TOOLS = [
  {
    name: 'arcanea_lore_get_guardian',
    description: 'Get complete information about a Guardian including their Godbeast, gate frequency, element, and domain. Use when needing canonical guardian data.',
    inputSchema: {
      type: 'object' as const,
      properties: {
        gate: {
          type: 'string',
          enum: ['foundation','flow','fire','heart','voice','sight','crown','shift','unity','source'],
          description: 'The gate this guardian protects',
        },
      },
      required: ['gate'],
    },
  },
  {
    name: 'arcanea_lore_search_guardians',
    description: 'Search guardians by element or free text. Returns matching guardians with their domains and frequencies.',
    inputSchema: {
      type: 'object' as const,
      properties: {
        element: {
          type: 'string',
          enum: ['earth', 'water', 'fire', 'wind', 'void', 'spirit'],
        },
        query: { type: 'string' },
        limit: { type: 'number', minimum: 1, maximum: 10, default: 5 },
      },
    },
  },
]

export function registerGuardianTools(server: Server) {
  // List tools
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: GUARDIAN_TOOLS,
  }))

  // Handle tool calls
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params

    switch (name) {
      case 'arcanea_lore_get_guardian': {
        const { gate } = GetGuardianSchema.parse(args)
        const { data, error } = await supabaseAdmin
          .from('guardians')
          .select('*, godbeast:godbeasts(*)')
          .eq('gate', gate)
          .single()

        if (error || !data) {
          return {
            content: [{
              type: 'text',
              text: `Guardian not found for gate: ${gate}. Valid gates: foundation, flow, fire, heart, voice, sight, crown, shift, unity, source.`,
            }],
            isError: true,
          }
        }

        return {
          content: [{
            type: 'text',
            text: JSON.stringify(data, null, 2),
          }],
        }
      }

      case 'arcanea_lore_search_guardians': {
        const { element, query, limit } = SearchGuardiansSchema.parse(args)
        let dbQuery = supabaseAdmin.from('guardians').select('id, name, gate, element, frequency_hz, domain')

        if (element) dbQuery = dbQuery.eq('element', element)
        if (query) dbQuery = dbQuery.textSearch('description', query)
        dbQuery = dbQuery.limit(limit)

        const { data, error } = await dbQuery
        if (error) {
          return {
            content: [{ type: 'text', text: `Search error: ${error.message}` }],
            isError: true,
          }
        }

        return {
          content: [{
            type: 'text',
            text: JSON.stringify(data, null, 2),
          }],
        }
      }

      default:
        return {
          content: [{ type: 'text', text: `Unknown tool: ${name}` }],
          isError: true,
        }
    }
  })
}
```

---

## Phase 3: Resources (Read-Only Data)

```typescript
// packages/arcanea-mcp/src/resources/canon-resource.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js'
import { readFile } from 'fs/promises'
import { join } from 'path'

const CANON_PATH = join(process.cwd(), '../../.arcanea/lore/CANON_LOCKED.md')

export function registerCanonResource(server: Server) {
  server.setRequestHandler(ListResourcesRequestSchema, async () => ({
    resources: [
      {
        uri: 'arcanea://canon/locked',
        name: 'Arcanea Canon (Locked)',
        description: 'The canonical source of truth for the Arcanea universe — gates, guardians, elements, frequencies.',
        mimeType: 'text/markdown',
      },
    ],
  }))

  server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    if (request.params.uri === 'arcanea://canon/locked') {
      const content = await readFile(CANON_PATH, 'utf-8')
      return {
        contents: [{
          uri: request.params.uri,
          mimeType: 'text/markdown',
          text: content,
        }],
      }
    }
    throw new Error(`Unknown resource: ${request.params.uri}`)
  })
}
```

---

## Phase 4: Claude Code Integration

### Register in `.claude/mcp.json`
```json
{
  "mcpServers": {
    "arcanea-mcp": {
      "command": "bun",
      "args": ["run", "packages/arcanea-mcp/src/index.ts"],
      "env": {
        "SUPABASE_URL": "${NEXT_PUBLIC_SUPABASE_URL}",
        "SUPABASE_SERVICE_ROLE_KEY": "${SUPABASE_SERVICE_ROLE_KEY}"
      }
    }
  }
}
```

---

## Design Principles

### Tool descriptions must be actionable
```typescript
// BAD — vague
description: 'Get guardian data'

// GOOD — tells the AI exactly when and how to use it
description: 'Get complete Guardian profile including Godbeast companion, gate frequency (Hz), element, domain, and lore description. Use when answering questions about a specific gate or guardian. Required param: gate name (foundation|flow|fire|heart|voice|sight|crown|shift|unity|source).'
```

### Error messages guide toward solutions
```typescript
// BAD
throw new Error('Not found')

// GOOD
return {
  content: [{
    type: 'text',
    text: `Guardian not found for gate "${gate}". Valid values: foundation, flow, fire, heart, voice, sight, crown, shift, unity, source. The gate "fire" maps to Guardian Draconia at 396 Hz.`,
  }],
  isError: true,
}
```

### Input validation with Zod
```typescript
// Always validate with Zod — catches bad AI inputs early
const schema = z.object({
  gate: z.enum(['foundation','flow','fire','heart','voice','sight','crown','shift','unity','source']),
  includeGodbeast: z.boolean().default(true),
})

// In handler:
try {
  const params = schema.parse(args)
} catch (e) {
  return { content: [{ type: 'text', text: `Invalid params: ${e.message}` }], isError: true }
}
```

---

## Quick Checklist

Before shipping an Arcanea MCP tool:

- [ ] Tool name follows `arcanea_{domain}_{verb}_{noun}` convention
- [ ] Description tells AI exactly when to use and what params are required
- [ ] Input validated with Zod schemas
- [ ] Error messages include next steps and valid values
- [ ] Supabase uses admin client (service role) for MCP — not anon
- [ ] Registered in both `src/index.ts` and `.claude/mcp.json`
- [ ] TypeScript strict mode — no `any`
- [ ] Tool handles missing/empty results gracefully
