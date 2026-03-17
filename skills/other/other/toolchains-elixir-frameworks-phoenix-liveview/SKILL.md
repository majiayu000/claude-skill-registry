---
name: phoenix-liveview
description: "Phoenix Framework with LiveView on the BEAM"
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Phoenix + LiveView on the BEAM for fault-tolerant, real-time web apps (OTP, Ecto, PubSub, Presence)."
    when_to_use:
      - "Building real-time, resilient web apps with minimal client-side JS"
      - "Needing fault tolerance, supervision, and soft-realtime latency on the BEAM"
      - "Using Ecto + Phoenix contexts for clear domain boundaries"
      - "Delivering interactive UI via LiveView without a heavy SPA bundle"
    quick_start:
      - "Install Erlang/Elixir (asdf or brew); mix archive.install hex phx_new"
      - "mix phx.new my_app --live && cd my_app && mix deps.get"
      - "mix ecto.create && mix phx.server (visit http://localhost:4000)"
  token_estimate:
    entry: 180
    full: 5600
---

# Phoenix + LiveView (Elixir/BEAM)

Phoenix builds on Elixir and the BEAM VM to deliver fault-tolerant, real-time web applications with minimal JavaScript. LiveView keeps UI state on the server while streaming HTML diffs over WebSockets. The BEAM provides lightweight processes, supervision trees, hot code upgrades, and soft-realtime scheduling.

**Key ideas**
- OTP supervision keeps web, data, and background processes isolated and restartable.
- Contexts encode domain boundaries (e.g., Accounts, Billing) around Ecto schemas and queries.
- LiveView renders HTML on the server, syncing UI state over WebSockets with minimal client code.
- PubSub + Presence enable fan-out updates, tracking, and collaboration features.

---

## Environment and Project Setup

```bash
# Erlang + Elixir via asdf (recommended)
asdf install erlang 27.0
asdf install elixir 1.17.3
asdf global erlang 27.0 elixir 1.17.3

# Install Phoenix generator
mix archive.install hex phx_new

# Create project with LiveView + Ecto + esbuild
mix phx.new my_app --live
cd my_app
mix deps.get
mix ecto.create
mix phx.server
```

Project layout (key pieces):
- `lib/my_app/application.ex` — OTP supervision tree (Repo, Endpoint, Telemetry, PubSub, Oban, etc.)
- `lib/my_app_web/endpoint.ex` — Endpoint, plugs, sockets, LiveView config
- `lib/my_app_web/router.ex` — Pipelines, scopes, routes, LiveSessions
- `lib/my_app/` — Contexts (domain modules) and Ecto schemas
- `test/support/{conn_case,data_case}.ex` — Testing helpers for Ecto + Phoenix

---

## BEAM + OTP Essentials

**Supervision tree (application.ex)**: keep short, isolated children.
```elixir
def start(_type, _args) do
  children = [
    MyApp.Repo,
    {Phoenix.PubSub, name: MyApp.PubSub},
    MyAppWeb.Endpoint,
    {Oban, Application.fetch_env!(:my_app, Oban)},
    MyApp.Metrics
  ]

  Supervisor.start_link(children, strategy: :one_for_one, name: MyApp.Supervisor)
end
```

**GenServer pattern**: wrap stateful services.
```elixir
defmodule MyApp.Counter do
  use GenServer

  def start_link(initial \\ 0), do: GenServer.start_link(__MODULE__, initial, name: __MODULE__)
  def increment(), do: GenServer.call(__MODULE__, :inc)

  @impl true
  def handle_call(:inc, _from, state) do
    new_state = state + 1
    {:reply, new_state, new_state}
  end
end
```

**BEAM principles**
- Prefer many small processes; processes are cheap and isolated.
- Supervise everything with clear restart strategies.
- Use message passing (`GenServer.cast`/`send`) to avoid shared state.
- Use ETS/Cachex for in-memory caches; keep them supervised.

---

## Phoenix Anatomy and Routing

**Pipelines and scopes (router.ex)**: keep browser/api concerns separated.
```elixir
defmodule MyAppWeb.Router do
  use MyAppWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_live_flash
    plug :protect_from_forgery
    plug :put_secure_browser_headers
    plug :fetch_current_user
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", MyAppWeb do
    pipe_through :browser
    live "/", HomeLive
    resources "/users", UserController
  end

  scope "/api", MyAppWeb do
    pipe_through :api
    resources "/users", Api.UserController, except: [:new, :edit]
  end
end
```

**Plugs**: composable request middleware. Keep plugs pure and short; prefer pipeline plugs over controller plugs when cross-cutting.

---

## Contexts and Ecto

**Schema + changeset**
```elixir
defmodule MyApp.Accounts.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :email, :string
    field :hashed_password, :string
    field :confirmed_at, :naive_datetime
    timestamps()
  end

  def registration_changeset(user, attrs) do
    user
    |> cast(attrs, [:email, :password])
    |> validate_required([:email, :password])
    |> validate_format(:email, ~r/@/)
    |> validate_length(:password, min: 12)
    |> unique_constraint(:email)
    |> put_password_hash()
  end

  defp put_password_hash(%{valid?: true} = changeset),
    do: put_change(changeset, :hashed_password, Argon2.hash_pwd_salt(get_change(changeset, :password)))
  defp put_password_hash(changeset), do: changeset
end
```

**Context API**
```elixir
defmodule MyApp.Accounts do
  import Ecto.Query, warn: false
  alias MyApp.{Repo, Accounts.User}

  def list_users, do: Repo.all(User)
  def get_user!(id), do: Repo.get!(User, id)

  def register_user(attrs) do
    %User{}
    |> User.registration_changeset(attrs)
    |> Repo.insert()
  end
end
```

