---
name: convert-haskell-roc
description: Convert Haskell code to idiomatic Roc. Use when migrating Haskell applications to Roc's platform model, translating lazy pure functional code to strict platform-based architecture, or refactoring type class based designs to ability-based patterns. Extends meta-convert-dev with Haskell-to-Roc specific patterns.
---

# Convert Haskell to Roc

Convert Haskell code to idiomatic Roc. This skill extends `meta-convert-dev` with Haskell-to-Roc specific type mappings, idiom translations, and tooling for translating from lazy pure functional programming to strict platform-based architecture.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Haskell's HM types → Roc's structural types
- **Idiom translations**: Type classes → abilities, monads → platform effects
- **Error handling**: Maybe/Either → Result with tag unions
- **Evaluation strategy**: Lazy → strict evaluation
- **Concurrency patterns**: STM/async → platform-managed tasks
- **Platform architecture**: GHC runtime → platform/application separation
- **Paradigm shift**: Pure lazy functional → strict functional with platform effects

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Haskell language fundamentals - see `lang-haskell-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Reverse conversion (Roc → Haskell) - see `convert-roc-haskell`
- Advanced type system features (GADTs, Type Families, DataKinds)

---

## Quick Reference

| Haskell | Roc | Notes |
|---------|-----|-------|
| `f :: a -> b`<br>`f x = ...` | `f : a -> b`<br>`f = \x -> ...` | Function definition |
| `String` | `Str` | String type |
| `Int` / `Integer` | `I64` / `I32` | Integer types (Roc fixed-size) |
| `Double` / `Float` | `F64` / `F32` | Floating point |
| `Bool` | `Bool` | Boolean type |
| `Nothing` / `Just a` | `None` / `Some a` | Optional values via tag unions |
| `[a]` | `List a` | Lists (Roc is strict, not lazy) |
| `(a, b)` | `(a, b)` | Tuples (same syntax) |
| `data` | Record or tag union | Depends on usage |
| `Maybe a` | `[Some a, None]` | Optional pattern |
| `Either e a` | `Result a e` | Error handling (note reversed order) |
| `IO a` | `Task a err` | Effects via platform |
| `class C a where` | Ability constraint | Type classes → abilities |
| `case x of` | `when x is` | Pattern matching |
| `do` notation | `!` suffix for tasks | Monadic sequencing |

---

## When Converting Code

1. **Analyze source thoroughly** - understand lazy semantics before converting
2. **Map types first** - convert type classes to ability constraints
3. **Identify strict vs lazy** - translate infinite lists to finite or iterators
4. **Preserve semantics** over syntax similarity
5. **Adopt platform model** - separate pure logic from I/O via platform boundary
6. **Handle monads explicitly** - IO → Task, Maybe → tag union, Either → Result
7. **Test equivalence** - same inputs → same outputs (watch for strictness differences)
8. **Leverage abilities** - replace type class constraints with ability constraints

---

## Type System Mapping

### Primitive Types

| Haskell | Roc | Notes |
|---------|-----|-------|
| `Int` | `I64` | 64-bit signed (platform-dependent in Haskell) |
| `Integer` | N/A | Arbitrary precision - use fixed size or external library |
| `Double` | `F64` | 64-bit floating point |
| `Float` | `F32` | 32-bit floating point |
| `Bool` | `Bool` | Direct mapping |
| `Char` | `U32` | Unicode code point |
| `()` | `{}` | Unit type |
| `String` | `Str` | String type |

**Important differences:**
- Haskell: Arbitrary precision `Integer`, lazy evaluation
- Roc: Fixed-size integers, strict evaluation
- Haskell: `String` is `[Char]` (linked list), lazy
- Roc: `Str` is UTF-8 byte array, strict

### Collection Types

| Haskell | Roc | Notes |
|---------|-----|-------|
| `[a]` | `List a` | **LAZY** in Haskell, **STRICT** in Roc |
| `(a, b)` | `(a, b)` | Tuples (same syntax) |
| `(a, b, c)` | `(a, b, c)` | N-tuples |
| `Map k v` | `Dict k v` | Dictionaries (requires `Hash` + `Eq` abilities) |
| `Set a` | `Set a` | Sets (requires `Hash` + `Eq` abilities) |

**Lazy → Strict Conversion:**
```haskell
-- Haskell: Infinite list (lazy)
naturals :: [Integer]
naturals = [0..]

