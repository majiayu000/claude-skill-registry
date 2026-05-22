---
name: elixir-otp-concurrency
description: Guide for OTP and Elixir concurrency. Use when implementing GenServers, designing supervision trees, or building fault-tolerant concurrent systems.
---

# Elixir OTP and Concurrency

This skill activates when working with OTP behaviors, building concurrent systems, managing processes, or implementing fault-tolerant architectures in Elixir.

## When to Use This Skill

Activate when:
- Implementing GenServer, GenStage, Supervisor, or other OTP behaviors
- Designing supervision trees and fault-tolerance strategies
- Working with Tasks, Agents, or process management
- Building concurrent or distributed systems
- Managing application state
- Troubleshooting process-related issues

## OTP Behaviors

### GenServer - Generic Server

Use GenServer for stateful processes:

```elixir
defmodule MyApp.Counter do
  use GenServer

  # Client API

  def start_link(initial_value) do
    GenServer.start_link(__MODULE__, initial_value, name: __MODULE__)
  end

  def increment do
    GenServer.call(__MODULE__, :increment)
  end

  def get_value do
    GenServer.call(__MODULE__, :get)
  end

  # Server Callbacks

  @impl true
  def init(initial_value) do
    {:ok, initial_value}
  end

  @impl true
  def handle_call(:increment, _from, state) do
    {:reply, state + 1, state + 1}
  end

  @impl true
  def handle_call(:get, _from, state) do
    {:reply, state, state}
  end
end
```

#### GenServer Best Practices

- Use `call` for synchronous requests that need a response
- Use `cast` for asynchronous fire-and-forget messages
- Use `handle_info` for receiving regular messages
- Keep server callbacks fast - delegate heavy work to Tasks
- Name processes with `via` tuples or Registry for dynamic naming
- Implement timeouts to prevent client processes from hanging

#### GenServer Patterns

**Background Work:**
```elixir
def init(state) do
  schedule_work()
  {:ok, state}
end

def handle_info(:work, state) do
  do_work(state)
  schedule_work()
  {:noreply, state}
end

defp schedule_work do
  Process.send_after(self(), :work, 5000)
end
```

**State Timeouts:**
```elixir
def handle_call(:get, _from, state) do
  {:reply, state, state, {:state_timeout, 30_000, :cleanup}}
end

def handle_state_timeout(:cleanup, state) do
  {:stop, :normal, state}
end
```

### Supervisor - Process Supervision

Build supervision trees for fault tolerance:

```elixir
defmodule MyApp.Application do
  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Database connection pool
      {MyApp.Repo, []},

      # PubSub system
      {Phoenix.PubSub, name: MyApp.PubSub},

      # Custom supervisor
      {MyApp.WorkerSupervisor, []},

      # Individual workers
      {MyApp.Cache, []},
      {MyApp.RateLimiter, []},

      # Web endpoint
      MyAppWeb.Endpoint
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

#### Supervision Strategies

**:one_for_one** - If a child dies, only that child is restarted
```elixir
Supervisor.start_link(children, strategy: :one_for_one)
```

**:one_for_all** - If any child dies, all children are terminated and restarted
```elixir
Supervisor.start_link(children, strategy: :one_for_all)
```

**:rest_for_one** - If a child dies, it and all children started after it are restarted
```elixir
Supervisor.start_link(children, strategy: :rest_for_one)
```

#### Dynamic Supervisors

For dynamically creating processes:

```elixir
defmodule MyApp.WorkerSupervisor do
  use DynamicSupervisor

  def start_link(init_arg) do
    DynamicSupervisor.start_link(__MODULE__, init_arg, name: __MODULE__)
  end

  def start_worker(args) do
    spec = {MyApp.Worker, args}
    DynamicSupervisor.start_child(__MODULE__, spec)
  end

  @impl true
  def init(_init_arg) do
    DynamicSupervisor.init(strategy: :one_for_one)
  end
