---
name: feishu-docx
description: Export Feishu/Lark cloud documents to Markdown. Supports docx, sheets, bitable, and wiki. Use this skill when you need to read, analyze, or reference content from Feishu knowledge base.
---

# Feishu Docx Exporter

Export Feishu/Lark cloud documents to Markdown format for AI analysis.

## Instructions

### Setup (One-time)

1. Install the tool:
```bash
pip install feishu-docx
```

2. Configure Feishu app credentials:
```bash
feishu-docx config set --app-id YOUR_APP_ID --app-secret YOUR_APP_SECRET
# or use 
```

3. Authorize with OAuth (opens browser):
```bash
feishu-docx auth
```

### Export Documents

Export any Feishu document URL to Markdown:

```bash
feishu-docx export "<FEISHU_URL>" -o ./output
```

The exported Markdown file will be saved with the document's title as filename.

### Supported Document Types

- **docx**: Feishu cloud documents → Markdown with images
- **sheet**: Spreadsheets → Markdown tables
- **bitable**: Multidimensional tables → Markdown tables
- **wiki**: Knowledge base nodes → Auto-resolved and exported

## Examples

### Export a wiki page

```bash
feishu-docx export "https://xxx.feishu.cn/wiki/ABC123" -o ./docs
```

### Export a document with custom filename

```bash
feishu-docx export "https://xxx.feishu.cn/docx/XYZ789" -o ./docs -n meeting_notes
```

### Export spreadsheet as Markdown table

```bash
feishu-docx export "https://xxx.feishu.cn/sheets/DEF456" --table md
```

### Read content directly (recommended for AI Agent)

```bash
# Output content to stdout instead of saving to file
feishu-docx export "https://xxx.feishu.cn/wiki/ABC123" --stdout
# or use short flag
feishu-docx export "https://xxx.feishu.cn/wiki/ABC123" -c
```

### Export with Block IDs (for later updates)

```bash
# Include block IDs as HTML comments in the Markdown output
# This enables updating specific blocks later
feishu-docx export "https://xxx.feishu.cn/wiki/ABC123" --with-block-ids
# or use short flag
feishu-docx export "https://xxx.feishu.cn/wiki/ABC123" -b

# Output format example:
# <!-- block:blk123abc -->
# # Heading
# <!-- /block -->
#
# <!-- block:blk456def -->
# This is a paragraph.
# <!-- /block -->
```

> **Tip for AI Agents**: When you need to update a specific section of a Feishu document, 
> first export with `--with-block-ids`, find the block ID from the HTML comment, 
> then use `FeishuWriter.update_block()` with that ID.

### Read content without saving to file (Python)

```python
from feishu_docx import FeishuExporter

exporter = FeishuExporter(app_id="xxx", app_secret="xxx")
content = exporter.export_content("https://xxx.feishu.cn/wiki/xxx")
print(content)
```

## Command Reference

| Command                    | Description                     |
|----------------------------|---------------------------------|
| `feishu-docx export <URL>` | Export document to Markdown     |
| `feishu-docx create <TITLE>` | Create new document            |
| `feishu-docx write <URL>`  | Append content to document      |
| `feishu-docx update <URL>` | Update specific block           |
| `feishu-docx auth`         | OAuth authorization             |
| `feishu-docx config set`   | Set credentials                 |
| `feishu-docx config show`  | Show current config             |
| `feishu-docx config clear` | Clear token cache               |

## Write Documents (CLI)

### Create Document

```bash
# Create empty document
feishu-docx create "我的笔记"

# Create with Markdown content
feishu-docx create "会议记录" -c "# 会议纪要\n\n- 议题一\n- 议题二"

# Create from Markdown file
feishu-docx create "周报" -f ./weekly_report.md

# Create in specific folder
feishu-docx create "笔记" --folder fldcnXXXXXX
```

### Append Content to Existing Document

```bash
# Append Markdown content
feishu-docx write "https://xxx.feishu.cn/docx/xxx" -c "## 新章节\n\n内容"

# Append from file
feishu-docx write "https://xxx.feishu.cn/docx/xxx" -f ./content.md
```

### Update Specific Block

```bash
# Step 1: Export with Block IDs
feishu-docx export "https://xxx.feishu.cn/docx/xxx" -b -o ./

# Step 2: Find block ID from HTML comments in output
# <!-- block:blk123abc -->
# # Heading
# <!-- /block -->

# Step 3: Update the specific block
feishu-docx update "https://xxx.feishu.cn/docx/xxx" -b blk123abc -c "新内容"
```

> **Tip for AI Agents**: When you need to update a specific section of a Feishu document:
> 1. Export with `-b` to get block IDs
> 2. Find the target block ID from HTML comments
> 3. Use `feishu-docx update` with that block ID

## Tips

- Images are automatically downloaded to a folder named after the document
- Use `--table md` for Markdown tables instead of HTML
- Token is cached and auto-refreshed, no need to re-authorize
- For Lark (overseas), add `--lark` flag
