---
name: convert-roc-haskell
description: Convert Roc code to idiomatic Haskell. Use when migrating Roc projects to Haskell, translating Roc patterns to idiomatic Haskell, or refactoring Roc codebases. Extends meta-convert-dev with Roc-to-Haskell specific patterns.
---

# Convert Roc to Haskell

Convert Roc code to idiomatic Haskell. This skill extends `meta-convert-dev` with Roc-to-Haskell specific type mappings, idiom translations, and tooling for migrating platform-based Roc code to pure functional Haskell.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Roc types → Haskell types
- **Idiom translations**: Roc patterns → idiomatic Haskell
- **Error handling**: Roc Result → Haskell Either/Maybe
- **Platform model**: Roc applications/platforms → Haskell IO/mtl
- **Abilities**: Roc abilities → Haskell type classes
- **Tag unions**: Roc structural tags → Haskell algebraic data types

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Haskell language fundamentals - see `lang-haskell-dev`
- Reverse conversion (Haskell → Roc) - see `convert-haskell-roc`
- Platform development - Both use different models; design from scratch

---

## Quick Reference

| Roc | Haskell | Notes |
|-----|---------|-------|
| `Str` | `String` or `Text` | Use Text for production |
| `U8`, `U16`, `U32`, `U64` | `Word8`, `Word16`, `Word32`, `Word64` | Unsigned integers |
| `I8`, `I16`, `I32`, `I64` | `Int8`, `Int16`, `Int32`, `Int64` | Signed integers |
| `F32`, `F64` | `Float`, `Double` | Floating point |
| `Bool` | `Bool` | Direct mapping |
| `List a` | `[a]` | Lists |
| `Dict k v` | `Map k v` | Use Data.Map |
| `Set a` | `Set a` | Use Data.Set |
| `Result a e` | `Either e a` | Note reversed type params |
| `[Tag1, Tag2]` | `data X = Tag1 \| Tag2` | Sum types |
| `{ field : Type }` | `data X = X { field :: Type }` | Records |
| `Task a err` | `IO a` or `ExceptT err IO a` | Effects |
| `where a implements Ability` | `(TypeClass a) =>` | Constraints |

## When Converting Code

1. **Analyze platform boundaries** - Understand where Roc platform ends and application begins
2. **Map types first** - Roc's structural types need explicit Haskell ADTs
3. **Preserve semantics** over syntax similarity
4. **Embrace laziness** - Haskell is lazy by default; Roc is strict
5. **Handle effects properly** - Roc Tasks become IO or monad transformers
6. **Test equivalence** - Same inputs → same outputs for pure logic

---

## Type System Mapping

### Primitive Types

| Roc | Haskell | Notes |
|-----|---------|-------|
| `Str` | `String` | List of Char (less efficient) |
| `Str` | `Text` | **Preferred** from Data.Text |
| `U8` | `Word8` | From Data.Word |
| `U16` | `Word16` | From Data.Word |
| `U32` | `Word32` | From Data.Word |
| `U64` | `Word64` | From Data.Word |
| `U128` | `Integer` | No direct u128, use arbitrary precision |
| `I8` | `Int8` | From Data.Int |
| `I16` | `Int16` | From Data.Int |
| `I32` | `Int32` | From Data.Int |
| `I64` | `Int64` | From Data.Int |
| `I128` | `Integer` | Arbitrary precision |
| `F32` | `Float` | 32-bit float |
| `F64` | `Double` | 64-bit float |
| `Bool` | `Bool` | Direct mapping |
| `Num a` | Polymorphic number | Use type classes |

### Collection Types

| Roc | Haskell | Notes |
|-----|---------|-------|
| `List a` | `[a]` | Linked list |
| `List a` | `Vector a` | For indexed access (Data.Vector) |
| `Dict k v` | `Map k v` | From Data.Map |
| `Set a` | `Set a` | From Data.Set |

### Composite Types

