---
name: x402
version: "1.5.0"
description: x402 open payment standard for HTTP-native crypto payments. Use for API monetization, AI agent payments, micropayments, and integrating USDC payments into web services using HTTP 402 status code.
---

# x402 Payment Protocol Skill

The open payment standard that enables services to charge for access to their APIs and content directly over HTTP using the `402 Payment Required` status code. Developed by Coinbase as an open standard and backed by the x402 Foundation (co-founded with Cloudflare), x402 enables crypto-native payments without accounts or traditional payment processors.

## Protocol Overview

x402 activates the long-reserved HTTP 402 "Payment Required" status code for programmatic cryptocurrency transactions. Key characteristics:

- **Zero Protocol Fees**: Only nominal blockchain network fees
- **HTTP-Native**: Built into existing HTTP request/response cycle
- **Instant Settlement**: Stablecoin payments settle in seconds
- **Stateless**: No sessions, accounts, or credentials required
- **Wallet-Based Identity**: Crypto wallet address serves as identity
- **AI-Ready**: Designed for machine-to-machine autonomous payments

**Ecosystem Partners**: AWS, Anthropic, Circle, NEAR, Cloudflare

**Current Scale** (as of 2025):
- 75M+ transactions processed
- $24M+ payment volume
- 94K+ buyers
- 22K+ sellers

## When to Use This Skill

This skill should be triggered when:
- Implementing paid APIs with cryptocurrency payments
- Building AI agent payment capabilities (autonomous payments)
- Setting up micropayment systems for web services
- Integrating USDC payments into HTTP APIs
- Working with HTTP 402 Payment Required responses
- Building MCP servers with payment handling
- Discovering or registering services on the x402 Bazaar
- Creating machine-to-machine payment workflows
- Monetizing APIs without traditional payment processors
- Building Cloudflare Workers with x402 payments
- Implementing deferred payment schemes
- Installing Coinbase Payments MCP for AI agents (Claude, Gemini, Codex)
- Using x402-mcp for Vercel AI SDK integration

## Quick Reference

### Installation

**Comprehensive TypeScript/JavaScript:**
```bash
# Full installation (all packages)
npm install @x402/core @x402/evm @x402/svm @x402/axios @x402/fetch \
  @x402/express @x402/hono @x402/next @x402/paywall @x402/extensions
```

**Seller (Node.js):**
```bash
# Express
npm install @x402/express @x402/core @x402/evm

# Next.js
npm install @x402/next @x402/core @x402/evm

# Hono (Cloudflare Workers)
npm install @x402/hono @x402/core @x402/evm
```

**Buyer (Node.js):**
```bash
# Minimal Fetch client
npm install @x402/core @x402/evm @x402/svm @x402/fetch

# Axios client
npm install @x402/core @x402/evm @x402/axios
```

**Cloudflare Agents SDK:**
```bash
# For Cloudflare Workers with x402 support
npm install @cloudflare/agents
```

**Go:**
```bash
go get github.com/coinbase/x402/go
```

**Python:**
```bash
pip install x402
```

**Payments MCP (AI Agents):**
```bash
# Interactive installation
npx @coinbase/payments-mcp

# Auto-configure for specific client
npx @coinbase/payments-mcp --client claude --auto-config
npx @coinbase/payments-mcp --client claude-code --auto-config
npx @coinbase/payments-mcp --client codex --auto-config
npx @coinbase/payments-mcp --client gemini --auto-config
```

**x402-mcp (Vercel AI SDK):**
```bash
npm install x402-mcp
```

### Package Reference

| Package | Purpose |
|---------|---------|
| `@x402/core` | Core protocol types and utilities |
| `@x402/evm` | Ethereum/Base chain support (EIP-3009) |
| `@x402/svm` | Solana chain support |
| `@x402/fetch` | Fetch API wrapper with payment |
| `@x402/axios` | Axios wrapper with payment |
| `@x402/express` | Express.js middleware |
| `@x402/hono` | Hono framework middleware |
| `@x402/next` | Next.js integration |
| `@x402/paywall` | Paywall utilities |
| `@x402/extensions` | Additional protocol extensions |
| `@coinbase/payments-mcp` | AI agent payments for Claude, Gemini, Codex |
| `x402-mcp` | Vercel AI SDK MCP integration |

### Network Identifiers (CAIP-2)

