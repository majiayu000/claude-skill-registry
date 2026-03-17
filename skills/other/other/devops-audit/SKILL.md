---
name: devops-audit
version: 1.0.0
description: >-
  This skill should be used when the user asks to "run a devops audit",
  "check release readiness", "audit CI/CD", "review DevOps setup",
  "check workflows", "validate packaging", "audit documentation accuracy",
  "check version synchronization", "validate release artifacts",
  "verify documentation accuracy",
  or mentions "devops findings", "release checklist", or "pre-publish review".
  Provides a systematic DevOps audit checklist derived from two rounds of
  real audit findings on this project.
---

# DevOps Audit Skill

Systematic DevOps audit for Python Claude Code plugins distributed via GitHub.
Derived from two real audit rounds that found 1 blocker, 10 warnings, and 4
suggestions — several of which were missed in the first pass.

## When to Invoke

- Before any version release or tag creation
- After significant infrastructure changes (new hooks, new migrations, CI edits)
- When preparing for marketplace or PyPI publishing
- On request for "devops audit" or "release readiness check"

## Audit Workflow

Execute in this order. Read `references/full-checklist.md` before starting
to understand all 51 verification criteria across these phases.

### Phase 1: Version Synchronization

Check that the version string is identical across all authoritative files.
This project has three:

1. `pyproject.toml` → `[project] version`
2. `.claude-plugin/plugin.json` → `version`
3. `.claude-plugin/marketplace.json` → `version`

Also verify CHANGELOG.md has a section header `## [X.Y.Z]` matching that version.

### Phase 2: CI Pipeline Integrity

Audit `.github/workflows/ci.yml`:

- **Dependency pinning**: All `pip install` commands pin upper bounds (e.g. `"ruff>=0.9.0,<1.0"`), not open-ended ranges. Bare `>=` without `<` is a finding.
- **Shell quoting**: `pip install foo>=1.0` without quotes is a shell redirect hazard on some runners. Must be quoted.
- **Matrix coverage**: Python versions in CI matrix match `requires-python` floor from pyproject.toml.
- **Build verification**: CI runs `python -m build` to prove the package builds.
- **Coverage upload**: Coverage artifact uploaded from a single canonical matrix cell.

### Phase 3: Release Workflow Integrity

Audit `.github/workflows/release.yml`:

- **Artifact attachment**: The release step MUST build (`python -m build`) and attach sdist + wheel via `files:` parameter. A release without downloadable artifacts is a blocker.
- **Changelog extraction**: The awk/grep that extracts release notes must use exact match (bracket-anchored), not substring match. `index($0, ver)` matches `2.1.0` inside `12.1.0`.
- **Test gate**: Tests run before release creation.
- **ODBC headers**: Linux runners need `unixodbc-dev` for pyodbc compilation.

### Phase 4: Dependency Management

- **Single source of truth**: Dependencies declared in `pyproject.toml` only. No parallel `requirements.txt` or `requirements-dev.txt` — these cause duplicate Dependabot PRs and version drift.
- **Dependabot config**: `.github/dependabot.yml` covers both `github-actions` and `pip` ecosystems.
- **Dev extras**: `[project.optional-dependencies] dev = [...]` contains test and lint tools.

### Phase 5: Documentation Accuracy

Cross-reference every claim in docs against actual code/config:

- **README install instructions**: Must list ALL migration files, not just the first one.
- **README tracking table**: Every hook type that exists in `plugin.json` must appear in the "What Gets Tracked" table. Compare hook keys in plugin.json against table rows.
- **README architecture diagram**: Must list every hook handler file. Compare against `hooks/db_*.py` files on disk.
- **README dev setup**: Must show `pip install -e ".[dev]"`, not reference deleted requirements files. Include cross-platform instructions, not just Windows PowerShell.
- **CONTRIBUTING.md install command**: Must match actual install method (`pip install -e ".[dev]"`).
- **CONTRIBUTING.md coverage figure**: Must match actual test output. Run `pytest --cov` and compare.
- **Migration section**: Must reference the full range of migration files, not a single example.

### Phase 6: Packaging & Build

- **Build succeeds**: `python -m build` produces both `.tar.gz` and `.whl` without errors.
- **Package name**: Verify `[tool.hatch.build.targets.wheel] packages` matches actual source directory.
- **Python floor**: `requires-python` in pyproject.toml matches CI matrix minimum and ruff `target-version`.

### Phase 7: Community & Security Files

Verify presence and accuracy of:
- `CHANGELOG.md` — current version documented
- `CONTRIBUTING.md` — install/test/lint commands accurate
- `SECURITY.md` — exists with contact info
- `LICENSE` or license field in pyproject.toml

## Lessons Learned (Anti-Patterns)

These are patterns that were missed in the first audit and only caught in round 2.
Pay special attention to these:

1. **Artifact-less releases**: A GitHub Release without `files:` looks complete but has nothing to download. Always verify the release action attaches built artifacts.

2. **Substring version matching in awk**: `index($0, "2.1.0")` matches inside `12.1.0` or `2.11.0`. Always anchor with brackets: `$0 ~ "\\[" ver "\\]"`.

3. **Orphaned requirements files**: After migrating to pyproject.toml extras, the old requirements*.txt files linger. They cause double Dependabot PRs and mislead contributors.

4. **Stale doc figures**: Coverage percentage, test count, migration file lists — these go stale silently. Always re-derive from actual command output during audit.

5. **New hooks missing from docs**: Adding a hook to plugin.json without updating README's tracking table and architecture diagram. Diff plugin.json hook keys against doc references.

6. **Platform-biased dev instructions**: README showing only Windows PowerShell for dev setup, despite CI testing on Ubuntu. Include cross-platform `pip install -e ".[dev]"` first.

7. **Unquoted pip specifiers in YAML**: `pip install ruff>=0.9.0` without quotes — works on most shells but is technically a redirect hazard and lacks an upper bound.

## Output Format

Present findings as a table:

```
| ID | Severity | Finding | Recommendation |
|----|----------|---------|----------------|
| B1 | Blocker  | ...     | ...            |
| W1 | Warning  | ...     | ...            |
| S1 | Suggest  | ...     | ...            |
```

Severity levels:
- **Blocker**: Broken functionality or release-blocking issue
- **Warning**: Correctness or maintainability problem
- **Suggestion**: Nice-to-have improvement

After presenting findings, propose a disposition for each (FIX / SKIP with rationale)
and ask the user to confirm before implementing.

## Additional Resources

### Reference Files

- **`references/full-checklist.md`** — Complete 45-item checklist with pass/fail criteria, organized by phase. Use for systematic audit execution.
