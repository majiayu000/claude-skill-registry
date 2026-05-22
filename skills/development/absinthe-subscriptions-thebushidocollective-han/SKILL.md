---
name: absinthe-subscriptions
description: Use when implementing real-time GraphQL subscriptions with Absinthe. Covers Phoenix channels, PubSub, and subscription patterns.
---

# Absinthe - Subscriptions

Guide to implementing real-time GraphQL subscriptions with Absinthe and Phoenix.

## Key Concepts

### Basic Setup

```elixir
# In your Phoenix endpoint
defmodule MyAppWeb.Endpoint do
  use Phoenix.Endpoint, otp_app: :my_app
  use Absinthe.Phoenix.Endpoint

  socket "/socket", MyAppWeb.UserSocket,
    websocket: true,
    longpoll: false
end

# Socket configuration
defmodule MyAppWeb.UserSocket do
  use Phoenix.Socket
  use Absinthe.Phoenix.Socket, schema: MyApp.Schema

  def connect(params, socket, _connect_info) do
    current_user = get_user_from_token(params["token"])
    socket = Absinthe.Phoenix.Socket.put_options(socket,
      context: %{current_user: current_user}
    )
    {:ok, socket}
  end

  def id(socket), do: "user_socket:#{socket.assigns.user_id}"
end
```

### Defining Subscriptions

```elixir
defmodule MyApp.Schema.Subscriptions do
  use Absinthe.Schema.Notation

  object :post_subscriptions do
    field :post_created, :post do
      config fn _args, _resolution ->
        {:ok, topic: "posts"}
      end

      trigger :create_post, topic: fn _post ->
        "posts"
      end
    end

    field :post_updated, :post do
      arg :id, non_null(:id)

      config fn %{id: id}, _resolution ->
        {:ok, topic: "post:#{id}"}
      end

      trigger :update_post, topic: fn post ->
        "post:#{post.id}"
      end
    end
  end
end
```

### Publishing from Mutations

```elixir
defmodule MyApp.Resolvers.Post do
  def create_post(_parent, %{input: input}, _resolution) do
    case MyApp.Posts.create_post(input) do
      {:ok, post} ->
        # Publish to subscription
        Absinthe.Subscription.publish(
          MyAppWeb.Endpoint,
          post,
          post_created: "posts"
        )
        {:ok, post}
      {:error, changeset} ->
        {:error, changeset}
    end
  end
end
```

### User-Specific Subscriptions

```elixir
field :user_notification, :notification do
  config fn _args, %{context: %{current_user: user}} ->
    {:ok, topic: "user:#{user.id}:notifications"}
  end
end

# Publishing
Absinthe.Subscription.publish(
  MyAppWeb.Endpoint,
  notification,
  user_notification: "user:#{user_id}:notifications"
)
```

## Best Practices

1. **Scope subscriptions** - Use topics to limit data exposure
2. **Authenticate connections** - Verify users in socket connect
3. **Use triggers** - Automatically publish on mutations
4. **Handle disconnections** - Clean up resources on disconnect
5. **Rate limit subscriptions** - Prevent abuse

## PubSub Configuration

```elixir
# config/config.exs
config :my_app, MyAppWeb.Endpoint,
  pubsub_server: MyApp.PubSub

# application.ex
children = [
  {Phoenix.PubSub, name: MyApp.PubSub},
  MyAppWeb.Endpoint,
  {Absinthe.Subscription, MyAppWeb.Endpoint}
]
```

## Authorization in Subscriptions

```elixir
field :private_messages, :message do
  config fn _args, %{context: context} ->
    case context do
      %{current_user: %{id: user_id}} ->
        {:ok, topic: "user:#{user_id}:messages"}
      _ ->
        {:error, "Unauthorized"}
    end
  end
end
```

## Anti-Patterns

- Don't publish sensitive data to broad topics
- Avoid subscriptions without authentication
- Don't skip connection-level authorization
- Avoid overly granular topics (performance impact)
