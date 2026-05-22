---
name: n8n-impl-integrations
description: >
  Use when integrating external APIs in n8n v1.x via HTTP Request node or
  OAuth2 credentials. Prevents pagination bugs from missing response handling
  or incorrect credential configuration. Covers HTTP Request node configuration,
  OAuth2 credential flows, pagination handling, generic credential usage for
  custom APIs, binary downloads, batch request patterns, and API error handling.
  Keywords: n8n, HTTP Request, API integration, OAuth2, pagination, credentials.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n API Integration Patterns

> HTTP Request node configuration, authentication, pagination, response handling, and batch requests for n8n v1.x.

## Quick Reference

| Task | Solution |
|------|----------|
| Call a REST API | HTTP Request node with method, URL, and authentication |
| Authenticate with API key | Predefined credential or Generic Credential (Header Auth / Query Auth) |
| Authenticate with OAuth2 | Predefined OAuth2 credential with callback URL configuration |
| Handle paginated responses | HTTP Request node pagination options (offset, cursor, or link-based) |
| Download a file | HTTP Request node with Response Format set to File |
| Send JSON body | Body Content Type = JSON, provide key-value pairs or raw JSON |
| Send form data | Body Content Type = Form-Data (multipart or URL-encoded) |
| Batch API calls | Split In Batches node before HTTP Request node |
| Handle API errors | Enable Retry On Fail and/or Continue On Fail per node |
| Access response metadata | `$response.statusCode`, `$response.headers`, `$response.body` |

## Decision Tree: Which Authentication Method

```
Need to call an external API?
├── API has a built-in n8n node? → Use the dedicated node with its predefined credential
├── API uses API key?
│   ├── Key goes in header? → Generic Credential (Header Auth)
│   ├── Key goes in query string? → Generic Credential (Query Auth)
│   └── Key goes in request body? → Use HTTP Request node with expressions
├── API uses OAuth2?
│   ├── n8n has predefined OAuth2 credential? → Use it (ALWAYS preferred)
│   └── No predefined credential? → Generic OAuth2 API credential
├── API uses Basic Auth?
│   └── Generic Credential (Basic Auth) or HTTP Request Header Auth credential
└── API uses Bearer Token?
    └── Generic Credential (Header Auth) with `Authorization: Bearer <token>`
```

## Decision Tree: Which Pagination Strategy

```
API returns paginated results?
├── Response includes next page URL?
│   └── Use "Response Contains Next URL" pagination mode
├── Response includes cursor/token for next page?
│   └── Use "Response Contains Next URL" with cursor parameter mapping
├── API uses offset + limit?
│   └── Use "Specify How Each Page Is Determined" with offset increment
└── API uses page numbers?
    └── Use "Specify How Each Page Is Determined" with page number increment
```

## HTTP Request Node Configuration

### Methods

| Method | Use Case |
|--------|----------|
| GET | Retrieve data (NEVER include a body) |
| POST | Create resources, send data |
| PUT | Full resource replacement |
| PATCH | Partial resource update |
| DELETE | Remove resources |
| HEAD | Check resource existence without body |

### URL Configuration

- ALWAYS use the full URL including protocol: `https://api.example.com/v1/resource`
- Use expressions for dynamic URLs: `https://api.example.com/v1/users/{{ $json.userId }}`
- NEVER hardcode credentials in the URL — use authentication options instead

### Body Content Types

| Type | When to Use |
|------|-------------|
| JSON | REST APIs expecting JSON payloads (most common) |
| Form URL-Encoded | APIs expecting `application/x-www-form-urlencoded` |
| Form-Data (Multipart) | File uploads, mixed data + file payloads |
| Binary | Sending raw binary data (images, PDFs) |
| Raw | Custom content types (XML, plain text, GraphQL) |
| n8n Binary File | Sending a binary file from a previous node's output |

### Headers and Query Parameters

- Add custom headers via the **Headers** section (key-value pairs)
- Add query parameters via the **Query Parameters** section
- Use expressions in values: `{{ $json.token }}` or `{{ $vars.apiVersion }}`
- ALWAYS set `Content-Type` explicitly when using Raw body type

### Response Handling

| Response Format | Output |
|-----------------|--------|
| JSON | Parsed JSON object in `$json` |
| Text | Raw text string in `$json.data` |
| File | Binary data attached to item (for downloads) |
| Autodetect | n8n determines format from Content-Type header |

**Response metadata** (available ONLY in HTTP Request node context):
- `$response.statusCode` — HTTP status code (200, 404, etc.)
- `$response.headers` — Response headers object
- `$response.body` — Response body
- `$response.statusMessage` — Status message string

## Authentication Options

### Predefined Credentials

ALWAYS use predefined credentials when available. n8n includes credentials for 400+ services.

1. Open HTTP Request node settings
2. Set **Authentication** to "Predefined Credential Type"
3. Select the service from the dropdown
4. Create or select existing credential

### Generic Credentials

Use when no predefined credential exists for your API.

