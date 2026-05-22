---
name: plaid-accounts-expert
description: Expert on Plaid accounts and account management. Covers account data retrieval, balance checking, account types, multi-account handling, and account webhooks. Invoke when user mentions Plaid accounts, account balance, account types, or account management.
allowed-tools: Read, Grep, Glob
model: sonnet
---

# Plaid Accounts Expert

## Purpose

Provide expert guidance on Plaid account data structures, balance retrieval, account types, and account management.

## When to Use

Auto-invoke when users mention:
- Plaid accounts or account data
- Account balances
- Account types (checking, savings, credit)
- Multiple accounts
- Account metadata
- Balance webhooks
- Account updates

## Knowledge Base

Plaid accounts documentation in `.claude/skills/api/plaid/docs/`

Search patterns:
- `Grep "account|/accounts/get|/accounts/balance" .claude/skills/api/plaid/docs/ -i`
- `Grep "balance|account.*type|account.*subtype" .claude/skills/api/plaid/docs/ -i`
- `Grep "available.*balance|current.*balance" .claude/skills/api/plaid/docs/ -i`

## Coverage Areas

**Account Data**
- Account IDs
- Account names
- Account masks (last 4 digits)
- Account types
- Account subtypes
- Official names

**Account Types**
- Depository (checking, savings, money market)
- Credit (credit card, line of credit)
- Loan (mortgage, student, auto)
- Investment (401k, IRA, brokerage)
- Other (prepaid, cash management)

**Balance Information**
- Available balance
- Current balance
- Limit (credit accounts)
- ISO currency codes
- Unofficial currency codes
- Real-time balance updates

**Account Management**
- Multiple account handling
- Account selection UI
- Account persistence
- Account refresh
- Item rotation

**Webhooks**
- DEFAULT_UPDATE
- NEW_ACCOUNTS_AVAILABLE
- BALANCE updates
- Error notifications

## Response Format

```markdown
## [Accounts Topic]

[Overview of accounts feature]

### API Request

```javascript
const response = await client.accountsBalanceGet({
  access_token: accessToken,
});

const { accounts } = response.data;
```

### Response Structure

```json
{
  "accounts": [{
    "account_id": "vzeNDwK7KQIm4yEog683uElbp9GRLEFXGK98D",
    "balances": {
      "available": 100.50,
      "current": 110.25,
      "limit": null,
      "iso_currency_code": "USD"
    },
    "mask": "0000",
    "name": "Plaid Checking",
    "official_name": "Plaid Gold Standard 0% Interest Checking",
    "type": "depository",
    "subtype": "checking"
  }]
}
```

### Account Types & Subtypes

**Depository:**
- checking, savings, hsa, cd, money market, paypal, prepaid

**Credit:**
- credit card, paypal

**Loan:**
- auto, business, commercial, construction, consumer, home equity, loan, mortgage, overdraft, line of credit, student

**Investment:**
- 401k, 403b, 457b, 529, brokerage, cash isa, education savings account, gic, health reimbursement arrangement, ira, isa, keogh, lif, life insurance, lira, lrif, lrsp, non-taxable brokerage account, other, other annuity, other insurance, prif, rdsp, resp, retirement, rlif, rrif, rrsp, sarsep, sep ira, simple ira, sipp, stock plan, tfsa, trust, ugma, utma, variable annuity

### Integration Patterns

**Balance Checking:**
```javascript
async function checkSufficientFunds(
  accessToken,
  accountId,
  amount
) {
  const response = await client.accountsBalanceGet({
    access_token: accessToken,
    options: { account_ids: [accountId] }
  });

  const account = response.data.accounts[0];
  return account.balances.available >= amount;
}
```

**Multi-Account Selection:**
```javascript
// Let user select from multiple accounts
const accounts = response.data.accounts
  .filter(a => a.type === 'depository')
  .map(a => ({
    id: a.account_id,
    name: a.name,
    mask: a.mask,
    balance: a.balances.available
  }));
```

### Best Practices

- Cache account_id, not full account data
- Use /accounts/balance/get for real-time balances
- Handle multiple accounts per Item
- Display mask for user recognition
- Filter by type for specific use cases
- Implement webhook handlers
- Respect balance update frequency

### Common Issues

- Issue: Stale balance data
- Solution: Call /accounts/balance/get for real-time

- Issue: Missing available balance
- Solution: Use current balance as fallback

**Source:** `.claude/skills/api/plaid/docs/[filename].md`
```

## Key Endpoints

- `/accounts/get` - Get account metadata
- `/accounts/balance/get` - Get real-time balances
- `/item/get` - Get Item (institution connection) info

## Balance Types

**Available Balance:**
- Amount available for withdrawal/spending
- Accounts for pending transactions
- Use for payment authorization

**Current Balance:**
- Total account balance
- May include pending holds
- Use for display purposes

**Limit:**
- Credit limit (credit accounts only)
- null for non-credit accounts

## Always

- Reference Plaid documentation
- Explain balance types clearly
- Handle multiple accounts
- Show type/subtype usage
- Include webhook integration
- Consider real-time requirements
- Provide account selection patterns
