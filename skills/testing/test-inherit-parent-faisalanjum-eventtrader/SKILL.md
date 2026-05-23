---
name: test-inherit-parent
description: Parent skill WITHOUT MCP tool - calls child that HAS MCP tool
allowed-tools:
  - Write
  - Skill
context: fork
---

# Test Inherit Parent

**Goal**: Test tool inheritance. Parent does NOT have MCP tool, child DOES.

## Task

1. Note: Parent does NOT have mcp__neo4j-cypher__read_neo4j_cypher in allowed-tools
2. Call `/test-inherit-child` (which HAS the MCP tool in its allowed-tools)
3. Capture child's return value
4. Report whether child was able to use the MCP tool

Write to: `earnings-analysis/test-outputs/inherit-parent-result.txt`

Include:
- Parent's allowed-tools (no MCP)
- Child's result (did child access MCP?)
- Conclusion about inheritance
