---
name: wallet-monitoring-bot
description: Build a Solana wallet monitoring bot (inflows/outflows, threshold alerts) with safe rate limits and privacy guardrails. Use for treasury monitoring, whale tracking, or security alerts.
---

# Wallet Monitoring Bot

Role framing: You are a Solana bot builder specializing in on-chain monitoring. Your goal is to build reliable wallet tracking systems that alert on meaningful events while respecting rate limits and privacy.

## Initial Assessment

- What wallets are you monitoring (treasury, whales, specific addresses)?
- What events matter: all transfers, specific tokens, thresholds only, NFT moves?
- Latency requirements: real-time (seconds) or batch (minutes)?
- Alert channels: Discord, Telegram, Slack, custom webhook?
- Data source: Helius webhooks, polling, WebSocket?
- Privacy requirements: public alerts or internal only?
- Budget: free tier limitations or paid indexer?

## Core Principles

- **Webhooks > Polling**: Use Helius/Triton webhooks when possible. Saves rate limits and provides lower latency.
- **Deduplicate by signature**: Every transaction has a unique signature. Use it as idempotency key.
- **Enrich, don't just relay**: Raw tx data is useless. Parse instructions, resolve token names, calculate USD values.
- **Throttle intelligently**: Aggregate small events; immediately alert on large ones.
- **Fail safe**: On error, miss an alert rather than spam duplicates.
- **Respect privacy**: Redact sensitive info for public channels; log full data internally.

## Workflow

### 1. Choose Data Source

```typescript
// Option A: Helius Webhooks (Recommended)
// - Real-time, low latency
// - No rate limit concerns for receiving
// - Requires Helius account

// Option B: Polling with getSignaturesForAddress
// - Works with any RPC
// - Higher latency (poll interval)
// - Rate limit sensitive

// Option C: WebSocket (accountSubscribe)
// - Real-time for account balance changes
// - Doesn't capture full tx details
// - Connection management complexity

const DATA_SOURCES = {
  heliusWebhook: {
    latency: '1-3 seconds',
    rateLimit: 'None (receiving)',
    setup: 'Medium',
    cost: 'Free tier: 10 webhooks, Paid: unlimited',
  },
  polling: {
    latency: 'Poll interval (5-60s typical)',
    rateLimit: 'Subject to RPC limits',
    setup: 'Easy',
    cost: 'RPC costs',
  },
  websocket: {
    latency: 'Sub-second',
    rateLimit: 'Connection limits',
    setup: 'Complex (reconnection logic)',
    cost: 'RPC costs',
  },
};
```

### 2. Setup Helius Webhook

```typescript
// Create webhook via Helius API
async function createHeliusWebhook(
  apiKey: string,
  walletAddresses: string[],
  webhookUrl: string
): Promise<string> {
  const response = await fetch('https://api.helius.xyz/v0/webhooks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      webhookURL: webhookUrl,
      transactionTypes: ['TRANSFER', 'SWAP', 'NFT_SALE'],
      accountAddresses: walletAddresses,
      webhookType: 'enhanced', // Parsed transaction data
      authHeader: 'X-Webhook-Secret: your-secret', // Optional
    }),
  });

  const { webhookID } = await response.json();
  return webhookID;
}

// Webhook payload structure (enhanced mode)
interface HeliusWebhookPayload {
  type: string;
  fee: number;
  feePayer: string;
  signature: string;
  slot: number;
  timestamp: number;
  nativeTransfers: NativeTransfer[];
  tokenTransfers: TokenTransfer[];
  description: string;
  source: string;
}
```

### 3. Polling Implementation (Alternative)

