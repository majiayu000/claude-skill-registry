---
name: gh-deps-intel
description: 'Runtime-aware dependency upgrade intelligence for JavaScript/TypeScript and Python repositories (including monorepos/turborepos), using package-manager outdated checks plus GitHub API release/changelog mining to produce definitive Markdown+JSON upgrade/refactor reports. Use when auditing dependency upgrades, planning compatible version bumps, mapping deprecations/breaking changes, standardizing GitHub API/CLI dependency workflows, or when asked to fully upgrade a specific dependency/package (for example: "use $gh-deps-intel to fully upgrade workflow").'
---

# Gh Deps Intel

Use this as the canonical dependency-upgrade workflow skill. The shared `deps-workbench` helpers provide lightweight preflight inventory, classification, and usage mapping; this skill remains the deeper GitHub-aware analysis and reporting engine. This skill absorbs the former `dep-upgrade-spec` role.

## Invocation Defaults

- Explicit invocation with upgrade language such as "fully upgrade", "apply the upgrade", or a specific target package defaults to `execute`.
- Explicit invocation without an implementation request defaults to `plan`.
- In `execute`, still stop if auth, package-manager access, or repo safety checks fail.

## Tool Routing (MUST FOLLOW)

1. If you need a cheap preflight, run the shared helpers first:
   - `/home/bjorn/.codex/skill-support/bin/deps-workbench inventory --cwd <repo> --out <json>`
   - `/home/bjorn/.codex/skill-support/bin/deps-workbench classify --input <json> --out <json>`
   - `/home/bjorn/.codex/skill-support/bin/deps-workbench usage-scan --cwd <repo> --packages <pkg...> --out <json>`
2. If the user explicitly requests `gh api`/CLI only, use `scripts/gh_release_diff.py`, `scripts/gh_compare_notes.py`, or `scripts/gh_rate_limit_diag.py` directly.
3. For single-package requests ("fully upgrade X package"), use `scripts/gh_deps_intel.py package --dependency <name>`.
4. Otherwise, use `scripts/gh_deps_intel.py full` as the single orchestrator path (REST-first with GraphQL fallback for release retrieval).
5. Default to `--mode safe`; use `--mode fast` only when the user opts in.

## Workflow Modes

- `plan`: produce the Markdown + JSON upgrade report and execution order without mutating dependencies.
- `execute`: follow the planned batches, apply the requested upgrades, run repo-native verification, and then refresh the report.

## Quick Start

1. Prerequisites:
- `gh` authenticated (`gh auth status`)
- `python3` available
- Optional: `bun`/`pnpm`/`npm`/`yarn`, `uv`

2. Run full analysis from target repository root:
- `python /home/bjorn/.agents/skills/gh-deps-intel/scripts/gh_deps_intel.py full --repo . --out reports --mode safe`

3. Read outputs:
- `reports/dependency-upgrade-report.md`
- `reports/dependency-upgrade-report.json`

## Execution Modes

- `safe` (default): serial GitHub API pacing + backoff/retries.
- `fast`: bounded parallel enrichment with automatic safe-mode fallback on rate-limit/error signals.

## Primary Commands

- Full pipeline (recommended):
  - `python scripts/gh_deps_intel.py full --repo . --out reports --mode safe`
- Single dependency comprehensive spec:
  - `python scripts/gh_deps_intel.py package --repo . --out reports --mode safe --dependency workflow`
  - `python scripts/upgrade_one_dep.py workflow --repo . --out reports --mode safe`
- Stage outputs:
  - `python scripts/gh_deps_intel.py scan --repo . --out reports`
  - `python scripts/gh_deps_intel.py enrich --repo . --out reports --mode safe`
  - `python scripts/gh_deps_intel.py analyze --repo . --out reports --mode safe`
- Rate-limit diagnostic:
  - `python scripts/gh_deps_intel.py rate-limit`

## Resource Map

| Path | Type | Purpose | Use When |
|---|---|---|---|
| `scripts/gh_deps_intel.py` | orchestrator | End-to-end scan/enrich/analyze/report pipeline | Default for all dependency intelligence requests |
| `scripts/upgrade_one_dep.py` | utility | Convenience wrapper for single dependency `package` workflow | You need a comprehensive refactor spec for one package |
| `scripts/detect_repo.py` | script | Detect runtime, package managers, workspace topology | You need repo/runtime context only |
| `scripts/collect_deps.py` | script | Parse dependencies from `package.json` and `pyproject.toml` | You need manifest-level dependency inventory |
| `scripts/outdated_probe.py` | script | Run outdated commands mapped to detected managers | You need current/wanted/latest signals |
| `scripts/repo_resolver.py` | script | Resolve registry metadata and GitHub source repos | You need package->repo mapping |
| `scripts/gh_release_fetch.py` | script | GitHub releases/tags/changelog retrieval with cache/retries | You need release notes/changelog context |
| `scripts/runtime_policy.py` | script | Runtime compatibility targeting (Node/Python) | You need latest compatible target selection |
| `scripts/impact_analyzer.py` | script | Extract breaking/deprecations/features and refactor actions | You need actionable migration deltas |
| `scripts/render_report.py` | script | Markdown + JSON report generation | You need final upgrade intelligence outputs |
| `scripts/gh_release_diff.py` | utility | Release-window notes for arbitrary `owner/repo` | Ad-hoc release research |
| `scripts/gh_compare_notes.py` | utility | Compare-summary between refs/tags | Changelog unavailable; need commit summary |
| `scripts/gh_rate_limit_diag.py` | utility | Current GitHub rate-limit status | Verify API budget before large runs |
| `references/workflow.md` | reference | Canonical run order and decision tree | You need process guidance |
| `references/command-mapping.md` | reference | Package manager command equivalents | You need bun/pnpm/npm/yarn/uv/pip mapping |
| `references/github-api-endpoints.md` | reference | Endpoint and backoff rules | You need API behavior details |
| `references/compatibility-policy.md` | reference | Runtime-pinned target rules | You need version policy rationale |
| `references/report-spec.md` | reference | Output schema and report sections | You need machine/human contract details |
| `references/troubleshooting.md` | reference | Common failures and mitigations | You hit auth/rate-limit/parse issues |

## Reporting Contract

Always produce both files in the same stable contract:
- Markdown: concise upgrade/refactor plan by dependency.
- JSON: full structured data for downstream automation.

For `package` mode, include:
- targeted dependency selectors
- repository impact map (usage hits + affected files)
- explicit refactor checklist for that package only

## Additional GH Workflows

- Release window diff:
  - `python scripts/gh_release_diff.py owner/repo --current 1.2.3 --target 2.0.0`
- Compare summary:
  - `python scripts/gh_compare_notes.py owner/repo v1.2.3 v2.0.0`
- Rate-limit budget:
  - `python scripts/gh_rate_limit_diag.py`

## Shared Support Alignment

- Preflight inventory and classification live in `/home/bjorn/.codex/skill-support/bin/deps-workbench`.
- Long-form GitHub release intelligence stays here.
- When both are used, treat the Markdown and JSON output files from this skill as the final contract.
