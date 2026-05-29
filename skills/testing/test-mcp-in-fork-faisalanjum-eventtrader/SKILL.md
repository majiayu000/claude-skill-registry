---
name: test-mcp-in-fork
description: Test if MCP tools can be accessed from forked skill context
allowed-tools: Read, Write, MCPSearch
model: claude-opus-4-5
permissionMode: dontAsk
context: fork
---

# Test MCP Access in Fork

**Goal**: Verify if MCP tools can be loaded and executed from a forked skill.

## Task

1. Use MCPSearch to load `mcp__neo4j-cypher__read_neo4j_cypher`
2. If loaded, execute a simple query: `MATCH (c:Company {ticker: 'AAPL'}) RETURN c.name LIMIT 1`
3. Write results to: `earnings-analysis/test-outputs/mcp-in-fork-result.txt`

Include in output:
- Whether MCPSearch was available
- Whether MCP tool was loaded successfully
- Whether query executed successfully
- The query result (if any)
- List of tools you have access to
