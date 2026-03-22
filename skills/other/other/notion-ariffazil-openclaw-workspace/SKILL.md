---
name: notion
description: Notion workspace — read/write pages, databases, search, create tasks via Notion API
user-invocable: true
---

# Notion Skill — arifOS_bot

Triggers: "notion", "note", "add to notion", "search notion", "create page",
          "update notion", "notion database", "my notes", "add task to notion",
          "notion doc", "write to notion"

API: `https://api.notion.com/v1` | Auth: `NOTION_API_KEY` (Integration Token)

---

## ⚙️ One-Time Setup (do once, then forget)

**Status: NOTION_API_KEY not yet configured.**

1. Go to: https://www.notion.so/my-integrations
2. Click **"New integration"** → name it `arifOS_bot`
3. Select your workspace → Submit → Copy the **Internal Integration Token** (`secret_...`)
4. Add the token to VPS:
   ```bash
   # On VPS host:
   echo 'NOTION_API_KEY=secret_YOUR_TOKEN_HERE' >> /srv/arifOS/.env
   docker compose up -d --force-recreate openclaw
   ```
5. **Share pages with the integration**: Open any Notion page → **Share** → invite `arifOS_bot`

After setup, test:
```bash
curl -s https://api.notion.com/v1/users/me \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" | python3 -m json.tool
```

---

## Search

```bash
# Search across your Notion workspace
curl -s -X POST https://api.notion.com/v1/search \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query":"YOUR SEARCH TERM","page_size":10}' \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
for r in d.get('results',[]):
    title = ''
    if r['object'] == 'page':
        props = r.get('properties',{})
        for k,v in props.items():
            if v.get('type') == 'title':
                title = ''.join([t['plain_text'] for t in v['title']])
                break
    elif r['object'] == 'database':
        title = ''.join([t['plain_text'] for t in r.get('title',[])])
    print(f\"{r['object']}: {title} — {r['id']}\")
"
```

---

## Read a Page

```bash
PAGE_ID="YOUR-PAGE-ID-HERE"  # from URL: notion.so/PAGE_ID

# Get page metadata
curl -s https://api.notion.com/v1/pages/${PAGE_ID} \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" | python3 -m json.tool

# Get page content (blocks)
curl -s https://api.notion.com/v1/blocks/${PAGE_ID}/children \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
for block in d.get('results', []):
    bt = block['type']
    content = block.get(bt, {})
    text = ''.join([t.get('plain_text','') for t in content.get('rich_text',[])])
    if text: print(f'[{bt}] {text}')
"
```

---

## Create a Page

```bash
PARENT_PAGE_ID="YOUR-PARENT-PAGE-ID"

curl -s -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{
    \"parent\": {\"page_id\": \"${PARENT_PAGE_ID}\"},
    \"properties\": {
      \"title\": {\"title\": [{\"text\": {\"content\": \"YOUR TITLE HERE\"}}]}
    },
    \"children\": [
      {
        \"object\": \"block\",
        \"type\": \"paragraph\",
        \"paragraph\": {
          \"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"Page content here.\"}}]
        }
      }
    ]
  }" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Created:', d.get('id'), d.get('url'))"
```

---

## Append to Existing Page

```bash
PAGE_ID="YOUR-PAGE-ID"
CONTENT="New content to append"

curl -s -X PATCH "https://api.notion.com/v1/blocks/${PAGE_ID}/children" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{
    \"children\": [
      {
        \"object\": \"block\",
        \"type\": \"paragraph\",
        \"paragraph\": {
          \"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"${CONTENT}\"}}]
        }
      }
    ]
  }" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Appended:', len(d.get('results',[])),'blocks')"
```

---

## Database — Query & Add Rows

```bash
DB_ID="YOUR-DATABASE-ID"

# Query database rows
curl -s -X POST "https://api.notion.com/v1/databases/${DB_ID}/query" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"page_size": 20}' \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'Total rows: {len(d[\"results\"])}')
for row in d['results'][:5]:
    props = row['properties']
    for k, v in props.items():
        if v.get('type') == 'title':
            title = ''.join([t['plain_text'] for t in v['title']])
            print(f'  - {title}')
"

# Add a row to database (adjust property names to match your DB schema)
curl -s -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{
    \"parent\": {\"database_id\": \"${DB_ID}\"},
    \"properties\": {
      \"Name\": {\"title\": [{\"text\": {\"content\": \"New Task\"}}]},
      \"Status\": {\"select\": {\"name\": \"Todo\"}}
    }
  }" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Row created:', d.get('id'))"
```

---

## Quick Shortcuts

```bash
# List all databases you have access to
curl -s -X POST https://api.notion.com/v1/search \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"filter":{"value":"database","property":"object"}}' \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
for db in d['results']:
    title = ''.join([t['plain_text'] for t in db.get('title',[])])
    print(f'{title}: {db[\"id\"]}')
"
```

---

## arifOS_bot → Notion Pipeline

When Arif says "log this to Notion" or "save this decision to Notion":
1. Search for the target page/database by name
2. Append content with timestamp and source tag
3. Log to `~/.openclaw/workspace/logs/audit.jsonl`

*arifOS_bot — Notion API v2022-06-28*
