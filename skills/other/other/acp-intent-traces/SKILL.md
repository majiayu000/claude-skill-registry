---
name: acp-intent-traces
description: Implement ACP intent traces — structured cart abandonment signals with reason codes for analytics and automated recovery workflows. Use when building abandonment tracking, recovery automation, or conversion optimization.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# ACP Intent Traces

## Before writing code

**Fetch live docs**:
1. Web-search `site:github.com agentic-commerce-protocol rfcs intent_traces` for the intent traces RFC
2. Fetch `https://developers.openai.com/commerce/specs/checkout/` for how intent traces integrate with checkout
3. Web-search `site:github.com agentic-commerce-protocol spec json-schema intent` for the schema

## Conceptual Architecture

### What Intent Traces Are

Intent traces are a **built-in ACP extension** that provides structured cart abandonment signals. When a buyer abandons a checkout, the agent sends a trace explaining why — enabling merchants to understand conversion barriers and automate recovery.

### 10 Reason Codes

| Code | Meaning |
|------|---------|
| `price_sensitivity` | Total was too expensive |
| `shipping_cost` | Shipping cost was a barrier |
| `shipping_speed` | Delivery time was too slow |
| `product_fit` | Product didn't match buyer's needs |
| `trust_security` | Buyer didn't trust the merchant/payment |
| `returns_policy` | Return/refund policy was inadequate |
| `payment_options` | Preferred payment method unavailable |
| `comparison` | Buyer is comparison shopping |
| `timing_deferred` | Buyer wants to purchase later |
| `other` | Doesn't fit other categories |

### How It Works

1. Buyer initiates checkout but doesn't complete
2. Agent detects abandonment (session timeout, explicit cancellation, navigation away)
3. Agent sends intent trace via `POST /checkout_sessions/{id}/cancel`, including a single `reason_code` (required enum string, exactly one per trace)
4. Merchant receives the trace and can:
   - Aggregate for analytics
   - Trigger automated recovery (email, discount offer)
   - Adjust pricing/shipping strategy

### Privacy Considerations

- Intent traces contain behavioral signals — handle per GDPR/CCPA
- Only collect traces when the buyer has consented to data collection
- Don't store personally identifiable information in trace metadata
- Aggregate traces for analytics rather than individual tracking

### Extension Negotiation

Like all extensions, intent traces must be negotiated:
1. Agent includes `intent_traces` in `capabilities.extensions[]`
2. Merchant confirms support
3. Only then are traces exchanged

### Use Cases

- Cart abandonment analytics dashboards
- Automated recovery email workflows
- Dynamic pricing based on price sensitivity signals
- Shipping strategy optimization
- A/B testing checkout flows
- Conversion funnel analysis

### Additional Trace Fields

- **`trace_summary`** — Optional free-text summary of the abandonment reason (max 500 characters)
- **`metadata`** — Optional flat key-value map for additional context (string keys and string values only)

### Write-Only Behavior

Intent traces are **write-only** — they are sent on the `POST /checkout_sessions/{id}/cancel` endpoint and are never echoed back in GET responses. This prevents information leakage and ensures traces are used only for analytics and recovery workflows.

### Best Practices

- Send traces on every abandonment — even `other` is better than no signal
- Each trace has a single `reason_code` (required enum string); if the buyer has multiple reasons, choose the most significant one
- Process traces asynchronously — don't block the cancellation flow
- Build aggregate dashboards before automated recovery
- Test trace collection end-to-end with the agent platform
- Respect buyer privacy — anonymize before long-term storage

Fetch the intent traces RFC for exact trace payload structure, reason code definitions, and integration points before implementing.
