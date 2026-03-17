---
name: lang-elixir-dev
description: Foundational Elixir patterns covering modules, pattern matching, processes, OTP behaviors (GenServer, Supervisor), Phoenix framework basics, and functional programming idioms. Use when writing Elixir code, building concurrent systems, working with Phoenix, or needing guidance on Elixir development patterns. This is the entry point for Elixir development.
---

# Elixir Fundamentals

Foundational Elixir patterns and core language features. This skill serves as both a reference for common patterns and an index to specialized Elixir skills.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Elixir Skill Hierarchy                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                  ┌───────────────────┐                          │
│                  │ lang-elixir-dev   │ ◄── You are here         │
│                  │   (foundation)    │                          │
│                  └─────────┬─────────┘                          │
│                            │                                    │
│       ┌────────────────────┼────────────────────┐               │
│       │                    │                    │               │
│       ▼                    ▼                    ▼               │
│  ┌─────────┐        ┌──────────┐        ┌──────────┐           │
│  │ phoenix │        │   otp    │        │  ecto    │           │
│  │  -dev   │        │  -dev    │        │  -dev    │           │
│  └─────────┘        └──────────┘        └──────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**This skill covers:**
- Core syntax (modules, functions, pattern matching)
- Data types and immutability
- Pattern matching and guards
- Processes and message passing
- OTP basics (GenServer, Supervisor)
- Mix project structure
- Common functional programming idioms
- Phoenix framework fundamentals

**This skill does NOT cover (see specialized skills):**
- Advanced Phoenix features → `lang-elixir-phoenix-dev`
- Advanced OTP patterns → `lang-elixir-otp-dev`
- Database patterns with Ecto → `lang-elixir-ecto-dev`
- Deployment and releases → `lang-elixir-deploy-dev`
- Testing patterns → `lang-elixir-testing-dev`

---

## Quick Reference

| Task | Pattern |
|------|---------|
| Define module | `defmodule MyModule do ... end` |
| Define function | `def function_name(args), do: result` |
| Private function | `defp private_function(args), do: result` |
| Pattern match | `{:ok, value} = result` |
| Pipe operator | `value \|> function1() \|> function2()` |
| Spawn process | `spawn(fn -> ... end)` |
| Send message | `send(pid, message)` |
| Receive message | `receive do pattern -> ... end` |
| GenServer call | `GenServer.call(pid, message)` |
| Supervisor start | `Supervisor.start_link(children, opts)` |

---

## Skill Routing

Use this table to find the right specialized skill:

| When you need to... | Use this skill |
|---------------------|----------------|
| Build web applications with Phoenix | `lang-elixir-phoenix-dev` |
| Design advanced OTP architectures | `lang-elixir-otp-dev` |
| Work with databases using Ecto | `lang-elixir-ecto-dev` |
| Deploy applications, create releases | `lang-elixir-deploy-dev` |
| Write tests with ExUnit | `lang-elixir-testing-dev` |

---

## Core Data Types

### Atoms

```elixir
# Atoms are constants where name is the value
:ok
:error
:atom_name
:"atom with spaces"

# Boolean atoms
true  # Same as :true
false # Same as :false
nil   # Same as :nil

# Module names are atoms
IO      # Same as :"Elixir.IO"
String  # Same as :"Elixir.String"
```

### Numbers

```elixir
# Integers (arbitrary precision)
42
1_000_000
0x1F  # Hexadecimal
0o777 # Octal
0b1010 # Binary

# Floats (64-bit double precision)
3.14
1.0e-10
```

### Strings and Charlists

```elixir
# Strings (UTF-8 binaries)
"hello"
"hello #{name}"  # Interpolation
"multi
line
string"

# String operations
String.upcase("hello")      # "HELLO"
String.length("hello")      # 5
String.split("a,b,c", ",")  # ["a", "b", "c"]
String.replace("hello", "l", "x")  # "hexxo"

# Charlists (lists of integers)
'hello'  # [104, 101, 108, 108, 111]
'hello' ++ ' world'  # 'hello world'
```

### Lists

```elixir
# Lists (linked lists)
[1, 2, 3]
[head | tail] = [1, 2, 3]  # head = 1, tail = [2, 3]

# List operations
[1, 2] ++ [3, 4]     # [1, 2, 3, 4] (concatenation)
[1, 2, 3] -- [2]     # [1, 3] (difference)
hd([1, 2, 3])        # 1 (head)
tl([1, 2, 3])        # [2, 3] (tail)
length([1, 2, 3])    # 3

# List module
Enum.map([1, 2, 3], fn x -> x * 2 end)  # [2, 4, 6]
Enum.filter([1, 2, 3], fn x -> rem(x, 2) == 0 end)  # [2]
Enum.reduce([1, 2, 3], 0, fn x, acc -> x + acc end)  # 6
```

### Tuples

```elixir
# Tuples (contiguous memory)
{:ok, "value"}
{:error, :not_found}
{1, 2, 3}

# Common pattern: tagged tuples
def divide(a, b) when b != 0, do: {:ok, a / b}
def divide(_, 0), do: {:error, :division_by_zero}

# Tuple operations
elem({:ok, 42}, 0)           # :ok
put_elem({:a, :b}, 1, :c)    # {:a, :c}
tuple_size({:a, :b, :c})     # 3
```

### Maps

```elixir
# Maps (key-value stores)
%{:name => "Alice", :age => 30}
%{name: "Alice", age: 30}  # Shorthand for atom keys

# Accessing values
map = %{name: "Alice", age: 30}
map[:name]       # "Alice"
map.name         # "Alice" (only for atom keys)

# Updating maps
%{map | age: 31}  # Update existing key
Map.put(map, :city, "NYC")  # Add new key
Map.delete(map, :age)  # Remove key

# Pattern matching
%{name: name} = %{name: "Alice", age: 30}  # name = "Alice"

# Map operations
Map.keys(map)       # [:name, :age]
Map.values(map)     # ["Alice", 30]
Map.merge(map1, map2)  # Merge maps
```

