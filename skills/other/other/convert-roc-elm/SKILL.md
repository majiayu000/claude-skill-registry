---
name: convert-roc-elm
description: Convert Roc code to idiomatic Elm. Use when migrating Roc applications to Elm frontend code, translating platform-agnostic Roc to browser-based Elm, or refactoring Roc CLI tools to Elm web applications. Extends meta-convert-dev with Roc-to-Elm specific patterns.
---

# Convert Roc to Elm

Convert Roc code to idiomatic Elm. This skill extends `meta-convert-dev` with Roc-to-Elm specific type mappings, idiom translations, and architectural patterns for moving from platform-agnostic Roc to browser-based Elm applications.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Roc types → Elm types
- **Idiom translations**: Roc patterns → idiomatic Elm
- **Architecture patterns**: Platform model → The Elm Architecture (TEA)
- **Effect system**: Task → Cmd/Sub
- **Error handling**: Result types (similar but different conventions)
- **Platform shift**: General-purpose → Frontend-specific

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Reverse conversion (Elm → Roc) - see `convert-elm-roc`
- Backend-specific Roc code - Elm is frontend-only

---

## Quick Reference

| Roc | Elm | Notes |
|-----|-----|-------|
| `Str` | `String` | Direct mapping |
| `I64`, `U64` | `Int` | Elm has arbitrary precision integers |
| `F64` | `Float` | Direct mapping |
| `Bool` | `Bool` | Direct mapping with capitalization |
| `List a` | `List a` | Same syntax and operations |
| `{ field : Type }` | `{ field : Type }` | Records are nearly identical |
| `[Tag1, Tag2]` | `type Custom = Tag1 \| Tag2` | Tag unions → Custom types |
| `Result a e` | `Result e a` | **Reversed parameter order!** |
| `[Some a, None]` | `Maybe a` | Optional values |
| `Task a err` | `Cmd Msg` or `Task Never a` | Effect systems differ |
| `when x is` | `case x of` | Pattern matching syntax |
| `!` suffix operator | `Task.perform` | Bang operator → explicit Task handling |

---

## Architectural Paradigm Shift

### From Platform Model to The Elm Architecture

| Aspect | Roc Platform Model | Elm TEA |
|--------|-------------------|---------|
| **Target** | Any platform (CLI, web, native) | Browser frontend only |
| **Effects** | Platform-provided Task | Runtime-managed Cmd/Sub |
| **Entry point** | `main : Task {} []` | `main : Program () Model Msg` |
| **State** | Implicit in Task chain | Explicit Model |
| **Updates** | Task composition | update : Msg → Model → (Model, Cmd Msg) |
| **I/O** | Platform exposes (File, Http, etc.) | Browser.* modules only |

### Roc Platform Application

```roc
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/..."
}

import pf.Stdout
import pf.Task exposing [Task]

main : Task {} []
main =
    Stdout.line! "Hello, World!"
    name = Stdin.line!
    Stdout.line! "Hello, \(name)!"
```

### Elm Equivalent Using TEA

```elm
module Main exposing (main)

import Browser
import Html exposing (Html, div, input, text)
import Html.Events exposing (onInput)
import Html.Attributes exposing (placeholder, value)

-- MODEL
type alias Model =
    { name : String
    , greeting : String
    }

init : () -> ( Model, Cmd Msg )
init _ =
    ( { name = "", greeting = "Hello, World!" }, Cmd.none )

-- UPDATE
type Msg
    = NameChanged String

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        NameChanged newName ->
            ( { model
                | name = newName
                , greeting = "Hello, " ++ newName ++ "!"
              }
            , Cmd.none
            )

-- VIEW
view : Model -> Html Msg
view model =
    div []
        [ div [] [ text model.greeting ]
        , input
            [ placeholder "Enter your name"
            , value model.name
            , onInput NameChanged
            ]
            []
        ]

-- MAIN
main : Program () Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , view = view
        , subscriptions = \_ -> Sub.none
        }
```

**Key shift:** Roc's imperative Task chain becomes Elm's declarative Model-Update-View cycle.