| Network | Identifier |
|---------|------------|
| Base Mainnet | `eip155:8453` |
| Base Sepolia (Testnet) | `eip155:84532` |
| Solana Mainnet | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` |
| Solana Devnet | `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` |

### Facilitator URLs

| Environment | URL |
|-------------|-----|
| Testnet | `https://x402.org/facilitator` |
| Mainnet (CDP) | `https://api.cdp.coinbase.com/platform/v2/x402` |

### Payment Flow

```
┌────────┐                    ┌────────┐                    ┌─────────────┐
│ Client │                    │ Server │                    │ Facilitator │
└────┬───┘                    └────┬───┘                    └──────┬──────┘
     │                             │                               │
     │  1. GET /paid-resource      │                               │
     │─────────────────────────────>                               │
     │                             │                               │
     │  2. 402 Payment Required    │                               │
     │    PAYMENT-REQUIRED: {...}  │                               │
     │<─────────────────────────────                               │
     │                             │                               │
     │  3. Sign payment payload    │                               │
     │  (wallet signature)         │                               │
     │                             │                               │
     │  4. GET /paid-resource      │                               │
     │    PAYMENT-SIGNATURE: {...} │                               │
     │─────────────────────────────>                               │
     │                             │                               │
     │                             │  5. POST /verify              │
     │                             │─────────────────────────────────>
     │                             │                               │
     │                             │  6. Verification result       │
     │                             │<─────────────────────────────────
     │                             │                               │
     │                             │  7. POST /settle              │
     │                             │─────────────────────────────────>
     │                             │                               │
     │                             │  8. Settlement confirmation   │
     │                             │<─────────────────────────────────
     │                             │                               │
     │  9. 200 OK + Resource       │                               │
     │    PAYMENT-RESPONSE: {...}  │                               │
     │<─────────────────────────────                               │
     │                             │                               │
```

**Simplified Flow:**
1. Client → Server: HTTP request for paid resource
2. Server → Client: 402 Payment Required + PAYMENT-REQUIRED header
3. Client: Signs payment payload with crypto wallet (EIP-3009 for EVM)
4. Client → Server: Retry with PAYMENT-SIGNATURE header
5. Server → Facilitator: Verify and settle payment on blockchain
6. Server → Client: 200 OK + resource + PAYMENT-RESPONSE header

### Seller Setup (Express Example)

```typescript
import express from "express";
import { paymentMiddleware } from "@x402/express";
import { x402Server } from "@x402/core/server";
import { registerExactEvmScheme } from "@x402/evm/exact/server";

const app = express();
const server = new x402Server();
registerExactEvmScheme(server);

app.use(paymentMiddleware(server, {
  facilitatorUrl: "https://x402.org/facilitator",
  routes: {
    "/api/paid-endpoint": {
      price: "$0.01",  // USD price
      network: "eip155:84532",  // Base Sepolia
      recipient: "0xYourWalletAddress"
    }
  }
}));

app.get("/api/paid-endpoint", (req, res) => {
  res.json({ data: "Premium content" });
});
```

### Buyer Setup (Fetch Example)

```typescript
import { wrapFetchWithPayment } from "@x402/fetch";
import { x402Client } from "@x402/core/client";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

// Create wallet signer
const signer = privateKeyToAccount(process.env.EVM_PRIVATE_KEY as `0x${string}`);

// Setup x402 client
const client = new x402Client();
registerExactEvmScheme(client, { signer });

// Wrap fetch with payment handling
const fetchWithPayment = wrapFetchWithPayment(fetch, client);

// Make paid request (handles 402 automatically)
const response = await fetchWithPayment("https://api.example.com/paid-endpoint");
const data = await response.json();
```

### Multi-Network Support

```typescript
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { registerExactSvmScheme } from "@x402/svm/exact/client";

const client = new x402Client();
registerExactEvmScheme(client, { signer: evmSigner });
registerExactSvmScheme(client, { signer: svmSigner });
```

### HTTP Headers

| Header | Direction | Purpose |
|--------|-----------|---------|
| `PAYMENT-REQUIRED` | Server → Client | Payment requirements (Base64 JSON) |
| `PAYMENT-SIGNATURE` | Client → Server | Signed payment payload (Base64 JSON) |
| `PAYMENT-RESPONSE` | Server → Client | Settlement confirmation (Base64 JSON) |

### PAYMENT-REQUIRED Header Schema

