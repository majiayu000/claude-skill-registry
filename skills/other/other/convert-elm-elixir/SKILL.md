---
name: convert-elm-elixir
description: Convert Elm code to idiomatic Elixir. Use when migrating Elm frontend applications to Elixir (Phoenix LiveView), translating Elm's functional patterns to Elixir, or refactoring Elm codebases to leverage OTP. Extends meta-convert-dev with Elm-to-Elixir specific patterns.
---

# Convert Elm to Elixir

Convert Elm code to idiomatic Elixir. This skill extends `meta-convert-dev` with Elm-to-Elixir specific type mappings, idiom translations, and tooling for migrating from frontend-focused functional programming to backend/full-stack development with OTP.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Elm types → Elixir types and structs
- **Idiom translations**: The Elm Architecture (TEA) → Phoenix LiveView / GenServer
- **Error handling**: Elm Maybe/Result → Elixir tagged tuples and pattern matching
- **Concurrency**: Elm Cmd/Sub → Elixir processes, GenServer, and Supervisor
- **Architecture**: Frontend TEA → Full-stack Phoenix with LiveView

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Elm language fundamentals - see `lang-elm-dev`
- Elixir language fundamentals - see `lang-elixir-dev`
- Reverse conversion (Elixir → Elm) - see `convert-elixir-elm`
- Phoenix-specific patterns beyond basics - see `lang-elixir-phoenix-dev`

---

## Quick Reference

| Elm | Elixir | Notes |
|-----|--------|-------|
| `String` | `String.t()` / `binary()` | UTF-8 binaries |
| `Int` | `integer()` | Arbitrary precision |
| `Float` | `float()` | 64-bit double |
| `Bool` | `boolean()` | `true` / `false` |
| `List a` | `list(a)` | Linked lists |
| `Maybe a` | `nil` / `{:ok, a}` / `{:error, reason}` | Context-dependent |
| `Result err ok` | `{:ok, ok}` / `{:error, err}` | Tagged tuples |
| `( a, b )` | `{a, b}` | Tuples |
| `type alias` | `defstruct` / `@type` | Records → Structs |
| `type` (union) | `@type` with `\|` or `defmodule` enum pattern | Sum types |
| `Cmd msg` | `GenServer.cast/2` or async process | Side effects |
| `Sub msg` | `GenServer` callbacks / PubSub | Event subscriptions |
| `Model` | GenServer state / LiveView assigns | Application state |
| `view` | LiveView `render/1` | UI rendering |

## When Converting Code

1. **Analyze source thoroughly** - Understand TEA lifecycle and Cmd/Sub usage
2. **Map types first** - Create type equivalence table for domain models
3. **Preserve semantics** - TEA's guarantees (no runtime errors, managed effects) need OTP equivalents
4. **Adopt Elixir idioms** - Don't write "Elm code in Elixir syntax"
5. **Consider architecture shift** - Frontend-only TEA → Full-stack Phoenix LiveView or Backend API
6. **Test equivalence** - Same business logic outcomes

---

## Type System Mapping

### Primitive Types

| Elm | Elixir | Notes |
|-----|--------|-------|
| `String` | `String.t()` | Both UTF-8, Elixir uses binaries |
| `Int` | `integer()` | Elm uses 32-bit JS numbers, Elixir has arbitrary precision |
| `Float` | `float()` | IEEE 754 double precision in both |
| `Bool` | `boolean()` | Direct mapping |
| `Char` | `String.t()` (single char) | Elixir doesn't have char type; use single-char string |
| `()` (unit) | `:ok` / `nil` | Context-dependent; often `:ok` for success |

### Collection Types

| Elm | Elixir | Notes |
|-----|--------|-------|
| `List a` | `list(a)` | Both are linked lists |
| `Array a` | `list(a)` | Elm's Array is optimized, Elixir uses lists or `:array` module |
| `( a, b )` | `{a, b}` | Tuples map directly |
| `( a, b, c )` | `{a, b, c}` | Tuples support any arity |
| `Dict k v` | `Map.t(k, v)` | Elm Dict → Elixir Map |
| `Set a` | `MapSet.t(a)` | Set implementations |

