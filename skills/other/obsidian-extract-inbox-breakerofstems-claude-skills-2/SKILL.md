---
name: obsidian-extract-inbox
description: Extract structured document proposals from messy inbox notes. Use when processing raw notes in _inbox folders to prepare them for canonical documentation.
---

# Obsidian Extract Inbox Skill

Turn messy inbox notes into structured document proposals without modifying any files.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Analyze raw notes from an Obsidian inbox and generate structured proposals for canonical documents, flagging uncertain items for human review.

## Background Knowledge

### What is an Inbox?

In Obsidian workflows, the `_inbox` (or similar) folder serves as a capture zone for:

- Quick notes and thoughts
- Copied content from other sources
- Drafts and fragments
- Unprocessed information awaiting organization

### Inbox Characteristics

Inbox notes typically have:

- Inconsistent formatting
- Mixed topics in single files
- Incomplete thoughts
- Informal language
- Missing context
- Redundant information across files

### Extraction Goals

Transform inbox content into:

- Clear document proposals with defined scope
- Identified source fragments
- Flagged uncertainties
- Suggested target paths

## Input Sources

The skill accepts:

- **Inbox path**: Directory containing raw notes
- **File list**: Optional specific files to process
- **Context**: Optional output from `obsidian-read-context`

## Output Contract

Produce a structured extraction result (this is **output only**, not file modifications):

```json
{
  "inbox_path": "_inbox/",
  "files_processed": 3,
  "proposals": [
    {
      "id": "proposal-1",
      "title": "Proposed Document Title",
      "target_path": "specs/document-name.md",
      "type": "spec | design | reference | guide",
      "summary": "One-paragraph description of document scope",
      "source_fragments": [
        {
          "file": "_inbox/note1.md",
          "lines": "15-42",
          "excerpt": "Relevant content excerpt...",
          "confidence": "high | medium | low"
        }
      ],
      "suggested_sections": [
        "Overview",
        "Requirements",
        "Implementation Notes"
      ],
      "dependencies": ["[[other-doc]]"],
      "confidence": "high | medium | low"
    }
  ],
  "uncertain_items": [
    {
      "file": "_inbox/note2.md",
      "lines": "5-10",
      "content": "Ambiguous content...",
      "reason": "Cannot determine if this is a requirement or a question",
      "possible_interpretations": [
        "Could be a feature request",
        "Could be a bug report"
      ]
    }
  ],
  "unprocessable": [
    {
      "file": "_inbox/corrupt.md",
      "reason": "File appears to be binary or corrupted"
    }
  ]
}
```

## Workflow

### 1. Enumerate Inbox Contents

List and categorize inbox files:

```bash
# List inbox files
ls -la /path/to/vault/_inbox/

# Check file types
file /path/to/vault/_inbox/*.md
```

### 2. Read and Parse Each File

For each file, extract:

- Frontmatter (if present)
- Headings structure
- Main content blocks
- Wikilinks and references
- Apparent topics

### 3. Identify Document Boundaries

Analyze content to determine:

- Where one topic ends and another begins
- Which fragments belong together
- What constitutes a complete "document unit"

**Signals for document boundaries:**

- Heading level 1 (`#`) often indicates new topic
- Clear topic shifts in content
- Date markers suggesting separate captures
- Explicit separators (`---`, `***`)

### 4. Generate Document Proposals

For each identified document unit:

1. **Title**: Derive from content or headings
2. **Target path**: Suggest appropriate location
3. **Type**: Classify the document type
4. **Source fragments**: Map back to original locations
5. **Confidence**: Assess certainty of interpretation

### 5. Flag Uncertainties

Mark items as uncertain when:

- Intent is ambiguous (question vs. statement)
- Multiple valid interpretations exist
- Context is missing
- Content appears incomplete

### 6. Report Unprocessable Items

Flag files that cannot be processed:

- Binary files
- Corrupted content
- Non-markdown files
- Empty files

## Example: Processing Legacy Notes

**Input file: `_inbox/legacy.md`**

