---
name: mcp-documentation-skill
description: "DEPRECATED - This skill references MCP servers that no longer exist in the codebase. The CodebaseDocumentation server was archived during MCP cleanup. Use native file reading tools (view_file, grep_search) for documentation access."
tags: [deprecated, mcp, legacy]
status: archived
---

# ⚠️ DEPRECATED: MCP Documentation Skill

**STATUS:** This skill is deprecated and should not be used.

## Why This Skill Was Deprecated

During the MCP cleanup (December 2025), we removed custom documentation caching servers due to:

1. **Stale Cache Issues**: Cached content became outdated as files changed
2. **Complexity Overhead**: Custom server maintenance vs. native file access
3. **Redundancy**: Direct file reading is simpler and more reliable
4. **Single Source of Truth**: Reading files directly ensures accuracy

### Servers That Were Removed

- ❌ **CodebaseDocumentation** (`documentation-server.py`) - Moved to `_legacy_archive/`
- ❌ All custom documentation indexing and caching

## Migration Guide

### Old Approach (Using This Deprecated Skill)

```
method: search_docs("deployment")
Risk: Returns cached (potentially stale) content
Token Claim: "90% token savings"
Reality: Cache invalidation issues outweigh benefits
```

### New Approach (Recommended)

```bash
# Direct file access (always current)
view_file /path/to/DOCUMENTATION.md

# Search across documentation
grep_search "deployment" in .claude/docs/

# Find specific docs
find_by_name "*.md" in .claude/

# List available agents
list_dir /home/njd/careercopilot/careercopilot-1/.claude/agents/

# List available skills  
list_dir /home/njd/careercopilot/careercopilot-1/.claude/skills/
```

## What To Use Instead

| Old MCP Method | New Approach | Benefits |
|----------------|--------------|----------|
| `search_docs` | `grep_search` with .md files | Always current, no cache staleness |
| `get_docs` | `view_file` on specific doc | Direct access, no caching layer |
| `get_agents` | `list_dir` + `view_file` | See actual file structure |
| `get_skills` | `list_dir` + `view_file` | See actual file structure |
| `index` | `find_by_name` + directory listing | Real-time file discovery |

## Current Documentation Structure

```
careercopilot-1/
├── .claude/
│   ├── agents/              # 20 agent definitions
│   ├── skills/              # 29 skill directories
│   ├── docs/                # Architecture docs
│   └── workflows/           # Workflow definitions
├── docs/                    # Project documentation
│   ├── architecture/
│   ├── archive_legacy_reports/
│   └── archive_mcp_configs/
└── README.md                # Main project documentation
```

## Accessing Documentation

### List All Agents

```typescript
// Old: mcp_documentation_get_agents()
// New:
list_dir("/home/njd/careercopilot/careercopilot-1/.claude/agents/")
// Then view specific agents:
view_file("/home/njd/careercopilot/careercopilot-1/.claude/agents/devops-specialist.md")
```

### List All Skills

```typescript
// Old: mcp_documentation_get_skills()
// New:
list_dir("/home/njd/careercopilot/careercopilot-1/.claude/skills/")
// Then view specific skill:
view_file("/home/njd/careercopilot/careercopilot-1/.claude/skills/component-builder/SKILL.md")
```

### Search Documentation

```typescript
// Old: mcp_documentation_search_docs("deployment")
// New:
grep_search({
  SearchPath: "/home/njd/careercopilot/careercopilot-1/.claude/docs",
  Query: "deployment",
  Includes: ["*.md"],
  MatchPerLine: true
})
```

### Find Workflows

```typescript
// Old: Not available in old MCP
// New:
list_dir("/home/njd/careercopilot/careercopilot-1/.agent/workflows/")
view_file("/home/njd/careercopilot/careercopilot-1/.agent/workflows/component_builder.md")
```

## Current MCP Ecosystem

For actual MCP capabilities, use:

1. **flash-sidekick MCP** - AI assistance
   - `consult_pro` - Deep reasoning/coding (Pro 2.5)
   - `quick_summarize` - Fast text summarization (Flash Lite)
   - `generate_idf` - Python IDF generation (Flash Lite)

2. **GitHub MCP** - Repository operations
   - File management, PR/issues, search

3. **Playwright MCP** - Browser automation
   - Via `browser_subagent` tool

4. **Docker MCP** - Container management

## Performance Reality Check

**Token Savings Claim**: "90-95% per request"

**Reality**: 
- Native file reading is fast (\<100ms)
- No cache invalidation complexity
- Always shows current content
- Simpler mental model
- No custom server maintenance

**The "token savings" were theoretical** and didn't account for:
- Cache invalidation overhead
- Stale content debugging
- Server maintenance complexity
- CI/CD integration issues

## Related Documentation

- See conversation `0b3a6c3f-6c7e-4743-bc7c-a34b3bbe08e3` for MCP cleanup
- Current MCP configuration: `mcp.json`
- Archived server: `_legacy_archive/documentation-server.py`

---

**Last Updated**: 2025-12-28  
**Deprecated**: 2025-12-27  
**Replacement**: Native file system tools (view_file, grep_search, list_dir, find_by_name)
