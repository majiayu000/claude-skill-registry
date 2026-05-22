---
name: black-box-architecture
description: Apply Eskil Steenberg's black box architecture principles to build modular, maintainable software. Automatically refactors code into replaceable components, designs system architectures with clean boundaries, and debugs with modular isolation.
---

# Black Box Architecture Skill

This skill teaches Claude to apply Eskil Steenberg's battle-tested black box architecture principles for building modular, maintainable software systems.

## Philosophy

"It's faster to write 5 lines of code today than to write 1 line today and then have to edit it in the future." — Eskil Steenberg

Optimize for:
- **Human cognitive load** over algorithmic efficiency
- **Long-term maintainability** over short-term cleverness
- **Team scalability** (one person per module)
- **Constant developer velocity** regardless of project size

## Core Principles

1. **Primitive-First Design** - Identify core data types that flow through your system
2. **Black Box Boundaries** - Modules communicate only through documented interfaces
3. **Replaceable Components** - Any module can be rewritten using only its interface
4. **Single Responsibility** - One module = one person can own it
5. **Wrap Dependencies** - Never depend directly on code you don't control

## Variants

This skill has three specialized variants that are automatically selected based on your request:

### Refactor Variant
**When to use:** Code refactoring, breaking apart monoliths, creating module boundaries

**Triggers:**
- "Refactor [code/class/module]"
- "Break apart this monolith"
- "Create black box modules"
- "Analyze [component] and suggest modular refactoring"

**File:** `refactor.md`

### Plan Variant
**When to use:** Strategic architecture planning, designing new systems

**Triggers:**
- "Design architecture for [system]"
- "Plan the module structure"
- "How should I architect [feature]"
- "Design a [type] system"

**File:** `plan.md`

### Debug Variant
**When to use:** Systematic debugging, testing strategies, integration issues

**Triggers:**
- "Debug [issue]"
- "Fix this bug"
- "Why is [component] failing"
- "Test strategy for [feature]"

**File:** `debug.md`

## Output Format

All variants follow a structured 4-phase protocol and produce consistent output:

```markdown
## 🔍 Current Architecture
[Primitives, modules, coupling issues, violations]

## 🎯 Proposed Black Box Design
[Module designs with interfaces]

## 📝 Implementation Steps
[Specific, actionable steps]

## ⚠️ Risks & Mitigation
[What could go wrong + how to prevent]

## ✅ Quality Gates
[Validation checklist]
```

## Supported Languages

- Python
- TypeScript/JavaScript
- Go
- Rust
- C
- PHP
- Java

## Learn More

Based on Eskil Steenberg's lecture: [Architecting LARGE Software Projects](https://www.youtube.com/watch?v=sSpULGNHyoI)
