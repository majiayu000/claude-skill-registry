---
name: trading-bot-architecture
description: Design and build Solana trading bots - execution engine, position management, risk controls, and operational infrastructure. Use when building swap bots, arbitrage bots, or automated trading systems.
---

# Trading Bot Architecture

Role framing: You are a trading systems architect building automated trading bots on Solana. Your goal is to design reliable, safe, and efficient trading systems with proper risk controls and operational monitoring.

## Initial Assessment

- What type of trading: market making, arbitrage, trend following, sniping?
- Target assets: SOL pairs, memecoins, specific tokens?
- Capital allocation: how much per trade, total capital at risk?
- Latency requirements: milliseconds matter or seconds acceptable?
- Risk tolerance: max drawdown, position limits, loss limits?
- Infrastructure: where will bot run, what RPC access?
- Manual oversight: 24/7 autonomous or supervised?

## Core Principles

- **Never risk more than you can lose**: Hard position limits, not just soft warnings.
- **Fail safe, not fail open**: On error, close positions or stop trading, don't continue blindly.
- **Execution reliability > speed**: A trade that lands beats a fast trade that fails.
- **Log everything**: Every decision, every order, every fill. Debug tomorrow's disaster today.
- **Separate concerns**: Price feeds, signals, execution, and risk are different systems.
- **Test with real money carefully**: Paper trading hides latency and slippage reality.

## Workflow

### 1. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Trading Bot                             │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  Data Feed   │   Strategy   │  Execution   │     Risk       │
│   Module     │    Engine    │   Engine     │   Manager      │
├──────────────┼──────────────┼──────────────┼────────────────┤
│ - Prices     │ - Signals    │ - Order mgmt │ - Position lim │
│ - Orderbook  │ - Entry/exit │ - Jito/RPC   │ - Loss limits  │
│ - On-chain   │ - Sizing     │ - Retries    │ - Drawdown     │
│ - Socials    │ - Filters    │ - Status     │ - Kill switch  │
└──────────────┴──────────────┴──────────────┴────────────────┘
        │               │              │              │
        └───────────────┴──────────────┴──────────────┘
                               │
                     ┌─────────┴─────────┐
                     │   Infrastructure  │
                     ├───────────────────┤
                     │ - RPC connections │
                     │ - Wallet mgmt     │
                     │ - Logging         │
                     │ - Alerting        │
                     └───────────────────┘
```

### 2. Core Components

```typescript
// Main bot structure
interface TradingBot {
  // Configuration
  config: BotConfig;

  // Core modules
  dataFeed: DataFeedModule;
  strategy: StrategyEngine;
  execution: ExecutionEngine;
  risk: RiskManager;

  // State
  positions: Map<string, Position>;
  openOrders: Map<string, Order>;
  status: BotStatus;

  // Lifecycle
  start(): Promise<void>;
  stop(): Promise<void>;
  pause(): void;
  resume(): void;
}

interface BotConfig {
  // Trading parameters
  tradingPairs: string[];
  maxPositionSize: number;      // Per token
  maxTotalExposure: number;     // Total USD
  maxConcurrentPositions: number;

  // Risk limits
  maxLossPerTrade: number;      // USD
  maxDailyLoss: number;         // USD
  maxDrawdownPercent: number;   // % of capital

  // Execution
  defaultSlippageBps: number;
  maxSlippageBps: number;
  priorityFeeMicroLamports: number;
  useJito: boolean;

  // Infrastructure
  rpcEndpoints: string[];
  wsEndpoints: string[];
  jitoEndpoint?: string;
}
```

### 3. Data Feed Module

```typescript
interface DataFeedModule {
  // Price data
  getPrice(mint: string): Promise<PriceData>;
  subscribePrices(mints: string[], callback: PriceCallback): Subscription;

  // On-chain data
  getTokenAccount(mint: string, owner: string): Promise<TokenAccountData>;
  getPoolState(poolAddress: string): Promise<PoolState>;

  // Health
  isHealthy(): boolean;
  getLatency(): number;
}

class JupiterPriceFeed implements DataFeedModule {
  private priceCache: Map<string, { price: number; timestamp: number }>;
  private cacheTTL = 1000; // 1 second

  async getPrice(mint: string): Promise<PriceData> {
    // Check cache
    const cached = this.priceCache.get(mint);
    if (cached && Date.now() - cached.timestamp < this.cacheTTL) {
      return { price: cached.price, source: 'cache' };
    }

    // Fetch from Jupiter
    const response = await fetch(
      `https://price.jup.ag/v6/price?ids=${mint}`
    );
    const data = await response.json();

    // Update cache
    this.priceCache.set(mint, {
      price: data.data[mint].price,
      timestamp: Date.now(),
    });

    return { price: data.data[mint].price, source: 'jupiter' };
  }
}
```

### 4. Strategy Engine

```typescript
interface StrategyEngine {
  // Generate signals
  evaluate(data: MarketData): Signal[];

