# App-function `*-hsmeta.json` (serverless) — upload validation

Use this when **`hs project upload`** or **`hs project validate`** fails on files under `src/app/functions/` (or the path your project uses for `app-function` components).

Official baseline: [Serverless functions reference](https://developers.hubspot.com/docs/apps/developer-platform/add-features/serverless-functions/reference).

## Private function (UI extension only)

Boilerplate from the docs is often:

```json
{
  "uid": "app_function_private",
  "type": "app-function",
  "config": {
    "entrypoint": "/app/functions/NewFunction.js",
    "secretKeys": []
  }
}
```

If the CLI still rejects the file, run **`hs project validate`** and align every reported field with the schema your **installed CLI version** expects (schemas tighten over time).

## HTTP / public endpoint functions

When a function is exposed as an **HTTP endpoint** (OAuth callbacks, webhooks, or other inbound HTTP), project validation commonly requires a **`config.endpoint`** object. Typical errors if it is missing:

- `Missing required field: 'config.endpoint'`

### `methods` must be an array (not `method`)

If you use a singular **`method`** property (for example `"method": "GET"`), validation may report:

- `Missing required field: 'config.endpoint.methods'`
- `config.endpoint must NOT have additional properties` with **`additionalProperty: method`**

**Fix:** remove `method` and supply **`methods`** as an **array** of HTTP verbs, for example:

```json
{
  "endpoint": {
    "path": "/jira-oauth-callback",
    "methods": ["GET"]
  }
}
```

Adjust `path` and `methods` to match your routes (e.g. `["POST"]` or `["GET", "POST"]`) per your app’s contract. Confirm allowed shape with **`hs project validate`** after edits.

Public endpoints have product constraints (see the serverless reference: **Content Hub Enterprise** for unauthenticated public endpoints, and implement your own access control where needed).

## Workflow

1. Run **`hs project validate`** for a full list of schema errors (faster iteration than upload alone).
2. Keep **`uid`** unique across all `*-hsmeta.json` files in the project.
3. After changing `*-hsmeta.json`, re-run **`hs project upload`**.

## Doc vs CLI drift

The marketing/reference docs may show older **`endpoint`** field examples (for example a single `method` string). If the **CLI validator** disagrees with a doc snippet, **trust the validator output** for your `hs --version`, and file feedback with HubSpot if the public doc is stale.
