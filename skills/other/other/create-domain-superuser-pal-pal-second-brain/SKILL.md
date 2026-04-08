---
name: create-domain
description: Create and validate PAL domains (project workspaces). USE WHEN create domain, new domain, domain structure, validate domain, map domain, sync domain, archive domain, project workspace, housekeeping. SkillSearch('create-domain') for docs.
user-invocable: false
---

# create-domain

MANDATORY domain creation system for ALL domain creation requests.

## Authoritative Source

**Before creating ANY domain, READ:** `DOMAINS_LOGIC.md`

## Naming Conventions (MANDATORY)

**Domain naming follows PAL's standard file naming conventions.**

| Category             | Convention            | Example                | Purpose                                            |
| :------------------- | :-------------------- | :--------------------- | :------------------------------------------------- |
| **Domain directory** | `PascalCase`          | `ProjectAlpha/`        | Standard IDE navigation.                           |
| **INDEX.md**         | `UPPERCASE.md`        | `INDEX.md`             | Source of Truth file (at domain root).             |
| **CONNECTIONS.yaml** | `UPPERCASE.yaml`      | `CONNECTIONS.yaml`     | External sources configuration.                    |
| **Core folders**     | `NN_UPPER_CASE`       | `01_PROJECTS/`         | Numbered prefixes for sorting + visibility.        |
| **Context files**    | `lower_snake_case.md` | `background_info.md`   | Reference docs in 00_CONTEXT/.                     |
| **Project files**    | `UPPER_SNAKE_CASE.md` | `PROJECT_FEATURE_X.md` | Active project files in 01_PROJECTS/.              |
| **Session logs**     | `YYYY-MM-DD_title.md` | `2026-01-15_sync.md`   | Chronological session logs.                        |
| **Pages files**      | `lower_snake_case.md` | `api_documentation.md` | Reference materials and assets.                    |
| **Workspace files**  | Flexible              | Any naming             | Agent workspace and staging area in 03_OUTPUT/. |

---

## Workflow Routing

| Workflow            | Trigger                                                     | File                           |
| :------------------ | :---------------------------------------------------------- | :----------------------------- |
| **create_domain**   | "create domain", "new domain"                               | `workflows/create_domain.md`   |
| **validate_domain** | "validate domain", "check domain"                           | `workflows/validate_domain.md` |
| **map_domain**      | "map domain", "sync domain", "housekeeping", "update index" | `workflows/map_domain.md`      |
| **archive_domain**  | "archive domain", "deprecate domain"                        | `workflows/archive_domain.md`  |

## Examples

**Example 1: Create a new domain from scratch**

```
User: "Create a domain for my blog project"
-> Invokes create_domain workflow
-> Reads DOMAINS_LOGIC.md for structure requirements
-> Creates domains/BlogProject/ with all 6 core folders
-> Generates INDEX.md with YAML frontmatter and template
-> Creates empty CONNECTIONS.yaml with schema comments
```

**Example 2: Sync domain after adding files**

```
User: "Map my ProjectAlpha domain"
-> Invokes map_domain workflow
-> Scans all 6 core folders
-> Detects naming violations, auto-fixes with confirmation
-> Refreshes INDEX.md Active Work table from 01_PROJECTS/
-> Reports summary of changes
```

**Example 3: Archive old content**

```
User: "Archive the old feature project in my domain"
-> Invokes archive_domain workflow
-> Moves file to 05_ARCHIVE/ with deprecation header
-> Updates INDEX.md to remove from Active Work
-> Confirms archive complete
```

## Domain Structure

Every domain follows this structure:

```
domains/DomainName/               # PascalCase directory
├── INDEX.md                      # Source of Truth (at domain root)
├── CONNECTIONS.yaml              # External sources (at domain root)
├── 00_CONTEXT/                   # Domain-specific context and reference docs
├── 01_PROJECTS/                  # Active project files
├── 04_SESSIONS/                  # Chronological interaction logs
├── 02_PAGES/                     # Reference materials
├── 03_OUTPUT/                    # Staging area for generated files
└── 05_ARCHIVE/                   # Deprecated content
```

**Nesting Limit:** Do not exceed three vertical levels below the domain root.

**Note:** Domains are prerequisites for agent creation. Every domain agent must bind to an existing domain. See `AGENTS_LOGIC.md` for agent-domain binding rules.
