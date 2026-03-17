---
name: github-repository-architect
description: Complete GitHub repository setup with production-grade standards including community health files, CI/CD workflows, issue templates, documentation site, badges, CODEOWNERS, and release management. Handles initialization, configuration, GitHub Pages deployment, and automated quality checks for professional open-source or enterprise projects.
---

# GitHub Repository Architect

Expert in creating production-ready GitHub repositories from scratch with comprehensive infrastructure, automation, and community standards. Provides end-to-end setup for open-source projects, enterprise codebases, and documentation sites with industry best practices.

## Core Competencies

### 1. Repository Foundation
- **Initialization**: Git configuration, .gitignore, license selection, README structure
- **Branch Strategy**: Main/develop branches, protection rules, merge policies
- **Access Control**: Team permissions, CODEOWNERS, branch protection
- **Repository Settings**: Features enablement, security policies, merge options
- **Topics & Metadata**: Discoverability optimization, GitHub search ranking

### 2. Community Health Files
- **README.md**: Project overview, quick start, badges, contributing links
- **LICENSE**: License selection and proper copyright attribution  
- **CODE_OF_CONDUCT.md**: Community standards and enforcement
- **CONTRIBUTING.md**: Contribution guidelines and development workflow
- **SECURITY.md**: Security policy and vulnerability reporting
- **CHANGELOG.md**: Version history following Keep a Changelog format
- **CITATION.cff**: Academic citation support (Citation File Format)

### 3. Issue & PR Templates
- **Issue Templates**: Bug reports, feature requests, documentation improvements
- **Pull Request Template**: PR description structure, checklist, review guidelines
- **Discussion Templates**: Q&A, ideas, announcements (if Discussions enabled)
- **Custom Forms**: GitHub issue forms with type validation
- **Auto-labeling**: Automatic label application based on issue type

### 4. CI/CD Automation
- **GitHub Actions**: Automated testing, linting, building, deployment
- **Quality Gates**: Code coverage, security scanning, dependency audits
- **Release Automation**: Semantic versioning, changelog generation, asset publishing
- **Documentation Deployment**: GitHub Pages auto-deployment on push
- **Dependency Management**: Dependabot, automated PR creation for updates

### 5. Documentation Site
- **GitHub Pages**: Static site deployment (Jekyll, Docsify, MkDocs, or custom)
- **Site Structure**: Hierarchical navigation, search functionality
- **Custom Domain**: DNS configuration and HTTPS setup
- **SEO Optimization**: Meta tags, sitemaps, structured data
- **Mobile Responsive**: Cross-device compatibility testing

## Implementation Phases

### Phase 1: Repository Initialization (30 min)

**Step 1: Local Repository Setup**
```bash
# Initialize git repository
git init
git branch -M main

# Create essential files
touch README.md LICENSE .gitignore

# First commit
git add .
git commit -m "chore: initialize repository"
```

**Step 2: GitHub Repository Creation**
```bash
# Create on GitHub (via gh CLI)
gh repo create OWNER/REPO --public --source=. --remote=origin

# Or use GitHub web interface for more options
```

**Step 3: Repository Settings**
- Enable Issues, Discussions, Projects (as needed)
- Disable Wiki (if using external docs)
- Set default branch to `main`
- Configure merge options (squash, rebase, merge commits)
- Enable "Automatically delete head branches"

### Phase 2: Community Health Files (45 min)

**README.md Template:**
```markdown
# Project Name

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/OWNER/REPO/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPO/actions)

**One-sentence project description**

## Features

- Feature 1
- Feature 2
- Feature 3

## Quick Start

\`\`\`bash
# Installation
npm install @org/package

# Usage
import { function } from '@org/package'
\`\`\`

## Documentation

Full documentation: [https://owner.github.io/repo](https://owner.github.io/repo)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

[MIT License](LICENSE) - see LICENSE file for details.
```

**LICENSE Selection Guide:**
- **MIT**: Permissive, simple, widely used (recommended for most projects)
- **Apache 2.0**: Patent grant protection, enterprise-friendly
- **GPL v3**: Copyleft, derivatives must be open-source
- **CC BY-NC-ND 4.0**: Creative Commons for non-code content (documentation, frameworks)
- **Proprietary**: Custom license for closed-source with limited distribution

**CODE_OF_CONDUCT.md:**
Use Contributor Covenant (industry standard):
```bash
# Via gh CLI
gh repo create-conduct

# Or download from https://www.contributor-covenant.org/
```

**CONTRIBUTING.md Structure:**
1. Getting Started (development environment setup)
2. Development Workflow (branch naming, commit messages)
3. Pull Request Process (review criteria, testing requirements)
4. Code Style Guidelines (linting, formatting)
5. Testing Requirements (coverage thresholds, test types)
6. Documentation Standards (inline comments, external docs)

**SECURITY.md:**
```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**DO NOT** open a public issue for security vulnerabilities.

Email: security@example.com

Expected response time: 48 hours
```

