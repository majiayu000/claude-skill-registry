---
name: midnight-dapp:wallet-integration
description: Use when setting up Lace wallet connection, handling multiple user accounts, switching between testnet and mainnet, troubleshooting wallet issues, or migrating from MetaMask/Web3 patterns.
---

# Wallet Integration

Connect Lace wallet to your Midnight DApp for user authentication, account management, and transaction signing.

## When to Use

- Setting up wallet connection for the first time
- Handling multiple user accounts
- Switching between testnet and mainnet
- Troubleshooting wallet connection issues
- Migrating from MetaMask/Web3 patterns

## Key Concepts

### Browser Wallet Pattern

Lace wallet is a Chrome extension that injects `window.midnight.mnLace` into web pages. This is similar to MetaMask's `window.ethereum` but with Midnight-specific APIs.

### Connection Flow

1. **Check availability** - Verify Lace extension is installed
2. **Request authorization** - User approves DApp access
3. **Get wallet state** - Retrieve address, public keys
4. **Configure providers** - Set up indexer and proof server connections

### Address Format

Midnight uses Bech32m addresses (e.g., `addr_test1qz...`) instead of Ethereum's hex format (0x...).

## References

| Document | Description |
|----------|-------------|
| [lace-connection.md](references/lace-connection.md) | Wallet connection lifecycle and error handling |
| [account-management.md](references/account-management.md) | Multiple accounts and address display |
| [network-switching.md](references/network-switching.md) | Testnet vs mainnet configuration |
| [web3-comparison.md](references/web3-comparison.md) | MetaMask to Lace migration guide |

## Examples

| Example | Description |
|---------|-------------|
| [connect-button/](examples/connect-button/) | Basic wallet connection button component |
| [account-switcher/](examples/account-switcher/) | Multi-account selection UI |
| [network-selector/](examples/network-selector/) | Network selection dropdown |

## Quick Start

### 1. Check Wallet Availability

```typescript
const wallet = window.midnight?.mnLace;
if (!wallet) {
  // Show "Install Lace Wallet" prompt
  throw new Error('Lace wallet not installed');
}
```

### 2. Request Authorization

```typescript
const walletAPI = await wallet.enable();
// User sees approval popup in Lace
```

### 3. Get Wallet State

```typescript
const state = await walletAPI.state();
console.log('Address:', state.address);
console.log('Coin Public Key:', state.coinPublicKey);
```

### 4. Get Service URLs

```typescript
const uris = await wallet.serviceUriConfig();
// { indexerUri, indexerWsUri, proverServerUri }
```

## Common Patterns

### Connection State Hook

```typescript
function useMidnightWallet() {
  const [connected, setConnected] = useState(false);
  const [address, setAddress] = useState<string | null>(null);
  const [error, setError] = useState<Error | null>(null);

  const connect = async () => {
    try {
      const wallet = window.midnight?.mnLace;
      if (!wallet) throw new Error('Lace not installed');

      const api = await wallet.enable();
      const state = await api.state();

      setAddress(state.address);
      setConnected(true);
    } catch (e) {
      setError(e as Error);
    }
  };

  return { connected, address, error, connect };
}
```

### Display Address

```typescript
function formatAddress(address: string): string {
  // Bech32m addresses are long - truncate for display
  if (address.length <= 20) return address;
  return `${address.slice(0, 12)}...${address.slice(-8)}`;
}
```

## Related Skills

- `proof-handling` - Transaction signing flow after wallet connection
- `transaction-flows` - Submitting transactions via wallet
- `error-handling` - Wallet error messages and recovery

## Related Commands

- `/dapp-check` - Validates wallet provider configuration
- `/dapp-debug wallet` - Diagnose wallet connection issues
