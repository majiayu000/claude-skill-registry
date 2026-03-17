---
name: lang-haskell-dev
description: Foundational Haskell patterns covering pure functional programming, type system, type classes, monads, and common idioms. Use when writing Haskell code, understanding pure functions, working with Maybe/Either, leveraging the type system, or needing guidance on functional programming patterns. This is the entry point for Haskell development.
---

# Haskell Fundamentals

Foundational Haskell patterns and core language features for pure functional programming. This skill serves as both a reference for common patterns and foundation for advanced Haskell development.

## Overview

**This skill covers:**
- Pure functions and immutability
- Type system and type inference
- Type classes (Functor, Applicative, Monad)
- Pattern matching and guards
- List comprehensions and recursion
- Common monads (Maybe, Either, IO, State)
- Function composition and higher-order functions
- Lazy evaluation fundamentals

**This skill does NOT cover:**
- Advanced type system features (GADTs, Type Families, DataKinds)
- Lens and optics
- Concurrency and parallelism (STM, async)
- Template Haskell and metaprogramming
- Specific frameworks (Yesod, Servant, Scotty)
- Build tools (Cabal, Stack) - see language-specific tooling skills

---

## Quick Reference

| Task | Pattern |
|------|---------|
| Define function | `name :: Type -> Type`<br>`name x = expression` |
| Pattern match | `case x of Pattern -> expr` |
| List comprehension | `[x * 2 \| x <- [1..10], x > 5]` |
| Lambda | `\x -> x + 1` |
| Function composition | `(f . g) x` equals `f (g x)` |
| Type class constraint | `func :: (Show a) => a -> String` |
| Monadic bind | `x >>= f` or `do { y <- x; ... }` |
| Functor map | `fmap f x` or `f <$> x` |
| Applicative apply | `f <*> x` |

---

## Core Concepts

### Pure Functions

```haskell
-- Pure function: same input always produces same output
add :: Int -> Int -> Int
add x y = x + y

-- No side effects - this is NOT valid pure code:
-- impureAdd x y = do
--     print "Adding..."  -- Side effect!
--     return (x + y)

-- Referential transparency: can replace call with result
result1 = add 2 3        -- Always 5
result2 = add 2 3        -- Always 5 (same)
```

### Immutability

```haskell
-- Values cannot be changed
x = 5
-- x = 6  -- Error: multiple declarations

-- "Update" by creating new values
data User = User { name :: String, age :: Int }

updateAge :: Int -> User -> User
updateAge newAge user = user { age = newAge }

-- Original unchanged
user1 = User "Alice" 25
user2 = updateAge 26 user1
-- user1 still has age 25
```

---

## Type System

### Type Inference

```haskell
-- Explicit type signature (recommended)
double :: Int -> Int
double x = x * 2

-- Type inference (compiler deduces type)
triple x = x * 3  -- Inferred: Num a => a -> a

-- Polymorphic types
identity :: a -> a
identity x = x
-- Works for any type: identity 5, identity "hello", etc.
```

### Algebraic Data Types

```haskell
-- Sum types (OR)
data Shape = Circle Float
           | Rectangle Float Float
           | Triangle Float Float Float

-- Product types (AND)
data Point = Point Float Float

-- Record syntax
data Person = Person
    { firstName :: String
    , lastName  :: String
    , age       :: Int
    } deriving (Show, Eq)

-- Using records
person = Person "Alice" "Smith" 30
name = firstName person  -- "Alice"
older = person { age = 31 }  -- Update syntax
```

### Type Aliases

```haskell
-- Simple alias
type Name = String
type Age = Int

-- Parameterized alias
type Pair a = (a, a)
type AssocList k v = [(k, v)]

-- Usage
getName :: Person -> Name
getName p = firstName p
```

### Newtype

```haskell
-- Zero-cost wrapper (compile-time only)
newtype UserId = UserId Int deriving (Show, Eq)
newtype Email = Email String deriving (Show, Eq)

-- Type safety: can't mix UserId and Email
processUser :: UserId -> String
processUser (UserId id) = "User " ++ show id

-- Can't accidentally pass wrong type
userId = UserId 42
-- processUser 42  -- Error!
processUser userId  -- Ok
```

---

## Pattern Matching

### Basic Patterns

```haskell
-- Match literals
isZero :: Int -> Bool
isZero 0 = True
isZero _ = False

-- Match constructors
describeShape :: Shape -> String
describeShape (Circle r) = "Circle with radius " ++ show r
describeShape (Rectangle w h) = "Rectangle " ++ show w ++ "x" ++ show h
describeShape (Triangle a b c) = "Triangle with sides " ++ show a ++ "," ++ show b ++ "," ++ show c

-- Match lists
listLength :: [a] -> Int
listLength [] = 0
listLength (_:xs) = 1 + listLength xs

-- First element pattern
head' :: [a] -> Maybe a
head' [] = Nothing
head' (x:_) = Just x
```

