---
name: elixir-expert
version: 1.0.0
description: Expert-level Elixir, Phoenix, OTP, and concurrent systems
category: languages
tags: [elixir, phoenix, otp, erlang, concurrent, functional]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(elixir:*, mix:*)
---

# Elixir Expert

Expert guidance for Elixir programming, Phoenix framework, OTP, and building highly concurrent, fault-tolerant systems.

## Core Concepts

### Elixir Fundamentals
- Functional programming
- Pattern matching
- Immutability
- Pipe operator
- Modules and functions
- Structs and maps

### OTP (Open Telecom Platform)
- GenServer
- Supervisors
- Applications
- Tasks
- Agents
- ETS (Erlang Term Storage)

### Phoenix Framework
- Contexts and schemas
- LiveView
- Channels (WebSockets)
- Plug
- Ecto (database)
- Testing

## Elixir Basics

```elixir
# Pattern matching
{:ok, result} = {:ok, 42}
[head | tail] = [1, 2, 3, 4]

# Functions
defmodule Math do
  def add(a, b), do: a + b

  def factorial(0), do: 1
  def factorial(n) when n > 0, do: n * factorial(n - 1)
end

# Pipe operator
"hello"
|> String.upcase()
|> String.reverse()
# "OLLEH"

# Anonymous functions
add = fn a, b -> a + b end
add.(1, 2)  # 3

# Capture operator
add = &(&1 + &2)
Enum.map([1, 2, 3], &(&1 * 2))

# Structs
defmodule User do
  defstruct [:id, :name, :email, age: 0]
end

user = %User{id: "123", name: "John", email: "john@example.com"}

# Pattern matching with structs
%User{name: name} = user

# Maps
user_map = %{id: "123", name: "John", email: "john@example.com"}
%{name: name} = user_map

# Conditionals
if user.age >= 18 do
  "Adult"
else
  "Minor"
end

# Case
case user.role do
  :admin -> "Administrator"
  :user -> "Regular user"
  _ -> "Unknown"
end

# Cond
cond do
  user.age < 13 -> "Child"
  user.age < 18 -> "Teen"
  user.age < 65 -> "Adult"
  true -> "Senior"
end

# With
with {:ok, user} <- fetch_user(id),
     {:ok, posts} <- fetch_posts(user.id) do
  {:ok, user, posts}
else
  {:error, reason} -> {:error, reason}
end
```

## GenServer

```elixir
defmodule UserCache do
  use GenServer

  # Client API
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, %{}, opts)
  end

  def get(server, key) do
    GenServer.call(server, {:get, key})
  end

  def put(server, key, value) do
    GenServer.cast(server, {:put, key, value})
  end

  # Server Callbacks
  @impl true
  def init(initial_state) do
    {:ok, initial_state}
  end

  @impl true
  def handle_call({:get, key}, _from, state) do
    {:reply, Map.get(state, key), state}
  end

  @impl true
  def handle_cast({:put, key, value}, state) do
    {:noreply, Map.put(state, key, value)}
  end

  @impl true
  def handle_info(:cleanup, state) do
    # Periodic cleanup
    {:noreply, state}
  end
end

# Usage
{:ok, cache} = UserCache.start_link()
UserCache.put(cache, :user1, %User{name: "John"})
UserCache.get(cache, :user1)
```

## Supervisors

```elixir
defmodule MyApp.Application do
  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Database connection pool
      {MyApp.Repo, []},

      # GenServer workers
      {UserCache, name: UserCache},
      {SessionManager, name: SessionManager},

      # Task supervisor
      {Task.Supervisor, name: MyApp.TaskSupervisor},

      # Phoenix endpoint
      MyAppWeb.Endpoint
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end

# Custom supervisor
defmodule WorkerSupervisor do
  use Supervisor

  def start_link(init_arg) do
    Supervisor.start_link(__MODULE__, init_arg, name: __MODULE__)
  end

  @impl true
  def init(_init_arg) do
    children = [
      {Worker, id: :worker1, restart: :permanent},
      {Worker, id: :worker2, restart: :temporary},
      {Worker, id: :worker3, restart: :transient}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end
end
```

## Phoenix Framework

```elixir
# Router
defmodule MyAppWeb.Router do
  use MyAppWeb, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/api", MyAppWeb do
    pipe_through :api

    resources "/users", UserController, except: [:new, :edit]
    get "/users/:id/posts", UserController, :posts
  end
end

# Controller
defmodule MyAppWeb.UserController do
  use MyAppWeb, :controller

  alias MyApp.Accounts
  alias MyApp.Accounts.User

  def index(conn, params) do
    users = Accounts.list_users(params)
    render(conn, "index.json", users: users)
  end

  def show(conn, %{"id" => id}) do
    case Accounts.get_user(id) do
      nil ->
        conn
        |> put_status(:not_found)
        |> json(%{error: "User not found"})

      user ->
        render(conn, "show.json", user: user)
    end
  end

  def create(conn, %{"user" => user_params}) do
    case Accounts.create_user(user_params) do
      {:ok, user} ->
        conn
        |> put_status(:created)
        |> put_resp_header("location", Routes.user_path(conn, :show, user))
        |> render("show.json", user: user)

      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> render(MyAppWeb.ChangesetView, "error.json", changeset: changeset)
    end
  end
end

# Context
defmodule MyApp.Accounts do
  import Ecto.Query
  alias MyApp.Repo
  alias MyApp.Accounts.User

  def list_users(params \\ %{}) do
    User
    |> apply_filters(params)
    |> Repo.all()
  end

  def get_user(id), do: Repo.get(User, id)

  def create_user(attrs) do
    %User{}
    |> User.changeset(attrs)
    |> Repo.insert()
  end

  def update_user(%User{} = user, attrs) do
    user
    |> User.changeset(attrs)
    |> Repo.update()
  end

  defp apply_filters(query, params) do
    Enum.reduce(params, query, fn
      {"name", name}, query ->
        from u in query, where: ilike(u.name, ^"%#{name}%")

      {"age_min", age}, query ->
        from u in query, where: u.age >= ^age

      _, query ->
        query
    end)
  end
end
```

