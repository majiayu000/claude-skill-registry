---
name: whatsapp-flows
description: Manage WhatsApp Flows via Kapso Platform API. List, create, update, publish flows, manage versions, attach data endpoints, and check encryption. Use when working with WhatsApp Flows, flow JSON, or data endpoints.
---

# WhatsApp Flow Management

## When to use

Use this skill to manage WhatsApp Flows end-to-end: discover flows, edit flow JSON via versions, publish/test, attach data endpoints, and inspect responses/logs.

## Setup

Env vars:
- `KAPSO_API_BASE_URL` (host only, no `/platform/v1`)
- `KAPSO_API_KEY`
- `PROJECT_ID`
- `META_GRAPH_VERSION` (optional, default `v24.0`)

Run scripts with Node or Bun:
```bash
node scripts/list-flows.js
```

## How to

### Create and publish a flow

1. Create flow: `node scripts/create-flow.js --phone-number-id <id> --name <name>`
2. Read `references/whatsapp-flows-spec.md` for Flow JSON rules
3. Update JSON: `node scripts/update-flow-json.js --flow-id <id> --json-file <path>`
4. Publish: `node scripts/publish-flow.js --flow-id <id>`
5. Test: `node scripts/send-test-flow.js --phone-number-id <id> --flow-id <id> --to <phone>`

### Attach a data endpoint (dynamic flows)

1. Set up encryption: `node scripts/setup-encryption.js --flow-id <id>`
2. Create endpoint: `node scripts/set-data-endpoint.js --flow-id <id> --code-file <path>`
3. Deploy: `node scripts/deploy-data-endpoint.js --flow-id <id>`
4. Register: `node scripts/register-data-endpoint.js --flow-id <id>`

### Debug flows

- List responses: `node scripts/list-flow-responses.js --flow-id <id>`
- Function logs: `node scripts/list-function-logs.js --flow-id <id>`
- Function invocations: `node scripts/list-function-invocations.js --flow-id <id>`

## Flow JSON rules

Static flows (no data endpoint):
- Use `version: "7.3"`
- `routing_model` and `data_api_version` are optional
- See `assets/sample-flow.json`

Dynamic flows (with data endpoint):
- Use `version: "7.3"` with `data_api_version: "3.0"`
- `routing_model` is **required** - defines valid screen transitions
- See `assets/dynamic-flow.json`

Read the full spec in `references/whatsapp-flows-spec.md` before editing.

## Data endpoint rules

Handler signature:
```js
async function handler(request, env) {
  const body = await request.json();
  // body.data_exchange.action: INIT | data_exchange | BACK
  // body.data_exchange.screen: current screen id
  // body.data_exchange.data: user inputs
  return Response.json({
    version: "3.0",
    screen: "NEXT_SCREEN_ID",
    data: { ... }
  });
}
```

- Do not use `export` or `module.exports`
- Completion uses `screen: "SUCCESS"` with `extension_message_response.params`
- Do not include `endpoint_uri` or `data_channel_uri` (Kapso injects these)

## Scripts

### Platform API

| Script | Purpose |
|--------|---------|
| `list-flows.js` | List all flows |
| `create-flow.js` | Create a new flow |
| `get-flow.js` | Get flow details |
| `read-flow-json.js` | Read flow JSON |
| `update-flow-json.js` | Update flow JSON (creates new version) |
| `publish-flow.js` | Publish a flow |
| `get-data-endpoint.js` | Get data endpoint config |
| `set-data-endpoint.js` | Create/update data endpoint code |
| `deploy-data-endpoint.js` | Deploy data endpoint |
| `register-data-endpoint.js` | Register data endpoint with Meta |
| `get-encryption-status.js` | Check encryption status |
| `setup-encryption.js` | Set up flow encryption |

### Meta proxy

| Script | Purpose |
|--------|---------|
| `send-test-flow.js` | Send a test flow message |
| `delete-flow.js` | Delete a flow |

### Logs and responses

| Script | Purpose |
|--------|---------|
| `list-flow-responses.js` | List stored flow responses |
| `list-function-logs.js` | List function logs |
| `list-function-invocations.js` | List function invocations |

## Troubleshooting

- **Preview shows "flow_token is missing"**: Flow is dynamic without a data endpoint. Attach one and refresh.
- **Encryption setup errors**: Enable encryption in Settings for the phone number/WABA.
- **OAuthException 139000 (Integrity)**: WABA must be verified in Meta security center.

## References

- [references/whatsapp-flows-spec.md](references/whatsapp-flows-spec.md) - Flow JSON spec (read before editing)
- [assets/sample-flow.json](assets/sample-flow.json) - Static flow example (no endpoint)
- [assets/dynamic-flow.json](assets/dynamic-flow.json) - Dynamic flow example (with endpoint)

## Related skills

- `whatsapp-messaging` - WhatsApp messaging and templates
- `kapso-automation` - Workflow automation
- `kapso-api` - Platform API and customers