---

## Type System Mapping

### Primitive Types

| Roc | Elm | Notes |
|-----|-----|-------|
| `Bool.true` / `Bool.false` | `True` / `False` | Capitalization differs |
| `42` | `42` | Integer literals (Elm has arbitrary precision) |
| `3.14` | `3.14` | Float literals |
| `"text"` | `"text"` | String literals (Roc uses Str, Elm uses String) |
| `I8, I16, I32, I64, I128` | `Int` | Elm has single Int type (arbitrary precision) |
| `U8, U16, U32, U64, U128` | `Int` | Same - map to Int |
| `F32, F64` | `Float` | Elm has single Float type |
| `Num a` | `number` | Flexible number type (inferred) |

### Collection Types

| Roc | Elm | Notes |
|-----|-----|-------|
| `List a` | `List a` | Identical syntax and semantics |
| `Dict k v` | `Dict k v` | Same interface, import from Dict module |
| `Set a` | `Set a` | Same interface, import from Set module |
| `(a, b)` | `( a, b )` | Tuples (Elm supports up to 3-tuples idiomatically) |

### Record Types

| Roc | Elm | Notes |
|-----|-----|-------|
| `{ name : Str, age : U32 }` | `{ name : String, age : Int }` | Nearly identical, just type name differences |
| `{ user & age: 31 }` | `{ user \| age = 31 }` | Record update syntax differs (&  vs \|) |
| `{ name, age } = user` | `{ name, age } = user` | Destructuring identical |
| `user.name` | `user.name` | Field access identical |

### Tag Unions to Custom Types

**Roc:**
```roc
# Structural tag union
Color : [Red, Green, Blue, Custom(U8, U8, U8)]

handleColor : Color -> Str
handleColor = \color ->
    when color is
        Red -> "red"
        Green -> "green"
        Blue -> "blue"
        Custom(r, g, b) -> "rgb(\(Num.toStr(r)), ...)"
```

**Elm:**
```elm
-- Named custom type (nominal)
type Color
    = Red
    | Green
    | Blue
    | Custom Int Int Int

handleColor : Color -> String
handleColor color =
    case color of
        Red ->
            "red"
        Green ->
            "green"
        Blue ->
            "blue"
        Custom r g b ->
            "rgb(" ++ String.fromInt r ++ ", ...)"
```

**Key differences:**
- Roc uses structural types (no declaration needed)
- Elm requires explicit `type` declaration
- Roc uses lowercase for type variables in tag payloads
- Elm uses type constructors with capital letters

### Optional Values

**Roc:**
```roc
# Inline tag union
email : [Some Str, None]
email = Some("alice@example.com")

# Pattern match
emailText = when email is
    Some(addr) -> addr
    None -> "no email"
```

**Elm:**
```elm
-- Built-in Maybe type
email : Maybe String
email = Just "alice@example.com"

-- Pattern match
emailText : String
emailText =
    case email of
        Just addr ->
            addr
        Nothing ->
            "no email"

-- Helper functions
emailOrDefault : String
emailOrDefault =
    Maybe.withDefault "no email" email
```

**Translation:**
- `[Some a, None]` → `Maybe a`
- `Some(value)` → `Just value`
- `None` → `Nothing`

### Result Type (Parameter Order Reversed!)

**Roc:**
```roc
# Result ok err
divide : I64, I64 -> Result I64 [DivByZero]
divide = \a, b ->
    if b == 0 then
        Err(DivByZero)
    else
        Ok(a // b)
```

**Elm:**
```elm
-- Result error ok (REVERSED!)
divide : Int -> Int -> Result String Int
divide a b =
    if b == 0 then
        Err "Division by zero"
    else
        Ok (a // b)
```

**CRITICAL:** Roc's `Result ok err` becomes Elm's `Result error ok` - parameters are reversed!

---

## Idiom Translation

### 1. Pattern Matching: when → case

**Roc:**
```roc
classify : I64 -> Str
classify = \n ->
    when n is
        0 -> "zero"
        x if x < 0 -> "negative"
        _ -> "positive"
```

