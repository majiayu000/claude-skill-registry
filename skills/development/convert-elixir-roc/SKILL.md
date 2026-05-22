---
name: convert-elixir-roc
description: Convert Elixir code to idiomatic Roc. Use when migrating Elixir projects to Roc, translating BEAM/OTP patterns to platform-based architecture, or refactoring Elixir codebases. Extends meta-convert-dev with Elixir-to-Roc specific patterns.
---

# Convert Elixir to Roc

Convert Elixir code to idiomatic Roc. This skill extends `meta-convert-dev` with Elixir-to-Roc specific type mappings, idiom translations, and architectural patterns for moving from dynamic, actor-based concurrency to static, pure functional programming with platform-provided effects.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Elixir dynamic types → Roc static types
- **Paradigm translation**: GenServer/OTP patterns → Pure state machines + platform Tasks
- **Idiom translations**: Elixir functional patterns → Roc functional patterns
- **Error handling**: Elixir error tuples + exceptions → Result types
- **Concurrency**: Processes/GenServer → Roc platform Tasks
- **Module system**: Elixir modules → Roc platform/application architecture
- **Metaprogramming**: Elixir macros → Roc abilities and external codegen

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Elixir language fundamentals - see `lang-elixir-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Reverse conversion (Roc → Elixir) - see `convert-roc-elixir`

---

## Quick Reference

| Elixir | Roc | Notes |
|--------|-----|-------|
| `:atom` | `[Tag]` | Atoms become tags in tag unions |
| `integer()` | `I64` / `U64` | Specify signedness explicitly |
| `float()` | `F64` | 64-bit float |
| `String.t()` | `Str` | UTF-8 strings |
| `binary()` | `List U8` | Byte sequences |
| `list()` | `List a` | Homogeneous lists |
| `tuple()` | `(a, b, c)` | Fixed-size tuples |
| `map()` | `Dict k v` | Key-value maps (requires Hash+Eq keys) |
| `keyword()` | `List (Str, a)` | List of tuples (no duplicate keys guaranteed) |
| `{:ok, value}` | `Ok(value)` | Success result |
| `{:error, reason}` | `Err(reason)` | Error result |
| `nil` | `None` in tag union | Optional values |
| `pid()` | - | No direct equivalent (platform handles processes) |
| `fn(x) -> x end` | `\x -> x` | Lambda syntax |
| `%{__struct__: Name}` | Opaque type `Name := ...` | Structs become opaque types |

## When Converting Code

1. **Analyze OTP patterns** before writing Roc - GenServers become pure state machines
2. **Identify process boundaries** - these become platform Task interactions
3. **Map dynamic patterns to static types** - use tag unions for variants
4. **Redesign supervision trees** - Roc platforms handle failure differently
5. **Extract pure logic** - separate computation from effects (Task, IO)
6. **Handle hot code loading** - not a language feature in Roc
7. **Test equivalence** - verify behavior matches despite different architecture

---

## Type System Mapping

### Primitive Types

| Elixir | Roc | Notes |
|--------|-----|-------|
| `:atom` | `[Tag]` | Atoms as tags in tag unions |
| `integer()` | `I64` | Default signed 64-bit |
| `integer()` | `U64` | Unsigned variant |
| `integer()` (small) | `I32` / `U32` | For smaller values |
| `integer()` (arbitrary) | - | Roc has fixed-size integers |
| `float()` | `F64` | 64-bit floating point |
| `boolean()` | `Bool` | Direct mapping |
| `String.t()` | `Str` | UTF-8 strings |
| `binary()` | `List U8` | Byte sequences |
| `bitstring()` | `List U8` | Byte-aligned only in Roc |
| `nil` | `None` | In tag union `[Some a, None]` |
| `pid()` | - | Processes don't exist in Roc |
| `port()` | - | Platform handles I/O |
| `reference()` | - | No direct equivalent |
| `function()` | Function types | See function mappings below |

### Collection Types

| Elixir | Roc | Notes |
|--------|-----|-------|
| `list()` | `List a` | Homogeneous lists (all same type) |
| `[T]` | `List T` | Type-safe, uniform elements |
| `tuple()` | `(A, B, C)` | Fixed-size tuples |
| `{A, B, C}` | `(A, B, C)` | Direct structural mapping |
| `map()` | `Dict k v` | Key-value dictionary (requires Hash+Eq for keys) |
| `%{K => V}` | `Dict K V` | Keys must implement Hash and Eq abilities |
| `MapSet.t()` | `Set a` | Unique values (requires Hash+Eq) |
| `keyword()` | `List (Str, a)` | List of tuples, no uniqueness guarantee |
| `[{:key, value}]` | `List (Str, a)` | Keyword lists as tuple lists |
| `Range.t()` | - | Use `List.range` to generate lists |
| `Stream.t()` | - | Roc has lazy iterators but no Stream type |

### Composite Types

| Elixir | Roc | Notes |
|--------|-----|-------|
| `defstruct` | `{ field : Type }` | Structs become records |
| `%Name{field: value}` | `{ field: value }` | Record literals |
| Tagged tuple `{:tag, value}` | `Tag(value)` | Tags with payloads |
| `@type name :: spec` | `Name : Type` | Type alias |
| `@opaque name :: spec` | Opaque type `Name := Type` | Hidden implementation |
| `@spec` annotations | Type signatures | Enforced in Roc |

### Function Types

| Elixir | Roc | Notes |
|--------|-----|-------|
| `(-> R)` | `({} -> R)` | Zero-argument function |
| `(A -> R)` | `(A -> R)` | Single argument |
| `(A, B -> R)` | `(A, B -> R)` | Multiple arguments (curried) |
| Variable arity | - | Roc doesn't support varargs |
| Default arguments | - | Use separate function signatures |

### Error Types

| Elixir | Roc | Notes |
|--------|-----|-------|
| `{:ok, value}` | `Ok(value)` | Success case |
| `{:error, reason}` | `Err(reason)` | Error case |
| `:ok` atom | `Ok({})` | Success with no value |
| `{:ok, V} \| {:error, R}` | `Result V R` | Result type |
| Exception raising | `Err` variant | No exceptions, use Result |
| `rescue` clause | Pattern match on Result | Explicit error handling |

---

## Idiom Translation

### Pattern 1: Simple Module Conversion

**Elixir:**
```elixir
defmodule MathUtils do
  @doc "Add two numbers"
  def add(a, b), do: a + b

  @doc "Square a number"
  def square(n), do: n * n

  # Private function
  defp internal_helper(x), do: x * 2
end
```

**Roc:**
```roc
interface MathUtils
    exposes [add, square]
    imports []

## Add two numbers
add : I64, I64 -> I64
add = \a, b -> a + b

## Square a number
square : I64 -> I64
square = \n -> n * n

# Private helper (not exposed)
internalHelper : I64 -> I64
internalHelper = \x -> x * 2
```

**Why this translation:**
- Elixir modules become Roc interfaces
- Public functions go in `exposes`
- Private functions are simply not exposed
- Doctests become inline `expect` tests in Roc
- Type signatures are explicit (not optional like typespecs)

### Pattern 2: Pattern Matching on Tagged Tuples

**Elixir:**
```elixir
def process_result({:ok, data}) do
  {:success, data}
end

def process_result({:error, reason}) do
  {:failure, reason}
end