### Case Expressions

```haskell
-- Case in expression
describe :: Maybe Int -> String
describe m = case m of
    Nothing -> "No value"
    Just x  -> "Value: " ++ show x

-- Nested patterns
evalExpr :: Expr -> Int
evalExpr expr = case expr of
    Lit n -> n
    Add e1 e2 -> evalExpr e1 + evalExpr e2
    Mul e1 e2 -> evalExpr e1 * evalExpr e2
```

### Guards

```haskell
-- Boolean conditions
classify :: Int -> String
classify n
    | n < 0     = "negative"
    | n == 0    = "zero"
    | n < 10    = "small"
    | otherwise = "large"

-- Pattern guards
processUser :: Maybe User -> String
processUser mu
    | Nothing <- mu = "No user"
    | Just u <- mu, age u >= 18 = "Adult: " ++ name u
    | Just u <- mu = "Minor: " ++ name u
```

---

## Type Classes

### Common Type Classes

```haskell
-- Eq: Equality
data Color = Red | Green | Blue deriving (Eq)
result = Red == Green  -- False

-- Ord: Ordering
data Priority = Low | Medium | High deriving (Eq, Ord)
result = High > Low  -- True

-- Show: String representation
data Point = Point Int Int deriving (Show)
p = Point 3 4
str = show p  -- "Point 3 4"

-- Read: Parse from string
value = read "42" :: Int
```

### Functor

```haskell
-- fmap: Apply function inside context
-- fmap :: Functor f => (a -> b) -> f a -> f b

-- Maybe Functor
result1 = fmap (*2) (Just 5)     -- Just 10
result2 = fmap (*2) Nothing      -- Nothing

-- List Functor
result3 = fmap (*2) [1,2,3]      -- [2,4,6]

-- Operator form: <$>
result4 = (*2) <$> Just 5        -- Just 10
result5 = (*2) <$> [1,2,3]       -- [2,4,6]

-- Function composition in Functor
result6 = (+1) <$> (*2) <$> Just 5  -- Just 11
```

### Applicative

```haskell
-- <*>: Apply function in context to value in context
-- pure: Lift value into context

-- Maybe Applicative
result1 = pure (+) <*> Just 3 <*> Just 4     -- Just 7
result2 = pure (+) <*> Nothing <*> Just 4    -- Nothing

-- Applicative style
result3 = (+) <$> Just 3 <*> Just 4          -- Just 7

-- Multiple arguments
data User = User String Int
createUser = User <$> Just "Alice" <*> Just 30  -- Just (User "Alice" 30)

-- List Applicative (Cartesian product)
result4 = (*) <$> [1,2] <*> [3,4]  -- [3,4,6,8]
```

### Monad

```haskell
-- >>= (bind): Chain operations that return monadic values
-- return: Lift value into monad (same as pure)

-- Maybe Monad
safeDivide :: Float -> Float -> Maybe Float
safeDivide _ 0 = Nothing
safeDivide x y = Just (x / y)

calculation :: Maybe Float
calculation = do
    a <- Just 10
    b <- Just 2
    result <- safeDivide a b
    return (result * 2)  -- Just 10.0

-- Same with bind operator
calculation' = Just 10 >>= \a ->
               Just 2  >>= \b ->
               safeDivide a b >>= \result ->
               return (result * 2)

-- Either Monad (for error handling)
type Error = String

validateAge :: Int -> Either Error Int
validateAge age
    | age < 0 = Left "Age cannot be negative"
    | age > 150 = Left "Age too high"
    | otherwise = Right age

validateEmail :: String -> Either Error String
validateEmail email
    | '@' `elem` email = Right email
    | otherwise = Left "Invalid email"

createUser :: Int -> String -> Either Error User
createUser age email = do
    validAge <- validateAge age
    validEmail <- validateEmail email
    return $ User validEmail validAge
```

---

## Lists and Recursion

### List Comprehensions

```haskell
-- Basic comprehension
squares = [x^2 | x <- [1..10]]

-- With filter
evenSquares = [x^2 | x <- [1..10], even x]

-- Multiple generators
pairs = [(x,y) | x <- [1..3], y <- [1..3]]
-- [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)]

-- Dependent generators
orderedPairs = [(x,y) | x <- [1..5], y <- [x..5]]
-- [(1,1),(1,2),...,(5,5)]

-- Multiple filters
pythagoras = [(a,b,c) | a <- [1..20],
                        b <- [a..20],
                        c <- [b..20],
                        a^2 + b^2 == c^2]
```

### Recursive Functions

