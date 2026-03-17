---
name: moltpho
description: Shop autonomously on Amazon via Moltpho - search products, manage credit, and purchase items using mUSD on Base mainnet
metadata: {"requires": {"http": true, "browser": true}}
---

# Moltpho Shopping Skill

Shop for items on Amazon autonomously using credit-backed mUSD tokens on Base mainnet.

## Overview

Moltpho is a headless shopping mall that enables AI agents to discover and purchase Amazon products using a credit system backed by mUSD (an ERC-20 token on Base mainnet). This skill handles:

- Agent registration and credential management
- Product search and discovery
- Autonomous and proactive purchasing
- Credit balance monitoring
- x402 payment protocol integration

## Bootstrap Flow

On first invocation, the skill MUST check for existing credentials and register if needed.

### Credentials Location

| Platform | Path |
|----------|------|
| Linux/macOS | `~/.config/moltpho/credentials.json` |
| Windows | `%APPDATA%\moltpho\credentials.json` |
| Override | `MOLTPHO_CREDENTIALS_PATH` environment variable |

### Registration Process

1. **Check credentials file** at the appropriate path
2. **If missing**, call `POST /v1/agents/register` with:
   - `openclaw_instance_id` (if available)
   - `agent_display_name`
   - `agent_description`
   - No shipping profile required at registration
3. **Save credentials** with `chmod 600` permissions
4. **Auto-open browser** with notice: "Opening portal in your browser to complete setup..."
5. Registration proceeds WITHOUT shipping profile - orders will fail until owner adds one via portal

### Credentials File Format

```json
{
  "agent_id": "uuid",
  "api_key_id": "moltpho_key_...",
  "api_key_secret": "moltpho_secret_...",
  "api_base_url": "https://api.moltpho.com",
  "wallet_address": "0xabc123..."
}
```

## Core Functions

### bootstrap()

Initialize agent credentials and open portal for owner setup.

```
1. Check if credentials file exists at platform-specific path
2. If exists and valid: load credentials, verify with GET /v1/agents/me
3. If missing or invalid:
   a. Call POST /v1/agents/register (no auth required)
   b. Receive: agent_id, api_key_id, api_key_secret, claim_url, wallet_address
   c. Write credentials file with chmod 600
   d. Display: "Opening portal in your browser to complete setup..."
   e. Open browser to claim_url (valid for 24 hours)
4. Return agent status (UNCLAIMED, CLAIMED, DEGRADED, SUSPENDED)
```

### collect_shipping_profile()

Optionally collect shipping information from the owner.

```
Note: This is OPTIONAL. Owners can configure shipping via the portal instead.
      Orders will fail with INVALID_SHIPPING_PROFILE until a profile exists.

If collecting in conversation:
1. Request full name
2. Request address (street, city, state, ZIP)
3. Request email
4. Request phone
5. Validate: US addresses only (international not supported in v1)
6. Call POST /v1/shipping_profiles (upsert_shipping_profile)
7. Confirm profile saved

The POST endpoint upserts the default profile:
- If no profile exists, creates one
- If a profile exists, updates it
```

### update_shipping_profile()

Update the shipping address for the agent.

```
Parameters:
- full_name: Recipient full name
- address1: Street address
- address2: Apt/suite (optional)
- city: City
- state: State (2-letter code)
- postal_code: ZIP code
- email: Contact email
- phone: Contact phone

Process:
1. Validate all required fields
2. Validate US address (only US supported in v1)
3. Call POST /v1/shipping_profiles (upserts default profile)
4. Return updated profile

Use cases:
- "Update my shipping address"
- "Change my delivery address to..."
- First-time setup during bootstrap
```

### catalog_search(query, constraints)

Search for products on Amazon via Moltpho.

```
Parameters:
- query: Search terms (string)
- constraints: Optional filters
  - max_price: Maximum price in USD
  - category: Product category keyword
  - min_rating: Minimum star rating (1-5)

Process:
1. Call GET /v1/catalog/search?query={query}&limit=20
2. Apply local constraints if provided
3. Present results with:
   - Product title and brand
   - Moltpho price (final price, includes 10% markup)
   - Availability status
   - Rating if available
4. If cache expired, results include "prices may have changed" warning

Rate limit: 60 requests/minute
```

### purchase(item, qty)

Execute a purchase through the x402 payment flow.

```
Parameters:
- item: ASIN or product identifier
- qty: Quantity (default 1)

Process:
1. BUDGET CHECK: Call GET /v1/balance to verify available credit
   - available_credit = balance - active_reservations
   - Check against per_order_cap if set
   - Check against daily_cap if set

2. CREATE QUOTE: Call POST /v1/quotes
   - Include: asin, quantity, shipping_profile_id
   - Returns: quote_id, total_due_usd, expires_at (10 min TTL)
   - Creates soft reservation against balance
   - May fail with INVALID_SHIPPING_PROFILE if no profile set

3. INITIATE ORDER: Call POST /v1/orders with quote_id
   - First call returns 402 Payment Required with PAYMENT-REQUIRED header

4. SIGN PAYMENT: Call POST /v1/wallets/x402/sign
   - Include: payment_required blob, idempotency_key
   - Returns: payment_signature for x402 header

5. COMPLETE ORDER: Retry POST /v1/orders with PAYMENT-SIGNATURE header
   - On success: returns order_id, status (PAID/PLACED)
   - Soft reservation converted to actual spend

Auto-retry on quote expiry:
- If quote expires during flow, automatically retry up to 3 times
- Only retry if new price is within 5% of original quote
- Fail after 3 retries or if price changed >5%

Rate limits:
- Quotes: 20/minute
- Orders: 5/minute
- Signing: 10/minute
```

