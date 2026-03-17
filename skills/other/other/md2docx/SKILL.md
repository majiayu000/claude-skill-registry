---
name: md2docx
description: Convert Markdown to Word (DOCX) documents. Use when user wants to export, convert, or create Word documents from Markdown content.
api_key: ""
---

# md2docx - Markdown to Word Converter

Convert Markdown text to professionally formatted Word (DOCX) documents.

## Quick Start

**Choose the right mode based on your environment**:

```bash
# URL mode: Returns download URL (for cloud/remote environments)
python scripts/convert.py input.md --url

# File mode: Saves file directly (for local environments)
python scripts/convert.py input.md --file
```

## Choosing the Right Mode

| Scenario | Mode | Command |
|----------|------|---------|
| Skill runs in cloud, user needs to download | `--url` | `python scripts/convert.py input.md --url` |
| Skill runs locally, user wants file saved | `--file` | `python scripts/convert.py input.md --file` |
| Remote execution (MCP, API, cloud agent) | `--url` | Returns URL for user to download |
| Local execution (user's machine) | `--file` | Saves .docx directly to disk |

**Decision Rule**:
- **Use `--url`** when the skill runs in a different environment than the user (cloud, remote server, MCP server)
- **Use `--file`** when the skill runs on the same machine where the user wants the output file

## How It Works

1. **Prepare Markdown**: Ensure content is in standard Markdown format
2. **Run Script**: Execute `scripts/convert.py` with appropriate mode
3. **Get Result**: 
   - URL mode: Receive download URL
   - File mode: File saved to specified location

## API Details

**Endpoints**:
- URL mode: `https://api.deepshare.app/convert-text-to-url` → Returns `{"url": "..."}`
- File mode: `https://api.deepshare.app/convert-text` → Returns DOCX file directly

**Authentication**: Include header `X-API-Key: {api_key}`

### API Key Configuration

You can configure the API key in three ways:

1. **Environment Variable** (Highest Priority)
   ```bash
   export DEEP_SHARE_API_KEY="your_api_key_here"
   ```

2. **Skill Variable** (Medium Priority)
   Edit the `api_key` field in the YAML frontmatter of this Skill file:
   ```yaml
   ---
   name: md2docx
   api_key: "your_api_key_here"
   ---
   ```

3. **Trial Key** (Fallback): `f4e8fe6f-e39e-486f-b7e7-e037d2ec216f`

**Priority Order**:
1. Environment variable `DEEP_SHARE_API_KEY` (if set)
2. Skill's `api_key` variable (if not empty)
3. Trial key (limited quota)

⚠️ **Trial Mode**: Limited quota. For stable production use, purchase at: https://ds.rick216.cn/purchase

## Request Format

```json
{
  "content": "markdown text here",
  "filename": "output",
  "template_name": "templates",
  "language": "zh",
  "hard_line_breaks": false,
  "remove_hr": false
}
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `content` | required | Markdown text to convert |
| `filename` | `"output"` | Output filename (without .docx) |
| `template_name` | `"templates"` | Template: `templates`, `论文`, `article`, `thesis`, etc. |
| `language` | `"zh"` | Template language: `zh` or `en` |
| `hard_line_breaks` | `false` | Preserve single line breaks |
| `remove_hr` | `false` | Remove horizontal rules |

## Common Templates

**Chinese** (`language: "zh"`):
- `templates` - General purpose
- `论文` - Academic paper
- `论文-首行不缩进` - Paper without indent
- `论文-标题加粗` - Paper with bold headings

**English** (`language: "en"`):
- `templates` - General purpose
- `article` - Article/report style
- `thesis` - Academic thesis

## Conversion Script Usage

### Command Line Options

```bash
python scripts/convert.py <input.md> [options]

Options:
  --url              Return download URL (default if no mode specified)
  --file             Save file directly to disk
  --template, -t     Template name (default: templates)
  --language, -l     Language: zh or en (default: zh)
  --output, -o       Output directory for file mode
  --api-key, -k      API key (optional)
```

### Examples

```bash
# URL mode (cloud/remote environments)
python scripts/convert.py document.md --url
python scripts/convert.py paper.md --url --template 论文 --language zh

# File mode (local environments)
python scripts/convert.py document.md --file
python scripts/convert.py paper.md --file --output ./docs --template thesis --language en

# With custom API key
python scripts/convert.py doc.md --url --api-key your_key
```

## Validation Before Conversion

Ensure Markdown content:
- Headers use `#` syntax
- Lists use `-` or `1.` syntax
- Code blocks use triple backticks
- Math formulas use `$...$` (inline) or `$$...$$` (block)
- Images use publicly accessible URLs

## Response Handling

### URL Mode Response

**Success** (200 OK):
```json
{
  "url": "https://flies.deepshare.app/mcp/hash/document_xxx.docx"
}
```

### File Mode Response

**Success**: File saved to disk, path printed to stdout

### Error Responses (Both Modes)

- `401 Unauthorized` - Invalid API key
- `403 Forbidden` - Quota exceeded → Purchase at https://ds.rick216.cn/purchase
- `413 Payload Too Large` - Content exceeds 10MB
- `500 Internal Server Error` - Service unavailable, retry

## User Communication

### On Success

Tell user:
1. Conversion completed successfully
2. **URL mode**: Provide the download URL
3. **File mode**: Provide the file path where document was saved
4. Check which API key was used:
   - **If using environment variable or Skill variable**: No reminder needed
   - **If using trial key**: Remind: "⚠️ You're using trial mode (limited quota). For stable production use, get your API key at: https://ds.rick216.cn/purchase"

### On Quota Exceeded

Tell user:
1. Conversion failed: quota exceeded
2. Purchase more credits at: https://ds.rick216.cn/purchase
3. Or use another API key

### On Other Errors

Tell user:
1. What went wrong (based on error message)
2. How to fix it
3. Offer to retry

## Tips

- **API Key Configuration**:
  - **Option 1 (Recommended)**: Set environment variable `DEEP_SHARE_API_KEY`
    ```bash
    export DEEP_SHARE_API_KEY="your_api_key_here"
    ```
  - **Option 2**: Edit `api_key` in this Skill's YAML frontmatter
  - **Option 3**: Use trial key (limited quota)
- **File Size**: Keep Markdown under 10MB
- **Images**: Use `https://` URLs, not local paths
- **Math**: Use LaTeX syntax: `$E=mc^2$` or `$$\int_0^\infty$$`
- **Line Breaks**: Use `hard_line_breaks: true` for addresses, poetry
- **Templates**: Choose based on document type (paper, article, etc.)

## Example Workflows

### Workflow 1: Cloud Environment (URL Mode)

**User asks**: "Convert this to Word" (skill running in cloud)

1. Save the Markdown content to a temporary file (e.g., `temp.md`)

2. Run the conversion script with URL mode:
   ```bash
   python scripts/convert.py temp.md --url
   ```

3. The script will:
   - Select API key by priority (env → skill → trial)
   - Call the conversion API
   - Return download URL

4. Provide the download URL to user

5. Clean up temporary file

### Workflow 2: Local Environment (File Mode)

**User asks**: "Convert my notes.md to Word" (skill running locally)

1. Run the conversion script with file mode:
   ```bash
   python scripts/convert.py notes.md --file --output ./output
   ```

2. The script will:
   - Select API key by priority (env → skill → trial)
   - Call the conversion API
   - Save the DOCX file directly

3. Tell user where the file was saved

4. No cleanup needed - file is the output