### Keyword Lists

```elixir
# Keyword lists (lists of 2-tuples with atom keys)
[name: "Alice", age: 30]
# Same as: [{:name, "Alice"}, {:age, 30}]

# Common in function options
String.split("a,b,c", ",", trim: true)

# Accessing values
list = [name: "Alice", age: 30]
list[:name]  # "Alice"
Keyword.get(list, :name)  # "Alice"

# Can have duplicate keys
[a: 1, a: 2, a: 3]
```

---

## Pattern Matching

### Basic Patterns

```elixir
# Match operator
{a, b, c} = {1, 2, 3}  # a=1, b=2, c=3

# List matching
[head | tail] = [1, 2, 3]  # head=1, tail=[2,3]
[first, second | rest] = [1, 2, 3, 4]  # first=1, second=2, rest=[3,4]

# Tuple matching
{:ok, result} = {:ok, 42}  # result=42
{:error, reason} = {:error, :not_found}  # reason=:not_found

# Map matching
%{name: name} = %{name: "Alice", age: 30}  # name="Alice"
%{name: name, age: age} = %{name: "Alice", age: 30}

# Pin operator (match against value)
x = 1
^x = 1  # OK
^x = 2  # MatchError
```

### Function Pattern Matching

```elixir
# Multiple function clauses
def greet(:morning), do: "Good morning!"
def greet(:afternoon), do: "Good afternoon!"
def greet(:evening), do: "Good evening!"

# Pattern match on structure
def handle_response({:ok, data}), do: process(data)
def handle_response({:error, reason}), do: handle_error(reason)

# Pattern match on lists
def sum([]), do: 0
def sum([head | tail]), do: head + sum(tail)

# Ignore values with underscore
def process({:ok, _}), do: :success
def process({:error, reason}), do: {:failed, reason}
```

### Guards

```elixir
# Guard clauses
def positive?(x) when x > 0, do: true
def positive?(_), do: false

# Multiple guards (AND)
def adult?(age) when is_integer(age) and age >= 18, do: true
def adult?(_), do: false

# Multiple guards (OR)
def number?(x) when is_integer(x) or is_float(x), do: true
def number?(_), do: false

# Common guard functions
is_atom(x)
is_binary(x)
is_boolean(x)
is_list(x)
is_map(x)
is_number(x)
is_tuple(x)
is_nil(x)
```

---

## Modules and Functions

### Module Definition

```elixir
defmodule Math do
  # Module attribute (compile-time constant)
  @pi 3.14159

  # Public function
  def circle_area(radius) do
    @pi * radius * radius
  end

  # Private function
  defp validate_radius(radius) when radius > 0, do: :ok
  defp validate_radius(_), do: :error

  # One-line function
  def double(x), do: x * 2

  # Function with multiple clauses
  def factorial(0), do: 1
  def factorial(n) when n > 0, do: n * factorial(n - 1)

  # Function with default arguments
  def greet(name, greeting \\ "Hello") do
    "#{greeting}, #{name}!"
  end
end
```

### Anonymous Functions

```elixir
# Define anonymous function
add = fn a, b -> a + b end
add.(1, 2)  # 3 (note the dot)

# Shorthand syntax
add = &(&1 + &2)
add.(1, 2)  # 3

# Capture operator with named functions
doubled = Enum.map([1, 2, 3], &(&1 * 2))
lengths = Enum.map(["a", "ab", "abc"], &String.length/1)

# Multiple clauses
handle = fn
  {:ok, result} -> result
  {:error, _} -> nil
end
```

### Function Composition

```elixir
# Pipe operator
"hello"
|> String.upcase()
|> String.reverse()
# "OLLEH"

# Function capture
numbers = [1, 2, 3, 4, 5]
evens = Enum.filter(numbers, &(rem(&1, 2) == 0))

# Composition example
def process_data(data) do
  data
  |> String.trim()
  |> String.downcase()
  |> String.split(",")
  |> Enum.map(&String.trim/1)
  |> Enum.reject(&(&1 == ""))
end
```

---

## Processes and Concurrency

### Spawning Processes

```elixir
# Spawn a process
pid = spawn(fn ->
  receive do
    {:hello, sender} -> send(sender, {:ok, "Hello back!"})
  end
end)

# Send message
send(pid, {:hello, self()})

# Receive message
receive do
  {:ok, message} -> IO.puts(message)
after
  1000 -> IO.puts("Timeout!")
end
```

### Process Links and Monitoring

```elixir
# Spawn linked process (failures propagate)
pid = spawn_link(fn -> raise "Error!" end)

# Trap exits to handle linked process failures
Process.flag(:trap_exit, true)
receive do
  {:EXIT, pid, reason} -> IO.puts("Process died: #{inspect(reason)}")
end

# Monitor process (doesn't link)
{:ok, pid} = some_process()
ref = Process.monitor(pid)
receive do
  {:DOWN, ^ref, :process, ^pid, reason} ->
    IO.puts("Process down: #{inspect(reason)}")
end
```

### Process State with Recursion

```elixir
# Counter process
defmodule Counter do
  def start(initial_value) do
    spawn(fn -> loop(initial_value) end)
  end

  defp loop(value) do
    receive do
      {:increment, caller} ->
        send(caller, {:ok, value + 1})
        loop(value + 1)

      {:get, caller} ->
        send(caller, {:ok, value})
        loop(value)

      :stop ->
        :ok
    end
  end
end

# Usage
counter = Counter.start(0)
send(counter, {:increment, self()})
receive do
  {:ok, new_value} -> IO.puts("New value: #{new_value}")
end
```

---

