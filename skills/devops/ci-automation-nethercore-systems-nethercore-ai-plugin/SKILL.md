---
name: CI Automation
description: |
  This skill provides CI/CD automation for Nethercore ZX games. Use when the user asks about "CI", "CD", "GitHub Actions", "automation", "build pipeline", "release workflow", "continuous integration", or "quality gates".

  **Load references when:**
  - Full workflow templates needed → `references/workflow-templates.md`
  - Quality gate details → `references/quality-gates.md`
version: 1.0.0
---

# CI/CD Automation for Nethercore ZX

Automate building, testing, and releasing ZX games with GitHub Actions.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `nether build --release` | Compile WASM + pack ROM |
| `nether run --sync-test` | Verify determinism |
| `cargo clippy -- -D warnings` | Lint check |
| `cargo test` | Unit tests |

## Quality Gates (Run In Order)

| Gate | Command | Purpose |
|------|---------|---------|
| Format | `cargo fmt --check` | Code style |
| Lint | `cargo clippy -- -D warnings` | Static analysis |
| Test | `cargo test` | Logic correctness |
| Build | `nether build --release` | WASM compilation |
| Sync | `nether run --sync-test --frames 1000` | Determinism |

## Versioning

Use semantic versioning in `nether.toml`:

```toml
[game]
version = "1.2.3"
```

**Tag format**: `v1.2.3`

**Release process**:
1. Update version in `nether.toml`
2. Update `CHANGELOG.md`
3. Commit, tag, push

## Key Files

- `.github/workflows/build.yml` - Build + test on push/PR
- `.github/workflows/release.yml` - Tag-triggered releases
- `CHANGELOG.md` - Version history

See `references/workflow-templates.md` for complete YAML templates.
See `references/quality-gates.md` for detailed gate configuration.
