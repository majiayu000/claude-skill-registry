---
name: deps-upgrade
description: Dependency-upgrade campaign — outdated scan, batch-by-severity, breaking-change remediation, lockfile audit. Use when CVEs require remediation, when a major upstream version lands, when stack compatibility forces a sweep, or on a scheduled (quarterly) hygiene cadence. CVE-driven bumps consume security audit findings as input.
---

Dependencies are inherited code. Upgrades are inherited risk. Patch in batch, minor in batch with a smoke test, major one-at-a-time with a CHANGELOG read.

## When to Apply / NOT

Apply: CVE remediation; major upstream release; compatibility forcing function; quarterly hygiene cadence; pre-release lockfile audit; deprecation warnings accumulating.

NOT apply: active feature branch with high churn; pre-release freeze window; mid-incident; API-break-driven refactor.

## Anti-patterns

- **Big-bang upgrade**: bumping every dep at once.
- **Skipping the lockfile**: floating ranges create non-reproducible builds.
- **Ignoring the CHANGELOG**: major bumps without reading upstream notes.
- **Suppressing deprecations**: `--warning-as-error=off` defers cost.
- **Bypassing audit signals**: `npm audit fix --force` without reading.
- **No smoke test on minor**: minor versions can introduce behavior shifts.
- **Forgetting transitives**: surface deps look fine; transitive CVE remains.
- **Mixing concerns in one commit**: upgrade + refactor + feature — atomize per `<git>` policy.

## Workflow (language-neutral)

1. **Inventory** — enumerate manifests + lockfiles across ecosystems. Many canonical names are extensionless (`go.mod`, `Gemfile`, `pom.xml`); filtering by extension alone misses them. `fd` only takes one glob per call, so anchor on canonical filenames via a single regex:

   ```sh
   fd -t f '^(package(-lock)?\.json|pnpm-lock\.yaml|yarn\.lock|Cargo\.(toml|lock)|pyproject\.toml|poetry\.lock|requirements.*\.txt|Pipfile\.lock|go\.(mod|sum)|pom\.xml|build\.gradle(\.kts)?|settings\.gradle(\.kts)?|libs\.versions\.toml|gradle\.lockfile|Gemfile(\.lock)?|.*\.gemspec|.*\.opam|dune-project|opam\.locked|mix\.(exs|lock)|composer\.(json|lock))$'
   ```

   Add ecosystem-specific names if the project uses something rarer (`Pipfile`, `Brewfile`, `flake.nix`, `shard.yml`, `pubspec.yaml`). Capture a lockfile snapshot for later diff (`difft`).
2. **Scan outdated** — run ecosystem outdated/upgradable command. Capture report.
3. **Categorize** — bin every candidate as **patch** / **minor** / **major**.
4. **Patch batch** — bump all patches at once; lockfile-only diff. Run full test suite. Commit `chore(deps): patch sweep`.
5. **Minor batch** — bump minors together; smoke-test. Read each minor CHANGELOG. Commit `chore(deps): minor sweep`.
6. **Major individually** — one major version per commit. Read CHANGELOG / migration guide first; apply codemod or manual edits; run full suite + adversarial tests. Commit `chore(deps)!: bump <pkg> <old>→<new>`.
7. **Lockfile audit** — compare pre/post with `difft` (not `diff`). Check transitive churn.
8. **Re-scan** — run CVE scanner again post-upgrade.
9. **Hand off** — major upgrade requires API-break propagation → cross to a refactor / break-compat workflow. New CVEs → hand to security-audit workflow.

## Breaking-Change Review Checklist

For each major bump, before writing any code:

- Read upstream `CHANGELOG.md` / `MIGRATION.md` / release notes
- Identify removed/renamed/behavior-changed/default-changed APIs
- Check for codemod / mod-tool the upstream supplies
- Run tests with deprecation-warnings-as-errors enabled
- Search for direct usage with `git grep -n -F '<symbol>'` and `ast-grep -p '<pattern>'`
- Verify peer-dep / runtime-version compatibility matrix
- Verify license has not changed in a blocking direction
- Verify SBOM diff matches expected dependency-tree change

## Parallel Lockfile / Upgrade Tooling

| Family | Outdated scan | Upgrade command | Lockfile |
|---|---|---|---|
| Rust | `cargo outdated`, `cargo audit` | `cargo update`, `cargo upgrade` | `Cargo.lock` |
| Python (Poetry) | `poetry show --outdated` | `poetry update`, `poetry add <pkg>@latest` | `poetry.lock` |
| Python (pip-tools) | `pip list --outdated`, `pip-audit` | `pip-compile --upgrade`, `pip-sync` | `requirements.txt` |
| JavaScript/TypeScript (pnpm) | `pnpm outdated`, `pnpm audit` | `pnpm update`, `pnpm up --latest` | `pnpm-lock.yaml` |
| JavaScript/TypeScript (npm) | `npm outdated`, `npm audit` | `npm update`, `ncu -u` | `package-lock.json` |
| Go | `go list -u -m all`, `govulncheck` | `go get -u <pkg>@latest`, `go mod tidy` | `go.sum` |
| Java/Kotlin (Gradle) | `gradle dependencyUpdates` | edit `libs.versions.toml`, `gradle dependencies --refresh-dependencies` | `gradle.lockfile` |
| Java/Kotlin (Maven) | `mvn versions:display-dependency-updates` | `mvn versions:use-latest-releases` | `pom.xml` |
| OCaml | `opam list --upgradable` | `opam upgrade <pkg>`, `opam pin <pkg>.<ver>` | `*.opam.locked` |

Use `fd -e <ext>` (not `find`). Use `difft` (not `diff`). Use `bat -P -p -n` (not `cat`). Use `git grep -n -F` (not `grep`).

## Constitutional Rules

1. **Lockfile is law** — always commit lockfile diffs.
2. **Atomic commits** — one bin per commit; one major per commit.
3. **Read the CHANGELOG** — major bump without primary-source review forbidden.
4. **Test after every bin**.
5. **Re-scan post-upgrade**.
6. **Deprecations are debt** — file follow-ups.
7. **Do not bypass audit signals**.

## Tooling notes

- `difft` is the mandated lockfile diff viewer; `diff` is banned.
- `hyperfine` validates upgrade did not regress hot-path performance.