def process_result(_unknown) do
  {:failure, :unknown_result}
end
```

**Roc:**
```roc
processResult : [Ok Data, Err Reason, Unknown] -> [Success Data, Failure Reason]
processResult = \result ->
    when result is
        Ok(data) -> Success(data)
        Err(reason) -> Failure(reason)
        Unknown -> Failure(UnknownResult)
```

**Why this translation:**
- Elixir tagged tuples map to Roc tags
- Pattern matching syntax is similar (`when` vs pattern match in function head)
- Tag unions make all cases explicit in type signature
- Type system ensures exhaustiveness (can't forget cases)

### Pattern 3: Pipe Operator

**Elixir:**
```elixir
def process_data(data) do
  data
  |> String.trim()
  |> String.downcase()
  |> String.split(",")
  |> Enum.map(&String.trim/1)
  |> Enum.reject(&(&1 == ""))
end
```

**Roc:**
```roc
processData : Str -> List Str
processData = \data ->
    data
    |> Str.trim
    |> Str.toLowercase
    |> Str.split(",")
    |> List.map(Str.trim)
    |> List.keepIf(\s -> s != "")
```

**Why this translation:**
- Both languages have pipe operators with similar semantics
- Roc uses `keepIf` instead of `reject` with negated predicate
- Capture operator `&` in Elixir becomes explicit lambdas in Roc
- Type inference works similarly in both

### Pattern 4: Enum Operations

**Elixir:**
```elixir
def sum(list), do: Enum.reduce(list, 0, &+/2)

def squares(list), do: Enum.map(list, fn x -> x * x end)

def evens(list), do: Enum.filter(list, fn x -> rem(x, 2) == 0 end)

def find_first_large(list) do
  Enum.find(list, fn x -> x > 100 end)
end
```

**Roc:**
```roc
sum : List I64 -> I64
sum = \list ->
    List.walk(list, 0, Num.add)

squares : List I64 -> List I64
squares = \list ->
    List.map(list, \x -> x * x)

evens : List I64 -> List I64
evens = \list ->
    List.keepIf(list, \x -> x % 2 == 0)

findFirstLarge : List I64 -> [Some I64, None]
findFirstLarge = \list ->
    list
    |> List.findFirst(\x -> x > 100)
    |> Result.map(Some)
    |> Result.withDefault(None)
```

**Why this translation:**
- `Enum.reduce` becomes `List.walk` (fold)
- `Enum.filter` becomes `List.keepIf`
- `Enum.find` returns `Result`, needs conversion to option type
- Function captures (`&+/2`) become explicit function references (`Num.add`)
- Roc requires explicit handling of "not found" cases

### Pattern 5: Struct to Record

**Elixir:**
```elixir
defmodule User do
  defstruct [:name, :email, age: 0]

  def new(name, email) do
    %User{name: name, email: email}
  end

  def update_age(user, new_age) do
    %{user | age: new_age}
  end

  def greet(%User{name: name}), do: "Hello, #{name}!"
end
```

**Roc:**
```roc
interface User
    exposes [User, new, updateAge, greet]
    imports []

User : {
    name : Str,
    email : Str,
    age : U32,
}

new : Str, Str -> User
new = \name, email ->
    { name, email, age: 0 }

updateAge : User, U32 -> User
updateAge = \user, newAge ->
    { user & age: newAge }

greet : User -> Str
greet = \{ name } ->
    "Hello, \(name)!"
```

**Why this translation:**
- Elixir structs map directly to Roc records
- Record update syntax is similar (`%{user | age:}` vs `{ user & age:}`)
- Pattern matching on records works similarly
- Roc records are structural (no `__struct__` metadata)
- Default values in struct definition become default in constructor

### Pattern 6: GenServer → Pure State Machine

**Elixir:**
```elixir
defmodule Counter do
  use GenServer

  # Client API

  def start_link(initial_value) do
    GenServer.start_link(__MODULE__, initial_value, name: __MODULE__)
  end

  def increment do
    GenServer.cast(__MODULE__, :increment)
  end

  def get do
    GenServer.call(__MODULE__, :get)
  end

  # Server Callbacks

  @impl true
  def init(initial_value) do
    {:ok, initial_value}
  end

  @impl true
  def handle_call(:get, _from, state) do
    {:reply, state, state}
  end

  @impl true
  def handle_cast(:increment, state) do
    {:noreply, state + 1}
  end
end
```

**Roc:**
```roc
# Pure state machine - no processes
interface Counter
    exposes [State, init, increment, get]
    imports []

State : I64

init : State
init = 0

increment : State -> State
increment = \count ->
    count + 1

get : State -> I64
get = \count ->
    count

# If you need effects, use platform Tasks
# The platform would provide state management and concurrency
# Application code remains pure
```

**Why this translation:**
- GenServer becomes pure state functions
- No process lifecycle - just data transformation
- State is explicit parameter and return value
- `call` operations become synchronous functions that return new state
- `cast` operations become functions that just transform state
- Effects and concurrency are platform responsibilities, not shown here
- Platform provides state management if needed

### Pattern 7: With Statement Error Handling

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

**Roc:**
```roc
createUser : Params -> Result User [ValidationErr, InsertErr, EmailErr]
createUser = \params ->
    validated = validateParams!(params)
    user = insertUser!(validated)
    _email = sendWelcomeEmail!(user)
    Ok(user)
```

**Why this translation:**
- Elixir `with` becomes Roc `!` operator (try/propagate)
- `!` suffix propagates errors automatically
- Error types are unified in tag union
- Early return on error is implicit with `!`
- More concise than explicit pattern matching

### Pattern 8: Optional Values

**Elixir:**
```elixir
def find_user(id, users) do
  Enum.find(users, fn user -> user.id == id end)
end

def get_email(nil), do: "no email"
def get_email(user), do: user.email

# Using in pipeline
def display_email(id, users) do
  users
  |> find_user(id)
  |> case do
    nil -> "User not found"
    user -> user.email
  end
end
```

**Roc:**
```roc
findUser : U64, List User -> [Some User, None]
findUser = \id, users ->
    users
    |> List.findFirst(\user -> user.id == id)
    |> Result.map(Some)
    |> Result.withDefault(None)

getEmail : [Some User, None] -> Str
getEmail = \maybeUser ->
    when maybeUser is
        Some({ email }) -> email
        None -> "no email"

displayEmail : U64, List User -> Str
displayEmail = \id, users ->
    when findUser(id, users) is
        Some(user) -> user.email
        None -> "User not found"
```

**Why this translation:**
- Elixir `nil` maps to `None` in tag union
- `Enum.find` returns `nil` or value; Roc `findFirst` returns `Result`
- Explicit pattern matching on option types
- Type system prevents forgetting to handle `None` case
- Must convert `Result` to option type with `Some`/`None`

### Pattern 9: List Comprehensions

**Elixir:**
```elixir
def squares(list) do
  for x <- list, do: x * x
end

def evens(list) do
  for x <- list, rem(x, 2) == 0, do: x
end

def cartesian_product(list1, list2) do
  for x <- list1, y <- list2, do: {x, y}
end

def filtered_map(list) do
  for x <- list, x > 0, into: %{}, do: {x, x * x}
end
```

**Roc:**
```roc
squares : List I64 -> List I64
squares = \list ->
    List.map(list, \x -> x * x)

