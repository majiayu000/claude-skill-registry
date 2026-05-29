---
name: organize-folders
description: Provides guidance on organizing folder structures and file system layouts for any project. Use when planning project organization, reorganizing messy directories, setting up folder hierarchies, designing directory layouts, structuring repositories, cleaning up files, suggesting folder structures, establishing naming conventions, or when you need help with folder structure or file organization. Helps with writing projects, code projects, document collections, or any file organization task.
allowed-tools: [Read, Grep, Glob]
# model: haiku
---

# Folder Organization Guidance

This skill provides **guidance and recommendations** for organizing folder structures and file system layouts. It helps you design effective file organization but doesn't automatically reorganize files.

## User Preferences

The user prefers simple, practical systems with a typical pattern:

- drafts
- published

The user prefers top-level folders for nesting but repository design is flexible. Recommend whatever system best fits the task, keeping things simple.

## Examples

### Writing Project: Blog Post Rewrite

For a blog post rewrite targeting a more technical audience:

- Create a new folder called `/rewrite`
- Within that folder, create subfolders like `/rewrite/v1`, `/rewrite/v2` or `/rewrite/drafts`

**When to use versioned folders** (v1, v2):

- Rewrite involves multiple assets (text + images) that need to stay together
- Each version is a complete package

**When to use drafts folder**:

- Text-only rewrites without supporting files
- Simpler iteration process

### Document Collection

For organizing a collection of PDF documents:

- Organize by source/publisher first, then by type
- Use flat structures only for small collections (<30 files)
- Create subdirectories when folders exceed ~50 files
- Document file counts in README.md at collection root

### Code Project

For a multi-component software project:

- `/src` - source code organized by feature or layer
- `/tests` - test files mirroring src structure
- `/docs` - documentation
- `/scripts` - automation and build scripts

### Photo/Media Library

For organizing photos, videos, or media files:

- By date: `/2024/01-January`, `/2024/02-February` (chronological)
- By event: `/Vacation-Hawaii-2024`, `/Birthday-Party-2024` (event-based)
- Hybrid: `/2024/Hawaii-Vacation`, `/2024/Birthday` (year + event)

Choose based on retrieval patterns - date for large collections, events for memorable occasions.

### Research Project

For academic or research work with papers and notes:

- `/papers` - PDFs organized by topic or author
- `/notes` - Reading notes and annotations
- `/writing` - Drafts of your own work
- `/data` - Datasets and analysis results
- `/references` - Bibliography and citation management

## General Principles

- **Start simple**: Use one file/folder until you need more
- **Split when needed**: Create subdirectories when folders get too large (~50+ items)
- **Name consistently**: Establish conventions early
- **Document structure**: Add README.md explaining organization when non-obvious
- **Follow the simplest solution that will get the job done**

## Common Organization Problems

### Too Many Files in One Folder

When a folder exceeds ~50 items, it becomes hard to navigate:

- **Solution**: Create subdirectories by logical grouping (type, date, category)
- **Example**: Split `/documents` into `/documents/contracts`, `/documents/reports`, `/documents/invoices`

### Deeply Nested Structures

More than 3-4 levels of nesting makes files hard to find:

- **Solution**: Flatten by combining middle levels or using more descriptive names
- **Example**: `/projects/client/2024/Q1/reports` → `/projects/client-2024-Q1-reports`

### Inconsistent Naming

Mixed conventions (spaces vs dashes, capitalization) cause confusion:

- **Solution**: Pick one convention and apply consistently
- **Recommended**: kebab-case for code projects, Title Case for documents

## References

For detailed guidance on specific topics, see the reference documentation:

### [document-collection-organization.md](document-collection-organization.md)

Comprehensive guide for organizing PDF and document collections:

- Publisher-first hierarchy strategies
- Size thresholds and when to split directories (30/50/100+ file triggers)
- PDF examination workflow (pdfinfo, pdftotext)
- Duplicate prevention and detection methods
- Periodic audit processes and checklists
- Collection README.md templates
- Handling inherited disorganized collections

### [naming-conventions.md](naming-conventions.md)

Complete naming conventions for all file types:

- Document collections: Title Case with spaces
- Code projects: kebab-case for directories, language-specific for files
- Media libraries: date-based (YYYY-MM-DD) vs event-based naming
- Research papers: Author-Year-Title patterns
- Common mistakes and how to fix them
- Batch renaming strategies and scripts
- Enforcement during audits

### [organization-patterns.md](organization-patterns.md)

Decision frameworks and pattern selection:

- Pattern decision tree (topic, chronological, publisher, type, project, hybrid)
- When to split directories (quantitative and qualitative triggers)
- Anti-patterns to avoid (excessive nesting, premature organization, misc dumping grounds)
- Reorganization strategies and when to reorganize
- Effective pattern combinations

### [examples-and-workflows.md](examples-and-workflows.md)

Step-by-step walkthroughs and templates:

- Organizing 200+ PDF research collection (complete 6-hour workflow)
- Migrating from disorganized to organized structure
- README.md templates for document and code collections
- Quarterly collection audit checklist
- Adding new files to existing collections
- Reorganizing when structure is outgrown
