---
name: baoyu-markdown-to-html
description: Converts Markdown to styled HTML with WeChat-compatible themes. Supports code highlighting, math, PlantUML, footnotes, alerts, and infographics. Use when user asks for "markdown to html", "convert md to html", "md转html", or needs styled HTML output from markdown.
---

# Markdown to HTML Converter

Converts Markdown files to beautifully styled HTML with inline CSS, optimized for WeChat Official Account and other platforms.

## Script Directory

**Agent Execution**: Determine this SKILL.md directory as `SKILL_DIR`, then use `${SKILL_DIR}/scripts/<name>.ts`.

| Script | Purpose |
|--------|---------|
| `scripts/main.ts` | Main entry point |

## Preferences (EXTEND.md)

Use Bash to check EXTEND.md existence (priority order):

```bash
# Check project-level first
test -f .baoyu-skills/baoyu-markdown-to-html/EXTEND.md && echo "project"

# Then user-level (cross-platform: $HOME works on macOS/Linux/WSL)
test -f "$HOME/.baoyu-skills/baoyu-markdown-to-html/EXTEND.md" && echo "user"
```

┌──────────────────────────────────────────────────────────────┬───────────────────┐
│                             Path                             │     Location      │
├──────────────────────────────────────────────────────────────┼───────────────────┤
│ .baoyu-skills/baoyu-markdown-to-html/EXTEND.md               │ Project directory │
├──────────────────────────────────────────────────────────────┼───────────────────┤
│ $HOME/.baoyu-skills/baoyu-markdown-to-html/EXTEND.md         │ User home         │
└──────────────────────────────────────────────────────────────┴───────────────────┘

┌───────────┬───────────────────────────────────────────────────────────────────────────┐
│  Result   │                                  Action                                   │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Found     │ Read, parse, apply settings                                               │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Not found │ Use defaults                                                              │
└───────────┴───────────────────────────────────────────────────────────────────────────┘

**EXTEND.md Supports**: Default theme | Custom CSS variables | Code block style

## Workflow

### Step 0: Pre-check (Chinese Content)

**Condition**: Only execute if input file contains Chinese text.

**Detection**:
1. Read input markdown file
2. Check if content contains CJK characters (Chinese/Japanese/Korean)
3. If no CJK content → skip to Step 1

**Format Suggestion**:

If CJK content detected AND `baoyu-format-markdown` skill is available:

Use `AskUserQuestion` to ask whether to format first. Formatting can fix:
- Bold markers with punctuation inside causing `**` parse failures
- CJK/English spacing issues

**If user agrees**: Invoke `baoyu-format-markdown` skill to format the file, then use formatted file as input.

**If user declines**: Continue with original file.

### Step 1: Confirm Theme

Before converting, use AskUserQuestion to confirm the theme (unless user already specified):

| Theme | Description |
|-------|-------------|
| `default` (Recommended) | 经典主题 - 传统排版，标题居中带底边，二级标题白字彩底 |
| `grace` | 优雅主题 - 文字阴影，圆角卡片，精致引用块 |
| `simple` | 简洁主题 - 现代极简风，不对称圆角，清爽留白 |

### Step 2: Convert

```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts <markdown_file> --theme <theme>
```

### Step 3: Report Result

Display the output path from JSON result. If backup was created, mention it.

## Usage

```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts <markdown_file> [options]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--theme <name>` | Theme name (default, grace, simple) | default |
| `--title <title>` | Override title from frontmatter | |
| `--keep-title` | Keep the first heading in content | false (removed) |
| `--help` | Show help | |

**Examples:**

```bash
# Basic conversion (uses default theme, removes first heading)
npx -y bun ${SKILL_DIR}/scripts/main.ts article.md

# With specific theme
npx -y bun ${SKILL_DIR}/scripts/main.ts article.md --theme grace

# Keep the first heading in content
npx -y bun ${SKILL_DIR}/scripts/main.ts article.md --keep-title

# Override title
npx -y bun ${SKILL_DIR}/scripts/main.ts article.md --title "My Article"
```

## Output

**File location**: Same directory as input markdown file.
- Input: `/path/to/article.md`
- Output: `/path/to/article.html`

**Conflict handling**: If HTML file already exists, it will be backed up first:
- Backup: `/path/to/article.html.bak-YYYYMMDDHHMMSS`

**JSON output to stdout:**

```json
{
  "title": "Article Title",
  "author": "Author Name",
  "summary": "Article summary...",
  "htmlPath": "/path/to/article.html",
  "backupPath": "/path/to/article.html.bak-20260128180000",
  "contentImages": [
    {
      "placeholder": "MDTOHTMLIMGPH_1",
      "localPath": "/path/to/img.png",
      "originalPath": "imgs/image.png"
    }
  ]
}
```

## Themes

| Theme | Description |
|-------|-------------|
| `default` | 经典主题 - 传统排版，标题居中带底边，二级标题白字彩底 |
| `grace` | 优雅主题 - 文字阴影，圆角卡片，精致引用块 (by @brzhang) |
| `simple` | 简洁主题 - 现代极简风，不对称圆角，清爽留白 (by @okooo5km) |

## Supported Markdown Features

| Feature | Syntax |
|---------|--------|
| Headings | `# H1` to `###### H6` |
| Bold/Italic | `**bold**`, `*italic*` |
| Code blocks | ` ```lang ` with syntax highlighting |
| Inline code | `` `code` `` |
| Tables | GitHub-flavored markdown tables |
| Images | `![alt](src)` |
| Links | `[text](url)` with footnote references |
| Blockquotes | `> quote` |
| Lists | `-` unordered, `1.` ordered |
| Alerts | `> [!NOTE]`, `> [!WARNING]`, etc. |
| Footnotes | `[^1]` references |
| Ruby text | `{base|annotation}` |
| Mermaid | ` ```mermaid ` diagrams |
| PlantUML | ` ```plantuml ` diagrams |

## Frontmatter

Supports YAML frontmatter for metadata:

```yaml
---
title: Article Title
author: Author Name
description: Article summary
---
```

If no title is found, extracts from first H1/H2 heading or uses filename.

## Extension Support

Custom configurations via EXTEND.md. See **Preferences** section for paths and supported options.