**Elm:**
```elm
classify : Int -> String
classify n =
    case n of
        0 ->
            "zero"
        x ->
            if x < 0 then
                "negative"
            else
                "positive"
```

**Why this translation:**
- Roc's `when` becomes Elm's `case`
- Roc has guard clauses (`if` after pattern), Elm uses `if` expressions in branches
- Elm requires explicit `->` and indentation

### 2. List Processing

**Roc:**
```roc
doubled : List I64
doubled = List.map([1, 2, 3, 4, 5], \x -> x * 2)

# Pipeline style
result = [1, 2, 3, 4, 5]
    |> List.map(\x -> x * 2)
    |> List.keepIf(\x -> x > 5)
    |> List.walk(0, Num.add)
```

**Elm:**
```elm
doubled : List Int
doubled =
    List.map (\x -> x * 2) [ 1, 2, 3, 4, 5 ]

-- Pipeline style (same!)
result : Int
result =
    [ 1, 2, 3, 4, 5 ]
        |> List.map (\x -> x * 2)
        |> List.filter (\x -> x > 5)
        |> List.foldl (+) 0
```

**Why this translation:**
- `List.keepIf` → `List.filter` (different name)
- `List.walk` → `List.foldl` or `List.foldr` (different name)
- Pipeline operator `|>` is identical
- Elm uses function-first, args-last (currying)

### 3. Record Updates

**Roc:**
```roc
user = { name: "Alice", age: 30 }
olderUser = { user & age: 31 }

# Multiple fields
updatedUser = { user &
    age: 31,
    name: "Alice Smith"
}
```

**Elm:**
```elm
user =
    { name = "Alice", age = 30 }

olderUser =
    { user | age = 31 }

-- Multiple fields
updatedUser =
    { user
        | age = 31
        , name = "Alice Smith"
    }
```

**Why this translation:**
- Roc uses `&` for updates, Elm uses `|`
- Roc uses `:` for field assignment, Elm uses `=`
- Syntax is almost identical otherwise

### 4. Task-Based Effects → Cmd/Task

**Roc:**
```roc
main : Task {} []
main =
    content = File.readUtf8!("input.txt")
    processed = String.toUpper(content)
    File.writeUtf8!("output.txt", processed)
    Stdout.line!("Done!")
```

**Elm:**
```elm
-- Elm doesn't have file access (browser only)
-- This example shows HTTP instead

type Msg
    = GotData (Result Http.Error String)
    | DataProcessed

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchData ->
            ( { model | loading = True }
            , Http.get
                { url = "/api/data"
                , expect = Http.expectString GotData
                }
            )

        GotData result ->
            case result of
                Ok content ->
                    ( { model
                        | data = String.toUpper content
                        , loading = False
                      }
                    , Cmd.none
                    )

                Err _ ->
                    ( { model | error = Just "Failed to load" }
                    , Cmd.none
                    )
```

**Why this translation:**
- Roc's `!` suffix operator becomes explicit Cmd in Elm
- Roc chains Tasks sequentially; Elm uses Model updates
- File I/O doesn't exist in Elm (browser sandbox)
- Must model async operations as Msg and handle in update

### 5. Error Propagation

**Roc:**
```roc
calculate : I64, I64, I64 -> Result I64 [DivByZero]
calculate = \a, b, c ->
    x = divide!(a, b)  # Returns early on Err
    y = divide!(x, c)  # Returns early on Err
    Ok(y)
```

**Elm:**
```elm
calculate : Int -> Int -> Int -> Result String Int
calculate a b c =
    divide a b
        |> Result.andThen (\x -> divide x c)

-- Or with explicit pattern matching
calculateExplicit : Int -> Int -> Int -> Result String Int
calculateExplicit a b c =
    case divide a b of
        Err e ->
            Err e
        Ok x ->
            case divide x c of
                Err e ->
                    Err e
                Ok y ->
                    Ok y
```

