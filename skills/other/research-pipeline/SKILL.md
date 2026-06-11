---
name: research-pipeline
description: |
  Formal 5-phase research pipeline with artifact saving and source quality gates:
  SCOPE, GATHER, SYNTHESIZE, VALIDATE, DELIVER. Parallel research agents
  mandatory (min 3). Saves findings to research/{topic}/ for future reference.
  Use for "research pipeline", "formal research", "research with artifacts".
user-invocable: true
argument-hint: "<research topic>"
agent: research-coordinator-engineer
context: fork
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Agent
  - Write
routing:
  triggers:
    - "research-pipeline"
    - "research"
    - "formal research"
    - "research with artifacts"
    - "systematic investigation"
    - "research report"
    - "gather evidence"
  not_for: "a quick one-off web search or chat-style lookup — that is deep-research. Pick this when the user wants a sourced report saved as an artifact (SCOPE-to-DELIVER), even when phrased as 'dig into X and give me a sourced report'."
  category: research
  pairs_with:
    - kb
    - topic-brainstormer
---

# Research Pipeline

Thin wrapper preserving slash-command access. Load the full pipeline definition:

```
Read skills/workflow/references/research-pipeline.md
```

Then follow all phases and gates defined there.
