---
name: managing-docs
description: >
  Expert at organizing and managing documentation structure across projects. Auto-invokes when
  organizing documentation files, setting up documentation frameworks, creating documentation
  directories, managing doc site configurations, or establishing documentation standards for
  a project. Provides guidance on documentation architecture and tooling.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Managing Documentation Skill

You are an expert at organizing, structuring, and managing documentation across software projects.

## When This Skill Activates

This skill auto-invokes when:
- User asks about documentation structure or organization
- User wants to set up documentation for a project
- User needs to configure documentation tools (Sphinx, MkDocs, etc.)
- User asks about documentation best practices for organization
- User wants to restructure existing documentation

## Documentation Architecture Patterns

### Pattern 1: Simple Project (README-Centric)

Best for: Small projects, libraries, single-purpose tools

```
project/
├── README.md           # Main documentation
├── CONTRIBUTING.md     # Contribution guidelines
├── CHANGELOG.md        # Version history
├── LICENSE             # License file
└── docs/
    └── api.md          # API reference (if needed)
```

### Pattern 2: Standard Project (Docs Directory)

Best for: Medium projects, applications with multiple features

```
project/
├── README.md           # Overview and quick start
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
└── docs/
    ├── index.md        # Documentation home
    ├── getting-started.md
    ├── installation.md
    ├── configuration.md
    ├── usage/
    │   ├── basic.md
    │   └── advanced.md
    ├── api/
    │   ├── index.md
    │   └── [module].md
    ├── guides/
    │   └── [topic].md
    └── troubleshooting.md
```

### Pattern 3: Large Project (Full Documentation Site)

Best for: Large projects, frameworks, platforms

```
project/
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
└── docs/
    ├── mkdocs.yml          # Doc site config
    ├── index.md
    ├── getting-started/
    │   ├── index.md
    │   ├── installation.md
    │   ├── quick-start.md
    │   └── first-project.md
    ├── guides/
    │   ├── index.md
    │   └── [topic]/
    │       └── index.md
    ├── reference/
    │   ├── index.md
    │   ├── api/
    │   ├── cli/
    │   └── configuration/
    ├── tutorials/
    │   └── [tutorial]/
    ├── concepts/
    │   └── [concept].md
    ├── examples/
    │   └── [example]/
    └── contributing/
        ├── index.md
        ├── development.md
        └── style-guide.md
```

### Pattern 4: Monorepo Documentation

Best for: Monorepos with multiple packages

```
monorepo/
├── README.md               # Monorepo overview
├── docs/
│   ├── index.md           # Overall documentation
│   ├── architecture.md
│   └── packages.md
└── packages/
    ├── package-a/
    │   ├── README.md      # Package-specific docs
    │   └── docs/
    └── package-b/
        ├── README.md
        └── docs/
```

## Documentation Types

### 1. Reference Documentation
- API documentation
- Configuration options
- CLI commands
- Data types and schemas

**Characteristics:**
- Comprehensive and exhaustive
- Organized alphabetically or by module
- Auto-generated when possible
- Linked from tutorials and guides

### 2. Conceptual Documentation
- Architecture overviews
- Design decisions
- How things work internally
- Theoretical background

**Characteristics:**
- Explains the "why"
- Provides context
- Uses diagrams when helpful
- Links to reference docs

### 3. Procedural Documentation (How-To Guides)
- Step-by-step instructions
- Task-oriented content
- Specific goals in mind
- Common workflows

**Characteristics:**
- Numbered steps
- Clear prerequisites
- Expected outcomes
- Troubleshooting tips

### 4. Tutorial Documentation
- Learning-oriented content
- Hands-on exercises
- Progressive complexity
- Complete examples

**Characteristics:**
- Beginner-friendly
- Self-contained
- Working code included
- Builds on previous steps

## Documentation Tools Setup

### MkDocs (Python Projects)

**Installation:**
```bash
pip install mkdocs mkdocs-material
```