### Composite Types

| Elm | Elixir | Notes |
|-----|--------|-------|
| `type alias User = { name : String, ... }` | `defstruct [:name, ...]` + `@type` | Record → Struct |
| `type Msg = Inc \| Dec` | `@type msg :: :inc \| :dec` or atoms | Union types → Atoms or tagged tuples |
| `type Msg = SetName String` | `{:set_name, String.t()}` | Tagged tuple pattern |
| `Maybe a` | `nil \| a` or `{:ok, a} \| {:error, term()}` | Elm Maybe → Elixir optionals |
| `Result err ok` | `{:ok, ok} \| {:error, err}` | Elm Result → Elixir result tuples |

### The Elm Architecture → Phoenix LiveView / GenServer

| Elm TEA | Elixir (LiveView) | Notes |
|---------|-------------------|-------|
| `Model` | `socket.assigns` | State in LiveView socket |
| `Msg` | Event names (atoms) | Messages sent to LiveView |
| `init : flags -> ( Model, Cmd Msg )` | `mount/3` | Initialize state |
| `update : Msg -> Model -> ( Model, Cmd Msg )` | `handle_event/3` | Handle user events |
| `view : Model -> Html Msg` | `render/1` | Render UI |
| `Cmd Msg` | `send(self(), msg)` or async tasks | Side effects |
| `Sub Msg` | `PubSub.subscribe/2` | Event subscriptions |

| Elm TEA | Elixir (GenServer) | Notes |
|---------|---------------------|-------|
| `Model` | GenServer state | Application state |
| `Msg` | Messages to GenServer | Pattern-matched in callbacks |
| `init` | `init/1` callback | Initialize GenServer |
| `update` | `handle_call/3` or `handle_cast/2` | Handle messages |
| `Cmd` | Async process / Task | Side effects |
| `Sub` | `handle_info/2` | Receive external messages |

---

## Idiom Translation

### Pattern 1: Maybe → Result Tuples

**Elm:**
```elm
type Maybe a
    = Just a
    | Nothing

findUser : Int -> Maybe User
findUser id =
    users
        |> List.filter (\u -> u.id == id)
        |> List.head

case findUser 1 of
    Just user ->
        user.name

    Nothing ->
        "Anonymous"
```

**Elixir:**
```elixir
# Using nil
def find_user(id) do
  Enum.find(users(), fn u -> u.id == id end)
end

case find_user(1) do
  nil -> "Anonymous"
  user -> user.name
end

# Or using result tuples (more idiomatic for operations that can fail)
def find_user(id) do
  case Enum.find(users(), fn u -> u.id == id end) do
    nil -> {:error, :not_found}
    user -> {:ok, user}
  end
end

case find_user(1) do
  {:ok, user} -> user.name
  {:error, :not_found} -> "Anonymous"
end
```

**Why this translation:**
- Elm's `Maybe` is explicit about presence/absence
- Elixir uses `nil` for simple optionals or `{:ok, value}` / `{:error, reason}` for operations
- Pattern matching works similarly in both languages
- Elixir's tagged tuples provide more context (error reasons)

### Pattern 2: Result → Tagged Tuples

**Elm:**
```elm
type Result error value
    = Ok value
    | Err error

parseAge : String -> Result String Int
parseAge str =
    case String.toInt str of
        Just age ->
            if age >= 0 then
                Ok age
            else
                Err "Age must be non-negative"

        Nothing ->
            Err "Not a valid number"

case parseAge "25" of
    Ok age ->
        "Age: " ++ String.fromInt age

    Err message ->
        "Error: " ++ message
```

