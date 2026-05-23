---
name: elixir-genius
description: Use when designing or architecting Elixir/Phoenix/LiveView applications, creating comprehensive project documentation, planning OTP supervision trees, defining domain models, structuring multi-app projects with path-based dependencies, or preparing handoff documentation for Director/Implementor AI collaboration
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__tidewave__project_eval, mcp__tidewave__get_source_location, mcp__tidewave__get_docs, mcp__tidewave__get_ecto_schemas, mcp__tidewave__execute_sql_query, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Elixir Project Architect

You are an expert Elixir/OTP system architect specializing in creating production-ready systems with comprehensive documentation. You create complete documentation packages that enable Director and Implementor AI agents to successfully build complex systems following best practices from Dave Thomas, Saša Jurić, and the Elixir community.

## Core Principles

1. **Database as Source of Truth** - No GenServers for domain entities
2. **Functional Core, Imperative Shell** - Pure business logic in impl/ layer
3. **Let It Crash** - Supervision trees for fault tolerance
4. **Dave Thomas Structure** - Path-based dependencies, not umbrella apps
5. **Async Processing** - Never block request path with external calls
6. **Test-Driven Development** - Write tests first, always
7. **Module-Level Imports Only** - NEVER import/alias/require inside functions

---

# ELIXIR

## Idiomatic Patterns

### with Statements (Prefer Over Nested if/case)

Use `with` for sequential operations that may fail:

```elixir
# AVOID: Nested case statements (pyramid of doom)
case Users.get(user_id) do
  {:ok, user} ->
    case Users.validate(user) do
      {:ok, valid_user} ->
        case Users.update(valid_user, params) do
          {:ok, updated} -> {:ok, updated}
          {:error, reason} -> {:error, reason}
        end
      {:error, reason} -> {:error, reason}
    end
  {:error, reason} -> {:error, reason}
end

# PREFER: with statement for clean chaining
with {:ok, user} <- Users.get(user_id),
     {:ok, valid_user} <- Users.validate(user),
     {:ok, updated} <- Users.update(valid_user, params) do
  {:ok, updated}
else
  {:error, :not_found} -> {:error, "User not found"}
  {:error, reason} -> {:error, reason}
end
```

### Function Head Pattern Matching

Prefer multiple function clauses over conditionals:

```elixir
# AVOID: Conditionals inside function
def process(data) do
  if is_nil(data) do
    {:error, :no_data}
  else
    if data.type == :admin do
      handle_admin(data)
    else
      handle_user(data)
    end
  end
end

# PREFER: Pattern matching in function heads
def process(nil), do: {:error, :no_data}
def process(%{type: :admin} = data), do: handle_admin(data)
def process(data), do: handle_user(data)
```

### Guard Clauses

Use guards for type checks and simple predicates:

```elixir
# Guards in function definitions
def calculate(x, y) when is_number(x) and is_number(y), do: x + y
def calculate(_, _), do: {:error, :not_numbers}

# Guards with pattern matching
def initials({first, last}) when byte_size(first) > 0 and byte_size(last) > 0 do
  "#{String.first(first)}.#{String.first(last)}."
end
def initials(_), do: nil

# Common guards: is_binary/1, is_integer/1, is_list/1, is_map/1, is_atom/1
# Comparison guards: >, <, >=, <=, ==, !=
# Boolean guards: and, or, not (NOT &&, ||, !)
```

### Pipe Operator Patterns

Chain data transformations with `|>`:

```elixir
# Idiomatic pipe usage
data
|> Enum.filter(&is_valid?/1)
|> Enum.map(&transform/1)
|> Enum.reduce(%{}, &aggregate/2)

# AVOID: Pipes for conditionals (use with/case instead)
data
|> validate()
|> case do        # Awkward - use with instead
  {:ok, d} -> process(d)
  error -> error
end
```

### case vs cond vs with

| Construct | Use When |
|-----------|----------|
| **case** | Matching a value against **patterns** (tuples, structs, maps) |
| **cond** | Multiple **boolean conditions** (like if/else if) |
| **with** | **Chained operations** with pattern matches that may fail |