**Transactions with Ecto.Multi**
```elixir
alias Ecto.Multi

def register_and_welcome(attrs) do
  Multi.new()
  |> Multi.insert(:user, User.registration_changeset(%User{}, attrs))
  |> Multi.run(:welcome_email, fn _repo, %{user: user} ->
    MyApp.Mailer.deliver_welcome(user)
    {:ok, :sent}
  end)
  |> Repo.transaction()
end
```

---

## LiveView Patterns

**LiveView module (stateful UI on server)**
```elixir
defmodule MyAppWeb.CounterLive do
  use MyAppWeb, :live_view

  def mount(_params, _session, socket) do
    {:ok, assign(socket, count: 0)}
  end

  def handle_event("inc", _params, socket) do
    {:noreply, update(socket, :count, &(&1 + 1))}
  end

  def render(assigns) do
    ~H"""
    <div class="space-y-4">
      <p class="text-lg">Count: <%= @count %></p>
      <button phx-click="inc" class="btn">Increment</button>
    </div>
    """
  end
end
```

**HEEx tips**
- Prefer `assign_new/3` to lazily compute expensive data only once per connected session.
- Use `stream/3` for large lists to minimize diff payloads.
- Handle params in `handle_params/3` for URL-driven state; avoid storing socket state in params.

**Live Components**
```elixir
defmodule MyAppWeb.NavComponent do
  use MyAppWeb, :live_component
  def render(assigns) do
    ~H"""
    <nav>
      <%= for item <- @items do %>
        <.link navigate={item.href}><%= item.label %></.link>
      <% end %>
    </nav>
    """
  end
end
```

**PubSub-driven LiveView**
```elixir
@impl true
def mount(_params, _session, socket) do
  if connected?(socket), do: Phoenix.PubSub.subscribe(MyApp.PubSub, "orders")
  {:ok, assign(socket, orders: [])}
end

@impl true
def handle_info({:order_created, order}, socket) do
  {:noreply, update(socket, :orders, fn orders -> [order | orders] end)}
end
```

---

## PubSub, Channels, and Presence

**Broadcast changes from contexts**
```elixir
def create_order(attrs) do
  with {:ok, order} <- %Order{} |> Order.changeset(attrs) |> Repo.insert() do
    Phoenix.PubSub.broadcast(MyApp.PubSub, "orders", {:order_created, order})
    {:ok, order}
  end
end
```

**Presence for online/typing indicators**
```elixir
defmodule MyAppWeb.RoomChannel do
  use Phoenix.Channel
  alias Phoenix.Presence

  def join("room:" <> room_id, _payload, socket) do
    send(self(), :after_join)
    {:ok, assign(socket, :room_id, room_id)}
  end

  def handle_info(:after_join, socket) do
    Presence.track(socket, socket.assigns.user_id, %{online_at: System.system_time(:second)})
    push(socket, "presence_state", Presence.list(socket))
    {:noreply, socket}
  end
end
```

**Security**: authorize topics in `join/3`, verify user tokens in params/session, and limit payload size.

---

## Testing Phoenix + LiveView

Use `mix test` with the generated helpers.

```elixir
# test/support/conn_case.ex
use MyAppWeb.ConnCase, async: true

test "renders home", %{conn: conn} do
  conn = get(conn, "/")
  assert html_response(conn, 200) =~ "Welcome"
end
```

```elixir
# LiveView test
use MyAppWeb.ConnCase, async: true
import Phoenix.LiveViewTest

test "counter increments", %{conn: conn} do
  {:ok, view, _html} = live(conn, "/counter")
  view |> element("button", "Increment") |> render_click()
  assert render(view) =~ "Count: 1"
end
```

**DataCase**: provide sandboxed DB connections; wrap tests in transactions to isolate data.

**Fixtures**: build factories with `ExMachina` or simple helper modules under `test/support/fixtures`.

---

## Performance, Ops, and Deployment

- **Telemetry**: Phoenix exposes events (`[:phoenix, :endpoint, ...]`). Export via `:telemetry_poller`, `OpentelemetryPhoenix`, and `OpentelemetryEcto`.
- **Assets**: `mix assets.deploy` runs npm install, esbuild, tailwind (if configured), and digests.
- **Releases**: `MIX_ENV=prod mix release`. Configure runtime env in `config/runtime.exs`. Start with `PHX_SERVER=true _build/prod/rel/my_app/bin/my_app start`.
- **Clustering**: add `libcluster` with DNS/epmd strategy for horizontal scale; use distributed PubSub/Presence.
- **Caching**: use ETS/Cachex for hot paths; prefer short TTLs and invalidate on write.
- **Background jobs**: Oban for retries/backoff; supervise it in application tree.
- **Hot path checks**: enable `:telemetry` metrics, check LiveView diff sizes, avoid large assigns; prefer streams.

---

## Common Pitfalls

- Forgetting to subscribe LiveViews to PubSub after `connected?/1` check — events will be missed on initial render.
- Doing heavy work inside LiveView render; move to contexts and precompute assigns.
- Not using `Ecto.Multi` for multi-step writes; failures leave partial state.
- Blocking BEAM schedulers with long NIFs or heavy CPU work; offload to ports/Oban jobs.
- Overusing global ETS without supervision or limits; leak memory.

---

## Reference Commands

- `mix phx.routes` — list routes and LiveView paths.
- `mix phx.gen.live Accounts User users email:string confirmed_at:naive_datetime` — generate LiveView CRUD (review context boundaries afterward).
- `mix format && mix credo --strict` — formatting and linting.
- `mix test --seed 0 --max-failures 1` — deterministic failures; pair with `mix test.watch`.

Phoenix + LiveView excels when domain logic stays in contexts, LiveViews stay thin, and the BEAM supervises every component for resilience.
