---
name: describe-laws-and-style
description: Distinction between laws (invariants) and style (conventions). Load when determining if a constraint is a law or style.
user-invocable: false
---

## Laws vs Style

**Laws** (`.ushabti/laws.md`):
- Non-negotiable invariants that must hold across all Phases, implementations, and refactors
- Examples: architectural boundaries, security constraints, correctness guarantees
- Laws are absolute — any violation fails a Phase
- Only Lawgiver defines or modifies laws

**Style** (`.ushabti/style.md`):
- Conventions that govern *how* the system is built
- Examples: directory layout, naming conventions, testing strategy, error handling
- Style may evolve over time; laws should not
- Only Artisan defines or modifies style
- Style must never contradict laws