take 10 naturals  -- [0,1,2,3,4,5,6,7,8,9]
```

```roc
# Roc: Must be finite or use generator pattern
naturals : List I64
naturals = List.range { start: At 0, end: At 1000000 }

List.take naturals 10  # [0,1,2,3,4,5,6,7,8,9]

# Alternative: Iterator/Stream pattern (platform-provided)
# naturalsStream = Stream.iterate 0 (\n -> n + 1)
# Stream.take naturalsStream 10
```

### Composite Types

| Haskell | Roc | Notes |
|---------|-----|-------|
| `data Point = Point Int Int` | `Point : { x : I64, y : I64 }` | Product type → record |
| `data Shape = Circle Float \| Rect Float Float` | `Shape : [Circle F64, Rect F64 F64]` | Sum type → tag union |
| `newtype Age = Age Int` | `Age := I64` | Newtype → opaque type |
| `type Name = String` | `Name : Str` | Type alias |

---

## Idiom Translation

### Pattern: Maybe/Optional Values

**Haskell:**
```haskell
findUser :: Int -> Maybe User
findUser 1 = Just (User "Alice" 30)
findUser _ = Nothing

-- Using Maybe
getUserName :: Int -> String
getUserName uid = case findUser uid of
    Just user -> name user
    Nothing -> "Unknown"

-- With do notation
getOlderUser :: Int -> Maybe User
getOlderUser uid = do
    user <- findUser uid
    return $ user { age = age user + 1 }
```

**Roc:**
```roc
findUser : I64 -> [Some User, None]
findUser = \uid ->
    if uid == 1 then
        Some { name: "Alice", age: 30 }
    else
        None

# Using pattern matching
getUserName : I64 -> Str
getUserName = \uid ->
    when findUser uid is
        Some user -> user.name
        None -> "Unknown"

# No monadic do - use direct manipulation
getOlderUser : I64 -> [Some User, None]
getOlderUser = \uid ->
    when findUser uid is
        Some user -> Some { user & age: user.age + 1 }
        None -> None
```

**Why this translation:**
- Roc uses structural tag unions instead of Maybe type constructor
- No monadic bind for optional values - use explicit pattern matching
- More verbose but clearer control flow

### Pattern: Either/Error Handling

**Haskell:**
```haskell
divide :: Float -> Float -> Either String Float
divide _ 0 = Left "Division by zero"
divide x y = Right (x / y)

-- Chaining with do notation
calculate :: Float -> Float -> Float -> Either String Float
calculate a b c = do
    x <- divide a b
    y <- divide x c
    return y

-- With error mapping
parseAge :: String -> Either String Int
parseAge str = case reads str of
    [(n, "")] -> if n >= 0
                 then Right n
                 else Left "Age must be non-negative"
    _ -> Left "Not a valid number"
```

**Roc:**
```roc
divide : F64, F64 -> Result F64 [DivByZero]
divide = \x, y ->
    if y == 0 then
        Err DivByZero
    else
        Ok (x / y)

# Chaining with try operator (!)
calculate : F64, F64, F64 -> Result F64 [DivByZero]
calculate = \a, b, c ->
    x = divide! a b  # Early return on Err
    y = divide! x c
    Ok y

# With error mapping
parseAge : Str -> Result I64 [ParseError Str, InvalidAge]
parseAge = \str ->
    n = Str.toI64! str |> Result.mapErr \_ -> ParseError "Not a number"

    if n >= 0 then
        Ok n
    else
        Err InvalidAge
```

**Why this translation:**
- Haskell `Either e a` maps to Roc `Result a e` (note reversed order!)
- Haskell's `do` notation maps to Roc's `!` try operator
- Tag unions allow more expressive error types than String

### Pattern: IO Monad → Task

**Haskell:**
```haskell
main :: IO ()
main = do
    putStrLn "What is your name?"
    name <- getLine
    putStrLn $ "Hello, " ++ name

-- Reading files
readConfig :: FilePath -> IO String
readConfig path = do
    content <- readFile path
    return content
```

**Roc:**
```roc
import pf.Stdout
import pf.Stdin
import pf.Task exposing [Task]

