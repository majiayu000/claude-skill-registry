---
name: assertion-troubleshooting
description: "Diagnoses common assertion failures and non-triggering issues. Use when assertions fail unexpectedly or do not execute."
---

# Assertion Troubleshooting

Use this when assertions fail unexpectedly, revert with OutOfGas, or never execute.

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
2. Ensure `cl.assertion()` is immediately before the target call.
3. Check if the target call reverted before assertions ran.
4. Verify cheatcodes are used in assertion functions, not constructors.
5. Use `pcl test -vvv` for traces and gas diagnostics.
6. Confirm `FOUNDRY_PROFILE=assertions` when running `pcl test`.

## Rationalizations to Reject
- "The assertion should have run." Verify triggers and call order first.
- "It is probably a test issue." Validate the target call succeeds without assertions.
- "Gas is fine." Happy path often consumes the most gas.

## References
- [Common Errors and Fixes](references/common-errors.md)
