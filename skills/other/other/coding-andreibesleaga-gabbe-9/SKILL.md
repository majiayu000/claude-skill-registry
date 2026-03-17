---
name: tool-construction
description: Dynamically building simple MCP servers or Python scripts to solve unique problems.
role: eng-tooling
triggers:
  - build tool
  - create mcp
  - make script
  - automate task
---

# tool-construction Skill

This skill guides the creation of NEW capabilities for the swarm.

## 1. Script vs MCP
- **Script**: One-off task (e.g., "Migrate CSV to JSON").
- **MCP Server**: Persistent tool needed by LLM (e.g., "Query internal Knowledge Base").

## 2. Building an MCP Server (Quick-Start)
Use the `@modelcontextprotocol/sdk`:
1.  Define Tools (Input Schema).
2.  Implement Logic.
3.  Connect to Stdio/SSE.

## 3. Tool Safety
- **Sandboxing**: Generated tools should not have root access.
- **Review**: A generated tool must be reviewed by `ops-security` (or human) before execution if it modifies files.

## 4. The "Toolsmith" Loop
1.  **Identify Pain**: "We keep grepping for X manually."
2.  **Spec Tool**: "Build a tool that finds X and formats as JSON."
3.  **Implement**: Write `tools/find_x.py`.
4.  **Register**: Add to `project_tools` in context configuration.
