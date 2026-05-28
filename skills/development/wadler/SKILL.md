---
name: wadler-monadic-elegance
description: Write functional code in the style of Philip Wadler, type theorist and monad evangelist. Emphasizes monadic composition, type-driven design, and the deep connection between logic and computation. Use when designing composable abstractions or understanding categorical patterns.
---

# Philip Wadler Style Guide

## Overview

Philip Wadler is a principal designer of Haskell, contributor to Java generics, and the person who brought monads from category theory into practical programming. His famous paper "Propositions as Types" illuminates the deep connection between logic and computation.

## Core Philosophy

> "The essence of functional programming is that programs are built by composing functions."

> "Monads are just monoids in the category of endofunctors."

> "A monad is a way to structure computations."

Wadler sees programming as applied mathematics—types are propositions, programs are proofs, and monads are the universal pattern for composition.

## Design Principles

1. **Types Are Propositions**: A type signature is a theorem; the implementation is its proof.

2. **Monads Everywhere**: IO, Maybe, List, State—all are instances of one pattern.

3. **Parametric Polymorphism**: Generic code that works for any type.

4. **Theorems for Free**: From the type, derive properties the code must have.

## When Writing Code

### Always

- Let types guide your implementation
- Use monadic composition for effects
- Exploit parametricity for correctness
- Derive functions from types systematically
- Prefer point-free style when it aids clarity
- Think in terms of algebraic laws

### Never

- Fight the type system
- Use partial functions without wrapping in Maybe
- Ignore the monad laws
- Mix effects without explicit structure
- Sacrifice correctness for convenience

### Prefer

- `Maybe` over null
- `Either` over exceptions
- Monadic composition over nested callbacks
- Type classes over ad-hoc polymorphism
- Algebraic reasoning over testing alone

## Code Patterns

### The Monad Pattern

```haskell
-- A monad has three components:
-- 1. A type constructor: m a
-- 2. return: a -> m a (inject a value)
-- 3. bind: m a -> (a -> m b) -> m b (sequence computations)

-- Maybe monad: computations that might fail
safeDivide :: Double -> Double -> Maybe Double
safeDivide _ 0 = Nothing
safeDivide x y = Just (x / y)

-- Composition with bind (>>=)
compute :: Double -> Double -> Double -> Maybe Double
compute x y z = safeDivide x y >>= \r -> safeDivide r z

-- Do notation (syntactic sugar for bind)
compute' :: Double -> Double -> Double -> Maybe Double
compute' x y z = do
    r <- safeDivide x y
    safeDivide r z


-- List monad: computations with multiple results
pairs :: [a] -> [b] -> [(a, b)]
pairs xs ys = do
    x <- xs
    y <- ys
    return (x, y)

-- Equivalent to:
pairs' xs ys = xs >>= \x -> ys >>= \y -> return (x, y)

-- Or with list comprehension:
pairs'' xs ys = [(x, y) | x <- xs, y <- ys]


-- IO monad: computations with side effects
greet :: IO ()
greet = do
    putStrLn "What is your name?"
    name <- getLine
    putStrLn ("Hello, " ++ name ++ "!")
```

### The Monad Laws

```haskell
-- Every monad must satisfy three laws:

-- 1. Left identity: return a >>= f  ≡  f a
-- 2. Right identity: m >>= return  ≡  m
-- 3. Associativity: (m >>= f) >>= g  ≡  m >>= (\x -> f x >>= g)

-- These laws ensure composition behaves predictably
-- Violating them leads to subtle bugs

-- Example: verifying Maybe satisfies the laws
-- Left identity:
--   return a >>= f
--   = Just a >>= f
--   = f a ✓

-- Right identity:
--   Just x >>= return
--   = return x
--   = Just x ✓

-- Associativity holds by case analysis on m
```

### Functor and Applicative

```haskell
-- Functor: things you can map over
-- fmap :: (a -> b) -> f a -> f b
-- Law: fmap id = id
-- Law: fmap (f . g) = fmap f . fmap g

incrementAll :: [Int] -> [Int]
incrementAll = fmap (+1)

-- Applicative: functors you can combine
-- pure :: a -> f a
-- (<*>) :: f (a -> b) -> f a -> f b

-- Combine Maybe values
addMaybe :: Maybe Int -> Maybe Int -> Maybe Int
addMaybe mx my = pure (+) <*> mx <*> my
-- addMaybe (Just 3) (Just 4) = Just 7
-- addMaybe Nothing (Just 4) = Nothing


-- The hierarchy: Functor → Applicative → Monad
-- Every Monad is an Applicative
-- Every Applicative is a Functor
```

### Parametric Polymorphism and Theorems for Free

```haskell
-- From the type alone, we can derive properties

-- What can this function possibly do?
mystery :: a -> a
-- It can ONLY be the identity function!
-- It cannot inspect 'a', so it can only return what it received.

-- What about this?
mystery2 :: [a] -> [a]
-- It can reorder, duplicate, or drop elements
-- But it cannot fabricate new 'a' values
-- Therefore: map f . mystery2 = mystery2 . map f

-- This is a "free theorem" - derived purely from the type

-- Practical example:
reverse :: [a] -> [a]
-- Free theorem: map f . reverse = reverse . map f
-- We get this property for free from the type!
```

### Monad Transformers

```haskell
import Control.Monad.Trans.Maybe
import Control.Monad.Trans.State
import Control.Monad.Trans.Class (lift)

-- Combine effects with monad transformers
type App a = MaybeT (StateT Int IO) a

-- MaybeT adds failure
-- StateT adds mutable state
-- IO adds side effects

runApp :: App a -> Int -> IO (Maybe a, Int)
runApp app initialState = runStateT (runMaybeT app) initialState

example :: App String
example = do
    lift $ lift $ putStrLn "Starting..."  -- IO
    lift $ modify (+1)                     -- State
    n <- lift get
    if n > 10
        then return "Big number"
        else MaybeT $ return Nothing       -- Maybe (failure)
```

### Type-Driven Development

```haskell
-- Start with the type, derive the implementation

-- Problem: safely index into a list
-- Type tells us what we need:
safeIndex :: [a] -> Int -> Maybe a

-- Implementation follows from the type:
safeIndex [] _ = Nothing
safeIndex (x:_) 0 = Just x
safeIndex (_:xs) n
    | n < 0     = Nothing
    | otherwise = safeIndex xs (n - 1)


-- Problem: traverse a structure with effects
-- The type guides us completely:
traverse :: (Applicative f) => (a -> f b) -> [a] -> f [b]
traverse _ [] = pure []
traverse f (x:xs) = (:) <$> f x <*> traverse f xs

-- Usage:
-- traverse readFile ["a.txt", "b.txt"] :: IO [String]
-- traverse Just [1, 2, 3] :: Maybe [Int]
```

## Mental Model

Wadler approaches programming by asking:

1. **What is the type?** The type is the specification
2. **What are the laws?** Algebraic properties guide implementation
3. **Is this a known pattern?** Functor, Applicative, Monad, etc.
4. **What theorems are free?** Derive properties from types
5. **Does this compose?** Good abstractions compose cleanly

## Signature Wadler Moves

- Monadic do-notation for sequencing effects
- Free theorems from parametric types
- Monad transformers for combined effects
- Type classes for ad-hoc polymorphism
- Algebraic laws as correctness criteria
- Category theory as design guide
