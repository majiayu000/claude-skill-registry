---
name: notion
description: Create, search, and update Notion pages/databases using the Notion API. Use for documenting work, generating runbooks, and automating knowledge base updates.
triggers:
- notion
---

# Notion

<IMPORTANT>
Before performing any Notion operations, first check if the required environment variable is set:

```bash
[ -n "$NOTION_INTEGRATION_KEY" ] && echo "NOTION_INTEGRATION_KEY is set" || echo "NOTION_INTEGRATION_KEY is NOT set"
```

If it’s missing, ask the user to provide it (or connect a Notion integration) before proceeding:
- **NOTION_INTEGRATION_KEY**: Notion integration secret (starts with `ntn_...`)

Also confirm the integration has been **shared** with the target page/database in Notion.
</IMPORTANT>

## Base headers

```bash
-H "Authorization: Bearer ${NOTION_INTEGRATION_KEY}" \
-H "Notion-Version: 2022-06-28" \
-H "Content-Type: application/json"
```

## Find a page (search)

Use Notion’s search endpoint to find a page by title.

```bash
curl -s https://api.notion.com/v1/search \
  -H "Authorization: Bearer ${NOTION_INTEGRATION_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "OpenHands Wiki",
    "page_size": 10
  }' | jq .
```

## Create a page under a parent page

```bash
PARENT_PAGE_ID="<parent_page_id>"

curl -s https://api.notion.com/v1/pages \
  -H "Authorization: Bearer ${NOTION_INTEGRATION_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"type": "page_id", "page_id": "'"${PARENT_PAGE_ID}"'"},
    "properties": {
      "title": {
        "title": [{"type": "text", "text": {"content": "My new page"}}]
      }
    },
    "children": [
      {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
          "rich_text": [{"type": "text", "text": {"content": "Hello from OpenHands."}}]
        }
      }
    ]
  }' | jq .
```

## Append blocks to an existing page

Use the page’s block id (same as page id) to append children.

```bash
PAGE_ID="<page_id>"

curl -s -X PATCH "https://api.notion.com/v1/blocks/${PAGE_ID}/children" \
  -H "Authorization: Bearer ${NOTION_INTEGRATION_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Appended section"}}]}
      }
    ]
  }' | jq .
```

## Tips / gotchas

- **Sharing is required**: even with a valid key, the integration can’t see a page/database until it has been shared with the integration in the Notion UI.
- **Rate limits**: keep requests small; for large pages, create the page first and then append blocks in batches.
- **IDs format**: Notion IDs may be returned with dashes; both dashed and non-dashed forms typically work in API calls.

## Documentation

- Notion API: https://developers.notion.com/reference/intro
- Search: https://developers.notion.com/reference/post-search
- Create a page: https://developers.notion.com/reference/post-page
- Append block children: https://developers.notion.com/reference/patch-block-children
