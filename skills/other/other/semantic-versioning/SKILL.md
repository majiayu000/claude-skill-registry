---
name: semantic-versioning
description: Implement semantic versioning (SemVer) with automated release management. Use conventional commits, semantic-release, and version bumping strategies.
---

# Semantic Versioning

## Overview

Establish semantic versioning practices to maintain consistent version numbering aligned with release significance, enabling automated version management and release notes generation.

## When to Use

- Package and library releases
- API versioning
- Version bumping automation
- Release note generation
- Breaking change tracking
- Dependency management
- Changelog management

## Implementation Examples

### 1. **Semantic Versioning Configuration**

```yaml
# package.json
{
  "name": "my-awesome-package",
  "version": "1.2.3",
  "description": "An awesome package",
  "main": "dist/index.js",
  "repository": {
    "type": "git",
    "url": "https://github.com/org/repo.git"
  },
  "scripts": {
    "release": "semantic-release"
  },
  "devDependencies": {
    "semantic-release": "^21.0.0",
    "@semantic-release/changelog": "^6.0.0",
    "@semantic-release/git": "^10.0.0",
    "@semantic-release/github": "^9.0.0",
    "conventional-changelog-cli": "^3.0.0"
  }
}
```

### 2. **Conventional Commits Format**

```bash
# Feature commit (MINOR bump)
git commit -m "feat: add new search feature"
git commit -m "feat(api): add pagination support"

# Bug fix commit (PATCH bump)
git commit -m "fix: resolve null pointer exception"
git commit -m "fix(auth): fix login timeout issue"

# Breaking change (MAJOR bump)
git commit -m "feat!: redesign API endpoints"
git commit -m "feat(api)!: remove deprecated methods"

# Documentation
git commit -m "docs: update README"

# Performance improvement
git commit -m "perf: optimize database queries"

# Refactoring
git commit -m "refactor: simplify authentication logic"

# Tests
git commit -m "test: add integration tests"

# Chore
git commit -m "chore: update dependencies"

# Complete example with body and footer
git commit -m "feat(payment): add Stripe integration

Add support for processing credit card payments via Stripe.
Includes webhook handling for payment confirmations.

BREAKING CHANGE: Payment API endpoint changed from /pay to /api/v2/payments
Closes #123"
```

### 3. **Semantic Release Configuration**

```javascript
// release.config.js
module.exports = {
  branches: ['main', {name: 'develop', prerelease: 'beta'}],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    '@semantic-release/changelog',
    '@semantic-release/git',
    '@semantic-release/github',
    '@semantic-release/npm'
  ]
};
```

### 4. **Version Bumping Script**

```bash
#!/bin/bash
# bump-version.sh

CURRENT_VERSION=$(grep '"version"' package.json | head -1 | sed 's/.*"version": "\([^"]*\)".*/\1/')
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

case "${1:-patch}" in
  major)
    NEW_VERSION="$((MAJOR + 1)).0.0"
    ;;
  minor)
    NEW_VERSION="$MAJOR.$((MINOR + 1)).0"
    ;;
  patch)
    NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"
    ;;
  *)
    echo "Usage: $0 {major|minor|patch}"
    exit 1
    ;;
esac

echo "Bumping version from $CURRENT_VERSION to $NEW_VERSION"

# Update package.json
npm version $NEW_VERSION --no-git-tag-v

# Update CHANGELOG
CHANGELOG_HEADER="## [$NEW_VERSION] - $(date +%Y-%m-%d)"
sed -i "1i\\$CHANGELOG_HEADER" CHANGELOG.md

# Commit and tag
git add package.json CHANGELOG.md package-lock.json
git commit -m "chore(release): version $NEW_VERSION"
git tag -a "v$NEW_VERSION" -m "Release $NEW_VERSION"

echo "✅ Version bumped to $NEW_VERSION"
```

### 5. **Changelog Generation**

```bash
#!/bin/bash
# generate-changelog.sh

# Using conventional-changelog CLI
conventional-changelog -p angular -i CHANGELOG.md -s

# Or manually format changelog
CHANGELOG="# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description

### Changed
- Changed feature description

### Deprecated
- Deprecated feature description

### Removed
- Removed feature description

### Fixed
- Bug fix description

### Security
- Security fix description

## [1.2.0] - 2024-01-15

### Added
- New search functionality
- Support for pagination

### Fixed
- Critical security vulnerability in authentication
- Memory leak in cache manager"

echo "$CHANGELOG" > CHANGELOG.md
```

### 6. **GitHub Actions Release Workflow**

```yaml
name: Semantic Release
on: [push, workflow_dispatch]
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - run: npm run build
      - uses: cycjimmy/semantic-release-action@v3
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Best Practices

### ✅ DO
- Follow strict MAJOR.MINOR.PATCH format
- Use conventional commits
- Automate version bumping
- Generate changelogs automatically
- Tag releases in git
- Document breaking changes
- Use prerelease versions for testing

### ❌ DON'T
- Manually bump versions inconsistently
- Skip breaking change documentation
- Use arbitrary version numbering
- Mix features in patch releases

## Version Examples

```
1.0.0 → First release
1.1.0 → New feature
1.1.1 → Bug fix
2.0.0 → Breaking changes
2.0.0-beta.1 → Beta
```

## Resources

- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
