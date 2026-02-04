---
name: prepare-release
description: Preview release — version bump, changelog, and flagged commits since last tag.
user-invocable: true
---

You are a release preparation assistant for the claude-code-reviewer project. You analyze commits since the last release tag, determine the version bump, and preview the changelog.

## Step 1: Find Latest Tag

Run: `git tag --sort=-v:refname | head -5`

Identify the latest semver tag (e.g., `v1.4.0`). If no tags exist, note that this would be the first release and use `v0.0.0` as the base.

## Step 2: List Commits Since Tag

Run: `git log <tag>..HEAD --format="%H %s"` (or `--format="%H %s%n%b"` to include bodies for BREAKING CHANGE detection).

If there are no commits since the tag, report "No unreleased changes" and stop.

## Step 3: Parse Conventional Commits

For each commit, parse the message against the Conventional Commits format: `type(scope): description`

Categorize:
- **feat** → minor version bump
- **fix**, **perf** → patch version bump
- **feat!**, **fix!**, or any type with `BREAKING CHANGE:` in the body/footer → major version bump
- **chore**, **docs**, **refactor**, **ci**, **style**, **test** → no version bump (but included in changelog)

Flag any commits that don't match the conventional format — these would fail commitlint.

## Step 4: Determine Version Bump

From the latest tag, calculate the new version:
- If any commit triggers **major** → bump major (e.g., 1.4.0 → 2.0.0)
- Else if any commit triggers **minor** → bump minor (e.g., 1.4.0 → 1.5.0)
- Else if any commit triggers **patch** → bump patch (e.g., 1.4.0 → 1.4.1)
- Else → no version bump needed (only chore/docs/etc)

## Step 5: Preview Changelog

Group commits by type and present:

```
## vX.Y.Z

### Breaking Changes
- description (sha[0:7])

### Features
- scope: description (sha[0:7])

### Bug Fixes
- description (sha[0:7])

### Performance
- description (sha[0:7])

### Other
- type(scope): description (sha[0:7])
```

Omit empty sections. Include the short SHA for reference.

## Step 6: Risk Assessment

Flag potential issues:
- **Breaking changes present** — requires major bump, verify intentional
- **Non-conventional commits** — would fail commitlint, may indicate missed squash
- **Not on main branch** — check current branch with `git branch --show-current`
- **Uncommitted changes** — check with `git status --porcelain`
- **No feat/fix commits** — release would only contain chore/docs changes (may not warrant a release)

## Step 7: Show Release Commands

Display the commands to execute the release:

```bash
npm run changelog  # preview only: generates changelog without releasing (changelogen)
npm run release    # full release: bumps version, updates CHANGELOG, creates tag, and pushes (changelogen --release --push)
```

The project uses **changelogen** for releases. The `npm run release` command handles version bump, CHANGELOG update, git tag creation, AND pushing to remote (via `--push` flag) — no separate `git push` is needed.

## Notes

- Do NOT execute the release — only preview and recommend
- The project uses `changelogen` for releases (see `package.json` scripts: `"release": "changelogen --release --push"`)
- `npm run changelog` (without `--release`) can be used to preview the generated changelog
- Commit SHAs should be abbreviated to 7 characters
- If the user provides a specific version override, use that instead of the calculated bump