```haskell
-- Sum of list
sum' :: [Int] -> Int
sum' [] = 0
sum' (x:xs) = x + sum' xs

-- Filter
filter' :: (a -> Bool) -> [a] -> [a]
filter' _ [] = []
filter' p (x:xs)
    | p x       = x : filter' p xs
    | otherwise = filter' p xs

-- Map
map' :: (a -> b) -> [a] -> [b]
map' _ [] = []
map' f (x:xs) = f x : map' f xs

-- Fold (right)
foldr' :: (a -> b -> b) -> b -> [a] -> b
foldr' _ acc [] = acc
foldr' f acc (x:xs) = f x (foldr' f acc xs)

-- Fibonacci
fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = fib (n-1) + fib (n-2)
```

### Common List Functions

```haskell
-- Construction and access
list = 1 : 2 : 3 : []        -- [1,2,3]
first = head [1,2,3]         -- 1
rest = tail [1,2,3]          -- [2,3]

-- Transformation
doubled = map (*2) [1,2,3]                    -- [2,4,6]
evens = filter even [1,2,3,4]                 -- [2,4]
sum = foldr (+) 0 [1,2,3,4]                   -- 10
reversed = reverse [1,2,3]                    -- [3,2,1]

-- Combination
combined = concat [[1,2], [3,4]]              -- [1,2,3,4]
flattened = concatMap (\x -> [x,x]) [1,2,3]   -- [1,1,2,2,3,3]
zipped = zip [1,2,3] ['a','b','c']            -- [(1,'a'),(2,'b'),(3,'c')]

-- Selection
taken = take 3 [1..10]      -- [1,2,3]
dropped = drop 3 [1..10]    -- [4,5,6,7,8,9,10]
split = splitAt 3 [1..10]   -- ([1,2,3],[4,5,6,7,8,9,10])
```

---

## Higher-Order Functions

### Function Composition

```haskell
-- Compose: (f . g) x = f (g x)
addThenDouble = (*2) . (+1)
result = addThenDouble 5  -- 12

-- Chain multiple functions
process = filter even . map (*2) . filter (>0)
result = process [-2,-1,0,1,2,3]  -- [2,4,6]

-- Point-free style
-- Instead of: f x = g (h x)
-- Write: f = g . h
sumOfSquares :: [Int] -> Int
sumOfSquares = sum . map (^2)
```

### Partial Application

```haskell
-- Functions are curried by default
add :: Int -> Int -> Int
add x y = x + y

-- Partial application
add5 :: Int -> Int
add5 = add 5

result = add5 10  -- 15

-- Common pattern
doubleAll = map (*2)
filterPositive = filter (>0)

result = doubleAll [1,2,3]     -- [2,4,6]
result = filterPositive [-1,0,1,2]  -- [1,2]
```

### Common Higher-Order Patterns

```haskell
-- Apply function n times
applyN :: Int -> (a -> a) -> a -> a
applyN 0 _ x = x
applyN n f x = applyN (n-1) f (f x)

result = applyN 3 (*2) 5  -- 40 (5*2*2*2)

-- Flip arguments
flip' :: (a -> b -> c) -> (b -> a -> c)
flip' f x y = f y x

-- Use with sections
subtractFrom10 = flip (-) 10
result = subtractFrom10 3  -- 7 (10 - 3)
```

---

## Common Monads

### Maybe

```haskell
-- Represent optional values
findUser :: Int -> Maybe User
findUser 1 = Just (User "Alice" 30)
findUser _ = Nothing

-- Chain operations
getUserEmail :: Int -> Maybe String
getUserEmail userId = do
    user <- findUser userId
    return (email user)

-- Handle Nothing
getEmailOrDefault :: Int -> String
getEmailOrDefault userId =
    case findUser userId of
        Just user -> email user
        Nothing -> "no-email@example.com"

-- Maybe functions
result1 = fromMaybe "default" (Just "value")  -- "value"
result2 = fromMaybe "default" Nothing         -- "default"
result3 = maybe "none" show (Just 42)         -- "42"
```

### Either

```haskell
-- Represent computations that can fail
parseAge :: String -> Either String Int
parseAge str =
    case reads str of
        [(n, "")] -> if n >= 0
                     then Right n
                     else Left "Age must be positive"
        _ -> Left "Not a valid number"

-- Chain Either operations
validateUser :: String -> String -> Either String User
validateUser ageStr emailStr = do
    age <- parseAge ageStr
    email <- validateEmail emailStr
    return $ User email age

-- Either functions
result1 = either show (*2) (Right 5)  -- 10
result2 = either show (*2) (Left "error")  -- "error"
```

### IO