```markdown
# Old Design Notes

## Auth stuff
Need OAuth for login. Maybe JWT tokens?
Check with team about refresh tokens.

---

## Database thoughts
- Users table
- Sessions table
- Need to handle migrations

This might conflict with the new schema proposal.

## Random TODO
- Buy coffee
- Fix that bug
- Ask about deadline
```

**Extraction Output:**

```json
{
  "inbox_path": "_inbox/",
  "files_processed": 1,
  "proposals": [
    {
      "id": "proposal-1",
      "title": "Authentication Design",
      "target_path": "design/authentication.md",
      "type": "design",
      "summary": "Design notes for authentication system including OAuth and JWT considerations",
      "source_fragments": [
        {
          "file": "_inbox/legacy.md",
          "lines": "3-5",
          "excerpt": "Need OAuth for login. Maybe JWT tokens? Check with team about refresh tokens.",
          "confidence": "medium"
        }
      ],
      "suggested_sections": [
        "Overview",
        "OAuth Integration",
        "Token Strategy",
        "Open Questions"
      ],
      "dependencies": [],
      "confidence": "medium"
    },
    {
      "id": "proposal-2",
      "title": "Database Schema",
      "target_path": "design/database-schema.md",
      "type": "design",
      "summary": "Database schema design covering user and session tables with migration considerations",
      "source_fragments": [
        {
          "file": "_inbox/legacy.md",
          "lines": "9-13",
          "excerpt": "- Users table\n- Sessions table\n- Need to handle migrations\n\nThis might conflict with the new schema proposal.",
          "confidence": "medium"
        }
      ],
      "suggested_sections": [
        "Tables",
        "Migrations",
        "Conflicts and Dependencies"
      ],
      "dependencies": ["[[schema-proposal]]"],
      "confidence": "medium"
    }
  ],
  "uncertain_items": [
    {
      "file": "_inbox/legacy.md",
      "lines": "4",
      "content": "Maybe JWT tokens?",
      "reason": "Unclear if this is a decision or open question",
      "possible_interpretations": [
        "Decision to use JWT tokens",
        "Open question about whether to use JWT"
      ]
    },
    {
      "file": "_inbox/legacy.md",
      "lines": "5",
      "content": "Check with team about refresh tokens.",
      "reason": "Action item - unclear if still pending",
      "possible_interpretations": [
        "Pending action item",
        "Completed action (historical note)"
      ]
    }
  ],
  "unprocessable": []
}
```

**Note:** The "Random TODO" section was intentionally excluded as it contains personal tasks unrelated to documentation.

## Confidence Levels

| Level | Meaning | Action |
|-------|---------|--------|
| `high` | Clear intent, unambiguous content | Safe to proceed with proposal |
| `medium` | Reasonable interpretation, some assumptions | Review recommended before proceeding |
| `low` | Significant ambiguity or missing context | Requires human clarification |

## Policies

### Always

- **Read-only operation** - never write, modify, or delete files
- Include source file and line references for traceability
- Flag genuinely ambiguous content rather than guessing
- Preserve original wording in excerpts
- Report confidence levels honestly
- Exclude obviously personal/unrelated content from proposals

### Never

- Write any files to the filesystem
- Assume intent where genuinely ambiguous
- Fabricate content not present in source files
- Ignore or silently skip problematic content
- Force low-confidence items into proposals

### Handling Mixed Content

When a file contains mixed topics:

1. Identify natural boundaries
2. Create separate proposals for each topic
3. Note the shared source file
4. Flag if boundaries are unclear

### Handling Incomplete Information

When content is incomplete:

1. Mark confidence as `low`
2. Note what information is missing
3. Suggest what would be needed to complete
4. Do not fill gaps with assumptions

## Integration

This skill works with:

- `obsidian-read-context` - Provides context for better extraction
- `obsidian-write-document` - Consumes proposals to create documents
- `obsidian-issue-from-doc` - Proposals may inform issue creation

## Output Format

When run, report:

1. Summary of files processed and proposals generated
2. The structured JSON extraction result
3. Highlighted uncertain items requiring human review
4. Recommended next steps:
   - Which proposals are ready for `obsidian-write-document`
   - Which items need human clarification first
