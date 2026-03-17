---
# VERSION: 2.88.0
name: openai-docs
description: "Access OpenAI developer documentation via Context7 MCP. Provides up-to-date docs for Codex CLI, OpenAI API, Python/Node SDKs, Agents SDK, and MCP configuration. Use when: (1) configuring Codex CLI or MCP servers, (2) writing OpenAI API integrations, (3) building agents with OpenAI SDKs, (4) troubleshooting Codex execution. Triggers: 'openai docs', 'codex documentation', 'openai api reference', 'codex mcp', 'agents sdk'."
---

# OpenAI Documentation Access Skill

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

**ultrathink** - Take a deep breath. We're not here to write code. We're here to make a dent in the universe.

## The Vision
Documentation lookups should feel inevitable and authoritative.

## Your Work, Step by Step
1. **Identify target**: Pick the right library and query.
2. **Resolve ID**: Use Context7 to get exact docs.
3. **Query precisely**: Ask for focused, answerable snippets.
4. **Apply results**: Convert docs into actionable guidance.

## Ultrathink Principles in Practice
- **Think Different**: Seek the most direct source of truth.
- **Obsess Over Details**: Use exact IDs and query wording.
- **Plan Like Da Vinci**: Decide the lookup path before querying.
- **Craft, Don't Code**: Keep results concise and relevant.
- **Iterate Relentlessly**: Re-query when ambiguity remains.
- **Simplify Ruthlessly**: Avoid unnecessary sources.

# OpenAI Documentation Access Skill

Access OpenAI's complete developer documentation through Context7 MCP integration.

## Quick Start

```yaml
# Query Codex CLI documentation
mcp__context7__query-docs:
  libraryId: "/websites/developers_openai_codex"
  query: "your question about Codex CLI"

# Query OpenAI API documentation
mcp__context7__query-docs:
  libraryId: "/websites/platform_openai"
  query: "your question about OpenAI API"
```

## Available Documentation Libraries

| Library ID | Content | Snippets | Score |
|------------|---------|----------|-------|
| `/websites/developers_openai_codex` | Codex CLI docs | 614 | 75.8 |
| `/websites/platform_openai` | OpenAI API docs | 9,418 | 69.1 |
| `/openai/openai-python` | Python SDK | 429 | 90.7 |
| `/openai/openai-node` | Node.js SDK | 437 | 87.9 |
| `/openai/codex` | Codex core | 491 | 62.1 |
| `/openai/codex-action` | GitHub Action | 36 | 78.8 |

## Common Queries

### Codex CLI Configuration

```yaml
# MCP server configuration
query-docs:
  libraryId: "/websites/developers_openai_codex"
  query: "MCP server configuration config.toml remote URL authentication"

# Sandbox modes and permissions
query-docs:
  libraryId: "/websites/developers_openai_codex"
  query: "sandbox modes read-only workspace-write danger-full-access"

# Session resume and parallel execution
query-docs:
  libraryId: "/websites/developers_openai_codex"
  query: "exec resume session parallel execution workflow"
```

### OpenAI API Integration

```yaml
# Chat completions
query-docs:
  libraryId: "/websites/platform_openai"
  query: "chat completions API streaming function calling"

# Embeddings and vector search
query-docs:
  libraryId: "/websites/platform_openai"
  query: "embeddings API text-embedding-3 vector dimensions"

# Assistants API
query-docs:
  libraryId: "/websites/platform_openai"
  query: "assistants API threads messages runs tools"
```

### SDK Usage

```yaml
# Python SDK async patterns
query-docs:
  libraryId: "/openai/openai-python"
  query: "async client streaming completions error handling"

# Node.js SDK TypeScript
query-docs:
  libraryId: "/openai/openai-node"
  query: "TypeScript types streaming response handling"
```

## MCP Configuration Reference

### Context7 (Already Configured)

```toml
# ~/.codex/config.toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp@latest"]
```

### Remote MCP Servers

```toml
# Streamable HTTP server format
[mcp_servers.example]
url = "https://example.com/mcp"
bearer_token_env_var = "EXAMPLE_TOKEN"
http_headers = { "X-Custom-Header" = "value" }
```

### STDIO Servers

```toml
# Local command-based server
[mcp_servers.local]
command = "npx"
args = ["-y", "@package/mcp-server"]

[mcp_servers.local.env]
API_KEY = "your-key"
```

## Integration with Codex CLI Skill

This skill complements `/codex-cli` by providing documentation lookup:

1. **Before execution**: Query docs for correct flags/options
2. **On error**: Look up error codes and solutions
3. **Configuration**: Find correct config.toml syntax

### Workflow Example

```bash
# 1. Query documentation for correct syntax
# Use mcp__context7__query-docs with libraryId="/websites/developers_openai_codex"

# 2. Execute Codex with correct options
codex exec -m gpt-5.2-codex --full-auto "task"

# 3. On error, query docs for solution
# Query: "error code XYZ troubleshooting"
```

## Claude-Codex Documentation Bridge

When Claude needs OpenAI documentation:

1. **Use Context7 MCP** (already available in both Claude and Codex)
2. **Query appropriate library** based on topic
3. **Apply findings** to implementation

This eliminates the need for a separate "openaiDevelopers" MCP - Context7 provides all OpenAI documentation with 614+ Codex CLI snippets and 9,400+ API snippets.

## See Also

- `/codex-cli` - Codex CLI orchestration skill
- `/library-docs` - General library documentation via Context7
- `~/.codex/config.toml` - MCP server configuration
