---
name: free-monad-gen
description: Free Monad Generation Skill (PLUS +1)
version: 1.0.0
---


# Free Monad Generation Skill (PLUS +1)

> Free structure generation from signatures

**Trit**: +1 (PLUS)  
**Color**: #D82626 (Red)  
**Role**: Generator/Creator

## Core Concept

Free monads generate structure from a functor signature:

```haskell
data Free f a 
  = Pure a                    -- Leaf (return)
  | Roll (f (Free f a))       -- Node (bind)
```

**Universal property**: `Free f` is left adjoint to forgetful functor U.

## Dual: Cofree Comonad

```haskell
data Cofree f a = a :< f (Cofree f a)
-- Head (extract) and infinite tail (duplicate)
```

| Free | Cofree |
|------|--------|
| Producer (effects) | Consumer (contexts) |
| Programs | Interpreters |
| Syntax | Semantics |

## Pattern Runs on Matter

```
Pattern (Free) ────runs-on────→ Matter (Cofree)
   ↓                                ↑
 Program                         Environment
   ↓                                ↑
 Effects                         Handlers
```

## Integration with Gay.jl

```julia
# Free monad for color stream generation
struct ColorFree{A}
    tag::Symbol  # :pure or :roll
    value::Union{A, Tuple{UInt64, ColorFree{A}}}
end

# Generate free color structure
function free_color_stream(seed::UInt64, n::Int)
    if n == 0
        ColorFree(:pure, seed)
    else
        next_seed = splitmix64(seed)
        ColorFree(:roll, (seed, free_color_stream(next_seed, n-1)))
    end
end

# Interpret to actual colors
function interpret(free::ColorFree, palette)
    if free.tag == :pure
        return []
    else
        (seed, rest) = free.value
        color = gay_color(seed)
        [color; interpret(rest, palette)]
    end
end
```

## Freer Monad (More Efficient)

```haskell
data Freer f a where
  Pure :: a -> Freer f a
  Impure :: f x -> (x -> Freer f a) -> Freer f a
```

Benefits:
- O(1) bind (vs O(n) for Free)
- Existential continuation
- Better for effect systems

## DSL Generation Pattern

```haskell
-- 1. Define signature functor
data MusicF next
  = Note Pitch Duration next
  | Rest Duration next
  | Chord [Pitch] Duration next
  | Par (Free MusicF ()) (Free MusicF ()) next

-- 2. Free monad gives DSL
type Music = Free MusicF

-- 3. Smart constructors
note :: Pitch -> Duration -> Music ()
note p d = liftF (Note p d ())

-- 4. Programs are data
melody = do
  note C4 quarter
  note E4 quarter
  note G4 half
```

## GF(3) Triads

```
sheaf-cohomology (-1) ⊗ kan-extensions (0) ⊗ free-monad-gen (+1) = 0 ✓
temporal-coalgebra (-1) ⊗ dialectica (0) ⊗ free-monad-gen (+1) = 0 ✓
three-match (-1) ⊗ unworld (0) ⊗ free-monad-gen (+1) = 0 ✓
```

## Commands

```bash
# Generate free structure from signature
just free-gen MusicF

# Interpret free structure
just free-interpret music.free synth

# Generate color stream
just free-color-stream $GAY_SEED 100

# Lift effect to free monad
just free-lift effect
```

## Effect System Integration

```haskell
-- Algebraic effects as free monads
data Effect = 
  | State s
  | Reader r  
  | Writer w
  | Async
  | Error e

type Eff effs = Freer (Union effs)

-- Handlers interpret effects
runState :: s -> Eff (State s ': effs) a -> Eff effs (a, s)
```

## References

- Swierstra, "Data Types à la Carte"
- Kiselyov & Ishii, "Freer Monads, More Extensible Effects"
- Capriotti & Kaposi, "Free Applicatives"



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `category-theory`: 139 citations in bib.duckdb
- `monads`: 13 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 1 (PLUS)
Home: Presheaves
Poly Op: ⊗
Kan Role: Lan_K
Color: #4ECDC4
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.