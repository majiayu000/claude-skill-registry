---
name: generate-changelog
description: "Create changelog from git commits. Use when preparing release notes."
mcp_fallback: none
category: generation
tier: 2
user-invocable: false
---

# Generate Changelog

Automatically extract commit messages and generate formatted changelog entries for release notes and version history.

## When to Use

- Preparing release notes
- Documenting version history
- Creating user-facing change summaries
- Generating development notes

## Quick Reference

```bash
# Extract commits since last tag
git log v1.0.0..HEAD --pretty=format:"%h - %s (%an) %d"

# Group by conventional commit type
git log --pretty=format:"%h %s" | grep -E "^[a-f0-9]+ (feat|fix|docs|refactor|test):"

# Generate markdown changelog
git log --reverse --pretty=format:"- %s (%h)" > CHANGELOG.md
```

## Workflow

1. **Extract commits**: Get commit messages since last release
2. **Parse convention**: Identify conventional commit types (feat, fix, docs, etc.)
3. **Categorize changes**: Group into sections (Features, Fixes, Documentation, etc.)
4. **Format output**: Create readable markdown or text format
5. **Add context**: Include version number, date, and links

## Output Format

Changelog entry:

- Version number and release date
- Features section (new capabilities)
- Fixes section (bug fixes)
- Documentation section (doc updates)
- Breaking changes (if any)
- Contributors
- Version links (GitHub compare)

## References

- See `doc-update-blog` skill for blog post updates
- See git documentation for commit message conventions
- See <https://keepachangelog.com/> for changelog format standards
