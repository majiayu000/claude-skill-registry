---
name: notion-cms
description: Guide for extracting content from Notion (Pages & Databases) using the Notion MCP server and converting it to high-fidelity Markdown/HTML for website CMS integration.
---

# Notion CMS Integration

## Overview

This skill enables the extraction of structured content from Notion for use in external websites (CMS). It leverages the **Notion MCP Server** to fetch raw block data and uses specialized Python scripts to convert that data into clean, front-matter-enriched Markdown.

**Use this skill when:**

- The user wants to "sync" or "copy" Notion pages to a website.
- The user asks to "get all data" from a Notion Database.
- You need to convert Notion Blocks (headers, lists, images, code) into Markdown.

## Capability Protocols

### 1. Database Discovery & Extraction

To extract all pages from a database:

1.  **Identify Database**: Use `mcp_notion_server_API_search_by_title` (or similar search tool) to find the database ID if not provided.
2.  **Query Database**: Use `mcp_notion_server_API_query_data_source` to get the list of pages.
3.  **Iterate**: For each page, extract its content (see Protocol 2).

### 2. Page Content Extraction (Deep Fetch)

Notion pages are composed of "Blocks". To get the full content, you must retrieve the blocks.

1.  **Retrieve Metadata**: Use `mcp_notion_server_API_retrieve_a_page` to get the page title, cover image, and properties (for frontmatter).
2.  **Retrieve Content**: Use `mcp_notion_server_API_retrieve_block_children` with the Page ID.
    - _Note_: If a block has `has_children: true`, you must recursively call `retrieve_block_children` on that block ID to get nested content (like lists or toggles).
3.  **Parse & Save**:
    - Do NOT attempt to manually format the JSON output into Markdown in your response.
    - INSTEAD, save the raw JSON response to a temporary file (e.g., `temp_notion_data.json`).
    - Run the bundled script `scripts/json_to_markdown.py` to convert the JSON to a `.md` file.

### 3. Markdown Conversion Rule

Always use the `scripts/json_to_markdown.py` script for conversion. It handles:

- Standard blocks (H1-H3, Paragraph, Lists).
- Rich text (Bold, Italic, Links).
- Code blocks (with language).
- Images (extracting URLs).
- Callouts and Quotes.

## Workflow Example

**User:** "Copy the 'Blog' database to my site."

**Agent Plan:**

1.  Search for "Blog" database -> ID: `db-123`.
2.  Query `db-123` -> Returns 5 pages.
3.  For each page:
    a. `retrieve_a_page(page_id)` -> Get title "Hello World".
    b. `retrieve_block_children(page_id)` -> Get blocks JSON.
    c. `write_to_file("temp.json", blocks_json)`.
    d. `run_command("python3 .agent/skills/notion-cms/scripts/json_to_markdown.py temp.json --output content/hello-world.md --frontmatter '{\"title\": \"Hello World\"}'")`.
    e. Confirm file creation.

## Resources

### scripts/

- `json_to_markdown.py`: Robust converter for Notion Block JSON to Markdown.

### assets/

- `frontmatter_template.yaml`: Template for Jekyll/Hugo/Next.js frontmatter.
