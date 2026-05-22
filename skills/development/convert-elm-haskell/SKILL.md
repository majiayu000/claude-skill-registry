---
name: convert-elm-haskell
description: Convert Elm code to idiomatic Haskell. Use when migrating Elm frontend code to Haskell, translating Elm patterns to idiomatic Haskell, or refactoring Elm codebases. Extends meta-convert-dev with Elm-to-Haskell specific patterns.
---

# Convert Elm to Haskell

Convert Elm code to idiomatic Haskell. This skill extends `meta-convert-dev` with Elm-to-Haskell specific type mappings, idiom translations, and tooling for migrating functional frontend code to backend or library code.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Elm types → Haskell types
- **Idiom translations**: The Elm Architecture (TEA) → Haskell patterns
- **Error handling**: Elm Maybe/Result → Haskell Maybe/Either
- **Async patterns**: Elm Cmd/Sub → Haskell IO/concurrency
- **JSON handling**: Elm decoders/encoders → Aeson

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Haskell language fundamentals - see `lang-haskell-dev`
- Reverse conversion (Haskell → Elm) - see `convert-haskell-elm`
- Frontend frameworks - Elm's TEA is frontend-specific; backend alternatives vary

---

## Quick Reference

| Elm | Haskell | Notes |
|-----|---------|-------|
| `String` | `String` or `Text` | Use Text for production |
| `Int` | `Int` or `Integer` | Integer for unbounded |
| `Float` | `Double` | Default floating point |
| `Bool` | `Bool` | Direct mapping |
| `List a` | `[a]` | Direct mapping |
| `Maybe a` | `Maybe a` | Same type! |
| `Result err ok` | `Either err ok` | Swap order: Either Left Right |
| `type alias` | `type` or `data` with record | Similar syntax |
| `type` (union) | `data` | Same concept, similar syntax |
| `Cmd msg` | `IO ()` | Side effects |
| `Sub msg` | Event sources | Streams, STM, async |
| `Html msg` | No direct equivalent | Frontend-specific |
| `Json.Decode.Decoder a` | `FromJSON a` | Aeson instance |
| `Json.Encode.Value` | `ToJSON a` | Aeson instance |

## When Converting Code

1. **Analyze source thoroughly** before writing target
2. **Map types first** - Elm and Haskell are very similar
3. **Preserve semantics** over syntax similarity
4. **Adapt TEA patterns** - No direct equivalent; rethink architecture
5. **Handle Cmd/Sub** - Map to IO, concurrency, or events
6. **Test equivalence** - Same inputs → same outputs for pure logic

---

## Type System Mapping

### Primitive Types

| Elm | Haskell | Notes |
|-----|---------|-------|
| `String` | `String` | List of Char (inefficient) |
| `String` | `Text` | **Preferred** for production (from `Data.Text`) |
| `Int` | `Int` | Bounded integer (architecture-dependent) |
| `Int` | `Integer` | Unbounded (arbitrary precision) |
| `Float` | `Float` | Single precision |
| `Float` | `Double` | **Preferred** double precision |
| `Bool` | `Bool` | Direct mapping |
| `()` | `()` | Unit type |
| `Never` | - | No direct equivalent; use polymorphic types |

### Collection Types

| Elm | Haskell | Notes |
|-----|---------|-------|
| `List a` | `[a]` | Identical linked list |
| `Array a` | `Vector a` | Use `Data.Vector` for efficient arrays |
| `Set a` | `Set a` | Use `Data.Set` |
| `Dict k v` | `Map k v` | Use `Data.Map` |
| `( a, b )` | `(a, b)` | Tuple - identical |
| `( a, b, c )` | `(a, b, c)` | Tuples up to any size |

### Composite Types

| Elm | Haskell | Notes |
|-----|---------|-------|
| `type alias User = { name : String }` | `data User = User { name :: String }` | Record syntax |
| `type Msg = Click \| Input String` | `data Msg = Click \| Input String` | Union type / sum type |
| `Maybe a` | `Maybe a` | **Identical** |
| `Result err ok` | `Either err ok` | Same concept, **different order** (Left = error, Right = success) |

