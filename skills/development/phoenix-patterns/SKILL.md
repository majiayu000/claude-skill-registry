---
name: phoenix-patterns
description: Use when applying Phoenix Framework best practices including context design, controller patterns, and application architecture. Use when building Phoenix applications.
allowed-tools:
  - Bash
  - Read
---

# Phoenix Patterns

Master Phoenix Framework patterns to build well-structured, maintainable web applications in Elixir.

## Context Design

Contexts are dedicated modules that expose and group related functionality:

```elixir
defmodule MyApp.Accounts do
  @moduledoc """
  The Accounts context handles user management and authentication.
  """

  alias MyApp.Repo
  alias MyApp.Accounts.User

  def list_users do
    Repo.all(User)
  end

  def get_user!(id), do: Repo.get!(User, id)

  def get_user_by_email(email) do
    Repo.get_by(User, email: email)
  end

  def create_user(attrs \\ %{}) do
    %User{}
    |> User.changeset(attrs)
    |> Repo.insert()
  end

  def update_user(%User{} = user, attrs) do
    user
    |> User.changeset(attrs)
    |> Repo.update()
  end

  def delete_user(%User{} = user) do
    Repo.delete(user)
  end

  def change_user(%User{} = user, attrs \\ %{}) do
    User.changeset(user, attrs)
  end
end
```

## Controller Patterns

```elixir
defmodule MyAppWeb.UserController do
  use MyAppWeb, :controller

  alias MyApp.Accounts
  alias MyApp.Accounts.User

  action_fallback MyAppWeb.FallbackController

  def index(conn, _params) do
    users = Accounts.list_users()
    render(conn, :index, users: users)
  end

  def create(conn, %{"user" => user_params}) do
    with {:ok, %User{} = user} <- Accounts.create_user(user_params) do
      conn
      |> put_status(:created)
      |> put_resp_header("location", ~p"/api/users/#{user}")
      |> render(:show, user: user)
    end
  end

  def show(conn, %{"id" => id}) do
    user = Accounts.get_user!(id)
    render(conn, :show, user: user)
  end

  def update(conn, %{"id" => id, "user" => user_params}) do
    user = Accounts.get_user!(id)

    with {:ok, %User{} = user} <- Accounts.update_user(user, user_params) do
      render(conn, :show, user: user)
    end
  end

  def delete(conn, %{"id" => id}) do
    user = Accounts.get_user!(id)

    with {:ok, %User{}} <- Accounts.delete_user(user) do
      send_resp(conn, :no_content, "")
    end
  end
end
```

## Fallback Controller

```elixir
defmodule MyAppWeb.FallbackController do
  use MyAppWeb, :controller

  def call(conn, {:error, :not_found}) do
    conn
    |> put_status(:not_found)
    |> put_view(json: MyAppWeb.ErrorJSON)
    |> render(:"404")
  end

  def call(conn, {:error, %Ecto.Changeset{} = changeset}) do
    conn
    |> put_status(:unprocessable_entity)
    |> put_view(json: MyAppWeb.ChangesetJSON)
    |> render(:error, changeset: changeset)
  end

  def call(conn, {:error, :unauthorized}) do
    conn
    |> put_status(:unauthorized)
    |> put_view(json: MyAppWeb.ErrorJSON)
    |> render(:"401")
  end
end
```

## Plug Pipelines

```elixir
defmodule MyAppWeb.Router do
  use MyAppWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_live_flash
    plug :put_root_layout, html: {MyAppWeb.Layouts, :root}
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
    plug MyAppWeb.Plugs.Authenticate
  end

  pipeline :admin do
    plug MyAppWeb.Plugs.RequireAdmin
  end

  scope "/", MyAppWeb do
    pipe_through :browser
    get "/", PageController, :home
  end

  scope "/api", MyAppWeb do
    pipe_through :api

    resources "/users", UserController, except: [:new, :edit]

    scope "/admin" do
      pipe_through :admin
      resources "/settings", Admin.SettingsController
    end
  end
end
```

## Custom Plugs

```elixir
defmodule MyAppWeb.Plugs.Authenticate do
  import Plug.Conn

  def init(opts), do: opts

  def call(conn, _opts) do
    with ["Bearer " <> token] <- get_req_header(conn, "authorization"),
         {:ok, user} <- MyApp.Accounts.verify_token(token) do
      assign(conn, :current_user, user)
    else
      _ ->
        conn
        |> put_status(:unauthorized)
        |> Phoenix.Controller.put_view(json: MyAppWeb.ErrorJSON)
        |> Phoenix.Controller.render(:"401")
        |> halt()
    end
  end
end
```

## When to Use This Skill

Use phoenix-patterns when you need to:

- Structure Phoenix application architecture
- Design context boundaries
- Implement REST API controllers
- Create custom authentication/authorization
- Build reusable plug pipelines

## Best Practices

- Keep controllers thin, contexts fat
- Use action_fallback for error handling
- Group related functionality in contexts
- Use plugs for cross-cutting concerns
- Follow RESTful conventions in routing
- Separate API and browser pipelines

## Common Pitfalls

- Putting business logic in controllers
- Not using contexts for organization
- Creating overly large contexts
- Forgetting to handle errors properly
- Not using pipelines effectively
- Mixing concerns in single plugs
