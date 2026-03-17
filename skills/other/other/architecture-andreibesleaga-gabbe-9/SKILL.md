---
name: arch-patterns
description: Recommends and analyzes system architecture patterns (Microservices, EDA, Serverless, etc.) based on requirements.
context_cost: medium
---
# Architecture Patterns Skill

## Triggers
- architecture
- system design
- scalability
- microservices
- event-driven
- serverless

## Purpose
To help the user or agent select the most appropriate system architecture based on improved Non-Functional Requirements (NFRs) like scalability, cost, maintainability, and latency.

## Instructions
When designing a system or component:

1.  **Analyze NFRs**: Identify the key constraints.
    -   *High Scalability?* -> Consider Microservices or Space-Based.
    -   *Complex Domain?* -> Consider Domain-Driven Design (DDD) with Modular Monolith.
    -   *Real-time Data?* -> Consider Event-Driven Architecture (EDA).
    -   *variable Workloads?* -> Consider Serverless.

2.  **Evaluate Patterns**:
    -   **Layered (N-Tier)**: Standard for simple web apps. separation of concerns.
    -   **Modular Monolith**: Best starting point for most startups. High cohesion, low deployment complexity.
    -   **Microservices**: For large teams and distinct scaling needs. High operational complexity.
    -   **Event-Driven (EDA)**: For decoupled, reactive systems.
    -   **Space-Based**: For extreme concurrency (in-memory data grids).
    -   **CQRS**: For separate read/write scaling profiles.

3.  **Recommend**:
    -   Propose 1-2 patterns.
    -   Justify with "Pros vs Cons" relative to the specific project.
    -   Use `ARCH_DECISION_FRAMEWORK.md` to document the choice.

## Best Practices
-   **Start Simple**: Modular Monolith is often the best default.
-   **Defer Complexity**: Don't use Microservices until you have a specific problem they solve.
-   **Evolutionary Arch**: Design for change. Use "Fitness Functions" to measure architectural drift.
