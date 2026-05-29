---
name: jito-bundles-and-priority-fees
description: Master Jito bundles for MEV protection and priority fee optimization on Solana - bundle submission, tip strategies, and transaction landing. Use for trading bots, high-priority transactions, and MEV-aware applications.
---

# Jito Bundles and Priority Fees

Role framing: You are a Solana transaction optimization specialist who understands Jito infrastructure, priority fees, and MEV dynamics. Your goal is to help applications land transactions reliably and protect against MEV extraction.

## Initial Assessment

- What are you building: trading bot, DEX, NFT mint, or general dApp?
- Transaction volume: occasional high-priority or sustained high-frequency?
- MEV exposure: are your transactions susceptible to front-running or sandwich attacks?
- Budget: what's acceptable tip/fee spend per transaction?
- Latency requirements: how critical is landing in the next slot?
- Do you need atomic bundles (multiple txs that must execute together)?

## Core Principles

- **Priority fees are for congestion, tips are for Jito**: Different mechanisms, different purposes.
- **Bundles are atomic**: All transactions in a bundle execute or none do.
- **Tips go to validators, not network**: Jito tips incentivize block builders to include your bundle.
- **Higher tip ≠ guaranteed inclusion**: You're competing with other bundles; tip relative to value.
- **Bundles can fail silently**: No on-chain record if bundle wasn't included.
- **Not all validators run Jito**: ~80-90% of stake, but some slots won't process bundles.

## Workflow

### 1. Understanding the Landscape

```
Standard Solana Transaction Path:
User → RPC → Leader Validator → Block

Jito Bundle Path:
User → Jito Block Engine → Jito Relayer → Leader Validator → Block

Key difference: Bundles go through Jito's infrastructure,
which sequences them to prevent MEV extraction.
```

Priority fees vs Jito tips:

| Aspect | Priority Fee | Jito Tip |
|--------|--------------|----------|
| Where paid | On-chain, part of tx | Separate tip tx in bundle |
| Who receives | Validator + burn | Validator (via Jito) |
| Guarantees | Higher priority in mempool | Bundle inclusion if won auction |
| Use case | General tx prioritization | MEV protection, atomic execution |

### 2. When to Use What

| Scenario | Recommendation |
|----------|----------------|
| Normal dApp transaction | Priority fee only |
| Trading bot (no MEV concern) | Priority fee, maybe Jito for speed |
| DEX swap (MEV risk) | Jito bundle for protection |
| Arbitrage | Jito bundle (atomic multi-tx) |
| NFT mint (competitive) | Priority fee + Jito bundle |
| Liquidation | Jito bundle (need speed + protection) |

### 3. Priority Fee Implementation

```typescript
import {
  ComputeBudgetProgram,
  Transaction,
  TransactionInstruction,
} from '@solana/web3.js';

// Add priority fee to transaction
function addPriorityFee(
  transaction: Transaction,
  microLamports: number,
  computeUnits: number = 200_000
): Transaction {
  // Set compute unit limit
  const computeLimitIx = ComputeBudgetProgram.setComputeUnitLimit({
    units: computeUnits,
  });

  // Set compute unit price (priority fee)
  const computePriceIx = ComputeBudgetProgram.setComputeUnitPrice({
    microLamports: microLamports, // micro-lamports per compute unit
  });

  // Prepend to transaction
  transaction.instructions = [
    computeLimitIx,
    computePriceIx,
    ...transaction.instructions,
  ];

  return transaction;
}

// Calculate fee in SOL:
// fee = (microLamports * computeUnits) / 1_000_000_000_000
// Example: 10,000 microLamports * 200,000 CU = 0.000002 SOL
```

Priority fee tiers (as of late 2024):

| Network State | Micro-lamports | ~Cost per 200k CU |
|---------------|----------------|-------------------|
| Quiet | 1,000 | 0.0000002 SOL |
| Normal | 10,000 | 0.000002 SOL |
| Busy | 50,000 | 0.00001 SOL |
| Congested | 200,000 | 0.00004 SOL |
| Extreme | 1,000,000+ | 0.0002+ SOL |

### 4. Jito Bundle Implementation

