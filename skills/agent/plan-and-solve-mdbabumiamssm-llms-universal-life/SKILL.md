---name: plan-and-solve-agent
description: Breaks down complex queries into a step-by-step plan before execution, improving performance on multi-hop reasoning tasks.
license: MIT
metadata:
  author: AI Group
  version: "1.0.0"
compatibility:
  - system: Python 3.10+
allowed-tools:
  - run_shell_command
  - read_file

keywords:
  - plan-and-solve
  - automation
  - biomedical
measurable_outcome: execute task with >95% success rate.
---"

# Plan-and-Solve Agent

The **Plan-and-Solve Agent** separates high-level planning from low-level execution. It is ideal for complex scientific inquiries that require multiple distinct steps (e.g., "Find targets for disease X, then design drugs, then check safety").

## When to Use This Skill

*   When a user query is too complex for a single "ReAct" loop.
*   When you need to visualize the reasoning process *before* committing to execution.
*   To orchestrate multiple specialized sub-agents.

## Core Capabilities

1.  **Decomposition**: Splits a goal into linear or parallel sub-tasks.
2.  **Execution**: runs each step sequentially (mocked in this version).
3.  **Reporting**: Summarizes the outputs of all steps.

## Workflow

1.  **Input**: A complex natural language query.
2.  **Plan**: The agent generates a list of `PlanNode` objects.
3.  **Execute**: The agent iterates through nodes, executing them (simulation).

## Example Usage

**User**: "Investigate the impact of variant X on drug response."

**Agent Action**:
```bash
python3 Skills/Agentic_AI/Agent_Architectures/Plan_and_Solve/plan_and_solve.py \
    --query "Investigate the impact of variant X on drug response."
```

```