**CHANGELOG.md:**
Follow [Keep a Changelog](https://keepachangelog.com/) format:
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-11-01

### Added
- Initial release
- Feature X
- Feature Y

### Changed
- Updated dependency Z

### Fixed
- Bug fix for issue #123
```

**CITATION.cff:**
```yaml
cff-version: 1.2.0
title: "Project Name"
message: "If you use this software, please cite it as below."
type: software
authors:
  - family-names: Last
    given-names: First
    email: author@example.com
    orcid: "https://orcid.org/0000-0000-0000-0000"
repository-code: "https://github.com/OWNER/REPO"
url: "https://owner.github.io/repo"
license: MIT
version: 1.0.0
date-released: 2025-11-01
```

### Phase 3: Issue & PR Templates (30 min)

**Directory Structure:**
```text
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   ├── feature_request.md
│   └── documentation.md
├── PULL_REQUEST_TEMPLATE.md
└── CODEOWNERS
```

**Bug Report Template (.github/ISSUE_TEMPLATE/bug_report.md):**
```markdown
---
name: Bug Report
about: Report a bug or unexpected behavior
title: "[BUG] "
labels: bug
assignees: ''
---

## Description
A clear description of the bug.

## Steps to Reproduce
1. Step 1
2. Step 2
3. See error

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- OS: [e.g., macOS 14.0]
- Version: [e.g., 1.0.0]
- Node: [e.g., 20.10.0]

## Additional Context
Screenshots, logs, or other context.
```

**Feature Request Template:**
```markdown
---
name: Feature Request
about: Suggest a new feature or enhancement
title: "[FEATURE] "
labels: enhancement
assignees: ''
---

## Problem Statement
What problem does this solve?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches you've thought about.

## Additional Context
Any other relevant information.
```

**Pull Request Template (.github/PULL_REQUEST_TEMPLATE.md):**
```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to break)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added covering changes
- [ ] All tests passing
- [ ] CHANGELOG.md updated

## Related Issues
Closes #(issue number)
```

**CODEOWNERS (.github/CODEOWNERS):**
```text
# Global owners
* @organization/maintainers

# Specific paths
/docs/ @organization/docs-team
/src/ @organization/core-team
/.github/ @organization/devops-team
/tests/ @organization/qa-team
```

### Phase 4: CI/CD Workflows (60 min)

**Lint Workflow (.github/workflows/lint.yml):**
```yaml
name: Lint

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run ESLint
        run: npm run lint
      
      - name: Run Prettier
        run: npm run format:check
```

**Test Workflow (.github/workflows/test.yml):**
```yaml
name: Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [18.x, 20.x]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```

**Release Workflow (.github/workflows/release.yml):**
```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false
```

**GitHub Pages Deploy (.github/workflows/pages.yml):**
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Build site
        run: |
          # Build commands here
          npm run build:docs
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./docs

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Phase 5: Documentation Site (60 min)

**Option 1: Docsify (Recommended for simplicity)**

1. Create `docs/` directory structure:
```text
docs/
├── index.html (Docsify config)
├── README.md (Home page)
├── _sidebar.md (Navigation)
├── guide/
│   ├── getting-started.md
│   └── advanced.md
└── reference/
    ├── api.md
    └── cli.md
```

2. `docs/index.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Project Documentation</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify/lib/themes/vue.css">
</head>
<body>
  <div id="app"></div>
  <script>
    window.$docsify = {
      name: 'Project Name',
      repo: 'https://github.com/owner/repo',
      loadSidebar: true,
      subMaxLevel: 2,
      search: 'auto'
    }
  </script>
  <script src="//cdn.jsdelivr.net/npm/docsify/lib/docsify.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/search.min.js"></script>
