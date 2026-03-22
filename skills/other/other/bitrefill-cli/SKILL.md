---
name: bitrefill-cli
description: "Buy gift cards, mobile top-ups, and eSIMs on Bitrefill. Pay with crypto and x402. 1,500+ brands, 180+ countries"
compatibility: "Node.js >=18, npm, Bitrefill account. Auth: BITREFILL_API_KEY env var (headless) or OAuth token. Payment: a crypto wallet able to send crypto or pay to x402 endpoint (USDC on Base)."
metadata:
  author: bitrefill
  version: "1.5.0"
  homepage: "https://www.bitrefill.com"
  repository: "https://github.com/bitrefill/cli"
---

# Bitrefill CLI

Search, purchase, and deliver digital goods (gift cards, mobile top-ups, eSIMs) via the [Bitrefill CLI](https://github.com/bitrefill/cli).

## Requirements

- A **Bitrefill account** is required to use this skill. Authentication is done via the Bitrefill API key or OAuth. See [Setup](#setup) for more details.
- A **crypto wallet** is required to send crypto or pay to x402 endpoint (USDC on Base). NOT PROVIDED BY THIS SKILL.
- "Browser usage" MCP or CLI is suggested for the agent to **redeem the code on the brand's website**, for fully autonomous shopping experiences. NOT PROVIDED BY THIS SKILL.

## Supported Payment Methods

Best payment experiences for instant agentic payments is store credits via **`balance`**, then USDC on Base via x402, then Lightning. All the other crypto payments requirse the agent to poll the invoice status to confirm payment.

CLI returns the full list with `bitrefill buy-products --help`

- **`balance`** — Instant fulfillment, no on-chain wait. User pre-funds at [bitrefill.com](https://www.bitrefill.com). Natural spending cap.
- **`usdc_base`** with x402 — Use `--return_payment_link true` (default) to get `x402_payment_url`. An x402-capable agent completes payment autonomously over Base.
- **`lightning`** — Lightning — `lightningInvoice`, `satoshiPrice`
- **`ethereum`** — Ethereum mainnet (ETH) — `address`, `paymentUri`, `altcoinPrice`
- **`eth_base`** — Base (8453), native ETH
- **`usdc_base`** — Base (8453), USDC
- **`usdc_arbitrum`** — Arbitrum (42161), USDC
- **`usdc_polygon`** — Polygon (137), USDC
- **`usdc_erc20`** — Ethereum (1), USDC
- **`usdc_solana`** — Solana, USDC
- **`usdt_polygon`** — Polygon (137), USDT
- **`usdt_erc20`** — Ethereum (1), USDT
- **Payment cards, local payment methods and other crypto payment methods are available in the checkout page returned by the `--return_payment_link true` option.**

## Spending Safeguards

This skill enables **real-money transactions**. Purchases are fulfilled instantly after payment is confirmed.

- **Default: always confirm before purchasing.** Present product, denomination, price, and payment method; wait for explicit approval before `buy-products`. Autonomous purchasing only when the user explicitly opts in for the current session.
- As soon as digital goods are delivered, they are refundable only in case they don't work as expected. According to the **EU Consumer Rights**, digital goods like gift card codes are not subject to 14-day change of mind policy.
- A **gift card code can be considered cash-like**, so it should be stored securely and not shared publicly. Only the agent's owner should have access to the code. Prefer encrypted data storage for the code rather than plain text.
- Try as much as possible to avoid re-writing the digital codes. If possible, prefer **in-memory storage** until the code is redeemed, and to programmatically access and use it only then.
- If the user asks for the code, return it but advise them to **store it securely, not share it publicly, and use it as soon as possible**.
- Use a **dedicated, limited-balance account** — never give agents access to high-balance accounts.
- **Terms of Service:** https://www.bitrefill.com/terms/ contains important information about the refund policy and purchase limits.
- **Log every purchase:** `invoice_id`, product, amount, payment method.
- **Not a wallet:** This skill is not a wallet. It is a tool for buying products on Bitrefill. It is not responsible for storing private keys or managing your crypto wallet.
- **Browser usage:** When trying to redeem a code on the brand's website, anti-bot protection mechanisms may block the agent. In that case, ask the user if they want to complete manually the redemption process and, in case, return the code to the user.

## Setup

### Install

```bash
npm install -g @bitrefill/cli
```

From source: `git clone https://github.com/bitrefill/cli.git && cd cli && pnpm install && pnpm build && npm link`

### Auth

Generate an API key at [bitrefill.com/account/developers](https://www.bitrefill.com/account/developers):

```bash
export BITREFILL_API_KEY=YOUR_API_KEY
```

Alternative: run any command without an API key to trigger browser-based OAuth. Token stored at `~/.config/bitrefill-cli/api.bitrefill.com.json`. Clear with `bitrefill logout`.

### Environment

| Variable | Purpose |
|----------|---------|
| `BITREFILL_API_KEY` | Headless auth (skips OAuth) |

## Core Workflow

```
search-products → get-product-details → buy-products → get-invoice-by-id / list-orders
```

### 1. Search

```bash
bitrefill search-products --query "Netflix" --country US
bitrefill search-products --query "eSIM" --product_type esim --country IT
bitrefill search-products --query "*" --category games
```

`--country` must be **uppercase Alpha-2 ISO** (`US`, `IT`, `BR`). `--product_type`: `giftcard` or `esim` (singular).

**Discovering categories:** Search with `--query "*"` — the response includes a `categories` array with slugs and counts (e.g. `food`, `games`, `streaming`). Add `--country` to see categories available in a specific country. Use these slugs as `--category` values.

### 2. Get Details

```bash
bitrefill get-product-details --product_id "steam-usa"
```

Returns a `packages` array. Each entry has a `package_value` — use this as `package_id` in `buy-products`.

**Ignore compound keys** like `steam-usa<&>5` — use only the value after `<&>`.

Three denomination types:

- **Numeric:** `5`, `50`, `200` (pass as number)
- **Duration:** `"1 Month"`, `"12 Months"` (exact string, case-sensitive)
- **Named:** `"1GB, 7 Days"`, `"PUBG New State 300 NC"` (exact string, case-sensitive)

Only values from `get-product-details` are accepted — arbitrary amounts are rejected.

### 3. Buy

`--cart_items` must be a **JSON array** `[...]`, even for a single item.

```bash
# Numeric
bitrefill buy-products \
  --cart_items '[{"product_id": "steam-usa", "package_id": 5}]' \
  --payment_method usdc_base

# Duration
bitrefill buy-products \
  --cart_items '[{"product_id": "spotify-usa", "package_id": "1 Month"}]' \
  --payment_method balance

# Named (eSIM)
bitrefill buy-products \
  --cart_items '[{"product_id": "bitrefill-esim-europe", "package_id": "1GB, 7 Days"}]' \
  --payment_method usdc_base
```

Response includes `invoice_id`, `payment_link`, and `x402_payment_url`.

Max 15 items per call.

### 4. Track

```bash
bitrefill get-invoice-by-id --invoice_id "UUID"
bitrefill list-orders --include_redemption_info true
```

## Critical Gotchas

**`cart_items` must be array, not object:**

```bash
# WRONG
--cart_items '{"product_id": "steam-usa", "package_id": 5}'
# RIGHT
--cart_items '[{"product_id": "steam-usa", "package_id": 5}]'
```

**Use `package_value` after `<&>`, not the compound key:**

```bash
# WRONG: "steam-usa<&>5"  →  RIGHT: 5
```

**Named/duration `package_id` must be exact, case-sensitive:**

```bash
# WRONG: "1GB"    →  RIGHT: "1GB, 7 Days"
# WRONG: "300 nc" →  RIGHT: "PUBG New State 300 NC"
```

**Country codes must be uppercase Alpha-2:**

```bash
# WRONG: us, USA, "United States"  →  RIGHT: US
```

## References

Load when needed:

| Reference | Use when |
|-----------|----------|
| [commands](references/commands.md) | Full option tables for any command |
| [payment](references/payment.md) | Payment methods list, x402 protocol, response fields |
| [troubleshooting](references/troubleshooting.md) | Errors beyond the critical gotchas above |
