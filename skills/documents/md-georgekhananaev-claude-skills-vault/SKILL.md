---
name: md
description: Write clean, error-free markdown that IDEs and linters can parse without warnings. Use when writing documentation, README files, or skill files with code examples.
author: George Khananaev
---

# Markdown Clean Skill

Write clean, error-free markdown that IDEs and linters can parse without warnings.

## When to Use

Invoke this skill when:
- Writing markdown documentation
- Creating README files
- Writing skill files with code examples
- Commands: `/md-clean`, `/markdown`

## Common IDE Errors & Fixes

### 1. Nested Code Blocks

**Problem:** Code blocks inside code blocks cause parsing errors.

**Error:** `Newline or semicolon expected`

**Wrong:**
````markdown
```markdown
Here is example:
```js
const x = 1;
```
```
````

**Fix:** Use different fence lengths (4 backticks for outer):

`````markdown
````markdown
Here is example:
```js
const x = 1;
```
````
`````

**Or** use indentation for inner blocks:

````markdown
```markdown
Here is example:

    const x = 1;
```
````

### 2. Unclosed Code Blocks

**Problem:** Missing closing fence.

**Error:** `Statement expected`, `Expression expected`

**Wrong:**
```
```js
const x = 1;
// forgot to close
```

**Fix:** Always close with matching fence:

```
```js
const x = 1;
```                    <-- closing fence
```

### 3. Mismatched Fence Characters

**Problem:** Opening with backticks, closing with tildes (or vice versa).

**Error:** `Newline or semicolon expected`

**Wrong:**
```
```js
const x = 1;
~~~
```

**Fix:** Match opening and closing:

```
```js
const x = 1;
```
```

### 4. Special Characters in Code Blocks

**Problem:** Unescaped backticks inside code blocks.

**Error:** `Unexpected token`

**Wrong:**
````markdown
```markdown
Use `code` for inline.
```
````

**Fix:** Use more backticks for outer fence:

`````markdown
````markdown
Use `code` for inline.
````
`````

### 5. Pipe Characters in Tables

**Problem:** Unescaped `|` in table cells.

**Error:** `Column count mismatch`

**Wrong:**
```markdown
| Command | Description |
|---------|-------------|
| a | b | Creates a|b |
```

**Fix:** Escape with backslash:

```markdown
| Command | Description |
|---------|-------------|
| a \| b | Creates a\|b |
```

### 6. HTML in Markdown

**Problem:** Unclosed HTML tags.

**Error:** `Tag not closed`

**Wrong:**
```markdown
<details>
<summary>Click</summary>
Content here
```

**Fix:** Close all tags:

```markdown
<details>
<summary>Click</summary>
Content here
</details>
```

### 7. Link Syntax Errors

**Problem:** Malformed links.

**Error:** `) expected`, `] expected`

**Wrong:**
```markdown
[Link(https://example.com)
[Link][ref
```

**Fix:** Proper syntax:

```markdown
[Link](https://example.com)
[Link][ref]

[ref]: https://example.com
```

### 8. List Indentation

**Problem:** Inconsistent indentation in nested lists.

**Error:** `Unexpected indent`

**Wrong:**
```markdown
- Item 1
   - Nested (3 spaces - inconsistent)
  - Another (2 spaces)
```

**Fix:** Consistent indentation (2 or 4 spaces):

```markdown
- Item 1
  - Nested (2 spaces)
  - Another (2 spaces)
```

### 9. Heading Syntax

**Problem:** No space after `#`.

**Error:** May not render as heading

**Wrong:**
```markdown
#Heading
##Another
```

**Fix:** Space after `#`:

```markdown
# Heading
## Another
```

### 10. Empty Lines Around Blocks

**Problem:** Missing blank lines before/after code blocks.

**Error:** `Unexpected token`

**Wrong:**
```markdown
Some text
```js
code
```
More text
```

**Fix:** Add blank lines:

```markdown
Some text

```js
code
```

More text
```

## Fence Level Guide

Use increasing backticks for nesting:

| Level | Fence | Use For |
|-------|-------|---------|
| 1 | ``` | Normal code |
| 2 | ```` | Code containing ``` |
| 3 | ````` | Code containing ```` |
| 4 | `````` | Code containing ````` |

## Safe Markdown Template

```markdown
# Title

Brief description.

## Section 1

Regular paragraph text.

### Subsection

- List item 1
- List item 2
  - Nested item

## Code Example

```language
code here
```

## Table

| Col 1 | Col 2 |
|-------|-------|
| A | B |

## Links

- [Text](https://url.com)
- [Reference][ref]

[ref]: https://url.com
```

## Validation Checklist

Before saving markdown:

- [ ] All code blocks have closing fences
- [ ] Fence characters match (``` with ```)
- [ ] Nested blocks use longer fences
- [ ] Tables have equal column counts
- [ ] All pipes in tables are escaped
- [ ] HTML tags are closed
- [ ] Links have proper syntax
- [ ] Lists use consistent indentation
- [ ] Headings have space after #
- [ ] Blank lines around code blocks

## Quick Fixes

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| Semicolon expected | Unclosed fence | Add closing ``` |
| Statement expected | Nested fence conflict | Use ```` for outer |
| ) expected | Malformed link | Check [text](url) |
| Expression expected | Code in paragraph | Add blank lines |
| Column mismatch | Table pipe issue | Escape \| or fix columns |

## Escaping Reference

Characters to escape in specific contexts:

| Char | Context | Escape |
|------|---------|--------|
| ` | Inline code | Use `` for outer |
| ``` | Code block | Use ```` for outer |
| \| | Tables | \\\| |
| [ ] | Not a link | \[ \] |
| * _ | Not emphasis | \* \_ |
| # | Not heading | \# |
| < > | Not HTML | \< \> or &lt; &gt; |

## IDE-Specific Tips

### VS Code
- Install "markdownlint" extension
- Enable "Format on Save"
- Use preview pane to verify

### JetBrains (WebStorm, IntelliJ)
- Enable Markdown plugin
- Check "Problems" panel
- Use "Reformat Code" (Cmd/Ctrl+Alt+L)

### Vim/Neovim
- Use vim-markdown plugin
- Enable conceallevel for preview
- Run `:MarkdownPreview`

## Validation Script

Use the included validation script to check markdown files:

```bash
# Validate single file
python scripts/validate.py README.md

# Validate directory
python scripts/validate.py ./docs

# Sample output
README.md:15:1: error [MD001] Unclosed code block
    Suggestion: Add closing ``` fence
README.md:42:1: warning [MD003] No space after heading hashes
    Suggestion: Add space: ## Heading...
```

### Error Codes

| Code | Severity | Description |
|------|----------|-------------|
| MD001 | error | Unclosed code block |
| MD002 | warning | Nested fence conflict |
| MD003 | warning | No space after heading # |
| MD004 | warning | Inconsistent list indent |
| MD005 | error | Table column mismatch |
| MD006 | error | Malformed link syntax |
| MD007 | warning | Unclosed HTML tag |
| MD008 | info | Trailing whitespace |
| MD009 | info | No blank line around block |