## OTP Basics

### GenServer

```elixir
defmodule Stack do
  use GenServer

  # Client API

  def start_link(initial_stack) do
    GenServer.start_link(__MODULE__, initial_stack, name: __MODULE__)
  end

  def push(item) do
    GenServer.cast(__MODULE__, {:push, item})
  end

  def pop do
    GenServer.call(__MODULE__, :pop)
  end

  # Server Callbacks

  @impl true
  def init(initial_stack) do
    {:ok, initial_stack}
  end

  @impl true
  def handle_call(:pop, _from, [head | tail]) do
    {:reply, head, tail}
  end

  def handle_call(:pop, _from, []) do
    {:reply, nil, []}
  end

  @impl true
  def handle_cast({:push, item}, state) do
    {:noreply, [item | state]}
  end
end

# Usage
{:ok, _pid} = Stack.start_link([])
Stack.push(1)
Stack.push(2)
Stack.pop()  # 2
```

### Supervisor

```elixir
defmodule MyApp.Application do
  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Worker
      {Stack, []},
      # Worker with custom config
      {MyWorker, name: MyWorker, restart: :transient},
      # Supervisor
      {Registry, keys: :unique, name: MyApp.Registry}
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end

# Restart strategies:
# :one_for_one - restart only failed child
# :one_for_all - restart all children if one fails
# :rest_for_one - restart failed child and those started after it
```

### GenServer with State Management

```elixir
defmodule Counter do
  use GenServer

  # Client

  def start_link(initial_value \\ 0) do
    GenServer.start_link(__MODULE__, initial_value, name: __MODULE__)
  end

  def increment do
    GenServer.call(__MODULE__, :increment)
  end

  def get do
    GenServer.call(__MODULE__, :get)
  end

  def async_increment do
    GenServer.cast(__MODULE__, :increment)
  end

  # Server

  @impl true
  def init(initial_value) do
    {:ok, initial_value}
  end

  @impl true
  def handle_call(:increment, _from, state) do
    {:reply, state + 1, state + 1}
  end

  def handle_call(:get, _from, state) do
    {:reply, state, state}
  end

  @impl true
  def handle_cast(:increment, state) do
    {:noreply, state + 1}
  end
end
```

---

## Mix Project Structure

### Creating a New Project

```bash
# Create new project
mix new my_app

# Create new supervised application
mix new my_app --sup

# Project structure:
# my_app/
# ├── lib/
# │   ├── my_app.ex
# │   └── my_app/
# │       └── application.ex
# ├── test/
# │   ├── my_app_test.exs
# │   └── test_helper.exs
# ├── mix.exs
# └── README.md
```

### mix.exs Configuration

```elixir
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
      {:ecto_sql, "~> 3.10"},
      {:postgrex, ">= 0.0.0"},
      {:jason, "~> 1.4"},
      {:plug_cowboy, "~> 2.6"}
    ]
  end
end
```

### Common Mix Tasks

```bash
# Compile project
mix compile

# Run tests
mix test

# Run application
mix run --no-halt

# Interactive shell
iex -S mix

# Get dependencies
mix deps.get

# Format code
mix format

# Create new module
mix phx.gen.context Accounts User users name:string email:string
```

---

## Phoenix Framework Basics

### Phoenix Project Structure

```
my_app/
├── assets/           # Frontend assets
├── config/           # Configuration
├── lib/
│   ├── my_app/       # Business logic
│   ├── my_app_web/   # Web interface
│   │   ├── controllers/
│   │   ├── views/
│   │   ├── templates/
│   │   └── router.ex
│   └── my_app.ex
├── priv/             # Database migrations, static files
└── test/
```

### Router

```elixir
defmodule MyAppWeb.Router do
  use MyAppWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", MyAppWeb do
    pipe_through :browser

    get "/", PageController, :index
    resources "/users", UserController
  end

  scope "/api", MyAppWeb do
    pipe_through :api

    resources "/posts", PostController, except: [:new, :edit]
  end
end
```

### Controller

```elixir
defmodule MyAppWeb.UserController do
  use MyAppWeb, :controller

  alias MyApp.Accounts
  alias MyApp.Accounts.User

  def index(conn, _params) do
    users = Accounts.list_users()
    render(conn, "index.html", users: users)
  end

  def show(conn, %{"id" => id}) do
    user = Accounts.get_user!(id)
    render(conn, "show.html", user: user)
  end

  def create(conn, %{"user" => user_params}) do
    case Accounts.create_user(user_params) do
      {:ok, user} ->
        conn
        |> put_flash(:info, "User created successfully.")
        |> redirect(to: ~p"/users/#{user}")

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, "new.html", changeset: changeset)
    end
  end
end
```

### LiveView Basics

```elixir
defmodule MyAppWeb.CounterLive do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, count: 0)}
  end

  @impl true
  def handle_event("increment", _params, socket) do
    {:noreply, update(socket, :count, &(&1 + 1))}
  end

  def handle_event("decrement", _params, socket) do
    {:noreply, update(socket, :count, &(&1 - 1))}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div>
      <h1>Count: <%= @count %></h1>
      <button phx-click="increment">+</button>
      <button phx-click="decrement">-</button>
    </div>
    """
  end
end
```

---

## Common Patterns and Idioms

### With Statement

```elixir
# Chain operations that can fail
def create_user(params) do
  with {:ok, validated} <- validate_params(params),
       {:ok, user} <- insert_user(validated),
       {:ok, email} <- send_welcome_email(user) do
    {:ok, user}
  else
    {:error, reason} -> {:error, reason}
  end
end
```

### Case Statement

```elixir
case File.read("config.json") do
  {:ok, contents} ->
    Jason.decode(contents)

  {:error, :enoent} ->
    {:error, "File not found"}

  {:error, reason} ->
    {:error, "Read error: #{inspect(reason)}"}
end
```

