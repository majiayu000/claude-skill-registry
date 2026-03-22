---
name: tdd-first
description: Enforce strict test-first discipline — no implementation code before a failing test exists
category: Testing BDD
---

# Skill: tdd-first

## What I do

I enforce the non-negotiable discipline of writing tests before implementation. Where `bdd-workflow` teaches *what* to test and *how* to structure specs, I enforce *when* — test FIRST, always. No exceptions. No shortcuts. No "I'll add tests later".

## When to use me

- Before writing ANY implementation code — load me and follow the mandatory sequence
- When an agent is tempted to "just write the function first"
- During code review to verify test-first discipline was followed
- When pairing with `bdd-workflow`, `ginkgo-gomega`, `jest`, or any test framework
- When fixing a bug — write the failing test that reproduces it BEFORE the fix

## Core principles

1. **Test first is non-negotiable** — No implementation code exists without a failing test that demanded it
2. **RED means the right failure** — The test fails because the behaviour doesn't exist yet, not because of a compilation error or wrong assertion
3. **Minimum to GREEN** — Write only enough implementation to make the failing test pass, nothing more
4. **Refactor under GREEN** — Improve design only when all tests pass; never refactor on RED
5. **Small cycles** — Each RED-GREEN-REFACTOR cycle should take minutes, not hours

## MANDATORY SEQUENCE (NON-NEGOTIABLE)

Every agent MUST follow this sequence. Violation is a blocking failure.

```
STEP 1: WRITE THE TEST
  → Describe the behaviour you want
  → Use your framework's syntax (It/Expect, test/assert, etc.)
  → The test MUST reference code that doesn't exist yet

STEP 2: MAKE IT COMPILE (stub only)
  → Create the function/method/type signature
  → Return zero values — Do NOT add any logic

STEP 3: RUN THE TEST — VERIFY RED
  → Confirm the test FAILS for the RIGHT REASON:
    ✅ "expected 42 but got 0" — correct RED (behaviour missing)
    ❌ "undefined: CreateUser" — compilation error, NOT red
    ❌ "nil pointer dereference" — crash, NOT red
  → If the test passes: your test is wrong

STEP 4: IMPLEMENT — MINIMUM TO GREEN
  → Write the simplest code that makes the test pass
  → Do NOT add extra features or optimisations
  → Run ALL tests — they must pass

STEP 5: REFACTOR UNDER GREEN
  → Improve naming, extract functions, remove duplication
  → Run tests after every change — stay GREEN

STEP 6: REPEAT — next behaviour, back to Step 1
```

## Patterns & examples

**WRONG (implementation first) — VIOLATION:**
```go
func CalculateDiscount(price float64, tier string) float64 {
    switch tier {
    case "gold": return price * 0.8
    case "silver": return price * 0.9
    default: return price
    }
}
// Then struggles to test rigid code — wasted tokens, poor design
```

**RIGHT (test first):**
```go
// STEP 1: Write the test
It("applies 20% discount for gold tier", func() {
    result := CalculateDiscount(100.0, "gold")
    Expect(result).To(Equal(80.0))
})

// STEP 2: Stub
func CalculateDiscount(price float64, tier string) float64 { return 0 }

// STEP 3: RED — "expected 80 but got 0" ✅

// STEP 4: Minimum to GREEN
func CalculateDiscount(price float64, tier string) float64 {
    if tier == "gold" { return price * 0.8 }
    return 0
}

// STEP 5: Refactor after more cases pass
```

## The cost of implementation first

Writing implementation before tests produces: coupled code, hard-to-mock dependencies, tests that conform to implementation rather than driving design, and wasted tokens fixing untestable code. Test-first produces injectable dependencies, clean interfaces, and safe refactoring from the first line. See KB doc for the full comparison table and interface stub pattern.

## Anti-patterns to avoid

- **"I'll add tests later"** — You won't. And if you do, they'll test the implementation, not the behaviour
- **GREEN without RED** — If you never saw the test fail, you don't know it tests anything
- **Compilation errors as RED** — `undefined: Foo` is not a failing test; stub the function first, then see the *behaviour* fail
- **Over-implementing on GREEN** — Write ONLY enough to pass. Extra code is untested code
- **Skipping REFACTOR** — The refactor phase is where clean design emerges; skipping it accumulates debt
- **Testing after debugging** — When you find a bug, write a failing test FIRST, then fix it

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/TDD First.md`

## Related skills

- `bdd-workflow` - Teaches BDD syntax and outside-in approach; tdd-first enforces the discipline
- `clean-code` - Apply during the REFACTOR phase of each cycle
- `ginkgo-gomega` - Go BDD framework; tdd-first ensures you use it test-first
- `jest` - JavaScript test framework; tdd-first ensures you use it test-first
- `rspec-testing` - Ruby BDD framework; tdd-first ensures you use it test-first
- `discipline` - General step discipline; tdd-first is the testing-specific enforcement
