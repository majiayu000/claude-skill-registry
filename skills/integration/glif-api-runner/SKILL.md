---
name: glif-api-runner
description: Run Glif workflows via API. Use when executing AI image/text generation workflows or integrating Glif into apps.
allowed-tools: Bash, Read, Edit
---

# Glif API Runner

Execute Glif workflows programmatically via the Simple API.

## API Basics

**Base URL:** `https://simple-api.glif.app`
**Auth:** Bearer token from https://glif.app/settings/api-tokens

## Running a Glif

```bash
curl -X POST https://simple-api.glif.app \
  -H "Authorization: Bearer $GLIF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "clgh1vxtu0011mo081dplq3xs",
    "inputs": ["your prompt here"]
  }'
```

## Input Formats

**Array (positional):**
```json
{"id": "glif_id", "inputs": ["input1", "input2"]}
```

**Object (named):**
```json
{"id": "glif_id", "inputs": {"prompt": "value", "style": "anime"}}
```

## Response Structure

```json
{
  "output": "https://res.cloudinary.com/.../image.png",
  "outputFull": {"type": "IMAGE", "value": "..."},
  "price": 5,
  "nodes": {...}
}
```

**Key fields:**
- `output` - Final result (URL for images, text for text)
- `price` - Credits consumed
- `error` - Error message if failed (still returns 200)

## Common Patterns

**Image generation:**
```bash
curl -X POST https://simple-api.glif.app \
  -H "Authorization: Bearer $GLIF_API_TOKEN" \
  -d '{"id": "IMAGE_GLIF_ID", "inputs": ["a cat wearing a hat"]}' \
  | jq -r '.output'
```

**With visibility:**
```json
{"id": "glif_id", "inputs": [...], "visibility": "PUBLIC"}
```

**Strict mode (fail on missing inputs):**
```
https://simple-api.glif.app?strict=1
```

## Error Handling

- API returns 200 even on errors - check `error` field
- Check `price` to verify credits were consumed
- Token issues return 401/403

## Finding Glif IDs

1. Go to glif.app and find a workflow
2. ID is in the URL: `glif.app/glifs/{GLIF_ID}`
3. Or use the "API" tab on any glif page
