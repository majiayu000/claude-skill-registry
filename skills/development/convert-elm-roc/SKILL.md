---
name: convert-elm-roc
description: Convert Elm code to idiomatic Roc. Use when migrating Elm frontend code to Roc applications, translating browser-based Elm to platform-agnostic Roc, or refactoring Elm web applications to Roc CLI/native tools. Extends meta-convert-dev with Elm-to-Roc specific patterns.
---

# Convert Elm to Roc

Convert Elm code to idiomatic Roc. This skill extends `meta-convert-dev` with Elm-to-Roc specific type mappings, idiom translations, and architectural patterns for moving from browser-based Elm applications to platform-agnostic Roc code.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Elm types → Roc types
- **Idiom translations**: Elm patterns → idiomatic Roc
- **Architecture patterns**: The Elm Architecture (TEA) → Platform model
- **Effect system**: Cmd/Sub → Task
- **Error handling**: Result types (**REVERSED parameter order!**)
- **Platform shift**: Frontend-specific → General-purpose

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Reverse conversion (Roc → Elm) - see `convert-roc-elm`
- Browser-specific Elm code - Roc doesn't have DOM access

---

## Quick Reference

| Elm | Roc | Notes |
|-----|-----|-------|
| `String` | `Str` | Direct mapping |
| `Int` | `I64` or `U64` | Choose signed/unsigned based on domain |
| `Float` | `F64` | Direct mapping |
| `Bool` | `Bool` | Same with capitalization |
| `List a` | `List a` | Same syntax and operations |
| `{ field : Type }` | `{ field : Type }` | Records are nearly identical |
| `type Custom = Tag1 \| Tag2` | `[Tag1, Tag2]` | Custom types → Tag unions |
| `Result err ok` | `Result ok err` | **REVERSED parameter order!** |
| `Maybe a` | `[Some a, None]` | Optional values |
| `Cmd Msg` or `Task err a` | `Task ok err` | Effect systems differ |
| `case x of` | `when x is` | Pattern matching syntax |
| `Task.perform` | `!` suffix operator | Explicit handling → Bang operator |

---

## 🚨 CRITICAL GOTCHA: Result Type Parameter Order

**This is the most important thing to remember when converting Elm to Roc:**

```elm
-- Elm: Result error ok
divide : Int -> Int -> Result String Int
```

```roc
# Roc: Result ok err (REVERSED!)
divide : I64, I64 -> Result I64 Str
```

### Why This Matters

The parameter order is **completely reversed** between Elm and Roc:

- **Elm**: `Result error ok` - Error type first, success type second
- **Roc**: `Result ok err` - Success type first, error type second

This affects:
- Type signatures
- Type annotations
- Generic type parameters
- Error handling patterns

### Always Remember

When you see Elm's `Result String User`, it becomes Roc's `Result User Str`.

❌ **Wrong**: `Result Str User` (copying Elm order)
✓ **Correct**: `Result User Str` (reversed order)

---

## Architectural Paradigm Shift

### From The Elm Architecture to Platform Model

| Aspect | Elm TEA | Roc Platform Model |
|--------|---------|-------------------|
| **Target** | Browser frontend only | Any platform (CLI, web, native) |
| **Effects** | Runtime-managed Cmd/Sub | Platform-provided Task |
| **Entry point** | `main : Program () Model Msg` | `main : Task {} []` |
| **State** | Explicit Model | Implicit in Task chain |
| **Updates** | `update : Msg → Model → (Model, Cmd Msg)` | Task composition |
| **I/O** | Browser.* modules only | Platform exposes (File, Http, etc.) |

### Elm TEA Application

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

### Roc Platform Equivalent

```roc
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.10.0/vNe6s9hWzoTZtFmNkvEICPErI9ptji_ySjicO6CkucY.tar.br"
}

import pf.Stdout
import pf.Stdin
import pf.Task exposing [Task]

main : Task {} []
main =
    Stdout.line! "Hello, World!"
    Stdout.line! "Enter your name:"
    name = Stdin.line!
    Stdout.line! "Hello, \(name)!"
```

