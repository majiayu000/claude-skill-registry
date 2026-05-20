---
name: convert-haskell-elm
description: Convert Haskell code to idiomatic Elm. Use when migrating Haskell logic to frontend applications, translating pure functional patterns to Elm's architecture, or refactoring Haskell code for web UI. Extends meta-convert-dev with Haskell-to-Elm specific patterns.
---

# Convert Haskell to Elm

Convert Haskell code to idiomatic Elm. This skill extends `meta-convert-dev` with Haskell-to-Elm specific type mappings, idiom translations, and The Elm Architecture integration.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Haskell types → Elm types
- **Idiom translations**: Haskell patterns → Elm idioms
- **TEA integration**: Pure functions → Model-View-Update pattern
- **Effect handling**: IO/State monads → Cmd/Sub in Elm
- **JSON handling**: Aeson patterns → Elm decoders/encoders

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Haskell language fundamentals - see `lang-haskell-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Reverse conversion (Elm → Haskell) - see `convert-elm-haskell`
- Advanced Haskell features (GADTs, Type Families) - no Elm equivalent
- Backend-specific Haskell code - focus on pure logic convertible to frontend

---

## Quick Reference

| Haskell | Elm | Notes |
|---------|-----|-------|
| `String` | `String` | Direct mapping |
| `Int` | `Int` | Direct mapping |
| `Float` / `Double` | `Float` | Elm has single float type |
| `Bool` | `Bool` | Direct mapping |
| `[a]` | `List a` | Direct mapping |
| `(a, b)` | `(a, b)` | Tuples identical |
| `Maybe a` | `Maybe a` | Direct mapping |
| `Either a b` | `Result a b` | Similar but swapped order |
| `data X = A \| B` | `type X = A \| B` | Union types |
| `newtype X = X a` | `type X = X a` | Custom types |
| `type X = Y` | `type alias X = Y` | Type aliases |
| `IO a` | `Cmd msg` | Effects via TEA |
| `map` | `List.map` | Core library |
| `fmap` / `<$>` | `Maybe.map` | Per-type functions |
| `>>=` | `Maybe.andThen` | Per-type, no do-notation |

## When Converting Code

1. **Identify pure logic** - Elm can only run in browser (frontend focus)
2. **Map types first** - Haskell and Elm types are very similar
3. **Convert IO/State to TEA** - Effects become Cmd, state becomes Model
4. **Preserve semantics** - Both are pure functional languages
5. **Simplify advanced features** - Elm deliberately limits language complexity
6. **Test equivalence** - Property-based tests translate well

---

## Type System Mapping

### Primitive Types

| Haskell | Elm | Notes |
|---------|-----|-------|
| `Int` | `Int` | Direct mapping |
| `Integer` | - | Arbitrary precision not in Elm; use Int |
| `Float` | `Float` | Single float type in Elm |
| `Double` | `Float` | Map to Elm's Float |
| `Char` | `Char` | Direct mapping |
| `String` | `String` | Both are lists of Char conceptually |
| `Bool` | `Bool` | Direct mapping |
| `()` | `()` | Unit type identical |

### Collection Types

| Haskell | Elm | Notes |
|---------|-----|-------|
| `[a]` | `List a` | Direct mapping |
| `(a, b)` | `(a, b)` | Tuples up to 3 elements |
| `(a, b, c)` | `(a, b, c)` | Maximum 3-tuple in Elm |
| `Data.Map k v` | `Dict k v` | Dict in Elm requires comparable k |
| `Data.Set a` | `Set a` | Set in Elm requires comparable a |
| `Data.Array a` | `Array a` | Similar, but Elm's is more limited |
| `Data.Text` | `String` | Elm String is the standard |

### Composite Types

| Haskell | Elm | Notes |
|---------|-----|-------|
| `data X = A \| B` | `type X = A \| B` | Union types (custom types in Elm) |
| `data X = X Int String` | `type X = X Int String` | Constructor with data |
| `newtype X = X Int` | `type X = X Int` | Single-constructor type |
| `type X = Int` | `type alias X = Int` | Type alias |
| `data X = X { f :: Int }` | `type alias X = { f : Int }` | Records use type alias in Elm |
| Type class | - | No type classes in Elm |

### Maybe and Result

| Haskell | Elm | Notes |
|---------|-----|-------|
| `Maybe a` | `Maybe a` | Identical |
| `Just x` | `Just x` | Identical |
| `Nothing` | `Nothing` | Identical |
| `Either a b` | `Result a b` | **Order swapped**: Either err ok → Result err ok |
| `Left err` | `Err err` | Error case |
| `Right ok` | `Ok ok` | Success case |

### Function Types

| Haskell | Elm | Notes |
|---------|-----|-------|
| `a -> b` | `a -> b` | Function type identical |
| `a -> b -> c` | `a -> b -> c` | Currying identical |
| `(a -> b) -> c` | `(a -> b) -> c` | Higher-order functions |
| Type class constraints | - | No constraints in Elm |

---

## Idiom Translation

### Pattern 1: Maybe Handling

**Haskell:**
```haskell
findUser :: Int -> Maybe User
findUser id = lookup id users

