---
name: snapshot-testing
description: "Snapshots are useful for detecting unintended UI changes but shouldn't be the only testing strategy Use when writing and organizing tests. Testing category skill."
metadata:
  category: Testing
  priority: low
  is-built-in: true
  session-guardian-id: builtin_snapshot_testing
---

# Snapshot Testing

Snapshots are useful for detecting unintended UI changes but shouldn't be the only testing strategy. Review snapshot changes carefully—don't blindly update them. Keep snapshots focused (specific components, not entire pages). Use inline snapshots for small outputs. Combine snapshots with behavioral tests that assert specific functionality. Large, frequently-changing snapshots lose value.