---
name: test-inherit-child
description: Child skill - tests if it can use MCP tool from its own allowed-tools (parent doesn't have it)
allowed-tools:
  - mcp__neo4j-cypher__read_neo4j_cypher
  - Write
context: fork
---

# Test Inherit Child

**Goal**: Test if child can use MCP tool listed in ITS OWN allowed-tools, even if parent doesn't have it.

## Task

1. Try to use mcp__neo4j-cypher__read_neo4j_cypher directly (no MCPSearch)
2. Execute: `MATCH (c:Company {ticker: 'IBM'}) RETURN c.name LIMIT 1`
3. Report result

Write to: `earnings-analysis/test-outputs/inherit-child-result.txt`

Return: "CHILD_MCP_ACCESS: [yes/no] | RESULT: [query result or error]"