displayName :: Maybe User -> String
displayName maybeUser = case maybeUser of
    Just user -> name user
    Nothing -> "Anonymous"

-- Using fmap
getName :: Maybe User -> Maybe String
getName = fmap name

-- Using bind
getUserEmail :: Int -> Maybe String
getUserEmail userId = do
    user <- findUser userId
    return (email user)
```

**Elm:**
```elm
findUser : Int -> Maybe User
findUser id =
    Dict.get id users

displayName : Maybe User -> String
displayName maybeUser =
    case maybeUser of
        Just user ->
            user.name

        Nothing ->
            "Anonymous"

-- Using Maybe.map (equivalent to fmap)
getName : Maybe User -> Maybe String
getName =
    Maybe.map .name

-- Using Maybe.andThen (equivalent to >>=)
getUserEmail : Int -> Maybe String
getUserEmail userId =
    findUser userId
        |> Maybe.map .email
```

**Why this translation:**
- Both languages have identical Maybe type
- Elm uses pipeline operator `|>` instead of do-notation
- Record access uses `.field` syntax in Elm
- No do-notation in Elm; use `Maybe.andThen` for chaining

### Pattern 2: List Operations

**Haskell:**
```haskell
-- List comprehension
evens :: [Int]
evens = [x | x <- [1..10], even x]

-- Map, filter, fold
processNumbers :: [Int] -> Int
processNumbers nums = foldr (+) 0 $ map (*2) $ filter (>0) nums

-- Pattern matching on lists
listLength :: [a] -> Int
listLength [] = 0
listLength (_:xs) = 1 + listLength xs

-- List functions
result = take 5 [1..10]
result = drop 3 [1..10]
result = head [1,2,3]
result = tail [1,2,3]
```

**Elm:**
```elm
-- No list comprehension; use functions
evens : List Int
evens =
    List.range 1 10
        |> List.filter (\x -> modBy 2 x == 0)

-- Map, filter, fold (same pattern)
processNumbers : List Int -> Int
processNumbers nums =
    nums
        |> List.filter (\x -> x > 0)
        |> List.map (\x -> x * 2)
        |> List.foldl (+) 0

-- Pattern matching on lists (identical)
listLength : List a -> Int
listLength list =
    case list of
        [] ->
            0

        _ :: xs ->
            1 + listLength xs

-- List functions (similar)
result = List.take 5 (List.range 1 10)
result = List.drop 3 (List.range 1 10)
result = List.head [1, 2, 3]  -- Returns Maybe a
result = List.tail [1, 2, 3]  -- Returns Maybe (List a)
```

**Why this translation:**
- No list comprehensions in Elm; use filter/map
- Pipeline operator `|>` for readability
- `head` and `tail` return Maybe in Elm (safer)
- Pattern matching on lists is identical
- Elm uses `modBy` instead of `mod`

### Pattern 3: Custom Types (ADTs)

**Haskell:**
```haskell
-- Simple sum type
data Shape = Circle Float
           | Rectangle Float Float
           | Triangle Float Float Float

area :: Shape -> Float
area (Circle r) = pi * r^2
area (Rectangle w h) = w * h
area (Triangle a b c) =
    let s = (a + b + c) / 2
    in sqrt (s * (s-a) * (s-b) * (s-c))