```json
{
  "x402Version": 2,
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "maxAmountRequired": "10000",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "recipient": "0x...",
      "extra": {
        "name": "USDC",
        "decimals": 6
      }
    }
  ],
  "timeout": 300,
  "description": "Access to premium API",
  "mimeType": "application/json"
}
```

### PAYMENT-SIGNATURE Header Schema

```json
{
  "x402Version": 2,
  "scheme": "exact",
  "network": "eip155:8453",
  "payload": {
    "signature": "0x...",
    "authorization": {
      "from": "0xBuyerWallet",
      "to": "0xSellerWallet",
      "value": "10000",
      "validAfter": 0,
      "validBefore": 1700000000,
      "nonce": "0x..."
    }
  }
}
```

### PAYMENT-RESPONSE Header Schema

```json
{
  "x402Version": 2,
  "scheme": "exact",
  "network": "eip155:8453",
  "transactionHash": "0x...",
  "settlementTimestamp": 1700000000,
  "status": "settled"
}
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **seller-integration.md** - Complete seller/server setup guide
- **buyer-integration.md** - Complete buyer/client setup guide
- **protocol-spec.md** - HTTP 402 protocol specification
- **facilitator.md** - Facilitator API and settlement
- **bazaar.md** - Service discovery layer
- **mcp-integration.md** - MCP server with x402 payments
- **ai-agents.md** - AI agent integration patterns
- **deferred-payments.md** - Cloudflare deferred payment scheme
- **cloudflare-agents.md** - Cloudflare Agents SDK with withX402 and paidTool
- **github-repo.md** - Official Coinbase x402 repository structure and examples
- **cdp-documentation.md** - CDP facilitator API, Bazaar discovery, and SDK integration
- **payments-mcp.md** - Coinbase Payments MCP for AI agents and x402-mcp integration

## Key Concepts

### What is x402?

x402 activates the previously reserved HTTP `402 Payment Required` status code for API-native cryptocurrency payments. It enables:

- **Frictionless Payments**: No accounts, no session tokens, just wallets
- **Machine-to-Machine**: AI agents can pay for APIs programmatically
- **Micropayments**: Sub-cent transactions without payment processor fees
- **Stateless**: Each request is independent; no persistent credentials
- **Open Standard**: Vendor-agnostic, works with any facilitator
- **Chain-Agnostic**: Extensible to any blockchain network

### Architecture Roles

**Client (Buyer)**: Initiates requests, signs payments with crypto wallet
**Server (Seller)**: Enforces payment requirements, delivers resources
**Facilitator**: Verifies payments, handles blockchain settlement (optional but recommended)

### Supported Tokens & Networks

| Asset | Network | Contract Address |
|-------|---------|------------------|
| USDC | Base Mainnet | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| USDC | Base Sepolia | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |
| USDC | Solana Mainnet | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |

**Fee Structure**: CDP facilitator offers zero-fee USDC settlement on Base

### Payment Schemes

**exact (Primary)**:
- Uses EIP-3009 `transferWithAuthorization` for EVM chains
- Gasless for payers (gas sponsored by facilitator)
- Signature authorizes specific transfer amount and recipient
- Uses SPL Token transfers on Solana

**deferred (Cloudflare Proposal)**:
- Delayed settlement for dispute handling
- Aggregated payments for efficiency
- HTTP Message Signatures for verification
- Supports traditional payment rails

**escrow (Proposed)**:
- Pre-funded usage-based payments
- For APIs where cost is unknown upfront (LLM tokens, compute)
- Lock funds, consume as needed, refund remainder

### CDP Facilitator API

The Coinbase Developer Platform (CDP) hosts the primary x402 facilitator with fee-free USDC settlement.

**Base URL:** `https://api.cdp.coinbase.com/platform/v2/x402`

