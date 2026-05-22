---
name: docx-editing-superdoc
description: Programmatically edit Word documents (.docx) with live preview and track changes via SuperDoc VS Code extension. Use when editing DOCX files, making tracked changes, redlining, marking up contracts, or when the user wants to modify Word documents with insertions/deletions visible. Triggers on docx, Word, track changes, redline, markup.
metadata:
  author: Antoine Louis
  license: AGPL-3.0
  version: 2026.01.29
---

# DOCX Live Editor

Edit Word documents with live preview and track changes in VS Code-compatible IDEs via [SuperDoc extension](https://github.com/lawvable/superdoc-vscode-extension/tree/feat/programmatic-command-api).

## How It Works

1. Write custom command to `path/to/.superdoc/{docname}.json`
2. Extension executes and overwrites file with response
3. Changes appear live in SuperDoc webview.

**State:** `"command"` field = pending | `"success"` field = response ready

## Prerequisites

1. SuperDoc VS Code extension installed. Check with:
    ```
    // macOS/Linux
    $(case "$(ps -p $PPID -o args= 2>/dev/null)" in *Cursor*) echo cursor ;; *Antigravity*) echo antigravity ;; *Code*) echo code ;; *) echo code ;; esac) --profile "Lawvable" --list-extensions | grep -i superdoc

    // Windows (PowerShell)
    $cli = switch -Regex ((Get-Process -Id (Get-CimInstance Win32_Process -Filter "ProcessId=$PID").ParentProcessId).ProcessName) { 'Cursor' { 'cursor' } 'Antigravity' { 'antigravity' } default { 'code' } }; & $cli --profile "Lawvable" --list-extensions | Select-String superdoc
    ```

2. Document must be open in VS Code/Cursor/Antigravity before editing. Open with:
    ```
    // macOS/Linux
    $(case "$(ps -p $PPID -o args= 2>/dev/null)" in *Cursor*) echo cursor ;; *Antigravity*) echo antigravity ;; *Code*) echo code ;; *) echo code ;; esac) path/to/doc.docx

    // Windows (PowerShell)
    $cli = switch -Regex ((Get-Process -Id (Get-CimInstance Win32_Process -Filter "ProcessId=$PID").ParentProcessId).ProcessName) { 'Cursor' { 'cursor' } 'Antigravity' { 'antigravity' } default { 'code' } }; & $cli path/to/doc.docx
    ```

3. To create a new blank document:
    ```
    // macOS/Linux
    $(case "$(ps -p $PPID -o args= 2>/dev/null)" in *Cursor*) echo cursor ;; *Antigravity*) echo antigravity ;; *Code*) echo code ;; *) echo code ;; esac) --open-url "vscode://superdoc.superdoc-vscode-extension/create?path=./new-document.docx"

    // Windows (PowerShell)
    $cli = switch -Regex ((Get-Process -Id (Get-CimInstance Win32_Process -Filter "ProcessId=$PID").ParentProcessId).ProcessName) { 'Cursor' { 'cursor' } 'Antigravity' { 'antigravity' } default { 'code' } }; & $cli --open-url "vscode://superdoc.superdoc-vscode-extension/create?path=./new-document.docx"
    ```
    The path can be relative (to workspace) or absolute. The `.docx` extension is added automatically if missing.

## File Structure

The `.superdoc/` folder must be **in the same directory** as the DOCX file. The JSON file uses the same basename as the DOCX:

```
project/
├── contract.docx              ← document at root
├── .superdoc/
│   └── contract.json          ← commands for contract.docx
└── subfolder/
    ├── report.docx            ← document in subfolder
    └── .superdoc/
        └── report.json        ← commands for subfolder/report.docx
```

## Commands

### `getText` - Read Document Content

```json
// Get both text and HTML (default)
{"command":"getText","args":{}}

// Get only plain text (fewer tokens)
{"command":"getText","args":{"format":"text"}}

// Get only HTML (preserves structure)
{"command":"getText","args":{"format":"html"}}
```

**Formats:** `text` (plain text with paragraph breaks), `html` (full HTML), `both` (default)

### `getNodes` - Get Document Structure

Get all nodes of a specific type with their positions. Useful for understanding document structure before making edits.

```json
// Get all paragraphs (use to identify section titles for TOC)
{"command":"getNodes","args":{"type":"paragraph"}}

// Get all tables
{"command":"getNodes","args":{"type":"table"}}
```

**Valid types:** `paragraph`, `table`, `tableRow`, `tableCell`, `bulletList`, `orderedList`, `listItem`, `image`, `blockquote`

**Returns:**
```json
{
  "nodes": [
    {"index": 0, "type": "paragraph", "from": 0, "to": 31, "text": "Non-Disclosure Agreement", "textLength": 24},
    {"index": 1, "type": "paragraph", "from": 227, "to": 241, "text": "Background", "textLength": 10},
    {"index": 2, "type": "paragraph", "from": 586, "to": 601, "text": "Definitions", "textLength": 11, "marker": "1."}
  ],
  "count": 3
}
```

### `replaceText` - Find and Replace (DELETION + INSERTION)

**Use when:** Changing existing text to something different. The found text is DELETED and replaced.
**Track changes effect:** Shows as ~~deleted text~~ + <u>new text</u> (strikethrough + underline).

```json
// Change a value: "2024" → "2025"
{"command":"replaceText","args":{"search":"2024","replacement":"2025"}}

// Change a placeholder: "[ORG_NAME]" → "Lawvable"
{"command":"replaceText","args":{"search":"[ORG_NAME]","replacement":"Lawvable"}}

// Change a word: "shall" → "must"
{"command":"replaceText","args":{"search":"shall","replacement":"must","occurrence":1}}

// Add formatting to existing text (text is replaced with formatted version)
{"command":"replaceText","args":{"search":"Important Notice","replacement":"<strong>Important Notice</strong>"}}
```

### `insertContent` - Insert New Content (INSERTION ONLY)

**Use when:** Adding new text/elements while keeping the anchor text intact. The anchor text STAYS, new content is added before/after.
**Track changes effect:** Shows as <u>new text</u> only (underline, no strikethrough).

**CRITICAL:** When you need to ADD words to a sentence without changing existing words, you MUST use `insertContent`, NOT `replaceText`. Using `replaceText` will show the entire sentence as deleted and rewritten, which clutters the track changes view.

```json
// CORRECT: Add a word after existing text - shows only the addition as tracked
// Original: "The party agrees to pay"  →  Result: "The party agrees to pay promptly"
{"command":"insertContent","args":{"content":" promptly","position":{"after":"agrees to pay"}}}

// WRONG: Using replaceText to add a word - shows entire phrase as deleted + rewritten
// This would show: "~~agrees to pay~~" + "agrees to pay promptly" (ugly track changes!)
// {"command":"replaceText","args":{"search":"agrees to pay","replacement":"agrees to pay promptly"}}

// Add a new section after a heading
{"command":"insertContent","args":{"content":"<h2>New Section</h2><p>Content here.</p>","position":{"after":"Introduction"}}}

// Add a disclaimer before signatures
{"command":"insertContent","args":{"content":"<p>By signing below, parties confirm agreement.</p>","position":{"before":"Signatures"}}}

// Add a clause after a section
{"command":"insertContent","args":{"content":"<p>Additional clause text.</p>","position":{"after":"Section 2."},"author":{"name":"Jane Smith"}}}
```

### When to Use Which (Track Changes Guide)

**Key principle:** Use `replaceText` only when you're CHANGING existing text. Use `insertContent` when you're ADDING new text.

| Task | Command | Track Changes Display |
|------|---------|----------------------|
| Change a value | `replaceText` | ~~2024~~ <u>2025</u> |
| Fill a placeholder | `replaceText` | ~~[NAME]~~ <u>John</u> |
| Fix a typo | `replaceText` | ~~teh~~ <u>the</u> |
| Change a word | `replaceText` | ~~shall~~ <u>must</u> |
| **Add a word to sentence** | `insertContent` | existing text<u> added word</u> |
| Add a new paragraph | `insertContent` | <u>entire new paragraph</u> |
| Add a new section | `insertContent` | <u>entire new section</u> |
| Add disclaimer | `insertContent` | <u>disclaimer text</u> |
| Add review comment | `addComment` | (comment balloon, no track change) |


### `insertTable` - Create a Table

```json
// Insert 3x4 table after specific text
{"command":"insertTable","args":{"rows":3,"cols":4,"position":{"after":"Introduction"}}}

// Insert 2x2 table (default) before specific text
{"command":"insertTable","args":{"position":{"before":"Signatures"}}}

// Pre-populated table with headers and data (dimensions inferred)
{"command":"insertTable","args":{"data":[["Name","Role"],["Alice","Engineer"]],"position":{"after":"Team:"}}}

// Cells support HTML formatting
{"command":"insertTable","args":{"data":[["<strong>Header</strong>"],["Value"]]}}

// With custom author for track changes
{"command":"insertTable","args":{"rows":2,"cols":3,"author":{"name":"John"}}}
```

**Parameters:**
- `rows`, `cols` - Dimensions (default: 2, or inferred from `data`)
- `data` - 2D array of cell contents (row-major). Supports plain text or HTML. Empty strings for blank cells.
- `position` - `{"after": "text"}` or `{"before": "text"}` for anchor-based positioning
- `author` - Optional author for track changes attribution

### `addComment` - Add Comment to Text

```json
// Add a comment on specific text
{"command":"addComment","args":{"search":"confidential information","comment":"This clause needs legal review"}}

// Comment on nth occurrence
{"command":"addComment","args":{"search":"Party","comment":"Verify party name","occurrence":2}}
```

**Parameters:**
- `search` (required) - Text to find and attach comment to
- `comment` (required) - The comment text
- `occurrence` - Which match (1-indexed), defaults to first
- `author` - Optional `{name, email}` for attribution

### `undo` / `redo` - History Navigation

```json
// Undo the last action
{"command":"undo","args":{}}

// Redo the last undone action
{"command":"redo","args":{}}
```

**Returns:** `{"success": true}` if action was undone/redone, `{"success": false}` if nothing to undo/redo.

### `formatText` - Apply Formatting

Apply text styling, paragraph properties, and heading conversion. **Not tracked** (applied directly for performance).

```json
// Multiple text formats on entire document
{"command":"formatText","args":{"fontFamily":"Arial","fontSize":"12pt","color":"#333333","scope":"document"}}

// Bold + highlight on specific range (use getNodes to find positions)
{"command":"formatText","args":{"bold":true,"highlight":"#FFEB3B","scope":{"from":100,"to":200}}}

// Remove formatting (false removes, omit leaves unchanged)
{"command":"formatText","args":{"bold":false,"highlight":false,"scope":{"from":100,"to":200}}}

// Add hyperlink to text range
{"command":"formatText","args":{"link":"https://example.com","scope":{"from":100,"to":120}}}

// Remove hyperlink
{"command":"formatText","args":{"link":false,"scope":{"from":100,"to":120}}}

// Set line height on entire document
{"command":"formatText","args":{"lineHeight":"1.5","scope":"document"}}

// Set spacing + indent
{"command":"formatText","args":{"spacingBefore":"12pt","spacingAfter":"6pt","indent":36,"scope":"document"}}
```

**Text-level parameters:**
- `fontFamily` - Font name (e.g., "Arial", "Times New Roman")
- `fontSize` - Size with unit (e.g., "12pt", "14px")
- `color` - Text color as CSS (e.g., "#ff0000", "red")
- `highlight` - Background color, or `false` to remove
- `bold`, `italic`, `underline`, `strikethrough` - `true` to apply, `false` to remove, omit to leave unchanged
- `link` - URL string to create hyperlink, or `false` to remove

**Block-level parameters:**
- `lineHeight` - Line spacing (e.g., "1.0", "1.5", "2.0")
- `indent` - Left indentation in points (e.g., 36 for 0.5", 72 for 1"). Use 0 to remove.
- `spacingBefore` - Space before paragraph (e.g., "12pt", "6pt")
- `spacingAfter` - Space after paragraph (e.g., "12pt", "6pt")

**Scope:** `"document"` for entire doc, or `{"from": N, "to": M}` for range. Use `getNodes` to find positions.

### `insertTableOfContents` - Create TOC with Bookmarks

Insert a proper table of contents with internal navigation links. You identify the heading entries (position + level), the command handles bookmarks and TOC node creation.

**Workflow:**
1. Use `getNodes` with type `paragraph` to get all paragraph positions
2. Identify which paragraphs are section titles (by text content, bold styling, numbering, etc.). Numbered paragraphs include a `marker` field (e.g., `"marker": "1."`) — the TOC automatically prepends it to the entry text.
3. Pass their positions and heading levels to `insertTableOfContents`

```json
// TOC matching document font (always pass style with fontFamily + fontSize)
{"command":"insertTableOfContents","args":{"entries":[{"level":1,"from":227,"to":241},{"level":2,"from":586,"to":601}],"position":{"after":"Non-Disclosure Agreement"},"style":{"fontFamily":"Arial","fontSize":"10pt"}}}

// Custom title
{"command":"insertTableOfContents","args":{"entries":[{"level":2,"from":229,"to":243}],"style":{"fontFamily":"Arial","fontSize":"10pt"},"title":"Contents"}}

// No title
{"command":"insertTableOfContents","args":{"entries":[{"level":2,"from":229,"to":243}],"style":{"fontFamily":"Arial","fontSize":"10pt"},"title":""}}
```

**Parameters:**
- `entries` (required) - Array of `{level: 1-6, from: N, to: M}`. Positions from `getNodes` output. The command reads the text automatically.
- `position` - `{"after": "text"}` or `{"before": "text"}` (default: beginning of document)
- `title` - TOC title (default: "Table of Contents", `""` for none)
- `style` (required) - `{fontFamily, fontSize}` to match the document's font conventions. **ALWAYS detect the document's font family and size** from `getText` with `html` format and pass them here. Bold and black (#000000) are applied by default. The title is automatically 2pt larger than entries. Optional: `color` to override the default black.
- `author` - Optional author for track changes attribution

The command inserts invisible bookmarks at each heading and creates TOC entries with internal links pointing to them. All entries are automatically left-indented based on their `level` (0.5" per level). The existing text and styling are not modified.

### `deleteTableOfContents` - Remove TOC

Delete the table of contents from the document.

```json
// Remove TOC only
{"command":"deleteTableOfContents","args":{}}

// Remove TOC and its bookmarks
{"command":"deleteTableOfContents","args":{"removeBookmarks":true}}
```

## HTML Formatting

| Format | HTML |
|--------|------|
| Headings | `<h1>`, `<h2>`, `<h3>` |
| Paragraph | `<p>Text</p>` |
| Bold/Italic/Underline | `<strong>`, `<em>`, `<u>` |
| Color | `<span style="color: red">text</span>` |
| Lists | `<ul><li>...</li></ul>`, `<ol><li>...</li></ol>` |
| Link | `<a href="url">text</a>` |

**Adding a link to existing text:**

Use `formatText` with `link` parameter and position scope:
```json
// Step 1: Get paragraph positions
{"command":"getNodes","args":{"type":"paragraph"}}

// Step 2: Apply link to the target range
{"command":"formatText","args":{"link":"https://example.com","scope":{"from":218,"to":230}}}
```

**Important:** Replacement strings are only parsed as HTML if they **start with `<tag>` and end with `</tag>`**. Including text before/after (e.g., `(<a>text</a>)`) treats the entire string as literal text.

**Creating lists with `insertContent`:**
```json
// Bullet list
{"command":"insertContent","args":{"content":"<ul><li>First</li><li>Second</li></ul>","position":{"after":"Key points:"}}}

// Numbered list with nested items and formatting
{"command":"insertContent","args":{"content":"<ol><li><strong>Step one</strong><ul><li>Sub-item</li></ul></li><li>Step two</li></ol>","position":{"after":"Instructions:"}}}
```

## How Search Works

Search extracts **plain text only**, ignoring all formatting:
- ✅ Matches across bold/normal, track changes, paragraphs
- ✅ Whitespace flexible (extra spaces/tabs/line breaks OK)
- Returns **first** occurrence. Use `occurrence` parameter for nth match, or include more context to make pattern unique.

## Best Practices

**Use unique phrases (5+ words):**
- ❌ `"the"` or `"Agreement"` (too common)
- ✅ `"agrees to pay the sum of"` or `"Section 3.2 Confidentiality"`

**Don't worry about formatting in search** - matches across bold, track changes, etc.

**Use `occurrence` for ambiguous matches** (1-indexed):
```json
{"command":"replaceText","args":{"search":"the","replacement":"that","occurrence":3}}
```

**For insertions, find unique anchor text nearby.**

## Workflow

**CRITICAL:** ALWAYS chain echo + sleep + cat in a single bash command to send and read response together.

### Step 1: Clarify Author (once per session)
Before making any edits, ALWAYS use `AskUserQuestion` to ask whether changes should be attributed to the user (ask their name) or the agent. If the user wants their name, pass `"author":{"name":"Their Name"}` in **every** `replaceText`, `insertContent`, `insertTable`, and `addComment` command.

### Step 2: Read First
Get document content to understand structure and find anchor text:
```bash
mkdir -p path/to/.superdoc && echo '{"command":"getText","args":{"format":"text"}}' > path/to/.superdoc/doc.json && sleep 2 && cat path/to/.superdoc/doc.json
```

Use `sleep 2` for the first command (extension needs time to detect the file). Use `sleep 0.5` for subsequent commands, except `insertTableOfContents` which needs `sleep 3` (it inserts bookmarks + TOC node). If the response still shows the command JSON instead of a result, re-send the full `echo + sleep + cat` — do NOT run `sleep && cat` separately.

### Step 3: Make Edit
Execute command and immediately read the response in one bash call (see "When to Use Which" table to pick the right command):
```bash
echo '{"command":"replaceText","args":{"search":"2024","replacement":"2025"}}' > path/to/.superdoc/doc.json && sleep 0.5 && cat path/to/.superdoc/doc.json
```

### Step 4: Verify with getText (content changes only)
For `replaceText`, `insertContent`, `insertTable` - verify the change is visible:
```bash
echo '{"command":"getText","args":{"format":"text"}}' > path/to/.superdoc/doc.json && sleep 0.5 && cat path/to/.superdoc/doc.json
```

**Skip verification for `formatText`** - formatting (font, color, highlight, spacing) is not visible in text output. The command response `{"success": true}` is sufficient.

### Multi-Edit Pattern
Repeat Steps 1-3 for each edit: `getText` → edit command → `getText` to verify. Each as a separate bash call.

## Troubleshooting

- **Command not executing**: Ensure document is open in SuperDoc and `.superdoc/` folder exists in same directory.
- **"Text not found" error**: Use `getText` first to see actual content, then include more surrounding context in search string.
- **Changes not visible**: Verify the SuperDoc extension is active.
