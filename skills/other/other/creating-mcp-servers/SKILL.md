---
name: creating-mcp-servers
description: Creates production-ready MCP servers using FastMCP v2. Use when building MCP servers, optimizing tool descriptions for context efficiency, implementing progressive disclosure for multiple capabilities, or packaging servers for distribution.
metadata:
  version: 1.1.0
---

# Creating MCP Servers

Build production-ready MCP servers using FastMCP v2 with optimal context efficiency through progressive disclosure patterns.

## Core Capabilities

1. **Apply mandatory patterns** - Four critical requirements for consistency
2. **Implement progressive disclosure** - Gateway patterns achieving 85-93% token reduction  
3. **Optimize tool descriptions** - 65-70% token reduction through proper patterns
4. **Bundle servers** - Package as MCPB files with validation
5. **Proven gateway patterns** - Three complete implementations (Skills, API, Query)

## Trigger Patterns

**Activate this skill when:**
- "MCP server", "create MCP", "build MCP", "FastMCP"
- "progressive disclosure", "gateway pattern", "context efficient"
- "optimize MCP", "reduce context", "tool descriptions"
- "MCPB", "bundle MCP", "package server"

## Architecture Decision

```
1-3 simple tools?
  → Standard FastMCP with optimized tools
  Load: references/MANDATORY_PATTERNS.md

5+ related capabilities?
  → Gateway pattern (progressive disclosure)
  Load: references/PROGRESSIVE_DISCLOSURE.md
  Load: references/GATEWAY_PATTERNS.md

Optimize existing server?
  → Apply mandatory patterns
  Load: references/MANDATORY_PATTERNS.md

Package for distribution?
  → MCPB bundler
  Load: references/MCPB_BUNDLING.md
  Execute: scripts/create_mcpb.py

Need FastMCP documentation?
  → Search references/LLMS_TXT.md for relevant URLs
  → Use web_fetch on gofastmcp.com URLs
```

## Mandatory Patterns (Summary)

Four critical requirements for ALL implementations:

1. **uv (never pip)** - `uv pip install fastmcp`
2. **Optimized tool descriptions** - Annotations, Annotated, concise docstrings
3. **Authoritative documentation** - Fetch from gofastmcp.com via LLMS_TXT.md index
4. **Apply all patterns** - Every implementation meets verification checklist

Details in [references/MANDATORY_PATTERNS.md](references/MANDATORY_PATTERNS.md)

## Documentation Retrieval Workflow

**To fetch FastMCP documentation:**

```
1. Read references/LLMS_TXT.md - complete URL index
2. Search for relevant topic keywords
3. Use web_fetch on matched URLs (append .md for markdown)
4. Apply patterns from fetched documentation
```

**Example:** Authentication patterns → Search LLMS_TXT.md for "authentication" → web_fetch https://gofastmcp.com/servers/auth/authentication.md

## Progressive Disclosure Pattern

For servers with 5+ capabilities:

**Three-tier loading:**
1. Metadata (~20 tokens/capability) - Always loaded
2. Content (~500 tokens) - Load on demand
3. Execution (0 tokens) - Execute without loading

Achieves 85-93% baseline reduction. See [references/PROGRESSIVE_DISCLOSURE.md](references/PROGRESSIVE_DISCLOSURE.md)

## Implementation Phases

### Phase 1: Research
Read LLMS_TXT.md → Find relevant URLs → web_fetch documentation

### Phase 2: Implement
Load appropriate reference based on architecture decision. Apply all four mandatory patterns.

### Phase 3: Package (Optional)
```bash
cd /home/claude
zip -r server-name.mcpb manifest.json server.py README.md
cp server-name.mcpb /mnt/user-data/outputs/
```

See [references/MCPB_BUNDLING.md](references/MCPB_BUNDLING.md) for manifest format.

## Reference Library

**Documentation index (load first for FastMCP knowledge):**
- [LLMS_TXT.md](references/LLMS_TXT.md) - Complete FastMCP v2 documentation URLs

**Core patterns:**
- [MANDATORY_PATTERNS.md](references/MANDATORY_PATTERNS.md) - Four critical requirements
- [PROGRESSIVE_DISCLOSURE.md](references/PROGRESSIVE_DISCLOSURE.md) - Architecture for 5+ capabilities

**Implementation:**
- [GATEWAY_PATTERNS.md](references/GATEWAY_PATTERNS.md) - Three production-ready implementations
- [MCPB_BUNDLING.md](references/MCPB_BUNDLING.md) - Packaging and distribution

**Scripts:**
- `scripts/create_mcpb.py` - Bundle MCP servers into .mcpb files

## Verification Checklist

Before completing any FastMCP implementation:

```
✓ Uses uv (not pip)
✓ FastMCP docs fetched from LLMS_TXT.md URLs (not web_search)
✓ Tool annotations (readOnlyHint, title, openWorldHint)
✓ Annotated parameters with Field
✓ Single-sentence docstrings
✓ 65-70% token reduction vs verbose
✓ Server instructions concise (<100 chars)
```

For gateway implementations, additionally verify:
```
✓ 85%+ baseline context reduction
✓ Discover returns metadata only
✓ Load fetches content on demand
✓ Execute runs without context cost
```

## Tool Description Pattern

**Before (180 tokens):**
```python
@mcp.tool()
async def search_items(query: str):
    """Search for items in the database.
    This tool allows comprehensive searching..."""
```

**After (55 tokens):**
```python
@mcp.tool(
    annotations={"title": "Search", "readOnlyHint": True, "openWorldHint": False}
)
async def search_items(
    query: Annotated[str, Field(description="Search text")],
    ctx: Context = None
):
    """Search items. Fast full-text search across all fields."""
```

## Common Pitfalls

❌ Using `mcpb pack` CLI (causes crashes, just use `zip`)  
❌ Using pip instead of uv  
❌ web_search for FastMCP docs (use web_fetch on LLMS_TXT.md URLs)  
❌ Verbose tool descriptions  
❌ Missing tool annotations  
❌ Gateway for 1-3 tools (overhead exceeds benefit)  
❌ Mixing unrelated capabilities in single gateway
