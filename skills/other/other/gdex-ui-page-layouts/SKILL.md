---
name: gdex-ui-page-layouts
description: Full page layout compositions for GDEX — trading page, portfolio page, copy trading page, and bridge page with responsive grid patterns
---

# GDEX: Page Layouts

Full page layout compositions for GDEX trading apps. Each layout combines components from other UI skills into a complete, responsive page.

## When to Use

- Building a full trading page with chart, order form, and positions
- Creating a portfolio dashboard page
- Composing a copy trading management page
- Building a bridge page

## Prerequisites

- Components from **gdex-ui-trading-components** and **gdex-ui-portfolio-dashboard**
- Theme set up per **gdex-ui-theming**
- SDK context provider from **gdex-ui-install-setup**

## Trading Page

The primary trading interface — chart, order form, positions, and optionally an orderbook.

```typescript
// app/trade/page.tsx
'use client';

import { useState } from 'react';
import { SpotTradeForm } from '@/components/SpotTradeForm';
import { PerpOrderForm } from '@/components/PerpOrderForm';
import { PositionTable } from '@/components/PositionTable';
import { TokenSearch } from '@/components/TokenSearch';
import { ChainSelector } from '@/components/ChainSelector';
import { PnLDisplay } from '@/components/PnLDisplay';

export default function TradingPage() {
  const [chain, setChain] = useState('solana');
  const [mode, setMode] = useState<'spot' | 'perp'>('spot');
  const [selectedToken, setSelectedToken] = useState<string>('');

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)]">
      {/* Top bar */}
      <header className="border-b border-[var(--border-primary)] px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-lg font-bold">GDEX Trade</h1>
          <div className="flex gap-1">
            <button onClick={() => setMode('spot')}
              className={`px-3 py-1 rounded text-sm ${mode === 'spot' ? 'bg-brand text-white' : ''}`}>
              Spot
            </button>
            <button onClick={() => setMode('perp')}
              className={`px-3 py-1 rounded text-sm ${mode === 'perp' ? 'bg-brand text-white' : ''}`}>
              Perp
            </button>
          </div>
        </div>
        <ChainSelector value={chain} onChange={setChain} />
      </header>

      {/* Main grid — responsive */}
      <div className="grid grid-cols-1 lg:grid-cols-[1fr_380px] gap-0 lg:gap-4 p-4">
        {/* Left: Chart + Token search + Positions */}
        <div className="space-y-4">
          {mode === 'spot' && (
            <TokenSearch chain={chain}
              onSelect={token => setSelectedToken(token.address)} />
          )}

          {/* Chart placeholder — integrate TradingView or Lightweight Charts */}
          <div className="bg-[var(--bg-card)] border border-[var(--border-primary)] rounded-lg h-[400px] flex items-center justify-center text-[var(--text-secondary)]">
            Chart — TradingView or Lightweight Charts
          </div>

          {/* Positions / Open orders */}
          {mode === 'perp' && (
            <div className="bg-[var(--bg-card)] border border-[var(--border-primary)] rounded-lg p-4">
              <h2 className="text-sm font-bold mb-3">Open Positions</h2>
              <PositionTable />
            </div>
          )}
        </div>

        {/* Right: Order form */}
        <div className="bg-[var(--bg-card)] border border-[var(--border-primary)] rounded-lg p-4 h-fit lg:sticky lg:top-4">
          <h2 className="text-sm font-bold mb-3">
            {mode === 'spot' ? 'Spot Trade' : 'Perp Order'}
          </h2>
          {mode === 'spot'
            ? <SpotTradeForm defaultChain={chain} />
            : <PerpOrderForm />
          }
        </div>
      </div>
    </div>
  );
}
```

### Layout Grid (responsive)

```
Mobile (< 1024px):          Desktop (≥ 1024px):
┌────────────────┐          ┌──────────────┬─────────┐
│ Token Search   │          │ Token Search │ Order   │
├────────────────┤          ├──────────────┤ Form    │
│ Chart          │          │ Chart        │         │
├────────────────┤          ├──────────────┤         │
│ Positions      │          │ Positions    │         │
├────────────────┤          └──────────────┴─────────┘
│ Order Form     │
└────────────────┘
```

