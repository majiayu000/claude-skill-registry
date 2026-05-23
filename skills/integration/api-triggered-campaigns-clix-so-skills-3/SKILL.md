---
name: clix-api-triggered-campaigns
display-name: API-Triggered Campaigns
short-description: API-triggered campaign setup
description: Helps developers configure API-triggered campaigns in the Clix console and
  trigger them from backend services with safe auth, payload schemas, dynamic
  audience filters (trigger.*), and personalization best practices. Use when the
  user mentions transactional notifications, backend-triggered sends,
  campaign_id trigger APIs, or "API-triggered campaigns".
user-invocable: true
---

# API-Triggered Campaigns (Backend → Clix)

Use this skill to set up **API-triggered campaigns** in the Clix console and
trigger them from your backend with dynamic data (`trigger.*`) for:

- Transactional notifications (orders, password reset, receipts)
- Workflow messages (assignments, approvals)
- System alerts (moderation, support tickets)
- Programmatic sends where marketers/ops should control content + targeting

## What the official docs guarantee (high-signal)

- API-triggered campaigns are configured in the console, then triggered via:
  `POST /api/v1/campaigns/{campaign_id}:trigger`
- Authentication uses **secret** headers:
  - `X-Clix-Project-ID`
  - `X-Clix-API-Key`
- Request `properties` become **`trigger.*`** for:
  - **Dynamic audience filtering** (console audience rules)
  - **Personalization** in templates (title/body/deep links)
- `audience.broadcast=true` sends to all users eligible under the campaign’s
  segment definition; `audience.targets` narrows to specific users/devices
  (still filtered by the segment definition).
- Dynamic audience filters are intentionally constrained for performance: **max
  3 attributes** in the audience definition.

## MCP-first (source of truth)

If Clix MCP tools are available, treat them as the **source of truth**:

- Use `clix-mcp-server:search_docs` to confirm the latest API contract + limits:
  - query examples:
    - `"API-triggered campaign trigger endpoint"`
    - `"campaigns/{campaign_id}:trigger audience targets broadcast"`
    - `"trigger.* dynamic audience filters limitations"`

If MCP tools are not available, use the bundled references:

- API contract → `references/api-contract.md`
- Console setup + dynamic filters → `references/console-setup.md`
- Backend patterns (auth, retries, timeouts) → `references/backend-patterns.md`
- Security/key handling → `references/security-and-keys.md`
- Personalization + dynamic filters →
  `references/personalization-and-dynamic-filters.md`
- Debugging checklist → `references/debugging.md`

## Workflow (copy + check off)

```
API-triggered campaign progress:
- [ ] 1) Confirm goals + trigger source (what backend event sends the message?)
- [ ] 2) Define campaign contract (properties keys/types; PII policy)
- [ ] 3) Configure campaign in console (API-triggered + audience rules + templates)
- [ ] 4) Implement backend trigger wrapper (auth, timeout, retries, logging)
- [ ] 5) Validate trigger plan JSON (schema + naming + safety)
- [ ] 6) Verify in Clix (test payloads, Message Logs, segment matching)
```

## 1) Confirm the minimum inputs

Ask only what’s needed:

- **Campaign**: where is it in the console? do you already have `campaign_id`?
- **Channel**: push / in-app / email / etc. (affects message template fields)
- **Audience mode**: broadcast vs explicit targets
- **Dynamic filter keys**: which `trigger.*` keys are used in audience rules
- **Properties**: list of keys + types + example values (avoid PII by default)
- **Backend**: runtime and HTTP client (Node/Fetch, Axios, Python, Go, etc.)

## 2) Create a “Trigger Plan” (before touching backend code)

Create `api-trigger-plan.json` in `.clix/` (recommended) or project root.

**Recommended location**: `.clix/api-trigger-plan.json`

**Plan schema (high-level):**

- `campaign_id` (string)
- `audience.mode`: `"broadcast" | "targets" | "default"`
- `audience.targets` (if mode is `"targets"`)
- `dynamic_filter_keys` (array of up to 3 snake_case keys)
- `properties` (map of snake_case keys → `{ type, required?, example?, pii? }`)

Example:

```json
{
  "campaign_id": "019aa002-1d0e-7407-a0c5-5bfa8dd2be30",
  "audience": {
    "mode": "broadcast"
  },
  "dynamic_filter_keys": ["store_location"],
  "properties": {
    "store_location": {
      "type": "string",
      "required": true,
      "example": "San Francisco"
    },
    "order_id": { "type": "string", "required": true, "example": "ORD-12345" },
    "item_count": { "type": "number", "required": true, "example": 3 },
    "pickup_time": { "type": "string", "required": false, "example": "2:30 PM" }
  }
}
```

## 3) Configure campaign in the console (API-triggered)

- Set the campaign type to **API-Triggered**.
- Build audience rules using `{{ trigger.* }}` for dynamic filters.
- Use `{{ trigger.* }}` in message templates + deep links.

See: `references/console-setup.md` for exact guidance and limitations.

## 4) Implement backend trigger wrapper (best practices)

Backend wrapper responsibilities:

- **Auth**: load `X-Clix-Project-ID` and `X-Clix-API-Key` from
  environment/secret store (never commit).
- **Timeout**: set a short timeout (e.g., 3–10s) and fail fast.
- **Retries**: retry only on transient failures (network/5xx), with backoff; do
  not retry blindly on 4xx.
- **Dedupe**: prevent double-sends in your system (e.g., unique key per order
  event) since the API call is “send-like”.
- **Logging**: log `campaign_id`, your correlation id (order id), and the Clix
  response (e.g., `trigger_id`).

Copy/paste examples:

- Node: `examples/trigger-campaign-node.js`
- Python: `examples/trigger-campaign-python.py`

## 5) Validate the plan (fast feedback loop)

Run:

```bash
bash <skill-dir>/scripts/validate-api-trigger-plan.sh .clix/api-trigger-plan.json
```

This validator checks:

- valid JSON
- `campaign_id` present
- `dynamic_filter_keys` is ≤ 3 and snake_case
- `properties` keys are snake_case and have valid types
- example values match declared types
- `targets` entries specify exactly one of `project_user_id` or `device_id`

## 6) Verify (Clix + end-to-end)

Minimum verification:

- Campaign is **API-Triggered** and `campaign_id` matches.
- If using dynamic audience filters, the `trigger.*` keys exist in the API call
  and match audience rules exactly.
- Trigger once with a known-good payload; confirm delivery + inspect Message
  Logs for rendering errors.

See `references/debugging.md`.

## Progressive Disclosure

- **Level 1**: This `SKILL.md` (always loaded)
- **Level 2**: `references/` (load when implementing details)
- **Level 3**: `examples/` (load when copy/pasting backend code)
- **Level 4**: `scripts/` (execute directly; do not load into context)

## References

- `references/api-contract.md`
- `references/console-setup.md`
- `references/backend-patterns.md`
- `references/security-and-keys.md`
- `references/personalization-and-dynamic-filters.md`
- `references/debugging.md`
