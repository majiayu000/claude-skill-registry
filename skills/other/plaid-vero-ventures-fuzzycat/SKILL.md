---
name: plaid
description: >
  Interact with Plaid API for bank account verification. Check sandbox status, test Link
  tokens, inspect items and accounts, and debug bank verification issues. Uses sandbox
  environment for development.
allowed-tools: Bash, Read, Grep, Glob
---

# Plaid REST API

Manage FuzzyCat's Plaid integration via curl. Currently in **sandbox** mode.

## Authentication

```bash
PLAID_CLIENT_ID=$(grep PLAID_CLIENT_ID .env.local | cut -d'"' -f2)
PLAID_SECRET=$(grep PLAID_SECRET .env.local | cut -d'"' -f2)
PLAID_ENV=$(grep PLAID_ENV .env.local | cut -d'"' -f2)  # "sandbox"

# Base URL by environment
# sandbox:     https://sandbox.plaid.com
# development: https://development.plaid.com
# production:  https://production.plaid.com
PLAID_URL="https://${PLAID_ENV}.plaid.com"
```

## Common Commands

### Health & Status

```bash
# Check API status (no auth needed)
curl -s "https://status.plaid.com/api/v2/status.json" | python3 -m json.tool
```

### Link Tokens

```bash
# Create a Link token (for testing)
curl -s -X POST "$PLAID_URL/link/token/create" \
  -H "Content-Type: application/json" \
  -d "{
    \"client_id\": \"$PLAID_CLIENT_ID\",
    \"secret\": \"$PLAID_SECRET\",
    \"user\": {\"client_user_id\": \"test-user-1\"},
    \"client_name\": \"FuzzyCat\",
    \"products\": [\"auth\"],
    \"country_codes\": [\"US\"],
    \"language\": \"en\"
  }" | python3 -m json.tool
```

### Items & Accounts

```bash
# Get item details (requires access_token from Link flow)
curl -s -X POST "$PLAID_URL/item/get" \
  -H "Content-Type: application/json" \
  -d "{
    \"client_id\": \"$PLAID_CLIENT_ID\",
    \"secret\": \"$PLAID_SECRET\",
    \"access_token\": \"access-sandbox-xxx\"
  }" | python3 -m json.tool

# Get auth data (account + routing numbers)
curl -s -X POST "$PLAID_URL/auth/get" \
  -H "Content-Type: application/json" \
  -d "{
    \"client_id\": \"$PLAID_CLIENT_ID\",
    \"secret\": \"$PLAID_SECRET\",
    \"access_token\": \"access-sandbox-xxx\"
  }" | python3 -m json.tool

# Get account balances
curl -s -X POST "$PLAID_URL/accounts/balance/get" \
  -H "Content-Type: application/json" \
  -d "{
    \"client_id\": \"$PLAID_CLIENT_ID\",
    \"secret\": \"$PLAID_SECRET\",
    \"access_token\": \"access-sandbox-xxx\"
  }" | python3 -m json.tool
```

### Sandbox Testing

```bash
# Create a sandbox public token (for testing without Link UI)
curl -s -X POST "$PLAID_URL/sandbox/public_token/create" \
  -H "Content-Type: application/json" \
  -d "{
    \"client_id\": \"$PLAID_CLIENT_ID\",
    \"secret\": \"$PLAID_SECRET\",
    \"institution_id\": \"ins_109508\",
    \"initial_products\": [\"auth\"]
  }" | python3 -m json.tool

# Exchange public token for access token
curl -s -X POST "$PLAID_URL/item/public_token/exchange" \
  -H "Content-Type: application/json" \
  -d "{
    \"client_id\": \"$PLAID_CLIENT_ID\",
    \"secret\": \"$PLAID_SECRET\",
    \"public_token\": \"public-sandbox-xxx\"
  }" | python3 -m json.tool

# Fire a sandbox webhook
curl -s -X POST "$PLAID_URL/sandbox/item/fire_webhook" \
  -H "Content-Type: application/json" \
  -d "{
    \"client_id\": \"$PLAID_CLIENT_ID\",
    \"secret\": \"$PLAID_SECRET\",
    \"access_token\": \"access-sandbox-xxx\",
    \"webhook_code\": \"DEFAULT_UPDATE\"
  }" | python3 -m json.tool
```

### Institutions

```bash
# Search institutions
curl -s -X POST "$PLAID_URL/institutions/search" \
  -H "Content-Type: application/json" \
  -d "{
    \"client_id\": \"$PLAID_CLIENT_ID\",
    \"secret\": \"$PLAID_SECRET\",
    \"query\": \"Chase\",
    \"products\": [\"auth\"],
    \"country_codes\": [\"US\"]
  }" | python3 -m json.tool
```

## FuzzyCat-Specific

- **Products used**: `auth` (account + routing numbers for ACH)
- **Sandbox credentials**: Username `user_good`, password `pass_good`
- **Key files**: `server/services/plaid.ts`, `app/api/plaid/` routes
- **Webhook**: JWT-verified at `/api/plaid/webhook`
- **Never store**: raw account/routing numbers (PCI compliance)
