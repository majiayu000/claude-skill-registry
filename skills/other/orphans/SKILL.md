---
context: fork
---

# /orphans

Find orphan notes (notes with no backlinks) using sub-agents for efficient scanning.

## Usage

```
/orphans
/orphans type:Meeting
/orphans --fix
```

## Instructions

### Phase 1: Planning

1. Determine scope:
   - All notes (default)
   - Specific type if provided
2. Plan the scan:
   - Get all notes in vault
   - Build link graph
   - Identify orphans

### Phase 2: Parallel Analysis (use sub-agents)

Launch these sub-agents in parallel using `model: "haiku"` for efficiency:

**Agent 1: Build Note Index** (Haiku)
- List all .md files in vault root and `+Meetings/` folder
- Extract: filename, type from frontmatter
- Return: complete note inventory

**Agent 2: Extract Outgoing Links** (Haiku)
- For each note, extract all [[wiki-links]]
- Build map: note → [linked notes]
- Return: outgoing link map

**Agent 3: Calculate Incoming Links** (Haiku)
- Invert the link map
- Build map: note → [notes linking to it]
- Return: incoming link counts

**Agent 4: Identify Special Cases** (Haiku)
- Find MOC files (should have many outgoing, few incoming)
- Find template files (expected orphans)
- Find daily notes (may not need links)
- Return: exclusion list

### Phase 3: Compile Results

```markdown
# Orphan Notes Report

**Scanned**: {{total notes}}
**Orphans Found**: {{count}}
**Generated**: {{DATE}}

## Summary

- Total notes: {{count}}
- With incoming links: {{count}} ({{%}})
- Orphans (no incoming): {{count}} ({{%}})
- Excluded (templates, MOCs): {{count}}

## Orphan Notes by Type

### Projects ({{count}})
These projects aren't referenced anywhere:
| Note | Created | Last Modified |
|------|---------|---------------|
{{orphan projects}}

### Meetings ({{count}})
Meetings not linked from any note:
{{orphan meetings}}

### People ({{count}})
People not mentioned in any note:
{{orphan people}}

### Pages ({{count}})
Documentation pages with no references:
{{orphan pages}}

### Tasks ({{count}})
Tasks not linked to projects:
{{orphan tasks}}

## Recommendations

### High Priority (should definitely be linked)
{{notes that seem important but have no links}}

### Consider Archiving
{{old notes with no links that may be obsolete}}

### Link Suggestions

| Orphan Note | Suggested Link From |
|-------------|---------------------|
{{AI-suggested connections based on content}}

## Quick Fixes

To link orphan meetings to their projects:
{{list of suggested edits}}
```

### --fix Mode

If `--fix` flag provided:
1. For each orphan meeting with a project in frontmatter, add link from project file
2. For each orphan person mentioned in meetings, add link from relevant meetings
3. Report changes made