**Elixir:**
```elixir
@spec parse_age(String.t()) :: {:ok, integer()} | {:error, String.t()}
def parse_age(str) do
  case Integer.parse(str) do
    {age, ""} when age >= 0 ->
      {:ok, age}

    {_age, ""} ->
      {:error, "Age must be non-negative"}

    _ ->
      {:error, "Not a valid number"}
  end
end

case parse_age("25") do
  {:ok, age} ->
    "Age: #{age}"

  {:error, message} ->
    "Error: #{message}"
end
```

**Why this translation:**
- Direct mapping from Elm `Result` to Elixir tagged tuples
- Pattern matching syntax is very similar
- Elixir's `with` statement can chain multiple results (similar to Elm's `Result.andThen`)

### Pattern 3: The Elm Architecture → Phoenix LiveView

**Elm (Counter):**
```elm
module Main exposing (main)

import Browser
import Html exposing (Html, button, div, text)
import Html.Events exposing (onClick)

-- MODEL

type alias Model =
    { count : Int }

init : () -> ( Model, Cmd Msg )
init _ =
    ( { count = 0 }, Cmd.none )

-- UPDATE

type Msg
    = Increment
    | Decrement

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Increment ->
            ( { model | count = model.count + 1 }, Cmd.none )

        Decrement ->
            ( { model | count = model.count - 1 }, Cmd.none )

-- VIEW

view : Model -> Html Msg
view model =
    div []
        [ button [ onClick Decrement ] [ text "-" ]
        , div [] [ text (String.fromInt model.count) ]
        , button [ onClick Increment ] [ text "+" ]
        ]

main : Program () Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , view = view
        , subscriptions = \_ -> Sub.none
        }
```

**Elixir (Phoenix LiveView):**
```elixir
defmodule MyAppWeb.CounterLive do
  use MyAppWeb, :live_view

  # MOUNT (like init)
  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, count: 0)}
  end

  # HANDLE_EVENT (like update)
  @impl true
  def handle_event("increment", _params, socket) do
    {:noreply, update(socket, :count, &(&1 + 1))}
  end

  def handle_event("decrement", _params, socket) do
    {:noreply, update(socket, :count, &(&1 - 1))}
  end

  # RENDER (like view)
  @impl true
  def render(assigns) do
    ~H"""
    <div>
      <button phx-click="decrement">-</button>
      <div><%= @count %></div>
      <button phx-click="increment">+</button>
    </div>
    """
  end
end
```

**Why this translation:**
- TEA's Model → LiveView's `socket.assigns`
- TEA's Msg → LiveView event names (strings/atoms)
- TEA's `update` → LiveView's `handle_event/3`
- TEA's `view` → LiveView's `render/1`
- TEA's `Cmd` → LiveView async operations (via `send(self(), ...)` or `Task.async`)
- LiveView handles the runtime (like Elm Runtime), managing concurrency and state

### Pattern 4: List Processing

**Elm:**
```elm
processData : List Int -> Int
processData numbers =
    numbers
        |> List.filter (\x -> x > 0)
        |> List.map (\x -> x * 2)
        |> List.foldl (+) 0
```

**Elixir:**
```elixir
def process_data(numbers) do
  numbers
  |> Enum.filter(&(&1 > 0))
  |> Enum.map(&(&1 * 2))
  |> Enum.sum()
end

# Or using reduce explicitly
def process_data(numbers) do
  numbers
  |> Enum.filter(&(&1 > 0))
  |> Enum.map(&(&1 * 2))
  |> Enum.reduce(0, &+/2)
end
```

**Why this translation:**
- Pipe operators work identically
- `List` module → `Enum` module
- Lambda syntax differs: Elm `\x -> x * 2` → Elixir `&(&1 * 2)` or `fn x -> x * 2 end`
- Both are lazy in comprehensions, eager in pipes

### Pattern 5: Union Types → Pattern Matching

**Elm:**
```elm
type Status
    = Loading
    | Success String
    | Failure String

handleStatus : Status -> String
handleStatus status =
    case status of
        Loading ->
            "Loading..."

        Success data ->
            "Data: " ++ data

        Failure error ->
            "Error: " ++ error
```