### Cond Statement

```elixir
cond do
  age < 13 -> "child"
  age < 20 -> "teenager"
  age < 60 -> "adult"
  true -> "senior"
end
```

### Using Structs

```elixir
defmodule User do
  defstruct [:name, :email, age: 0, active: true]

  def new(name, email) do
    %User{name: name, email: email}
  end

  def activate(%User{} = user) do
    %{user | active: true}
  end
end

# Usage
user = %User{name: "Alice", email: "alice@example.com"}
user = User.activate(user)

# Pattern matching
def greet(%User{name: name}), do: "Hello, #{name}!"
```

### Protocols

```elixir
# Define protocol
defprotocol Serializable do
  def serialize(data)
end

# Implement for different types
defimpl Serializable, for: Map do
  def serialize(map), do: Jason.encode!(map)
end

defimpl Serializable, for: List do
  def serialize(list), do: Jason.encode!(list)
end

# Usage
Serializable.serialize(%{name: "Alice"})
Serializable.serialize([1, 2, 3])
```

### Use Directive

```elixir
# Define reusable behavior
defmodule MyMacro do
  defmacro __using__(opts) do
    quote do
      import MyMacro
      @opts unquote(opts)

      def common_function do
        "This is common"
      end
    end
  end
end

# Use it
defmodule MyModule do
  use MyMacro, option: :value
end
```

---

## Enum and Stream

### Enum Module (Eager)

```elixir
# Map
Enum.map([1, 2, 3], fn x -> x * 2 end)  # [2, 4, 6]

# Filter
Enum.filter([1, 2, 3, 4], fn x -> rem(x, 2) == 0 end)  # [2, 4]

# Reduce
Enum.reduce([1, 2, 3], 0, fn x, acc -> x + acc end)  # 6

# Find
Enum.find([1, 2, 3], fn x -> x > 2 end)  # 3

# Chaining
[1, 2, 3, 4, 5]
|> Enum.filter(&(rem(&1, 2) == 0))
|> Enum.map(&(&1 * 2))
# [4, 8]

# Common functions
Enum.any?([1, 2, 3], &(&1 > 2))      # true
Enum.all?([1, 2, 3], &(&1 > 0))      # true
Enum.count([1, 2, 3])                # 3
Enum.sum([1, 2, 3])                  # 6
Enum.max([1, 2, 3])                  # 3
Enum.min([1, 2, 3])                  # 1
Enum.sort([3, 1, 2])                 # [1, 2, 3]
Enum.uniq([1, 2, 2, 3])              # [1, 2, 3]
Enum.zip([1, 2], [:a, :b])           # [{1, :a}, {2, :b}]
```

### Stream Module (Lazy)

```elixir
# Lazy operations (only computed when needed)
stream = Stream.map([1, 2, 3], fn x -> x * 2 end)
Enum.to_list(stream)  # [2, 4, 6]

# Infinite streams
Stream.iterate(0, &(&1 + 1))
|> Stream.take(5)
|> Enum.to_list()
# [0, 1, 2, 3, 4]

# File streaming (memory efficient)
File.stream!("large_file.txt")
|> Stream.map(&String.trim/1)
|> Stream.filter(&(&1 != ""))
|> Enum.count()
```

---

## Error Handling

### Try-Rescue

```elixir
try do
  raise "Error!"
rescue
  e in RuntimeError -> "Caught runtime error: #{e.message}"
  e -> "Caught: #{inspect(e)}"
after
  cleanup()
end
```

### Try-Catch

```elixir
try do
  throw(:error)
catch
  :error -> "Caught thrown value"
  :exit, _ -> "Caught exit"
end
```

### Result Tuples

```elixir
# Preferred pattern in Elixir
def divide(a, b) when b != 0, do: {:ok, a / b}
def divide(_, 0), do: {:error, :division_by_zero}

# Usage
case divide(10, 2) do
  {:ok, result} -> "Result: #{result}"
  {:error, reason} -> "Error: #{reason}"
end

# With pattern matching
{:ok, result} = divide(10, 2)  # Raises if not :ok
```

---

## Troubleshooting

### Match Error

**Problem:** `MatchError: no match of right hand side value`

```elixir
# Cause: Pattern doesn't match
{:ok, value} = {:error, :not_found}  # MatchError!

# Fix: Use case or handle both patterns
case result do
  {:ok, value} -> value
  {:error, reason} -> handle_error(reason)
end
```

### Undefined Function

**Problem:** `UndefinedFunctionError`

```elixir
# Cause: Function not defined or not imported
String.upcase("hello")  # OK
upcase("hello")         # UndefinedFunctionError

# Fix: Import or use full module name
import String
upcase("hello")  # OK
```

### Process Crashes

**Problem:** Process dies unexpectedly

```elixir
# Use supervisors to restart failed processes
children = [
  {MyWorker, restart: :permanent}
]

Supervisor.start_link(children, strategy: :one_for_one)
```

### Genserver Timeout

**Problem:** GenServer call times out

```elixir
# Default timeout is 5 seconds
GenServer.call(server, :slow_operation)  # May timeout

# Increase timeout
GenServer.call(server, :slow_operation, 30_000)  # 30 seconds

# Or use cast for async operations
GenServer.cast(server, :slow_operation)
```

---

## Testing

Elixir has excellent testing support built-in with ExUnit, along with doctests, property-based testing, and mocking capabilities.

### ExUnit Basics

```elixir
# test/math_test.exs
defmodule MathTest do
  use ExUnit.Case

  # Test with assertion
  test "add/2 adds two numbers" do
    assert Math.add(2, 3) == 5
    assert Math.add(-1, 1) == 0
  end

  # Refute (opposite of assert)
  test "add/2 does not return incorrect sum" do
    refute Math.add(2, 3) == 6
  end

  # Pattern matching in assertions
  test "divide/2 returns ok tuple" do
    assert {:ok, result} = Math.divide(10, 2)
    assert result == 5
  end

  # Testing errors
  test "divide/2 returns error on division by zero" do
    assert {:error, :division_by_zero} = Math.divide(10, 0)
  end
end
```

