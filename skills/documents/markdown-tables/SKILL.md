---
name: markdown-tables
description: Use when creating or formatting tables in markdown. Covers table syntax, alignment, escaping, and best practices.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Markdown Tables

Comprehensive guide to creating and formatting tables in markdown.

## Basic Table Syntax

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

Renders as:

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

## Column Alignment

```markdown
| Left     | Center   | Right    |
|:---------|:--------:|---------:|
| Left     | Center   | Right    |
| aligned  | aligned  | aligned  |
```

Renders as:

| Left     | Center   | Right    |
|:---------|:--------:|---------:|
| Left     | Center   | aligned  |
| text     | text     | text     |

- `:---` Left align (default)
- `:--:` Center align
- `---:` Right align

## Minimum Syntax

The pipes and dashes don't need to align:

```markdown
|Header|Header|
|-|-|
|Cell|Cell|
```

However, aligned tables are more readable in source.

## Escaping Pipe Characters

Use `\|` to include a literal pipe in a cell:

```markdown
| Command | Description |
|---------|-------------|
| `a \| b` | Pipe operator |
| `cmd \|\| exit` | Or operator |
```

## Inline Formatting in Tables

Tables support inline markdown:

```markdown
| Feature | Syntax |
|---------|--------|
| **Bold** | `**text**` |
| *Italic* | `*text*` |
| `Code` | `` `code` `` |
| [Link](url) | `[text](url)` |
```

## Multi-line Cell Content

Standard markdown tables don't support multi-line cells. Workarounds:

### Using `<br>` Tags

```markdown
| Step | Description |
|------|-------------|
| 1 | First line<br>Second line |
| 2 | Another step |
```

### Using HTML Tables

For complex layouts, use HTML:

```html
<table>
  <tr>
    <th>Header</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Item</td>
    <td>
      <ul>
        <li>Point one</li>
        <li>Point two</li>
      </ul>
    </td>
  </tr>
</table>
```

## Empty Cells

Use a space or leave empty:

```markdown
| A | B | C |
|---|---|---|
| 1 |   | 3 |
| 4 | 5 |   |
```

## Wide Tables

For tables with many columns, consider:

### Scrollable Container (HTML)

```html
<div style="overflow-x: auto;">

| Col 1 | Col 2 | Col 3 | Col 4 | Col 5 | Col 6 |
|-------|-------|-------|-------|-------|-------|
| Data  | Data  | Data  | Data  | Data  | Data  |

</div>
```

### Vertical Layout

Transform wide tables into key-value pairs:

```markdown
### Item 1

| Property | Value |
|----------|-------|
| Name     | Foo   |
| Type     | Bar   |
| Status   | Active |
```

## Common Table Patterns

### Comparison Table

```markdown
| Feature | Free | Pro | Enterprise |
|---------|:----:|:---:|:----------:|
| Users   | 5    | 50  | Unlimited  |
| Storage | 1GB  | 10GB| 100GB      |
| Support | ❌   | ✅  | ✅         |
```

### API Reference

```markdown
| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `id`      | string | ✅ | Unique identifier |
| `name`    | string | ✅ | Display name |
| `limit`   | number | ❌ | Max results (default: 10) |
```

### Keyboard Shortcuts

```markdown
| Action | Windows/Linux | macOS |
|--------|---------------|-------|
| Copy   | `Ctrl+C`      | `⌘+C` |
| Paste  | `Ctrl+V`      | `⌘+V` |
| Undo   | `Ctrl+Z`      | `⌘+Z` |
```

### Changelog

```markdown
| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024-01-15 | Breaking: New API |
| 1.2.0 | 2024-01-01 | Added feature X |
| 1.1.0 | 2023-12-15 | Bug fixes |
```

## Best Practices

1. **Keep tables simple**: If content is complex, consider alternatives
2. **Use consistent alignment**: Align source pipes for readability
3. **Header row required**: Always include a header row
4. **Escape special characters**: Use `\|` for literal pipes
5. **Limit columns**: Wide tables are hard to read
6. **Consider alternatives**: Lists or definition lists may work better
7. **Test rendering**: Tables render differently across platforms

## Markdownlint Rules for Tables

| Rule | Description |
|------|-------------|
| MD055 | Table pipe style should be consistent |
| MD056 | Table column count should match header |
| MD058 | Tables should be surrounded by blank lines |

## Alternatives to Tables

### Definition Lists (Some Parsers)

```markdown
Term 1
: Definition 1

Term 2
: Definition 2
```

### Bullet Lists with Bold Keys

```markdown
- **Name**: John Doe
- **Email**: john@example.com
- **Role**: Developer
```

### Nested Lists

```markdown
- Item 1
  - Property A: Value
  - Property B: Value
- Item 2
  - Property A: Value
  - Property B: Value
```
