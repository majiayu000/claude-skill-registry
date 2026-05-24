---
name: cargo-make-protocol
description: "Master Cargo Make build orchestration. Poka-yoke error-proofing, SLO enforcement (check <5s, test <30s, lint <60s), andon signals. Essential: always cargo make, never direct cargo."
allowed_tools: "Bash(cargo make:*)"
---

# Cargo Make Protocol (80/20 Edition)

## Golden Rule

```bash
ALWAYS: cargo make [target]
NEVER:  cargo [command]
```

Direct cargo bypasses timeouts, quality gates, andon signals.

## Quick Reference

### Fast Feedback (<20s)
```bash
cargo make check      # Compile (<5s)
cargo make test-unit  # Unit tests (<16s)
cargo make lint       # Clippy (<60s)
```

### Pre-Commit
```bash
cargo make pre-commit # fmt + lint + test (<2min)
```

### Full Validation
```bash
cargo make test       # All tests (<30s)
cargo make ci         # Full CI pipeline
cargo make slo-check  # Verify SLOs
```

## SLO Targets

| Target | SLO | Escalation |
|--------|-----|------------|
| check | <5s | 30s |
| test-unit | <16s | 150s |
| test | <30s | 120s |
| lint | <60s | - |
| pre-commit | <2min | - |

## Andon Signals

| Signal | Trigger | Action |
|--------|---------|--------|
| 🔴 RED | error[E...], FAILED | **STOP** - fix now |
| 🟡 YELLOW | warning:, clippy:: | Investigate |
| 🟢 GREEN | test result: ok | Continue |

## Three-Layer Validation

```bash
# Layer 1: Compile
cargo make check && cargo make lint

# Layer 2: Test
cargo make test

# Layer 3: Runtime (catches fake greens)
cargo make verify-cli
```

## Common Workflows

### Development Cycle
```bash
cargo make check      # After changes
cargo make pre-commit # Before commit
cargo make ci         # Before push
```

### Quality Audit
```bash
cargo make test-audit     # Mutation testing
cargo make detect-gaps    # Coverage gaps
cargo make audit-all      # Security
```

### Release
```bash
cargo make release-validate  # 8 FMEA gates
cargo make release           # Build + deploy
```

## Prohibited Patterns

```bash
# ❌ WRONG
cargo check
cargo test
cargo clippy

# ✅ CORRECT
cargo make check
cargo make test
cargo make lint
```

## Best Practices

1. **Always cargo make** - never direct cargo
2. **Receipt-based** - evidence not narrative
3. **Three-layer validation** - compile → test → runtime
4. **Respect andon signals** - RED = stop
5. **SLO enforcement** - timeouts prevent hangs

**Constitutional**: `cargo make [target] ONLY | Receipts replace review | Andon = stop-the-line`
