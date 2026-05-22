---
name: absinthe-resolvers
description: Use when implementing GraphQL resolvers with Absinthe. Covers resolver patterns, dataloader integration, batching, and error handling.
---

# Absinthe - Resolvers

Guide to implementing efficient and maintainable resolvers in Absinthe.

## Key Concepts

### Basic Resolvers

```elixir
defmodule MyApp.Resolvers.User do
  alias MyApp.Accounts

  def list_users(_parent, args, _resolution) do
    {:ok, Accounts.list_users(args)}
  end

  def get_user(_parent, %{id: id}, _resolution) do
    case Accounts.get_user(id) do
      nil -> {:error, "User not found"}
      user -> {:ok, user}
    end
  end

  def create_user(_parent, %{input: input}, _resolution) do
    case Accounts.create_user(input) do
      {:ok, user} -> {:ok, user}
      {:error, changeset} -> {:error, changeset}
    end
  end
end
```

### Resolution Context

```elixir
def current_user(_parent, _args, %{context: %{current_user: user}}) do
  {:ok, user}
end

def current_user(_parent, _args, _resolution) do
  {:error, "Not authenticated"}
end
```

### Dataloader Integration

```elixir
defmodule MyApp.Schema do
  use Absinthe.Schema

  def context(ctx) do
    loader =
      Dataloader.new()
      |> Dataloader.add_source(MyApp.Repo, Dataloader.Ecto.new(MyApp.Repo))

    Map.put(ctx, :loader, loader)
  end

  def plugins do
    [Absinthe.Middleware.Dataloader] ++ Absinthe.Plugin.defaults()
  end
end

# In type definitions
object :user do
  field :posts, list_of(:post) do
    resolve dataloader(MyApp.Repo)
  end
end
```

### Custom Dataloader Source

```elixir
defmodule MyApp.Loaders.User do
  def data() do
    Dataloader.KV.new(&fetch/2)
  end

  defp fetch(:posts_count, user_ids) do
    counts = MyApp.Posts.count_by_user_ids(user_ids)

    Map.new(user_ids, fn id ->
      {id, Map.get(counts, id, 0)}
    end)
  end
end
```

## Best Practices

1. **Use Dataloader** - Prevents N+1 queries
2. **Keep resolvers thin** - Delegate to context modules
3. **Handle errors gracefully** - Return meaningful error messages
4. **Use middleware** - For cross-cutting concerns like auth
5. **Batch related queries** - Use dataloader batching

## Middleware

```elixir
defmodule MyApp.Middleware.Auth do
  @behaviour Absinthe.Middleware

  def call(resolution, _config) do
    case resolution.context do
      %{current_user: %{}} ->
        resolution
      _ ->
        resolution
        |> Absinthe.Resolution.put_result({:error, "Unauthorized"})
    end
  end
end

# Apply to fields
field :admin_data, :string do
  middleware MyApp.Middleware.Auth
  resolve &MyApp.Resolvers.Admin.get_data/3
end
```

## Error Handling

```elixir
defmodule MyApp.Resolvers.Helpers do
  def handle_changeset_errors(%Ecto.Changeset{} = changeset) do
    errors =
      Ecto.Changeset.traverse_errors(changeset, fn {msg, opts} ->
        Enum.reduce(opts, msg, fn {key, value}, acc ->
          String.replace(acc, "%{#{key}}", to_string(value))
        end)
      end)

    {:error, errors}
  end
end
```

## Anti-Patterns

- Avoid business logic in resolvers
- Don't query database directly in resolvers
- Avoid returning raw Ecto changesets
- Don't skip error handling