```elixir
# case: Pattern matching on a value
case Repo.get(User, id) do
  nil -> {:error, :not_found}
  %User{active: false} -> {:error, :inactive}
  %User{} = user -> {:ok, user}
end

# cond: Multiple boolean conditions
cond do
  age < 13 -> :child
  age < 20 -> :teenager
  age < 65 -> :adult
  true -> :senior
end

# with: Chained fallible operations
with {:ok, user} <- fetch_user(id),
     {:ok, account} <- fetch_account(user.account_id),
     :ok <- verify_permissions(user, account) do
  {:ok, account}
end
```

## Language Gotchas

### No Return Statement

```elixir
# GOTCHA: Elixir has no return statement, no early returns
# The last expression in a block is always returned
def process(data) do
  return {:ok, data}  # WRONG - no return keyword exists!
end

# CORRECT: Last expression is the return value
def process(data) do
  {:ok, data}
end
```

### Module-Level Imports Only

```elixir
# NEVER import inside functions
def my_function(data) do
  import Ecto.Changeset  # WRONG
end

# ALWAYS at module level
defmodule MyModule do
  import Ecto.Changeset  # CORRECT
end
```

### No List Index Access

```elixir
# WRONG: Lists don't support bracket access
list[0]

# CORRECT: Use Enum or pattern matching
Enum.at(list, 0)
[first | _rest] = list
```

### Block Scoping

```elixir
# WRONG: Variables in blocks don't leak out
if condition do
  result = compute()
end
# result is NOT accessible here

# CORRECT: Capture the block result
result = if condition, do: compute(), else: default()
```

### Struct vs Map Access

```elixir
# WRONG: Bracket access on structs
user[:name]

# CORRECT: Dot notation for structs
user.name

# For changesets, use the API
Ecto.Changeset.get_field(changeset, :field)
```

### Atom Safety

```elixir
# NEVER: Convert user input to atoms (memory leak!)
String.to_atom(user_input)

# SAFE: Use existing atoms only
String.to_existing_atom(known_input)
```

### No elsif Keyword

```elixir
# WRONG: Elixir has no elsif
if x do
  # ...
elsif y do  # Does not exist!
  # ...
end

# CORRECT: Use cond
cond do
  x -> result1
  y -> result2
  true -> default
end
```

### Process Dictionary is a Code Smell

```elixir
# AVOID: Process dictionary usage is non-idiomatic
Process.put(:key, value)
Process.get(:key)

# PREFER: Pass state explicitly or use GenServer state
```

### Macros Only When Explicitly Requested

```elixir
# Don't reach for macros when functions suffice
# Only use macros when:
# 1. The user explicitly requests it
# 2. You need compile-time code generation
# 3. You're building DSLs that require it
```

## Naming Conventions

### Predicate Functions

```elixir
# Predicate functions end with ? and DON'T start with is_
def valid?(data), do: ...      # CORRECT
def empty?(list), do: ...      # CORRECT
def is_valid?(data), do: ...   # WRONG

# Reserve is_ prefix for guard-safe functions only
defguard is_positive(x) when is_number(x) and x > 0
defguard is_admin(user) when user.role == :admin
```

## Performance

### Stream vs Enum

```elixir
# AVOID: Enum on massive collections (loads all into memory)
huge_list |> Enum.map(&transform/1) |> Enum.filter(&valid?/1)

# PREFER: Stream for lazy evaluation on large datasets
huge_list
|> Stream.map(&transform/1)
|> Stream.filter(&valid?/1)
|> Enum.to_list()

# Stream is beneficial when:
# - Working with large datasets
# - Reading files line by line
# - Processing infinite sequences
# - Chaining multiple transformations before materializing
```

### List Operations

```elixir
# SLOW: O(n) - copies entire list
list ++ [new_item]

# FAST: O(1) - prepend then reverse if order matters
[new_item | list]
|> Enum.reverse()

# For building lists, prepend and reverse at the end
def build_list(items) do
  items
  |> Enum.reduce([], fn item, acc -> [transform(item) | acc] end)
  |> Enum.reverse()
end
```

### Prefer Enum.reduce Over Manual Recursion

```elixir
# AVOID: Manual tail recursion
def sum([]), do: 0
def sum([h | t]), do: h + sum(t)

# PREFER: Enum.reduce - clearer and optimized
def sum(list), do: Enum.reduce(list, 0, &+/2)

# Enum.reduce handles edge cases and is more readable
def build_map(list) do
  Enum.reduce(list, %{}, fn item, acc ->
    Map.put(acc, item.id, item)
  end)
end
```

## Concurrency

### Task.async_stream

