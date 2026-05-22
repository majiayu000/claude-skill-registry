---
name: receive-feedback
description: Process external code review feedback with technical rigor. Use when receiving feedback from another LLM, human reviewer, or CI tool. Verifies claims before implementing, tracks disposition.
---

# Receive Feedback

## Overview

Process code review feedback with verification-first discipline.
No performative agreement. Technical correctness over social comfort.

## Quick Reference

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   VERIFY    │ ──▶ │   EVALUATE   │ ──▶ │   EXECUTE   │
│ (tool-based)│     │ (decision    │     │ (implement/ │
│             │     │  matrix)     │     │  reject/    │
└─────────────┘     └──────────────┘     │  defer)     │
                                         └─────────────┘
```

## Core Principle

**Verify before implementing. Ask before assuming.**

## When To Use

- Receiving code review from another LLM session
- Processing PR review comments
- Evaluating CI/linter feedback
- Handling suggestions from pair programming

## Workflow

For each feedback item:

1. **Verify** - Use tools to check if feedback is technically valid
2. **Evaluate** - Apply decision matrix to determine action
3. **Execute** - Implement, reject with evidence, or defer

## Files

- `VERIFICATION.md` - Tool-based verification workflow
- `EVALUATION.md` - Decision matrix and rules
- `RESPONSE.md` - Structured output format
- `references/skill-integration.md` - Using with code-review skills
