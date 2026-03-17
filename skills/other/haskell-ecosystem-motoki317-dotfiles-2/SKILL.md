---
name: Haskell Ecosystem
description: This skill should be used when working with Haskell projects, "cabal.project", "stack.yaml", "ghc", "cabal build/test/run", "stack build/test/run", or Haskell language patterns. Provides comprehensive Haskell ecosystem patterns and best practices.
version: 0.1.0
---

# Haskell Ecosystem

## Core Concepts

- **Purity**: Functions have no side effects; same input always produces same output
- **Laziness**: Expressions evaluated only when needed; enables infinite data structures
- **Type inference**: Hindley-Milner; explicit signatures recommended for top-level definitions
- **Monads**: Compose computations with effects (IO, Maybe, Either, State, Reader)
- **Type classes**: Ad-hoc polymorphism (Eq, Ord, Functor, Applicative, Monad)

## Common Type Classes

- `Functor` - `fmap`, `<$>`
- `Applicative` - `<*>`, `pure`
- `Monad` - `>>=`, `return`, do-notation
- `Foldable` - `foldr`, `foldl`, `toList`
- `Traversable` - `traverse`, `sequenceA`
- `Semigroup` - `<>`
- `Monoid` - `mempty`, `mappend`

## Type-Level Programming

```haskell
-- GADTs
{-# LANGUAGE GADTs #-}
data Expr a where
  LitInt  :: Int -> Expr Int
  LitBool :: Bool -> Expr Bool
  Add     :: Expr Int -> Expr Int -> Expr Int

-- Type Families
{-# LANGUAGE TypeFamilies #-}
type family Element c where
  Element [a]     = a
  Element (Set a) = a

-- DataKinds
{-# LANGUAGE DataKinds, KindSignatures #-}
data Nat = Zero | Succ Nat
data Vec (n :: Nat) a where
  VNil  :: Vec 'Zero a
  VCons :: a -> Vec n a -> Vec ('Succ n) a
```

## Monad Transformers (mtl)

```haskell
import Control.Monad.Reader
import Control.Monad.State
import Control.Monad.Except

doSomething :: (MonadReader Config m, MonadState AppState m, MonadError AppError m) => m Result
doSomething = do
  cfg <- ask
  st <- get
  when (invalid cfg) $ throwError InvalidConfig
  pure (compute cfg st)
```

Common transformers: `ReaderT`, `StateT`, `ExceptT`, `WriterT`, `MaybeT`

## Lens (optics)

```haskell
import Control.Lens

data Person = Person { _name :: String, _age :: Int }
makeLenses ''Person

getName p = p ^. name        -- view
setName n p = p & name .~ n  -- set
modifyAge f p = p & age %~ f -- over
```

Operators: `^.` (view), `.~` (set), `%~` (over), `^?` (preview), `^..` (toListOf)

## Cabal File

```cabal
cabal-version: 3.0
name:          my-project
version:       0.1.0.0

common warnings
  ghc-options: -Wall -Wcompat -Wincomplete-record-updates

library
  import:           warnings
  exposed-modules:  MyProject
  build-depends:    base ^>=4.18, text ^>=2.0
  hs-source-dirs:   src
  default-language: GHC2021
```

## Testing

```haskell
-- HSpec
import Test.Hspec
main = hspec $ do
  describe "Calculator" $ do
    it "adds two numbers" $ add 1 2 `shouldBe` 3

-- QuickCheck property
prop_reverseReverse :: [Int] -> Bool
prop_reverseReverse xs = reverse (reverse xs) == xs

-- With HSpec
it "is its own inverse" $ property $
  \xs -> reverse (reverse xs) == (xs :: [Int])
```

## Anti-Patterns

- **Partial functions**: Avoid `head`, `tail`, `fromJust`; use safe alternatives
- **String for text**: Use `Text` or `ByteString` for performance
- **Lazy IO**: Use strict IO or streaming (conduit, pipes) in production
- **Orphan instances**: Use newtype wrappers or define in appropriate modules

## Commands

- `cabal build` / `cabal test` / `cabal run`
- `cabal repl` - Start GHCi
- `stack build` / `stack test` / `stack ghci`
- `hlint src/` - Linter
- `fourmolu -i src/**/*.hs` - Formatter

## Build Tool Choice

- **Stack**: Reproducible builds with Stackage LTS; simpler for beginners
- **Cabal**: Native format for Hackage; better for complex dependency overrides
- **Nix**: Use with haskell.nix or nixpkgs Haskell infrastructure

## Context7 Reference

- Servant: `/haskell-servant/servant`
- HSpec: `/websites/hackage_haskell_package_hspec-2_11_12`
- Optics: `/websites/hackage_haskell_package_optics-0_4_2_1`