main : Task {} []
main =
    Stdout.line! "What is your name?"
    name = Stdin.line!
    Stdout.line! "Hello, \(name)"

# Reading files
import pf.File

readConfig : Str -> Task Str [FileReadErr]
readConfig = \path ->
    content = File.readUtf8! path
    Task.ok content
```

**Why this translation:**
- Haskell's `IO` monad maps to Roc's `Task` type
- Platform provides I/O primitives (Stdout, File, etc.)
- No explicit `return` - use `Task.ok` for wrapping pure values
- `!` suffix for task sequencing (like Haskell's `<-`)

### Pattern: Type Classes → Abilities

**Haskell:**
```haskell
-- Type class definition
class Eq a where
    (==) :: a -> a -> Bool

class Show a where
    show :: a -> String

-- Using type class constraints
printEqual :: (Eq a, Show a) => a -> a -> IO ()
printEqual x y = putStrLn $ if x == y
    then show x ++ " equals " ++ show y
    else show x ++ " not equals " ++ show y

-- Deriving instances
data Color = Red | Green | Blue
    deriving (Eq, Show)
```

**Roc:**
```roc
# Abilities are automatically derived for records and tags
Color : [Red, Green, Blue]

# Ability constraints in function signatures
printEqual : a, a -> Task {} [] where a implements Eq & Inspect
printEqual = \x, y ->
    msg = if x == y then
        "\(Inspect.toStr x) equals \(Inspect.toStr y)"
    else
        "\(Inspect.toStr x) not equals \(Inspect.toStr y)"
    Stdout.line! msg

# Automatic derivation
User : {
    name : Str,
    age : U32,
}
# User automatically has: Eq, Hash, Inspect, Encode, Decode

user1 = { name: "Alice", age: 30 }
user2 = { name: "Alice", age: 30 }
user1 == user2  # Works automatically
```

**Why this translation:**
- Haskell type classes map to Roc abilities
- Haskell `Show` maps to Roc `Inspect`
- Roc derives abilities automatically for records/tags
- No manual instance definitions needed for common abilities

### Pattern: Functor/Applicative/Monad → Direct Operations

**Haskell:**
```haskell
-- Functor: fmap
doubled :: Maybe Int -> Maybe Int
doubled = fmap (*2)

-- Applicative
createUser :: Maybe String -> Maybe Int -> Maybe User
createUser mName mAge = User <$> mName <*> mAge

-- Monad: bind
chain :: Maybe Int -> Maybe Int
chain mx = mx >>= \x -> return (x * 2)
```

**Roc:**
```roc
# No Functor/Applicative/Monad abstractions
# Use explicit pattern matching or helper functions

doubled : [Some I64, None] -> [Some I64, None]
doubled = \m ->
    when m is
        Some x -> Some (x * 2)
        None -> None

# Or use Result.map for Result type
doubled = \m ->
    Result.map m \x -> x * 2

# No applicative - construct directly
createUser : [Some Str, None], [Some U32, None] -> [Some User, None]
createUser = \mName, mAge ->
    when (mName, mAge) is
        (Some name, Some age) -> Some { name, age }
        _ -> None

# Chaining
chain : [Some I64, None] -> [Some I64, None]
chain = \mx ->
    when mx is
        Some x -> Some (x * 2)
        None -> None
```

**Why this translation:**
- Roc doesn't have Functor/Applicative/Monad abstractions
- Use explicit pattern matching for clarity
- Platform-specific types (Task, Result) may have helper functions
- Simpler mental model at the cost of some verbosity

---

## Evaluation Strategy

### Lazy → Strict Translation

**Haskell (Lazy):**
```haskell
-- Infinite Fibonacci
fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

take 10 fibs  -- Only computes first 10

-- Lazy evaluation allows cycles
ones :: [Int]
ones = 1 : ones
```

**Roc (Strict):**
```roc
# Must generate finite list or use explicit generator
fibList : I64 -> List I64
fibList = \n ->
    List.walk (List.range { start: At 0, end: Before n })
        [0, 1]
        \fibs, _ ->
            a = List.get fibs (List.len fibs - 2)
                |> Result.withDefault 0
            b = List.get fibs (List.len fibs - 1)
                |> Result.withDefault 0
            List.append fibs (a + b)

