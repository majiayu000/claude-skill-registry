---
name: bb80-specification-closure
description: "Verify 100% specification closure before Big Bang 80/20 single-pass construction."
allowed_tools: "Read, Glob, Grep"
---

# Big Bang 80/20: Specification Closure

## Core Concept

Specification closure is the **gate before EPIC 9 fan-out**.

No implementation begins without closure verification.

## Closure Checklist

A specification is **closed** when:

- [ ] All inputs characterized (domain, constraints, edge cases)
- [ ] All outputs specified (behavior, invariants, success criteria)
- [ ] All errors enumerated (what happens when things fail)
- [ ] All ambiguities resolved (no TBD, TODO, undefined)
- [ ] All user stories have acceptance scenarios
- [ ] SHACL validation passes

## Quick Validation

```bash
# Check for incomplete markers
grep -r "TBD\|TODO\|FIXME\|undefined" .specify/

# Validate SHACL conformance
cargo make speckit-validate
```

## Reference
See CLAUDE.md sections:
- Three Paradigms (Big Bang 80/20)
- When to Use EPIC 9
- Agents: bb80-specification-validator