## Portfolio Page

```typescript
// app/portfolio/page.tsx
'use client';

import { useState } from 'react';
import { PortfolioOverview } from '@/components/PortfolioOverview';
import { TokenBalanceGrid } from '@/components/TokenBalanceGrid';
import { TradeHistoryTable } from '@/components/TradeHistoryTable';
import { ChainSelector } from '@/components/ChainSelector';

export default function PortfolioPage() {
  const [chain, setChain] = useState('all');
  const [tab, setTab] = useState<'balances' | 'history'>('balances');

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-4 space-y-6">
      <h1 className="text-2xl font-bold">Portfolio</h1>

      {/* Overview cards */}
      <PortfolioOverview />

      {/* Chain filter */}
      <ChainSelector value={chain} onChange={setChain} />

      {/* Tabs */}
      <div className="flex gap-4 border-b border-[var(--border-primary)]">
        <button onClick={() => setTab('balances')}
          className={`pb-2 text-sm ${tab === 'balances' ? 'border-b-2 border-brand font-bold' : 'text-[var(--text-secondary)]'}`}>
          Token Balances
        </button>
        <button onClick={() => setTab('history')}
          className={`pb-2 text-sm ${tab === 'history' ? 'border-b-2 border-brand font-bold' : 'text-[var(--text-secondary)]'}`}>
          Trade History
        </button>
      </div>

      {/* Content */}
      {tab === 'balances'
        ? <TokenBalanceGrid chain={chain === 'all' ? undefined : chain} />
        : <TradeHistoryTable />
      }
    </div>
  );
}
```

## Copy Trading Page

```typescript
// app/copy-trade/page.tsx
'use client';

import { useState } from 'react';
import { CopyTradePanel } from '@/components/CopyTradePanel';

export default function CopyTradingPage() {
  const [platform, setPlatform] = useState<'solana' | 'hyperliquid'>('solana');

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-4 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Copy Trading</h1>
        <div className="flex gap-2">
          <button onClick={() => setPlatform('solana')}
            className={`px-3 py-1.5 rounded text-sm ${platform === 'solana' ? 'bg-[var(--color-chain-solana)] text-white' : 'border'}`}>
            Solana Spot
          </button>
          <button onClick={() => setPlatform('hyperliquid')}
            className={`px-3 py-1.5 rounded text-sm ${platform === 'hyperliquid' ? 'bg-brand text-white' : 'border'}`}>
            HL Perp
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_400px] gap-6">
        {/* Left: Leaderboard / Top traders */}
        <div className="bg-[var(--bg-card)] border border-[var(--border-primary)] rounded-lg p-4">
          <h2 className="text-lg font-bold mb-4">Top Traders</h2>
          <p className="text-sm text-[var(--text-secondary)]">
            {platform === 'solana' ? 'Top Solana spot traders by PnL' : 'Top HyperLiquid perp traders by PnL'}
          </p>
          {/* Trader leaderboard list */}
        </div>

        {/* Right: Active copy trades */}
        <div className="bg-[var(--bg-card)] border border-[var(--border-primary)] rounded-lg p-4">
          <h2 className="text-lg font-bold mb-4">Your Copy Trades</h2>
          <CopyTradePanel />
        </div>
      </div>
    </div>
  );
}
```

## Bridge Page