### proactive_monitoring()

Watch conversation for purchase need signals and act when appropriate.

```
This function runs passively during conversation to detect purchase opportunities.

NEED SIGNALS (explicit):
- "I need", "we're out of", "buy", "order", "replace"
- "running low on", "almost out of"
- Direct product mentions with urgency

NEED SIGNALS (implicit):
- Repeated complaints about missing items
- Critical item shortages mentioned
- Context suggesting immediate need

CONFIDENCE SCORING:
- 1.0: Explicit purchase request ("buy me X")
- 0.8: Strong implied need ("we're completely out of toilet paper")
- 0.5: Weak implied convenience (do NOT buy)
- 0.0: Unknown/unclear

BUDGET SIGNAL HANDLING:
- Phrases like "money is tight", "on a budget", "can't afford"
- Reduce confidence by 0.3-0.5
- Proceed cautiously if still above threshold

PROACTIVE PURCHASE ALLOWED IF ALL TRUE:
- Owner has enabled proactive purchasing (default ON)
- Confidence >= 0.8 (threshold)
- Item matches low-risk categories:
  - Household essentials
  - Office supplies
  - Cables/adapters
  - Basic kitchen items
  - Toiletries
- Price <= min(per_order_cap, $75)
- Item keywords not in denied categories
- Item not in system blocklist
- Shipping profile exists

LOGGING:
Every purchase logs:
- "why we bought" (decision reason)
- Signals detected
- Confidence tier (HIGH/MEDIUM/LOW)
- Budget impact
```

### budget_check()

Verify sufficient credit before any purchase.

```
Process:
1. Call GET /v1/balance
2. Response includes:
   - available_credit_cents: Spendable amount
   - staged_refunds: Pending refunds (shown with asterisk)
   - target_limit: Owner's configured credit limit
3. Compare against:
   - Quote total
   - per_order_cap (if set)
   - daily_cap (if set, track daily spending)
4. Return: can_purchase (bool), available_amount, reason_if_blocked
```

### create_support_ticket(type, description, order_id)

Create a support ticket for returns, lost packages, or other issues.

```
Parameters:
- type: Ticket type - RETURN, LOST_PACKAGE, or OTHER
- description: Detailed description of the issue (1-2000 chars)
- order_id: Order ID (required for RETURN and LOST_PACKAGE)

Process:
1. Validate ticket type and description
2. If RETURN or LOST_PACKAGE, verify order_id is provided
3. Call POST /v1/support_tickets with { type, description, order_id }
4. Return ticket ID and status

Use cases:
- "I want to return this item" → type=RETURN, link to order
- "My package never arrived" → type=LOST_PACKAGE, link to order
- "I have a question about billing" → type=OTHER, no order needed

Note: Returns and lost packages require a support ticket.
      Automated refunds only happen for order cancellations.
```

### list_support_tickets()

List the agent's support tickets.

```
Process:
1. Call GET /v1/support_tickets
2. Display tickets with: type, status, order link, creation date
3. Status meanings:
   - OPEN: Submitted, awaiting support review
   - IN_PROGRESS: Being handled
   - WAITING_CUSTOMER: Support needs more info from you
   - RESOLVED: Issue resolved
   - CLOSED: Ticket closed
```

### logout()

Delete local credentials (agent persists server-side).

```
Process:
1. Delete credentials file at platform-specific path
2. Display: "Credentials removed. Agent still exists on Moltpho servers."
3. To fully delete agent, owner must use portal

Note: This only removes LOCAL credentials. The agent account, wallet, and
      purchase history remain on Moltpho servers until owner deletes via portal.
```

## Browser Portal Usage

The skill uses the browser for owner-sensitive operations.

### When to Open Browser

| Action | Method |
|--------|--------|
| Complete setup (claim link) | Auto-open with notice |
| Add/manage payment cards | Direct owner to portal |
| Set credit limits | Direct owner to portal |
| Configure shipping profile | Direct owner to portal |
| View order history | Direct owner to portal |

### Browser Guidelines

- Always display notice: "Opening portal in your browser..."
- NEVER request card numbers, passwords, or sensitive credentials in chat
- Portal handles all PCI-sensitive operations via Stripe Elements
- Owner authenticates via magic link (email-based)

## API Authentication

All API requests (except registration) require authentication.

### Headers

```
Authorization: Bearer <api_key_secret>
```

