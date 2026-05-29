---
name: implementing-assertions
description: "Phylax Credible Layer assertions implementation. Implements phylax/credible layer assertion contracts using cheatcodes, triggers, and event/state inspection."
---

# Implementing Assertions

Turn a written invariant spec into a correct, gas-safe assertion contract.

## Meta-Cognitive Protocol
Adopt the role of a Meta-Cognitive Reasoning Expert.

For every complex problem:
1.DECOMPOSE: Break into sub-problems
2.SOLVE: Address each with explicit confidence (0.0-1.0)
3.VERIFY: Check logic, facts, completeness, bias
4.SYNTHESIZE: Combine using weighted confidence
5.REFLECT: If confidence <0.8, identify weakness and retry
For simple questions, skip to direct answer.

Always output:
∙Clear answer
∙Confidence level
∙Key caveats

## When to Use
- Writing a new assertion contract from a defined invariant.
- Refactoring or optimizing existing assertions.
- Adding trigger logic, call input parsing, or event/state checks.

## When NOT to Use
- You only need invariant ideation or trigger selection. Use `designing-assertions`.
- You only need testing patterns. Use `testing-assertions`.

## Quick Start
Setup:
- Install the standard library: `forge install phylaxsystems/credible-std` (https://github.com/phylaxsystems/credible-std).
- Update `remappings.txt` with:
  - `credible-std/=lib/credible-std/src/` (https://github.com/phylaxsystems/credible-std)
  - `forge-std/=lib/forge-std/src/` (https://github.com/foundry-rs/forge-std)
- Credible cheatcodes (`ph.*`) are documented at https://docs.phylax.systems/credible/cheatcodes-overview and https://docs.phylax.systems/credible/cheatcodes-reference; use `credible-std/src/PhEvm.sol` in https://github.com/phylaxsystems/credible-std for the exact interface.
- Credible Layer overview: https://docs.phylax.systems/credible/credible-introduction.

## File and Naming Conventions
- **Assertion files**: `{ContractOrFeature}Assertion.a.sol` (e.g., `VaultOwnerAssertion.a.sol`)
- **Test files**: `{ContractOrFeature}Assertion.t.sol` (e.g., `VaultOwnerAssertion.t.sol`)
- **Assertion functions**: must start with `assertion` followed by the property name (e.g., `assertionOwnershipChange`, `assertionHealthFactor`, `assertionSupplyCap`)
- **Directory structure**: `assertions/src/` for assertion contracts, `assertions/test/` for tests

```solidity
contract MyAssertion is Assertion {
    function triggers() external view override {
        registerCallTrigger(this.assertionMonotonic.selector, ITarget.doThing.selector);
    }

    function assertionMonotonic() external {
        ITarget target = ITarget(ph.getAssertionAdopter());
        ph.forkPreTx();
        uint256 pre = target.totalAssets();
        ph.forkPostTx();
        uint256 post = target.totalAssets();
        require(post >= pre, "Invariant violated");
    }
}
```

## Implementation Checklist
- **Triggers**: use the narrowest possible trigger; avoid global triggers (`registerCallTrigger(fn)` or `registerStorageChangeTrigger(fn)` without a selector/slot).
- **One Trigger, One Assertion**: avoid multi-selector dispatchers; register each selector to its own assertion function and reuse shared helpers.
- **Interface Clarity**: use selectors from the interface that declares the function; if the adopter inherits it (e.g., ERC20/4626), call that out so the trigger source is obvious.
- **Pre/Post**: call `forkPreTx()` only when needed; default is post-state.
- **Call-Scoped Checks**: use `getCallInputs` + `forkPreCall`/`forkPostCall` for per-call invariants.
- **Call Input Shape**: `CallInputs.input` contains args only (selector is stripped). Decode args directly; if you need `msg.data` (e.g., timelock keys), rebuild with `abi.encodePacked(selector, input)`.
- **Preconditions**: use `before*` hook triggers or `forkPreCall` to assert pre-state requirements.
- **Baselines**: for intra-tx stability, read `forkPreTx()` once and compare per-call post snapshots.
- **Event Parsing**: filter by `emitter` and `topics[0]`; decode indexed vs data fields correctly.
- **Storage Slots**: use `ph.load` (not `vm.load`) for EIP-1967 slots, packed fields, and mappings; derive slots via `forge inspect <Contract> storage-layout`.
- **State Changes**: `getStateChanges*` includes the initial value at index 0; length 0 means no changes.
- **Constructors**: cheatcodes are unavailable; prefer `ph.getAssertionAdopter()` inside assertion functions and pass only constants via constructor args if needed.
- **Nested Calls**: avoid double counting; prefer `getCallInputs` to avoid proxy duplicates.
- **Internal Calls**: internal Solidity calls are not traced; register on external entrypoints (or `this.` calls) when you need call inputs.
- **Batch Dedupe**: deduplicate targets/accounts when a batch can repeat entries.
- **Tolerances**: use minimal, documented tolerances for price/decimals rounding.
- **Optional Interfaces**: use `staticcall` probing and skip when unsupported.
- **Token Quirks**: validate using balance deltas; handle fee-on-transfer and rebasing tokens.
- **Packed Calldata**: decode using protocol packing logic (assetId, amount, mode) and map ids via helpers.
- **Delta-Based Supply Checks**: compare totalSupply delta to sum of per-call amounts instead of enumerating users.
- **Id Mapping Guards**: if a packed id maps to `address(0)`, skip or fail early to avoid false positives.
- **Sentinel Amounts**: normalize `max`/sentinel values (e.g., full repay/withdraw) using pre-state.
- **Gas**: assertion gas cap is 300k; happy path is often most expensive; early return, cache reads, and limit loops.
- **Size Limit**: organize assertions by domain (e.g., access control, timelock, accounting) and split if you hit `CreateContractSizeLimit`.

## Anti-Patterns

### ❌ Dispatcher Pattern (Avoid)
Do not route multiple triggers through one assertion function that dispatches to helpers:
```solidity
// ❌ WRONG: Many triggers → one dispatcher → helpers
function triggers() external view override {
    registerCallTrigger(this.assertionOwnership.selector, IVault.setFee.selector);
    registerCallTrigger(this.assertionOwnership.selector, IVault.setGuardian.selector);
    registerCallTrigger(this.assertionOwnership.selector, IVault.submitCap.selector);
}

function assertionOwnership() external {
    // Dispatches internally based on what was called - hard to debug, wastes gas
}
```

### ✅ One Trigger, One Assertion (Preferred)
Register each trigger to its own assertion function. Share logic via internal helpers:
```solidity
// ✅ CORRECT: Each trigger has its own assertion function
function triggers() external view override {
    registerCallTrigger(this.assertionSetFee.selector, IVault.setFee.selector);
    registerCallTrigger(this.assertionSetGuardian.selector, IVault.setGuardian.selector);
    registerCallTrigger(this.assertionSubmitCap.selector, IVault.submitCap.selector);
}

function assertionSetFee() external {
    _checkOnlyOwner(); // Reuse helper
}

function assertionSetGuardian() external {
    _checkOnlyOwner(); // Reuse helper
}
```

### ❌ Mixed Interfaces (Avoid)
Do not mix selectors from parent and child interfaces:
```solidity
// ❌ CONFUSING: Mixing IERC4626 and IVault when IVault extends IERC4626
registerCallTrigger(this.assertionDeposit.selector, IERC4626.deposit.selector);
registerCallTrigger(this.assertionSubmitCap.selector, IVault.submitCap.selector);
```

### ✅ Consistent Interface (Preferred)
Use the adopter's interface consistently:
```solidity
// ✅ CLEAR: Use IVault for everything since it extends IERC4626
registerCallTrigger(this.assertionDeposit.selector, IVault.deposit.selector);
registerCallTrigger(this.assertionSubmitCap.selector, IVault.submitCap.selector);
```

## Rationalizations to Reject
- "Use getAllCallInputs everywhere." It can double-count proxy calls.
- "Many selectors can share one assertion dispatcher." It hurts gas and makes debugging harder.
- "I can ignore nested calls." Batched flows are common and must be handled.
- "Events are enough." If events can be skipped, back them with state checks.
- "We can rely on storage layout guesses." Always derive slots from layout.

## References
- [Cheatcodes and Traces](references/cheatcodes-and-traces.md)
- [Storage Layouts and Slots](references/storage-layouts-and-slots.md)
- [Event Parsing](references/event-parsing.md)
- [Tolerance and Rounding](references/tolerance-and-rounding.md)
- [Token Integration Safety](references/token-integration-safety.md)
