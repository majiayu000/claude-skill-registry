---
name: test-3layer-bottom
description: Layer 3 (bottom) of 3-layer test - executes MCP query
allowed-tools: Write, MCPSearch
context: fork
---

# Layer 3 Bottom

**Goal**: Execute MCP query and return result to Layer 2.

## Task

1. Use MCPSearch to load `mcp__neo4j-cypher__read_neo4j_cypher`
2. Execute: `MATCH (c:Company) RETURN c.ticker LIMIT 3`
3. Write to: `earnings-analysis/test-outputs/3layer-bottom.txt`

Return format: "LAYER3_RESULT: [list of tickers]"
