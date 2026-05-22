---
name: google-docs-formatter
description: Format Google Docs with proper native formatting (headings, bold, tables) instead of markdown. Google Docs does NOT render markdown - you must use the formatting API.
---

# Google Docs Formatter

Google Docs does NOT render markdown. Text like `# Header` or `**bold**` appears as literal characters. Use native Google Docs formatting via the MCP gdrive tools.

## Document Location

**IMPORTANT:** Before using this skill to format documents, ensure the document was created using the **/gdrive-manager** skill, which enforces the `claude-code/` folder structure. All research documents should be in:
- `claude-code/experiments/` - Experiment documentation
- `claude-code/logs/` - Daily logs
- `claude-code/updates/` - Weekly updates
- `claude-code/slides/` - Presentations

See `.claude/skills/gdrive-manager/references/folder-ids.md` for folder IDs.

## Key Principle

**Always get document content first** to find text indices, then apply formatting to those ranges.

## Workflow

### Step 1: Get Document Content with Indices

```
mcp__gdrive__getGoogleDocContent(documentId: "your-doc-id")
```

Returns content with index ranges like:
```
[1-55] Code vs NL Representation: Mutual Information Analysis
[57-62] TL;DR
[63-189] Code representations consistently encode MORE...
```

The indices are 1-based and required for all formatting operations.

### Step 2: Apply Paragraph Styles (Headings)

```
mcp__gdrive__formatGoogleDocParagraph(
  documentId: "...",
  startIndex: 1,
  endIndex: 55,
  namedStyleType: "TITLE"  // or HEADING_1, HEADING_2, etc.
)
```

**Available styles:**
| Style | Use Case |
|-------|----------|
| TITLE | Document title (largest) |
| HEADING_1 | Major sections |
| HEADING_2 | Subsections |
| HEADING_3 | Sub-subsections |
| HEADING_4-6 | Deeper nesting |
| NORMAL_TEXT | Regular paragraphs |

**Alignment options:** START, CENTER, END, JUSTIFIED

### Step 3: Apply Text Formatting (Bold, Italic, etc.)

```
mcp__gdrive__formatGoogleDocText(
  documentId: "...",
  startIndex: 191,
  endIndex: 204,
  bold: true
)
```

**Available options:**
- `bold`: true/false
- `italic`: true/false
- `underline`: true/false
- `strikethrough`: true/false
- `fontSize`: number (in points)
- `foregroundColor`: { red: 0-1, green: 0-1, blue: 0-1 }

## Document Structure

### Required: TL;DR Section

**Every document MUST start with a TL;DR section immediately after the title.** This provides readers with a quick summary before diving into details.

**Format:**
```
[Document Title]

TL;DR
• Key finding/point 1
• Key finding/point 2
• Key finding/point 3

[Rest of document...]
```

**Formatting for TL;DR:**
1. Apply HEADING_2 style to "TL;DR"
2. Keep it to 2-4 bullet points
3. Each bullet should be one concise sentence
4. Bold the most critical terms/numbers within the TL;DR

**Example TL;DR content:**
```
TL;DR
• Code representations encode 1.2 bits MORE mutual information than NL on average
• Effect is consistent across all 6 tested models (p < 0.01)
• Larger models show bigger code vs NL gap
```

## Content Best Practices

### Instead of Markdown, Use:

| Markdown | Google Docs Equivalent |
|----------|----------------------|
| `# Header` | Apply TITLE or HEADING_1 style |
| `## Subheader` | Apply HEADING_2 style |
| `**bold**` | Apply bold: true to text range |
| `- bullet` | Use bullet character: • |
| `1. numbered` | Use actual numbers: 1. 2. 3. |
| `\| table \|` | Use tab-separated text or create Google Sheet |

### Bullet Points

Use the bullet character directly in content:
```
• First item
• Second item
• Third item
```

### Tables

Google Docs API has limited table support. Options:
1. **Tab-separated text** - Simple but no borders
2. **Google Sheets** - Better for real tables, then link/embed

Tab-separated example:
```
Model	Code MI	NL MI	Diff
claude-haiku	2.10	0.93	1.17
gpt-4o-mini	1.23	0.35	0.87
```

## Common Formatting Patterns

### Format a Research Document

1. Get content indices
2. Apply TITLE to document title
3. **Apply HEADING_2 to "TL;DR" section** (required, immediately after title)
4. Bold key findings/numbers in the TL;DR bullets
5. Apply HEADING_1 to section headers (Introduction, Methods, Results, etc.)
6. Apply HEADING_2 to subsections
7. Bold key terms and important findings
8. Use bullet points (•) for lists

### Bold Key Labels

For configuration sections like:
```
• Model: Claude Haiku 4.5
• Backend: OpenRouter
```

Bold "Model:" and "Backend:" by finding their indices and applying `bold: true`.

## Document Search

Find documents by name:
```
mcp__gdrive__search(query: "Document Name")
```

Then get the document ID from results to use with formatting tools.

## Example: Full Formatting Flow

```python
# 1. Search for document
search_result = mcp__gdrive__search(query="My Research Doc")
doc_id = "extracted-from-search"

# 2. Get content with indices
content = mcp__gdrive__getGoogleDocContent(documentId=doc_id)
# Returns: [1-30] My Research Title\n[32-37] TL;DR\n[39-120] • Key finding...\n[122-135] Introduction...

# 3. Apply title style
mcp__gdrive__formatGoogleDocParagraph(
  documentId=doc_id,
  startIndex=1,
  endIndex=30,
  namedStyleType="TITLE"
)

# 4. Apply HEADING_2 to TL;DR (REQUIRED - always include this)
mcp__gdrive__formatGoogleDocParagraph(
  documentId=doc_id,
  startIndex=32,
  endIndex=37,
  namedStyleType="HEADING_2"
)

# 5. Bold key numbers/findings in TL;DR
mcp__gdrive__formatGoogleDocText(
  documentId=doc_id,
  startIndex=50,  # "1.2 bits" within the TL;DR
  endIndex=58,
  bold=True
)

# 6. Apply heading to main sections
mcp__gdrive__formatGoogleDocParagraph(
  documentId=doc_id,
  startIndex=122,
  endIndex=135,
  namedStyleType="HEADING_1"
)
```

## Gotchas

1. **Indices change after edits** - Always re-fetch content after updating text
2. **Indices are 1-based** - First character is index 1, not 0
3. **Newlines count** - Each `\n` is one character in the index
4. **Formatting is additive** - Multiple calls can layer formatting
5. **No markdown rendering** - Symbols like # * | appear literally

## Integration with Research Executor

The **research-executor** agent MUST use this skill for all Google Docs documentation at checkpoints.

**Research Executor Checkpoint Structure:**
- **Experiment: {name}** → HEADING_1
- **Phase: {phase}** → HEADING_2
- **Timestamp** → Italic normal text
- Sections (Hypothesis, Progress, Results, etc.) → HEADING_2
- Key findings/numbers → Bold

**Workflow:**
1. Write checkpoint content to Google Doc
2. Get document content with indices
3. Apply paragraph styles to headers
4. Bold key metrics and findings

## Related Skills and Agents

- **/gdrive-manager** - Use BEFORE this skill to create documents in correct folder
- **research-executor** agent - Primary user for experiment documentation
- **weekly-update-writer** agent - Creates weekly updates
- **research-slides-architect** agent - Creates presentations
- **/using-git-worktrees** - Creates worktrees for experiments
- **/finish-branch** - Cleans up after PR is merged
