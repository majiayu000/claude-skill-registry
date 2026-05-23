---
name: phoenix-routing
description: Define routes and URL helpers in Phoenix applications including resources, scopes, pipelines, and verified routes
allowed-tools: [Bash, Read]
---

# Phoenix Routing

Phoenix routing maps incoming HTTP requests to controller actions. The router is the entry point for all web requests and determines which controller action should handle each request. Phoenix provides powerful routing macros for RESTful resources, scopes, pipelines, and verified routes.

## Basic Route Declaration

### Single Routes

Define individual routes using HTTP verb macros:

```elixir
get "/", PageController, :home
```

Phoenix supports all standard HTTP verbs:

```elixir
get "/users", UserController, :index
post "/users", UserController, :create
patch "/users/:id", UserController, :update
put "/users/:id", UserController, :update
delete "/users/:id", UserController, :delete
```

### Routes with Dynamic Segments

Capture URL parameters using the `:param_name` syntax:

```elixir
get "/hello/:messenger", HelloController, :show
```

The `:messenger` segment becomes available in the controller's params map.

## Resource Routes

### Basic Resource Declaration

Generate all standard RESTful routes with the `resources` macro:

```elixir
resources "/users", UserController
```

This generates eight routes:

```text
GET     /users           UserController :index
GET     /users/:id/edit  UserController :edit
GET     /users/new       UserController :new
GET     /users/:id       UserController :show
POST    /users           UserController :create
PATCH   /users/:id       UserController :update
PUT     /users/:id       UserController :update
DELETE  /users/:id       UserController :delete
```

### Limiting Resource Routes

Use `:only` to generate specific routes:

```elixir
resources "/users", UserController, only: [:show]
resources "/posts", PostController, only: [:index, :show]
```

Use `:except` to exclude specific routes:

```elixir
resources "/users", UserController, except: [:create, :delete]
```

### Aliasing Resources

Customize the route path helper name with `:as`:

```elixir
resources "/users", UserController, as: :person
```

This generates path helpers like `~p"/person"` instead of `~p"/users"`.

### Nested Resources

Create hierarchical resource relationships:

```elixir
resources "/users", UserController do
  resources "/posts", PostController
end
```

Generated routes include the parent resource ID:

```text
GET     /users/:user_id/posts           PostController :index
GET     /users/:user_id/posts/:id/edit  PostController :edit
GET     /users/:user_id/posts/new       PostController :new
GET     /users/:user_id/posts/:id       PostController :show
POST    /users/:user_id/posts           PostController :create
PATCH   /users/:user_id/posts/:id       PostController :update
PUT     /users/:user_id/posts/:id       PostController :update
DELETE  /users/:user_id/posts/:id       PostController :delete
```

## Verified Routes

### Using the ~p Sigil

Phoenix provides compile-time verified routes using the `~p` sigil:

```elixir
# Static paths
~p"/users"
~p"/posts/new"

# Dynamic segments with variables
~p"/users/#{user_id}"
~p"/users/#{user_id}/posts/#{post_id}"
```

### Verified Routes with Structs

Pass structs directly to generate paths:

```elixir
~p"/users/#{@user}"
# Generates: "/users/42"

~p"/users/#{user}/posts/#{post}"
# Generates: "/users/42/posts/17"
```

Phoenix automatically extracts the ID using the `Phoenix.Param` protocol.

### Benefits of Verified Routes

1. **Compile-time validation** - Catch routing errors during compilation
2. **Refactoring safety** - Route changes are caught immediately
3. **Type safety** - Ensure correct parameter types
4. **URL slug support** - Easy transition to slug-based URLs

## Scopes

### Basic Scopes

Group routes under a common path prefix:

```elixir
scope "/admin", HelloWeb.Admin do
  pipe_through :browser

  resources "/users", UserController
end
```

Generated paths include the scope prefix:

```elixir
~p"/admin/users"
```

### Scopes with Aliases

Reduce repetition by aliasing controller modules:

```elixir
scope "/", HelloWeb do
  pipe_through :browser

  get "/", PageController, :home
  resources "/posts", PostController
end
```

### Nested Scopes

Create hierarchical route organization:

```elixir
scope "/api", HelloWeb.Api, as: :api do
  pipe_through :api

  scope "/v1", V1, as: :v1 do
    resources "/users", UserController
  end

  scope "/v2", V2, as: :v2 do
    resources "/users", UserController
  end
end
```

Generated path helpers reflect the nesting:

```elixir
~p"/api/v1/users"
~p"/api/v2/users"
```

## Pipelines

### Defining Pipelines

Pipelines group plugs that run for specific routes:

```elixir
pipeline :browser do
  plug :accepts, ["html"]
  plug :fetch_session
  plug :fetch_live_flash
  plug :put_root_layout, html: {HelloWeb.Layouts, :root}
  plug :protect_from_forgery
  plug :put_secure_browser_headers
end

pipeline :api do
  plug :accepts, ["json"]
end
```

### Applying Pipelines to Scopes

Use `pipe_through` to apply pipelines:

