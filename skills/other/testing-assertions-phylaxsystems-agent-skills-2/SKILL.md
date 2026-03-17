---
name: testing-assertions
description: "Phylax Credible Layer assertions testing. Tests phylax/credible layer assertions with CredibleTest, fuzzing, and backtesting."
---

# Testing Assertions

Build confidence that assertions block invalid transactions and allow valid ones.

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

- Writing unit, fuzz, or backtesting tests for assertions.
- Investigating false positives or gas-limit risks.
- Adding regression tests after protocol or assertion changes.

## When NOT to Use

- You need help designing invariants or triggers. Use `designing-assertions`.
- You only need implementation details. Use `implementing-assertions`.
- You need a backtesting setup. Use `backtesting-assertions`.

## Test Directory Structure

```
assertions/test/
├── unit/           # Unit tests (.t.sol)
├── fuzz/           # Fuzz tests (.t.sol)
└── backtest/       # Backtest tests (.t.sol)
```

- **Test files**: `{ContractOrFeature}Assertion.t.sol` (e.g., `VaultOwnerAssertion.t.sol`)
- **Test functions**: start with `test` (e.g., `testAssertionSetFeePasses`, `testAssertionSetFeeFails`)

Run tests by type using Foundry profiles:

- All tests: `FOUNDRY_PROFILE=assertions pcl test`
- Unit only: `FOUNDRY_PROFILE=assertions-unit pcl test`
- Fuzz only: `FOUNDRY_PROFILE=assertions-fuzz pcl test`
- Backtests only: `FOUNDRY_PROFILE=assertions-backtest pcl test`

See `pcl-assertion-workflow` for full `foundry.toml` profile configuration.

## Quick Start

- Use `CredibleTest` and `cl.assertion(...)` to register a single assertion function for the next transaction.
- **One assertion per test**: `cl.assertion(...)` registers exactly one assertion function. Create separate test functions for each assertion you want to verify.
- `cl.assertion(...)` is consumed by the next external call (like `vm.prank`) and still requires a matching trigger.
- Register full assertion contracts with `cl.addAssertion(...)` (usually in `setUp`) so `cl.validate(...)` can find them; this cheatcode is only available under `pcl test`.
- Passing assertions persist state changes; failing assertions revert and roll back state.
- For constructor args in tests, use `abi.encodePacked(type(MyAssertion).creationCode, abi.encode(args))`.
- Test both passing and failing paths with `vm.expectRevert`.
- Add at least one failing test per assertion function; use simple mock contracts when the protocol prevents invalid state. Create minimal mocks with the same function signature that do the wrong thing (e.g., don't mark nullifier as spent, send wrong amount).
- If `vm.expectRevert` fails due to call depth issues (e.g., "call didn't revert at a lower depth than cheatcode call depth"), use a low-level call pattern instead:

  ```solidity
  (bool success,) = address(target).call(abi.encodeCall(target.someFunction, (args)));
  assertFalse(success, "Should revert due to assertion failure");
  ```

- Add batch helper contracts for multi-operation transactions.
- If you must use fallback-based batches, call `address(batch).call("")` and assert on the `success` flag.
- Consider property-based testing (Echidna) for state invariants.
- For Forge cheatcodes (`vm.*`), see <https://getfoundry.sh/forge/tests/cheatcodes> and `forge-std/src/Vm.sol` in <https://github.com/foundry-rs/forge-std>; for Credible testing cheats (`cl.*`), see `credible-std/src/CredibleTest.sol` in <https://github.com/phylaxsystems/credible-std> plus <https://docs.phylax.systems/credible/testing-assertions> and <https://docs.phylax.systems/credible/cheatcodes-reference>.
- Credible Layer overview: <https://docs.phylax.systems/credible/credible-introduction>.
- <u>Use `pcl test` for assertion tests because it includes the `cl.addAssertion` cheatcode; use `forge test` only for regular protocol tests.</u>
- `pcl test` accepts `forge test` flags (fuzzing, verbosity), but may lag Forge versions.
- Tests are Solidity functions starting with `test`; convention is `test/*.t.sol`.
- Use `FOUNDRY_PROFILE=assertions` (or unit/fuzz/backtest profiles) for predictable config.
- If proxy/delegatecall makes call inputs unreliable, add a log-based assertion variant and test both.
- Organize assertions into modular contracts by domain (access control, timelock, caps). Split further if you hit `CreateContractSizeLimit`, and test each contract separately.
- For timelocked actions, include `submit` + `skip` or `warp` in tests so the action can execute before assertions run.

## Core Test Patterns

- **Positive path**: expected to pass and keep state consistent.
- **Negative path**: expected to revert with the assertion message.
- **Edge cases**: zero supply, empty vaults, proxy upgrades, nested batches.

## Gas Limit Checks

- Assertions are capped at 300k gas.
- The happy path is often the most expensive. Test with max sizes.
- Use `pcl test -vvvv` to inspect full traces and per-call gas usage.

## Rationalizations to Reject

- "One passing test is enough." Assertions must also fail on violations.
- "The protocol already reverts, so negative tests are pointless." Assertions still need a failing path.
- "Gas limits are a production problem." Exceeding 300k drops valid txs.
- "Fuzzing is optional." It finds edge cases that manual tests miss.

## References

- [Test Patterns](references/test-patterns.md)
- [PCL Test Parity](references/pcl-test-parity.md)