**Why this translation:**
- Roc's `!` operator doesn't exist in Elm
- Use `Result.andThen` for chaining (monadic bind)
- Or use explicit `case` expressions

### 6. Opaque Types

**Roc:**
```roc
Age := U32

createAge : U32 -> Age
createAge = \n -> @Age(n)

getAge : Age -> U32
getAge = \@Age(n) -> n
```

**Elm:**
```elm
-- Elm uses module visibility for opacity
module Age exposing (Age, create, toInt)

type Age
    = Age Int

create : Int -> Maybe Age
create n =
    if n >= 0 && n < 150 then
        Just (Age n)
    else
        Nothing

toInt : Age -> Int
toInt (Age n) =
    n

-- Constructor Age is NOT exposed, only create function
```

**Why this translation:**
- Roc uses `@` unwrapping syntax, Elm uses pattern matching
- Elm achieves opacity through module exports (`Age` type exposed, constructor hidden)
- Elm typically adds validation in smart constructors

---

## Paradigm Translation: Platform Model → TEA

### Mental Model Shift

| Roc Concept | Elm Approach | Key Insight |
|-------------|--------------|-------------|
| Task chain (sequential) | Model-Update-View loop | Imperative → Declarative |
| Platform provides I/O | Browser provides events | CLI/Native → Browser |
| `main` returns Task | `main` returns Program | Effect → Pure |
| Tasks compose with `!` | Cmd issued, Msg received | Direct → Indirect |

### Concurrency Mental Model

| Roc Model | Elm Model | Conceptual Translation |
|-----------|-----------|------------------------|
| Platform handles Tasks | Runtime handles Cmd/Sub | Both managed by runtime |
| Sequential with `!` | Asynchronous with Msg | Chain → Event-driven |
| Task.ok/Task.err | Cmd.none / new Cmd | Return value → Side effect |

---

## Error Handling

### Roc Result → Elm Result

**Key Difference: Parameter order is reversed!**

```roc
-- Roc: Result ok err
parseAge : Str -> Result U32 [ParseError Str, NegativeAge]
parseAge = \str ->
    when Str.toU32(str) is
        Ok(age) if age >= 0 -> Ok(age)
        Ok(_) -> Err(NegativeAge)
        Err(_) -> Err(ParseError("Not a number"))
```

```elm
-- Elm: Result err ok (REVERSED!)
type ParseError
    = NotANumber
    | NegativeAge

parseAge : String -> Result ParseError Int
parseAge str =
    case String.toInt str of
        Just age ->
            if age >= 0 then
                Ok age
            else
                Err NegativeAge

        Nothing ->
            Err NotANumber
```

### Error Type Modeling

**Roc uses inline tag unions:**
```roc
fetchUser : U64 -> Task User [NetworkError, NotFound, Unauthorized]
```

**Elm uses named custom types:**
```elm
type FetchError
    = NetworkError Http.Error
    | NotFound
    | Unauthorized

fetchUser : Int -> Task FetchError User
```

---

## Effect System Translation

### Task in Roc vs Task/Cmd in Elm

**Roc Task:**
```roc
# Platform-provided, sequential execution
fetchAndProcess : Task Str []
fetchAndProcess =
    data = Http.get!("https://api.example.com/data")
    processed = String.toUpper(data)
    Task.ok(processed)
```

**Elm Cmd (most common):**
```elm
type Msg
    = GotData (Result Http.Error String)

fetchData : Cmd Msg
fetchData =
    Http.get
        { url = "https://api.example.com/data"
        , expect = Http.expectString GotData
        }

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchData ->
            ( model, fetchData )

        GotData result ->
            case result of
                Ok data ->
                    ( { model | data = String.toUpper data }
                    , Cmd.none
                    )

                Err _ ->
                    ( { model | error = Just "Failed" }
                    , Cmd.none
                    )
```

