---
category: Business
id: proxy-pay-mcp
name: Proxy Pay Mcp
description: Proxy MCP server integration for agent payments. Use MCP tools to create intents, issue cards within policy, and track transactions. Supports agent tokens for autonomous runs and OAuth for interactive clients.
---

# Proxy MCP Integration

Connect to Proxy's MCP server for agent payments.

## MCP server config

### Agent token (autonomous)

```json
{
  "mcpServers": {
    "proxy": {
      "type": "http",
      "url": "https://mcp.useproxy.ai/api/mcp",
      "headers": {
        "Authorization": "Bearer $PROXY_AGENT_TOKEN"
      }
    }
  }
}
```

### OAuth (interactive clients)

Add the MCP server and run your client's OAuth login flow. OAuth is for interactive clients (Codex, Claude, Cursor).

## Core flow (agent token)

```
proxy.kyc.status
proxy.balance.get
proxy.policies.simulate (optional)
proxy.intents.create
if approvalRequired/pending_approval -> proxy.intents.request_approval
proxy.cards.get_sensitive (include intentId + reason)
proxy.transactions.list_for_card
```

## Agent-token tools (autonomous)

- proxy.user.get
- proxy.kyc.status
- proxy.kyc.link
- proxy.policies.get
- proxy.policies.simulate
- proxy.balance.get
- proxy.tools.list
- proxy.intents.create (agent token required)
- proxy.intents.list
- proxy.intents.get
- proxy.intents.request_approval
- proxy.intents.approval_status
- proxy.cards.get_sensitive
- proxy.transactions.list_for_card
- proxy.transactions.get
- proxy.receipts.attach
- proxy.evidence.list_for_intent
- proxy.merchants.resolve
- proxy.mcc.explain (advisory)
- proxy.merchants.allowlist_suggest (advisory)

## Human-only tools (blocked for agent tokens)

- proxy.funding.get
- proxy.cards.list
- proxy.cards.get
- proxy.cards.freeze
- proxy.cards.unfreeze
- proxy.cards.rotate
- proxy.cards.close
- proxy.intents.approve
- proxy.intents.reject
- proxy.webhooks.list
- proxy.webhooks.test_event

## Approval behavior

- Approval is required only when policy.requireApproval is true and the amount exceeds autoApproveBelow.
- Agents should call proxy.intents.request_approval only when needed.

## Notes

- Intents are required for every purchase. Cards stay locked between intents.
- Merchant/MCC rules are advisory unless issuer-level controls are enabled.
- proxy.cards.get_sensitive requires intentId and a clear reason; avoid logging PAN/CVV.
- Amounts are in cents; formatted fields are provided for display where applicable.

## Error format

```json
{
  "success": false,
  "error": {
    "code": "POLICY_REQUIRED",
    "message": "No policy configured",
    "hint": "Assign a policy to this agent",
    "context": "intents.create"
  }
}
```