### Test Lifecycle

```elixir
defmodule UserTest do
  use ExUnit.Case

  # Setup runs before each test
  setup do
    user = %User{name: "Alice", age: 30}
    {:ok, user: user}
  end

  # Access setup data via context
  test "user has name", %{user: user} do
    assert user.name == "Alice"
  end

  # Setup with explicit context
  setup context do
    if context[:admin] do
      {:ok, user: %User{name: "Admin", role: :admin}}
    else
      :ok
    end
  end

  @tag :admin
  test "admin user has correct role", %{user: user} do
    assert user.role == :admin
  end

  # Setup all (runs once before all tests)
  setup_all do
    # Start database connection
    {:ok, conn} = Database.connect()
    on_exit(fn -> Database.disconnect(conn) end)
    {:ok, conn: conn}
  end
end
```

### Assertions

```elixir
# Equality
assert 1 + 1 == 2
refute 1 + 1 == 3

# Pattern matching
assert {:ok, value} = function_that_returns_tuple()
assert %User{name: name} = get_user()

# Boolean
assert is_binary("hello")
assert is_list([1, 2, 3])

# Membership
assert 3 in [1, 2, 3]
refute 4 in [1, 2, 3]

# Approximate equality (floats)
assert_in_delta 0.1 + 0.2, 0.3, 0.0001

# Exception testing
assert_raise ArithmeticException, fn ->
  1 / 0
end

assert_raise ArgumentError, "invalid argument", fn ->
  raise ArgumentError, "invalid argument"
end

# Receive message testing
send(self(), {:hello, "world"})
assert_receive {:hello, msg}
assert msg == "world"

# No message received
refute_receive {:unexpected, _}, 100
```

### Doctests

```elixir
defmodule Math do
  @doc """
  Adds two numbers together.

  ## Examples

      iex> Math.add(2, 3)
      5

      iex> Math.add(-1, 1)
      0

      iex> Math.add(0.1, 0.2)
      0.30000000000000004
  """
  def add(a, b), do: a + b

  @doc """
  Divides two numbers.

  ## Examples

      iex> Math.divide(10, 2)
      {:ok, 5.0}

      iex> Math.divide(10, 0)
      {:error, :division_by_zero}
  """
  def divide(_a, 0), do: {:error, :division_by_zero}
  def divide(a, b), do: {:ok, a / b}
end

# In test file, enable doctests
defmodule MathTest do
  use ExUnit.Case
  doctest Math
end
```

### Async Tests

```elixir
# Run tests asynchronously (safe if no shared state)
defmodule FastTest do
  use ExUnit.Case, async: true

  test "independent test 1" do
    assert 1 + 1 == 2
  end

  test "independent test 2" do
    assert 2 * 2 == 4
  end
end

# Synchronous tests (default, for shared resources)
defmodule DatabaseTest do
  use ExUnit.Case  # async: false is default

  test "writes to database" do
    # Safe to share database
  end
end
```

### Test Tags and Filtering

```elixir
defmodule UserTest do
  use ExUnit.Case

  # Tag individual test
  @tag :slow
  test "slow integration test" do
    # ...
  end

  # Tag with value
  @tag timeout: 5000
  test "test with custom timeout" do
    # ...
  end

  # Multiple tags
  @tag :integration
  @tag :database
  test "database integration" do
    # ...
  end

  # Module-level tags (apply to all tests)
  @moduletag :integration
end
```

```bash
# Run only tagged tests
mix test --only slow
mix test --only integration

# Exclude tagged tests
mix test --exclude slow
mix test --exclude integration:database

# Include by default excluded tests
mix test --include pending
```

### Mocking with Mox

```elixir
# Define behaviour
defmodule WeatherAPI do
  @callback get_temperature(city :: String.t()) :: {:ok, float()} | {:error, term()}
end

# Define mock in test_helper.exs
Mox.defmock(WeatherAPIMock, for: WeatherAPI)

# In your module, inject dependency
defmodule WeatherService do
  def get_weather(city, api \\ WeatherAPI) do
    case api.get_temperature(city) do
      {:ok, temp} -> "Temperature in #{city}: #{temp}°C"
      {:error, _} -> "Could not fetch weather"
    end
  end
end

# In test
defmodule WeatherServiceTest do
  use ExUnit.Case, async: true
  import Mox

  # Set up expectations
  setup :verify_on_exit!

  test "returns temperature message" do
    expect(WeatherAPIMock, :get_temperature, fn "NYC" ->
      {:ok, 25.0}
    end)

    result = WeatherService.get_weather("NYC", WeatherAPIMock)
    assert result == "Temperature in NYC: 25.0°C"
  end

  test "handles API errors" do
    expect(WeatherAPIMock, :get_temperature, fn _city ->
      {:error, :timeout}
    end)

    result = WeatherService.get_weather("NYC", WeatherAPIMock)
    assert result == "Could not fetch weather"
  end

  test "allows multiple calls" do
    stub(WeatherAPIMock, :get_temperature, fn _city ->
      {:ok, 20.0}
    end)

    WeatherService.get_weather("NYC", WeatherAPIMock)
    WeatherService.get_weather("SF", WeatherAPIMock)
    # Both calls succeed with stub
  end
end
```

### Property-Based Testing with StreamData

