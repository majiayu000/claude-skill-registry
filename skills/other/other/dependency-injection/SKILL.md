---
name: dependency-injection
description: Pass dependencies through constructors or setters rather than instantiating them internally Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: high
  is-built-in: true
  session-guardian-id: builtin_dependency_injection
---

# Dependency Injection

Pass dependencies through constructors or setters rather than instantiating them internally. This makes dependencies explicit, enables testing with mocks, and allows easy configuration changes. Use DI containers for complex applications to manage object lifetimes and resolve dependencies automatically. Constructor injection is preferred for required dependencies.