| Roc | Haskell | Notes |
|-----|---------|-------|
| `{ name : Str, age : U32 }` | `data User = User { name :: Text, age :: Word32 }` | Record syntax |
| `[Ok a, Err e]` | `Either e a` | Note: type params reversed! |
| `[Some a, None]` | `Maybe a` | Optional values |
| `[Tag1, Tag2, Tag3]` | `data X = Tag1 \| Tag2 \| Tag3` | Sum types |
| `[Tag(T)]` | `data X = Tag T` | Tag with payload |

### Function Types

| Roc | Haskell | Notes |
|-----|---------|-------|
| `a -> b` | `a -> b` | Simple function |
| `a, b -> c` | `a -> b -> c` | Curried by default |
| `a -> b where a implements Eq` | `(Eq a) => a -> b` | Type class constraint |

---

## Idiom Translation

### Pattern 1: Records and Record Updates

**Roc:**
```roc
user = { name: "Alice", age: 30, email: "alice@example.com" }

# Update syntax
olderUser = { user & age: 31 }

# Field access
userName = user.name
```

**Haskell:**
```haskell
data User = User
    { name :: Text
    , age :: Word32
    , email :: Text
    } deriving (Show, Eq)

user = User "Alice" 30 "alice@example.com"

-- Update syntax
olderUser = user { age = 31 }

-- Field access (auto-generated accessor functions)
userName = name user
```

**Why this translation:**
- Roc's anonymous records need named data declarations in Haskell
- Both support record update syntax, but Haskell generates accessor functions
- Haskell requires explicit type declarations; Roc infers structural types

### Pattern 2: Tag Unions and Pattern Matching

**Roc:**
```roc
# Tag union
Color : [Red, Yellow, Green, Custom(U8, U8, U8)]

# Pattern matching
colorName = when color is
    Red -> "red"
    Yellow -> "yellow"
    Green -> "green"
    Custom(r, g, b) -> "rgb(\(Num.toStr(r)), \(Num.toStr(g)), \(Num.toStr(b)))"
```

**Haskell:**
```haskell
-- Algebraic data type
data Color
    = Red
    | Yellow
    | Green
    | Custom Word8 Word8 Word8
    deriving (Show, Eq)

-- Pattern matching with case
colorName :: Color -> String
colorName color = case color of
    Red -> "red"
    Yellow -> "yellow"
    Green -> "green"
    Custom r g b -> "rgb(" ++ show r ++ ", " ++ show g ++ ", " ++ show b ++ ")"

-- Or with function patterns
colorName' :: Color -> String
colorName' Red = "red"
colorName' Yellow = "yellow"
colorName' Green = "green"
colorName' (Custom r g b) = "rgb(" ++ show r ++ ", " ++ show g ++ ", " ++ show b ++ ")"
```

**Why this translation:**
- Roc's structural tag unions become nominal ADTs in Haskell
- Both enforce exhaustive pattern matching
- Haskell allows pattern matching in function definitions, not just case expressions

### Pattern 3: Result Type and Error Handling

**Roc:**
```roc
divide : I64, I64 -> Result I64 [DivByZero]
divide = \a, b ->
    if b == 0 then
        Err(DivByZero)
    else
        Ok(a // b)

# Using try (!) for propagation
calculate : I64, I64, I64 -> Result I64 [DivByZero]
calculate = \a, b, c ->
    x = divide!(a, b)
    y = divide!(x, c)
    Ok(y)
```

**Haskell:**
```haskell
-- Either for errors (note reversed params from Roc)
data DivError = DivByZero deriving (Show, Eq)

divide :: Int64 -> Int64 -> Either DivError Int64
divide a 0 = Left DivByZero
divide a b = Right (a `div` b)

-- Using do-notation for propagation
calculate :: Int64 -> Int64 -> Int64 -> Either DivError Int64
calculate a b c = do
    x <- divide a b
    y <- divide x c
    return y

-- Or with applicative style
calculate' :: Int64 -> Int64 -> Int64 -> Either DivError Int64
calculate' a b c =
    divide a b >>= \x ->
    divide x c
```

