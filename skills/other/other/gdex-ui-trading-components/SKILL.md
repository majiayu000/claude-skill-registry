---
name: gdex-ui-trading-components
description: React component patterns for GDEX trading UIs — order entry forms, position tables, copy trade panels, orderbook displays, and PnL views
---

# GDEX: Trading UI Components

React component patterns for building trading interfaces with the GDEX SDK. Each component shows the props interface, SDK method it calls, and state management pattern.

## When to Use

- Building a spot or perp trading form
- Displaying open positions or orders
- Creating a copy trade management panel
- Showing PnL or orderbook data

## Prerequisites

- GDEX SDK context provider set up — see **gdex-ui-install-setup**
- Authenticated via `loginWithApiKey()` — see **gdex-authentication**

## Spot Trade Form

```typescript
// components/SpotTradeForm.tsx
'use client';

import { useState } from 'react';
import { useGdex } from '@/providers/GdexProvider';

interface SpotTradeFormProps {
  defaultChain?: string;
  onTradeComplete?: (result: any) => void;
}

export function SpotTradeForm({ defaultChain = 'solana', onTradeComplete }: SpotTradeFormProps) {
  const { skill, isReady } = useGdex();
  const [mode, setMode] = useState<'buy' | 'sell'>('buy');
  const [chain, setChain] = useState(defaultChain);
  const [tokenAddress, setTokenAddress] = useState('');
  const [amount, setAmount] = useState('');
  const [slippage, setSlippage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isReady) return;
    setLoading(true);
    setError(null);
    try {
      const fn = mode === 'buy' ? skill.buyToken : skill.sellToken;
      const result = await fn.call(skill, { chain, tokenAddress, amount, slippage });
      onTradeComplete?.(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Trade failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Buy / Sell toggle */}
      <div className="flex gap-2">
        <button type="button" onClick={() => setMode('buy')}
          className={mode === 'buy' ? 'bg-green-600 text-white' : 'bg-gray-200'}>
          Buy
        </button>
        <button type="button" onClick={() => setMode('sell')}
          className={mode === 'sell' ? 'bg-red-600 text-white' : 'bg-gray-200'}>
          Sell
        </button>
      </div>

      {/* Chain selector */}
      <select value={chain} onChange={e => setChain(e.target.value)}>
        <option value="solana">Solana</option>
        <option value="8453">Base</option>
        <option value="42161">Arbitrum</option>
        <option value="1">Ethereum</option>
        <option value="56">BSC</option>
        <option value="sui">Sui</option>
      </select>

      <input placeholder="Token address" value={tokenAddress}
        onChange={e => setTokenAddress(e.target.value)} required />
      <input type="number" placeholder="Amount" value={amount}
        onChange={e => setAmount(e.target.value)} step="any" min="0" required />
      <input type="number" placeholder="Slippage %" value={slippage}
        onChange={e => setSlippage(Number(e.target.value))} step="0.1" min="0.1" max="50" />

      {error && <p className="text-red-500">{error}</p>}
      <button type="submit" disabled={loading || !isReady}>
        {loading ? 'Executing...' : `${mode === 'buy' ? 'Buy' : 'Sell'} Token`}
      </button>
    </form>
  );
}
```

**SDK methods called:** `skill.buyToken()`, `skill.sellToken()`

## Perp Order Form

```typescript
// components/PerpOrderForm.tsx
'use client';

import { useState } from 'react';
import { useGdex } from '@/providers/GdexProvider';

interface PerpOrderFormProps {
  onOrderPlaced?: (result: any) => void;
}

export function PerpOrderForm({ onOrderPlaced }: PerpOrderFormProps) {
  const { skill, isReady } = useGdex();
  const [coin, setCoin] = useState('BTC');
  const [side, setSide] = useState<'long' | 'short'>('long');
  const [sizeUsd, setSizeUsd] = useState('');
  const [leverage, setLeverage] = useState(5);
  const [takeProfitPrice, setTakeProfitPrice] = useState('');
  const [stopLossPrice, setStopLossPrice] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isReady) return;
    setLoading(true);
    setError(null);
    try {
      const result = await skill.openPerpPosition({
        coin, side, sizeUsd, leverage,
        ...(takeProfitPrice && { takeProfitPrice }),
        ...(stopLossPrice && { stopLossPrice }),
      });
      onOrderPlaced?.(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Order failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="flex gap-2">
        <button type="button" onClick={() => setSide('long')}
          className={side === 'long' ? 'bg-green-600 text-white' : 'bg-gray-200'}>
          Long
        </button>
        <button type="button" onClick={() => setSide('short')}
          className={side === 'short' ? 'bg-red-600 text-white' : 'bg-gray-200'}>
          Short
        </button>
      </div>

      <select value={coin} onChange={e => setCoin(e.target.value)}>
        <option value="BTC">BTC</option>
        <option value="ETH">ETH</option>
        <option value="SOL">SOL</option>
        <option value="ARB">ARB</option>
      </select>

      <input type="number" placeholder="Size (USD)" value={sizeUsd}
        onChange={e => setSizeUsd(e.target.value)} min="10" required />
      <input type="range" min="1" max="50" value={leverage}
        onChange={e => setLeverage(Number(e.target.value))} />
      <span>Leverage: {leverage}×</span>

      <input type="number" placeholder="Take Profit Price (optional)" value={takeProfitPrice}
        onChange={e => setTakeProfitPrice(e.target.value)} step="any" />
      <input type="number" placeholder="Stop Loss Price (optional)" value={stopLossPrice}
        onChange={e => setStopLossPrice(e.target.value)} step="any" />

      {error && <p className="text-red-500">{error}</p>}
      <button type="submit" disabled={loading || !isReady}
        className={side === 'long' ? 'bg-green-600' : 'bg-red-600'}>
        {loading ? 'Placing...' : `${side === 'long' ? 'Long' : 'Short'} ${coin}`}
      </button>
    </form>
  );
}
```