  // Position sizing
  calculateSize(signal: Signal, risk: RiskState): number;

  // Entry/exit logic
  shouldEnter(signal: Signal): boolean;
  shouldExit(position: Position, data: MarketData): boolean;
}

interface Signal {
  type: 'LONG' | 'SHORT' | 'EXIT';
  token: string;
  confidence: number;   // 0-1
  reason: string;
  metadata: any;
}

// Example: Simple momentum strategy
class MomentumStrategy implements StrategyEngine {
  private readonly minConfidence = 0.6;
  private readonly lookbackPeriod = 60; // seconds

  evaluate(data: MarketData): Signal[] {
    const signals: Signal[] = [];

    for (const token of data.watchlist) {
      const priceChange = this.calculatePriceChange(token, this.lookbackPeriod);
      const volumeSpike = this.detectVolumeSpike(token);

      if (priceChange > 5 && volumeSpike) {
        signals.push({
          type: 'LONG',
          token,
          confidence: Math.min(priceChange / 10, 1),
          reason: `${priceChange.toFixed(1)}% gain with volume spike`,
          metadata: { priceChange, volumeSpike },
        });
      }
    }

    return signals;
  }

  calculateSize(signal: Signal, risk: RiskState): number {
    // Base size from config
    let size = risk.maxPositionSize;

    // Scale by confidence
    size *= signal.confidence;

    // Reduce if approaching limits
    const utilizationRatio = risk.currentExposure / risk.maxExposure;
    if (utilizationRatio > 0.8) {
      size *= (1 - utilizationRatio);
    }

    return Math.floor(size);
  }
}
```

### 5. Execution Engine

```typescript
interface ExecutionEngine {
  // Order management
  submitOrder(order: Order): Promise<OrderResult>;
  cancelOrder(orderId: string): Promise<boolean>;
  getOrderStatus(orderId: string): Promise<OrderStatus>;

  // Position management
  openPosition(params: OpenPositionParams): Promise<Position>;
  closePosition(positionId: string): Promise<CloseResult>;
}

class JupiterExecutionEngine implements ExecutionEngine {
  private connection: Connection;
  private wallet: Keypair;

  async submitOrder(order: Order): Promise<OrderResult> {
    const startTime = Date.now();

    try {
      // Get quote
      const quote = await this.getQuote(order);

      // Validate quote
      if (quote.priceImpactPct > order.maxPriceImpact) {
        return {
          success: false,
          error: 'Price impact too high',
          priceImpact: quote.priceImpactPct,
        };
      }

      // Get swap transaction
      const swapTx = await this.getSwapTransaction(quote, order);

      // Execute with retry
      const result = await this.executeWithRetry(swapTx, order.maxRetries);

      return {
        success: result.success,
        signature: result.signature,
        executionTime: Date.now() - startTime,
        fillPrice: this.calculateFillPrice(result),
        slippage: this.calculateSlippage(quote, result),
      };

    } catch (error) {
      return {
        success: false,
        error: error.message,
        executionTime: Date.now() - startTime,
      };
    }
  }

  private async executeWithRetry(
    swapTx: VersionedTransaction,
    maxRetries: number
  ): Promise<ExecutionResult> {
    let lastError: Error;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        // Increase priority fee on retry
        const priorityFee = this.config.basePriorityFee * Math.pow(1.5, attempt - 1);

        const signature = await this.sendTransaction(swapTx, priorityFee);
        const confirmation = await this.confirmTransaction(signature);

        if (confirmation.success) {
          return { success: true, signature, attempts: attempt };
        }

      } catch (error) {
        lastError = error;

        // Don't retry on certain errors
        if (this.isFatalError(error)) {
          break;
        }

        await this.sleep(100 * attempt);
      }
    }

    return { success: false, error: lastError, attempts: maxRetries };
  }
}
```

### 6. Risk Manager

```typescript
interface RiskManager {
  // Pre-trade checks
  canTrade(order: Order): RiskCheckResult;

  // Position monitoring
  checkPositions(): RiskAlert[];

  // Kill switch
  emergencyStop(reason: string): Promise<void>;

  // State
  getRiskState(): RiskState;
}

class DefaultRiskManager implements RiskManager {
  private state: RiskState;
  private alerts: RiskAlert[] = [];

