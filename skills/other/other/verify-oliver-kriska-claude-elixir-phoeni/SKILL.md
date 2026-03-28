---
name: phx:verify
description: Full verification loop for Elixir/Phoenix changes. Use after completing any code implementation to catch issues before committing. Run before creating PRs, after fixing bugs, or whenever you want to confirm compile, format, and tests all pass together.
effort: low
---

# Verification Loop

Project-aware verification for Elixir/Phoenix. Reads `mix.exs` and `.check.exs` to discover tools, test commands, and custom aliases before running anything.

## Iron Laws

1. **Discover before running** — Read `mix.exs` first; never run `mix credo` if credo isn't a dependency
2. **Prefer ex_check** — If `:ex_check` + `.check.exs` exists, `mix check` replaces individual steps
3. **Prefer project aliases** — If `mix ci` or composite alias exists, use it over individual steps
4. **Run in order** — Later steps assume earlier ones pass
5. **Ask before E2E tests** — Unit tests run automatically; E2E/integration tests need user confirmation
6. **NEVER report success without showing actual command output** — "should work" is not verification

## Step 0: Project Discovery (ALWAYS FIRST)

Read `mix.exs` — extract `deps/0`, `aliases/0`, and `cli/0` (for `preferred_envs`). Also check for `.check.exs`. See `${CLAUDE_SKILL_DIR}/references/project-discovery.md` for full patterns.

**Discover tools** (deps): `:credo`, `:dialyxir`, `:sobelow`, `:ex_check`, `:excoveralls`, `:boundary`

**Discover test commands** (aliases + deps):

- Unit: `mix test` (always), or custom alias like `mix test.with_coverage`
- E2E: `mix playwright.test`, `mix cypress.run`, or similar (check `preferred_envs` for `MIX_ENV`)
- Fast E2E: `mix playwright.run` (skips setup — for re-runs)

**Discover composite runner**: If `.check.exs` exists, read it — `mix check` may handle compile, format, credo, test, dialyzer, sobelow, and more.

Report discovery:

```
Project tools: compile ✓ | format ✓ | credo ✓ | dialyzer ✓ | sobelow ✓ | ex_check ✓
Test commands: mix test (unit) | mix playwright.test (E2E, MIX_ENV=int_test)
Composite runner: mix check (.check.exs covers: compiler, formatter, credo, dialyzer, sobelow, tests)
Strategy: Running `mix check` then asking about E2E
```

## Verification Sequence

**CRITICAL**: Before using ANY discovered alias or composite command, verify it works:

1. Check the dependency is in `mix.lock` (not just `mix.exs`) — deps may not be fetched
2. Run the command — if it fails with "command not found" or dependency error, fall back to individual steps
3. Log the fallback: "mix check failed (ex_check not installed?), falling back to individual steps"

**If `ex_check` installed + `.check.exs` exists**: Try `mix check`. If it fails, fall back to individual steps.

**If composite alias found** (e.g., `mix ci`, `mix precommit`): Try it. If it fails, fall back to individual steps.

**Otherwise** (or after fallback): Run individual steps, skipping unavailable tools.

### Step 1: Compile

`mix compile --warnings-as-errors` — always

### Step 2: Format

`mix format --check-formatted` — always (auto-fix with `mix format` if fails)

### Step 3: Credo

`mix credo --strict` — if `:credo` in deps, else skip

### Step 4: Test

`mix test --trace` — use project test alias if available

### Step 5: Dialyzer

`mix dialyzer` — if `:dialyxir` in deps, pre-PR only

### Step 6: Sobelow

`mix sobelow --config` — if `:sobelow` in deps

Skip unavailable tools with: "Credo: ⏭ Not installed"

### Step 7: Additional Test Offer

After core verification passes, check if project has additional test commands (E2E, integration, coverage). **Ask the user**:

```
Core verification passed. Additional test commands available:
1. mix playwright.test (E2E, MIX_ENV=int_test) — ~5min
2. mix test.with_coverage (unit + coverage report)
Run any of these? [1/2/both/skip]
```

Respect `preferred_envs` / `cli/0` for correct `MIX_ENV` on each command.

## Quick Reference

| Step | Command | Condition |
|------|---------|-----------|
| Discovery | Read `mix.exs` + `.check.exs` | Always first |
| Composite | `mix check` | If `:ex_check` installed |
| Compile | `mix compile --warnings-as-errors` | Always |
| Format | `mix format --check-formatted` | Always |
| Credo | `mix credo --strict` | `:credo` in deps |
| Test | `mix test --trace` | Always (use alias if exists) |
| Dialyzer | `mix dialyzer` | `:dialyxir` in deps, pre-PR |
| Sobelow | `mix sobelow --config` | `:sobelow` in deps |
| E2E/Extra | Ask user | If additional test commands found |

## Usage

1. Run `/phx:verify` — discovery happens automatically
2. Core checks run in order, adapted to project
3. After pass, offered additional test commands (E2E, coverage)
4. Commit only after all chosen checks pass