fibList 10  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Alternative: Iterator pattern (if platform provides)
# fibStream = Stream.iterate (0, 1) \(a, b) -> (b, a + b)
#             |> Stream.map \(a, _) -> a
# Stream.take fibStream 10
```

**Key differences:**
- Haskell: Infinite structures work naturally (lazy)
- Roc: Must use finite structures or explicit generators
- Haskell: Evaluation on demand
- Roc: Immediate evaluation

---

## Concurrency Patterns

### STM → Platform Tasks

**Haskell:**
```haskell
import Control.Concurrent.STM

type Account = TVar Int

transfer :: Account -> Account -> Int -> STM ()
transfer from to amount = do
    fromBal <- readTVar from
    when (fromBal >= amount) $ do
        modifyTVar from (subtract amount)
        modifyTVar to (+ amount)

-- Run transaction
main = do
    acc1 <- newTVarIO 1000
    acc2 <- newTVarIO 0
    atomically $ transfer acc1 acc2 500
```

**Roc:**
```roc
# No built-in STM - platform manages state
# Pattern: Use platform-provided state management

import pf.Task exposing [Task]

# Platform-specific state API (example)
# This depends on your platform implementation

Account : { balance : I64 }

transfer : Account, Account, I64 -> Task {} [InsufficientFunds]
transfer = \from, to, amount ->
    if from.balance >= amount then
        # Platform handles atomicity
        newFrom = { from & balance: from.balance - amount }
        newTo = { to & balance: to.balance + amount }
        Task.ok {}
    else
        Task.err InsufficientFunds

# Usage
main : Task {} []
main =
    acc1 = { balance: 1000 }
    acc2 = { balance: 0 }
    transfer! acc1 acc2 500
    Task.ok {}
```

**Why this translation:**
- Haskell: Built-in STM for transactional memory
- Roc: Platform manages concurrency and state
- Application code stays pure; platform handles atomicity
- Platform-specific APIs vary

### Async → Task-Based

**Haskell:**
```haskell
import Control.Concurrent.Async

main :: IO ()
main = do
    (res1, res2) <- concurrently
        (fetchUrl "http://example.com/1")
        (fetchUrl "http://example.com/2")
    print (res1, res2)
```

**Roc:**
```roc
import pf.Task exposing [Task]
import pf.Http

# Platform may provide concurrent execution
main : Task {} []
main =
    # Sequential by default
    res1 = Http.get! "http://example.com/1"
    res2 = Http.get! "http://example.com/2"

    # Or platform-provided parallel execution (if available)
    # (res1, res2) = Task.parallel2!(
    #     Http.get "http://example.com/1",
    #     Http.get "http://example.com/2"
    # )

    Stdout.line! (Inspect.toStr (res1, res2))
```

**Why this translation:**
- Haskell: Explicit async library
- Roc: Platform controls concurrency
- Application code composes tasks; platform decides execution strategy

---

## Common Pitfalls

### 1. Lazy vs Strict - Infinite Lists

**Problem:** Direct translation of lazy infinite structures

```haskell
-- Haskell: Works fine
naturals = [0..]
evens = filter even naturals
```

```roc
# Roc: Would hang forever!
# naturals = List.range { start: At 0, end: At maxI64 }  # Too large
# evens = List.keepIf naturals Num.isEven  # Never completes
```

**Fix:** Use finite ranges or iterators
```roc
# Generate finite range
naturals = List.range { start: At 0, end: Before 1000 }
evens = List.keepIf naturals Num.isEven

# Or use stream/iterator pattern (if platform provides)
```

### 2. Type Class Constraints → Ability Constraints

**Problem:** Assuming type class polymorphism works the same

```haskell
-- Haskell: Polymorphic function
sort :: Ord a => [a] -> [a]
sort = ...
```

```roc
# Roc: Ability constraint
sort : List a -> List a where a implements Ord
sort = \list -> ...

# BUT: Roc doesn't have Ord ability built-in!
# Must use specific types or platform-provided sorting
```

**Fix:** Use concrete types or platform functions
```roc
# Concrete type
sortInts : List I64 -> List I64
sortInts = List.sortAsc

# Or use platform's polymorphic sort (if available)
```

### 3. IO Monad → Task Platform Boundary

**Problem:** Mixing pure and impure code

```haskell
-- Haskell: IO monad isolates effects
main :: IO ()
main = do
    content <- readFile "config.txt"  -- IO
    let result = process content       -- Pure
    print result                        -- IO