**Why this translation:**
- Roc's `Result a e` maps to Haskell's `Either e a` (type params reversed!)
- Roc's `!` suffix maps to Haskell's `<-` in do-notation
- Both provide monadic error propagation
- Haskell's Either is more general (any error type), Roc uses tag unions

### Pattern 4: Abilities to Type Classes

**Roc:**
```roc
# Using ability constraint
toString : a -> Str where a implements Inspect
toString = \value ->
    Inspect.toStr(value)

# Custom type automatically implements abilities
User : {
    name : Str,
    age : U32,
}

user = { name: "Alice", age: 30 }
expect Inspect.toStr(user) == "{ name: \"Alice\", age: 30 }"
```

**Haskell:**
```haskell
-- Type class constraint
toString :: (Show a) => a -> String
toString value = show value

-- Custom type with deriving
data User = User
    { name :: Text
    , age :: Word32
    } deriving (Show, Eq)

user = User "Alice" 30
-- show user == "User {name = \"Alice\", age = 30}"
```

**Why this translation:**
- Roc abilities are similar to Haskell type classes
- Roc auto-derives abilities; Haskell requires explicit `deriving` clauses
- Haskell has more established type classes (Functor, Monad, etc.)

### Pattern 5: List Pipeline Operations

**Roc:**
```roc
numbers = [1, 2, 3, 4, 5]

result = numbers
    |> List.map(\n -> n * 2)
    |> List.keepIf(\n -> n > 5)
    |> List.walk(0, \acc, n -> acc + n)
```

**Haskell:**
```haskell
import Data.Function ((&))

numbers = [1, 2, 3, 4, 5]

-- Using function composition (right to left)
result = foldr (+) 0 . filter (>5) . map (*2) $ numbers

-- Or using & operator (left to right, like Roc)
result' = numbers
    & map (*2)
    & filter (>5)
    & foldr (+) 0
```

**Why this translation:**
- Roc's `|>` maps to Haskell's `&` operator
- Function composition `.` is more idiomatic but reads backward
- Haskell's `foldr`/`foldl` map to Roc's `List.walk`

---

## Error Handling

### Result → Either Translation

**Type Mapping:**
```
Roc:     Result a e
         [Ok a, Err e]

Haskell: Either e a
         Left e | Right a
```

**Key Difference:** Type parameters are reversed!

**Roc:**
```roc
parseAge : Str -> Result U32 [ParseError Str]
parseAge = \str ->
    when Str.toU32(str) is
        Ok(n) -> Ok(n)
        Err(_) -> Err(ParseError("Not a valid number"))

# Chain operations
validateUser : Str, Str -> Result User [ParseError Str, InvalidEmail]
validateUser = \ageStr, emailStr ->
    age = parseAge!(ageStr)
    email = validateEmail!(emailStr)
    Ok({ name: "User", age, email })
```

**Haskell:**
```haskell
import Text.Read (readMaybe)
import Data.Text (Text)

data ValidationError
    = ParseError String
    | InvalidEmail
    deriving (Show, Eq)

parseAge :: Text -> Either ValidationError Word32
parseAge str =
    case readMaybe (unpack str) of
        Just n -> Right n
        Nothing -> Left (ParseError "Not a valid number")

-- Chain with do-notation
validateUser :: Text -> Text -> Either ValidationError User
validateUser ageStr emailStr = do
    age <- parseAge ageStr
    email <- validateEmail emailStr
    return $ User "User" age email
```

### Multiple Error Types

**Roc:**
```roc
# Tag union for multiple errors
Error : [ParseError Str, DivByZero, NetworkError Str]

process : Str, Str -> Result I64 Error
process = \aStr, bStr ->
    a = Str.toI64!(aStr) |> Result.mapErr(\_ -> ParseError("Invalid a"))
    b = Str.toI64!(bStr) |> Result.mapErr(\_ -> ParseError("Invalid b"))
    divide!(a, b) |> Result.mapErr(\_ -> DivByZero)
```