```elixir
scope "/", HelloWeb do
  pipe_through :browser

  get "/", PageController, :home
  resources "/users", UserController
end

scope "/api", HelloWeb.Api do
  pipe_through :api

  resources "/users", UserController
end
```

### Custom Plugs in Pipelines

Add application-specific plugs:

```elixir
pipeline :browser do
  plug :accepts, ["html"]
  plug :fetch_session
  plug :fetch_live_flash
  plug :put_root_layout, html: {HelloWeb.Layouts, :root}
  plug :protect_from_forgery
  plug :put_secure_browser_headers
  plug HelloWeb.Plugs.Locale, "en"
end
```

### Nesting Pipelines

Compose pipelines for complex authentication flows:

```elixir
pipeline :auth do
  plug :browser
  plug :ensure_authenticated_user
  plug :ensure_user_owns_review
end

scope "/reviews", HelloWeb do
  pipe_through :auth

  resources "/", ReviewController
end
```

This applies the `:browser` pipeline first, then the authentication plugs.

## Advanced Pipeline Patterns

### Session Management Pipeline

Create a pipeline for session-based features:

```elixir
pipeline :browser do
  plug :accepts, ["html"]
  plug :fetch_session
  plug :fetch_live_flash
  plug :put_root_layout, html: {HelloWeb.Layouts, :root}
  plug :protect_from_forgery
  plug :put_secure_browser_headers
  plug :fetch_current_scope_for_user
end

defp fetch_current_scope_for_user(conn, _opts) do
  if id = get_session(conn, :scope_id) do
    assign(conn, :current_scope, MyApp.Scope.for_id(id))
  else
    id = System.unique_integer()

    conn
    |> put_session(:scope_id, id)
    |> assign(:current_scope, MyApp.Scope.for_id(id))
  end
end
```

### Multi-tenant Routing

Assign organization context from URL parameters:

```elixir
pipeline :browser do
  plug :accepts, ["html"]
  plug :fetch_session
  plug :fetch_live_flash
  plug :put_root_layout, html: {HelloWeb.Layouts, :root}
  plug :protect_from_forgery
  plug :put_secure_browser_headers
  plug :fetch_current_scope_for_user
  plug :assign_org_to_scope
end

defp assign_org_to_scope(conn, _opts) do
  case conn.params["org"] do
    nil -> conn
    org_slug ->
      scope = conn.assigns.current_scope
      org = MyApp.Organizations.get_by_slug!(org_slug)
      assign(conn, :current_scope, Map.put(scope, :organization, org))
  end
end
```

### Shopping Cart Pipeline

Fetch or create a cart for the current session:

```elixir
pipeline :browser do
  plug :accepts, ["html"]
  plug :fetch_session
  plug :fetch_live_flash
  plug :put_root_layout, html: {HelloWeb.Layouts, :root}
  plug :protect_from_forgery
  plug :put_secure_browser_headers
  plug :fetch_current_scope_for_user
  plug :fetch_current_cart
end

alias MyApp.ShoppingCart

defp fetch_current_cart(%{assigns: %{current_scope: scope}} = conn, _opts)
    when not is_nil(scope) do
  if cart = ShoppingCart.get_cart(scope) do
    assign(conn, :cart, cart)
  else
    {:ok, new_cart} = ShoppingCart.create_cart(scope, %{})
    assign(conn, :cart, new_cart)
  end
end

defp fetch_current_cart(conn, _opts), do: conn
```

## Forwarding

### Forward to Plugs

Delegate a path prefix to another plug or application:

```elixir
defmodule HelloWeb.Router do
  use HelloWeb, :router

  scope "/", HelloWeb do
    pipe_through :browser
    get "/", PageController, :home
  end

  forward "/jobs", BackgroundJob.Plug
end
```

All requests to `/jobs/*` are handled by `BackgroundJob.Plug`.

### Common Forward Use Cases

```elixir
# Admin interface
forward "/admin", HelloWeb.AdminRouter

# API documentation
forward "/api/docs", PhoenixSwagger.Plug.SwaggerUI

# Background job dashboard
forward "/jobs", Oban.Web.Router
```

## Inspecting Routes

### Using mix phx.routes

View all defined routes in your application:

```bash
mix phx.routes
```

Output shows HTTP verb, path, controller, and action:

```text
GET     /                HelloWeb.PageController :home
GET     /users           HelloWeb.UserController :index
GET     /users/:id/edit  HelloWeb.UserController :edit
GET     /users/new       HelloWeb.UserController :new
GET     /users/:id       HelloWeb.UserController :show
POST    /users           HelloWeb.UserController :create
PATCH   /users/:id       HelloWeb.UserController :update
PUT     /users/:id       HelloWeb.UserController :update
DELETE  /users/:id       HelloWeb.UserController :delete
```

### Filtering Routes

Grep for specific routes:

```bash
mix phx.routes | grep users
mix phx.routes | grep POST
```

## Building Paths Programmatically

### Static Paths

Build static paths easily:

```elixir
~p"/users"
# Returns: "/users"

~p"/posts/new"
# Returns: "/posts/new"
```

### Paths with Integer IDs

Interpolate IDs directly:

