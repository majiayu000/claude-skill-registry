---
name: convert-roc-elixir
description: Convert Roc code to idiomatic Elixir. Use when migrating Roc platform-based applications to Elixir/BEAM, translating statically-typed functional code to dynamic functional style, or refactoring compile-time verified patterns to leverage Elixir's actor model and OTP. Extends meta-convert-dev with Roc-to-Elixir specific patterns.
---

# Convert Roc to Elixir

Convert Roc code to idiomatic Elixir. This skill extends `meta-convert-dev` with Roc-to-Elixir specific type mappings, idiom translations, and tooling for translating from statically-typed platform-based architecture to dynamically-typed BEAM runtime with OTP.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Roc's static types → Elixir's dynamic types with optional specs
- **Idiom translations**: Compile-time verified patterns → runtime pattern matching
- **Error handling**: Result type with exhaustive matching → tagged tuples with case
- **Concurrency models**: Platform-managed Tasks → BEAM processes and OTP
- **Platform architecture**: Platform/application separation → Mix application with OTP tree
- **Paradigm shift**: Static functional with structural types → dynamic functional with protocols

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Roc language fundamentals - see `lang-roc-dev`
- Elixir language fundamentals - see `lang-elixir-dev`
- Reverse conversion (Elixir → Roc) - see `convert-elixir-roc`
- Roc platform development - focus is on Roc applications to Elixir/OTP

---

## Quick Reference

| Roc | Elixir | Notes |
|-----|--------|-------|
| `Str` | `String.t()` | UTF-8 strings (binary in Elixir) |
| `I64` / `U64` | `integer()` | Arbitrary precision in Elixir |
| `F64` | `float()` | 64-bit floating point |
| `Bool` | `boolean()` | true/false atoms |
| `[Some a, None]` | `{:ok, a} \| nil` | Optional values |
| `Result a err` | `{:ok, a} \| {:error, err}` | Result pattern |
| `List a` | `[a]` | Lists (different impl: indexed vs linked) |
| `{ field : Type }` | `%{field: value}` or `defstruct` | Records → maps or structs |
| `[TagA, TagB]` | `:tag_a \| :tag_b` | Tag unions → atoms |
| `TagA(payload)` | `{:tag_a, payload}` | Tags with data → tuples |
| `\x -> x` | `fn x -> x end` | Anonymous functions |
| `func : a -> b` | `@spec func(a) :: b` | Type signatures → specs |
| `when x is` | `case x do` | Pattern matching |
| `Task ok err` | `GenServer` or `Task` | Effects → processes/tasks |

---

## When Converting Code

1. **Analyze source thoroughly** - Understand Roc's platform model and static guarantees
2. **Map types first** - Convert static type signatures to @specs and guards
3. **Preserve semantics** - Functional purity mostly translates, add runtime validation
4. **Embrace BEAM** - Platform Tasks → OTP processes for concurrency and fault tolerance
5. **Adopt Elixir idioms** - Pattern matching, with statements, pipe operator, protocols
6. **Handle optionality** - Tag unions → tagged tuples, add nil handling
7. **Test equivalence** - Same inputs → same outputs, add property tests for static invariants
8. **Add supervision** - Roc's platform restart → OTP supervision trees

---

## Type System Mapping

### Primitive Types

| Roc | Elixir | Notes |
|-----|--------|-------|
| `Str` | `String.t()` | Both UTF-8, Elixir on binaries |
| `I8` / `I16` / `I32` / `I64` / `I128` | `integer()` | Elixir: arbitrary precision integers |
| `U8` / `U16` / `U32` / `U64` / `U128` | `non_neg_integer()` | Use guards for unsigned semantics |
| `F32` / `F64` | `float()` | 64-bit double precision |
| `Dec` | `Decimal.t()` (library) | Use `decimal` package for precision |
| `Bool` | `boolean()` | `true` / `false` atoms |
| `Num *` (inferred) | `number()` | Generic number type |

**Important differences:**
- Roc: Fixed-size integers with explicit overflow behavior
- Elixir: Arbitrary precision integers, no overflow
- Roc: Compile-time type inference
- Elixir: Runtime type checking via guards and pattern matching

### Collection Types

