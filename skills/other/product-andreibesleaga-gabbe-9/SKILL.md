---
name: systems-thinking
description: Analyze complex systems, feedback loops, and leverage points. Avoid linear thinking for complex problems.
triggers: [systems thinking, causal loop, feedback loop, leverage point, root cause, system map, holism, iceberg model]
context_cost: medium
---

# Systems Thinking Skill

## Goal
To understand the system as a whole, specifically focusing on relationships, feedback loops, and delays, rather than looking at isolated parts. Use this when solving stubborn, recurring problems or designing robust architectures.

## Steps

1.  **The Iceberg Model Analysis**
    *   **Events (React):** What just happened? (The bug/incident)
    *   **Patterns (Anticipate):** What trends have been happening over time?
    *   **Structures (Design):** What influenced the patterns? (Architecture, Org chart, Incentives)
    *   **Mental Models (Transform):** What assumptions/beliefs keep the system in place?

2.  **Causal Loop Diagramming (CLD)**
    *   Identify variables (e.g., "Code Quality", "Velocity", "Tech Debt").
    *   Map relationships (S = Same direction, O = Opposite direction).
    *   Identify Loops:
        *   **Reinforcing (R):** Exponential growth/collapse (Virtuous/Vicious cycles).
        *   **Balancing (B):** Goal-seeking/Stabilizing.
    *   *Output:* Mermaid diagram or text-based CLD.

3.  **Identify Leverage Points**
    *   Where is the intervention point with the highest impact?
    *   Examples: Changing a buffer size (Low leverage) vs Changing the goal of the system (High leverage).

4.  **Archetype Matching**
    *   Does this match a known system trap?
    *   *Examples:* "Fixes that Fail", "Shifting the Burden", "Tragedy of the Commons", "Drifting Goals".

## Output Format
A strategic analysis document at `docs/strategic/SYSTEM_ANALYSIS.md` containing the Iceberg analyis and Causal Loop Diagrams.

## Constraints
*   Look for circular causality, not linear (A causes B, but B also influences A).
*   Watch out for *delays* in the system—they cause oscillation.