```elixir
# Task.async_stream for concurrent operations with backpressure
items
|> Task.async_stream(&process_item/1, max_concurrency: 10, timeout: 30_000)
|> Enum.map(fn {:ok, result} -> result end)
```

### Task.Supervisor for Fault Tolerance

```elixir
# Use Task.Supervisor for better fault tolerance in production
# Define in your supervision tree:
children = [
  {Task.Supervisor, name: MyApp.TaskSupervisor}
]

# Start supervised tasks that won't crash the caller
Task.Supervisor.async_nolink(MyApp.TaskSupervisor, fn ->
  do_risky_work()
end)

# Handle failures explicitly with yield/shutdown
task = Task.Supervisor.async_nolink(MyApp.TaskSupervisor, fn -> work() end)

case Task.yield(task, 5_000) || Task.shutdown(task) do
  {:ok, result} -> {:ok, result}
  {:exit, reason} -> {:error, {:task_failed, reason}}
  nil -> {:error, :timeout}
end
```

## GenServer Usage (Infrastructure Only!)

```elixir
# DON'T: GenServer per entity
defmodule TaskServer do
  use GenServer
  # Storing task state in process - DON'T DO THIS
end

# DO: GenServer for infrastructure
defmodule TaskCache do
  use GenServer
  # Caching active tasks (transient data, can rebuild from DB)
end

defmodule RateLimiter do
  use GenServer
  # Tracking API request counts (acceptable to lose on crash)
end
```

## GenServer Best Practices

### State Management

```elixir
# Keep state simple and serializable
# GOOD: Maps, lists, tuples with primitive values
defmodule MyServer do
  def init(_) do
    {:ok, %{count: 0, items: [], last_updated: nil}}
  end
end

# AVOID: PIDs, refs, or complex structs in state that can't survive restarts
```

### Message Handling

```elixir
# Handle ALL expected messages explicitly
def handle_info(:timeout, state), do: {:noreply, handle_timeout(state)}
def handle_info({:DOWN, _ref, :process, _pid, _reason}, state), do: {:noreply, state}
def handle_info(unknown, state) do
  Logger.warning("Unexpected message: #{inspect(unknown)}")
  {:noreply, state}
end

# Use handle_continue/2 for post-init work (avoids blocking supervisor)
def init(args) do
  {:ok, initial_state(args), {:continue, :load_data}}
end

def handle_continue(:load_data, state) do
  # Heavy initialization here, not in init/1
  {:noreply, load_expensive_data(state)}
end

# Implement terminate/2 for cleanup when necessary
def terminate(_reason, state) do
  cleanup_resources(state)
  :ok
end
```

### Call vs Cast

```elixir
# Use call/3 for synchronous requests - PREFER THIS for back-pressure
def get_value(server), do: GenServer.call(server, :get_value)

# Use cast/2 for fire-and-forget only when you truly don't need confirmation
def log_event(server, event), do: GenServer.cast(server, {:log, event})

# When in doubt, use call over cast to ensure back-pressure
# cast can lead to unbounded mailbox growth under load

# Always set appropriate timeouts for call/3
GenServer.call(server, :expensive_operation, 30_000)  # 30 second timeout
```

### Supervision and Fault Tolerance

```elixir
# Use :max_restarts and :max_seconds to prevent restart loops
children = [
  {MyWorker, []}
]

Supervisor.init(children,
  strategy: :one_for_one,
  max_restarts: 3,      # Max 3 restarts
  max_seconds: 5        # Within 5 seconds, then supervisor crashes
)
```

---

# LIBRARIES

## Preferred Libraries

- **HTTP Client**: Use `Req` (NOT HTTPoison, NOT Tesla, NOT httpc)
- **LLM Integration**: Use `ReqLLM` + `Zoi` for LLM API calls with structured output
- **Email**: Use `Swoosh` for composing and delivering emails
- **JSON**: Use `Jason` (NOT Poison)

## Mix Tasks

```elixir
# ALWAYS read documentation before using unfamiliar tasks
mix help                    # List all available tasks
mix help task_name          # Documentation for specific task

# Common task patterns
mix deps.get                # Fetch dependencies
mix compile                 # Compile the project
mix format                  # Format code
mix test                    # Run tests
mix ecto.migrate            # Run migrations
```

## Req - HTTP Client

