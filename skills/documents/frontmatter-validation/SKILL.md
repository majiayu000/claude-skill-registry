---
skill_name: frontmatter-validation
skill_category: documentation
description: Validate and fix YAML frontmatter in markdown documentation
allowed_tools: [Read, Edit, Glob, Grep]
token_estimate: 950
version: 1.0
last_updated: 2025-12-21
owner: Claude Copilot
status: active
tags: [frontmatter, yaml, documentation, validation, metadata, shared-docs]
related_skills: [token-budget-check, link-validation]
trigger_files: ["*.md", "**\/SKILL.md"]
trigger_keywords: [frontmatter, yaml, metadata, validation, headers]
---

# Frontmatter Validation

Validate and fix YAML frontmatter metadata in markdown documentation files.

## Purpose

Frontmatter enables efficient AI navigation of documentation. This skill ensures all files have correct, complete metadata for their document type.

## Frontmatter Schemas by Document Type

### Tier 1: Skills (SKILL.md)

```yaml
---
skill_name: forces-analysis          # required, kebab-case
skill_category: analysis             # required: analysis, engineering, facilitation, strategy
description: One-line description    # required, max 100 chars
allowed_tools: [Read, Write, Edit]   # required, array
token_estimate: 1850                 # required, integer
version: 1.2                         # required, semver
last_updated: 2025-01-15             # required, ISO date
owner: Service Design Team           # required
status: active                       # required: active, deprecated, draft
tags: [forces, organization]         # required, array
related_skills: [moments-mapping]    # optional, array
methodology: path/to/methodology.md  # optional, relative path
---
```

### Tier 2: Product Documentation

```yaml
---
product: Insights Copilot            # required
status: active                       # required: active, beta, deprecated
last_updated: 2025-01-15             # required, ISO date
owner: Platform Team                 # required
token_estimate: 650                  # required, integer
doc_type: architecture               # required: overview, architecture, api, integration, security
source_of_truth: ../repo/docs/...    # optional, path to canonical doc
dependencies: [product-a, product-b] # optional, array
summary: Brief description           # optional, 1-2 sentences
key_entities: [Force, Pattern]       # optional, domain entities
integration_endpoints: [POST /api/x] # optional, for API docs
---
```

### Tier 3: Operational Documentation

```yaml
---
title: Documentation Strategy Guide  # required
doc_type: guide                       # required: guide, standard, reference, runbook
category: operations                  # required: operations, security, development
last_updated: 2025-01-15              # required, ISO date
version: 2.1                          # optional
status: active                        # required: active, deprecated, draft
primary_audience: [developers]        # optional, array
required_reading: false               # optional, boolean
token_estimate: 2500                  # required, integer
replaces: _archive/old-doc.md         # optional, path to replaced doc
related: [other-doc.md]               # optional, array
---
```

## Procedure

### 1. Identify Target Files

```bash
find . -name "*.md" -type f -not -path "./_archive/*"
```

### 2. Detect Document Type

Infer from path and filename:

| Pattern | Document Type |
|---------|---------------|
| `*/SKILL.md` | Tier 1: Skill |
| `02-products/*` | Tier 2: Product |
| `03-ai-enabling/03-operations/*` | Tier 3: Operational |
| `*/00-overview.md` | Product overview |
| `*-profile.md` or `02-profiles/*` | Agent profile |

### 3. Extract Existing Frontmatter

Frontmatter is YAML between `---` markers at file start:

```bash
sed -n '/^---$/,/^---$/p' file.md | head -n -1 | tail -n +2
```

### 4. Validate Against Schema

Check for:

| Check | Severity | Description |
|-------|----------|-------------|
| Required fields missing | ERROR | Must be present |
| Wrong type | ERROR | e.g., string instead of array |
| Invalid value | ERROR | e.g., status: "live" not in enum |
| Missing token_estimate | WARNING | Should be calculated and added |
| Stale last_updated | WARNING | Older than file modification |
| Broken path reference | WARNING | source_of_truth doesn't exist |

### 5. Auto-Fix Where Possible

| Missing Field | Auto-Fix Strategy |
|---------------|-------------------|
| `token_estimate` | Calculate from word count × 1.4 |
| `last_updated` | Use current date |
| `status` | Default to "active" |
| `skill_name` | Derive from directory name |
| `doc_type` | Infer from path/filename |

### 6. Generate Missing Frontmatter

For files without frontmatter, generate based on type:

```yaml
---
title: [Derived from H1 or filename]
doc_type: [Inferred from path]
last_updated: 2025-12-21
status: active
token_estimate: [Calculated]
---
```

## Output Format

```markdown
## Frontmatter Validation Report

### Summary
- Files scanned: N
- Valid: N
- Errors: N
- Warnings: N
- Fixed: N

### Errors (Must Fix)

| File | Issue | Field | Details |
|------|-------|-------|---------|
| skills/x/SKILL.md | Missing required | skill_name | Add skill name |
| products/y.md | Invalid value | status | "live" not valid, use "active" |

### Warnings

| File | Issue | Field | Suggestion |
|------|-------|-------|------------|
| docs/guide.md | Missing | token_estimate | Add: 1,250 (calculated) |
| docs/api.md | Stale | last_updated | Update to current date |

### Auto-Fixes Applied

| File | Field | Old Value | New Value |
|------|-------|-----------|-----------|
| docs/setup.md | token_estimate | (missing) | 890 |
| docs/setup.md | last_updated | 2024-06-01 | 2025-12-21 |
```

## Validation Rules

### Field Value Rules

| Field | Valid Values |
|-------|--------------|
| `status` | active, deprecated, draft, beta |
| `skill_category` | analysis, engineering, facilitation, strategy, documentation |
| `doc_type` | overview, architecture, api, integration, security, guide, standard, reference, runbook |
| `allowed_tools` | Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch |

### Path Validation

For path fields (`source_of_truth`, `methodology`, `replaces`, `related`):
- Resolve relative to file location
- Check target exists
- Warn if external to repository

### Token Estimate Accuracy

Compare `token_estimate` to actual:
- Within 10%: OK
- 10-25% off: WARNING
- >25% off: ERROR (likely stale)