```typescript
import { Connection, Keypair, Transaction, VersionedTransaction } from '@solana/web3.js';

// Jito endpoints
const JITO_ENDPOINTS = {
  mainnet: {
    blockEngine: 'https://mainnet.block-engine.jito.wtf',
    // Regional endpoints for lower latency:
    // ny: 'https://ny.mainnet.block-engine.jito.wtf'
    // amsterdam: 'https://amsterdam.mainnet.block-engine.jito.wtf'
    // frankfurt: 'https://frankfurt.mainnet.block-engine.jito.wtf'
    // tokyo: 'https://tokyo.mainnet.block-engine.jito.wtf'
  },
};

// Jito tip accounts (rotate through these)
const JITO_TIP_ACCOUNTS = [
  '96gYZGLnJYVFmbjzopPSU6QiEV5fGqZNyN9nmNhvrZU5',
  'HFqU5x63VTqvQss8hp11i4wVV8bD44PvwucfZ2bU7gRe',
  'Cw8CFyM9FkoMi7K7Crf6HNQqf4uEMzpKw6QNghXLvLkY',
  'ADaUMid9yfUytqMBgopwjb2DTLSokTSzL1zt6iGPaS49',
  'DfXygSm4jCyNCybVYYK6DwvWqjKee8pbDmJGcLWNDXjh',
  'ADuUkR4vqLUMWXxW9gh6D6L8pMSawimctcNZ5pGwDcEt',
  'DttWaMuVvTiduZRnguLF7jNxTgiMBZ1hyAumKUiL2KRL',
  '3AVi9Tg9Uo68tJfuvoKvqKNWKkC5wPdSSdeBnizKZ6jT',
];

// Create tip instruction
function createTipInstruction(
  fromPubkey: PublicKey,
  tipLamports: number
): TransactionInstruction {
  const tipAccount = new PublicKey(
    JITO_TIP_ACCOUNTS[Math.floor(Math.random() * JITO_TIP_ACCOUNTS.length)]
  );

  return SystemProgram.transfer({
    fromPubkey,
    toPubkey: tipAccount,
    lamports: tipLamports,
  });
}

// Send bundle to Jito
async function sendJitoBundle(
  transactions: (Transaction | VersionedTransaction)[],
  tipLamports: number,
  payer: Keypair
): Promise<string> {
  // Serialize transactions
  const serializedTxs = transactions.map((tx) => {
    if (tx instanceof VersionedTransaction) {
      return Buffer.from(tx.serialize()).toString('base64');
    }
    return Buffer.from(tx.serialize()).toString('base64');
  });

  // Send to Jito block engine
  const response = await fetch(
    `${JITO_ENDPOINTS.mainnet.blockEngine}/api/v1/bundles`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 1,
        method: 'sendBundle',
        params: [serializedTxs],
      }),
    }
  );

  const result = await response.json();

  if (result.error) {
    throw new Error(`Bundle failed: ${result.error.message}`);
  }

  return result.result; // Bundle ID
}

// Check bundle status
async function checkBundleStatus(bundleId: string): Promise<any> {
  const response = await fetch(
    `${JITO_ENDPOINTS.mainnet.blockEngine}/api/v1/bundles`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 1,
        method: 'getBundleStatuses',
        params: [[bundleId]],
      }),
    }
  );

  return response.json();
}
```

### 5. Tip Strategy

```typescript
// Dynamic tip calculation based on expected value
function calculateTip(
  expectedProfitLamports: number,
  urgency: 'low' | 'medium' | 'high' | 'critical'
): number {
  const urgencyMultiplier = {
    low: 0.01,      // 1% of profit
    medium: 0.05,   // 5% of profit
    high: 0.10,     // 10% of profit
    critical: 0.20, // 20% of profit
  };

  const baseTip = expectedProfitLamports * urgencyMultiplier[urgency];

  // Floor and ceiling
  const minTip = 10_000; // 0.00001 SOL
  const maxTip = 100_000_000; // 0.1 SOL

  return Math.max(minTip, Math.min(maxTip, Math.floor(baseTip)));
}

// Typical tip ranges:
// - Simple swap protection: 0.0001 - 0.001 SOL
// - Competitive arb: 0.001 - 0.01 SOL
// - High-value arb: 1-10% of profit
// - NFT mint: 0.01 - 0.1 SOL during peak
```

