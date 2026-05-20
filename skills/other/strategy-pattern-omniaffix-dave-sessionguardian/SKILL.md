---
name: strategy-pattern
description: Use the Strategy pattern when you have multiple algorithms for the same task and want to select o... Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_strategy_pattern
---

# Strategy Pattern

Use the Strategy pattern when you have multiple algorithms for the same task and want to select one at runtime. Instead of complex if/else chains, define a common interface and implement it with different strategies. This enables adding new behaviors without modifying existing code. Common uses: payment processors, shipping calculators, validation rules.