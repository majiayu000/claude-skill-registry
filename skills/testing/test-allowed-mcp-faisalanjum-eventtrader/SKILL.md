---
name: test-allowed-mcp
description: Test if allowed-tools with MCP tool makes it available without MCPSearch
allowed-tools:
  - mcp__neo4j-cypher__read_neo4j_cypher
  - Write
context: fork
---

# Test: MCP Tool in allowed-tools

**Goal**: Test if listing MCP tool in `allowed-tools:` makes it directly available WITHOUT calling MCPSearch first.

## Task

1. **DO NOT use MCPSearch** - try to use the MCP tool directly
2. Try to execute: `MATCH (c:Company {ticker: 'GE'}) RETURN c.name LIMIT 1`
3. Report whether it worked or failed

Write to: `earnings-analysis/test-outputs/allowed-mcp-result.txt`

Include:
- Did you have direct access to mcp__neo4j-cypher__read_neo4j_cypher?
- Did you need to call MCPSearch first?
- Did the query execute?
- Any error messages
