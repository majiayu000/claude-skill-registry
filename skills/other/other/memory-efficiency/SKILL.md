---
name: memory-efficiency
description: Avoid creating unnecessary intermediate objects in hot paths Use when optimizing code performance. Performance category skill.
metadata:
  category: Performance
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_memory_efficiency
---

# Memory Efficiency

Avoid creating unnecessary intermediate objects in hot paths. Release references to large objects when done. Use streams for processing large files instead of loading entirely into memory. Watch for closure memory leaks (closures holding references to large scopes). In long-running processes, ensure event listeners and subscriptions are properly cleaned up.