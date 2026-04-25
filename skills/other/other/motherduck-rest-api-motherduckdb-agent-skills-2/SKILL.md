---
name: motherduck-rest-api
description: Use when automating or advising on MotherDuck REST API control-plane workflows for service-account provisioning, supported access-token lifecycle operations, Duckling instance configuration, active account inspection, or Dive embed sessions. Do not use for SQL or data-plane query work.
license: MIT
---

# REST API Administration

Use this skill when the user needs to manage MotherDuck service accounts, supported token operations, Duckling configuration, active accounts, or Dive embed sessions through the REST API.

## Source Of Truth

- Prefer current MotherDuck REST API documentation, the public OpenAPI spec at `https://api.motherduck.com/docs/specs`, or an explicit OpenAPI spec supplied by the user.
- For token scope and embed behavior, cross-check the REST API docs and the Embedded Dives docs because they include operational constraints not obvious from the raw schema.
- If the MotherDuck MCP `ask_docs_question` feature is available, use it to check whether public REST API guidance has changed.
- Treat endpoint availability, preview status, token fields, and role requirements as current only when backed by the supplied spec or current docs.

## Default Posture

- Treat the REST API as the control plane. Use `motherduck-query` for SQL and data-plane work.
- Use `https://api.motherduck.com` as the base URL unless the user provides another environment.
- Authenticate with `Authorization: Bearer ${MOTHERDUCK_ADMIN_TOKEN}` and keep admin read-write tokens in backend-managed secrets.
- Never use read-scaling tokens for REST API administration.
- Prefer read-before-write flows for configuration changes so the current account, service account, Duckling config, or Dive metadata is known before mutation.
- Treat `POST /v1/users` as service-account creation unless current docs explicitly broaden the API.
- Assume active-account, Duckling configuration, service-account creation, service-account token creation, and Dive embed-session endpoints require an organization admin bearer token unless current docs say otherwise.
- Never expose generated access tokens in logs, browser code, client bundles, or committed files.
- Confirm destructive deletes with the user. Deleting a user permanently deletes that user and all of their data.

## Workflow

1. Identify whether the task is service-account provisioning, token management, Duckling sizing, active-account inspection, or Dive embedding.
2. Confirm the admin token location and the target `username` or `dive_id`; never invent production identifiers.
3. Check token scope before calling token endpoints: users can create tokens for themselves, and admins can create tokens for service accounts, but admins cannot create tokens for other non-service-account members through the API.
4. For Duckling config changes, read the current config first, then update both `read_write` and `read_scaling` because the `PUT` payload requires both.
5. Preserve response fields that are only returned once, especially newly created token strings and embed session strings.
6. Surface API errors by status and response body; do not hide `400`, `401`, `403`, `404`, or `500` responses behind success-shaped fallbacks.

## Open Next

- `references/REST_API_GUIDE.md` for endpoint summaries, auth headers, request payloads, curl examples, validation limits, and operational gotchas

## Related Skills

- `motherduck-connect` for connection tokens and application connection posture
- `motherduck-security-governance` for admin-token handling, service-account posture, and access-boundary questions
- `motherduck-create-dive` for designing Dives before minting embed sessions
