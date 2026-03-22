---
name: gdex-ui-install-setup
description: React and Next.js project setup for GDEX — SDK initialization, context providers, environment variables, and TypeScript configuration
---

# GDEX: Frontend Installation & Setup

Set up a React or Next.js project to build trading UIs with the GDEX SDK. This skill covers project scaffolding, provider patterns, and SDK initialization.

## When to Use

- Starting a new frontend project that integrates GDEX trading
- Adding GDEX SDK to an existing React/Next.js app
- Setting up the provider hierarchy and context pattern
- Configuring TypeScript and environment variables for GDEX

## Prerequisites

- Node.js 18+ installed
- Basic React/Next.js knowledge

## Project Setup

### Next.js (Recommended)

```bash
npx create-next-app@latest my-gdex-app --typescript --tailwind --app
cd my-gdex-app
npm install @gdexsdk/gdex-skill ethers
```

### Vite + React

```bash
npm create vite@latest my-gdex-app -- --template react-ts
cd my-gdex-app
npm install @gdexsdk/gdex-skill ethers
```

## Environment Variables

```env
# .env.local (Next.js) or .env (Vite)
NEXT_PUBLIC_GDEX_API_KEY=9b4e1c73-6a2f-4d88-b5c9-3e7a2f1d6c54
# Or use the secondary key:
# NEXT_PUBLIC_GDEX_API_KEY=2c8f0a91-5d34-4e7b-9a62-f1c3d8e4b705
```

> For Vite, use `VITE_GDEX_API_KEY` prefix instead of `NEXT_PUBLIC_`.

## SDK Context Provider

Create a React context that initializes and shares the `GdexSkill` instance across your app:

```typescript
// src/providers/GdexProvider.tsx
'use client'; // Next.js App Router

import React, { createContext, useContext, useEffect, useRef, useState } from 'react';
import { GdexSkill } from '@gdexsdk/gdex-skill';

interface GdexContextValue {
  skill: GdexSkill;
  isReady: boolean;
  error: string | null;
}

const GdexContext = createContext<GdexContextValue | null>(null);

export function GdexProvider({ children, apiKey }: { children: React.ReactNode; apiKey: string }) {
  const skillRef = useRef(new GdexSkill());
  const [isReady, setIsReady] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    try {
      skillRef.current.loginWithApiKey(apiKey);
      setIsReady(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initialize GDEX SDK');
    }
  }, [apiKey]);

  return (
    <GdexContext.Provider value={{ skill: skillRef.current, isReady, error }}>
      {children}
    </GdexContext.Provider>
  );
}

export function useGdex(): GdexContextValue {
  const ctx = useContext(GdexContext);
  if (!ctx) throw new Error('useGdex must be used within <GdexProvider>');
  return ctx;
}
```

## App Layout with Provider

### Next.js App Router

```typescript
// src/app/layout.tsx
import { GdexProvider } from '@/providers/GdexProvider';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <GdexProvider apiKey={process.env.NEXT_PUBLIC_GDEX_API_KEY!}>
          {children}
        </GdexProvider>
      </body>
    </html>
  );
}
```

### Vite + React

```typescript
// src/main.tsx
import { GdexProvider } from './providers/GdexProvider';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <GdexProvider apiKey={import.meta.env.VITE_GDEX_API_KEY}>
    <App />
  </GdexProvider>
);
```

## Custom Hooks Pattern

Build feature-specific hooks on top of `useGdex()`:

```typescript
// src/hooks/usePortfolio.ts
import { useState, useCallback } from 'react';
import { useGdex } from '@/providers/GdexProvider';

export function usePortfolio() {
  const { skill, isReady } = useGdex();
  const [portfolio, setPortfolio] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const refresh = useCallback(async () => {
    if (!isReady) return;
    setLoading(true);
    try {
      const data = await skill.getPortfolio();
      setPortfolio(data);
    } finally {
      setLoading(false);
    }
  }, [skill, isReady]);

  return { portfolio, loading, refresh };
}
```

```typescript
// src/hooks/useTrade.ts
import { useState } from 'react';
import { useGdex } from '@/providers/GdexProvider';

export function useTrade() {
  const { skill, isReady } = useGdex();
  const [pending, setPending] = useState(false);
  const [result, setResult] = useState<any>(null);

  const buyToken = async (params: { chain: string; tokenAddress: string; amount: string; slippage?: number }) => {
    if (!isReady) throw new Error('SDK not ready');
    setPending(true);
    try {
      const res = await skill.buyToken(params);
      setResult(res);
      return res;
    } finally {
      setPending(false);
    }
  };

  const sellToken = async (params: { chain: string; tokenAddress: string; amount: string; slippage?: number }) => {
    if (!isReady) throw new Error('SDK not ready');
    setPending(true);
    try {
      const res = await skill.sellToken(params);
      setResult(res);
      return res;
    } finally {
      setPending(false);
    }
  };

  return { buyToken, sellToken, pending, result };
}
```

## TypeScript Configuration

Ensure your `tsconfig.json` includes Node.js types for the SDK:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "strict": true,
    "jsx": "react-jsx",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## Provider Hierarchy

For apps with wallet connection + GDEX + theming:

```
ThemeProvider          ← dark/light mode (see gdex-ui-theming)
  └─ WalletProvider   ← wallet connection (see gdex-ui-wallet-connection)
       └─ GdexProvider ← SDK instance + auth state
            └─ App     ← your trading UI
```

## Related Skills

- **gdex-ui-trading-components** — Trading UI component patterns (order forms, position tables)
- **gdex-ui-wallet-connection** — Wallet connection UI and auth flows
- **gdex-ui-theming** — CSS theming for trading interfaces
- **gdex-ui-page-layouts** — Full page compositions (trading, portfolio, copy trade)
- **gdex-authentication** — Backend auth details (encryption, session keys)
