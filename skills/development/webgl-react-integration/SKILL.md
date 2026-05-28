---
name: webgl-react-integration
description: Manage WebGL contexts and 3D scenes declaratively using React reconciliation.
---

# WebGL and React Integration

## Summary
Manage WebGL contexts and 3D scenes declaratively using React reconciliation.

## Key Capabilities
- Map React props to WebGL uniform updates.
- Manage canvas resize and context loss events.
- Integrate DOM overlays with 3D scene coordinates.

## PhD-Level Challenges
- Bridge the imperative render loop with React's scheduler.
- Optimize object creation/destruction for garbage collection.
- Implement raycasting for interaction events.

## Acceptance Criteria
- Render a 3D scene driven by React state.
- Demonstrate performant frame updates (60fps).
- Implement mouse interaction with 3D objects.