**SDK method called:** `skill.openPerpPosition()`

## Position Table

```typescript
// components/PositionTable.tsx
'use client';

import { useState, useEffect, useCallback } from 'react';
import { useGdex } from '@/providers/GdexProvider';

export function PositionTable({ pollInterval = 10000 }: { pollInterval?: number }) {
  const { skill, isReady } = useGdex();
  const [positions, setPositions] = useState<any[]>([]);

  const refresh = useCallback(async () => {
    if (!isReady) return;
    const data = await skill.hlGetPositions();
    setPositions(data?.positions ?? []);
  }, [skill, isReady]);

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, pollInterval);
    return () => clearInterval(id);
  }, [refresh, pollInterval]);

  if (!positions.length) return <p className="text-gray-500">No open positions</p>;

  return (
    <table className="w-full text-sm">
      <thead>
        <tr className="text-left border-b">
          <th>Asset</th><th>Side</th><th>Size</th><th>Entry</th>
          <th>Mark</th><th>PnL</th><th>Leverage</th><th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {positions.map((pos, i) => {
          const pnl = pos.unrealizedPnl ?? pos.pnl ?? 0;
          const isLong = Number(pos.szi ?? pos.size ?? 0) > 0;
          return (
            <tr key={i} className="border-b">
              <td>{pos.coin}</td>
              <td className={isLong ? 'text-green-500' : 'text-red-500'}>
                {isLong ? 'LONG' : 'SHORT'}
              </td>
              <td>${Math.abs(Number(pos.szi ?? pos.size ?? 0)).toFixed(2)}</td>
              <td>${Number(pos.entryPx ?? 0).toFixed(2)}</td>
              <td>${Number(pos.markPx ?? 0).toFixed(2)}</td>
              <td className={pnl >= 0 ? 'text-green-500' : 'text-red-500'}>
                ${Number(pnl).toFixed(2)}
              </td>
              <td>{pos.leverage?.value ?? '—'}×</td>
              <td>
                <button onClick={() => skill.closePerpPosition({ coin: pos.coin })}
                  className="text-red-500 hover:underline">
                  Close
                </button>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
```

**SDK methods called:** `skill.hlGetPositions()`, `skill.closePerpPosition()`

## Copy Trade Panel

```typescript
// components/CopyTradePanel.tsx
'use client';

import { useState, useEffect } from 'react';
import { useGdex } from '@/providers/GdexProvider';

export function CopyTradePanel() {
  const { skill, isReady } = useGdex();
  const [activeTrades, setActiveTrades] = useState<any[]>([]);
  const [topTraders, setTopTraders] = useState<any[]>([]);
  const [tab, setTab] = useState<'active' | 'discover'>('active');

  useEffect(() => {
    if (!isReady) return;
    // Load active copy trades
    skill.getCopyTrades?.().then(setActiveTrades).catch(() => {});
    // Load top traders for discovery
    skill.getTopTraders?.({ chain: 'solana', limit: 10 })
      .then(setTopTraders).catch(() => {});
  }, [skill, isReady]);

  return (
    <div>
      <div className="flex gap-2 mb-4">
        <button onClick={() => setTab('active')}
          className={tab === 'active' ? 'font-bold border-b-2' : ''}>
          Active ({activeTrades.length})
        </button>
        <button onClick={() => setTab('discover')}
          className={tab === 'discover' ? 'font-bold border-b-2' : ''}>
          Discover
        </button>
      </div>

      {tab === 'active' && (
        <div className="space-y-2">
          {activeTrades.map((trade, i) => (
            <div key={i} className="border rounded p-3 flex justify-between">
              <div>
                <p className="font-mono text-sm">{trade.traderWallet}</p>
                <p className="text-xs text-gray-500">{trade.copyTradeName}</p>
              </div>
              <span className="text-sm">
                {trade.copyBuyAmount} {trade.buyMode === 'fixed' ? 'fixed' : '%'}
              </span>
            </div>
          ))}
          {!activeTrades.length && <p className="text-gray-500">No active copy trades</p>}
        </div>
      )}

      {tab === 'discover' && (
        <div className="space-y-2">
          {topTraders.map((trader, i) => (
            <div key={i} className="border rounded p-3 flex justify-between items-center">
              <div>
                <p className="font-mono text-sm">{trader.wallet}</p>
                <p className="text-xs text-green-500">PnL: {trader.pnl}</p>
              </div>
              <button className="bg-blue-600 text-white px-3 py-1 rounded text-sm">
                Copy
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

**SDK methods called:** `skill.getCopyTrades()`, `skill.getTopTraders()`

## PnL Display

```typescript
// components/PnLDisplay.tsx
interface PnLDisplayProps {
  value: number;
  label?: string;
  showSign?: boolean;
  currency?: string;
}

