---
name: github-release
description: Use this skill when the user asks to "create a GitHub release", "publish a release", "make a release", "draft release notes", or needs guidance on using gh CLI to manage GitHub releases. This skill specializes in creating comprehensive, well-formatted GitHub releases using the GitHub CLI (gh).
version: 1.0.0
license: MIT
---

# GitHub Release Creation Skill

This skill helps you create professional, comprehensive GitHub releases using
the `gh` CLI tool. It covers release notes drafting, version management, and
best practices for open-source release communication.

## When to Use This Skill

Trigger this skill when you encounter requests like:

- "Create a GitHub release for version X.Y.Z"
- "Help me draft release notes"
- "Publish a release with these changes"
- "Compare version A.B.C and version X.Y.Z"
- "Make a release for this project"

## Prerequisites

1. **GitHub CLI (gh) must be installed and authenticated**
   ```bash
   gh auth status
   ```
   Should show: `✓ Logged in to github.com account <username>`

2. **Git repository should be properly tagged**
   ```bash
   git tag -l "v*"
   ```

## Core Concepts

### Version Numbering (Semantic Versioning)

- **Major (X.0.0)**: Breaking changes, major features
- **Minor (x.Y.0)**: New features, backward compatible
- **Patch (x.y.Z)**: Bug fixes, small improvements

### Release Types

- **Stable Release**: Final production-ready version (e.g., v4.0.0)
- **Pre-release**: Alpha, beta, or RC versions (e.g., v4.0.0-rc.1)
- **Draft Release**: Work-in-progress release notes

## Step-by-Step Release Creation Process

### Step 1: Analyze Changes Since Last Release

Identify the base version to compare against:

```bash
# Get latest tags
git tag -l "v*" --sort=-version:refname | head -5

# Get commits since last release
git log v3.3.0..HEAD --oneline

# Get detailed commit messages
git log v3.3.0..HEAD --pretty=format:"%h|%ad|%s" --date=short
```

Key information to extract:

- Commit count since last release
- Major features added
- Bug fixes and improvements
- Breaking changes (if any)
- Performance improvements
- Documentation updates

### Step 2: Determine Version Number

**Guidelines for choosing version numbers:**

| Scenario                               | Version Bump | Example                    |
| -------------------------------------- | ------------ | -------------------------- |
| New major features or breaking changes | Major        | v3.3.0 → v4.0.0            |
| New backward-compatible features       | Minor        | v3.3.0 → v3.4.0            |
| Bug fixes and minor improvements       | Patch        | v3.3.0 → v3.3.1            |
| Pre-release versions                   | Suffix       | v4.0.0-beta.1, v4.0.0-rc.1 |

**Questions to ask:**

- Does this introduce breaking changes? → Major bump
- Are there significant new features? → Minor bump
- Is it primarily bug fixes? → Patch bump

### Step 3: Draft Release Notes

Structure professional release notes with these sections:

#### 1. **Overview** (2-3 sentences)

- High-level summary of the release
- Key theme or focus area
- Version significance (major/minor/patch)

#### 2. **What's New** (categorized changes)

Organize changes by type:

- ✨ **Features**: New functionality
- 🔧 **Performance**: Speed/resource improvements
- 🐛 **Bug Fixes**: Resolved issues
- 📚 **Documentation**: Doc updates
- 💥 **Breaking Changes**: Incompatible changes (if any)
- ♻️ **Refactoring**: Code quality improvements

#### 3. **Comparison with Previous Version**

Create comparison tables showing behavior changes:

- Before (vX.Y.Z) → After (vX.Y.Z)
- Performance metrics
- Feature additions
- Configuration changes

#### 4. **Migration Guide** (if applicable)

- Configuration changes needed
- Breaking changes and how to adapt
- Deprecated features
- Upgrade steps

#### 5. **Installation Instructions**

```bash
# Docker
docker pull user/repo:version

# Build from source
git clone https://github.com/user/repo.git
cd repo
git checkout vX.Y.Z
go build -o binary ./cmd/

# Download binaries
# Link to release assets
```

#### 6. **Full Changelog**

List all commits with hashes and dates:

```markdown
### Commits since v3.3.0

- `9a8ebda` - Fix: Bypass internal HTTP proxy server (2026-01-09)
- `680f785` - Feat: Add SOCKS5 Direct Mode (2025-12-15)
```

#### 7. **Additional Sections** (as needed)

- Known Issues
- Credits/Contributors
- License information
- Related links

### Step 4: Create Git Tag

```bash
# Create annotated tag
git tag -a v4.0.0 -m "Release v4.0.0: Major performance improvements"

# Or create lightweight tag
git tag v4.0.0

# Push tag to GitHub
git push origin v4.0.0

# Or push all tags
git push origin --tags
```

