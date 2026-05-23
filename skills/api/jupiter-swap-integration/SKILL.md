---
name: jupiter-swap-integration
description: Integrate Jupiter aggregator for swaps - API usage, route optimization, slippage handling, and frontend/bot implementation. Use when building swap UIs or trading bots.
---

# Jupiter Swap Integration

Role framing: You are a Jupiter integration specialist who builds swap interfaces and trading bots. Your goal is to implement reliable, efficient swaps with proper error handling and user experience.

## Initial Assessment

- What are you building: frontend swap UI, trading bot, or backend service?
- Volume expectations: casual user swaps or high-frequency trading?
- Token types: mainstream (SOL/USDC) or long-tail memecoins?
- Slippage tolerance requirements: tight (0.5%) or loose (5%+)?
- Do you need advanced features: limit orders, DCA, or just spot swaps?
- What's your RPC setup: public endpoints or dedicated providers?
- Error handling requirements: retry logic, fallback strategies?

## Core Principles

- **Jupiter aggregates, doesn't execute**: It finds best routes across DEXs; you submit the transaction.
- **Slippage is protection, not suggestion**: Set it based on volatility; too tight = failed txs, too loose = bad fills.
- **Priority fees are essential**: Without them, swaps fail during congestion. Budget 0.0001-0.001 SOL.
- **Quote ≠ guaranteed execution**: Prices move; always use `onlyDirectRoutes: false` for better fills.
- **Rate limits exist**: Free tier is 60 req/min; paid tiers scale higher. Cache quotes when possible.
- **Versioned transactions required**: Jupiter returns V0 transactions; ensure your wallet/SDK handles them.

## Workflow

### 1. API Setup and Authentication

```typescript
// Base URLs
const JUPITER_API = 'https://quote-api.jup.ag/v6';
const JUPITER_PRICE_API = 'https://price.jup.ag/v6';

// No API key required for basic usage
// For high volume, contact Jupiter for dedicated endpoints

// Rate limits (free tier):
// - Quote API: 60 requests/minute
// - Price API: 600 requests/minute
```

### 2. Get Quote

```typescript
interface QuoteParams {
  inputMint: string;      // Token to sell
  outputMint: string;     // Token to buy
  amount: string;         // Amount in smallest units (lamports/base units)
  slippageBps: number;    // Slippage in basis points (100 = 1%)
  onlyDirectRoutes?: boolean;  // false = better routes, true = simpler
  asLegacyTransaction?: boolean; // false = versioned tx (recommended)
}

async function getQuote(params: QuoteParams) {
  const url = new URL(`${JUPITER_API}/quote`);
  url.searchParams.set('inputMint', params.inputMint);
  url.searchParams.set('outputMint', params.outputMint);
  url.searchParams.set('amount', params.amount);
  url.searchParams.set('slippageBps', params.slippageBps.toString());

  const response = await fetch(url.toString());
  if (!response.ok) {
    throw new Error(`Quote failed: ${response.status}`);
  }
  return response.json();
}

// Example: Swap 1 SOL to USDC
const quote = await getQuote({
  inputMint: 'So11111111111111111111111111111111111111112', // SOL
  outputMint: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v', // USDC
  amount: '1000000000', // 1 SOL in lamports
  slippageBps: 50, // 0.5%
});

// Quote response includes:
// - inAmount: input amount
// - outAmount: expected output (before slippage)
// - otherAmountThreshold: minimum output (after slippage)
// - routePlan: array of swap steps
// - priceImpactPct: price impact percentage
```

### 3. Build Swap Transaction

```typescript
interface SwapParams {
  quoteResponse: any;
  userPublicKey: string;
  wrapAndUnwrapSol?: boolean;  // true = auto wrap/unwrap SOL
  computeUnitPriceMicroLamports?: number; // priority fee
  dynamicComputeUnitLimit?: boolean; // auto-size compute
}

async function getSwapTransaction(params: SwapParams) {
  const response = await fetch(`${JUPITER_API}/swap`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      quoteResponse: params.quoteResponse,
      userPublicKey: params.userPublicKey,
      wrapAndUnwrapSol: params.wrapAndUnwrapSol ?? true,
      computeUnitPriceMicroLamports: params.computeUnitPriceMicroLamports ?? 1000,
      dynamicComputeUnitLimit: params.dynamicComputeUnitLimit ?? true,
    }),
  });

  const { swapTransaction } = await response.json();
  return swapTransaction; // Base64 encoded versioned transaction
}
```

### 4. Sign and Send Transaction

```typescript
import { VersionedTransaction, Connection } from '@solana/web3.js';

async function executeSwap(
  swapTransaction: string,
  wallet: any, // Wallet adapter
  connection: Connection
) {
  // Decode the transaction
  const txBuffer = Buffer.from(swapTransaction, 'base64');
  const tx = VersionedTransaction.deserialize(txBuffer);

  // Sign with wallet
  const signedTx = await wallet.signTransaction(tx);

  // Send with retry logic
  const signature = await connection.sendTransaction(signedTx, {
    skipPreflight: false,
    maxRetries: 3,
  });

  // Confirm transaction
  const confirmation = await connection.confirmTransaction(signature, 'confirmed');

  if (confirmation.value.err) {
    throw new Error(`Transaction failed: ${JSON.stringify(confirmation.value.err)}`);
  }

  return signature;
}
```