-- Type with records
data Person = Person
    { firstName :: String
    , lastName :: String
    , age :: Int
    } deriving (Show, Eq)

fullName :: Person -> String
fullName person = firstName person ++ " " ++ lastName person
```

**Elm:**
```elm
-- Simple union type
type Shape
    = Circle Float
    | Rectangle Float Float
    | Triangle Float Float Float

area : Shape -> Float
area shape =
    case shape of
        Circle r ->
            pi * r ^ 2

        Rectangle w h ->
            w * h

        Triangle a b c ->
            let
                s =
                    (a + b + c) / 2
            in
            sqrt (s * (s - a) * (s - b) * (s - c))

-- Type with records (use type alias)
type alias Person =
    { firstName : String
    , lastName : String
    , age : Int
    }

fullName : Person -> String
fullName person =
    person.firstName ++ " " ++ person.lastName
```

**Why this translation:**
- Haskell `data` becomes Elm `type` for union types
- Haskell records become Elm `type alias` with record
- No automatic deriving in Elm
- Pattern matching is nearly identical
- Record field access uses dot notation in Elm

### Pattern 4: Recursive Functions

**Haskell:**
```haskell
-- Factorial
factorial :: Int -> Int
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- Fibonacci
fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = fib (n-1) + fib (n-2)

-- Map implementation
map' :: (a -> b) -> [a] -> [b]
map' _ [] = []
map' f (x:xs) = f x : map' f xs

-- Fold implementation
foldr' :: (a -> b -> b) -> b -> [a] -> b
foldr' _ acc [] = acc
foldr' f acc (x:xs) = f x (foldr' f acc xs)
```

**Elm:**
```elm
-- Factorial
factorial : Int -> Int
factorial n =
    case n of
        0 ->
            1

        _ ->
            n * factorial (n - 1)

-- Fibonacci
fib : Int -> Int
fib n =
    case n of
        0 ->
            0

        1 ->
            1

        _ ->
            fib (n - 1) + fib (n - 2)

-- Map implementation
map_ : (a -> b) -> List a -> List b
map_ f list =
    case list of
        [] ->
            []

        x :: xs ->
            f x :: map_ f xs

-- Fold implementation
foldr_ : (a -> b -> b) -> b -> List a -> b
foldr_ f acc list =
    case list of
        [] ->
            acc

        x :: xs ->
            f x (foldr_ f acc xs)
```

**Why this translation:**
- Elm doesn't support function pattern matching directly
- Use `case` expressions for pattern matching in Elm
- List cons operator `::` is identical
- Recursion patterns are the same

### Pattern 5: Higher-Order Functions

**Haskell:**
```haskell
-- Function composition
addThenDouble :: Int -> Int
addThenDouble = (*2) . (+1)

-- Partial application
add5 :: Int -> Int
add5 = (+5)

-- Map and filter composition
process :: [Int] -> [Int]
process = filter even . map (*2)

-- Lambda functions
square = \x -> x * x

-- Using $ to avoid parentheses
result = show $ sum $ map (*2) [1,2,3]
```

**Elm:**
```elm
-- Function composition
addThenDouble : Int -> Int
addThenDouble =
    (+) 1 >> (*) 2

-- Partial application
add5 : Int -> Int
add5 =
    (+) 5

-- Map and filter composition
process : List Int -> List Int
process =
    List.map ((*) 2) >> List.filter (\x -> modBy 2 x == 0)

-- Lambda functions (identical)
square =
    \x -> x * x

-- Using |> and <| instead of $
result =
    [1, 2, 3]
        |> List.map ((*) 2)
        |> List.sum
        |> String.fromInt
```

**Why this translation:**
- Elm uses `>>` for left-to-right composition (vs `.` in Haskell)
- Elm uses `<<` for right-to-left composition (like Haskell's `.`)
- Pipeline operator `|>` replaces many uses of `$`
- Operator sections work differently; `(+5)` becomes `(+) 5` in Elm

### Pattern 6: Type Aliases vs Newtypes

**Haskell:**
```haskell
-- Type alias
type UserId = Int
type Email = String

-- Newtype for type safety
newtype UserId = UserId Int deriving (Show, Eq)
newtype Email = Email String deriving (Show, Eq)

