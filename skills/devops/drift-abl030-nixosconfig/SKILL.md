---
name: drift
description: Detect configuration drift using hash-based verification
---

# Configuration Drift Detection

Verify refactors produce no unintended changes by comparing derivation hashes.

## Quick Commands

```bash
# Compare all hosts against baseline (shows nix-diff for changes)
./scripts/hash-compare.sh

# Run the full quality gate including drift detection (slow)
check --drift

# Quick summary without detailed diffs
./scripts/hash-compare.sh --summary

# Check specific host
./scripts/hash-compare.sh framework

# Update baselines after intentional changes
./scripts/hash-capture.sh
```

## How It Works

NixOS's deterministic builds mean identical `system.build.toplevel` hashes guarantee identical systems. No need for complex test logic.

- **MATCH**: Hash unchanged - pure refactor, no functional changes
- **DRIFT**: Hash differs - configuration changed, nix-diff shows what

## Typical Workflow

### Before Refactoring
```bash
# Ensure baselines are current
./scripts/hash-compare.sh --summary
# Should show: Matched: 15, Drifted: 0
```

### During Refactoring
```bash
# Check frequently
./scripts/hash-compare.sh --summary
# DRIFT is expected if you're changing configs
```

### After Refactoring
```bash
# Full comparison with diffs
./scripts/hash-compare.sh

# If changes are intentional, update baselines
./scripts/hash-capture.sh
```

## Key Features

- Processes ALL hosts - never bails on first error
- nix-diff integration shows exact root cause of changes
- Baselines auto-update in nightly CI

## Files

| File | Purpose |
|------|---------|
| `scripts/hash-capture.sh` | Capture current hashes |
| `scripts/hash-compare.sh` | Compare against baselines |
| `hashes/*.txt` | Stored baseline hashes |
| `docs/hash-verification.md` | Full documentation |