```haskell
-- IO actions are first-class values
greeting :: IO ()
greeting = do
    putStrLn "What is your name?"
    name <- getLine
    putStrLn $ "Hello, " ++ name

-- Read file
readConfig :: FilePath -> IO String
readConfig path = do
    contents <- readFile path
    return contents

-- Write file
writeLog :: String -> IO ()
writeLog message = do
    appendFile "log.txt" (message ++ "\n")

-- Sequence IO actions
main :: IO ()
main = do
    putStrLn "Starting..."
    result <- computation
    putStrLn $ "Result: " ++ show result
    putStrLn "Done"
```

### State

```haskell
import Control.Monad.State

-- Stateful computation
type Counter a = State Int a

-- Increment counter
increment :: Counter ()
increment = modify (+1)

-- Get current count
getCount :: Counter Int
getCount = get

-- Stateful computation
computation :: Counter Int
computation = do
    increment
    increment
    increment
    count <- getCount
    return count

-- Run state
result = runState computation 0  -- (3, 3)
finalState = execState computation 0  -- 3
finalValue = evalState computation 0  -- 3
```

---

## Lazy Evaluation

### Infinite Lists

```haskell
-- Infinite list of naturals
naturals = [1..]

-- Take first 10
first10 = take 10 naturals  -- [1,2,3,4,5,6,7,8,9,10]

-- Infinite Fibonacci
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)
first10Fibs = take 10 fibs  -- [0,1,1,2,3,5,8,13,21,34]

-- Infinite repeat
ones = repeat 1
cycle123 = cycle [1,2,3]  -- [1,2,3,1,2,3,1,2,3,...]
```

### Strictness

```haskell
-- Lazy by default
lazySum xs = if null xs then 0 else head xs + lazySum (tail xs)

-- Force strict evaluation with $!
strictSum xs = if null xs then 0 else head xs $! strictSum (tail xs)

-- seq: Force evaluation
forceEval x y = x `seq` y

-- BangPatterns extension
{-# LANGUAGE BangPatterns #-}
strictFunc !x = x + 1  -- x evaluated immediately
```

---

## Common Idioms

### Pipeline Style

```haskell
-- Use $ to avoid parentheses
result = show $ sum $ map (*2) [1,2,3]

-- Use & for left-to-right flow (Data.Function)
import Data.Function ((&))
result = [1,2,3]
       & map (*2)
       & sum
       & show
```

### Where vs Let

```haskell
-- where: Definitions after expression
circleArea r = pi * r^2
  where pi = 3.14159

-- let: Definitions before expression
circleArea' r =
  let pi = 3.14159
  in pi * r^2

-- let in do-notation
computation = do
    let x = 5
        y = 10
    return (x + y)
```

### Operator Sections

```haskell
-- Partially apply operators
add5 = (+5)      -- Add 5 to argument
half = (/2)      -- Divide argument by 2
double = (*2)    -- Multiply argument by 2

-- Use with map
doubled = map (*2) [1,2,3]  -- [2,4,6]
```

---

## Troubleshooting

### Type Errors

**Problem:** Type mismatch

```haskell
-- Error: Couldn't match expected type 'Int' with actual type '[Int]'
badFunc :: Int -> Int
badFunc x = [x]  -- Returns list, not Int
```

**Fix:** Match return type:
```haskell
goodFunc :: Int -> [Int]
goodFunc x = [x]
```

### Infinite Loops

**Problem:** Non-terminating recursion

```haskell
-- Never terminates!
badLength xs = 1 + badLength xs
```

**Fix:** Add base case:
```haskell
goodLength [] = 0
goodLength (_:xs) = 1 + goodLength xs
```

### Monad Type Errors

**Problem:** Couldn't match type 'Maybe a' with 'a'

```haskell
-- Error: findUser returns Maybe User, not User
badCode = name (findUser 1)
```

**Fix:** Extract with bind or pattern match:
```haskell
goodCode = do
    user <- findUser 1
    return (name user)

-- Or:
goodCode = case findUser 1 of
    Just user -> name user
    Nothing -> "Unknown"
```

### Lazy Evaluation Issues

**Problem:** Stack overflow on large list

```haskell
-- Lazy accumulation builds up thunks
badSum = foldl (+) 0 [1..1000000]
```

**Fix:** Use strict fold:
```haskell
import Data.List (foldl')
goodSum = foldl' (+) 0 [1..1000000]
```

---

## Module System

### Module Basics

```haskell
-- Module declaration (must match file path)
-- File: src/MyApp/User.hs
module MyApp.User
    ( User(..)           -- Export type and all constructors
    , createUser         -- Export function
    , validateEmail      -- Export function
    ) where

import Data.Text (Text)
import qualified Data.Map as M
import Data.List (sort, nub)

-- Module contents...
data User = User { name :: Text, email :: Text }

createUser :: Text -> Text -> User
createUser n e = User n e

validateEmail :: Text -> Bool
validateEmail = undefined -- implementation
```