| Roc | Elixir | Notes |
|-----|--------|-------|
| `List a` | `[a]` | Roc: indexed access O(1); Elixir: linked list O(n) |
| `Set a` | `MapSet.t(a)` | Set implementations |
| `Dict k v` | `%{k => v}` | Hash maps |
| `(a, b)` | `{a, b}` | Tuples (2-element) |
| `(a, b, c)` | `{a, b, c}` | Tuples (3-element) |
| `Str` (bytes) | `binary()` | Byte sequences |

**Key difference:**
- Roc: Lists support efficient indexed access
- Elixir: Lists are linked lists; use tuples or arrays for indexed access

### Composite Types

| Roc | Elixir | Notes |
|-----|--------|-------|
| `{ name: Str, age: U32 }` | `%{name: String.t(), age: non_neg_integer()}` | Records → maps |
| Type alias `User : { ... }` | `defstruct [:name, :age]` or `@type` | Structs for typed data |
| `[Red, Yellow, Green]` | `:red \| :yellow \| :green` | Tags → atoms |
| `[Ok a, Err e]` | `{:ok, a} \| {:error, e}` | Result type → tagged tuples |
| `[Some a, None]` | `a \| nil` | Optional → nullable or tagged tuple |
| `TagA(a, b)` | `{:tag_a, a, b}` | Tags with payloads → tuples |

### Function Types

| Roc | Elixir | Notes |
|-----|--------|-------|
| `a -> b` | `@spec func(a) :: b` | Function signature → typespec |
| `a, b -> c` | `@spec func(a, b) :: c` | Multi-argument function |
| `(a -> b) -> c` | Higher-order function | Functions as values work similarly |
| `where a implements Eq` | No direct equivalent | Use protocols or runtime checks |

---

## Paradigm Translation

### Mental Model Shift: Roc/Platform → Elixir/BEAM

| Roc Concept | Elixir Approach | Key Insight |
|-------------|-----------------|-------------|
| Platform/Application separation | Mix application with OTP | Platform I/O → GenServer/Task processes |
| Structural types (records) | Structs with @type specs | Named vs anonymous data |
| Tag unions (exhaustive) | Atoms + pattern matching | Compiler checks → runtime patterns |
| Result type | Tagged tuples {:ok/:error} | Explicit → idiomatic convention |
| Abilities (traits) | Protocols | Polymorphism approaches differ |
| Compile-time verification | Runtime guards + dialyzer | Static → gradual typing |
| Tasks (platform effects) | Task/GenServer/Agent | Effects → actor model |
| Immutable by default | Immutable by default | Both functional, different impl |

### Concurrency Mental Model

| Roc Model | Elixir Model | Conceptual Translation |
|-----------|--------------|------------------------|
| Task (platform-managed) | GenServer/Agent | Effects → stateful processes |
| Sequential Tasks with `!` | GenServer.call chaining | Synchronous execution |
| Platform concurrency | spawn/Task.async | Platform handles → explicit processes |
| No shared state | Process isolation | Both message-passing |
| Platform supervision | OTP Supervisor | Restart policies explicit in Elixir |

---

## Idiom Translation

### Pattern: Tag Unions → Tagged Tuples

Roc uses tag unions for discriminated values. Elixir uses tagged tuples with atoms.

**Roc:**
```roc
# Define union type
Color : [Red, Yellow, Green, Custom(U8, U8, U8)]

# Pattern matching
colorName : Color -> Str
colorName = \color ->
    when color is
        Red -> "red"
        Yellow -> "yellow"
        Green -> "green"
        Custom(r, g, b) -> "rgb(#{Num.toStr(r)}, #{Num.toStr(g)}, #{Num.toStr(b)})"
```

**Elixir:**
```elixir
# Type specification
@type color :: :red | :yellow | :green | {:custom, non_neg_integer(), non_neg_integer(), non_neg_integer()}

# Pattern matching
@spec color_name(color()) :: String.t()
def color_name(color) do
  case color do
    :red -> "red"
    :yellow -> "yellow"
    :green -> "green"
    {:custom, r, g, b} -> "rgb(#{r}, #{g}, #{b})"
  end
end
```

**Why this translation:**
- Roc's exhaustive checking → Elixir relies on runtime pattern matching
- Tags → atoms (lightweight constants)
- Tags with payloads → tuples with atom tag as first element
- Add @type specs for documentation and dialyzer support

---

