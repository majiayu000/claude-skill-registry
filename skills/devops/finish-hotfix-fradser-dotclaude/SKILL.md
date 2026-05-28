---
name: finish-hotfix
allowed-tools: Bash(git:*), Read, Write, Skill
description: Complete and merge hotfix branch
model: haiku
argument-hint: [version]
user-invocable: true
---

## Your Task

1. **Load the `gitflow:gitflow-workflow` skill** using the `Skill` tool to access GitFlow workflow capabilities.
2. Gather context: current branch, git status, recent commits, version files.
3. Validate branch follows `hotfix/*` convention and working tree is clean.
4. Run tests if available. If tests fail, report the failures and exit without merging; the user must fix issues first.
5. Normalize the provided version from `$ARGUMENTS` to `$HOTFIX_VERSION`:
   - Accept `v1.2.3` or `1.2.3`
   - Normalize to `1.2.3` (and tag as `v$HOTFIX_VERSION` when tagging)
6. **Update CHANGELOG**:
   - Identify previous version tag.
   - Collect commits since previous tag following the user-facing principle defined in the `gitflow-workflow` skill (include feat, fix, refactor, docs, perf, deprecate, remove, security; exclude chore, build, ci, test, merge commits).
   - Update `CHANGELOG.md` (or create if missing) with the new version and date, following the format in `${CLAUDE_PLUGIN_ROOT}/examples/changelog.md`.
   - Commit the updated `CHANGELOG.md` to the current hotfix branch using conventional commit format (e.g., `chore: update changelog for v$HOTFIX_VERSION`) and MUST include the `Co-Authored-By` footer.
7. Merge into the production branch (often `main`/`production`), create the version tag, then propagate the changes to the integration branch (often `develop`/`main`), and push all changes.
8. Delete the hotfix branch locally and remotely. Skip deletion if the branch is shared or the user requests to keep it.
