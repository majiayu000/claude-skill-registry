---
name: mcp-generator
description: "Use when setting up project-specific development tools or after analyzing a codebase - generates custom MCP server with semantic search, project-aware tools, and health monitoring capabilities. Works with both basic and enhanced modes. Do NOT use if generic popkit commands are sufficient or for small projects where MCP server overhead isn't justified - stick with built-in tools for simple workflows."
---

# MCP Server Generator

## Overview

Generate a custom MCP (Model Context Protocol) server tailored to the specific project's needs, including semantic search, project-specific tools, and contextual capabilities.

**Core principle:** Every project deserves tools that understand its unique architecture.

**Trigger:** `/popkit:project mcp` command after project analysis

## Operating Modes

| Mode         | Availability        | Capabilities                                            |
| ------------ | ------------------- | ------------------------------------------------------- |
| **Basic**    | Always (no API key) | Project analysis, tech stack detection, recommendations |
| **Enhanced** | With API key        | Custom MCP generation, semantic search, embeddings      |

Get API key: `/popkit:cloud signup` (free)

## Arguments

| Flag              | Description                                    |
| ----------------- | ---------------------------------------------- |
| `--from-analysis` | Use `.claude/analysis.json` for tool selection |
| `--no-embed`      | Skip auto-embedding of tools                   |
| `--no-semantic`   | Don't include semantic search capabilities     |
| `--tools <list>`  | Comma-separated list of tools to generate      |

## Generated Structure

```
.claude/mcp-servers/[project-name]-dev/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts              # MCP server entry point
│   ├── tools/
│   │   ├── project-tools.ts  # Project-specific tools
│   │   ├── health-check.ts   # Service health checks
│   │   └── search.ts         # Semantic search
│   └── resources/
│       └── project-context.ts # Project documentation
└── README.md
```

## Tool Selection Matrix

| Framework        | Generated Tools                                                                                     |
| ---------------- | --------------------------------------------------------------------------------------------------- |
| `nextjs`         | `check_dev_server`, `check_build`, `run_typecheck`                                                  |
| `express`        | `check_api_server`, `health_endpoints`                                                              |
| `prisma`         | `check_database`, `run_migrations`, `prisma_studio`                                                 |
| `supabase`       | `check_supabase`, `supabase_status`                                                                 |
| `redis`          | `check_redis`, `redis_info`                                                                         |
| `docker-compose` | `docker_status`, `docker_logs`                                                                      |
| **Common**       | `git_status`, `git_diff`, `git_recent_commits`, `morning_routine`, `nightly_routine`, `tool_search` |

### Language-Specific Tools

**Node.js**: check_nextjs/vite/express, run_typecheck, run_lint, run_tests, npm_scripts
**Python**: run_pytest, run_mypy, check_virtualenv, run_lint (ruff/black)
**Rust**: cargo_check, cargo_test, cargo_clippy

## Generation Workflow

1. **Analyze Project** - Detect tech stack, frameworks, test tools
2. **Select Tools** - Use analysis.json or auto-detect
3. **Generate Code** - TypeScript implementations with semantic descriptions
4. **Export Embeddings** - tool_embeddings.json for semantic search
5. **Register Server** - Update .claude/settings.json
6. **Report Status** - Tools created, embedding summary, next steps

<details>
<summary>📄 See detailed workflow steps (optional)</summary>

### Step 1: Project Detection

```bash
# Detect tech stack
ls package.json Cargo.toml pyproject.toml go.mod 2>/dev/null
# Find main directories
ls -d src lib app components 2>/dev/null
# Detect test framework
grep -l "jest\|mocha\|vitest\|pytest" package.json pyproject.toml 2>/dev/null
```

### Step 2: Tool Implementation

See `examples/tool-implementation.ts` for detailed examples

### Step 3: Server Registration

**Uses Claude Code 2.0.70+ wildcard syntax:**

```json
{
  "mcpServers": {
    "[project]-dev": {
      "command": "node",
      "args": [".claude/mcp-servers/[project]-dev/dist/index.js"],
      "permissions": {
        "allowed": ["mcp__[project]-dev__*"]
      }
    }
  }
}
```