### Pattern: Result Type → Tagged Tuples

Roc's Result type maps directly to Elixir's {:ok, value} / {:error, reason} idiom.

**Roc:**
```roc
# Using Result type
divide : I64, I64 -> Result I64 [DivByZero]
divide = \a, b ->
    if b == 0 then
        Err(DivByZero)
    else
        Ok(a // b)

# Using try (!) for propagation
calculate : I64, I64, I64 -> Result I64 [DivByZero]
calculate = \a, b, c ->
    x = divide!(a, b)
    y = divide!(x, c)
    Ok(y)
```

**Elixir:**
```elixir
# Using tagged tuples
@spec divide(integer(), integer()) :: {:ok, integer()} | {:error, :division_by_zero}
def divide(a, b) when b != 0, do: {:ok, div(a, b)}
def divide(_, 0), do: {:error, :division_by_zero}

# Using with for error propagation
@spec calculate(integer(), integer(), integer()) :: {:ok, integer()} | {:error, :division_by_zero}
def calculate(a, b, c) do
  with {:ok, x} <- divide(a, b),
       {:ok, y} <- divide(x, c) do
    {:ok, y}
  end
end
```

**Why this translation:**
- Roc's `Result a err` → Elixir's `{:ok, a} | {:error, err}` convention
- Roc's `!` try operator → Elixir's `with` statement for chaining
- Both make error handling explicit in return types
- Elixir pattern matching handles missing cases at runtime

---

### Pattern: Records → Structs

Roc's structural records map to Elixir's structs for typed data.

**Roc:**
```roc
# Record type
User : {
    name : Str,
    email : Str,
    age : U32,
}

# Creating records
user : User
user = { name: "Alice", email: "alice@example.com", age: 30 }

# Updating records
updatedUser = { user & age: 31 }

# Pattern matching
getName : User -> Str
getName = \{ name } -> name
```

**Elixir:**
```elixir
# Define struct
defmodule User do
  @type t :: %__MODULE__{
    name: String.t(),
    email: String.t(),
    age: non_neg_integer()
  }

  defstruct [:name, :email, :age]
end

# Creating structs
user = %User{name: "Alice", email: "alice@example.com", age: 30}

# Updating structs
updated_user = %{user | age: 31}

# Pattern matching
@spec get_name(User.t()) :: String.t()
def get_name(%User{name: name}), do: name
```

**Why this translation:**
- Roc's structural records → Elixir's named structs
- Record update syntax `{ r & field: value }` → `%{struct | field: value}`
- Pattern matching syntax similar in both
- Add @type for documentation and static analysis

---

### Pattern: Abilities → Protocols

Roc's ability system (type classes) translates to Elixir's protocols.

**Roc:**
```roc
# Using Inspect ability
debug : a -> Str where a implements Inspect
debug = \value ->
    Inspect.toStr(value)

# Using Eq ability
areEqual : a, a -> Bool where a implements Eq
areEqual = \x, y ->
    x == y
```

**Elixir:**
```elixir
# Using String.Chars protocol (similar to Inspect)
@spec debug(term()) :: String.t()
def debug(value) do
  inspect(value)
end

# Equality is built-in for all terms
@spec are_equal(term(), term()) :: boolean()
def are_equal(x, y), do: x == y

# Custom protocol
defprotocol Serializable do
  @spec serialize(t) :: String.t()
  def serialize(data)
end

defimpl Serializable, for: Map do
  def serialize(map), do: Jason.encode!(map)
end
```

**Why this translation:**
- Roc's `implements` constraints → Elixir's protocol dispatch
- Roc: compile-time ability resolution; Elixir: runtime protocol dispatch
- Built-in abilities (Inspect, Eq) → built-in functions (inspect/1, ==)
- Custom abilities → defprotocol + defimpl

---

### Pattern: Platform Tasks → OTP Processes

Roc's platform-based Task model translates to Elixir's OTP processes.

**Roc:**
```roc
# Platform-provided Task
main : Task {} []
main =
    content = File.readUtf8!("input.txt")
    processed = String.toUpper(content)
    File.writeUtf8!("output.txt", processed)
    Stdout.line!("Done!")
```

