---
name: synthetic-event-system-internals
description: Leverage React's event delegation system for optimization and custom event behavior.
---

# Synthetic Event System Internals

## Summary
Leverage React's event delegation system for optimization and custom event behavior.

## Key Capabilities
- Trace event propagation through the React tree vs. DOM.
- Implement custom event plugins for non-standard gestures.
- Optimize high-frequency event listeners (scroll, resize).

## PhD-Level Challenges
- Debug issues arising from mixed React/native event listeners.
- Analyze the memory impact of the synthetic event pool (historical/modern).
- Simulate event re-targeting in portal subtrees.

## Acceptance Criteria
- Demonstrate correct event delegation behavior.
- Provide a custom event hook implementation.
- Document event propagation nuances in Portals.