evens : List I64 -> List I64
evens = \list ->
    List.keepIf(list, \x -> x % 2 == 0)

cartesianProduct : List a, List b -> List (a, b)
cartesianProduct = \list1, list2 ->
    List.joinMap(list1, \x ->
        List.map(list2, \y -> (x, y))
    )

filteredMap : List I64 -> Dict I64 I64
filteredMap = \list ->
    list
    |> List.keepIf(\x -> x > 0)
    |> List.map(\x -> (x, x * x))
    |> Dict.fromList
```

**Why this translation:**
- Comprehensions become `map`/`keepIf` operations
- Nested comprehensions use `joinMap` (flatMap/concatMap)
- Filters become `keepIf`
- `into: %{}` becomes `Dict.fromList`
- More verbose but explicit
- Type signatures make intent clear

### Pattern 10: Protocol Implementation

**Elixir:**
```elixir
defprotocol Serializable do
  @doc "Serialize to JSON"
  def to_json(data)
end

defimpl Serializable, for: Map do
  def to_json(map) do
    Jason.encode!(map)
  end
end

defimpl Serializable, for: List do
  def to_json(list) do
    Jason.encode!(list)
  end
end

# Usage
Serializable.to_json(%{name: "Alice"})
```

**Roc:**
```roc
# Roc uses abilities (similar to typeclasses)
# Built-in Encode ability is auto-derived for most types

# For custom encoding:
toJson : a -> Str where a implements Encode
toJson = \value ->
    value
    |> Encode.toBytes(Json.utf8)
    |> Str.fromUtf8

# Automatic for records and tags
user = { name: "Alice", age: 30 }
json = toJson(user)  # Works automatically

# For custom types with specific behavior:
User := { name : Str, age : U32 }

toJsonUser : User -> Str
toJsonUser = \@User({ name, age }) ->
    """
    {\"name\": \"\(name)\", \"age\": \(Num.toStr(age))}
    """
```

**Why this translation:**
- Elixir protocols map to Roc abilities
- Many abilities are auto-derived (Encode, Decode, Eq, Hash, Inspect)
- For custom behavior, write explicit functions
- No dynamic dispatch in Roc - abilities are compile-time
- Roc's approach is more restrictive but type-safe

---

## Concurrency Patterns

### Elixir Process Model vs Roc Task Model

Elixir's concurrency is built on lightweight BEAM processes with message passing. Roc has no built-in concurrency - it's all platform-provided through Tasks.

**Mental Model Shift:**

| Elixir Concept | Roc Approach | Key Insight |
|----------------|--------------|-------------|
| Process with state | Pure state machine + platform Task | Data and behavior separated |
| Message passing | Function parameters and results | Explicit data flow, no mailboxes |
| `spawn` | Platform Task creation | Effects are platform capability |
| GenServer | Pure functions + Task orchestration | Business logic pure, I/O delegated |
| Supervisor | Platform-level concern | Fault tolerance in host |
| Hot code reload | Not available | Platform restart required |

### Pattern: Spawned Task

**Elixir:**
```elixir
defmodule Worker do
  def start do
    spawn(fn -> loop() end)
  end

  defp loop do
    receive do
      {:work, from, data} ->
        result = process(data)
        send(from, {:result, result})
        loop()
      :stop ->
        :ok
    end
  end

  defp process(data), do: String.upcase(data)
end

# Usage
pid = Worker.start()
send(pid, {:work, self(), "hello"})
receive do
  {:result, result} -> IO.puts(result)
end
```

**Roc:**
```roc
# Pure processing function
process : Str -> Str
process = \data ->
    Str.toUppercase(data)

# If concurrency is needed, platform provides it
import pf.Task exposing [Task]

processAsync : Str -> Task Str []
processAsync = \data ->
    # Platform handles concurrent execution
    Task.await(Task.fromThunk(\{} -> process(data)))

# Usage (in Task context)
main : Task {} []
main =
    result = processAsync!("hello")
    Stdout.line!(result)
```

**Why this translation:**
- No process spawning in Roc - platform handles concurrency
- Pure function for business logic (`process`)
- Platform Task for effects
- No message passing - direct function composition
- Platform decides execution strategy (sync/async/parallel)

### Pattern: GenServer State

**Elixir:**
```elixir
defmodule Cache do
  use GenServer

  def start_link do
    GenServer.start_link(__MODULE__, %{}, name: __MODULE__)
  end

  def get(key) do
    GenServer.call(__MODULE__, {:get, key})
  end

  def put(key, value) do
    GenServer.cast(__MODULE__, {:put, key, value})
  end

  @impl true
  def init(_), do: {:ok, %{}}

  @impl true
  def handle_call({:get, key}, _from, state) do
    {:reply, Map.get(state, key), state}
  end

  @impl true
  def handle_cast({:put, key, value}, state) do
    {:noreply, Map.put(state, key, value)}
  end
end
```

**Roc:**
```roc
# Pure state functions
State : Dict Str Str

init : State
init = Dict.empty({})

get : State, Str -> [Some Str, None]
get = \state, key ->
    Dict.get(state, key)
    |> Result.map(Some)
    |> Result.withDefault(None)

put : State, Str, Str -> State
put = \state, key, value ->
    Dict.insert(state, key, value)

# Platform would provide state management
# For example, a hypothetical Agent-like platform API:
#
# import pf.Agent exposing [Agent, start, getState, updateState]
#
# cacheAgent : Agent State
# cacheAgent = start(init)
#
# getValue : Str -> Task [Some Str, None] []
# getValue = \key ->
#     Agent.getState(cacheAgent, \state -> get(state, key))
#
# putValue : Str, Str -> Task {} []
# putValue = \key, value ->
#     Agent.updateState(cacheAgent, \state -> put(state, key, value))
```

**Why this translation:**
- GenServer becomes pure state transformations
- State management delegated to platform (Agent, Store, etc.)
- No process registered names - platform handles references
- No `call` vs `cast` distinction - just sync vs async Task
- Fault tolerance handled by platform, not supervision tree

### Pattern: Task.async

**Elixir:**
```elixir
def fetch_multiple(urls) do
  tasks = Enum.map(urls, fn url ->
    Task.async(fn -> fetch_url(url) end)
  end)

  Task.await_many(tasks, 5000)
end

defp fetch_url(url) do
  case HTTPoison.get(url) do
    {:ok, %{body: body}} -> {:ok, body}
    {:error, reason} -> {:error, reason}
  end
end
```

**Roc:**
```roc
import pf.Http
import pf.Task exposing [Task]

fetchMultiple : List Str -> Task (List Str) [HttpErr]
fetchMultiple = \urls ->
    urls
    |> List.map(\url -> Http.get(url))
    |> Task.sequence  # Platform may execute concurrently
    |> Task.map(\responses -> List.map(responses, \r -> r.body))

# Platform-specific concurrent execution
# Some platforms may provide parallel primitives:
# fetchMultipleParallel : List Str -> Task (List Str) [HttpErr]
# fetchMultipleParallel = \urls ->
#     Task.parallel(List.map(urls, Http.get))
```

**Why this translation:**
- `Task.async` maps to platform Task creation
- Platform decides concurrency strategy
- `Task.sequence` combines multiple Tasks
- Timeout is platform-specific (may be in Task API)
- No separate "await" - composition with `!` or `Task.map`

### Pattern: Agent State

**Elixir:**
```elixir
defmodule Counter do
  use Agent

  def start_link(_opts) do
    Agent.start_link(fn -> 0 end, name: __MODULE__)
  end

  def increment do
    Agent.update(__MODULE__, &(&1 + 1))
  end

  def get do
    Agent.get(__MODULE__, & &1)
  end
