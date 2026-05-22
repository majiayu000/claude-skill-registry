---
name: convert-elixir-elm
description: Convert Elixir code to idiomatic Elm. Use when migrating server-side Elixir logic to frontend applications, translating BEAM concurrency patterns to The Elm Architecture, or refactoring Elixir codebases for browser-based UI. Extends meta-convert-dev with Elixir-to-Elm specific patterns.
---

# Convert Elixir to Elm

Convert Elixir code to idiomatic Elm. This skill extends `meta-convert-dev` with Elixir-to-Elm specific type mappings, idiom translations, and architectural guidance for translating server-side BEAM code to client-side functional UI.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Elixir dynamic types → Elm static types
- **Idiom translations**: Pattern matching, pipelines, and functional patterns
- **Architecture translation**: GenServer/OTP → The Elm Architecture (TEA)
- **Concurrency translation**: Processes/message passing → Cmd/Sub model
- **Error handling**: `{:ok, _}` / `{:error, _}` → Result type
- **Effect management**: Side effects anywhere → Managed Cmd/Sub

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Elixir language fundamentals - see `lang-elixir-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Reverse conversion (Elm → Elixir) - see `convert-elm-elixir`
- Server-side Elixir deployment - focus on logic portable to frontend
- Phoenix-specific patterns - Phoenix LiveView is client-server hybrid

---

## Quick Reference

| Elixir | Elm | Notes |
|--------|-----|-------|
| `String.t()` | `String` | Direct mapping |
| `integer()` | `Int` | Elm Int is fixed-width |
| `float()` | `Float` | Direct mapping |
| `boolean()` | `Bool` | `:true` / `:false` → `True` / `False` |
| `list(a)` | `List a` | Direct mapping |
| `{a, b}` | `(a, b)` | Tuples up to 3 elements in Elm |
| `map()` / `%{}` | `Dict comparable v` | Elm Dict requires comparable keys |
| `{:ok, value}` | `Ok value` | Result type |
| `{:error, reason}` | `Err reason` | Result type |
| `nil` | `Nothing` | Use Maybe type |
| Pattern match | `case ... of` | Both support pattern matching |
| `\|>` pipe | `\|>` pipe | Identical operator |
| `Enum.map/2` | `List.map` | Similar API |
| GenServer state | TEA Model | State management pattern shift |
| `send/receive` | Cmd/Sub | Effects are managed |

## When Converting Code

1. **Identify pure business logic** - Elm runs in browser, not on BEAM VM
2. **Map dynamic types to static** - Add explicit type annotations
3. **Convert processes to TEA** - GenServers become Model-View-Update
4. **Translate effects** - Side effects become Cmd, subscriptions become Sub
5. **Preserve semantics** - Both are functional, immutable languages
6. **Handle compilation errors first** - Elm compiler guides you to correctness
7. **Test with property-based tests** - Both languages support them well

---

## Type System Mapping

### Primitive Types

| Elixir | Elm | Notes |
|--------|-----|-------|
| `integer()` | `Int` | Elm has fixed-width integers (no BigInt) |
| `float()` | `Float` | Direct mapping |
| `boolean()` | `Bool` | `:true` → `True`, `:false` → `False` |
| `String.t()` | `String` | Both are UTF-8 strings |
| `atom()` | Union types | `:ok`, `:error` become custom type variants |
| `nil` | `Nothing` | Use `Maybe a` type |
| `binary()` | - | No direct binary type; use String or custom encoding |
| `charlist()` | `String` | Convert charlists to strings |

### Collection Types

| Elixir | Elm | Notes |
|--------|-----|-------|
| `list(a)` | `List a` | Direct mapping |
| `{a, b}` | `(a, b)` | Tuples identical, max 3 in Elm |
| `{a, b, c}` | `(a, b, c)` | Max tuple size in Elm |
| `map()` / `%{k => v}` | `Dict comparable v` | Elm requires comparable keys |
| `MapSet.t(a)` | `Set comparable` | Elm requires comparable elements |
| `Keyword.t()` | `List (String, a)` | Convert keyword lists to list of tuples |
| `Range.t()` | `List Int` | Use `List.range start end` |

### Composite Types

| Elixir Pattern | Elm Pattern | Notes |
|----------------|-------------|-------|
| `%{name: String.t(), age: integer()}` | `type alias User = { name : String, age : Int }` | Maps → Records |
| `{:ok, value} \| {:error, reason}` | `Result reason value` | Tagged tuples → Result type |
| `value \| nil` | `Maybe value` | Nil → Nothing, value → Just value |
| `@type result :: :ok \| :error` | `type Result = Ok \| Error` | Atoms → Union type variants |
| Struct (`%User{}`) | `type alias User = { ... }` | Structs → Type aliases |
| Protocol implementation | - | No protocols in Elm, use functions on types |

### Function Types

| Elixir | Elm | Notes |
|--------|-----|-------|
| `(a -> b)` | `a -> b` | Function type identical syntax |
| `(a, b -> c)` | `a -> b -> c` | Elm auto-curries, no arity-2 syntax |
| `(() -> a)` | `() -> a` | No-argument functions |
| Anonymous fn | Lambda | Both support anonymous functions |

---

## Idiom Translation

### Pattern 1: Tagged Tuples → Result

**Elixir:**
```elixir
def divide(a, b) when b != 0, do: {:ok, a / b}
def divide(_, 0), do: {:error, :division_by_zero}