### 5. Slippage Strategy by Token Type

| Token Type | Suggested Slippage | Reasoning |
|------------|-------------------|-----------|
| SOL/USDC | 0.1-0.3% | Deep liquidity, stable |
| Major tokens (JUP, BONK) | 0.5-1% | Good liquidity |
| Mid-cap memecoins | 1-3% | Variable liquidity |
| New/low-cap tokens | 3-10% | Thin liquidity, volatile |
| Pump.fun tokens | 5-15% | Extremely volatile |

### 6. Priority Fee Strategy

```typescript
// Estimate priority fee based on network conditions
async function estimatePriorityFee(connection: Connection): Promise<number> {
  const recentFees = await connection.getRecentPrioritizationFees();

  if (recentFees.length === 0) return 1000; // default 1000 micro-lamports

  // Use 75th percentile for reliability
  const sorted = recentFees.map(f => f.prioritizationFee).sort((a, b) => a - b);
  const p75Index = Math.floor(sorted.length * 0.75);

  return Math.max(sorted[p75Index], 1000);
}

// Priority fee tiers:
// - 1,000 micro-lamports: Normal conditions
// - 10,000 micro-lamports: Moderate congestion
// - 100,000 micro-lamports: High congestion
// - 1,000,000+ micro-lamports: Extreme (minting events, etc.)
```

### 7. Error Handling and Retries

```typescript
async function swapWithRetry(
  params: SwapParams,
  maxRetries: number = 3
): Promise<string> {
  let lastError: Error | null = null;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      // Get fresh quote (prices change)
      const quote = await getQuote(params.quoteParams);

      // Check if price moved too much
      if (quote.priceImpactPct > 5) {
        throw new Error(`Price impact too high: ${quote.priceImpactPct}%`);
      }

      // Get swap transaction
      const swapTx = await getSwapTransaction({
        quoteResponse: quote,
        userPublicKey: params.userPublicKey,
        computeUnitPriceMicroLamports: params.priorityFee * attempt, // Increase fee on retry
      });

      // Execute
      return await executeSwap(swapTx, params.wallet, params.connection);

    } catch (error: any) {
      lastError = error;

      // Don't retry on certain errors
      if (error.message.includes('insufficient funds')) throw error;
      if (error.message.includes('slippage')) throw error;

      // Wait before retry (exponential backoff)
      await new Promise(r => setTimeout(r, 1000 * attempt));
    }
  }

  throw lastError || new Error('Swap failed after retries');
}
```

## Templates / Playbooks

### Frontend Swap Component Structure

```typescript
// State management
interface SwapState {
  inputToken: Token | null;
  outputToken: Token | null;
  inputAmount: string;
  quote: QuoteResponse | null;
  loading: boolean;
  error: string | null;
  txStatus: 'idle' | 'signing' | 'confirming' | 'success' | 'failed';
}

// Component flow:
// 1. User selects tokens → fetch quote
// 2. User enters amount → debounced quote refresh
// 3. Display: output amount, price impact, route
// 4. User clicks swap → sign → send → confirm
// 5. Show success/failure with tx link

// Quote refresh interval: 10-15 seconds (balance freshness vs rate limits)
```

### Bot Swap Configuration

```typescript
interface BotSwapConfig {
  // Execution
  maxSlippageBps: number;
  minPriorityFeeMicroLamports: number;
  maxPriorityFeeMicroLamports: number;
  maxRetries: number;

  // Safety
  maxTradeSize: number; // In USD
  maxPriceImpact: number; // Percentage
  cooldownMs: number; // Between trades

  // Monitoring
  logAllQuotes: boolean;
  alertOnFailure: boolean;
}

const defaultBotConfig: BotSwapConfig = {
  maxSlippageBps: 100,
  minPriorityFeeMicroLamports: 1000,
  maxPriorityFeeMicroLamports: 100000,
  maxRetries: 3,
  maxTradeSize: 1000,
  maxPriceImpact: 3,
  cooldownMs: 1000,
  logAllQuotes: true,
  alertOnFailure: true,
};
```

### Price Impact Thresholds

```typescript
function assessPriceImpact(impactPct: number): {
  level: 'low' | 'medium' | 'high' | 'extreme';
  warning: string | null;
} {
  if (impactPct < 0.5) return { level: 'low', warning: null };
  if (impactPct < 2) return { level: 'medium', warning: 'Moderate price impact' };
  if (impactPct < 5) return { level: 'high', warning: 'High price impact - consider smaller trade' };
  return { level: 'extreme', warning: 'Extreme price impact - trade size too large for liquidity' };
}
```

