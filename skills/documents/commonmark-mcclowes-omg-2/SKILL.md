---
name: commonmark
# prettier-ignore
description: Use when parsing or generating Markdown following the CommonMark specification - AST structure, block/inline elements, and extensions
---

# CommonMark Markdown

## Quick Start

```typescript
import { Parser, HtmlRenderer } from 'commonmark';

const parser = new Parser();
const renderer = new HtmlRenderer();

const ast = parser.parse('# Hello\n\nWorld');
const html = renderer.render(ast);
```

## AST Node Types

### Block Elements

| Type | Description |
|------|-------------|
| `document` | Root node |
| `heading` | `# ` through `###### ` |
| `paragraph` | Text block |
| `code_block` | Fenced (```) or indented |
| `block_quote` | `> ` prefixed |
| `list` | Ordered or bullet list |
| `item` | List item |
| `thematic_break` | `---`, `***`, `___` |

### Inline Elements

| Type | Description |
|------|-------------|
| `text` | Plain text |
| `emph` | `*italic*` or `_italic_` |
| `strong` | `**bold**` or `__bold__` |
| `code` | `` `inline` `` |
| `link` | `[text](url)` |
| `image` | `![alt](src)` |
| `softbreak` | Line break in source |
| `hardbreak` | Two spaces + newline |

## Walking the AST

```typescript
const walker = ast.walker();
let event;
while ((event = walker.next())) {
  const { node, entering } = event;
  if (node.type === 'heading' && entering) {
    console.log(`H${node.level}: ${node.firstChild?.literal}`);
  }
}
```

## Key Parsing Rules

- Blank line separates paragraphs
- 4-space indent = code block (unless in list)
- Fenced code: 3+ backticks, optional info string
- Setext headings: `===` or `---` underline
- Links: `[text](url "title")` or `[text][ref]`

## Extensions (GFM)

GitHub Flavored Markdown adds:
- Tables: `| col | col |`
- Strikethrough: `~~text~~`
- Task lists: `- [ ]` and `- [x]`
- Autolinks: URLs become links automatically

## Tips

- Use `node.literal` for text content
- Use `node.destination` for link/image URLs
- `node.info` contains fenced code language
- Modify AST before rendering for transformations
