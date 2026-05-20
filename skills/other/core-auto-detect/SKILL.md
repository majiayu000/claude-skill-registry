---
name: core-auto-detect
description: Automatic environment detection and skill activation based on context
category: Session Knowledge
---

# Skill: core-auto-detect

## What I do

I detect project environments by scanning root-level files and recommend appropriate skills to load, enabling automatic domain expertise activation without explicit configuration.

## When to use me

- Starting a new development session in an unfamiliar project
- Automating skill selection in CI/CD or batch workflows
- Reducing manual skill specification overhead

## Core principles

1. **File-presence detection** — Check root directory only (no recursive scanning)
2. **Skill mapping** — Each environment maps to curated recommended skills
3. **Non-invasive** — Read-only, offline, millisecond completion
4. **Composable** — Multiple detections fire simultaneously

## Detection rules & skill recommendations

### Go Projects
**Detection:** `go.mod` exists

**Recommended skills:** `golang`, `ginkgo-gomega`, `clean-code`

### Node.js / JavaScript Projects
**Detection:** `package.json` exists

**Recommended skills:** `javascript`, `jest`, `clean-code`

### Ruby Projects
**Detection:** `Gemfile` exists

**Recommended skills:** `ruby`, `rspec-testing`, `clean-code`

### Python Projects
**Detection:** `pyproject.toml` or `setup.py` exists

**Recommended skills:** `python`, `clean-code`

### Embedded / Microcontroller Projects
**Detection:** `platformio.ini` exists

**Recommended skills:** `cpp`, `platformio`, `embedded-testing`

### Rust Projects
**Detection:** `Cargo.toml` exists

**Recommended skills:** `rust`, `clean-code`

### Nix / NixOS Projects
**Detection:** `flake.nix` or `shell.nix` exists

**Recommended skills:** `nix`, `devops`

### CI/CD / GitHub Actions
**Detection:** `.github/workflows/` directory exists

**Recommended skills:** `github-expert`, `devops`, `automation`

### Build Automation
**Detection:** `Makefile` exists

**Recommended skills:** `automation`, `scripter`

## Patterns & examples

**Single-language:** `go.mod` → golang, ginkgo-gomega, clean-code

**Polyglot with CI/CD:** `go.mod` + `package.json` + `.github/workflows/` → golang, ginkgo-gomega, javascript, jest, github-expert, devops, automation, clean-code

**Embedded with build:** `platformio.ini` + `Makefile` → cpp, platformio, embedded-testing, automation, scripter

## Anti-patterns to avoid

- ❌ **Recursive scanning** — Check root directory only
- ❌ **Network calls** — Detection must be instant and offline
- ❌ **Recommending for non-existent files** — Only recommend if file is confirmed present
- ❌ **Over-recommending** — Suggest 2-4 core skills per environment
- ❌ **Ignoring skill composition** — Include `clean-code` in every recommendation


## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Agent-Guidance/Core Auto Detect.md`

## Related skills

- `clean-code` — Applies across all detected environments
- `automation` — Complements build system detection
- `devops` — Complements CI/CD detection
- `critical-thinking` — For evaluating when to trust auto-detection vs manual selection
