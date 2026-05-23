---
name: recompile-workflows
description: Regenerate and post-process all agentic workflows. Use when gh-aw is updated, workflow .md files change, or when asked to recompile/regenerate workflows.
allowed-tools: Bash(gh:*), Bash(npx:*), Read, Glob, Edit
---

# Recompile Agentic Workflows

Use this skill when you need to regenerate all agentic workflow lock files and apply post-processing.

## IMPORTANT: Post-processing is required after EVERY lock file change

Any time `.lock.yml` files are regenerated — whether via `gh aw compile`, `gh aw upgrade`, or any other gh-aw command — you MUST run the post-processing script afterward. This is not optional.

## Steps

### 1. Compile or upgrade workflows

Use whichever command is appropriate:

```bash
# Full upgrade (updates agents, actions, codemods, then compiles)
gh aw upgrade

# Just recompile (when only .md workflow files changed)
gh aw compile
```

If any workflow fails to compile (e.g., strict mode violations like `contents: write`), fix the `.md` source file and re-run.

### 2. Run post-processing script (ALWAYS)

**This step MUST run every time lock files are regenerated, regardless of how they were generated.**

The post-processing script replaces the "Install awf binary" step in smoke and build-test workflows with local build+install steps, so CI tests the repo's own code instead of a released binary.

```bash
npx ts-node scripts/ci/postprocess-smoke-workflows.ts
```

This updates these lock files:
- `smoke-copilot.lock.yml`
- `smoke-claude.lock.yml`
- `smoke-chroot.lock.yml`
- `build-test-node.lock.yml`
- `build-test-go.lock.yml`
- `build-test-rust.lock.yml`
- `build-test-java.lock.yml`
- `build-test-cpp.lock.yml`
- `build-test-deno.lock.yml`
- `build-test-bun.lock.yml`

## Common Issues

### Strict mode violations
Newer gh-aw versions enforce strict mode which disallows write permissions like `contents: write`, `issues: write`, etc. Workflows should use `safe-outputs` for write operations and only request `read` permissions.

### Discussion category warnings
Warnings about "General" vs "general" discussion category casing are non-blocking.

## Verification

After both steps, run `git diff --stat` to review all changed files. Expect changes in:
- `.github/agents/` - Updated agent files
- `.github/aw/actions-lock.json` - Updated action pins
- `.github/workflows/*.lock.yml` - Regenerated lock files
- `.github/workflows/*.md` - If codemods applied fixes