**Basic mkdocs.yml:**
```yaml
site_name: Project Name
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - search.highlight

nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quick-start.md
  - Guides:
    - guides/index.md
  - API Reference:
    - reference/index.md

plugins:
  - search
  - autorefs

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - admonition
  - toc:
      permalink: true
```

**Commands:**
```bash
mkdocs serve      # Local development server
mkdocs build      # Build static site
mkdocs gh-deploy  # Deploy to GitHub Pages
```

### Docusaurus (JavaScript Projects)

**Installation:**
```bash
npx create-docusaurus@latest docs classic
```

**Key Configuration (docusaurus.config.js):**
```javascript
module.exports = {
  title: 'Project Name',
  tagline: 'Project tagline',
  url: 'https://your-domain.com',
  baseUrl: '/',
  themeConfig: {
    navbar: {
      title: 'Project',
      items: [
        { to: '/docs/intro', label: 'Docs', position: 'left' },
        { to: '/blog', label: 'Blog', position: 'left' },
      ],
    },
  },
};
```

### Sphinx (Python API Docs)

**Installation:**
```bash
pip install sphinx sphinx-rtd-theme
sphinx-quickstart docs
```

**conf.py Setup:**
```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

html_theme = 'sphinx_rtd_theme'

# Napoleon settings for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
```

### TypeDoc (TypeScript Projects)

**Installation:**
```bash
npm install typedoc --save-dev
```

**typedoc.json:**
```json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs/api",
  "exclude": ["**/*.test.ts"],
  "excludePrivate": true,
  "includeVersion": true
}
```

## Documentation Standards

### File Naming Conventions

```
✓ getting-started.md      # Lowercase with hyphens
✓ api-reference.md        # Clear and descriptive
✓ installation.md         # Single word when possible

✗ GettingStarted.md       # No PascalCase
✗ getting_started.md      # No underscores
✗ GETTING-STARTED.md      # No all caps (except special files)
```

### Special Files

```
README.md       # Project overview (required)
CONTRIBUTING.md # Contribution guidelines
CHANGELOG.md    # Version history
LICENSE         # License text
CODE_OF_CONDUCT.md # Community standards
SECURITY.md     # Security policy
```

### Documentation Structure Checklist

**Project Root:**
- [ ] README.md with overview and quick start
- [ ] CONTRIBUTING.md with contribution guidelines
- [ ] CHANGELOG.md with version history
- [ ] LICENSE file

**Documentation Directory:**
- [ ] Clear navigation structure
- [ ] Getting started guide
- [ ] API/reference documentation
- [ ] Examples directory
- [ ] Search functionality (if using doc site)

**Individual Documents:**
- [ ] Clear title
- [ ] Table of contents (for long docs)
- [ ] Logical section organization
- [ ] Code examples where relevant
- [ ] Links to related content

## Versioned Documentation

For projects with multiple versions:

### Strategy 1: Branch-Based
```
docs/
├── latest/           # Symlink to current version
├── v2.0/
├── v1.5/
└── v1.0/
```

### Strategy 2: Docusaurus Versioning
```bash
npm run docusaurus docs:version 1.0
```

### Strategy 3: ReadTheDocs Versioning
Automatic version switching based on git tags.

## Migration Strategies

### Migrating to Docs Directory

1. Create `docs/` directory structure
2. Move inline docs to appropriate files
3. Update links and references
4. Add navigation configuration
5. Set up doc site generator (if using)
6. Redirect old documentation URLs

### Consolidating Documentation

1. Audit all existing documentation
2. Identify duplicates and conflicts
3. Create canonical versions
4. Remove or redirect duplicates
5. Update all internal links

## Automation

### GitHub Actions for Docs

```yaml
name: Deploy Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - run: pip install mkdocs-material
      - run: mkdocs gh-deploy --force
```

### Pre-commit Hooks for Docs

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.37.0
    hooks:
      - id: markdownlint
        args: ['--fix']
```

## Integration

This skill works with:
- **analyzing-docs** skill for assessing current documentation state
- **writing-docs** skill for creating documentation content
- **docs-analyzer** agent for comprehensive documentation projects