**Endpoints:**

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/verify` | POST | Required | Verify payment payload (~100ms) |
| `/settle` | POST | Required | Submit to blockchain (~2s on Base) |
| `/discovery/resources` | GET | Optional | Query x402 Bazaar |

**Verify Request:**
```json
{
  "x402Version": 1,
  "paymentPayload": {
    "scheme": "exact",
    "network": "eip155:8453",
    "payload": { /* signed authorization */ }
  },
  "paymentRequirements": {
    "scheme": "exact",
    "network": "eip155:8453",
    "payTo": "0xRecipient",
    "maxAmountRequired": "1000000",
    "resource": "/api/endpoint"
  }
}
```

**Verify Response:**
```json
{ "isValid": true, "invalidReason": null }
```

**Settle Response:**
```json
{ "success": true, "txID": "0x1234..." }
```

**Bazaar Discovery:**
```bash
curl "https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources?limit=10"
```

**Authentication:**
```bash
# Environment variables for CDP API
CDP_API_KEY_ID=your_key_id
CDP_API_KEY_SECRET=your_key_secret
```

### Multi-Network Configuration

Support multiple blockchains on the same endpoint:

```typescript
app.use(paymentMiddleware(server, {
  facilitatorUrl: "https://api.cdp.coinbase.com/platform/v2/x402",
  routes: {
    "GET /weather": {
      accepts: [
        {
          scheme: "exact",
          price: "$0.001",
          network: "eip155:8453",       // Base mainnet (EVM)
          payTo: "0xYourEvmAddress",
        },
        {
          scheme: "exact",
          price: "$0.001",
          network: "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",  // Solana mainnet
          payTo: "YourSolanaAddress",
        },
      ],
      description: "Weather data",
    },
  },
}));
```

### Server-Side Scheme Registration

```typescript
import { x402ResourceServer, FacilitatorClient } from "@x402/core";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { ExactSvmScheme } from "@x402/svm/exact/server";

const facilitatorClient = new FacilitatorClient(FACILITATOR_URL);
const resourceServer = new x402ResourceServer(facilitatorClient)
  .register("eip155:*", new ExactEvmScheme())   // All EVM chains
  .register("solana:*", new ExactSvmScheme());  // All Solana chains
```

## Common Patterns

### Enable Bazaar Discovery

```typescript
app.use(paymentMiddleware(server, {
  facilitatorUrl: "https://api.cdp.coinbase.com/platform/v2/x402",
  routes: {
    "/api/weather": {
      price: "$0.001",
      network: "eip155:8453",
      recipient: "0xYourWallet",
      extensions: {
        bazaar: {
          discoverable: true,
          category: "weather",
          tags: ["forecast", "api"]
        }
      }
    }
  }
}));
```

### Query Bazaar for Services

```typescript
const response = await fetch(
  "https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources"
);
const services = await response.json();
```

### Go Seller Implementation

```go
import (
    "github.com/coinbase/x402/go/pkg/x402"
    "github.com/coinbase/x402/go/pkg/middleware"
)

server := x402.NewServer()
evmscheme.RegisterExactEvmScheme(server)

config := middleware.Config{
    FacilitatorURL: "https://x402.org/facilitator",
    Routes: map[string]middleware.RouteConfig{
        "/api/data": {
            Price:     "0.01",
            Network:   "eip155:84532",
            Recipient: "0xYourWallet",
        },
    },
}

handler := middleware.PaymentMiddleware(server, config)(yourHandler)
```

### Go Buyer Implementation

```go
import (
    "github.com/coinbase/x402/go/pkg/x402"
    evmsigners "github.com/coinbase/x402/go/pkg/evm/signers"
)

signer, _ := evmsigners.NewClientSignerFromPrivateKey(os.Getenv("EVM_PRIVATE_KEY"))
client := x402.NewClient()
evmscheme.RegisterExactEvmScheme(client, signer)

httpClient := x402http.WrapHTTPClientWithPayment(http.DefaultClient, client)
resp, _ := httpClient.Get("https://api.example.com/paid-endpoint")
```

## Cloudflare Agents SDK Integration

Cloudflare has embedded x402 directly into its Agents SDK and MCP infrastructure, enabling AI agents to pay per use for data access, tool execution, or inference APIs.

### withX402 Server Wrapper

Transform any MCP server to support paid tools:

```typescript
import { McpServer } from "@cloudflare/agents";
import { withX402 } from "@cloudflare/agents/x402";
import { z } from "zod";

const X402_CONFIG = {
  network: "base-sepolia",
  recipient: "0xYourWalletAddress",
  facilitatorUrl: "https://x402.org/facilitator"
};

// Wrap MCP server with x402 payment support
const server = withX402(
  new McpServer({ name: "PaidMCP", version: "1.0.0" }),
  X402_CONFIG
);
```

### paidTool() Method

Define tools with USD pricing:

```typescript
// Paid tool - costs $0.01 per call
server.paidTool(
  "square",                    // Tool name
  "Squares a number",          // Description
  0.01,                        // Price in USD
  { number: z.number() },      // Input schema
  {},                          // Options
  async ({ number }) => {
    return {
      content: [{ type: "text", text: String(number ** 2) }]
    };
  }
);

