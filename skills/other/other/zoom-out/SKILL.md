---
name: zoom-out
description: Step up one layer of abstraction and surface a map of relevant modules and callers when the local view is too narrow. Trigger when the agent (or user) is unfamiliar with a code region and needs the surrounding architecture before committing to a change.
disable-model-invocation: true
---

Stop reading the local fragment. Climb one level of abstraction and produce a map: which modules surround this region, who calls into it, what it calls out to, and where its invariants live. Dispatch an Explore agent (`fd`-first discovery, then `git grep`/`ast-grep` for call-site enumeration) rather than reading individual files — the goal is structural orientation, not line-level detail.

Output is a compact module-and-caller map, not a narrative. Name the surrounding components, the inbound and outbound edges, and any obvious invariant boundaries (transactional scope, ownership, IO surfaces). Stop at one layer up unless the user asks for more — over-zoom dilutes the orientation.