```elixir
user_id = 42
post_id = 17
~p"/users/#{user_id}/posts/#{post_id}"
# Returns: "/users/42/posts/17"
```

### Paths with Structs

Let Phoenix extract IDs from structs:

```elixir
~p"/users/#{user}/posts/#{post}"
# Returns: "/users/42/posts/17"
```

This uses the `Phoenix.Param` protocol to extract the ID.

### Custom Param Implementation

Implement custom URL generation for structs:

```elixir
defimpl Phoenix.Param, for: MyApp.Blog.Post do
  def to_param(%{slug: slug}), do: slug
end

# Now this generates slug-based URLs:
~p"/posts/#{post}"
# Returns: "/posts/my-great-post"
```

## Router Configuration Example

### Complete Router Setup

A typical Phoenix router includes multiple pipelines and scopes:

```elixir
defmodule HelloWeb.Router do
  use HelloWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_live_flash
    plug :put_root_layout, html: {HelloWeb.Layouts, :root}
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", HelloWeb do
    pipe_through :browser

    get "/", PageController, :home
    get "/hello", HelloController, :index
    get "/hello/:messenger", HelloController, :show
  end

  scope "/api/v1", HelloWeb.Api.V1, as: :api_v1 do
    pipe_through :api

    resources "/users", UserController, only: [:index, :show]
  end

  # Admin interface
  scope "/admin", HelloWeb.Admin, as: :admin do
    pipe_through [:browser, :admin_auth]

    resources "/users", UserController
    resources "/posts", PostController
  end

  # Enable LiveDashboard in development
  if Mix.env() in [:dev, :test] do
    import Phoenix.LiveDashboard.Router

    scope "/" do
      pipe_through :browser
      live_dashboard "/dashboard", metrics: HelloWeb.Telemetry
    end
  end
end
```

## When to Use This Skill

Use this skill when you need to:

1. Define new routes for controllers and actions
2. Create RESTful resource routes for CRUD operations
3. Organize routes with scopes and namespaces
4. Build nested resource relationships
5. Configure request processing pipelines
6. Generate verified route paths in controllers and templates
7. Implement API versioning with scoped routes
8. Debug routing issues and inspect available routes
9. Forward requests to external plugs or applications
10. Implement custom URL slug generation
11. Set up authentication and authorization pipelines
12. Create multi-tenant routing architectures
13. Build admin interfaces with separate scopes
14. Configure different response formats (HTML, JSON, etc.)

## Best Practices

1. **Use verified routes** - Always use `~p` sigil for compile-time safety
2. **Group related routes** - Use scopes to organize routes logically
3. **Limit resource actions** - Only generate routes you actually need
4. **Name scopes clearly** - Use descriptive scope prefixes and aliases
5. **Keep pipelines focused** - Each pipeline should have a single responsibility
6. **Order routes carefully** - More specific routes should come before general ones
7. **Use resources** - Prefer `resources` over individual route declarations
8. **Document custom routes** - Add comments for non-standard routing patterns
9. **Avoid deep nesting** - Limit nested resources to 2-3 levels maximum
10. **Version APIs** - Use scopes for API versioning
11. **Secure sensitive routes** - Apply authentication pipelines appropriately
12. **Test route resolution** - Verify routes resolve to correct controllers
13. **Use forward wisely** - Forward to well-defined plug interfaces
14. **Inspect regularly** - Use `mix phx.routes` during development
15. **Follow conventions** - Stick to RESTful conventions for resources

## Common Pitfalls

1. **Hardcoding paths** - Using strings instead of verified routes
2. **Over-nesting resources** - Creating deeply nested resource hierarchies
3. **Missing pipeline** - Forgetting to pipe routes through required pipelines
4. **Wrong route order** - General routes catching specific route requests
5. **Exposing all actions** - Generating unnecessary CRUD routes
6. **Not using scopes** - Repeating controller module prefixes
7. **Inconsistent naming** - Mixing naming conventions for routes
8. **Skipping CSRF protection** - Removing security plugs without understanding implications
9. **Missing authentication** - Not protecting sensitive routes
10. **Duplicate routes** - Defining the same route in multiple places
11. **Incorrect HTTP verbs** - Using wrong verbs for actions (GET for destructive actions)
12. **Not testing routes** - Failing to verify route configuration
13. **Exposing internal routes** - Making debug/admin routes available in production
14. **Complex route logic** - Putting business logic in route definitions
15. **Ignoring route conflicts** - Not checking for overlapping route patterns

## Resources

- [Phoenix Routing Guide](https://hexdocs.pm/phoenix/routing.html)
- [Phoenix.Router Documentation](https://hexdocs.pm/phoenix/Phoenix.Router.html)
- [Phoenix.VerifiedRoutes Documentation](https://hexdocs.pm/phoenix/Phoenix.VerifiedRoutes.html)
- [Plug.Router Documentation](https://hexdocs.pm/plug/Plug.Router.html)
- [Phoenix Plug Guide](https://hexdocs.pm/phoenix/plug.html)
- [Phoenix Request Lifecycle](https://hexdocs.pm/phoenix/request_lifecycle.html)
