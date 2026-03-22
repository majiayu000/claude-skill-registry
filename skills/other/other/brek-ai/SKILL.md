---
name: brek-ai-skill
description: Integrate with Brek Partner Core Chat API for hotel-search and booking assistant flows. Use when an agent needs to create or continue Brek chat sessions, send user events safely, enforce anti-abuse call controls, and run payment setup or payment confirmation without collecting raw card data.
metadata:
  required_env_vars: BREK_BASE_URL,BREK_PARTNER_API_KEY
  primary_credential: BREK_PARTNER_API_KEY
  required_runtime_inputs: actorId,workspaceId,partnerId,clientActionId
  storage_requirements: durable idempotency dedupe store,budget counter store,usage metering log
  autonomous_invocation: "false"
  always_on_presence: "false"
  config_paths: none
---

# Brek AI Partner Core Chat

Execute Brek through `/api/partner/v1/core-chat`.

Use this execution order:
1. Create one session per end user (`POST /sessions`) with a stable `actor.actorId`.
2. Reuse that session for all follow-up messages (`POST /events`).
3. Read the latest state when needed (`GET /sessions/{sessionId}`).

Do not share one session across different users.

## Required runtime inputs

Require these inputs before calling Brek:
- `BREK_BASE_URL`
- `BREK_PARTNER_API_KEY`
- `actorId` (stable partner-side end-user ID)
- `workspaceId` or tenant context if your product uses workspaces
- `partnerId` (stable partner tenant ID for idempotency and billing grouping)
- `clientActionId` for each write-like event kind

If one required input is missing, stop and request it.

If `BREK_PARTNER_API_KEY` is missing:
- stop outbound calls
- ask the user to get the key from their internal owner or approved support channel
- never request secrets through unapproved channels

## Call safety guardrails

Apply these guardrails before every upstream call:
1. Enforce local budget limits from `references/call-control.md`.
2. Attach a deterministic `idempotencyKey` for all write-like event kinds.
3. Respect `429` with `retry-after` and exponential backoff.
4. Open a circuit breaker after repeated 5xx or timeout failures.
5. Log `x-request-id`, `x-partner-id`, `x-ratelimit-limit`, and `x-ratelimit-remaining`.

Never retry booking or payment-confirm actions without the same `idempotencyKey`.

## Event-kind rules

When `kind` is one of:
- `command_book_by_option_id`
- `action_book_option`
- `action_confirm_price_change`
- `action_confirm_payment_card`
- `action_cancel_booking`

Always include `idempotencyKey`.

Generate `idempotencyKey` as:
- `<partnerId>:<sessionId>:<kind>:<clientActionId>`

If `partnerId` is unavailable in your runtime, use stable tenant context (for example `workspaceId`) and keep the key format deterministic.

## Payment handling

Handle payment in two layers:
1. End-user card setup and confirmation in secure portal flow.
2. Agent-to-agent usage billing and settlement.

Follow `references/payment-and-billing.md` for both layers.

Hard rules:
- Never request or store raw card number, CVV, or full PAN in chat.
- Accept only tokenized `paymentMethodId` from provider-hosted fields.
- Require explicit user confirmation before `action_confirm_payment_card` and booking actions.

## Response mapping

Map Brek response as:
- `data.result.status` -> state machine key for UI and orchestration
- `data.result.message.text` -> user-visible assistant text
- `data.result.artifacts` -> structured payload (shortlist, payment setup URL, booking metadata)

## Error handling

- `400`: request validation failed. Fix payload.
- `401/403`: API key issue. Stop calls. Tell user to rotate or provision key through their internal owner or approved support channel.
- `404`: session not found or wrong tenant.
- `409`: actor/session mismatch. Recreate correct session.
- `429`: throttle locally and retry by `retry-after`.
- `5xx`: retry with backoff, then open breaker.

## References

Read only what you need:
- API payload templates: `references/api-templates.md`
- Call-control and anti-abuse policy: `references/call-control.md`
- Payment and billing orchestration: `references/payment-and-billing.md`