### Type Aliases vs Data

**Elm:**
```elm
-- Type alias: Just a synonym
type alias Point = { x : Float, y : Float }

-- Custom type: New type with constructors
type Shape = Circle Float | Rectangle Float Float
```

**Haskell:**
```haskell
-- Type synonym: Just an alias (no constructor)
type Point = (Double, Double)

-- Or with record syntax (creates constructor and accessors)
data Point = Point { x :: Double, y :: Double }

-- Custom type: Algebraic data type
data Shape = Circle Double | Rectangle Double Double
```

**Why this translation:**
- Elm's `type alias` for records creates a constructor; Haskell `type` does not
- Use Haskell `data` with record syntax for Elm record type aliases
- Union types map directly to Haskell algebraic data types

---

## Idiom Translation

### Pattern 1: Maybe Handling

**Elm:**
```elm
findUser : Int -> Maybe User
findUser id =
    List.head (List.filter (\u -> u.id == id) users)

displayName : Maybe User -> String
displayName maybeUser =
    case maybeUser of
        Just user ->
            user.name
        Nothing ->
            "Anonymous"

-- With pipeline
name =
    findUser 1
        |> Maybe.map .name
        |> Maybe.withDefault "Anonymous"
```

**Haskell:**
```haskell
import Data.Maybe (fromMaybe, maybe, listToMaybe)
import Data.List (find)

findUser :: Int -> Maybe User
findUser userId = find (\u -> userId == id u) users

displayName :: Maybe User -> String
displayName maybeUser =
    case maybeUser of
        Just user -> name user
        Nothing -> "Anonymous"

-- With applicative/functor
userName :: Maybe String
userName = name <$> findUser 1

userName' :: String
userName' = fromMaybe "Anonymous" (name <$> findUser 1)
```

**Why this translation:**
- Maybe is identical in both languages
- Elm's `Maybe.withDefault` = Haskell's `fromMaybe`
- Elm's `.field` accessor becomes Haskell function `field`
- Pattern matching syntax is nearly identical

### Pattern 2: Result/Either Error Handling

**Elm:**
```elm
type alias Error = String

parseAge : String -> Result Error Int
parseAge str =
    case String.toInt str of
        Just age ->
            if age >= 0 then
                Ok age
            else
                Err "Age must be non-negative"
        Nothing ->
            Err "Not a valid number"

validateUser : String -> String -> Result Error User
validateUser ageStr emailStr =
    Result.andThen
        (\age -> Result.map (User age) (validateEmail emailStr))
        (parseAge ageStr)
```

**Haskell:**
```haskell
import Text.Read (readMaybe)

type Error = String

parseAge :: String -> Either Error Int
parseAge str =
    case readMaybe str of
        Just age ->
            if age >= 0
                then Right age
                else Left "Age must be non-negative"
        Nothing ->
            Left "Not a valid number"

validateUser :: String -> String -> Either Error User
validateUser ageStr emailStr = do
    age <- parseAge ageStr
    email <- validateEmail emailStr
    return $ User age email

-- Or with Applicative
validateUser' :: String -> String -> Either Error User
validateUser' ageStr emailStr =
    User <$> parseAge ageStr <*> validateEmail emailStr
```

**Why this translation:**
- `Result err ok` maps to `Either err ok` (note: Left = error, Right = success)
- Elm's `Result.andThen` = Haskell's `>>=` (monadic bind)
- Haskell's do-notation is more concise for chaining
- Both support applicative style for independent validations

### Pattern 3: List Operations

**Elm:**
```elm
processNumbers : List Int -> Int
processNumbers numbers =
    numbers
        |> List.filter (\x -> x > 0)
        |> List.map (\x -> x * 2)
        |> List.foldl (+) 0

-- List comprehension (rare in Elm)
squares : List Int
squares =
    List.map (\x -> x * x) (List.range 1 10)
```