**Haskell:**
```haskell
data Error
    = ParseError String
    | DivByZero
    | NetworkError String
    deriving (Show, Eq)

process :: Text -> Text -> Either Error Int64
process aStr bStr = do
    a <- parseI64 aStr `mapLeft` const (ParseError "Invalid a")
    b <- parseI64 bStr `mapLeft` const (ParseError "Invalid b")
    divide a b `mapLeft` const DivByZero
  where
    mapLeft f (Left e) = Left (f e)
    mapLeft _ (Right x) = Right x
```

---

## Platform Model Translation

### Roc Platform/Application → Haskell IO

**Roc Application:**
```roc
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/..."
}

import pf.Stdout
import pf.Task exposing [Task]
import pf.File

main : Task {} []
main =
    content = File.readUtf8!("input.txt")
    processed = Str.toUpper(content)
    File.writeUtf8!("output.txt", processed)
    Stdout.line!("Done!")
```

**Haskell:**
```haskell
import qualified Data.Text.IO as TIO
import qualified Data.Text as T
import System.IO

main :: IO ()
main = do
    content <- TIO.readFile "input.txt"
    let processed = T.toUpper content
    TIO.writeFile "output.txt" processed
    putStrLn "Done!"
```

**Key Differences:**
- Roc separates platform (I/O) from application (pure code)
- Haskell uses IO monad throughout
- Roc's `!` suffix maps to Haskell's `<-` in do-notation
- Both use monadic composition for effects

### Task Error Handling

**Roc:**
```roc
readConfig : Str -> Task Config [FileNotFound, ParseError Str]
readConfig = \path ->
    content = File.readUtf8!(path)  # May fail with FileNotFound
    when parseJson(content) is
        Ok(config) -> Task.ok(config)
        Err(e) -> Task.err(ParseError(e))
```

**Haskell:**
```haskell
import Control.Monad.Except
import qualified Data.Text.IO as TIO

data ConfigError
    = FileNotFound
    | ParseError String
    deriving (Show, Eq)

readConfig :: FilePath -> ExceptT ConfigError IO Config
readConfig path = do
    contentE <- liftIO $ try $ TIO.readFile path
    content <- case contentE of
        Left (_ :: IOException) -> throwError FileNotFound
        Right c -> return c
    case parseJson content of
        Left e -> throwError (ParseError e)
        Right config -> return config
```

**Why this translation:**
- Roc Tasks with error types map to `ExceptT err IO a`
- Both provide error propagation and recovery
- Haskell separates IO errors (exceptions) from domain errors (Either/ExceptT)

---

## Concurrency Patterns

### Roc Task Concurrency → Haskell Async

**Roc:**
```roc
# Platform-provided concurrency
import pf.Task exposing [Task]
import pf.Http

fetchBoth : Task (Str, Str) [HttpErr]
fetchBoth =
    # Platform may execute concurrently
    Task.parallel2(
        Http.get("http://api.example.com/1"),
        Http.get("http://api.example.com/2")
    )
```

**Haskell:**
```haskell
import Control.Concurrent.Async
import Network.HTTP.Simple

fetchBoth :: IO (ByteString, ByteString)
fetchBoth = concurrently
    (getResponseBody <$> httpBS "http://api.example.com/1")
    (getResponseBody <$> httpBS "http://api.example.com/2")

-- Or with race (first wins)
fetchFirst :: IO ByteString
fetchFirst = race
    (getResponseBody <$> httpBS "http://api.example.com/1")
    (getResponseBody <$> httpBS "http://api.example.com/2")
    >>= either return return
```

**Why this translation:**
- Roc delegates all concurrency to the platform
- Haskell provides explicit concurrency primitives (async library)
- Both provide structured concurrency with proper cleanup

