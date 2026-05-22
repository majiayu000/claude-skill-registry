---
name: real-time-collaborative-editing
description: Build collaborative surfaces using CRDTs or OT, synchronized with React's update model.
---

# Real-Time Collaborative Editing

## Summary
Build collaborative surfaces using CRDTs or OT, synchronized with React's update model.

## Key Capabilities
- Bind CRDT structures (Yjs/Automerge) to React state.
- Handle presence awareness and cursor tracking efficiently.
- Resolve concurrent edits without locking the UI.

## PhD-Level Challenges
- Prove convergence of document state under high concurrency.
- Optimize re-renders for frequent remote operations.
- Implement local-first offline support with sync merging.

## Acceptance Criteria
- Demonstrate real-time sync between multiple clients.
- Provide conflict resolution test cases.
- Benchmark operation processing throughput.