```typescript
import { Connection, PublicKey } from '@solana/web3.js';

class WalletPoller {
  private connection: Connection;
  private lastSignatures: Map<string, string> = new Map();
  private pollInterval: number;

  constructor(rpcUrl: string, pollIntervalMs: number = 10000) {
    this.connection = new Connection(rpcUrl);
    this.pollInterval = pollIntervalMs;
  }

  async startPolling(
    wallets: string[],
    onTransaction: (wallet: string, tx: ParsedTransaction) => void
  ) {
    // Initial fetch to set baseline
    for (const wallet of wallets) {
      const sigs = await this.connection.getSignaturesForAddress(
        new PublicKey(wallet),
        { limit: 1 }
      );
      if (sigs.length > 0) {
        this.lastSignatures.set(wallet, sigs[0].signature);
      }
    }

    // Poll loop
    setInterval(async () => {
      for (const wallet of wallets) {
        try {
          await this.checkWallet(wallet, onTransaction);
        } catch (error) {
          console.error(`Error polling ${wallet}:`, error);
        }
      }
    }, this.pollInterval);
  }

  private async checkWallet(
    wallet: string,
    onTransaction: (wallet: string, tx: ParsedTransaction) => void
  ) {
    const lastSig = this.lastSignatures.get(wallet);

    const sigs = await this.connection.getSignaturesForAddress(
      new PublicKey(wallet),
      {
        until: lastSig,
        limit: 20,
      }
    );

    if (sigs.length === 0) return;

    // Update last seen
    this.lastSignatures.set(wallet, sigs[0].signature);

    // Process new transactions (oldest first)
    for (const sig of sigs.reverse()) {
      const tx = await this.connection.getParsedTransaction(sig.signature, {
        maxSupportedTransactionVersion: 0,
      });

      if (tx) {
        onTransaction(wallet, tx);
      }
    }
  }
}
```

### 4. Transaction Parsing

```typescript
interface ParsedTransfer {
  signature: string;
  timestamp: number;
  type: 'SOL' | 'TOKEN' | 'NFT';
  direction: 'IN' | 'OUT';
  amount: number;
  amountUsd?: number;
  token?: {
    mint: string;
    symbol: string;
    decimals: number;
  };
  from: string;
  to: string;
  fee: number;
}

function parseTransaction(
  watchedWallet: string,
  tx: ParsedTransactionWithMeta
): ParsedTransfer[] {
  const transfers: ParsedTransfer[] = [];

  // Parse native SOL transfers
  const preBalances = tx.meta?.preBalances || [];
  const postBalances = tx.meta?.postBalances || [];
  const accounts = tx.transaction.message.accountKeys;

  for (let i = 0; i < accounts.length; i++) {
    const account = accounts[i].pubkey.toString();
    const change = (postBalances[i] - preBalances[i]) / 1e9;

    if (account === watchedWallet && Math.abs(change) > 0.0001) {
      transfers.push({
        signature: tx.transaction.signatures[0],
        timestamp: tx.blockTime || 0,
        type: 'SOL',
        direction: change > 0 ? 'IN' : 'OUT',
        amount: Math.abs(change),
        from: change < 0 ? watchedWallet : 'unknown',
        to: change > 0 ? watchedWallet : 'unknown',
        fee: tx.meta?.fee || 0,
      });
    }
  }

  // Parse token transfers
  const tokenTransfers = tx.meta?.postTokenBalances || [];
  // ... additional parsing logic

  return transfers;
}
```

### 5. Filtering and Thresholds

```typescript
interface FilterConfig {
  // Amount thresholds (in USD or native units)
  minSolAmount?: number;
  minUsdAmount?: number;

  // Token filters
  tokenWhitelist?: string[]; // Only these tokens
  tokenBlacklist?: string[]; // Ignore these tokens

  // Direction filters
  directions?: ('IN' | 'OUT')[];

  // Aggregation
  aggregateWindow?: number; // ms to aggregate small transfers
  aggregateThreshold?: number; // Below this, aggregate

  // Cooldown
  cooldownPerWallet?: number; // ms between alerts for same wallet
}

class TransferFilter {
  private config: FilterConfig;
  private lastAlert: Map<string, number> = new Map();
  private pendingAggregates: Map<string, ParsedTransfer[]> = new Map();

  constructor(config: FilterConfig) {
    this.config = config;
  }

  shouldAlert(wallet: string, transfer: ParsedTransfer): boolean {
    // Check cooldown
    const lastTime = this.lastAlert.get(wallet) || 0;
    if (Date.now() - lastTime < (this.config.cooldownPerWallet || 0)) {
      return false;
    }

    // Check direction
    if (this.config.directions && !this.config.directions.includes(transfer.direction)) {
      return false;
    }

    // Check token filters
    if (transfer.token) {
      if (this.config.tokenWhitelist &&
          !this.config.tokenWhitelist.includes(transfer.token.mint)) {
        return false;
      }
      if (this.config.tokenBlacklist?.includes(transfer.token.mint)) {
        return false;
      }
    }

    // Check amount thresholds
    if (transfer.type === 'SOL' && this.config.minSolAmount &&
        transfer.amount < this.config.minSolAmount) {
      return false;
    }
    if (this.config.minUsdAmount && transfer.amountUsd &&
        transfer.amountUsd < this.config.minUsdAmount) {
      return false;
    }

    return true;
  }
}
```

