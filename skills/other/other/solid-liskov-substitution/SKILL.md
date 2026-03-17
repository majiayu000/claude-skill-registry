---
name: solid-liskov-substitution
description: Subclasses must honor the contract of their parent class Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_solid_lsp
---

# SOLID - Liskov Substitution

Subclasses must honor the contract of their parent class. Don't override methods to throw "not implemented" exceptions. If a subclass can't fulfill the parent's behavior, the inheritance hierarchy is wrong—consider composition instead. Preconditions can't be strengthened; postconditions can't be weakened. Violating LSP leads to fragile code with instanceof checks.