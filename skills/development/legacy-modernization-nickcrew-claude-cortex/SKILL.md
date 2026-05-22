---
name: legacy-modernization
description: Modernize legacy systems using proven migration patterns like strangler fig, feature flags, and incremental refactoring. Use when planning system migrations, modernizing monoliths, or managing technical debt.
---

# Legacy Modernization

Expert guidance for safe, incremental modernization of legacy systems, frameworks, and dependencies using proven migration patterns and risk mitigation strategies.

## When to Use This Skill

- Planning framework migrations (jQuery to React, Java 8 to 17, Python 2 to 3)
- Decomposing monoliths into microservices or modular architectures
- Modernizing databases (stored procedures to ORMs, schema migrations)
- Reducing technical debt with a phased, low-risk approach
- Updating outdated dependencies with backward compatibility concerns
- Establishing test coverage for untested legacy code before refactoring
- Designing rollback procedures for migration phases
- Implementing feature flags for gradual rollout of modernized components

## Quick Reference

| Task | Load reference |
| --- | --- |
| Strangler fig, feature flags, migration checklists, rollback procedures | `skills/legacy-modernization/references/modernization-patterns.md` |

## Workflow

### 1. Assessment

Inventory legacy components, risks, and dependencies before changing anything.

- Map the dependency graph and identify high-risk areas
- Define modernization goals and phased milestones
- Establish success metrics (test coverage, performance, defect rate)
- Prioritize based on business value and risk

### 2. Safety Net Setup

Establish guardrails before any migration work begins.

- Add characterization tests for existing behavior
- Set up feature flags for gradual rollout
- Create compatibility layers and adapter interfaces
- Document current behavior and integration points

### 3. Incremental Execution

Apply the strangler fig pattern: replace components one at a time.

- Route traffic gradually to new implementations
- Maintain backward compatibility at every step
- Run old and new paths in parallel where possible
- Monitor for regressions continuously

### 4. Stabilization

Validate the migration and retire legacy paths.

- Run full regression suites against new implementations
- Monitor adoption metrics and error rates
- Deprecate and remove legacy code paths
- Document the new architecture and migration decisions

## Common Mistakes

- Attempting big-bang rewrites instead of incremental migration
- Refactoring without tests covering existing behavior
- Removing backward compatibility before all consumers migrate
- Skipping rollback planning for each migration phase
- Ignoring data migration complexity and state synchronization
- Not involving stakeholders in deprecation timelines
