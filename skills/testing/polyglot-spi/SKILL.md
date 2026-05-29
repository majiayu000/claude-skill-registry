---
name: polyglot-spi
description: Cross-Language Strong Parallelism Invariance Verification
version: 1.0.0
---


# polyglot-spi

> Cross-Language Strong Parallelism Invariance Verification

**Version**: 1.0.0  
**Trit**: -1 (Validator - verifies cross-language consistency)  
**Bundle**: verification  

## Overview

Polyglot-SPI verifies that the SPI (Strong Parallelism Invariance) seed `0xf061ebbc2ca74d78` produces identical color sequences across all supported languages. This ensures deterministic parallel execution regardless of runtime.

## The SPI Invariant

```
GAY_SEED = 0x598F318E2B9E884
splitmix64(GAY_SEED) → 0xf061ebbc2ca74d78 (index 0)

This value MUST be identical in:
- Julia (Gay.jl)
- Rust (gay-rs, tf-moose)
- Python (gay_spi.py)
- TypeScript (eg-walker)
- Clojure (spi.cljd)
- Haskell (GaySPI.hs)
- Go (gay-go)
- Zig (gay_spi_zig.zig)
- OCaml (gay_spi.ml)
- Unison (gay.u)
- Common Lisp (slime)
- Scheme (geiser-chicken)
- Babashka (gay_spi_sci.bb)
```

## Capabilities

### 1. verify-all-languages

Run SPI verification across all implementations.

```bash
#!/bin/bash
# spi-galois-test.sh

REF_0="0xf061ebbc2ca74d78"

echo "=== SPI Cross-Language Verification ==="

# Julia
julia --project=Gay.jl -e \
  'using Gay; @assert splitmix64(GAY_SEED) == 0xf061ebbc2ca74d78'
echo "✓ Julia"

# Python
python3 -c \
  'from gay_spi import splitmix64, GAY_SEED; assert splitmix64(GAY_SEED) == 0xf061ebbc2ca74d78'
echo "✓ Python"

# Rust
cargo test --package gay-rs spi_invariant
echo "✓ Rust"

# Go
go test -run TestSPIInvariant ./gay-go/...
echo "✓ Go"

# ... (all 15+ languages)

echo "=== All languages verified ==="
```

### 2. generate-verification-suite

Generate test files for a new language.

```python
from polyglot_spi import generate_tests

generate_tests(
    language="kotlin",
    output_path="gay_spi.kt",
    seed=0x598F318E2B9E884,
    expected_values={
        0: 0xf061ebbc2ca74d78,
        5: 0xb5222cb8ae6e1886,
        9: 0xd726fcf3f1d357d5
    }
)
```

### 3. splitmix64-reference

Canonical SplitMix64 implementation for comparison.

```python
def splitmix64(state: int) -> tuple[int, int]:
    """
    Reference SplitMix64 implementation.
    Returns (next_state, output_value).
    """
    state = (state + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    return state, (z ^ (z >> 31)) & 0xFFFFFFFFFFFFFFFF

# Verify
GAY_SEED = 0x598F318E2B9E884
state, value = splitmix64(GAY_SEED)
assert value == 0xf061ebbc2ca74d78
```

### 4. color-sequence-verify

Verify full color sequences match across languages.

```python
def verify_color_sequence(n: int = 100) -> bool:
    """
    Generate n colors in each language and compare.
    """
    reference = julia_generate_colors(n)
    
    for lang in ['python', 'rust', 'go', 'typescript']:
        colors = generate_colors(lang, n)
        for i, (ref, actual) in enumerate(zip(reference, colors)):
            if ref != actual:
                raise AssertionError(
                    f"Mismatch at index {i}: {lang} produced {actual}, expected {ref}"
                )
    
    return True
```

### 5. trit-sequence-verify

Verify GF(3) trit sequences are identical.

```python
def verify_trit_sequence(n: int = 1000) -> bool:
    """
    Trits must sum to 0 mod 3 for every consecutive triple.
    """
    trits = generate_trits(n, seed=0xf061ebbc2ca74d78)
    
    for i in range(0, n - 2, 3):
        triple_sum = trits[i] + trits[i+1] + trits[i+2]
        if triple_sum % 3 != 0:
            raise AssertionError(f"GF(3) violation at index {i}")
    
    return True
```

## Language Implementations

| Language | File | Status |
|----------|------|--------|
| Julia | `Gay.jl/src/kernels.jl` | ✓ Reference |
| Python | `gay_spi.py` | ✓ Verified |
| Rust | `gay-rs/src/lib.rs` | ✓ Verified |
| Go | `gay-go/gay.go` | ✓ Verified |
| TypeScript | `eg-walker/src/gay.ts` | ✓ Verified |
| Haskell | `gay-birb-hs/src/GaySPI.hs` | ✓ Verified |
| Clojure | `jrpn-cljd/src/gay/spi.cljd` | ✓ Verified |
| Babashka | `gay_spi_sci.bb` | ✓ Verified |
| Zig | `gay_spi_zig.zig` | ✓ Verified |
| OCaml | `gay_spi.ml` | ✓ Verified |
| Unison | `gay.u` | ✓ Verified |
| Swift | `gay_spi_swift.swift` | ✓ Verified |
| Dafny | `spi_galois.dfy` | ✓ Proven |

## GF(3) Triad Integration

| Trit | Skill | Role |
|------|-------|------|
| -1 | **polyglot-spi** | Validates cross-language |
| 0 | spi-parallel-verify | Coordinates verification |
| +1 | gay-mcp | Generates color sequences |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## Expected Values Table

```python
EXPECTED_VALUES = {
    0: 0xf061ebbc2ca74d78,
    1: 0x4b6bda257af3c7de,
    2: 0x89a7d3e2c5b91f4a,
    5: 0xb5222cb8ae6e1886,
    9: 0xd726fcf3f1d357d5,
    100: 0x3a91e5c82f4d6b17,
    1000: 0x7c8f2a1d5e3b4690
}
```

## Configuration

```yaml
# polyglot-spi.yaml
verification:
  seed: 0x598F318E2B9E884
  expected_0: 0xf061ebbc2ca74d78
  sequence_length: 1000
  
languages:
  - julia
  - python
  - rust
  - go
  - typescript
  - haskell
  - clojure

parallel:
  max_workers: 8
  timeout_seconds: 30
```

## Justfile Recipes

```makefile
# Verify all languages
spi-verify-all:
    ./spi-galois-test.sh

# Verify specific language
spi-verify lang="python":
    python3 -c 'from gay_spi import verify_spi; verify_spi()'

# Generate test suite for new language
spi-generate-tests lang="kotlin":
    python3 -c 'from polyglot_spi import generate_tests; generate_tests("{{lang}}")'
```

## Related Skills

- `spi-parallel-verify` - Parallel stream verification
- `gay-mcp` - Color generation
- `triad-interleave` - Stream interleaving



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `polynomial-functors`: 8 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.