### Import Variations

```haskell
-- Import everything
import Data.List

-- Import specific items
import Data.List (sort, nub, groupBy)

-- Import with hiding
import Prelude hiding (head, tail)

-- Qualified import (prevents name collisions)
import qualified Data.Map as M
import qualified Data.Text as T

-- Use: M.lookup, T.pack, T.unpack

-- Qualified with original name
import qualified Data.ByteString.Lazy
-- Use: Data.ByteString.Lazy.readFile

-- Combined: import some, qualify others
import Data.Text (Text)
import qualified Data.Text as T
```

### Export Control

```haskell
-- Export everything (not recommended)
module MyModule where

-- Explicit exports (recommended)
module MyModule
    ( -- Types
      User(..)              -- Export type with all constructors
    , Config(Config)        -- Export type with specific constructor
    , Connection            -- Export type only (abstract)

      -- Functions
    , createUser
    , updateUser

      -- Re-exports
    , module Data.Text      -- Re-export entire module
    ) where

-- Internal/private by default
internalHelper :: Int -> Int  -- Not exported, private
internalHelper x = x + 1
```

### Hierarchical Modules

```
src/
├── MyApp.hs              -- module MyApp
├── MyApp/
│   ├── Types.hs          -- module MyApp.Types
│   ├── User.hs           -- module MyApp.User
│   └── Internal/
│       └── Utils.hs      -- module MyApp.Internal.Utils
```

```haskell
-- Re-export pattern for convenience
-- File: src/MyApp.hs
module MyApp
    ( module MyApp.Types
    , module MyApp.User
    ) where

import MyApp.Types
import MyApp.User

-- Users can now:
-- import MyApp (User, createUser, ...)
```

### Package Structure

```yaml
# package.yaml (hpack) or .cabal
name: my-app
version: 0.1.0.0

library:
  source-dirs: src
  exposed-modules:
    - MyApp
    - MyApp.Types
    - MyApp.User
  other-modules:
    - MyApp.Internal.Utils  # Not exposed to consumers
```

---

## Zero and Default Values

### Default Type Class

```haskell
import Data.Default

-- Using Default type class
data Config = Config
    { port :: Int
    , host :: String
    , debug :: Bool
    }

instance Default Config where
    def = Config
        { port = 8080
        , host = "localhost"
        , debug = False
        }

-- Usage
config1 = def :: Config                    -- All defaults
config2 = def { port = 3000 }              -- Override port
config3 = def { debug = True, port = 80 }  -- Override multiple
```

### Monoid and Mempty

```haskell
import Data.Monoid

-- mempty: identity element for Monoid
emptyList = mempty :: [a]           -- []
emptyString = mempty :: String      -- ""
emptySum = mempty :: Sum Int        -- Sum 0
emptyProduct = mempty :: Product Int -- Product 1

-- Custom monoid with default
data Settings = Settings
    { timeout :: Maybe Int
    , retries :: Maybe Int
    }

instance Semigroup Settings where
    a <> b = Settings
        { timeout = timeout b <|> timeout a
        , retries = retries b <|> retries a
        }

instance Monoid Settings where
    mempty = Settings Nothing Nothing
```

### Maybe for Optional Values

```haskell
-- Maybe represents optional values
data Maybe a = Nothing | Just a

-- Common patterns
findUser :: UserId -> Maybe User
findUser uid = lookup uid users

-- Default with fromMaybe
import Data.Maybe (fromMaybe)

getPort :: Config -> Int
getPort cfg = fromMaybe 8080 (configPort cfg)

-- Chain with <|>
getEnv :: String -> Maybe String -> Maybe String
getEnv key fallback = lookup key env <|> fallback <|> Just "default"
```

### Empty/Zero Values by Type

| Type | Zero/Empty Value | Function |
|------|------------------|----------|
| `Int`, `Integer` | `0` | Literal |
| `Float`, `Double` | `0.0` | Literal |
| `String` | `""` | `mempty` |
| `Text` | `""` | `T.empty` |
| `[a]` | `[]` | `mempty` |
| `Maybe a` | `Nothing` | Constructor |
| `Map k v` | `M.empty` | `mempty` |
| `Set a` | `S.empty` | `mempty` |

---

## Concurrency

Haskell provides powerful concurrency abstractions with strong safety guarantees. For cross-language comparison, see `patterns-concurrency-dev`.

### Lightweight Threads

```haskell
import Control.Concurrent

-- Spawn lightweight thread (green thread)
main = do
    forkIO $ do
        threadDelay 1000000  -- 1 second in microseconds
        putStrLn "Hello from thread"

    putStrLn "Main thread continues"
    threadDelay 2000000  -- Wait for child

-- Thread with MVar communication
example = do
    result <- newEmptyMVar

    forkIO $ do
        value <- computeExpensive
        putMVar result value

    -- Block until result available
    answer <- takeMVar result
    print answer
```

