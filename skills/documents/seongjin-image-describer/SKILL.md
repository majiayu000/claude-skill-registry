---
name: Seongjin_Image-Describer
description: Convert Wiki-style image links to Markdown format with AI-generated descriptions. Use when preprocessing markdown files for PPT generation, converting ![[image.png]] to ![description](path) format, or enabling text-based image understanding.
allowed-tools: Read, Bash, Glob
version: 1.0.0
updated: 2026-01-04
status: active
---

# Image-Describer: Wiki to Markdown Image Link Converter

Convert Wiki-style image links (![[image.png]]) to Markdown format (![AI-generated description](path)) with intelligent AI-powered image analysis.

---

## Quick Reference (30 seconds)

**Purpose**: Convert Wiki-style image links to Markdown format with AI-generated alt text descriptions.

**Execution Command**:
```bash
cd "{working_directory}/.claude/skills/Seongjin_Image-Describer/Scripts" && \
source .venv/bin/activate && \
python Convert_Image-Link_Wiki-to-Markdown.py "{markdown_path}" -m gpt
```

**Script Location**:
`.claude/skills/Seongjin_Image-Describer/Scripts/Convert_Image-Link_Wiki-to-Markdown.py`

**Prerequisites**:
- Python venv with: `openai`, `google-generativeai`, `pillow`, `python-dotenv`
- API Key: `.claude/skills/Seongjin_Image-Describer/Scripts/.env` with `OPENAI_API_KEY` or `GOOGLE_API_KEY`

**Output**: In-place modification of the markdown file.

---

## Implementation Guide (5 minutes)

### Basic Usage

**Step 1**: Ensure virtual environment is set up
```bash
cd "{working_directory}/.claude/skills/Seongjin_Image-Describer/Scripts"
python -m venv .venv
source .venv/bin/activate
pip install python-dotenv openai google-generativeai Pillow
```

**Step 2**: Create `.env` file in Scripts directory
```bash
# Create at: .claude/skills/Seongjin_Image-Describer/Scripts/.env
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_MODEL=gpt-5-mini

# Or for Gemini
GOOGLE_API_KEY=AIza-your-google-key-here
GOOGLE_MODEL=gemini-3-flash-preview
```

**Step 3**: Execute the script
```bash
# Using GPT (default)
python Convert_Image-Link_Wiki-to-Markdown.py "/path/to/document.md" -m gpt

# Using Gemini
python Convert_Image-Link_Wiki-to-Markdown.py "/path/to/document.md" -m gemini

# Path conversion only (no AI analysis)
python Convert_Image-Link_Wiki-to-Markdown.py "/path/to/document.md" --no-describe

# Dry-run mode (preview changes without modifying file)
python Convert_Image-Link_Wiki-to-Markdown.py "/path/to/document.md" -n
```

### Input/Output Format

**Input (Wiki-style)**:
```markdown
![[image.png]]
![[folder/diagram.jpg]]
![[screenshot.webp]]
```

**Output (Markdown-style)**:
```markdown
![Detailed AI-generated description of the image content](absolute/path/to/image.png)
![System architecture diagram showing...](absolute/path/to/folder/diagram.jpg)
![Screenshot of the application interface...](absolute/path/to/screenshot.webp)
```

### CLI Options

| Option | Description |
|--------|-------------|
| `-n, --dry-run` | Preview changes without modifying the file |
| `-m, --model` | AI model selection: `gpt` (default) or `gemini` |
| `--no-describe` | Skip AI description generation (path conversion only) |

### Script Configuration

Configurable constants in the script:

```python
CONTEXT_CHARS = 500   # Characters before/after image for context
MAX_RETRIES = 3       # API call retry attempts
CONCURRENT = 20       # Maximum parallel image analyses
```

### Image Search Behavior

The script searches for images in the following order:
1. Current directory of the markdown file
2. Parent directory
3. Grandparent directory
4. Common asset folders (Attachments, images, assets)
5. Full vault search as fallback

### Output Example

