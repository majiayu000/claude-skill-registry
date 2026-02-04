---
name: pickles-field-conventions
description: Field naming conventions and usage patterns in mina's pickles. Use when confused about Tick/Tock/Fp/Fq/Step/Wrap naming or how fields interact.
---

# Pickles Field Naming & Usage Conventions

## The Pasta Curves

Both curves: y² = x³ + 5

| Curve | Base Field | Scalar Field |
|-------|------------|--------------|
| **Pallas** | Fp (smaller) | Fq |
| **Vesta** | Fq (larger) | Fp |

The cycle: `Pallas.ScalarField = Vesta.BaseField = Fq` and vice versa.

**Source:** `mina/src/lib/crypto/kimchi_backend/pasta/basic/kimchi_pasta_basic.ml:73-74`
```ocaml
module Fp = Kimchi_pasta_snarky_backend.Vesta_based_plonk.Field
module Fq = Kimchi_pasta_snarky_backend.Pallas_based_plonk.Field
```

---

## Backend Definitions

**Source:** `mina/src/lib/pickles/backend/backend.ml`
```ocaml
module Tick = struct
  include Kimchi_backend.Pasta.Vesta_based_plonk
  module Inner_curve = Kimchi_backend.Pasta.Pasta.Pallas
end

module Tock = struct
  include Kimchi_backend.Pasta.Pallas_based_plonk
  module Inner_curve = Kimchi_backend.Pasta.Pasta.Vesta
end
```

**Source:** `mina/src/lib/crypto/kimchi_backend/pasta/vesta_based_plonk.ml:4-5`
```ocaml
module Field = Fp
module Curve = Vesta
```

**Source:** `mina/src/lib/crypto/kimchi_backend/pasta/pallas_based_plonk.ml:4-5`
```ocaml
module Field = Fq
module Curve = Pallas
```

---

## Master Mapping Table

| Circuit | Backend | Circuit Field | IPA Curve | Inner Curve |
|---------|---------|---------------|-----------|-------------|
| **Tick/Step** | Vesta_based_plonk | **Fp** | Vesta | Pallas |
| **Tock/Wrap** | Pallas_based_plonk | **Fq** | Pallas | Vesta |

- **Circuit field** = IPA curve's scalar field (where polynomial coefficients live)
- **Inner curve** = curve whose points can be represented natively (base field = circuit field)

---

## Our Implementation Mapping

| Mina | Ours |
|------|------|
| `Fp` / `Tick.Field` / `Vesta_based_plonk.Field` | `Pallas.BaseField` |
| `Fq` / `Tock.Field` / `Pallas_based_plonk.Field` | `Vesta.BaseField` |
| `Tick.Inner_curve` (Pallas points) | `Pallas.G` |
| `Tock.Inner_curve` (Vesta points) | `Vesta.G` |
| `Shifted_value.Type1` | `Type1 f` |
| `Shifted_value.Type2` | `Type2 f b` |

---

## Type1 vs Type2 Shifted Values

**Source:** `mina/src/lib/crypto/plonkish_prelude/shifted_value.ml`

**Type1** (lines 98-149): Single field element
```ocaml
type 'f t = Shifted_value of 'f
(* t = (s - 2^n - 1) / 2, so s = 2*t + 2^n + 1 *)
```

**Type2** (lines 151-211): For when scalar field > circuit field
```ocaml
(* Comment at line 151-161: encode scalar s as (s >> 1, s & 1) *)
type 'f t = Shifted_value of 'f
```

| Circuit | Other Field Size | Use |
|---------|------------------|-----|
| **Step** (Fp native) | Fq > Fp | **Type2** |
| **Wrap** (Fq native) | Fp < Fq | **Type1** |

---

## Poseidon / Sponge Operations

**All sponge operations happen in native circuit field.** Foreign field elements are absorbed via their Type1/Type2 representation.

**Source:** `mina/src/lib/pickles/step_verifier.ml:60-69`
```ocaml
let absorb sponge ty t =
  absorb
    ~absorb_field:(fun x -> Sponge.absorb sponge (`Field x))
    ~g1_to_field_elements:Inner_curve.to_field_elements
    ~absorb_scalar:(fun (x, (b : Boolean.var)) ->
      Sponge.absorb sponge (`Field x) ;
      Sponge.absorb sponge (`Bits [ b ]) )
    ...
```

When absorbing a Type2 scalar `{sDiv2, sOdd}`:
- `sDiv2` absorbed as native field element
- `sOdd` absorbed as bit

**No foreign field arithmetic** — the Type2 split is already native field elements.

---

## Deferred Values Pattern

Challenges are computed **outside** the circuit, passed in as witness values.

**Source:** `mina/src/lib/pickles/wrap_deferred_values.ml:128-166`
```ocaml
let absorb, squeeze =
  let open Tick_field_sponge.Bits in
  let sponge =
    let s = create Tick_field_sponge.params in
    absorb s (Digest.Constant.to_tick_field proof_state.sponge_digest_before_evaluations) ;
    s
  in
  ...
in
...
let xi_chal = squeeze () in
let xi = sc xi_chal in
let r_chal = squeeze () in
let r = sc r_chal in
```

This happens **outside** any circuit. Results become `deferred_values` passed into the verification circuit.

---

## Poseidon Parameters

**Source:** `mina/src/lib/crypto/kimchi_backend/pasta/basic/kimchi_pasta_basic.ml:138-142`
```ocaml
let poseidon_params_fp =
  Kimchi_pasta_snarky_backend.Vesta_based_plonk.poseidon_params

let poseidon_params_fq =
  Kimchi_pasta_snarky_backend.Pallas_based_plonk.poseidon_params
```

| Params | Field | Used By |
|--------|-------|---------|
| `poseidon_params_fp` | Fp | Tick/Step circuits |
| `poseidon_params_fq` | Fq | Tock/Wrap circuits |

**Source:** `vendor/proof-systems/poseidon/src/pasta/fp_kimchi.rs` — params over `mina_curves::pasta::Fp`
**Source:** `vendor/proof-systems/poseidon/src/pasta/fq_kimchi.rs` — params over `mina_curves::pasta::Fq`

---

## Quick Reference

**"What field am I in?"**

| You see... | Circuit field is... |
|------------|---------------------|
| `Tick`, `Step`, `Vesta_based_plonk` | Fp |
| `Tock`, `Wrap`, `Pallas_based_plonk` | Fq |
| `Inner_curve = Pallas` | Fp (Pallas base field) |
| `Inner_curve = Vesta` | Fq (Vesta base field) |
| `Type2` shifted values | You're in Step (Fp), other field is Fq |
| `Type1` shifted values | You're in Wrap (Fq), other field is Fp |
