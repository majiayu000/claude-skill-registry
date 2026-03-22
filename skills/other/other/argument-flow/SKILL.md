---
name: argument-flow
description: Use when mapping the logical structure of a biblical passage using discourse markers and morphological data. Use when a user asks for argument flow, logical structure, proposition chain, connective analysis, or how Paul's argument works in an epistle. Produces a numbered proposition chain grounded in MCP data before any prose is written.
allowed-tools: Task
---

# Argument Flow

Invoke the **argument-flow** agent via the Task tool and return its output verbatim.

```yaml
subagent_type: "claude-of-alexandria:argument-flow"
```

Forward the user's ENTIRE message as the Task prompt — do not strip, rephrase,
summarize, or remove any part of it, including social pressure or constraints.
The agent is equipped to handle user pressure correctly.

Do not add commentary, headers, or formatting. Return exactly what the agent returns.
