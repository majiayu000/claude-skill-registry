---
name: test-agent-field
description: Test if agent: field references existing agent for permissionMode
agent: neo4j-report
context: fork
---

# Test Agent Field

**Goal**: Test if `agent: neo4j-report` grants this skill the agent's permissionMode and tools.

## Task

1. Check if you have access to MCP tool `mcp__neo4j-cypher__read_neo4j_cypher`
2. Try to execute: `MATCH (c:Company {ticker: 'MSFT'}) RETURN c.name LIMIT 1`
3. Check if any permission prompts appeared (they shouldn't if permissionMode: dontAsk works)
4. Report your findings

Write to: `earnings-analysis/test-outputs/agent-field-result.txt`

Include:
- Whether agent: field was recognized
- Whether MCP tool was accessible
- Whether query executed without permission prompt
- Any error messages