getUserById :: UserId -> Maybe User
getUserById (UserId id) = lookup id users

-- Can't mix UserId and Email
```

**Elm:**
```elm
-- Type alias (no type safety)
type alias UserId =
    Int

type alias Email =
    String

-- Custom type for type safety
type UserId
    = UserId Int

type Email
    = Email String

getUserById : UserId -> Maybe User
getUserById (UserId id) =
    Dict.get id users

-- Can't mix UserId and Email (type safety enforced)
```

**Why this translation:**
- Haskell `type` becomes Elm `type alias`
- Haskell `newtype` becomes Elm `type` (custom type)
- Both provide type safety at compile time
- Elm custom types have zero runtime cost (like newtype)

---

## Error Handling

### Haskell Either → Elm Result

**Haskell:**
```haskell
type Error = String

parseAge :: String -> Either Error Int
parseAge str = case reads str of
    [(n, "")] -> if n >= 0
                 then Right n
                 else Left "Age must be non-negative"
    _ -> Left "Not a valid number"

validateUser :: String -> String -> Either Error User
validateUser ageStr emailStr = do
    age <- parseAge ageStr
    email <- validateEmail emailStr
    return $ User email age

-- Using either
displayResult :: Either Error User -> String
displayResult = either ("Error: " ++) (show . userId)
```

**Elm:**
```elm
type alias Error =
    String

parseAge : String -> Result Error Int
parseAge str =
    case String.toInt str of
        Just n ->
            if n >= 0 then
                Ok n
            else
                Err "Age must be non-negative"

        Nothing ->
            Err "Not a valid number"

validateUser : String -> String -> Result Error User
validateUser ageStr emailStr =
    parseAge ageStr
        |> Result.andThen (\age ->
            validateEmail emailStr
                |> Result.map (\email ->
                    User email age
                )
        )

-- Using Result.withDefault or case
displayResult : Result Error User -> String
displayResult result =
    case result of
        Ok user ->
            String.fromInt user.userId

        Err error ->
            "Error: " ++ error
```

**Why this translation:**
- `Either a b` becomes `Result a b` (same order)
- `Left` becomes `Err`, `Right` becomes `Ok`
- No do-notation in Elm; use `Result.andThen` for chaining
- `Result.map` and `Result.andThen` replace fmap and >>=

---

## Effect Handling: IO/State → The Elm Architecture

### IO Actions → Cmd

**Haskell:**
```haskell
-- IO actions
main :: IO ()
main = do
    putStrLn "What is your name?"
    name <- getLine
    putStrLn $ "Hello, " ++ name

-- HTTP request (using simple-http)
fetchUser :: Int -> IO (Either Error User)
fetchUser userId = do
    response <- httpGet $ "/users/" ++ show userId
    return $ decodeUser response
```

**Elm:**
```elm
-- Commands in TEA
type Msg
    = NameEntered String
    | FetchUser Int
    | GotUser (Result Http.Error User)

-- No IO monad; effects via Cmd
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        NameEntered name ->
            ( { model | name = name }, Cmd.none )

        FetchUser userId ->
            ( model, fetchUser userId )

        GotUser result ->
            case result of
                Ok user ->
                    ( { model | user = Just user }, Cmd.none )

                Err error ->
                    ( { model | error = Just error }, Cmd.none )

-- HTTP request
fetchUser : Int -> Cmd Msg
fetchUser userId =
    Http.get
        { url = "/users/" ++ String.fromInt userId
        , expect = Http.expectJson GotUser userDecoder
        }
```

**Why this translation:**
- Haskell IO becomes Elm Cmd
- No imperative sequencing in Elm
- Effects handled by The Elm Architecture runtime
- State updates and commands returned together as tuple

### State Monad → Model

**Haskell:**
```haskell
import Control.Monad.State

type Counter a = State Int a

increment :: Counter ()
increment = modify (+1)

getCount :: Counter Int
getCount = get

computation :: Counter Int
computation = do
    increment
    increment
    count <- getCount
    return count

-- Run state
result = runState computation 0  -- (2, 2)
```

**Elm:**
```elm
-- No State monad; use Model in TEA
type alias Model =
    { count : Int
    }

