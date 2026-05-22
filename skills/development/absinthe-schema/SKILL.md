---
name: absinthe-schema
description: Use when designing GraphQL schemas with Absinthe. Covers type definitions, interfaces, unions, enums, and schema organization patterns.
---

# Absinthe - Schema Design

Comprehensive guide to designing GraphQL schemas with Absinthe in Elixir.

## Key Concepts

### Type Definitions

```elixir
defmodule MyApp.Schema.Types do
  use Absinthe.Schema.Notation

  object :user do
    field :id, non_null(:id)
    field :name, non_null(:string)
    field :email, :string
    field :posts, list_of(:post) do
      resolve &MyApp.Resolvers.User.posts/3
    end
    field :inserted_at, :datetime
  end

  object :post do
    field :id, non_null(:id)
    field :title, non_null(:string)
    field :body, :string
    field :author, :user do
      resolve &MyApp.Resolvers.Post.author/3
    end
  end
end
```

### Interfaces

```elixir
interface :node do
  field :id, non_null(:id)

  resolve_type fn
    %MyApp.User{}, _ -> :user
    %MyApp.Post{}, _ -> :post
    _, _ -> nil
  end
end

object :user do
  interface :node
  field :id, non_null(:id)
  field :name, non_null(:string)
end
```

### Unions

```elixir
union :search_result do
  types [:user, :post, :comment]

  resolve_type fn
    %MyApp.User{}, _ -> :user
    %MyApp.Post{}, _ -> :post
    %MyApp.Comment{}, _ -> :comment
    _, _ -> nil
  end
end
```

### Enums

```elixir
enum :post_status do
  value :draft, as: "draft"
  value :published, as: "published"
  value :archived, as: "archived"
end
```

### Input Objects

```elixir
input_object :create_post_input do
  field :title, non_null(:string)
  field :body, :string
  field :status, :post_status, default_value: :draft
end
```

## Best Practices

1. **Organize types by domain** - Group related types in separate modules
2. **Use non_null sparingly** - Only for truly required fields
3. **Leverage interfaces** - For shared fields across types
4. **Define input objects** - For complex mutation arguments
5. **Use custom scalars** - For dates, UUIDs, JSON, etc.

## Schema Organization

```elixir
defmodule MyApp.Schema do
  use Absinthe.Schema

  import_types MyApp.Schema.Types
  import_types MyApp.Schema.Queries
  import_types MyApp.Schema.Mutations
  import_types MyApp.Schema.Subscriptions
  import_types Absinthe.Type.Custom  # DateTime, etc.

  query do
    import_fields :user_queries
    import_fields :post_queries
  end

  mutation do
    import_fields :user_mutations
    import_fields :post_mutations
  end

  subscription do
    import_fields :post_subscriptions
  end
end
```

## Custom Scalars

```elixir
scalar :uuid, name: "UUID" do
  serialize &to_string/1
  parse &parse_uuid/1
end

defp parse_uuid(%Absinthe.Blueprint.Input.String{value: value}) do
  case Ecto.UUID.cast(value) do
    {:ok, uuid} -> {:ok, uuid}
    :error -> :error
  end
end

defp parse_uuid(_), do: :error
```

## Anti-Patterns

- Avoid deeply nested types without pagination
- Don't expose database IDs directly without consideration
- Avoid circular dependencies in type definitions
- Don't skip field descriptions for documentation
