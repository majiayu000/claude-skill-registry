---
skill_name: link-validation
skill_category: documentation
description: Validate markdown links and cross-references in documentation
allowed_tools: [Read, Bash, Glob, Grep]
token_estimate: 900
version: 1.0
last_updated: 2025-12-21
owner: Claude Copilot
status: active
tags: [links, documentation, validation, shared-docs, cross-references]
related_skills: [token-budget-check, frontmatter-validation]
trigger_files: ["*.md", "**\/docs/**\/*.md"]
trigger_keywords: [links, broken-links, validation, cross-reference, anchor, markdown-links]
---

# Link Validation

Validate markdown links and cross-references to ensure documentation integrity.

## Purpose

Broken links in shared-docs waste Claude's time and tokens. This skill finds and fixes broken internal links, missing anchors, and incorrect cross-references.

## Link Types to Validate

| Type | Pattern | Example |
|------|---------|---------|
| Relative file | `[text](./path.md)` | `[Overview](./00-overview.md)` |
| Anchor | `[text](#heading)` | `[Setup](#installation)` |
| File + anchor | `[text](./file.md#section)` | `[Auth](./60-security.md#auth)` |
| Parent path | `[text](../other/file.md)` | `[Index](../00-INDEX.md)` |
| Absolute (external) | `https://...` | Skip or warn |

## Procedure

### 1. Find All Markdown Files

```bash
find . -name "*.md" -type f -not -path "./_archive/*"
```

### 2. Extract Links from Each File

Use grep to find markdown links:

```bash
grep -oE '\[([^\]]+)\]\(([^\)]+)\)' file.md
```

### 3. Categorize Links

For each link:
- **External** (starts with `http`): Skip or optionally validate
- **Anchor only** (`#heading`): Validate heading exists in same file
- **Relative file**: Resolve path and check file exists
- **File + anchor**: Check both file and heading exist

### 4. Validate Internal Links

For relative paths:

```bash
# From the file's directory, check if target exists
target_file="resolved/path/to/target.md"
if [ -f "$target_file" ]; then
  echo "OK: $target_file"
else
  echo "BROKEN: $target_file"
fi
```

### 5. Validate Anchors

Anchors should match headings (lowercase, hyphens for spaces):

```bash
# Extract headings from target file
grep -E '^#{1,6} ' target.md | sed 's/^#* //' | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g'
```

### 6. Attempt Auto-Fix

For broken links, search for likely correct targets:

| Broken Link | Search Strategy |
|-------------|-----------------|
| `./old-name.md` | Find files with similar names |
| `#old-heading` | Find similar headings in file |
| `../wrong/path.md` | Search for filename in other directories |

## Output Format

```markdown
## Link Validation Report

### Summary
- Files scanned: N
- Total links: N
- Valid: N
- Broken: N
- Warnings: N

### Broken Links

| File | Line | Link | Issue | Suggested Fix |
|------|------|------|-------|---------------|
| docs/setup.md | 45 | `./old-guide.md` | File not found | `./10-guide.md` |
| docs/api.md | 23 | `#authenication` | Anchor not found | `#authentication` |

### Warnings

| File | Link | Warning |
|------|------|---------|
| docs/intro.md | `https://old.example.com` | External link (not validated) |

### Fixes Applied
- docs/setup.md:45 - Changed `./old-guide.md` to `./10-guide.md`
```

## Cross-Reference Patterns

### Link Registry Pattern

If `00-links.md` exists in a directory, validate all links defined there:

```yaml
## Internal Links
- ecosystem: ../00-ecosystem-overview.md
- glossary: ../../03-ai-enabling/03-operations/12-shared-glossary.md
```

### Source of Truth Pattern

Frontmatter may reference external docs:

```yaml
source_of_truth: ../../insights-copilot/docs/04-architecture/system-design.md
```

Validate these paths exist (may be outside current repo).

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| File moved | Renamed with number prefix | Update link with new prefix |
| Heading changed | Wording updated | Update anchor text |
| Case mismatch | GitHub case-sensitive | Match exact case |
| Missing extension | `.md` omitted | Add `.md` extension |
