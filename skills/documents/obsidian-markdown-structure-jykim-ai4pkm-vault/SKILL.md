---
name: obsidian-markdown-structure
description: Validate and enforce markdown document structure including frontmatter positioning, heading hierarchy, and content organization. Use when creating or validating markdown files.
allowed-tools:
  - Read
  - Edit
license: MIT
---

# Markdown Structure Validation

Enforce consistent markdown structure across all vault content.

## When to Use This Skill

Activate when you need to:
- Create new markdown documents
- Validate document structure
- Fix structural issues
- Ensure consistent formatting

## Core Structure Rules

### 1. Frontmatter Positioning

**Single YAML block at top, blank line after**:
```markdown
✅ CORRECT:
---
title: Document Title
created: 2025-10-31
tags:
  - tag1
---

## First Section Header
Content starts here...

❌ INCORRECT:
---
title: Document Title
---
## First Section (no blank line)

❌ INCORRECT:
## Title

---
frontmatter: here
---
(frontmatter not at top)
```

**Critical Rules**:
- One YAML block only
- Must be first thing in file
- Blank line after closing `---`
- No content before first heading

> **Note**: This skill validates frontmatter **POSITION** (where it goes in the document).
> For frontmatter **CONTENT** (properties, values, formatting), use `obsidian-yaml-frontmatter` skill.

### 2. Heading Hierarchy

**Start with H2, no H1 duplication**:
```markdown
✅ CORRECT:
---
title: Document Title
---

## Introduction
Content...

### Subsection
Content...

❌ INCORRECT:
# Document Title (duplicates frontmatter title)

## Section
```

**Hierarchy Rules**:
- Use H2 (`##`) for main sections
- Use H3 (`###`) for subsections
- Use H4 (`####`) sparingly
- Don't skip levels (H2 → H4)

### 3. Content Organization

**Summary-first structure**:
```markdown
✅ CORRECT:
---
frontmatter
---

## Summary
Overview of key points...

## Main Content
Detailed content...

## Related Topics
Links and connections...

❌ INCORRECT:
---
frontmatter
---

This is content without a heading.

## First Section
```

### 4. Quote Block Formatting

**Blockquotes with attribution**:
```markdown
✅ CORRECT:
> "Quote text here" - Speaker/Context

> "Knowledge is power, but enthusiasm pulls the switch."
> - Ivern Ball

❌ INCORRECT:
"Quote text" (not in blockquote)
> Quote without attribution
```

## Structure Validation Workflow

### Step 1: Check Frontmatter
```markdown
Verify:
- [ ] Single YAML block at top
- [ ] Blank line after closing ---
- [ ] All required properties present
- [ ] Consistent property names
```

### Step 2: Check Heading Hierarchy
```markdown
Verify:
- [ ] No H1 after frontmatter (except special cases)
- [ ] Main sections use H2
- [ ] Subsections use H3
- [ ] No skipped levels
- [ ] Logical organization
```

### Step 3: Check Content Organization
```markdown
Verify:
- [ ] No content before first heading
- [ ] Summary/overview section first
- [ ] Sections follow logical order
- [ ] Proper quote formatting
```

### Step 4: Content-Type Specific
```markdown
Check content follows appropriate template structure:
- [ ] Journal: H1 title, standard sections
- [ ] Roundup: Opening quote(s), structured headers
- [ ] Events: Executive Summary, Key Takeaways, Next Actions
- [ ] Clippings: Summary first, then detailed sections
```

## Quality Checklist

Before completing structure validation:
- [ ] Single YAML frontmatter at top
- [ ] Blank line after frontmatter
- [ ] No content before first heading
- [ ] Heading hierarchy correct (H2 → H3 → H4)
- [ ] Quote blocks properly formatted
- [ ] Summary/overview section present
- [ ] Sections in logical order
- [ ] Template structure followed for content type