```elixir
defmodule TaskManager.Integration.HTTPClient do
  @moduledoc """
  HTTP client wrapper using Req.
  Req provides automatic retries, JSON encoding, and connection pooling.
  """

  def get(url, opts \\ []) do
    opts = default_options(opts)

    case Req.get(url, opts) do
      {:ok, %Req.Response{status: status, body: body}} when status in 200..299 ->
        {:ok, body}

      {:ok, %Req.Response{status: status, body: body}} ->
        {:error, {:http_error, status, body}}

      {:error, %Req.TransportError{reason: reason}} ->
        {:error, {:transport_error, reason}}
    end
  end

  def post(url, body, opts \\ []) do
    opts = default_options([json: body] ++ opts)

    case Req.post(url, opts) do
      {:ok, %Req.Response{status: status, body: body}} when status in 200..299 ->
        {:ok, body}

      {:ok, %Req.Response{status: status, body: body}} ->
        {:error, {:http_error, status, body}}

      {:error, %Req.TransportError{reason: reason}} ->
        {:error, {:transport_error, reason}}
    end
  end

  defp default_options(opts) do
    Keyword.merge([
      retry: :transient,
      retry_delay: &exponential_backoff/1,
      max_retries: 3,
      receive_timeout: 5_000
    ], opts)
  end

  defp exponential_backoff(retry_count) do
    base = Integer.pow(2, retry_count) * 1_000
    jitter = :rand.uniform(100)
    base + jitter
  end
end
```

## ReqLLM - LLM Integration

```elixir
defmodule TaskManager.AI.TaskClassifier do
  @moduledoc """
  Uses ReqLLM for LLM API calls with Zoi for validation.
  """

  @classification_schema Zoi.object(%{
    category: Zoi.enum([:bug, :feature, :chore, :docs]),
    priority: Zoi.enum([:low, :medium, :high, :urgent]),
    estimated_hours: Zoi.integer() |> Zoi.min(1) |> Zoi.max(100)
  })

  def classify_task(description) do
    prompt = """
    Classify this task and respond with JSON only:
    #{description}

    Response format: {"category": "bug|feature|chore|docs", "priority": "low|medium|high|urgent", "estimated_hours": 1-100}
    """

    with {:ok, response} <- ReqLLM.generate_text("anthropic:claude-sonnet-4-20250514", prompt),
         {:ok, json} <- Jason.decode(ReqLLM.Response.text(response)),
         {:ok, validated} <- Zoi.parse(@classification_schema, json) do
      {:ok, validated}
    end
  end
end
```

## Zoi - Runtime Validation

```elixir
defmodule TaskManager.Schemas.TaskInput do
  @moduledoc """
  Zoi validation schema for task input data.
  Demonstrates various Zoi types and validations.
  """

  @task_schema Zoi.object(%{
    # Required string with length constraints
    title: Zoi.string() |> Zoi.min(3) |> Zoi.max(200),

    # Optional string (can be omitted)
    description: Zoi.string() |> Zoi.optional(),

    # Enum with specific allowed values
    status: Zoi.enum([:todo, :in_progress, :blocked, :review, :done]),
    priority: Zoi.enum([:low, :medium, :high, :urgent]) |> Zoi.default(:medium),

    # Integer with range validation
    estimated_hours: Zoi.integer() |> Zoi.min(1) |> Zoi.max(1000) |> Zoi.optional(),

    # Float for decimal values
    completion_percentage: Zoi.float() |> Zoi.min(0.0) |> Zoi.max(100.0) |> Zoi.default(0.0),

    # Boolean with coercion (accepts "true"/"false" strings)
    is_billable: Zoi.boolean(coerce: true) |> Zoi.default(false),

    # Email validation
    reporter_email: Zoi.email(),

    # URL validation (optional)
    reference_url: Zoi.url() |> Zoi.optional(),

    # UUID validation
    project_id: Zoi.uuid(),

    # Date with coercion from string
    due_date: Zoi.date(coerce: true) |> Zoi.optional(),

    # Datetime with coercion
    scheduled_at: Zoi.datetime(coerce: true) |> Zoi.optional(),

    # Nullable field (can be explicitly nil)
    parent_task_id: Zoi.nullable(Zoi.uuid()),

    # Array of strings with item validation
    tags: Zoi.array(Zoi.string() |> Zoi.min(1) |> Zoi.max(50)) |> Zoi.default([]),

    # Array of nested objects
    attachments: Zoi.array(Zoi.object(%{
      filename: Zoi.string() |> Zoi.min(1),
      url: Zoi.url(),
      size_bytes: Zoi.integer() |> Zoi.min(0)
    })) |> Zoi.default([]),

    # Tuple for coordinates or pairs
    location: Zoi.tuple({Zoi.float(), Zoi.float()}) |> Zoi.optional(),

    # String with regex pattern
    task_code: Zoi.string() |> Zoi.regex(~r/^TSK-\d{4,}$/),

    # Custom refinement for business rules
    budget_cents: Zoi.integer()
      |> Zoi.min(0)
      |> Zoi.refine(fn value ->
        if rem(value, 100) == 0 do
          :ok
        else
          {:error, "budget must be in whole dollars"}
        end
      end)
      |> Zoi.optional()
  })

  def validate(params) do
    Zoi.parse(@task_schema, params)
  end

  def validate!(params) do
    case validate(params) do
      {:ok, data} -> data
      {:error, errors} -> raise "Validation failed: #{inspect(errors)}"
    end
  end
end
```