### Async for Structured Concurrency

```haskell
import Control.Concurrent.Async

-- Run two actions concurrently, wait for both
main = do
    (result1, result2) <- concurrently
        (fetchUrl "http://example.com/1")
        (fetchUrl "http://example.com/2")
    print (result1, result2)

-- Race: first to complete wins
winner <- race
    (fetchFromServer1 key)
    (fetchFromServer2 key)

-- Map concurrently
results <- mapConcurrently fetchUrl urls

-- With timeout
maybeResult <- timeout 5000000 longComputation  -- 5 second timeout
```

### Software Transactional Memory (STM)

```haskell
import Control.Concurrent.STM

-- Transactional variables
type Account = TVar Int

-- Atomic transfer between accounts
transfer :: Account -> Account -> Int -> STM ()
transfer from to amount = do
    fromBalance <- readTVar from
    when (fromBalance < amount) retry  -- Blocks until condition met
    modifyTVar from (subtract amount)
    modifyTVar to (+ amount)

-- Run transaction
main = do
    account1 <- newTVarIO 1000
    account2 <- newTVarIO 0

    atomically $ transfer account1 account2 500

    balances <- atomically $ do
        b1 <- readTVar account1
        b2 <- readTVar account2
        return (b1, b2)

    print balances  -- (500, 500)
```

### Parallel Evaluation

```haskell
import Control.Parallel.Strategies

-- Parallel map
parMap :: (a -> b) -> [a] -> [b]
parMap f xs = map f xs `using` parList rseq

-- Parallel computation
compute :: [Int] -> Int
compute xs = sum squares `using` rpar
  where squares = map (^2) xs

-- Spark parallel evaluation
import Control.Parallel (par, pseq)

parFib :: Int -> Int
parFib n
    | n < 2 = n
    | otherwise =
        let x = parFib (n-1)
            y = parFib (n-2)
        in x `par` y `pseq` (x + y)
```

---

## Metaprogramming

Haskell's metaprogramming uses Template Haskell for compile-time code generation. For cross-language comparison, see `patterns-metaprogramming-dev`.

### Template Haskell Basics

```haskell
{-# LANGUAGE TemplateHaskell #-}

import Language.Haskell.TH

-- Generate function at compile time
-- Creates: add5 x = x + 5
$(do
    let name = mkName "add5"
    let body = [| \x -> x + 5 |]
    [d| $(varP name) = $body |]
 )

-- Quote expressions
expr :: Q Exp
expr = [| 1 + 2 |]  -- Represents the expression (1 + 2)

-- Quote types
myType :: Q Type
myType = [t| Maybe Int |]

-- Quote patterns
myPat :: Q Pat
myPat = [p| (x, y) |]
```

### Deriving with Template Haskell

```haskell
{-# LANGUAGE TemplateHaskell #-}

import Data.Aeson.TH

-- Generate JSON instances
data User = User
    { userName :: String
    , userAge :: Int
    }

$(deriveJSON defaultOptions ''User)
-- Generates: instance FromJSON User where ...
--            instance ToJSON User where ...

-- With options
$(deriveJSON defaultOptions{fieldLabelModifier = drop 4} ''User)
-- Strips "user" prefix from JSON keys
```

### Lens Generation

```haskell
{-# LANGUAGE TemplateHaskell #-}

import Control.Lens

data Person = Person
    { _name :: String
    , _age :: Int
    }

makeLenses ''Person
-- Generates: name :: Lens' Person String
--            age :: Lens' Person Int

-- Usage
updateAge :: Person -> Person
updateAge = over age (+1)

getName :: Person -> String
getName = view name
```

### GHC Generics (Alternative to TH)

```haskell
{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE DeriveAnyClass #-}

import GHC.Generics
import Data.Aeson

-- Automatic deriving via Generics
data Config = Config
    { configPort :: Int
    , configHost :: String
    } deriving (Generic, FromJSON, ToJSON)

-- Works out of the box
config = decode "{\"configPort\":8080,\"configHost\":\"localhost\"}"
```

---

## Serialization

For cross-language serialization patterns and comparison, see `patterns-serialization-dev`.

### Aeson (JSON)

```haskell
{-# LANGUAGE DeriveGeneric #-}

import Data.Aeson
import GHC.Generics

-- Automatic JSON with Generics
data User = User
    { name :: String
    , email :: String
    , age :: Int
    } deriving (Generic, Show)

instance FromJSON User
instance ToJSON User

-- Encode/decode
encodeUser :: User -> ByteString
encodeUser = encode

decodeUser :: ByteString -> Maybe User
decodeUser = decode
```

### Custom JSON Instances