## Common Failure Modes + Debugging

### "Transaction simulation failed"
- Cause: Stale quote, price moved beyond slippage
- Detection: Error message contains "slippage" or "amount out"
- Fix: Increase slippage or refresh quote before executing

### "Transaction expired"
- Cause: Blockhash expired before confirmation (>60 seconds)
- Detection: Error message contains "blockhash not found"
- Fix: Increase priority fee; use `skipPreflight: false`

### "Insufficient SOL for fees"
- Cause: User doesn't have enough SOL for rent + priority fees
- Detection: Pre-check balance before swap
- Fix: Reserve 0.01 SOL minimum; warn user

### "Rate limited by Jupiter"
- Cause: Exceeded 60 requests/minute
- Detection: 429 status code
- Fix: Implement request queuing; cache quotes; use paid tier

### "Route not found"
- Cause: No liquidity path between tokens
- Detection: Empty routes in quote response
- Fix: Check if token has any liquidity; try with intermediate token (SOL/USDC)

### "Transaction too large"
- Cause: Complex route with many hops
- Detection: Error mentions transaction size
- Fix: Use `onlyDirectRoutes: true` or increase compute budget

## Quality Bar / Validation

Integration is complete when:
- [ ] Quotes fetch reliably with proper error handling
- [ ] Slippage is set appropriately for token type
- [ ] Priority fees adjust to network conditions
- [ ] Failed transactions retry with backoff
- [ ] User sees clear status at each step (loading, signing, confirming)
- [ ] Price impact warnings display for large trades
- [ ] Rate limiting handled gracefully
- [ ] Transaction links provided on success

## Output Format

Provide:
1. **Implementation code**: TypeScript with proper types and error handling
2. **Configuration values**: Slippage, priority fees, timeouts
3. **Error handling strategy**: Which errors to retry, which to surface
4. **UX considerations**: Loading states, confirmations, warnings
5. **Testing checklist**: Scenarios to verify before deployment

## Examples

### Simple Example: Basic Swap Function

**Input**: "Create a function to swap SOL to any token"

**Output**:
```typescript
import { Connection, PublicKey, VersionedTransaction } from '@solana/web3.js';

const JUPITER_API = 'https://quote-api.jup.ag/v6';
const SOL_MINT = 'So11111111111111111111111111111111111111112';

interface SwapSolParams {
  outputMint: string;
  amountLamports: number;
  slippageBps: number;
  userPublicKey: PublicKey;
  signTransaction: (tx: VersionedTransaction) => Promise<VersionedTransaction>;
  connection: Connection;
}

export async function swapSolToToken(params: SwapSolParams): Promise<string> {
  // 1. Get quote
  const quoteUrl = `${JUPITER_API}/quote?inputMint=${SOL_MINT}&outputMint=${params.outputMint}&amount=${params.amountLamports}&slippageBps=${params.slippageBps}`;

  const quoteResponse = await fetch(quoteUrl);
  if (!quoteResponse.ok) throw new Error('Failed to get quote');
  const quote = await quoteResponse.json();

  // 2. Get swap transaction
  const swapResponse = await fetch(`${JUPITER_API}/swap`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      quoteResponse: quote,
      userPublicKey: params.userPublicKey.toBase58(),
      wrapAndUnwrapSol: true,
      computeUnitPriceMicroLamports: 5000, // 0.000005 SOL priority
    }),
  });

  const { swapTransaction } = await swapResponse.json();

  // 3. Sign and send
  const tx = VersionedTransaction.deserialize(Buffer.from(swapTransaction, 'base64'));
  const signedTx = await params.signTransaction(tx);

  const signature = await params.connection.sendTransaction(signedTx);
  await params.connection.confirmTransaction(signature, 'confirmed');

  return signature;
}
```

### Complex Example: Production Swap Service

**Input**: "Build a swap service with retries, rate limiting, and monitoring"

**Output**:
```typescript
// See full implementation in examples/swap-service.ts
// Key features:
// - Request queue with rate limiting (60/min)
// - Exponential backoff on failures
// - Priority fee escalation on retries
// - Quote caching (10s TTL)
// - Prometheus metrics export
// - Structured logging
// - Health check endpoint

class JupiterSwapService {
  private requestQueue: RequestQueue;
  private quoteCache: LRUCache<string, Quote>;
  private metrics: SwapMetrics;

  async swap(params: SwapParams): Promise<SwapResult> {
    const startTime = Date.now();

    try {
      // Check rate limit
      await this.requestQueue.acquire();

      // Get or refresh quote
      const quote = await this.getQuoteWithCache(params);

      // Validate
      this.validateQuote(quote, params);

      // Execute with retries
      const signature = await this.executeWithRetry(quote, params);

      // Record success
      this.metrics.recordSwap('success', Date.now() - startTime);

      return { success: true, signature, quote };

    } catch (error) {
      this.metrics.recordSwap('failure', Date.now() - startTime);
      throw error;
    }
  }
}
```
