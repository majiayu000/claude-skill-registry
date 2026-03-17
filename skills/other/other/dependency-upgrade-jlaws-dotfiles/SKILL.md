---
name: dependency-upgrade
description: Dependency upgrade strategy and risk assessment. Use when upgrading major dependencies, resolving conflicts, or planning migration paths.
---

# Dependency Upgrade

## Upgrade Strategy

### Golden Rule: One Major at a Time
- Never upgrade multiple major versions simultaneously
- Upgrade in dependency order: core language -> framework -> routing/state -> testing -> build tools
- Each upgrade = separate branch + full test run

### Risk Assessment Matrix

| Risk Factor | Low | Medium | High |
|-------------|-----|--------|------|
| **Breaking changes** | Deprecation warnings only | API renames, config changes | New paradigms, rewrite required |
| **Ecosystem impact** | No peer deps affected | 2-3 peer deps need updating | Entire plugin ecosystem changes |
| **Test coverage** | >80% on affected code | 50-80% | <50% |
| **Rollback cost** | Revert one commit | Revert + data migration | Can't rollback |

High risk = dedicated spike, staging validation, phased rollout.

## Upgrade Process

### Phase 1: Assessment
- Read CHANGELOG.md and MIGRATION.md for every major version between current and target
- Check peer dependency compatibility (React 18 needs react-dom 18, testing-library 13+, etc.)
- Search GitHub issues for the upgrade path -- others have hit the gotchas already
- Run existing test suite as baseline

### Phase 2: Execution
- Create feature branch from main
- Git tag current state for easy rollback reference
- Upgrade the dependency + its required peer deps together
- Fix TypeScript errors first (they reveal API changes)
- Fix test failures
- Run full test suite
- Check bundle size impact: >10% increase warrants investigation

### Phase 3: Validation
- Smoke test in staging with real data
- Monitor error rates for 24-48 hours post-deploy
- Keep rollback branch ready for one week

## Automated Dependency Updates

### Renovate (preferred)
- Auto-merge minor/patch with passing CI
- Manual review for major updates with `labels: ["major-update"]`
- Group related packages: `"groupName": "react"` for react + react-dom
- Schedule: weekly, before business hours

### Dependabot
- Simpler config, GitHub-native
- Limit open PRs to 5 to avoid PR fatigue
- Use `commit-message: { prefix: "chore" }` for conventional commits

### Which to Choose
- **Renovate**: More control, grouping, auto-merge rules. Use for serious projects.
- **Dependabot**: Simpler, good enough for smaller projects. Built into GitHub.

## Common Gotchas

### Lock File Hygiene
- Always commit lock files (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`)
- Use `npm ci` / `pnpm install --frozen-lockfile` in CI
- After upgrade: `npm dedupe` / `pnpm dedupe` to flatten duplicate versions

### Peer Dependency Resolution
- `--legacy-peer-deps` is a bandaid, not a fix. Understand why it's needed.
- `overrides` (npm) / `resolutions` (yarn) / `pnpm.overrides` for forcing versions
- Document overrides with comments explaining why they exist

### Codemods
- Check if the library provides official codemods (React, Next.js, ESLint do)
- Run codemods before manual fixes
- Review codemod output -- they're not perfect

### Workspace Upgrades
- Upgrade shared packages first, then consumers
- Use `pnpm --filter ... build` to test downstream impact
- Pin workspace dependencies with `workspace:*` protocol

## Upgrade Checklist

**Pre-upgrade:**
- [ ] Read changelogs for breaking changes
- [ ] Check peer dependency compatibility
- [ ] Create branch, tag current state
- [ ] Run full test suite (baseline)

**During upgrade:**
- [ ] One major version at a time
- [ ] Update peer dependencies
- [ ] Fix TS errors -> test failures -> runtime issues
- [ ] Check bundle size

**Post-upgrade:**
- [ ] Full regression test
- [ ] Deploy to staging
- [ ] Monitor errors 24-48h
- [ ] Update documentation if APIs changed
