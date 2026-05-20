---
name: gfm
description: Use when writing or reviewing GitHub-flavored Markdown (README, issues, PRs, docs)
argument-hint: "[file | topic | review]"
---

# GitHub-Flavored Markdown

## Arguments
```
$ARGUMENTS
```

## Instructions

Parse arguments to determine task:
- **File path** → Write/edit markdown file
- **"review"** → Audit existing markdown for GFM best practices
- **Topic/description** → Draft markdown content

### Writing Guidelines

**Structure:**
- Use heading hierarchy (`#` through `######`)—GitHub auto-generates TOC for 2+ headings
- Prefer ATX headings (`#`) over Setext (`===`)
- One blank line before headings

**Text styling:**
| Style | Syntax |
|-------|--------|
| Bold | `**text**` |
| Italic | `_text_` |
| Bold+italic | `***text***` |
| Strikethrough | `~~text~~` |
| Code | `` `code` `` |
| Subscript | `<sub>x</sub>` |
| Superscript | `<sup>2</sup>` |

**Code blocks:**
````markdown
```language
code here
```
````

**Lists:**
- Unordered: use `-` consistently
- Ordered: `1.`, `2.`, etc.
- Task lists: `- [ ]` incomplete, `- [x]` complete
- Nest by aligning under parent text

**Links:**
- Inline: `[text](url)`
- Section anchors: `[text](#heading-name)` (lowercase, hyphens, no punctuation)
- Relative paths for repo files: `docs/CONTRIBUTING.md`

**Images:** `![alt text](url)` — always include alt text

**Alerts (callouts):**
```markdown
> [!NOTE]
> Useful information

> [!TIP]
> Helpful advice

> [!IMPORTANT]
> Essential info

> [!WARNING]
> Urgent attention

> [!CAUTION]
> Risk warning
```

**Footnotes:**
```markdown
Text with footnote[^1].

[^1]: Footnote content.
```

**Color swatches:** `` `#FF5733` ``, `` `rgb(255,87,51)` ``, `` `hsl(11,100%,60%)` ``

### Review Checklist

When reviewing markdown:
- [ ] Heading hierarchy is logical (no skipped levels)
- [ ] Code blocks specify language for syntax highlighting
- [ ] Links use relative paths for repo files
- [ ] Images have meaningful alt text
- [ ] Task lists use proper syntax
- [ ] Alerts use correct `> [!TYPE]` format
- [ ] No trailing whitespace except intentional line breaks
- [ ] Tables are properly aligned

## Examples

```
/gfm README.md                → Edit/create README
/gfm review docs/             → Audit markdown files in docs/
/gfm API documentation        → Draft API docs content
/gfm changelog entry          → Write changelog in GFM style
```