| Generic Type | Injection Point |
|--------------|-----------------|
| Header Auth | Custom header (e.g., `X-API-Key: <value>`) |
| Query Auth | URL query parameter (e.g., `?api_key=<value>`) |
| Basic Auth | `Authorization: Basic <base64(user:pass)>` header |
| Digest Auth | HTTP Digest authentication |
| OAuth1 API | OAuth 1.0a flow |
| OAuth2 API | OAuth 2.0 flow (Authorization Code, Client Credentials) |
| Custom Auth | Arbitrary headers, query params, or body fields |

### OAuth2 Configuration

1. Create a new **OAuth2 API** credential in n8n
2. Configure these fields:
   - **Authorization URL** — Provider's authorization endpoint
   - **Access Token URL** — Provider's token endpoint
   - **Client ID** — From API provider's developer console
   - **Client Secret** — From API provider's developer console
   - **Scope** — Required permissions (space-separated)
   - **Auth URI Query Parameters** — Additional params if needed
3. Copy the **OAuth Callback URL** from n8n (displayed in credential form)
4. Register this callback URL in the API provider's developer console
5. Click **Connect my account** to complete the authorization flow

**Token refresh**: n8n handles token refresh automatically when `Refresh Token` is provided. NEVER store tokens manually in workflow logic.

**Callback URL format**: `https://<n8n-host>/rest/oauth2-credential/callback`

## Pagination

### Automatic Pagination Modes

Enable pagination in HTTP Request node under **Options > Pagination**.

**Mode 1: Response Contains Next URL**
- n8n extracts the next page URL from the response
- Configure the **Next URL** expression: `{{ $response.body.next }}` or `{{ $response.headers.link }}`
- ALWAYS set a **Maximum Pages** limit to prevent infinite loops

**Mode 2: Specify How Each Page Is Determined**
- Configure page parameters manually for offset, cursor, or page-number APIs
- Set **Page Size** parameter name and value
- Set **Pagination Parameter** with increment logic
- Access current page count via `$pageCount`

### Pagination Completion

ALWAYS configure a stop condition:
- **Maximum Pages** — Hard limit on pages fetched
- **Complete When** expression — Stop when response indicates no more data
  - Example: `{{ $response.body.results.length === 0 }}`
  - Example: `{{ $response.body.hasMore === false }}`

## Batch Requests

### Split In Batches Pattern

When sending many items to an API (rate-limited or bulk operations):

1. Add **Split In Batches** node before HTTP Request
2. Set **Batch Size** to match API rate limits (e.g., 10 items per batch)
3. Connect HTTP Request node to Split In Batches output
4. Connect a **Wait** node after HTTP Request if rate limiting requires delays
5. Loop back to Split In Batches node

### Item-Level Processing

The HTTP Request node processes each input item separately by default. If you have 50 items, it makes 50 HTTP calls.

- ALWAYS use Split In Batches when calling APIs with rate limits
- NEVER send all items at once to rate-limited APIs — this causes 429 errors

## Error Handling for API Calls

### Retry On Fail

Enable in node Settings tab:
- **Retry On Fail**: true
- **Max Tries**: 3 (recommended for transient errors)
- **Wait Between Tries**: 1000ms (increase for rate-limited APIs)

ALWAYS enable Retry On Fail for external API calls. Network issues and rate limits cause transient failures.

### Continue On Fail

Enable in node Settings tab to prevent workflow failure on API errors:
- Failed items receive `$json.error` with error details
- Use an IF node after to route errors vs. successes

### Error Output Branch

The HTTP Request node supports an **error output** (second output connector):
- Route failed requests to a separate processing path
- Check `$json.error`, `$json.statusCode` for error details

### Status Code Handling

Use the IF node after HTTP Request to branch on status codes:
- `{{ $response.statusCode === 200 }}` — Success path
- `{{ $response.statusCode === 429 }}` — Rate limited, needs retry/wait
- `{{ $response.statusCode >= 400 }}` — Client/server error path

## Generic Credential Request Pattern

For custom APIs without a dedicated n8n node:

1. Create a **Generic Credential** (Header Auth, Query Auth, or OAuth2)
2. Configure the credential with your API's auth details
3. In HTTP Request node, select **Authentication > Predefined Credential Type**
4. Choose the generic credential type you created
5. Build requests using URL, method, headers, query params, and body

This pattern keeps credentials encrypted and reusable across multiple HTTP Request nodes.

## Key Rules

- ALWAYS use predefined credentials over manual header injection
- ALWAYS set pagination limits to prevent infinite request loops
- ALWAYS enable Retry On Fail for external API calls
- ALWAYS use Split In Batches for bulk API operations with rate limits
- NEVER hardcode API keys, tokens, or secrets in expressions or URLs
- NEVER use the Code node for HTTP requests — ALWAYS use the HTTP Request node
- NEVER send request bodies with GET or HEAD methods
- NEVER ignore `$response.statusCode` — ALWAYS handle non-200 responses

## Reference Files

- [methods.md](references/methods.md) — HTTP Request node options, OAuth2 flow, pagination options, generic credentials
- [examples.md](references/examples.md) — REST API integration, OAuth2 flow, paginated fetching, batch requests
- [anti-patterns.md](references/anti-patterns.md) — Common integration mistakes and corrections
