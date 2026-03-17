---
name: miro
description: Manage Miro boards, sticky notes, and shapes via Miro API. Create collaborative whiteboards programmatically.
metadata: {"clawdbot":{"emoji":"🎨","requires":{"env":["MIRO_ACCESS_TOKEN"]}}}
---

# Miro

Collaborative whiteboard platform.

## Environment

```bash
export MIRO_ACCESS_TOKEN="xxxxxxxxxx"
```

## List Boards

```bash
curl "https://api.miro.com/v2/boards" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN"
```

## Create Board

```bash
curl -X POST "https://api.miro.com/v2/boards" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Project Planning", "description": "Sprint planning board"}'
```

## Get Board

```bash
curl "https://api.miro.com/v2/boards/{board_id}" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN"
```

## Create Sticky Note

```bash
curl -X POST "https://api.miro.com/v2/boards/{board_id}/sticky_notes" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"content": "New idea!", "shape": "square"},
    "position": {"x": 0, "y": 0},
    "style": {"fillColor": "yellow"}
  }'
```

## Create Shape

```bash
curl -X POST "https://api.miro.com/v2/boards/{board_id}/shapes" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"shape": "rectangle", "content": "Task 1"},
    "position": {"x": 100, "y": 100},
    "geometry": {"width": 200, "height": 100}
  }'
```

## Get All Items on Board

```bash
curl "https://api.miro.com/v2/boards/{board_id}/items" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN"
```

## Links
- Dashboard: https://miro.com/app/dashboard/
- Docs: https://developers.miro.com/reference/api-reference