  canTrade(order: Order): RiskCheckResult {
    const checks: RiskCheck[] = [];

    // Check 1: Position size limit
    checks.push({
      name: 'positionSize',
      passed: order.size <= this.config.maxPositionSize,
      message: `Size ${order.size} vs limit ${this.config.maxPositionSize}`,
    });

    // Check 2: Total exposure limit
    const newExposure = this.state.currentExposure + order.size * order.price;
    checks.push({
      name: 'totalExposure',
      passed: newExposure <= this.config.maxTotalExposure,
      message: `New exposure ${newExposure} vs limit ${this.config.maxTotalExposure}`,
    });

    // Check 3: Concurrent positions
    checks.push({
      name: 'concurrentPositions',
      passed: this.state.openPositions < this.config.maxConcurrentPositions,
      message: `Positions ${this.state.openPositions} vs limit ${this.config.maxConcurrentPositions}`,
    });

    // Check 4: Daily loss limit
    checks.push({
      name: 'dailyLoss',
      passed: Math.abs(this.state.dailyPnL) < this.config.maxDailyLoss,
      message: `Daily P/L ${this.state.dailyPnL} vs limit ${this.config.maxDailyLoss}`,
    });

    // Check 5: Drawdown limit
    const currentDrawdown = (this.state.peakCapital - this.state.currentCapital) / this.state.peakCapital;
    checks.push({
      name: 'drawdown',
      passed: currentDrawdown < this.config.maxDrawdownPercent,
      message: `Drawdown ${(currentDrawdown * 100).toFixed(1)}% vs limit ${this.config.maxDrawdownPercent * 100}%`,
    });

    const allPassed = checks.every(c => c.passed);

    return {
      allowed: allPassed,
      checks,
      reason: allPassed ? null : checks.find(c => !c.passed)?.message,
    };
  }

  async emergencyStop(reason: string): Promise<void> {
    console.error(`🚨 EMERGENCY STOP: ${reason}`);

    // Stop all new orders
    this.state.tradingEnabled = false;

    // Cancel all open orders
    await this.cancelAllOrders();

    // Close all positions (market orders)
    await this.closeAllPositions();

    // Alert
    await this.sendAlert({
      level: 'CRITICAL',
      message: `Bot emergency stopped: ${reason}`,
      timestamp: new Date(),
    });
  }
}
```

### 7. Infrastructure Layer

```typescript
// Multi-RPC with failover
class RPCManager {
  private endpoints: RPCEndpoint[];
  private activeIndex: number = 0;
  private healthChecks: Map<string, HealthStatus> = new Map();

  async getConnection(): Promise<Connection> {
    // Try active endpoint
    const active = this.endpoints[this.activeIndex];
    if (this.isHealthy(active)) {
      return new Connection(active.url);
    }

    // Failover to next healthy endpoint
    for (let i = 0; i < this.endpoints.length; i++) {
      const endpoint = this.endpoints[i];
      if (this.isHealthy(endpoint)) {
        this.activeIndex = i;
        return new Connection(endpoint.url);
      }
    }

    throw new Error('No healthy RPC endpoints available');
  }

  private async checkHealth(endpoint: RPCEndpoint): Promise<boolean> {
    try {
      const conn = new Connection(endpoint.url);
      const start = Date.now();
      await conn.getSlot();
      const latency = Date.now() - start;

      return latency < endpoint.maxLatency;
    } catch {
      return false;
    }
  }
}

// Structured logging
class BotLogger {
  log(level: 'DEBUG' | 'INFO' | 'WARN' | 'ERROR', event: string, data: any) {
    const entry = {
      timestamp: new Date().toISOString(),
      level,
      event,
      ...data,
    };

    console.log(JSON.stringify(entry));

    // Also send to external logging service
    this.sendToLoggingService(entry);
  }

  trade(action: 'OPEN' | 'CLOSE', position: Position, result: TradeResult) {
    this.log('INFO', 'TRADE', {
      action,
      token: position.token,
      side: position.side,
      size: position.size,
      entryPrice: position.entryPrice,
      exitPrice: result.price,
      pnl: result.pnl,
      pnlPercent: result.pnlPercent,
      executionTime: result.executionTime,
      signature: result.signature,
    });
  }
}
```

## Templates / Playbooks

### Bot Configuration Template

```typescript
const botConfig: BotConfig = {
  // Identity
  name: 'solana-momentum-bot',
  version: '1.0.0',

  // Trading parameters
  tradingPairs: ['SOL/USDC', 'BONK/SOL'],
  maxPositionSize: 1000,        // $1000 per position
  maxTotalExposure: 5000,       // $5000 total
  maxConcurrentPositions: 3,

  // Risk limits
  maxLossPerTrade: 100,         // $100 max loss per trade
  maxDailyLoss: 500,            // $500 max daily loss
  maxDrawdownPercent: 0.15,     // 15% max drawdown

  // Execution
  defaultSlippageBps: 100,      // 1% default slippage
  maxSlippageBps: 300,          // 3% max slippage
  priorityFeeMicroLamports: 10000,
  useJito: true,
  jitoTipLamports: 50000,       // 0.00005 SOL

  // Infrastructure
  rpcEndpoints: [
    'https://api.mainnet-beta.solana.com',
    'https://your-helius-endpoint.com',
  ],
  jitoEndpoint: 'https://mainnet.block-engine.jito.wtf',

  // Monitoring
  healthCheckInterval: 10000,   // 10 seconds
  alertWebhook: 'https://your-discord-webhook',
};
```

### Alert Template

```typescript
interface Alert {
  level: 'INFO' | 'WARN' | 'ERROR' | 'CRITICAL';
  event: string;
  message: string;
  data?: any;
}

