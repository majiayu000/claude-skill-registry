---
name: brighty
description: Banking interface for AI bots and automation. Get a bank account, issue a Mastercard, buy and sell crypto, send payments and invoices — all via API. Use when the user needs a bank account for a bot, wants to manage balances, make transfers, handle payouts, or operate cards.
metadata: {"openclaw":{"requires":{"env":["BRIGHTY_API_KEY"],"bins":["mcporter"]},"primaryEnv":"BRIGHTY_API_KEY","emoji":"🏦","homepage":"https://github.com/Maay/brighty_mcp"}}
---

# Brighty Business & Freelance Banking

Give your bot a bank account. MCP server for [Brighty](https://brighty.app) banking API via mcporter — open accounts, issue Mastercard cards, buy and sell crypto, send SEPA/SWIFT payments. Works for both business and freelance accounts.

## Getting Started

### 1. Sign up

Register at [Brighty Business Portal](https://business.brighty.app/auth?signup=true). Both business and freelance accounts are supported — freelance accounts are particularly well-suited for bots and automation. The owner walks through the onboarding steps.

**What you get by default:**
- Crypto account
- EUR / USD / GBP fiat account for self-transfers only (no third-party payments)
- Mastercard virtual card issuance (linked to crypto or fiat accounts)

**Need to pay third parties (invoices, salaries, etc.)?**
Contact support to enable a full fiat account with outgoing payments:
- Telegram: [@DonatasSupportBot](https://t.me/DonatasSupportBot)
- Email: support@brighty.app

The bank will set it up within a few days.

### 2. Get API key

Go to [Account > Business](https://business.brighty.app/account/business) and click **Create API Token**. Only the business **owner** can do this.

### 3. Configure

This skill includes `config/mcporter.json` which auto-registers the brighty MCP server. You just need to set the API key:

```bash
# Add to your environment (e.g. ~/.openclaw/.env)
BRIGHTY_API_KEY=your-api-key
```

Or configure manually:

```bash
mcporter config add brighty --command "npx -y github:Maay/brighty_mcp" --env BRIGHTY_API_KEY=your-api-key
```

Check connection: `mcporter call brighty.brighty_status`

**Security:**
- Never store API key in SKILL.md, memory files, or chat history
- Key lives only in env or `config/mcporter.json` (local, not pushed to git)

## Authorization Notice

All actions performed through this skill are executed on behalf of the business owner. By using this skill, the owner confirms they authorize these operations.

## Tool Reference

All tools called via `mcporter call brighty.<tool> [params]`.

### Accounts
- `brighty_list_accounts` — list all accounts (optional: `type=CURRENT|SAVING`, `holderId=UUID`)
- `brighty_get_account id=UUID` — account details
- `brighty_create_account name=X type=CURRENT|SAVING currency=EUR`
- `brighty_terminate_account id=UUID` — close account (must be zero balance)
- `brighty_get_account_addresses id=UUID` — routing/crypto deposit addresses

### Cards
- `brighty_list_cards` — all business cards
- `brighty_get_card id=UUID`
- `brighty_order_card customerId=UUID cardName=X sourceAccountId=UUID cardDesignId=UUID`
- `brighty_freeze_card id=UUID` / `brighty_unfreeze_card id=UUID`
- `brighty_set_card_limits id=UUID currency=EUR dailyLimit=1000 monthlyLimit=5000`
- `brighty_list_card_designs` / `brighty_get_virtual_card_product`

### Transfers (between own accounts)
- `brighty_transfer_own sourceAccountId=UUID targetAccountId=UUID amount=100 currency=EUR`
- `brighty_transfer_intent` — preview exchange rate/fees before transfer (same params + `side=SELL|BUY`, `sourceCurrency`, `targetCurrency`)

### Payouts (batch transfers to others)
- `brighty_list_payouts` / `brighty_get_payout id=UUID`
- `brighty_create_payout name=X` — create batch
- `brighty_create_internal_transfer` — add Brighty-to-Brighty transfer to payout (by `recipientAccountId` or `recipientTag`)
- `brighty_create_external_transfer` — add fiat (IBAN) or crypto transfer to payout
- `brighty_start_payout id=UUID` — execute all transfers in batch

### Team
- `brighty_list_members`
- `brighty_add_members emails=a@b.com,c@d.com role=ADMIN|MEMBER`
- `brighty_remove_members memberIds=UUID1,UUID2`

## Workflows

### Pay an invoice
1. Extract recipient name, IBAN, BIC, amount, currency, reference from invoice
2. `brighty_list_accounts` — find source account
3. `brighty_create_payout name="Invoice payment"`
4. `brighty_create_external_transfer` with extracted details
5. **Confirm with user** before `brighty_start_payout`

### Mass salary payout
1. Parse recipient list (names, IBANs, amounts)
2. `brighty_create_payout name="Salaries Feb 2026"`
3. Add each transfer via `brighty_create_external_transfer` or `brighty_create_internal_transfer`
4. Show summary, **confirm with user**, then `brighty_start_payout`

## Safety

- **Always confirm** before executing payouts (`brighty_start_payout`)
- **Always confirm** before terminating accounts
- Show amounts and recipients clearly before any money movement
- API docs: [apidocs.brighty.app](https://apidocs.brighty.app/docs/api/brighty-api)
