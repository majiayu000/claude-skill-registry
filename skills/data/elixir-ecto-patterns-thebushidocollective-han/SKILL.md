---
name: elixir-ecto-patterns
description: Use when Elixir Ecto patterns including schemas, changesets, queries, and transactions. Use when building database-driven Elixir applications.
allowed-tools:
  - Bash
  - Read
---

# Elixir Ecto Patterns

Master Ecto, Elixir's database wrapper and query generator. This skill
covers schemas, changesets, queries, associations, and transactions for
building robust database applications.

## Schema Definition

```elixir
defmodule MyApp.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :name, :string
    field :email, :string
    field :age, :integer
    field :is_active, :boolean, default: true
    field :role, Ecto.Enum, values: [:user, :admin, :moderator]

    has_many :posts, MyApp.Post
    belongs_to :organization, MyApp.Organization

    timestamps()
  end

  def changeset(user, attrs) do
    user
    |> cast(attrs, [:name, :email, :age, :is_active, :role])
    |> validate_required([:name, :email])
    |> validate_format(:email, ~r/@/)
    |> validate_number(:age, greater_than: 0, less_than: 150)
    |> unique_constraint(:email)
  end
end
```

## Changeset Validations

```elixir
defmodule MyApp.Post do
  use Ecto.Schema
  import Ecto.Changeset

  schema "posts" do
    field :title, :string
    field :body, :text
    field :published, :boolean, default: false
    field :tags, {:array, :string}, default: []

    belongs_to :user, MyApp.User

    timestamps()
  end

  def changeset(post, attrs) do
    post
    |> cast(attrs, [:title, :body, :published, :tags, :user_id])
    |> validate_required([:title, :body, :user_id])
    |> validate_length(:title, min: 3, max: 100)
    |> validate_length(:body, min: 10)
    |> foreign_key_constraint(:user_id)
  end

  def publish_changeset(post) do
    post
    |> change(published: true)
  end
end
```

## Basic Queries

```elixir
import Ecto.Query

# Get all users
Repo.all(User)

# Get user by ID
Repo.get(User, 1)
Repo.get!(User, 1)  # Raises if not found

# Get by specific field
Repo.get_by(User, email: "user@example.com")

# Filter with where clause
query = from u in User, where: u.age > 18
Repo.all(query)

# Select specific fields
query = from u in User, select: {u.id, u.name}
Repo.all(query)

# Order results
query = from u in User, order_by: [desc: u.inserted_at]
Repo.all(query)

# Limit and offset
query = from u in User, limit: 10, offset: 20
Repo.all(query)
```

## Complex Queries

```elixir
# Combining multiple conditions
query =
  from u in User,
    where: u.is_active == true,
    where: u.age >= 18,
    order_by: [desc: u.inserted_at],
    limit: 10

Repo.all(query)

# Using pipe syntax
User
|> where([u], u.is_active == true)
|> where([u], u.age >= 18)
|> order_by([u], desc: u.inserted_at)
|> limit(10)
|> Repo.all()

# Dynamic queries
def filter_users(params) do
  User
  |> filter_by_name(params["name"])
  |> filter_by_age(params["min_age"])
  |> Repo.all()
end

defp filter_by_name(query, nil), do: query
defp filter_by_name(query, name) do
  where(query, [u], ilike(u.name, ^"%#{name}%"))
end

defp filter_by_age(query, nil), do: query
defp filter_by_age(query, min_age) do
  where(query, [u], u.age >= ^min_age)
end
```

## Associations and Preloading

```elixir
# Preload associations
user = Repo.get(User, 1) |> Repo.preload(:posts)

# Preload nested associations
user = Repo.get(User, 1) |> Repo.preload([posts: :comments])

# Query with preload
query = from u in User, preload: [:posts, :organization]
Repo.all(query)

# Custom preload query
posts_query = from p in Post, where: p.published == true

query = from u in User, preload: [posts: ^posts_query]
Repo.all(query)

# Join and preload
query =
  from u in User,
    join: p in assoc(u, :posts),
    where: p.published == true,
    preload: [posts: p]

Repo.all(query)
```

## Aggregations and Grouping

```elixir
# Count records
Repo.aggregate(User, :count)

# Count with condition
query = from u in User, where: u.is_active == true
Repo.aggregate(query, :count)

# Other aggregations
Repo.aggregate(User, :avg, :age)
Repo.aggregate(User, :sum, :age)
Repo.aggregate(User, :max, :age)

# Group by
query =
  from u in User,
    group_by: u.role,
    select: {u.role, count(u.id)}

Repo.all(query)

# Group with having
query =
  from u in User,
    group_by: u.role,
    having: count(u.id) > 5,
    select: {u.role, count(u.id)}

Repo.all(query)
```

