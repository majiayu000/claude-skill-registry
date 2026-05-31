---
name: media-processor
description: "Specialized visual and multimedia processing tools. Use this skill whenever a task involves complex visual content — UI mockups, dense screenshots, design images, charts, artwork — where precise details like spacing, hex colors, font sizes, and component hierarchy need to be extracted accurately. Also use for: reviewing or auditing existing UI against designs, comparing screenshots for visual regressions, transcribing audio/video, extracting data from PDFs with complex layouts, and generating images. Trigger whenever the user wants to implement from a design, review or compare UI screenshots, analyze visual details precisely, describe artwork or aesthetic content, or process any media file (audio, video, PDF)."
---

# Media Processor

Specialized tools for extracting precise visual details (exact colors, spacing, hierarchy), processing audio/video, and generating images.

## Tools

All scripts live in `scripts/` relative to this skill's directory. They auto-select the best model per task and handle retries, large file uploads, and error reporting.

| Script | Purpose |
|--------|---------|
| `gemini_batch_process.py` | Analyze images, transcribe audio/video, extract data from PDFs |
| `image_gen.py` | Generate and edit images (paid plan required) |
| `document_converter.py` | Convert PDF, DOCX, XLSX, PPTX to Markdown; extract page ranges and images |

Requires `GEMINI_API_KEY` in environment or `.env` in this skill's directory. Run any script with `--help` for setup details and available parameters.

**Quick start — image analysis:**
```bash
python <skill-dir>/scripts/gemini_batch_process.py \
  --files <image-path> \
  --task analyze \
  --prompt "<tailored prompt>" \
  --output <output-path>.md
```

## Prompt Quality Matters

The prompt sent to the processing model is the single biggest factor in output quality. Tailor prompts to what the task actually needs — generic prompts produce generic results.

**What makes a good analysis prompt:**
- Ask for the specific details the task requires (hex colors, spacing in px, component hierarchy) rather than "describe this image"
- Structure the ask as a numbered list — the model mirrors the structure back, making output easy to parse
- Name the desired output format ("as a markdown table", "as JSON", "as a component tree")
- Include implementation context when relevant ("for React with Tailwind") so the model emphasizes useful details

**Example prompt patterns:**

UI implementation: *"Extract component hierarchy, layout type, exact hex colors, typography (sizes/weights), spacing in px, interactive states, icons and decorative elements"*

Chart data: *"Extract chart type, axes with units, every data point with exact values, legend entries with colors. Output as a markdown table"*

Design review: *"Compare this screenshot against the design. Flag differences in spacing, colors, alignment, missing elements, and visual inconsistencies. Note exact values for each discrepancy"*

## Pasted Images

When a user pastes images in chat, they are auto-saved to:
```
$CLAUDE_DIR/image-cache/<current_session_id>/<image_number>.png
```
Use `ls "$CLAUDE_DIR/image-cache/"` to discover the session ID, then list its contents to find available images.

## Model Overrides

Scripts auto-select models per task (see [model-routing.md](./references/model-routing.md)). Override with `--model <model-id>` when the default isn't enough — for example, `--model gemini-3.1-pro-preview` for complex visual analysis where the pro model catches more detail than flash.

## References

| Reference | When to read |
|-----------|-------------|
| [api-gotchas.md](./references/api-gotchas.md) | Before using image generation, video processing, or raw API calls — prevents common failures |
| [model-routing.md](./references/model-routing.md) | When choosing or overriding the default model for a task |
| [media-optimization.md](./references/media-optimization.md) | When files are too large to upload — ffmpeg compression recipes |

## Gotchas

- **Rate limits** — scripts retry up to 3 times with backoff. If still rate-limited after retries, stop and ask the user to check their API key quota or provide a new key.
- **Model IDs change** — Google frequently rotates preview model IDs. If you get a 404, the model was likely superseded — check the [models page](https://ai.google.dev/gemini-api/docs/models) for current IDs.
- **Safety filters** — the API may refuse some content. Report clearly to the user rather than retrying.
- **Large files auto-upload** — files >20MB automatically use the File API (2GB max, 48h retention). No action needed.
