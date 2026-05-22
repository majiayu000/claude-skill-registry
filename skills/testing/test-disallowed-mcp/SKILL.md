---
name: test-disallowed-mcp
description: Test if disallowedTools blocks MCP tools
allowed-tools:
  - Write
  - MCPSearch
disallowedTools:
  - mcp__neo4j-cypher__read_neo4j_cypher
context: fork
---

# Test: disallowedTools for MCP

**Goal**: Test if `disallowedTools:` can block specific MCP tools.

## Task

1. Try to use MCPSearch to load `mcp__neo4j-cypher__read_neo4j_cypher`
2. If loaded, try to execute a query
3. Report whether the tool was blocked or accessible

Write to: `earnings-analysis/test-outputs/disallowed-mcp-result.txt`

Include:
- Was MCPSearch able to load the disallowed tool?
- Was the query blocked or did it execute?
- Is disallowedTools enforced?
