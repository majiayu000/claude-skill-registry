---
name: obsidian-read-context
description: Analyze Obsidian vault documentation to understand current knowledge state. Use when exploring documentation structure, identifying gaps, or planning documentation consolidation.
---

# Obsidian Read Context Skill

Understand the current state of knowledge in an Obsidian vault by analyzing markdown files.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Scan and analyze Obsidian vault contents to identify topics, detect overlaps, find gaps, and suggest canonical document targets for consolidation.

## Background Knowledge

### What is an Obsidian Vault?

An Obsidian vault is a folder containing Markdown files that form a knowledge base. Key characteristics:

- **Markdown files**: Plain text with `.md` extension
- **Wikilinks**: Internal links using `[[double brackets]]` syntax
- **Frontmatter**: Optional YAML metadata at file start
- **Folders**: Organize notes by category or status (e.g., `_inbox`, `specs`, `design`)

### Common Vault Structures

```
vault/
├── _inbox/           # Unprocessed notes, quick captures
├── specs/            # Technical specifications
├── design/           # Design documents
├── notes/            # General notes
├── templates/        # Obsidian templates
└── README.md         # Vault overview
```

### Reading Modes

| Mode | Purpose | Depth |
|------|---------|-------|
| `skim` | Quick overview of structure and topics | Read titles, headings, frontmatter |
| `deep` | Full content analysis | Read entire file contents |

## Input Sources

The skill accepts:

- **Paths**: Single files or directories within the vault
- **Mode**: `skim` or `deep` analysis depth
- **Filters**: Optional file patterns to include/exclude

## Output Contract

Produce a structured analysis:

```json
{
  "vault_path": "/path/to/vault",
  "files_analyzed": 42,
  "mode": "skim | deep",
  "topics": [
    {
      "name": "Topic Name",
      "files": ["file1.md", "file2.md"],
      "coverage": "partial | complete | fragmented"
    }
  ],
  "overlaps": [
    {
      "topic": "Topic Name",
      "files": ["file1.md", "file2.md"],
      "description": "Both files cover X"
    }
  ],
  "gaps": [
    {
      "topic": "Topic Name",
      "description": "Missing coverage of X",
      "suggested_sources": ["file1.md mentions this"]
    }
  ],
  "suggested_canonicals": [
    {
      "target_path": "specs/feature-x.md",
      "title": "Feature X Specification",
      "source_files": ["_inbox/note1.md", "_inbox/note2.md"],
      "rationale": "Consolidate fragmented notes into spec"
    }
  ]
}
```

## Workflow

### 1. Identify Vault Boundary

Locate the vault root and verify it contains Obsidian markers:

```bash
# Check for .obsidian folder (indicates vault root)
ls -la /path/to/vault/.obsidian 2>/dev/null && echo "Vault confirmed"

# List top-level structure
ls -la /path/to/vault/
```

### 2. Gather File List

Enumerate markdown files in target paths:

```bash
# List all markdown files
find /path/to/vault -name "*.md" -type f

# Count files per directory
find /path/to/vault -name "*.md" -type f | xargs -I{} dirname {} | sort | uniq -c
```

### 3. Skim Mode Analysis

For quick overview, extract:

- File names and paths
- First-level headings (`# Heading`)
- Frontmatter keys
- Wikilink targets

```bash
# Extract headings from a file
grep -E "^#+ " /path/to/file.md

# Extract wikilinks
grep -oE "\[\[[^\]]+\]\]" /path/to/file.md
```

### 4. Deep Mode Analysis

For thorough analysis, additionally read:

- Full file content
- All heading levels
- Paragraph content for topic extraction
- Link relationships

### 5. Detect Topics and Patterns

Analyze collected data to identify:

- **Topics**: Recurring themes across files
- **Overlaps**: Multiple files covering same concepts
- **Gaps**: Referenced but undefined concepts
- **Orphans**: Files with no incoming links

### 6. Generate Suggestions

Based on analysis, propose:

- Canonical document targets for fragmented content
- Consolidation opportunities
- Missing documentation needs

## Example: Analyzing an Inbox

**Input:**
```
Path: vault/_inbox/
Mode: deep
```

**Analysis Process:**

1. List all files in `_inbox/`
2. Read each file's content
3. Extract topics and relationships
4. Identify consolidation opportunities

**Output:**

```json
{
  "vault_path": "vault",
  "files_analyzed": 5,
  "mode": "deep",
  "topics": [
    {
      "name": "Authentication",
      "files": ["_inbox/auth-notes.md", "_inbox/login-flow.md"],
      "coverage": "fragmented"
    },
    {
      "name": "Database Schema",
      "files": ["_inbox/db-thoughts.md"],
      "coverage": "partial"
    }
  ],
  "overlaps": [
    {
      "topic": "Authentication",
      "files": ["_inbox/auth-notes.md", "_inbox/login-flow.md"],
      "description": "Both cover OAuth flow with different details"
    }
  ],
  "gaps": [
    {
      "topic": "Error Handling",
      "description": "Referenced in auth notes but no dedicated coverage",
      "suggested_sources": ["_inbox/auth-notes.md line 42"]
    }
  ],
  "suggested_canonicals": [
    {
      "target_path": "specs/authentication.md",
      "title": "Authentication Specification",
      "source_files": ["_inbox/auth-notes.md", "_inbox/login-flow.md"],
      "rationale": "Consolidate fragmented auth documentation"
    }
  ]
}
```

## Policies

### Always

- Operate in **read-only** mode - never modify files
- Respect vault boundaries - only analyze specified paths
- Report uncertainty when topics are ambiguous
- Include source file references for all findings
- Use relative paths from vault root in output

### Never

- Modify, move, or delete any files
- Access files outside the specified vault/paths
- Make assumptions about file organization intent
- Infer meaning where content is genuinely ambiguous

### Handling Ambiguity

When encountering unclear content:

1. Flag the item as uncertain
2. Include the raw excerpt for human review
3. Suggest multiple possible interpretations if applicable
4. Do not force a single interpretation

## Integration

This skill works with:

- `obsidian-extract-inbox` - Use read context to inform extraction
- `obsidian-write-document` - Suggested canonicals inform document creation
- `obsidian-issue-from-doc` - Topics inform issue generation

## Output Format

When run, report:

1. Summary statistics (files analyzed, mode used)
2. The structured JSON analysis
3. Key findings highlighted for human review
4. Recommended next steps (which skills to invoke next)
