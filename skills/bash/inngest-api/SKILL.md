---
name: inngest-api
description: >-
  Use when the user explicitly asks for the Inngest REST API v2, raw HTTP,
  OpenAPI, API docs, API authentication, or an endpoint that the Inngest CLI
  does not expose. Covers api-docs.inngest.com, llms.txt, the OpenAPI v2 spec,
  Bearer authentication with API keys or signing keys, production and local
  base URLs, raw curl/fetch requests, request-shape discovery, pagination,
  secret redaction, and when to prefer the `inngest-api-cli` skill instead.
---

# Inngest REST API v2

Use this skill for raw REST API v2 work and API reference lookup. If the task
can be completed through `npx inngest-cli@latest api`, use `inngest-api-cli`
instead; the CLI is safer for agents because it handles target/auth flags and
endpoint command wiring.

## Prefer CLI First

Use `inngest-api-cli` for:

- Run and trace debugging from a run ID or event ID.
- Account, environment, key, webhook, app sync, and function invocation checks.
- Insights table/schema/query workflows.
- Local dev server or Cloud operational checks.

Use raw REST API v2 only when:

- The CLI does not expose the needed endpoint.
- The user explicitly asks for HTTP, curl, fetch, OpenAPI, or API docs.
- You need to inspect request/response schemas before deciding what to do.

## Docs Lookup

When precision matters, fetch current docs instead of guessing:

- API overview: `https://api-docs.inngest.com/`
- Authentication: `https://api-docs.inngest.com/authentication`
- LLM index: `https://api-docs.inngest.com/llms.txt`
- OpenAPI v2 spec: `https://api-docs.inngest.com/api-specs/v2.json`
- Markdown page pattern: add `.md` to a docs URL, for example
  `https://api-docs.inngest.com/v2/runs/GetFunctionTrace.md`
- Endpoint request/response schemas:
  [references/rest-api-v2.md](references/rest-api-v2.md)

If a Markdown page returns an error or omits generated reference details, use
the OpenAPI spec for methods, paths, parameters, request bodies, and schemas.

## Base URLs

- Cloud v2: `https://api.inngest.com/v2`
- Local dev server v2: `http://localhost:8288/api/v2`
- API docs say the dev server may also be reached through the local server
  origin. Confirm the actual dev server port before making local requests.

## Authentication

The REST API uses Bearer token authentication.

- Prefer `INNGEST_API_KEY` for requests from CI, scripts, tools, and agents.
- Signing keys are primarily for apps communicating with Inngest; use them for
  API requests only when that is the available, appropriate credential.
- API keys are for v2 endpoints only.
- Include `X-Inngest-Env` or use an environment-scoped API key when operating
  outside the default production environment.
- Never paste, print, commit, or log API keys, event keys, signing keys,
  webhook URLs, or decrypted secrets.

Example:

```bash
curl -fsSL \
  -H "Authorization: Bearer $INNGEST_API_KEY" \
  -H "X-Inngest-Env: $INNGEST_ENV" \
  https://api.inngest.com/v2/account
```

## Endpoint Discovery

Use the OpenAPI spec as the source of truth:

```bash
curl -fsSL https://api-docs.inngest.com/api-specs/v2.json
```

Current v2 areas include account, environments, keys, webhooks, apps, function
invocation, event-run lookup, function runs, traces, Insights, and partner APIs.
Endpoint coverage can change, so inspect the spec before writing a raw request.

For API-only or access-gated endpoints, such as partner-account endpoints,
confirm the user has the needed access before attempting a call.

## Request Rules

- Derive method, path, query params, headers, and body from OpenAPI.
- Do not invent undocumented request fields.
- Use structured JSON parsing before making decisions from responses.
- Use body files or here-docs for complex JSON instead of shell-escaped one
  liners.
- Add pagination cursors when `page.hasMore` is true and complete results are
  needed.
- Treat missing `data` in list responses as an empty list unless an error is
  present.

## Mutation Safety

Read before write. Confirm target account, environment, resource, and intent
before raw HTTP mutations unless the user's instruction already makes all of
that explicit.

Treat these categories as mutating or side-effecting:

- Creating or patching environments.
- Creating webhooks.
- Syncing apps.
- Invoking functions.
- Partner account creation.
- Broad Insights queries that may be expensive or noisy.

## Output Handling

- Summarize IDs, names, statuses, pagination, and actionable errors.
- Redact token values, webhook URLs, sensitive payload fields, and decrypted
  secrets.
- Do not paste large raw traces, full OpenAPI fragments, or full response
  bodies unless the user asks.
- If auth fails, first verify that a credential is present in the environment;
  then ask the user to provide or rotate `INNGEST_API_KEY` without pasting it
  into chat.
