---
name: transaction-hooks
description: Patterns to follow for implementing transaction hooks with tracking. Use when implementing new features interacting with EVM contracts, signing transactions, permit... etc.
---


### Transaction Pattern

```typescript
// 1. Transaction hook
const { approveAndExecute, signAndExecute, isLoading } = useXTransaction({ ... });

// 2. Named callback with useCallback
const handleExecute = useCallback(() => {
  if (!isApproved) {
    void approveAndExecute();
  } else {
    void signAndExecute();
  }
}, [isApproved, approveAndExecute, signAndExecute]);

// 3. ExecuteTransactionButton (handles connection/chain switching)
<ExecuteTransactionButton
  targetChainId={chainId}
  onClick={handleExecute}
  isLoading={isLoading}
  disabled={!amount}
>
  Execute
</ExecuteTransactionButton>
```

### Transaction Tracking & Process Modal

Multi-step transactions use `useTransactionTracking` + `GlobalTransactionModals` for persistent progress UI.

**Architecture:**
```
useTransactionTracking (hook)
    ↓ writes to
useTransactionProcessStore (Zustand)
    ↓ watched by
GlobalTransactionModals (renders ProcessModal)
    ↓ background txs shown in
TransactionIndicator (navbar indicator)
```

**Usage in transaction hooks:**

```typescript
import { useTransactionTracking } from '@/hooks/useTransactionTracking';

export function useSupplyTransaction(market: Market, onSuccess?: () => void) {
  const tracking = useTransactionTracking('supply');

  const steps = [
    { id: 'approve', title: 'Approve Token', description: 'Approving...' },
    { id: 'signing', title: 'Sign Message', description: 'Sign in wallet' },
    { id: 'supplying', title: 'Confirm Supply', description: 'Confirm tx' },
  ];

  const execute = async () => {
    // Start tracking - modal appears automatically
    tracking.start(steps, {
      title: `Supply ${market.loanAsset.symbol}`,        // Required
      description: `Supplying to market`,                // Optional
      tokenSymbol: market.loanAsset.symbol,              // Optional metadata
    }, 'approve');

    try {
      await doApproval();
      tracking.update('signing');     // Move to next step

      await doSign();
      tracking.update('supplying');

      await doSupply();
      tracking.complete();            // Removes from store, modal closes
      onSuccess?.();
    } catch (error) {
      tracking.fail();                // Removes from store
      throw error;
    }
  };

  return { execute, transaction: tracking.transaction };
}
```

**Key methods:**
- `start(steps, metadata, initialStep)` - Begin tracking, modal shows
- `update(stepId)` - Move to next step
- `complete()` / `fail()` - End tracking, remove from store
- `dismiss()` - Hide modal, tx continues in background (shows in indicator)

**No component-level ProcessModal needed.** `GlobalTransactionModals` (in layout) automatically renders modals for all visible transactions. When user dismisses, tx appears in `TransactionIndicator`. Clicking indicator restores the modal.

---

### useTransactionWithToast

Wraps wagmi's `useSendTransaction` with automatic toast notifications for pending, success, and error states.


**Usage:**

```typescript
import { useTransactionWithToast } from '@/hooks/useTransactionWithToast';

const { isConfirming, sendTransactionAsync } = useTransactionWithToast({
  toastId: 'supply',
  pendingText: `Supplying ${formatBalance(amount, decimals)} ${symbol}`,
  successText: `${symbol} Supplied`,
  errorText: 'Failed to supply',
  chainId,
  pendingDescription: `Supplying to market ${marketId.slice(2, 8)}...`,
  successDescription: `Successfully supplied to market ${marketId.slice(2, 8)}`,
  onSuccess,
});

// Execute transaction
await sendTransactionAsync({
  account,
  to: contractAddress,
  data: encodedData,
  value: ethValue,
  gas: gasLimit,  // Optional: override gas estimation
});
```

**Returns:**
- `sendTransactionAsync` - Async function to send transaction
- `sendTransaction` - Sync mutation function
- `isConfirming` - Boolean, true while waiting for confirmation
- `isConfirmed` - Boolean, true when transaction confirmed

**Combined with useTransactionTracking:**

For multi-step flows (approve → sign → execute), use both hooks together:
- `useTransactionTracking` - Shows step-by-step progress modal
- `useTransactionWithToast` - Handles the actual transaction toast notifications

```typescript
const tracking = useTransactionTracking('supply');
const { sendTransactionAsync, isConfirming } = useTransactionWithToast({ ... });

const execute = async () => {
  tracking.start(steps, metadata, 'approve');

  await doApproval();
  tracking.update('supplying');

  await sendTransactionAsync({ ... });  // Toast appears automatically
  tracking.complete();
};
```

---