### 6. Bundle Construction Best Practices

```typescript
// Example: Protected swap with tip
async function protectedSwap(
  swapIx: TransactionInstruction[],
  payer: Keypair,
  connection: Connection
): Promise<string> {
  // Create swap transaction
  const swapTx = new Transaction();
  swapTx.add(...swapIx);

  // Add priority fee for backup
  addPriorityFee(swapTx, 10_000, 400_000);

  // Create tip transaction (separate tx in bundle)
  const tipTx = new Transaction();
  tipTx.add(createTipInstruction(payer.publicKey, 100_000)); // 0.0001 SOL

  // Get recent blockhash
  const { blockhash } = await connection.getLatestBlockhash();
  swapTx.recentBlockhash = blockhash;
  tipTx.recentBlockhash = blockhash;
  swapTx.feePayer = payer.publicKey;
  tipTx.feePayer = payer.publicKey;

  // Sign both
  swapTx.sign(payer);
  tipTx.sign(payer);

  // Bundle: [swap, tip] - tip goes last
  // If swap fails, tip doesn't execute (atomic)
  const bundleId = await sendJitoBundle([swapTx, tipTx], 100_000, payer);

  return bundleId;
}
```

### 7. Monitoring and Retry Logic

```typescript
async function sendBundleWithRetry(
  transactions: Transaction[],
  tipLamports: number,
  payer: Keypair,
  maxRetries: number = 5
): Promise<{ success: boolean; signature?: string; attempts: number }> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const bundleId = await sendJitoBundle(transactions, tipLamports, payer);

      // Wait for result
      await new Promise((r) => setTimeout(r, 500));

      const status = await checkBundleStatus(bundleId);

      if (status.result?.value?.[0]?.confirmation_status === 'confirmed') {
        return {
          success: true,
          signature: status.result.value[0].transactions[0],
          attempts: attempt,
        };
      }

      // Bundle not landed, retry with higher tip
      tipLamports = Math.floor(tipLamports * 1.5);

    } catch (error) {
      console.error(`Attempt ${attempt} failed:`, error);
    }

    // Small delay between retries
    await new Promise((r) => setTimeout(r, 100));
  }

  return { success: false, attempts: maxRetries };
}
```

## Templates / Playbooks

### Fee/Tip Decision Matrix

```typescript
interface FeeStrategy {
  scenario: string;
  priorityFee: number; // micro-lamports
  jitoTip: number; // lamports
  useBundle: boolean;
}

const strategies: FeeStrategy[] = [
  {
    scenario: 'Normal dApp interaction',
    priorityFee: 10_000,
    jitoTip: 0,
    useBundle: false,
  },
  {
    scenario: 'Time-sensitive but not MEV-exposed',
    priorityFee: 50_000,
    jitoTip: 0,
    useBundle: false,
  },
  {
    scenario: 'DEX swap (MEV protection)',
    priorityFee: 10_000,
    jitoTip: 50_000,
    useBundle: true,
  },
  {
    scenario: 'Arbitrage',
    priorityFee: 10_000,
    jitoTip: 'dynamic (% of profit)',
    useBundle: true,
  },
  {
    scenario: 'NFT mint (competitive)',
    priorityFee: 200_000,
    jitoTip: 1_000_000,
    useBundle: true,
  },
  {
    scenario: 'Liquidation',
    priorityFee: 100_000,
    jitoTip: 500_000,
    useBundle: true,
  },
];
```

### RPC + Jito Configuration

```typescript
const infraConfig = {
  // Primary RPC for reads
  rpcRead: process.env.RPC_READ_URL,

  // RPC for non-Jito sends
  rpcSend: process.env.RPC_SEND_URL,

  // Jito for bundles
  jito: {
    blockEngine: process.env.JITO_BLOCK_ENGINE,
    // Use regional endpoint closest to you
    region: 'ny', // ny, amsterdam, frankfurt, tokyo
  },

  // Fallback strategy
  fallback: {
    onJitoFailure: 'retry_with_rpc', // or 'fail_fast'
    maxJitoRetries: 3,
    priorityFeeEscalation: 1.5, // multiply on each retry
  },
};
```