### 6. Alert Formatting

```typescript
interface AlertMessage {
  title: string;
  description: string;
  fields: { name: string; value: string; inline?: boolean }[];
  color: number;
  url?: string;
}

function formatDiscordAlert(
  wallet: string,
  transfer: ParsedTransfer,
  walletLabel?: string
): AlertMessage {
  const direction = transfer.direction === 'IN' ? '📥 Received' : '📤 Sent';
  const emoji = transfer.direction === 'IN' ? '🟢' : '🔴';

  const amount = transfer.type === 'SOL'
    ? `${transfer.amount.toFixed(4)} SOL`
    : `${transfer.amount.toLocaleString()} ${transfer.token?.symbol || 'tokens'}`;

  const usdValue = transfer.amountUsd
    ? ` (~$${transfer.amountUsd.toLocaleString()})`
    : '';

  return {
    title: `${emoji} ${direction}${walletLabel ? ` - ${walletLabel}` : ''}`,
    description: `${amount}${usdValue}`,
    fields: [
      {
        name: 'Wallet',
        value: `\`${wallet.slice(0, 4)}...${wallet.slice(-4)}\``,
        inline: true,
      },
      {
        name: transfer.direction === 'IN' ? 'From' : 'To',
        value: `\`${(transfer.direction === 'IN' ? transfer.from : transfer.to).slice(0, 8)}...\``,
        inline: true,
      },
      {
        name: 'Time',
        value: `<t:${transfer.timestamp}:R>`,
        inline: true,
      },
    ],
    color: transfer.direction === 'IN' ? 0x00ff00 : 0xff6b6b,
    url: `https://solscan.io/tx/${transfer.signature}`,
  };
}

// Send to Discord
async function sendDiscordAlert(
  webhookUrl: string,
  alert: AlertMessage
): Promise<void> {
  await fetch(webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      embeds: [{
        title: alert.title,
        description: alert.description,
        fields: alert.fields,
        color: alert.color,
        url: alert.url,
        timestamp: new Date().toISOString(),
      }],
    }),
  });
}
```

### 7. Deduplication

```typescript
class SignatureDeduplicator {
  private seen: Set<string> = new Set();
  private maxSize: number;
  private cleanupThreshold: number;

  constructor(maxSize: number = 10000) {
    this.maxSize = maxSize;
    this.cleanupThreshold = maxSize * 0.8;
  }

  isDuplicate(signature: string): boolean {
    if (this.seen.has(signature)) {
      return true;
    }

    // Add to seen set
    this.seen.add(signature);

    // Cleanup if too large (simple approach: clear half)
    if (this.seen.size > this.maxSize) {
      const toKeep = Array.from(this.seen).slice(-this.cleanupThreshold);
      this.seen = new Set(toKeep);
    }

    return false;
  }
}

// For persistent deduplication, use Redis
import Redis from 'ioredis';

class RedisDeduplicator {
  private redis: Redis;
  private keyPrefix: string;
  private ttlSeconds: number;

  constructor(redisUrl: string, ttlSeconds: number = 86400) {
    this.redis = new Redis(redisUrl);
    this.keyPrefix = 'tx:seen:';
    this.ttlSeconds = ttlSeconds;
  }

  async isDuplicate(signature: string): Promise<boolean> {
    const key = `${this.keyPrefix}${signature}`;
    const exists = await this.redis.exists(key);

    if (exists) {
      return true;
    }

    await this.redis.setex(key, this.ttlSeconds, '1');
    return false;
  }
}
```

## Templates / Playbooks

### Bot Configuration Template

```typescript
interface BotConfig {
  // Wallets to monitor
  wallets: {
    address: string;
    label: string;
    filters?: FilterConfig;
  }[];

  // Data source
  dataSource: 'helius' | 'polling' | 'websocket';
  heliusApiKey?: string;
  rpcUrl?: string;
  pollIntervalMs?: number;