**Haskell:**
```haskell
processNumbers :: [Int] -> Int
processNumbers numbers =
    foldl (+) 0 $
        map (*2) $
            filter (>0) numbers

-- Or with function composition
processNumbers' :: [Int] -> Int
processNumbers' = foldl (+) 0 . map (*2) . filter (>0)

-- Or with pipeline using & (from Data.Function)
import Data.Function ((&))

processNumbers'' :: [Int] -> Int
processNumbers'' numbers =
    numbers
        & filter (>0)
        & map (*2)
        & foldl (+) 0

-- List comprehension (idiomatic in Haskell)
squares :: [Int]
squares = [x * x | x <- [1..10]]
```

**Why this translation:**
- List operations are nearly identical
- Elm's `|>` pipeline = Haskell's `&` (from Data.Function) or `$` (right-associative)
- Function composition (`.`) is more idiomatic in Haskell
- List comprehensions more common in Haskell than Elm

### Pattern 4: Pattern Matching and Case Expressions

**Elm:**
```elm
describeList : List a -> String
describeList list =
    case list of
        [] ->
            "empty"
        [ x ] ->
            "singleton"
        x :: xs ->
            "list with multiple elements"

-- Destructuring in function parameters
head : List a -> Maybe a
head list =
    case list of
        [] -> Nothing
        x :: _ -> Just x
```

**Haskell:**
```haskell
describeList :: [a] -> String
describeList list =
    case list of
        [] -> "empty"
        [x] -> "singleton"
        (x:xs) -> "list with multiple elements"

-- Pattern matching in function definition (more idiomatic)
describeList' :: [a] -> String
describeList' [] = "empty"
describeList' [x] = "singleton"
describeList' (x:xs) = "list with multiple elements"

-- Direct pattern matching for head
head' :: [a] -> Maybe a
head' [] = Nothing
head' (x:_) = Just x
```

**Why this translation:**
- Pattern matching is nearly identical
- Haskell allows pattern matching in function definitions (more concise)
- Syntax differences: `x :: xs` (Elm) vs `(x:xs)` (Haskell)
- Both support guards and nested patterns

### Pattern 5: Record Updates

**Elm:**
```elm
type alias User =
    { name : String
    , age : Int
    , email : String
    }

updateAge : Int -> User -> User
updateAge newAge user =
    { user | age = newAge }

updateMultiple : User -> User
updateMultiple user =
    { user | age = user.age + 1, name = "Updated" }
```

**Haskell:**
```haskell
data User = User
    { name :: String
    , age :: Int
    , email :: String
    } deriving (Show, Eq)

updateAge :: Int -> User -> User
updateAge newAge user = user { age = newAge }

updateMultiple :: User -> User
updateMultiple user = user
    { age = age user + 1
    , name = "Updated"
    }
```

**Why this translation:**
- Record update syntax is nearly identical
- Haskell requires parentheses for field access: `age user` vs Elm's `user.age`
- Both create new values (immutability)

### Pattern 6: Custom Types and Constructors

**Elm:**
```elm
type Msg
    = NoOp
    | Increment
    | Decrement
    | SetValue Int
    | SetName String

type RemoteData error value
    = NotAsked
    | Loading
    | Success value
    | Failure error
```

**Haskell:**
```haskell
data Msg
    = NoOp
    | Increment
    | Decrement
    | SetValue Int
    | SetName String
    deriving (Show, Eq)

data RemoteData error value
    = NotAsked
    | Loading
    | Success value
    | Failure error
    deriving (Show, Eq, Functor)
```

**Why this translation:**
- Syntax is identical
- Haskell allows deriving type classes (Show, Eq, Functor, etc.)
- Elm auto-derives equality; Haskell requires explicit `deriving Eq`

---

## The Elm Architecture → Haskell Patterns

### TEA Structure

**Elm's TEA:**
```elm
-- MODEL
type alias Model = { count : Int }

init : () -> ( Model, Cmd Msg )
init _ = ( { count = 0 }, Cmd.none )

-- UPDATE
type Msg = Increment | Decrement

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment -> ( { model | count = model.count + 1 }, Cmd.none )
        Decrement -> ( { model | count = model.count - 1 }, Cmd.none )

-- VIEW
view : Model -> Html Msg
view model =
    div []
        [ button [ onClick Decrement ] [ text "-" ]
        , div [] [ text (String.fromInt model.count) ]
        , button [ onClick Increment ] [ text "+" ]
        ]
```

