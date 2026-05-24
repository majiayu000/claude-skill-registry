---
name: elixir-otp-patterns
description: Use when Elixir OTP patterns including GenServer, Supervisor, Agent, and Task. Use when building concurrent, fault-tolerant Elixir applications.
allowed-tools:
  - Bash
  - Read
---

# Elixir OTP Patterns

Master OTP (Open Telecom Platform) patterns to build concurrent,
fault-tolerant Elixir applications. This skill covers GenServer,
Supervisor, Agent, Task, and other OTP behaviors.

## GenServer Basics

```elixir
defmodule Counter do
  use GenServer

  # Client API

  def start_link(initial_value \\ 0) do
    GenServer.start_link(__MODULE__, initial_value, name: __MODULE__)
  end

  def increment do
    GenServer.cast(__MODULE__, :increment)
  end

  def get_value do
    GenServer.call(__MODULE__, :get_value)
  end

  # Server Callbacks

  @impl true
  def init(initial_value) do
    {:ok, initial_value}
  end

  @impl true
  def handle_call(:get_value, _from, state) do
    {:reply, state, state}
  end

  @impl true
  def handle_cast(:increment, state) do
    {:noreply, state + 1}
  end
end

# Usage
{:ok, _pid} = Counter.start_link(0)
Counter.increment()
Counter.get_value()  # => 1
```

## GenServer with State Management

```elixir
defmodule UserCache do
  use GenServer

  # Client API

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, %{}, name: __MODULE__)
  end

  def put(user_id, user_data) do
    GenServer.cast(__MODULE__, {:put, user_id, user_data})
  end

  def get(user_id) do
    GenServer.call(__MODULE__, {:get, user_id})
  end

  def delete(user_id) do
    GenServer.cast(__MODULE__, {:delete, user_id})
  end

  def all do
    GenServer.call(__MODULE__, :all)
  end

  # Server Callbacks

  @impl true
  def init(_opts) do
    {:ok, %{}}
  end

  @impl true
  def handle_call({:get, user_id}, _from, state) do
    {:reply, Map.get(state, user_id), state}
  end

  @impl true
  def handle_call(:all, _from, state) do
    {:reply, state, state}
  end

  @impl true
  def handle_cast({:put, user_id, user_data}, state) do
    {:noreply, Map.put(state, user_id, user_data)}
  end

  @impl true
  def handle_cast({:delete, user_id}, state) do
    {:noreply, Map.delete(state, user_id)}
  end
end
```

## Supervisor Strategies

```elixir
defmodule MyApp.Application do
  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # One-for-one: restart only failed child
      {Counter, 0},
      {UserCache, []},

      # One-for-all supervisor
      {Supervisor,
       strategy: :one_for_all,
       name: MyApp.CriticalSupervisor,
       children: [
         {Database, []},
         {Cache, []}
       ]},

      # Rest-for-one supervisor
      {Supervisor,
       strategy: :rest_for_one,
       name: MyApp.OrderedSupervisor,
       children: [
         {ConfigLoader, []},
         {DatabasePool, []},
         {WebServer, []}
       ]}
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

## Dynamic Supervisor

```elixir
defmodule TaskRunner do
  use GenServer

  def start_link(task_id) do
    GenServer.start_link(__MODULE__, task_id)
  end

  @impl true
  def init(task_id) do
    Process.send_after(self(), :run_task, 0)
    {:ok, task_id}
  end

  @impl true
  def handle_info(:run_task, task_id) do
    # Perform task work
    IO.puts("Running task #{task_id}")
    {:noreply, task_id}
  end
end

defmodule TaskSupervisor do
  use DynamicSupervisor

  def start_link(_opts) do
    DynamicSupervisor.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  def start_task(task_id) do
    spec = {TaskRunner, task_id}
    DynamicSupervisor.start_child(__MODULE__, spec)
  end

  def stop_task(pid) do
    DynamicSupervisor.terminate_child(__MODULE__, pid)
  end

  @impl true
  def init(:ok) do
    DynamicSupervisor.init(strategy: :one_for_one)
  end
end

# Usage
TaskSupervisor.start_link([])
{:ok, pid} = TaskSupervisor.start_task(1)
TaskSupervisor.stop_task(pid)
```

## Agent for Simple State

```elixir
defmodule SimpleCounter do
  use Agent

  def start_link(initial_value) do
    Agent.start_link(fn -> initial_value end, name: __MODULE__)
  end

  def increment do
    Agent.update(__MODULE__, &(&1 + 1))
  end

  def decrement do
    Agent.update(__MODULE__, &(&1 - 1))
  end

  def value do
    Agent.get(__MODULE__, & &1)
  end

  def reset do
    Agent.update(__MODULE__, fn _ -> 0 end)
  end
end

# Usage
{:ok, _pid} = SimpleCounter.start_link(0)
SimpleCounter.increment()
SimpleCounter.value()  # => 1
```

## Task for Async Operations

```elixir
defmodule DataFetcher do
  def fetch_all do
    tasks = [
      Task.async(fn -> fetch_users() end),
      Task.async(fn -> fetch_posts() end),
      Task.async(fn -> fetch_comments() end)
    ]

    results = Task.await_many(tasks, 5000)

    %{
      users: Enum.at(results, 0),
      posts: Enum.at(results, 1),
      comments: Enum.at(results, 2)
    }
  end

  defp fetch_users do
    # Simulate API call
    Process.sleep(100)
    ["user1", "user2", "user3"]
  end

  defp fetch_posts do
    Process.sleep(200)
    ["post1", "post2"]
  end

  defp fetch_comments do
    Process.sleep(150)
    ["comment1", "comment2", "comment3"]
  end
