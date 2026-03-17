---
name: project-organization
description: Expert guidance for setting up and organizing research software projects following Sam Abbott's established patterns for R packages, Julia packages, and research projects
---

# Project Organization

Use this skill when creating new projects, scaffolding packages, or reviewing project structure to ensure consistency with established patterns.

## Quick Reference

**R packages**: See [R project patterns](references/r-projects.md)
**Julia packages**: See [Julia project patterns](references/julia-projects.md)

## Core Principles

### Project Root Structure

Every project should have:

```
project/
├── .claude/              # Claude Code project config (optional)
│   └── CLAUDE.md         # Or in project root
├── .github/              # GitHub Actions and templates
│   └── workflows/
├── .pre-commit-config.yaml
├── .gitignore
├── CLAUDE.md             # Project-specific instructions
├── LICENSE.md
├── NEWS.md               # Changelog
├── README.md             # Or README.Rmd for R
└── CITATION.cff          # Citation metadata
```

### CLAUDE.md Structure

Every project CLAUDE.md should include:

1. **Package/Project Overview** - What it does, core purpose
2. **Development Commands** - How to test, build, document
3. **Architecture** - Key components and their relationships
4. **Testing Patterns** - Framework, conventions, special considerations
5. **Code Style** - Language-specific guidelines beyond global rules

Template:
```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Package Overview

[Brief description of purpose and core functionality]

## Development Commands

```bash
# Key commands with comments
```

## Architecture

### Core Components

- **Component**: Description
- **Component**: Description

### Testing Patterns

[Framework, conventions, file naming]

## Code Style

[Project-specific rules beyond global CLAUDE.md]
```

### Pre-commit Hooks

All projects use pre-commit for automated quality checks:

```bash
# Install
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

Common hooks:
- Trailing whitespace removal
- End of file fixing
- Large file checks
- YAML validation
- Language-specific linting and formatting

## When to Use This Skill

Activate when:
- Creating a new R or Julia package
- Setting up a research project repository
- Reviewing project structure for consistency
- Adding configuration files to existing projects
- Scaffolding CI/CD workflows

For language-specific patterns, see the reference files.