**Elm Task (advanced):**
```elm
import Task

-- For chaining async operations
fetchAndProcess : Task Http.Error String
fetchAndProcess =
    Http.task
        { method = "GET"
        , headers = []
        , url = "https://api.example.com/data"
        , body = Http.emptyBody
        , resolver = Http.stringResolver handleResponse
        , timeout = Nothing
        }
        |> Task.map String.toUpper

-- Convert to Cmd
performFetch : Cmd Msg
performFetch =
    Task.attempt GotData fetchAndProcess
```

---

## Common Pitfalls

1. **Result parameter order reversal**
   - Roc: `Result ok err`
   - Elm: `Result err ok`
   - **Always swap parameters** when converting Result types

2. **Record update syntax**
   - Roc: `{ record & field: value }`
   - Elm: `{ record | field = value }`
   - Don't mix up `&`/`|` and `:`/`=`

3. **Case vs When syntax**
   - Roc: `when x is`
   - Elm: `case x of`
   - Remember `of` not `is`

4. **Module target mismatch**
   - Roc CLI/native modules (File, Stdout) don't exist in Elm
   - Must redesign as browser-based UI
   - No file I/O, only HTTP and localStorage

5. **Bang operator translation**
   - Roc: `value = task!`
   - Elm: Must use `Task.andThen` or Cmd with Msg handling
   - No direct equivalent to `!` operator

6. **Capitalization**
   - Roc: `Bool.true`
   - Elm: `True`
   - Watch for True/False vs true/false

7. **Function application**
   - Both use space for application, but Elm heavily uses currying
   - Roc: `List.map(list, fn)` or `List.map list fn`
   - Elm: `List.map fn list` (function first)

---

## Tooling

| Tool | Roc | Elm | Notes |
|------|-----|-----|-------|
| Formatter | `roc format` | `elm-format` | Both enforce standard style |
| REPL | `roc repl` | `elm repl` | Both support interactive testing |
| Test | `roc test` | `elm-test` | Different syntax, same concept |
| Build | `roc build` | `elm make` | Roc → native, Elm → JavaScript |
| Package manager | Platform URLs | `elm install` | Elm has centralized package repo |
| Linter | N/A | `elm-review` | Elm has rich linting ecosystem |

---

## Examples

### Example 1: Simple - Type and Function Translation

**Before (Roc):**
```roc
User : { name : Str, age : U32 }

greet : User -> Str
greet = \user ->
    "Hello, \(user.name)! You are \(Num.toStr(user.age)) years old."

expect greet({ name: "Alice", age: 30 }) == "Hello, Alice! You are 30 years old."
```

**After (Elm):**
```elm
type alias User =
    { name : String
    , age : Int
    }

greet : User -> String
greet user =
    "Hello, " ++ user.name ++ "! You are " ++ String.fromInt user.age ++ " years old."

-- Test (in tests/ directory)
import Test exposing (test)
import Expect

suite =
    test "greet formats message correctly" <|
        \_ ->
            greet { name = "Alice", age = 30 }
                |> Expect.equal "Hello, Alice! You are 30 years old."
```

**Key changes:**
- `Str` → `String`, `U32` → `Int`
- String interpolation `\(...)` → concatenation `++`
- `Num.toStr` → `String.fromInt`
- `expect` → separate test file with `Test` module

### Example 2: Medium - Tag Unions and Pattern Matching

**Before (Roc):**
```roc
Color : [Red, Green, Blue, Custom(U8, U8, U8)]

toHex : Color -> Str
toHex = \color ->
    when color is
        Red -> "#FF0000"
        Green -> "#00FF00"
        Blue -> "#0000FF"
        Custom(r, g, b) ->
            "#\(toHexByte(r))\(toHexByte(g))\(toHexByte(b))"

toHexByte : U8 -> Str
toHexByte = \n ->
    # Implementation details...
```

**After (Elm):**
```elm
type Color
    = Red
    | Green
    | Blue
    | Custom Int Int Int

toHex : Color -> String
toHex color =
    case color of
        Red ->
            "#FF0000"

        Green ->
            "#00FF00"

        Blue ->
            "#0000FF"

        Custom r g b ->
            "#" ++ toHexByte r ++ toHexByte g ++ toHexByte b

toHexByte : Int -> String
toHexByte n =
    -- Implementation using Hex library or String.fromInt with base conversion
    String.fromInt n  -- Simplified for example
```

