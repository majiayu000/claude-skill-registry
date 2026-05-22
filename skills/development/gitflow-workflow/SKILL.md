---
name: gitflow-workflow
description: Use this skill for GitFlow tasks: starting/finishing features, releases, hotfixes; managing branches; versioning; or general GitFlow operations.
user-invocable: false
allowed-tools: Read
version: 0.1.0
---

## Purpose

All detailed command manuals live under `./references/` and should be consulted when you need exact flags/options.

## Required invariants (used by the 6 instruction-type skills)

### Preflight

Before any start/finish operation:
- Confirm working tree is clean (use `git status` to verify).
- Identify current branch and verify the branch type matches the operation (`feature/*`, `hotfix/*`, `release/*`).
- Determine the active workflow preset (Classic GitFlow vs GitHub Flow vs GitLab Flow) to identify correct base/target branches.

### Branch naming

- Use kebab-case and a strict prefix: `<type>/<kebab-case>` (e.g. `feature/user-authentication`).

### Finish behavior

- Prefer non-fast-forward merges when finishing (e.g. `--no-ff`) to preserve a visible integration history, unless the repo workflow config says otherwise.
- Run tests if available before finishing; fix failures before merging.
- After finishing hotfix/release, ensure the integration branch receives the changes (often merging back into `develop`).
- Delete topic branches locally and remotely after finishing when policy allows.

### Changelog generation

When updating CHANGELOG.md during `finish-release` or `finish-hotfix` operations, follow these principles:

**Core principle:** Include all commits that represent **user-facing changes** since the previous version tag. Exclude internal-only changes (build, CI, tooling) and administrative commits (merges, releases).

**Note:** The `finish-feature` operation updates the `[Unreleased]` section without filtering, as features are already user-facing by nature.

**Commit collection process for releases and hotfixes:**
1. Identify the previous version tag (e.g., `v1.5.0`)
2. Collect commits: `git log --oneline <previous-tag>..HEAD`
3. Filter commits using conventional commit format, applying the user-facing principle:
   - **Include**: Commits that affect end users, API consumers, or documented behavior (e.g., `feat`, `fix`, `refactor`, `docs`, `perf`, `deprecate`, `remove`, `security`)
   - **Exclude**: Internal tooling (`chore`, `build`, `ci`), test-only changes (`test`), merge commits, release commits
4. Map commit types to appropriate Keep a Changelog sections (`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`)
5. Format entries using present/imperative tense and user-facing language
6. Merge repetitive items and include sufficient context to understand impact

See `${CLAUDE_PLUGIN_ROOT}/examples/changelog.md` for the standard format.

## Minimal templates (what the 6 skills assume)
The operation-specific templates have been moved into the corresponding `start-*` / `finish-*` skills to keep those tasks self-contained.

## Reference index

- `./references/context-gathering.md`
- `./references/naming-rules.md`
- `./references/workflow-presets.md`
- `./references/versioning-and-tags.md`
- `./references/commands-core.md`
- `./references/commands-topic.md`

## External References

- [git-flow-next Documentation](https://git-flow.sh/docs/)
- [git-flow-next Commands](https://git-flow.sh/docs/commands/)
- [git-flow-next Cheat Sheet](https://git-flow.sh/docs/cheat-sheet/)