</body>
</html>
```

3. `docs/_sidebar.md`:
```markdown
- [Home](/)
- [Getting Started](guide/getting-started.md)
- [API Reference](reference/api.md)
```

**Option 2: Jekyll (GitHub Pages default)**

1. Create `_config.yml`:
```yaml
title: Project Documentation
description: Project description
theme: jekyll-theme-cayman
markdown: kramdown
```

2. Enable GitHub Pages in repository settings
3. Select source: `main` branch, `/docs` folder

**Option 3: MkDocs (Python-based, feature-rich)**

1. Install: `pip install mkdocs mkdocs-material`
2. Initialize: `mkdocs new .`
3. Configure `mkdocs.yml`
4. Build: `mkdocs build`
5. Deploy: `mkdocs gh-deploy`

### Phase 6: Badges & Metadata (15 min)

**Essential Badges:**
```markdown
[![Version](https://img.shields.io/github/v/release/OWNER/REPO)](https://github.com/OWNER/REPO/releases)
[![License](https://img.shields.io/github/license/OWNER/REPO)](LICENSE)
[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPO/actions)
[![Coverage](https://codecov.io/gh/OWNER/REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/OWNER/REPO)
[![npm](https://img.shields.io/npm/v/@org/package)](https://www.npmjs.com/package/@org/package)
```

**Repository Topics:**
- Maximum 20 topics
- Use lowercase, hyphens for spaces
- Include: language, framework, use-case, industry
- Example: `typescript`, `api`, `mental-models`, `cognitive-framework`

**About Section:**
- Concise description (160 chars max)
- Include primary use case
- Add website URL if applicable
- Select appropriate topics

## Quality Checklist

### Repository Health ✅
- [ ] README with badges, quick start, and documentation links
- [ ] LICENSE file present and appropriate
- [ ] CODE_OF_CONDUCT.md following Contributor Covenant
- [ ] CONTRIBUTING.md with clear guidelines
- [ ] SECURITY.md with vulnerability reporting process
- [ ] CHANGELOG.md following Keep a Changelog format
- [ ] .gitignore appropriate for project type

### Automation ✅
- [ ] CI workflow testing on push/PR
- [ ] Linting workflow enforcing code style
- [ ] Security scanning (Dependabot, CodeQL)
- [ ] Automated releases on version tags
- [ ] Documentation deployment on main branch push

### Templates ✅
- [ ] Bug report template
- [ ] Feature request template
- [ ] Pull request template with checklist
- [ ] CODEOWNERS file for automatic review assignment

### Documentation ✅
- [ ] GitHub Pages enabled and deploying
- [ ] Navigation structure clear and hierarchical
- [ ] Search functionality working
- [ ] Mobile-responsive design
- [ ] All links functional

### Metadata ✅
- [ ] Repository description set
- [ ] Topics configured (10-20 relevant tags)
- [ ] Website URL added (if applicable)
- [ ] Social preview image (1280x640px)

## Best Practices

### Branch Protection Rules
```text
Settings → Branches → Add rule

Branch name pattern: main

Protection settings:
✅ Require pull request before merging
  ✅ Require approvals (1-2)
  ✅ Dismiss stale reviews
✅ Require status checks to pass
  ✅ Require branches to be up to date
✅ Require conversation resolution before merging
✅ Require signed commits (optional, high security)
✅ Include administrators (recommended)
```

### Semantic Versioning
```text
MAJOR.MINOR.PATCH (e.g., 2.1.3)

MAJOR: Breaking changes
MINOR: New features (backwards compatible)
PATCH: Bug fixes (backwards compatible)

Pre-release: 1.0.0-alpha.1, 1.0.0-beta.2, 1.0.0-rc.1
Build metadata: 1.0.0+20130313144700
```

### Commit Message Convention
```text
<type>(<scope>): <subject>

<body>

<footer>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation only
- style: Formatting, no code change
- refactor: Code change (neither fix nor feature)
- perf: Performance improvement
- test: Adding or updating tests
- chore: Maintenance (dependencies, config)
- ci: CI/CD changes

Examples:
feat(api): add mental model search endpoint
fix(parser): handle empty input gracefully
docs(readme): update installation instructions
```

### Release Process
```bash
# 1. Update version
npm version [patch|minor|major]

# 2. Update CHANGELOG.md
# Add new version section with changes

# 3. Commit changes
git add .
git commit -m "chore: release v1.2.0"

# 4. Create and push tag
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin main --tags

# 5. GitHub Actions automatically creates release
# Or manually via gh CLI:
gh release create v1.2.0 --title "v1.2.0" --notes-file RELEASE_NOTES.md
```

## Common Pitfalls

### Pitfall 1: Incomplete .gitignore
**Problem:** Sensitive files or build artifacts committed  
**Solution:** Use gitignore.io templates, review before first commit

### Pitfall 2: No Branch Protection
**Problem:** Direct pushes to main, untested code in production  
**Solution:** Enable branch protection immediately after repo creation

### Pitfall 3: Unclear Contributing Guidelines
**Problem:** Poor quality PRs, inconsistent code style  
**Solution:** Detailed CONTRIBUTING.md with examples and linting automation

### Pitfall 4: Missing CI/CD
**Problem:** Broken code merged, manual deployment friction  
**Solution:** Set up basic CI before accepting first PR

### Pitfall 5: Stale Documentation
**Problem:** Docs out of sync with code  
**Solution:** Automate docs deployment, make docs updates part of PR checklist

## Resources

- **GitHub Docs**: <https://docs.github.com>
- **Keep a Changelog**: <https://keepachangelog.com>
- **Semantic Versioning**: <https://semver.org>
- **Contributor Covenant**: <https://www.contributor-covenant.org>
- **Citation File Format**: <https://citation-file-format.github.io>
- **GitHub Actions Marketplace**: <https://github.com/marketplace?type=actions>

## Success Criteria

**Production-ready repository includes:**
1. ✅ All community health files present and complete
2. ✅ Automated testing and linting via GitHub Actions
3. ✅ Branch protection preventing untested code in main
4. ✅ Clear contribution guidelines and templates
5. ✅ GitHub Pages documentation site live
6. ✅ Proper versioning and release automation
7. ✅ Security policy and vulnerability reporting process
8. ✅ Repository discoverable via topics and description

**Repository fails if:**
1. ❌ Missing LICENSE or unclear licensing
2. ❌ No CI/CD, manual testing only
3. ❌ Direct commits to main possible
4. ❌ No documentation or stale docs
5. ❌ No contribution guidelines
6. ❌ Security vulnerabilities in dependencies