end
```

**Roc:**
```roc
# Pure state functions
State : I64

init : State
init = 0

increment : State -> State
increment = \count -> count + 1

get : State -> I64
get = \count -> count

# Hypothetical platform API for stateful agents
# (actual API depends on platform)
#
# import pf.Agent exposing [Agent]
#
# counterAgent : Agent State
# counterAgent = Agent.start(init)
#
# incrementCounter : Task {} []
# incrementCounter =
#     Agent.update(counterAgent, increment)
#
# getCounter : Task I64 []
# getCounter =
#     Agent.get(counterAgent, get)
```

**Why this translation:**
- Agent pattern becomes pure state + platform state management
- No global registered names - agent references are explicit
- Updates are explicit functions, not anonymous lambdas
- Platform provides concurrency-safe state updates
- Business logic (increment, get) remains pure and testable

---

## Error Handling

### Elixir Error Model → Roc Result Type

| Elixir Pattern | Roc Pattern | Translation Strategy |
|----------------|-------------|----------------------|
| `{:ok, value}` | `Ok(value)` | Direct mapping |
| `{:error, reason}` | `Err(reason)` | Direct mapping |
| `raise/1` | `Err` variant | No exceptions in Roc |
| `rescue` clause | Pattern match on `Result` | Explicit error handling |
| `try/rescue` | `Result` combinators | Compose with `Result.try`, `Result.map` |
| Multiple error tuples | Tag union error type | `[Err1, Err2, Err3]` |
| `!` (bang) functions | Regular functions returning `Result` | All errors explicit |

### Pattern: Error Propagation

**Elixir:**
```elixir
def calculate(a, b, c) do
  with {:ok, x} <- divide(a, b),
       {:ok, y} <- divide(x, c) do
    {:ok, y}
  else
    {:error, reason} -> {:error, reason}
  end
end

# Or using the ! convention:
def calculate!(a, b, c) do
  x = divide!(a, b)
  y = divide!(x, c)
  y
end
```

**Roc:**
```roc
calculate : I64, I64, I64 -> Result I64 [DivByZero]
calculate = \a, b, c ->
    x = divide!(a, b)  # Propagates error automatically
    y = divide!(x, c)
    Ok(y)

# Or explicitly:
calculateExplicit : I64, I64, I64 -> Result I64 [DivByZero]
calculateExplicit = \a, b, c ->
    divide(a, b)
    |> Result.try(\x ->
        divide(x, c)
    )
```

**Why this translation:**
- Elixir `with` becomes Roc `!` operator
- `!` in Roc is try/propagate (not unwrap/crash like Elixir!)
- Both patterns allow early return on error
- Roc's approach is more concise
- Type system ensures all errors are handled

### Pattern: Multiple Error Types

**Elixir:**
```elixir
defmodule Parser do
  def parse_and_save(input) do
    with {:ok, data} <- parse(input),
         {:ok, validated} <- validate(data),
         :ok <- save(validated) do
      {:ok, validated}
    else
      {:error, :invalid_format} -> {:error, "Invalid format"}
      {:error, :validation_failed, msg} -> {:error, "Validation: #{msg}"}
      {:error, :save_failed} -> {:error, "Could not save"}
    end
  end
end
```

**Roc:**
```roc
parseAndSave : Str -> Result Data [InvalidFormat, ValidationFailed Str, SaveFailed]
parseAndSave = \input ->
    data = parse!(input)  # Returns Result Data [InvalidFormat]
    validated = validate!(data)  # Returns Result Data [ValidationFailed Str]
    save!(validated)  # Returns Result {} [SaveFailed]
    Ok(validated)

# Error handling with descriptive messages
parseAndSaveWithMsg : Str -> Result Data Str
parseAndSaveWithMsg = \input ->
    parseAndSave(input)
    |> Result.mapErr(\err ->
        when err is
            InvalidFormat -> "Invalid format"
            ValidationFailed(msg) -> "Validation: \(msg)"
            SaveFailed -> "Could not save"
    )
```

**Why this translation:**
- Elixir error atoms map to Roc tag variants
- Error payloads become tag parameters
- `!` operator unifies error types automatically
- `Result.mapErr` converts to user-friendly messages
- Type signature documents all possible errors

### Pattern: Raise and Rescue

**Elixir:**
```elixir
def process_file(path) do
  content = File.read!(path)  # Raises on error
  parse(content)
rescue
  e in File.Error -> {:error, "File error: #{e.message}"}
  e in ArgumentError -> {:error, "Invalid arguments"}
end

# Safer alternative
def process_file_safe(path) do
  case File.read(path) do
    {:ok, content} -> parse(content)
    {:error, reason} -> {:error, "File error: #{inspect(reason)}"}
  end
end
```

**Roc:**
```roc
# Roc has no exceptions - all errors are Result types
import pf.File

processFile : Str -> Result Data [FileErr Str, ParseErr]
processFile = \path ->
    content = File.readUtf8!(path)  # ! propagates error
    parse!(content)

# Explicit error handling
processFileExplicit : Str -> Result Data Str
processFileExplicit = \path ->
    when File.readUtf8(path) is
        Ok(content) ->
            when parse(content) is
                Ok(data) -> Ok(data)
                Err(ParseErr) -> Err("Parse error")
        Err(err) -> Err("File error: \(File.errorToStr(err))")
```

**Why this translation:**
- No `raise`/`rescue` in Roc - all errors are values
- File I/O returns `Result`, never throws
- Bang functions in Roc propagate errors (not panic like Elixir)
- Error handling is always explicit
- Can't forget to handle errors (type system enforces)

---

## Metaprogramming

### Elixir Macros → Roc Alternatives

Roc has no macro system. Elixir's metaprogramming capabilities must be replaced with alternative patterns.

| Elixir Feature | Roc Alternative | Notes |
|----------------|-----------------|-------|
| `defmacro` | External codegen | Build-time code generation |
| `use Module` | Interface composition | Import and compose interfaces |
| `quote` / `unquote` | - | Not available |
| Protocols | Abilities | Auto-derivation, compile-time |
| `@derive` | Automatic | Most abilities auto-derived |
| Compile-time code gen | Build scripts | External tools generate Roc |
| AST manipulation | - | Not supported |

### Pattern: Use Directive

**Elixir:**
```elixir
defmodule MyGenServer do
  use GenServer  # Injects callbacks and helpers

  @impl true
  def init(state), do: {:ok, state}

  @impl true
  def handle_call(:get, _from, state) do
    {:reply, state, state}
  end
end
```

**Roc:**
```roc
# No macro injection - explicit structure
interface MyServer
    exposes [State, init, handleGet]
    imports []

State : I64

init : I64 -> State
init = \initialValue -> initialValue

handleGet : State -> (I64, State)
handleGet = \state ->
    (state, state)