**Elixir:**
```elixir
# Using Task for one-off operations
def main do
  case File.read("input.txt") do
    {:ok, content} ->
      processed = String.upcase(content)
      File.write!("output.txt", processed)
      IO.puts("Done!")
    {:error, reason} ->
      IO.puts("Error: #{inspect(reason)}")
  end
end

# Or for stateful operations, use GenServer
defmodule FileProcessor do
  use GenServer

  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def process_file(input, output) do
    GenServer.call(__MODULE__, {:process, input, output})
  end

  @impl true
  def init(_opts), do: {:ok, %{}}

  @impl true
  def handle_call({:process, input, output}, _from, state) do
    with {:ok, content} <- File.read(input),
         processed = String.upcase(content),
         :ok <- File.write(output, processed) do
      {:reply, {:ok, "Done!"}, state}
    else
      {:error, reason} -> {:reply, {:error, reason}, state}
    end
  end
end
```

**Why this translation:**
- Roc's Task (sequential effects) → Elixir's procedural code or Task.async
- Roc's platform manages execution → Elixir explicit process management
- Stateful Tasks → GenServer with state
- Platform supervision → OTP Supervisor for fault tolerance

---

## Error Handling Translation

### From Result Type to Tagged Tuples

**Roc:**
```roc
# Multiple error types with tag union
parseAndDivide : Str, Str -> Result I64 [ParseError Str, DivByZero]
parseAndDivide = \aStr, bStr ->
    a = Str.toI64!(aStr) |> Result.mapErr(\_ -> ParseError("Invalid a"))
    b = Str.toI64!(bStr) |> Result.mapErr(\_ -> ParseError("Invalid b"))
    divide!(a, b)

# Handling all error cases (exhaustive)
when parseAndDivide("10", "2") is
    Ok(result) -> "Result: #{Num.toStr(result)}"
    Err(ParseError(msg)) -> "Parse error: #{msg}"
    Err(DivByZero) -> "Division by zero"
```

**Elixir:**
```elixir
# Multiple error types with tagged tuples
@spec parse_and_divide(String.t(), String.t()) ::
  {:ok, integer()} | {:error, {:parse_error, String.t()} | :division_by_zero}
def parse_and_divide(a_str, b_str) do
  with {:ok, a} <- parse_int(a_str, "Invalid a"),
       {:ok, b} <- parse_int(b_str, "Invalid b"),
       {:ok, result} <- divide(a, b) do
    {:ok, result}
  end
end

defp parse_int(str, error_msg) do
  case Integer.parse(str) do
    {num, ""} -> {:ok, num}
    _ -> {:error, {:parse_error, error_msg}}
  end
end

# Handling all error cases
case parse_and_divide("10", "2") do
  {:ok, result} -> "Result: #{result}"
  {:error, {:parse_error, msg}} -> "Parse error: #{msg}"
  {:error, :division_by_zero} -> "Division by zero"
end
```

**Key differences:**
- Roc: Compiler enforces exhaustive pattern matching
- Elixir: Runtime pattern matching, dialyzer can help detect missing cases
- Both make error handling explicit in types/specs

---

## Concurrency Patterns

### Platform Tasks → GenServer State Management

**Roc:**
```roc
# Platform manages state via Task
Counter : Task {} []
Counter =
    state = 0
    loop(state)

loop : I64 -> Task {} []
loop = \state ->
    when receive() is
        Increment -> loop(state + 1)
        Get(caller) ->
            send(caller, state)
            loop(state)
```

**Elixir:**
```elixir
# Explicit GenServer for state management
defmodule Counter do
  use GenServer

  # Client API
  def start_link(initial_value \\ 0) do
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
  def init(initial_value), do: {:ok, initial_value}

  @impl true
  def handle_cast(:increment, state) do
    {:noreply, state + 1}
  end

  @impl true
  def handle_call(:get, _from, state) do
    {:reply, state, state}
  end
end
```

**Why this translation:**
- Roc: Platform abstracts process lifecycle
- Elixir: Explicit OTP behaviors for structure
- Both: Message passing for state updates
- Elixir adds supervision, hot code reloading, distribution

---

## Module System Translation

### Roc Modules → Elixir Modules

**Roc:**
```roc
# Interface declaration
interface Math
    exposes [add, multiply, square]
    imports []

add : I64, I64 -> I64
add = \a, b -> a + b

multiply : I64, I64 -> I64
multiply = \a, b -> a * b

# Private function
internal : I64 -> I64
internal = \x -> x * 2

square : I64 -> I64
square = \x -> multiply(x, x)
```