type Msg
    = Increment
    | GetCount

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment ->
            ( { model | count = model.count + 1 }, Cmd.none )

        GetCount ->
            -- In Elm, view always has access to model
            -- No need for separate "get" operation
            ( model, Cmd.none )

-- Model updates are explicit in update function
-- No hidden state threading
```

**Why this translation:**
- State monad patterns become Model updates
- Explicit state passing via Model in update function
- No monad; state is first-class in TEA
- All state changes visible in update

---

## JSON Handling

### Aeson → Elm Decoders

**Haskell:**
```haskell
{-# LANGUAGE DeriveGeneric #-}

import Data.Aeson
import GHC.Generics

data User = User
    { name :: String
    , email :: String
    , age :: Int
    } deriving (Generic, Show)

instance FromJSON User
instance ToJSON User

-- Decode JSON
decodeUser :: ByteString -> Either String User
decodeUser = eitherDecode

-- Encode JSON
encodeUser :: User -> ByteString
encodeUser = encode
```

**Elm:**
```elm
import Json.Decode as Decode exposing (Decoder)
import Json.Encode as Encode

type alias User =
    { name : String
    , email : String
    , age : Int
    }

-- Decoder (explicit, no deriving)
userDecoder : Decoder User
userDecoder =
    Decode.map3 User
        (Decode.field "name" Decode.string)
        (Decode.field "email" Decode.string)
        (Decode.field "age" Decode.int)

-- Encoder (explicit)
encodeUser : User -> Encode.Value
encodeUser user =
    Encode.object
        [ ( "name", Encode.string user.name )
        , ( "email", Encode.string user.email )
        , ( "age", Encode.int user.age )
        ]

-- Decode JSON string
decodeUser : String -> Result Decode.Error User
decodeUser jsonString =
    Decode.decodeString userDecoder jsonString
```

**Why this translation:**
- No automatic deriving in Elm
- Decoders are explicit and composable
- Elm decoders fail at first error (like Aeson)
- Encoders are straightforward value constructors

---

## Concurrency Patterns

### Haskell Async → Elm Cmd.batch

**Haskell:**
```haskell
import Control.Concurrent.Async

-- Run multiple IO actions concurrently
fetchMultiple :: IO (User, Orders)
fetchMultiple = do
    (user, orders) <- concurrently fetchUser fetchOrders
    return (user, orders)

-- With mapConcurrently
fetchAllUsers :: [UserId] -> IO [User]
fetchAllUsers = mapConcurrently fetchUser
```

**Elm:**
```elm
-- Commands execute concurrently (managed by runtime)
type Msg
    = GotUser (Result Http.Error User)
    | GotOrders (Result Http.Error (List Order))

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        StartFetching ->
            ( { model | loading = True }
            , Cmd.batch
                [ Http.get { url = "/user", expect = Http.expectJson GotUser userDecoder }
                , Http.get { url = "/orders", expect = Http.expectJson GotOrders ordersDecoder }
                ]
            )

        GotUser result ->
            -- Handle user result
            ( handleUserResult result model, Cmd.none )

        GotOrders result ->
            -- Handle orders result
            ( handleOrdersResult result model, Cmd.none )

-- Multiple requests
fetchAllUsers : List Int -> Cmd Msg
fetchAllUsers userIds =
    userIds
        |> List.map (\id -> Http.get { url = "/users/" ++ String.fromInt id, ... })
        |> Cmd.batch
```

**Why this translation:**
- `Cmd.batch` sends multiple commands
- Elm runtime manages concurrency
- Each response handled independently via Msg
- No explicit async/await or threads

---

## Common Pitfalls

### 1. No Type Classes

**Problem:** Trying to use type class polymorphism

```haskell
-- Haskell: type classes
show :: Show a => a -> String
(==) :: Eq a => a -> a -> Bool
```

**Solution:** Use concrete types or phantom types

```elm
-- Elm: No type classes, use concrete functions
String.fromInt : Int -> String
String.fromFloat : Float -> String

-- Equality works only on comparable types
(==) : comparable -> comparable -> Bool

-- For custom types, write explicit functions
showUser : User -> String
showUser user =
    user.name ++ " (" ++ String.fromInt user.age ++ ")"
```

### 2. No Do-Notation

**Problem:** Trying to use do-notation

```haskell
-- Haskell
getUserEmail :: Int -> Maybe String
getUserEmail userId = do
    user <- findUser userId
    return (email user)
```

**Solution:** Use `andThen` and pipelines

```elm
-- Elm
getUserEmail : Int -> Maybe String
getUserEmail userId =
    findUser userId
        |> Maybe.map .email

-- For complex chains
validateAndCreate : Form -> Result Error User
validateAndCreate form =
    validateEmail form.email
        |> Result.andThen (\email ->
            validateAge form.ageStr
                |> Result.map (\age ->
                    User email age
                )
        )
```

### 3. No Lazy Evaluation by Default

**Problem:** Assuming infinite lists

```haskell
-- Haskell: infinite lists work
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)
take 10 fibs  -- [0,1,1,2,3,5,8,13,21,34]
```

**Solution:** Generate finite lists

```elm
-- Elm: Must be finite
fibs : Int -> List Int
fibs n =
    fibsHelper n [0, 1]

