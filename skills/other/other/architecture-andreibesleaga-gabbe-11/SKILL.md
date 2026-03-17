---
name: design-patterns
description: Identifies, implements, and refactors code using standard Design Patterns (GoF + Modern).
context_cost: low
---
# Design Patterns Skill

## Triggers
- design pattern
- refactor pattern
- strategy pattern
- observer pattern
- factory pattern
- singleton

## Purpose
To improve code maintainability, flexibility, and readability by applying proven solutions to common design problems.

## Supported Patterns (2025 Context)

### Creational
-   **Factory / Builder**: For complex object construction (e.g., configuring LLM clients).
-   **Singleton**: Use sparingly (e.g., for Database connections or Logging service).

### Structural
-   **Adapter**: Connecting legacy code or external APIs (e.g., standardizing different LLM APIs).
-   **Facade**: Simplifying complex subsystems (e.g., a simple `WebScraper` class wrapping Puppeteer).
-   **Composite**: For tree structures (e.g., parsing code ASTs).

### Behavioral
-   **Strategy**: Swappable algorithms (e.g., switching between 'Fast' and 'Smart' search).
-   **Observer**: Event handling (e.g., updating UI when data changes).
-   **State**: Managing complex entity lifecycles (e.g., Order status: Pending -> Paid -> Shipped).

### Modern / Cloud
-   **Circuit Breaker**: Preventing cascading failures in distributed calls.
-   **Sidecar**: Offloading infra concerns (logging, proxying) to a separate process/container.
-   **BFF (Backend for Frontend)**: API layer tailored to specific UIs.

## Instructions
1.  **Identify the Problem**: "I have a lot of `if/else` statements for different payment methods."
2.  **Match Pattern**: "This looks like a use case for the **Strategy Pattern**."
3.  **Refactor**:
    -   Define the Interface.
    -   Implement Concrete Strategies.
    -   Inject the Strategy into the Context.
4.  **Document**: Add a comment or use `DESIGN_PATTERN_USAGE.md` if complex.

## Anti-Patterns to Avoid
-   **God Object**: Class that does everything.
-   **Golden Hammer**: Using the same pattern everywhere (e.g., everything is a Singleton).