**Elixir:**
```elixir
defmodule Math do
  @moduledoc """
  Math operations module.
  """

  @spec add(integer(), integer()) :: integer()
  def add(a, b), do: a + b

  @spec multiply(integer(), integer()) :: integer()
  def multiply(a, b), do: a * b

  # Private function
  @spec internal(integer()) :: integer()
  defp internal(x), do: x * 2

  @spec square(integer()) :: integer()
  def square(x), do: multiply(x, x)
end
```

**Why this translation:**
- Roc's `interface` → Elixir's `defmodule`
- Roc's `exposes` → Elixir's `def` (public) vs `defp` (private)
- Both support documentation (Roc: doc comments; Elixir: @moduledoc/@doc)
- Add @spec for type documentation

---

## Common Pitfalls

### 1. Losing Static Type Safety

**Problem:** Roc's compile-time type checking → Elixir runtime errors

```roc
# Roc: compile error if color not handled
colorName = \color ->
    when color is
        Red -> "red"
        # Missing other cases - compiler error!
```

```elixir
# Elixir: runtime error if pattern not matched
def color_name(color) do
  case color do
    :red -> "red"
    # Missing other cases - crash at runtime!
  end
end
```

**Fix:** Add exhaustive patterns and dialyzer specs

```elixir
@spec color_name(color()) :: String.t()
def color_name(color) do
  case color do
    :red -> "red"
    :yellow -> "yellow"
    :green -> "green"
    {:custom, r, g, b} -> "rgb(#{r}, #{g}, #{b})"
  end
end
```

### 2. List Performance Assumptions

**Problem:** Roc lists support O(1) indexed access; Elixir lists are linked (O(n))

```roc
# Roc: O(1) indexed access
getItem = \list, index ->
    List.get(list, index)
```

```elixir
# Elixir: O(n) for lists - inefficient!
def get_item(list, index) do
  Enum.at(list, index)
end
```

**Fix:** Use tuples or arrays for indexed access

```elixir
# Use tuple for fixed-size indexed access
tuple = {1, 2, 3, 4}
elem(tuple, 2)  # O(1)

# Or use :array module for dynamic arrays
array = :array.from_list([1, 2, 3, 4])
:array.get(2, array)  # Efficient indexed access
```

### 3. Integer Overflow Behavior

**Problem:** Roc has explicit overflow behavior; Elixir has arbitrary precision

```roc
# Roc: Fixed-size integers can overflow
x : U8
x = 255
y = x + 1  # Wraps to 0 or raises depending on context
```

```elixir
# Elixir: Arbitrary precision - no overflow
x = 255
y = x + 1  # Just 256, promotes to bigint automatically
```

**Fix:** Add explicit bounds checking if needed

```elixir
def safe_add_u8(a, b) when a >= 0 and a <= 255 and b >= 0 and b <= 255 do
  result = a + b
  if result > 255 do
    {:error, :overflow}
  else
    {:ok, result}
  end
end
```

### 4. Platform Abstractions

**Problem:** Roc's platform model hides I/O details; Elixir makes them explicit

```roc
# Roc: Platform handles concurrency
main =
    content1 = File.readUtf8!("file1.txt")
    content2 = File.readUtf8!("file2.txt")
    # Platform may parallelize
```

```elixir
# Elixir: Explicit sequential execution
def main do
  {:ok, content1} = File.read("file1.txt")
  {:ok, content2} = File.read("file2.txt")
  # Sequential by default
end
```

**Fix:** Use Task.async for parallelism

```elixir
def main do
  task1 = Task.async(fn -> File.read("file1.txt") end)
  task2 = Task.async(fn -> File.read("file2.txt") end)

  {:ok, content1} = Task.await(task1)
  {:ok, content2} = Task.await(task2)
end
```

### 5. Nil vs Tag Unions

**Problem:** Roc has no nil; Elixir uses nil pervasively

```roc
# Roc: Explicit optional type
findUser : U64 -> [Some User, None]
findUser = \id ->
    # Must return tag union
```

```elixir
# Elixir: Can return nil implicitly
def find_user(id) do
  # nil is valid return value
  if id == 1 do
    %User{name: "Alice"}
  else
    nil
  end
end
```

