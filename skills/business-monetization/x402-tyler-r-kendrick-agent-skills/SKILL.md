---
name: x402
description: |
    Use when implementing the x402 protocol for HTTP-native micropayments. Covers server middleware, client payment flows, facilitator integration, and stablecoin payments for APIs and AI agents.
    USE FOR: API micropayments, monetizing endpoints, stablecoin HTTP payments, automated agent payments for API access
    DO NOT USE FOR: full commerce flows with cart/checkout (use ap2), agent communication (use a2a), tool integration (use mcp)
license: Apache-2.0
metadata:
  displayName: "x402 (HTTP Payment Protocol)"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "x402 Protocol GitHub Repository"
    url: "https://github.com/coinbase/x402"
  - title: "x402 Documentation"
    url: "https://www.x402.org"
---

# x402 — HTTP Payment Protocol

## Overview
x402 is an open payment protocol from Coinbase that revives the HTTP 402 (Payment Required) status code for instant, automatic stablecoin micropayments. It enables APIs and services to be monetized natively over HTTP — no accounts, sessions, or traditional payment processors required. Both human clients and AI agents can pay programmatically.

## How It Works
```
Client                          Server                      Facilitator
  │                               │                             │
  │── GET /weather ──────────────►│                             │
  │◄── 402 Payment Required ─────│                             │
  │    (price, payTo, network)    │                             │
  │                               │                             │
  │── sign payment ──────────────►│                             │
  │   (PAYMENT-SIGNATURE header)  │── verify + settle ────────►│
  │                               │◄── confirmation ────────────│
  │◄── 200 OK (content) ─────────│                             │
```

## Server Middleware

### Express (TypeScript)
```typescript
import { paymentMiddleware, x402ResourceServer } from "@x402/express";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { HTTPFacilitatorClient } from "@x402/core/server";

const resourceServer = new x402ResourceServer(
  new HTTPFacilitatorClient({ url: "https://x402.org/facilitator" })
);
resourceServer.register("eip155:84532", new ExactEvmScheme());

app.use(paymentMiddleware(
  {
    "GET /weather": {
      accepts: {
        scheme: "exact",
        price: "$0.001",
        network: "eip155:84532",
        payTo: "0xYourAddress",
      },
    },
  },
  resourceServer,
));
```

### Flask (Python)
```python
from flask import Flask
from x402.flask.middleware import PaymentMiddleware

app = Flask(__name__)
payment_middleware = PaymentMiddleware(app)

payment_middleware.add(
    path="/weather",
    price="$0.001",
    pay_to_address="0xYourAddress",
    network="base-sepolia",
)

@app.route("/weather")
def get_weather():
    return {"report": {"weather": "sunny", "temperature": 70}}
```

## Client Integration

### TypeScript
```typescript
import { x402Client } from "@x402/core/client";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const client = new x402Client()
  .register("eip155:*", new ExactEvmScheme(privateKeyToAccount(privateKey)));

let response = await fetch(url);
if (response.status === 402) {
  const paymentRequired = decodePaymentRequiredHeader(
    response.headers.get("PAYMENT-REQUIRED")
  );
  const payload = await client.createPaymentPayload(paymentRequired);
  response = await fetch(url, {
    headers: { "PAYMENT-SIGNATURE": encodePaymentSignatureHeader(payload) },
  });
}
```

### Python (httpx)
```python
from eth_account import Account
from x402.clients.httpx import x402HttpxClient

account = Account.from_key(os.getenv("PRIVATE_KEY"))

async with x402HttpxClient(account=account, base_url="https://api.example.com") as client:
    response = await client.get("/protected-endpoint")
```

## HTTP Headers
| Header | Direction | Description |
|--------|-----------|-------------|
| `PAYMENT-REQUIRED` | Response (402) | Payment terms (price, payTo, network, scheme) |
| `PAYMENT-SIGNATURE` | Request (retry) | Signed payment payload |

## Supported Networks
x402 works with fast, low-fee blockchains:
- **Base** (Coinbase L2) — primary network
- **Base Sepolia** — testnet
- **Solana** — supported via Solana scheme
- **Ethereum mainnet** — supported but higher fees

## Best Practices
- Use testnet (Base Sepolia) during development; switch to mainnet for production.
- Set prices in USD strings (`"$0.001"`) — the protocol handles conversion.
- Use the public facilitator (`https://x402.org/facilitator`) for verification and settlement.
- For AI agents, wrap the x402 client in the agent's HTTP layer so payments are automatic.
- Keep per-request prices low (fractions of a cent) for API monetization — x402 is designed for micropayments.
- Add x402 middleware only to routes that need monetization, not globally.
