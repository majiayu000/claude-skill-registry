---
context: fork
---

# /attachment-audit

Audit all images and attachments in the vault using Sonnet sub-agents for comprehensive visual analysis.

## Usage

```
/attachment-audit
/attachment-audit --type images
/attachment-audit --unused
/attachment-audit --folder +Attachments/2025
```

## Instructions

This skill uses **Sonnet model sub-agents** for thorough analysis of vault attachments.

### Phase 1: Inventory

1. Scan `+Attachments/` folder for all files
2. Categorise by type (images, PDFs, documents)
3. Build list of files to analyse

### Phase 2: Comprehensive Analysis (Sonnet Sub-Agents)

Launch these sub-agents using `model: "sonnet"`:

**Agent 1: File Inventory** (Sonnet)
```
Task: Build complete attachment inventory
- List all files in +Attachments/ recursively
- Categorise by file type
- Get file sizes and modification dates
- Identify naming patterns
- Note any duplicates or similar names
Return: Complete file inventory with metadata
```

**Agent 2: Usage Analysis** (Sonnet)
```
Task: Analyse attachment usage across vault
- Search all markdown files for attachment references
- Map each attachment to notes that reference it
- Identify orphan attachments (not referenced anywhere)
- Find broken references (links to non-existent files)
- Note most frequently used attachments
Return: Usage map with orphan and broken link lists
```

**Agent 3: Image Content Analysis** (Sonnet)
```
Task: Analyse image contents for documentation
- For each image, read and analyse visually
- Categorise: screenshot, diagram, photo, document, other
- Identify what each image depicts
- Extract any visible text
- Note which images might need better filenames
- Identify potentially sensitive content
Return: Image content summary for each file
```

**Agent 4: Organisation Recommendations** (Sonnet)
```
Task: Recommend organisation improvements
- Assess current folder structure
- Identify files that should be renamed
- Suggest categorisation (by project, date, type)
- Find large files that could be compressed
- Recommend archival candidates
- Suggest metadata or tagging approach
Return: Organisation recommendations
```

### Phase 3: Compile Report

```markdown
# Attachment Audit Report

**Audit Date**: {{DATE}}
**Total Attachments**: {{count}}
**Total Size**: {{size}}

## Summary

{{Overview of attachment health and key findings}}

## Inventory

### By Type
| Type | Count | Size | % of Total |
|------|-------|------|------------|
| Images (PNG/JPG) | {{count}} | {{size}} | {{%}} |
| PDFs | {{count}} | {{size}} | {{%}} |
| Documents | {{count}} | {{size}} | {{%}} |
| Other | {{count}} | {{size}} | {{%}} |

### By Category (Content)
| Category | Count | Examples |
|----------|-------|----------|
| Screenshots | {{count}} | {{examples}} |
| Architecture Diagrams | {{count}} | {{examples}} |
| Process Flows | {{count}} | {{examples}} |
| Meeting Photos | {{count}} | {{examples}} |
| Documents/Scans | {{count}} | {{examples}} |
| Other | {{count}} | {{examples}} |

## Usage Analysis

### Well-Referenced (3+ links)
{{list of frequently used attachments}}

### Single Reference
{{attachments only used once}}

### Orphan Attachments (No References)
| File | Type | Size | Recommendation |
|------|------|------|----------------|
{{orphan files with suggested actions}}

### Broken References
| Note | Broken Link | Suggestion |
|------|-------------|------------|
{{notes with broken attachment links}}

## Content Summary

### Screenshots
{{summary of screenshot contents}}

### Diagrams
{{summary of diagram contents}}

### Documents
{{summary of document contents}}

## Issues Found

### Naming Issues
{{files with unclear or inconsistent names}}

### Large Files
{{files over 1MB that could be optimised}}

### Potential Duplicates
{{files that appear to be duplicates}}

### Sensitive Content
{{files that may contain sensitive information}}

## Recommendations

### Immediate Actions
1. {{high priority recommendation}}
2. {{high priority recommendation}}

### Rename Suggestions
| Current Name | Suggested Name | Reason |
|--------------|----------------|--------|
{{rename recommendations}}

### Archive Candidates
{{old or unused files that could be archived}}

### Folder Structure
{{suggested folder organisation}}

## Quick Fixes

To remove orphan attachments:
```bash
{{commands to clean up orphans}}
```

To fix broken links:
{{suggested edits}}
```

### Modes

**--type images**: Only analyse image files
**--unused**: Focus on orphan/unused attachments
**--folder <path>**: Limit to specific subfolder

### Notes

- Full audit can take several minutes for large vaults
- Image analysis provides content descriptions for better organisation
- Useful for vault maintenance and cleanup
