---
name: fetch-rfc
description: Fetch an RFC from Notion given a URL. Use when user wants to view, review, or work with an existing RFC document. Accepts Notion page URLs or page IDs.
argument-hint: <notion-url-or-id>
user-invocable: true
---

# Fetch RFC from Notion

Fetch and display an RFC document from Notion for review or reference.

## Input

Notion page URL or ID: $ARGUMENTS

Accepted formats:

- Full URL: `https://www.notion.so/RFC-Title-2e7258b8ba0c81b4bb63e95dd3811984`
- URL with workspace: `https://www.notion.so/workspace/RFC-Title-2e7258b8ba0c81b4bb63e95dd3811984`
- Page ID with dashes: `2e7258b8-ba0c-81b4-bb63-e95dd3811984`
- Page ID without dashes: `2e7258b8ba0c81b4bb63e95dd3811984`

## Steps

1. Parse the input from `$ARGUMENTS`:
   - If full URL, extract the page ID (32-character hex string at the end)
   - If page ID, use directly
   - Validate format before proceeding

2. Fetch the RFC using Notion MCP:

   ```
   mcp__notion__notion-fetch with:
   - id: {page_id or full URL}
   ```

   The tool accepts both URLs and IDs directly.

3. Extract from the response:
   - Page title
   - Page content (Notion-flavored Markdown)
   - Page URL (for reference)

4. Display the RFC content:
   - Show the title prominently
   - Render the full RFC content
   - Include the Notion URL for direct access

## Output Format

```markdown
# {RFC Title}

**Notion URL:** {url}

---

{Full RFC content in Markdown}
```

## Error Handling

- If page not found: "RFC not found. Please check the URL or page ID."
- If access denied: "Unable to access this RFC. The page may not be shared with the Notion integration."
- If invalid format: "Invalid Notion URL or page ID. Expected format: https://www.notion.so/... or a 32-character page ID."

## Notes

- The Notion MCP `notion-fetch` tool handles URL parsing internally
- Content is returned in Notion-flavored Markdown format
- This skill is read-only - it does not modify the RFC
- For creating new RFCs, use `/plan-rfc` instead
- For breaking down an RFC into tickets, use `/breakdown-rfc` (if available)