**Key shift:** Elm's declarative Model-Update-View loop becomes Roc's imperative Task chain.

**Note:** The Roc version is CLI-based because Roc doesn't target the browser. For equivalent browser functionality, you'd need a Roc web platform (still in development).

---

## Type System Mapping

### Primitive Types

| Elm | Roc | Notes |
|-----|-----|-------|
| `True` / `False` | `Bool.true` / `Bool.false` | Capitalization differs |
| `42` | `42` | Integer literals |
| `3.14` | `3.14` | Float literals |
| `"text"` | `"text"` | String literals |
| `Int` | `I64` or `U64` | Elm has arbitrary precision, Roc has sized types |
| `Float` | `F64` or `F32` | Elm has single Float, Roc has sized types |
| `String` | `Str` | Direct mapping |
| `Char` | `U32` | Roc treats chars as Unicode scalar values |

### Collection Types

| Elm | Roc | Notes |
|-----|-----|-------|
| `List a` | `List a` | Identical syntax and semantics |
| `Dict comparable v` | `Dict k v` | Roc requires `k` to implement Hash & Eq |
| `Set comparable` | `Set a` | Roc requires `a` to implement Hash & Eq |
| `( a, b )` | `(a, b)` | Tuples (Roc supports arbitrary tuple sizes) |
| `Array a` | `List a` | Elm's Array → Roc's List (Roc optimizes internally) |

### Record Types

| Elm | Roc | Notes |
|-----|-----|-------|
| `{ name : String, age : Int }` | `{ name : Str, age : U32 }` | Nearly identical, just type name differences |
| `{ user \| age = 31 }` | `{ user & age: 31 }` | Record update syntax differs (\| vs &, = vs :) |
| `{ name, age } = user` | `{ name, age } = user` | Destructuring identical |
| `user.name` | `user.name` | Field access identical |

### Custom Types to Tag Unions

**Elm:**
```elm
-- Named custom type (nominal)
type Color
    = Red
    | Green
    | Blue
    | Custom Int Int Int

type alias RGB =
    { r : Int, g : Int, b : Int }
```

**Roc:**
```roc
# Structural tag union
Color : [Red, Green, Blue, Custom(U8, U8, U8)]

# Record type alias
RGB : { r : U8, g : U8, b : U8 }
```

**Key differences:**
- Elm requires explicit `type` declaration
- Roc uses structural types (no declaration needed)
- Elm uses type constructors with `|`
- Roc uses tag union syntax with `[]`

### Optional Values

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

**Roc:**
```roc
# Inline tag union (no built-in Maybe)
email : [Some Str, None]
email = Some("alice@example.com")

# Pattern match
emailText : Str
emailText =
    when email is
        Some(addr) -> addr
        None -> "no email"

# Manual helper or use Result
```

**Translation:**
- `Maybe a` → `[Some a, None]`
- `Just value` → `Some(value)`
- `Nothing` → `None`

### Result Type (Parameter Order Reversed!)

**Elm:**
```elm
-- Result error ok
divide : Int -> Int -> Result String Int
divide a b =
    if b == 0 then
        Err "Division by zero"
    else
        Ok (a // b)
```

**Roc:**
```roc
# Result ok err (REVERSED!)
divide : I64, I64 -> Result I64 Str
divide = \a, b ->
    if b == 0 then
        Err("Division by zero")
    else
        Ok(a // b)
```

**CRITICAL:**
- Elm's `Result error ok` has error first
- Roc's `Result ok err` has success first
- **Always reverse the parameter order** when converting

---

## Idiom Translation

### 1. Pattern Matching: case → when

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

**Roc:**
```roc
classify : I64 -> Str
classify = \n ->
    when n is
        0 -> "zero"
        x if x < 0 -> "negative"
        _ -> "positive"
```

**Why this translation:**
- Elm's `case` becomes Roc's `when`
- Elm uses `if` expressions in branches, Roc has guard clauses (`if` after pattern)
- Roc allows inline guards which are more concise

### 2. List Processing

