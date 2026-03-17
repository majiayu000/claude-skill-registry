---
name: multi-agent-orch
description: Plans and orchestrates multi-agent swarms, defining roles, topologies, and handoffs.
context_cost: medium
---
# Multi-Agent Orchestration Skill

## Triggers
- orchestrate
- swarm
- delegation
- multi-agent
- agent-team

## Purpose
To design and manage the execution of tasks across multiple specialized agents. This skill helps identify necessary roles, select the appropriate communication topology (hierarchical, sequential, mesh), and define clear handoff protocols.

## Instructions
When the user asks to "orchestrate a swarm" or "design a multi-agent system":

1.  **Analyze the Goal**: Break down the high-level objective into distinct sub-problems.
2.  **Identify Roles**: Determine the specific agent personas needed (e.g., `Researcher`, `Writer`, `Reviewer`, `Coder`).
    -   Use `AGENT_PROFILE_TEMPLATE.md` to define each role if needed.
3.  **Select Topology**: Choose the best interaction pattern:
    -   **Sequential**: A -> B -> C (Linear workflows)
    -   **Hierarchical**: Manager -> [Worker A, Worker B] (Complex tasks needing coordination)
    -   **Mesh**: Agents communicate peer-to-peer (Collaborative problem solving)
    -   **Star**: Central Hub <-> Agents (Centralized data processing)
4.  **Define Handoffs**: Specify *exactly* what data each agent passes to the next.
    -   Format: JSON, Markdown, or structured text.
    -   Validation: Ensure the receiving agent has the context to understand the input.
5.  **Output the Plan**: Produce a `SWARM_ARCHITECTURE_TEMPLATE.md` filled with the design.

## Best Practices
-   **Single Responsibility**: Each agent should have one clear job.
-   **Clear Contracts**: Define strict input/output schemas for handoffs.
-   **Error Handling**: Who handles failure? (Usually the Orchestrator or Manager).
-   **Human-in-the-Loop**: Designate checkpoints where human review is required.