// Free tool in same server
server.tool(
  "greet",
  "Says hello",
  { name: z.string() },
  async ({ name }) => {
    return {
      content: [{ type: "text", text: `Hello, ${name}!` }]
    };
  }
);
```

### withX402Client for Agents

Enable agents to pay for tools:

```typescript
import { withX402Client } from "@cloudflare/agents/x402";
import { privateKeyToAccount } from "viem/accounts";

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);

// With human confirmation callback
const client = withX402Client(mcpClient, {
  account,
  onPaymentRequired: async (paymentInfo) => {
    // Show user the payment amount and get approval
    const approved = await askUserForApproval(paymentInfo);
    return approved;
  }
});

// Or automatic payment (no confirmation)
const autoPayClient = withX402Client(mcpClient, {
  account,
  onPaymentRequired: null  // Pay automatically
});
```

### x402-axios for MCP Tools

Use x402-axios within MCP tool implementations:

```typescript
import { withPaymentInterceptor } from "x402-axios";
import { privateKeyToAccount } from "viem/accounts";
import axios from "axios";

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const client = withPaymentInterceptor(
  axios.create({ baseURL: "https://paid-api.example.com" }),
  account
);

// MCP tool that calls paid external API
server.tool(
  "get-weather-data",
  "Get weather data from the paid API",
  {},
  async () => {
    const res = await client.get("/weather");
    return {
      content: [{ type: "text", text: JSON.stringify(res.data) }]
    };
  }
);
```

### Cloudflare Worker with Paywall

Gate specific endpoints in a Worker:

```typescript
import { paymentMiddleware } from "@x402/hono";
import { Hono } from "hono";

const app = new Hono();

// Apply payment middleware
app.use("/api/premium/*", paymentMiddleware({
  facilitatorUrl: "https://x402.org/facilitator",
  routes: {
    "/api/premium/data": {
      price: "$0.01",
      network: "base-sepolia",
      recipient: "0xYourWallet"
    }
  }
}));

// Free endpoint
app.get("/api/free", (c) => c.json({ message: "Free data" }));

// Paid endpoint (protected by middleware)
app.get("/api/premium/data", (c) => c.json({ data: "Premium content" }));

export default app;
```

## Coinbase Payments MCP

Coinbase's Payments MCP is the easiest way to enable AI agents (Claude, Gemini, Codex) with x402 payment capabilities. It combines wallets, onramps, and payments into a single solution requiring no API keys.

### Installation

```bash
# Interactive setup (prompts for client)
npx @coinbase/payments-mcp

# Auto-configure for Claude Desktop
npx @coinbase/payments-mcp --client claude --auto-config

# Auto-configure for Claude Code
npx @coinbase/payments-mcp --client claude-code --auto-config

# Check status
npx @coinbase/payments-mcp status
```

### Supported Clients

| Client | Auto-Config | Command |
|--------|-------------|---------|
| Claude Desktop | Yes | `--client claude` |
| Claude Code | Yes | `--client claude-code` |
| Codex CLI | Yes | `--client codex` |
| Gemini CLI | Yes | `--client gemini` |
| Cherry Studio | Yes | - |
| Other | Manual | `--client other` |

### Manual Configuration

```json
{
  "mcpServers": {
    "payments-mcp": {
      "command": "node",
      "args": ["/Users/your-home-dir/.payments-mcp/bundle.js"]
    }
  }
}
```

### Features

- **Email-based wallet creation**: No seed phrases or API keys
- **Integrated Bazaar Explorer**: Discover paid services in the UI
- **Spend limits**: Agents have dedicated funds with explicit caps
- **Local execution**: Runs on desktop for security
- **Built-in onramp**: Add funds via Coinbase in supported regions

### Security Model

Agents have isolated wallets with explicit funding limits. No access to your main wallet, and impossible to accumulate unexpected charges.

## x402-mcp (Vercel)

Vercel's `x402-mcp` integrates x402 payments with MCP servers and the AI SDK.

### Creating Paid MCP Tools

```typescript
import { createPaidMcpHandler } from "x402-mcp";
import z from "zod";

