---
name: browser-workbench-setup
description: Set up browser automation and UI QA for a new repository using playwright-interactive as the primary interactive tool and agent-browser as the secondary CLI smoke-check tool. Use when a user wants to bootstrap browser testing, screenshots, auth-state reuse, or local UI debugging conventions in a fresh repo.
---

# Browser Workbench Setup

Use this skill to configure a new repository for browser-based UI work with the smallest durable setup.

Default tool split:

- `playwright-interactive` is the primary tool for iterative UI/UX work, auth flows, layout debugging, screenshots, and deeper investigation.
- `agent-browser` is the secondary tool for quick smoke checks, annotated screenshots, fast snapshots, and lightweight CLI automation.

Do not create a custom framework, wrapper package, or shared browser helper layer unless the user explicitly asks for one.

Load references only as needed:

- Read [references/playwright-interactive.md](references/playwright-interactive.md) when setting up the primary interactive workflow.
- Read [references/agent-browser.md](references/agent-browser.md) when setting up CLI smoke checks, session persistence, or annotated screenshots.
- Read exactly one provider file when the repository auth stack is clear:
  - [references/auth-clerk.md](references/auth-clerk.md)
  - [references/auth-supabase.md](references/auth-supabase.md)
  - [references/auth-auth0.md](references/auth-auth0.md)
  - [references/auth-neon.md](references/auth-neon.md)

If the repo uses Neon with an upstream identity provider such as Clerk or Auth0, read both `auth-neon.md` and the upstream provider file. Neon may be the database auth verifier while the browser login still belongs to the upstream provider.

## Preconditions

- Confirm `playwright-interactive` is installed and available in Codex.
- Confirm `agent-browser` CLI is installed.
- Confirm Codex has `js_repl = true`.
- Confirm the session can run with `danger-full-access` when using `playwright-interactive`.

If any of those are missing, fix that first before touching the repository.

## Setup Goals

For a normal web repository, finish with:

- repo-local Playwright dependency installed with the repository's package manager
- browser binaries installed
- stable artifact directories for screenshots, traces, and auth state
- ignore rules for local browser artifacts
- a clear convention for when to use `playwright-interactive` vs `agent-browser`

## Workflow

1. Inspect the repository first.
   - Read `package.json`, lockfiles, and any repo `AGENTS.md`.
   - Detect the package manager from the repo, not from habit.
   - Reuse existing test/artifact conventions if they already exist.
   - Detect the auth provider from dependencies, env vars, routes, and middleware before making changes.
   - Provider detection hints:
     - Clerk: `@clerk/`, `CLERK_`, `NEXT_PUBLIC_CLERK_`
     - Supabase: `@supabase/`, `SUPABASE_URL`, `SUPABASE_`, `createBrowserClient`, `createServerClient`
     - Auth0: `@auth0/`, `AUTH0_`, `/auth/login`, `Auth0Client`
     - Neon Auth: `neon_auth`, Neon auth endpoints, Neon JWT/JWKS setup, provider-owned auth integration

2. Install Playwright in the repo with the repo's package manager.
   - For Bun repos, prefer:
   ```bash
   bun add -d playwright
   bunx playwright install chromium
   ```
   - For pnpm/npm/yarn repos, match the repo standard.
   - Install only what is needed. Default browser is Chromium unless the user asked for more.

3. Create a minimal artifact convention.
   - Preferred defaults:
     - `output/playwright/screenshots/`
     - `output/playwright/traces/`
     - `output/playwright/auth/`
     - `output/agent-browser/`
   - Reuse an existing `reports/` or `output/` convention if the repo already has one.

4. Add ignore rules for local-only artifacts.
   - Typical entries:
   ```gitignore
   output/playwright/
   output/agent-browser/
   playwright/.auth/
   ```
   - Do not add duplicate ignore entries.

5. Standardize auth-state handling.
   - Prefer Playwright `storageState` for authenticated iteration and reusable test sessions.
   - Use `agent-browser` profiles or session names only for quick local smoke work.
   - Keep auth files out of git.
   - Prefer provider-supported test helpers when they exist.
   - If the provider has no first-party Playwright helper, prefer seeded test users plus saved browser state.
   - Avoid MFA in automated browser runs unless the provider explicitly supports it in test helpers.

6. Keep the responsibility split explicit.
   - Use `playwright-interactive` for:
     - serious interactive debugging
     - auth-heavy flows
     - desktop/mobile passes
     - console/network inspection
     - screenshots and trace evidence
   - Use `agent-browser` for:
     - quick smoke checks
     - annotated screenshots
     - fast snapshots
     - simple DOM or screenshot diffs

7. Avoid unnecessary additions.
   - Do not add Playwright test scaffolding unless the user asked for formal test coverage.
   - Do not add helper scripts, custom CLIs, or wrapper packages by default.
   - Do not add CI config unless the user asked for CI.
   - For auth setup, add only the minimum repo changes needed to make interactive browser work repeatable.
   - User-level tools such as `~/.agent-browser/config.json` belong outside the repo.

## Provider Routing

After the initial repo scan:

- Read `playwright-interactive.md` for the primary workflow.
- Read `agent-browser.md` for CLI setup and persistence.
- Read one provider auth file for the active identity stack.
- For Neon-backed repos:
  - if Neon Auth owns the user lifecycle, read `auth-neon.md`
  - if Neon is only verifying JWTs from Clerk/Auth0/etc., read `auth-neon.md` plus that upstream provider file

Do not load every provider reference by default.

## Automation Standard

When the user asks to set this up in a repo, complete the work end to end:

- install the repo-local Playwright dependency
- install browser binaries
- create artifact directories
- add ignore rules
- add or align formal auth bootstrap only if the repo already has Playwright tests or the user asked for them
- configure `agent-browser` persistence with either a profile path or a session name convention
- report the exact auth path chosen and why

## Preferred Defaults

When no repo convention conflicts:

- install only `playwright`
- install only Chromium first
- keep artifacts under `output/`
- use repo-local ignores, not global git excludes
- keep setup changes small and reviewable

## Deliverable

When you finish, report:

- package manager used
- dependency added
- directories added
- ignore rules added
- any user-level config that must exist outside the repo
- provider-specific auth path selected
- the exact command the user should run first with `playwright-interactive`

## First-Run Prompt

After setup, suggest a first real task such as:

`Use $playwright-interactive to open the local app, verify sign-in, test theme persistence, run desktop and mobile passes, and capture screenshots.`
