---
name: test-inherit-child2
description: Child skill WITHOUT MCP tool - tests if it inherits from parent
allowed-tools:
  - Write
context: fork
---

# Test Inherit Child 2

**Goal**: Test if MCP tool is PRE-LOADED (directly usable) when only parent has it.

## Task

1. Child does NOT have mcp__neo4j-cypher__read_neo4j_cypher in allowed-tools
2. **DO NOT use MCPSearch** - try to call MCP tool directly
3. Report if it works WITHOUT MCPSearch

Write to: `earnings-analysis/test-outputs/inherit-child2-result.txt`

Return: "MCP_PRELOADED_FROM_PARENT: [yes/no] | DIRECT_ACCESS: [worked/failed]"