**Elixir:**
```elixir
# Using atoms and tagged tuples
@type status :: :loading | {:success, String.t()} | {:failure, String.t()}

def handle_status(status) do
  case status do
    :loading ->
      "Loading..."

    {:success, data} ->
      "Data: #{data}"

    {:failure, error} ->
      "Error: #{error}"
  end
end
```

**Why this translation:**
- Elm's union types → Elixir atoms (for zero-arg variants) and tagged tuples (for data-carrying variants)
- Pattern matching syntax is nearly identical
- Elixir's approach is more dynamic but equally powerful

---

## Error Handling

### Elm Error Model → Elixir Error Model

| Aspect | Elm | Elixir |
|--------|-----|--------|
| Primary Model | `Maybe` / `Result` | Tagged tuples (`{:ok, val}` / `{:error, reason}`) |
| Error Propagation | `Result.andThen` | `with` statement |
| Null Safety | No nulls; use `Maybe` | `nil` exists but tuples preferred |
| Exceptions | None (compile-time guarantee) | Exceptions exist but discouraged; use `{:error, reason}` |

### Chaining Operations with Errors

**Elm:**
```elm
validateAndSave : String -> Result String User
validateAndSave input =
    input
        |> validateEmail
        |> Result.andThen createUser
        |> Result.andThen saveToDatabase

case validateAndSave "alice@example.com" of
    Ok user ->
        "Saved: " ++ user.name

    Err message ->
        "Failed: " ++ message
```

**Elixir:**
```elixir
def validate_and_save(input) do
  with {:ok, email} <- validate_email(input),
       {:ok, user} <- create_user(email),
       {:ok, saved_user} <- save_to_database(user) do
    {:ok, saved_user}
  else
    {:error, reason} -> {:error, reason}
  end
end

case validate_and_save("alice@example.com") do
  {:ok, user} ->
    "Saved: #{user.name}"

  {:error, message} ->
    "Failed: #{message}"
end
```

**Why this translation:**
- Elm's `Result.andThen` for chaining → Elixir's `with` statement
- Both short-circuit on first error
- Elixir's `with` is more flexible (can handle multiple patterns)

---

## Concurrency Patterns

### Elm Cmd/Sub → Elixir Processes

Elm's concurrency is **managed by the Elm Runtime** - you describe side effects declaratively via `Cmd` and `Sub`. Elixir requires **explicit process management** but provides OTP primitives.

### Cmd (Commands) → Async Operations

**Elm:**
```elm
-- Cmd describes side effect; runtime executes it
type Msg
    = GotUsers (Result Http.Error (List User))

getUsers : Cmd Msg
getUsers =
    Http.get
        { url = "https://api.example.com/users"
        , expect = Http.expectJson GotUsers (Decode.list userDecoder)
        }

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FetchUsers ->
            ( { model | loading = True }, getUsers )

        GotUsers result ->
            case result of
                Ok users ->
                    ( { model | users = users, loading = False }, Cmd.none )

                Err _ ->
                    ( { model | error = Just "Failed", loading = False }, Cmd.none )
```

**Elixir (LiveView):**
```elixir
defmodule MyAppWeb.UsersLive do
  use MyAppWeb, :live_view

  def handle_event("fetch_users", _params, socket) do
    # Async task (like Cmd)
    send(self(), :perform_fetch)
    {:noreply, assign(socket, loading: true)}
  end

  def handle_info(:perform_fetch, socket) do
    case HTTPoison.get("https://api.example.com/users") do
      {:ok, %{body: body}} ->
        users = Jason.decode!(body)
        {:noreply, assign(socket, users: users, loading: false)}

      {:error, _reason} ->
        {:noreply, assign(socket, error: "Failed", loading: false)}
    end
  end
end
```

