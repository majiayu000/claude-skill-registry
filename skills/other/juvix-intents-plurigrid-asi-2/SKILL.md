---
name: juvix-intents
description: "Juvix intent-centric language for Anoma with Geb compilation and GF(3) typed resources"
source: anoma/juvix (504 stars)
license: GPL-3.0
trit: +1
gf3_conserved: true
repo: hatchery_repos/plurigrid__juvix
---

# Juvix Intents (+1)

> Intent-centric language compiling to Geb categorical semantics

**Trit**: +1 (PLUS - generative)
**Compiles to**: Geb → Vampir → ZK proofs

## Overview

Juvix is Anoma's **intent-centric programming language**:

```
Juvix Source → Core → Geb Morphisms → Vampir IR → ZK Circuit
     ↑            ↑          ↑            ↑
   Types      Normalize   Categorify   Arithmetize
```

## Obstruction Types

```juvix
module Obstruction;

-- GF(3) trit type
type GF3 := Minus | Ergodic | Plus;

-- Trit arithmetic (mod 3)
add : GF3 -> GF3 -> GF3
add Minus Minus := Plus      -- (-1) + (-1) = +1 (mod 3)
add Minus Ergodic := Minus   -- (-1) + 0 = -1
add Minus Plus := Ergodic    -- (-1) + (+1) = 0
add Ergodic x := x           -- 0 + x = x
add Plus Minus := Ergodic    -- (+1) + (-1) = 0
add Plus Ergodic := Plus     -- (+1) + 0 = +1
add Plus Plus := Minus;      -- (+1) + (+1) = -1 (mod 3)

-- Obstruction from Bumpus decomposition failure
type Obstruction := mkObstruction {
  sexp : ByteArray;          -- S-expression witness
  trit : GF3;                -- Triadic charge
  h1Class : Nat;             -- Cohomology class (>0 = obstruction)
  treewidth : Nat;           -- Exceeded threshold
  color : Word64;            -- Gay.jl deterministic color
  seed : Word64              -- SplitMix64 seed
};

-- Check if decomposition failed
isObstruction : Obstruction -> Bool
isObstruction obs := h1Class obs > 0;

-- VCG externality payment
vcgExternality : Obstruction -> Nat
vcgExternality obs :=
  let baseCost := 1000000    -- 0.001 APT
      multiplier := 10000    -- 100%
  in (h1Class obs) * baseCost * multiplier / 10000;
```

## Intent Types

```juvix
module Intent;

import Obstruction;

-- Resource type (what can be nullified/committed)
type Resource :=
  | ObstructionRes Obstruction
  | TokenRes Token
  | ReceiptRes ChainId ByteArray;

-- Intent: preference over state transitions
type Intent := mkIntent {
  owner : Address;
  nullify : List Resource;   -- Resources to consume
  commit : List Resource;    -- Resources to produce
  constraints : List Constraint
};

-- Constraint on intent satisfaction
type Constraint :=
  | VcgPayment Nat           -- Minimum VCG payment
  | GF3Balance               -- Sum of trits must be 0 (mod 3)
  | SpectralGap Float;       -- Minimum spectral gap preserved

-- Cross-chain pass intent
passObstruction : Address -> Obstruction -> ChainId -> Intent
passObstruction owner obs target :=
  mkIntent {
    owner := owner;
    nullify := [ObstructionRes obs];
    commit := [ReceiptRes target (hash obs)];
    constraints := [VcgPayment (vcgExternality obs), GF3Balance]
  };
```

## Compilation to Geb

```juvix
module GebCompile;

import Intent;
import Geb;

-- Compile intent to Geb morphism
compileIntent : Intent -> Geb.Morphism
compileIntent intent :=
  -- Intent = pair of (nullify, commit)
  -- Nullify: inject-left to void (consume)
  -- Commit: inject-right from void (produce)
  Geb.pair
    (compileNullify (nullify intent))
    (compileCommit (commit intent));

-- Compile nullification
compileNullify : List Resource -> Geb.Morphism
compileNullify [] := Geb.terminal Geb.so1
compileNullify (r :: rs) :=
  Geb.pair
    (Geb.injectLeft (compileResource r) Geb.so0)
    (compileNullify rs);

-- Compile commitment
compileCommit : List Resource -> Geb.Morphism
compileCommit [] := Geb.init Geb.so0
compileCommit (r :: rs) :=
  Geb.pair
    (Geb.injectRight Geb.so0 (compileResource r))
    (compileCommit rs);

-- Resource to Geb type
compileResource : Resource -> Geb.Object
compileResource (ObstructionRes obs) :=
  Geb.prod
    (Geb.prod Geb.so1 Geb.so1)   -- (sexp, trit)
    (Geb.prod Geb.so1 Geb.so1);  -- (h1Class, color)
compileResource (TokenRes tok) := Geb.so1;
compileResource (ReceiptRes _ _) := Geb.so1;
```

## Free Monad for Obstruction Game

