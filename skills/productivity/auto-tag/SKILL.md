---
name: auto-tag
context: fork
skill: auto-tag
model: haiku
description: Batch auto-tag untagged notes using content analysis
tags: [activity/governance, domain/tooling, automation]
---

# /auto-tag

Batch auto-tag notes that have empty or missing tags by analysing their content and type. Addresses the 61% empty tag rate in the vault.

## Usage

```
/auto-tag                    # Process all untagged notes
/auto-tag <path>             # Process specific file or folder
/auto-tag --dry-run          # Preview changes without applying
/auto-tag --type Meeting     # Only process untagged notes of a specific type
/auto-tag --limit 50         # Process at most 50 notes
```

## Instructions

### Phase 1: Find Untagged Notes

Use Grep and Glob to find notes with empty tags:

```bash
# Find files with empty tags arrays
Grep for "tags: \[\]" in *.md files (exclude Templates/, .obsidian/, .claude/, Archive/)

# Also find files with no tags field at all
# Notes with tags containing only template variables
```

Filter results:
- Exclude `Templates/`, `.obsidian/`, `.claude/`, `Archive/`, `Attachments/`
- If `--type` specified, filter by frontmatter type field
- If `<path>` specified, scope to that path
- Sort by type for batch efficiency

### Phase 2: Analyse and Tag (Parallel)

Launch parallel Haiku sub-agents, batching 20 notes per agent:

For each note, the agent should:

1. **Read frontmatter** — extract `type`, `title`, `project`, `status`
2. **Read body content** — first 500 words
3. **Determine tags** using these rules:

#### Tag Selection Rules

**By note type** (always apply):

| Type | Auto-tags |
|------|-----------|
| ADR | `type/adr`, `activity/architecture` |
| Meeting | (infer from title/content) |
| Task | (infer project from `project:` field) |
| Project | `activity/delivery` + self-referencing `project/` tag |
| System | `type/system` |
| Incubator | `activity/research` |
| Research | `activity/research` |
| Concept | (infer from content) |
| Pattern | (infer from content) |
| Email | (infer from content) |
| Reference | (infer from referenceType and content) |
| Trip | (no tags needed — skip) |
| Daily | `daily` |

**By content analysis** (keyword matching):

| Content Keywords | Suggested Tag |
|-----------------|---------------|
| AWS, Lambda, S3, EC2, Bedrock | `technology/aws` |
| SAP, BTP, S/4HANA, UI5 | `technology/sap` |
| ERPSystem, MRO Vendor | `technology/erp` |
| Kafka, streaming, event | `technology/kafka` |
| Snowflake, data warehouse | `technology/snowflake` |
| security, IAM, encryption | `domain/security` |
| data, analytics, pipeline | `domain/data` |
| engineering, maintenance, MRO | `domain/engineering` |
| integration, API, middleware | `domain/integration` |
| cloud, infrastructure | `domain/cloud` |
| architecture, design, pattern | `activity/architecture` |
| research, investigation, POC | `activity/research` |
| governance, compliance, policy | `activity/governance` |

**By `project:` field** (if present):

| Project Link | Tag |
|-------------|-----|
| `[[Project - Alpha]]` | `project/alpha` |
| `[[Project - Beta]]` or `[[Project - Beta]]` | `project/beta` |
| `[[Project - AlertHub]]` | `project/alerthub` |
| `[[Project - Gamma]]` | `project/gamma` |
| `[[Project - Delta]]` | `project/delta` |
| `[[Project - Epsilon]]` | `project/epsilon` |
| `[[Project - Cyber Uplift]]` | `project/cyber-uplift` |

**Tag count target:** 2-5 tags per note. Prefer fewer, more accurate tags over many vague ones.

4. **Format tags** — all lowercase, hierarchical, no `#` prefix
5. **Return** — list of (filepath, suggested_tags) tuples

### Phase 3: Apply Tags

For each note with suggested tags:

1. Read current frontmatter
2. If `tags: []` — replace with suggested tags
3. If no tags field — add `tags:` with suggested tags
4. Write updated file using Edit tool

**Format:**
```yaml
# Inline for 1-3 tags:
tags: [activity/research, domain/data]

# Multi-line for 4+ tags:
tags:
  - activity/architecture
  - technology/aws
  - domain/cloud
  - project/alerthub
```

### Phase 4: Report

```markdown
## Auto-Tag Results

**Notes processed:** {{count}}
**Notes tagged:** {{tagged_count}}
**Notes skipped:** {{skipped_count}} (already tagged or no suggestions)

### By Type
| Type | Tagged | Example Tags |
|------|--------|-------------|
| Meeting | 45 | project/*, domain/* |
| Concept | 30 | activity/*, domain/* |
| ADR | 20 | type/adr, technology/* |

### Sample Changes
| Note | Tags Added |
|------|-----------|
| {{note}} | {{tags}} |
| {{note}} | {{tags}} |
```

## Safety

- Always use `--dry-run` first for vault-wide operations
- Never overwrite existing non-empty tags
- Commit to git before running
- Tags are additive only — never removes existing tags
- Use the `.claude/context/tag-taxonomy.md` reference for valid hierarchies

## Related Skills

- `/tag-management` — Manual tag analysis and refactoring
- `/quality-report` — Includes tag coverage metrics
- `/vault-maintenance` — Includes tag health checks