## Inserting and Updating

```elixir
# Insert with changeset
attrs = %{name: "John", email: "john@example.com", age: 30}

%User{}
|> User.changeset(attrs)
|> Repo.insert()

# Insert without changeset
Repo.insert(%User{name: "Jane", email: "jane@example.com"})

# Update
user = Repo.get(User, 1)

user
|> User.changeset(%{age: 31})
|> Repo.update()

# Update all
query = from u in User, where: u.is_active == false
Repo.update_all(query, set: [is_active: true])

# Delete
user = Repo.get(User, 1)
Repo.delete(user)

# Delete all
query = from u in User, where: u.is_active == false
Repo.delete_all(query)
```

## Transactions

```elixir
# Basic transaction
Repo.transaction(fn ->
  user = Repo.insert!(%User{name: "Alice"})
  Repo.insert!(%Post{title: "First post", user_id: user.id})
end)

# Multi for complex transactions
alias Ecto.Multi

Multi.new()
|> Multi.insert(:user, User.changeset(%User{}, user_attrs))
|> Multi.insert(:post, fn %{user: user} ->
  Post.changeset(%Post{}, Map.put(post_attrs, :user_id, user.id))
end)
|> Multi.run(:send_email, fn _repo, %{user: user} ->
  send_welcome_email(user)
end)
|> Repo.transaction()
```

## Embedded Schemas

```elixir
defmodule MyApp.Address do
  use Ecto.Schema
  import Ecto.Changeset

  embedded_schema do
    field :street, :string
    field :city, :string
    field :state, :string
    field :zip, :string
  end

  def changeset(address, attrs) do
    address
    |> cast(attrs, [:street, :city, :state, :zip])
    |> validate_required([:city, :state])
  end
end

defmodule MyApp.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :name, :string
    embeds_one :address, MyApp.Address

    timestamps()
  end

  def changeset(user, attrs) do
    user
    |> cast(attrs, [:name])
    |> cast_embed(:address, required: true)
  end
end
```

## Custom Ecto Types

```elixir
defmodule MyApp.Encrypted do
  use Ecto.Type

  def type, do: :binary

  def cast(value) when is_binary(value), do: {:ok, value}
  def cast(_), do: :error

  def dump(value) when is_binary(value) do
    {:ok, encrypt(value)}
  end

  def load(value) when is_binary(value) do
    {:ok, decrypt(value)}
  end

  defp encrypt(value) do
    # Encryption logic
    value
  end

  defp decrypt(value) do
    # Decryption logic
    value
  end
end

# Usage in schema
schema "users" do
  field :secret, MyApp.Encrypted
end
```

## When to Use This Skill

Use elixir-ecto-patterns when you need to:

- Build database-backed Elixir applications
- Define schemas and data models with validations
- Write complex database queries with Ecto's DSL
- Manage database relationships and associations
- Handle data transformations with changesets
- Implement transactions for data consistency
- Work with PostgreSQL, MySQL, or other databases
- Build Phoenix applications with database access
- Create robust data validation layers

## Best Practices

- Always use changesets for data validation
- Preload associations to avoid N+1 queries
- Use transactions for multi-step database operations
- Leverage Ecto.Multi for complex transaction logic
- Keep schemas focused and avoid god objects
- Use virtual fields for computed or temporary data
- Index foreign keys and frequently queried fields
- Use fragments for complex SQL when needed
- Write composable query functions
- Test database constraints and validations

## Common Pitfalls

- Not preloading associations (N+1 query problem)
- Forgetting to validate required fields
- Not using transactions for related operations
- Hardcoding queries instead of composing them
- Ignoring database constraints in schemas
- Not handling changeset errors properly
- Overusing embedded schemas for relational data
- Missing indexes on foreign keys
- Not using Repo.transaction for multi-step operations
- Exposing raw Ecto queries in business logic

## Resources

- [Ecto Documentation](https://hexdocs.pm/ecto/)
- [Ecto Query Guide](https://hexdocs.pm/ecto/Ecto.Query.html)
- [Ecto Changeset](https://hexdocs.pm/ecto/Ecto.Changeset.html)
- [Phoenix with Ecto](https://hexdocs.pm/phoenix/ecto.html)
- [Ecto Best Practices](https://hexdocs.pm/ecto/getting-started.html)
