---
name: releasing-plugin-versions
description: Use when releasing a new plugin version, bumping versions, creating git tags, or publishing GitHub releases for this marketplace
---

# Releasing Plugin Versions

## Critical Distinction

**`metadata.version` ≠ plugin version.** These are DIFFERENT things:

| Field               | What It Tracks                | When to Update               |
| ------------------- | ----------------------------- | ---------------------------- |
| `plugins[].version` | Individual plugin version     | Every plugin release         |
| `metadata.version`  | Marketplace catalog structure | Adding/removing plugins ONLY |

**Common mistake:** Thinking metadata.version should "stay in sync" with plugin versions. It should NOT.

## Plugin Version Locations (Update ALL 4)

When releasing a plugin (e.g., swift 1.2.0 → 1.3.0):

1. `plugins/swift/.claude-plugin/plugin.json` → `"version": "1.3.0"`
2. `.claude-plugin/marketplace.json` → `plugins[].version: "1.3.0"`
3. `plugins/swift/README.md` → Version section: `1.3.0`
4. `README.md` (root) → Available Plugins table: `1.3.0`

## Release Commands

```bash
# 1. Stage changes
git add -A

# 2. Commit
git commit -m "Release swift v1.3.0

- Description of changes"

# 3. Tag (format: v1.3.0, NOT swift-v1.3.0)
git tag v1.3.0

# 4. Push
git push && git push origin v1.3.0

# 5. GitHub release
gh release create v1.3.0 --title "v1.3.0" --notes "## Changes

- Change 1
- Change 2

**Full Changelog**: https://github.com/OWNER/REPO/compare/v1.2.0...v1.3.0"
```

## Tag Format

Use `v1.3.0`, NOT `swift-v1.3.0`. Check existing tags:

```bash
git tag --sort=-v:refname | head -5
```

## When NOT to Update metadata.version

- Releasing a new plugin version ❌
- Fixing plugin bugs ❌
- Adding features to existing plugins ❌
- Updating plugin documentation ❌

## When TO Update metadata.version

- Adding a NEW plugin to the catalog ✓
- Removing a plugin from the catalog ✓
- Changing marketplace owner/name ✓