**Haskell Equivalent (no direct frontend):**

For pure logic (testable):
```haskell
-- MODEL
data Model = Model { count :: Int } deriving (Show, Eq)

init :: Model
init = Model { count = 0 }

-- UPDATE
data Msg = Increment | Decrement deriving (Show, Eq)

update :: Msg -> Model -> Model
update msg model =
    case msg of
        Increment -> model { count = count model + 1 }
        Decrement -> model { count = count model - 1 }

-- No VIEW in backend context
-- For testing or CLI:
renderModel :: Model -> String
renderModel model = "Count: " ++ show (count model)
```

For interactive CLI:
```haskell
import Control.Monad (forever)
import System.IO (hFlush, stdout)

-- REPL-style interaction
mainLoop :: Model -> IO ()
mainLoop model = forever $ do
    putStrLn $ renderModel model
    putStrLn "Commands: + (increment), - (decrement), q (quit)"
    putStr "> "
    hFlush stdout
    input <- getLine
    case input of
        "+" -> mainLoop (update Increment model)
        "-" -> mainLoop (update Decrement model)
        "q" -> return ()
        _ -> mainLoop model

main :: IO ()
main = mainLoop init
```

**Why this adaptation:**
- Elm's Model/Update pattern translates to pure state machines in Haskell
- `Cmd` becomes `IO` for side effects
- Frontend view logic has no direct backend equivalent
- For web: use Servant, Scotty, or Yesod with separate architecture

### Cmd and Effects

**Elm:**
```elm
type Msg = GotUsers (Result Http.Error (List User))

getUsers : Cmd Msg
getUsers =
    Http.get
        { url = "https://api.example.com/users"
        , expect = Http.expectJson GotUsers (Json.Decode.list userDecoder)
        }

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUsers -> ( { model | loading = True }, getUsers )
        GotUsers result -> ...
```

**Haskell:**
```haskell
import Network.HTTP.Simple
import Data.Aeson (FromJSON, eitherDecode)

data Msg = GotUsers (Either String [User]) deriving (Show)

getUsers :: IO (Either String [User])
getUsers = do
    response <- httpLBS "https://api.example.com/users"
    return $ eitherDecode (getResponseBody response)

-- In a real app, you'd use async or STM for event handling
handleMsg :: Msg -> Model -> IO Model
handleMsg msg model =
    case msg of
        GotUsers (Right users) -> return $ model { users = users, loading = False }
        GotUsers (Left err) -> return $ model { error = Just err, loading = False }

-- Async version
import Control.Concurrent.Async

fetchUsersAsync :: (Msg -> IO ()) -> IO ()
fetchUsersAsync dispatch = do
    result <- getUsers
    dispatch (GotUsers result)
```

**Why this adaptation:**
- Elm's `Cmd` is a managed effect system; Haskell uses `IO` directly
- Elm runtime handles effect execution; Haskell requires explicit async/threading
- Consider using async, STM, or event libraries for complex state management

---

## JSON Handling

### JSON Decoders

**Elm:**
```elm
import Json.Decode as Decode exposing (Decoder)
import Json.Decode.Pipeline exposing (required, optional)

type alias User =
    { name : String
    , email : String
    , age : Int
    }

userDecoder : Decoder User
userDecoder =
    Decode.succeed User
        |> required "name" Decode.string
        |> required "email" Decode.string
        |> required "age" Decode.int
```

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

-- Automatic derivation (recommended)
instance FromJSON User
instance ToJSON User

-- Manual (for custom field names)
instance FromJSON User where
    parseJSON = withObject "User" $ \v -> User
        <$> v .: "name"
        <*> v .: "email"
        <*> v .: "age"
```

**Why this translation:**
- Elm requires explicit decoders; Haskell can auto-derive via `Generic`
- Elm's `Decode.Pipeline` ≈ Haskell's `Applicative` operators (`<$>`, `<*>`)
- Aeson is more concise for simple cases; Elm decoders are more explicit

### JSON Encoders

**Elm:**
```elm
import Json.Encode as Encode