```haskell
import Data.Aeson
import Data.Aeson.Types

data Status = Active | Inactive | Pending

instance ToJSON Status where
    toJSON Active = String "active"
    toJSON Inactive = String "inactive"
    toJSON Pending = String "pending"

instance FromJSON Status where
    parseJSON = withText "Status" $ \t ->
        case t of
            "active" -> return Active
            "inactive" -> return Inactive
            "pending" -> return Pending
            _ -> fail "Invalid status"

-- Complex type with field renaming
data Config = Config
    { configPort :: Int
    , configHost :: String
    }

instance ToJSON Config where
    toJSON (Config p h) = object
        [ "port" .= p
        , "host" .= h
        ]

instance FromJSON Config where
    parseJSON = withObject "Config" $ \v -> Config
        <$> v .: "port"
        <*> v .: "host"
```

### Aeson Options

```haskell
{-# LANGUAGE TemplateHaskell #-}

import Data.Aeson.TH

data ApiResponse = ApiResponse
    { responseStatus :: String
    , responseData :: Value
    , responseTimestamp :: Int
    }

$(deriveJSON defaultOptions
    { fieldLabelModifier = camelTo2 '_' . drop 8  -- Remove "response" prefix, snake_case
    , omitNothingFields = True
    } ''ApiResponse)

-- Produces: {"status": "...", "data": ..., "timestamp": ...}
```

### YAML

```haskell
import Data.Yaml

-- Same types work with YAML (Aeson-based)
config <- decodeFileThrow "config.yaml" :: IO Config

-- Encode to YAML
encodeFile "output.yaml" config
```

### Validation

```haskell
-- Manual validation with Either
validateUser :: User -> Either String User
validateUser u
    | null (name u) = Left "Name cannot be empty"
    | age u < 0 = Left "Age must be non-negative"
    | '@' `notElem` email u = Left "Invalid email"
    | otherwise = Right u

-- With Validation Applicative
import Data.Validation

validateUser' :: User -> Validation [String] User
validateUser' u = User
    <$> validateName (name u)
    <*> validateAge (age u)
    <*> validateEmail (email u)
  where
    validateName n
        | null n = Failure ["Name cannot be empty"]
        | otherwise = Success n
    -- ... etc
```

---

## Build and Dependencies

### Cabal

```cabal
-- my-app.cabal
cabal-version: 2.4
name:          my-app
version:       0.1.0.0
license:       MIT
author:        Your Name

common shared
    ghc-options: -Wall
    default-language: Haskell2010

library
    import: shared
    exposed-modules:
        MyApp
        MyApp.Types
    other-modules:
        MyApp.Internal
    build-depends:
        base >= 4.14 && < 5
      , text >= 1.2
      , aeson >= 2.0
      , containers
    hs-source-dirs: src

executable my-app
    import: shared
    main-is: Main.hs
    build-depends:
        base
      , my-app  -- Depend on library
    hs-source-dirs: app

test-suite my-app-test
    import: shared
    type: exitcode-stdio-1.0
    main-is: Spec.hs
    build-depends:
        base
      , my-app
      , hspec >= 2.7
      , QuickCheck
    hs-source-dirs: test
```

### Stack

```yaml
# stack.yaml
resolver: lts-21.0  # Stackage snapshot

packages:
  - .

extra-deps:
  - some-package-1.0.0
  - git: https://github.com/user/repo
    commit: abc123

# package.yaml (hpack format, generates .cabal)
name: my-app
version: 0.1.0.0

dependencies:
  - base >= 4.14 && < 5
  - text
  - aeson

library:
  source-dirs: src

executables:
  my-app:
    main: Main.hs
    source-dirs: app
    dependencies:
      - my-app

tests:
  my-app-test:
    main: Spec.hs
    source-dirs: test
    dependencies:
      - my-app
      - hspec
      - QuickCheck
```

### Common Commands

```bash
# Cabal
cabal init                    # Initialize new project
cabal build                   # Build project
cabal run                     # Build and run executable
cabal test                    # Run tests
cabal repl                    # Start REPL with project loaded
cabal install --lib aeson     # Install library globally

# Stack
stack new my-project          # Create new project
stack build                   # Build project
stack run                     # Build and run
stack test                    # Run tests
stack ghci                    # REPL with project
stack install                 # Install executables
```

### GHC Options

```cabal
-- Common GHC options
ghc-options:
    -Wall                     -- Enable all warnings
    -Wcompat                  -- Warn about future incompatibilities
    -Wincomplete-patterns     -- Warn about incomplete patterns
    -Wincomplete-uni-patterns
    -Wredundant-constraints
    -O2                       -- Optimization level 2
    -threaded                 -- Enable threaded runtime
    -rtsopts                  -- Enable RTS options
    -with-rtsopts=-N          -- Use all CPU cores
```

