---
name: source-normalization
description: Use when processing files, URLs, or text inputs - normalizes various formats into structured citations with stable IDs, checksums, and standardized metadata
allowed-tools: Read, Write, Bash
---

# Source Normalization

## Purpose

Convert diverse source formats into standardized citation entries:
- Normalize file paths, URLs, and pasted text
- Generate stable source IDs (hash-based)
- Calculate checksums for change detection
- Create consistent metadata structure
- Deduplicate by content or URL
- Maintain citations/sources.json registry

## When to Use This Skill

Activate automatically when:
- `content-run` workflow processes input files/URLs/text
- `research-processing` workflow adds external sources
- User provides mixed input formats (files + URLs + text)
- Any workflow needs citation tracking
- Building content with source attribution

## Source Input Types

### 1. File Inputs
**Format:** Absolute or relative paths, glob patterns

**Examples:**
```
/Users/jay/llm/datasets/meetings/Customers/PrettyBoy/2025/10-15_sales_discovery-call.md
datasets/learning/sources/seasonality/**/*.md
~/Workspace/llm/datasets/research/competitive-analysis/klaviyo-pricing.md
```

**Normalization:**
- Expand globs to individual files
- Convert relative paths to absolute
- Verify file existence
- Calculate checksum
- Extract metadata from frontmatter (if present)

### 2. URL Inputs
**Format:** HTTP/HTTPS URLs

**Examples:**
```
https://www.klaviyo.com/blog/segment-examples
https://example.com/analyst-report.pdf
https://github.com/company/repo/README.md
```

**Normalization:**
- Fetch content (if `--web` enabled)
- Save to `inputs/` directory as markdown
- Extract title from HTML <title> or first H1
- Calculate checksum of fetched content
- Store original URL in metadata

### 3. Text Inputs
**Format:** Pasted text blocks, inline context

**Examples:**
```
TEXT:
>>>
Add a counterpoint on over-segmentation and a simple prompt example.
User feedback from Slack: "We need better export options for campaign data."
<<<
```

**Normalization:**
- Save to `inputs/context_{timestamp}.md`
- Generate title from first sentence or timestamp
- Calculate checksum
- Mark kind as "note"

## Normalization Process

### 1. Detect Source Type

**For each input:**
```
If starts with "http://" or "https://":
  → Type: URL
Else if file path (contains "/" or "\" or exists as file):
  → Type: FILE
Else if in TEXT block or pasted content:
  → Type: TEXT
```

### 2. Expand and Validate

**FILE inputs:**
```
1. Expand glob patterns to file list
2. Convert relative paths to absolute
3. Verify each file exists (stat check)
4. If missing: Log error, skip
```

**URL inputs:**
```
1. Validate URL format (regex)
2. If `--web` enabled:
   - Fetch content using WebFetch
   - Save to inputs/fetched_{slug}_{timestamp}.md
   - Extract title from <title> or first H1
3. If `--web` not enabled:
   - Create placeholder entry (URL stored, content not fetched)
```

**TEXT inputs:**
```
1. Write to inputs/context_{timestamp}.md
2. Generate title from first 5-10 words or "Context {timestamp}"
```

### 3. Calculate Checksum

**For all source types:**
```bash
# Read file content (or fetched content for URLs)
content=$(cat /path/to/source.md)

# Calculate SHA-256 checksum
checksum=$(echo "$content" | sha256sum | awk '{print "sha256:"$1}')
```

**Why checksums matter:**
- Detect file modifications
- Enable change-based sync (Mochi flashcards)
- Verify content integrity
- Support caching and deduplication

### 4. Generate Stable ID

**ID format:** `src_{first8chars_of_checksum}`

**Example:**
```
Checksum: sha256:a7f3b2c19d4e5f6g...
ID: src_a7f3b2c1
```

**Why stable IDs:**
- Consistent reference across workflows
- URL-safe identifiers
- Content-based (same content = same ID)
- Short and readable

### 5. Extract Metadata

**From file frontmatter (if YAML present):**
```yaml
title: "Source Title"
author: "Author Name"
published_date: "YYYY-MM-DD"
url: "https://original-url.com" (if this file was fetched)
topic: "strategic-category"
tags: ["keyword1", "keyword2"]
```

**From HTML (for fetched URLs):**
```html
<title>Page Title</title>
→ Extract as title

<meta name="author" content="Author Name">
→ Extract as author

<meta name="description" content="Description">
→ Extract as summary
```

**Fallback values:**
- title: Filename or first H1 or "Untitled Source"
- author: null
- published_date: null (or fetch date for URLs)

### 6. Create Citation Entry

