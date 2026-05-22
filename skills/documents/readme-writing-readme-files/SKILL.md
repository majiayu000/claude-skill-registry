---
description: README quality standards for engaging, accessible, scannable content including problem-solution hooks, plain language (no unexplained jargon), acronym context, paragraph limits (≤5 lines), benefits-focused language, visual hierarchy, and progressive disclosure. Essential for creating effective README files that welcome and guide users.
---

# Writing README Files

## Purpose

This Skill provides comprehensive guidance for writing **high-quality README files** that are engaging, accessible, and scannable. READMEs serve as the entry point for repositories, projects, and directories, requiring special attention to clarity, structure, and user experience.

**When to use this Skill:**

- Creating repository README.md files
- Writing project/package README files
- Creating directory README files for navigation
- Updating existing READMEs for clarity
- Reviewing READMEs for quality standards

## Core README Principles

### Problem-Solution Hook

**Start with WHY**: Begin with a clear problem-solution hook that immediately shows value.

✅ **Good opening**:

```markdown
# Project Name

**Problem**: Managing enterprise Shariah-compliant rules is complex and time-consuming.
**Solution**: Open Sharia Enterprise provides automated, validated rule management.
```

❌ **Weak opening**:

```markdown
# Project Name

This is a project that does things.
```

### Plain Language Requirement

**Avoid unexplained jargon**: Use plain language and explain technical terms on first use.

✅ **Good**:

```markdown
Uses **Nx** (a monorepo build system) to manage multiple applications.
```

❌ **Bad**:

```markdown
Uses Nx for the monorepo. ← What's Nx? What's a monorepo?
```

**Acronym Context**: Define acronyms on first use.

✅ **Good**: `WCAG (Web Content Accessibility Guidelines)`
❌ **Bad**: `WCAG compliance required`

### Paragraph Length Limit

**Maximum 5 lines per paragraph**: Keep paragraphs scannable.

✅ **Good**:

```markdown
This project uses Volta for Node.js version management. Volta automatically
switches to the correct Node.js and npm versions based on package.json
configuration. This ensures all developers have identical environments.

Benefits include simplified onboarding and zero version conflicts.
```

❌ **Bad** (8 lines in one paragraph):

```markdown
This project uses Volta for Node.js version management which automatically
switches to the correct Node.js and npm versions based on package.json
configuration ensuring all developers have identical environments and this
provides benefits including simplified onboarding and zero version conflicts
and removes the need for manual version switching and solves many common
environment-related issues that teams face when working with different
Node.js versions across development, staging, and production environments.
```

### Benefits-Focused Language

**Emphasize outcomes, not features**: Show WHAT users gain, not just WHAT the system does.

✅ **Benefits-focused**:

```markdown
## Key Benefits

- **Faster Development**: Automated code generation reduces boilerplate by 70%
- **Fewer Bugs**: Type-safe APIs catch errors at compile time
- **Easier Onboarding**: Standardized structure helps new developers start quickly
```

❌ **Feature-focused**:

```markdown
## Features

- Has code generation
- Uses TypeScript
- Has standardized folder structure
```

### Visual Hierarchy and Structure

**Use headings, lists, and formatting to create scannable structure:**

- **H2 for major sections**: ## Installation, ## Usage, ## Contributing
- **Lists for steps**: Use ordered lists for sequential steps
- **Bold for emphasis**: Highlight key terms
- **Code blocks for commands**: Always format code properly
- **Tables for comparisons**: Use tables for structured data

### Progressive Disclosure

**Layer information from essential to detailed:**

1. **Above the fold**: Problem, solution, key benefits
2. **Quick start**: Minimal steps to get started
3. **Common use cases**: Typical workflows
4. **Detailed documentation**: Link to full docs
5. **Advanced topics**: Link to in-depth guides

## Standard README Structure

````markdown
# Project Name

Brief one-line description (what it does, who it's for)

[Optional: Badges for build status, version, license]

## Overview

Problem-solution hook (2-3 paragraphs max)

## Key Benefits

- Benefit 1
- Benefit 2
- Benefit 3

## Quick Start

```bash
# Minimal steps to run
npm install
npm start
```
````

## Installation

Detailed installation steps (if different from Quick Start)

## Usage

Common use cases with code examples

## Documentation

Links to full documentation

## Contributing

How to contribute (link to CONTRIBUTING.md)

## License

License type with link to LICENSE file

```

## Common Mistakes

### ❌ Mistake 1: Starting with features, not benefits

**Wrong**: Lists features without context
**Right**: Shows problem, solution, and benefits first

### ❌ Mistake 2: Unexplained acronyms

**Wrong**: "Supports WCAG, ARIA, WAI"
**Right**: "Supports WCAG (Web Content Accessibility Guidelines), ARIA (Accessible Rich Internet Applications), and WAI (Web Accessibility Initiative) standards"

### ❌ Mistake 3: Wall of text paragraphs

**Wrong**: 10+ line paragraphs that are hard to scan
**Right**: Max 5 lines per paragraph, use lists and headings

### ❌ Mistake 4: Missing context for jargon

**Wrong**: "Uses Nx monorepo with affected builds"
**Right**: "Uses **Nx** (a monorepo build system) to manage multiple apps. The 'affected' feature only rebuilds changed projects, saving time."

### ❌ Mistake 5: No quick start section

**Wrong**: Jumps directly into detailed installation
**Right**: Provides "Quick Start" with minimal steps, then detailed installation

## Quick Quality Checklist

- [ ] Problem-solution hook in first 2-3 paragraphs
- [ ] All acronyms explained on first use
- [ ] All jargon explained in plain language
- [ ] No paragraphs exceed 5 lines
- [ ] Benefits emphasized over features
- [ ] Clear visual hierarchy (headings, lists, formatting)
- [ ] Quick start section with minimal steps
- [ ] Code blocks properly formatted with language
- [ ] Links to detailed documentation
- [ ] Professional, welcoming tone

## References

**Primary Convention**: [README Quality Convention](../../../governance/conventions/content/readme-quality.md)

**Related Conventions**:

- [Content Quality Principles](../../../governance/conventions/content/quality.md) - Universal markdown standards
- [Accessibility First Principle](../../../governance/principles/content/accessibility-first.md) - Accessibility requirements

**Related Skills**:

- `docs__applying-content-quality` - Universal content quality standards

---

This Skill packages README quality standards for creating engaging, accessible, scannable entry points for repositories and projects. For comprehensive details, consult the primary convention document.
```