end
```

## Task.Supervisor for Managed Tasks

```elixir
defmodule MyApp.TaskSupervisor do
  use Task.Supervisor

  def start_link(_opts) do
    Task.Supervisor.start_link(name: __MODULE__)
  end

  def run_task(fun) do
    Task.Supervisor.async(__MODULE__, fun)
  end

  def run_task_nolink(fun) do
    Task.Supervisor.async_nolink(__MODULE__, fun)
  end
end

# In application.ex
children = [
  {Task.Supervisor, name: MyApp.TaskSupervisor}
]

# Usage
task = Task.Supervisor.async(
  MyApp.TaskSupervisor,
  fn -> expensive_operation() end
)
result = Task.await(task)
```

## GenServer with Timeouts

```elixir
defmodule SessionManager do
  use GenServer

  @timeout 60_000  # 60 seconds

  def start_link(session_id) do
    GenServer.start_link(__MODULE__, session_id)
  end

  def refresh(pid) do
    GenServer.cast(pid, :refresh)
  end

  @impl true
  def init(session_id) do
    {:ok, session_id, @timeout}
  end

  @impl true
  def handle_cast(:refresh, state) do
    {:noreply, state, @timeout}
  end

  @impl true
  def handle_info(:timeout, state) do
    IO.puts("Session #{state} timed out")
    {:stop, :normal, state}
  end
end
```

## Registry for Process Lookup

```elixir
defmodule UserSession do
  use GenServer

  def start_link(user_id) do
    GenServer.start_link(
      __MODULE__,
      user_id,
      name: via_tuple(user_id)
    )
  end

  def via_tuple(user_id) do
    {:via, Registry, {MyApp.Registry, {:user_session, user_id}}}
  end

  def send_message(user_id, message) do
    case Registry.lookup(MyApp.Registry, {:user_session, user_id}) do
      [{pid, _}] ->
        GenServer.cast(pid, {:message, message})
      [] ->
        {:error, :not_found}
    end
  end

  @impl true
  def init(user_id) do
    {:ok, %{user_id: user_id, messages: []}}
  end

  @impl true
  def handle_cast({:message, message}, state) do
    {:noreply, %{state | messages: [message | state.messages]}}
  end
end

# In application.ex
children = [
  {Registry, keys: :unique, name: MyApp.Registry}
]
```

## Implementing GenServer with State Cleanup

```elixir
defmodule FileWatcher do
  use GenServer

  def start_link(file_path) do
    GenServer.start_link(__MODULE__, file_path)
  end

  @impl true
  def init(file_path) do
    case File.open(file_path, [:read]) do
      {:ok, file} ->
        schedule_check()
        {:ok, %{file: file, path: file_path, position: 0}}
      {:error, reason} ->
        {:stop, reason}
    end
  end

  @impl true
  def handle_info(:check, state) do
    # Read new lines from file
    schedule_check()
    {:noreply, state}
  end

  @impl true
  def terminate(_reason, %{file: file}) do
    File.close(file)
    :ok
  end

  defp schedule_check do
    Process.send_after(self(), :check, 1000)
  end
end
```

## Using ETS with GenServer

```elixir
defmodule CacheServer do
  use GenServer

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  def put(key, value) do
    GenServer.call(__MODULE__, {:put, key, value})
  end

  def get(key) do
    case :ets.lookup(__MODULE__, key) do
      [{^key, value}] -> {:ok, value}
      [] -> :not_found
    end
  end

  @impl true
  def init(:ok) do
    :ets.new(__MODULE__, [:named_table, :set, :public])
    {:ok, %{}}
  end

  @impl true
  def handle_call({:put, key, value}, _from, state) do
    :ets.insert(__MODULE__, {key, value})
    {:reply, :ok, state}
  end
end
```

## When to Use This Skill

Use elixir-otp-patterns when you need to:

- Build concurrent applications with isolated processes
- Implement fault-tolerant systems with supervision trees
- Manage application state across process lifecycles
- Create worker pools for async task processing
- Build real-time systems with multiple concurrent users
- Implement pub/sub or event-driven architectures
- Create distributed systems with process communication
- Handle long-running background jobs
- Build scalable web servers and APIs

## Best Practices

- Use GenServer for stateful processes with complex logic
- Use Agent for simple state that doesn't need custom logic
- Use Task for one-off async operations
- Always define proper supervision strategies
- Use Registry for dynamic process lookup
- Implement proper timeout handling
- Clean up resources in terminate/2 callbacks
- Use via tuples for named process registration
- Separate client API from server callbacks
- Keep handle_* functions focused and simple

## Common Pitfalls

- Not implementing proper supervision strategies
- Blocking GenServer calls with long-running operations
- Forgetting to handle :timeout messages
- Not cleaning up resources in terminate/2
- Using cast when you need synchronous confirmation
- Creating too many processes unnecessarily
- Not handling process exits properly
- Storing large data in process state instead of ETS
- Not using Registry for dynamic process management
- Ignoring backpressure in async operations

## Resources

- [Elixir GenServer Guide](https://hexdocs.pm/elixir/GenServer.html)
- [Supervisor Documentation](https://hexdocs.pm/elixir/Supervisor.html)
- [OTP Design Principles](https://www.erlang.org/doc/design_principles/des_princ.html)
- [Elixir in Action Book](https://www.manning.com/books/elixir-in-action-second-edition)
- [Agent Guide](https://hexdocs.pm/elixir/Agent.html)
- [Task Documentation](https://hexdocs.pm/elixir/Task.html)