**Elm:**
```elm
doubled : List Int
doubled =
    List.map (\x -> x * 2) [ 1, 2, 3, 4, 5 ]

-- Pipeline style
result : Int
result =
    [ 1, 2, 3, 4, 5 ]
        |> List.map (\x -> x * 2)
        |> List.filter (\x -> x > 5)
        |> List.foldl (+) 0
```

**Roc:**
```roc
doubled : List I64
doubled = List.map([1, 2, 3, 4, 5], \x -> x * 2)

# Pipeline style (same!)
result : I64
result = [1, 2, 3, 4, 5]
    |> List.map(\x -> x * 2)
    |> List.keepIf(\x -> x > 5)
    |> List.walk(0, Num.add)
```

**Why this translation:**
- `List.filter` → `List.keepIf` (different name, same semantics)
- `List.foldl` / `List.foldr` → `List.walk` (different name)
- Pipeline operator `|>` is identical
- Roc supports both `List.map(list, fn)` and `List.map list fn` syntax

### 3. Record Updates

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

**Why this translation:**
- Elm uses `|` for updates, Roc uses `&`
- Elm uses `=` for field assignment, Roc uses `:`
- Syntax is almost identical otherwise

### 4. Cmd/Task → Task

**Elm:**
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

**Roc:**
```roc
main : Task {} []
main =
    data = Http.get!("https://api.example.com/data")
    processed = Str.toUpper(data)
    Task.ok({})
```

**Why this translation:**
- Elm's Cmd with Msg handling becomes Roc's direct Task chaining
- Elm's `Task.perform` becomes Roc's `!` operator
- Elm's event-driven model becomes Roc's sequential execution
- No Model or Msg types needed in Roc for simple cases

### 5. Error Propagation

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

**Roc:**
```roc
# Roc: Result ok err (reversed params!)
calculate : I64, I64, I64 -> Result I64 Str
calculate = \a, b, c ->
    x = divide!(a, b)  # Returns early on Err
    y = divide!(x, c)  # Returns early on Err
    Ok(y)
```

**Why this translation:**
- Elm's `Result.andThen` becomes Roc's `!` operator
- Roc's `!` provides automatic early return on error
- Much more concise than Elm's explicit chaining
- Remember to **reverse Result type parameters**!

### 6. Opaque Types

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

**Roc:**
```roc
interface Age
    exposes [Age, create, toU32]
    imports []

# Opaque type
Age := U32

create : U32 -> Result Age [InvalidAge]
create = \n ->
    if n >= 0 && n < 150 then
        Ok(@Age(n))
    else
        Err(InvalidAge)

toU32 : Age -> U32
toU32 = \@Age(n) -> n
```

**Why this translation:**
- Elm uses pattern matching for unwrapping, Roc uses `@` syntax
- Both achieve opacity through module exports
- Roc's `@Age(n)` wrapping is more explicit than Elm's `Age n`
- Roc uses `Result` for validation, Elm uses `Maybe` (different conventions)

---

## Paradigm Translation: TEA → Platform Model

### Mental Model Shift

| Elm Concept | Roc Approach | Key Insight |
|-------------|--------------|-------------|
| Model-Update-View loop | Task chain (sequential) | Declarative → Imperative |
| Browser provides events | Platform provides I/O | Browser → CLI/Native |
| `main` returns Program | `main` returns Task | Pure → Effect |
| Cmd issued, Msg received | Tasks compose with `!` | Indirect → Direct |

### Effect System Comparison

| Elm Model | Roc Model | Conceptual Translation |
|-----------|-----------|------------------------|
| Runtime handles Cmd/Sub | Platform handles Tasks | Both managed by runtime |
| Asynchronous with Msg | Sequential with `!` | Event-driven → Chain |
| Cmd.none / new Cmd | Task.ok/Task.err | Side effect → Return value |

### Example: HTTP Fetch

