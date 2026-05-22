---
name: obsidian-links
description: Format and validate Obsidian wiki links with proper filename, section, and folder conventions. Verify links exist before creation and fix broken links. Use when creating or checking wiki links in markdown files.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
license: MIT
---

# Obsidian Wiki Links

Format, validate, and fix wiki links according to vault conventions.

## When to Use This Skill

Activate when you need to:
- Create wiki links to other vault files
- Add section links to specific headers
- Format links in YAML frontmatter properties
- Verify links point to existing files/sections
- Find and fix broken links
- Validate link integrity in documents

## Core Link Formatting Rules

### 1. Complete Filename Format

**Always use full filename with date prefix**:
```markdown
✅ CORRECT: [[2025-10-31 Project Notes]]
❌ INCORRECT: [[Project Notes]] (missing date)
❌ INCORRECT: [[2025-10-31]] (missing title)
```

### 2. Folder Path Conventions

**Include folder prefix for clarity**:
```markdown
✅ CORRECT: [[Journal/2025-10-31]]
✅ CORRECT: [[Articles/2025-10-31 Perennial Seller]]
✅ CORRECT: [[Roundup/2025-10-31]]
```

**Rule**: Use consistent folder prefixes for clarity and navigation.

### 3. Section Links

**Use exact header text, character-for-character**:
```markdown
Source file header:
## PKM System Maintenance

✅ CORRECT:
[[Journal/2025-10-31#PKM System Maintenance]]

❌ INCORRECT:
[[Journal/2025-10-31#PKM System]] (truncated)
[[Journal/2025-10-31#pkm-system-maintenance]] (slug format)
```

**Critical**: Match characters, punctuation, spacing exactly as written.

### 4. Link to Sources, Not Indices

**Always link to original content, not topic aggregations**:
```markdown
✅ CORRECT: [[Articles/2025-08-15 Skill Development]]
❌ INCORRECT: [[Topics/Career#Skill Development]]

Reason: Maintains source attribution and traceability
```

### 5. Properties Link Format

**Wrap links in quotes when used in YAML lists**:
```yaml
sources:
  - "[[Journal/2025-10-31]]"
  - "[[Articles/2025-10-31 Title]]"

links:
  - "[[Roundup/2025-10-31]]"

attendees:
  - "[[People/John]]"
```

## Link Validation Principles

### 1. Search Before Link

**ALWAYS verify target exists before creating link**:
```markdown
Process:
1. Search for target file using Glob or Grep
2. Verify file exists
3. If section link, read file and verify header exists
4. Create link with exact filename and header text

❌ NEVER:
- Guess at filenames
- Assume files exist
- Fabricate section headers
```

### 2. Verify Section Headers

**For section links, read source and match exactly**:
```markdown
Steps:
1. Read target file
2. Search for exact header text
3. Copy character-for-character (including special characters)
4. Create section link

If unsure about exact header:
✅ Link to file only: [[Journal/2025-10-31]]
❌ Don't guess: [[Journal/2025-10-31#Guessed Header]]
```

### 3. File Existence Checking

**Use appropriate tools to verify files**:
```markdown
For specific file:
- Use Glob with full path pattern: "Journal/2025-10-31.md"
- Or Read the file directly

For finding files by keyword:
- Use Glob with pattern: "Articles/**/*keyword*.md"
- Check Topics directory before linking to topics
```

### 4. Fix Broken Links Immediately

**When you find broken links, fix them**:
```markdown
Process:
1. Identify broken link
2. Search for correct target file
3. Update link with correct path/filename (use Edit tool)
4. Verify section header if applicable
5. Report fix to user
```

## Complete Workflow

### Creating New Links (Format + Validate)

```markdown
Step 1: Determine Target
- Identify file to link to
- Note folder location
- Note complete filename

Step 2: Verify File Exists
- Use Glob: "**/{filename}.md"
- Or Read file directly
- If not found, search by keyword

Step 3: Verify Section (if needed)
- Read target file
- Search for exact header text
- Copy character-for-character
- If unsure, link to file only

Step 4: Format Link
- Use complete filename: [[YYYY-MM-DD Title]]
- Add folder prefix
- Add section if verified: [[File#Exact Header]]
- Wrap in quotes if in YAML property

Step 5: Create Link
- Link points to existing file
- Section header matches exactly (if used)
- Follows folder prefix conventions
```

### Finding and Fixing Broken Links

```markdown
Step 1: Detection
- Read document content
- Extract all wiki links
- For each link, verify file exists
- For section links, verify header exists

Step 2: Search for Correct Target
- Use context to determine intent
- Search vault with Glob/Grep
- Verify file exists

Step 3: Fix Link
- Use Edit tool to update broken link
- Replace with correct path/filename
- Verify section header if applicable

Step 4: Report
- Show old link (broken)
- Show new link (fixed)
- Explain reason for fix
```

## Special Cases

### Journal/Daily Files
```markdown
Path: Journal/YYYY-MM-DD.md
Format: [[Journal/YYYY-MM-DD]]

Section links:
- Headers may vary by language
- ALWAYS verify exact text before linking
- If unsure, link to file only

Validation:
1. Check file: Journal/YYYY-MM-DD.md
2. Read file content
3. Search for exact header
4. Use exact match or file-only link
```

### Topic Links
```markdown
CRITICAL: Search Topics directory BEFORE linking

Validation:
1. Use Glob: "Topics/**/*{keyword}*.md"
2. Find matching topic page
3. Use complete category path

Examples:
- [[Topics/Technology/PKM]]
- [[Topics/Career/Skills]]

❌ NEVER link to non-existent topic pages
```

### Person Names
```markdown
Simple name: [[John]]
With context: [[People/John]] (if folder exists)

Validation: Verify person file exists before linking
```

## Quality Checklist

Before completing link operations:

**Formatting**:
- [ ] All links use complete filenames
- [ ] Folder prefixes follow conventions
- [ ] Section headers match exactly (character-for-character)
- [ ] Links in YAML properties are wrapped in quotes
- [ ] All links point to sources, not topic indices

**Validation**:
- [ ] All target files verified to exist
- [ ] Section headers verified (not guessed)
- [ ] Topic links point to existing topic pages
- [ ] Broken links identified and fixed