### No Direct Threading

**Roc:**
```roc
# Roc applications don't directly manage threads
# All concurrency is platform capability
# Task composition is the only abstraction
```

**Haskell:**
```haskell
import Control.Concurrent

-- Haskell provides lightweight threads
main = do
    forkIO $ do
        threadDelay 1000000
        putStrLn "Hello from thread"
    putStrLn "Main thread continues"
    threadDelay 2000000

-- Use async for structured concurrency (recommended)
import Control.Concurrent.Async

main' = do
    a <- async $ do
        threadDelay 1000000
        return "result"
    result <- wait a
    print result
```

---

## Laziness Translation

### Roc (Strict) → Haskell (Lazy)

**Roc:**
```roc
# Roc is strict by default
numbers = [1, 2, 3, 4, 5]

# This evaluates immediately
doubled = List.map(numbers, \n -> n * 2)

# Infinite lists require Stream or explicit laziness
naturals = Stream.iterate(0, \n -> n + 1)
```

**Haskell:**
```haskell
-- Haskell is lazy by default
numbers = [1, 2, 3, 4, 5]

-- This creates a thunk, evaluated on demand
doubled = map (*2) numbers

-- Infinite lists work naturally
naturals = iterate (+1) 0
take 10 naturals  -- [0,1,2,3,4,5,6,7,8,9]

-- Force strict evaluation when needed
import Control.DeepSeq

strictDoubled = force $ map (*2) numbers
```

**Key Differences:**
- Roc evaluates eagerly; add explicit limits before processing
- Haskell evaluates lazily; infinite structures work out of the box
- When converting, be careful with space leaks in Haskell (use `seq`, `$!`, or strict data structures)

---

## Common Pitfalls

### 1. Result Type Parameter Order

```
❌ Assuming Roc Result and Haskell Either have same param order
✓ Remember: Result a e → Either e a (reversed!)
```

**Roc:**
```roc
divide : I64, I64 -> Result I64 [DivByZero]
#                    Result ^ok  ^err
```

**Haskell:**
```haskell
divide :: Int64 -> Int64 -> Either DivError Int64
--                          Either ^err     ^ok
```

### 2. Structural vs Nominal Types

```
❌ Using Haskell tuples for Roc records
✓ Define proper ADTs with record syntax
```

**Roc:**
```roc
user = { name: "Alice", age: 30 }  # Structural type
```

**Haskell:**
```haskell
-- Wrong: (Text, Word32)  -- Positional, no field names
-- Right:
data User = User { name :: Text, age :: Word32 }
```

### 3. Platform Boundary Confusion

```
❌ Trying to replicate Roc's platform model in Haskell
✓ Use IO monad or mtl transformers for effects
```

### 4. Strict vs Lazy Semantics

```
❌ Assuming Roc's eager evaluation in Haskell
✓ Add explicit limits (take, drop) before consuming infinite lists
✓ Use strict variants when performance matters (foldl', force)
```

### 5. Ability Auto-Derivation

```
❌ Expecting Haskell to auto-derive like Roc
✓ Add explicit deriving clauses (Show, Eq, etc.)
```

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| GHC | Haskell compiler | Primary compiler |
| GHCi | REPL | Interactive development |
| Stack | Build tool | Dependency management, reproducible builds |
| Cabal | Build tool | Alternative to Stack |
| HLint | Linter | Code suggestions |
| Ormolu / Brittany | Formatter | Code formatting |
| hspec / QuickCheck | Testing | Unit and property-based tests |

No direct Roc→Haskell transpiler exists; conversion is manual.

---

## Examples

### Example 1: Simple - Tag Union Pattern Matching

**Before (Roc):**
```roc
Status : [Pending, Approved, Rejected]

handleStatus : Status -> Str
handleStatus = \status ->
    when status is
        Pending -> "Waiting..."
        Approved -> "Done!"
        Rejected -> "Failed"
```