# Platform would provide GenServer-like behavior
# but without macro magic - explicit function signatures
```

**Why this translation:**
- No compile-time code injection in Roc
- All functions are explicit
- Behavior is defined by interface contract, not macros
- Platform provides runtime, application provides logic
- More verbose but clearer

### Pattern: Protocol Derivation

**Elixir:**
```elixir
defmodule User do
  @derive {Jason.Encoder, only: [:name, :email]}
  @derive Jason.Decoder

  defstruct [:name, :email, :age]
end

# Automatic implementation
Jason.encode!(%User{name: "Alice", email: "alice@example.com", age: 30})
```

**Roc:**
```roc
# Abilities are auto-derived for most types
User : {
    name : Str,
    email : Str,
    age : U32,
}

# Encode/Decode automatically available
user = { name: "Alice", email: "alice@example.com", age: 30 }
encoded = Encode.toBytes(user, Json.utf8)

# For custom encoding (rare):
encodeUser : User -> List U8
encodeUser = \{ name, email, age } ->
    # Manual JSON construction if needed
    jsonStr = """
    {"name":"\(name)","email":"\(email)","age":\(Num.toStr(age))}
    """
    Str.toUtf8(jsonStr)
```

**Why this translation:**
- Most abilities (Eq, Hash, Inspect, Encode, Decode) auto-derived
- No need for `@derive` - happens automatically
- Custom encoding requires explicit functions
- More restrictive but simpler
- No runtime overhead (compile-time derivation)

### Pattern: Compile-Time Configuration

**Elixir:**
```elixir
defmodule MyApp do
  @api_url Application.compile_env(:my_app, :api_url, "https://default.com")

  def fetch_data do
    HTTPoison.get(@api_url <> "/data")
  end
end
```

**Roc:**
```roc
# No compile-time config in language
# Use build scripts or environment-specific modules

# Option 1: Separate config modules (build-time switch)
# config/prod.roc
apiUrl : Str
apiUrl = "https://prod.com"

# config/dev.roc
apiUrl : Str
apiUrl = "https://dev.com"

# Option 2: Platform environment variables
import pf.Env

fetchData : Task Response [HttpErr, EnvErr]
fetchData =
    apiUrl = Env.var!("API_URL")  # Runtime config
    Http.get("\(apiUrl)/data")

# Option 3: External codegen
# Build script generates config.roc from environment
```

**Why this translation:**
- No compile-time metaprogramming in Roc
- Config is either build-time (separate modules) or runtime (Env vars)
- External tools can generate Roc modules
- Simpler language, more predictable builds
- Clear separation of build vs runtime config

### Pattern: Macros for DSLs

**Elixir:**
```elixir
defmodule Router do
  import MyWeb.Router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
  end

  scope "/", MyWeb do
    pipe_through :browser

    get "/", PageController, :index
    get "/users/:id", UserController, :show
  end
end
```

**Roc:**
```roc
# No DSL macros - use plain data structures
Route : {
    method : [Get, Post, Put, Delete],
    path : Str,
    handler : Request -> Task Response [],
}

Pipeline : List (Request -> Task Request [])

browserPipeline : Pipeline
browserPipeline = [
    acceptsHtml,
    fetchSession,
]

routes : List Route
routes = [
    { method: Get, path: "/", handler: pageIndex },
    { method: Get, path: "/users/:id", handler: userShow },
]

# Platform provides routing engine that interprets data
# No macros needed - just data and functions
```

**Why this translation:**
- DSLs become data structures
- Macros become data transformation functions
- Platform interprets routing data
- More verbose but explicit
- Easier to reason about (no compile-time magic)

---

## Module System Translation

### Elixir Modules → Roc Interfaces

| Elixir | Roc | Notes |
|--------|-----|-------|
| `defmodule` | `interface` | Module declaration |
| `@moduledoc` | Doc comments `##` | Module documentation |
| `@doc` | Doc comments `##` | Function documentation |
| `def` (public) | In `exposes` list | Public functions |
| `defp` (private) | Not in `exposes` | Private functions |
| `import` | `import` | Import modules |
| `alias` | - | Roc uses full names |
| `use` | - | No macro injection |

### Pattern: Module Organization

**Elixir:**
```elixir
# lib/my_app/accounts/user.ex
defmodule MyApp.Accounts.User do
  @moduledoc """
  User account management.
  """

  defstruct [:name, :email, :age]

  @doc "Create a new user"
  def new(name, email) do
    %__MODULE__{name: name, email: email, age: 0}
  end

  @doc "Update user age"
  def update_age(user, age) do
    %{user | age: age}
  end

  defp validate(user), do: # ...
end

# lib/my_app/accounts.ex
defmodule MyApp.Accounts do
  alias MyApp.Accounts.User

  def create_user(name, email) do
    User.new(name, email)
  end
end
```

**Roc:**
```roc
# MyApp/Accounts/User.roc
## User account management
interface User
    exposes [User, new, updateAge]
    imports []

User : {
    name : Str,
    email : Str,
    age : U32,
}

## Create a new user
new : Str, Str -> User
new = \name, email ->
    { name, email, age: 0 }

## Update user age
updateAge : User, U32 -> User
updateAge = \user, age ->
    { user & age }

# Private function (not exposed)
validate : User -> Bool
validate = \user -> # ...

# MyApp/Accounts.roc
interface Accounts
    exposes [createUser]
    imports [User]

createUser : Str, Str -> User.User
createUser = \name, email ->
    User.new(name, email)
```

**Why this translation:**
- File structure mirrors namespace
- Interfaces replace modules
- `exposes` replaces public `def`
- Documentation uses `##` comments
- Imports are explicit (no `alias` shorthand)
- Nested namespaces use directory structure

### Pattern: Behaviours and Callbacks

**Elixir:**
```elixir
defmodule MyBehaviour do
  @callback handle(term()) :: {:ok, term()} | {:error, term()}
  @callback init(term()) :: {:ok, term()}
end

defmodule MyImplementation do
  @behaviour MyBehaviour

  @impl true
  def init(config), do: {:ok, config}

  @impl true
  def handle(data), do: {:ok, process(data)}

  defp process(data), do: data
end
```

**Roc:**
```roc
# Behaviours become ability constraints or explicit interfaces

# Option 1: Ability (for polymorphism)
Handler implements
    handle : a, Request -> Result Response Err where a implements Handler
    init : Config -> Result a Err where a implements Handler

# Option 2: Interface contract (simpler, common case)
interface MyHandler
    exposes [State, init, handle]
    imports []

State : { config : Config }

init : Config -> Result State Err
init = \config -> Ok({ config })

handle : State, Request -> Result Response Err
handle = \state, request ->
    Ok(process(request))

# Private
process : Request -> Response
process = \request -> # ...
```

**Why this translation:**
- Behaviours map to abilities (for polymorphism) or interfaces (simpler)
- No `@impl` annotations needed (type system checks)
- Callbacks become function signatures in interface
- Type system ensures implementation matches contract
- More restrictive but type-safe

---

## Testing Strategy

### Elixir ExUnit → Roc Expect

| Elixir | Roc | Notes |
|--------|-----|-------|
| `ExUnit.Case` | `expect` statements | Inline tests |
| `test "..."` | `expect ...` | No test names |
| `assert` | `expect x == y` | Boolean expressions |
| `refute` | `expect !(x == y)` | Negation |
| `setup` | - | No test lifecycle hooks |
| `describe` | Comments `#` | Organizational comments |
| Doctest | `expect` in docs | Inline in documentation |
| `assert_receive` | - | No message-based testing |

