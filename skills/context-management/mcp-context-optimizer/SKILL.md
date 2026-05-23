---
name: mcp-context-optimizer
description: Optimize MCP tool context loading through progressive disclosure and hierarchical indexing. Use when working with large MCP tool sets (e.g., Miyabi's 172 tools) to prevent context window bloat. Triggers include "find tool", "search mcp", "tool lookup", "which tool", "context optimization", or when dealing with many MCP tools.
version: 1.0.0
author: Miyabi
---

# MCP Context Optimizer

Solve the context window bloat problem when working with large MCP tool collections through **progressive disclosure** and **hierarchical indexing**.

## Problem Statement

Large MCP implementations (like Miyabi with 172 tools across 22 categories) can overwhelm the context window:
- All tool definitions load into main context
- Token consumption increases dramatically
- Risk of selecting wrong tools
- Slower response times

## Solution: Progressive Disclosure Pattern

```
┌─────────────────────────────────────────────────────────────┐
│  Level 1: Category Index (Always Loaded)                    │
│  ~200 tokens - 22 categories with descriptions              │
├─────────────────────────────────────────────────────────────┤
│  Level 2: Tool Index (On-Demand)                            │
│  ~50 tokens per category - tool names + short descriptions  │
├─────────────────────────────────────────────────────────────┤
│  Level 3: Full Tool Schema (On-Demand)                      │
│  Variable - complete parameters and usage                   │
└─────────────────────────────────────────────────────────────┘
```

## Quick Reference: Miyabi MCP Categories

| Category | Count | Primary Use Case |
|----------|-------|------------------|
| github | 21 | Issues, PRs, workflows, releases |
| git | 19 | Version control operations |
| network | 15 | Connectivity, diagnostics |
| process | 14 | Process management |
| tmux | 10 | Terminal multiplexer |
| resource | 10 | CPU, memory, disk monitoring |
| file | 10 | File operations |
| docker | 10 | Container management |
| speckit | 9 | Spec-driven development |
| claude | 8 | Claude Code session |
| log | 7 | Log analysis |
| k8s | 6 | Kubernetes |
| db | 6 | Database operations |
| compose | 4 | Docker Compose |
| time | 4 | Time utilities |
| gen | 4 | UUID, password, hash |
| linux | 3 | Systemd services |
| mcp | 3 | Tool discovery |
| calc | 3 | Math calculations |
| think | 3 | Reasoning chains |
| windows | 2 | Windows services |
| health | 1 | System health |

## Workflow: Tool Discovery Protocol

### Step 1: Identify Category
```
User Request → Parse Intent → Match Category
```

**Category Matching Rules:**
- Git operations (commit, branch, diff) → `git`
- GitHub (PR, issue, workflow) → `github`
- Container (docker run, logs) → `docker`
- System monitoring (CPU, memory) → `resource`
- File operations (read, search) → `file`
- Network (ping, port check) → `network`

### Step 2: Search Within Category
```javascript
// Use mcp_search_tools with category filter
miyabi:mcp_search_tools({
  category: "docker",
  query: "logs"  // optional refinement
})
```

### Step 3: Get Full Tool Info
```javascript
// Only load full schema when needed
miyabi:mcp_get_tool_info({
  tool: "docker_logs"
})
```

## Implementation Patterns

### Pattern 1: Intent-Based Routing
```markdown
## User says: "Check container logs for errors"

1. Parse: container + logs → category: docker
2. Search: mcp_search_tools(category: "docker", query: "logs")
3. Result: docker_logs tool
4. Load: mcp_get_tool_info("docker_logs")
5. Execute: docker_logs(container: "x", tail: 100)
```

### Pattern 2: Multi-Category Workflow
```markdown
## User says: "Deploy and verify"

1. Parse: deploy → docker/compose, verify → health/network
2. Workflow:
   a. compose_up (compose category)
   b. network_port_check (network category)
   c. docker_logs (docker category)
   d. health_check (health category)
```

### Pattern 3: Fallback Search
```markdown
## When category unclear:

1. Use broad search: mcp_search_tools(query: "user's keywords")
2. Review results
3. Narrow if needed
```

## Best Practices

### DO:
- ✅ Start with category identification
- ✅ Use `mcp_search_tools` before loading full schemas
- ✅ Cache frequently used tool info in conversation
- ✅ Combine related tools in single workflow

### DON'T:
- ❌ Load all 172 tool definitions upfront
- ❌ Guess tool names without searching
- ❌ Repeat tool info lookups in same conversation
- ❌ Use broad search when category is known

## Tool Discovery Commands

### List All Categories
```
miyabi:mcp_list_categories()
```

### Search Tools
```
miyabi:mcp_search_tools({
  category: "git",      // optional filter
  query: "branch"       // optional keyword
})
```

### Get Tool Details
```
miyabi:mcp_get_tool_info({
  tool: "git_branch_list"
})
```

## Context Budget Guidelines

| Scenario | Token Budget | Strategy |
|----------|-------------|----------|
| Simple task | ~500 | Direct tool call |
| Multi-step | ~1000 | Category + 2-3 tools |
| Complex workflow | ~2000 | Full tool chain |
| Exploration | ~300 | Category list only |

## Integration with Other Skills

### With full-dev-cycle Skill
```
1. mcp-context-optimizer identifies tools
2. full-dev-cycle executes workflow
3. Progressive loading throughout
```

### With miyabi-agent-orchestration
```
1. Lead agent uses optimizer for tool selection
2. Sub-agents receive only needed tool schemas
3. Reduced context per agent
```

## Troubleshooting

### "Can't find the right tool"
1. Check category mapping above
2. Try broader search query
3. List all tools in suspected category

### "Context too large"
1. Use `mcp_list_categories` first (lowest token cost)
2. Filter by category before detailed search
3. Don't request tool info until needed

### "Tool doesn't exist"
1. Verify category with `mcp_list_categories`
2. Search without typos
3. Check if tool is platform-specific (linux/windows)

## Metrics for Success

- **Token Reduction**: 60-80% vs loading all tools
- **Accuracy**: Higher tool selection accuracy
- **Speed**: Faster response with targeted loading
- **Scalability**: Works with 100+ tools

## Future Enhancements

- [ ] Auto-categorization from natural language
- [ ] Tool usage frequency caching
- [ ] Cross-category tool suggestions
- [ ] Workflow template library
