---
name: semantic-release
description: Automate versioning and releases with semantic versioning based on commit messages. Generate changelogs, publish packages, create GitHub releases. Use for automated releases, changelog generation, or npm publishing. Triggers on semantic-release, automated versioning, changelog, release automation.
---

# Semantic Release

Fully automated version management and package publishing.

## Quick Reference

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `fix:` | Patch (1.0.x) | Bug fixes |
| `feat:` | Minor (1.x.0) | New features |
| `BREAKING CHANGE:` | Major (x.0.0) | Breaking changes |
| `docs:`, `chore:` | No release | Documentation, maintenance |

## 1. Setup

### Installation

```bash
# npm
npm install -D semantic-release @semantic-release/changelog @semantic-release/git

# With plugins
npm install -D semantic-release \
  @semantic-release/commit-analyzer \
  @semantic-release/release-notes-generator \
  @semantic-release/changelog \
  @semantic-release/npm \
  @semantic-release/github \
  @semantic-release/git
```

### Basic Configuration (.releaserc.json)

```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    "@semantic-release/github",
    "@semantic-release/git"
  ]
}
```

## 2. Configuration Options

### Branch Configuration

```json
{
  "branches": [
    "main",
    { "name": "beta", "prerelease": true },
    { "name": "alpha", "prerelease": true },
    { "name": "next", "prerelease": true },
    { "name": "develop", "prerelease": "dev" },
    "+([0-9])?(.{+([0-9]),x}).x"
  ]
}
```

### Full Configuration (.releaserc.json)

```json
{
  "branches": ["main", { "name": "beta", "prerelease": true }],
  "plugins": [
    [
      "@semantic-release/commit-analyzer",
      {
        "preset": "conventionalcommits",
        "releaseRules": [
          { "type": "feat", "release": "minor" },
          { "type": "fix", "release": "patch" },
          { "type": "perf", "release": "patch" },
          { "type": "revert", "release": "patch" },
          { "type": "docs", "scope": "README", "release": "patch" },
          { "breaking": true, "release": "major" }
        ]
      }
    ],
    [
      "@semantic-release/release-notes-generator",
      {
        "preset": "conventionalcommits",
        "presetConfig": {
          "types": [
            { "type": "feat", "section": "Features" },
            { "type": "fix", "section": "Bug Fixes" },
            { "type": "perf", "section": "Performance" },
            { "type": "revert", "section": "Reverts" },
            { "type": "docs", "section": "Documentation", "hidden": false },
            { "type": "chore", "section": "Miscellaneous", "hidden": true }
          ]
        }
      }
    ],
    [
      "@semantic-release/changelog",
      {
        "changelogFile": "CHANGELOG.md",
        "changelogTitle": "# Changelog"
      }
    ],
    [
      "@semantic-release/npm",
      {
        "npmPublish": true
      }
    ],
    [
      "@semantic-release/github",
      {
        "assets": [
          { "path": "dist/**/*.js", "label": "Distribution" },
          { "path": "dist/**/*.d.ts", "label": "Type Definitions" }
        ],
        "successComment": false,
        "releasedLabels": ["released"]
      }
    ],
    [
      "@semantic-release/git",
      {
        "assets": ["CHANGELOG.md", "package.json", "package-lock.json"],
        "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
      }
    ]
  ]
}
```

## 3. Commit Message Format

### Conventional Commits

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Examples

```bash
# Patch release (1.0.0 -> 1.0.1)
git commit -m "fix: resolve login button alignment"

# Minor release (1.0.0 -> 1.1.0)
git commit -m "feat: add dark mode support"

# Major release (1.0.0 -> 2.0.0)
git commit -m "feat!: redesign API endpoints

BREAKING CHANGE: All API endpoints now use /v2/ prefix"

# With scope
git commit -m "feat(auth): implement OAuth2 login"

# With body and footer
git commit -m "fix(api): handle rate limiting errors

Added retry logic with exponential backoff.

Fixes #123
Reviewed-by: Jane Doe"
```

### Types Reference

| Type | Description | Release |
|------|-------------|---------|
| `feat` | New feature | Minor |
| `fix` | Bug fix | Patch |
| `docs` | Documentation | None* |
| `style` | Formatting | None |
| `refactor` | Code change (no feature/fix) | None |
| `perf` | Performance improvement | Patch |
| `test` | Adding tests | None |
| `chore` | Maintenance | None |
| `ci` | CI configuration | None |
| `build` | Build system | None |
| `revert` | Revert commit | Patch |

## 4. GitHub Actions Integration

### Basic Workflow

```yaml
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  issues: write
  pull-requests: write
  packages: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release
```

### With Build Step

```yaml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npm run build
      - run: npm test

      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release
```

### Multi-Package (Monorepo)

```yaml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        package: [core, cli, utils]
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm ci

      - name: Release ${{ matrix.package }}
        working-directory: packages/${{ matrix.package }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release
```

## 5. Plugin Configuration

### Commit Analyzer

