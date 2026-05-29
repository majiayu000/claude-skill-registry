---
name: source-integrity
description: Use when processing external sources - validates checksums, metadata completeness, and expiry dates for research sources
allowed-tools: Read, Bash
---

# Source Integrity

## Purpose

Ensure all research sources and external inputs maintain:
- Accurate checksums (detect file modifications)
- Complete metadata (title, author, date, type)
- Valid expiry dates (prevent stale data usage)
- Consistent schema across all sources

## When to Use This Skill

Activate automatically when:
- Processing external sources with `research-processing` workflow
- Validating flashcard content hashes for Mochi sync
- Verifying meeting transcript integrity
- User explicitly requests source validation
- Any workflow depends on external data integrity

## Integrity Requirements

### 1. Checksum Validation

**Requirement**: All sources must have content checksums for change detection

**Supported algorithms:**
- SHA-256 (preferred)
- MD5 (legacy support)

**Validation process:**
1. Read source file content
2. Calculate checksum of current content
3. Compare to stored checksum in metadata
4. Flag mismatch as modification

**Pass**:
```yaml
checksum: "sha256:a7f3b2c1..."
```
Calculated checksum matches stored value.

**Fail**:
```yaml
checksum: "sha256:a7f3b2c1..."
```
Calculated checksum: `sha256:d4e5f6g7...` (mismatch = file modified)

### 2. Metadata Completeness

**Required fields for research sources:**
```yaml
title: "Source Title"
kind: "file" | "url" | "note"
path: "/absolute/path/to/source.md"  # for kind=file
url: "https://..."  # for kind=url
checksum: "sha256:..."
added_utc: "YYYY-MM-DDTHH:MM:SSZ"
topic: "strategic-category"  # e.g., competitive-analysis, pricing-strategy
expiry_date: "YYYY-MM-DD"  # optional, based on source type
```

**Optional but recommended:**
```yaml
author: "Author Name"
published_date: "YYYY-MM-DD"
summary: "Brief description"
tags: ["keyword1", "keyword2"]
```

**Validation process:**
1. Read source metadata (YAML frontmatter or citations/sources.json entry)
2. Verify all required fields present
3. Validate field formats (dates, URLs, paths)
4. Flag missing or malformed fields

**Pass**:
All required fields present and properly formatted.

**Fail examples:**
- Missing `checksum` field
- Invalid date format (`added_utc: "2025-10-21"` instead of ISO 8601)
- Relative path instead of absolute (`path: "notes/file.md"`)
- Unknown `kind` value (`kind: "pdf"` when only file/url/note supported)

### 3. Expiry Management

**Purpose**: Prevent using stale data in strategic decisions

**Expiry guidelines by source type:**

| Source Type | Suggested Expiry | Rationale |
|-------------|------------------|-----------|
| Frameworks | 1-2 years | Conceptual models change slowly |
| Market data | 3-6 months | Markets evolve quickly |
| Competitor intel | 6-12 months | Product changes, pricing shifts |
| Customer quotes | 6-12 months | Needs/priorities evolve |
| Internal meeting notes | 12 months | Context becomes stale |

**Validation process:**
1. Read source `expiry_date` field (if present)
2. Compare to current date
3. If expired: Flag for review/refresh
4. If no expiry_date: Suggest based on source type

**Pass**:
```yaml
expiry_date: "2026-03-15"
```
Current date: 2025-10-21 (not expired)

**Fail**:
```yaml
expiry_date: "2025-05-01"
```
Current date: 2025-10-21 (expired, requires refresh)

### 4. Schema Consistency

**Requirement**: All sources follow standardized schema

**Research source schema** (`datasets/research/{topic}/{filename}.md`):
```markdown
---
title: "Source Title"
kind: "file" | "url" | "note"
topic: "strategic-category"
url: "https://..." (if applicable)
checksum: "sha256:..."
added_utc: "YYYY-MM-DDTHH:MM:SSZ"
expiry_date: "YYYY-MM-DD"
---

# Source Title

## Key Insights
- Insight 1
- Insight 2

## Strategic Applications
- How this informs decisions
- Relevant use cases

## Citations / Quotes
> "Verbatim quote for future citation"
> — Author, Publication (Date)

## Related Internal Links
- [Meeting notes](datasets/meetings/...)
- [Epic](datasets/product/epics/...)
```

**Meeting schema** (see `meeting-schema-validation` skill)