**After (Haskell):**
```haskell
data Status = Pending | Approved | Rejected
    deriving (Show, Eq)

handleStatus :: Status -> String
handleStatus Pending = "Waiting..."
handleStatus Approved = "Done!"
handleStatus Rejected = "Failed"
```

### Example 2: Medium - Result with Error Propagation

**Before (Roc):**
```roc
divide : I64, I64 -> Result I64 [DivByZero]
divide = \a, b ->
    if b == 0 then
        Err(DivByZero)
    else
        Ok(a // b)

calculate : I64, I64, I64 -> Result I64 [DivByZero]
calculate = \a, b, c ->
    x = divide!(a, b)
    y = divide!(x, c)
    Ok(y)

# Usage
when calculate(20, 4, 2) is
    Ok(result) -> Num.toStr(result)
    Err(DivByZero) -> "Error: division by zero"
```

**After (Haskell):**
```haskell
data DivError = DivByZero
    deriving (Show, Eq)

divide :: Int64 -> Int64 -> Either DivError Int64
divide _ 0 = Left DivByZero
divide a b = Right (a `div` b)

calculate :: Int64 -> Int64 -> Int64 -> Either DivError Int64
calculate a b c = do
    x <- divide a b
    y <- divide x c
    return y

-- Usage
result = case calculate 20 4 2 of
    Right r -> show r
    Left DivByZero -> "Error: division by zero"
```

### Example 3: Complex - Platform Application to IO

**Before (Roc):**
```roc
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/..."
}

import pf.Stdout
import pf.File
import pf.Task exposing [Task]

Config : { port : U16, host : Str }

parseConfig : Str -> Result Config [ParseError Str]
parseConfig = \content ->
    # Parse JSON content
    when Json.decode(content) is
        Ok(config) -> Ok(config)
        Err(e) -> Err(ParseError(e))

main : Task {} []
main =
    # Read config file
    content = File.readUtf8!("config.json")

    # Parse config
    config = when parseConfig(content) is
        Ok(c) -> Task.ok!(c)
        Err(ParseError(msg)) ->
            Stdout.line!("Config error: \(msg)")
            Task.err!(ConfigError)

    # Use config
    Stdout.line!("Starting server on \(config.host):\(Num.toStr(config.port))")
```

**After (Haskell):**
```haskell
{-# LANGUAGE DeriveGeneric #-}

import qualified Data.Text.IO as TIO
import qualified Data.Text as T
import Data.Aeson (FromJSON, eitherDecode)
import GHC.Generics
import Control.Monad.Except
import qualified Data.ByteString.Lazy as BL

data Config = Config
    { port :: Word16
    , host :: Text
    } deriving (Generic, Show)

instance FromJSON Config

data AppError
    = ParseError String
    | ConfigError
    deriving (Show, Eq)

parseConfig :: BL.ByteString -> Either AppError Config
parseConfig content =
    case eitherDecode content of
        Right config -> Right config
        Left err -> Left (ParseError err)

main :: IO ()
main = do
    result <- runExceptT $ do
        -- Read config file
        content <- liftIO $ BL.readFile "config.json"

        -- Parse config
        config <- case parseConfig content of
            Right c -> return c
            Left (ParseError msg) -> do
                liftIO $ putStrLn $ "Config error: " ++ msg
                throwError ConfigError

        -- Use config
        liftIO $ putStrLn $
            "Starting server on " ++ T.unpack (host config)
            ++ ":" ++ show (port config)

    case result of
        Left err -> putStrLn $ "Error: " ++ show err
        Right _ -> return ()
```

---

## See Also

For more examples and patterns, see:

- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-elm-haskell` - Similar pure functional language conversion
- `lang-roc-dev` - Roc development patterns
- `lang-haskell-dev` - Haskell development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Compare Roc Task model with Haskell async/STM
- `patterns-serialization-dev` - JSON handling across languages
- `patterns-metaprogramming-dev` - Template Haskell vs no metaprogramming in Roc
