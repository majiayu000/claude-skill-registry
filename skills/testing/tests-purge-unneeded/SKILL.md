---
name: tests-purge-unneeded
description: Delete tests that don't catch real bugs — the inverse of TDD. Use when reviewing legacy test suites, slow CI investigations, refactor-driven test sweeps, or evaluating whether a test the type system already covers should stay. Thesis — a test exists only if removing it would let a real bug reach production.
---

# Purge unneeded tests — deletion as discipline

Tests are not assets. Tests are liabilities that pay rent by catching real bugs. Volume is not a quality signal — coverage percentage is not a quality signal — only the counterfactual matters: **if I delete this test, can a real bug now reach prod?** If the answer is no, the test is dead weight, and dead weight slows CI, breeds noise, and trains reviewers to ignore failures.

**Modern insight (2025)**: TDD pairs with purge discipline. The same rigor that earns RED before GREEN earns deletion before keep — a test that cannot describe the bug it would catch should not exist. Mutation testing exposes which tests are actually load-bearing; the rest are cargo cult.

See [python](references/python.md) for pytest examples (dynamic-language carve-out).
See [typescript](references/typescript.md) for jest/vitest examples (static-language redundancy).
See [rust](references/rust.md) for cargo test examples (compile-time-guaranteed redundancy).
See [keep-vs-delete-table](references/keep-vs-delete-table.md) for the language-agnostic decision rubric.

---

## When to Apply

- Reviewing a legacy test suite where CI takes minutes per run
- Post-refactor sweeps — refactoring made some tests redundant; the refactor commit is the right place to delete them
- PR review where the diff adds tests that assert structure the type system already guarantees
- Onboarding to a codebase — flag suspicious patterns to surface for the original author
- Mutation testing reports — tests that survive every mutation are not catching anything

## When NOT to Apply

- Standalone "delete tests" sweep PRs — these become unreviewable and bundle unrelated concerns. Deletions ride alongside the work that makes them safe to delete.
- Behavior-change PRs where you have not separately confirmed the deletion is safe
- Code paths under active migration where coverage is the only safety net
- Any test whose failure mode you cannot articulate — if you cannot say what bug it would catch, you also cannot say it catches none

---

## The four mandates

The principles below are load-bearing. Internalize them; do not paraphrase.

### 1. A test exists to catch real bugs. If deleting the test would not let a bug reach production, delete the test.

This is the discriminator. Before keeping any test, ask: *what bug, specifically, does this fail on?* If the answer is "none I can name" or "a bug the compiler would catch", the test does not earn its keep. The bar is a real bug — not a hypothetical, not a "what if the implementation changes" — a concrete failure mode that a real change could plausibly introduce and that this test would catch.

### 2. Test contracts and boundaries: protocol compliance, error semantics, security invariants, integration across real I/O.

Tests earn their keep at boundaries. Protocol compliance (HTTP status codes, message formats, retry semantics), error semantics (what happens on malformed input, partial failure, timeout), security invariants (authz/authn enforcement, input validation, rate limits), and real-I/O integration (DB transactions, file I/O, network calls) are exactly where bugs hide and where the type system cannot help. These tests stay.

### 3. Do not test configuration shapes, constructor output fields, or struct assembly — the type system and constructors already guarantee those.

In statically-typed languages, the compiler already proves that a constructor returns the type it claims, that a struct has the fields it declares, and that a config object has the shape its type asserts. A test like `assert User(name="x").name == "x"` does not catch any bug a compiler does not — the only way it can fail is if `User`'s type signature changes, in which case the *test itself* fails to compile and the assertion is moot. Delete it.

### 4. Do not test that a function returns exactly what you passed in.

Identity-passthrough tests (`assert echo(x) == x`, `expect(passthrough(value)).toEqual(value)`) prove nothing — they describe the function's signature, not its behavior. If `echo` is supposed to validate or transform `x`, test the validation/transformation. If `echo` is genuinely identity, the function is dead code.

---

## Static-guarantee carve-out (mirror of `~/.claude/claude/system-prompt-baseline.md` `<directives>`)

The carve-out for mandate 3 is **language-dependent** and must mirror the user's system-prompt-baseline.md testing charter exactly:

- **Static-guarantee languages — Rust / TypeScript-strict / Kotlin / Java / C++ / OCaml**: structural assertions are redundant. A test that asserts a struct has the fields the compiler proved it has catches no bug. Delete.
- **Dynamic languages — Python / JavaScript / Ruby**: there is no compile-time guarantee that a function returns the shape the docstring claims. A boundary shape/type test IS a real-bug test — a refactor that silently changes the return shape would slip past type hints (which are advisory, not enforced at runtime). Keep.

The split is not aesthetic — it is about what guarantee the language provides. See `references/python.md` vs `references/typescript.md` for the contrasting examples.

---

## Decision rubric (summary; full table in `references/keep-vs-delete-table.md`)

| Pattern | Static lang | Dynamic lang |
|---------|-------------|--------------|
| Constructor returns expected fields | Delete — type system covers | Keep — boundary shape test |
| Function passes input through verbatim | Delete | Delete (test the dead code, then delete it) |
| HTTP handler returns 401 on missing auth | Keep — security invariant | Keep |
| Parser rejects malformed input | Keep — boundary | Keep |
| Two structs equal after struct-assembly | Delete | Keep if shape changes are plausible |
| Mock returns fixture, test asserts the fixture | Delete — testing the mock |
| Real DB transaction commits + rolls back | Keep — real I/O integration |

---

## Workflow

1. **Identify candidate** — a test that survives mutation, asserts structure, or has no clear failure scenario.
2. **Articulate the bug it catches** — write one sentence: *"this test fails when ___ goes wrong."* If you cannot complete that sentence with a real bug, the test is a candidate for deletion.
3. **Check the static guarantee** — for the test's language, would the compiler/type-checker already catch the bug? If yes, delete.
4. **Check the boundary contract** — does the test verify protocol/error/security/real-I/O behavior? If yes, keep.
5. **Inject the bug** — modify the production code to introduce the bug the test claims to catch. Run the suite. If the test still passes, the test does not catch that bug — delete.
6. **Delete with rationale in the commit message** — record *why* the deletion is safe, not just *that* it happened.

---

## Constitutional Rules (Non-Negotiable)

1. **Never delete a test as part of an unrelated change** — deletions are atomic commits with their own rationale, even if they ride in the same PR as the work that makes them safe.
2. **Never delete a test whose failure mode you have not understood** — confusion is not a license; if you cannot articulate the bug, you cannot prove its absence.
3. **Never reduce coverage of a security invariant** — auth, authz, input validation, secrets handling — these stay even when redundant.
4. **If conflict with `~/.claude/claude/system-prompt-baseline.md`, system-prompt-baseline.md wins** — this skill mirrors the user's testing charter; if drift is detected, system-prompt-baseline.md is the source of truth.

## Validation Gates

| Gate | Pass Criteria | Blocking |
|------|---------------|----------|
| Bug articulation | Each candidate has a one-sentence failure-mode description | Yes |
| Static-guarantee check | Confirmed compiler/type-checker does or does not cover the test | Yes |
| Bug-injection check | Test verified to NOT catch the bug, before deletion | Yes |
| Atomic commit | Deletion is its own commit with rationale | Yes |
| Suite still passes | Remaining tests green after deletion | Yes |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Deletion safe — bug-injection confirmed test catches nothing, atomic commit landed |
| 11 | Test framework not detected — cannot run bug-injection check |
| 12 | Bug articulation failed — candidate kept pending review |
| 13 | Static guarantee unclear — language carve-out not resolvable; kept pending |
| 14 | Test caught the injected bug — load-bearing; kept |
| 15 | Suite regressed after deletion — rollback required |

---

## See also

- `cleanup-codebase` — sibling deletion discipline for non-test code (dead fields, redundant wrappers, stale config)
- `tests-adversarial` — the complement: writing tests that *do* catch bugs, especially in failure paths and silent-failure regions
- `test-driven` — the design-side discipline (RED → GREEN → REFACTOR); purge runs in the REFACTOR phase
- `~/.claude/claude/system-prompt-baseline.md` `<directives>` testing charter — the source-of-truth principle this skill mirrors
