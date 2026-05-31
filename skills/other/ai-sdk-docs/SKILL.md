---
name: AI SDK Documentation
description: This skill should be used when working with Vercel AI SDK, AI Gateway, streamText, generateText, generateObject, streamObject, tool calling, or AI SDK providers. Also relevant for "ai-sdk", "@ai-sdk/*" packages, or questions about AI SDK patterns, configuration, and best practices.
---

# AI SDK Documentation Skill

This skill provides tools for accessing Vercel AI SDK documentation and AI Gateway model information. Use the bundled scripts to discover available documentation pages and fetch their full content.

## Overview

The Vercel AI SDK documentation lives at `ai-sdk.dev` and covers:
- **Core SDK** (`ai` package) - generating text, streaming, tool calling, embeddings
- **UI integrations** - React hooks, streaming UI components
- **RSC** - React Server Components integration
- **Providers** - Configuration for OpenAI, Anthropic, Google, and 30+ other providers
- **AI Gateway** - Vercel's multi-provider routing service

The documentation is large (600+ pages) and frequently updated. Rather than relying on stale knowledge, always use the scripts to fetch current documentation.

## Scripts

All scripts are located in `${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/`.

### list-docs.sh

Discover available documentation pages.

**Usage:**
```bash
# List all pages grouped by category
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/list-docs.sh

# List pages in a specific category
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/list-docs.sh docs
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/list-docs.sh cookbook
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/list-docs.sh providers
```

**Categories:**
- `docs` - Core documentation (concepts, guides, API reference)
- `cookbook` - Code examples by framework (Next.js, Node.js, etc.)
- `providers` - Provider-specific setup and configuration
- `elements` - UI component library documentation
- `tools-registry` - Third-party tool integrations

**When to use:** Run this first to discover what pages exist. Do not assume documentation structure.

### fetch-doc.sh

Fetch the full markdown content of a specific documentation page.

**Usage:**
```bash
# Fetch a documentation page
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/fetch-doc.sh /docs/ai-sdk-core/generating-text

# Fetch a cookbook example
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/fetch-doc.sh /cookbook/next/generating-structured-data

# Fetch provider documentation
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/fetch-doc.sh /providers/ai-sdk-providers/openai
```

**Input:** A documentation path (e.g., `/docs/ai-sdk-core/tools-and-tool-calling`)

**Output:** Full markdown content of the page

**When to use:** After identifying relevant pages with `list-docs.sh`, fetch the ones that look most relevant to the task.

### query-models.sh

Query the AI Gateway models API for available models and their capabilities.

**Usage:**
```bash
# List all models with their provider
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/query-models.sh list

# List all providers
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/query-models.sh providers

# List all capability tags
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/query-models.sh tags

# List models from a specific provider
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/query-models.sh --provider anthropic

# List models with a specific capability
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/query-models.sh --tag vision
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/query-models.sh --tag tool-use

# Get full details for a specific model
${CLAUDE_PLUGIN_ROOT}/skills/ai-sdk-docs/scripts/query-models.sh --details openai/gpt-4o
```

**Model details include:** context window, max tokens, pricing, capability tags (vision, tool-use, reasoning, etc.)

**When to use:** When needing to know what models are available, compare model capabilities, or check pricing/context limits.

## Workflow Guidelines

### Finding Documentation

1. **Start with discovery**: Run `list-docs.sh` to see available pages
2. **Identify relevant pages**: Look for pages whose paths match the topic
3. **Fetch content**: Use `fetch-doc.sh` to get full content of relevant pages
4. **Read multiple pages if needed**: Topics often span multiple pages (e.g., a concept page + API reference page)

## Important Notes

- **Always fetch current docs**: Do not rely on potentially outdated knowledge. Use the scripts to get current documentation.
- If a page doesn't appear in `list-docs.sh` output, it doesn't exist.
- **Some pages may not have .md versions**: The script will indicate when this happens.
- **Documentation is comprehensive**: The AI SDK docs include guides, API references, examples, and troubleshooting. Check multiple sections for complete information.

## AI Gateway

The AI Gateway is Vercel's unified API for accessing multiple AI providers. Key points:

- Single API endpoint, multiple providers
- Use `query-models.sh` to see all available models
- Models are identified as `provider/model-name` (e.g., `anthropic/claude-sonnet-4`)
- Provider-specific documentation is under `/providers/`
