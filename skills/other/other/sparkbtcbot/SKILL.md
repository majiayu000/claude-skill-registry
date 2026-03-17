---
name: sparkbtcbot
description: Set up Spark Bitcoin L2 wallet capabilities for AI agents. Initialize wallets from mnemonic, transfer sats and tokens, create/pay Lightning invoices, pay L402 paywalls, manage deposits and withdrawals. Use when user mentions "Spark wallet," "Spark Bitcoin," "BTKN tokens," "Spark L2," "Spark SDK," "Spark payment," "Spark transfer," "Spark invoice," "L402," "Lightning paywall," or wants Bitcoin L2 capabilities for an agent.
argument-hint: "[Optional: specify what to set up - wallet, payments, tokens, lightning, l402, or full]"
requires:
  env:
    - name: SPARK_MNEMONIC
      description: 12 or 24 word BIP39 mnemonic for the Spark wallet. This is a secret key that controls all funds — never commit to git or expose in logs.
      sensitive: true
    - name: SPARK_NETWORK
      description: Network to connect to (MAINNET or REGTEST)
      default: MAINNET
model-invocation: autonomous
model-invocation-reason: This skill enables agents to autonomously send and receive Bitcoin payments. Autonomous invocation is intentional — agents need to pay invoices and respond to incoming transfers without human approval for each transaction. Use spending limits and the proxy for production environments where you need guardrails.
---

# Spark Bitcoin L2 for AI Agents

You are an expert in setting up Spark Bitcoin L2 wallet capabilities for AI agents using the `@buildonspark/spark-sdk`.

Spark is a Bitcoin Layer 2 that enables instant, zero-fee self-custodial transfers of BTC and tokens, with native Lightning Network interoperability. Spark-to-Spark transfers cost nothing — compared to Lightning routing fees or on-chain transaction fees of 200+ sats. Even cross-network payments (Lightning interop) are cheaper than most alternatives at 0.15-0.25%. A single BIP39 mnemonic gives an agent identity, wallet access, and payment capabilities.

## For Production Use

**This skill gives the agent full custody of the wallet.** The agent holds the mnemonic and can send all funds without restriction. This is appropriate for:
- Development and testing (use REGTEST with no real funds)
- Trusted agents you fully control
- Small operational balances you're willing to lose