encodeUser : User -> Encode.Value
encodeUser user =
    Encode.object
        [ ( "name", Encode.string user.name )
        , ( "email", Encode.string user.email )
        , ( "age", Encode.int user.age )
        ]
```

**Haskell:**
```haskell
import Data.Aeson

-- Automatic (if using Generic)
encodeUser :: User -> Value
encodeUser = toJSON

-- Manual
instance ToJSON User where
    toJSON (User n e a) = object
        [ "name" .= n
        , "email" .= e
        , "age" .= a
        ]
```

**Why this translation:**
- Both use object/record encoding
- Haskell's `.=` operator is more concise than Elm's tuple syntax
- Generics make simple cases trivial

---

## Concurrency Patterns

Elm uses `Cmd` and `Sub` for managed effects. Haskell requires explicit concurrency handling.

### Subscriptions → Event Streams

**Elm:**
```elm
subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch
        [ Time.every 1000 Tick
        , Browser.Events.onResize WindowResized
        ]
```

**Haskell (using async):**
```haskell
import Control.Concurrent (threadDelay, forkIO)
import Control.Concurrent.STM
import Control.Concurrent.Async

-- Event channel
type EventBus msg = TChan msg

-- Timer subscription
timerSub :: EventBus Msg -> IO ()
timerSub bus = forever $ do
    threadDelay 1000000  -- 1 second
    atomically $ writeTChan bus Tick

-- Main loop
mainWithSubs :: IO ()
mainWithSubs = do
    eventBus <- newTChanIO
    async $ timerSub eventBus

    forever $ do
        msg <- atomically $ readTChan eventBus
        -- handle msg
        return ()
```

**Why this adaptation:**
- Elm's subscriptions are declarative; Haskell requires imperative setup
- Use STM, async, or event libraries for similar patterns
- Consider libraries like `reactive-banana` for FRP-style event handling

---

## Common Pitfalls

### 1. Assuming Elm's Simplicity Limits Apply

**Problem:** Elm intentionally limits features (no type classes, no laziness control). Haskell has these features.

**Solution:**
- Use type classes for polymorphism (Eq, Show, Functor, etc.)
- Leverage lazy evaluation (but beware space leaks)
- Use advanced type system features when beneficial (GADTs, type families)

### 2. Direct Translation of TEA

**Problem:** The Elm Architecture is frontend-specific. Direct translation to Haskell backend makes no sense.

**Solution:**
- Extract pure business logic (Model + Update) - this translates directly
- Rethink effects: `Cmd` → IO, async, or STM
- For web backends: use Servant, Scotty, or Yesod patterns

### 3. Forgetting Field Accessor Syntax

**Problem:** Elm's `user.name` vs Haskell's `name user`.

**Elm:**
```elm
userName = user.name
```

**Haskell:**
```haskell
userName = name user  -- Function application
```

**Solution:** Remember Haskell record fields are functions.

### 4. Result vs Either Argument Order

**Problem:** `Result err ok` vs `Either err ok` - **same order**, but different conventions.

**Elm:**
```elm
type Result error value = Err error | Ok value
```

**Haskell:**
```haskell
data Either a b = Left a | Right b
-- By convention: Left = error, Right = success
```

**Solution:**
- Elm `Ok x` → Haskell `Right x`
- Elm `Err e` → Haskell `Left e`

### 5. Missing Text Import

**Problem:** Using `String` instead of `Text` in production code.

**Solution:**
```haskell
import Data.Text (Text)
import qualified Data.Text as T

