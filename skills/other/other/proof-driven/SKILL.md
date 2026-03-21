---
name: proof-driven
description: Proof-driven development - design proofs from requirements, then execute CREATE -> VERIFY -> REMEDIATE cycle. Use when implementing with formal verification using property-based testing, theorem proving, or proof tactics; zero unproven property policy enforced.
---

# Proof-driven development

Prove properties from requirements before writing code. Proofs guide implementation, not the reverse. Zero unproven properties in final code.

**Modern insight (2025)**: PBT + example tests pairing is the standard -- properties discover edge cases, example tests prevent regressions and serve as documentation. Counterexamples from shrinking should always become permanent regression tests. AI-assisted PBT (Anthropic 2025) can generate properties from docstrings, but human judgment for property selection remains essential.

See [frameworks](references/frameworks.md) for language-specific PBT and stateful testing tools.
See [examples](references/examples.md) for brief property test patterns per language.
See [formal-tools](references/formal-tools.md) for theorem provers and bounded model checkers.

---

## Property Categories

| Category | Description | Example |
|----------|-------------|---------|
| **Postcondition** | Output satisfies contract | `sorted(sort(xs))` |
| **Invariant** | Property preserved by operation | `len(xs) == len(sort(xs))` |
| **Idempotence** | `f(f(x)) == f(x)` | `deduplicate(deduplicate(xs))` |
| **Inverse / Round-trip** | `g(f(x)) == x` | `decode(encode(x)) == x` |
| **Model-based** | Implementation matches reference | `my_sort(xs) == stdlib_sort(xs)` |
| **Commutativity** | Order doesn't matter | `a + b == b + a` |
| **Metamorphic** | Relationship between outputs | `sin(-x) == -sin(x)` |

**Most effective** (OOPSLA 2025): Model-based properties (~80% bug detection), postconditions (~65%). Least effective: properties that reimplement the logic under test.

**Anti-pattern**: Don't reimplement the function in the property. Properties should be *simpler* than the code they test.

---

## When to Apply

- Critical algorithms (sort, search, crypto, compression)
- Financial calculations (rounding, currency conversion)
- Consensus/distributed protocols (invariants across nodes)
- Safety-critical systems (medical, automotive, aerospace)
- Data structure invariants (balanced tree, heap property)
- Serialization round-trip (encode/decode fidelity)
- Stateful systems (databases, queues, caches) -- via stateful PBT

## When NOT to Apply

- UI rendering, visual layout
- Simple CRUD endpoints
- Configuration management
- Non-critical utility code
- Rapidly changing requirements (properties are expensive to maintain)

---

## Anti-patterns

- **Happy-path-only properties**: Properties must cover edge cases -- that's their primary value
- **Skipping stateful testing for stateful systems**: Use model-based stateful PBT (Hypothesis RuleBasedStateMachine, jqwik stateful)
- **Ignoring counterexamples**: Shrunk counterexamples are gold -- always convert to permanent regression tests
- **Properties that test the framework**: `assert fast_check works` is not `assert my_code works`
- **Permanently skipped/pending properties**: Zero-skip policy -- skip = unfinished work
- **Conflating PBT with unit testing**: PBT explores input space; unit tests verify known examples. Use both.
- **Not using shrinking**: If counterexample is 500-line input, it's useless. Shrinking finds minimal failing case.
- **Reimplementing logic in properties**: Property should be simpler than the code. If property is as complex as implementation, it adds no confidence.

---

## Shrinking

Shrinking transforms a failing complex input into the minimal input that still fails. This is the most valuable feature of PBT frameworks.

- **Integrated shrinking** (Hypothesis, Hedgehog): Generates shrink tree during generation. Preserves generator invariants. Superior approach.
- **Type-based shrinking** (QuickCheck): Separate shrinker functions. Can violate generator constraints.
- **Always investigate shrunk counterexamples**: They reveal the essential failure, stripped of noise.

## PBT vs Fuzzing (decision guidance)

| Aspect | PBT | Fuzzing |
|--------|-----|---------|
| Input generation | Guided by properties | Guided by code coverage |
| Oracle | User-written property assertions | Crashes/exceptions/timeouts |
| Best for | Correctness, algorithms, contracts | Security, memory safety, crash detection |
| **Convergence (2025)** | Hybrid tools (Bolero, Antithesis) combine both approaches |

---

## Proof Strategies

- **Simplification**: Reduce by known rules, use shrinking to find minimal counterexamples
- **Arithmetic**: Generate numeric edge cases (0, 1, MAX, negative, overflow boundaries)
- **Case analysis**: Split on constructors/variants, test each branch independently
- **Induction**: Recursive/sequential properties via stateful testing
- **Fuzzing**: Empirical exploration when properties are hard to specify formally
- **Metamorphic relations**: When oracle is unknown, test relationships between outputs

## Theorem Hierarchy

```
Main Property (Goal)
|-- Supporting Property 1
|   +-- Helper Property 1a
|-- Supporting Property 2
+-- Edge Case Property 3
```

---

## Workflow (language-neutral)

1. **PLAN** -- Identify correctness, safety, invariant, and termination properties. Design hierarchy. Choose property categories.
2. **CREATE** -- Write property test files. One property per concern. Tag by category (postcondition, invariant, inverse, etc.).
3. **VERIFY** -- Run all properties. Count unproven (skipped/pending). Analyze counterexamples via shrinking.
4. **REMEDIATE** -- Fill in each skipped property using proof strategies. Convert every counterexample to a permanent regression test.

---

## Constitutional Rules (Non-Negotiable)

1. **CREATE First**: Generate all property test artifacts from plan design before verification
2. **Complete All Proofs**: Zero skipped/pending properties in final code
3. **Totality Required**: All definitions must terminate
4. **Target Mirrors Model**: Implementation structure corresponds to proven model
5. **Iterative Remediation**: Fix proof failures, don't abandon verification

## Validation Gates

| Gate | Pass Criteria | Blocking |
|------|---------------|----------|
| Framework | PBT framework available and configured | Yes |
| Properties | All property tests pass | Yes |
| Unproven | Zero skipped/pending properties | Yes |
| Coverage | >= 80% line coverage | If present |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All properties pass, zero unproven/skipped |
| 11 | Property testing framework not available |
| 12 | No property tests created |
| 13 | Property tests failed or proofs incomplete |
| 14 | Coverage gaps (properties missing) |
