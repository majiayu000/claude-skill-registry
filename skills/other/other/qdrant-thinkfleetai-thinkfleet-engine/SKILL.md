---
name: qdrant
description: "Manage Qdrant vector database — collections, points, and vector search via the REST API."
metadata: {"thinkfleetbot":{"emoji":"🎯","requires":{"bins":["curl","jq"],"env":["QDRANT_URL","QDRANT_API_KEY"]}}}
---

# Qdrant

Manage collections, points, and vector search.

## Environment Variables

- `QDRANT_URL` - Qdrant instance URL
- `QDRANT_API_KEY` - API key

## List collections

```bash
curl -s -H "api-key: $QDRANT_API_KEY" \
  "$QDRANT_URL/collections" | jq '.result.collections[] | {name}'
```

## Get collection info

```bash
curl -s -H "api-key: $QDRANT_API_KEY" \
  "$QDRANT_URL/collections/COLLECTION_NAME" | jq '.result | {vectors_count, points_count}'
```

## Search vectors

```bash
curl -s -X POST -H "api-key: $QDRANT_API_KEY" \
  -H "Content-Type: application/json" \
  "$QDRANT_URL/collections/COLLECTION_NAME/points/search" \
  -d '{"vector":[0.1,0.2,0.3],"limit":5,"with_payload":true}' | jq '.result[] | {id, score, payload}'
```

## Upsert points

```bash
curl -s -X PUT -H "api-key: $QDRANT_API_KEY" \
  -H "Content-Type: application/json" \
  "$QDRANT_URL/collections/COLLECTION_NAME/points" \
  -d '{"points":[{"id":1,"vector":[0.1,0.2,0.3],"payload":{"text":"example"}}]}' | jq '{status}'
```

## Notes

- Always confirm before upserting or deleting points.