**Elm (TEA):**
```elm
type alias Model =
    { users : RemoteData Http.Error (List User)
    }

type Msg
    = FetchUsers
    | GotUsers (Result Http.Error (List User))

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUsers ->
            ( { model | users = Loading }
            , Http.get
                { url = "/api/users"
                , expect = Http.expectJson GotUsers usersDecoder
                }
            )

        GotUsers result ->
            case result of
                Ok users ->
                    ( { model | users = Success users }, Cmd.none )

                Err error ->
                    ( { model | users = Failure error }, Cmd.none )
```

**Roc (Platform):**
```roc
main : Task {} []
main =
    users = Http.get!("/api/users")
    decoded = Decode.fromBytes!(users, usersDecoder)
    Stdout.line!("Fetched \(List.len(decoded) |> Num.toStr) users")
```

**Key differences:**
- Elm models loading states explicitly
- Roc handles success/error sequentially
- Elm's async becomes Roc's sequential (platform handles concurrency)
- No Model or Msg types needed in Roc

---

## Error Handling

### Elm Result → Roc Result

**Key Difference: Parameter order is reversed!**

```elm
-- Elm: Result err ok
parseAge : String -> Result String Int
parseAge str =
    case String.toInt str of
        Just age ->
            if age >= 0 then
                Ok age
            else
                Err "Negative age"

        Nothing ->
            Err "Not a number"
```

```roc
# Roc: Result ok err (REVERSED!)
parseAge : Str -> Result U32 Str
parseAge = \str ->
    when Str.toU32(str) is
        Ok(age) if age >= 0 -> Ok(age)
        Ok(_) -> Err("Negative age")
        Err(_) -> Err("Not a number")
```

### Error Type Modeling

**Elm uses named custom types:**
```elm
type FetchError
    = NetworkError Http.Error
    | NotFound
    | Unauthorized

fetchUser : Int -> Task FetchError User
```

**Roc uses inline tag unions:**
```roc
fetchUser : U64 -> Task User [NetworkError, NotFound, Unauthorized]
```

**Translation:**
- Elm's named error types → Roc's inline tag unions
- Same expressiveness, less ceremony
- Roc is structural, Elm is nominal

---

## Effect System Translation

### Cmd in Elm vs Task in Roc

**Elm Cmd (event-driven):**
```elm
type Msg
    = GotData (Result Http.Error String)

fetchData : Cmd Msg
fetchData =
    Http.get
        { url = "https://api.example.com/data"
        , expect = Http.expectString GotData
        }

-- Must handle result in update function
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GotData result ->
            -- Handle result here
            ...
```

**Roc Task (sequential):**
```roc
fetchData : Task Str []
fetchData =
    Http.get!("https://api.example.com/data")
```

**Why this translation:**
- Elm's Cmd is fire-and-forget, result comes via Msg
- Roc's Task chains sequentially with `!`
- Elm separates effect from handling, Roc combines them

### Sub in Elm vs Task in Roc

**Elm Subscriptions:**
```elm
subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch
        [ Time.every 1000 Tick
        , Browser.Events.onResize WindowResized
        ]
```

**Roc approach:**
Roc doesn't have built-in subscriptions. Platforms may provide equivalent mechanisms through Task-based polling or event streams, but this is platform-specific.

For periodic tasks, you'd typically use platform-specific APIs or structure your `main` Task to loop.

---

## Module System Translation

### Elm Modules → Roc Interfaces

**Elm:**
```elm
module User exposing (User, create, getName, getAge)

type alias User =
    { name : String
    , age : Int
    }

create : String -> Int -> User
create name age =
    { name = name, age = age }

getName : User -> String
getName user =
    user.name

getAge : User -> Int
getAge user =
    user.age
```

**Roc:**
```roc
interface User
    exposes [User, create, getName, getAge]
    imports []

User : {
    name : Str,
    age : U32,
}

create : Str, U32 -> User
create = \name, age ->
    { name, age }

getName : User -> Str
getName = \user -> user.name

getAge : User -> U32
getAge = \user -> user.age
```

**Translation:**
- `module` → `interface`
- `exposing` → `exposes`
- `type alias` → type annotation
- Same visibility model (only exposed items are public)

### Import Patterns

**Elm:**
```elm
import Dict
import Dict exposing (Dict)
import List exposing (map, filter)
import Maybe exposing (Maybe(..))
import Html as H
import Html.Events as Events
```