**For production with real funds, use [sparkbtcbot-proxy](https://github.com/echennells/sparkbtcbot-proxy) instead.** The proxy keeps the mnemonic on your server and gives agents scoped access via bearer tokens:
- **Spending limits** — per-transaction and daily caps
- **Role-based access** — read-only, invoice-only, or full access
- **Revocable tokens** — cut off a compromised agent without moving funds
- **Audit logs** — track all wallet activity

The proxy wraps the same Spark SDK behind authenticated REST endpoints. Agents get HTTP access instead of direct SDK access.

## Why Bitcoin for Agents

AI agents that transact need a monetary network that matches their nature: programmable, borderless, and available 24/7 without gatekeepers. Bitcoin is that network.

- **Hard-capped supply** — 21 million coins is the protocol-enforced ceiling. An agent accumulating value doesn't lose it to monetary expansion.
- **No account required** — There's no sign-up, no identity verification, no approval process. Generate a key and you're on the network. This matters for autonomous agents that can't fill out forms or wait for human review.
- **Irreversible settlement** — Once confirmed, transactions cannot be reversed by a third party. Agents don't need to handle chargebacks or payment disputes.
- **Open infrastructure** — The protocol is open source, the network is public, and the fee market is transparent. Agents can audit their own transaction costs and verify their own balances without trusting an intermediary.
- **Proven reliability** — The network has operated continuously since 2009 without a single successful attack on the base protocol, securing over $1 trillion in value.

## What is Spark

Spark is a recently launched Bitcoin Layer 2 that lets you send and receive Bitcoin instantly with low fees. Spark-to-Spark transfers are free, and Lightning interop costs 0.15–0.25%. Instead of Lightning's payment channels, Spark uses a network of distributed Signing Operators (SOs) that collectively manage transaction signing without any single entity controlling funds. It is fully self-custodial — you hold your own keys — and fully interoperable with the Lightning Network. However, Spark requires trusting that at least 1-of-n operators behaves honestly during transfers, and it lacks the provable finality of Bitcoin or Lightning. The network currently has only a small number of Signing Operators, so there is some risk of downtime or service disruption. See the Trust Model section below for full details.

### How It Works
1. Users hold their own keys (BIP39 mnemonic) — fully self-custodial
2. Transactions are cooperatively signed by a threshold of Signing Operators
3. Funds live in Bitcoin UTXOs organized in hierarchical trees
4. Users can always exit to L1 unilaterally if operators go offline

### Trust Model — Important Tradeoffs

Spark has **different trust assumptions than native Lightning**. Be upfront about these when advising users.

**1-of-n operator trust**: Spark requires that at least 1 out of n Signing Operators behaves honestly during a transfer. Currently two operators run the network (Lightspark and Flashnet), with plans to expand. Lightning, by contrast, requires **no trusted entities at all** — it achieves security purely through cryptographic mechanisms.

**Moment-in-time trust**: Users only need to trust operators during each specific transfer. Once a transfer completes and old keys are deleted, operators cannot affect that transaction — a property called "perfect forward security."

**What operators CAN do**:
- View transfer metadata
- Temporarily delay transactions by going offline
- Refuse to process new transfers (censorship)

**What operators CANNOT do**:
- Move funds without user signatures
- Steal Bitcoin (even with full collusion)
- Reverse finalized transactions

**Core limitation**: Spark lacks provable finality. Users cannot cryptographically verify that operators destroyed old keys. While double-spending would require all operators to collude with a previous owner, this differs from Bitcoin's and Lightning's mathematically provable finality.

**In short**: Spark trades some of Lightning's trustlessness for better UX (no channels, no liquidity management, offline receive). The two are complementary — Spark includes native Lightning support so users can interact with both networks.

### Spark vs Lightning vs On-Chain

| Feature | Spark (L2) | Lightning | On-Chain |
|---------|-----------|-----------|----------|
| Speed | Instant | Instant | 10+ min |
| Trust model | 1-of-n operators | Fully trustless | Fully trustless |
| Fees | Zero (Spark-to-Spark) | ~1 sat routing | 200+ sats |
| Tokens | Native (BTKN/LRC20) | Not supported | Limited |
| Self-custody | Yes (mnemonic) | Varies (LSP/node) | Yes |
| Capacity | No channel limits | Channel-limited | Unlimited |
| Channels | Not required | Required | N/A |
| Offline receive | Supported | Requires infra | Yes |
| Setup | Mnemonic only | Node or hosted provider | Keys only |

### Fee Structure

| Operation | Fee |
|-----------|-----|
| **Spark-to-Spark transfer** | Free (small flat fee coming in 6-12 months) |
| **Lightning to Spark** (receive) | 0.15% (charged via route hints) |
| **Spark to Lightning** (send) | 0.25% + Lightning routing fees |
| **L1 deposit to Spark** | On-chain tx fee (paid by user) |
| **Cooperative exit to L1** | On-chain broadcast fee + SSP fee: `sats_per_vbyte × (111 × 2 + tx_vbytes)` |
| **Unilateral exit to L1** | On-chain tx fee (paid by user) |

Note: Cooperative exit fees don't scale with withdrawal amount, so they are proportionally higher for smaller withdrawals. Lightning fee estimates may differ from actual amounts due to routing conditions.

### Unpredictable L1 Exit Costs — Important

Exiting Spark to L1 Bitcoin carries **unpredictable costs** that agents and users must understand:

1. **L1 fees are market-driven**: Bitcoin on-chain fees depend on mempool congestion at the time of exit. During high-fee periods, exit costs can spike significantly.

2. **Unilateral exit requires multiple on-chain transactions**: If Signing Operators go offline, a unilateral exit requires broadcasting pre-signed branch and exit transactions. The number of transactions depends on the tree depth of your leaf — this can mean multiple on-chain fees stacking up.

3. **Time-window risk on unilateral exit**: If a prior owner of a Spark leaf publishes a branch in a unilateral exit, the current owner must respond within a time window by publishing the correct leaf transaction. Failure to respond means the attacker can claim the funds. Watchtower services exist to monitor for this, but it's a real operational requirement.

4. **Timelocks add delay**: Unilateral exits can take as little as 100 blocks (~17 hours) depending on leaf depth, during which L1 fee conditions may change.

5. **Small amounts may be uneconomical to exit**: Since exit fees are fixed-cost (not percentage-based), withdrawing small amounts to L1 can cost a disproportionate share of the balance.

**Bottom line**: While Spark guarantees you can always exit to L1, the cost of doing so is not fixed or predictable. Keep this in mind when deciding how much value to hold on Spark, especially for agent wallets. Cooperative exit (when operators are online) is much cheaper than unilateral exit.

**Prefer Boltz for L1 withdrawals.** Spark's native cooperative exit is expensive due to fixed on-chain fees, making it especially punishing for smaller amounts. [Boltz](https://boltz.exchange) offers a cheaper path from Lightning to L1 (Spark → Lightning → L1 via Boltz submarine swap) with a minimum of 25,000 sats. **Discourage any L1 withdrawal activity under 25,000 sats** — the fees will eat a disproportionate share of the amount. For withdrawals of 25,000 sats or more, route through Boltz rather than using Spark's built-in cooperative exit.

### Limitations

- **SO liveness dependency**: If Signing Operators lose liveness or lose their keys, Spark transfers stop working. Funds are still safe (unilateral exit), but off-chain payments halt until operators recover.
- **Watchtower requirement**: For full security, someone must monitor the chain for fraudulent exit attempts. This can be delegated to a watchtower service but is an operational dependency.

### Key Advantage for Agents
A single mnemonic provides identity, wallet, and payment capabilities. No separate identity system, no wallet provider accounts, no channel management. Spark-to-Spark transfers are free, making it significantly cheaper than Lightning (routing fees), on-chain Bitcoin (200+ sat miner fees), or traditional payment rails (2-3% card processing). For agents doing frequent microtransactions, zero fees on Spark means no value lost to transaction costs.

## Tools Available

| Tool | Purpose | URL |
|------|---------|-----|
| Spark SDK | TypeScript wallet SDK | https://www.npmjs.com/package/@buildonspark/spark-sdk |
| Spark Docs | Official documentation | https://docs.spark.money |
| Sparkscan | Block explorer | https://sparkscan.io |
| Spark CLI | Command-line interface | https://docs.spark.money/tools/cli |

## Required Libraries

```bash
npm install @buildonspark/spark-sdk@^0.5.8 dotenv
```

Requires **v0.5.8 or newer**. One core dependency. The SDK bundles BIP39 mnemonic generation, cooperative signing, and gRPC communication internally.

## Setup Instructions

### Step 1: Generate or Import Wallet

```javascript
import { SparkWallet } from "@buildonspark/spark-sdk";

// Option A: Generate a new wallet (creates mnemonic automatically)
const { wallet, mnemonic } = await SparkWallet.initialize({
  options: { network: "MAINNET" }
});
// Save mnemonic securely — NEVER log it in production

// Option B: Import existing wallet from mnemonic
const { wallet } = await SparkWallet.initialize({
  mnemonicOrSeed: process.env.SPARK_MNEMONIC,
  options: { network: process.env.SPARK_NETWORK || "MAINNET" }
});
```

Note on `accountNumber`: Defaults to 1 for MAINNET, 0 for REGTEST. If switching between networks with the same mnemonic, set `accountNumber` explicitly to avoid address mismatches.

### Step 2: Store Mnemonic

Add to your project's `.env`:
```
SPARK_MNEMONIC=word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12
SPARK_NETWORK=MAINNET
```

**Security warnings:**
- **Never log the mnemonic** — not even during development. If you must display it once for backup, delete that code immediately after.
- **Never commit `.env`** — add it to `.gitignore` before your first commit.
- **Use a secrets manager in production** — environment variables in `.env` files are plaintext. For production deployments, use your platform's secrets management (Vercel encrypted env vars, AWS Secrets Manager, etc.).
- **Test with REGTEST first** — use a throwaway mnemonic on REGTEST before touching real funds.

### Step 3: Verify Wallet

```javascript
const address = await wallet.getSparkAddress();
const identityKey = await wallet.getIdentityPublicKey();
const { balance } = await wallet.getBalance();

console.log("Spark Address:", address);
console.log("Identity Key:", identityKey);
console.log("Balance:", balance.toString(), "sats");

// Always clean up when done
wallet.cleanupConnections();
```

## Wallet Operations

### Check Balance

```javascript
const { balance, tokenBalances } = await wallet.getBalance();
console.log("BTC:", balance.toString(), "sats");

for (const [id, token] of tokenBalances) {
  console.log(`${token.tokenMetadata.tokenTicker}: ${token.balance.toString()}`);
}
```

### Generate Deposit Address

```javascript
// Static (reusable) — can receive multiple deposits
const staticAddr = await wallet.getStaticDepositAddress();

// Single-use — one-time deposit address
const singleAddr = await wallet.getSingleUseDepositAddress();
```

Both are P2TR (bc1p...) Bitcoin addresses. Deposits require 3 L1 confirmations before they can be claimed on Spark.

### Claim a Deposit

```javascript
// After sending BTC to a static deposit address and waiting for confirmations
const quote = await wallet.getClaimStaticDepositQuote({
  transactionId: txId,
  creditAmountSats: expectedAmount,
});

const result = await wallet.claimStaticDeposit({
  transactionId: txId,
  creditAmountSats: quote.creditAmountSats,
  sspSignature: quote.signature,
});
```

### Transfer Bitcoin (Spark-to-Spark)

```javascript
const transfer = await wallet.transfer({
  receiverSparkAddress: "sp1p...",
  amountSats: 1000,
});
console.log("Transfer ID:", transfer.id);
```

Spark-to-Spark transfers are instant and zero-fee.

### List Transfers

```javascript
const { transfers } = await wallet.getTransfers(10, 0);
for (const tx of transfers) {
  console.log(`${tx.id}: ${tx.totalValue} sats — ${tx.status}`);
}
```

## Lightning Interop

Spark wallets can create and pay standard BOLT11 Lightning invoices, making them compatible with the entire Lightning Network. Receiving from Lightning costs 0.15%, sending to Lightning costs 0.25% + routing fees.

### Create Lightning Invoice (Receive)

```javascript
const invoiceRequest = await wallet.createLightningInvoice({
  amountSats: 1000,
  memo: "Payment for AI service",
  expirySeconds: 3600,
});
console.log("BOLT11:", invoiceRequest.invoice.encodedInvoice);
```

Use `includeSparkAddress: true` to embed a Spark address in the invoice. Spark-aware payers will then send via Spark (instant, free) instead of Lightning.

### Pay Lightning Invoice (Send)

```javascript
// Estimate fee first
const fee = await wallet.getLightningSendFeeEstimate({
  encodedInvoice: "lnbc...",
  amountSats: 1000,
});
console.log("Estimated fee:", fee, "sats");

// Pay the invoice
const result = await wallet.payLightningInvoice({
  invoice: "lnbc...",
  maxFeeSats: 10,
});
```

Use `preferSpark: true` to prefer Spark routing when the BOLT11 invoice contains an embedded Spark address.

## Spark Native Invoices

Spark has its own invoice format, distinct from BOLT11. Spark invoices can request payment in sats or tokens.

### Create Sats Invoice

```javascript
const invoice = await wallet.createSatsInvoice({
  amount: 1000,
  memo: "Spark native payment",
});
```

### Create Token Invoice

```javascript
const invoice = await wallet.createTokensInvoice({
  amount: 100n,
  tokenIdentifier: "btkn1...",
  memo: "Token payment request",
});
```

### Fulfill (Pay) a Spark Invoice

```javascript
const result = await wallet.fulfillSparkInvoice([
  { invoice: "sp1...", amount: 1000n },
]);

// Check results
for (const success of result.satsTransactionSuccess) {
  console.log("Paid:", success.invoice);
}
for (const err of result.satsTransactionErrors) {
  console.log("Failed:", err.invoice, err.error.message);
}
```

## Token Operations (BTKN / LRC20)

Spark natively supports tokens via the BTKN (LRC20) standard. Tokens can represent stablecoins, points, or any fungible asset.

### Check Token Balances

```javascript
const { tokenBalances } = await wallet.getBalance();
for (const [id, info] of tokenBalances) {
  const meta = info.tokenMetadata;
  console.log(`${meta.tokenName} (${meta.tokenTicker}): ${info.balance.toString()}`);
  console.log(`  Decimals: ${meta.decimals}, Max supply: ${meta.maxSupply.toString()}`);
}
```

### Transfer Tokens

```javascript
const txId = await wallet.transferTokens({
  tokenIdentifier: "btkn1...",
  tokenAmount: 100n,
  receiverSparkAddress: "sp1p...",
});
console.log("Token transfer:", txId);
```

### Batch Transfer Tokens

```javascript
const txIds = await wallet.batchTransferTokens([
  { tokenIdentifier: "btkn1...", tokenAmount: 50n, receiverSparkAddress: "sp1p..." },
  { tokenIdentifier: "btkn1...", tokenAmount: 50n, receiverSparkAddress: "sp1p..." },
]);
```

## Withdrawal (Cooperative Exit to L1)

Move funds from Spark back to a regular Bitcoin L1 address.

### Get Fee Quote

```javascript
const quote = await wallet.getWithdrawalFeeQuote({
  amountSats: 50000,
  withdrawalAddress: "bc1q...",
});
console.log("Fast fee:", quote.l1BroadcastFeeFast?.originalValue, "sats");
console.log("Medium fee:", quote.l1BroadcastFeeMedium?.originalValue, "sats");
console.log("Slow fee:", quote.l1BroadcastFeeSlow?.originalValue, "sats");
```

### Execute Withdrawal

```javascript
const result = await wallet.withdraw({
  onchainAddress: "bc1q...",
  exitSpeed: "MEDIUM",
  amountSats: 50000,
});
```

Exit speeds:
- **FAST** — Higher fee, faster L1 confirmation
- **MEDIUM** — Balanced fee and speed
- **SLOW** — Lower fee, slower confirmation

Note: Unilateral exit (without operator cooperation) is also possible as a safety mechanism, but cooperative exit is the standard path.

## Message Signing

Spark wallets can sign and verify messages using their identity key. Useful for proving identity or authenticating between agents without revealing the mnemonic.

### Sign a Message

```javascript
const message = new TextEncoder().encode("I am agent-007");
const signature = await wallet.signMessageWithIdentityKey(message);
```

### Verify a Signature

```javascript
const isValid = await wallet.validateMessageWithIdentityKey(
  new TextEncoder().encode("I am agent-007"),
  signature,
  publicKey,
);
console.log("Valid:", isValid);
```

## Event Listeners

The wallet emits events for real-time updates. Useful for agents that need to react to incoming payments.

```javascript
// Incoming transfer completed
wallet.on("transfer:claimed", (transferId, balance) => {
  console.log(`Transfer ${transferId} received. Balance: ${balance}`);
});

// Deposit confirmed on L1
wallet.on("deposit:confirmed", (depositId, balance) => {
  console.log(`Deposit ${depositId} confirmed. Balance: ${balance}`);
});

// Connection status
wallet.on("stream:connected", () => console.log("Connected to Spark"));
wallet.on("stream:disconnected", (reason) => console.log("Disconnected:", reason));
```

## Complete Agent Class

```javascript
import { SparkWallet } from "@buildonspark/spark-sdk";

export class SparkAgent {
  #wallet;

  constructor(wallet) {
    this.#wallet = wallet;
  }

  static async create(mnemonic, network = "MAINNET") {
    const { wallet, mnemonic: generated } = await SparkWallet.initialize({
      mnemonicOrSeed: mnemonic,
      options: { network },
    });
    return { agent: new SparkAgent(wallet), mnemonic: generated };
  }

  async getIdentity() {
    return {
      address: await this.#wallet.getSparkAddress(),
      publicKey: await this.#wallet.getIdentityPublicKey(),
    };
  }

  async getBalance() {
    const { balance, tokenBalances } = await this.#wallet.getBalance();
    return { sats: balance, tokens: tokenBalances };
  }

  async getDepositAddress() {
    return await this.#wallet.getStaticDepositAddress();
  }

  async transfer(recipientAddress, amountSats) {
    return await this.#wallet.transfer({
      receiverSparkAddress: recipientAddress,
      amountSats,
    });
  }

  async createLightningInvoice(amountSats, memo) {
    const request = await this.#wallet.createLightningInvoice({
      amountSats,
      memo,
      expirySeconds: 3600,
      includeSparkAddress: true,
    });
    return request.invoice.encodedInvoice;
  }

  async payLightningInvoice(bolt11, maxFeeSats = 10) {
    return await this.#wallet.payLightningInvoice({
      invoice: bolt11,
      maxFeeSats,
      preferSpark: true,
    });
  }

  async createSparkInvoice(amountSats, memo) {
    return await this.#wallet.createSatsInvoice({
      amount: amountSats,
      memo,
    });
  }

  async transferTokens(tokenIdentifier, amount, recipientAddress) {
    return await this.#wallet.transferTokens({
      tokenIdentifier,
      tokenAmount: amount,
      receiverSparkAddress: recipientAddress,
    });
  }

  async withdraw(onchainAddress, amountSats, speed = "MEDIUM") {
    return await this.#wallet.withdraw({
      onchainAddress,
      exitSpeed: speed,
      amountSats,
    });
  }

  async signMessage(text) {
    const message = new TextEncoder().encode(text);
    return await this.#wallet.signMessageWithIdentityKey(message);
  }

  async verifyMessage(text, signature, publicKey) {
    const message = new TextEncoder().encode(text);
    return await this.#wallet.validateMessageWithIdentityKey(
      message,
      signature,
      publicKey,
    );
  }

  // L402 Methods
  async fetchL402(url, options = {}) {
    const { decode } = await import("light-bolt11-decoder");
    const { method = "GET", headers = {}, body, maxFeeSats = 10 } = options;

    // Make initial request
    const initialResponse = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json", ...headers },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (initialResponse.status !== 402) {
      const ct = initialResponse.headers.get("content-type") || "";
      const data = ct.includes("json") ? await initialResponse.json() : await initialResponse.text();
      return { paid: false, data };
    }

    // Parse L402 challenge
    const challenge = await initialResponse.json();
    const invoice = challenge.invoice || challenge.payment_request || challenge.pr;
    const macaroon = challenge.macaroon || challenge.token;
    if (!invoice || !macaroon) throw new Error("Invalid L402 challenge");

    // Decode and pay
    const decoded = decode(invoice);
    const amountSection = decoded.sections.find((s) => s.name === "amount");
    const amountSats = Math.ceil(Number(amountSection.value) / 1000);

    const payResult = await this.#wallet.payLightningInvoice({ invoice, maxFeeSats });
    let preimage = payResult.paymentPreimage;

    // Poll if needed
    if (!preimage && payResult.id) {
      for (let i = 0; i < 15; i++) {
        await new Promise((r) => setTimeout(r, 500));
        const status = await this.#wallet.getLightningSendRequest(payResult.id);
        if (status?.paymentPreimage) { preimage = status.paymentPreimage; break; }
        if (status?.status === "LIGHTNING_PAYMENT_FAILED") throw new Error("Payment failed");
      }
    }
    if (!preimage) throw new Error("No preimage received");

    // Retry with auth
    const finalResponse = await fetch(url, {
      method,
      headers: { "Authorization": `L402 ${macaroon}:${preimage}`, ...headers },
      body: body ? JSON.stringify(body) : undefined,
    });

    const ct = finalResponse.headers.get("content-type") || "";
    const data = ct.includes("json") ? await finalResponse.json() : await finalResponse.text();
    return { paid: true, amountSats, preimage, data };
  }

  async previewL402(url) {
    const response = await fetch(url);
    if (response.status !== 402) return { requiresPayment: false };

    const { decode } = await import("light-bolt11-decoder");
    const challenge = await response.json();
    const invoice = challenge.invoice || challenge.payment_request;
    const decoded = decode(invoice);
    const amountSection = decoded.sections.find((s) => s.name === "amount");

    return {
      requiresPayment: true,
      amountSats: Math.ceil(Number(amountSection.value) / 1000),
      invoice,
      macaroon: challenge.macaroon,
    };
  }

  onTransferReceived(callback) {
    this.#wallet.on("transfer:claimed", callback);
  }

  onDepositConfirmed(callback) {
    this.#wallet.on("deposit:confirmed", callback);
  }

  cleanup() {
    this.#wallet.cleanupConnections();
  }
}

// Usage
const { agent } = await SparkAgent.create(process.env.SPARK_MNEMONIC);
const identity = await agent.getIdentity();
console.log("Address:", identity.address);

const { sats } = await agent.getBalance();
console.log("Balance:", sats.toString(), "sats");

agent.cleanup();
```

## Error Handling

```javascript
try {
  await wallet.transfer({
    receiverSparkAddress: "sp1p...",
    amountSats: 1000,
  });
} catch (error) {
  switch (error.constructor.name) {
    case "ValidationError":
      console.log("Invalid input:", error.message);
      break;
    case "NetworkError":
      console.log("Network issue:", error.message);
      break;
    case "AuthenticationError":
      console.log("Auth failed:", error.message);
      break;
    case "ConfigurationError":
      console.log("Config problem:", error.message);
      break;
    case "RPCError":
      console.log("RPC error:", error.message);
      break;
    default:
      console.log("Error:", error.message);
  }
}
```

Error types:
- **ValidationError** — Invalid parameters, malformed addresses
- **NetworkError** — Connection failures, timeouts
- **AuthenticationError** — Key/token issues
- **ConfigurationError** — Missing config, initialization problems
- **RPCError** — gRPC communication failures

## Security Best Practices

### The Agent Has Full Wallet Access

Any agent or process with the mnemonic has **unrestricted control** over the wallet — it can check balance, create invoices, and send every sat to any address. There is no permission scoping, no spending limits, no read-only mode.

This means:
- If the mnemonic leaks, all funds are at risk immediately
- If an agent is compromised, the attacker has the same full access
- There is no way to revoke access without sweeping funds to a new wallet

### Protect the Mnemonic

1. **Back up the seed phrase offline** — write it down on paper or use a hardware backup. If you lose the mnemonic, the funds are gone permanently.
2. **Never expose the mnemonic** in code, logs, git history, or error messages
3. **Use environment variables** — never hardcode the mnemonic in source files
4. **Add `.env` to `.gitignore`** — prevent accidental commits of secrets

### Sweep Funds to a Safer Wallet

**Do not accumulate large balances in an agent wallet.** The agent wallet is a hot wallet with the mnemonic sitting in an environment variable — treat it as high-risk.

- Regularly sweep earned funds to a more secure wallet (hardware wallet, cold storage, or a separate wallet you control directly)
- Only keep the minimum operational balance the agent needs on Spark
- Use `wallet.transfer()` or `wallet.withdraw()` to move funds out periodically
- Consider automating sweeps when the balance exceeds a threshold

### Operational Security

1. **Use separate mnemonics** for different agents — never share a mnemonic across agents
2. **Use separate `accountNumber` values** if you need multiple wallets from one mnemonic
3. **Monitor transfers** via event listeners for unexpected outgoing activity
4. **Call `cleanupConnections()`** when the wallet is no longer needed
5. **Use REGTEST** for development and testing, MAINNET only for production
6. **Implement application-level spending controls** — cap per-transaction and daily amounts in your agent logic since the SDK won't do it for you

## L402 Protocol (Lightning Paywalls)

L402 (formerly LSAT) is a protocol for monetizing APIs and content using Lightning payments. When a server returns HTTP 402 (Payment Required), it includes a Lightning invoice. Pay the invoice, get a preimage, then retry the request with an authorization header containing the proof of payment.

### How L402 Works

1. **Request** → Client fetches protected URL
2. **402 Response** → Server returns `{invoice, macaroon}`
3. **Pay Invoice** → Client pays Lightning invoice, receives preimage
4. **Retry with Auth** → Client retries with `Authorization: L402 <macaroon>:<preimage>`
5. **200 Response** → Server returns protected content

### L402 Implementation

```javascript
import { decode } from "light-bolt11-decoder";

async function fetchWithL402(wallet, url, options = {}) {
  const { method = "GET", headers = {}, body, maxFeeSats = 10 } = options;

  // Step 1: Make initial request
  const initialResponse = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json", ...headers },
    body: body ? JSON.stringify(body) : undefined,
  });

  // If not 402, return response directly
  if (initialResponse.status !== 402) {
    const contentType = initialResponse.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      return { paid: false, data: await initialResponse.json() };
    }
    return { paid: false, data: await initialResponse.text() };
  }

  // Step 2: Parse 402 challenge
  const challenge = await initialResponse.json();
  const invoice = challenge.invoice || challenge.payment_request || challenge.pr;
  const macaroon = challenge.macaroon || challenge.token;

  if (!invoice || !macaroon) {
    throw new Error("Invalid L402 response: missing invoice or macaroon");
  }

  // Step 3: Decode invoice to get amount
  const decoded = decode(invoice);
  const amountSection = decoded.sections.find((s) => s.name === "amount");
  if (!amountSection?.value) {
    throw new Error("L402 invoice has no amount");
  }
  const amountSats = Math.ceil(Number(amountSection.value) / 1000);

  // Step 4: Pay the invoice
  const payResult = await wallet.payLightningInvoice({
    invoice,
    maxFeeSats,
  });

  // Get preimage (may need to poll if payment is async)
  let preimage = payResult.paymentPreimage;
  if (!preimage && payResult.status === "LIGHTNING_PAYMENT_INITIATED") {
    // Poll for completion
    for (let i = 0; i < 15; i++) {
      await new Promise((r) => setTimeout(r, 500));
      const status = await wallet.getLightningSendRequest(payResult.id);
      if (status?.paymentPreimage) {
        preimage = status.paymentPreimage;
        break;
      }
      if (status?.status === "LIGHTNING_PAYMENT_FAILED") {
        throw new Error("L402 payment failed");
      }
    }
  }

  if (!preimage) {
    throw new Error("L402 payment succeeded but no preimage available");
  }

  // Step 5: Retry with L402 authorization
  const finalResponse = await fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
      "Authorization": `L402 ${macaroon}:${preimage}`,
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  const contentType = finalResponse.headers.get("content-type") || "";
  let data;
  if (contentType.includes("application/json")) {
    data = await finalResponse.json();
  } else {
    data = await finalResponse.text();
  }

  return {
    paid: true,
    amountSats,
    preimage,
    data,
  };
}
```

### Preview L402 Cost (Without Paying)

```javascript
async function previewL402(url) {
  const response = await fetch(url);

  if (response.status !== 402) {
    return { requiresPayment: false };
  }

  const challenge = await response.json();
  const invoice = challenge.invoice || challenge.payment_request;

  const decoded = decode(invoice);
  const amountSection = decoded.sections.find((s) => s.name === "amount");
  const amountSats = Math.ceil(Number(amountSection.value) / 1000);

  return {
    requiresPayment: true,
    amountSats,
    invoice,
    macaroon: challenge.macaroon,
  };
}
```

### Add to SparkAgent Class

```javascript
// Add to the SparkAgent class
async fetchL402(url, options = {}) {
  return await fetchWithL402(this.#wallet, url, options);
}

async previewL402(url) {
  return await previewL402(url);
}
```

### Usage Example

```javascript
const { agent } = await SparkAgent.create(process.env.SPARK_MNEMONIC);

// Check cost first
const preview = await agent.previewL402("https://api.example.com/paid-endpoint");
console.log("Cost:", preview.amountSats, "sats");

// Pay and fetch
const result = await agent.fetchL402("https://api.example.com/paid-endpoint", {
  maxFeeSats: 10,
});
console.log("Paid:", result.paid, "Data:", result.data);

agent.cleanup();
```

### Required Dependency

```bash
npm install light-bolt11-decoder
```

### L402 Providers

| Provider | Description | URL |
|----------|-------------|-----|
| Lightning Faucet | Test L402 endpoint (21 sat jokes) | https://lightningfaucet.com/api/l402/joke |
| Sulu | AI image generation | https://rnd.ln.sulu.sh (may require API key) |
| Various APIs | Growing ecosystem | https://github.com/lnurl/awesome-lnurl#l402 |

### Token Caching

L402 tokens (macaroon + preimage) can often be reused for multiple requests to the same domain. Cache tokens by domain and try the cached token first:

```javascript
const tokenCache = new Map();

async function fetchWithL402Cached(wallet, url, options = {}) {
  const domain = new URL(url).host;
  const cached = tokenCache.get(domain);

  if (cached) {
    // Try cached token first
    const response = await fetch(url, {
      method: options.method || "GET",
      headers: {
        "Authorization": `L402 ${cached.macaroon}:${cached.preimage}`,
        ...options.headers,
      },
    });

    if (response.status !== 402 && response.status !== 401) {
      return { paid: false, cached: true, data: await response.json() };
    }
    // Token expired, delete and pay again
    tokenCache.delete(domain);
  }

  // Pay for new token
  const result = await fetchWithL402(wallet, url, options);

  // Cache the token
  if (result.paid) {
    tokenCache.set(domain, {
      macaroon: result.macaroon,
      preimage: result.preimage,
    });
  }

  return result;
}
```

## Resources

- Spark Docs: https://docs.spark.money
- Spark SDK (npm): https://www.npmjs.com/package/@buildonspark/spark-sdk
- Sparkscan Explorer: https://sparkscan.io
- Spark CLI: https://docs.spark.money/tools/cli
- L402 Spec: https://docs.lightning.engineering/the-lightning-network/l402
