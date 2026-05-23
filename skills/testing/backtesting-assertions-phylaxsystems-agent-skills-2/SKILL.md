---
name: backtesting-assertions
description: "Phylax Credible Layer assertions backtesting. Runs assertion backtests against historical transactions. Use when validating phylax/credible layer assertions on real chain data or known exploits."
---

# Backtesting Assertions

Use Credible Layer backtesting to replay historical transactions with assertions enabled.

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
- You want to validate assertions against real mainnet transactions.
- You are testing a known exploit block or incident transaction.
- You need to confirm triggers match real protocol entrypoints.

## When NOT to Use
- You only need unit or fuzz tests. Use `testing-assertions`.
- You are designing invariants or triggers. Use `designing-assertions`.
- You only need Solidity implementation details. Use `implementing-assertions`.

## Quick Start
1. Place backtest files in `assertions/test/backtest/` (e.g., `VaultAssertion.backtest.t.sol`).
2. Create a test that inherits `CredibleTestWithBacktesting`.
3. Configure `BacktestingConfig` with target contract, block range, and assertion selector.
4. Call `executeBacktest` and assert failures are zero.
5. Run with the backtest profile: `FOUNDRY_PROFILE=assertions-backtest pcl test` (or use `--ffi` flag).

See `pcl-assertion-workflow` for the full profile configuration with `ffi = true`.

## Workflow
- Pick a target contract (the assertion adopter address).
- Choose `endBlock` and `blockRange`.
- Verify RPC env vars; skip or fallback when missing.
- Prefer `useTraceFilter = true` to detect internal calls; fall back to block scanning if your RPC lacks `trace_filter`.
- For large ranges, use a paid RPC to avoid rate limits; `useTraceFilter` reduces calls.
- Use `forkByTxHash = true` only when debugging state-dependent failures.
- Use `blockRange = 1` for a specific known exploit tx.
- If your invariant is keyed by `msg.data` (timelocks), rebuild calldata from selector + args; call inputs exclude the selector.
- Interpret results: `PASS`, `NEEDS_REVIEW` (selector mismatch or replay failure), `ASSERTION_FAIL` (often false positives or gas), `UNKNOWN_ERROR` (RPC or unexpected).
- If many `NEEDS_REVIEW`, the selector/target does not match or you need `forkByTxHash`.

## Rationalizations to Reject
- "We only need unit tests." Backtesting catches real-world call patterns.
- "Trace filter is optional." Without it you miss internal calls.
- "forkByTxHash everywhere." It is slow and RPC-heavy; use it for debugging only.
- "RPC isn't needed." Backtesting requires a working RPC and FFI.

## References
- [Backtesting Template](references/backtesting-template.md)
