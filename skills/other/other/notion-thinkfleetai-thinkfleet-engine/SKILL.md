---
name: notion
description: "Manage Notion pages, databases, and blocks via the REST API."
metadata: {"thinkfleetbot":{"emoji":"📓","requires":{"bins":["curl","jq"],"env":["NOTION_API_KEY"]}}}
---

# Notion

Manage Notion pages and databases via the REST API.

## Environment Variables

- `NOTION_API_KEY` - Integration token (generate at https://www.notion.so/my-integrations)

## Search

```bash
curl -s -X POST -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" \
  "https://api.notion.com/v1/search" \
  -d '{"query":"search term","page_size":10}' | jq '.results[] | {id, type: .object, title: (if .object=="page" then .properties.title.title[0].plain_text // .properties.Name.title[0].plain_text // null else .title[0].plain_text // null end)}'
```

## Get page

```bash
curl -s -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  "https://api.notion.com/v1/pages/PAGE_ID" | jq '{id, url, created_time, properties}'
```

## Create page

```bash
curl -s -X POST -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" \
  "https://api.notion.com/v1/pages" \
  -d '{"parent":{"database_id":"DATABASE_ID"},"properties":{"Name":{"title":[{"text":{"content":"New page title"}}]}}}' | jq '{id, url}'
```

## Update page

```bash
curl -s -X PATCH -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" \
  "https://api.notion.com/v1/pages/PAGE_ID" \
  -d '{"properties":{"Status":{"select":{"name":"Done"}}}}' | jq '{id, url}'
```

## Query database

```bash
curl -s -X POST -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" \
  "https://api.notion.com/v1/databases/DATABASE_ID/query" \
  -d '{"filter":{"property":"Status","select":{"equals":"In Progress"}},"page_size":20}' | jq '.results[] | {id, properties}'
```

## List databases

```bash
curl -s -X POST -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" \
  "https://api.notion.com/v1/search" \
  -d '{"filter":{"value":"database","property":"object"},"page_size":20}' | jq '.results[] | {id, title: .title[0].plain_text}'
```

## Create database entry

```bash
curl -s -X POST -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" \
  "https://api.notion.com/v1/pages" \
  -d '{"parent":{"database_id":"DATABASE_ID"},"properties":{"Name":{"title":[{"text":{"content":"New entry"}}]},"Status":{"select":{"name":"To Do"}}}}' | jq '{id, url}'
```

## Get block children

```bash
curl -s -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  "https://api.notion.com/v1/blocks/BLOCK_ID/children?page_size=50" | jq '.results[] | {id, type, text: (if .type=="paragraph" then .paragraph.rich_text[0].plain_text // null else null end)}'
```
