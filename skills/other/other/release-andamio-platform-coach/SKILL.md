---
name: release
description: Release a new version of Coach across all three distribution channels — Claude Code marketplace, npm, and GitHub.
license: MIT
metadata:
  author: Andamio
  version: 1.0.0
---

# Skill: Release

Publish a new version of Coach to all distribution channels.

## Instructions

### 1. Preflight Checks

Before starting, verify the release is ready:

- Confirm you are on the `main` branch: `git branch --show-current`
- Confirm the working tree is clean: `git status`
- If there are uncommitted changes, stop and ask the user to commit or stash first.

### 2. Determine Version Bump

Ask the user which version bump to apply:

```
What type of release is this?

1. Patch (x.x.1) — Wording improvements, typo fixes, minor knowledge corrections
2. Minor (x.1.0) — New skills, significant instruction rewrites, new knowledge seed patterns
3. Major (1.0.0) — Knowledge schema changes that break compound data, or skill removals
```

Read the current version from `package.json` (the `version` field) and compute the new version.

### 3. Generate Changelog Entry

Review what changed since the last release:

```bash
git log $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~10)..HEAD --oneline
```

If no tags exist yet, review all recent commits.

Draft a changelog entry in [Keep a Changelog](https://keepachangelog.com/) format. Group changes under the appropriate headings:

- **Added** — new skills, new features
- **Changed** — modifications to existing skills or knowledge
- **Fixed** — bug fixes, corrections
- **Removed** — removed skills or features

Present the draft to the user for approval before writing.

### 4. Apply Version Bump

After the user approves the changelog, update versions in all locations:

**4a. `package.json`**

Run `npm version <patch|minor|major> --no-git-tag-version` to bump the version without creating a git tag (we tag manually later).

**4b. `.claude-plugin/plugin.json`**

Update the `"version"` field to match the new version.

**4c. SKILL.md frontmatter**

For each skill that changed in this release, update `metadata.version` in its SKILL.md frontmatter to the new version. Skills that did not change keep their existing version.

**4d. `CHANGELOG.md`**

Insert the approved changelog entry at the top of the file (below the header, above the previous release). Add the release link at the bottom:

```markdown
[X.Y.Z]: https://github.com/Andamio-Platform/coach/releases/tag/vX.Y.Z
```

### 5. Commit and Tag

```bash
git add .
git commit -m "chore: release vX.Y.Z"
git tag vX.Y.Z
```

Do not push yet — confirm with the user first.

### 6. Publish to All Channels

Present the release summary and ask for confirmation:

```
Ready to publish vX.Y.Z to all channels:

1. GitHub — push main + tag
2. Claude Code marketplace — update andamio-marketplace version
3. npm — npm publish --access public (requires OTP)

Proceed?
```

On confirmation, execute in order:

**6a. GitHub**

```bash
git push origin main
git push origin vX.Y.Z
```

**6b. Claude Code Marketplace**

Read `~/projects/01-projects/andamio-marketplace/.claude-plugin/marketplace.json`. Update the coach plugin's `"version"` field to the new version. Commit and push:

```bash
cd ~/projects/01-projects/andamio-marketplace
git add .
git commit -m "chore: bump coach to vX.Y.Z"
git push origin main
```

**6c. npm**

```bash
cd ~/projects/01-projects/coach
npm publish --access public
```

The user will need to authenticate with an OTP. Wait for confirmation that it succeeded.

### 7. Create GitHub Release (Optional)

Ask the user if they want a GitHub release:

```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file - <<< "CHANGELOG_ENTRY_HERE"
```

### 8. Summary

Report what was published:

```
## Release Complete: vX.Y.Z

| Channel | Status | How users get it |
|---------|--------|------------------|
| GitHub | Pushed + tagged | git pull |
| Claude Code | Marketplace updated | /plugin marketplace update |
| npm | Published | npm update @andamio/coach |
| Community (SkillsMP, SkillHub) | Automatic | Crawlers re-index on their schedule |
```