```
Building image index...
Found 10751 image files

============================================================
  Images requiring description: 5
  Model: GPT
  Concurrent processing: 20
============================================================

[1/5] Analyzing: chart.png
        Completed: This chart shows sales growth from 2020 to 2024...
[2/5] Analyzing: diagram.jpg
        Completed: System architecture diagram illustrating...

============================================================
  Processing Results Summary
   Success: 5
   Failed: 0
   Skipped: 0
   Total: 5
============================================================

Completed: document.md
```

---

## Advanced Implementation (10+ minutes)

### Two-Phase Processing

The script operates in two distinct phases:

**Phase 1 - Link Conversion**:
- Converts Wiki links (![[file]]) to Markdown format (![](path))
- Resolves image paths using vault-wide search
- Saves changes immediately after conversion

**Phase 2 - AI Description Generation**:
- Identifies Markdown images with empty alt text
- Extracts contextual text (500 chars before/after)
- Generates AI descriptions using GPT or Gemini
- Saves each description immediately after generation

### Error Handling

**Image Not Found**:
- Detection: File not found in vault index
- Behavior: Keeps original Wiki link unchanged
- Output: Warning message displayed

**API Failure**:
- Detection: Network or API errors
- Recovery: Up to 3 retry attempts with 1-second delay
- Behavior: Continues with remaining images

**Invalid Markdown**:
- Detection: Malformed image links
- Behavior: Graceful handling, partial conversion

### Concurrent Processing

The script uses asyncio for efficient parallel processing:
- Semaphore limits concurrent API calls to 20
- Lock ensures safe file writes from multiple tasks
- Results are saved immediately as each image completes

### Supported Image Formats

png, jpg, jpeg, gif, webp, svg, bmp, tiff, ico

---

## PPT Workflow Integration

This skill serves as a critical pre-processing step in the PPT generation workflow.

### Integration Flow

**Step 1**: Image-Describer processes markdown file
- Converts Wiki links to Markdown format
- Generates AI descriptions for all images

**Step 2**: PPT-Planner reads pre-processed markdown
- Understands image content through text descriptions
- Creates slide outlines based on visual content

**Step 3**: Nano-Banana generates slide images
- Uses PPT-Planner output to create final slides

### Benefits

**Context Overflow Prevention**:
- Visual content converted to text descriptions
- Significantly reduces token usage in PPT-Planner

**Enhanced Understanding**:
- PPT-Planner can make intelligent decisions about image placement
- AI descriptions provide semantic understanding of visual content

---

## Related Resources

**Related Agent**:
- `Seongjin_Agent_PPT-Planner`: Consumes pre-processed markdown for slide planning

**Related Skills**:
- `Seongjin_Nano-Banana`: Generates final PPT slide images
- `Seongjin_Book-Prep`: Can pre-process book chunks before conversion

**Related Command**:
- `/ppt`: Orchestrates complete workflow including image pre-processing

---

## Works Well With

- `/ppt` command - Pre-processes markdown before slide generation workflow
- `Seongjin_Agent_PPT-Planner` - Consumes pre-processed markdown with image descriptions
- `Seongjin_Book-Prep` - Can pre-process book chunks before PPT generation
- `Seongjin_Nano-Banana` - Final step in PPT generation pipeline

---

## Troubleshooting

**API Key Not Found**:
- Ensure `.env` file exists at `.claude/skills/Seongjin_Image-Describer/Scripts/.env`
- Verify `OPENAI_API_KEY` or `GOOGLE_API_KEY` is set correctly

**Image Not Found**:
- Check if image file exists in the vault
- Verify file extension matches supported formats
- Use dry-run mode to preview path resolution

**Empty Descriptions**:
- Check API connectivity
- Verify API key has sufficient quota
- Review API error messages in console output

**Partial Processing**:
- Script saves progress after each image
- Re-run script to process remaining images
- Already-processed images (with alt text) are skipped

**Virtual Environment Issues**:
```bash
# Recreate virtual environment
cd "{working_directory}/.claude/skills/Seongjin_Image-Describer/Scripts"
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install python-dotenv openai google-generativeai Pillow
```