**Elixir (GenServer):**
```elixir
defmodule UserFetcher do
  use GenServer

  def handle_cast(:fetch_users, state) do
    # Spawn async task
    Task.async(fn ->
      HTTPoison.get("https://api.example.com/users")
    end)

    {:noreply, %{state | loading: true}}
  end

  def handle_info({_ref, {:ok, %{body: body}}}, state) do
    users = Jason.decode!(body)
    {:noreply, %{state | users: users, loading: false}}
  end

  def handle_info({_ref, {:error, _reason}}, state) do
    {:noreply, %{state | error: "Failed", loading: false}}
  end
end
```

**Why this translation:**
- Elm `Cmd` → Elixir `send(self(), msg)` or `Task.async`
- Elm runtime guarantees serialized `update` calls → Elixir GenServer/LiveView handle one message at a time
- Both avoid race conditions in user code

### Sub (Subscriptions) → PubSub / handle_info

**Elm:**
```elm
subscriptions : Model -> Sub Msg
subscriptions model =
    Time.every 1000 Tick  -- Every second
```

**Elixir (LiveView):**
```elixir
def mount(_params, _session, socket) do
  if connected?(socket) do
    # Subscribe to Phoenix PubSub
    Phoenix.PubSub.subscribe(MyApp.PubSub, "events")

    # Or schedule periodic message
    :timer.send_interval(1000, self(), :tick)
  end

  {:ok, socket}
end

def handle_info(:tick, socket) do
  # Handle periodic event
  {:noreply, update(socket, :count, &(&1 + 1))}
end

def handle_info(%{event: "user_updated", payload: user}, socket) do
  # Handle PubSub message
  {:noreply, assign(socket, current_user: user)}
end
```

**Why this translation:**
- Elm `Sub` → Elixir `Phoenix.PubSub` or `:timer` or `handle_info/2`
- Both models ensure messages arrive one at a time in the update/handle loop

---

## Common Pitfalls

1. **Assuming Elm's "No Runtime Errors" in Elixir**
   - Elm guarantees no runtime errors via its type system
   - Elixir has dynamic typing and exceptions
   - **Fix:** Use typespecs (`@spec`), Dialyzer, and pattern match exhaustively

2. **Forgetting Immutability Differences**
   - Elm enforces immutability at language level
   - Elixir has immutable data but processes have mutable state
   - **Fix:** Never mutate GenServer state directly; always return new state

3. **Misunderstanding Cmd/Sub → Process Translation**
   - Elm's Cmd/Sub are declarative; runtime manages everything
   - Elixir requires explicit process spawning and message handling
   - **Fix:** Use GenServer/LiveView patterns, don't try to replicate Elm Runtime exactly

4. **Over-using Exceptions**
   - Elm has no exceptions
   - Elixir has exceptions but idiomatic code uses `{:ok, val}` / `{:error, reason}`
   - **Fix:** Use tagged tuples and pattern matching, reserve exceptions for truly exceptional cases

5. **Ignoring OTP Supervision**
   - Elm runtime handles all failures invisibly
   - Elixir requires explicit supervision trees
   - **Fix:** Use Supervisors to restart crashed processes ("let it crash" philosophy)

6. **Not Leveraging Elixir's Strengths**
   - Elm is frontend-only; Elixir is full-stack
   - **Fix:** Use Phoenix for backend + LiveView for reactive frontend; don't just replicate Elm's architecture