```elixir
# Add to mix.exs
defp deps do
  [
    {:stream_data, "~> 0.6", only: :test}
  ]
end

# Property-based test
defmodule StringPropertiesTest do
  use ExUnit.Case
  use ExUnitProperties

  property "reversing a string twice returns original" do
    check all string <- string(:printable) do
      reversed_twice = string |> String.reverse() |> String.reverse()
      assert reversed_twice == string
    end
  end

  property "list concatenation is associative" do
    check all list1 <- list_of(integer()),
              list2 <- list_of(integer()),
              list3 <- list_of(integer()) do
      assert (list1 ++ list2) ++ list3 == list1 ++ (list2 ++ list3)
    end
  end

  property "sorting is idempotent" do
    check all list <- list_of(integer()) do
      sorted_once = Enum.sort(list)
      sorted_twice = Enum.sort(sorted_once)
      assert sorted_once == sorted_twice
    end
  end

  # Custom generator
  property "user age is always positive" do
    check all name <- string(:alphanumeric),
              age <- positive_integer() do
      user = %User{name: name, age: age}
      assert User.valid?(user)
    end
  end
end
```

### Testing Processes and GenServers

```elixir
defmodule CounterTest do
  use ExUnit.Case

  test "counter increments" do
    {:ok, pid} = Counter.start_link(0)

    Counter.increment(pid)
    Counter.increment(pid)

    assert Counter.get(pid) == 2
  end

  test "counter handles cast" do
    {:ok, pid} = Counter.start_link(0)

    Counter.async_increment(pid)
    # Give it time to process cast
    Process.sleep(10)

    assert Counter.get(pid) == 1
  end

  test "counter can be supervised" do
    children = [
      {Counter, 0}
    ]

    {:ok, supervisor} = Supervisor.start_link(children, strategy: :one_for_one)

    # Get counter pid from supervisor
    [{Counter, pid, _, _}] = Supervisor.which_children(supervisor)

    Counter.increment(pid)
    assert Counter.get(pid) == 1

    # Clean up
    Supervisor.stop(supervisor)
  end
end
```

### Testing with ExUnit.CaptureIO

```elixir
import ExUnit.CaptureIO

test "prints greeting to stdout" do
  output = capture_io(fn ->
    IO.puts("Hello, World!")
  end)

  assert output == "Hello, World!\n"
end

test "captures user input" do
  result = capture_io("Alice\n", fn ->
    name = IO.gets("Enter name: ")
    String.trim(name)
  end)

  assert result == "Alice"
end

test "captures stderr" do
  output = capture_io(:stderr, fn ->
    IO.warn("Warning message")
  end)

  assert output =~ "Warning message"
end
```

### Common Testing Patterns

```elixir
# Test with multiple assertions using pipe
test "user creation pipeline" do
  params = %{name: "Alice", email: "alice@example.com"}

  assert {:ok, user} =
    params
    |> User.changeset()
    |> Repo.insert()

  assert user.name == "Alice"
  assert user.email == "alice@example.com"
end

# Test with pattern matching and guards
test "validates positive numbers" do
  assert {:ok, result} = Math.sqrt(4)
  assert result == 2.0

  assert {:error, :negative_number} = Math.sqrt(-1)
end

# Test with describe blocks for organization
describe "User.create/1" do
  test "creates user with valid params" do
    # ...
  end

  test "returns error with invalid email" do
    # ...
  end

  test "returns error with duplicate email" do
    # ...
  end
end

# Test with shared setup using tags
setup context do
  case context[:user_type] do
    :admin -> {:ok, user: create_admin_user()}
    :regular -> {:ok, user: create_regular_user()}
    _ -> :ok
  end
end

@tag user_type: :admin
test "admin can delete users", %{user: admin} do
  assert admin.role == :admin
end
```

---

## Metaprogramming

Elixir provides powerful metaprogramming capabilities through macros, which operate on the Abstract Syntax Tree (AST) at compile time.

### Quote and Unquote

```elixir
# quote turns code into AST representation
quote do
  1 + 2
end
# {:+, [context: Elixir, imports: [{1, Kernel}, {2, Kernel}]], [1, 2]}

# unquote injects values into quoted expressions
defmodule Example do
  x = 10
  quoted = quote do
    unquote(x) + 5
  end
  # {+, _, [10, 5]}
end

# unquote_splicing for lists
args = [1, 2, 3]
quote do
  sum(unquote_splicing(args))
end
# {:sum, [], [1, 2, 3]}
```

### Defining Macros

```elixir
defmodule MyMacros do
  # Basic macro
  defmacro say(expression) do
    quote do
      IO.puts(unquote(expression))
    end
  end

  # Macro with variable hygiene
  defmacro double(x) do
    quote do
      result = unquote(x)
      result * 2
    end
  end

  # Debugging macro - shows expression and result
  defmacro debug(expression) do
    quote bind_quoted: [expr: expression] do
      IO.inspect(expr, label: unquote(Macro.to_string(expression)))
    end
  end
end

# Usage
require MyMacros
MyMacros.say("Hello!")
MyMacros.debug(1 + 2)  # 1 + 2: 3
```

### The __using__ Macro

```elixir
defmodule MyBehaviour do
  # __using__ is called when `use MyBehaviour` is invoked
  defmacro __using__(opts) do
    quote do
      import MyBehaviour
      @behaviour MyBehaviour

      # Inject default implementations
      def default_name, do: unquote(opts[:name] || "Unknown")

      # Allow override
      defoverridable default_name: 0
    end
  end

  @callback required_callback() :: term()
end

# Usage
defmodule MyModule do
  use MyBehaviour, name: "Custom"
end
```

### AST Manipulation

```elixir
# Traverse and transform AST
defmodule ASTHelper do
  def transform(ast) do
    Macro.prewalk(ast, fn
      {:+, meta, [left, right]} ->
        {:-, meta, [left, right]}  # Replace + with -
      node ->
        node
    end)
  end

  # Expand macros in AST
  def expand_all(ast, env) do
    Macro.expand(ast, env)
  end

  # Convert AST to string
  def to_string(ast) do
    Macro.to_string(ast)
  end
end

# Inspect AST structure
quote do: if(true, do: 1, else: 2)
|> Macro.to_string()
# "if(true, do: 1, else: 2)"
```