```

```roc
# Roc: Clear platform boundary
main : Task {} []
main =
    content = File.readUtf8! "config.txt"  # Task (platform)
    result = process content                # Pure function
    Stdout.line! (Inspect.toStr result)     # Task (platform)

# Pure function (no Task)
process : Str -> Str
process = \text ->
    Str.toUpper text
```

**Key difference:**
- Haskell: IO type tracks effects
- Roc: Platform boundary separates pure from effectful
- Pure functions in Roc have no Task type

### 4. Monadic Do Notation → Try Operator

**Problem:** Expecting do-notation to work

```haskell
-- Haskell
parseUser :: String -> Either String User
parseUser str = do
    age <- parseAge str
    email <- parseEmail str
    return $ User email age
```

```roc
# Roc: Use try operator (!)
parseUser : Str -> Result User [ParseErr Str]
parseUser = \str ->
    age = parseAge! str      # Early return on Err
    email = parseEmail! str  # Early return on Err
    Ok { email, age }
```

**Key difference:**
- Haskell: `do` notation for any monad
- Roc: `!` operator only for Result and Task

### 5. Type Inference Differences

**Problem:** Expecting Haskell-level inference

```haskell
-- Haskell: Polymorphic
id x = x  -- Inferred: a -> a
```

```roc
# Roc: Usually needs annotation for polymorphic functions
identity : a -> a
identity = \x -> x

# Or will infer concrete type from usage
id = \x -> x  # Type depends on how it's used
```

**Fix:** Add type signatures for polymorphic functions

---

## Testing Strategy

### Property Testing: QuickCheck → Roc Expect

**Haskell (QuickCheck):**
```haskell
import Test.QuickCheck

prop_reverse :: [Int] -> Bool
prop_reverse xs = reverse (reverse xs) == xs

prop_sortLength :: [Int] -> Bool
prop_sortLength xs = length (sort xs) == length xs
```

**Roc (Expect):**
```roc
# Inline property-style tests
expect
    xs = [1, 2, 3, 4, 5]
    List.reverse (List.reverse xs) == xs

expect
    xs = [3, 1, 4, 1, 5, 9]
    List.len (List.sortAsc xs) == List.len xs

# For comprehensive property testing, use external fuzzer
# or generate test cases
```

**Limitations:**
- Roc: No built-in property testing framework
- Use expect for inline tests
- Generate test cases externally or use platform-provided fuzzing

---

## Tooling

| Haskell Tool | Roc Equivalent | Notes |
|--------------|----------------|-------|
| GHC | `roc` compiler | Compiles to native or LLVM IR |
| GHCi (REPL) | `roc repl` | Interactive REPL |
| Stack / Cabal | Platforms | Dependency management via platforms |
| HSpec / Tasty | `roc test` | Built-in testing with expect |
| QuickCheck | N/A | No built-in property testing |
| hlint | N/A | No Roc linter yet |
| Hoogle | `roc docs` | Generate docs from code |

---

## Examples

### Example 1: Simple - Maybe to Tag Union

**Before (Haskell):**
```haskell
data User = User { name :: String, age :: Int }

findUser :: Int -> Maybe User
findUser 1 = Just (User "Alice" 30)
findUser _ = Nothing

displayUser :: Int -> String
displayUser uid = case findUser uid of
    Just user -> "Found: " ++ name user
    Nothing -> "Not found"
```

**After (Roc):**
```roc
User : {
    name : Str,
    age : I64,
}

findUser : I64 -> [Some User, None]
findUser = \uid ->
    if uid == 1 then
        Some { name: "Alice", age: 30 }
    else
        None

displayUser : I64 -> Str
displayUser = \uid ->
    when findUser uid is
        Some user -> "Found: \(user.name)"
        None -> "Not found"
```

### Example 2: Medium - Either Error Handling

**Before (Haskell):**
```haskell
divide :: Double -> Double -> Either String Double
divide _ 0 = Left "Division by zero"
divide x y = Right (x / y)

validateAge :: Int -> Either String Int
validateAge age
    | age < 0 = Left "Age cannot be negative"
    | age > 150 = Left "Age too high"
    | otherwise = Right age

