---
name: stdlib-point-at-infinity
description: Guidelines for handling point-at-infinity in stdlib circuit types. Use when working on serialization, public inputs, or cycle_group/biggroup code.
---

# Stdlib Point-at-Infinity Handling

## Two stdlib element types for bn254

- **`element_default::element`** (Ultra arithmetization): Separate `_is_infinity` bool_ct flag. Coordinates can be arbitrary when infinity is set. Has `is_point_at_infinity()` returning `bool_ct`.
- **`goblin_element`** (Mega arithmetization): Represents infinity as `(0,0)` by construction. No separate infinity flag. No `is_point_at_infinity()` method on the circuit type. ECCVM enforces the `(0,0)` convention.
- The alias `element<Builder, Fq, Fr, G>` resolves to one or the other via `IsGoblinBigGroup`.
- Both types have `get_value()` returning a native `affine_element` with `is_point_at_infinity()`.

## cycle_group (Grumpkin) infinity handling

`cycle_group` has `_is_infinity` bool computed from `x^2 + 5*y^2 == 0` (which has no non-trivial solutions in the field, since `p == 2 mod 5`). For `(0,0)` this gives `0 == 0`, so infinity is auto-detected.

**Non-canonical infinity**: `cycle_group` operations (`operator+`, `operator-`, `dbl`, `batch_mul`) can produce points at infinity with non-canonical coordinates (`_is_infinity=true` but `x,y != 0,0`). This happens because the arithmetic uses `conditional_assign` to avoid division by zero -- the "real" coordinates are garbage when the infinity flag is set.

**Observation boundaries**: Canonicalization to `(0,0)` is deferred to these boundaries:
- `StdlibCodec::serialize_to_fields` -- canonicalizes `grumpkin_commitment` via `conditional_assign`
- `cycle_group::set_public` -- canonicalizes before exposing as public inputs
- `cycle_group::operator==` and `assert_equal` -- handles infinity comparison

## StdlibCodec::serialize_to_fields (field_conversion.hpp)

- **grumpkin_commitment**: Canonicalizes infinity to `(0,0)` via `conditional_assign`. This IS needed because the `IPA::accumulate` -> `full_verify_recursive` path computes `G_zero_1 + G_zero_2 * alpha` using `cycle_group` arithmetic, which can produce non-canonical infinity when a malicious prover sends both `G_zero` values as `(0,0)`.
- **bn254_commitment**: Allows canonical `(0,0)` infinity; asserts (`BB_ASSERT`) that infinity points have zero coordinates. All existing code paths (public inputs, transcript) produce canonical `(0,0)` infinity, so the assert is a safety guard against misuse. No canonicalization is performed (unlike `grumpkin_commitment`), since there are no available code paths that produce non-canonical bn254 infinity.

## Analyzing whether canonicalization is needed

Trace whether the value comes from:

1. **Deserialization** (from public inputs via `reconstruct_from_public`, or from transcript via `receive_from_prover`): Coordinates are already canonical `(0,0)` for infinity. Canonicalization is a no-op.
2. **cycle_group arithmetic** (`operator+`, `operator-`, `dbl`, `batch_mul`): Coordinates may be non-canonical when `_is_infinity` is true. Canonicalization IS needed.

Key production paths for grumpkin commitments through `serialize_to_fields`:
- **IPA `add_claim_to_hash_buffer`** (verifier side): Commitment is deserialized from public inputs -> already canonical.
- **IPA `accumulate` hashing of `G_zero`**: `G_zero` is deserialized from transcript -> already canonical.
- **IPA `full_verify_recursive`**: Accumulated commitment is the result of cycle_group arithmetic (`G_zero_1 + G_zero_2 * alpha`) -> may be non-canonical if infinity -> canonicalization needed.
- **VK hashing** (`flavor.hpp` `to_field_elements`/`hash_with_origin_tagging`): Commitments are deserialized from fields -> already canonical.

## Recursive verification and malicious provers

For recursive verifier circuits, the circuit must be **constructible** even with malicious witness values (it just won't be satisfiable). This means:
- Do NOT use `BB_ASSERT` on values a malicious prover can control -- it would crash circuit construction.
- Use `conditional_assign` canonicalization instead, which produces correct circuit constraints regardless of witness values.
- `BB_ASSERT` is appropriate for invariants that hold across all existing code paths (e.g., `bn254_commitment` in `serialize_to_fields` asserts canonical `(0,0)` form for infinity, since all paths that can reach it produce canonical infinity).

## Common bug patterns to watch for

These patterns have caused repeated bugs across biggroup, cycle_group, ECCVM, AVM, and ECDSA:

### 1. Representation mismatch: internal sentinel vs `(0,0)`
BB's native `affine_element` uses an internal sentinel for infinity (MSB set on the x coordinate's raw representation, not a valid field element). Noir, AVM, and the transcript convention use `(0,0)`. Any code that reads raw coordinates without checking `is_point_at_infinity()` (or without calling `get_standard_form()` on stdlib types) will see sentinel values, not `(0,0)`. Always use the standard-form convention `(0,0)` at component boundaries.

### 2. Forgetting to propagate the infinity flag through conditional operations
When doing `conditional_assign` or `conditional_select` on points, both the coordinates AND the `_is_infinity` flag must be selected. Multiple ECDSA and biggroup bugs came from selecting x/y but leaving `_is_infinity` unchanged.

### 3. Incomplete addition formulas crash on infinity
Performance-optimized ECC (chain_add, Montgomery ladder) assumes inputs are never infinity and never equal. When infinity appears as an intermediate value, these formulas divide by zero or produce wrong results. If a code path can encounter infinity mid-computation, use complete addition (`operator+`) instead of `chain_add_start`/`chain_add`/`chain_add_end`. This costs ~2% more gates but is correct.

### 4. Constructor and validation bypasses
Constructors that accept a direct `is_infinity` flag can bypass on-curve validation (a point with `is_infinity=true` but `x,y != 0` passes `validate_on_curve` because the check is skipped for infinity). The 4-argument biggroup constructor with explicit infinity flag is now private. Prefer the 2-argument `(x, y)` constructor which auto-detects infinity from `x == 0 && y == 0`.

### 5. Forgetting to canonicalize before comparison or hashing
`cycle_group::operator==` and `assert_equal` handle infinity correctly, but raw coordinate comparison does not. Before comparing or hashing point coordinates, ensure infinity points have canonical `(0,0)` coordinates. The observation boundary pattern (serialize_to_fields, set_public, operator==) exists for this reason.
