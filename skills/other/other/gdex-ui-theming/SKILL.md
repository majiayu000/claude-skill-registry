---
name: gdex-ui-theming
description: CSS theming system for GDEX trading UIs — dark/light modes, trading colors, responsive breakpoints, and Tailwind CSS configuration
---

# GDEX: UI Theming

CSS theming system for building polished trading interfaces. Covers dark/light mode, trading-specific color semantics (long/short/PnL), responsive layouts, and Tailwind CSS integration.

## When to Use

- Setting up dark/light mode for a trading app
- Defining trading-specific color semantics (buy/sell, PnL, chains)
- Configuring responsive breakpoints for trading layouts
- Extending Tailwind CSS with trading theme tokens

## CSS Custom Properties

Define a base theme using CSS variables. Trading UIs need specialized color semantics beyond generic UI:

```css
/* styles/theme.css */

:root {
  /* Brand */
  --color-brand: #3B82F6;
  --color-brand-hover: #2563EB;

  /* Trading — Long / Short */
  --color-long: #22C55E;
  --color-long-bg: #22C55E1A;
  --color-short: #EF4444;
  --color-short-bg: #EF44441A;

  /* PnL */
  --color-pnl-positive: #22C55E;
  --color-pnl-negative: #EF4444;
  --color-pnl-neutral: #6B7280;

  /* Order Status */
  --color-status-filled: #22C55E;
  --color-status-pending: #F59E0B;
  --color-status-cancelled: #6B7280;
  --color-status-failed: #EF4444;

  /* Chain Colors */
  --color-chain-solana: #9945FF;
  --color-chain-ethereum: #627EEA;
  --color-chain-base: #0052FF;
  --color-chain-arbitrum: #2D374B;
  --color-chain-bsc: #F0B90B;
  --color-chain-sui: #4DA2FF;
  --color-chain-optimism: #FF0420;

  /* Surfaces (light mode) */
  --bg-primary: #FFFFFF;
  --bg-secondary: #F9FAFB;
  --bg-tertiary: #F3F4F6;
  --bg-card: #FFFFFF;
  --bg-input: #F9FAFB;
  --border-primary: #E5E7EB;
  --border-secondary: #D1D5DB;

  /* Text (light mode) */
  --text-primary: #111827;
  --text-secondary: #6B7280;
  --text-tertiary: #9CA3AF;
  --text-on-brand: #FFFFFF;

  /* Typography */
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Spacing */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;
}

/* Dark Mode */
[data-theme='dark'], .dark {
  --bg-primary: #0F1117;
  --bg-secondary: #1A1D28;
  --bg-tertiary: #252836;
  --bg-card: #1A1D28;
  --bg-input: #252836;
  --border-primary: #2D3348;
  --border-secondary: #3D4462;

  --text-primary: #F9FAFB;
  --text-secondary: #9CA3AF;
  --text-tertiary: #6B7280;
}
```

## Dark / Light Mode Toggle

```typescript
// components/ThemeToggle.tsx
'use client';

import { useEffect, useState } from 'react';

export function ThemeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem('gdex-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setDark(saved ? saved === 'dark' : prefersDark);
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
    document.documentElement.classList.toggle('dark', dark);
    localStorage.setItem('gdex-theme', dark ? 'dark' : 'light');
  }, [dark]);

  return (
    <button onClick={() => setDark(!dark)}
      className="p-2 rounded-lg border border-[var(--border-primary)] hover:bg-[var(--bg-tertiary)]">
      {dark ? '☀️' : '🌙'}
    </button>
  );
}
```

## Tailwind CSS Configuration

Extend Tailwind with GDEX trading theme tokens:

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: 'class',
  content: ['./src/**/*.{ts,tsx}', './app/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: 'var(--color-brand)',
        'brand-hover': 'var(--color-brand-hover)',
        long: 'var(--color-long)',
        'long-bg': 'var(--color-long-bg)',
        short: 'var(--color-short)',
        'short-bg': 'var(--color-short-bg)',
        'pnl-positive': 'var(--color-pnl-positive)',
        'pnl-negative': 'var(--color-pnl-negative)',
        'pnl-neutral': 'var(--color-pnl-neutral)',
        'surface-primary': 'var(--bg-primary)',
        'surface-secondary': 'var(--bg-secondary)',
        'surface-card': 'var(--bg-card)',
      },
      fontFamily: {
        sans: ['var(--font-sans)'],
        mono: ['var(--font-mono)'],
      },
      borderRadius: {
        sm: 'var(--radius-sm)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
      },
    },
  },
};

export default config;
```

### Usage in Components

```tsx
{/* Trading colors via Tailwind */}
<span className="text-long">+$420.69</span>     {/* green — long position / profit */}
<span className="text-short">-$69.42</span>      {/* red — short position / loss */}
<div className="bg-long-bg p-2">Long highlight</div>
<div className="bg-surface-card border border-[var(--border-primary)]">Card</div>
```

## Responsive Breakpoints

Trading UIs have unique layout needs — the primary trading view should maximize horizontal space:

```css
/* Trading layout breakpoints */
@media (min-width: 768px) {
  /* Tablet: stack chart above order form */
  .trading-layout { grid-template-columns: 1fr; }
}

@media (min-width: 1024px) {
  /* Desktop: chart + order form side by side */
  .trading-layout { grid-template-columns: 1fr 360px; }
}

@media (min-width: 1440px) {
  /* Wide: chart + orderbook + order form */
  .trading-layout { grid-template-columns: 280px 1fr 360px; }
}
```

```tsx
{/* Responsive trading grid */}
<div className="grid grid-cols-1 lg:grid-cols-[1fr_360px] xl:grid-cols-[280px_1fr_360px] gap-4">
  <aside className="hidden xl:block">{/* Orderbook */}</aside>
  <main>{/* Chart + Positions */}</main>
  <aside>{/* Order Form */}</aside>
</div>
```

## Component Styling Patterns

### Trading Buttons

```tsx
{/* Long / Short buttons */}
<button className="w-full py-3 rounded-lg font-bold text-white bg-long hover:opacity-90">
  Long BTC
</button>
<button className="w-full py-3 rounded-lg font-bold text-white bg-short hover:opacity-90">
  Short BTC
</button>
```

### PnL with Color

```tsx
function PnL({ value }: { value: number }) {
  const color = value > 0 ? 'text-pnl-positive' : value < 0 ? 'text-pnl-negative' : 'text-pnl-neutral';
  const sign = value > 0 ? '+' : '';
  return <span className={`font-mono font-bold ${color}`}>{sign}${value.toFixed(2)}</span>;
}
```

### Chain Badge

```tsx
const CHAIN_COLORS: Record<string, string> = {
  solana: 'var(--color-chain-solana)',
  ethereum: 'var(--color-chain-ethereum)',
  base: 'var(--color-chain-base)',
  arbitrum: 'var(--color-chain-arbitrum)',
  bsc: 'var(--color-chain-bsc)',
  sui: 'var(--color-chain-sui)',
};

function ChainBadge({ chain }: { chain: string }) {
  return (
    <span className="px-2 py-0.5 rounded-full text-xs font-medium text-white"
      style={{ backgroundColor: CHAIN_COLORS[chain] ?? '#6B7280' }}>
      {chain}
    </span>
  );
}
```

## Related Skills

- **gdex-ui-install-setup** — Project setup (includes Tailwind setup)
- **gdex-ui-page-layouts** — Full page layouts using these theme tokens
- **gdex-ui-trading-components** — Trading components that use theme colors
