---
name: troubleshoot-errors
description: Diagnose and fix common Algorand errors including smart contract failures, transaction rejections, and SDK exceptions. Use when encountering smart contract logic errors or assertion failures, transaction rejections or confirmation timeouts, SDK exceptions (AlgodHTTPError, LogicError), account-related errors (insufficient balance, not opted in), or ABI encoding/decoding errors. Strong triggers include "logic eval error", "assert failed", "overspend", "transaction rejected", "pc=X" in error messages, "opcode budget exceeded", "account not found", "asset not found".
---

# Troubleshoot Errors

Diagnose and resolve common Algorand development errors.

## Error Categories

| Category | Common Causes | Reference |
|----------|---------------|-----------|
| Contract Errors | Assert failures, opcode budget, invalid operations | [contract-errors.md](./references/contract-errors.md) |
| Transaction Errors | Overspend, invalid params, group issues | [transaction-errors.md](./references/transaction-errors.md) |

## Quick Diagnosis Flow

1. **Identify the error type** from the message
2. **Check the error code** if present (e.g., `pc=123`)
3. **Find the root cause** using the reference docs
4. **Apply the fix** from the common solutions

## Common Error Patterns

### Logic Eval Error (Contract Failure)

```
logic eval error: assert failed pc=123
```

**Cause:** An `assert` statement in the smart contract evaluated to false.

**Debug steps:**
1. The `pc=123` indicates the program counter where failure occurred
2. Use source maps to find the exact line in your code
3. Check the assertion condition and input values

### Transaction Rejected

```
TransactionPool.Remember: transaction TXID: overspend
```

**Cause:** Sender account has insufficient balance for amount + fee.

**Fix:** Fund the sender account or reduce the transaction amount.

### Opcode Budget Exceeded

```
logic eval error: dynamic cost budget exceeded
```

**Cause:** Contract exceeded the 700 opcode budget per app call.

**Fix:**
- Add more app calls to the group for additional budget (pooled)
- Optimize contract logic to reduce operations
- Split complex operations across multiple calls

### Asset Not Opted In

```
asset ASSET_ID missing from ACCOUNT_ADDRESS
```

**Cause:** The receiving account hasn't opted into the asset.

**Fix:** Have the receiver opt in before transferring:
```python
algorand.send.asset_opt_in(AssetOptInParams(
    sender=receiver_address,
    asset_id=asset_id,
))
```

## How to Proceed

1. **Find your error** in the category references below
2. **Understand the cause** from the explanation
3. **Apply the solution** from the code examples

## References

- [Contract Errors](./references/contract-errors.md) - Smart contract and logic errors
- [Transaction Errors](./references/transaction-errors.md) - Transaction and account errors
- [Debugging Guide](https://dev.algorand.co/concepts/smart-contracts/debugging/)
- [Error Handling in AlgoKit Utils](https://dev.algorand.co/algokit/utils/typescript/debugging/)
