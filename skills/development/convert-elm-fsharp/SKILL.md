---
name: convert-elm-fsharp
description: Convert Elm code to idiomatic F#. Use when migrating Elm applications to F#, translating Elm's Model-View-Update pattern to F# patterns, or refactoring Elm codebases to leverage .NET ecosystem. Extends meta-convert-dev with Elm-to-F# specific patterns.
---

# Convert Elm to F#

Convert Elm code to idiomatic F#. This skill extends `meta-convert-dev` with Elm-to-F# specific type mappings, idiom translations, and tooling for migrating functional frontend code to the .NET ecosystem.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Elm types → F# types
- **Idiom translations**: Elm patterns → idiomatic F#
- **Error handling**: Elm Result/Maybe → F# Result/Option
- **Architecture**: The Elm Architecture (TEA) → F# Elmish or MVU patterns
- **Functional patterns**: Pure functions, immutability preserved in F#

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Elm language fundamentals - see `lang-elm-dev`
- F# language fundamentals - see `lang-fsharp-dev`
- Reverse conversion (F# → Elm) - see `convert-fsharp-elm`
- F# web frameworks in depth - see framework-specific skills

---

## Quick Reference

| Elm | F# | Notes |
|-----|-----|-------|
| `String` | `string` | Direct mapping |
| `Int` | `int` | 32-bit signed integer |
| `Float` | `float` | 64-bit floating point |
| `Bool` | `bool` | Direct mapping |
| `List a` | `'a list` | Immutable linked list |
| `Array a` | `'a array` | Mutable fixed-size array |
| `Maybe a` | `'a option` | Same semantics: Some/None |
| `Result error value` | `Result<'value, 'error>` | Same semantics: Ok/Error |
| `type alias` | `type` (type alias) | Direct mapping |
| `type` (union) | `type` (discriminated union) | Direct mapping |
| `Cmd msg` | `Async<'msg>` or Elmish `Cmd<'msg>` | Depends on framework |
| `Sub msg` | Event subscriptions in Elmish | Framework-specific |
| `Html msg` | Elmish.React `ReactElement` | Frontend framework |

## When Converting Code

1. **Analyze source thoroughly** before writing target
2. **Map types first** - Elm and F# type systems are very similar
3. **Preserve functional purity** - both languages emphasize immutability
4. **Adopt F# idioms** - leverage .NET libraries and computation expressions
5. **Handle The Elm Architecture** - map to Elmish or custom MVU implementation
6. **Test equivalence** - same inputs → same outputs

---

## Type System Mapping

### Primitive Types

| Elm | F# | Notes |
|-----|-----|-------|
| `String` | `string` | UTF-16 in F# (via .NET), UTF-8 in Elm |
| `Int` | `int` | Both 32-bit signed |
| `Float` | `float` | F# `float` is 64-bit (alias for `double`) |
| `Bool` | `bool` | Direct mapping |
| `Char` | `char` | Single character |
| `()` | `unit` | Unit type (void) |
| `never` | N/A | Elm's impossible type; F# doesn't have exact equivalent |

### Collection Types

| Elm | F# | Notes |
|-----|-----|-------|
| `List a` | `'a list` | Immutable linked list, same semantics |
| `Array a` | `'a array` | F# arrays are mutable but similar performance |
| `Set a` | `Set<'a>` | Immutable set in both |
| `Dict k v` | `Map<'k, 'v>` | Immutable map; F# also has `Dictionary<'k,'v>` (mutable) |
| `Tuple` | Tuple | Same syntax: `(a, b)` |

### Composite Types

| Elm | F# | Notes |
|-----|-----|-------|
| `type alias` | `type` (type alias) | `type Person = { Name: string; Age: int }` |
| `type` (union) | `type` (discriminated union) | Same concept, slightly different syntax |
| Record | Record | Same semantics, nearly identical syntax |
| Opaque type | Single-case union | `type Email = Email of string` |

### Option/Maybe Types

| Elm | F# | Notes |
|-----|-----|-------|
| `Maybe a` | `'a option` | Both have `Some`/`Just` and `None`/`Nothing` |
| `Just x` | `Some x` | Constructor name differs |
| `Nothing` | `None` | Constructor name differs |
| `Maybe.withDefault` | `Option.defaultValue` | Same semantics |
| `Maybe.map` | `Option.map` | Same semantics |
| `Maybe.andThen` | `Option.bind` | Monadic bind |

### Result Types

| Elm | F# | Notes |
|-----|-----|-------|
| `Result error value` | `Result<'value, 'error>` | Type parameters in reverse order! |
| `Ok value` | `Ok value` | Same constructor |
| `Err error` | `Error error` | F# uses `Error`, not `Err` |
| `Result.map` | `Result.map` | Same semantics |
| `Result.andThen` | `Result.bind` | Monadic bind |
| `Result.withDefault` | `Result.defaultValue` | Same semantics |

**Critical Note:** Elm's `Result error value` has error first, but F# `Result<'T, 'TError>` has value first!

### Generic Type Parameters

| Elm | F# | Notes |
|-----|-----|-------|
| `a`, `b`, `c` | `'a`, `'b`, `'c` | F# uses single quote prefix |
| `comparable` | `'a when 'a : comparison` | Constraint syntax differs |
| `number` | `^a when ^a : (static member (+) : ^a * ^a -> ^a)` | F# uses SRTPs (complex) |
| `appendable` | No built-in equivalent | Manual trait constraints |

---

## Idiom Translation

### Pattern 1: Maybe/Option Handling

**Elm:**
```elm
type alias User =
    { name : String
    , email : Maybe String
    }

getUserEmail : User -> String
getUserEmail user =
    Maybe.withDefault "No email" user.email

findUser : Int -> List User -> Maybe User
findUser id users =
    List.filter (\u -> u.id == id) users
        |> List.head
```

**F#:**
```fsharp
type User = {
    Name: string
    Email: string option
}

let getUserEmail (user: User) : string =
    user.Email |> Option.defaultValue "No email"

let findUser (id: int) (users: User list) : User option =
    users |> List.tryFind (fun u -> u.Id = id)
```

**Why this translation:**
- `Maybe` → `option` is a direct semantic mapping
- `Just` → `Some`, `Nothing` → `None`
- `Maybe.withDefault` → `Option.defaultValue`
- `List.head : List a -> Maybe a` → `List.tryFind` or `List.tryHead`
- F# has richer `Option` module with more combinators

### Pattern 2: Result/Error Handling

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
            Err "Not a valid integer"

validateUser : String -> String -> Result Error User
validateUser name ageStr =
    parseAge ageStr
        |> Result.andThen (\age -> Ok { name = name, age = age })
```

**F#:**
```fsharp
type Error = string

let parseAge (str: string) : Result<int, Error> =
    match System.Int32.TryParse(str) with
    | true, age when age >= 0 ->
        Ok age
    | true, _ ->
        Error "Age must be non-negative"
    | false, _ ->
        Error "Not a valid integer"

let validateUser (name: string) (ageStr: string) : Result<User, Error> =
    parseAge ageStr
    |> Result.bind (fun age -> Ok { Name = name; Age = age })
```

**Why this translation:**
- `Result error value` (Elm) → `Result<'value, 'error>` (F#) - **note reversed type parameters**
- `Ok`/`Err` → `Ok`/`Error`
- `Result.andThen` → `Result.bind`
- F# uses `TryParse` pattern for parsing (returns tuple `bool * value`)
- Both support railway-oriented programming with bind/map

### Pattern 3: Union Types and Pattern Matching

**Elm:**
```elm
type Msg
    = Increment
    | Decrement
    | SetValue Int
    | Reset

update : Msg -> Model -> Model
update msg model =
    case msg of
        Increment ->
            { model | count = model.count + 1 }

        Decrement ->
            { model | count = model.count - 1 }

        SetValue n ->
            { model | count = n }

        Reset ->
            { model | count = 0 }
```

**F#:**
```fsharp
type Msg =
    | Increment
    | Decrement
    | SetValue of int
    | Reset

let update (msg: Msg) (model: Model) : Model =
    match msg with
    | Increment ->
        { model with Count = model.Count + 1 }

    | Decrement ->
        { model with Count = model.Count - 1 }

    | SetValue n ->
        { model with Count = n }

    | Reset ->
        { model with Count = 0 }
```

**Why this translation:**
- Discriminated unions are nearly identical
- Elm: `Type arg` → F#: `Type of arg`
- Record update syntax: `{ model | field = value }` → `{ model with Field = value }`
- Pattern matching syntax is nearly identical
- F# requires explicit `of` keyword for union cases with data

### Pattern 4: List Operations

**Elm:**
```elm
users : List User
users =
    [ { name = "Alice", age = 30 }
    , { name = "Bob", age = 25 }
    ]

activeUsers : List User -> List User
activeUsers =
    List.filter .active
        >> List.map .name
        >> List.sort

totalAge : List User -> Int
totalAge users =
    List.foldl (\user sum -> sum + user.age) 0 users
```

**F#:**
```fsharp
let users: User list =
    [ { Name = "Alice"; Age = 30 }
      { Name = "Bob"; Age = 25 } ]

let activeUsers: User list -> string list =
    List.filter (fun u -> u.Active)
    >> List.map (fun u -> u.Name)
    >> List.sort

let totalAge (users: User list) : int =
    users |> List.fold (fun sum user -> sum + user.Age) 0
```

**Why this translation:**
- List syntax nearly identical: `[ items ]`
- Function composition: `>>` in both languages
- `List.foldl` → `List.fold` (F# fold is left-associative by default)
- F# has more list functions (`List.sumBy`, `List.groupBy`, etc.)
- Record access: `.field` → `(fun r -> r.Field)` or use lambda

### Pattern 5: The Elm Architecture (TEA) → F# Elmish

**Elm:**
```elm
type alias Model =
    { count : Int }

type Msg
    = Increment
    | Decrement

init : ( Model, Cmd Msg )
init =
    ( { count = 0 }, Cmd.none )

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment ->
            ( { model | count = model.count + 1 }, Cmd.none )

        Decrement ->
            ( { model | count = model.count - 1 }, Cmd.none )

view : Model -> Html Msg
view model =
    div []
        [ button [ onClick Decrement ] [ text "-" ]
        , text (String.fromInt model.count)
        , button [ onClick Increment ] [ text "+" ]
        ]
```

**F# (using Elmish):**
```fsharp
open Elmish

type Model = { Count: int }

type Msg =
    | Increment
    | Decrement

let init () : Model * Cmd<Msg> =
    { Count = 0 }, Cmd.none

let update (msg: Msg) (model: Model) : Model * Cmd<Msg> =
    match msg with
    | Increment ->
        { model with Count = model.Count + 1 }, Cmd.none

    | Decrement ->
        { model with Count = model.Count - 1 }, Cmd.none

let view (model: Model) (dispatch: Msg -> unit) =
    div [] [
        button [ OnClick (fun _ -> dispatch Decrement) ] [ str "-" ]
        str (string model.Count)
        button [ OnClick (fun _ -> dispatch Increment) ] [ str "+" ]
    ]
```

**Why this translation:**
- Elmish is F#'s implementation of The Elm Architecture
- Model, Msg, init, update, view pattern is identical
- `Cmd` type is similar but uses F# async under the hood
- View function receives `dispatch` explicitly in F#
- `Html msg` → `ReactElement` (via Fable.React)

### Pattern 6: JSON Decoding

**Elm:**
```elm
import Json.Decode as Decode

type alias User =
    { id : Int
    , name : String
    , email : Maybe String
    }

userDecoder : Decode.Decoder User
userDecoder =
    Decode.map3 User
        (Decode.field "id" Decode.int)
        (Decode.field "name" Decode.string)
        (Decode.maybe (Decode.field "email" Decode.string))
```

**F#:**
```fsharp
open System.Text.Json
open System.Text.Json.Serialization

type User = {
    [<JsonPropertyName("id")>]
    Id: int

    [<JsonPropertyName("name")>]
    Name: string

    [<JsonPropertyName("email")>]
    Email: string option
}

// Automatic with System.Text.Json or Thoth.Json
let parseUser (json: string) : Result<User, string> =
    try
        JsonSerializer.Deserialize<User>(json) |> Ok
    with ex ->
        Error ex.Message

// Or with Thoth.Json for Elm-style decoders
open Thoth.Json.Net

let userDecoder : Decoder<User> =
    Decode.object (fun get -> {
        Id = get.Required.Field "id" Decode.int
        Name = get.Required.Field "name" Decode.string
        Email = get.Optional.Field "email" Decode.string
    })
```

**Why this translation:**
- F# offers two approaches: attribute-based (simpler) or decoder-based (like Elm)
- Thoth.Json provides Elm-style decoders for F#
- System.Text.Json uses attributes and reflection
- `Maybe` fields → `option` with proper serialization handling
- F# has more serialization libraries available (.NET ecosystem)

---

## Error Handling

### Elm's Error Model

Elm guarantees **no runtime exceptions** through its type system:
- All errors are encoded in types (`Maybe`, `Result`)
- Impossible states are made impossible via union types
- Compiler enforces exhaustive pattern matching

### F#'s Error Model

F# has multiple error handling approaches:

1. **Option/Result types** (recommended for Elm migrations)
2. **Exceptions** (for interop with .NET libraries)
3. **Computation expressions** (for error workflows)

### Migration Strategy

**Preserve Elm's error safety:**
```fsharp
// Use Result for expected errors
type ValidationError =
    | EmptyName
    | InvalidEmail
    | AgeTooYoung

let validateUser name email age : Result<User, ValidationError> =
    if String.IsNullOrWhiteSpace(name) then
        Error EmptyName
    elif not (email.Contains("@")) then
        Error InvalidEmail
    elif age < 18 then
        Error AgeTooYoung
    else
        Ok { Name = name; Email = email; Age = age }

// Chain validations
let createUser name email age =
    result {
        let! validatedUser = validateUser name email age
        let! savedUser = saveToDatabase validatedUser
        return savedUser
    }
```

**Handle .NET exceptions when necessary:**
```fsharp
// Wrap .NET APIs that throw exceptions
let safeParse (str: string) : Result<int, string> =
    try
        int str |> Ok
    with
    | :? System.FormatException -> Error "Invalid format"
    | :? System.OverflowException -> Error "Number too large"
    | ex -> Error ex.Message
```

---

## Concurrency Patterns

### Elm: Cmd and Tasks

Elm uses `Cmd` for side effects and `Task` for asynchronous operations:

```elm
type Msg
    = GotUsers (Result Http.Error (List User))

fetchUsers : Cmd Msg
fetchUsers =
    Http.get
        { url = "https://api.example.com/users"
        , expect = Http.expectJson GotUsers usersDecoder
        }
```

### F#: Async and Elmish Commands

F# uses `Async<'T>` for asynchronous operations and Elmish `Cmd<'Msg>`:

```fsharp
type Msg =
    | GotUsers of Result<User list, string>

let fetchUsers : Cmd<Msg> =
    Cmd.OfAsync.perform
        (fun () -> async {
            let! response = Http.get "https://api.example.com/users"
            return! parseUsers response
        })
        ()
        (fun users -> GotUsers (Ok users))
        (fun ex -> GotUsers (Error ex.Message))

// Or with computation expression
let fetchUsersAsync () : Async<Result<User list, string>> =
    async {
        try
            let! response = Http.AsyncGet("https://api.example.com/users")
            let! users = parseUsersAsync response
            return Ok users
        with ex ->
            return Error ex.Message
    }
```

**Why this translation:**
- `Cmd msg` → `Cmd<'msg>` (Elmish)
- `Task` → `Async<'T>` (F# async workflow)
- Elmish provides helpers like `Cmd.OfAsync.perform`
- F# async is more powerful but requires explicit error handling

---

## Common Pitfalls

1. **Type Parameter Order in Result**
   - Elm: `Result error value` (error first)
   - F#: `Result<'value, 'error>` (value first)
   - Always double-check when converting Result types!

2. **Constructor Names**
   - Elm: `Just`, `Nothing`, `Err`
   - F#: `Some`, `None`, `Error`
   - Remember to rename when converting

3. **Record Update Syntax**
   - Elm: `{ model | field = value }`
   - F#: `{ model with Field = value }`
   - Different keywords: `|` vs `with`

4. **Union Case Syntax**
   - Elm: `Type arg`
   - F#: `Type of arg`
   - F# requires `of` keyword

5. **List vs Array Performance**
   - Both Elm and F# `list` are immutable linked lists
   - F# also has mutable `array` for performance-critical code
   - Prefer `list` for Elm semantics, consider `array` for hot paths

6. **Module Qualification**
   - Elm: `List.map`, `String.toInt`
   - F#: `List.map`, `System.Int32.Parse`
   - F# may require fully qualified names for .NET types

7. **Null Safety**
   - Elm: No null, ever
   - F#: `null` exists for .NET interop
   - Use `Option.ofObj` to convert nullable .NET values to `option`

8. **Capitalization Conventions**
   - Elm: camelCase for everything except types
   - F#: PascalCase for types and record fields, camelCase for values
   - Must rename fields when converting records

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| **Fable** | F# → JavaScript compiler | Compile F# to JS like Elm compiles to JS |
| **Elmish** | TEA implementation for F# | Official F# implementation of Elm Architecture |
| **Elmish.React** | React bindings for Elmish | Render views using React |
| **Thoth.Json** | JSON decoding like Elm | Elm-style decoders for F# |
| **Feliz** | Modern F# React DSL | Alternative to Elmish.React |
| **Ionide** | F# IDE support | VS Code extension for F# |
| **Fantomas** | F# code formatter | Like elm-format |
| **FsCheck** | Property-based testing | Like Elm's fuzz testing |

---

## Examples

### Example 1: Simple - Type and Function

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
```

**After (F#):**
```fsharp
type Point = {
    X: float
    Y: float
}

let distance (p1: Point) (p2: Point) : float =
    let dx = p1.X - p2.X
    let dy = p1.Y - p2.Y
    sqrt (dx * dx + dy * dy)
```

### Example 2: Medium - Union Types and Pattern Matching

**Before (Elm):**
```elm
type Tree a
    = Empty
    | Node a (Tree a) (Tree a)

depth : Tree a -> Int
depth tree =
    case tree of
        Empty ->
            0

        Node _ left right ->
            1 + max (depth left) (depth right)

mapTree : (a -> b) -> Tree a -> Tree b
mapTree f tree =
    case tree of
        Empty ->
            Empty

        Node value left right ->
            Node (f value) (mapTree f left) (mapTree f right)
```

**After (F#):**
```fsharp
type Tree<'a> =
    | Empty
    | Node of 'a * Tree<'a> * Tree<'a>

let rec depth (tree: Tree<'a>) : int =
    match tree with
    | Empty ->
        0

    | Node (_, left, right) ->
        1 + max (depth left) (depth right)

let rec mapTree (f: 'a -> 'b) (tree: Tree<'a>) : Tree<'b> =
    match tree with
    | Empty ->
        Empty

    | Node (value, left, right) ->
        Node (f value, mapTree f left, mapTree f right)
```

### Example 3: Complex - The Elm Architecture with HTTP

**Before (Elm):**
```elm
module Main exposing (main)

import Browser
import Html exposing (..)
import Html.Events exposing (onClick)
import Http
import Json.Decode as Decode

type alias Model =
    { users : List User
    , loading : Bool
    , error : Maybe String
    }

type alias User =
    { id : Int
    , name : String
    }

type Msg
    = LoadUsers
    | GotUsers (Result Http.Error (List User))

init : () -> ( Model, Cmd Msg )
init _ =
    ( { users = [], loading = False, error = Nothing }
    , Cmd.none
    )

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        LoadUsers ->
            ( { model | loading = True, error = Nothing }
            , fetchUsers
            )

        GotUsers (Ok users) ->
            ( { model | users = users, loading = False }
            , Cmd.none
            )

        GotUsers (Err error) ->
            ( { model | loading = False, error = Just (errorToString error) }
            , Cmd.none
            )

view : Model -> Html Msg
view model =
    div []
        [ button [ onClick LoadUsers ] [ text "Load Users" ]
        , if model.loading then
            text "Loading..."
          else
            div []
                [ viewError model.error
                , viewUsers model.users
                ]
        ]

viewError : Maybe String -> Html Msg
viewError error =
    case error of
        Just err ->
            div [] [ text ("Error: " ++ err) ]

        Nothing ->
            text ""

viewUsers : List User -> Html Msg
viewUsers users =
    ul [] (List.map viewUser users)

viewUser : User -> Html Msg
viewUser user =
    li [] [ text user.name ]

fetchUsers : Cmd Msg
fetchUsers =
    Http.get
        { url = "https://api.example.com/users"
        , expect = Http.expectJson GotUsers usersDecoder
        }

usersDecoder : Decode.Decoder (List User)
usersDecoder =
    Decode.list userDecoder

userDecoder : Decode.Decoder User
userDecoder =
    Decode.map2 User
        (Decode.field "id" Decode.int)
        (Decode.field "name" Decode.string)

errorToString : Http.Error -> String
errorToString error =
    case error of
        Http.BadUrl url ->
            "Bad URL: " ++ url

        Http.Timeout ->
            "Timeout"

        Http.NetworkError ->
            "Network error"

        Http.BadStatus code ->
            "Bad status: " ++ String.fromInt code

        Http.BadBody message ->
            "Bad body: " ++ message

main =
    Browser.element
        { init = init
        , update = update
        , view = view
        , subscriptions = \_ -> Sub.none
        }
```

**After (F#):**
```fsharp
module Main

open Elmish
open Elmish.React
open Fable.React
open Fable.React.Props
open Thoth.Json.Decode
open Fable.SimpleHttp

type Model = {
    Users: User list
    Loading: bool
    Error: string option
}

type User = {
    Id: int
    Name: string
}

type Msg =
    | LoadUsers
    | GotUsers of Result<User list, string>

let init () : Model * Cmd<Msg> =
    { Users = []; Loading = false; Error = None }, Cmd.none

let update (msg: Msg) (model: Model) : Model * Cmd<Msg> =
    match msg with
    | LoadUsers ->
        { model with Loading = true; Error = None }, fetchUsers ()

    | GotUsers (Ok users) ->
        { model with Users = users; Loading = false }, Cmd.none

    | GotUsers (Error error) ->
        { model with Loading = false; Error = Some error }, Cmd.none

let view (model: Model) (dispatch: Msg -> unit) =
    div [] [
        button [ OnClick (fun _ -> dispatch LoadUsers) ] [ str "Load Users" ]
        if model.Loading then
            str "Loading..."
        else
            div [] [
                viewError model.Error
                viewUsers model.Users
            ]
    ]

let viewError (error: string option) =
    match error with
    | Some err ->
        div [] [ str ("Error: " + err) ]
    | None ->
        str ""

let viewUsers (users: User list) =
    ul [] (users |> List.map viewUser)

let viewUser (user: User) =
    li [] [ str user.Name ]

let fetchUsers () : Cmd<Msg> =
    Cmd.OfAsync.perform
        (fun () -> async {
            let! response = Http.get "https://api.example.com/users"
            match response.statusCode with
            | 200 ->
                match Decode.fromString usersDecoder response.responseText with
                | Ok users -> return Ok users
                | Error err -> return Error err
            | code ->
                return Error $"Bad status: {code}"
        })
        ()
        GotUsers
        (fun ex -> GotUsers (Error ex.Message))

let userDecoder : Decoder<User> =
    Decode.object (fun get -> {
        Id = get.Required.Field "id" Decode.int
        Name = get.Required.Field "name" Decode.string
    })

let usersDecoder : Decoder<User list> =
    Decode.list userDecoder

Program.mkProgram init update view
|> Program.withReactSynchronous "root"
|> Program.run
```

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational conversion patterns with cross-language examples
- `lang-elm-dev` - Elm development patterns and The Elm Architecture
- `lang-fsharp-dev` - F# development patterns and functional programming
- `patterns-concurrency-dev` - Async patterns across languages
- `patterns-serialization-dev` - JSON handling across languages
