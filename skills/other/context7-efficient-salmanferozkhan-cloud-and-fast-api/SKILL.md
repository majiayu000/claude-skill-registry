---
name: context7-efficient
description: Token-efficient library documentation fetcher using Context7 MCP with 86.8% token savings through intelligent shell pipeline filtering. Fetches code examples, API references, and best practices for JavaScript, Python, Go, Rust, and other libraries. Use when users ask about library documentation, need code examples, want API usage patterns, are learning a new framework, need syntax reference, or troubleshooting with library-specific information. Triggers include questions like "Show me React hooks", "How do I use Prisma", "What's the Next.js routing syntax", or any request for library/framework documentation.
---

# Context7 Efficient Documentation Fetcher

Fetch library documentation with automatic 77% token reduction via shell pipeline.

## Quick Start

**Always use the token-efficient shell pipeline:**

```bash
# Automatic library resolution + filtering
bash scripts/fetch-docs.sh --library <library-name> --topic <topic>

# Examples:
bash scripts/fetch-docs.sh --library react --topic useState
bash scripts/fetch-docs.sh --library nextjs --topic routing
bash scripts/fetch-docs.sh --library prisma --topic queries
```

**Result:** Returns ~205 tokens instead of ~934 tokens (77% savings).

## Standard Workflow

For any documentation request, follow this workflow:

### 1. Identify Library and Topic

Extract from user query:
- **Library:** React, Next.js, Prisma, Express, etc.
- **Topic:** Specific feature (hooks, routing, queries, etc.)

### 2. Fetch with Shell Pipeline

```bash
bash scripts/fetch-docs.sh --library <library> --topic <topic> --verbose
```

The `--verbose` flag shows token savings statistics.

### 3. Use Filtered Output

The script automatically:
- Fetches full documentation (934 tokens, stays in subprocess)
- Filters to code examples + API signatures + key notes
- Returns only essential content (205 tokens to Claude)

## Parameters

### Basic Usage

```bash
bash scripts/fetch-docs.sh [OPTIONS]
```

**Required (pick one):**
- `--library <name>` - Library name (e.g., "react", "nextjs")
- `--library-id <id>` - Direct Context7 ID (faster, skips resolution)

**Optional:**
- `--topic <topic>` - Specific feature to focus on
- `--mode <code|info>` - code for examples (default), info for concepts
- `--page <1-10>` - Pagination for more results
- `--verbose` - Show token savings statistics

### Mode Selection

**Code Mode (default):** Returns code examples + API signatures
```bash
--mode code
```

**Info Mode:** Returns conceptual explanations + fewer examples
```bash
--mode info
```

## Common Library IDs

Use `--library-id` for faster lookup (skips resolution):

```bash
React:      /reactjs/react.dev
Next.js:    /vercel/next.js
Express:    /expressjs/express
Prisma:     /prisma/docs
MongoDB:    /mongodb/docs
Fastify:    /fastify/fastify
NestJS:     /nestjs/docs
Vue.js:     /vuejs/docs
Svelte:     /sveltejs/site
```

## Workflow Patterns

### Pattern 1: Quick Code Examples

User asks: "Show me React useState examples"

```bash
bash scripts/fetch-docs.sh --library react --topic useState --verbose
```

Returns: 5 code examples + API signatures + notes (~205 tokens)

### Pattern 2: Learning New Library

User asks: "How do I get started with Prisma?"

```bash
# Step 1: Get overview
bash scripts/fetch-docs.sh --library prisma --topic "getting started" --mode info

# Step 2: Get code examples
bash scripts/fetch-docs.sh --library prisma --topic queries --mode code
```

### Pattern 3: Specific Feature Lookup

User asks: "How does Next.js routing work?"

```bash
bash scripts/fetch-docs.sh --library-id /vercel/next.js --topic routing
```

Using `--library-id` is faster when you know the exact ID.

### Pattern 4: Deep Exploration

User needs comprehensive information:

```bash
# Page 1: Basic examples
bash scripts/fetch-docs.sh --library react --topic hooks --page 1

# Page 2: Advanced patterns
bash scripts/fetch-docs.sh --library react --topic hooks --page 2
```

## Token Efficiency

**How it works:**

1. `fetch-docs.sh` calls `fetch-raw.sh` (which uses `mcp-client.py`)
2. Full response (934 tokens) stays in subprocess memory
3. Shell filters (awk/grep/sed) extract essentials (0 LLM tokens used)
4. Returns filtered output (205 tokens) to Claude

**Savings:**
- Direct MCP: 934 tokens per query
- This approach: 205 tokens per query
- **77% reduction**

**Do NOT use `mcp-client.py` directly** - it bypasses filtering and wastes tokens.

## Advanced: Library Resolution

If library name fails, try variations:

```bash
# Try different formats
--library "next.js"    # with dot
--library "nextjs"     # without dot
--library "next"       # short form

# Or search manually
bash scripts/fetch-docs.sh --library "your-library" --verbose
# Check output for suggested library IDs
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Library not found | Try name variations or use broader search term |
| No results | Use `--mode info` or broader topic |
| Need more examples | Increase page: `--page 2` |
| Want full context | Use `--mode info` for explanations |

## References

For detailed Context7 MCP tool documentation, see:
- [references/context7-tools.md](references/context7-tools.md) - Complete tool reference

## Implementation Notes

**Components (for reference only, use fetch-docs.sh):**
- `mcp-client.py` - Universal MCP client (foundation)
- `fetch-raw.sh` - MCP wrapper
- `extract-code-blocks.sh` - Code example filter (awk)
- `extract-signatures.sh` - API signature filter (awk)
- `extract-notes.sh` - Important notes filter (grep)
- `fetch-docs.sh` - **Main orchestrator (ALWAYS USE THIS)**

**Architecture:**
Shell pipeline processes documentation in subprocess, keeping full response out of Claude's context. Only filtered essentials enter the LLM context, achieving 77% token savings with 100% functionality preserved.

Based on [Anthropic's "Code Execution with MCP" blog post](https://www.anthropic.com/engineering/code-execution-with-mcp).
