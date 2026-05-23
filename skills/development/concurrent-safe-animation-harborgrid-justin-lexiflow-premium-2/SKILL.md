---
name: concurrent-safe-animation
description: Implement animation systems resilient to concurrent rendering and interrupted updates.
---

# Concurrent-Safe Animation (React 18)

## Summary

Implement animation systems resilient to concurrent rendering and interrupted updates.

## Key Capabilities

- Prevent animation glitches caused by re-entrancy.
- Coordinate animation timelines with render commits.
- Maintain stable layout measurements under transitions.

## PhD-Level Challenges

- Prove animation continuity under interrupted renders.
- Model animation schedules as concurrent state machines.
- Evaluate trade-offs between animation fidelity and throughput.

## Acceptance Criteria

- Demonstrate glitch-free animations under rapid updates.
- Provide tests for interrupted animation scenarios.
- Document synchronization strategy with rendering.

