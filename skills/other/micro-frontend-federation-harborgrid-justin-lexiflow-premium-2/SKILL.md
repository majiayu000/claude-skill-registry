---
name: micro-frontend-federation
description: Orchestrate distributed React applications using Module Federation and shared context bridges.
---

# Micro-Frontend Federation (React 18)

## Summary
Orchestrate distributed React applications using Module Federation and shared context bridges.

## Key Capabilities
- Share React Context across federation boundaries.
- Manage version skew in shared dependencies at runtime.
- Isolate styling and event propagation between remote modules.

## PhD-Level Challenges
- Design a fault-tolerant loading strategy for failing remotes.
- Prove type-safety across dynamic module boundaries.
- Analyze memory overhead of duplicate dependency loading.

## Acceptance Criteria
- Deploy a host app with seamlessly integrated remotes.
- Demonstrate shared state synchronization.
- Document the dependency sharing policy.
