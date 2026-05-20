---
name: htmlpix-api
description: "Use when the user wants to call, test, or integrate the HTMLPix HTML-to-image API — including auth setup, signed URL minting, image rendering, template CRUD, and AI template generation."
---

# HTMLPix API Skill

Use the API contracts below when generating code, curl commands, SDK wrappers, or troubleshooting responses.

## Base URL and Auth

- API Base URL: [https://api.htmlpix.com](https://api.htmlpix.com)
- Private endpoints require: `Authorization: Bearer <API_KEY>`
- API key can be found at [https://htmlpix.com/api-keys](https://htmlpix.com/api-keys)
- Do not call private endpoints from browser client code; mint URLs on the backend.

Auth/plan/quota failures map to:

- `401` `MISSING_KEY` or `INVALID_KEY`
- `403` `KEY_INACTIVE`
- `402` `SUBSCRIPTION_INACTIVE`
- `429` `QUOTA_EXCEEDED`
- `503` `NOT_READY`

## Endpoint Contracts

### POST `/v1/url` (private)
Mint one signed image URL.

Request JSON:

- `templateId` (required, string, max 128)
- `width` (optional int, 1..4096)
- `height` (optional int, 1..4096)
- `format` (optional: `png | jpeg | webp`)
- `quality` (optional int, 0..100)
- `tv` (optional string, max 128)
- `variables` (optional object, max 64 keys, each value must be JSON-serializable)

Response JSON:

- `{ "url": string, "expiresAt": number }`

Operational limits (default server values):

- Body size max: `32KB`
- Rate: `120` mint requests per `60s` per API key
- Concurrency: `4` in-flight per user, `64` global

### POST `/v1/urls` (private)
Mint multiple signed image URLs.

Request JSON:

- `{ "items": ImageUrlMintRequest[] }`
- `items.length` must be `1..25`
- Each item has the same shape as `POST /v1/url`

Response JSON:

- `{ "urls": [{ "templateId": string, "url": string, "expiresAt": number }] }`

Operational limits:

- Body size max: `256KB`

### GET `/v1/image` (public, signed)
Render/fetch image bytes using a signed query string.

Required query params:

- `templateId`
- `uid`
- `exp` (unix ms)
- `sig`

Optional query params:

- `width` (default `1200`)
- `height` (default `630`)
- `format` (default `webp`)
- `quality`
- `tv`
- Variables encoded as `v_<name>=<value>`

Behavior:

- Rejects expired URL: `403 URL_EXPIRED`
- Rejects bad signature: `403 INVALID_SIGNATURE`
- Returns image bytes with immutable caching headers and ETag
- Supports `304 Not Modified` with `If-None-Match`

Important: treat minted URL as opaque. If any query value changes, signature validation will fail.

### GET `/v1/templates` (private)
List templates.

Query:

- `scope` optional: `all | mine | starter` (default: `all`)

Response:

- `{ "scope": "...", "templates": [...] }`

### POST `/v1/templates` (private)
Create custom template.

Request JSON:

- `name` required string (max 120)
- `description` optional string (max 2000)
- `jsx` required string (max 120000, validated for safe JSX subset)
- `variables` required array (max 100)
- `googleFonts` optional array (max 10 strings)
- `width`/`height` optional ints 1..4096
- `format` optional `png | jpeg | webp`

Response:

- `201 { "templateId": string, "template": object }`

### GET `/v1/templates/:templateId` (private)
Fetch one template visible to caller.

Response:

- `{ "template": object }`

### PATCH `/v1/templates/:templateId` (private)
Update template fields.

Request JSON:

- At least one field is required (`EMPTY_UPDATE` if none)
- Updatable fields: `name`, `description`, `jsx`, `variables`, `googleFonts`, `width`, `height`, `format`

Response:

- `{ "template": object }`

### POST `/v1/templates/generate` (private)
AI-assisted template generation.

Supports either:

- Single: `{ "prompt": string, "width"?: number, "height"?: number }`
- Batch: `{ "items": [{ "prompt": string, "width"?: number, "height"?: number }] }`

Rules:

- `prompt` max 2000 chars
- `width`/`height` default to `1200x630`
- Batch max `5` items
- Upstream timeout default: `60s`

Response:

- Single request: returns one generated result object
- Batch request: `{ "results": [...] }`

## Safe Integration Pattern

1. Keep API key server-side only.
2. Mint with `POST /v1/url` or `/v1/urls`.
3. Store/embed returned `url` directly (meta tags, email HTML, social cards, etc.).
4. Do not re-sign or mutate query params client-side.
5. Handle `402`, `429`, and `503` with retries/fallback messaging.

## Minimal Examples

```bash
curl -X POST https://api.htmlpix.com/v1/url \
  -H "Authorization: Bearer $HTMLPIX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "templateId": "tmpl_123",
    "variables": { "title": "Launch Day" },
    "width": 1200,
    "height": 630,
    "format": "png"
  }'
```

```bash
curl -X GET "https://api.htmlpix.com/v1/templates?scope=mine" \
  -H "Authorization: Bearer $HTMLPIX_API_KEY"
```

If the user asks for an endpoint not listed above, say it is not present in the current server route table and avoid inventing routes.