case divide(10, 2) do
  {:ok, result} -> IO.puts("Result: #{result}")
  {:error, reason} -> IO.puts("Error: #{reason}")
end
```

**Elm:**
```elm
divide : Float -> Float -> Result String Float
divide a b =
    if b /= 0 then
        Ok (a / b)
    else
        Err "division_by_zero"

-- Usage
case divide 10 2 of
    Ok result ->
        "Result: " ++ String.fromFloat result

    Err reason ->
        "Error: " ++ reason
```

**Why this translation:**
- Elixir's `{:ok, value}` / `{:error, reason}` pattern maps directly to Elm's `Result error value`
- Guards in Elixir (`when b != 0`) become if-expressions in Elm
- Atoms like `:division_by_zero` become strings or custom types
- Both use pattern matching in case expressions

### Pattern 2: Nil Handling → Maybe

**Elixir:**
```elixir
def find_user(id) do
  users = %{1 => %{name: "Alice"}, 2 => %{name: "Bob"}}
  Map.get(users, id)
end

def display_name(user) do
  case user do
    nil -> "Anonymous"
    %{name: name} -> name
  end
end

# Pipeline with defaults
name = find_user(1) |> display_name()
```

**Elm:**
```elm
findUser : Int -> Maybe User
findUser id =
    let
        users =
            Dict.fromList
                [ ( 1, { name = "Alice" } )
                , ( 2, { name = "Bob" } )
                ]
    in
    Dict.get id users

displayName : Maybe User -> String
displayName maybeUser =
    case maybeUser of
        Nothing ->
            "Anonymous"

        Just user ->
            user.name

-- Pipeline with Maybe.map
name : String
name =
    findUser 1
        |> Maybe.map .name
        |> Maybe.withDefault "Anonymous"
```

**Why this translation:**
- Elixir's `nil` becomes Elm's `Nothing`
- Present values become `Just value`
- `Maybe.withDefault` replaces nil coalescing
- Pattern matching translates directly

### Pattern 3: Enum Operations → List Functions

**Elixir:**
```elixir
[1, 2, 3, 4, 5]
|> Enum.filter(&(rem(&1, 2) == 0))
|> Enum.map(&(&1 * 2))
|> Enum.reduce(0, &(&1 + &2))
```

**Elm:**
```elm
[ 1, 2, 3, 4, 5 ]
    |> List.filter (\x -> modBy 2 x == 0)
    |> List.map (\x -> x * 2)
    |> List.foldl (+) 0