**Roc:**
```roc
import Dict
import Dict exposing [Dict]
import List exposing [map, keepIf]
import pf.Stdout
import pf.Task exposing [Task]

# Note: Roc doesn't have import aliasing yet
# Must use full qualified names
```

**Translation:**
- `exposing` → `exposing`
- Parentheses `()` → Brackets `[]`
- Elm's `import as` → Not yet available in Roc

---

## Common Pitfalls

1. **Result parameter order reversal (MOST CRITICAL)**
   - Elm: `Result err ok`
   - Roc: `Result ok err`
   - **Always reverse parameters** when converting Result types
   - Double-check every Result type signature!

2. **Record update syntax**
   - Elm: `{ record | field = value }`
   - Roc: `{ record & field: value }`
   - Don't mix up `|`/`&` and `=`/`:`

3. **Case vs When syntax**
   - Elm: `case x of`
   - Roc: `when x is`
   - Remember `is` not `of`

4. **Platform target mismatch**
   - Elm targets browser only (DOM, HTML, CSS)
   - Roc is platform-agnostic (CLI, native, potentially web)
   - Browser-specific Elm code needs redesign

5. **Bang operator vs explicit Task**
   - Elm: No `!` operator, use `Task.perform` or `Cmd`
   - Roc: `value = task!` for sequential execution
   - Much more concise in Roc

6. **Capitalization**
   - Elm: `True`, `False`
   - Roc: `Bool.true`, `Bool.false`
   - Watch for True/False differences

7. **Function types**
   - Elm: `a -> b -> c` (curried)
   - Roc: `a, b -> c` (comma-separated params)
   - Roc allows both, but commas are clearer

8. **Maybe vs tag union**
   - Elm: Built-in `Maybe a` with `Just`/`Nothing`
   - Roc: Use `[Some a, None]` (no built-in Maybe)
   - Must define tag union explicitly

9. **List function names**
   - Elm: `List.filter`, `List.foldl`, `List.foldr`
   - Roc: `List.keepIf`, `List.walk`
   - Same concepts, different names

10. **String interpolation**
    - Elm: `"Hello, " ++ name ++ "!"`
    - Roc: `"Hello, \(name)!"`
    - Roc has built-in string interpolation

---

## Tooling

| Tool | Elm | Roc | Notes |
|------|-----|-----|-------|
| Formatter | `elm-format` | `roc format` | Both enforce standard style |
| REPL | `elm repl` | `roc repl` | Both support interactive testing |
| Test | `elm-test` | `roc test` | Different syntax (case vs expect) |
| Build | `elm make` | `roc build` | Elm → JavaScript, Roc → native |
| Package manager | `elm install` | Platform URLs | Roc uses URL-based dependencies |
| Linter | `elm-review` | N/A | Elm has rich linting, Roc doesn't yet |

---

## Examples

### Example 1: Simple - Type and Function Translation

**Before (Elm):**
```elm
type alias User =
    { name : String
    , age : Int
    }

greet : User -> String
greet user =
    "Hello, " ++ user.name ++ "! You are " ++ String.fromInt user.age ++ " years old."

-- Test
import Test exposing (test)
import Expect

suite =
    test "greet formats message correctly" <|
        \_ ->
            greet { name = "Alice", age = 30 }
                |> Expect.equal "Hello, Alice! You are 30 years old."
```

**After (Roc):**
```roc
User : { name : Str, age : U32 }

greet : User -> Str
greet = \user ->
    "Hello, \(user.name)! You are \(Num.toStr(user.age)) years old."

expect greet({ name: "Alice", age: 30 }) == "Hello, Alice! You are 30 years old."
```

**Key changes:**
- `String` → `Str`, `Int` → `U32`
- String concatenation `++` → interpolation `\(...)`
- `String.fromInt` → `Num.toStr`
- Elm's separate test file → inline `expect`
- `type alias` → type annotation

### Example 2: Medium - Custom Types and Pattern Matching

**Before (Elm):**
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
    -- Implementation using Hex library
    String.fromInt n  -- Simplified