fibsHelper : Int -> List Int -> List Int
fibsHelper remaining acc =
    if remaining <= 0 then
        List.reverse acc
    else
        case acc of
            x :: y :: _ ->
                fibsHelper (remaining - 1) (x + y :: acc)

            _ ->
                acc

-- Or use recursion with explicit limit
take10Fibs = fibs 10
```

### 4. Different Operator Precedence

**Problem:** Assuming Haskell operator behavior

```haskell
-- Haskell
result = f $ g $ h x  -- Right associative
composed = f . g . h  -- Function composition
```

**Solution:** Use Elm operators correctly

```elm
-- Elm
result =
    x
        |> h
        |> g
        |> f

-- Or use <|
result = f <| g <| h x

-- Function composition
composed = f << g << h  -- Right-to-left (like Haskell .)
composed = h >> g >> f  -- Left-to-right (more intuitive)
```

### 5. No Arbitrary Type Constructors in Type Aliases

**Problem:** Using higher-kinded types

```haskell
-- Haskell
type Container f a = f a
```

**Solution:** Use concrete types

```elm
-- Elm: No higher-kinded types
type alias MaybeContainer a =
    Maybe a

type alias ListContainer a =
    List a

-- Can't abstract over the container type
```

---

## Tooling

| Task | Haskell | Elm | Notes |
|------|---------|-----|-------|
| Build | `cabal build` / `stack build` | `elm make` | Elm is simpler |
| REPL | `ghci` | `elm repl` | Similar experience |
| Format | `brittany` / `ormolu` | `elm-format` | Elm format is standard |
| Test | `hspec` / `QuickCheck` | `elm-test` | Property tests in both |
| Lint | `hlint` | `elm-review` | Elm-review is powerful |
| Docs | Haddock | `elm-doc-preview` | Elm docs are interactive |

---

## Examples

### Example 1: Simple - Maybe and Pattern Matching

**Before (Haskell):**
```haskell
data User = User { name :: String, age :: Int }

findUser :: Int -> Maybe User
findUser 1 = Just (User "Alice" 30)
findUser _ = Nothing

greetUser :: Int -> String
greetUser userId = case findUser userId of
    Just user -> "Hello, " ++ name user
    Nothing -> "User not found"
```

**After (Elm):**
```elm
type alias User =
    { name : String
    , age : Int
    }

findUser : Int -> Maybe User
findUser userId =
    if userId == 1 then
        Just { name = "Alice", age = 30 }
    else
        Nothing

greetUser : Int -> String
greetUser userId =
    case findUser userId of
        Just user ->
            "Hello, " ++ user.name

        Nothing ->
            "User not found"
```

### Example 2: Medium - List Processing and Result

**Before (Haskell):**
```haskell
validateAge :: Int -> Either String Int
validateAge age
    | age < 0 = Left "Age cannot be negative"
    | age > 150 = Left "Age too high"
    | otherwise = Right age

processAges :: [Int] -> Either String [Int]
processAges ages = mapM validateAge $ filter (> 0) ages

computeTotal :: Either String [Int] -> Int
computeTotal result = case result of
    Right ages -> sum ages
    Left _ -> 0
