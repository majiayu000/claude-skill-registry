---
name: finish-release
allowed-tools: Bash(git:*), Bash(gh:*), Read, Write, Skill
description: Complete and merge release branch
model: haiku
argument-hint: [version]
user-invocable: true
---

## Your Task

1. **Load the `gitflow:gitflow-workflow` skill** using the `Skill` tool to access GitFlow workflow capabilities.
2. Gather context: current branch, git status, recent commits, version files.
3. Validate branch follows `release/*` convention and working tree is clean.
4. Run tests if available. If tests fail, report the failures and exit without merging; the user must fix issues first.
5. Normalize the provided version from `$ARGUMENTS` to `$RELEASE_VERSION`:
   - Accept `v1.2.3`, `1.2.3`, or `release/1.2.3`
   - Normalize to `1.2.3` (and tag as `v$RELEASE_VERSION` when tagging)
6. **Update CHANGELOG** (mandatory):
   - Identify previous version tag.
   - Collect commits since previous tag following the user-facing principle defined in the `gitflow-workflow` skill (include feat, fix, refactor, docs, perf, deprecate, remove, security; exclude chore, build, ci, test, merge commits).
   - Update `CHANGELOG.md` (create if missing) with the new version and date, following the format in `${CLAUDE_PLUGIN_ROOT}/examples/changelog.md`.
   - If `CHANGELOG.md` was manually updated during start-release, merge or reconcile entries while preserving manual curation.
   - Commit the updated `CHANGELOG.md` to the current release branch using conventional commit format (e.g., `chore: update changelog for v$RELEASE_VERSION`) and MUST include the `Co-Authored-By` footer.
7. Merge into `main` (often with `--no-ff`), create the version tag.
8. Merge `main` back to `develop`, push all changes.
9. Delete release branch locally and remotely. Skip deletion if the branch is shared or the user requests to keep it.
10. **Publish GitHub Release**:
   - Use the `gh` CLI to create the release using the version tag.
   - `gh release create v$RELEASE_VERSION --title "Release v$RELEASE_VERSION" --notes "<content from CHANGELOG for this version>"`