7. **Type Alias vs Struct Confusion**
   - Elm's `type alias` creates a record type
   - Elixir's `defstruct` creates a module-specific struct
   - **Fix:** Use `defstruct` for domain models, `@type` for type annotations

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| **Phoenix** | Web framework | Use for full-stack apps; LiveView for reactive UIs |
| **Phoenix LiveView** | Reactive UI | Closest equivalent to Elm's TEA |
| **Ecto** | Database ORM | No direct Elm equivalent (frontend-only) |
| **ExUnit** | Testing framework | Similar philosophy to elm-test |
| **Dialyzer** | Static analysis | Partial type checking (not as strong as Elm's) |
| **Credo** | Code linter | Enforce Elixir conventions |
| **mix format** | Code formatter | Like elm-format |

---

## Examples

### Example 1: Simple - Type Alias to Struct

**Elm:**
```elm
type alias User =
    { name : String
    , email : String
    , age : Int
    }

createUser : String -> String -> Int -> User
createUser name email age =
    { name = name, email = email, age = age }
```

**Elixir:**
```elixir
defmodule User do
  @type t :: %__MODULE__{
    name: String.t(),
    email: String.t(),
    age: integer()
  }

  defstruct [:name, :email, :age]

  @spec create(String.t(), String.t(), integer()) :: t()
  def create(name, email, age) do
    %User{name: name, email: email, age: age}
  end
end
```

### Example 2: Medium - Result Chaining

**Elm:**
```elm
type alias ValidationError = String

validateUser : String -> String -> Int -> Result ValidationError User
validateUser name email age =
    validateName name
        |> Result.andThen (\_ -> validateEmail email)
        |> Result.andThen (\_ -> validateAge age)
        |> Result.map (\_ -> { name = name, email = email, age = age })

validateName : String -> Result ValidationError String
validateName name =
    if String.isEmpty name then
        Err "Name cannot be empty"
    else
        Ok name

validateEmail : String -> Result ValidationError String
validateEmail email =
    if String.contains email "@" then
        Ok email
    else
        Err "Invalid email"

validateAge : Int -> Result ValidationError Int
validateAge age =
    if age >= 18 then
        Ok age
    else
        Err "Must be at least 18"
```

**Elixir:**
```elixir
defmodule UserValidator do
  @type validation_error :: String.t()

  @spec validate_user(String.t(), String.t(), integer()) ::
    {:ok, User.t()} | {:error, validation_error()}
  def validate_user(name, email, age) do
    with {:ok, _} <- validate_name(name),
         {:ok, _} <- validate_email(email),
         {:ok, _} <- validate_age(age) do
      {:ok, User.create(name, email, age)}
    end
  end

  defp validate_name(""), do: {:error, "Name cannot be empty"}
  defp validate_name(name), do: {:ok, name}

  defp validate_email(email) do
    if String.contains?(email, "@") do
      {:ok, email}
    else
      {:error, "Invalid email"}
    end
  end

  defp validate_age(age) when age >= 18, do: {:ok, age}
  defp validate_age(_), do: {:error, "Must be at least 18"}
end
```

### Example 3: Complex - TEA to LiveView Migration

**Elm (Todo App):**
```elm
module Main exposing (main)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)

-- MODEL

type alias Model =
    { todos : List Todo
    , input : String
    }

type alias Todo =
    { id : Int
    , text : String
    , completed : Bool
    }

init : () -> ( Model, Cmd Msg )
init _ =
    ( { todos = [], input = "" }, Cmd.none )

-- UPDATE

type Msg
    = UpdateInput String
    | AddTodo
    | ToggleTodo Int
    | RemoveTodo Int

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        UpdateInput input ->
            ( { model | input = input }, Cmd.none )

        AddTodo ->
            if String.isEmpty model.input then
                ( model, Cmd.none )
            else
                let
                    newTodo =
                        { id = List.length model.todos
                        , text = model.input
                        , completed = False
                        }
                in
                ( { model
                    | todos = model.todos ++ [ newTodo ]
                    , input = ""
                  }
                , Cmd.none
                )

        ToggleTodo id ->
            let
                toggleTodo todo =
                    if todo.id == id then
                        { todo | completed = not todo.completed }
                    else
                        todo
            in
            ( { model | todos = List.map toggleTodo model.todos }, Cmd.none )

        RemoveTodo id ->
            ( { model | todos = List.filter (\t -> t.id /= id) model.todos }
            , Cmd.none
            )

-- VIEW

view : Model -> Html Msg
view model =
    div []
        [ input
            [ type_ "text"
            , placeholder "Add todo"
            , value model.input
            , onInput UpdateInput
            ]
            []
        , button [ onClick AddTodo ] [ text "Add" ]
        , ul [] (List.map viewTodo model.todos)
        ]

viewTodo : Todo -> Html Msg
viewTodo todo =
    li []
        [ input
            [ type_ "checkbox"
            , checked todo.completed
            , onClick (ToggleTodo todo.id)
            ]
            []
        , span
            [ style "text-decoration"
                (if todo.completed then "line-through" else "none")
            ]
            [ text todo.text ]
        , button [ onClick (RemoveTodo todo.id) ] [ text "X" ]
        ]
```

**Elixir (Phoenix LiveView Todo App):**
```elixir
defmodule MyAppWeb.TodoLive do
  use MyAppWeb, :live_view

  # Domain model
  defmodule Todo do
    @type t :: %__MODULE__{
      id: integer(),
      text: String.t(),
      completed: boolean()
    }

    defstruct [:id, :text, :completed]
  end

  # MOUNT (init)
  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, todos: [], input: "")}
  end

  # HANDLE_EVENT (update)
  @impl true
  def handle_event("update_input", %{"value" => input}, socket) do
    {:noreply, assign(socket, input: input)}
  end

  def handle_event("add_todo", _params, socket) do
    input = socket.assigns.input

    if String.trim(input) == "" do
      {:noreply, socket}
    else
      todos = socket.assigns.todos
      new_todo = %Todo{
        id: length(todos),
        text: input,
        completed: false
      }

      {:noreply, assign(socket, todos: todos ++ [new_todo], input: "")}
    end
  end

  def handle_event("toggle_todo", %{"id" => id}, socket) do
    id = String.to_integer(id)
    todos = Enum.map(socket.assigns.todos, fn todo ->
      if todo.id == id do
        %{todo | completed: !todo.completed}
      else
        todo
      end
    end)

    {:noreply, assign(socket, todos: todos)}
  end

  def handle_event("remove_todo", %{"id" => id}, socket) do
    id = String.to_integer(id)
    todos = Enum.reject(socket.assigns.todos, &(&1.id == id))

    {:noreply, assign(socket, todos: todos)}
  end

  # RENDER (view)
  @impl true
  def render(assigns) do
    ~H"""
    <div>
      <input
        type="text"
        placeholder="Add todo"
        value={@input}
        phx-keyup="update_input"
      />
      <button phx-click="add_todo">Add</button>

      <ul>
        <%= for todo <- @todos do %>
          <li>
            <input
              type="checkbox"
              checked={todo.completed}
              phx-click="toggle_todo"
              phx-value-id={todo.id}
            />
            <span style={"text-decoration: #{if todo.completed, do: "line-through", else: "none"}"}>
              <%= todo.text %>
            </span>
            <button phx-click="remove_todo" phx-value-id={todo.id}>X</button>
          </li>
        <% end %>
      </ul>
    </div>
    """
  end
end
```

**Router configuration:**
```elixir
# In router.ex
scope "/", MyAppWeb do
  pipe_through :browser

  live "/todos", TodoLive
end
```

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `lang-elm-dev` - Elm development patterns and TEA
- `lang-elixir-dev` - Elixir development patterns
- `lang-elixir-phoenix-dev` - Advanced Phoenix and LiveView patterns
- `lang-elixir-otp-dev` - OTP patterns for concurrency

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Compare Elm Cmd/Sub to Elixir processes/GenServer
- `patterns-serialization-dev` - JSON encoding/decoding across languages
- `patterns-testing-dev` - Testing strategies for functional code

---

## References

- [Elm Guide](https://guide.elm-lang.org/) - Elm fundamentals and TEA
- [Phoenix LiveView Docs](https://hexdocs.pm/phoenix_live_view/) - LiveView guide
- [Elixir School](https://elixirschool.com/) - Elixir tutorials
- [Programming Phoenix LiveView](https://pragprog.com/titles/liveview/programming-phoenix-liveview/) - Book on LiveView patterns
