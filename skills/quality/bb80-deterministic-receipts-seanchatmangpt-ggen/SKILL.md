---
name: bb80-deterministic-receipts
description: "Replace human review with reproducible evidence. Always provide deterministic receipts, never narratives."
allowed_tools: "Bash(cargo make:*)"
---

# Big Bang 80/20: Deterministic Receipts

## Core Concept

**Deterministic Receipts** replace human review with reproducible evidence.

Never say "code looks good". Instead provide receipts.

## The Pattern

**❌ BAD** (Narrative):
```
"I reviewed the code. It looks good. Performance should be fine."
```

**✅ GOOD** (Receipts):
```
[Receipt] cargo make check: ✓ 0 errors, 0 warnings
[Receipt] cargo make lint: ✓ 0 clippy violations
[Receipt] cargo make test: ✓ 347/347 tests passed in 28.3s
[Receipt] SLO compliance: ✓ test <30s (target met)
```

## Essential Receipts

```bash
cargo make check      # [Receipt] Compilation status
cargo make test       # [Receipt] Test pass/fail counts
cargo make lint       # [Receipt] Clippy warnings
cargo make pre-commit # [Receipt] Quality gate status
```

## Reference
See CLAUDE.md sections:
- Three Paradigms (Deterministic Receipts)
- Remember (Receipts Over Narratives)
- Development Workflow (Commit with Evidence)