```juvix
module ObstructionMonad;

import Obstruction;

-- Functor for obstruction game
type ObstructionF (a : Type) :=
  | NoObstruction a                    -- Decomposition succeeded
  | WithObstruction Obstruction a;     -- Decomposition failed → H¹ ≠ 0

-- Free monad
type Free (f : Type -> Type) (a : Type) :=
  | Pure a
  | Roll (f (Free f a));

-- Obstruction monad = Free ObstructionF
ObstructionMonad : Type -> Type
ObstructionMonad := Free ObstructionF;

-- Attempt decomposition (creates obstruction if tw > threshold)
attemptDecomposition : ByteArray -> Nat -> Word64 -> ObstructionMonad Unit
attemptDecomposition sexp tw seed :=
  if tw <= 3
  then Pure unit
  else 
    let h1 := tw - 3
        trit := toGF3 ((seed `xor` (natToWord64 tw)) `mod` 3)
        color := gayColor seed tw
        obs := mkObstruction sexp trit h1 tw color seed
    in Roll (WithObstruction obs (Pure unit));

-- Bind preserves spectral gap
bind : ObstructionMonad a -> (a -> ObstructionMonad b) -> ObstructionMonad b
bind (Pure a) k := k a
bind (Roll (NoObstruction rest)) k := Roll (NoObstruction (bind rest k))
bind (Roll (WithObstruction obs rest)) k := 
  Roll (WithObstruction obs (bind rest k));
```

## Spectral Gap Tracking

```juvix
module SpectralMonad;

-- Monad that tracks spectral gap through composition
type SpectralFree (f : Type -> Type) (a : Type) := mkSpectralFree {
  computation : Free f a;
  spectralGap : Float
};

-- Bind propagates minimum gap
bindSpectral : SpectralFree f a -> (a -> SpectralFree f b) -> SpectralFree f b
bindSpectral sf k :=
  let result := bind (computation sf) (\a -> computation (k a))
      newGap := min (spectralGap sf) (gapOf result)
  in mkSpectralFree result newGap;

-- Ramanujan bound for d=3
ramanujanBound : Float
ramanujanBound := 3.0 - 2.0 * sqrt 2.0;  -- ≈ 0.172

-- Check if spectral gap preserved
gapPreserved : SpectralFree f a -> Bool
gapPreserved sf := spectralGap sf >= ramanujanBound;
```

## GF(3) Type-Level Conservation

```juvix
module GF3Types;

-- Type-level GF(3) for compile-time conservation
type Trit := T_Minus | T_Ergodic | T_Plus;

-- Type-level addition (mod 3)
type family TritAdd (a : Trit) (b : Trit) : Trit where
  TritAdd T_Minus T_Plus := T_Ergodic
  TritAdd T_Plus T_Minus := T_Ergodic
  TritAdd T_Ergodic x := x
  TritAdd x T_Ergodic := x
  TritAdd T_Plus T_Plus := T_Minus
  TritAdd T_Minus T_Minus := T_Plus;

-- Typed resource with trit charge
type TResource (t : Trit) := mkTResource {
  payload : Resource;
  trit : GF3  -- Runtime trit must match type-level
};

-- Balanced transaction: trits sum to 0
type BalancedTx :=
  forall (a b c : Trit).
  TritAdd a (TritAdd b c) == T_Ergodic =>
  Triple (TResource a) (TResource b) (TResource c);
```

## CLI Commands

```bash
# Compile Juvix to Geb
juvix compile intent.juvix --target geb

# Type check with GF(3) verification
juvix typecheck --gf3-check module.juvix

# Generate Vampir circuit
juvix compile intent.juvix --target vampir

# Run obstruction monad
juvix eval "attemptDecomposition sexp 5 0x42"

# Verify spectral gap preservation
juvix verify --spectral-gap intent.juvix
```

## GF(3) Triads

```
juvix-intents (+1) ⊗ anoma-intents (0) ⊗ solver-fee (-1) = 0 ✓
  └─ Compiles DSL        └─ Routes          └─ Extracts fee

juvix-intents (+1) ⊗ geb (+1) ⊗ sheaf-cohomology (-1) = 1 ✗ (need -1)
  → Add intent-sink (-1): juvix (+1) ⊗ geb (+1) ⊗ intent-sink (-1) ⊗ sheaf (-1) ...

juvix-intents (+1) ⊗ open-games (0) ⊗ ramanujan-expander (-1) = 0 ✓
  └─ Type-level gap      └─ Coordinates     └─ Validates bound
```

## Integration with Obstruction Hot Potato

```juvix
-- Full hot potato game in Juvix
module HotPotato;

import Obstruction;
import Intent;
import ObstructionMonad;

-- Player state
type Player := mkPlayer {
  address : Address;
  stake : Nat;
  obstructions : List Obstruction;
  alive : Bool
};

-- Game action
type Action :=
  | AttemptDecomposition ByteArray Nat
  | PassObstruction Address Nat
  | EndRound;

-- Game monad: State + Obstruction effects
type GameMonad := StateT (List Player) ObstructionMonad;

-- Execute action
executeAction : Action -> GameMonad Unit
executeAction (AttemptDecomposition sexp tw) := do
  obs <- lift (attemptDecomposition sexp tw (currentSeed ()))
  when (isObstruction obs) (addObstructionToPlayer obs)
executeAction (PassObstruction target idx) := do
  player <- getCurrentPlayer
  obs <- getObstruction player idx
  vcg <- pure (vcgExternality obs)
  transferPayment player target vcg
  moveObstruction player target idx
executeAction EndRound := do
  players <- get
  deadPlayers <- filterM hasNegativeUtility players
  mapM_ slashStake deadPlayers
  verifyGF3Conservation;
```

## References

- **anoma/juvix** - https://github.com/anoma/juvix (504 stars)
- **anoma/geb** - Categorical compilation target
- **Juvix docs** - https://docs.juvix.org
- **Bumpus arXiv:2402.00206** - Decomposition theory
- **Roughgarden CS364A** - VCG mechanism

---

**Trit**: +1 (PLUS - generative)
**Key Property**: Intent DSL with type-level GF(3) conservation