```

**Why this translation:**
- `Enum.filter` → `List.filter`
- `Enum.map` → `List.map`
- `Enum.reduce` → `List.foldl` (or `List.foldr`)
- Pipeline operator `|>` is identical
- Capture operator `&()` becomes lambda `\x ->`
- `rem` becomes `modBy` in Elm

### Pattern 4: Pattern Matching Lists

**Elixir:**
```elixir
def sum([]), do: 0
def sum([head | tail]), do: head + sum(tail)

def first([head | _]), do: {:ok, head}
def first([]), do: {:error, :empty_list}
```

**Elm:**
```elm
sum : List Int -> Int
sum list =
    case list of
        [] ->
            0

        head :: tail ->
            head + sum tail

first : List a -> Result String a
first list =
    case list of
        head :: _ ->
            Ok head

        [] ->
            Err "empty_list"
```

**Why this translation:**
- List pattern matching syntax is nearly identical
- `[head | tail]` in Elixir → `head :: tail` in Elm
- Multiple function clauses become case branches
- Guards can become if-expressions inside branches

### Pattern 5: With Statement → Nested Case or Result.andThen

**Elixir:**
```elixir
def create_user(params) do
  with {:ok, validated} <- validate_params(params),
       {:ok, user} <- insert_user(validated),
       {:ok, _email} <- send_welcome_email(user) do
    {:ok, user}
  else
    {:error, reason} -> {:error, reason}
  end
end
```

**Elm:**
```elm
-- Option 1: Nested case
createUser : Params -> Result Error User
createUser params =
    case validateParams params of
        Ok validated ->
            case insertUser validated of
                Ok user ->
                    case sendWelcomeEmail user of
                        Ok _ ->
                            Ok user

                        Err reason ->
                            Err reason

                Err reason ->
                    Err reason

        Err reason ->
            Err reason

-- Option 2: Result.andThen (preferred)
createUser : Params -> Result Error User
createUser params =
    validateParams params
        |> Result.andThen insertUser
        |> Result.andThen (\user ->
            sendWelcomeEmail user
                |> Result.map (\_ -> user)
        )
```

**Why this translation:**
- Elixir's `with` chains `{:ok, _}` results
- Elm uses `Result.andThen` for equivalent chaining
- Early error returns are handled by Result's short-circuiting
- Pipeline style preserves readability

---

## Architecture Translation: GenServer → The Elm Architecture

### GenServer State Management

**Elixir (GenServer):**
```elixir
defmodule Counter do
  use GenServer

  # Client API
  def start_link(initial_value) do
    GenServer.start_link(__MODULE__, initial_value, name: __MODULE__)
  end

  def increment do
    GenServer.call(__MODULE__, :increment)
  end

  def get do
    GenServer.call(__MODULE__, :get)
  end

  # Server Callbacks
  @impl true
  def init(initial_value), do: {:ok, initial_value}

  @impl true
  def handle_call(:increment, _from, state) do
    {:reply, state + 1, state + 1}
  end

  def handle_call(:get, _from, state) do
    {:reply, state, state}
  end
end
```

**Elm (TEA Model):**
```elm
-- MODEL
type alias Model =
    { count : Int
    }

init : () -> ( Model, Cmd Msg )
init _ =
    ( { count = 0 }, Cmd.none )

-- UPDATE
type Msg
    = Increment
    | Get

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment ->
            ( { model | count = model.count + 1 }, Cmd.none )

        Get ->
            -- In Elm, view always has access to model
            -- No need for explicit "get" message
            ( model, Cmd.none )

-- VIEW
view : Model -> Html Msg
view model =
    div []
        [ button [ onClick Increment ] [ text "+" ]
        , div [] [ text (String.fromInt model.count) ]
        ]
```

**Why this translation:**
- GenServer state → Model
- Client API calls → Msg variants
- `handle_call` → `update` function branches
- Synchronous replies → View reads model directly
- No process needed; Elm runtime manages state

### Process Communication → Cmd/Sub

**Elixir (Process Messages):**
```elixir
# Sending process
pid = spawn(fn ->
  receive do
    {:fetch_user, caller, user_id} ->
      user = fetch_user_from_db(user_id)
      send(caller, {:user_fetched, user})
  end
end)

