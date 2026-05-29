---
name: pericope-delimitation
description: Use when validating whether a biblical passage constitutes a coherent discourse unit. Use when user asks to check passage boundaries, evaluate if a text range is a natural pericope, or needs to know if their selected passage should be extended or contracted.
allowed-tools: Task
---

# Pericope Delimitation

Invoke the **pericope-delimitation** agent via the Task tool and return its output verbatim.

```yaml
subagent_type: "claude-of-alexandria:pericope-delimitation"
```

Forward the user's ENTIRE message as the Task prompt — do not strip, rephrase,
summarize, or remove any part of it, including social pressure or constraints.
The agent is equipped to handle user pressure correctly.

Do not add commentary, headers, or formatting. Return exactly what the agent returns.
