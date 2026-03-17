---
name: convert-erlang-elm
description: Convert Erlang code to idiomatic Elm. Use when migrating Erlang backend logic to Elm frontend applications, translating BEAM VM patterns to functional frontend code, or refactoring distributed systems to type-safe UIs. Extends meta-convert-dev with Erlang-to-Elm specific patterns.
---

# Convert Erlang to Elm

Convert Erlang code to idiomatic Elm. This skill extends `meta-convert-dev` with Erlang-to-Elm specific type mappings, idiom translations, and architectural patterns for moving from distributed backend systems to type-safe frontend applications.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Erlang types → Elm types
- **Idiom translations**: Erlang patterns → idiomatic Elm
- **Architecture patterns**: OTP behaviors → The Elm Architecture (TEA)
- **Message passing**: Process mailboxes → Elm commands/subscriptions
- **Error handling**: let-it-crash → Maybe/Result types
- **Concurrency**: Processes/gen_server → Elm runtime effects

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Erlang language fundamentals - see `lang-erlang-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Reverse conversion (Elm → Erlang) - see `convert-elm-erlang`
- Backend-to-backend conversions - see other conversion skills

---

## Quick Reference

| Erlang | Elm | Notes |
|--------|-----|-------|
| `atom()` | `String` or custom type | Atoms become string literals or union types |
| `binary()` | `String` | UTF-8 encoded strings |
| `integer()` | `Int` | Arbitrary precision → fixed size |
| `float()` | `Float` | Direct mapping |
| `boolean()` | `Bool` | `true`/`false` mapping |
| `list()` | `List a` | Homogeneous typed lists |
| `tuple()` | Custom type or record | Named fields preferred |
| `map()` | `Dict k v` | Key-value storage |
| `pid()` | N/A | No direct equivalent (use Cmd/Sub) |
| `undefined` | `Nothing` in `Maybe a` | Explicit nullability |
| `{ok, Value}` | `Just Value` or `Ok Value` | Success wrapper |
| `{error, Reason}` | `Err Reason` in `Result e a` | Error wrapper |

---

## Architectural Paradigm Shift

### From OTP to The Elm Architecture (TEA)

| Aspect | Erlang OTP | Elm TEA |
|--------|------------|---------|
| **Purpose** | Distributed, fault-tolerant backend | Type-safe, reactive frontend |
| **Concurrency** | Millions of processes | Single-threaded event loop |
| **State** | Process-local mutable state | Immutable application state |
| **Communication** | Message passing between processes | Commands/Subscriptions to runtime |
| **Error handling** | Let-it-crash + supervision trees | Compiler-enforced exhaustive handling |

### Mapping OTP Behaviors to TEA Components

**Erlang gen_server:**
```erlang
-module(counter_server).
-behaviour(gen_server).

-record(state, {count = 0}).

