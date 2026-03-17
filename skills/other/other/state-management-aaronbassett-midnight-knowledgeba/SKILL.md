---
name: midnight-dapp:state-management
description: Use when reading public ledger state, implementing reactive UI that updates with chain state, caching state for performance, or understanding public vs private state in Midnight DApps.
---

# State Management

Read, sync, and cache contract state in Midnight DApps with proper handling of the dual-state model.

## When to Use

- Reading public ledger state from deployed contracts
- Implementing reactive UI that updates with chain state
- Caching state for performance optimization
- Understanding when to use public vs private state
- Syncing state across multiple components

## Key Concepts

### Dual-State Model

Midnight contracts have two types of state:

| State Type | Storage Location | Access Method | Visibility |
|------------|------------------|---------------|------------|
| **Public Ledger State** | On-chain (indexer) | `contract.state.*` | Anyone can read |
| **Private Local State** | Browser (LevelDB) | `WitnessContext.privateState` | Only local user |

This is fundamentally different from Ethereum where all state is public on-chain.

### State Access Patterns

```typescript
// Public state - anyone can read
const totalSupply = await contract.state.total_supply();
const balance = await contract.state.balances.get(address);

// Private state - accessed only in witnesses
const witnesses = {
  get_secret: ({ privateState }) => privateState.secretKey,
};
```

### Chain Synchronization

State on-chain can change from other transactions. DApps must handle:

1. **Initial Load** - Fetch current state when component mounts
2. **Polling** - Periodically check for updates
3. **WebSocket** - Subscribe to real-time updates
4. **Optimistic Updates** - Update UI before confirmation

## References

| Document | Description |
|----------|-------------|
| [contract-state.md](references/contract-state.md) | Reading public and private contract state |
| [chain-sync.md](references/chain-sync.md) | Synchronization patterns and subscriptions |
| [privacy-aware-caching.md](references/privacy-aware-caching.md) | Safe caching strategies for Midnight |
| [web3-comparison.md](references/web3-comparison.md) | Ethereum state patterns vs Midnight |

## Examples

| Example | Description |
|---------|-------------|
| [use-contract-state/](examples/use-contract-state/) | React hook for reading contract state |
| [state-sync-provider/](examples/state-sync-provider/) | Context provider for state synchronization |
| [cache-manager/](examples/cache-manager/) | Privacy-aware caching utilities |

## Quick Start

### 1. Read Simple State Values

```typescript
// After contract deployment, read public state
const contract = await deployedContract();

// Simple value
const totalSupply: bigint = await contract.state.total_supply();

// Map lookup
const balance: bigint | undefined = await contract.state.balances.get(userAddress);

// Set membership
const isMember: boolean = await contract.state.members.has(userAddress);
```

### 2. Create a State Hook

```typescript
function useContractState<T>(
  contract: Contract,
  accessor: (state: ContractState) => Promise<T>
) {
  const [value, setValue] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function fetchState() {
      setLoading(true);
      const result = await accessor(contract.state);
      if (!cancelled) {
        setValue(result);
        setLoading(false);
      }
    }

    fetchState();
    return () => { cancelled = true; };
  }, [contract, accessor]);

  return { value, loading };
}
```

### 3. Subscribe to Updates

```typescript
// Poll for state changes
useEffect(() => {
  const interval = setInterval(async () => {
    const newBalance = await contract.state.balances.get(address);
    setBalance(newBalance);
  }, 5000); // Poll every 5 seconds

  return () => clearInterval(interval);
}, [contract, address]);
```

## Common Patterns

### Type-Safe State Reading

```typescript
interface ContractState {
  total_supply(): Promise<bigint>;
  balances: {
    get(address: string): Promise<bigint | undefined>;
  };
  members: {
    has(address: string): Promise<boolean>;
  };
}

// The compiler generates these types from your Compact contract
```

### Error Handling

```typescript
async function safeStateRead<T>(
  accessor: () => Promise<T>,
  fallback: T
): Promise<T> {
  try {
    return await accessor();
  } catch (error) {
    console.error('State read failed:', error);
    return fallback;
  }
}

const balance = await safeStateRead(
  () => contract.state.balances.get(address),
  0n
);
```

### Optimistic Updates

```typescript
// Update UI immediately, then sync with chain
const [balance, setBalance] = useState<bigint>(0n);

async function transfer(to: string, amount: bigint) {
  // Optimistic update
  setBalance(prev => prev - amount);

  try {
    await contract.callTx.transfer(to, amount, witnesses);
    // State will sync on next poll
  } catch (error) {
    // Revert optimistic update
    setBalance(prev => prev + amount);
    throw error;
  }
}
```

## Related Skills

- `wallet-integration` - Required for setting up providers
- `proof-handling` - Witness implementation that accesses private state
- `transaction-flows` - Submitting state-changing transactions
- `error-handling` - Handling state read errors

## Related Commands

- `/dapp-check` - Validates provider configuration
- `/dapp-debug state` - Debug state synchronization issues