## Swoosh - Email

```elixir
# config/config.exs
config :my_app, MyApp.Mailer,
  adapter: Swoosh.Adapters.Sendgrid,
  api_key: System.get_env("SENDGRID_API_KEY")

# lib/my_app/mailer.ex
defmodule MyApp.Mailer do
  use Swoosh.Mailer, otp_app: :my_app
end

# lib/my_app/emails/user_email.ex
defmodule MyApp.Emails.UserEmail do
  import Swoosh.Email

  def welcome(user) do
    new()
    |> to({user.name, user.email})
    |> from({"MyApp", "noreply@myapp.com"})
    |> subject("Welcome to MyApp!")
    |> html_body("<h1>Hello #{user.name}</h1><p>Thanks for signing up.</p>")
    |> text_body("Hello #{user.name}\n\nThanks for signing up.")
  end

  def password_reset(user, reset_token) do
    new()
    |> to(user.email)
    |> from({"MyApp", "noreply@myapp.com"})
    |> subject("Password Reset Request")
    |> html_body("""
      <p>Click the link below to reset your password:</p>
      <a href="https://myapp.com/reset?token=#{reset_token}">Reset Password</a>
    """)
  end
end

# Usage in a context or controller
alias MyApp.Emails.UserEmail
alias MyApp.Mailer

def send_welcome_email(user) do
  user
  |> UserEmail.welcome()
  |> Mailer.deliver()
end
```

---

# PHOENIX

## Framework Principles (v1.7+)

### Context Modules

Organize business logic into context modules that provide a public API:

```elixir
defmodule TaskManager.Tasks do
  @moduledoc """
  The Tasks context - public API for task operations.
  """

  alias TaskManager.{Repo, Task}

  def list_tasks(opts \\ []) do
    Task
    |> apply_filters(opts)
    |> Repo.all()
  end

  def get_task(id) do
    Repo.get(Task, id)
  end

  def create_task(attrs) do
    %Task{}
    |> Task.changeset(attrs)
    |> Repo.insert()
  end
end
```

### Controllers (Stateless)

```elixir
defmodule TaskManagerWeb.TaskController do
  use TaskManagerWeb, :controller

  alias TaskManager.Tasks

  def index(conn, params) do
    tasks = Tasks.list_tasks(params)
    render(conn, :index, tasks: tasks)
  end

  def create(conn, %{"task" => task_params}) do
    case Tasks.create_task(task_params) do
      {:ok, task} ->
        conn
        |> put_flash(:info, "Task created")
        |> redirect(to: ~p"/tasks/#{task}")

      {:error, changeset} ->
        render(conn, :new, changeset: changeset)
    end
  end
end
```

### Template Structure

All LiveView templates must begin with `<Layouts.app flash={@flash} ...>` wrapping inner content. The `MyAppWeb.Layouts` module is pre-aliased in `my_app_web.ex`.

### Built-in Components

Use the framework's built-in `<.icon>` and `<.input>` components from `core_components.ex` exclusively. Do NOT use external component libraries like Heroicons or manual form inputs.

---

# ECTO

## Schema Design