**Fix:** Be explicit with tagged tuples for consistency

```elixir
@spec find_user(non_neg_integer()) :: {:ok, User.t()} | :error
def find_user(id) do
  if id == 1 do
    {:ok, %User{name: "Alice"}}
  else
    :error
  end
end
```

---

## Testing Strategy

### Porting Roc Expects to ExUnit

**Roc:**
```roc
# Inline expect tests
expect 1 + 1 == 2

expect List.map([1, 2, 3], \x -> x * 2) == [2, 4, 6]

expect
    result = divide(10, 2)
    result == Ok(5)
```

**Elixir:**
```elixir
defmodule MathTest do
  use ExUnit.Case

  test "addition works" do
    assert 1 + 1 == 2
  end

  test "list map doubles values" do
    assert Enum.map([1, 2, 3], fn x -> x * 2 end) == [2, 4, 6]
  end

  test "divide returns ok tuple" do
    assert {:ok, 5} = Math.divide(10, 2)
  end
end
```

### Property-Based Testing for Static Invariants

Use StreamData to test invariants that Roc guarantees statically:

**Elixir:**
```elixir
defmodule PropertiesTest do
  use ExUnit.Case
  use ExUnitProperties

  # Test invariant that Roc enforces: division never returns invalid results
  property "division always returns ok or error" do
    check all a <- integer(),
              b <- integer() do
      result = Math.divide(a, b)
      assert match?({:ok, _}, result) or match?({:error, _}, result)
    end
  end

  # Test exhaustiveness (Roc compiler enforces this)
  property "all color tags have names" do
    check all color <- one_of([
                constant(:red),
                constant(:yellow),
                constant(:green),
                tuple({constant(:custom), integer(0..255), integer(0..255), integer(0..255)})
              ]) do
      # Should not raise
      assert is_binary(ColorModule.color_name(color))
    end
  end
end
```

---

## Tooling

| Category | Roc | Elixir | Notes |
|----------|-----|--------|-------|
| Build Tool | `roc` CLI | Mix | Mix manages deps, compilation, tasks |
| Package Manager | Platform URLs | Hex | Hex.pm for packages |
| Test Framework | `expect`, `roc test` | ExUnit | Built-in testing |
| Type Checking | Built-in | Dialyzer (optional) | Add @spec for static analysis |
| REPL | Planned | IEx | Interactive shell |
| Documentation | Doc comments | ExDoc | Generate HTML docs |
| Formatter | `roc format` | `mix format` | Code formatting |
| Linter | Built-in compiler | Credo (optional) | Code quality |

---

## Build System Migration

### Roc Application → Mix Project

**Roc:**
```roc
# app header
app [main] {
    pf: platform "https://github.com/roc-lang/basic-cli/releases/download/0.10.0/..."
}

import pf.Stdout
import pf.Task exposing [Task]

main : Task {} []
main =
    Stdout.line!("Hello, World!")
```

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
      extra_applications: [:logger]
    ]
  end

  defp deps do
    [
      {:jason, "~> 1.4"}  # Example dependency
    ]
  end
end

# lib/my_app.ex
defmodule MyApp do
  def main do
    IO.puts("Hello, World!")
  end
end
```

**Migration steps:**
1. Create Mix project: `mix new my_app`
2. Convert platform dependencies → Hex packages
3. Roc's `main : Task {} []` → Elixir's `def main` or OTP application
4. Platform I/O → Elixir stdlib or OTP
5. Add supervision tree if stateful

---

## Cross-Cutting Patterns

For language-agnostic patterns and cross-language comparison, see:

- `patterns-concurrency-dev` - Compare Roc's Task model with Elixir's processes/GenServers
- `patterns-serialization-dev` - Encode/Decode abilities vs Jason/Protocols
- `patterns-metaprogramming-dev` - Roc's minimalist approach vs Elixir's powerful macros

---

## Examples

### Example 1: Simple - Type Conversion

**Before (Roc):**
```roc
# Simple function with type signature
double : I64 -> I64
double = \x -> x * 2

# Using it
result = double(21)  # 42
```

**After (Elixir):**
```elixir
# Function with typespec
@spec double(integer()) :: integer()
def double(x), do: x * 2

