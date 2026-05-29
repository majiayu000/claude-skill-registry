---
id: notion-knowledge-base
name: Notion Knowledge Base
description: Search and surface docs, create/update pages for FAQs
role: support
requiredTools:
  - type: mcpService
    serviceType: notion
---

## Notion Knowledge Base

When using Notion for knowledge or FAQs:

- Search for pages and databases to find relevant docs before answering.
- Read page content to cite specific sections when answering user questions.
- When creating or updating pages, use the correct parent (page, database, or workspace) and property schema.
- For FAQs, prefer updating existing pages when the answer already exists; create new pages when the topic is new.
- Keep page titles and properties consistent with the existing workspace structure.

## Step-by-step instructions

1. For “find/answer X”: use Notion search (pages/databases) with the topic; open the most relevant page(s) and read content.
2. Answer from the page content; cite page title and section.
3. For “add/update FAQ”: search for an existing page on the topic; if found, update that page; if not, create a new page under the right parent with correct properties.
4. When creating/updating, use the parent (page, database, or workspace) and property types the workspace expects.

## Examples of inputs and outputs

- **Input**: “What’s our policy on refunds?”  
  **Output**: Short answer drawn from the relevant Notion page, with “According to [Page title]…” and section reference.

- **Input**: “Add a FAQ: How do I reset my password?”  
  **Output**: Confirm the answer text and target page/database; then create or update the page and confirm “Added/updated [page title].”

## Common edge cases

- **No page found**: Say “I didn’t find a page about [topic]” and offer to create one if the user wants.
- **Multiple matching pages**: Pick the most relevant (e.g. by title or type) or summarize from the best one and mention others.
- **Missing parent or schema**: Ask which parent page or database to use, or list options from search.
- **API/oauth error**: Report that Notion returned an error and suggest reconnecting or retrying.

## Tool usage for specific purposes

- **Search (pages/databases)**: Use to find existing docs and FAQs before answering or before creating/updating.
- **Read page**: Use to get content for answering questions and to check existing FAQ content before updating.
- **Create/update page**: Use to add or update FAQ content; always specify parent and required properties.