**Benefits of wildcard permissions:**

- All current and future tools automatically allowed
- Less configuration maintenance
- Clearer intent: "trust this MCP server"
- See `docs/MCP_WILDCARD_PERMISSIONS.md` for details
</details>

## Semantic Tool Descriptions

Write descriptions optimized for semantic search:

| Guideline                | Example                              |
| ------------------------ | ------------------------------------ |
| **State action clearly** | "Check if...", "Run...", "Get..."    |
| **Include target**       | "...Next.js development server..."   |
| **Mention use cases**    | "...troubleshoot startup issues..."  |
| **List outputs**         | "Returns status, URL, response time" |

<details>
<summary>📋 Before/After Examples</summary>

### Before (Too Brief)

```typescript
{
  name: "health:dev-server",
  description: "Check dev server"
}
```

### After (Semantic-Friendly)

```typescript
{
  name: "health:dev-server",
  description: "Check if the Next.js development server is running and responding on port 3000. Use this to verify the dev environment is working, troubleshoot startup issues, or confirm the app is accessible. Returns status, URL, and response time."
}
```

</details>

## Auto-Embedding Tools

Generated servers include `tool_embeddings.json` for semantic search:

```json
{
  "generated_at": "2025-12-26T10:00:00Z",
  "model": "voyage-3.5",
  "dimension": 1024,
  "tools": [
    {
      "name": "health:dev-server",
      "description": "Check if the Next.js...",
      "embedding": [0.123, 0.456, ...]
    }
  ]
}
```

Requires Voyage API key. Set `VOYAGE_API_KEY` environment variable or skip with `--no-embed`.

## Post-Generation Output

```
MCP server generated at .claude/mcp-servers/[project]-dev/

Tools created (8):
✓ health:dev-server - Check Next.js dev server
✓ health:database - Check PostgreSQL connectivity
✓ quality:typecheck - Run TypeScript type checking
✓ quality:lint - Run ESLint checks
✓ quality:test - Run Jest test suite
✓ git:status - Get git working tree status
✓ git:diff - Show staged and unstaged changes
✓ search:tools - Semantic tool search

Embedding Summary:
- Tool embeddings: .claude/tool_embeddings.json
- Total tools: 8
- Successfully embedded: 8
- Model: voyage-3.5

Next steps:
1. cd .claude/mcp-servers/[project]-dev
2. npm install
3. npm run build
4. Restart Claude Code to load MCP server

Would you like me to build and test it?
```

## MCP Wildcard Permissions

**Added in Claude Code 2.0.70**

PopKit-generated MCP servers use wildcard permissions by default:

```json
{
  "mcpServers": {
    "{project-name}-dev": {
      "permissions": {
        "allowed": ["mcp__{project-name}-dev__*"]
      }
    }
  }
}
```

### Permission Patterns

| Pattern                 | Use Case                                              |
| ----------------------- | ----------------------------------------------------- |
| `mcp__server__*`        | Trust all tools (recommended for first-party servers) |
| `mcp__server__health-*` | Trust tools by namespace prefix                       |
| Explicit list           | Trust specific tools only (third-party servers)       |

### Custom Permissions

Override permissions after generation:

1. Edit `.claude/settings.json` or `.mcp.json`
2. Change from wildcard to explicit allow-list if needed
3. Add denied list for risky operations:

```json
{
  "permissions": {
    "allowed": ["mcp__git-tools__*"],
    "denied": ["mcp__git-tools__force-push", "mcp__git-tools__delete-branch"]
  }
}
```

**Documentation:** `docs/MCP_WILDCARD_PERMISSIONS.md`

## Integration Requirements

**Optional:**

- Project analysis (via analyze-project skill) for best results
- Voyage AI API key for auto-embedding (recommended)

**Enables:**

- Project-specific tools in Claude Code
- Semantic tool search with natural language queries
- Health monitoring with detailed status
- Custom workflows tailored to your stack
- Discoverable tools across projects

---

See `examples/` directory for detailed code samples and implementation patterns.