### Step 5: Create GitHub Release Using gh CLI

#### Basic Release Creation

```bash
gh release create v4.0.0 \
  --title "v4.0.0 - Major Performance Release" \
  --notes "Release notes here..."
```

#### Advanced Options

```bash
# Create release from notes file
gh release create v4.0.0 \
  --title "v4.0.0" \
  --notes-file RELEASE_NOTES.md

# Create draft release (not published yet)
gh release create v4.0.0 \
  --title "v4.0.0" \
  --notes "Draft notes" \
  --draft

# Create pre-release
gh release create v4.0.0-beta.1 \
  --title "v4.0.0-beta.1" \
  --notes "Beta release notes" \
  --prerelease

# Release with target commit
gh release create v4.0.0 \
  --target main \
  --title "v4.0.0" \
  --notes "Release notes"

# Release from existing tag notes
gh release create v4.0.0 \
  --notes-tag \
  --title "v4.0.0"
```

#### Release with Assets

```bash
# Attach binaries
gh release create v4.0.0 \
  --title "v4.0.0" \
  --notes "Release notes" \
  ./dist/binary-linux-amd64 \
  ./dist/binary-darwin-amd64 \
  ./dist/binary-windows-amd64.exe

# Attach all files from directory
gh release create v4.0.0 \
  --title "v4.0.0" \
  --notes "Release notes" \
  ./dist/*
```

### Step 6: Publish and Verify

```bash
# View release
gh release view v4.0.0

# List all releases
gh release list

# Open in browser
gh browse --release v4.0.0

# Edit if needed
gh release edit v4.0.0 --notes "Updated notes"
```

## Release Notes Template

````markdown
# [Project Name] v[VERSION]

## 🎉 Overview

[2-3 sentence summary of the release]

## 🚀 What's New

### ✨ Features

- **Feature name**: Description of the feature
  - Technical details
  - Benefits for users

### 🔧 Performance Improvements

| Metric  | Previous Version | This Version | Improvement |
| ------- | ---------------- | ------------ | ----------- |
| Latency | ~100ms           | ~50ms        | 50% ↓       |
| Memory  | 100MB            | 85MB         | 15% ↓       |

### 🐛 Bug Fixes

- Fixed issue where [description]
- Resolved [problem] by [solution]

### 📚 Documentation

- Updated [file] with [information]
- Added guide for [topic]

## 📊 Comparison with v[PREVIOUS_VERSION]

### Behavior Changes

| Scenario  | v[PREVIOUS]  | v[CURRENT]       |
| --------- | ------------ | ---------------- |
| Feature A | Old behavior | **New behavior** |

### Technical Details

- **Architecture**: [description of changes]
- **Modified Files**:
  - [file1](link) - Change description
  - [file2](link) - Change description

## 🔄 Migration from v[PREVIOUS]

### ✅ No Configuration Changes Required

[If applicable: "This release is 100% backward compatible"]

### Breaking Changes

[If any: List breaking changes and migration steps]

## 🛠️ Installation

### Docker

```bash
docker pull user/repo:v[VERSION]
```
````

### Build from Source

```bash
git clone https://github.com/user/repo.git
cd repo
git checkout v[VERSION]
[build commands]
```

### Download Binaries

