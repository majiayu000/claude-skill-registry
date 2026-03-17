---
name: sparkbtcbot-proxy
description: Use a Spark Bitcoin L2 wallet proxy for AI agents via HTTP API. Check balances, send payments, create invoices, pay L402 paywalls — all without holding the mnemonic. Use when user mentions "Spark proxy," "wallet API," "L402," "proxy payment," "bearer token auth," or wants secured Bitcoin capabilities for an agent.
argument-hint: "[Optional: specify operation - balance, pay, invoice, l402, transfer, or setup]"
homepage: https://github.com/echennells/sparkbtcbot-proxy
source: https://github.com/echennells/sparkbtcbot-proxy
requires:
  env:
    - name: PROXY_URL
      description: HTTPS URL of your deployed sparkbtcbot-proxy instance (e.g., https://your-app.vercel.app)
      sensitive: false
    - name: PROXY_TOKEN
      description: Bearer token for proxy authentication. Create via POST /api/tokens with an admin token. Use least-privilege roles — prefer 'read-only', 'invoice', or 'pay-only' over 'admin' for agents.
      sensitive: true
model-invocation: autonomous
model-invocation-reason: This skill enables agents to call a wallet proxy API. Autonomous invocation is intentional for payment workflows, but the proxy enforces spending limits and role-based access. Always use least-privilege tokens and set per-tx/daily caps on the proxy side.
---

# Spark Bitcoin L2 Proxy for AI Agents

You are an expert in using the sparkbtcbot-proxy — a serverless HTTP API that gives AI agents scoped access to a Spark Bitcoin L2 wallet without exposing the private key.

## Why Use the Proxy Instead of Direct SDK

| Concern | Direct SDK (sparkbtcbot-skill) | Proxy (this skill) |
|---------|-------------------------------|-------------------|
| Mnemonic location | Agent holds it | Server holds it |
| Spending limits | None (agent decides) | Per-tx and daily caps |
| Access revocation | Move funds to new wallet | Revoke bearer token |
| Role-based access | No | Yes (admin, invoice, pay-only, read-only) |
| Setup complexity | npm install + mnemonic | HTTP calls + bearer token |

**Use the proxy when:**
- You don't trust the agent with full wallet control
- You need spending limits or audit logs
- You want to revoke access without moving funds
- Multiple agents share one wallet with different permissions

**Use direct SDK when:**
- Testing or development
- Agent needs offline signing
- You're building the proxy itself

## Before You Start

1. **Deploy your own proxy** — see [sparkbtcbot-proxy](https://github.com/echennells/sparkbtcbot-proxy) for setup instructions. The proxy runs on Vercel (free tier works) with Upstash Redis.

2. **Use HTTPS only** — never connect to a proxy over plain HTTP. All Vercel deployments use HTTPS by default.

3. **Create least-privilege tokens** — don't give agents admin tokens. Use the most restrictive role that works:
   - `read-only` for monitoring/dashboard agents
   - `invoice` for agents that receive payments but don't spend
   - `pay-only` for agents that pay L402 paywalls but don't create invoices
   - `admin` only for your own management scripts

4. **Set spending limits** — configure `maxTxSats` and `dailyBudgetSats` when creating tokens. The proxy enforces these server-side.

5. **Test with small amounts** — start with a few hundred sats until you trust your agent's behavior.

6. **Have a revocation plan** — know how to revoke tokens via `DELETE /api/tokens` if an agent is compromised.

## Token Roles

| Role | Permissions |
|------|-------------|
| `admin` | Full access: read, create invoices, pay, transfer, manage tokens |
| `invoice` | Read + create invoices. Cannot pay or transfer. |
| `pay-only` | Read + pay invoices and L402. Cannot create invoices or transfer. |
| `read-only` | Read only (balance, info, transactions, logs). Cannot pay or create invoices. |

## Base URL

The proxy runs on Vercel. Your base URL will look like:
```
https://your-deployment.vercel.app
```

All requests require authentication:
```
Authorization: Bearer <your-token>
```

## API Reference

### Read Operations (any role)

#### Get Balance

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/balance"
```

Response:
```json
{
  "success": true,
  "data": {
    "balance": "50000",
    "tokenBalances": {
      "btkn1...": {
        "balance": "1000",
        "tokenMetadata": {
          "tokenName": "Example Token",
          "tokenTicker": "EXT",
          "decimals": 0
        }
      }
    }
  }
}
```

#### Get Wallet Info

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/info"
```

Response:
```json
{
  "success": true,
  "data": {
    "sparkAddress": "sp1p...",
    "identityPublicKey": "02abc..."
  }
}
```

#### Get Deposit Address (L1 Bitcoin)

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/deposit-address"
```

Response:
```json
{
  "success": true,
  "data": {
    "address": "bc1p..."
  }
}
```

#### Get Transaction History

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/transactions?limit=10&offset=0"
```

#### Get Fee Estimate

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/fee-estimate?invoice=lnbc..."
```

Response:
```json
{
  "success": true,
  "data": {
    "feeSats": 5
  }
}
```

#### Get Activity Logs

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/logs?limit=20"
```

### Invoice Operations (admin or invoice role)

#### Create Lightning Invoice (BOLT11)

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amountSats": 1000, "memo": "Payment for service", "expirySeconds": 3600}' \
  "$PROXY_URL/api/invoice/create"
```

Response:
```json
{
  "success": true,
  "data": {
    "encodedInvoice": "lnbc10u1p..."
  }
}
```

#### Create Spark Invoice

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 1000, "memo": "Spark payment"}' \
  "$PROXY_URL/api/invoice/spark"
```

### Payment Operations (admin or pay-only role)

#### Pay Lightning Invoice

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"invoice": "lnbc10u1p...", "maxFeeSats": 10}' \
  "$PROXY_URL/api/pay"
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "payment-id-123",
    "status": "LIGHTNING_PAYMENT_SUCCEEDED",
    "paymentPreimage": "abc123..."
  }
}
```

#### Transfer to Spark Address

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receiverSparkAddress": "sp1p...", "amountSats": 1000}' \
  "$PROXY_URL/api/transfer"
```