**Key changes:**
- Structural tag union → Named `type` declaration
- `when x is` → `case x of`
- `U8` → `Int` (Elm doesn't have sized integers)
- String interpolation → concatenation

### Example 3: Complex - Task Chain to TEA

**Before (Roc):**
```roc
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/..."
}

import pf.Http
import pf.Stdout
import pf.Task exposing [Task]

User : { id : U64, name : Str, email : Str }

fetchUser : U64 -> Task User [HttpError]
fetchUser = \userId ->
    url = "https://api.example.com/users/\(Num.toStr(userId))"
    response = Http.get!(url)
    when Decode.fromBytes(response.body, userDecoder) is
        Ok(user) -> Task.ok(user)
        Err(_) -> Task.err(HttpError)

main : Task {} []
main =
    user = fetchUser!(1)
    Stdout.line!("User: \(user.name) (\(user.email))")
```

**After (Elm):**
```elm
module Main exposing (main)

import Browser
import Html exposing (Html, div, text, button)
import Html.Events exposing (onClick)
import Http
import Json.Decode as Decode exposing (Decoder)

-- MODEL

type alias User =
    { id : Int
    , name : String
    , email : String
    }

type RemoteData e a
    = NotAsked
    | Loading
    | Success a
    | Failure e

type alias Model =
    { user : RemoteData Http.Error User
    }

init : () -> ( Model, Cmd Msg )
init _ =
    ( { user = NotAsked }, Cmd.none )

-- UPDATE

type Msg
    = FetchUser
    | GotUser (Result Http.Error User)

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUser ->
            ( { model | user = Loading }
            , fetchUser 1
            )

        GotUser result ->
            case result of
                Ok user ->
                    ( { model | user = Success user }
                    , Cmd.none
                    )

                Err error ->
                    ( { model | user = Failure error }
                    , Cmd.none
                    )

-- HTTP

fetchUser : Int -> Cmd Msg
fetchUser userId =
    Http.get
        { url = "https://api.example.com/users/" ++ String.fromInt userId
        , expect = Http.expectJson GotUser userDecoder
        }

userDecoder : Decoder User
userDecoder =
    Decode.map3 User
        (Decode.field "id" Decode.int)
        (Decode.field "name" Decode.string)
        (Decode.field "email" Decode.string)

-- VIEW

view : Model -> Html Msg
view model =
    div []
        [ case model.user of
            NotAsked ->
                button [ onClick FetchUser ] [ text "Fetch User" ]

            Loading ->
                text "Loading..."

            Success user ->
                div []
                    [ text ("User: " ++ user.name ++ " (" ++ user.email ++ ")")
                    ]

            Failure error ->
                text ("Error: " ++ httpErrorToString error)
        ]

httpErrorToString : Http.Error -> String
httpErrorToString error =
    case error of
        Http.BadUrl url ->
            "Bad URL: " ++ url

        Http.Timeout ->
            "Timeout"

        Http.NetworkError ->
            "Network error"

        Http.BadStatus status ->
            "Bad status: " ++ String.fromInt status

        Http.BadBody body ->
            "Bad body: " ++ body

-- MAIN

main : Program () Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , view = view
        , subscriptions = \_ -> Sub.none
        }
```

**Key changes:**
- Roc's imperative Task chain → Elm's TEA (Model-Update-View)
- Roc's `!` operator → Elm's Cmd and Msg handling
- Roc's CLI output → Elm's HTML view
- Roc's sequential execution → Elm's event-driven updates
- Added loading states (NotAsked, Loading, Success, Failure)
- Explicit error handling in view

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-erlang-elm` - Similar backend-to-frontend conversion patterns
- `lang-roc-dev` - Roc development patterns
- `lang-elm-dev` - Elm development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Task vs Cmd/Sub comparison
- `patterns-serialization-dev` - JSON encoding/decoding across languages
