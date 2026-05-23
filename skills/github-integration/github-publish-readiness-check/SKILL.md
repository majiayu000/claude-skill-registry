---
name: "github-publish-readiness-check"
description: "Audit a local repository before creating a new public GitHub remote"
domain: "release-operations"
confidence: "high"
source: "bishop-readiness-check"
---

## Context

Use this when someone asks whether a local codebase is ready to become a new public GitHub repository, especially when the repo may have local-only IDE state, build outputs, or an incomplete tracked history.

## Patterns

### 1. Separate transport readiness from content readiness

- Check `git remote -v`, branch, and working-tree state first.
- Check `gh` availability/auth separately.
- Check target repo-name availability on GitHub before any create/push step.

Passing auth is not enough; a dirty or incomplete working tree is still a publish blocker.

### 2. Trust `git status` only after ignore hygiene

Before judging what is really ready to publish, make sure common local-only state is ignored:

- `.vs/`
- `.copilot/`
- `bin/`
- `obj/`
- `TestResults/`
- `*.user`, `*.suo`, `*.slnLaunch.user`

This removes noise from WPF/.NET/VS workflows so the remaining untracked set reflects intended repo content.

### 3. Check for public-repo blockers explicitly

- Existing remote already bound to another destination
- No `gh` CLI or not authenticated
- Target repo name already exists under the owner
- Large build artifacts that should not be committed
- Secret-like strings in the working tree
- Core app source still untracked

### 4. Stop when provenance is ambiguous

If most real source files are still untracked after ignore cleanup, do not create the public repo yet. That means the local repo history does not yet represent the product honestly.

## Checklist

1. `git rev-parse --show-toplevel`
2. Read team/project context if applicable
3. `git status --short --branch`
4. `git remote -v`
5. Confirm `gh` exists and `gh auth status` succeeds
6. Check whether the likely repo name already exists on GitHub
7. Tighten `.gitignore` for local-only files if needed
8. Re-check `git status`
9. Scan for obvious secrets / oversized artifacts
10. Report blockers in human terms; do not publish until source content is intentionally committed

## Anti-Patterns

- Creating the remote just because `gh` is authenticated
- Trusting a noisy `git status` that still includes build outputs and IDE caches
- Publishing a docs-only tracked history while the real app is untracked locally