init([]) -> {ok, #state{}}.

handle_call(get, _From, State) ->
    {reply, State#state.count, State};
handle_call({increment, N}, _From, State) ->
    NewCount = State#state.count + N,
    {reply, NewCount, State#state{count = NewCount}}.
```

**Elm equivalent using TEA:**
```elm
module Counter exposing (Model, Msg, init, update, view)

-- MODEL
type alias Model =
    { count : Int }

init : Model
init =
    { count = 0 }

-- UPDATE
type Msg
    = Increment Int
    | Get

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        Increment n ->
            ( { model | count = model.count + n }, Cmd.none )

        Get ->
            ( model, Cmd.none )

-- VIEW
view : Model -> Html Msg
view model =
    div []
        [ text ("Count: " ++ String.fromInt model.count)
        , button [ onClick (Increment 1) ] [ text "Increment" ]
        ]
```

---

## Type System Mapping

### Primitive Types

| Erlang | Elm | Notes |
|--------|-----|-------|
| `true` / `false` | `True` / `False` | Capitalized in Elm |
| `42` | `42` | Integer literals |
| `3.14` | `3.14` | Float literals |
| `<<"binary">>` | `"String"` | UTF-8 strings |
| `'atom'` | `"string"` or custom type | Context-dependent |

### Collection Types

| Erlang | Elm | Example |
|--------|-----|---------|
| `[1, 2, 3]` | `[1, 2, 3]` | Homogeneous lists |
| `#{key => value}` | `Dict.fromList [("key", value)]` | Requires Dict module |
| `{ok, 42}` | `Ok 42` | Result type |
| `{error, "failed"}` | `Err "failed"` | Result type |
| `undefined` | `Nothing` | Maybe type |

### Structured Types

**Erlang Records → Elm Type Aliases**

```erlang
%% Erlang
-record(user, {
    id :: integer(),
    name :: binary(),
    age :: integer() | undefined
}).
```

```elm
-- Elm
type alias User =
    { id : Int
    , name : String
    , age : Maybe Int
    }
```

---

## Idiom Translation

### 1. Pattern Matching

**Erlang:**
```erlang
classify(N) when N > 0 -> positive;
classify(N) when N < 0 -> negative;
classify(0) -> zero.
```

**Elm:**
```elm
classify : Int -> String
classify n =
    case compare n 0 of
        GT -> "positive"
        LT -> "negative"
        EQ -> "zero"
```

### 2. List Processing

**Erlang:**
```erlang
Squares = [X * X || X <- [1, 2, 3, 4, 5], X rem 2 == 0].
```

**Elm:**
```elm
squares : List Int
squares =
    [1, 2, 3, 4, 5]
        |> List.filter (\x -> modBy 2 x == 0)
        |> List.map (\x -> x * x)
```

### 3. Error Handling

**Erlang:**
```erlang
parse_int(Str) ->
    try binary_to_integer(Str) of
        Int -> {ok, Int}
    catch
        error:badarg -> {error, invalid_integer}
    end.
```

**Elm:**
```elm
parseInt : String -> Result String Int
parseInt str =
    String.toInt str
        |> Result.fromMaybe "Invalid integer"
```

### 4. Optional Values

**Erlang:**
```erlang
get_timeout(#config{timeout = undefined}) -> 5000;
get_timeout(#config{timeout = T}) -> T.
```

**Elm:**
```elm
getTimeout : Config -> Int
getTimeout config =
    Maybe.withDefault 5000 config.timeout
```

### 5. HTTP Requests (Message Passing Replacement)

**Erlang:**
```erlang
fetch_data(Url) ->
    Pid = self(),
    spawn(fun() ->
        Response = httpc:request(get, {Url, []}, [], []),
        Pid ! {http_response, Response}
    end).
```

**Elm:**
```elm
type Msg
    = GotData (Result Http.Error String)

fetchData : String -> Cmd Msg
fetchData url =
    Http.get
        { url = url
        , expect = Http.expectString GotData
        }
```

### 6. State Machine

**Erlang:**
```erlang
locked(cast, {button, Code}, #{code := Code} = Data) ->
    {next_state, unlocked, Data};
locked(cast, {button, _}, Data) ->
    {keep_state, Data}.
```

**Elm:**
```elm
type DoorState
    = Locked
    | Unlocked

type Msg
    = ButtonPressed String

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case (msg, model.state) of
        (ButtonPressed code, Locked) ->
            if code == model.correctCode then
                ( { model | state = Unlocked }, Cmd.none )
            else
                ( model, Cmd.none )
        _ ->
            ( model, Cmd.none )
```

---

## Error Handling Philosophy

### Philosophy Shift

| Erlang | Elm |
|--------|-----|
| **Let-it-crash**: Supervisors restart failed processes | **Prevent-all-crashes**: Compiler enforces handling all cases |
| Runtime errors are acceptable | Compile-time guarantees eliminate runtime errors |

### Practical Translation

**Erlang:**
```erlang
safe_divide(_, 0) -> {error, division_by_zero};
safe_divide(X, Y) -> {ok, X / Y}.
```

**Elm:**
```elm
type DivisionError = DivisionByZero

safeDivide : Float -> Float -> Result DivisionError Float
safeDivide a b =
    if b == 0 then
        Err DivisionByZero
    else
        Ok (a / b)
```

---

## Migration Strategy

### What CAN be converted:
- Business logic (calculations, validations)
- Data transformations
- State machines
- Request/response patterns

### What CANNOT be converted:
- Process supervision (no equivalent)
- Distributed systems (Elm is frontend-only)
- Hot code reloading
- Low-level concurrency

### Architecture Mapping

```
Erlang OTP Application
│
├── Supervision Tree ──────────> [Remains in Erlang backend]
├── gen_server (State) ────────> Elm Model + Update
├── handle_call/cast ──────────> Msg variants + update cases
├── State transitions ─────────> Model updates
└── API endpoints ─────────────> Elm HTTP commands

Result: Hybrid architecture
- Backend: Erlang OTP (supervision, distributed state)
- Frontend: Elm (UI, client state, type-safe interactions)
- Communication: HTTP/WebSocket APIs
```

---

## Common Pitfalls

### 1. Trying to Port Process Concurrency
**Problem:** Erlang's concurrency model doesn't translate to Elm.
**Solution:** Re-architect around TEA with commands/subscriptions.

### 2. Expecting Mutable State
**Problem:** Erlang processes have mutable state; Elm is purely functional.
**Solution:** Embrace immutability. Return new model versions from update.

### 3. Over-relying on Dynamic Types
**Problem:** Erlang's dynamic typing has no direct Elm equivalent.
**Solution:** Use custom types (union types) to model all possibilities.

### 4. Ignoring JSON Boundaries
**Problem:** Assuming Erlang terms can be directly used in Elm.
**Solution:** Always create explicit JSON encoders/decoders for API contracts.

---

## Tooling Translation

| Erlang | Elm | Purpose |
|--------|-----|---------|
| `rebar3 compile` | `elm make` | Build project |
| `rebar3 eunit` | `elm-test` | Run tests |
| `rebar3 shell` | `elm repl` | Interactive shell |
| `dialyzer` | `elm` compiler | Type checking |
| `observer` | Elm debugger | Runtime inspection |

---

## Example: Counter with Backend

**Elm Frontend:**
```elm
module Counter exposing (main)

import Browser
import Html exposing (..)
import Html.Events exposing (onClick)
import Http

type alias Model =
    { count : Int, loading : Bool }

type Msg
    = Increment Int
    | GotCount (Result Http.Error Int)

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        Increment n ->
            ( { model | loading = True }
            , incrementCount n
            )

        GotCount (Ok count) ->
            ( { model | count = count, loading = False }
            , Cmd.none
            )

        GotCount (Err _) ->
            ( { model | loading = False }
            , Cmd.none
            )

incrementCount : Int -> Cmd Msg
incrementCount n =
    Http.post
        { url = "/api/counter"
        , body = Http.jsonBody (Encode.object [("increment", Encode.int n)])
        , expect = Http.expectJson GotCount countDecoder
        }
```

---

## See Also

- `lang-erlang-dev` - Erlang language fundamentals
- `lang-elm-dev` - Elm language fundamentals
- `meta-convert-dev` - General conversion methodology
- `convert-elm-erlang` - Reverse conversion
