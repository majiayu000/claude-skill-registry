---
name: tests-adversarial
description: "Write adversarial tests that intentionally stress failure paths. Use when hardening error handling, stress-testing assumptions, validating boundary behavior, or hunting silent failures."
---

# Adversarial Testing — Think Like the Attacker

Every line of code makes assumptions. Your job is to find them and violate them — systematically, not randomly. The goal is distrust, not coverage. A passing test suite proves nothing if it only tests the happy path.

## The Adversarial Mindset

1. **Every input is a lie.** Callers will send garbage, nulls, negative numbers, empty strings, and types that satisfy the compiler but violate intent.
2. **Implicit contracts are targets.** If the code assumes ordering, uniqueness, non-emptiness, or positive values without enforcing it — that is your entry point.
3. **The system is your adversary.** Files disappear, connections drop, clocks jump, memory runs out, permissions change between check and use.
4. **Passing tests prove nothing.** They prove the happy path works. Adversarial tests prove the sad paths do not silently corrupt.

## Assumption Hunting (Core Technique)

For every function or module under test, ask these six questions:

1. **What does it assume about inputs?** Violate each assumption: wrong type coercion, boundary values, null/nil/None, empty collections, maximum-size payloads.
2. **What does it assume about ordering?** Reorder arguments, reverse sequences, interleave concurrent calls, call methods out of lifecycle order.
3. **What does it assume about timing?** Delay responses past timeouts, deliver results before the consumer is ready, inject clock skew, expire tokens mid-operation.
4. **What does it assume about state?** Start from half-initialized state, corrupt shared state mid-operation, test post-error recovery state, double-close resources.
5. **What does it assume about resources?** Exhaust file descriptors, fill disk, revoke permissions, return allocation failures, saturate connection pools.
6. **What does it assume will NOT happen?** Make it happen. Concurrent modification during iteration, recursive re-entry, self-referential data, stack overflow via deep nesting.

## Attack Vectors (Thinking Prompts)

**Data:**
- Zero, negative, MAX_INT, NaN, Infinity, negative zero
- Empty string, null bytes in strings, multi-byte Unicode (emoji, RTL, ZWJ sequences)
- Empty collections, single-element, collections at capacity
- Encode a value, corrupt one byte, decode it

**State:**
- Double-close, use-after-free/dispose, read-after-error
- Concurrent mutation during iteration or serialization
- Half-written state from interrupted operation (crash mid-transaction)
- State machine receiving events for a different state

**Environment:**
- File not found, permission denied, disk full, read-only filesystem
- Network timeout, connection reset, DNS failure, partial write
- Clock jumps (forward 1 hour, backward 5 minutes, NTP correction)
- OOM at the worst possible moment (during cleanup/rollback)

**Protocol:**
- Out-of-order messages, duplicate delivery, missing acknowledgment
- Partial writes (half a JSON object, truncated protobuf)
- Version mismatch between client and server
- Request after connection close, response after timeout already fired

## The No-Cheating Rule

- Test through the **public API only**. If you need private access to break it, the abstraction is leaking — file that as a finding.
- If a scenario is "impossible," prove it with types or contracts. If you cannot prove it, it is not impossible — test it.
- Every test scenario must be **production-plausible**. Cosmic rays flipping bits are not plausible; a user pasting 10MB into a text field is.

## Writing Strategy

1. **Read the code.** Understand what it does, not what the docs say it does.
2. **List assumptions.** Write them down explicitly — one per line, no hedging.
3. **Write violation tests.** One test per assumption. Name it after what it violates: `test_rejects_negative_quantity`, `test_handles_empty_result_set`, `test_recovers_from_mid_write_crash`.
4. **Verify error quality.** When the code fails, does it produce a meaningful error? Silent corruption is worse than a crash.
5. **Test boundaries from both sides.** If the limit is 100, test 99, 100, and 101. If the limit is 0, test -1, 0, and 1.
6. **Run sanitizers and race detectors.** After writing tests: ASan, MSan, TSan, `-race`, Miri, or your language's equivalent. Tests that pass without sanitizers may hide undefined behavior.

## Validation Gates

| Gate | Condition |
|------|-----------|
| Assumptions documented | Every implicit assumption in the code under test is written down |
| Violations tested | Each documented assumption has at least one test that violates it |
| Errors are meaningful | Every failure path produces a descriptive error, not silence or generic message |
| Sanitizers pass | All tests pass under sanitizers / race detectors with zero warnings |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All assumptions identified, violated, and handled — error paths produce meaningful output |
| 1 | Untested assumptions remain — some assumptions lack violation tests |
| 2 | Silent failures found — code swallows errors or produces wrong output without signaling |
| 3 | Crashes or panics discovered — unhandled exceptions, segfaults, or undefined behavior found |
