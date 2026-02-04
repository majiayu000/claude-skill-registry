---
name: project-developer-guide
description: Development conventions and practices for this codebase. Use when writing PureScript code, tests, or FFI in this project.
---

# Project Developer Guide

These are the established conventions and practices for this codebase.

## 1. Library Source is Local — Look It Up

All PureScript dependencies are installed with full source code in `.spago/p/`. When uncertain about a function's behavior, signature, or available instances — **look it up**.

```
.spago/p/prelude-7.0.0/src/...
.spago/p/transformers-6.1.0/src/...
.spago/p/foldable-traversable-7.0.0/src/...
```

Use whatever tool fits the situation:
- **repomix** to understand a whole library's structure
- **grep** to find a specific function or type
- **read** when you know exactly where to look

Do not guess at function signatures or behaviors. Do not rely on potentially stale knowledge. The source is right there.

## 2. Property-Based Testing Only

All testing uses `spec`, `quickcheck`, and `spec-quickcheck`. We do not write one-off unit tests or example-based tests.

Tests assert properties over randomly generated inputs. This is appropriate for the domain — cryptographic primitives and circuit correctness are about invariants holding universally, not about specific examples passing.

Consult `.spago/p/` for these libraries when needed:
- `spec` — test organization and assertions
- `quickcheck` — property-based testing, `Arbitrary` instances
- `spec-quickcheck` — integration between the two

## 3. Circuit Testing via snarky-test-utils

For testing arithmetic circuits, use **`packages/snarky-test-utils`**. Do not invent new testing infrastructure.

The core pattern is `CircuitSpec`:

```purescript
type CircuitSpec f c r m a avar b =
  { builtState :: CircuitBuilderState c r
  , solver :: SolverT f c m a b
  , checker :: Checker f c
  , testFunction :: a -> Expectation b    -- pure reference function
  , postCondition :: PostCondition f c r
  }
```

The test framework:
1. Runs the circuit solver to produce output
2. Runs the pure `testFunction` to get expected output
3. Verifies all constraints are satisfied
4. Compares: circuit output must equal pure function output

The utilities in `snarky-test-utils` are used throughout the codebase. If you need a testing pattern, it's almost certainly already there.

## 4. FFI: The Three-Layer Pattern

Cryptographic primitives come from Rust via `packages/crypto-provider` (the `snarky-crypto` node module). The FFI follows a three-layer architecture:

### Layer 1: Rust (via napi-rs)
- Exposes minimal surface from arkworks / o1labs/proof-systems
- Functions take simple arguments (primitives, arrays) — not complex structs
- Sharing Rust objects across FFI is painful, so we avoid it

### Layer 2: JavaScript Wrapper
- Each PureScript module with `foreign import` has a corresponding `.js` file
- Imports from `snarky-crypto`
- Handles translation: restructures flat arrays into records, applies currying, shapes data for PureScript
- Absorbs awkwardness so both Rust and PureScript have clean interfaces

### Parse at the FFI Boundary, Not in PureScript

When FFI returns flat/unstructured data (like `[x0, y0, x1, y1, ...]`), transform it in the JS layer into properly structured records that match domain semantics.

**Why:**
1. **PureScript only sees clean, typed structures** — `Vector 16 (LrPair f)` instead of `Array f`
2. **Types are self-documenting** — `{ l :: AffinePoint f, r :: AffinePoint f }` immediately conveys meaning
3. **Parsing happens once at the boundary** — not scattered throughout PureScript code
4. **No unsafe array indexing in PureScript** — the JS layer handles flat-to-structured conversion

**Example:** Rust returns `lr` pairs as flat coordinates `[l0.x, l0.y, r0.x, r0.y, l1.x, ...]`

```javascript
// In .js file — parse into structured records
export const proofOpeningLr = (proof) => {
  const flat = snarky.proofOpeningLrFlat(proof);
  const pairs = [];
  for (let i = 0; i < flat.length; i += 4) {
    pairs.push({
      l: { x: flat[i], y: flat[i + 1] },
      r: { x: flat[i + 2], y: flat[i + 3] }
    });
  }
  return pairs;
};
```

