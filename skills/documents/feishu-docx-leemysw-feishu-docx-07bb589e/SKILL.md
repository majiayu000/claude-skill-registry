---
name: feishu-docx
description: Export, write, and manage Feishu/Lark cloud documents. Supports docx, sheets, bitable, wiki, WeChat article import/export, drive management, and browser-based export for public or browser-readable docs. Use this skill when you need to read, analyze, write, or manage content in a Feishu knowledge base.
---

# Feishu Docx Exporter

Export Feishu/Lark cloud documents to Markdown for AI analysis, writing, and automation.

## Setup (One-time)

```bash
pip install feishu-docx
feishu-docx config set --app-id YOUR_APP_ID --app-secret YOUR_APP_SECRET
```

> Token auto-refreshes. No user interaction required.

### Optional: Browser-Based Export

`export-browser` requires Playwright and a Chromium runtime:

```bash
pip install playwright
playwright install chromium
```

## Export Documents

```bash
feishu-docx export "<FEISHU_URL>" -o ./output
```

The exported Markdown file will be saved with the document's title as filename.

If the document is public or only readable in your current browser session, prefer:

```bash
feishu-docx export-browser "<FEISHU_OR_LARK_URL>" -o ./output
```

Or reuse an existing Playwright session:

```bash
feishu-docx export-browser "<FEISHU_OR_LARK_URL>" --storage-state ./storage_state.json
```

### Supported Document Types

- **docx**: Feishu cloud documents → Markdown with images
- **sheet**: Spreadsheets → Markdown tables
- **bitable**: Multidimensional tables → Markdown tables
- **wiki**: Knowledge base nodes → Auto-resolved and exported
- **public/browser-readable docs**: Browser-based export with local images and attachments

## Command Reference

| Command | Description |
|---------|-------------|
| `feishu-docx export <URL>` | Export document to Markdown |
| `feishu-docx export-browser <URL>` | Export in a real browser session with local assets |
| `feishu-docx export-wechat <URL>` | Export WeChat article to Markdown |
| `feishu-docx create <TITLE>` | Create new document |
| `feishu-docx create --url <URL>` | Create document from WeChat article |
| `feishu-docx write <URL>` | Append content to document |
| `feishu-docx update <URL>` | Update specific block |
| `feishu-docx drive ls` | List app or personal cloud-space files |
| `feishu-docx drive perm-show <TOKEN>` | Show public permission |
| `feishu-docx drive perm-members <TOKEN>` | List permission members |
| `feishu-docx drive clear` | Clear files with double confirmation |
| `feishu-docx export-wiki-space <URL>` | Batch export entire wiki space |
| `feishu-docx export-workspace-schema <ID>` | Export bitable database schema |
| `feishu-docx auth` | OAuth authorization |
| `feishu-docx config set` | Set credentials |
| `feishu-docx config show` | Show current config |
| `feishu-docx config clear` | Clear token cache |
| `feishu-docx tui` | Interactive TUI interface |

## Examples

### Export a wiki page

```bash
feishu-docx export "https://xxx.feishu.cn/wiki/ABC123" -o ./docs
```

### Export a document with custom filename

```bash
feishu-docx export "https://xxx.feishu.cn/docx/XYZ789" -o ./docs -n meeting_notes
```

### Export a public or browser-readable doc in a real browser session

```bash
feishu-docx export-browser "https://xxx.larkoffice.com/wiki/ABC123" -o ./browser_docs
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
feishu-docx export "https://xxx.feishu.cn/wiki/ABC123" --with-block-ids
# or use short flag
feishu-docx export "https://xxx.feishu.cn/wiki/ABC123" -b
```

### Batch Export Entire Wiki Space

```bash
# Export all documents in a wiki space (auto-extract space_id from URL)
feishu-docx export-wiki-space "https://xxx.feishu.cn/wiki/ABC123" -o ./wiki_backup

# Specify depth limit
feishu-docx export-wiki-space "https://xxx.feishu.cn/wiki/ABC123" -o ./docs --max-depth 3

# Export with Block IDs for later updates
feishu-docx export-wiki-space "https://xxx.feishu.cn/wiki/ABC123" -o ./docs -b
```

### Export Database Schema

```bash
# Export bitable/workspace database schema as Markdown
feishu-docx export-workspace-schema <workspace_id>

# Specify output file
feishu-docx export-workspace-schema <workspace_id> -o ./schema.md
```

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

# Create from a WeChat article URL
feishu-docx create --url "https://mp.weixin.qq.com/s/xxxxx"
```

**如何获取 folder token**:
1. 在浏览器中打开目标文件夹
2. 从 URL 中提取 token：`https://xxx.feishu.cn/drive/folder/fldcnXXXXXX`
3. `fldcnXXXXXX` 就是 folder token

### Append Content to Existing Document

```bash
# Append Markdown content
feishu-docx write "https://xxx.feishu.cn/docx/xxx" -c "## 新章节\n\n内容"

# Append from file
feishu-docx write "https://xxx.feishu.cn/docx/xxx" -f ./content.md
```

## Manage Drive Files

```bash
# List app cloud-space documents
feishu-docx drive ls --auth-mode tenant --type docx

# List personal cloud-space documents
feishu-docx drive ls --auth-mode oauth --type docx

# Show public permission
feishu-docx drive perm-show "https://xxx.feishu.cn/docx/ABC123"

# List permission members
feishu-docx drive perm-members "https://xxx.feishu.cn/docx/ABC123"

# Clear files with double confirmation
feishu-docx drive clear --type docx
```

### Update Specific Block

```bash
# Step 1: Export with Block IDs
feishu-docx export "https://xxx.feishu.cn/docx/xxx" -b -o ./

# Step 2: Find block ID from HTML comments
# <!-- block:blk123abc -->
# # Heading
# <!-- /block -->

# Step 3: Update the specific block
feishu-docx update "https://xxx.feishu.cn/docx/xxx" -b blk123abc -c "新内容"
```

> **Tip for AI Agents**: When you need to update a specific section:
> 1. Export with `-b` to get block IDs
> 2. Find the target block ID from HTML comments
> 3. Use `feishu-docx update` with that block ID

## Tips

- Images and attachments auto-download to `{doc_title}/` folder when local assets are available
- Prefer `export-browser` for public share links or browser-readable docs
- Use `--stdout` or `-c` for direct content output (recommended for agents)
- Use `-b` to export with block IDs for later updates
- Token auto-refreshes, no re-auth needed
- For Lark (overseas): add `--lark` flag
- `tenant_access_token` manages app cloud space, `user_access_token` manages personal cloud space