end
```

#### Restart Strategies

Configure child restart behavior:

```elixir
children = [
  # Always restart (default)
  {MyApp.CriticalWorker, restart: :permanent},

  # Never restart
  {MyApp.OneTimeTask, restart: :temporary},

  # Only restart on abnormal exit
  {MyApp.OptionalWorker, restart: :transient}
]
```

### Task - Concurrent Work

#### Fire-and-forget Tasks

For concurrent work without needing results:

```elixir
Task.start(fn ->
  send_email(user, "Welcome!")
end)
```

#### Awaited Tasks

For concurrent work with results:

```elixir
task = Task.async(fn ->
  expensive_computation()
end)

# Do other work...

result = Task.await(task, 5000)  # 5 second timeout
```

#### Supervised Tasks

For long-running tasks under supervision:

```elixir
defmodule MyApp.Application do
  use Application

  def start(_type, _args) do
    children = [
      {Task.Supervisor, name: MyApp.TaskSupervisor}
    ]

    Supervisor.start_link(children, strategy: :one_for_one)
  end
end

# Use the supervised task
Task.Supervisor.start_child(MyApp.TaskSupervisor, fn ->
  long_running_operation()
end)
```

#### Concurrent Map

Process collections concurrently:

```elixir
# Sequential
results = Enum.map(urls, &fetch_url/1)

# Concurrent
results = Task.async_stream(urls, &fetch_url/1, max_concurrency: 10)
         |> Enum.to_list()
```

### Agent - Simple State Management

Use Agent for simple state:

```elixir
{:ok, agent} = Agent.start_link(fn -> %{} end, name: MyApp.Cache)

# Get state
value = Agent.get(MyApp.Cache, fn state -> Map.get(state, :key) end)

# Update state
Agent.update(MyApp.Cache, fn state -> Map.put(state, :key, value) end)

# Get and update atomically
Agent.get_and_update(MyApp.Cache, fn state ->
  {Map.get(state, :key), Map.delete(state, :key)}
end)
```

**When to use Agent vs GenServer:**
- Use Agent for simple key-value state
- Use GenServer when you need complex logic, callbacks, or process lifecycle management

## Process Communication

### send/receive

Basic message passing:

```elixir
# Send message
send(pid, {:hello, "world"})

# Receive message
receive do
  {:hello, msg} -> IO.puts(msg)
after
  5000 -> IO.puts("Timeout")
end
```

### Process Registration

Register processes by name:

```elixir
# Local registration
Process.register(self(), :my_process)
send(:my_process, :hello)

# Via Registry
{:ok, _} = Registry.start_link(keys: :unique, name: MyApp.Registry)

{:ok, pid} = GenServer.start_link(MyWorker, nil,
  name: {:via, Registry, {MyApp.Registry, "worker_1"}}
)

# Look up process
[{pid, _}] = Registry.lookup(MyApp.Registry, "worker_1")
```

### Process Links and Monitors

**Links** - Bidirectional, propagate exits:

```elixir
# Link processes
Process.link(pid)

# Spawn linked
spawn_link(fn -> do_work() end)
```

**Monitors** - Unidirectional, receive DOWN messages:

```elixir
ref = Process.monitor(pid)

receive do
  {:DOWN, ^ref, :process, ^pid, reason} ->
    IO.puts("Process died: #{inspect(reason)}")
end
```

## Concurrency Patterns

### Pipeline Pattern

Chain operations with concurrency:

```elixir
defmodule Pipeline do
  def process(data) do
    data
    |> async(&step1/1)
    |> async(&step2/1)
    |> async(&step3/1)
    |> await_all()
  end

  defp async(input, fun) do
    Task.async(fn -> fun.(input) end)
  end

  defp await_all(tasks) when is_list(tasks) do
    Enum.map(tasks, &Task.await/1)
  end
