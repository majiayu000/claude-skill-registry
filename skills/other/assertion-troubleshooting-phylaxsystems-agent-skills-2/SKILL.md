---
name: assertion-troubleshooting
description: "Phylax Credible Layer assertions troubleshooting. Diagnoses common assertion failures and non-triggering issues. Use when phylax/credible layer assertions fail unexpectedly or do not execute."
---

# Assertion Troubleshooting

Use this when assertions fail unexpectedly, revert with OutOfGas, or never execute.

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
- Tests show "Expected 1 assertion to be executed, but 0 were executed".
- Assertions revert with `OutOfGas` or unknown reasons.
- Call inputs appear empty or duplicate.

## When NOT to Use
- You need invariant design. Use `designing-assertions`.
- You need implementation details. Use `implementing-assertions`.
- You need test strategy or fuzzing. Use `testing-assertions`.

## Quick Start
1. Confirm trigger selector matches the target function.
2. Ensure `cl.assertion()` is immediately before the target call; the next external call consumes it.
3. Check if the target call reverted before assertions ran.
4. Verify cheatcodes are used in assertion functions, not constructors (`ph.load`, not `vm.load`).
5. Remember internal Solidity calls are not traced; triggers only fire on external entrypoints.
6. Use `pcl test -vvvv` for full traces and gas diagnostics.
7. Confirm `FOUNDRY_PROFILE=assertions` when running `pcl test`.
8. <u>Use `pcl test` for assertion tests because it includes the `cl.addAssertion` cheatcode; use `forge test` only for regular protocol tests.</u>
9. If the failure is `CreateContractSizeLimit`, split assertions into smaller contracts.
10. If the failure is an empty revert or ABI decode panic, re-check call input decoding (call inputs exclude selectors).

## Rationalizations to Reject
- "The assertion should have run." Verify triggers and call order first.
- "It is probably a test issue." Validate the target call succeeds without assertions.
- "Gas is fine." Happy path often consumes the most gas.

## References
- [Common Errors and Fixes](references/common-errors.md)
