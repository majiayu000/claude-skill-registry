---
name: look-at
version: 1.0
description: "This skill should be used when the user asks to 'look at', 'analyze', 'describe', 'extract from', or 'what's in' media files like PDFs, images, diagrams, screenshots, or charts. Triggers include: 'what does this image show', 'extract the table from this PDF', 'describe this diagram', 'what's in this screenshot', 'analyze this chart', 'read this image', 'get text from this PDF', 'summarize this document', or requests for specific data extraction from visual or document files. Use when analyzed/interpreted content is needed rather than literal file reading (which uses Read tool)."
---

# Look At - Multimodal File Analysis

Fast, cost-effective file analysis using Google's Gemini 2.5 Flash Lite model for PDFs, images, diagrams, and other media files.

## Tool Selection Enforcement

### Rationalization Table - STOP When Thinking:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "I can read images directly with Read" | You'll waste thousands of context tokens showing the full image | Use look_at for analysis |
| "I'll use Read for this PDF" | You'll lose table structure and visual information by extracting raw text | Use look_at for PDFs with tables/charts/diagrams |
| "Just a quick glance at the file" | Your quick glances still consume full context tokens | Use look_at for targeted extraction |
| "I need exact text, so Read is required" | Gemini's extraction is accurate for most use cases | Use look_at first, Read only if extraction insufficient |
| "look_at adds complexity" | You gain context savings and faster processing | Use look_at for media files |
| "The file is small" | Your small files still waste context if uninterpreted | Size doesn't determine tool choice, content type does |
| "I'll process it myself" | You waste reasoning tokens on trivial extraction | Delegate to look_at |

### Red Flags - STOP Immediately When Thinking:

- If you catch yourself thinking "Let me Read this image/PDF/screenshot" → STOP. Use look_at for media files.
- If you catch yourself thinking "I can see the image directly" → STOP. Seeing it directly still wastes context. Use look_at.
- If you catch yourself thinking "Just need to glance at this diagram" → STOP. Glancing still costs context tokens. Use look_at.
- If you catch yourself thinking "The PDF is text-based, so Read is fine" → STOP. If it has structure/tables/charts, use look_at.

### Cost & Context Benefits

| Scenario | Read Tool | look_at Tool |
|----------|-----------|--------------|
| **PDF with table** | Extracts raw text (~1000 tokens), loses table structure | Extracts table as structured data (~100 tokens) |
| **Screenshot** | Loads entire image (~500 tokens), requires interpretation | Describes content (~50 tokens) |
| **Diagram** | Shows image (~800 tokens), requires analysis | Explains architecture (~100 tokens) |
| **Multi-page PDF** | All pages loaded (~5000 tokens) | Extracts specific sections (~200 tokens) |

**look_at saves 80-95% of context tokens by extracting only relevant information.**

## When to Use

**Use look_at when you need:**
- Media files the Read tool cannot interpret
- Extracting specific information or summaries from documents
- Describing visual content in images or diagrams
- Analyzing charts, tables, or structured data in PDFs
- When analyzed/extracted data is needed, not raw file contents

**Never use look_at when:**
- Source code or plain text files needing exact contents (use Read)
- Files that need editing afterward (need literal content from Read)
- Simple file reading where no interpretation is needed
- Exact formatting or structure must be preserved

## How It Works

1. Provide a file path and a specific goal (what to extract)
2. The helper script uploads the file to Gemini's API
3. Gemini 2.5 Flash Lite analyzes the file and extracts requested information
4. Only the relevant extracted information is returned (saves context tokens)

## Usage Pattern

**CRITICAL - Display Requirement:**
Always set the Bash tool `description` parameter to show a clean invocation:
```
description: "look-at: [goal text]"
```

Never display the full Python command to the user.

```bash
# Basic usage
python3 ${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py \
    --file "/path/to/file.pdf" \
    --goal "Extract the title and date from this document"

# With custom model
python3 ${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py \
    --file "/path/to/diagram.png" \
    --goal "Describe the architecture shown in this diagram" \
    --model "gemini-2.5-flash"
```

**IMPORTANT:**
- Always use absolute paths for files
- Always set Bash tool `description` to `"look-at: [goal]"` for clean UX

## Response Rules

When using look_at, the response includes:
- Only the extracted information matching the goal
- Clear statement if requested information is not found
- Concise output focused on the goal (no preamble)

Use this extracted information directly in continued work without loading the full file into context.