const handler = createPaidMcpHandler(
  (server) => {
    server.paidTool(
      "premium_analysis",
      { price: 0.01 },  // $0.01 per call
      { data: z.string() },
      async (args) => {
        const result = await analyzeData(args.data);
        return { content: [{ type: "text", text: result }] };
      }
    );
  },
  { recipient: process.env.WALLET_ADDRESS }
);

export { handler as GET, handler as POST };
```

### Client Integration with AI SDK

```typescript
import { experimental_createMCPClient as createMCPClient } from "ai";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { withPayment } from "x402-mcp";

const mcpClient = await createMCPClient({
  transport: new StreamableHTTPClientTransport(url),
}).then((client) => withPayment(client, { account }));

const tools = await mcpClient.tools();
```

## AI Agent Integration

x402 was designed from the ground up to enable autonomous AI agent payments:

### Agent Payment Flow

```typescript
// AI Agent with x402 payment capability
import { x402Client } from "@x402/core/client";
import { wrapFetchWithPayment } from "@x402/fetch";

async function agentWorkflow(query: string) {
  // 1. Discover relevant services from Bazaar
  const services = await fetch(
    "https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources"
  ).then(r => r.json());

  // 2. Find service matching query
  const service = services.resources.find(s =>
    s.description.toLowerCase().includes(query.toLowerCase())
  );

  // 3. Make paid request (automatic 402 handling)
  const client = new x402Client();
  registerExactEvmScheme(client, { signer });
  const fetchWithPayment = wrapFetchWithPayment(fetch, client);

  return await fetchWithPayment(service.url).then(r => r.json());
}
```

### MCP Server Integration

Claude and other AI assistants can make payments through MCP servers:

```typescript
// Claude Desktop config: ~/.config/claude/claude_desktop_config.json
{
  "mcpServers": {
    "x402-payments": {
      "command": "node",
      "args": ["/path/to/mcp-server/index.js"],
      "env": {
        "EVM_PRIVATE_KEY": "0x...",
        "RESOURCE_SERVER_URL": "https://api.example.com"
      }
    }
  }
}
```

### Spending Limits for Agents

```typescript
const DAILY_LIMIT = 1.00; // $1.00 USD
let dailySpend = 0;

async function makePayment(amount: number) {
  if (dailySpend + amount > DAILY_LIMIT) {
    throw new Error("Daily spending limit exceeded");
  }
  dailySpend += amount;
  // ... proceed with payment
}
```

## Security Considerations

### Replay Protection
- Each payment authorization includes nonce and validity window
- `validAfter` and `validBefore` bounds prevent reuse
- Facilitator tracks used nonces

### Signature Verification
- Cryptographic verification of payer authorization
- Amount must match requirement exactly
- Recipient must match specified address

### Best Practices

1. **Private Key Storage**: Use environment variables or secret managers
2. **Wallet Funding**: Only fund with amounts needed for expected usage
3. **Spending Limits**: Implement daily/monthly caps for AI agents
4. **Audit Logging**: Log all payment transactions
5. **Testnet First**: Always test on Base Sepolia before mainnet

## Error Handling

### Error Codes

| Code | Description |
|------|-------------|
| `INVALID_SIGNATURE` | Payment signature verification failed |
| `INSUFFICIENT_FUNDS` | Payer wallet has insufficient balance |
| `EXPIRED_AUTHORIZATION` | Payment validity window has passed |
| `INVALID_NETWORK` | Unsupported network identifier |
| `INVALID_SCHEME` | Unsupported payment scheme |
| `ALREADY_USED` | Payment authorization already settled |
| `AMOUNT_MISMATCH` | Payment amount doesn't match requirement |
| `RECIPIENT_MISMATCH` | Payment recipient doesn't match requirement |

### Error Handling Example

```typescript
import { X402Error } from "@x402/core";

try {
  const response = await fetchWithPayment(url);
} catch (error) {
  if (error instanceof X402Error) {
    switch (error.code) {
      case 'INSUFFICIENT_FUNDS':
        console.error('Add USDC to wallet on correct network');
        break;
      case 'SCHEME_NOT_REGISTERED':
        console.error('Register payment scheme first');
        break;
      case 'EXPIRED_AUTHORIZATION':
        console.error('Payment timed out, retry with fresh payload');
        break;
      default:
        console.error('Payment error:', error.message);
    }
  }
  throw error;
}
```

## Testing

1. Use testnet facilitator: `https://x402.org/facilitator`
2. Use testnet networks: `eip155:84532` (Base Sepolia)
3. Get testnet USDC from faucets
4. Verify 402 response includes `PAYMENT-REQUIRED` header
5. Verify successful response includes `PAYMENT-RESPONSE` header

