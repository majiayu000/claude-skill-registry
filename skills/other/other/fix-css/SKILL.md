---
name: fix-css
description: Fixes corrupted Panda CSS styled-system when styles appear broken, CSS isn't applying, or the build fails with styled-system errors. Use when CSS looks wrong, styles are missing, or after prettier/formatters may have corrupted generated files.
allowed-tools: Bash, Read, Glob
---

# Fix Corrupted Panda CSS (styled-system)

This project uses **Panda CSS** which generates a `styled-system/` directory. This directory can become corrupted when:

- Prettier or other formatters modify the generated files
- Git merge conflicts in styled-system/
- Interrupted `panda codegen` runs
- Node modules corruption

## Symptoms

- Styles not applying correctly
- CSS appears broken or missing
- Build errors mentioning `styled-system`
- Type errors in `styled-system/` imports
- Visual regressions that appeared without code changes

## Fix Procedure

Run these commands in order:

```bash
# 1. Delete the corrupted styled-system
rm -rf apps/web/styled-system

# 2. Regenerate it with Panda CSS
cd apps/web && pnpm panda codegen

# 3. Clear Next.js cache (if build errors persist)
rm -rf apps/web/.next

# 4. Rebuild to verify
cd /Users/antialias/projects/soroban-abacus-flashcards && pnpm build
```

## Verification

After regeneration, verify:

1. `apps/web/styled-system/` directory exists with fresh files
2. `pnpm build` completes without styled-system errors
3. Dev server shows correct styling

## Prevention

The repo has `.prettierignore` at the root that excludes `**/styled-system/**`. If corruption keeps happening:

1. Verify `.prettierignore` contains `**/styled-system/**`
2. Check that IDE formatters respect `.prettierignore`
3. Ensure git hooks don't format styled-system files

## Quick One-Liner

For fast fix without explanation:

```bash
rm -rf apps/web/styled-system apps/web/.next && cd apps/web && pnpm panda codegen && cd ../.. && pnpm build
```