### Pattern: Basic Testing

**Elixir:**
```elixir
defmodule MathUtilsTest do
  use ExUnit.Case

  describe "add/2" do
    test "adds two positive numbers" do
      assert MathUtils.add(2, 3) == 5
    end

    test "adds negative numbers" do
      assert MathUtils.add(-1, 1) == 0
    end
  end

  describe "divide/2" do
    test "divides successfully" do
      assert MathUtils.divide(10, 2) == {:ok, 5.0}
    end

    test "returns error on division by zero" do
      assert MathUtils.divide(10, 0) == {:error, :division_by_zero}
    end
  end
end
```

**Roc:**
```roc
interface MathUtils
    exposes [add, divide]
    imports []

add : I64, I64 -> I64
add = \a, b -> a + b

# Tests for add
expect add(2, 3) == 5
expect add(-1, 1) == 0
expect add(0, 0) == 0

divide : F64, F64 -> Result F64 [DivisionByZero]
divide = \a, b ->
    if b == 0 then
        Err(DivisionByZero)
    else
        Ok(a / b)

# Tests for divide
expect divide(10, 2) == Ok(5.0)
expect divide(10, 0) == Err(DivisionByZero)
expect
    when divide(20, 4) is
        Ok(result) -> result == 5.0
        Err(_) -> Bool.false
```

**Why this translation:**
- No test framework setup needed
- `expect` statements run with `roc test`
- No test names - expectations speak for themselves
- Inline with code (closer to doctest philosophy)
- Can use pattern matching in expects

### Pattern: Doctests

**Elixir:**
```elixir
defmodule Calculator do
  @doc """
  Adds two numbers.

  ## Examples

      iex> Calculator.add(2, 3)
      5

      iex> Calculator.add(-1, 1)
      0
  """
  def add(a, b), do: a + b
end
```

**Roc:**
```roc
interface Calculator
    exposes [add]
    imports []

## Adds two numbers.
##
## Examples:
##
## ```
## expect add(2, 3) == 5
## expect add(-1, 1) == 0
## ```
add : I64, I64 -> I64
add = \a, b -> a + b

# Actual test expectations (run with roc test)
expect add(2, 3) == 5
expect add(-1, 1) == 0
```

**Why this translation:**
- Documentation includes example `expect` statements
- Actual tests are separate `expect` statements
- No special doctest syntax
- Examples in docs can be copy-pasted as tests
- Simpler mental model

### Pattern: Setup and Teardown

**Elixir:**
```elixir
defmodule DatabaseTest do
  use ExUnit.Case

  setup do
    {:ok, conn} = Database.connect()
    on_exit(fn -> Database.disconnect(conn) end)
    {:ok, conn: conn}
  end

  test "inserts user", %{conn: conn} do
    assert {:ok, user} = Database.insert(conn, %User{name: "Alice"})
    assert user.name == "Alice"
  end
end
```

**Roc:**
```roc
# No setup/teardown in Roc tests
# Tests are pure - create test data inline

interface Database
    exposes [connect, disconnect, insert, User]
    imports []

User : { name : Str }

# Tests create their own state
expect
    conn = testConnection  # Helper for test connections
    user = insert(conn, { name: "Alice" })
    when user is
        Ok(u) -> u.name == "Alice"
        Err(_) -> Bool.false

# Helper for test data
testConnection : Connection
testConnection = # Create test connection
```

**Why this translation:**
- No setup/teardown hooks
- Tests are pure functions
- Create test data inline or with helper functions
- No shared mutable state between tests
- Simpler but requires more explicit test data creation

### Pattern: Property-Based Testing

**Elixir:**
```elixir
defmodule StringPropertiesTest do
  use ExUnit.Case
  use ExUnitProperties

  property "reversing twice returns original" do
    check all string <- string(:printable) do
      assert string |> String.reverse() |> String.reverse() == string
    end
  end

  property "length is preserved when reversing" do
    check all string <- string(:alphanumeric) do
      assert String.length(string) == String.length(String.reverse(string))
    end
  end
end
```

**Roc:**
```roc
# Roc doesn't have built-in property-based testing yet
# Write tests for specific cases or use external tools

# Specific test cases
expect
    str = "hello"
    str == (str |> Str.reverse |> Str.reverse)

expect
    str = "Roc Lang"
    str == (str |> Str.reverse |> Str.reverse)

expect
    str = ""
    str == (str |> Str.reverse |> Str.reverse)

# Length preservation
expect
    str = "testing"
    Str.countUtf8Bytes(str) == Str.countUtf8Bytes(Str.reverse(str))
```

**Why this translation:**
- No built-in property-based testing library yet
- Write representative test cases manually
- Consider external codegen for test generation
- Simpler but less comprehensive
- May evolve as ecosystem matures

---

## Build System and Dependencies

### Mix → Roc Platform System

| Elixir (Mix) | Roc | Notes |
|--------------|-----|-------|
| `mix.exs` | `app` / `package` header | Project definition |
| `deps` | Platform URL | Dependencies via platforms |
| `mix deps.get` | Automatic | Platforms fetched automatically |
| `mix compile` | `roc build` | Build command |
| `mix test` | `roc test` | Test runner |
| `mix format` | `roc format` | Code formatter |
| `mix run` | `roc run` | Run application |

### Pattern: Project Configuration

**Elixir:**
```elixir
# mix.exs
defmodule MyApp.MixProject do
  use Mix.Project

  def project do
    [
      app: :my_app,
      version: "0.1.0",
      elixir: "~> 1.14",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger],
      mod: {MyApp.Application, []}
    ]
  end

  defp deps do
    [
      {:phoenix, "~> 1.7"},
      {:jason, "~> 1.4"},
      {:httpoison, "~> 2.0"}
    ]
  end
end
```

**Roc:**
```roc
# MyApp.roc - Application header
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.10.0/vNe6s9hWzoTZtFmNkvEICPErI9ptji_ySjicO6CkucY.tar.br"
}

import pf.Stdout
import pf.Task exposing [Task]

main : Task {} []
main =
    Stdout.line!("Hello, World!")

# No separate config file
# Platform URL includes all dependencies
# Version is embedded in URL hash
```

**Why this translation:**
- No `mix.exs` equivalent - project is defined in app header
- Dependencies come through platform (not direct package deps)
- Version pinning via URL hash
- Simpler dependency model but less flexible
- Platform provides cohesive set of APIs

### Pattern: Custom Mix Tasks

**Elixir:**
```elixir
# lib/mix/tasks/generate_docs.ex
defmodule Mix.Tasks.GenerateDocs do
  use Mix.Task

  @shortdoc "Generate custom documentation"

  def run(_args) do
    Mix.shell().info("Generating documentation...")
    # Custom logic
  end
end

# Usage: mix generate_docs
```

**Roc:**
```roc
# No mix task equivalent
# Use external build scripts or just/make

# Justfile
generate-docs:
    #!/usr/bin/env bash
    echo "Generating documentation..."
    roc run generate_docs.roc

# Or shell script: scripts/generate_docs.sh
#!/usr/bin/env bash
roc build docs_generator.roc
./docs_generator
```

**Why this translation:**
- No task system in Roc
- Use external build tools (just, make, shell scripts)
- Write Roc programs for custom tooling
- Platform provides basic commands only
- Simpler language, external orchestration

---

## Common Pitfalls

### 1. Process-Based Thinking in Pure Code

**Pitfall:**
```roc
# ❌ Trying to replicate GenServer with state
# This doesn't work - Roc has no processes
counter = 0  # Can't have mutable module-level state

