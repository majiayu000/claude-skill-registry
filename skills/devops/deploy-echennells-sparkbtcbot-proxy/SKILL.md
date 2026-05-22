---
name: sparkbtcbot-proxy-deploy
description: Deploy a serverless Spark Bitcoin L2 proxy on Vercel with spending limits, auth, and Redis logging. Use when user wants to set up a new proxy, configure env vars, deploy to Vercel, or manage the proxy infrastructure.
argument-hint: "[Optional: setup, deploy, rotate-token, or configure]"
---

# Deploy sparkbtcbot-proxy

You are an expert in deploying and managing the sparkbtcbot-proxy — a serverless middleware that wraps the Spark Bitcoin L2 SDK behind authenticated REST endpoints on Vercel.

## What This Proxy Does

Gives AI agents scoped wallet access without exposing the mnemonic:
- Role-based token auth (`admin` for full access, `invoice` for read + create invoices only)
- Token management via API — create, list, revoke without redeploying
- Per-transaction and daily spending caps
- Activity logging to Redis
- Lazy detection of paid Lightning invoices
- MCP server for Claude Code integration

## What You Need

**Ask the user for these upfront:**

- Vercel account (free Hobby tier works)
- Upstash account email and API key (from https://console.upstash.com/account/api) — OR existing `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` if they already have a database
- BIP39 mnemonic for the Spark wallet (or generate one in step 3)
- Node.js 20+

**Generated during setup (don't ask for these):**

- `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` — created by the Upstash management API in step 2
- `API_AUTH_TOKEN` — generated in step 4

## Step-by-Step Deployment

### 1. Clone and install

```bash
git clone https://github.com/echennells/sparkbtcbot-proxy.git
cd sparkbtcbot-proxy
npm install
```

### 2. Create Upstash Redis

If the user already has `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`, skip to step 3.

Otherwise, create a database via the Upstash API. The user needs their Upstash email and API key from https://console.upstash.com/account/api:

```bash
curl -X POST "https://api.upstash.com/v2/redis/database" \
  -u "UPSTASH_EMAIL:UPSTASH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "sparkbtcbot-proxy", "region": "global", "primary_region": "us-east-1"}'
```

**Note:** Regional database creation is deprecated. You must use `"region": "global"` with a `"primary_region"` field. The Upstash docs may not reflect this yet.

The response includes `rest_url` and `rest_token` — save these for step 5.

### 3. Generate a wallet mnemonic (if needed)

`SparkWallet.initialize()` returns `{ mnemonic, wallet }` when called without a mnemonic. One-liner:

```bash
node -e "import('@buildonspark/spark-sdk').then(({SparkWallet}) => SparkWallet.initialize({mnemonicOrSeed: null, options: {network: 'MAINNET'}}).then(r => { console.log(r.mnemonic); r.wallet.cleanupConnections() }))"
```

Save the 12-word mnemonic securely — it controls all funds in the wallet. There is no `getMnemonic()` method; you can only retrieve the mnemonic at initialization time.

Or use any BIP39 mnemonic generator. 12 or 24 words.

### 4. Generate an API auth token

```bash
openssl rand -base64 30
```

### 5. Deploy to Vercel

```bash
npx vercel --prod
```

When prompted, accept the defaults. Then set environment variables. All 7 are required:

| Variable | Description | Example |
|----------|-------------|---------|
| `SPARK_MNEMONIC` | 12-word BIP39 mnemonic | `fence connect trigger ...` |
| `SPARK_NETWORK` | Spark network | `MAINNET` |
| `API_AUTH_TOKEN` | Admin fallback bearer token | output of step 4 |
| `UPSTASH_REDIS_REST_URL` | Redis REST endpoint | `https://xxx.upstash.io` |
| `UPSTASH_REDIS_REST_TOKEN` | Redis auth token | from step 2 |
| `MAX_TRANSACTION_SATS` | Per-transaction spending cap | `10000` |
| `DAILY_BUDGET_SATS` | Daily spending cap (resets midnight UTC) | `100000` |

**Important:** Do NOT use `vercel env add` with heredoc/`<<<` input — it appends newlines that break the Spark SDK. Either use the Vercel dashboard or the REST API:

```bash
curl -X POST "https://api.vercel.com/v10/projects/<PROJECT_ID>/env?teamId=<TEAM_ID>" \
  -H "Authorization: Bearer <VERCEL_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"type":"encrypted","key":"SPARK_MNEMONIC","value":"your mnemonic here","target":["production","preview","development"]}'
```

Redeploy after setting env vars:

```bash
npx vercel --prod
```

### 6. Test

```bash
curl -H "Authorization: Bearer <your-token>" https://<your-deployment>.vercel.app/api/balance
```

Should return `{"success":true,"data":{"balance":"0","tokenBalances":{}}}`.

### 7. Create scoped tokens (optional)

Use the admin token to create limited tokens for agents:

```bash
curl -X POST -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{"role": "invoice", "label": "my-agent"}' \
  https://<your-deployment>.vercel.app/api/tokens
```

The response includes the full token string — save it, it's only shown once. See the **Token Roles** section below for details.

### 8. Set up MCP server (optional)

For Claude Code or MCP-compatible assistants:

```bash
cd mcp && npm install
claude mcp add spark-wallet \
  -e SPARK_PROXY_URL=https://<your-deployment>.vercel.app \
  -e SPARK_PROXY_TOKEN=<your-token> \
  -- node /path/to/sparkbtcbot-proxy/mcp/index.js
```

If `claude mcp add` runs silently without creating a config, you can create the `.mcp.json` file directly in your project root:

```json
{
  "mcpServers": {
    "spark-wallet": {
      "type": "stdio",
      "command": "node",
      "args": ["/path/to/sparkbtcbot-proxy/mcp/index.js"],
      "env": {
        "SPARK_PROXY_URL": "https://<your-deployment>.vercel.app",
        "SPARK_PROXY_TOKEN": "<your-token>"
      }
    }
  }
}
```

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/balance` | Wallet balance (sats + tokens) |
| GET | `/api/info` | Spark address and identity pubkey |
| GET | `/api/transactions` | Transfer history (`?limit=&offset=`) |
| GET | `/api/deposit-address` | Bitcoin L1 deposit address |
| GET | `/api/fee-estimate` | Lightning send fee estimate (`?invoice=`) |
| GET | `/api/logs` | Recent activity logs (`?limit=`) |
| POST | `/api/invoice/create` | Create Lightning invoice (`{amountSats, memo?, expirySeconds?}`) |
| POST | `/api/invoice/spark` | Create Spark invoice (`{amount?, memo?}`) |
| POST | `/api/pay` | Pay Lightning invoice — admin only (`{invoice, maxFeeSats}`) |
| POST | `/api/transfer` | Spark transfer — admin only (`{receiverSparkAddress, amountSats}`) |
| GET | `/api/tokens` | List API tokens — admin only |
| POST | `/api/tokens` | Create a new token — admin only (`{role, label}`) |
| DELETE | `/api/tokens` | Revoke a token — admin only (`{token}`) |

## Token Roles

There are two token roles:

| Role | Permissions |
|------|------------|
| `admin` | Everything — read, create invoices, pay, transfer, manage tokens |
| `invoice` | Read (balance, info, transactions, logs, fee-estimate, deposit-address) + create invoices. Cannot pay or transfer. |

The `API_AUTH_TOKEN` env var is a hardcoded admin fallback — it always works even if Redis is down or tokens get wiped. Use it to bootstrap: create scoped tokens via the API, then hand those out to agents.

### Managing tokens

Create an invoice-only token for a merchant bot:

```bash
curl -X POST -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{"role": "invoice", "label": "merchant-bot"}' \
  https://<deployment>/api/tokens
```

List all tokens (shows prefixes, labels, roles — not full token strings):

```bash
curl -H "Authorization: Bearer <admin-token>" https://<deployment>/api/tokens
```

Revoke a token:

```bash
curl -X DELETE -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{"token": "<full-token-string>"}' \
  https://<deployment>/api/tokens
```

Tokens are stored in Redis (hash `spark:tokens`). They survive redeploys but not Redis flushes.

## Common Operations

### Rotate the admin fallback token

1. Generate a new token: `openssl rand -base64 30`
2. Update `API_AUTH_TOKEN` in Vercel env vars
3. Redeploy: `npx vercel --prod`
4. Update any MCP configs or agents using the old token

Redis-stored tokens are not affected by this — they continue working.

### Adjust spending limits

Update `MAX_TRANSACTION_SATS` and `DAILY_BUDGET_SATS` in Vercel env vars and redeploy. Budget resets daily at midnight UTC.

### Check logs

```bash
curl -H "Authorization: Bearer <token>" https://<deployment>/api/logs?limit=20
```

## Architecture

- **Vercel serverless functions** — each request spins up, initializes the Spark SDK (~1.5s), handles the request, and shuts down. No always-on process, no billing when idle.
- **Upstash Redis** — stores daily spend counters, activity logs, pending invoice tracking, and API tokens. Accessed over HTTP REST (no persistent connection needed). Free tier is limited to 1 database.
- **Spark SDK** — `@buildonspark/spark-sdk` connects to Spark Signing Operators via gRPC over HTTP/2. Pure JavaScript, no native addons.
- **Lazy invoice check** — on every request, the middleware checks Redis for pending invoices and compares against recent wallet transfers. Expired invoices are cleaned up, paid ones are logged. Max 5 checks per request, wrapped in try/catch so failures never affect the main request.
