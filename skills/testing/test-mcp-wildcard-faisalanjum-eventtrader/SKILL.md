---
name: test-mcp-wildcard
description: Test if MCP wildcards work in allowed-tools
context: fork
allowed-tools:
  - Write
  - mcp__neo4j-cypher__*
---

# MCP Wildcard Test

**Goal**: Test if `mcp__neo4j-cypher__*` pre-loads all neo4j-cypher MCP tools.

## Task

1. Check if you have direct access to `mcp__neo4j-cypher__read_neo4j_cypher` WITHOUT using MCPSearch
2. Try to execute: `MATCH (c:Company {ticker: 'AAPL'}) RETURN c.name LIMIT 1`
3. Write results to `earnings-analysis/test-outputs/mcp-wildcard-result.txt`

Include:
- Whether MCP tool was directly available (no MCPSearch needed)
- Whether query executed successfully
- Result of query
- Whether wildcard `mcp__neo4j-cypher__*` worked for pre-loading