-- Use Text for all string data
data User = User { name :: Text } deriving (Show)
```

---

## Tooling

### Transpilers & Converters

| Tool | Direction | Status | Notes |
|------|-----------|--------|-------|
| `haskelm` | Haskell → Elm | Experimental | Template Haskell based |
| `haskell-to-elm` | Haskell → Elm | Active | Type + JSON codec generation |
| `elm-bridge` | Haskell ↔ Elm | Active | Bidirectional type sync |
| `elm-street` | Haskell → Elm | Active | Aeson-compatible codegen |

**Note:** Most tools focus on **Haskell → Elm** for full-stack apps. Manual conversion recommended for Elm → Haskell.

### Type Synchronization Libraries

For full-stack apps (Haskell backend + Elm frontend), these maintain type safety:

```haskell
-- haskell-to-elm example
{-# LANGUAGE DeriveGeneric #-}
import GHC.Generics
import Language.Elm.Pretty (pretty)
import qualified Language.Haskell.To.Elm as Elm

data User = User { name :: Text, age :: Int }
    deriving (Generic, Elm.HasElmType, Elm.HasElmEncoder Aeson.Value, Elm.HasElmDecoder Aeson.Value)

-- Generates Elm type + JSON encoders/decoders
```

### Testing Strategy

```haskell
-- HSpec for behavior
import Test.Hspec

spec :: Spec
spec = describe "update function" $ do
    it "increments count" $ do
        let model = Model { count = 0 }
        let result = update Increment model
        count result `shouldBe` 1

-- QuickCheck for properties
import Test.QuickCheck

prop_updateIdempotent :: Msg -> Model -> Property
prop_updateIdempotent msg model =
    update msg (update msg model) === update msg model
```

---

## Examples

### Example 1: Simple - Type Definitions and Functions

**Before (Elm):**
```elm
type alias Point =
    { x : Float
    , y : Float
    }

distance : Point -> Point -> Float
distance p1 p2 =
    let
        dx = p1.x - p2.x
        dy = p1.y - p2.y
    in
    sqrt (dx * dx + dy * dy)

midpoint : Point -> Point -> Point
midpoint p1 p2 =
    { x = (p1.x + p2.x) / 2
    , y = (p1.y + p2.y) / 2
    }
```

**After (Haskell):**
```haskell
data Point = Point
    { x :: Double
    , y :: Double
    } deriving (Show, Eq)

distance :: Point -> Point -> Double
distance p1 p2 =
    let dx = x p1 - x p2
        dy = y p1 - y p2
    in sqrt (dx * dx + dy * dy)

midpoint :: Point -> Point -> Point
midpoint p1 p2 = Point
    { x = (x p1 + x p2) / 2
    , y = (y p1 + y p2) / 2
    }
```

### Example 2: Medium - JSON and Error Handling

**Before (Elm):**
```elm
import Json.Decode as D
import Json.Encode as E
import Http

type alias Config =
    { apiUrl : String
    , timeout : Maybe Int
    }

configDecoder : D.Decoder Config
configDecoder =
    D.map2 Config
        (D.field "apiUrl" D.string)
        (D.maybe (D.field "timeout" D.int))

encodeConfig : Config -> E.Value
encodeConfig config =
    E.object
        [ ( "apiUrl", E.string config.apiUrl )
        , ( "timeout", Maybe.withDefault E.null (Maybe.map E.int config.timeout) )
        ]

type alias ApiError = String

loadConfig : String -> (Result ApiError Config -> msg) -> Cmd msg
loadConfig url toMsg =
    Http.get
        { url = url
        , expect = Http.expectJson toMsg configDecoder
        }
```

**After (Haskell):**
```haskell
{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE OverloadedStrings #-}

import Data.Aeson
import GHC.Generics
import Network.HTTP.Simple
import Data.Text (Text)

data Config = Config
    { apiUrl :: Text
    , timeout :: Maybe Int
    } deriving (Generic, Show, Eq)

instance FromJSON Config
instance ToJSON Config where
    toJSON (Config url t) = object $
        [ "apiUrl" .= url ] ++
        maybe [] (\v -> ["timeout" .= v]) t

type ApiError = String

loadConfig :: String -> IO (Either ApiError Config)
loadConfig url = do
    response <- httpLBS (parseRequest_ url)
    return $ case eitherDecode (getResponseBody response) of
        Right config -> Right config
        Left err -> Left err
```

### Example 3: Complex - State Machine with Side Effects

**Before (Elm):**
```elm
type Model
    = LoggedOut
    | LoggingIn { username : String }
    | LoggedIn { user : User, token : String }
    | Error String

type Msg
    = StartLogin String
    | LoginSuccess User String
    | LoginFailure String
    | Logout

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        StartLogin username ->
            ( LoggingIn { username = username }
            , performLogin username
            )

        LoginSuccess user token ->
            ( LoggedIn { user = user, token = token }
            , Cmd.none
            )

        LoginFailure err ->
            ( Error err
            , Cmd.none
            )

        Logout ->
            case model of
                LoggedIn _ ->
                    ( LoggedOut, clearSession )

                _ ->
                    ( model, Cmd.none )

performLogin : String -> Cmd Msg
performLogin username =
    Http.post
        { url = "/api/login"
        , body = Http.jsonBody (E.object [ ( "username", E.string username ) ])
        , expect = Http.expectJson
            (\result ->
                case result of
                    Ok { user, token } -> LoginSuccess user token
                    Err _ -> LoginFailure "Login failed"
            )
            loginResponseDecoder
        }
```

**After (Haskell):**
```haskell
{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE OverloadedStrings #-}

import Data.Aeson
import GHC.Generics
import Network.HTTP.Simple
import Data.Text (Text)

data Model
    = LoggedOut
    | LoggingIn { username :: Text }
    | LoggedIn { user :: User, token :: Text }
    | Error String
    deriving (Show, Eq)

data Msg
    = StartLogin Text
    | LoginSuccess User Text
    | LoginFailure String
    | Logout
    deriving (Show, Eq)

-- Pure update (no IO)
update :: Msg -> Model -> Model
update msg model =
    case msg of
        StartLogin username ->
            LoggingIn { username = username }

        LoginSuccess usr tok ->
            LoggedIn { user = usr, token = tok }

        LoginFailure err ->
            Error err

        Logout ->
            case model of
                LoggedIn _ -> LoggedOut
                _ -> model

-- Effects handled separately
handleEffect :: Msg -> IO (Maybe Msg)
handleEffect (StartLogin username) = do
    result <- performLogin username
    return $ Just $ case result of
        Right (usr, tok) -> LoginSuccess usr tok
        Left err -> LoginFailure err
handleEffect Logout = do
    clearSession
    return Nothing
handleEffect _ = return Nothing

-- HTTP request
performLogin :: Text -> IO (Either String (User, Text))
performLogin username = do
    let requestBody = object ["username" .= username]
    response <- httpJSON $ setRequestBodyJSON requestBody $ parseRequest_ "/api/login"
    return $ case getResponseBody response of
        LoginResponse usr tok -> Right (usr, tok)
        _ -> Left "Login failed"

clearSession :: IO ()
clearSession = putStrLn "Session cleared"

-- Main loop
mainLoop :: Model -> IO ()
mainLoop model = do
    print model
    -- Get user input, dispatch msg, handle effects
    return ()
```

---

## Limitations

### Elm Features Not in Haskell

- **The Elm Architecture**: No direct equivalent; must design architecture per use case
- **Compiler guarantees**: Elm's "no runtime exceptions" doesn't apply (Haskell has partial functions)
- **Frontend-specific types**: `Html`, `Svg`, `Browser.Events` have no backend equivalents

### Haskell Features Not in Elm

- **Type classes**: Use for polymorphism (Elm uses explicit passing)
- **Lazy evaluation**: Can cause space leaks if not careful
- **Advanced types**: GADTs, type families, existentials
- **Partial functions**: `head`, `tail` can crash (use `Maybe` versions)

### Conversion Challenges

1. **TEA translation**: Requires rethinking application architecture
2. **Cmd/Sub**: No built-in runtime; must use async/STM/events
3. **Frontend UI**: No equivalent; backend conversion only makes sense for business logic
4. **JSON decoders**: More implicit in Haskell (Generics) vs explicit in Elm

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `lang-elm-dev` - Elm development patterns (TEA, JSON, types)
- `lang-haskell-dev` - Haskell development patterns (monads, type classes, concurrency)
- `convert-typescript-rust` - Similar pure functional language conversion

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Compare Elm's Cmd/Sub to Haskell's IO/STM/async
- `patterns-serialization-dev` - JSON decoders/encoders across languages
- `patterns-metaprogramming-dev` - Template Haskell vs Elm's limitations
