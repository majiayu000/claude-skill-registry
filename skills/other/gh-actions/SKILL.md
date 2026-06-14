---
name: gh-actions
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: "Use when creating GitHub Actions workflows, release automation, checksums, signing, or CI/CD."
practices:
- pragmatic-programmer
---
# Optimal GitHub Actions

Production-tested patterns + 2025-2026 best practices.

## Quick Start: Which Workflow?

| Need | Template | Reference |
|------|----------|-----------|
| CI on push/PR | `ci.yml` | [CI-CORE](references/CI-CORE.md) |
| Release on tag | `release.yml` | [RELEASE-BUILD](references/RELEASE-BUILD.md) |
| Nightly fuzz/bench | `fuzz.yml` | [TESTING](references/TESTING.md) |
| Dependency updates | `dependabot.yml` | [DEPENDABOT](references/DEPENDABOT.md) |

---

## Core Patterns (Every Workflow)

```yaml
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # false for releases

permissions:
  contents: read  # Minimal by default

jobs:
  build:
    timeout-minutes: 30  # Never use default 6h
```

---

## Language Quick Reference

| Language | Setup | Template |
|----------|-------|----------|
| **Rust** | `dtolnay/rust-toolchain@stable` | [TEMPLATE-RUST](references/TEMPLATE-RUST.md) |
| **Go** | `actions/setup-go@v6` | [TEMPLATE-GO](references/TEMPLATE-GO.md) |
| **TypeScript** | `oven-sh/setup-bun@v2` | [TEMPLATE-TS](references/TEMPLATE-TS.md) |
| **Bash** | — | [TEMPLATE-BASH](references/TEMPLATE-BASH.md) |
| **Python** | `astral-sh/setup-uv@v7` | [TEMPLATE-PYTHON](references/TEMPLATE-PYTHON.md) |

---

## Cross-Platform Matrix (Native ARM 2025+)

```yaml
strategy:
  fail-fast: false
  matrix:
    include:
      - os: ubuntu-latest        # Linux x64
        target: x86_64-unknown-linux-gnu
      - os: ubuntu-24.04-arm     # Linux ARM (native!)
        target: aarch64-unknown-linux-gnu
      - os: macos-14             # Apple Silicon (native!)
        target: aarch64-apple-darwin
      - os: macos-15-intel       # macOS x64
        target: x86_64-apple-darwin
      - os: windows-latest       # Windows x64
        target: x86_64-pc-windows-msvc
```

**Key insight:** Native ARM runners are 10x faster than QEMU emulation.

---

## Release Checklist

- [ ] Cross-platform build matrix
- [ ] Generate checksums (`sha256sum`)
- [ ] Sign artifacts (minisign/cosign)
- [ ] Create GitHub Release (`softprops/action-gh-release@v2`)
- [ ] Notify package managers (Homebrew/Scoop)
- [ ] Generate SBOM (syft)
- [ ] Attach SLSA provenance

**Patterns:** [RELEASE-BUILD](references/RELEASE-BUILD.md) | [RELEASE-EXTRAS](references/RELEASE-EXTRAS.md) | [SECURITY-SIGNING](references/SECURITY-SIGNING.md)

---

## Caching

| Language | Action | Notes |
|----------|--------|-------|
| Rust | `Swatinem/rust-cache@v2` | Auto-caches cargo + target |
| Go | `actions/setup-go@v6` | Built-in, enabled by default |
| Node/Bun | `actions/cache@v4` | Cache `node_modules` |

**Include arch in cache key for cross-platform:**
```yaml
key: ${{ runner.os }}-${{ runner.arch }}-${{ hashFiles('Cargo.lock') }}
```

---

## Security (2025 Best Practices)

| Practice | Example |
|----------|---------|
| Pin to SHA | `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` |
| OIDC auth | `permissions: { id-token: write }` + cloud provider action |
| Keyless signing | `sigstore/cosign-installer@v3` |
| SLSA Level 3 | `actions/attest-build-provenance@v2` |

**Full patterns:** [SECURITY-CORE](references/SECURITY-CORE.md) | [SECURITY-SIGNING](references/SECURITY-SIGNING.md)

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| `@main` for third-party actions | Pin to SHA |
| Default 6h timeout | Set explicit `timeout-minutes` |
| QEMU for ARM builds | Native ARM runners |
| Store secrets in workflow | Use `secrets.*` |
| Skip concurrency controls | Use `concurrency:` group |

---

## Reference Index

### By Topic
| Topic | Reference |
|-------|-----------|
| CI essentials (triggers, jobs, env) | [CI-CORE](references/CI-CORE.md) |
| CI advanced (matrix, caching, artifacts) | [CI-ADVANCED](references/CI-ADVANCED.md) |
| Release build workflows | [RELEASE-BUILD](references/RELEASE-BUILD.md) |
| Signing, versioning, install scripts | [RELEASE-EXTRAS](references/RELEASE-EXTRAS.md) |
| GoReleaser config | [GORELEASER](references/GORELEASER.md) |
| Security fundamentals | [SECURITY-CORE](references/SECURITY-CORE.md) |
| Signing and provenance | [SECURITY-SIGNING](references/SECURITY-SIGNING.md) |
| Coverage collection | [COVERAGE](references/COVERAGE.md) |
| Fuzzing, benchmarks, analysis | [TESTING](references/TESTING.md) |
| Dependabot configuration | [DEPENDABOT](references/DEPENDABOT.md) |
| Playwright browser tests | [BROWSER-TESTS](references/BROWSER-TESTS.md) |
| Docker/OCI with signing | [OCI-PATTERNS](references/OCI-PATTERNS.md) |
| Python wheels (maturin) | [PYTHON-WHEELS](references/PYTHON-WHEELS.md) |
| Database service containers | [SERVICES](references/SERVICES.md) |
| ACFS checksum notifications | [ACFS-PATTERNS](references/ACFS-PATTERNS.md) |

### By Language
| Language | Template |
|----------|----------|
| Rust | [TEMPLATE-RUST](references/TEMPLATE-RUST.md) |
| Go | [TEMPLATE-GO](references/TEMPLATE-GO.md) |
| TypeScript/Bun | [TEMPLATE-TS](references/TEMPLATE-TS.md) |
| Bash | [TEMPLATE-BASH](references/TEMPLATE-BASH.md) |
| Python/uv | [TEMPLATE-PYTHON](references/TEMPLATE-PYTHON.md) |

---

## Validation

```bash
actionlint .github/workflows/*.yml
gh workflow list && gh run list --workflow=ci.yml
```
