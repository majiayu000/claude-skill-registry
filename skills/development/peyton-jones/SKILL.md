---
name: peyton-jones-practical-haskell
description: Write functional code in the style of Simon Peyton Jones, lead architect of GHC. Emphasizes practical laziness, compiler-friendly code, and making functional programming work in the real world. Use when writing performant Haskell or understanding evaluation strategies.
---

# Simon Peyton Jones Style Guide

## Overview

Simon Peyton Jones is the principal architect of the Glasgow Haskell Compiler (GHC) and has spent decades making functional programming practical. He bridges the gap between theory and implementation, showing that pure functional programming can be efficient.

## Core Philosophy

> "Laziness keeps you honest."

> "Purity is the key to reasoning about programs."

> "The best programs are written by people who know what the compiler will do."

SPJ believes that laziness and purity, while seeming like constraints, actually unlock powerful reasoning and optimization opportunities.

## Design Principles

1. **Laziness by Default**: Evaluate only what's needed, when it's needed.

2. **Purity Enables Optimization**: The compiler can transform pure code freely.

3. **Types Prevent Bugs**: Strong static typing catches errors at compile time.

4. **Understand the Runtime**: Know how your code executes to write it well.

## When Writing Code

### Always

- Understand strictness and laziness in your code
- Use bang patterns when strictness matters
- Profile before optimizing
- Write small, composable functions
- Let the compiler inline and specialize
- Use Core output to understand performance

### Never

- Build up large lazy thunks accidentally
- Ignore space leaks
- Fight the garbage collector
- Assume laziness is always good (or bad)
- Micro-optimize without profiling

### Prefer

- Strict data fields for accumulators
- Fusion-friendly operations (map, filter, fold)
- Stream processing over building lists
- Newtypes for zero-cost abstraction
- GHC pragmas for performance hints

## Code Patterns

### Understanding Laziness

```haskell
-- Lazy: this list is never fully in memory
naturals :: [Integer]
naturals = [1..]

-- Take only what you need
firstTen = take 10 naturals  -- [1..10]

-- Infinite data structures work!
fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

fib100 = fibs !! 100  -- Computes only what's needed


-- BUT: laziness can cause space leaks
-- BAD: builds up a chain of thunks
badSum :: [Int] -> Int
badSum = foldl (+) 0
-- badSum [1,2,3] builds: ((0+1)+2)+3 as thunks!

-- GOOD: strict left fold
goodSum :: [Int] -> Int
goodSum = foldl' (+) 0
-- Forces evaluation at each step

import Data.List (foldl')
```

### Strictness Annotations

```haskell
{-# LANGUAGE BangPatterns #-}

-- Bang patterns force evaluation
strictSum :: [Int] -> Int
strictSum = go 0
  where
    go !acc []     = acc      -- !acc is strict
    go !acc (x:xs) = go (acc + x) xs

-- Strict data fields
data Point = Point !Double !Double
-- Fields are evaluated when Point is constructed

-- Versus lazy (default):
data LazyPoint = LazyPoint Double Double
-- Fields can be thunks


-- UNPACK for removing indirection
data Vec3 = Vec3 {-# UNPACK #-} !Double
                 {-# UNPACK #-} !Double
                 {-# UNPACK #-} !Double
-- Stores three doubles directly, no pointers
```

### Fusion and Deforestation

```haskell
-- GHC can fuse pipelines to avoid intermediate lists

-- This looks like it builds 3 lists:
result = sum . map (*2) . filter even $ [1..1000000]

-- But GHC fuses it into a single loop!
-- No intermediate lists are allocated

-- Write in fusion-friendly style:
-- Use map, filter, foldr, concatMap, etc.
-- Avoid: length, (!!), reverse in hot paths


-- The RULES pragma enables fusion
{-# RULES
"map/map" forall f g xs. map f (map g xs) = map (f . g) xs
"map/filter" forall f p xs. 
    map f (filter p xs) = foldr (\x ys -> if p x then f x : ys else ys) [] xs
#-}

-- GHC's list fusion uses foldr/build:
-- build (\c n -> ... c ... n ...) >>= foldr c n
-- fuses to: ... c ... n ...
```

### Newtypes for Zero-Cost Abstraction

```haskell
-- newtype has no runtime overhead
newtype UserId = UserId Int
    deriving (Eq, Ord, Show)

newtype Email = Email String
    deriving (Eq, Show)

-- Type safety with zero cost
createUser :: UserId -> Email -> User
createUser uid email = ...

-- Cannot accidentally swap arguments!
-- createUser someEmail someUserId  -- Type error!


-- GeneralizedNewtypeDeriving for free instances
{-# LANGUAGE GeneralizedNewtypeDeriving #-}

newtype Money = Money Int
    deriving (Eq, Ord, Num, Show)

-- Now you can do: Money 100 + Money 50 = Money 150
```

### Monomorphism and Specialization

```haskell
-- Polymorphic code has overhead (dictionary passing)
genericSum :: Num a => [a] -> a
genericSum = foldl' (+) 0

-- SPECIALIZE to remove overhead for known types
{-# SPECIALIZE genericSum :: [Int] -> Int #-}
{-# SPECIALIZE genericSum :: [Double] -> Double #-}

-- Or use INLINABLE to let GHC specialize at use sites
{-# INLINABLE genericSum #-}

-- For hot code, monomorphic is faster
intSum :: [Int] -> Int
intSum = foldl' (+) 0
```

### Understanding Core

```haskell
-- Use -ddump-simpl to see GHC Core output
-- Core shows what GHC actually compiles

-- Example: does this fuse?
test :: [Int] -> Int
test = sum . map (+1) . filter even

-- Compile with: ghc -O2 -ddump-simpl Test.hs
-- Look for single recursive function (fused)
-- vs multiple (not fused)


-- Key Core concepts:
-- - let: allocation
-- - case: evaluation (forcing)
-- - λ: function
-- - Type applications: @Int, @Bool

-- Fewer lets = less allocation
-- Strategic cases = proper strictness
```

### Efficient Recursion

```haskell
-- Tail recursion with accumulator
factorial :: Integer -> Integer
factorial n = go n 1
  where
    go 0 !acc = acc
    go n !acc = go (n-1) (n*acc)

-- Worker/wrapper transformation
-- Expose strict worker, wrap with friendly interface
{-# INLINE factorial #-}


-- Avoid: naive recursion with growing stack
badFactorial :: Integer -> Integer
badFactorial 0 = 1
badFactorial n = n * badFactorial (n-1)
-- Builds: n * (n-1) * (n-2) * ... * 1 as thunks


-- Use continuation-passing for complex control flow
data Tree a = Leaf a | Node (Tree a) (Tree a)

sumTree :: Num a => Tree a -> a
sumTree t = go t id
  where
    go (Leaf x) k = k x
    go (Node l r) k = go l (\sl -> go r (\sr -> k (sl + sr)))
```

## Mental Model

SPJ approaches Haskell by asking:

1. **What gets evaluated when?** Understand lazy vs strict
2. **Where are the thunks?** Potential space leaks
3. **Will this fuse?** Intermediate structures eliminated?
4. **What does Core look like?** The ground truth
5. **Is this inlined?** Key for performance

## Signature SPJ Moves

- Bang patterns for strategic strictness
- UNPACK for unboxed fields
- INLINE/INLINABLE for specialization
- Fusion-friendly combinators
- Worker/wrapper pattern
- Core inspection for optimization