end
```

### Worker Pool

Implement a worker pool:

```elixir
defmodule MyApp.WorkerPool do
  use GenServer

  def start_link(opts) do
    pool_size = Keyword.get(opts, :size, 10)
    GenServer.start_link(__MODULE__, pool_size, name: __MODULE__)
  end

  def execute(fun) do
    GenServer.call(__MODULE__, {:execute, fun})
  end

  @impl true
  def init(pool_size) do
    workers = for _ <- 1..pool_size do
      {:ok, pid} = Task.Supervisor.start_link()
      pid
    end

    {:ok, %{workers: workers, index: 0}}
  end

  @impl true
  def handle_call({:execute, fun}, _from, state) do
    worker = Enum.at(state.workers, state.index)
    task = Task.Supervisor.async_nolink(worker, fun)

    new_index = rem(state.index + 1, length(state.workers))
    {:reply, task, %{state | index: new_index}}
  end
end
```

### Backpressure with GenStage

For producer-consumer pipelines:

```elixir
defmodule Producer do
  use GenStage

  def start_link(initial) do
    GenStage.start_link(__MODULE__, initial, name: __MODULE__)
  end

  def init(initial) do
    {:producer, initial}
  end

  def handle_demand(demand, state) do
    events = Enum.to_list(state..state + demand - 1)
    {:noreply, events, state + demand}
  end
end

defmodule Consumer do
  use GenStage

  def start_link() do
    GenStage.start_link(__MODULE__, :ok)
  end

  def init(:ok) do
    {:consumer, :ok}
  end

  def handle_events(events, _from, state) do
    Enum.each(events, &process_event/1)
    {:noreply, [], state}
  end
end
```

## ETS - Erlang Term Storage

In-memory key-value storage:

```elixir
# Create table
:ets.new(:my_table, [:named_table, :public, read_concurrency: true])

# Insert
:ets.insert(:my_table, {:key, "value"})

# Lookup
[{:key, value}] = :ets.lookup(:my_table, :key)

# Delete
:ets.delete(:my_table, :key)

# Match patterns
:ets.match(:my_table, {:"$1", "value"})

# Iterate
:ets.foldl(fn {k, v}, acc -> [{k, v} | acc] end, [], :my_table)
```

### ETS Best Practices

- Use `read_concurrency: true` for read-heavy workloads
- Use `write_concurrency: true` for write-heavy workloads
- Prefer `:set` (default) for unique keys
- Use `:bag` or `:duplicate_bag` for multiple values per key
- Always own ETS tables in a GenServer or Supervisor to prevent data loss

## Error Handling and Fault Tolerance

### Let It Crash Philosophy

Design for failure:

```elixir
# Don't do defensive programming
def process_order(order_id) do
  # Let it crash if order doesn't exist
  order = Repo.get!(Order, order_id)

  # Let it crash if validation fails
  {:ok, processed} = process(order)

  processed
end
```

### Proper Error Handling

When to handle errors vs let crash:

```elixir
# Handle expected errors
def fetch_user(id) do
  case HTTPoison.get("#{@api_url}/users/#{id}") do
    {:ok, %{status_code: 200, body: body}} ->
      Jason.decode(body)

    {:ok, %{status_code: 404}} ->
      {:error, :not_found}

    {:ok, %{status_code: status}} ->
      {:error, {:unexpected_status, status}}

    {:error, reason} ->
      {:error, {:network_error, reason}}
  end
end

# Let unexpected errors crash
def update_user!(id, params) do
  user = Repo.get!(User, id)  # Crash if not found

  user
  |> User.changeset(params)
  |> Repo.update!()  # Crash if invalid
