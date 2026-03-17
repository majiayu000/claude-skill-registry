---
name: pre-publish-qa
description: Run comprehensive QA checks before publishing to npm. Validates builds, tests, organon health, file lists, version alignment, and changelog. Use before any npm publish.
protocol_id: PROTO-ORG-10
protocol_file: organon/protocols/PROTOCOLS.md
tools:
  - organon-verify
  - organon-health
  - npm-test
  - npm-build
loads:
  - CLAUDE.md
---

# Pre-Publish QA Workflow

> Implements PROTO-ORG-10 from `organon/protocols/PROTOCOLS.md`. Comprehensive quality gate before npm publication.

---

## When to Use This Skill

Use this skill when:
- **Before publishing** — mandatory check before any npm release
- **Before running release script** — ensures everything is clean
- **After significant changes** — when you want publish-level confidence

**Purpose:** Catch version misalignment, missing files, broken builds, and test failures before they reach npm.

---

## Context Loading

1. Load project constraints:
   - Read `CLAUDE.md` (project invariants and development workflow)

**Note:** This workflow is self-contained. Additional context is only needed if a specific check fails.

---

## Steps

### Step 1: Clean Build Both Packages

Use `npm-build` to compile both packages. Build order matters — `@organon-methodology/testing` must build before `@organon-methodology/tools`.

```bash
cd packages/testing && npm run clean && npm run build
cd packages/tools && npm run clean && npm run build
```

Both must compile without TypeScript errors.

### Step 2: Run All Tests

Use `npm-test` to run test suites in both packages:

```bash
npm run test -w packages/testing
npm run test -w packages/tools
```

All tests must pass. Zero failures, zero skipped.

### Step 3: Run Organon Verify

```bash
cd packages/tools && npx organon verify --project-root ../..
```

All 9 gates must pass: frontmatter, triplets, references, placeholder-detection, freshness, invariant-coverage, workflow-quality, tier4-tests, version-alignment.

### Step 4: Run Organon Health

```bash
cd packages/tools && npx organon health --project-root ../..
```

Score must be 100/100. Do not publish with degraded health.

### Step 5: Check npm pack Dry Run

```bash
cd packages/testing && npm pack --dry-run
cd packages/tools && npm pack --dry-run
```

Verify each package includes:
- `dist/` directory (compiled output)
- `LICENSE` file
- `README.md` file
- No unexpected files (no `src/`, no `node_modules/`, no test files)

### Step 6: Verify Version Alignment

Check these four locations have the **same** version string:

| Location | Field |
|----------|-------|
| `packages/tools/package.json` | `version` |
| `packages/testing/package.json` | `version` |
| `organon.config.json` | `methodology_version` |
| `packages/tools/src/templates/config.ts` | `METHODOLOGY_VERSION` |

### Step 7: Verify CHANGELOG.md

- `CHANGELOG.md` must have an entry for the current version
- Entry must include a date (format: `YYYY-MM-DD`)
- Entry must not be empty (at least one Added/Changed/Fixed section)

### Step 8: Check for TODOs

```bash
grep -r "TODO\|FIXME" packages/tools/src/ packages/testing/src/ || echo "Clean"
```

No TODO or FIXME comments should exist in published source code. If found, either resolve them or move them to a tracking issue.

---

## Verification

- [ ] Both packages build without TypeScript errors
- [ ] All tests pass in both packages (zero failures)
- [ ] `organon verify` passes all 9 gates
- [ ] `organon health` reports 100/100
- [ ] `npm pack --dry-run` shows correct file lists (dist, LICENSE, README)
- [ ] All four version locations are aligned
- [ ] CHANGELOG.md has entry for current version with date
- [ ] No TODOs or FIXMEs in src/ directories

---

## Error Recovery

| Failure | Recovery Action |
|---------|-----------------|
| Build fails in `@organon-methodology/tools` | Check if `@organon-methodology/testing` was built first. The tools package depends on it. |
| Tests fail | Fix failing tests. Never skip tests for a release. |
| `organon verify` gate failure | Use `/verify-and-health` skill to diagnose and fix. |
| Health score below 100 | Fix organon issues. Check frontmatter accuracy, reference integrity, and triplet bindings. |
| Version misalignment | The release script (`scripts/release.mjs`) updates all four locations atomically. If manually editing, check all four. |
| Missing LICENSE in pack | Ensure `LICENSE` file exists in the package directory (not just repo root) and is in the `files` array of `package.json`. |
| TODOs found in source | Resolve the TODO or create a GitHub issue and remove the comment. |
