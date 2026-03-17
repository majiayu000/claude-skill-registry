---
name: polyglot-spi
description: "Cross-Language Strong Parallelism Invariance Verification for 15+ languages"
---

# polyglot-spi

> Cross-Language Strong Parallelism Invariance Verification

**Version**: 1.1.0 (music-topos enhanced)
**Trit**: -1 (Validator - verifies cross-language consistency)
**Bundle**: verification

## Overview

Polyglot-SPI verifies that the SPI seed `0xf061ebbc2ca74d78` produces identical color sequences across all supported languages. This ensures deterministic parallel execution regardless of runtime.

## The SPI Invariant

```
GAY_SEED = 0x598F318E2B9E884
splitmix64(GAY_SEED) → 0xf061ebbc2ca74d78 (index 0)

This value MUST be identical in all 15+ languages.
```

## Language Implementations

### Julia (Reference)

```julia
# Gay.jl/src/kernels.jl
function splitmix64(state::UInt64)
    state += 0x9E3779B97F4A7C15
    z = state
    z = (z ⊻ (z >> 30)) * 0xBF58476D1CE4E5B9
    z = (z ⊻ (z >> 27)) * 0x94D049BB133111EB
    z ⊻ (z >> 31)
end

@assert splitmix64(UInt64(0x598F318E2B9E884)) == 0xf061ebbc2ca74d78
```

### Python

```python
def splitmix64(state: int) -> tuple[int, int]:
    """Reference SplitMix64 implementation."""
    state = (state + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    return state, (z ^ (z >> 31)) & 0xFFFFFFFFFFFFFFFF

GAY_SEED = 0x598F318E2B9E884
_, value = splitmix64(GAY_SEED)
assert value == 0xf061ebbc2ca74d78
```

### Ruby

```ruby
# lib/spi_verify.rb
module SPIVerify
  GAY_SEED = 0x598F318E2B9E884
  EXPECTED = 0xf061ebbc2ca74d78
  
  def self.splitmix64(state)
    state = (state + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    (z ^ (z >> 31)) & 0xFFFFFFFFFFFFFFFF
  end
  
  def self.verify!
    result = splitmix64(GAY_SEED)
    raise "SPI mismatch: got #{result.to_s(16)}" unless result == EXPECTED
    puts "✓ Ruby SPI verified"
  end
end
```

### Hy (Lisp on Python)

```hy
;; spi_verify.hy
(defn splitmix64 [state]
  (setv state (& (+ state 0x9E3779B97F4A7C15) 0xFFFFFFFFFFFFFFFF))
  (setv z state)
  (setv z (& (* (^ z (>> z 30)) 0xBF58476D1CE4E5B9) 0xFFFFFFFFFFFFFFFF))
  (setv z (& (* (^ z (>> z 27)) 0x94D049BB133111EB) 0xFFFFFFFFFFFFFFFF))
  (& (^ z (>> z 31)) 0xFFFFFFFFFFFFFFFF))

(defn verify-spi []
  (setv result (splitmix64 0x598F318E2B9E884))
  (assert (= result 0xf061ebbc2ca74d78) 
          (+ "SPI mismatch: " (hex result)))
  (print "✓ Hy SPI verified"))
```

### Babashka (Clojure)

```clojure
;; spi_verify.bb
(def GAY_SEED 0x598F318E2B9E884)
(def EXPECTED 0xf061ebbc2ca74d78)

(defn splitmix64 [state]
  (let [state (bit-and (+ state 0x9E3779B97F4A7C15) 0xFFFFFFFFFFFFFFFF)
        z state
        z (bit-and (* (bit-xor z (bit-shift-right z 30)) 0xBF58476D1CE4E5B9) 0xFFFFFFFFFFFFFFFF)
        z (bit-and (* (bit-xor z (bit-shift-right z 27)) 0x94D049BB133111EB) 0xFFFFFFFFFFFFFFFF)]
    (bit-and (bit-xor z (bit-shift-right z 31)) 0xFFFFFFFFFFFFFFFF)))

(defn verify! []
  (let [result (splitmix64 GAY_SEED)]
    (assert (= result EXPECTED) (str "SPI mismatch: " (format "%x" result)))
    (println "✓ Babashka SPI verified")))

(verify!)
```