## Resources

- [x402 Documentation](https://x402.gitbook.io/x402)
- [GitHub Repository](https://github.com/coinbase/x402)
- [x402.org Landing Page](https://x402.org)
- [x402 Whitepaper (PDF)](https://www.x402.org/x402-whitepaper.pdf)
- [CDP x402 Documentation](https://docs.cdp.coinbase.com/x402/welcome)
- [Cloudflare Agents x402 Docs](https://developers.cloudflare.com/agents/x402/)
- [Cloudflare MCP Documentation](https://developers.cloudflare.com/agents/model-context-protocol/)
- [Vercel Starter Template](https://vercel.com/templates/next.js/x402-starter)
- [CDP Wallet API](https://docs.cdp.coinbase.com)
- [Cloudflare x402 Foundation Announcement](https://blog.cloudflare.com/x402/)
- [Zuplo x402 MCP Tutorial](https://zuplo.com/blog/mcp-api-payments-with-x402)
- [Payments MCP Documentation](https://docs.cdp.coinbase.com/payments-mcp/welcome)
- [Payments MCP GitHub](https://github.com/coinbase/payments-mcp)
- [x402-mcp (Vercel)](https://vercel.com/blog/introducing-x402-mcp-open-protocol-payments-for-mcp-tools)
- [x402 AI Starter Template](https://vercel.com/templates/ai/x402-ai-starter)

## x402 Foundation

The x402 Foundation was established by Coinbase and Cloudflare to promote adoption of the x402 protocol as an open standard for internet-native payments. Goals include:

- Encouraging community contributions to the open-source repository
- Developing governance structures for protocol evolution
- Expanding network and payment scheme support
- Standardizing AI agent payment patterns

## Notes

- x402 was developed by Coinbase as an open standard
- The protocol is vendor-agnostic and works with any facilitator
- Currently supports USDC on Base and Solana networks
- AI agents can use x402 for autonomous payments
- MCP integration enables Claude and other AI assistants to make payments
- Cloudflare proposed deferred payment scheme for aggregated settlement
- Partners include AWS, Anthropic, Circle, NEAR, and Cloudflare
- Payments MCP provides no-code x402 integration for AI agents
- x402 is being included in Google's Agents Payment Protocol (AP2) initiative

## Version History

- **1.5.0** (2026-01-08): Enhanced with Payments MCP documentation
  - Added Coinbase Payments MCP section with installation and configuration
  - Added x402-mcp (Vercel) section for AI SDK integration
  - Added supported MCP clients table (Claude, Codex, Gemini)
  - Added payments-mcp.md comprehensive reference file
  - Added installation commands for Payments MCP and x402-mcp packages
  - Updated package reference table
- **1.4.0** (2026-01-08): Enhanced with CDP documentation
  - Added CDP Facilitator API section with verify/settle/discovery endpoints
  - Added authentication requirements and request/response schemas
  - Added cdp-documentation.md comprehensive reference file
  - Added Bazaar discovery query examples
- **1.3.0** (2026-01-08): Enhanced with GitHub repository details
  - Added comprehensive package reference table
  - Added multi-network configuration examples
  - Added server-side scheme registration patterns
  - Added escrow scheme proposal info
  - Added full installation commands
  - Added github-repo.md reference file
- **1.2.0** (2026-01-08): Enhanced with Cloudflare Agents SDK
  - Added Cloudflare Agents SDK integration section
  - Added withX402 server wrapper documentation
  - Added paidTool() method examples
  - Added withX402Client for agent payments
  - Added x402-axios MCP integration
  - Added Cloudflare Worker paywall example
  - Added cloudflare-agents.md reference file
- **1.1.0** (2026-01-08): Enhanced with whitepaper research
  - Added protocol overview and ecosystem scale metrics
  - Added detailed HTTP header schemas
  - Added AI agent integration patterns
  - Added security considerations and error codes
  - Added x402 Foundation information
  - Added deferred payment scheme documentation
- **1.0.0** (2025-01-07): Initial release