**Citation schema** (`citations/sources.json`):
```json
{
  "id": "src_abc123",
  "title": "Source Title",
  "kind": "file|url|note",
  "path": "/absolute/path",
  "url": "https://..." (optional),
  "checksum": "sha256:...",
  "added_utc": "2025-10-21T14:30:00Z"
}
```

## Validation Process

### 1. Load Source

Read source from:
- `datasets/research/{topic}/{filename}.md`, OR
- `citations/sources.json` entry, OR
- `datasets/learning/cards/{topic}/{filename}.md` (for flashcard validation)

### 2. Apply Integrity Checks

Run all checks in sequence:

**Checksum:**
```bash
# Calculate current checksum
sha256sum /path/to/source.md | awk '{print "sha256:"$1}'

# Compare to stored checksum in metadata
```

**Metadata:**
- Verify required fields present
- Validate date formats (ISO 8601)
- Validate paths (absolute, exists)
- Validate URLs (proper format)

**Expiry:**
- Check expiry_date against current date
- Flag expired sources
- Suggest expiry dates for sources without them

**Schema:**
- Verify YAML frontmatter format
- Check required sections exist (for markdown sources)
- Validate JSON structure (for citations/sources.json)

### 3. Generate Report

**If all pass:**
```markdown
# Source Integrity Validation: PASS

**Source**: [filename or title]

✓ Checksum valid: sha256:a7f3b2c1... (matches stored value)
✓ Metadata complete: All required fields present
✓ Not expired: expiry_date 2026-03-15 (172 days remaining)
✓ Schema valid: Proper YAML frontmatter and sections

**Status**: Source integrity verified
```

**If any fail:**
```markdown
# Source Integrity Validation: FAIL

**Source**: [filename or title]

✗ Checksum mismatch:
  - Stored: sha256:a7f3b2c1...
  - Calculated: sha256:d4e5f6g7...
  - **Action**: File modified. Review changes and update checksum.

✗ Missing metadata fields:
  - `added_utc` not present
  - `topic` not present
  - **Action**: Add required fields to frontmatter

✗ Expired source:
  - expiry_date: 2025-05-01 (173 days ago)
  - **Action**: Review and refresh source, or extend expiry if still valid

**Required fixes**:
1. Recalculate and update checksum
2. Add missing metadata fields
3. Refresh expired source or justify extension

**Status**: NEEDS_FIX
```

### 4. Block or Approve

**If PASS:**
- Source can be used in workflows
- Citations can reference this source
- Integrity confirmed

**If FAIL:**
- Source blocked from usage
- Workflows depending on this source flagged
- Must address violations before use

## Integration with Workflows

### Research Processing Integration

**Invoked by:**
- `research-processing` workflow (when adding new sources)
- `source-normalization` skill (after creating citation entry)

**Blocking behavior:**
- If integrity check fails → source not added to citations/sources.json
- User notified of required fixes

### Mochi Sync Integration

**Invoked by:**
- `mochi-sync` workflow (validates flashcard content hashes)

**Behavior:**
- Checksums determine if card content changed
- If checksum mismatch → card marked for update in Mochi
- If checksum matches → skip card (already synced)

### Meeting Processing Integration

**Optional usage:**
- Can validate meeting transcript integrity
- Detect if transcript modified after initial processing
- Flag for re-processing if changed

## Success Criteria

Source integrity validated when:
- Checksum matches current file content
- All required metadata fields present and valid
- Source not expired (or expiry justified)
- Schema matches expected format
- Validation report shows PASS status

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting to update checksum after edits | Recalculate and update metadata |
| Using relative paths | Convert to absolute paths |
| Missing expiry_date on time-sensitive sources | Add expiry based on source type |
| Invalid date format | Use ISO 8601: YYYY-MM-DDTHH:MM:SSZ |
| Ignoring expired sources | Refresh or explicitly justify continued use |

## Related Skills

- **source-normalization**: Creates normalized source entries (invokes this skill for validation)
- **research-processing**: Uses this skill to validate external sources
- **mochi-sync**: Uses checksum logic from this skill for sync tracking

## Anti-Rationalization Blocks

Common excuses that are **explicitly rejected**:

| Rationalization | Reality |
|----------------|---------|
| "Checksum mismatch doesn't matter" | Integrity violation. Fix or fail. |
| "This source doesn't need expiry" | Add suggested expiry based on type. |
| "Close enough" on metadata | All required fields or fail. |
| "File path is obvious" | Use absolute paths, no assumptions. |