### L402 Paywall Operations (admin or pay-only role)

L402 lets you pay for API access with Lightning. The proxy handles the full flow automatically.

#### Pay L402 and Fetch Content

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://lightningfaucet.com/api/l402/joke", "maxFeeSats": 50}' \
  "$PROXY_URL/api/l402"
```

Response (immediate success):
```json
{
  "success": true,
  "data": {
    "status": 200,
    "paid": true,
    "priceSats": 21,
    "preimage": "be2ebe7c...",
    "data": {"setup": "Why do programmers...", "punchline": "..."}
  }
}
```

Response (cached token reused):
```json
{
  "success": true,
  "data": {
    "status": 200,
    "paid": false,
    "cached": true,
    "data": {"setup": "...", "punchline": "..."}
  }
}
```

#### Preview L402 Cost (any role)

Check what an L402 resource costs without paying:

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://lightningfaucet.com/api/l402/joke"}' \
  "$PROXY_URL/api/l402/preview"
```

Response:
```json
{
  "success": true,
  "data": {
    "requires_payment": true,
    "invoice_amount_sats": 21,
    "invoice": "lnbc210n1p...",
    "macaroon": "AgELbGlnaHRuaW5n..."
  }
}
```

#### Handling Pending L402 Payments (IMPORTANT)

Lightning payments are asynchronous. If the preimage isn't available within ~7.5 seconds, the proxy returns a pending status:

```json
{
  "success": true,
  "data": {
    "status": "pending",
    "pendingId": "a1b2c3d4...",
    "message": "Payment sent but preimage not yet available. Poll GET /api/l402/status?id=<pendingId> to complete.",
    "priceSats": 21
  }
}
```

**You MUST handle this case.** The payment has been sent — if you don't poll, you lose sats without getting content.

Poll for completion:

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/l402/status?id=a1b2c3d4..."
```

**Recommended retry logic:**

```javascript
async function fetchL402(proxyUrl, token, targetUrl, maxFeeSats = 50) {
  const response = await fetch(`${proxyUrl}/api/l402`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url: targetUrl, maxFeeSats }),
  });

  const result = await response.json();

  if (result.data?.status === 'pending') {
    const pendingId = result.data.pendingId;
    for (let i = 0; i < 10; i++) {
      await new Promise(r => setTimeout(r, 3000));
      const statusResponse = await fetch(
        `${proxyUrl}/api/l402/status?id=${pendingId}`,
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      const statusResult = await statusResponse.json();
      if (statusResult.data?.status !== 'pending') {
        return statusResult;
      }
    }
    throw new Error('L402 payment timed out');
  }

  return result;
}
```

### Token Management (admin role only)

#### List Tokens

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/tokens"
```

#### Create Token

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role": "invoice", "label": "merchant-bot", "maxTxSats": 5000, "dailyBudgetSats": 50000}' \
  "$PROXY_URL/api/tokens"
```

Response includes the full token string — save it, shown only once:
```json
{
  "success": true,
  "data": {
    "token": "sbp_abc123...",
    "role": "invoice",
    "label": "merchant-bot"
  }
}
```

#### Revoke Token

```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"token": "sbp_abc123..."}' \
  "$PROXY_URL/api/tokens"