increment = \{} ->
    counter = counter + 1  # Error: counter is not mutable
```

**Solution:**
```roc
# ✓ Use explicit state passing
State : I64

increment : State -> State
increment = \count -> count + 1

# State is passed explicitly, not hidden in process
# Platform provides state management if needed
```

### 2. Expecting Dynamic Types

**Pitfall:**
```roc
# ❌ Trying to use heterogeneous lists
users = [
    { name: "Alice", age: 30 },
    "Invalid user",  # Error: different type
    42,              # Error: different type
]
```

**Solution:**
```roc
# ✓ Use tag unions for variants
User : [Valid { name : Str, age : U32 }, Invalid Str, Unknown I64]

users : List User
users = [
    Valid({ name: "Alice", age: 30 }),
    Invalid("Invalid user"),
    Unknown(42),
]
```

### 3. Message Passing Patterns

**Pitfall:**
```roc
# ❌ Trying to use message passing
# No send/receive in Roc
send(pid, message)  # Error: no send function
```

**Solution:**
```roc
# ✓ Use function composition
# Messages become function parameters
handleMessage : Message -> State -> State
handleMessage = \msg, state ->
    when msg is
        Increment -> increment(state)
        Decrement -> decrement(state)
        Get -> state
```

### 4. Hot Code Loading Expectations

**Pitfall:**
Expecting to reload modules without restart (Elixir/BEAM feature).

**Solution:**
- Roc requires full program restart
- Design for stateless or externalizable state
- Use platform-level state persistence if needed
- Accept different deployment model

### 5. Macro-Heavy Code

**Pitfall:**
```elixir
# Elixir macro-heavy DSL
defmacro assert_valid(condition, message) do
  quote do
    unless unquote(condition) do
      raise ArgumentError, unquote(message)
    end
  end
end
```

**Solution:**
```roc
# ✓ Use plain functions
assertValid : Bool, Str -> Result {} [ValidationErr Str]
assertValid = \condition, message ->
    if condition then
        Ok({})
    else
        Err(ValidationErr(message))
```

### 6. nil vs None Confusion

**Pitfall:**
```roc
# ❌ Expecting nil to work like Elixir
user = nil  # Error: no nil value
```

**Solution:**
```roc
# ✓ Use tag unions for optional values
User : [Some { name : Str }, None]

user : User
user = None

# Or simpler:
MaybeUser : [Some { name : Str }, None]
```

### 7. String vs Atom Usage

**Pitfall:**
```roc
# ❌ Using strings where tags are better
status = "pending"  # Strings don't get exhaustiveness checking
```

**Solution:**
```roc
# ✓ Use tags for enumerations
Status : [Pending, Approved, Rejected]

status : Status
status = Pending

# Compiler ensures all cases handled
when status is
    Pending -> "waiting"
    Approved -> "done"
    Rejected -> "failed"
    # Forgot a case? Compiler error!
```

---

## Tooling

| Purpose | Elixir | Roc | Notes |
|---------|--------|-----|-------|
| Build | `mix compile` | `roc build` | Compile project |
| Run | `mix run` | `roc run` | Execute application |
| Test | `mix test` | `roc test` | Run tests |
| Format | `mix format` | `roc format` | Code formatting |
| REPL | `iex` | `roc repl` | Interactive shell |
| Docs | `mix docs` (ExDoc) | `roc docs` | Generate documentation |
| Dependency fetch | `mix deps.get` | Automatic | Platform URLs fetched automatically |
| Type checking | Dialyzer | Built-in | Type checking |
| Hot reload | `iex -S mix` | - | Not available in Roc |
| Code analysis | Credo | - | No equivalent yet |

---

## Examples

### Example 1: Simple - Basic List Processing

**Before (Elixir):**
```elixir
defmodule ListUtils do
  @doc "Sum all numbers in a list"
  def sum(list), do: Enum.reduce(list, 0, &+/2)

  @doc "Double all numbers in a list"
  def double(list), do: Enum.map(list, &(&1 * 2))

  @doc "Filter even numbers"
  def evens(list), do: Enum.filter(list, &(rem(&1, 2) == 0))
end

# Tests
ExUnit.start()

defmodule ListUtilsTest do
  use ExUnit.Case

  test "sum/1" do
    assert ListUtils.sum([1, 2, 3, 4, 5]) == 15
  end

  test "double/1" do
    assert ListUtils.double([1, 2, 3]) == [2, 4, 6]
  end

  test "evens/1" do
    assert ListUtils.evens([1, 2, 3, 4, 5]) == [2, 4]
  end
end
```

**After (Roc):**
```roc
interface ListUtils
    exposes [sum, double, evens]
    imports []

## Sum all numbers in a list
sum : List I64 -> I64
sum = \list ->
    List.walk(list, 0, Num.add)

## Double all numbers in a list
double : List I64 -> List I64
double = \list ->
    List.map(list, \x -> x * 2)

## Filter even numbers
evens : List I64 -> List I64
evens = \list ->
    List.keepIf(list, \x -> x % 2 == 0)

# Tests (inline)
expect sum([1, 2, 3, 4, 5]) == 15
expect double([1, 2, 3]) == [2, 4, 6]
expect evens([1, 2, 3, 4, 5]) == [2, 4]
```

### Example 2: Medium - Result Type and Error Handling

**Before (Elixir):**
```elixir
defmodule Calculator do
  @doc "Safely divide two numbers"
  def divide(a, b) when b != 0, do: {:ok, a / b}
  def divide(_, 0), do: {:error, :division_by_zero}

  @doc "Chain multiple divisions"
  def chain_divide(a, b, c) do
    with {:ok, x} <- divide(a, b),
         {:ok, y} <- divide(x, c) do
      {:ok, y}
    else
      {:error, reason} -> {:error, reason}
    end
  end

  @doc "Safely parse and divide"
  def parse_and_divide(a_str, b_str) do
    with {:ok, a} <- parse_int(a_str),
         {:ok, b} <- parse_int(b_str),
         {:ok, result} <- divide(a, b) do
      {:ok, result}
    else
      {:error, :invalid_integer} -> {:error, "Invalid number format"}
      {:error, :division_by_zero} -> {:error, "Cannot divide by zero"}
    end
  end

  defp parse_int(str) do
    case Integer.parse(str) do
      {int, ""} -> {:ok, int}
      _ -> {:error, :invalid_integer}
    end
  end
end

# Tests
defmodule CalculatorTest do
  use ExUnit.Case

  test "divide/2 success" do
    assert Calculator.divide(10, 2) == {:ok, 5.0}
  end

  test "divide/2 by zero" do
    assert Calculator.divide(10, 0) == {:error, :division_by_zero}
  end

  test "chain_divide/3" do
    assert Calculator.chain_divide(20, 2, 2) == {:ok, 5.0}
    assert Calculator.chain_divide(10, 0, 2) == {:error, :division_by_zero}
  end

  test "parse_and_divide/2" do
    assert Calculator.parse_and_divide("10", "2") == {:ok, 5.0}
    assert Calculator.parse_and_divide("abc", "2") == {:error, "Invalid number format"}
    assert Calculator.parse_and_divide("10", "0") == {:error, "Cannot divide by zero"}
  end
