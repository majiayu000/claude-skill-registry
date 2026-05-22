---
name: testing-assertions
description: "Tests Phylax Credible Layer assertions with CredibleTest, fuzzing, and backtesting. Use when writing or reviewing assertion tests."
---

# Testing Assertions

Build confidence that assertions block invalid transactions and allow valid ones.

## When to Use
- Writing unit, fuzz, or backtesting tests for assertions.
- Investigating false positives or gas-limit risks.
- Adding regression tests after protocol or assertion changes.

## When NOT to Use
- You need help designing invariants or triggers. Use `designing-assertions`.
- You only need implementation details. Use `implementing-assertions`.
- You need a backtesting setup. Use `backtesting-assertions`.

## Quick Start
- Use `CredibleTest` and `cl.assertion(...)` to register a single assertion function for the next transaction.
- `cl.assertion(...)` is consumed by the next external call and still requires a matching trigger.
- Test both passing and failing paths with `vm.expectRevert`.
- Add batch helper contracts for multi-operation transactions.
- Consider property-based testing (Echidna) for state invariants.
- Run tests with `pcl test`; it behaves like `forge test` (same flags, fuzzing, verbosity), but may lag Forge versions.
- Tests are Solidity functions starting with `test`; convention is `test/*.t.sol`.
- Use `FOUNDRY_PROFILE=assertions` (or unit/fuzz/backtest profiles) for predictable config.
- If proxy/delegatecall makes call inputs unreliable, add a log-based assertion variant and test both.

## Core Test Patterns
- **Positive path**: expected to pass and keep state consistent.
- **Negative path**: expected to revert with the assertion message.
- **Edge cases**: zero supply, empty vaults, proxy upgrades, nested batches.

## Gas Limit Checks
- Assertions are capped at 300k gas.
- The happy path is often the most expensive. Test with max sizes.
- Use `pcl test -vvv` to inspect per-call gas usage.

## Rationalizations to Reject
- "One passing test is enough." Assertions must also fail on violations.
- "Gas limits are a production problem." Exceeding 300k drops valid txs.
- "Fuzzing is optional." It finds edge cases that manual tests miss.

## References
- [Test Patterns](references/test-patterns.md)
- [PCL Test Parity](references/pcl-test-parity.md)