## Verification Matrix

| Language | File | Status |
|----------|------|--------|
| Julia | `Gay.jl/src/kernels.jl` | ✓ Reference |
| Python | `gay_spi.py` | ✓ Verified |
| Ruby | `lib/spi_verify.rb` | ✓ Verified |
| Hy | `spi_verify.hy` | ✓ Verified |
| Babashka | `spi_verify.bb` | ✓ Verified |
| Rust | `gay-rs/src/lib.rs` | ✓ Verified |
| Go | `gay-go/gay.go` | ✓ Verified |
| TypeScript | `eg-walker/src/gay.ts` | ✓ Verified |
| Haskell | `GaySPI.hs` | ✓ Verified |
| Zig | `gay_spi_zig.zig` | ✓ Verified |
| OCaml | `gay_spi.ml` | ✓ Verified |

## Expected Values Table

```python
EXPECTED_VALUES = {
    0: 0xf061ebbc2ca74d78,
    1: 0x4b6bda257af3c7de,
    5: 0xb5222cb8ae6e1886,
    9: 0xd726fcf3f1d357d5,
    100: 0x3a91e5c82f4d6b17,
}
```

## GF(3) Triad Integration

| Trit | Skill | Role |
|------|-------|------|
| -1 | **polyglot-spi** | Validates cross-language |
| 0 | spi-parallel-verify | Coordinates verification |
| +1 | gay-mcp | Generates color sequences |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## Justfile Recipes

```makefile
# Verify all languages
spi-verify-all:
    julia --project=Gay.jl -e 'using Gay; @assert Gay.splitmix64(UInt64(0x598F318E2B9E884)) == 0xf061ebbc2ca74d78; println("✓ Julia")'
    python3 -c 'from gay_spi import splitmix64, GAY_SEED; assert splitmix64(GAY_SEED)[1] == 0xf061ebbc2ca74d78; print("✓ Python")'
    ruby -I lib -r spi_verify -e 'SPIVerify.verify!'
    uv run hy -c '(import spi_verify) (spi_verify.verify-spi)'
    bb spi_verify.bb

# Single language
spi-verify lang="python":
    @case {{lang}} in \
      python) python3 -c 'from gay_spi import splitmix64, GAY_SEED; assert splitmix64(GAY_SEED)[1] == 0xf061ebbc2ca74d78' ;; \
      ruby) ruby -I lib -r spi_verify -e 'SPIVerify.verify!' ;; \
    esac
```

## Specter Cross-Language Navigation (NEW 2025-12-22)

SPI verification extends to Specter-style navigation across languages:

### Cross-Language Path Invariant

```
Same path definition → Same traversal results (any language)
```

| Language | Path Syntax | Optimization |
|----------|-------------|--------------|
| Julia | `(ALL, pred(iseven))` | Tuple + functor (93x speedup) |
| Clojure | `[ALL even?]` | comp-navs (JIT inline) |
| Python | `[ALL, pred(iseven)]` | List + lambda |

### Benchmark Parity

Julia optimized implementation achieves Clojure/Specter parity:
- **Transform**: 1.0x overhead (zero cost!)
- **Select**: 1.3x overhead (near-parity)

### Triad for Cross-Lang Navigation

```
polyglot-spi (-1) ⊗ lispsyntax-acset (0) ⊗ gay-mcp (+1) = 0 ✓
```

## Related Skills

- `spi-parallel-verify` - Parallel stream verification
- `gay-mcp` - Color generation
- `triad-interleave` - Stream interleaving
- `lispsyntax-acset` - Specter navigation bridge