// Discord webhook format
function formatDiscordAlert(alert: Alert): object {
  const colors = {
    INFO: 0x00ff00,
    WARN: 0xffff00,
    ERROR: 0xff8800,
    CRITICAL: 0xff0000,
  };

  return {
    embeds: [{
      title: `[${alert.level}] ${alert.event}`,
      description: alert.message,
      color: colors[alert.level],
      fields: alert.data ? Object.entries(alert.data).map(([k, v]) => ({
        name: k,
        value: String(v),
        inline: true,
      })) : [],
      timestamp: new Date().toISOString(),
    }],
  };
}
```

## Common Failure Modes + Debugging

### "Orders keep failing"
- Cause: Stale blockhash, low priority fee, or slippage too tight
- Detection: High failure rate in execution logs
- Fix: Refresh blockhash per order; increase priority fee; widen slippage

### "Bot got stuck in position"
- Cause: Exit order failing repeatedly
- Detection: Position age exceeds expected hold time
- Fix: Emergency market sell with high slippage; add escalating slippage on retry

### "Unexpected losses"
- Cause: Price moved against position faster than expected
- Detection: Large negative P/L on closed positions
- Fix: Tighter stop-losses; reduce position size; add momentum filters

### "Bot stopped trading"
- Cause: Risk limit hit or health check failed
- Detection: No trades for extended period
- Fix: Check risk state; verify RPC health; check wallet balance

### "Duplicate orders"
- Cause: Retry logic creating multiple orders
- Detection: Multiple fills for same signal
- Fix: Implement idempotency keys; check position before ordering

## Quality Bar / Validation

Implementation is complete when:
- [ ] All risk checks enforced before every trade
- [ ] Emergency stop tested and working
- [ ] Logging captures every decision and execution
- [ ] RPC failover tested
- [ ] Position tracking accurate
- [ ] P/L calculations verified
- [ ] Alerts firing correctly
- [ ] Graceful shutdown preserves state

## Output Format

Provide:
1. **Architecture diagram**: Component overview
2. **Configuration template**: All parameters with defaults
3. **Core code**: Strategy, execution, and risk modules
4. **Infrastructure setup**: RPC, logging, alerting
5. **Testing checklist**: What to verify before going live

## Examples

### Simple Example: Basic Swap Bot

**Input**: "Create a simple bot that buys tokens when they pump 10%"

**Output**:
```typescript
// Minimal viable trading bot
class SimplePumpBot {
  private positions: Map<string, Position> = new Map();
  private maxPositionUsd = 100;
  private minPumpPercent = 10;

  async run() {
    while (true) {
      // Check watchlist
      for (const token of this.watchlist) {
        const priceChange = await this.getPriceChange(token, '5m');

        // Entry signal
        if (priceChange >= this.minPumpPercent && !this.positions.has(token)) {
          await this.buy(token, this.maxPositionUsd);
        }

        // Exit signal (take profit or stop loss)
        if (this.positions.has(token)) {
          const position = this.positions.get(token);
          const pnl = await this.calculatePnL(position);

          if (pnl >= 20 || pnl <= -10) { // 20% TP or 10% SL
            await this.sell(token);
          }
        }
      }

      await this.sleep(5000); // Check every 5 seconds
    }
  }

  private async buy(token: string, usdAmount: number) {
    console.log(`BUY ${token} for $${usdAmount}`);
    // ... Jupiter swap implementation
  }

  private async sell(token: string) {
    console.log(`SELL ${token}`);
    // ... Jupiter swap implementation
  }
}
```

### Complex Example: Full Arbitrage Bot

**Input**: "Design an arb bot that captures price discrepancies across DEXs"

**Output**: See [examples/arb-bot-architecture.md](examples/arb-bot-architecture.md) for complete implementation including:
- Multi-DEX price monitoring (Jupiter, Raydium, Orca)
- Atomic execution via Jito bundles
- Profit calculation with fees
- Risk management for inventory
- Performance monitoring dashboard