Or preferably:
```
X-Moltpho-Key-Id: <api_key_id>
X-Moltpho-Signature: <HMAC signature>
```

### Idempotency

For state-changing operations, always include:
```
Idempotency-Key: <unique-key>
```

Required for:
- POST /v1/quotes
- POST /v1/orders
- POST /v1/wallets/x402/sign

## Error Handling

### Common Errors

| Code | Error | Action |
|------|-------|--------|
| 401 | UNAUTHORIZED | Re-bootstrap or check credentials |
| 402 | PAYMENT_REQUIRED | Sign and retry with x402 signature |
| 409 | PRICE_CHANGED | Re-quote if price increased >2% |
| 409 | INSUFFICIENT_CREDIT | Inform user, suggest adding credit |
| 409 | QUOTE_EXPIRED | Auto-retry (up to 3x) or re-quote |
| 422 | INVALID_SHIPPING_PROFILE | Prompt owner to add shipping via portal |
| 422 | AGENT_SUSPENDED | Inform owner, direct to portal |
| 429 | RATE_LIMITED | Wait per Retry-After header |
| 503 | TOKEN_PAUSED | System halted, wait for admin |

### Quote Expiry Auto-Retry

When a quote expires during the x402 flow:
1. Fetch new quote for same item
2. Compare price to original quote
3. If within 5% tolerance: continue with new quote
4. If >5% change: fail with PRICE_CHANGED
5. Maximum 3 retry attempts

## Constraints and Limits

### System Limits

| Limit | Value |
|-------|-------|
| Maximum item price | $10,000 USD |
| Quote TTL | 10 minutes (fixed) |
| Price tolerance | 2% increase allowed |
| Retry price tolerance | 5% for auto-retry |
| Max concurrent quotes | 5 per agent |
| Proactive purchase cap | min(per_order_cap, $75) |

### Rate Limits

| Endpoint | Limit |
|----------|-------|
| Catalog search | 60/minute |
| Quotes | 20/minute |
| Orders | 5/minute |
| Signing | 10/minute |

### Blocked Items (System Enforced)

The following categories CANNOT be purchased regardless of owner settings:
- Weapons, firearms, ammunition
- Controlled substances, prescription medications
- Tobacco, nicotine products
- Alcohol
- Adult content
- Hazardous materials

## Payment System

### Credit Model

- Owner sets target credit limit in USD
- Weekly automatic top-up restores credit to target
- Credit backed by mUSD tokens on Base mainnet
- 10% markup over Amazon prices (covers fees + gas)

### x402 Flow

1. POST /v1/orders returns 402 with PAYMENT-REQUIRED header
2. Call POST /v1/wallets/x402/sign with payment blob
3. Wallet service signs EIP-3009 authorization
4. Retry order with PAYMENT-SIGNATURE header
5. Facilitator settles on Base mainnet
6. Order proceeds to fulfillment

### Refunds

| Scenario | Refund Target |
|----------|---------------|
| Procurement failure | mUSD balance (auto) |
| Order canceled (within 5 min) | mUSD balance (auto) |
| Owner decreases credit limit | Card via Stripe |
| Return/lost package | Support ticket required (use create_support_ticket) |

## Agent States

| State | Meaning | Can Order? |
|-------|---------|------------|
| UNCLAIMED | Registered, awaiting owner claim | No |
| CLAIMED | Owner claimed, fully operational | Yes |
| DEGRADED | Payment methods failed, using remaining balance | Yes (if balance) |
| SUSPENDED | Admin action, requires manual resolution | No |

## Best Practices

### Before Any Purchase

1. Call budget_check() to verify available credit
2. Confirm shipping profile exists
3. Check item against category denylist
4. Verify confidence threshold for proactive purchases

### Conversation Guidelines

- Always confirm purchase with total price before executing
- Report order status and remaining credit after purchase
- If budget signals detected, acknowledge constraints
- Never pressure user to add more credit

### Error Recovery

- On INSUFFICIENT_CREDIT: suggest adding credit via portal
- On INVALID_SHIPPING_PROFILE: collect shipping info and call upsert_shipping_profile(), or direct to portal
- On SUSPENDED: explain owner must resolve via portal

## Quick Reference

### Essential Endpoints

| Endpoint | Purpose |
|----------|---------|
| POST /v1/agents/register | New agent registration |
| GET /v1/agents/me | Current agent status |
| GET /v1/balance | Available credit |
| GET /v1/catalog/search | Search products |
| POST /v1/quotes | Create purchase quote |
| POST /v1/orders | Place order (x402) |
| POST /v1/wallets/x402/sign | Sign payment |
| GET /v1/shipping_profiles | List shipping profiles |
| POST /v1/shipping_profiles | Create/update shipping profile |
| POST /v1/support_tickets | Create support ticket |
| GET /v1/support_tickets | List support tickets |

### Portal URL

```
https://portal.moltpho.com
```

Owner actions:
- /claim/{token} - Claim agent ownership
- /agents - Manage agents
- /cards - Payment methods
- /orders - Order history
- /settings - Credit limits and preferences
