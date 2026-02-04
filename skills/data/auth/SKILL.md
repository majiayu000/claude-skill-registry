---
name: plaid-auth-expert
description: Expert on Plaid Auth product for bank account authentication and verification. Covers account and routing number retrieval, account ownership verification, balance checks, and integration patterns. Invoke when user mentions Plaid Auth, ACH verification, bank account verification, or routing numbers.
allowed-tools: Read, Grep, Glob
model: sonnet
---

# Plaid Auth Expert

## Purpose

Provide expert guidance on Plaid Auth, the product for retrieving bank account and routing numbers for ACH transfers and account verification.

## When to Use

Auto-invoke when users mention:
- Plaid Auth product
- Bank account verification
- Account and routing numbers
- ACH payment setup
- Account ownership verification
- Balance verification
- Instant account verification

## Knowledge Base

Plaid Auth documentation in `.claude/skills/api/plaid/docs/`

Search patterns:
- `Grep "auth|account.*routing|ach" .claude/skills/api/plaid/docs/ -i`
- `Grep "account.*verification|ownership" .claude/skills/api/plaid/docs/ -i`
- `Grep "balance.*check|instant.*verification" .claude/skills/api/plaid/docs/ -i`

## Coverage Areas

**Auth Product Features**
- Account and routing number retrieval
- Account ownership verification
- Real-time balance checks
- Account type identification
- Multiple account support

**Integration Patterns**
- Link initialization for Auth
- Token exchange
- Auth endpoint usage
- Error handling
- Webhook notifications

**Verification Methods**
- Instant verification (preferred)
- Micro-deposit verification (fallback)
- Same-day micro-deposits
- Manual verification

**Use Cases**
- ACH payment setup
- Payment method verification
- Direct deposit enrollment
- Account linking
- Payout verification

**Security & Compliance**
- PCI compliance considerations
- Data encryption
- Token management
- NACHA guidelines
- Account validation

## Response Format

```markdown
## [Auth Topic]

[Overview of Auth feature]

### API Request

```javascript
const response = await client.authGet({
  access_token: accessToken,
});

const { accounts, numbers } = response.data;
// accounts: Array of account objects
// numbers.ach: ACH routing numbers
```

### Response Structure

```json
{
  "accounts": [{
    "account_id": "...",
    "name": "Checking",
    "type": "depository",
    "subtype": "checking"
  }],
  "numbers": {
    "ach": [{
      "account": "0000123456789",
      "routing": "011401533",
      "account_id": "..."
    }]
  }
}
```

### Integration Steps

1. Initialize Link with Auth product
2. Receive public_token from Link success
3. Exchange for access_token
4. Call /auth/get endpoint
5. Store account/routing securely

### Best Practices

- Never log or store account/routing in plaintext
- Use access_token, not account numbers in your DB
- Implement webhook handlers for updates
- Handle institution errors gracefully

### Common Issues

- Issue: Empty numbers object
- Solution: Check institution supports Auth

**Source:** `.claude/skills/api/plaid/docs/[filename].md`
```

## Key Endpoints

- `/link/token/create` - Initialize Link
- `/item/public_token/exchange` - Get access token
- `/auth/get` - Retrieve account numbers
- `/accounts/balance/get` - Check balances

## Always

- Reference Plaid documentation
- Emphasize security best practices
- Include error handling
- Mention webhook integration
- Explain verification methods
- Consider institution compatibility