createUser :: String -> Int -> Either String User
createUser email age = do
    validAge <- validateAge age
    return $ User email validAge
```

**After (Roc):**
```roc
divide : F64, F64 -> Result F64 [DivByZero]
divide = \x, y ->
    if y == 0 then
        Err DivByZero
    else
        Ok (x / y)

validateAge : I64 -> Result I64 [NegativeAge, AgeTooHigh]
validateAge = \age ->
    if age < 0 then
        Err NegativeAge
    else if age > 150 then
        Err AgeTooHigh
    else
        Ok age

createUser : Str, I64 -> Result User [NegativeAge, AgeTooHigh]
createUser = \email, age ->
    validAge = validateAge! age
    Ok { email, age: validAge }
```

### Example 3: Complex - IO Monad to Platform Task

**Before (Haskell):**
```haskell
import System.IO
import Control.Exception

data Config = Config { port :: Int, host :: String }
    deriving (Show, Read)

readConfig :: FilePath -> IO (Either String Config)
readConfig path = catch
    (do
        content <- readFile path
        case reads content of
            [(config, "")] -> return $ Right config
            _ -> return $ Left "Invalid config format"
    )
    (\(e :: IOException) -> return $ Left $ show e)

runApp :: Config -> IO ()
runApp config = do
    putStrLn $ "Starting server on " ++ host config
    putStrLn $ "Port: " ++ show (port config)
    -- Actual server logic here

main :: IO ()
main = do
    result <- readConfig "config.txt"
    case result of
        Right config -> runApp config
        Left err -> putStrLn $ "Error: " ++ err
```

**After (Roc):**
```roc
import pf.Stdout
import pf.File
import pf.Task exposing [Task]

Config : {
    port : I64,
    host : Str,
}

readConfig : Str -> Task Config [FileReadErr, InvalidFormat Str]
readConfig = \path ->
    content = File.readUtf8! path
        |> Task.mapErr \_ -> FileReadErr

    # Parse JSON or custom format
    # For simplicity, assume JSON parsing available via platform
    config = parseConfig! content
        |> Task.mapErr \_ -> InvalidFormat "Invalid config format"

    Task.ok config

parseConfig : Str -> Result Config [ParseErr]
parseConfig = \content ->
    # Parsing logic (simplified)
    # In real code, use JSON parser
    Ok { port: 8080, host: "localhost" }

runApp : Config -> Task {} []
runApp = \config ->
    Stdout.line! "Starting server on \(config.host)"
    Stdout.line! "Port: \(Num.toStr config.port)"
    # Actual server logic here
    Task.ok {}

main : Task {} []
main =
    when readConfig "config.txt" is
        Ok config -> runApp! config
        Err FileReadErr -> Stdout.line! "Error: Could not read config file"
        Err (InvalidFormat msg) -> Stdout.line! "Error: \(msg)"
```

---

## Limitations (lang-roc-dev gaps)

The following areas required external research due to incomplete coverage in `lang-roc-dev`:

1. **Zero/Default Values**: Roc has optional fields via tag unions, but no comprehensive Default trait equivalent
2. **Serialization Idioms**: Encode/Decode abilities mentioned but lacks practical examples (JSON, YAML)
3. **Build/Deps**: Package structure shown but no `roc build`, `roc test`, `roc run` command documentation

These gaps have been addressed in this skill through:
- External Roc documentation research
- Inference from Roc design philosophy
- Comparison with similar languages

See issues #XXX, #YYY, #ZZZ for tracking improvements to lang-roc-dev.

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-clojure-roc` - Dynamic FP to static FP (similar paradigm shift)
- `lang-haskell-dev` - Haskell development patterns
- `lang-roc-dev` - Roc development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - STM vs Task models across languages
- `patterns-serialization-dev` - JSON, YAML serialization patterns
- `patterns-metaprogramming-dev` - Type classes vs abilities comparison

---

## References

- [Roc Tutorial](https://www.roc-lang.org/tutorial)
- [Roc vs Haskell Comparison](https://www.roc-lang.org/faq.html#how-does-roc-compare-to-haskell)
- [Haskell to Roc Migration Guide](https://github.com/roc-lang/roc/wiki/Haskell-to-Roc)
- [Learn You a Haskell](http://learnyouahaskell.com/)
- [Real World Haskell](http://book.realworldhaskell.org/)
