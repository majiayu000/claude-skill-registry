---
name: typo3-docs
description: "Create and maintain TYPO3 extension documentation following official docs.typo3.org standards. Use when creating/editing Documentation/*.rst files or README.md, using TYPO3 directives (confval, versionadded, card-grid, accordion, tabs, admonitions), creating/adding screenshots, rendering/testing/viewing docs locally, or deploying to docs.typo3.org. By Netresearch."
---

# TYPO3 Documentation Skill

Create and maintain TYPO3 extension documentation following official docs.typo3.org standards.

## Core Workflow

To create or maintain TYPO3 documentation, follow these steps:

1. Consult the appropriate reference file for the task
2. Use TYPO3-specific directives, not plain text
3. Run `scripts/validate_docs.sh` to check syntax
4. Run `scripts/render_docs.sh` to build HTML output
5. Verify rendered output visually in browser
6. Keep README.md and Documentation/ synchronized

> **Critical**: When the user asks to "show docs", render and display HTML output, not raw RST.

## Using Reference Documentation

### File Structure and Setup

When setting up documentation structure, consult `references/file-structure.md` for directory layout, file naming conventions, and required files.

When configuring guides.xml, consult `references/guides-xml.md` for build configuration, project metadata, and interlink settings.

When setting up editor configuration, consult `references/coding-guidelines.md` for .editorconfig requirements, indentation rules, and line length limits.

### RST Syntax and Elements

When writing RST content, consult `references/rst-syntax.md` for heading levels, lists, tables, and basic formatting.

When using inline code references, consult `references/text-roles-inline-code.md` for text roles like `:php:`, `:file:`, `:guilabel:`, and `:ref:`.

When documenting code, consult `references/code-structure-elements.md` for code blocks, literalinclude, confval directives, and PHP domain syntax.

When using TYPO3-specific directives, consult `references/typo3-directives.md` for confval, versionadded, versionchanged, deprecated, and other TYPO3 directives.

When creating interactive content, consult `references/content-directives.md` for accordion, tabs, card-grid, and admonition directives.

### Images and Screenshots

When adding screenshots, consult `references/screenshots.md` for image requirements, alt text, figure directives, and screenshot best practices.

### Rendering and Deployment

When rendering documentation locally, consult `references/rendering.md` for Docker commands, live preview, and troubleshooting.

When deploying to docs.typo3.org, consult `references/intercept-deployment.md` for webhook configuration, build triggers, and deployment verification.

### Advanced Topics

When writing Architecture Decision Records, consult `references/architecture-decision-records.md` for ADR templates, directory structure, and RST formatting.

When analyzing documentation coverage, consult `references/documentation-coverage-analysis.md` for feature coverage methodology and gap analysis.

When extracting documentation from code, consult `references/extraction-patterns.md` for automated extraction workflows and data flow.

When understanding TYPO3 extension structure, consult `references/typo3-extension-architecture.md` for file hierarchy and documentation priority weighting.

## Running Scripts

### Documentation Validation

To validate RST syntax before committing:

```bash
scripts/validate_docs.sh /path/to/extension
```

### Documentation Rendering

To render documentation to HTML:

```bash
scripts/render_docs.sh /path/to/extension
```

### Documentation Extraction

To extract documentation data from all sources:

```bash
scripts/extract-all.sh /path/to/extension
```

To extract from specific sources:

```bash
# Extract PHP API documentation
scripts/extract-php.sh /path/to/extension

# Extract extension configuration (ext_emconf.php, ext_localconf.php)
scripts/extract-extension-config.sh /path/to/extension

# Extract Composer metadata
scripts/extract-composer.sh /path/to/extension

# Extract build configurations (CI, testing)
scripts/extract-build-configs.sh /path/to/extension

# Extract project files (README, CHANGELOG)
scripts/extract-project-files.sh /path/to/extension

# Extract repository metadata (GitHub/GitLab)
scripts/extract-repo-metadata.sh /path/to/extension
```

### Documentation Analysis

To analyze documentation coverage and identify gaps:

```bash
scripts/analyze-docs.sh /path/to/extension
```

### AI Context Setup

To add AGENTS.md template to Documentation/ folder:

```bash
scripts/add-agents-md.sh /path/to/extension
```

## Using Asset Templates

### AI Agent Context

To provide AI assistants with documentation context, copy `assets/AGENTS.md` to the extension's `Documentation/` folder. This template includes:
- Documentation type and strategy
- Target audience definition
- File structure overview
- Style guidelines for AI-generated content

## Critical Rules

- **UTF-8** encoding, **4-space** indentation, **80 character** max line length, **LF** line endings
- **CamelCase** for file and directory names, **sentence case** for headings
- **Index.rst** required in every subdirectory
- **PNG** format for screenshots with `:alt:` text
- **.editorconfig** required in `Documentation/` directory

## Element Selection Guide

| Content Type | Directive to Use |
|--------------|------------------|
| Code (5+ lines) | `literalinclude` (preferred) |
| Short code snippets | `code-block` with `:caption:` |
| Configuration options | `confval` with `:type:`, `:default:` |
| PHP API documentation | `php:class::`, `php:method::` |
| Important notices | `note`, `tip`, `warning`, `important` |
| Feature grids | `card-grid` |
| Alternative approaches | `tabs` (synchronized) |
| Collapsible content | `accordion` |

## Pre-Commit Checklist

1. `.editorconfig` exists in `Documentation/`
2. Every directory has `Index.rst` with CamelCase naming
3. 4-space indentation, no tabs, max 80 characters per line
4. Code blocks have `:caption:` and valid syntax highlighting
5. Inline code uses appropriate roles (`:php:`, `:file:`, `:typoscript:`)
6. `scripts/validate_docs.sh` passes without errors
7. Visual verification of rendered HTML output
8. README.md and Documentation/ content is consistent

## External Resources

When understanding TYPO3 documentation standards, consult the [TYPO3 Documentation Writing Guide](https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/).

When seeking rendering tool documentation, consult the [TYPO3 Documentation Rendering](https://github.com/typo3-documentation/render-guides).

When checking directive syntax, consult the [TYPO3 Documentation Reference](https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/WritingReST/Reference/).

---

> **Contributing:** https://github.com/netresearch/typo3-docs-skill