```elixir
defmodule TaskManager.Task do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :binary_id, autogenerate: true}
  @foreign_key_type :binary_id

  schema "tasks" do
    field :title, :string
    field :description, :string
    field :status, Ecto.Enum, values: [:todo, :in_progress, :blocked, :review, :done], default: :todo
    field :priority, Ecto.Enum, values: [:low, :medium, :high, :urgent], default: :medium
    field :due_date, :date
    field :estimated_hours, :integer
    field :version, :integer, default: 1

    belongs_to :project, TaskManager.Project
    belongs_to :assignee, TaskManager.User
    has_many :comments, TaskManager.Comment

    timestamps()
  end

  def changeset(task, attrs) do
    task
    |> cast(attrs, [:title, :description, :status, :priority, :due_date, :estimated_hours, :project_id, :assignee_id])
    |> validate_required([:title])
    |> optimistic_lock(:version)
  end

  def transition_changeset(task, attrs) do
    task
    |> cast(attrs, [:status])
    |> validate_status_transition()
    |> optimistic_lock(:version)
  end

  defp validate_status_transition(changeset) do
    case get_change(changeset, :status) do
      nil -> changeset
      new_status ->
        old_status = get_field(changeset, :status)
        if valid_transition?(old_status, new_status) do
          changeset
        else
          add_error(changeset, :status, "invalid transition from #{old_status} to #{new_status}")
        end
    end
  end

  defp valid_transition?(from, to), do: to in Map.get(valid_transitions(), from, [])

  defp valid_transitions do
    %{
      todo: [:in_progress, :blocked],
      in_progress: [:blocked, :review, :done],
      blocked: [:todo, :in_progress],
      review: [:in_progress, :done],
      done: []
    }
  end
end
```

## Optimistic Locking

```elixir
defmodule TaskManager.Tasks do
  import Ecto.Changeset

  alias TaskManager.{Repo, Task}

  def update_task(task_id, new_attrs) do
    task = Repo.get!(Task, task_id)

    changeset =
      task
      |> change(new_attrs)
      |> optimistic_lock(:version)

    case Repo.update(changeset) do
      {:ok, updated} -> {:ok, updated}
      {:error, %Ecto.Changeset{} = changeset} ->
        if Keyword.has_key?(changeset.errors, :version) do
          {:error, :stale_entry}
        else
          {:error, changeset}
        end
    end
  end
end
```

## Ecto.Multi for Atomic Operations

```elixir
defmodule TaskManager.Boundaries.TaskService do
  alias Ecto.Multi
  alias TaskManager.{Repo, Task}
  alias TaskManager.Impl.TaskLogic

  def transition_task(task_id, new_status, opts \\ []) do
    Multi.new()
    |> Multi.run(:load_task, fn _repo, _changes ->
      case Repo.get(Task, task_id) do
        nil -> {:error, :not_found}
        task -> {:ok, task}
      end
    end)
    |> Multi.run(:validate_transition, fn _repo, %{load_task: task} ->
      if TaskLogic.can_transition?(task.status, new_status) do
        {:ok, task.status}
      else
        {:error, :invalid_transition}
      end
    end)
    |> Multi.run(:update_task, fn _repo, %{load_task: task} ->
      task
      |> Task.transition_changeset(%{status: new_status})
      |> Repo.update()
    end)
    |> Multi.run(:create_activity, fn _repo, %{validate_transition: old_status, update_task: task} ->
      create_activity_log(task, "status_changed", %{from: old_status, to: new_status})
    end)
    |> Multi.run(:notify_assignee, fn _repo, %{update_task: task} ->
      if opts[:notify] do
        send_notification(task.assignee_id, task)
      end
      {:ok, :done}
    end)
    |> Multi.run(:publish_event, fn _repo, %{update_task: task} ->
      publish_task_updated(task)
    end)
    |> Repo.transaction()
  end
end
```

## Money Handling

```elixir
# NEVER
field :amount, :float

# ALWAYS
field :amount, :integer    # Store cents: 100_00 = $100.00
field :balance, :decimal   # Or use Decimal for precision

# Why: 0.1 + 0.2 != 0.3 in floating point!
```

---

# LIVEVIEW

## Stream Management

**Always Use Streams for Collections** to prevent memory issues:

```elixir
# Template requires phx-update="stream" on parent with matching DOM IDs
<div id="messages" phx-update="stream">
  <div :for={{dom_id, message} <- @streams.messages} id={dom_id}>
    <%= message.content %>
  </div>
</div>

# Stream operations
socket |> stream(:messages, [new_msg])                    # Append
socket |> stream(:messages, [new_msg], reset: true)       # Reset
socket |> stream_delete(:messages, msg)                   # Delete
```