```

**After (Roc):**
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
    # Implementation
    Num.toStr(n)  # Simplified
```

**Key changes:**
- Named `type` declaration → Structural tag union
- `case x of` → `when x is`
- `Int` → `U8` (Roc has sized integers)
- String concatenation → interpolation
- Constructor `Custom r g b` → `Custom(r, g, b)`

### Example 3: Complex - TEA to Platform Model

**Before (Elm):**
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

**After (Roc):**
```roc
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.10.0/vNe6s9hWzoTZtFmNkvEICPErI9ptji_ySjicO6CkucY.tar.br"
}

import pf.Http
import pf.Stdout
import pf.Task exposing [Task]
import json.Decode

# Note: Result type parameters REVERSED!
# Elm: Result Http.Error User
# Roc: Result User [HttpErr]

User : { id : U64, name : Str, email : Str }

fetchUser : U64 -> Task User [HttpErr, DecodeErr]
fetchUser = \userId ->
    url = "https://api.example.com/users/\(Num.toStr(userId))"
    response = Http.get!(url)

    when Decode.fromBytes(response.body, userDecoder) is
        Ok(user) -> Task.ok(user)
        Err(err) -> Task.err(DecodeErr)

userDecoder : Decode.Decoder User
userDecoder =
    Decode.record(\field ->
        {
            id: field.required("id", Decode.u64),
            name: field.required("name", Decode.str),
            email: field.required("email", Decode.str),
        }
    )

main : Task {} []
main =
    when fetchUser(1) is
        Ok(user) ->
            Stdout.line!("User: \(user.name) (\(user.email))")

        Err(HttpErr) ->
            Stdout.line!("HTTP error occurred")

        Err(DecodeErr) ->
            Stdout.line!("Failed to decode user")
```

**Key changes:**
- Elm's TEA (Model-Update-View) → Roc's Task chain
- Elm's `Cmd Msg` handling → Roc's `!` operator
- Elm's HTML view → Roc's CLI output
- Elm's loading states → Roc's direct execution
- Elm's `Result Http.Error User` → Roc's `Result User [HttpErr, DecodeErr]` (**reversed params!**)
- No Model, Msg, or update function needed
- Direct error handling with pattern matching

---

## Testing Translation

### Elm's elm-test → Roc's expect

**Elm:**
```elm
-- tests/UserTests.elm
module UserTests exposing (suite)

import Test exposing (Test, describe, test)
import Expect
import User

suite : Test
suite =
    describe "User module"
        [ describe "greet"
            [ test "formats greeting correctly" <|
                \_ ->
                    User.greet { name = "Alice", age = 30 }
                        |> Expect.equal "Hello, Alice! You are 30 years old."

            , test "handles young age" <|
                \_ ->
                    User.greet { name = "Bob", age = 5 }
                        |> Expect.equal "Hello, Bob! You are 5 years old."
            ]
        ]
```

**Roc:**
```roc
# User.roc
interface User
    exposes [User, greet]
    imports []

User : { name : Str, age : U32 }

greet : User -> Str
greet = \user ->
    "Hello, \(user.name)! You are \(Num.toStr(user.age)) years old."

# Inline tests
expect greet({ name: "Alice", age: 30 }) == "Hello, Alice! You are 30 years old."
expect greet({ name: "Bob", age: 5 }) == "Hello, Bob! You are 5 years old."
```

**Translation:**
- Elm's separate test files → Roc's inline `expect`
- Elm's `describe` and `test` → Roc's flat `expect` statements
- Elm's `Expect.equal` → Roc's `==` operator
- Run with `elm-test` → Run with `roc test`

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-roc-elm` - Reverse conversion (Roc → Elm)
- `convert-elm-haskell` - Similar functional language conversion patterns
- `lang-elm-dev` - Elm development patterns
- `lang-roc-dev` - Roc development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Cmd/Sub vs Task comparison
- `patterns-serialization-dev` - JSON encoding/decoding across languages
- `patterns-metaprogramming-dev` - Why both languages avoid metaprogramming
