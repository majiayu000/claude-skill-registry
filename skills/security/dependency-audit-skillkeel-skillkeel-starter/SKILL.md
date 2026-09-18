---
name: dependency-audit
description: Use when the user asks to check dependencies for vulnerabilities, outdated packages, or before a release. Runs the ecosystem's real audit tool, separates fixable from unfixable, and proposes minimal safe upgrades with lockfile changes reviewed, never bulk-upgrading blindly.
---

# dependency-audit

## Procedure
1. Detect ecosystems by manifest: `package.json` (+ lockfile → npm/pnpm/yarn), `pyproject.toml`/`requirements*.txt`, `Cargo.toml`, `go.mod`, `Gemfile`, `composer.json`. Handle each present one.
2. Run the audit tool that exists (check availability first with `command -v`):
   - npm: `npm audit --json` / pnpm: `pnpm audit --json` / yarn: `yarn npm audit --json`
   - Python: `pip-audit -f json` (or `pip install pip-audit` in a venv if allowed) ; fallback `pip list --outdated`
   - Rust: `cargo audit --json` ; Go: `govulncheck ./...` ; Ruby: `bundle audit` ; PHP: `composer audit`
3. Summarise: table of `package | installed | severity | fixed in | direct/transitive | breaking?`. Sort by severity.
4. Propose fixes in tiers:
   - **Tier 1 (do now):** patch/minor bumps of direct deps with a fix available. Apply with the package manager (`npm install pkg@^x.y.z`), run the test suite, show the lockfile diff summary.
   - **Tier 2 (ask first):** major bumps or transitive overrides (`overrides`/`resolutions`).
   - **Tier 3 (document):** no fix available → note in `SECURITY.md` or an issue with the advisory link.
5. Re-run the audit and paste the before/after counts.

## Rules
- Never run `npm audit fix --force` or equivalent.
- Never bump beyond what the advisory requires unless asked.
- Run the project's tests after every applied bump; revert the bump if tests fail and report.
- If no audit tool is available and installing is not allowed, say so and stop at the outdated-list.

## Eval
`evals/dependency-audit/`: fixture `package.json` with a pinned old `lodash` and a package-lock; expected: audit run, lodash listed with severity, patch bump proposed as Tier 1, no `--force`.