export function PnLDisplay({ value, label, showSign = true, currency = '$' }: PnLDisplayProps) {
  const isPositive = value >= 0;
  const formatted = `${showSign && isPositive ? '+' : ''}${currency}${Math.abs(value).toFixed(2)}`;

  return (
    <div className="text-center">
      {label && <p className="text-xs text-gray-500 mb-1">{label}</p>}
      <p className={`text-lg font-bold ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
        {formatted}
      </p>
    </div>
  );
}
```

## Token Search with Autocomplete

```typescript
// components/TokenSearch.tsx
'use client';

import { useState, useCallback } from 'react';
import { useGdex } from '@/providers/GdexProvider';
import { debounce } from '@/utils/debounce'; // simple debounce utility

interface TokenSearchProps {
  chain: string;
  onSelect: (token: { address: string; symbol: string; name: string }) => void;
}

export function TokenSearch({ chain, onSelect }: TokenSearchProps) {
  const { skill, isReady } = useGdex();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);

  const search = useCallback(
    debounce(async (q: string) => {
      if (!isReady || q.length < 2) { setResults([]); return; }
      const data = await skill.getTokenDetails({ chain, address: q });
      setResults(data ? [data] : []);
    }, 300),
    [skill, isReady, chain]
  );

  return (
    <div className="relative">
      <input placeholder="Token address or symbol" value={query}
        onChange={e => { setQuery(e.target.value); search(e.target.value); }} />
      {results.length > 0 && (
        <ul className="absolute bg-white border rounded shadow-lg w-full z-10">
          {results.map((token, i) => (
            <li key={i} onClick={() => { onSelect(token); setResults([]); setQuery(token.symbol); }}
              className="p-2 hover:bg-gray-100 cursor-pointer">
              <span className="font-bold">{token.symbol}</span> — {token.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

**SDK method called:** `skill.getTokenDetails()`

## Component → SDK Method Reference

| Component | SDK Method | Skill |
|-----------|------------|-------|
| `SpotTradeForm` | `buyToken()`, `sellToken()` | gdex-spot-trading |
| `PerpOrderForm` | `openPerpPosition()` | gdex-perp-trading |
| `PositionTable` | `hlGetPositions()`, `closePerpPosition()` | gdex-perp-trading |
| `CopyTradePanel` | `getCopyTrades()`, `getTopTraders()` | gdex-copy-trading |
| `PnLDisplay` | (display only) | — |
| `TokenSearch` | `getTokenDetails()` | gdex-token-discovery |

## Backend Quirks Affecting UI (Live-Tested)

1. **Spot trading amounts in managed custody are RAW UNITS** (lamports/wei), not human-readable. The `SpotTradeForm` above uses `skill.buyToken()` which handles conversion, but if using `submitManagedPurchase()` directly, convert first.
2. **`hlCloseAll` is unreliable** — the `PositionTable` close button should use reduce-only orders, not `skill.hlCloseAll()`. See **gdex-perp-trading** for the workaround.
3. **Solana Meteora tokens fail** — if building a token selector, filter out `dexId === 'meteora'` tokens to avoid failed trades.
4. **Leverage slider is informational only** — `hlUpdateLeverage` returns 404. Effective leverage is determined by position size vs account equity.
5. **`getTopTraders()` needs numeric chainId** — use `622112261`, not `'solana'`.

## Related Skills

- **gdex-ui-install-setup** — Project setup and provider pattern
- **gdex-ui-portfolio-dashboard** — Portfolio display components
- **gdex-ui-page-layouts** — Full page compositions using these components
- **gdex-spot-trading** — Spot trading SDK API details and managed-custody quirks
- **gdex-perp-trading** — Perpetual futures SDK API details and close-position workaround
