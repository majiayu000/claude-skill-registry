---
name: bases
description: Query Obsidian Bases via the Bases Query plugin (RPC). Use when you need to read structured data from Obsidian bases.
---

# Bases Skill

Query Obsidian Bases via the Bases Query plugin.

## Endpoint

`http://127.0.0.1:27125/rpc`

## Methods

### List All Bases
```bash
curl -s -X POST http://127.0.0.1:27125/rpc \
  -d '{"method":"bases"}' | jq '.results[].name'
```

### Query a View
```bash
curl -s -X POST http://127.0.0.1:27125/rpc \
  -d '{"method":"query","params":{"base":"path/to/file.base","view":"View Name"}}'
```

### Get Schema (discover fields)
```bash
curl -s -X POST http://127.0.0.1:27125/rpc \
  -d '{"method":"schema","params":{"base":"path/to/file.base","view":"View Name"}}'
```

## Response Format

```json
{
  "count": 2,
  "results": [
    {
      "path": "Notes/Example.md",
      "name": "Example",
      "frontmatter": {
        "status": "active",
        "date": "2026-01-03"
      }
    }
  ]
}
```

## Extract Data with jq

```bash
# Names only
jq '.results[].name'

# Name + specific field
jq '.results[] | {name, status: .frontmatter.status}'
```

## Plugin Required

Install via BRAT: `https://github.com/ArtemXTech/obsidian-bases-query`
