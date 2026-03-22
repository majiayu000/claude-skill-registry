---
name: notion-to-markdown
description: Directly convert Notion pages to Obsidian-friendly Markdown using MCP fetch and local processing. Use this skill when you need to migrate specific Notion pages identified by URL or ID into the local Obsidian vault, ensuring LaTeX normalization, image localization, and property-to-frontmatter mapping.
---

# Notion to Markdown

This skill provides a high-level workflow for fetching live Notion pages and converting them into clean, localized Markdown files suitable for an Obsidian vault.

## Overview

Unlike bulk migration from exports, this skill leverages the Notion MCP (`notion-fetch`) to retrieve page content directly and then uses the `stable_jarvis.notion_to_obsidian` toolkit to perform surgical processing.

## Execution Workflow

### Step 1: Precise Identification
Use `notion-search` to find the exact page ID or URL.
```bash
# Example search
notion-search query="Leveraging Skills from Unlabeled Prior Data"
```

### Step 2: Fetch and Save Content
Retrieve the raw Notion content and save it to a temporary JSON file.
```bash
# Fetch content via MCP
notion-fetch id="[PAGE_ID]" > temp_fetch.json
```

### Step 3: Local Processing
Run the migration script to convert the JSON content to localized Markdown.
```bash
python skills/notion-to-markdown/scripts/migrate.py temp_fetch.json [OUTPUT_DIR]
```

### Step 4: Verification and Refinement
Inspect the output Markdown. Notion content can sometimes be "jammed" or have deep indentation that script-based normalization might miss. Use the `replace` tool to:
- **Normalize Indentation**: Ensure consistent 2 or 4-space indentation for nested blocks.
- **Fix Block Spacing**: Ensure double newlines exist between headings, details blocks, and paragraphs.
- **Verify Equations**: Check that all `$$` blocks are correctly populated with recovered LaTeX.
- **Final Polish**: Remove any redundant HTML tags or artifacts (e.g., empty `<span>` tags).

## Key Capabilities

- **LaTeX Normalization**: Converts Notion's `$ \dots $` and `$ \dots $` to standard `$...$` and `$$...$$` syntax.
- **Image Localization**: Automatically detects and downloads Notion S3-hosted images, saving them to a local `assets/` folder and updating Markdown links.
- **Frontmatter Mapping**: Extracts Notion properties (Status, Tags, Journal Name, etc.) and maps them to YAML frontmatter.
- **Style Conversion**: Transforms Notion-specific spans (e.g., color backgrounds) to Obsidian highlights (`==text==`).

## Dependencies

- **Conda Environment**: Must use the `jarvis` environment (`conda activate jarvis`).
- **`notion-fetch` MCP Tool**: Required to retrieve page data.
- **`stable_jarvis` package**: Must be installed in editable mode (`pip install -e .`) within the `jarvis` environment.
- **`httpx`**: Used for reliable image downloads.

## Troubleshooting

- **Expired Image URLs**: Notion S3 URLs are temporary. Ensure the `migrate.py` script is run immediately after `notion-fetch`.
- **Missing Content**: If the fetch result is truncated, ensure you are capturing the full output of the `notion-fetch` tool.