```

**After (Elm):**
```elm
validateAge : Int -> Result String Int
validateAge age =
    if age < 0 then
        Err "Age cannot be negative"
    else if age > 150 then
        Err "Age too high"
    else
        Ok age

processAges : List Int -> Result String (List Int)
processAges ages =
    ages
        |> List.filter (\a -> a > 0)
        |> List.map validateAge
        |> combineResults

combineResults : List (Result e a) -> Result e (List a)
combineResults results =
    List.foldr (Result.map2 (::)) (Ok []) results

computeTotal : Result String (List Int) -> Int
computeTotal result =
    case result of
        Ok ages ->
            List.sum ages

        Err _ ->
            0
```

### Example 3: Complex - The Elm Architecture Integration

**Before (Haskell - Pure Logic):**
```haskell
data TodoItem = TodoItem
    { itemId :: Int
    , text :: String
    , completed :: Bool
    }

data TodoList = TodoList
    { items :: [TodoItem]
    , nextId :: Int
    }

addTodo :: String -> TodoList -> TodoList
addTodo text list = TodoList
    { items = newItem : items list
    , nextId = nextId list + 1
    }
  where
    newItem = TodoItem (nextId list) text False

toggleTodo :: Int -> TodoList -> TodoList
toggleTodo targetId list = list
    { items = map toggleIfMatch (items list) }
  where
    toggleIfMatch item =
        if itemId item == targetId
        then item { completed = not (completed item) }
        else item

filterTodos :: (TodoItem -> Bool) -> TodoList -> [TodoItem]
filterTodos predicate = filter predicate . items
```

**After (Elm - Full TEA Application):**
```elm
-- MODEL

type alias TodoItem =
    { itemId : Int
    , text : String
    , completed : Bool
    }

type alias Model =
    { items : List TodoItem
    , nextId : Int
    , inputText : String
    , filter : Filter
    }

type Filter
    = All
    | Active
    | Completed

init : Model
init =
    { items = []
    , nextId = 1
    , inputText = ""
    , filter = All
    }

-- UPDATE

type Msg
    = UpdateInput String
    | AddTodo
    | ToggleTodo Int
    | SetFilter Filter

update : Msg -> Model -> Model
update msg model =
    case msg of
        UpdateInput text ->
            { model | inputText = text }

        AddTodo ->
            if String.isEmpty model.inputText then
                model
            else
                { model
                    | items =
                        { itemId = model.nextId
                        , text = model.inputText
                        , completed = False
                        }
                            :: model.items
                    , nextId = model.nextId + 1
                    , inputText = ""
                }

        ToggleTodo targetId ->
            { model
                | items =
                    List.map
                        (\item ->
                            if item.itemId == targetId then
                                { item | completed = not item.completed }
                            else
                                item
                        )
                        model.items
            }

        SetFilter filter ->
            { model | filter = filter }

-- VIEW

view : Model -> Html Msg
view model =
    div []
        [ input
            [ placeholder "What needs to be done?"
            , value model.inputText
            , onInput UpdateInput
            ]
            []
        , button [ onClick AddTodo ] [ text "Add" ]
        , div []
            [ button [ onClick (SetFilter All) ] [ text "All" ]
            , button [ onClick (SetFilter Active) ] [ text "Active" ]
            , button [ onClick (SetFilter Completed) ] [ text "Completed" ]
            ]
        , ul [] (List.map viewTodoItem (filteredItems model))
        ]

filteredItems : Model -> List TodoItem
filteredItems model =
    case model.filter of
        All ->
            model.items

        Active ->
            List.filter (\item -> not item.completed) model.items

        Completed ->
            List.filter .completed model.items

viewTodoItem : TodoItem -> Html Msg
viewTodoItem item =
    li
        [ onClick (ToggleTodo item.itemId)
        , style "text-decoration"
            (if item.completed then
                "line-through"
             else
                "none"
            )
        ]
        [ text item.text ]
```

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `lang-haskell-dev` - Haskell development patterns
- `lang-elm-dev` - Elm development patterns and The Elm Architecture
- `patterns-concurrency-dev` - Compare IO/STM to Elm's Cmd/Sub
- `patterns-serialization-dev` - JSON handling across languages