```json
[
  "@semantic-release/commit-analyzer",
  {
    "preset": "conventionalcommits",
    "releaseRules": [
      { "type": "feat", "release": "minor" },
      { "type": "fix", "release": "patch" },
      { "type": "perf", "release": "patch" },
      { "type": "revert", "release": "patch" },
      { "type": "docs", "release": false },
      { "type": "style", "release": false },
      { "type": "refactor", "release": false },
      { "type": "test", "release": false },
      { "type": "chore", "release": false },
      { "scope": "no-release", "release": false }
    ],
    "parserOpts": {
      "noteKeywords": ["BREAKING CHANGE", "BREAKING CHANGES", "BREAKING"]
    }
  }
]
```

### Changelog Generator

```json
[
  "@semantic-release/changelog",
  {
    "changelogFile": "CHANGELOG.md",
    "changelogTitle": "# Changelog\n\nAll notable changes to this project will be documented in this file."
  }
]
```

### npm Plugin

```json
[
  "@semantic-release/npm",
  {
    "npmPublish": true,
    "tarballDir": "dist",
    "pkgRoot": "."
  }
]
```

### GitHub Plugin

```json
[
  "@semantic-release/github",
  {
    "assets": [
      { "path": "dist/*.tgz", "label": "npm package" },
      { "path": "dist/*.zip", "label": "Distribution (zip)" }
    ],
    "successComment": "This ${issue.pull_request ? 'PR' : 'issue'} is included in version ${nextRelease.version}",
    "failComment": "The release from branch ${branch.name} failed",
    "releasedLabels": ["released", "v${nextRelease.version}"],
    "addReleases": "bottom"
  }
]
```

### Git Plugin

```json
[
  "@semantic-release/git",
  {
    "assets": [
      "CHANGELOG.md",
      "package.json",
      "package-lock.json",
      "docs/**/*"
    ],
    "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
  }
]
```

## 6. Dry Run and Debugging

```bash
# Dry run (no actual release)
npx semantic-release --dry-run

# With debug output
DEBUG=semantic-release:* npx semantic-release

# Specific branch
npx semantic-release --branches beta

# Skip CI commit
npx semantic-release --ci false
```

## 7. Monorepo Support

### Using semantic-release-monorepo

```bash
npm install -D semantic-release-monorepo
```

```json
// packages/core/.releaserc.json
{
  "extends": "semantic-release-monorepo",
  "branches": ["main"],
  "tagFormat": "core-v${version}",
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/npm",
    "@semantic-release/github"
  ]
}
```

## 8. Private npm Registry

```json
{
  "plugins": [
    [
      "@semantic-release/npm",
      {
        "npmPublish": true
      }
    ]
  ]
}
```

```bash
# .npmrc
//registry.npmjs.org/:_authToken=${NPM_TOKEN}
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
@myorg:registry=https://npm.pkg.github.com
```

## 9. Complete Example

```json
{
  "branches": [
    "main",
    { "name": "beta", "prerelease": true },
    { "name": "alpha", "prerelease": true }
  ],
  "plugins": [
    [
      "@semantic-release/commit-analyzer",
      {
        "preset": "conventionalcommits",
        "releaseRules": [
          { "type": "feat", "release": "minor" },
          { "type": "fix", "release": "patch" },
          { "type": "perf", "release": "patch" },
          { "type": "revert", "release": "patch" },
          { "type": "docs", "scope": "README", "release": "patch" },
          { "breaking": true, "release": "major" }
        ]
      }
    ],
    [
      "@semantic-release/release-notes-generator",
      {
        "preset": "conventionalcommits",
        "presetConfig": {
          "types": [
            { "type": "feat", "section": "Features", "hidden": false },
            { "type": "fix", "section": "Bug Fixes", "hidden": false },
            { "type": "perf", "section": "Performance", "hidden": false },
            { "type": "revert", "section": "Reverts", "hidden": false },
            { "type": "docs", "section": "Documentation", "hidden": false },
            { "type": "style", "section": "Styles", "hidden": true },
            { "type": "chore", "section": "Miscellaneous", "hidden": true },
            { "type": "refactor", "section": "Code Refactoring", "hidden": true },
            { "type": "test", "section": "Tests", "hidden": true },
            { "type": "build", "section": "Build System", "hidden": true },
            { "type": "ci", "section": "CI/CD", "hidden": true }
          ]
        }
      }
    ],
    [
      "@semantic-release/changelog",
      {
        "changelogFile": "CHANGELOG.md"
      }
    ],
    "@semantic-release/npm",
    [
      "@semantic-release/github",
      {
        "assets": [
          { "path": "dist/**/*.js", "label": "Distribution" }
        ]
      }
    ],
    [
      "@semantic-release/git",
      {
        "assets": ["CHANGELOG.md", "package.json"],
        "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
      }
    ]
  ]
}
```

## Best Practices

1. **Enforce commit format** - Use commitlint with husky
2. **Protect main branch** - Require PRs and CI pass
3. **Use conventional commits** - Consistent commit messages
4. **Generate changelogs** - Document all changes
5. **Pin plugin versions** - Reproducible releases
6. **Dry run first** - Test before real release
7. **Token security** - Use GitHub secrets
8. **Skip CI on release commits** - Prevent loops
9. **Semantic versioning** - Follow semver strictly
10. **Branch strategy** - Use prerelease branches