end
```

**After (Roc):**
```roc
interface Calculator
    exposes [divide, chainDivide, parseAndDivide]
    imports []

## Safely divide two numbers
divide : F64, F64 -> Result F64 [DivisionByZero]
divide = \a, b ->
    if b == 0 then
        Err(DivisionByZero)
    else
        Ok(a / b)

## Chain multiple divisions
chainDivide : F64, F64, F64 -> Result F64 [DivisionByZero]
chainDivide = \a, b, c ->
    x = divide!(a, b)  # ! propagates error
    y = divide!(x, c)
    Ok(y)

## Safely parse and divide
parseAndDivide : Str, Str -> Result F64 [InvalidInteger, DivisionByZero]
parseAndDivide = \aStr, bStr ->
    a = parseFloat!(aStr)  # Returns Result F64 [InvalidInteger]
    b = parseFloat!(bStr)
    divide!(a, b)

# Helper for parsing
parseFloat : Str -> Result F64 [InvalidInteger]
parseFloat = \str ->
    when Str.toF64(str) is
        Ok(num) -> Ok(num)
        Err(_) -> Err(InvalidInteger)

# Convert to user-friendly messages
parseAndDivideMsg : Str, Str -> Result F64 Str
parseAndDivideMsg = \aStr, bStr ->
    parseAndDivide(aStr, bStr)
    |> Result.mapErr(\err ->
        when err is
            InvalidInteger -> "Invalid number format"
            DivisionByZero -> "Cannot divide by zero"
    )

# Tests
expect divide(10, 2) == Ok(5.0)
expect divide(10, 0) == Err(DivisionByZero)
expect chainDivide(20, 2, 2) == Ok(5.0)
expect chainDivide(10, 0, 2) == Err(DivisionByZero)
expect
    when parseAndDivideMsg("10", "2") is
        Ok(result) -> result == 5.0
        Err(_) -> Bool.false
expect parseAndDivideMsg("abc", "2") == Err("Invalid number format")
expect parseAndDivideMsg("10", "0") == Err("Cannot divide by zero")
```

### Example 3: Complex - GenServer to Pure State Machine with Platform Tasks

**Before (Elixir):**
```elixir
defmodule UserCache do
  use GenServer

  # Client API

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, %{}, name: __MODULE__)
  end

  def get(user_id) do
    GenServer.call(__MODULE__, {:get, user_id})
  end

  def put(user_id, user) do
    GenServer.cast(__MODULE__, {:put, user_id, user})
  end

  def delete(user_id) do
    GenServer.cast(__MODULE__, {:delete, user_id})
  end

  def all_users do
    GenServer.call(__MODULE__, :all_users)
  end

  # Server Callbacks

  @impl true
  def init(_args) do
    {:ok, %{}}
  end

  @impl true
  def handle_call({:get, user_id}, _from, state) do
    {:reply, Map.get(state, user_id), state}
  end

  def handle_call(:all_users, _from, state) do
    {:reply, Map.values(state), state}
  end

  @impl true
  def handle_cast({:put, user_id, user}, state) do
    {:noreply, Map.put(state, user_id, user)}
  end

  def handle_cast({:delete, user_id}, state) do
    {:noreply, Map.delete(state, user_id)}
  end
end

# Supervision tree
defmodule MyApp.Application do
  use Application

  def start(_type, _args) do
    children = [
      UserCache
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end

# Tests
defmodule UserCacheTest do
  use ExUnit.Case

  setup do
    {:ok, _pid} = start_supervised(UserCache)
    :ok
  end

  test "get and put user" do
    user = %{name: "Alice", email: "alice@example.com"}

    :ok = UserCache.put(1, user)
    assert UserCache.get(1) == user
  end

  test "get non-existent user returns nil" do
    assert UserCache.get(999) == nil
  end

  test "delete user" do
    user = %{name: "Bob", email: "bob@example.com"}

    :ok = UserCache.put(2, user)
    assert UserCache.get(2) == user

    :ok = UserCache.delete(2)
    assert UserCache.get(2) == nil
  end

  test "all_users returns all cached users" do
    user1 = %{name: "Alice", email: "alice@example.com"}
    user2 = %{name: "Bob", email: "bob@example.com"}

    :ok = UserCache.put(1, user1)
    :ok = UserCache.put(2, user2)

    users = UserCache.all_users()
    assert length(users) == 2
    assert user1 in users
    assert user2 in users
  end
end
```

**After (Roc):**
```roc
# Pure state machine - no GenServer
interface UserCache
    exposes [
        State,
        User,
        init,
        get,
        put,
        delete,
        allUsers,
    ]
    imports []

User : {
    name : Str,
    email : Str,
}

State : Dict U64 User

## Initialize empty cache
init : State
init = Dict.empty({})

## Get user by ID
get : State, U64 -> [Some User, None]
get = \state, userId ->
    Dict.get(state, userId)
    |> Result.map(Some)
    |> Result.withDefault(None)

## Put user in cache
put : State, U64, User -> State
put = \state, userId, user ->
    Dict.insert(state, userId, user)

## Delete user from cache
delete : State, U64 -> State
delete = \state, userId ->
    Dict.remove(state, userId)

## Get all users
allUsers : State -> List User
allUsers = \state ->
    Dict.values(state)

# Tests
expect
    state = init
    user = { name: "Alice", email: "alice@example.com" }
    newState = put(state, 1, user)
    get(newState, 1) == Some(user)

expect
    state = init
    get(state, 999) == None

expect
    state = init
    user = { name: "Bob", email: "bob@example.com" }
    stateWithUser = put(state, 2, user)
    get(stateWithUser, 2) == Some(user)

    stateAfterDelete = delete(stateWithUser, 2)
    get(stateAfterDelete, 2) == None

expect
    state = init
    user1 = { name: "Alice", email: "alice@example.com" }
    user2 = { name: "Bob", email: "bob@example.com" }

    state
    |> put(1, user1)
    |> put(2, user2)
    |> allUsers
    |> List.len
    |> \len -> len == 2

# Hypothetical platform integration (if state management needed)
# This would be provided by the platform, not shown here:
#
# import pf.Agent exposing [Agent]
#
# cacheAgent : Agent State
# cacheAgent = Agent.start(init)
#
# getUser : U64 -> Task [Some User, None] []
# getUser = \userId ->
#     Agent.get(cacheAgent, \state -> get(state, userId))
#
# putUser : U64, User -> Task {} []
# putUser = \userId, user ->
#     Agent.update(cacheAgent, \state -> put(state, userId, user))
#
# deleteUser : U64 -> Task {} []
# deleteUser = \userId ->
#     Agent.update(cacheAgent, \state -> delete(state, userId))
#
# getAllUsers : Task (List User) []
# getAllUsers =
#     Agent.get(cacheAgent, allUsers)
```

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-erlang-roc` - Related BEAM → Roc conversion (similar paradigm shift)
- `lang-elixir-dev` - Elixir development patterns
- `lang-roc-dev` - Roc development patterns

Cross-cutting pattern skills (for areas not fully covered by lang-*-dev):
- `patterns-concurrency-dev` - Process model vs Task model comparison
- `patterns-serialization-dev` - JSON, validation across languages
- `patterns-metaprogramming-dev` - Macros vs abilities comparison
