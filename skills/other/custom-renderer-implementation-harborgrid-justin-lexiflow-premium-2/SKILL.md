---
name: custom-renderer-implementation
description: Architect bespoke React renderers for non-DOM environments using the `react-reconciler` package.
---

# Custom Renderer Implementation (React 18)

## Summary
Architect bespoke React renderers for non-DOM environments using the `react-reconciler` package.

## Key Capabilities
- Implement a full HostConfig interface for a custom target.
- Map fiber mutations to imperative host API calls.
- Manage persistent vs. transient host instance updates.

## PhD-Level Challenges
- Design a scheduling-aware host config for Frame-limited targets.
- Prove correctness of the mutation queue execution order.
- Implement concurrent mode support for a custom target.

## Acceptance Criteria
- Deploy a working custom renderer (e.g., to Canvas or Terminal).
- Demonstrate correct update propogation.
- Pass the standard React conformance test suite for renderers.
