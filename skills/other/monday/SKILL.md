---
name: monday
description: "Manage Monday.com boards, items, and groups via the GraphQL API."
metadata: {"thinkfleetbot":{"emoji":"🟣","requires":{"bins":["curl","jq"],"env":["MONDAY_API_TOKEN"]}}}
---

# Monday.com

Manage Monday.com boards and items via the GraphQL API.

## Environment Variables

- `MONDAY_API_TOKEN` - API token (generate at https://monday.com/developers/apps)

## List boards

```bash
curl -s -X POST -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.monday.com/v2" \
  -d '{"query":"{ boards(limit: 20) { id name state } }"}' | jq '.data.boards[] | {id, name, state}'
```

## List items

```bash
curl -s -X POST -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.monday.com/v2" \
  -d '{"query":"{ boards(ids: [BOARD_ID]) { items_page(limit: 20) { items { id name state group { title } } } } }"}' | jq '.data.boards[0].items_page.items[] | {id, name, state, group: .group.title}'
```

## Create item

```bash
curl -s -X POST -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.monday.com/v2" \
  -d '{"query":"mutation { create_item(board_id: BOARD_ID, group_id: \"GROUP_ID\", item_name: \"New item\") { id name } }"}' | jq '.data.create_item'
```

## Update item

```bash
curl -s -X POST -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.monday.com/v2" \
  -d '{"query":"mutation { change_simple_column_value(board_id: BOARD_ID, item_id: ITEM_ID, column_id: \"status\", value: \"Done\") { id } }"}' | jq '.data.change_simple_column_value'
```

## List groups

```bash
curl -s -X POST -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.monday.com/v2" \
  -d '{"query":"{ boards(ids: [BOARD_ID]) { groups { id title color } } }"}' | jq '.data.boards[0].groups[] | {id, title, color}'
```

## Get board

```bash
curl -s -X POST -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.monday.com/v2" \
  -d '{"query":"{ boards(ids: [BOARD_ID]) { id name description state columns { id title type } } }"}' | jq '.data.boards[0]'
```

## Add update

```bash
curl -s -X POST -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.monday.com/v2" \
  -d '{"query":"mutation { create_update(item_id: ITEM_ID, body: \"Update text here\") { id body } }"}' | jq '.data.create_update'
```

## List columns

```bash
curl -s -X POST -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.monday.com/v2" \
  -d '{"query":"{ boards(ids: [BOARD_ID]) { columns { id title type settings_str } } }"}' | jq '.data.boards[0].columns[] | {id, title, type}'
```