---

## Testing

### HSpec

```haskell
-- test/Spec.hs
{-# OPTIONS_GHC -F -pgmF hspec-discover #-}

-- test/MyApp/UserSpec.hs
module MyApp.UserSpec where

import Test.Hspec
import MyApp.User

spec :: Spec
spec = do
    describe "createUser" $ do
        it "creates a user with the given name" $ do
            let user = createUser "Alice" "alice@example.com"
            userName user `shouldBe` "Alice"

        it "creates a user with the given email" $ do
            let user = createUser "Alice" "alice@example.com"
            userEmail user `shouldBe` "alice@example.com"

    describe "validateEmail" $ do
        it "returns True for valid email" $ do
            validateEmail "user@example.com" `shouldBe` True

        it "returns False for email without @" $ do
            validateEmail "invalid" `shouldBe` False
```

### HSpec Matchers

```haskell
import Test.Hspec

spec :: Spec
spec = do
    describe "Matchers" $ do
        -- Equality
        it "shouldBe" $ 1 + 1 `shouldBe` 2

        -- Boolean
        it "shouldSatisfy" $ 5 `shouldSatisfy` (> 0)

        -- Lists
        it "shouldContain" $ [1,2,3] `shouldContain` [2]
        it "shouldMatchList" $ [1,2,3] `shouldMatchList` [3,1,2]

        -- Maybe
        it "shouldBe Just" $ Just 5 `shouldBe` Just 5
        it "shouldBe Nothing" $ (Nothing :: Maybe Int) `shouldBe` Nothing

        -- Exceptions
        it "shouldThrow" $
            evaluate (error "boom") `shouldThrow` anyException

        -- Approximate equality
        it "shouldSatisfy approx" $
            3.14159 `shouldSatisfy` (\x -> abs (x - pi) < 0.001)
```

### QuickCheck (Property-Based Testing)

```haskell
import Test.QuickCheck
import Test.Hspec
import Test.Hspec.QuickCheck

spec :: Spec
spec = do
    describe "reverse" $ do
        prop "reversing twice gives original" $ \xs ->
            reverse (reverse xs) == (xs :: [Int])

        prop "length is preserved" $ \xs ->
            length (reverse xs) == length (xs :: [Int])

    describe "sort" $ do
        prop "result is sorted" $ \xs ->
            isSorted (sort (xs :: [Int]))

        prop "length is preserved" $ \xs ->
            length (sort xs) == length (xs :: [Int])

        prop "all elements preserved" $ \xs ->
            sort (xs :: [Int]) `shouldMatchList` xs

isSorted :: Ord a => [a] -> Bool
isSorted [] = True
isSorted [_] = True
isSorted (x:y:xs) = x <= y && isSorted (y:xs)
```

### Custom Generators

```haskell
import Test.QuickCheck

-- Generator for positive integers
positiveInt :: Gen Int
positiveInt = abs <$> arbitrary `suchThat` (> 0)

-- Generator for valid emails
validEmail :: Gen String
validEmail = do
    user <- listOf1 $ elements ['a'..'z']
    domain <- listOf1 $ elements ['a'..'z']
    return $ user ++ "@" ++ domain ++ ".com"

-- Use with forAll
prop_positiveSquare :: Property
prop_positiveSquare = forAll positiveInt $ \n ->
    n * n > 0

-- Arbitrary instance for custom type
data User = User String Int

instance Arbitrary User where
    arbitrary = User
        <$> listOf1 (elements ['a'..'z'])
        <*> choose (0, 120)
```

### Hedgehog (Alternative Property Testing)

```haskell
import Hedgehog
import qualified Hedgehog.Gen as Gen
import qualified Hedgehog.Range as Range

prop_reverse :: Property
prop_reverse = property $ do
    xs <- forAll $ Gen.list (Range.linear 0 100) Gen.alpha
    reverse (reverse xs) === xs

prop_sort :: Property
prop_sort = property $ do
    xs <- forAll $ Gen.list (Range.linear 0 100) (Gen.int $ Range.linear 0 1000)
    let sorted = sort xs
    assert $ isSorted sorted
    length sorted === length xs
```

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-concurrency-dev` - STM, async, parallel strategies
- `patterns-serialization-dev` - Aeson, YAML, validation patterns
- `patterns-metaprogramming-dev` - Template Haskell, Generics

---

## References

- [Learn You a Haskell](http://learnyouahaskell.com/)
- [Haskell Wiki](https://wiki.haskell.org/)
- [Hoogle (API Search)](https://hoogle.haskell.org/)
- [Real World Haskell](http://book.realworldhaskell.org/)
- [GHC User Guide](https://downloads.haskell.org/ghc/latest/docs/users_guide/)