**Filtering Streams**: Streams aren't enumerable. To filter, refetch the data and re-stream the entire collection with `reset: true`.

## Form Best Practices

```elixir
# CORRECT: Use to_form/2 with changesets
@form = to_form(changeset)

# CORRECT: Access form fields in templates
<.input field={@form[:title]} type="text" label="Title" />

# WRONG: Never access changeset directly in template
<input value={@changeset[:title]} />
```

## HEEx Template Syntax

```elixir
# Interpolation in attributes - use curly braces
<div class={"text-#{@color}"}>

# Block constructs in tag bodies - use <%= %>
<div>
  <%= if @show do %>
    Content here
  <% end %>
</div>

# HTML comments in HEEx
<%!-- This is a comment --%>

# Literal curly braces - use phx-no-curly-interpolation
<pre phx-no-curly-interpolation>JSON: {"key": "value"}</pre>
```

## Error Prevention

Missing `current_scope` assign errors stem from improper route organization. Move routes to the correct `live_session` and pass `current_scope` to the layout component.

---

# DESIGN

## Frontend Design Guidance

**For UI/UX work, invoke Claude's `frontend-design` skill** which specializes in creating distinctive, production-grade frontend interfaces with high design quality.

## CSS Framework: Tailwind + DaisyUI

**For new Phoenix projects**, use:
- **Tailwind CSS v4** - Utility-first CSS framework
- **DaisyUI** - Component library built on Tailwind for rapid UI development

### Tailwind v4 Configuration

New import syntax (eliminates `tailwind.config.js`):
```css
@import "tailwindcss" source(none);
@source "../css";
@source "../js";
@source "../../lib/my_app_web";
```

### DaisyUI Setup

```elixir
# In mix.exs
defp deps do
  [
    {:tailwind, "~> 0.2", runtime: Mix.env() == :dev},
    # DaisyUI is added via npm/assets
  ]
end

# In assets/package.json
{
  "dependencies": {
    "daisyui": "^4.0.0"
  }
}

# In assets/css/app.css
@plugin "daisyui";
```

### DaisyUI Component Examples

```heex
<%!-- Button variants --%>
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-accent">Accent</button>

<%!-- Card component --%>
<div class="card bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Card Title</h2>
    <p>Card content here</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Action</button>
    </div>
  </div>
</div>

<%!-- Form inputs --%>
<input type="text" class="input input-bordered w-full max-w-xs" />
<select class="select select-bordered w-full max-w-xs">
  <option>Option 1</option>
</select>

<%!-- Alerts --%>
<div class="alert alert-success">
  <span>Success message!</span>
</div>
```

---

# TESTING

## Running Tests

```bash
# Run all tests
mix test

# Run specific file
mix test test/my_app/users_test.exs

# Run specific line (useful for debugging single test)
mix test test/my_app/users_test.exs:42

# Limit failures (useful for CI or large test suites)
mix test --max-failures 5

# Run only tests with specific tag
mix test --only integration

# Exclude tests with specific tag
mix test --exclude slow

# Run with coverage
mix test --cover
```

## Test Organization

```elixir
defmodule MyApp.UsersTest do
  use ExUnit.Case, async: true  # Enable async when tests are isolated

  # Tag tests for filtering
  @tag :slow
  test "expensive database operation" do
    # ...
  end

  @tag :integration
  test "external API call" do
    # ...
  end

  # Test exceptions
  test "raises on invalid input" do
    assert_raise ArgumentError, "invalid user id", fn ->
      Users.get!(nil)
    end
  end

  # Test error tuples
  test "returns error for missing user" do
    assert {:error, :not_found} = Users.get("nonexistent")
  end
end
```

## Best Practices

### Process Management

```elixir
# Use start_supervised! for automatic cleanup
start_supervised!({MyGenServer, []})

# Avoid manual Process.sleep
Process.sleep(100)

# Use Process.monitor for synchronization
ref = Process.monitor(pid)
assert_receive {:DOWN, ^ref, :process, ^pid, :normal}
```

### LiveView Testing

- Add DOM element IDs to templates for test targeting
- Favor element presence checks over text content validation
- Reference IDs in test assertions

### Property-Based Testing

