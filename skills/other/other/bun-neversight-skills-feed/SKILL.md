---
name: bun
description: |
  Complete Bun lifecycle management. Audits current state, plans migration,
  executes changes, verifies success. Full orchestrator for Bun adoption.
  Invoke for: migrate to bun, adopt bun, bun migration, switch to bun.
---

# /bun

Complete Bun lifecycle management. Audit → Plan → Execute → Verify.

## What This Does

1. Run comprehensive Bun compatibility audit
2. Determine migration scope (full, hybrid, or skip)
3. Execute migration steps via `/fix-bun` iterations
4. Verify complete migration
5. Benchmark performance improvement
6. Update documentation

## Process

### 1. Assess Current State

Run `/check-bun` to get full audit:

```
/check-bun
```

Review the output for:
- **P0 Blockers**: If any exist, recommend SKIP or HYBRID
- **P1 Essential**: Must fix before migration
- **Migration complexity**: LOW, MEDIUM, or HIGH
- **Recommendation**: PROCEED, HYBRID, or SKIP

### 2. Determine Migration Scope

**PROCEED (Full Migration)**
- No blockers
- Platform supports Bun
- Team ready for Bun

**HYBRID (Partial Migration)**
- Platform limitations (Expo, Vercel serverless)
- Keep pnpm for production apps
- Use Bun for internal tools/scripts

**SKIP (Not Recommended)**
- Critical blockers exist
- Platform doesn't support Bun
- Migration cost exceeds benefit

### 3. Interview (If Needed)

Use `AskUserQuestion` to clarify:
- Migration scope preference (full vs hybrid)
- Timeline constraints
- Specific concerns about Bun

### 4. Create Migration Branch

```bash
git checkout -b chore/bun-migration
```

### 5. Execute Migration

**For PROCEED scope:**

```
# Fix issues in priority order
/fix-bun  # P1: Lockfile cleanup
/fix-bun  # P1: CI migration
/fix-bun  # P1: Workspace migration
/fix-bun  # P2: Script updates
/fix-bun  # P2: Test runner
```

**For HYBRID scope:**

Keep pnpm for apps, set up Bun for tools:
```bash
# Main monorepo stays pnpm
# Add Bun for specific directories
mkdir -p tools/scripts
cd tools/scripts && bun init
```

### 6. Verification Checklist

After migration, verify everything works:

```bash
# 1. Clean install
rm -rf node_modules
bun install

# 2. Type checking
bun run typecheck  # or tsc --noEmit

# 3. Linting
bun run lint

# 4. Tests pass
bun test

# 5. Build succeeds
bun run build

# 6. Dev server works
bun run dev &
sleep 10
curl -f http://localhost:3000 > /dev/null && echo "✓ Dev server works"
kill %1
```

### 7. Performance Benchmark

Compare against pnpm baseline:

```bash
# Baseline (before migration, on main branch)
git stash
time pnpm install --force 2>&1 | tail -1
time pnpm run build 2>&1 | tail -1
time pnpm test 2>&1 | tail -1
git stash pop

# Bun (on migration branch)
time bun install --force 2>&1 | tail -1
time bun run build 2>&1 | tail -1
time bun test 2>&1 | tail -1
```

### 8. Update Documentation

**Update README.md:**
```markdown
## Development

This project uses [Bun](https://bun.sh) for package management and script execution.

### Prerequisites
- Bun 1.1.0+ (install: `curl -fsSL https://bun.sh/install | bash`)

### Setup
\`\`\`bash
bun install
bun run dev
\`\`\`
```

**Update CONTRIBUTING.md (if exists):**
```markdown
## Package Manager
This project uses Bun. Do not commit pnpm-lock.yaml or package-lock.json.

\`\`\`bash
bun install --frozen-lockfile
bun test
\`\`\`
```

### 9. Commit and PR

```bash
git add -A
git commit -m "chore: migrate to Bun package manager

- Replace pnpm with Bun for package management
- Update CI to use oven-sh/setup-bun
- Migrate workspace configuration to package.json
- Update documentation

Performance improvement:
- Install: Xms → Yms (Z% faster)
- Build: Xms → Yms (Z% faster)
- Test: Xms → Yms (Z% faster)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Output Report

```markdown
## Bun Migration Complete

### Scope
[FULL/HYBRID]

### Changes Made
- ✓ Removed pnpm-lock.yaml, added bun.lock
- ✓ Updated CI to use oven-sh/setup-bun
- ✓ Migrated workspace config to package.json
- ✓ Updated scripts to use bun run
- ✓ Updated documentation

### Performance Results
| Operation | Before (pnpm) | After (Bun) | Improvement |
|-----------|---------------|-------------|-------------|
| Install   | Xms           | Yms         | Z% faster   |
| Build     | Xms           | Yms         | Z% faster   |
| Test      | Xms           | Yms         | Z% faster   |

### Verification
- ✓ Clean install succeeds
- ✓ Type checking passes
- ✓ Linting passes
- ✓ All tests pass
- ✓ Build succeeds
- ✓ Dev server works

### Next Steps
1. Review and merge PR
2. Update any external CI/CD configs
3. Notify team of tooling change
```

## Rollback Procedure

If migration fails:

```bash
# Revert to pnpm
git checkout main
rm -rf node_modules bun.lock bun.lockb
pnpm install
```

## Related

- `/check-bun` - Audit for Bun compatibility
- `/fix-bun` - Fix one Bun issue at a time
- `/bun-best-practices` - When to use Bun (reference)
