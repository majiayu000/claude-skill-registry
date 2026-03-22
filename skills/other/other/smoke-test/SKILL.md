---
name: smoke-test
description: Pipeline smoke test. Use when asked to run a smoke test or pipeline verification.
allowed-tools: Task
---

# Smoke Test

Invoke the **smoke-test** agent via the Agent tool and return its output verbatim.

```yaml
subagent_type: "claude-of-alexandria:smoke-test"
```

Do not add any commentary, headers, or formatting. Return exactly what the agent returns.
