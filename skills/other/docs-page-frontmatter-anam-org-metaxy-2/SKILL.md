---
name: docs-page-frontmatter
description: Write YAML front matter for documentation pages with appropriate titles and descriptions for social cards.
---

# Documentation Page Front Matter

This skill guides writing YAML front matter for mkdocs-material documentation pages. Front matter controls social card generation and page metadata.

## Front Matter Format

```yaml
---
title: "Page Title"
description: "Brief description of the page."
---
```

## Title Guidelines

- Use descriptive titles that provide context
- Include the subject matter (e.g., "LanceDB Configuration" not just "Configuration")
- Keep titles concise but informative
- For API reference pages: "[Subject] API" or "API reference for [Subject]"
- For configuration pages: "[Subject] Configuration"
- For index pages: Use the section name (e.g., "Integrations", "User Guide")

## Description Guidelines

**DO:**

- Briefly summarize what the page covers
- Keep descriptions general and conceptual
- Use simple, direct language
- Focus on the page content, not the subject itself

**DON'T:**

- Enumerate specific implementation details that may become outdated
- List specific technologies, databases, or tools unless the page is specifically about one
- Prescribe use cases (avoid "for local development", "ideal for production", etc.)
- Use verbose explanations
- Describe what the subject does (describe the page instead)

## Examples

### Good Descriptions

```yaml
# API reference page
description: "API reference for DuckDBMetadataStore."

# Configuration page
description: "Configuration options for ClickHouseMetadataStore."

# Concept page
description: "How Metaxy calculates and tracks versions."

# Index page
description: "Available metadata store backends for Metaxy."

# Integration overview
description: "Dagster integration for Metaxy."

# Guide page
description: "Defining dependencies between features."
```

### Bad Descriptions (Avoid These)

```yaml
# Too verbose, lists specific details
description: "Connect Metaxy with orchestrators like Dagster, databases like ClickHouse and BigQuery, and plugins for SQLModel and SQLAlchemy."

# Prescribes use case
description: "Use DuckDB as a fast embedded analytical database for local development and testing with Metaxy."

# Enumerates implementation details
description: "Configuration options for DuckDBMetadataStore including database path, extensions, and DuckLake settings."

# Describes the subject, not the page
description: "A pluggable metadata layer for ML pipelines that tracks feature versions, dependencies, and data lineage."
```

## Patterns by Page Type

| Page Type      | Title Pattern             | Description Pattern                              |
| -------------- | ------------------------- | ------------------------------------------------ |
| Overview/Index | Section name              | Brief summary of section contents                |
| API Reference  | "[Subject] API"           | "API reference for [Subject]."                   |
| Configuration  | "[Subject] Configuration" | "Configuration options for [Subject]."           |
| Concept/Guide  | Concept name              | Brief statement of what the page explains        |
| Example        | "[Name] Example"          | Brief statement of what the example demonstrates |
| Integration    | "[Tool] Integration"      | "[Tool] integration for Metaxy."                 |

## Checklist

Before finalizing front matter, verify:

- [ ] Title provides enough context to be meaningful in isolation
- [ ] Description is one sentence or less
- [ ] Description describes the page, not the subject
- [ ] No specific implementation details that could become outdated
- [ ] No prescriptive language about use cases
- [ ] Consistent with patterns used across the documentation