```purescript
-- In .purs file — clean typed interface
foreign import proofOpeningLr :: Proof g f -> Array { l :: AffinePoint f, r :: AffinePoint f }
```

The JS layer acts as a **marshalling layer** between native representation and the PureScript type system.

### Layer 3: PureScript
- `foreign import` declarations with proper types
- `foreign import data` for opaque Rust objects
- Type classes to abstract over variants (e.g., Pallas/Vesta curves)
- Functional dependencies for type inference

**Example:** See `packages/pickles/test/Test/Pickles/ProofFFI.{purs,js}` for a comprehensive example of this pattern.

## 5. Circuit vs Pure Functions — Rust is Ground Truth

Many operations exist in two forms:
- **Circuit version** — uses the snarky DSL, creates constraints
- **Pure version** — regular computation, no constraints

### Where pure functions come from

Pure functions are typically **thin wrappers around Rust FFI**, not PureScript implementations. The Rust code (especially `o1labs/proof-systems`) provides the ground truth.

Why? This is cryptography. Complex arithmetic sequences must match protocols exactly. Since we're defining circuits that compute these protocols, we need "one foot in truth" — the pure reference function must come from a known-correct implementation.

### Where pure functions live

- **In library code** when needed at circuit boundaries (constructing inputs/outputs) or reused across packages
- **In tests** when only needed for testing a specific circuit

### Testing enforces correctness

The `snarky-test-utils` pattern ensures circuits match their pure counterparts:
```
Circuit output == Pure function output (backed by Rust)
```

If these disagree, the test fails. This is how we know circuits are correct.

## 6. The Advice Pattern — Witness Data via the `m` Parameter

The `Snarky c t m` monad has three type parameters:
- `c` — constraint type (e.g., `KimchiConstraint f`)
- `t` — state type for circuit building
- `m` — **the advice monad** for providing witness data

### What is advice?

Circuits sometimes need data that can't be computed from circuit variables alone. For example:
- Looking up an account address from a public key
- Factoring a number
- Fetching a Merkle path from a tree

This data must be "conjured up" by the prover during witness generation. The `m` parameter is how we abstract over this.

### The pattern

**1. Define a typeclass for your advice:**

```purescript
-- Simple example from snarky-test-utils/src/Test/Snarky/Circuit/Factors.purs
class Monad m <= FactorM f m where
  factor :: F f -> m { a :: F f, b :: F f }
```

**2. Use it in your circuit via `exists`:**

```purescript
factorsCircuit :: forall t m f c. FactorM f m => CircuitM f c t m => FVar f -> Snarky c t m Unit
factorsCircuit n = do
  { a, b } <- exists do
    nVal <- read n          -- read the circuit variable's concrete value
    lift $ factor @f nVal   -- call into the advice monad
  -- Now a and b are circuit variables (FVar f)
  -- The prover provided their values, the circuit constrains them
  c1 <- equals_ n =<< mul_ a b
  assert_ c1
```

**3. Provide instances for different phases:**

```purescript
-- For proving: actually compute the witness
instance PrimeField f => FactorM f Gen where
  factor n = do
    a <- arbitrary `suchThat` \a -> a /= one && a /= n
    pure { a, b: n / a }

-- For compilation: crash (should never be called)
instance FactorM f Effect where
  factor _ = throw "unhandled request: Factor"
```

### Two monads, two phases

| Phase | Monad | Advice behavior |
|-------|-------|-----------------|
| **Compile** | `Effect` or `Identity`-based | Crashes — advice should not be requested during compilation |
| **Prove** | `Gen`, `ReaderT Ref Effect`, etc. | Provides actual witness data |

### Testing with advice

Use `circuitSpec'` (not `circuitSpecPure'`) when your circuit needs advice:

```purescript
circuitSpec' 100 randomSampleOne  -- randomSampleOne :: Gen ~> Effect
  { builtState: s
  , checker: eval
  , solver: solver
  , testFunction: satisfied_
  , postCondition: postCondition
  }
  gen
```

The second argument is a natural transformation `m ~> Effect` that runs the advice monad.

### Full example

See `packages/example/` for a complete worked example:
- `src/Snarky/Example/Circuits.purs` — circuits using `AccountMapM` and `MerkleRequestM`
- `test/Test/Snarky/Example/Monad.purs` — `TransferRefM` (proving) and `TransferCompileM` (compilation) instances
- `test/Test/Snarky/Example/Circuits.purs` — testing with `circuitSpec'`

### When to use advice

Use advice when your circuit needs witness data that:
- Comes from external state (databases, trees, maps)
- Requires non-trivial computation (factoring, searching)
- Depends on prover-only knowledge

Do **not** use advice for values that can be computed purely from circuit inputs — just compute them directly.

---

## 7. Prefer Statically Sized Types

In the context of circuits, proofs, and cryptographic verification, data is almost always **statically sized**. Use PureScript's type-level sized containers instead of dynamic collections.

### The types

| Dynamic (avoid) | Static (prefer) | Package |
|-----------------|-----------------|---------|
| `Array a` | `Vector n a` | `sized-vector` |
| `BigInt` (unconstrained) | `SizedF n f` | `snarky` |

### Why this matters

1. **Circuit data is fixed-size** — IPA rounds, witness columns, polynomial evaluations all have known sizes at compile time
2. **Type safety catches bugs** — mismatched vector lengths are compile errors, not runtime surprises
3. **Zero runtime cost** — PureScript newtypes compile away; `Vector n a` is just `Array a` at runtime

### FFI boundary

Even when the underlying JavaScript/Rust type is dynamically sized (e.g., `Array`), **use static types on the PureScript side**:

```purescript
-- The JS returns an Array, but we know it's always 15 elements
foreign import proofWitnessEvals :: Proof g f -> Vector 15 (PointEval f)

-- The challenges are always IPA_ROUNDS long (e.g., 16 for SRS size 2^16)
foreign import proofBulletproofChallenges :: ... -> Array f  -- Convert to Vector d f
```

The JS wrapper can return a plain array; the PureScript `foreign import` declares the static type. If sizes don't match, you'll get a runtime error — which is the correct behavior (it indicates a bug in the Rust/JS layer or a misunderstanding of the protocol).

### When to determine sizes

Before writing code, investigate:
1. What is this data? (e.g., "bulletproof challenges")
2. What determines its size? (e.g., "IPA rounds = SRS log2 size")
3. Is it fixed for a given circuit/proof? (almost always yes)

Then use the appropriate type-level natural.

### Example: Converting at boundaries

```purescript
-- FFI returns Array (dynamic)
challengesArray :: Array f
challengesArray = proofBulletproofChallenges proverIndex { proof, publicInput }

-- Convert to Vector (static) — fails if length doesn't match
challenges :: Vector 16 f
challenges = unsafePartial $ fromJust $ Vector.toVector challengesArray
```

The `unsafePartial` is acceptable here because a length mismatch indicates a protocol violation, not normal program flow.

---

## Summary

| Principle | Practice |
|-----------|----------|
| Uncertain about a library function? | Look it up in `.spago/p/` |
| Writing tests? | Property-based with quickcheck, use `snarky-test-utils` for circuits |
| Need crypto primitives? | FFI from `crypto-provider`, follow three-layer pattern |
| Implementing a circuit? | Test against pure function; pure function wraps Rust |
| Reimplementing crypto in PureScript? | Don't. Wrap the Rust. |
| Circuit needs external witness data? | Use the advice pattern with `exists` and a custom typeclass |
| Data has known size? | Use `Vector n a` or `SizedF n f`, not `Array` |