send(pid, {:fetch_user, self(), 123})

receive do
  {:user_fetched, user} -> IO.inspect(user)
after
  5000 -> IO.puts("Timeout")
end
```

**Elm (Commands and Subscriptions):**
```elm
-- Commands represent effects to perform
type Msg
    = FetchUser Int
    | GotUser (Result Http.Error User)

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUser userId ->
            ( { model | loading = True }
            , Http.get
                { url = "/api/users/" ++ String.fromInt userId
                , expect = Http.expectJson GotUser userDecoder
                }
            )

        GotUser result ->
            case result of
                Ok user ->
                    ( { model | user = Just user, loading = False }
                    , Cmd.none
                    )

                Err _ ->
                    ( { model | loading = False }
                    , Cmd.none
                    )

-- Subscriptions for incoming events
subscriptions : Model -> Sub Msg
subscriptions model =
    -- Listen to time every second
    Time.every 1000 Tick
```

**Why this translation:**
- `send` → Create Cmd in update
- `receive` → Handle Msg in update
- Process spawning → Cmd.batch for multiple effects
- Message passing → Msg type with variants
- Timeouts → Handled by Sub/Cmd cancellation

### Supervision Trees → Application Structure

**Elixir (Supervisor):**
```elixir
defmodule MyApp.Application do
  use Application

  def start(_type, _args) do
    children = [
      {Counter, 0},
      {UserCache, []},
      {DatabasePool, pool_size: 10}
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

**Elm (Module Organization):**
```elm
-- No supervision needed - no crashes!
-- Instead: Organize code into modules

-- Main.elm
module Main exposing (main)

import Browser
import Counter
import UserCache

type alias Model =
    { counter : Counter.Model
    , userCache : UserCache.Model
    }

type Msg
    = CounterMsg Counter.Msg
    | UserCacheMsg UserCache.Msg

init : () -> ( Model, Cmd Msg )
init _ =
    let
        ( counterModel, counterCmd ) =
            Counter.init ()

        ( cacheModel, cacheCmd ) =
            UserCache.init ()
    in
    ( { counter = counterModel
      , userCache = cacheModel
      }
    , Cmd.batch
        [ Cmd.map CounterMsg counterCmd
        , Cmd.map UserCacheMsg cacheCmd
        ]
    )

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        CounterMsg subMsg ->
            let
                ( counterModel, counterCmd ) =
                    Counter.update subMsg model.counter
            in
            ( { model | counter = counterModel }
            , Cmd.map CounterMsg counterCmd
            )

        UserCacheMsg subMsg ->
            let
                ( cacheModel, cacheCmd ) =
                    UserCache.update subMsg model.userCache
            in
            ( { model | userCache = cacheModel }
            , Cmd.map UserCacheMsg cacheCmd
            )
```

**Why this translation:**
- No supervision needed - Elm has no runtime exceptions
- Module composition replaces supervision trees
- Each "child" is a module with its own Model/Msg/update
- Parent routes messages to appropriate child module
- Cmd.map translates between parent and child messages

---

## Concurrency Model Translation

### Elixir: Process-Based Concurrency

```elixir
# Multiple concurrent processes
tasks = Enum.map(user_ids, fn id ->
  Task.async(fn -> fetch_user(id) end)
end)

users = Task.await_many(tasks, 5000)
```

### Elm: Command-Based Concurrency

```elm
-- Multiple HTTP requests (runtime handles concurrency)
type Msg
    = FetchUsers
    | GotUser Int (Result Http.Error User)

fetchUsers : List Int -> Cmd Msg
fetchUsers userIds =
    userIds
        |> List.map (\id ->
            Http.get
                { url = "/api/users/" ++ String.fromInt id
                , expect = Http.expectJson (GotUser id) userDecoder
                }
        )
        |> Cmd.batch

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUsers ->
            ( { model | loading = True }
            , fetchUsers [ 1, 2, 3, 4, 5 ]
            )

        GotUser id result ->
            -- Each response handled as it arrives
            case result of
                Ok user ->
                    ( { model | users = Dict.insert id user model.users }
                    , Cmd.none
                    )

                Err _ ->
                    ( model, Cmd.none )
```

**Why this translation:**
- Elixir's `Task.async` → Elm's `Cmd.batch`
- Elixir manages processes explicitly → Elm runtime handles concurrency
- Both allow multiple operations in flight
- Elm guarantees serialized message handling (no race conditions)

### GenServer Periodic Work → Time Subscriptions

**Elixir:**
```elixir
defmodule PeriodicWorker do
  use GenServer

  def start_link(_), do: GenServer.start_link(__MODULE__, %{}, name: __MODULE__)

  def init(state) do
    schedule_work()
    {:ok, state}
  end

  def handle_info(:work, state) do
    do_work()
    schedule_work()
    {:noreply, state}
  end

  defp schedule_work do
    Process.send_after(self(), :work, 5000)
  end
end
```

**Elm:**
```elm
import Time

type Msg
    = DoWork Time.Posix

subscriptions : Model -> Sub Msg
subscriptions model =
    Time.every 5000 DoWork  -- 5000 milliseconds

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        DoWork time ->
            ( model, performWork time )

performWork : Time.Posix -> Cmd Msg
performWork time =
    -- Perform work here
    Cmd.none
```

**Why this translation:**
- `Process.send_after` → `Time.every` subscription
- `handle_info` → `update` with time-based Msg
- No manual rescheduling needed; Sub is continuous
- Elm runtime manages subscription lifecycle

---

## Error Handling

### Elixir Error Patterns

```elixir
# Pattern 1: Tagged tuples
{:ok, value} | {:error, reason}

# Pattern 2: Raise/rescue
try do
  dangerous_operation()
rescue
  e in RuntimeError -> {:error, e.message}
end

# Pattern 3: Pattern match or default
user = find_user(id) || %User{name: "Anonymous"}

# Pattern 4: With statement
with {:ok, a} <- step1(),
     {:ok, b} <- step2(a) do
  {:ok, b}
else
  {:error, reason} -> {:error, reason}
end
```

### Elm Error Patterns

```elm
-- Pattern 1: Result type
Ok value | Err reason

-- Pattern 2: No exceptions!
-- All errors are values
dangerousOperation : () -> Result String Value
dangerousOperation () =
    -- Cannot throw, must return Result

-- Pattern 3: Maybe with default
user : User
user =
    findUser id
        |> Maybe.withDefault { name = "Anonymous" }

-- Pattern 4: Result.andThen
processData : Input -> Result String Output
processData input =
    step1 input
        |> Result.andThen step2
        |> Result.andThen step3
```

**Key Differences:**
- Elm has NO exceptions - all errors are Result or Maybe values
- No try/rescue needed - compiler enforces error handling
- `with` statement → `Result.andThen` chaining
- Pattern matching on errors is identical

---

## Testing Strategy

### Property-Based Testing

**Elixir (StreamData):**
```elixir
defmodule MathTest do
  use ExUnit.Case
  use ExUnitProperties

  property "addition is commutative" do
    check all x <- integer(),
              y <- integer() do
      assert Math.add(x, y) == Math.add(y, x)
    end
  end

  property "list reverse is idempotent" do
    check all list <- list_of(integer()) do
      assert list |> Enum.reverse() |> Enum.reverse() == list
    end
  end
end
```

**Elm (elm-test with fuzz):**
```elm
module MathTest exposing (..)

import Expect
import Fuzz exposing (int, list)
import Test exposing (Test, describe, fuzz, fuzz2)

suite : Test
suite =
    describe "Math properties"
        [ fuzz2 int int "addition is commutative" <|
            \x y ->
                Math.add x y
                    |> Expect.equal (Math.add y x)

        , fuzz (list int) "list reverse is idempotent" <|
            \list ->
                list
                    |> List.reverse
                    |> List.reverse
                    |> Expect.equal list
        ]
```

**Why this translation:**
- Both support property-based testing
- `check all` → `fuzz` / `fuzz2`
- Generators translate directly
- Same test philosophy

### Unit Testing

**Elixir:**
```elixir
test "parses valid age" do
  assert {:ok, 25} = parse_age("25")
end

test "rejects negative age" do
  assert {:error, _} = parse_age("-5")
end
```

**Elm:**
```elm
test "parses valid age" <|
    \_ ->
        parseAge "25"
            |> Expect.equal (Ok 25)

test "rejects negative age" <|
    \_ ->
        parseAge "-5"
            |> Expect.err
```

---

## Common Pitfalls

### 1. Expecting Runtime Dynamism

```elixir
# Elixir: Dynamic typing allows this
defmodule Flexible do
  def process(value) when is_integer(value), do: value * 2
  def process(value) when is_binary(value), do: String.upcase(value)
end

process(5)      # 10
process("hi")   # "HI"
```

```elm
-- Elm: Must use union types for different types
type Value
    = IntValue Int
    | StringValue String

process : Value -> String
process value =
    case value of
        IntValue int ->
            String.fromInt (int * 2)

        StringValue str ->
            String.toUpper str

-- Usage
process (IntValue 5)       -- "10"
process (StringValue "hi") -- "HI"
```

**Fix:** Define explicit union types for polymorphic values.

### 2. Side Effects Anywhere vs. Managed Effects

```elixir
# Elixir: Can perform IO anywhere
def get_user(id) do
  IO.puts("Fetching user #{id}")  # Side effect!
  Database.get(:users, id)         # Side effect!
end
```

```elm
-- Elm: All effects through Cmd
getUser : Int -> Cmd Msg
getUser id =
    -- Cannot perform side effects directly
    -- Must return Cmd for Elm runtime
    Http.get
        { url = "/api/users/" ++ String.fromInt id
        , expect = Http.expectJson GotUser userDecoder
        }

-- "Logging" must also be a command (via port)
port logMessage : String -> Cmd msg

getUserWithLog : Int -> Cmd Msg
getUserWithLog id =
    Cmd.batch
        [ logMessage ("Fetching user " ++ String.fromInt id)
        , getUser id
        ]
```

**Fix:** Plan where effects belong in your Elm architecture.

### 3. Assuming Atoms Translate to Strings

```elixir
# Elixir: Atoms are efficient, unique
:ok
:error
:atom_name
```

```elm
-- Elm: Create custom types instead
type Status
    = Ok
    | Error
    | AtomName

-- NOT strings!
-- type Status = String  -- WRONG - loses type safety
```

**Fix:** Use union types for atom-like values, not strings.

### 4. GenServer State vs. TEA Model

```elixir
# Elixir: State hidden in process
GenServer.call(MyServer, :get_state)
```

```elm
-- Elm: State is always in Model, always visible to view
view : Model -> Html Msg
view model =
    -- Direct access to all state
    div [] [ text model.name ]
```

**Fix:** In Elm, embrace that all state is in Model and visible.

### 5. Expecting to "Let It Crash"

```elixir
# Elixir: Supervision restarts crashed processes
def risky_operation(value) do
  # If this crashes, supervisor restarts the process
  dangerous_thing(value)
end
```

```elm
-- Elm: NO CRASHES - compiler guarantees no runtime exceptions
riskyOperation : Value -> Result Error Output
riskyOperation value =
    -- Must handle all error cases explicitly
    case dangerousThing value of
        Ok result ->
            Ok result

        Err error ->
            Err error
```

**Fix:** Handle all error cases explicitly with Result type.

---

## Tooling

| Elixir Tool | Elm Equivalent | Notes |
|-------------|----------------|-------|
| `mix format` | `elm-format` | Auto-formatting |
| `mix test` | `elm-test` | Unit and property testing |
| `credo` | `elm-review` | Linting and code quality |
| `dialyzer` | Elm compiler | Type checking (Elm is stricter) |
| `iex` | `elm repl` | Interactive REPL |
| `mix deps.get` | `elm install` | Dependency management |
| `observer` | Browser DevTools | Runtime inspection |
| `mix docs` | `elm-doc-preview` | Documentation generation |

---

## Example: Complete Conversion

### Elixir: User Management Module

```elixir
defmodule UserManager do
  use GenServer

  # Client API
  def start_link(_) do
    GenServer.start_link(__MODULE__, %{}, name: __MODULE__)
  end

  def add_user(user) do
    GenServer.call(__MODULE__, {:add, user})
  end

  def get_user(id) do
    GenServer.call(__MODULE__, {:get, id})
  end

  def list_users do
    GenServer.call(__MODULE__, :list)
  end

  # Server Callbacks
  @impl true
  def init(_) do
    {:ok, %{}}
  end

  @impl true
  def handle_call({:add, user}, _from, state) do
    new_state = Map.put(state, user.id, user)
    {:reply, {:ok, user}, new_state}
  end

  def handle_call({:get, id}, _from, state) do
    result = Map.get(state, id)
    {:reply, result, state}
  end

  def handle_call(:list, _from, state) do
    users = Map.values(state)
    {:reply, users, state}
  end
end

# Usage
{:ok, _} = UserManager.start_link([])
UserManager.add_user(%{id: 1, name: "Alice"})
UserManager.list_users()
```

### Elm: User Management in TEA

```elm
module Main exposing (main)

import Browser
import Dict exposing (Dict)
import Html exposing (Html, button, div, input, text)
import Html.Attributes exposing (placeholder, value)
import Html.Events exposing (onClick, onInput)

-- MODEL

type alias User =
    { id : Int
    , name : String
    }

type alias Model =
    { users : Dict Int User
    , nextId : Int
    , nameInput : String
    }

init : () -> ( Model, Cmd Msg )
init _ =
    ( { users = Dict.empty
      , nextId = 1
      , nameInput = ""
      }
    , Cmd.none
    )

-- UPDATE

type Msg
    = AddUser
    | SetNameInput String
    | RemoveUser Int

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        AddUser ->
            if String.isEmpty model.nameInput then
                ( model, Cmd.none )
            else
                let
                    user =
                        { id = model.nextId
                        , name = model.nameInput
                        }

                    newUsers =
                        Dict.insert model.nextId user model.users
                in
                ( { model
                    | users = newUsers
                    | nextId = model.nextId + 1
                    | nameInput = ""
                  }
                , Cmd.none
                )

        SetNameInput name ->
            ( { model | nameInput = name }, Cmd.none )

        RemoveUser id ->
            ( { model | users = Dict.remove id model.users }
            , Cmd.none
            )

-- VIEW

view : Model -> Html Msg
view model =
    div []
        [ div []
            [ input
                [ placeholder "Enter name"
                , value model.nameInput
                , onInput SetNameInput
                ]
                []
            , button [ onClick AddUser ] [ text "Add User" ]
            ]
        , div [] (viewUsers model.users)
        ]

viewUsers : Dict Int User -> List (Html Msg)
viewUsers users =
    users
        |> Dict.values
        |> List.map viewUser

viewUser : User -> Html Msg
viewUser user =
    div []
        [ text user.name
        , button [ onClick (RemoveUser user.id) ] [ text "Remove" ]
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

**Key Translation Points:**
1. GenServer state → Model record
2. `handle_call` → `update` function branches
3. Client API → Msg variants
4. Synchronous calls → Direct model access in view
5. Map-based storage → Dict in Elm

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-elm-scala` - Related conversion from Elm
- `convert-haskell-elm` - Similar pure functional → frontend conversion
- `lang-elixir-dev` - Elixir development patterns
- `lang-elm-dev` - Elm development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Processes, async, and message passing across languages
- `patterns-serialization-dev` - JSON handling and data encoding patterns
- `patterns-metaprogramming-dev` - Compare dynamic features to type-driven design
