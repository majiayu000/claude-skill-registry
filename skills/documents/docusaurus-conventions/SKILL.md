---
name: docusaurus-conventions
description: Docusaurus file naming, syntax, and structure conventions for RoboLearn platform
domain: authoring
version: 1.0.0
created: 2025-11-29
triggers:
  - Creating lesson files
  - Creating module/chapter structure
  - Writing MDX content
  - Fixing Docusaurus build errors
learned_from:
  - Module 1 ROS 2 implementation (2025-11-29)
  - 8 file extension fixes, 10 mermaid removals, 3 MDX syntax errors
---

# Docusaurus Conventions Skill

## Persona

Think like a Docusaurus expert who ensures all content builds successfully on the first attempt. You understand the quirks of MDX parsing, file naming conventions, and how Docusaurus resolves document IDs.

---

## Pre-Flight Questions

Before creating or modifying any Docusaurus content, ask yourself:

### 1. File Naming
- **Q**: What file extension should I use?
  - **A**: Always `.md` (NOT `.mdx`)
  - **Why**: The project doesn't use MDX components; `.mdx` causes unnecessary complexity

- **Q**: What should chapter/module index files be named?
  - **A**: Always `README.md` (NOT `index.md`)
  - **Why**: Docusaurus resolves `README.md` as the index; `index.md` can cause duplicate ID errors

- **Q**: What naming pattern for lesson files?
  - **A**: `NN-descriptive-name.md` (e.g., `01-digital-to-physical.md`)
  - **Why**: Numeric prefix ensures correct ordering; descriptive name aids navigation

### 2. MDX Syntax Safety
- **Q**: Does my content contain `<` characters outside of code blocks?
  - **A**: Replace with spelled-out alternatives
  - **Examples**:
    - `<2 seconds` → `less than 2 seconds`
    - `<10 hours` → `under 10 hours`
    - `[<10 hrs` → `[under 10 hrs`
  - **Why**: MDX parser interprets `<` as JSX tag start, causing build errors

- **Q**: Am I using comparison operators in prose?
  - **A**: Use words instead of symbols
  - **Examples**:
    - `latency < 100ms` → `latency under 100ms` or use inline code: `latency < 100ms`
    - `if (x < 5)` in code block is fine (code blocks are not parsed as MDX)

### 3. Diagrams
- **Q**: Am I using Mermaid diagrams?
  - **A**: NO - Mermaid plugin is not configured
  - **Alternatives**:
    - ASCII text diagrams for simple flows
    - Image files for complex diagrams
    - Code blocks showing structure
  - **Example replacement**:
    ```
    # Instead of mermaid:
    ```mermaid
    graph TD
      A --> B
    ```

    # Use ASCII:
    ```
    A → B → C
    └── D
    ```
    ```

### 4. Internal Links
- **Q**: How should I link to other lessons?
  - **A**: Use relative paths with `.md` extension
  - **Examples**:
    - Same chapter: `[Next](./02-next-lesson.md)`
    - Different chapter: `[Overview](../chapter-2-topic/README.md)`
    - Module root: `[Module](../README.md)`
  - **Never use**: `.mdx` extension or `index.md`

---

## Principles

### Principle 1: Build-First Validation
**Before committing any content, verify it builds.**

```bash
npm run build 2>&1 | tail -30
```

Expected: `[SUCCESS] Generated static files in "build"`

If errors:
1. Check for duplicate doc IDs (two files with same `id` frontmatter)
2. Check for MDX syntax errors (unexpected character errors)
3. Check for broken links (file not found warnings)

### Principle 2: Consistent File Structure

**Module structure:**
```
docs/module-N-name/
├── README.md                    # Module overview (NOT index.md)
├── chapter-1-topic/
│   ├── README.md                # Chapter overview
│   ├── 01-first-lesson.md
│   ├── 02-second-lesson.md
│   └── ...
├── chapter-2-topic/
│   └── ...
└── ...
```

### Principle 3: Frontmatter ID Uniqueness

**Every lesson must have unique `id`:**
```yaml
---
id: lesson-1-1-digital-to-physical   # Unique across entire docs folder
title: "Lesson 1.1: From ChatGPT to Walking Robots"
---
```

**ID pattern**: `lesson-{chapter}-{lesson}-{slug}`
- `lesson-1-1-digital-to-physical`
- `lesson-3-2-turtlesim-action`
- `custom-messages` (for standalone topics)

### Principle 4: Safe Text Patterns

**Avoid these patterns in prose (outside code blocks):**

| Pattern | Problem | Solution |
|---------|---------|----------|
| `<N` | JSX parsing | `less than N`, `under N` |
| `>N` | JSX parsing | `more than N`, `over N` |
| `{var}` | JSX interpolation | Use code: `` `{var}` `` |
| `<Component>` | JSX component | Use code or escape |

**Safe in code blocks:**
```python
if x < 5:  # This is fine - inside code block
    pass
```

---

## Checklist (Use Before Every Lesson Creation)

- [ ] File extension is `.md` (not `.mdx`)
- [ ] Index files named `README.md` (not `index.md`)
- [ ] Unique `id` in frontmatter
- [ ] No `<` or `>` in prose outside code blocks
- [ ] No Mermaid diagrams (use ASCII or images)
- [ ] Internal links use `.md` extension
- [ ] Internal links use `README.md` not `index.md`
- [ ] Build passes: `npm run build`

---

## Recovery Patterns

### Fix: Duplicate Doc ID Error
```
Error: The docs plugin found docs sharing the same id
```
**Solution**:
1. Delete one of the duplicate files
2. Or change the `id` in frontmatter to be unique

### Fix: MDX Syntax Error
```
Unexpected character 'N' (U+004E) before name
```
**Solution**:
1. Find the `<` character in prose
2. Replace with word equivalent (`less than`, `under`)
3. Or wrap in inline code

### Fix: Mermaid Not Rendering
**Solution**:
1. Replace mermaid block with ASCII text diagram
2. Or create image and reference it

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2025-11-29 | Initial skill from Module 1 lessons learned |
