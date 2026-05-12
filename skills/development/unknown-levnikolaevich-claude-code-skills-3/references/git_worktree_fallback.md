<!-- SOURCE-OF-TRUTH: shared/references/git_worktree_fallback.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Git Worktree Isolation

<!-- SCOPE: Universal worktree isolation for code-writing skills. Self-detection + branch naming + fallback. -->

## Lifecycle

Any skill that modifies code checks its git context and creates isolation if needed:

| Step | Action |
|------|--------|
| 1 | `git branch --show-current` — if already on `feature/*` / `optimize/*` / `upgrade/*` / `modernize/*` → skip to step 4 |
| 2 | Check for uncommitted changes: `changes=$(git diff HEAD)` |
| 2a | IF changes not empty: `git diff HEAD > .hex-skills/pipeline/carry-changes.patch` |
| 2b | Detect base branch per `references/git_scope_detection.md` §Base Branch Detection, then: `git fetch origin && git merge origin/{base_branch}` |
| 3 | `git worktree add {worktree_dir} -b {branch}` |
| 3a | IF patch exists: `git -C {worktree_dir} apply .hex-skills/pipeline/carry-changes.patch && rm .hex-skills/pipeline/carry-changes.patch` |
| 3b | IF apply fails (conflicts): warn user "Patch conflicts — continuing without uncommitted changes", continue (non-blocking) |
| 4 | All edits, benchmarks, commits in worktree |
| 5 | `git push -u origin {branch}` + report branch name to caller |
| 6 | `git worktree remove {worktree_dir}` (branch preserved on remote) |

## Branch Naming

| Category | Branch Pattern | Worktree Dir |
|----------|---------------|--------------|
| Story execution | `feature/{id}-{slug}` | `.hex-skills/worktrees/story-{id}` |
| Performance optimization | `optimize/{skill}-{target}-{ts}` | `../optimize-{skill}-{target}-{ts}` |
| Dependency upgrade (npm) | `upgrade/{skill}-npm-{ts}` | `../upgrade-{skill}-{ts}` |
| Dependency upgrade (NuGet) | `upgrade/{skill}-nuget-{ts}` | `../upgrade-{skill}-{ts}` |
| Dependency upgrade (pip) | `upgrade/{skill}-pip-{ts}` | `../upgrade-{skill}-{ts}` |
| OSS replacement | `modernize/{skill}-{module}-{ts}` | `../modernize-{skill}-{module}-{ts}` |
| Bundle optimization | `modernize/{skill}-bundle-{ts}` | `../modernize-{skill}-{ts}` |

`{ts}` = `YYYYMMDD-HHMMSS`. Both branch and directory include timestamp to prevent collision on reruns.

## Fallback (no worktree support)

If `git worktree` is not available, fall back to branch mode:

| Operation | worktree (default) | branch (fallback) |
|-----------|----------|--------|
| **Create** | `git worktree add -b {branch} {dir} develop` | `git checkout -b {branch}` |
| **Uncommitted** | Carry via patch (steps 2-3a above) | Stay in working dir (no action) |
| **Work dir** | `{worktree_dir}/` | Current directory |
| **Git commands** | `git -C {dir} ...` | `git ...` (no -C needed) |
| **Cleanup** | `git worktree remove {dir}` | `git branch -d {branch}` |

## Usage in SKILL.md

```markdown
**MANDATORY READ:** Load `references/git_worktree_fallback.md`
```

---
**Version:** 3.0.0
**Last Updated:** 2026-04-05