**Standard schema:**
```json
{
  "id": "src_a7f3b2c1",
  "title": "Source Title",
  "kind": "file" | "url" | "note",
  "path": "/absolute/path/to/source.md",  // for kind=file or saved URLs
  "url": "https://...",  // for kind=url (original URL)
  "checksum": "sha256:a7f3b2c1...",
  "added_utc": "2025-10-21T14:30:00Z",
  "author": "Author Name" (optional),
  "published_date": "YYYY-MM-DD" (optional),
  "topic": "strategic-category" (optional),
  "tags": ["keyword1", "keyword2"] (optional)
}
```

### 7. Deduplicate

**Deduplication strategies:**

**By checksum:**
```
If sources.json already contains entry with same checksum:
  → Skip (identical content already registered)
  → Log: "Source already exists: {existing_id}"
```

**By URL (for URL inputs):**
```
If sources.json already contains entry with same URL:
  → Check if content changed (compare checksums)
  → If changed: Update entry with new checksum and timestamp
  → If unchanged: Skip
```

**By path (for FILE inputs):**
```
If sources.json already contains entry with same absolute path:
  → Check if content changed (compare checksums)
  → If changed: Update entry with new checksum
  → If unchanged: Skip
```

### 8. Write to citations/sources.json

**File structure:**
```json
{
  "sources": [
    {
      "id": "src_a7f3b2c1",
      "title": "Source 1",
      "kind": "file",
      "path": "/path/to/source1.md",
      "checksum": "sha256:a7f3b2c1...",
      "added_utc": "2025-10-21T14:30:00Z"
    },
    {
      "id": "src_d4e5f6g7",
      "title": "Source 2",
      "kind": "url",
      "path": "/path/to/inputs/fetched_source2.md",
      "url": "https://example.com/source2",
      "checksum": "sha256:d4e5f6g7...",
      "added_utc": "2025-10-21T14:35:00Z"
    }
  ],
  "version": "1.0",
  "last_updated": "2025-10-21T14:35:00Z"
}
```

**Write operation:**
1. Read existing citations/sources.json (if exists)
2. Append new entries (or update existing)
3. Sort by added_utc (descending)
4. Write back to file with pretty formatting (indent: 2)

## Output Structure

**Created files:**
```
content/{date}_{type}_{slug}/
├── inputs/
│   ├── {original_filename}.md  (copied from FILE input)
│   ├── fetched_{slug}_{timestamp}.md  (from URL input)
│   └── context_{timestamp}.md  (from TEXT input)
└── citations/
    └── sources.json  (normalized citation registry)
```

## Integration with Workflows

### Content Pipeline Integration

**Invoked by:**
- `content-run` workflow (after intent gathering, before brief creation)
- `content-intent-gathering` skill (processes FILES/URLS/TEXT sections)

**Inputs:**
- FILES: Array of file paths (may include globs)
- URLS: Array of URLs
- TEXT: Pasted text blocks
- `--web` flag: Whether to fetch URLs

**Outputs:**
- Normalized files in inputs/ directory
- citations/sources.json with all source entries
- Ready for citation in brief/outline/draft

### Research Processing Integration

**Invoked by:**
- `research-processing` workflow

**Inputs:**
- External source URL or file path
- Topic category for organization

**Outputs:**
- Normalized source file in datasets/research/{topic}/
- Citation entry in sources.json
- Checksum for integrity validation

### Quality Gate Integration

**Used by:**
- `citation-compliance` (reads sources.json for verification)
- `source-integrity` (validates checksums in sources.json)
- `link-verification` (uses URL entries for validation)

## Success Criteria

Source normalization complete when:
- All input sources processed (files, URLs, text)
- Stable IDs generated for each source
- Checksums calculated
- Metadata extracted (or sensible defaults applied)
- Deduplication applied (no duplicate entries)
- citations/sources.json created/updated
- All source files accessible in inputs/ directory

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Keeping relative paths | Convert to absolute paths |
| Not expanding globs | Use Bash or Glob to expand patterns |
| Skipping checksum calculation | Always calculate for integrity tracking |
| Missing deduplication | Check for existing entries before adding |
| Inconsistent ID generation | Use first 8 chars of checksum |
| Not saving fetched URLs | Write fetched content to inputs/ directory |

## Related Skills

- **source-integrity**: Validates checksums and metadata completeness
- **citation-compliance**: Uses sources.json for verification
- **link-verification**: Validates URL accessibility
- **content-intent-gathering**: Provides source inputs for normalization
- **research-processing**: Uses normalization for external sources

## Anti-Rationalization Blocks

Common excuses that are **explicitly rejected**:

| Rationalization | Reality |
|----------------|---------|
| "Relative path is fine" | Convert to absolute or fail. |
| "Skip checksum, not needed" | Always calculate for integrity. |
| "Duplicate entry is okay" | Deduplicate by checksum/URL/path. |
| "Fetched content doesn't need saving" | Save to inputs/ for offline access. |
