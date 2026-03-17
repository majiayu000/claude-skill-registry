---
name: convert-fsharp-elm
description: Convert F# code to idiomatic Elm. Use when migrating F# projects to Elm, translating backend F# to frontend Elm, refactoring .NET backends with Elm frontends, or exploring functional patterns across backend and frontend domains. Extends meta-convert-dev with F#-to-Elm specific patterns.
---

# Convert F# to Elm

Convert F# code to idiomatic Elm for type-safe frontend applications. This skill extends `meta-convert-dev` with F#-to-Elm specific type mappings, idiom translations, and patterns for translating backend functional code to frontend functional code.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: F# types → Elm types (including discriminated unions)
- **Idiom translations**: F# patterns → idiomatic Elm (Railway-Oriented Programming, computation expressions → TEA)
- **Error handling**: F# Result → Elm Result (similar but frontend-focused)
- **Async patterns**: F# async workflows → Elm Cmd/Task
- **Architecture translation**: Backend F# → Frontend Elm Architecture (TEA)
- **Platform differences**: .NET/CLR → Browser/JavaScript runtime

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- F# language fundamentals - see `lang-fsharp-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Reverse conversion (Elm → F#) - see `convert-elm-fsharp`
- Fable-specific patterns (F#-to-JavaScript transpilation)

---

## Quick Reference

| F# | Elm | Notes |
|-----|------|-------|
| `string` | `String` | Direct mapping |
| `int` | `Int` | Elm Int is limited precision (JavaScript) |
| `float` | `Float` | Direct mapping |
| `bool` | `Bool` | Direct mapping |
| `'a list` | `List a` | Immutable linked list |
| `'a[]` | `Array a` | Different performance characteristics |
| `'a option` | `Maybe a` | Nearly identical semantics |
| `Result<'T,'E>` | `Result error value` | Order reversed in Elm |
| `Async<'T>` | `Cmd Msg` / `Task error value` | Different execution model |
| `type X = A \| B` | `type X = A \| B` | Discriminated unions map directly |
| `{ Name: string }` | `{ name : String }` | Records (camelCase in Elm) |
| `Map<'K,'V>` | `Dict comparable v` | Key must be comparable |
| `Set<'T>` | `Set comparable` | Value must be comparable |
| `unit` | `()` | Unit type |

## When Converting Code

1. **Analyze source thoroughly** before writing target
2. **Map types first** - create type equivalence table
3. **Identify architectural shift** - Backend async → Frontend TEA
4. **Preserve semantics** over syntax similarity
5. **Adopt Elm idioms** - don't write "F# code in Elm syntax"
6. **Handle platform differences** - .NET runtime → Browser
7. **No side effects in views** - Pure functions only
8. **Test equivalence** - same inputs → same outputs

---

## Type System Mapping

### Primitive Types

| F# | Elm | Notes |
|-----|------|-------|
| `string` | `String` | UTF-16 (F#) vs UTF-8-ish (Elm/JS) |
| `int` | `Int` | F# int is 32-bit, Elm Int is JavaScript number (53-bit precision) |
| `int64` | `Int` | Loss of precision possible in Elm |
| `float` / `double` | `Float` | IEEE 754 double precision (both) |
| `bool` | `Bool` | Direct mapping |
| `char` | `Char` | Similar but Elm Char is a single UTF-16 code unit |
| `byte` | `Int` | No dedicated byte type in Elm |
| `unit` | `()` | Unit type, represents "no value" |
| `decimal` | - | No decimal type in Elm; use Int for cents or Float |
| `bigint` | - | No arbitrary precision integers in Elm |

**Critical Note on Numbers**: F# has precise integer types (int32, int64, bigint) and decimal. Elm's Int is JavaScript's number (53-bit safe integer range). For currency, use Int representing cents/pence.

### Collection Types

| F# | Elm | Notes |
|-----|------|-------|
| `'a list` | `List a` | Immutable linked list (same performance characteristics) |
| `'a[]` | `Array a` | Elm Array is tree-based, not native array |
| `'a seq` | - | No lazy sequences in Elm; use List |
| `Map<'K,'V>` | `Dict comparable v` | Key type must be `comparable` (Int, Float, Char, String, tuples/lists of comparable) |
| `Set<'T>` | `Set comparable` | Value must be `comparable` |
| `ResizeArray<'T>` | `Array a` | Mutable .NET List → Immutable Elm Array |
| `('a * 'b)` | `( a, b )` | Tuple (same syntax!) |
| `('a * 'b * 'c)` | `( a, b, c )` | 3-tuple (Elm supports up to 3-tuple) |

### Option and Result Types

| F# | Elm | Notes |
|-----|------|-------|
| `'a option` | `Maybe a` | Nearly identical |
| `Some value` | `Just value` | Constructor name differs |
| `None` | `Nothing` | Constructor name differs |
| `Result<'T,'E>` | `Result error value` | **Order reversed**: Elm puts error first |
| `Ok value` | `Ok value` | Same constructor |
| `Error err` | `Err err` | Constructor name differs (Err vs Error) |

**Important:** F# Result is `Result<Success, Error>` but Elm Result is `Result error value` (error first, value second in type signature).

### Discriminated Unions

| F# | Elm | Notes |
|-----|------|-------|
| `type X = A \| B` | `type X = A \| B` | Syntax nearly identical! |
| `type X = A of int` | `type X = A Int` | No `of` keyword in Elm |
| `type X = A of x:int * y:int` | `type X = A Int Int` or use record | Named fields require records in Elm |

```fsharp
// F#
type Shape =
    | Circle of radius: float
    | Rectangle of width: float * height: float
```

```elm
-- Elm (unnamed fields)
type Shape
    = Circle Float
    | Rectangle Float Float

-- Elm (named fields with record)
type Shape
    = Circle { radius : Float }
    | Rectangle { width : Float, height : Float }
```

### Record Types

| F# | Elm | Notes |
|-----|------|-------|
| `{ Name: string }` | `{ name : String }` | Convention: PascalCase (F#) vs camelCase (Elm) |
| `{ person with Age = 31 }` | `{ person \| age = 31 }` | Copy-and-update syntax differs |
| `type alias Person = { ... }` | `type alias Person = { ... }` | Type alias syntax identical |

```fsharp
// F#
type Person = {
    FirstName: string
    LastName: string
    Age: int
}

let person = { FirstName = "Alice"; LastName = "Smith"; Age = 30 }
let older = { person with Age = 31 }
```

```elm
-- Elm
type alias Person =
    { firstName : String
    , lastName : String
    , age : Int
    }

person : Person
person =
    { firstName = "Alice"
    , lastName = "Smith"
    , age = 30
    }

older : Person
older =
    { person | age = 31 }
```

### Function Types

| F# | Elm | Notes |
|-----|------|-------|
| `'a -> 'b` | `a -> b` | Function type (same concept) |
| `'a -> 'b -> 'c` | `a -> b -> c` | Curried function |
| `('a * 'b) -> 'c` | `( a, b ) -> c` | Tuple parameter |
| `unit -> 'a` | `() -> a` | No-argument function |

---

## Idiom Translation

### Pattern 1: Option/Maybe Handling

**F#:**
```fsharp
let findUser id =
    if id = 1 then
        Some { Name = "Alice"; Age = 30 }
    else
        None

// Using option combinators
let displayName user =
    user
    |> Option.map (fun u -> u.Name)
    |> Option.defaultValue "Anonymous"

// Pattern matching
match findUser 1 with
| Some user -> printfn "Found: %s" user.Name
| None -> printfn "Not found"
```

**Elm:**
```elm
findUser : Int -> Maybe User
findUser id =
    if id == 1 then
        Just { name = "Alice", age = 30 }
    else
        Nothing

-- Using Maybe helpers
displayName : Maybe User -> String
displayName user =
    user
        |> Maybe.map .name
        |> Maybe.withDefault "Anonymous"

-- Pattern matching
case findUser 1 of
    Just user ->
        "Found: " ++ user.name
    Nothing ->
        "Not found"
```

**Why this translation:**
- `Some` → `Just` (constructor name)
- `None` → `Nothing` (constructor name)
- `Option.defaultValue` → `Maybe.withDefault`
- Pattern matching syntax differs (`match x with` vs `case x of`)
- Elm uses `==` for equality (not `=`)

### Pattern 2: Result Type (Railway-Oriented Programming)

**F#:**
```fsharp
type ValidationError = string

let validateEmail email =
    if email.Contains("@") then
        Ok email
    else
        Error "Invalid email"

let validateAge age =
    if age >= 0 && age <= 120 then
        Ok age
    else
        Error "Invalid age"

// Using result computation expression
let createUser email age =
    result {
        let! validEmail = validateEmail email
        let! validAge = validateAge age
        return { Email = validEmail; Age = validAge }
    }
```

**Elm:**
```elm
type alias ValidationError =
    String

validateEmail : String -> Result ValidationError String
validateEmail email =
    if String.contains "@" email then
        Ok email
    else
        Err "Invalid email"

validateAge : Int -> Result ValidationError Int
validateAge age =
    if age >= 0 && age <= 120 then
        Ok age
    else
        Err "Invalid age"

-- Chaining with Result.andThen (no computation expression in Elm)
createUser : String -> Int -> Result ValidationError User
createUser email age =
    validateEmail email
        |> Result.andThen (\validEmail ->
            validateAge age
                |> Result.map (\validAge ->
                    { email = validEmail, age = validAge }
                )
        )

-- Alternative: Using Result.map2
createUser : String -> Int -> Result ValidationError User
createUser email age =
    Result.map2 User
        (validateEmail email)
        (validateAge age)
```

**Why this translation:**
- `Error` → `Err` (constructor name)
- F# has computation expressions (`result { ... }`), Elm uses `Result.andThen` and `Result.map`
- `Result.map2` for combining two Results is more idiomatic in Elm
- Type order: F# `Result<'T,'E>` vs Elm `Result error value`

### Pattern 3: List Operations

**F#:**
```fsharp
let numbers = [1; 2; 3; 4; 5]

// Map, filter, fold
let doubled = numbers |> List.map (fun x -> x * 2)
let evens = numbers |> List.filter (fun x -> x % 2 = 0)
let sum = numbers |> List.fold (+) 0

// List comprehension
let squares = [ for x in 1..10 -> x * x ]

// Cons operator
let newList = 0 :: numbers
```

**Elm:**
```elm
numbers : List Int
numbers =
    [ 1, 2, 3, 4, 5 ]

-- Map, filter, fold
doubled : List Int
doubled =
    List.map (\x -> x * 2) numbers

evens : List Int
evens =
    List.filter (\x -> modBy 2 x == 0) numbers

sum : Int
sum =
    List.foldl (+) 0 numbers

-- List range
squares : List Int
squares =
    List.range 1 10
        |> List.map (\x -> x * x)

-- Cons operator (same!)
newList : List Int
newList =
    0 :: numbers
```

**Why this translation:**
- List syntax: F# uses `;` separator, Elm uses `,`
- `List.fold` → `List.foldl` (Elm also has `foldr`)
- F# has list comprehensions, Elm uses `List.range` + `List.map`
- `%` (modulo) → `modBy` function in Elm
- Cons operator `::` is the same in both!

### Pattern 4: Pattern Matching

**F#:**
```fsharp
type Shape =
    | Circle of radius: float
    | Rectangle of width: float * height: float

let area shape =
    match shape with
    | Circle radius -> 3.14 * radius * radius
    | Rectangle (width, height) -> width * height

// Guards
let classify n =
    match n with
    | x when x < 0 -> "negative"
    | 0 -> "zero"
    | _ -> "positive"
```

**Elm:**
```elm
type Shape
    = Circle Float
    | Rectangle Float Float

area : Shape -> Float
area shape =
    case shape of
        Circle radius ->
            3.14 * radius * radius
        Rectangle width height ->
            width * height

-- No guards in Elm - use if/else
classify : Int -> String
classify n =
    case n of
        0 ->
            "zero"
        _ ->
            if n < 0 then
                "negative"
            else
                "positive"
```

**Why this translation:**
- `match x with` → `case x of`
- F# allows guards (`when`), Elm requires `if/else` expressions
- Destructuring in `case` is similar but Elm doesn't use parentheses for tuple destructuring

### Pattern 5: Record Updates

**F#:**
```fsharp
type Person = {
    FirstName: string
    LastName: string
    Age: int
}

let person = { FirstName = "Alice"; LastName = "Smith"; Age = 30 }
let older = { person with Age = 31 }
let renamed = { person with FirstName = "Alicia"; LastName = "Jones" }
```

**Elm:**
```elm
type alias Person =
    { firstName : String
    , lastName : String
    , age : Int
    }

person : Person
person =
    { firstName = "Alice"
    , lastName = "Smith"
    , age = 30
    }

older : Person
older =
    { person | age = 31 }

renamed : Person
renamed =
    { person | firstName = "Alicia", lastName = "Jones" }
```

**Why this translation:**
- `{ record with Field = value }` → `{ record | field = value }`
- F# uses `with`, Elm uses `|`
- Multiple fields: F# uses `;`, Elm uses `,`

### Pattern 6: Pipe Operator

**F#:**
```fsharp
let result =
    someValue
    |> function1
    |> function2
    |> function3

// Forward composition
let composed = function1 >> function2 >> function3
```

**Elm:**
```elm
result : ResultType
result =
    someValue
        |> function1
        |> function2
        |> function3

-- Forward composition
composed : a -> d
composed =
    function1 >> function2 >> function3
```

**Why this translation:**
- Pipe operator `|>` is identical!
- Composition operator `>>` is identical!
- Elm style guide prefers indenting each pipe

### Pattern 7: Active Patterns → Custom Types with Helper Functions

**F#:**
```fsharp
let (|Even|Odd|) n =
    if n % 2 = 0 then Even else Odd

match 42 with
| Even -> "even"
| Odd -> "odd"

// Partial active pattern
let (|Integer|_|) (str: string) =
    match System.Int32.TryParse(str) with
    | true, value -> Some value
    | false, _ -> None

match "123" with
| Integer n -> sprintf "Number: %d" n
| _ -> "Not a number"
```

**Elm:**
```elm
-- No active patterns - use helper functions

type Parity
    = Even
    | Odd

parity : Int -> Parity
parity n =
    if modBy 2 n == 0 then
        Even
    else
        Odd

-- Usage
case parity 42 of
    Even ->
        "even"
    Odd ->
        "odd"

-- Partial pattern equivalent
parseInteger : String -> Maybe Int
parseInteger str =
    String.toInt str

-- Usage
case parseInteger "123" of
    Just n ->
        "Number: " ++ String.fromInt n
    Nothing ->
        "Not a number"
```

**Why this translation:**
- Elm doesn't have active patterns - define custom types + helper functions instead
- Helper function returns a discriminated union or Maybe
- More explicit but arguably clearer

---

## Paradigm Translation

### Mental Model Shift: Backend F# → Frontend Elm

| F# (Backend) Concept | Elm (Frontend) Approach | Key Insight |
|---------------------|------------------------|-------------|
| Async workflows for I/O | Cmd/Task for effects | All side effects go through Elm Runtime |
| Domain services/repositories | Model + update functions | State is centralized in Model |
| Mutable state (ref, ResizeArray) | Immutable Model updates | Always return new Model |
| Side effects anywhere | Pure functions + Cmd | View and update are pure; Cmd describes effects |
| OOP when interoping with C# | Only data structures (no classes) | Records and custom types only |
| Computation expressions | Chaining with Result.andThen, Maybe.andThen | No do-notation in Elm |

### The Elm Architecture vs F# Application Structure

**F# Backend Pattern:**
```fsharp
// Domain types
type User = { Id: int; Name: string; Email: string }

// Service with dependencies
type IUserRepository =
    abstract member GetUser: int -> Async<User option>
    abstract member SaveUser: User -> Async<unit>

// Service implementation
type UserService(repo: IUserRepository) =
    member _.GetUserById(id: int) =
        async {
            let! user = repo.GetUser(id)
            return user
        }
```

**Elm Frontend Pattern (TEA):**
```elm
-- MODEL
type alias Model =
    { user : Maybe User
    , loading : Bool
    , error : Maybe String
    }

-- MSG
type Msg
    = FetchUser Int
    | GotUser (Result Http.Error User)

-- UPDATE
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUser id ->
            ( { model | loading = True }
            , Http.get
                { url = "/api/users/" ++ String.fromInt id
                , expect = Http.expectJson GotUser userDecoder
                }
            )

        GotUser result ->
            case result of
                Ok user ->
                    ( { model | user = Just user, loading = False }, Cmd.none )

                Err error ->
                    ( { model | error = Just (httpErrorToString error), loading = False }, Cmd.none )

-- VIEW
view : Model -> Html Msg
view model =
    case model.user of
        Just user ->
            div [] [ text user.name ]
        Nothing ->
            if model.loading then
                div [] [ text "Loading..." ]
            else
                button [ onClick (FetchUser 1) ] [ text "Load User" ]
```

**Key Differences:**
- F# services manage state internally; Elm centralizes state in Model
- F# async workflows execute immediately; Elm Cmd is a description that the runtime executes
- F# patterns match imperative backends; Elm enforces unidirectional data flow

---

## Error Handling

### F# Result → Elm Result

Both languages have similar Result types, but with reversed type parameter order.

**F# Result:**
```fsharp
type Result<'T,'TError> =
    | Ok of ResultValue: 'T
    | Error of ErrorValue: 'TError
```

**Elm Result:**
```elm
type Result error value
    = Ok value
    | Err error
```

### Basic Error Translation

**F#:**
```fsharp
let divide x y =
    if y = 0.0 then
        Error "Division by zero"
    else
        Ok (x / y)

match divide 10.0 2.0 with
| Ok result -> printfn "Result: %f" result
| Error msg -> printfn "Error: %s" msg

// Using Result module
let doubled =
    divide 10.0 2.0
    |> Result.map (fun x -> x * 2.0)
```

**Elm:**
```elm
divide : Float -> Float -> Result String Float
divide x y =
    if y == 0.0 then
        Err "Division by zero"
    else
        Ok (x / y)

case divide 10.0 2.0 of
    Ok result ->
        "Result: " ++ String.fromFloat result
    Err msg ->
        "Error: " ++ msg

-- Using Result module
doubled : Result String Float
doubled =
    divide 10.0 2.0
        |> Result.map (\x -> x * 2.0)
```

**Why this translation:**
- `Error` → `Err` (constructor name)
- Type parameter order reversed
- `Result.map`, `Result.andThen`, `Result.withDefault` exist in both

### Railway-Oriented Programming (Same Pattern!)

Both F# and Elm use Railway-Oriented Programming effectively.

**F#:**
```fsharp
let validateEmail email =
    if email.Contains("@") then Ok email
    else Error "Invalid email"

let validateAge age =
    if age >= 0 && age <= 120 then Ok age
    else Error "Invalid age"

let createUser email age =
    result {
        let! validEmail = validateEmail email
        let! validAge = validateAge age
        return { Email = validEmail; Age = validAge }
    }
```

**Elm:**
```elm
validateEmail : String -> Result String String
validateEmail email =
    if String.contains "@" email then
        Ok email
    else
        Err "Invalid email"

validateAge : Int -> Result String Int
validateAge age =
    if age >= 0 && age <= 120 then
        Ok age
    else
        Err "Invalid age"

createUser : String -> Int -> Result String User
createUser email age =
    Result.map2 User
        (validateEmail email)
        (validateAge age)
```

**Why this translation:**
- F# has computation expressions for cleaner chaining
- Elm uses `Result.map2` for combining two Results
- Both achieve same goal: composable error handling

---

## Async Patterns

### F# Async → Elm Cmd/Task

F# async workflows and Elm's Cmd/Task serve similar purposes but have different execution models.

| F# | Elm | Conceptual Translation |
|-----|------|----------------------|
| `Async<'T>` | `Task error value` | Description of async operation |
| `async { ... }` | `Task.andThen`, `Task.map` | Chaining async operations |
| `Async.RunSynchronously` | Runtime executes Cmd | Runtime handles execution |
| `let!` binding | `Task.andThen` | Sequential composition |
| `Async.Parallel` | `Task.sequence` + Cmd.batch | Parallel operations |

### Basic Async Translation

**F#:**
```fsharp
let fetchUser id = async {
    // Simulated async operation
    do! Async.Sleep 1000
    return { Id = id; Name = "Alice"; Email = "alice@example.com" }
}

let processUser id = async {
    let! user = fetchUser id
    printfn "Got user: %s" user.Name
    return user.Name
}

// Run async
Async.RunSynchronously (processUser 1)
```

**Elm:**
```elm
-- In Elm, HTTP requests return Cmd, not Task
type Msg
    = GotUser (Result Http.Error User)

fetchUser : Int -> Cmd Msg
fetchUser id =
    Http.get
        { url = "/api/users/" ++ String.fromInt id
        , expect = Http.expectJson GotUser userDecoder
        }

-- Update handles the result
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        LoadUser id ->
            ( { model | loading = True }, fetchUser id )

        GotUser result ->
            case result of
                Ok user ->
                    ( { model | user = Just user, loading = False }, Cmd.none )
                Err _ ->
                    ( { model | error = Just "Failed to load user", loading = False }, Cmd.none )
```

**Why this translation:**
- F# async workflows are imperative; Elm Cmd is declarative
- F# `let!` binds result; Elm runtime sends result as Msg to update
- No `RunSynchronously` in Elm - runtime manages execution
- Elm enforces separation: update returns (Model, Cmd), doesn't execute effects

### Task for Sequential Operations

**F#:**
```fsharp
let workflow = async {
    let! user = fetchUser 1
    let! orders = fetchOrders user.Id
    let! details = fetchOrderDetails orders.[0].Id
    return details
}
```

**Elm:**
```elm
-- Using Task for sequential composition
import Http
import Task exposing (Task)

workflow : Task Http.Error OrderDetails
workflow =
    fetchUser 1
        |> Task.andThen (\user ->
            fetchOrders user.id
        )
        |> Task.andThen (\orders ->
            case List.head orders of
                Just firstOrder ->
                    fetchOrderDetails firstOrder.id
                Nothing ->
                    Task.fail (Http.BadBody "No orders")
        )

-- Convert Task to Cmd to execute
type Msg
    = GotDetails (Result Http.Error OrderDetails)

executeWorkflow : Cmd Msg
executeWorkflow =
    Task.attempt GotDetails workflow
```

**Why this translation:**
- F# computation expression syntax vs Elm explicit chaining
- Elm requires converting Task → Cmd via `Task.attempt`
- Task describes the workflow; Cmd triggers execution via runtime

### Parallel Operations

**F#:**
```fsharp
let fetchBoth = async {
    let! results =
        [ fetchUser 1; fetchUser 2; fetchUser 3 ]
        |> Async.Parallel
    return results
}
```

**Elm:**
```elm
type Msg
    = GotAllUsers (List (Result Http.Error User))

fetchBoth : Cmd Msg
fetchBoth =
    Cmd.batch
        [ fetchUser 1 |> Cmd.map (GotUser 1)
        , fetchUser 2 |> Cmd.map (GotUser 2)
        , fetchUser 3 |> Cmd.map (GotUser 3)
        ]

-- Or using Task
fetchBothTask : Task Http.Error (List User)
fetchBothTask =
    Task.sequence
        [ fetchUserTask 1
        , fetchUserTask 2
        , fetchUserTask 3
        ]
        |> Task.attempt GotAllUsers
```

**Why this translation:**
- F# `Async.Parallel` executes and waits for all
- Elm `Cmd.batch` sends multiple commands; each result comes back separately
- Elm `Task.sequence` waits for all tasks but requires different Msg handling

---

## Common Pitfalls

### 1. Assuming F# Computation Expressions Exist in Elm

**Problem:** Trying to use `result { ... }` or `option { ... }` syntax.

```elm
-- ✗ Doesn't exist in Elm
createUser : String -> Int -> Result String User
createUser email age =
    result {  -- Error: No such thing
        let! validEmail = validateEmail email
        let! validAge = validateAge age
        return { email = validEmail, age = validAge }
    }
```

**Fix:** Use `Result.map2`, `Result.andThen`, or explicit case expressions.

```elm
-- ✓ Use Result.map2
createUser : String -> Int -> Result String User
createUser email age =
    Result.map2 User
        (validateEmail email)
        (validateAge age)

-- ✓ Or Result.andThen
createUser : String -> Int -> Result String User
createUser email age =
    validateEmail email
        |> Result.andThen (\validEmail ->
            validateAge age
                |> Result.map (\validAge ->
                    { email = validEmail, age = validAge }
                )
        )
```

### 2. Trying to Execute Side Effects Directly

**Problem:** Coming from F# where you can run `Async.RunSynchronously` or use `printfn` anywhere.

```elm
-- ✗ Can't execute effects in Elm
view : Model -> Html Msg
view model =
    let
        _ = Debug.log "Rendering model" model  -- This logs, but shouldn't be in production
        user = Http.get { ... }  -- Error: Http.get returns Cmd, can't execute here
    in
    div [] [ text model.name ]
```

**Fix:** All effects go through Cmd, returned from update.

```elm
-- ✓ Effects only in update
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUser id ->
            ( { model | loading = True }
            , Http.get
                { url = "/api/users/" ++ String.fromInt id
                , expect = Http.expectJson GotUser userDecoder
                }
            )
```

### 3. F# Mutable State Patterns

**Problem:** Trying to use mutable references or modify collections in place.

```elm
-- ✗ No mutable state in Elm
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    model.users <- List.append model.users [ newUser ]  -- Error: Can't mutate
    ( model, Cmd.none )
```

**Fix:** Always return new state.

```elm
-- ✓ Immutable updates
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    ( { model | users = model.users ++ [ newUser ] }, Cmd.none )
```

### 4. Discriminated Union Named Fields

**Problem:** Using F# named field syntax in discriminated unions.

```fsharp
// F#
type Shape =
    | Circle of radius: float
    | Rectangle of width: float * height: float

let shape = Circle (radius = 5.0)
```

```elm
-- ✗ No named fields in Elm union constructors
type Shape
    = Circle { radius : Float }  -- This is a record inside, not named field
    | Rectangle { width : Float, height : Float }

-- ✗ Can't use named syntax
shape = Circle { radius = 5.0 }  -- This works, but it's a record
```

**Fix:** Use positional fields or records.

```elm
-- ✓ Positional fields
type Shape
    = Circle Float
    | Rectangle Float Float

shape : Shape
shape =
    Circle 5.0

-- ✓ Or use records for clarity
type Shape
    = Circle { radius : Float }
    | Rectangle { width : Float, height : Float }

shape : Shape
shape =
    Circle { radius = 5.0 }
```

### 5. Type Parameter Order in Result

**Problem:** Mixing up the order of error and value in Result.

```fsharp
// F#: Result<'T, 'TError> - Success first, Error second
let result: Result<int, string> = Ok 42
```

```elm
-- ✗ Wrong order (F# order)
result : Result Int String  -- Error first, not second!
result =
    Ok 42

-- ✓ Correct order
result : Result String Int  -- Error first, value second
result =
    Ok 42
```

### 6. Trying to Use F# Operators

**Problem:** Using F# operators that don't exist in Elm.

```fsharp
// F#
let compose = function1 >> function2  -- Forward composition
let pipe = value |> function1  -- Pipe
let result = if x > 0 && y < 10 then ...  -- Logical AND
```

```elm
-- ✓ Most F# operators work, but some differ
compose = function1 >> function2  -- ✓ Same
pipe = value |> function1  -- ✓ Same
result = if x > 0 && y < 10 then ...  -- ✓ Same

-- ✗ Some don't exist
modulo = x % y  -- Error: Use modBy function instead
remainder = x % y  -- Error: Use remainderBy function
```

**Fix:** Learn Elm equivalents.

```elm
-- ✓ Elm functions instead of operators
modulo = modBy y x  -- Note: arguments reversed!
remainder = remainderBy y x
```

### 7. Expecting Units of Measure

**Problem:** F# has units of measure; Elm doesn't.

```fsharp
// F#
[<Measure>] type kg
[<Measure>] type m

let distance = 100.0<m>
let mass = 50.0<kg>
// let invalid = distance + mass  // Compile error!
```

```elm
-- ✗ No units of measure in Elm
type Meter = Meter Float
type Kilogram = Kilogram Float

distance = Meter 100.0
mass = Kilogram 50.0
-- Can accidentally add these, no compile error
```

**Fix:** Use opaque types for type safety, but no compile-time unit checking.

```elm
-- ✓ Opaque types for safety (runtime, not compile-time)
type Meter = Meter Float
type Kilogram = Kilogram Float

-- Must unwrap to do math
addMeters : Meter -> Meter -> Meter
addMeters (Meter a) (Meter b) =
    Meter (a + b)
```

### 8. Module Naming Conflicts

**Problem:** F# allows nested modules; Elm uses file-based modules.

```fsharp
// F#
module MyApp.Domain.User

type User = { Name: string }
```

```elm
-- ✗ Can't have nested modules like this
module MyApp.Domain.User exposing (..)  -- Error: Only one level

-- ✓ Use file path to represent hierarchy
-- File: src/MyApp/Domain/User.elm
module MyApp.Domain.User exposing (User)

type alias User =
    { name : String }
```

---

## Tooling

### Development Workflow Comparison

| Stage | F# | Elm | Notes |
|-------|-----|------|-------|
| Package Manager | NuGet, Paket | elm install | Elm has much smaller package ecosystem |
| Build Tool | dotnet CLI, FAKE | elm make | Elm compiler is fast, no incremental builds needed |
| REPL | F# Interactive (fsi) | elm repl | Both have REPLs for experimentation |
| Formatting | Fantomas | elm-format | elm-format is built-in, automatic |
| Linting | FSharpLint | elm-review | elm-review is more structural analysis |
| Testing | Expecto, xUnit, FsCheck | elm-test, elm-explorations/test | Elm has built-in fuzz testing |
| IDE Support | VS Code, Rider, VS | VS Code with elm extension | Both have good VS Code support |

### Common Package Equivalents

| F# Package | Elm Package | Notes |
|------------|-------------|-------|
| `FSharp.Data` | `elm/json`, `elm/http` | JSON and HTTP |
| `Newtonsoft.Json` | `elm/json` | JSON serialization |
| `FsCheck` | `elm-explorations/test` (fuzz) | Property-based testing |
| `Expecto` | `elm-explorations/test` | Unit testing |
| `Hopac` / `Ply` | - | No direct equivalent (Elm runtime handles async) |
| `Suave` / `Giraffe` | - | Elm is frontend-only |

### Elm-Specific Tools

```bash
# Initialize new Elm project
elm init

# Install package
elm install elm/http

# Build
elm make src/Main.elm

# Build optimized for production
elm make src/Main.elm --optimize --output=main.js

# Start dev server (live reload)
elm reactor

# Run tests
elm-test

# Format code (automatic, always same style)
elm-format src/ --yes

# Static analysis
elm-review
```

---

## Examples

### Example 1: Simple - Option/Maybe Pattern

**Before (F#):**
```fsharp
type User = {
    Name: string
    Email: string
}

let findUser (id: int) : User option =
    if id = 1 then
        Some { Name = "Alice"; Email = "alice@example.com" }
    else
        None

let displayName (maybeUser: User option) : string =
    match maybeUser with
    | Some user -> user.Name
    | None -> "Anonymous"

// Using option helpers
let name =
    findUser 1
    |> Option.map (fun u -> u.Name)
    |> Option.defaultValue "Anonymous"
```

**After (Elm):**
```elm
type alias User =
    { name : String
    , email : String
    }

findUser : Int -> Maybe User
findUser id =
    if id == 1 then
        Just { name = "Alice", email = "alice@example.com" }
    else
        Nothing

displayName : Maybe User -> String
displayName maybeUser =
    case maybeUser of
        Just user ->
            user.name
        Nothing ->
            "Anonymous"

-- Using Maybe helpers
name : String
name =
    findUser 1
        |> Maybe.map .name
        |> Maybe.withDefault "Anonymous"
```

### Example 2: Medium - Result-Based Validation

**Before (F#):**
```fsharp
type ValidationError = string

type UserForm = {
    Email: string
    Age: string
}

let validateEmail email =
    if email.Contains("@") then
        Ok email
    else
        Error "Invalid email format"

let validateAge ageStr =
    match System.Int32.TryParse(ageStr) with
    | true, age when age >= 0 && age <= 120 ->
        Ok age
    | _ ->
        Error "Age must be between 0 and 120"

let validateUser (form: UserForm) =
    result {
        let! email = validateEmail form.Email
        let! age = validateAge form.Age
        return { Email = email; Age = age }
    }

// Usage
match validateUser { Email = "test@example.com"; Age = "30" } with
| Ok user -> printfn "Valid: %s" user.Email
| Error msg -> printfn "Error: %s" msg
```

**After (Elm):**
```elm
type alias ValidationError =
    String

type alias UserForm =
    { email : String
    , age : String
    }

type alias ValidatedUser =
    { email : String
    , age : Int
    }

validateEmail : String -> Result ValidationError String
validateEmail email =
    if String.contains "@" email then
        Ok email
    else
        Err "Invalid email format"

validateAge : String -> Result ValidationError Int
validateAge ageStr =
    case String.toInt ageStr of
        Just age ->
            if age >= 0 && age <= 120 then
                Ok age
            else
                Err "Age must be between 0 and 120"
        Nothing ->
            Err "Age must be a number"

validateUser : UserForm -> Result ValidationError ValidatedUser
validateUser form =
    Result.map2 ValidatedUser
        (validateEmail form.email)
        (validateAge form.age)

-- Usage in update function
type Msg
    = SubmitForm
    | ValidationResult (Result ValidationError ValidatedUser)

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        SubmitForm ->
            case validateUser model.form of
                Ok validUser ->
                    ( { model | user = Just validUser }, Cmd.none )
                Err error ->
                    ( { model | error = Just error }, Cmd.none )
```

### Example 3: Complex - Full TEA Application with HTTP

**Before (F# Backend API Handler):**
```fsharp
open System
open Suave
open Suave.Filters
open Suave.Operators
open Suave.Successful

type User = {
    Id: int
    Name: string
    Email: string
}

type CreateUserRequest = {
    Name: string
    Email: string
}

type UserService() =
    let mutable users = [
        { Id = 1; Name = "Alice"; Email = "alice@example.com" }
    ]

    member _.GetAll() = async {
        return users
    }

    member _.Create(req: CreateUserRequest) = async {
        let newId = (users |> List.map (fun u -> u.Id) |> List.max) + 1
        let newUser = { Id = newId; Name = req.Name; Email = req.Email }
        users <- users @ [newUser]
        return newUser
    }

let userService = UserService()

let getUsers = async {
    let! users = userService.GetAll()
    return OK (Newtonsoft.Json.JsonConvert.SerializeObject(users))
}

let createUser req = async {
    let! user = userService.Create(req)
    return OK (Newtonsoft.Json.JsonConvert.SerializeObject(user))
}

let app =
    choose [
        GET >=> path "/api/users" >=> request (fun _ -> getUsers)
        POST >=> path "/api/users" >=> request (fun r -> createUser r)
    ]
```

**After (Elm Frontend Application):**
```elm
module Main exposing (main)

import Browser
import Html exposing (Html, button, div, input, text, ul, li)
import Html.Attributes exposing (placeholder, value)
import Html.Events exposing (onClick, onInput)
import Http
import Json.Decode as Decode exposing (Decoder)
import Json.Encode as Encode

-- MODEL

type alias User =
    { id : Int
    , name : String
    , email : String
    }

type alias CreateUserForm =
    { name : String
    , email : String
    }

type alias Model =
    { users : List User
    , form : CreateUserForm
    , loading : Bool
    , error : Maybe String
    }

init : () -> ( Model, Cmd Msg )
init _ =
    ( { users = []
      , form = { name = "", email = "" }
      , loading = False
      , error = Nothing
      }
    , fetchUsers
    )

-- UPDATE

type Msg
    = FetchUsers
    | GotUsers (Result Http.Error (List User))
    | SetName String
    | SetEmail String
    | CreateUser
    | CreatedUser (Result Http.Error User)

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUsers ->
            ( { model | loading = True }, fetchUsers )

        GotUsers result ->
            case result of
                Ok users ->
                    ( { model | users = users, loading = False, error = Nothing }, Cmd.none )

                Err error ->
                    ( { model | loading = False, error = Just (httpErrorToString error) }, Cmd.none )

        SetName name ->
            let
                form =
                    model.form
            in
            ( { model | form = { form | name = name } }, Cmd.none )

        SetEmail email ->
            let
                form =
                    model.form
            in
            ( { model | form = { form | email = email } }, Cmd.none )

        CreateUser ->
            ( { model | loading = True }, createUser model.form )

        CreatedUser result ->
            case result of
                Ok user ->
                    ( { model
                        | users = model.users ++ [ user ]
                        , form = { name = "", email = "" }
                        , loading = False
                        , error = Nothing
                      }
                    , Cmd.none
                    )

                Err error ->
                    ( { model | loading = False, error = Just (httpErrorToString error) }, Cmd.none )

-- VIEW

view : Model -> Html Msg
view model =
    div []
        [ div []
            [ input [ placeholder "Name", value model.form.name, onInput SetName ] []
            , input [ placeholder "Email", value model.form.email, onInput SetEmail ] []
            , button [ onClick CreateUser ] [ text "Create User" ]
            ]
        , case model.error of
            Just error ->
                div [] [ text ("Error: " ++ error) ]

            Nothing ->
                text ""
        , if model.loading then
            div [] [ text "Loading..." ]

          else
            ul []
                (List.map viewUser model.users)
        ]

viewUser : User -> Html msg
viewUser user =
    li [] [ text (user.name ++ " (" ++ user.email ++ ")") ]

-- HTTP

fetchUsers : Cmd Msg
fetchUsers =
    Http.get
        { url = "/api/users"
        , expect = Http.expectJson GotUsers (Decode.list userDecoder)
        }

createUser : CreateUserForm -> Cmd Msg
createUser form =
    Http.post
        { url = "/api/users"
        , body = Http.jsonBody (encodeCreateUserForm form)
        , expect = Http.expectJson CreatedUser userDecoder
        }

-- DECODERS

userDecoder : Decoder User
userDecoder =
    Decode.map3 User
        (Decode.field "id" Decode.int)
        (Decode.field "name" Decode.string)
        (Decode.field "email" Decode.string)

-- ENCODERS

encodeCreateUserForm : CreateUserForm -> Encode.Value
encodeCreateUserForm form =
    Encode.object
        [ ( "name", Encode.string form.name )
        , ( "email", Encode.string form.email )
        ]

-- HELPERS

httpErrorToString : Http.Error -> String
httpErrorToString error =
    case error of
        Http.BadUrl url ->
            "Bad URL: " ++ url

        Http.Timeout ->
            "Request timed out"

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

**Key Translation Points:**
- F# backend service with mutable state → Elm Model with immutable state
- F# async workflows → Elm Cmd for HTTP requests
- F# pattern matching on request types → Elm Msg types with pattern matching
- F# JSON serialization → Elm JSON encoders/decoders
- Backend imperative handlers → Frontend declarative TEA (Model-View-Update)

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `lang-fsharp-dev` - F# development patterns
- `lang-elm-dev` - Elm development patterns
- `patterns-serialization-dev` - JSON handling across languages
- `patterns-concurrency-dev` - Async patterns across languages