### Compile-Time Code Generation

```elixir
defmodule Router do
  # Generate functions at compile time from data
  @routes [
    {:get, "/", :index},
    {:get, "/users", :users},
    {:post, "/users", :create_user}
  ]

  for {method, path, handler} <- @routes do
    def route(unquote(method), unquote(path)) do
      apply(__MODULE__, unquote(handler), [])
    end
  end

  def index, do: "Home page"
  def users, do: "List users"
  def create_user, do: "Create user"
end

# Also useful: Module.register_attribute/3 for accumulating data
defmodule PluginHost do
  Module.register_attribute(__MODULE__, :plugins, accumulate: true)

  @plugins :auth
  @plugins :logging
  @plugins :caching

  def plugins, do: @plugins  # [:caching, :logging, :auth]
end
```

---

## Serialization

Elixir uses Jason (or Poison) for JSON serialization and Protocol-based encoding for custom types.

### Jason (Recommended)

```elixir
# Add to mix.exs: {:jason, "~> 1.4"}

# Encoding
Jason.encode!(%{name: "Alice", age: 30})
# "{\"name\":\"Alice\",\"age\":30}"

# Decoding
Jason.decode!("{\"name\":\"Alice\",\"age\":30}")
# %{"name" => "Alice", "age" => 30}

# With atom keys
Jason.decode!("{\"name\":\"Alice\"}", keys: :atoms)
# %{name: "Alice"}

# Pretty printing
Jason.encode!(%{user: %{name: "Alice"}}, pretty: true)
```

### Implementing Jason.Encoder Protocol

```elixir
defmodule User do
  @derive {Jason.Encoder, only: [:id, :name, :email]}
  defstruct [:id, :name, :email, :password_hash]
end

# Custom encoder implementation
defmodule Money do
  defstruct [:amount, :currency]
end

defimpl Jason.Encoder, for: Money do
  def encode(%Money{amount: amount, currency: currency}, opts) do
    Jason.Encode.string("#{currency} #{amount}", opts)
  end
end

# Usage
Jason.encode!(%Money{amount: 100, currency: "USD"})
# "\"USD 100\""
```

### Poison (Alternative)

```elixir
# Add to mix.exs: {:poison, "~> 5.0"}

Poison.encode!(%{name: "Alice"})
Poison.decode!("{\"name\":\"Alice\"}")

# Implementing Poison.Encoder
defimpl Poison.Encoder, for: DateTime do
  def encode(datetime, options) do
    Poison.Encoder.BitString.encode(DateTime.to_iso8601(datetime), options)
  end
end
```

### Ecto Changesets for Validation

```elixir
defmodule User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :name, :string
    field :email, :string
    field :age, :integer
    timestamps()
  end

  def changeset(user, attrs) do
    user
    |> cast(attrs, [:name, :email, :age])
    |> validate_required([:name, :email])
    |> validate_format(:email, ~r/@/)
    |> validate_number(:age, greater_than: 0)
  end
end

# Validate incoming JSON
params = Jason.decode!(json_string)
changeset = User.changeset(%User{}, params)

if changeset.valid? do
  {:ok, Ecto.Changeset.apply_changes(changeset)}
else
  {:error, changeset.errors}
end
```

### Term Serialization

```elixir
# Erlang Term Format (binary)
binary = :erlang.term_to_binary(%{key: "value", list: [1, 2, 3]})
:erlang.binary_to_term(binary)

# External Term Format (for distributed systems)
binary = :erlang.term_to_binary(data, [:compressed])

# Safe deserialization (atoms must exist)
:erlang.binary_to_term(binary, [:safe])
```

---

## REPL and Development Workflow

IEx (Interactive Elixir) is central to Elixir development, providing a powerful REPL with debugging, introspection, and hot code reloading.

### Starting IEx

```bash
# Basic IEx
iex

# With Mix project loaded
iex -S mix

# With Phoenix server
iex -S mix phx.server

# With custom configuration
iex --dot-iex path/to/.iex.exs -S mix
```

### IEx Helpers

```elixir
# In IEx session:

# Help and documentation
h Enum.map/2           # Function docs
h Enum                 # Module docs
t Enum.t()             # Type specs

# Code inspection
i [1, 2, 3]            # Inspect value
i Enum                 # Inspect module

# Compilation
c "path/to/file.ex"    # Compile file
r MyModule             # Recompile module
recompile()            # Recompile project

# Value history
v()                    # Last result
v(1)                   # First result
v(-1)                  # Previous result

# Shell commands
pwd()                  # Current directory
ls()                   # List files
cd("path")             # Change directory
```

### IEx.pry for Debugging

```elixir
defmodule MyModule do
  def process(data) do
    transformed = transform(data)

    # Insert breakpoint
    require IEx; IEx.pry()

    finalize(transformed)
  end
end

# When code hits pry:
# - Inspect local variables: transformed, data
# - Call functions: transform(other_data)
# - Continue: respawn() or Ctrl+C twice
```

### Hot Code Reloading

```elixir
# Recompile and reload module in IEx
recompile()

# Reload specific module
r MyModule

# For Phoenix - automatic in dev mode
# Code changes trigger recompilation on next request

# In production (Distillery/Release)
# Use hot code upgrades via :code.load_file/1
:code.purge(MyModule)
:code.load_file(MyModule)
```

### Observer for System Inspection

```elixir
# Start Observer (GUI)
:observer.start()

# Observer shows:
# - System overview (memory, CPU, processes)
# - Process list with message queues
# - Application supervision trees
# - ETS tables
# - Port info

# For remote nodes
Node.connect(:"app@hostname")
:observer.start()
# Then select remote node in Nodes menu
```

