---
name: devtools-secrets
description: >
  Knowledge and guardrails for the mise + fnox + infisical secrets toolchain.
  Use when the user asks to "configure secrets", "set up fnox", "infisical",
  "mise env", "secrets management", "environment variables for secrets",
  or mentions secret injection, secret providers, or env var hygiene.
---

# DevTools Secrets

Knowledge and guardrails for the **mise + fnox + infisical** secrets toolchain.

## Toolchain Validation

**IMPORTANT: Check tool availability before proceeding with any guidance.**

- mise: !`command -v mise >/dev/null 2>&1 && echo "INSTALLED ($(mise --version 2>/dev/null | head -1))" || echo "MISSING — install with: curl https://mise.run | sh"`
- fnox: !`command -v fnox >/dev/null 2>&1 && echo "INSTALLED ($(fnox --version 2>/dev/null | head -1))" || echo "MISSING — install with: mise use -g fnox"`
- infisical: !`command -v infisical >/dev/null 2>&1 && echo "INSTALLED ($(infisical --version 2>/dev/null | head -1))" || echo "MISSING — install with: mise use -g infisical"`

If any tool above shows **MISSING**, stop and help the user install it before
proceeding. Do not provide configuration guidance for tools that aren't
installed.

## Project Config State

- fnox.toml: !`test -f fnox.toml && echo "YES" || echo "NO (run: fnox init)"`
- .infisical.json: !`test -f .infisical.json && cat .infisical.json || echo "NO (run: infisical init)"`
- mise.toml env section: !`grep -A5 '^\[env\]' mise.toml 2>/dev/null || echo "No env section"`

## System/Global Config

- mise global config: !`test -f ~/.config/mise/config.toml && head -10 ~/.config/mise/config.toml || echo "No global mise config"`
- fnox global config: !`test -f ~/.config/fnox/config.toml && head -10 ~/.config/fnox/config.toml || echo "No global fnox config"`
- infisical logged in: !`infisical user get 2>/dev/null | head -3 || echo "Not logged in or not installed"`

## Tool Roles

| Tool | Role |
|------|------|
| **mise** | Task runner + env manager. Orchestrates dev tooling, runs tasks, manages env vars through plugins. |
| **fnox** | Unified secret interface. Abstracts over multiple secret backends (infisical, age, env files) with a single CLI. |
| **infisical** | Remote secrets backend. Stores, syncs, and injects secrets from a central server. |

These tools complement each other: infisical stores secrets remotely, fnox
provides a unified local interface to them, and mise orchestrates tasks that
consume secrets via fnox.

## Integration Chain

The typical flow:

1. **fnox.toml** defines infisical as a provider with project/environment config
2. **`fnox exec --`** resolves secrets from the provider and injects them as env vars
3. **mise tasks** can wrap `fnox exec` to run commands with secrets injected
4. Alternatively, **mise env plugins** can call fnox directly for auto-injection on `cd`

## Secrets Enforcement

This project enforces secrets hygiene via **always-on hooks** in
`.claude/settings.json` (not scoped to this skill):

- **`block-hardcoded-secrets.py`** — Blocks Edit/Write operations containing
  hardcoded API keys, tokens, passwords, or known secret prefixes (sk-, ghp_,
  AKIA, xox[bpras]-)
- **`block-bare-secret-exports.py`** — Blocks Bash commands that `export`
  secret-like env vars without wrapping in `fnox exec` or `infisical run`

These hooks are always active regardless of whether this skill is loaded.

## Configuration Patterns

Detailed configuration for each tool is in the reference files:

- @references/mise-integration.md — mise env plugins, tasks, fnox integration
- @references/fnox-configuration.md — fnox.toml structure, providers, profiles
- @references/infisical-patterns.md — infisical CLI, scanning, CI/CD

## Gotchas

- **Order matters**: fnox.toml must exist before `fnox exec` works. Run
  `fnox init` if missing.
- **Profile mismatches**: fnox profiles (dev/staging/prod) must match infisical
  environment slugs. A mismatch silently returns empty secrets.
- **`.infisical.json` is safe to commit** — it contains project IDs and
  workspace config, not secrets.
- **`fnox.toml` may contain sensitive paths** — review before committing if
  using age-encrypted file provider.
- **mise env plugins run on `cd`** — if a plugin calls fnox and fnox is
  misconfigured, you get errors on every directory change.
- **infisical auth expires** — `infisical login` tokens have a TTL. CI/CD
  should use `INFISICAL_TOKEN` (service token) instead.
- **Token path scope is explicit** — a service token scoped to `/` cannot
  access secrets in child paths like `/git_actions`. Each path requires its
  own token or use `--recursive` with the CLI directly.