Download from [Releases](https://github.com/user/repo/releases) page.

## 📋 Full Changelog

### Commits since v[PREVIOUS]

- `hash` - **Type**: Description (date)
- `hash` - **Type**: Description (date)

## 🐛 Known Issues

[List any known issues or "None reported"]

## 🙏 Credits

Contributors:

- @username1
- @username2

## 📄 License

[License information]

## 🔗 Links

- [Documentation](link)
- [Migration Guide](link)
- [GitHub Repository](link)

---

**Full Changelog**:
https://github.com/user/repo/compare/v[PREVIOUS]...v[CURRENT]

````
## Best Practices

### DO ✅

1. **Use semantic versioning** consistently
2. **Write comprehensive release notes** that stand alone
3. **Include installation instructions** for common use cases
4. **Highlight breaking changes** prominently
5. **Credit contributors** who helped with the release
6. **Link to related issues/PRs** when relevant
7. **Use consistent formatting** (Markdown tables, code blocks)
8. **Test the release process** on a test repository first
9. **Keep release notes concise but complete**
10. **Include comparison data** for performance changes

### DON'T ❌

1. **NEVER create releases without proper tagging**
2. **NEVER skip authentication check** before creating releases
3. **NEVER publish release notes without review**
4. **DON'T use internal jargon** without explanation
5. **DON'T forget to verify** the release after creation
6. **DON'T create major releases** for trivial changes
7. **DON'T skip backward compatibility notes** for breaking changes
8. **DON'T forget to push tags** to remote repository
9. **DON'T use vague commit messages** (improves changelog quality)
10. **NEVER release untested code** to production

## Common Workflows

### Workflow 1: Regular Feature Release

```bash
# 1. Checkout main branch
git checkout main
git pull

# 2. Review changes since last release
git tag -l "v*" --sort=-version:refname | head -1
git log v3.3.0..HEAD --oneline

# 3. Determine version (e.g., v3.4.0 for new features)

# 4. Create tag
git tag -a v3.4.0 -m "Release v3.4.0: New features and improvements"
git push origin v3.4.0

# 5. Create release (from prepared notes file)
gh release create v3.4.0 \
  --title "v3.4.0 - New Features" \
  --notes-file RELEASE_NOTES.md
````

### Workflow 2: Hotfix Patch Release

```bash
# 1. Create hotfix branch
git checkout -b hotfix/critical-bug-fix

# 2. Make fix and commit
git commit -m "fix: Critical security vulnerability"

# 3. Create patch tag
git tag -a v3.3.1 -m "Release v3.3.1: Critical security fix"
git push origin hotfix/critical-bug-fix v3.3.1

# 4. Create release with urgent notes
gh release create v3.3.1 \
  --title "v3.3.1 - Security Fix" \
  --notes "## 🚨 Security Fix

This release addresses a critical security vulnerability.

**Upgrade immediately if you are affected.**

[Fix details]"
```

### Workflow 3: Major Version Release

```bash
# 1. Comprehensive changelog analysis
git log v3.0.0..HEAD --pretty=format:"%h|%ad|%s" --date=short > changes.txt

# 2. Create migration guide
# Write MIGRATION.md with breaking changes

# 3. Create major tag
git tag -a v4.0.0 -m "Release v4.0.0: Major architecture improvements"
git push origin v4.0.0

# 4. Create comprehensive release
gh release create v4.0.0 \
  --title "v4.0.0 - Major Release" \
  --notes-file COMPREHENSIVE_NOTES.md \
  --draft

# 5. Review and publish
gh release view v4.0.0 --web
# (Review in browser, then publish when ready)
```

### Workflow 4: Pre-release (Beta/RC)

```bash
# 1. Create pre-release tag
git tag -a v4.0.0-beta.1 -m "Beta 1 for v4.0.0"
git push origin v4.0.0-beta.1

# 2. Create pre-release
gh release create v4.0.0-beta.1 \
  --title "v4.0.0-beta.1 - Testing Release" \
  --notes "## 🧪 Beta Release

This is a pre-release for testing purposes.

**Not recommended for production use.**

[Features to test]" \
  --prerelease

# 3. After testing, create final release
git tag -a v4.0.0 -m "Release v4.0.0"
git push origin v4.0.0
gh release create v4.0.0 --notes "Final release notes"
```

## Troubleshooting

### Issue: "gh not authenticated"

**Solution:**

```bash
gh auth login
gh auth status  # Verify
```

### Issue: "Tag not found"

**Solution:**

```bash
# Push tag first
git push origin <tag-name>

# Or verify tag exists
git tag -l | grep <tag-name>
```

### Issue: "Release already exists"

**Solution:**

```bash
# Delete existing release
gh release delete <tag-name> --yes

# Or edit existing release
gh release edit <tag-name> --notes "New notes"
```

### Issue: "Permission denied"

**Solution:**

- Verify repository permissions: `gh repo view`
- Check authentication: `gh auth status`
- Ensure you have admin/write access

## Additional Resources

- [GitHub Releases Documentation](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

## Tips for High-Quality Releases

1. **Start Early**: Begin drafting release notes during development
2. **Track Features**: Maintain a CHANGELOG.md file
3. **Communicate**: Use issues/PRs to discuss release plans
4. **Test Thoroughly**: Test installation instructions
5. **Be Honest**: Clearly document known issues
6. **Celebrate**: Highlight community contributions
7. **Stay Organized**: Use consistent structure across releases
8. **Provide Context**: Explain why changes matter to users
9. **Include Metrics**: Use data to demonstrate improvements
10. **Link Forward**: Point to next version or roadmap

## Example Commands Reference

```bash
# View all gh release commands
gh release --help

# Create release from stdin
echo "Release notes" | gh release create v1.0.0

# Create release with discussion
gh release create v1.0.0 \
  --discussion "Discuss v1.0.0 release"

# Delete release
gh release delete v1.0.0 --yes

# Download release assets
gh release download v1.0.0 \
  --dir ./downloads \
  --pattern "*.zip"

# List releases
gh release list \
  --limit 20 \
  --json name,tagName,publishedAt
```

---

**Remember**: Good releases communicate value, build trust, and make users
excited about your project!
