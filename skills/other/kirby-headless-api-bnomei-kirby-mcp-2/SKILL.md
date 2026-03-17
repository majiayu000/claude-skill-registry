---
name: kirby-headless-api
description: Exposes Kirby content to headless clients using the API, KQL, and JSON representations. Use when building API endpoints, KQL queries, or headless frontends.
---

# Kirby Headless API

## KB entry points

- `kirby://kb/scenarios/44-headless-api-with-kql`
- `kirby://kb/scenarios/02-json-content-representation-ajax-load-more`
- `kirby://kb/scenarios/45-headless-kiosk-application`
- `kirby://kb/scenarios/28-figma-auto-populate`

## Required inputs

- Consumers and auth requirements.
- Public vs private content boundaries.
- Response shape and caching policy.
- Preferred approach (KQL, representations, or routes).

## Default delivery choices

- Use `.json` representations for page-backed responses.
- Use KQL for cross-collection queries and filtered datasets.
- Use routes for non-page or composite endpoints.

## Default response envelope

```json
{
  "status": "ok",
  "data": {}
}
```

## Caching rule

- Public endpoints: set `Cache-Control` with a short max-age.
- Authenticated endpoints: disable caching.

## Common pitfalls

- Exposing private fields or drafts in JSON output.
- Caching authenticated responses.

## Verification checklist

- Confirm auth requirements and public/private boundaries.
- Validate JSON output for required fields.

## Workflow

1. Clarify consumers, authentication, and which content is public vs private.
2. Call `kirby:kirby_init` and read `kirby://config/api` to confirm API settings.
3. Check plugin availability for KQL: `kirby:kirby_plugins_index`.
4. If you need custom endpoints, inspect existing routes with `kirby:kirby_routes_index` (install runtime if needed).
5. Search the KB with `kirby:kirby_search` (examples: "headless api with kql", "json content representation", "figma auto populate", "headless kiosk").
6. Use `kirby:kirby_online` to fetch official API/KQL docs when KB coverage is insufficient.
7. Implement:
   - enable API auth (`api.basicAuth`) when required
   - create or update KQL queries for `/api/query`
   - add `.json` representations for template-backed JSON
8. Verify:
   - request `/api/query` with Basic Auth
   - render `.json` representations with `kirby:kirby_render_page(contentType: json)`