  // Alerting
  alertChannels: {
    type: 'discord' | 'telegram' | 'slack' | 'webhook';
    url: string;
    minSeverity?: 'info' | 'warning' | 'critical';
  }[];

  // Defaults
  defaultFilters: FilterConfig;

  // Operations
  healthCheckInterval: number;
  metricsEnabled: boolean;
}

const exampleConfig: BotConfig = {
  wallets: [
    {
      address: 'Treasury...xyz',
      label: 'Project Treasury',
      filters: { minUsdAmount: 1000 },
    },
    {
      address: 'Whale...abc',
      label: 'Known Whale',
      filters: { directions: ['OUT'] },
    },
  ],
  dataSource: 'helius',
  heliusApiKey: process.env.HELIUS_API_KEY,
  alertChannels: [
    {
      type: 'discord',
      url: process.env.DISCORD_WEBHOOK,
    },
  ],
  defaultFilters: {
    minSolAmount: 1,
    minUsdAmount: 100,
    cooldownPerWallet: 60000,
  },
  healthCheckInterval: 60000,
  metricsEnabled: true,
};
```

### Alert Severity Matrix

| Event | Threshold | Severity | Alert Behavior |
|-------|-----------|----------|----------------|
| Large SOL out | > 100 SOL | Critical | Immediate, all channels |
| Medium SOL out | 10-100 SOL | Warning | Immediate, primary channel |
| Small SOL out | 1-10 SOL | Info | Batch every 15 min |
| Any SOL in | > 1 SOL | Info | Batch every 15 min |
| Token transfer | > $1000 | Warning | Immediate |
| NFT move | Any | Info | Batch |

## Common Failure Modes + Debugging

### "Duplicate alerts"
- Cause: Retry logic without deduplication
- Detection: Same tx appearing multiple times
- Fix: Implement signature-based idempotency; use Redis for persistence

### "Missing transactions"
- Cause: Poll interval too long, or webhook not receiving
- Detection: Compare with explorer
- Fix: Verify webhook is active; reduce poll interval; add health check

### "Rate limited"
- Cause: Too many RPC calls when polling
- Detection: 429 errors in logs
- Fix: Switch to webhooks; batch requests; add exponential backoff

### "Wrong token amounts"
- Cause: Not accounting for decimals
- Detection: Amounts off by 10^X
- Fix: Fetch mint info for decimals; cache token metadata

### "Bot crashed but no alert"
- Cause: No health monitoring
- Detection: Silent failure
- Fix: Add health check endpoint; alert on missed heartbeat

## Quality Bar / Validation

Implementation is complete when:
- [ ] Webhooks or polling working reliably
- [ ] Deduplication prevents duplicate alerts
- [ ] Filters correctly apply thresholds
- [ ] Alert formatting is clear and includes links
- [ ] Rate limits respected
- [ ] Health monitoring in place
- [ ] Error handling doesn't spam alerts
- [ ] Tested with real transactions on devnet

## Output Format

Provide:
1. **Architecture overview**: Data flow diagram
2. **Configuration**: Wallets, filters, channels
3. **Code**: Core monitoring and alerting logic
4. **Alert examples**: Sample formatted alerts
5. **Operational runbook**: Health checks, debugging steps

## Examples

### Simple Example: Treasury Monitor

**Input**: "Monitor our treasury for any outgoing transfer > 10 SOL"

**Output**:
```typescript
const treasuryMonitor = new WalletMonitor({
  wallets: [{
    address: 'TreasuryAddressHere',
    label: 'Project Treasury',
  }],
  filters: {
    directions: ['OUT'],
    minSolAmount: 10,
  },
  alertChannel: {
    type: 'discord',
    url: process.env.DISCORD_TREASURY_WEBHOOK,
  },
});

// Alert format:
// 🔴 Sent - Project Treasury
// 25.5 SOL (~$2,550)
// Wallet: Trea...xyz
// To: 7xK8...abc
// Time: 2 minutes ago
// [View on Solscan]
```

### Complex Example: Multi-Wallet Whale Tracker

**Input**: "Build a whale tracker that monitors top 10 holders of $TOKEN with different alert rules per whale"

**Output**: See full implementation with:
- Per-wallet custom thresholds
- Cross-wallet correlation (detect if multiple whales moving together)
- Aggregated daily summaries
- Critical alerts for large simultaneous sells
- Integration with price feed for USD conversion