### .iex.exs Configuration

```elixir
# In ~/.iex.exs or project .iex.exs

# Custom aliases
alias MyApp.{Repo, User, Account}

# Import helpers
import Ecto.Query

# Custom helpers
defmodule H do
  def reload do
    IEx.Helpers.recompile()
    IO.puts("Reloaded!")
  end

  def user(id), do: Repo.get(User, id)
end

# Configure IEx
IEx.configure(
  colors: [enabled: true],
  history_size: 100,
  inspect: [limit: :infinity]
)
```

### Runtime Debugging

```elixir
# Trace function calls
:dbg.tracer()
:dbg.p(:all, :c)
:dbg.tp(MyModule, :my_function, :x)
# Now calls to MyModule.my_function will be traced

# Stop tracing
:dbg.stop()

# Using :recon for production debugging
# Add {:recon, "~> 2.5"} to mix.exs
:recon.proc_count(:memory, 10)      # Top 10 by memory
:recon.proc_count(:message_queue_len, 10)  # Top 10 by queue
:recon.bin_leak(5)                  # Binary memory leaks
```

---

## Zero and Default Values

Elixir handles absence of values through nil and pattern matching, with explicit default handling patterns.

### Nil Handling

```elixir
# nil is a valid value (not an error)
user = nil
is_nil(user)  # true

# Nil-safe access with pattern matching
case get_user(id) do
  nil -> {:error, :not_found}
  user -> {:ok, user}
end

# Nil coalescing with ||
name = user_name || "Anonymous"

# Access with default
Map.get(map, :key, "default")
Keyword.get(opts, :timeout, 5000)

# Nil-safe navigation (no ?. operator, use pattern matching)
defp get_city(user) do
  case user do
    %{address: %{city: city}} -> city
    _ -> nil
  end
end

# Or with get_in
get_in(user, [:address, :city])
```

### Default Function Arguments

```elixir
defmodule Config do
  # Default arguments
  def connect(host, port \\ 80, opts \\ []) do
    timeout = Keyword.get(opts, :timeout, 5000)
    ssl = Keyword.get(opts, :ssl, false)
    {host, port, timeout, ssl}
  end
end

# Multiple clauses with defaults
Config.connect("localhost")           # port=80, opts=[]
Config.connect("localhost", 443)      # opts=[]
Config.connect("localhost", 443, ssl: true)
```

### Struct Defaults

```elixir
defmodule User do
  # All fields with defaults
  defstruct name: "Unknown",
            email: nil,
            role: :user,
            active: true,
            metadata: %{}

  # Enforce required fields
  @enforce_keys [:email]
  defstruct [:email, name: "Unknown", role: :user]
end

# Creating with defaults
%User{email: "test@example.com"}
# %User{email: "test@example.com", name: "Unknown", role: :user}

# Pattern match with defaults
def greet(%User{name: name}) do
  "Hello, #{name}!"
end
```

### Default Values in Maps

```elixir
# Access with default
map = %{a: 1, b: 2}
Map.get(map, :c, 0)  # 0

# Update with default
Map.update(map, :c, 0, &(&1 + 1))  # %{a: 1, b: 2, c: 0}

# get_and_update with default
Map.get_and_update(map, :c, fn
  nil -> {nil, 0}
  val -> {val, val + 1}
end)

# Merge with defaults
defaults = %{timeout: 5000, retries: 3}
config = %{timeout: 10000}
Map.merge(defaults, config)
# %{timeout: 10000, retries: 3}
```

### With Construct for Nil Propagation

```elixir
# Chain operations that may return nil
def process_order(order_id) do
  with {:ok, order} <- fetch_order(order_id),
       {:ok, user} <- fetch_user(order.user_id),
       {:ok, payment} <- process_payment(user, order) do
    {:ok, %{order: order, user: user, payment: payment}}
  else
    nil -> {:error, :not_found}
    {:error, reason} -> {:error, reason}
  end
end

# Helper for nil-returning functions
defp fetch_order(id) do
  case Repo.get(Order, id) do
    nil -> {:error, :order_not_found}
    order -> {:ok, order}
  end
end
```

### Default Behaviours

```elixir
defmodule Cache do
  @callback get(key :: term()) :: {:ok, term()} | :error
  @callback put(key :: term(), value :: term()) :: :ok

  # Optional callback with default
  @callback ttl() :: integer()
  @optional_callbacks ttl: 0

  defmacro __using__(_opts) do
    quote do
      @behaviour Cache

      # Default implementation
      def ttl, do: 3600

      defoverridable ttl: 0
    end
  end
end

defmodule MyCache do
  use Cache

  def get(key), do: # ...
  def put(key, value), do: # ...
  # ttl/0 uses default of 3600
end
```

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-concurrency-dev` - Processes, GenServers, supervision trees
- `patterns-serialization-dev` - JSON encoding/decoding, protocols
- `patterns-metaprogramming-dev` - Macros, compile-time code generation
- `patterns-testing-dev` - Testing strategies, property-based testing

---

## References

- [Elixir Language](https://elixir-lang.org/)
- [Elixir School](https://elixirschool.com/)
- [Phoenix Framework](https://www.phoenixframework.org/)
- [Hex Package Manager](https://hex.pm/)
- [Elixir Forum](https://elixirforum.com/)
- [ExUnit Documentation](https://hexdocs.pm/ex_unit/ExUnit.html)
- [Mox Documentation](https://hexdocs.pm/mox/Mox.html)
- [StreamData Documentation](https://hexdocs.pm/stream_data/StreamData.html)
- Specialized skills: `lang-elixir-phoenix-dev`, `lang-elixir-otp-dev`, `lang-elixir-ecto-dev`