```

## Complete Agent Class (JavaScript)

```javascript
export class SparkProxyAgent {
  #baseUrl;
  #token;

  constructor(baseUrl, token) {
    this.#baseUrl = baseUrl.replace(/\/$/, '');
    this.#token = token;
  }

  async #request(method, path, body = null) {
    const options = {
      method,
      headers: {
        'Authorization': `Bearer ${this.#token}`,
        'Content-Type': 'application/json',
      },
    };
    if (body) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(`${this.#baseUrl}${path}`, options);
    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || 'Request failed');
    }
    return result.data;
  }

  async getBalance() {
    return this.#request('GET', '/api/balance');
  }

  async getInfo() {
    return this.#request('GET', '/api/info');
  }

  async getDepositAddress() {
    return this.#request('GET', '/api/deposit-address');
  }

  async getTransactions(limit = 10, offset = 0) {
    return this.#request('GET', `/api/transactions?limit=${limit}&offset=${offset}`);
  }

  async getFeeEstimate(invoice) {
    return this.#request('GET', `/api/fee-estimate?invoice=${encodeURIComponent(invoice)}`);
  }

  async createLightningInvoice(amountSats, memo = '', expirySeconds = 3600) {
    return this.#request('POST', '/api/invoice/create', {
      amountSats,
      memo,
      expirySeconds,
    });
  }

  async createSparkInvoice(amount, memo = '') {
    return this.#request('POST', '/api/invoice/spark', { amount, memo });
  }

  async payLightningInvoice(invoice, maxFeeSats = 10) {
    return this.#request('POST', '/api/pay', { invoice, maxFeeSats });
  }

  async transfer(receiverSparkAddress, amountSats) {
    return this.#request('POST', '/api/transfer', {
      receiverSparkAddress,
      amountSats,
    });
  }

  async previewL402(url) {
    return this.#request('POST', '/api/l402/preview', { url });
  }

  async fetchL402(url, options = {}) {
    const { method = 'GET', headers = {}, body, maxFeeSats = 50 } = options;

    const result = await this.#request('POST', '/api/l402', {
      url,
      method,
      headers,
      body,
      maxFeeSats,
    });

    // Handle pending status with polling
    if (result.status === 'pending') {
      const pendingId = result.pendingId;
      for (let i = 0; i < 10; i++) {
        await new Promise(r => setTimeout(r, 3000));
        const status = await this.#request('GET', `/api/l402/status?id=${pendingId}`);
        if (status.status !== 'pending') {
          return status;
        }
      }
      throw new Error('L402 payment timed out');
    }

    return result;
  }
}

// Usage
const agent = new SparkProxyAgent(
  process.env.PROXY_URL,
  process.env.PROXY_TOKEN
);

const balance = await agent.getBalance();
console.log('Balance:', balance.balance, 'sats');

const invoice = await agent.createLightningInvoice(1000, 'Test payment');
console.log('Invoice:', invoice.encodedInvoice);

const l402Result = await agent.fetchL402('https://lightningfaucet.com/api/l402/joke');
console.log('Joke:', l402Result.data);
```

## Environment Variables for Agent

```
PROXY_URL=https://your-deployment.vercel.app
PROXY_TOKEN=sbp_your_token_here
```

## Error Handling

All errors return:
```json
{
  "success": false,
  "error": "Error message here"
}
```

Common errors:
- **401 Unauthorized** — Invalid or missing bearer token
- **403 Forbidden** — Token role doesn't permit this operation
- **400 Bad Request** — Missing required parameters
- **429 Too Many Requests** — Daily budget exceeded
- **500 Internal Server Error** — Spark SDK or server error

## Spending Limits

The proxy enforces two types of limits:

1. **Global limits** (from env vars):
   - `MAX_TRANSACTION_SATS` — per-transaction cap
   - `DAILY_BUDGET_SATS` — daily total cap (resets midnight UTC)

2. **Per-token limits** (set when creating token):
   - `maxTxSats` — per-transaction cap for this token
   - `dailyBudgetSats` — daily cap for this token

The lower of global and per-token limits applies.

## Security Notes

1. **Treat bearer tokens like passwords** — they grant wallet access up to their role
2. **Use the most restrictive role possible** — if an agent only creates invoices, use `invoice` role
3. **Set per-token spending limits** — don't rely solely on global limits
4. **Monitor logs** — check `/api/logs` for unexpected activity
5. **Revoke compromised tokens immediately** — no need to move funds

## Resources

- Proxy repo: https://github.com/echennells/sparkbtcbot-proxy
- Direct SDK skill: https://github.com/echennells/sparkbtcbot-skill
- Spark docs: https://docs.spark.money
- L402 spec: https://docs.lightning.engineering/the-lightning-network/l402