```typescript
// app/bridge/page.tsx
'use client';

import { useState } from 'react';
import { useGdex } from '@/providers/GdexProvider';
import { ChainSwitcher } from '@/components/ChainSwitcher';

export default function BridgePage() {
  const { skill, isReady } = useGdex();
  const [fromChain, setFromChain] = useState(1);
  const [toChain, setToChain] = useState(622112261);
  const [amount, setAmount] = useState('');
  const [estimate, setEstimate] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const getEstimate = async () => {
    if (!isReady || !amount) return;
    setLoading(true);
    try {
      const est = await skill.getBridgeEstimate({
        fromChain: String(fromChain),
        toChain: String(toChain),
        amount,
      });
      setEstimate(est);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-4">
      <h1 className="text-2xl font-bold mb-6">Bridge</h1>

      <div className="max-w-lg mx-auto bg-[var(--bg-card)] border border-[var(--border-primary)] rounded-lg p-6 space-y-4">
        {/* From chain */}
        <div>
          <label className="text-xs text-[var(--text-secondary)] mb-1 block">From</label>
          <ChainSwitcher value={fromChain} onChange={setFromChain} />
        </div>

        {/* Swap button */}
        <div className="flex justify-center">
          <button onClick={() => { setFromChain(toChain); setToChain(fromChain); }}
            className="p-2 border rounded-full hover:bg-[var(--bg-tertiary)]">
            ↕
          </button>
        </div>

        {/* To chain */}
        <div>
          <label className="text-xs text-[var(--text-secondary)] mb-1 block">To</label>
          <ChainSwitcher value={toChain} onChange={setToChain} />
        </div>

        {/* Amount */}
        <input type="number" placeholder="Amount (native token)" value={amount}
          onChange={e => setAmount(e.target.value)} step="any" min="0"
          className="w-full p-3 border rounded-lg bg-[var(--bg-input)]" />

        {/* Estimate */}
        <button onClick={getEstimate} disabled={loading || !amount}
          className="w-full py-3 bg-brand text-white rounded-lg font-bold disabled:opacity-50">
          {loading ? 'Getting estimate...' : 'Get Estimate'}
        </button>

        {estimate && (
          <div className="border border-[var(--border-primary)] rounded-lg p-4 space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-[var(--text-secondary)]">You receive</span>
              <span className="font-bold">{estimate.estimatedAmount}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[var(--text-secondary)]">Fee</span>
              <span>{estimate.fee}</span>
            </div>
            <button className="w-full py-2 mt-2 bg-brand text-white rounded-lg">
              Bridge Now
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
```

## Navigation Layout

```typescript
// components/Navigation.tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ConnectButton } from './ConnectButton';
import { ThemeToggle } from './ThemeToggle';

const NAV_ITEMS = [
  { href: '/trade', label: 'Trade' },
  { href: '/portfolio', label: 'Portfolio' },
  { href: '/copy-trade', label: 'Copy Trade' },
  { href: '/bridge', label: 'Bridge' },
];

export function Navigation() {
  const pathname = usePathname();

  return (
    <nav className="border-b border-[var(--border-primary)] bg-[var(--bg-primary)]">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-14">
        <div className="flex items-center gap-6">
          <span className="font-bold text-lg">GDEX</span>
          {NAV_ITEMS.map(item => (
            <Link key={item.href} href={item.href}
              className={`text-sm ${pathname === item.href
                ? 'text-brand font-bold'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'}`}>
              {item.label}
            </Link>
          ))}
        </div>
        <div className="flex items-center gap-3">
          <ThemeToggle />
          <ConnectButton />
        </div>
      </div>
    </nav>
  );
}
```

## Page → Component → SDK Method Map

| Page | Components Used | SDK Methods |
|------|----------------|-------------|
| Trading | `SpotTradeForm`, `PerpOrderForm`, `PositionTable`, `TokenSearch`, `ChainSelector` | `buyToken`, `sellToken`, `openPerpPosition`, `hlGetPositions`, `getTokenDetails` |
| Portfolio | `PortfolioOverview`, `TokenBalanceGrid`, `TradeHistoryTable`, `ChainSelector` | `getPortfolio`, `getTradeHistory` |
| Copy Trading | `CopyTradePanel` | `getCopyTrades`, `getTopTraders` |
| Bridge | `ChainSwitcher` | `getBridgeEstimate`, `executeBridge` |

## Related Skills

- **gdex-ui-install-setup** — Project scaffolding to build these pages
- **gdex-ui-trading-components** — Individual component patterns
- **gdex-ui-portfolio-dashboard** — Dashboard-specific components
- **gdex-ui-theming** — Theme tokens and CSS variables used throughout
- **gdex-ui-wallet-connection** — ConnectButton and auth flows