## Supported File Types

| Type | Extensions | MIME Types |
|------|-----------|------------|
| Images | .jpg, .jpeg, .png, .webp, .heic, .heif | image/* |
| Videos | .mp4, .mpeg, .mov, .avi, .webm | video/* |
| Audio | .wav, .mp3, .aiff, .aac, .ogg, .flac | audio/* |
| Documents | .pdf, .txt, .csv, .md, .html | application/pdf, text/* |

## Model Options

| Model | Use Case | Speed | Cost |
|-------|----------|-------|------|
| `gemini-2.5-flash-lite` | Default - fast, cheap analysis | Fastest | Lowest |
| `gemini-3-flash` | More complex extraction needs | Fast | Low |
| `gemini-3-flash-preview` | Agentic vision with code execution | Fast | Low |
| `gemini-3-pro-preview` | Highest accuracy required | Medium | Medium |

**Default is gemini-2.5-flash-lite** for optimal speed/cost ratio.

## Agentic Vision Mode

For complex visual reasoning tasks, use the `--agentic` flag to enable code execution. This allows Gemini to:
- **Zoom into specific regions** of an image for detailed analysis
- **Count objects** precisely using programmatic analysis
- **Perform calculations** on visual data (measurements, statistics)
- **Process structured data** in images (charts, tables) with higher accuracy

**When to use `--agentic`:**
- Counting objects in an image ("How many items are in this photo?")
- Reading fine details ("What does the small text in the corner say?")
- Analyzing charts with specific data points ("What's the exact value for Q3?")
- Complex spatial reasoning ("Which element is closest to the center?")

**Usage:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py \
    --file "photo.jpg" \
    --goal "Count the number of people in this image" \
    --agentic
```

**Note:** Agentic mode automatically uses `gemini-3-flash-preview` regardless of the `--model` setting.

## Common Patterns

**REMEMBER:** Always use `description: "look-at: [goal]"` in the Bash tool call.

### Extract Specific Information
```bash
# Bash tool call with:
# description: "look-at: Extract the executive summary section"
python3 ${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py \
    --file "report.pdf" \
    --goal "Extract the executive summary section"
```

### Describe Visual Content
```bash
# Bash tool call with:
# description: "look-at: List all UI elements and their layout"
python3 ${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py \
    --file "screenshot.png" \
    --goal "List all UI elements and their layout"
```

### Analyze Diagrams
```bash
# Bash tool call with:
# description: "look-at: Explain the data flow and component relationships"
python3 ${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py \
    --file "architecture.png" \
    --goal "Explain the data flow and component relationships"
```

### Extract Structured Data
```bash
# Bash tool call with:
# description: "look-at: Extract the table data as JSON"
python3 ${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py \
    --file "table.pdf" \
    --goal "Extract the table data as JSON with columns: name, value, date"
```

### Count Objects (Agentic)
```bash
# Bash tool call with:
# description: "look-at: Count the number of people in the photo"
python3 ${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py \
    --file "crowd.jpg" \
    --goal "Count the number of people visible in this image" \
    --agentic
```

### Analyze Chart Details (Agentic)
```bash
# Bash tool call with:
# description: "look-at: Extract specific data points from the chart"
python3 ${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py \
    --file "quarterly_chart.png" \
    --goal "Extract the exact values for each quarter and calculate the year-over-year change" \
    --agentic
```

## Environment Setup

**Required environment variable:**
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

**Required Python package:**
```bash
pip install google-genai
```

For pixi-managed projects, add to `pixi.toml`:
```toml
[dependencies]
google-genai = ">=1.0.0"
```

## Cost Optimization

- **Gemini 2.5 Flash Lite** is the most cost-effective option
- Only extracts requested information (saves on output tokens)
- Avoids loading full files into main conversation context
- Use specific goals to minimize unnecessary processing

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API key not set | Set `GOOGLE_API_KEY` environment variable |
| File not found | Use absolute paths, verify file exists |
| Large file timeout | Break into smaller files or use lower-quality images |
| Rate limit errors | Add retry logic or use batch processing |
| Empty response | Check that goal is clear and specific |

## Examples

See `examples/` directory for:
- `analyze_pdf.sh` - PDF document extraction
- `describe_image.sh` - Image analysis
- `extract_table.sh` - Structured data extraction

## Related Skills

- `/gemini-batch` - For batch processing of many files
- Standard `Read` tool - For text files needing exact contents
