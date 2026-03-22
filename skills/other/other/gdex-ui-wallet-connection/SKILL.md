---
name: gdex-ui-wallet-connection
description: React patterns for GDEX wallet connection — connect buttons, account displays, chain switching, and API key vs wallet auth UI flows
---

# GDEX: Wallet Connection UI

React component patterns for wallet connection, authentication state management, and account display in GDEX trading apps.

## When to Use

- Adding a connect wallet / login button to your app
- Displaying account info (address, chain, balance)
- Managing authentication state (API key vs wallet-based)
- Implementing chain switching UI

## Prerequisites

- GDEX SDK context provider set up — see **gdex-ui-install-setup**
- Understanding of auth flows — see **gdex-authentication**

## Auth State Provider

Extend the base `GdexProvider` with wallet connection state:

```typescript
// providers/AuthProvider.tsx
'use client';

import React, { createContext, useContext, useState, useCallback } from 'react';
import { useGdex } from '@/providers/GdexProvider';

type AuthMethod = 'none' | 'api-key' | 'wallet';

interface AuthContextValue {
  authMethod: AuthMethod;
  walletAddress: string | null;
  managedAddress: string | null;
  isAuthenticated: boolean;
  loginWithApiKey: (key: string) => void;
  loginWithWallet: (address: string, signFn: (msg: string) => Promise<string>) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const { skill } = useGdex();
  const [authMethod, setAuthMethod] = useState<AuthMethod>('none');
  const [walletAddress, setWalletAddress] = useState<string | null>(null);
  const [managedAddress, setManagedAddress] = useState<string | null>(null);

  const loginWithApiKey = useCallback((key: string) => {
    skill.loginWithApiKey(key);
    setAuthMethod('api-key');
    setWalletAddress(null);
  }, [skill]);

  const loginWithWallet = useCallback(async (
    address: string,
    signFn: (msg: string) => Promise<string>
  ) => {
    await skill.loginWithWallet(address, signFn);
    setAuthMethod('wallet');
    setWalletAddress(address);
    // Fetch managed address after login
    const user = await skill.getWalletInfo();
    setManagedAddress(user?.managedAddress ?? null);
  }, [skill]);

  const logout = useCallback(() => {
    setAuthMethod('none');
    setWalletAddress(null);
    setManagedAddress(null);
  }, []);

  return (
    <AuthContext.Provider value={{
      authMethod,
      walletAddress,
      managedAddress,
      isAuthenticated: authMethod !== 'none',
      loginWithApiKey,
      loginWithWallet,
      logout,
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within <AuthProvider>');
  return ctx;
}
```

## Connect Button

```typescript
// components/ConnectButton.tsx
'use client';

import { useState } from 'react';
import { useAuth } from '@/providers/AuthProvider';
import { GDEX_API_KEY_PRIMARY } from '@gdexsdk/gdex-skill';

export function ConnectButton() {
  const { isAuthenticated, authMethod, walletAddress, loginWithApiKey, logout } = useAuth();
  const [showMenu, setShowMenu] = useState(false);

  if (isAuthenticated) {
    return (
      <div className="relative">
        <button onClick={() => setShowMenu(!showMenu)}
          className="px-4 py-2 border rounded-lg flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-green-500" />
          {authMethod === 'wallet'
            ? `${walletAddress!.slice(0, 6)}...${walletAddress!.slice(-4)}`
            : 'API Key Connected'}
        </button>
        {showMenu && (
          <div className="absolute right-0 mt-2 w-48 bg-white border rounded-lg shadow-lg z-50">
            <button onClick={() => { logout(); setShowMenu(false); }}
              className="w-full text-left px-4 py-2 hover:bg-gray-100 text-red-600">
              Disconnect
            </button>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="flex gap-2">
      {/* Quick connect with shared API key */}
      <button onClick={() => loginWithApiKey(GDEX_API_KEY_PRIMARY)}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
        Quick Connect
      </button>
    </div>
  );
}
```

## Account Display

