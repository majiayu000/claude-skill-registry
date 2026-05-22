---
name: review:architecture
description: Architecture-focused review covering boundaries, performance, scalability, and API contracts. Spawns the senior-review-specialist agent for architectural analysis.
---

# Architecture Code Review

Run an architecture-focused review using 4 architecture checklists via the senior-review-specialist agent.

## Instructions

Spawn the `senior-review-specialist` agent to perform this review.

## Checklists to Apply

Load and apply these review checklists:

- `commands/review/architecture.md` - Boundaries, dependencies, layering
- `commands/review/performance.md` - Algorithmic efficiency, N+1 queries, bottlenecks
- `commands/review/scalability.md` - Load handling, dataset growth, multi-tenancy
- `commands/review/api-contracts.md` - Stability, correctness, consumer usability

## Agent Instructions

The agent should:

1. **Get working tree changes**: Run `git diff` to see all changes
2. **Map the architecture**:
   - Identify architectural layers (presentation, service, domain, infra)
   - Identify dependency direction
   - Identify coupling points
3. **For each changed file**:
   - Read the full file content
   - Go through each diff hunk
   - Apply all 4 architecture checklists
   - Look for layer violations and circular dependencies
4. **Cross-reference related files**: Check import graphs, module boundaries
5. **Assess coupling impact**: How many modules are affected?

## Output Format

Generate an architecture review report with:

- **Critical Issues (BLOCKER)**: Circular dependencies, boundary violations
- **High Priority Issues**: God objects, coupling problems
- **Medium Priority Issues**: Missing abstractions, low cohesion
- **Architectural Map**: Layers, boundaries, dependency direction
- **Coupling Metrics**: Fan-in, fan-out, affected modules
- **File Summary**: Architecture issues per file
- **Overall Assessment**: Architecture health recommendation