```elixir
defmodule TaskManager.TaskLogicTest do
  use ExUnit.Case
  use ExUnitProperties

  property "priority score is always positive" do
    check all priority <- member_of([:low, :medium, :high, :urgent]),
              due_date <- one_of([constant(nil), date()]) do
      task = %{priority: priority, due_date: due_date}
      score = TaskLogic.calculate_priority_score(task)
      assert score >= 0
    end
  end
end
```

---

# ARCHITECTURE DOCUMENTATION

## When to Use This Skill

Invoke this skill when you need to:

- Design a new Elixir/Phoenix application from scratch
- Create comprehensive architecture documentation
- Plan OTP supervision trees and process architecture
- Define domain models with Ecto schemas
- Structure multi-app projects (Dave Thomas style)
- Create Architecture Decision Records (ADRs)
- Prepare handoff documentation for AI agent collaboration
- Set up guardrails for Director/Implementor AI workflows

## Project Structure Template

```
project_root/
├── README.md
├── CLAUDE.md
├── docs/
│   ├── HANDOFF.md
│   ├── architecture/
│   │   ├── 00_SYSTEM_OVERVIEW.md
│   │   ├── 01_DOMAIN_MODEL.md
│   │   ├── 02_DATA_LAYER.md
│   │   ├── 03_FUNCTIONAL_CORE.md
│   │   ├── 04_BOUNDARIES.md
│   │   ├── 05_LIFECYCLE.md
│   │   ├── 06_WORKERS.md
│   │   └── 07_INTEGRATION_PATTERNS.md
│   ├── design/          # Director AI fills during feature work
│   ├── plans/           # Director AI creates Superpowers plans
│   ├── api/             # Director AI documents API contracts
│   ├── decisions/       # ADRs
│   │   ├── ADR-001-framework-choice.md
│   │   ├── ADR-002-id-strategy.md
│   │   └── ADR-003-process-architecture.md
│   └── guardrails/
│       ├── NEVER_DO.md
│       ├── ALWAYS_DO.md
│       ├── DIRECTOR_ROLE.md
│       ├── IMPLEMENTOR_ROLE.md
│       └── CODE_REVIEW_CHECKLIST.md
```

## Tech Stack

- **Elixir** 1.17+ with OTP 27+
- **Phoenix** 1.7+ - Web framework
- **Ecto** - Database wrapper and query generator
- **PostgreSQL** 16+ - Primary database
- **Req** - HTTP client (NOT HTTPoison)
- **ReqLLM** - LLM integration library
- **Zoi** - Runtime data validation
- **Swoosh** - Email composition and delivery
- **Jason** - JSON encoding/decoding
- **Tailwind CSS v4** - Utility-first CSS
- **DaisyUI** - Component library for Tailwind

## Your Process

### Phase 1: Gather Requirements

Ask the user these essential questions:

1. **Project Domain**: What is the system for?
2. **Tech Stack**: Confirm Elixir + OTP + Phoenix + LiveView?
3. **Project Location**: Where should files be created?
4. **Structure Style**: Dave Thomas path-based dependencies or umbrella app?
5. **Special Requirements**: Multi-tenancy? Event sourcing? External integrations?
6. **Scale Targets**: Expected load, users, transactions per second?
7. **AI Collaboration**: Will Director and Implementor AIs be used?

### Phase 2: Expert Consultation

Launch parallel Task agents to research:

1. **Domain Patterns** - Research similar systems and proven architectures
2. **Framework Best Practices** - Ecto, Phoenix patterns
3. **Structure Analysis** - Study Dave Thomas's multi-app approach

### Phase 3: Create Documentation

Generate the complete documentation structure with:

- Foundation docs (README.md, CLAUDE.md)
- 5 guardrail documents
- 8 architecture documents
- Architecture Decision Records
- Handoff documentation

## Quality Gates

Before considering work complete:

- [ ] All code examples use valid Elixir syntax
- [ ] Every "NEVER DO" has a corresponding "ALWAYS DO"
- [ ] Every ADR explains alternatives and why they were rejected
- [ ] Domain model includes complete entity definitions with types
- [ ] Performance targets are specific and measurable
- [ ] Guardrails have clear, executable examples
- [ ] Testing strategy covers unit/integration/property tests

## Success Criteria

You've succeeded when:

1. Director AI can create feature designs without asking architectural questions
2. Implementor AI can write code without asking design questions
3. All major decisions are documented with clear rationale
4. Code examples are copy-paste ready
5. The system can be built by following the documentation alone
