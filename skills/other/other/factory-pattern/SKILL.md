---
name: factory-pattern
description: Use factories when object creation is complex, involves choosing between implementations, or you ... Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_factory_pattern
---

# Factory Pattern

Use factories when object creation is complex, involves choosing between implementations, or you want to hide implementation details. Factory functions return objects implementing an interface without exposing concrete classes. This enables easier testing (factory returns mocks) and flexibility (change implementation without changing consumers). Prefer simple factory functions over complex abstract factory hierarchies.