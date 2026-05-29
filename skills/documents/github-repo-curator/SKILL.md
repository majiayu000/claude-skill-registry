---
name: github-repo-curator
description: Organize GitHub repositories for professional presentation and maintainability. README templates, documentation standards, repo organization patterns, and profile optimization. Triggers on GitHub cleanup, repo organization, README writing, or open source presentation requests.
license: MIT
---

# GitHub Repo Curator

Transform scattered repositories into professional portfolio.

## Profile Optimization

### Profile README

Create `[username]/[username]/README.md` for profile landing:

```markdown
# Hi, I'm [Name] 👋

[One-line positioning statement]

## 🔭 Currently Working On
- [Project 1] - [Brief description]
- [Project 2] - [Brief description]

## 🌱 Currently Learning
- [Technology/Skill]

## 💼 Professional Focus
[2-3 sentences about your work and interests]

## 📫 How to Reach Me
- [Email/LinkedIn/Website]

## 🛠️ Tech Stack
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
[Add relevant badges]

---
[Optional: GitHub stats, activity graph, etc.]
```

### Pinned Repositories

Pin 6 repositories that showcase:
1. **Best technical work** (most impressive)
2. **Most relevant to target role**
3. **Active/maintained project**
4. **Shows different skill** (range)
5. **Personal/passion project** (personality)
6. **Collaborative work** (teamwork)

---

## Repository Organization

### Naming Conventions

```
# Pattern: [type]-[name] or [name]-[technology]

# Good
portfolio-website
cli-tool-name
react-component-library
python-data-pipeline
api-gateway-service

# Avoid
test123
my-project
untitled
asdfgh
```

### Visibility Strategy

| Visibility | Use For |
|------------|---------|
| Public | Portfolio pieces, open source, learning |
| Private | Client work, incomplete projects, experiments |
| Archive | Completed/abandoned but worth keeping |
| Delete | Truly obsolete, embarrassing, or redundant |

### Repository Audit Checklist

For each repo, decide:
- [ ] Keep public (portfolio-worthy)
- [ ] Keep private (valuable but not showcase)
- [ ] Archive (done but reference value)
- [ ] Delete (no value)

---

## README Framework

### Minimal README

```markdown
# Project Name

Brief description of what this project does.

## Installation

```bash
npm install project-name
```

## Usage

```javascript
import { thing } from 'project-name';
thing.doSomething();
```

## License

MIT
```

### Standard README

```markdown
# Project Name

![Build Status](badge-url)
![License](badge-url)
![Version](badge-url)

One-paragraph description of the project: what it does, who it's for, 
and why it exists.

## Features

- ✅ Feature one
- ✅ Feature two
- ✅ Feature three

## Quick Start

### Prerequisites

- Node.js >= 18
- npm or yarn

### Installation

```bash
git clone https://github.com/user/project
cd project
npm install
```

### Usage

```bash
npm start
```

## Documentation

[Link to full docs or wiki]

## Contributing

[Link to CONTRIBUTING.md]

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE).

## Acknowledgments

- [Credit 1]
- [Credit 2]
```

### Comprehensive README

See `references/readme-template.md`

---

## Documentation Standards

### File Structure

```
project/
├── README.md           # Project overview
├── CONTRIBUTING.md     # How to contribute
├── LICENSE             # License file
├── CHANGELOG.md        # Version history
├── CODE_OF_CONDUCT.md  # Community standards
├── docs/               # Extended documentation
│   ├── getting-started.md
│   ├── api-reference.md
│   ├── examples.md
│   └── troubleshooting.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/      # GitHub Actions
└── src/                # Source code
```

### CONTRIBUTING.md Template

```markdown
# Contributing to [Project Name]

Thank you for your interest in contributing!

## How to Contribute

### Reporting Bugs

1. Check existing issues
2. Use the bug report template
3. Include reproduction steps

### Suggesting Features

1. Check existing feature requests
2. Use the feature request template
3. Explain the use case

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

[Instructions for local development]

## Code Style

[Style guidelines or link to linter config]

## Testing

[How to run tests]
```

### CHANGELOG.md Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- New feature X

### Changed
- Updated dependency Y

### Fixed
- Bug in feature Z

## [1.0.0] - 2024-01-15

### Added
- Initial release
- Feature A
- Feature B
```

---

## Badges

### Build & Status
```markdown
![Build Status](https://github.com/user/repo/workflows/CI/badge.svg)
![Coverage](https://codecov.io/gh/user/repo/branch/main/graph/badge.svg)
```

### Package Info
```markdown
![npm version](https://img.shields.io/npm/v/package-name)
![Downloads](https://img.shields.io/npm/dm/package-name)
```

### License & Social
```markdown
![License](https://img.shields.io/github/license/user/repo)
![Stars](https://img.shields.io/github/stars/user/repo)
![Forks](https://img.shields.io/github/forks/user/repo)
```

### Technology
```markdown
![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)
```

### Badge Generator
Use [shields.io](https://shields.io) for custom badges.

---

## Repository Cleanup Workflow

### Phase 1: Audit

1. List all repositories
2. Categorize by purpose/status
3. Identify gaps (what's missing?)
4. Flag for action (keep/archive/delete)

### Phase 2: Clean

1. Delete truly obsolete repos
2. Archive completed/abandoned
3. Make private anything not portfolio-ready
4. Update visibility settings

### Phase 3: Polish

1. Add/update READMEs
2. Add licenses
3. Update descriptions and topics
4. Add relevant badges
5. Clean up commit history if needed

### Phase 4: Present

1. Pin best repositories
2. Create/update profile README
3. Organize with topics/labels
4. Cross-link related projects

---

## Topics/Tags Strategy

### Use Topics For:
- Primary language: `python`, `typescript`, `rust`
- Framework: `react`, `nextjs`, `fastapi`
- Domain: `machine-learning`, `web-dev`, `cli`
- Type: `library`, `tool`, `template`, `tutorial`
- Status: `active`, `archived`, `experimental`

### Example Topic Set:
```
typescript react nextjs portfolio web-development
```

---

## Git Hygiene

### Commit Messages

```
type(scope): subject

body (optional)

footer (optional)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Branch Strategy

```
main          # Production-ready
develop       # Integration branch
feature/*     # New features
bugfix/*      # Bug fixes
release/*     # Release prep
hotfix/*      # Production fixes
```

### .gitignore Essentials

```gitignore
# Dependencies
node_modules/
venv/
.env

# Build
dist/
build/
*.pyc

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Secrets
*.pem
*.key
.env.local
```

---

## References

- `references/readme-template.md` - Full README template
- `references/license-guide.md` - Choosing a license
- `references/github-actions.md` - CI/CD workflows