```typescript
// components/AccountDisplay.tsx
'use client';

import { useAuth } from '@/providers/AuthProvider';

export function AccountDisplay() {
  const { isAuthenticated, authMethod, walletAddress, managedAddress } = useAuth();

  if (!isAuthenticated) return null;

  return (
    <div className="border rounded-lg p-4 space-y-2">
      <div className="flex justify-between items-center">
        <span className="text-xs text-gray-500">Auth Method</span>
        <span className="text-sm font-medium capitalize">{authMethod.replace('-', ' ')}</span>
      </div>

      {walletAddress && (
        <div className="flex justify-between items-center">
          <span className="text-xs text-gray-500">Control Wallet</span>
          <span className="font-mono text-sm">
            {walletAddress.slice(0, 6)}...{walletAddress.slice(-4)}
          </span>
        </div>
      )}

      {managedAddress && (
        <div className="flex justify-between items-center">
          <span className="text-xs text-gray-500">Managed Wallet</span>
          <span className="font-mono text-sm">
            {managedAddress.slice(0, 6)}...{managedAddress.slice(-4)}
          </span>
        </div>
      )}

      <p className="text-xs text-gray-400 mt-2">
        All trades execute from the managed wallet. Your control wallet only signs authentication.
      </p>
    </div>
  );
}
```

> **Critical:** `walletAddress` is the **control wallet** (used for sign-in). The **managed wallet** is GDEX's server-side wallet that executes trades. Never confuse them — all API calls use the control address as `userId`.

## Chain Switcher

```typescript
// components/ChainSwitcher.tsx
'use client';

import { useState } from 'react';

const SUPPORTED_CHAINS = [
  { id: 1, name: 'Ethereum', symbol: 'ETH' },
  { id: 8453, name: 'Base', symbol: 'ETH' },
  { id: 42161, name: 'Arbitrum', symbol: 'ETH' },
  { id: 56, name: 'BSC', symbol: 'BNB' },
  { id: 10, name: 'Optimism', symbol: 'ETH' },
  { id: 622112261, name: 'Solana', symbol: 'SOL' },
  { id: 1313131213, name: 'Sui', symbol: 'SUI' },
];

interface ChainSwitcherProps {
  value: number;
  onChange: (chainId: number) => void;
}

export function ChainSwitcher({ value, onChange }: ChainSwitcherProps) {
  const [open, setOpen] = useState(false);
  const selected = SUPPORTED_CHAINS.find(c => c.id === value);

  return (
    <div className="relative">
      <button onClick={() => setOpen(!open)} className="px-3 py-2 border rounded-lg flex items-center gap-2">
        {selected?.name ?? 'Select Chain'}
        <span className="text-xs">▼</span>
      </button>
      {open && (
        <ul className="absolute mt-1 w-48 bg-white border rounded-lg shadow-lg z-50">
          {SUPPORTED_CHAINS.map(chain => (
            <li key={chain.id}>
              <button onClick={() => { onChange(chain.id); setOpen(false); }}
                className={`w-full text-left px-4 py-2 hover:bg-gray-100 ${
                  chain.id === value ? 'font-bold bg-gray-50' : ''
                }`}>
                {chain.name} ({chain.symbol})
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## Provider Hierarchy

```
ThemeProvider
  └─ AuthProvider          ← wallet/API key state
       └─ GdexProvider     ← SDK instance
            └─ App
```

```typescript
// app/layout.tsx
import { GdexProvider } from '@/providers/GdexProvider';
import { AuthProvider } from '@/providers/AuthProvider';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <GdexProvider apiKey={process.env.NEXT_PUBLIC_GDEX_API_KEY!}>
          <AuthProvider>
            {children}
          </AuthProvider>
        </GdexProvider>
      </body>
    </html>
  );
}
```

## Two Auth Paths

| Path | When | Flow |
|------|------|------|
| **API Key (quick)** | Shared/demo accounts, agent-driven apps | Call `loginWithApiKey(GDEX_API_KEY_PRIMARY)` — instant, no wallet needed |
| **Wallet (full)** | User's own wallet, production apps | User connects wallet → signs message → `loginWithWallet(address, signFn)` → SDK creates session key |

> Most agent-driven apps use the **API key path** since shared keys are built into the SDK. Wallet-based auth is for production apps where users bring their own wallets.

## Related Skills

- **gdex-ui-install-setup** — Base project setup and GdexProvider
- **gdex-authentication** — Full auth flow details (encryption, session keys, managed custody)
- **gdex-ui-trading-components** — Trading forms that require authenticated SDK
- **gdex-wallet-setup** — Generate wallets for users who don't have one
