---
name: notion-page-content-updater
description: When the user needs to update or populate a Notion page with structured content extracted from documents or data sources. This skill handles the complete workflow of 1) Searching for and locating specific Notion pages by name, 2) Extracting content from source documents (Word/PDF/text files), 3) Analyzing document structure to identify relevant sections, 4) Mapping extracted content to Notion page sections, 5) Modifying page blocks (adding, deleting, updating paragraphs, lists, and headings), and 6) Organizing information in appropriate Notion formats (bullet lists, paragraphs, structured sections). Use this skill when users request to 'update a Notion page with information from a document' or need to synchronize content between documents and Notion workspaces.
---
# Skill: Notion Page Content Updater

## Purpose
Update a specified Notion page with structured content extracted from a source document (e.g., Word, PDF, text). This skill automates the end-to-end process of finding the page, reading the document, parsing its content, and updating the Notion page's blocks accordingly.

## Core Workflow
Follow these steps precisely:

1.  **Clarify Request & Identify Target:** Confirm the exact name of the Notion page to update and the path/filename of the source document.
2.  **Locate the Notion Page:**
    *   Use `notion-API-post-search` with the exact page name. If no results, search more broadly (e.g., partial name) or use an empty query `{}` to list all pages/databases.
    *   From the search results, identify the correct page by its `title` property. Note its `id`.
3.  **Extract Source Content:**
    *   Use the appropriate tool (`word-get_document_text`, `pdf-get_document_text`, `filesystem-read_file`) to read the source document's full text.
4.  **Analyze Page Structure & Plan Updates:**
    *   Retrieve the current page structure using `notion-API-get-block-children` with the page ID.
    *   Analyze the returned blocks to identify the target sections (e.g., headings for "About Me", "Paintings"). Note the block IDs that come **immediately before** where new content should be inserted.
    *   Parse the extracted document text to identify the relevant content for each target section.
5.  **Execute Page Updates (Section by Section):**
    *   **For placeholder content:** If a section contains placeholder text (e.g., `[Birth, Your education...]`), delete the old block using `notion-API-delete-a-block`.
    *   **To add new content after a heading/block:** Use `notion-API-patch-block-children`. Specify the page ID as `block_id`, use the `after` parameter with the ID of the heading block, and provide the new content in the `children` array.
    *   **Structure the content appropriately:** Use `paragraph` blocks for descriptive text and `bulleted_list_item` blocks for lists.
    *   Process one major section at a time (e.g., About Me, then Paintings, then Workshop, etc.).
6.  **Verify & Conclude:** After all updates, retrieve the page children again to confirm the changes. Provide a clear summary of what was updated.

## Critical Implementation Notes
*   **Block Update Limitation:** The `notion-API-update-a-block` endpoint has very limited functionality and often cannot be used to change a block's type or rich text content. The primary method for adding content is `patch-block-children`.
*   **Content Chunking:** Notion API calls have size limits. Break long document text into logical paragraphs when creating `children` arrays.
*   **Special Characters:** Escape quotation marks and newlines (`\n`) properly in JSON payloads for block content.
*   **Error Handling:** If a search finds multiple pages with similar names, ask the user for clarification. If a section heading doesn't exist on the target page, you may need to create it first.

## Required Tools
*   `notion-API-post-search`
*   `notion-API-get-block-children`
*   `notion-API-patch-block-children`
*   `notion-API-delete-a-block`
*   `word-get_document_text` / `pdf-get_document_text` / `filesystem-read_file`
*   `local-claim_done`

## Example Trajectory Pattern
The provided trajectory is a canonical example. Follow its pattern: search, extract, analyze structure, then sequentially update sections using `patch-block-children` after relevant headings.