## Common Failure Modes + Debugging

### "Bundle not landing"
- Cause: Tip too low, competing with higher-tipping bundles
- Detection: Bundle status shows "dropped" or no confirmation
- Fix: Increase tip; check current tip floor via Jito API; retry with escalating tips

### "Bundle landed but transaction failed"
- Cause: On-chain error (slippage, insufficient funds, etc.)
- Detection: Transaction shows error on explorer
- Fix: This is application logic issue, not Jito issue. Debug the transaction itself

### "Transaction landed via RPC before bundle"
- Cause: RPC was faster than Jito path
- Detection: Signature exists but bundle shows "dropped"
- Fix: Not a problem if tx succeeded. For MEV protection, ensure you're not sending to RPC simultaneously

### "Bundle simulation failed"
- Cause: Transaction would fail on-chain
- Detection: Jito returns simulation error
- Fix: Fix the transaction before sending; ensure fresh blockhash

### "Rate limited by Jito"
- Cause: Exceeded request limits
- Detection: 429 response
- Fix: Implement backoff; contact Jito for higher limits if needed

## Quality Bar / Validation

Implementation is complete when:
- [ ] Priority fee calculation adapts to network conditions
- [ ] Jito bundles submit successfully with appropriate tips
- [ ] Retry logic handles failures gracefully
- [ ] Tip amounts scale with transaction value/urgency
- [ ] Monitoring tracks bundle landing rates
- [ ] Fallback to RPC exists for non-Jito validators

## Output Format

Provide:
1. **Strategy recommendation**: Use Jito bundles, priority fees, or both
2. **Configuration code**: Priority fee and tip calculations
3. **Bundle construction**: How to structure transactions
4. **Monitoring setup**: How to track success rates
5. **Cost estimate**: Expected fees per transaction type

## Examples

### Simple Example: Add Priority Fee to Swap

**Input**: "Make this swap transaction land faster"

**Output**:
```typescript
import { ComputeBudgetProgram, Transaction } from '@solana/web3.js';

// Your existing swap instruction
const swapIx = /* ... your Jupiter/Raydium swap instruction ... */;

// Create transaction with priority fee
const tx = new Transaction();

// 1. Set compute limit (estimate or use 400k for swaps)
tx.add(
  ComputeBudgetProgram.setComputeUnitLimit({ units: 400_000 })
);

// 2. Set priority fee (50k microlamports = ~0.00002 SOL for 400k CU)
tx.add(
  ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 50_000 })
);

// 3. Add your swap instruction
tx.add(swapIx);

// Total additional cost: ~0.00002 SOL
// Should land within 1-2 slots during normal conditions
```

### Complex Example: MEV-Protected Arbitrage Bundle

**Input**: "Build an arb bot that uses Jito for MEV protection"

**Output**:
```typescript
// See examples/jito-arb-bot.ts for full implementation
// Key components:

class JitoArbBot {
  private jitoClient: JitoClient;
  private minProfitLamports = 50_000; // 0.00005 SOL minimum

  async executeArb(
    buyIx: TransactionInstruction[],
    sellIx: TransactionInstruction[],
    expectedProfitLamports: number
  ): Promise<ArbResult> {
    // Don't execute if profit too low after tip
    const tip = this.calculateTip(expectedProfitLamports);
    const netProfit = expectedProfitLamports - tip;

    if (netProfit < this.minProfitLamports) {
      return { executed: false, reason: 'Profit below threshold after tip' };
    }

    // Build atomic bundle:
    // Tx 1: Buy
    // Tx 2: Sell
    // Tx 3: Tip (only executes if buy+sell succeed)
    const bundle = await this.buildArbBundle(buyIx, sellIx, tip);

    // Send with retry
    const result = await this.sendBundleWithRetry(bundle, tip);

    return {
      executed: result.success,
      signature: result.signature,
      expectedProfit: expectedProfitLamports,
      actualTip: tip,
      netProfit: netProfit,
    };
  }

  private calculateTip(profitLamports: number): number {
    // Dynamic tip: 5% of profit, min 10k lamports, max 1 SOL
    return Math.max(
      10_000,
      Math.min(1_000_000_000, Math.floor(profitLamports * 0.05))
    );
  }
}
```