# Using it
result = double(21)  # 42
```

### Example 2: Medium - Result Type with Pattern Matching

**Before (Roc):**
```roc
# Function returning Result
parseAge : Str -> Result U32 [InvalidAge Str]
parseAge = \input ->
    when Str.toU32(input) is
        Ok(age) if age > 0 && age < 150 -> Ok(age)
        Ok(_) -> Err(InvalidAge("Age out of range"))
        Err(_) -> Err(InvalidAge("Not a number"))

# Using with pattern matching
displayAge : Str -> Str
displayAge = \input ->
    when parseAge(input) is
        Ok(age) -> "Valid age: #{Num.toStr(age)}"
        Err(InvalidAge(msg)) -> "Error: #{msg}"
```

**After (Elixir):**
```elixir
# Function returning tagged tuple
@spec parse_age(String.t()) :: {:ok, non_neg_integer()} | {:error, {:invalid_age, String.t()}}
def parse_age(input) do
  case Integer.parse(input) do
    {age, ""} when age > 0 and age < 150 ->
      {:ok, age}
    {_, ""} ->
      {:error, {:invalid_age, "Age out of range"}}
    _ ->
      {:error, {:invalid_age, "Not a number"}}
  end
end

# Using with pattern matching
@spec display_age(String.t()) :: String.t()
def display_age(input) do
  case parse_age(input) do
    {:ok, age} -> "Valid age: #{age}"
    {:error, {:invalid_age, msg}} -> "Error: #{msg}"
  end
end
```

### Example 3: Complex - GenServer State Machine

**Before (Roc):**
```roc
# State machine with platform task
State : [Idle, Processing Str, Completed { result : Str, duration : U64 }]

process : State, Event -> Task State []
process = \state, event ->
    when (state, event) is
        (Idle, Start(input)) ->
            Task.ok(Processing(input))

        (Processing(input), Complete) ->
            result = String.toUpper(input)
            duration = 100  # ms
            Task.ok(Completed({ result, duration }))

        (Completed(_), Reset) ->
            Task.ok(Idle)

        _ ->
            # Invalid transition
            Task.ok(state)
```

**After (Elixir):**
```elixir
defmodule StateMachine do
  use GenServer

  # Client API
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, :idle, opts)
  end

  def start_processing(pid, input) do
    GenServer.call(pid, {:start, input})
  end

  def complete(pid) do
    GenServer.call(pid, :complete)
  end

  def reset(pid) do
    GenServer.call(pid, :reset)
  end

  def get_state(pid) do
    GenServer.call(pid, :get_state)
  end

  # Server Callbacks
  @impl true
  def init(_) do
    {:ok, :idle}
  end

  @impl true
  def handle_call({:start, input}, _from, :idle) do
    {:reply, :ok, {:processing, input}}
  end

  def handle_call(:complete, _from, {:processing, input}) do
    result = String.upcase(input)
    duration = 100  # ms
    state = {:completed, %{result: result, duration: duration}}
    {:reply, {:ok, state}, state}
  end

  def handle_call(:reset, _from, {:completed, _}) do
    {:reply: :ok, :idle}
  end

  def handle_call(:get_state, _from, state) do
    {:reply, state, state}
  end

  # Invalid transitions
  def handle_call(_, _from, state) do
    {:reply, {:error, :invalid_transition}, state}
  end
end

# Usage with supervision
defmodule MyApp.Application do
  use Application

  def start(_type, _args) do
    children = [
      {StateMachine, name: StateMachine}
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-clojure-elixir` - Similar dynamic functional language pair
- `convert-clojure-roc` - Reverse direction (dynamic → static)
- `lang-roc-dev` - Roc development patterns and platform model
- `lang-elixir-dev` - Elixir development patterns and OTP
- `patterns-concurrency-dev` - Async, processes, actors across languages
- `patterns-serialization-dev` - JSON, validation, encoding across languages

---

## References

- [Roc Language](https://www.roc-lang.org/)
- [Roc Tutorial](https://www.roc-lang.org/tutorial)
- [Elixir Language](https://elixir-lang.org/)
- [Phoenix Framework](https://www.phoenixframework.org/)
- [Hex Package Manager](https://hex.pm/)
- [Dialyzer](https://www.erlang.org/doc/man/dialyzer.html)
- [StreamData](https://hexdocs.pm/stream_data/)