## Ecto

```elixir
# Schema
defmodule MyApp.Accounts.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :name, :string
    field :email, :string
    field :age, :integer
    field :role, Ecto.Enum, values: [:admin, :user, :guest]

    has_many :posts, MyApp.Blog.Post

    timestamps()
  end

  def changeset(user, attrs) do
    user
    |> cast(attrs, [:name, :email, :age, :role])
    |> validate_required([:name, :email])
    |> validate_format(:email, ~r/@/)
    |> validate_number(:age, greater_than: 0, less_than: 150)
    |> unique_constraint(:email)
  end
end

# Queries
import Ecto.Query

# Simple query
Repo.all(from u in User, where: u.age > 18)

# With preload
Repo.all(from u in User, preload: [:posts])

# Complex query
query =
  from u in User,
    join: p in assoc(u, :posts),
    where: u.age > 18,
    group_by: u.id,
    having: count(p.id) > 5,
    select: {u, count(p.id)}

Repo.all(query)

# Dynamic queries
defmodule UserQueries do
  import Ecto.Query

  def base_query, do: from(u in User)

  def filter_by_age(query, min_age) do
    from u in query, where: u.age >= ^min_age
  end

  def filter_by_role(query, role) do
    from u in query, where: u.role == ^role
  end

  def with_posts(query) do
    from u in query, preload: [:posts]
  end
end

# Usage
User
|> UserQueries.base_query()
|> UserQueries.filter_by_age(18)
|> UserQueries.filter_by_role(:admin)
|> UserQueries.with_posts()
|> Repo.all()
```

## Phoenix LiveView

```elixir
defmodule MyAppWeb.UserLive.Index do
  use MyAppWeb, :live_view

  alias MyApp.Accounts

  @impl true
  def mount(_params, _session, socket) do
    if connected?(socket) do
      Phoenix.PubSub.subscribe(MyApp.PubSub, "users")
    end

    {:ok, assign(socket, users: Accounts.list_users())}
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket) do
    user = Accounts.get_user!(id)
    {:ok, _} = Accounts.delete_user(user)

    {:noreply, assign(socket, users: Accounts.list_users())}
  end

  @impl true
  def handle_info({:user_created, user}, socket) do
    {:noreply, update(socket, :users, fn users -> [user | users] end)}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div>
      <h1>Users</h1>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <%= for user <- @users do %>
            <tr>
              <td><%= user.name %></td>
              <td><%= user.email %></td>
              <td>
                <button phx-click="delete" phx-value-id={user.id}>
                  Delete
                </button>
              </td>
            </tr>
          <% end %>
        </tbody>
      </table>
    </div>
    """
  end
end
```

## Concurrency

```elixir
# Tasks
task = Task.async(fn -> expensive_computation() end)
result = Task.await(task)

# Parallel processing
results =
  [1, 2, 3, 4, 5]
  |> Enum.map(&Task.async(fn -> process(&1) end))
  |> Enum.map(&Task.await/1)

# Task supervisor
Task.Supervisor.async_nolink(MyApp.TaskSupervisor, fn ->
  perform_background_job()
end)

# Agents
{:ok, agent} = Agent.start_link(fn -> %{} end)
Agent.update(agent, fn state -> Map.put(state, :key, "value") end)
Agent.get(agent, fn state -> Map.get(state, :key) end)

# ETS
table = :ets.new(:my_table, [:set, :public])
:ets.insert(table, {:key, "value"})
:ets.lookup(table, :key)
```

## Best Practices

### Elixir
- Use pattern matching extensively
- Leverage pipe operator
- Write small, focused functions
- Handle all pattern match cases
- Use proper error handling
- Follow naming conventions
- Write documentation

### OTP
- Use GenServers for state
- Implement supervisors properly
- Design for failure
- Keep processes focused
- Use process monitoring
- Implement timeouts
- Log appropriately

### Phoenix
- Follow context boundaries
- Use changesets for validation
- Implement proper authentication
- Handle errors gracefully
- Test thoroughly
- Use LiveView for interactivity
- Optimize queries

## Anti-Patterns

❌ Using mutable state
❌ Long-running GenServer calls
❌ Not supervising processes
❌ Ignoring errors
❌ Large modules
❌ N+1 query problems
❌ Not using pattern matching

## Resources

- Elixir: https://elixir-lang.org/
- Phoenix: https://www.phoenixframework.org/
- Hex: https://hex.pm/
- Elixir School: https://elixirschool.com/
- Programming Elixir (book)