end
```

### Circuit Breaker

Prevent cascading failures:

```elixir
defmodule CircuitBreaker do
  use GenServer

  def start_link(_) do
    GenServer.start_link(__MODULE__, %{status: :closed, failures: 0}, name: __MODULE__)
  end

  def call(fun) do
    case GenServer.call(__MODULE__, :status) do
      :open -> {:error, :circuit_open}
      :closed -> execute(fun)
    end
  end

  defp execute(fun) do
    try do
      result = fun.()
      GenServer.cast(__MODULE__, :success)
      {:ok, result}
    rescue
      e ->
        GenServer.cast(__MODULE__, :failure)
        {:error, e}
    end
  end

  @impl true
  def init(state), do: {:ok, state}

  @impl true
  def handle_call(:status, _from, state) do
    {:reply, state.status, state}
  end

  @impl true
  def handle_cast(:success, state) do
    {:noreply, %{state | failures: 0, status: :closed}}
  end

  @impl true
  def handle_cast(:failure, state) do
    new_failures = state.failures + 1

    if new_failures >= 5 do
      Process.send_after(self(), :half_open, 30_000)
      {:noreply, %{state | failures: new_failures, status: :open}}
    else
      {:noreply, %{state | failures: new_failures}}
    end
  end

  @impl true
  def handle_info(:half_open, state) do
    {:noreply, %{state | status: :closed, failures: 0}}
  end
end
```

## Testing Concurrent Systems

### Testing GenServers

```elixir
defmodule MyApp.CounterTest do
  use ExUnit.Case, async: true

  test "increments counter" do
    {:ok, pid} = MyApp.Counter.start_link(0)

    assert MyApp.Counter.increment(pid) == 1
    assert MyApp.Counter.increment(pid) == 2
    assert MyApp.Counter.get_value(pid) == 2
  end
end
```

### Testing Asynchronous Processes

```elixir
test "process receives message" do
  parent = self()

  spawn(fn ->
    receive do
      :ping -> send(parent, :pong)
    end
  end)

  send(pid, :ping)

  assert_receive :pong, 1000
end
```

### Testing Supervision

```elixir
test "supervisor restarts crashed worker" do
  {:ok, sup} = Supervisor.start_link([MyApp.Worker], strategy: :one_for_one)

  [{_, worker_pid, _, _}] = Supervisor.which_children(sup)

  # Crash the worker
  Process.exit(worker_pid, :kill)

  # Wait for restart
  Process.sleep(100)

  # Verify new worker started
  [{_, new_pid, _, _}] = Supervisor.which_children(sup)
  assert new_pid != worker_pid
  assert Process.alive?(new_pid)
end
```

## Debugging Concurrent Systems

### Observer

Launch Observer for visual process inspection:

```elixir
:observer.start()
```

### Process Info

Inspect running processes:

```elixir
# List all processes
Process.list()

# Process information
Process.info(pid)

# Message queue length
{:message_queue_len, count} = Process.info(pid, :message_queue_len)

# Current function
{:current_function, {mod, fun, arity}} = Process.info(pid, :current_function)
```

### Tracing

Use `:sys` module for debugging:

```elixir
# Enable tracing
:sys.trace(pid, true)

# Get state
:sys.get_state(pid)

# Get status
:sys.get_status(pid)
```

## Performance Considerations

### Process Spawning

- Processes are lightweight (< 2KB overhead)
- Spawning thousands/millions of processes is normal
- Use process pools when spawn rate is very high

### Message Passing

- Messages are copied between processes
- Large messages are expensive - consider ETS or persistent_term
- Use binary for efficient large data transfer

### Bottlenecks

- Single GenServer can become bottleneck
- Solution: shard state across multiple processes
- Use ETS with `read_concurrency` for read-heavy workloads

## Key Principles

- **Embrace concurrency**: Use processes liberally, they're cheap
- **Let it crash**: Don't write defensive code, use supervision
- **Isolate failures**: Design supervision trees to contain failures
- **Communicate via messages**: Avoid shared state between processes
- **Use the right tool**: GenServer for state, Task for work, Agent for simple state
- **Test at boundaries**: Test process APIs, not internal implementation
- **Monitor and observe**: Use Observer and logging to understand system behavior
