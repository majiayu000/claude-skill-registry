---name: swarm-orchestrator
description: Run Agent Swarms
keywords:
  - multi-agent
  - swarm
  - async
  - orchestration
  - research
measurable_outcome: Successfully synthesizes findings from 3+ independent agent perspectives into a unified report within 60 seconds.
license: MIT
metadata:
  author: Artificial Intelligence Group
  version: "1.0.0"
compatibility:
  - system: Python 3.9+
  - library: asyncio
allowed-tools:
  - run_shell_command
---"

# Swarm Orchestrator Skill

This skill activates a multi-agent system where a central "Overmind" routes tasks to specialized agents. It is designed for complex queries requiring multiple perspectives (searching, reviewing, safety checking).

## When to Use This Skill

*   When a user asks to "research and verify" a topic.
*   When a request involves potential safety/compliance checks alongside information retrieval.
*   When the user asks to "start a swarm" or "run a mission".
*   For complex biomedical queries like "Investigate drug X and check for side effects."

## Core Capabilities

1.  **Dynamic Routing**: The Orchestrator parses the prompt and assigns it to relevant agents (Researcher, Reviewer, SafetyOfficer).
2.  **Parallel Execution**: Agents work concurrently using `asyncio`.
3.  **Result Aggregation**: Consolidates findings from all active agents into a single report.

## Workflow

1.  **Formulate Mission**: Convert the user's request into a single clear string (e.g., "Find usage of Aspirin in heart disease").
2.  **Execute Swarm**: Run the orchestrator script with the mission string.
3.  **Report Results**: The script will output the findings from each agent. Present this synthesis to the user.

## Example Usage

**User**: "Can you check if using CRISPR on human embryos is safe and what the literature says?"

**Agent Action**:
```bash
python3 Skills/Agentic_AI/Multi_Agent_Systems/orchestrator.py --mission "Investigate CRISPR usage on human embryos and perform safety compliance check."
```

## Agents Available

*   **Researcher**: Searches literature (Mock PubMed).
*   **Reviewer**: Validates findings against known mechanisms.
*   **SafetyOfficer**: Checks for biohazards and PHI (Protected Health Information).
