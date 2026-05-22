---
name: ecto-schema-patterns
description: Use when defining data structures using Ecto schemas including fields, associations, embedded schemas, and schema metadata. Use for modeling domain data in Elixir applications.
allowed-tools:
  - Bash
  - Read
---

# Ecto Schema Patterns

Master Ecto schemas to define robust data structures for your Elixir applications.
This skill covers schema definitions, field types, associations, embedded schemas,
and advanced patterns for modeling complex domain data.

## Basic Schema Definition

```elixir
defmodule MyApp.User do
  use Ecto.Schema

  schema "users" do
    field :name, :string
    field :email, :string
    field :age, :integer
    field :confirmed_at, :naive_datetime

    timestamps()
  end
end
```

Schemas map to database tables and define the structure of your data. Each schema
has a source name (table name) and a list of fields with their types. The `timestamps()`
macro automatically adds `inserted_at` and `updated_at` fields.

## Field Types and Options

```elixir
defmodule MyApp.Product do
  use Ecto.Schema

  schema "products" do
    # Standard field types
    field :title, :string
    field :description, :string
    field :price, :decimal
    field :quantity, :integer
    field :is_active, :boolean, default: true
    field :published_at, :utc_datetime

    # Enum type
    field :status, Ecto.Enum, values: [:draft, :published, :archived]

    # Map type for unstructured data
    field :metadata, :map

    # Array type
    field :tags, {:array, :string}

    # Binary type for binary data
    field :image_data, :binary

    # Virtual field (not persisted to database)
    field :display_price, :string, virtual: true

    timestamps()
  end
end
```

Ecto supports a wide range of field types including strings, integers, decimals,
booleans, datetime types, enums, maps, arrays, and binary data. Virtual fields
exist only in memory and are useful for computed values.

## Using Map Type for Flexible Data

```elixir
defmodule MyApp.User do
  use Ecto.Schema

  schema "users" do
    field :name, :string
    field :email, :string
    field :data, :map

    timestamps()
  end
end

# Usage
user = %MyApp.User{
  name: "John Doe",
  email: "john@example.com",
  data: %{
    preferences: %{
      theme: "dark",
      notifications: true
    },
    settings: %{
      language: "en"
    }
  }
}
```

The `:map` type allows storing arbitrary Elixir maps in the database, providing
flexibility for unstructured or semi-structured data without requiring schema changes.

## Embedded Schemas

```elixir
defmodule MyApp.Address do
  use Ecto.Schema

  embedded_schema do
    field :street, :string
    field :city, :string
    field :state, :string
    field :zip_code, :string
    field :country, :string, default: "US"
  end
end
```

Embedded schemas define data structures that are not tied to a database table.
They can be embedded within other schemas or used independently in memory for
data validation and casting.

## Embedding One Association

```elixir
defmodule MyApp.Order do
  use Ecto.Schema

  schema "orders" do
    field :total, :decimal
    field :status, :string

    embeds_one :item, Item

    timestamps()
  end
end

defmodule MyApp.Item do
  use Ecto.Schema

  embedded_schema do
    field :title, :string
    field :price, :decimal
    field :quantity, :integer
  end
end
```

The `embeds_one` macro defines a one-to-one relationship with an embedded schema.
The embedded data is stored as a JSON or map column in the parent table, not in
a separate table.

## Inline Embedded Schema Definition

```elixir
defmodule MyApp.Parent do
  use Ecto.Schema

  schema "parents" do
    field :name, :string

    embeds_one :child, Child do
      field :name, :string
      field :age, :integer
    end

    timestamps()
  end
end
```

Schemas can be embedded inline using a `do` block, which creates a nested module
(e.g., `MyApp.Parent.Child`). This is useful for simpler embedded structures that
don't need to be defined separately.

## Embedding Many Association

```elixir
defmodule MyApp.Order do
  use Ecto.Schema

  schema "orders" do
    field :customer_name, :string
    field :total, :decimal

    embeds_many :items, OrderItem do
      field :product_name, :string
      field :quantity, :integer
      field :price, :decimal
    end

    timestamps()
  end
end
```

The `embeds_many` macro defines a one-to-many relationship with embedded schemas.
Multiple embedded records are stored as a JSON array in the parent table.

## Complex Embedded Schema with Custom Changeset

```elixir
defmodule MyApp.User do
  use Ecto.Schema

  schema "users" do
    field :full_name, :string
    field :email, :string
    field :avatar_url, :string
    field :confirmed_at, :naive_datetime

    embeds_one :profile, Profile do
      field :online, :boolean
      field :dark_mode, :boolean
      field :visibility, Ecto.Enum, values: [:public, :private, :friends_only]
    end

    timestamps()
  end

  def changeset(%__MODULE__{} = user, attrs \\ %{}) do
    user
    |> Ecto.Changeset.cast(attrs, [:full_name, :email])
    |> Ecto.Changeset.cast_embed(:profile, required: true, with: &profile_changeset/2)
  end

  def profile_changeset(profile, attrs \\ %{}) do
    profile
    |> Ecto.Changeset.cast(attrs, [:online, :dark_mode, :visibility])
    |> Ecto.Changeset.validate_required([:online, :visibility])
  end
end
```

Custom changeset functions can be defined for embedded schemas using the `:with`
option in `cast_embed/3`. This allows for specific validation logic on nested data.

## Extracted Embedded Schema Module

```elixir
# user/user.ex
defmodule MyApp.User do
  use Ecto.Schema

  schema "users" do
    field :full_name, :string
    field :email, :string
    field :avatar_url, :string
    field :confirmed_at, :naive_datetime

    embeds_one :profile, MyApp.UserProfile

    timestamps()
  end
end

# user/user_profile.ex
defmodule MyApp.UserProfile do
  use Ecto.Schema

  embedded_schema do
    field :online, :boolean
    field :dark_mode, :boolean
    field :visibility, Ecto.Enum, values: [:public, :private, :friends_only]
  end

  def changeset(%__MODULE__{} = profile, attrs \\ %{}) do
    profile
    |> Ecto.Changeset.cast(attrs, [:online, :dark_mode, :visibility])
    |> Ecto.Changeset.validate_required([:online, :visibility])
  end
end
```

Extracting embedded schemas into dedicated modules improves organization and
allows the embedded schema to have its own changeset functions, validations,
and behavior.

## Belongs To Association

```elixir
defmodule MyApp.Comment do
  use Ecto.Schema

  schema "comments" do
    field :body, :string
    field :author, :string

    belongs_to :post, MyApp.Post

    timestamps()
  end
end

defmodule MyApp.Post do
  use Ecto.Schema

  schema "posts" do
    field :title, :string
    field :body, :string

    has_many :comments, MyApp.Comment

    timestamps()
  end
end
```

The `belongs_to` macro defines a foreign key relationship. By default, it creates
a `post_id` field in the `comments` table. The parent schema typically defines
the inverse relationship with `has_many`.

## Custom Belongs To Field

```elixir
defmodule MyApp.Comment do
  use Ecto.Schema

  schema "comments" do
    field :post_id, :integer
    belongs_to :post, MyApp.Post, define_field: false
  end
end
```

You can customize the foreign key field definition by setting `define_field: false`
and manually defining the field. This is useful when you need special options on
the foreign key field.

## Has One Association

```elixir
defmodule MyApp.Account do
  use Ecto.Schema

  schema "accounts" do
    field :email, :string

    has_one :profile, MyApp.Profile

    timestamps()
  end
end

defmodule MyApp.Profile do
  use Ecto.Schema

  schema "profiles" do
    field :name, :string
    field :age, :integer

    belongs_to :account, MyApp.Account

    timestamps()
  end
end
```

The `has_one` macro defines a one-to-one relationship where the foreign key is
stored in the associated schema. The associated schema must have a corresponding
`belongs_to` relationship.

## Has Many Association

```elixir
defmodule MyApp.User do
  use Ecto.Schema

  schema "users" do
    field :name, :string
    field :email, :string

    has_many :posts, MyApp.Post, foreign_key: :author_id

    timestamps()
  end
end
```

The `has_many` macro defines a one-to-many relationship. You can customize the
foreign key name using the `foreign_key` option if it differs from the default
convention.

## Many to Many Association with Join Table

```elixir
defmodule MyApp.Post do
  use Ecto.Schema

  schema "posts" do
    field :title, :string
    field :body, :string

    many_to_many :tags, MyApp.Tag,
      join_through: "posts_tags",
      on_replace: :delete

    timestamps()
  end
end

defmodule MyApp.Tag do
  use Ecto.Schema

  schema "tags" do
    field :name, :string

    many_to_many :posts, MyApp.Post,
      join_through: "posts_tags"

    timestamps()
  end
end
```

The `many_to_many` macro defines a many-to-many relationship through a join table.
The `join_through` option specifies the table name, and `on_replace: :delete`
controls how the association is updated.

## Many to Many with Join Schema

```elixir
defmodule MyApp.User do
  use Ecto.Schema

  schema "users" do
    field :name, :string

    many_to_many :organizations, MyApp.Organization,
      join_through: MyApp.UserOrganization

    timestamps()
  end
end

defmodule MyApp.Organization do
  use Ecto.Schema

  schema "organizations" do
    field :name, :string

    many_to_many :users, MyApp.User,
      join_through: MyApp.UserOrganization

    timestamps()
  end
end

defmodule MyApp.UserOrganization do
  use Ecto.Schema

  @primary_key false
  schema "users_organizations" do
    belongs_to :user, MyApp.User
    belongs_to :organization, MyApp.Organization
    field :role, :string
    field :joined_at, :utc_datetime

    timestamps()
  end
end
```

Using a dedicated join schema (instead of just a table name) allows you to add
additional fields to the join table, such as role or timestamp information.

## Schema with Composite Primary Key

```elixir
defmodule MyApp.UserOrganization do
  use Ecto.Schema

  @primary_key false
  schema "users_organizations" do
    belongs_to :user, MyApp.User, primary_key: true
    belongs_to :organization, MyApp.Organization, primary_key: true
    field :role, :string

    timestamps()
  end
end
```

Composite primary keys can be created by setting `@primary_key false` and marking
the relevant `belongs_to` associations with `primary_key: true`.

## Custom Primary Key

```elixir
defmodule MyApp.Product do
  use Ecto.Schema

  @primary_key {:sku, :string, autogenerate: false}
  schema "products" do
    field :name, :string
    field :price, :decimal

    timestamps()
  end
end
```

You can customize the primary key field name, type, and autogeneration behavior
using the `@primary_key` module attribute.

## Schema Metadata Access

```elixir
defmodule MyApp.User do
  use Ecto.Schema

  schema "users" do
    field :name, :string
    field :email, :string

    has_many :posts, MyApp.Post
    belongs_to :organization, MyApp.Organization

    timestamps()
  end
end

# Access schema metadata
MyApp.User.__schema__(:source)        # "users"
MyApp.User.__schema__(:fields)        # [:id, :name, :email, :organization_id, :inserted_at, :updated_at]
MyApp.User.__schema__(:primary_key)   # [:id]
MyApp.User.__schema__(:associations)  # [:posts, :organization]
MyApp.User.__schema__(:type, :name)   # :string
```

The `__schema__/1` and `__schema__/2` functions provide access to schema metadata
at runtime, useful for metaprogramming and dynamic query building.

## Self-Referencing Association

```elixir
defmodule MyApp.Person do
  use Ecto.Schema

  schema "people" do
    field :name, :string

    many_to_many :relations, MyApp.Person,
      join_through: MyApp.Relationship,
      join_keys: [person_id: :id, relation_id: :id]

    timestamps()
  end
end

defmodule MyApp.Relationship do
  use Ecto.Schema

  @primary_key false
  schema "relationships" do
    belongs_to :person, MyApp.Person
    belongs_to :relation, MyApp.Person
    field :relationship_type, :string

    timestamps()
  end
end
```

Self-referencing associations allow a schema to reference itself, useful for
hierarchical data or relationships between entities of the same type.

## Polymorphic Association Pattern

```elixir
defmodule MyApp.TodoItem do
  use Ecto.Schema

  schema "todo_items" do
    field :description, :string

    timestamps()
  end
end

defmodule MyApp.Comment do
  use Ecto.Schema

  schema "comments" do
    field :body, :string
    field :commentable_id, :integer
    field :commentable_type, :string

    timestamps()
  end
end

# Create a comment for a TodoItem
comment = %MyApp.Comment{
  body: "This needs to be done ASAP",
  commentable_id: todo_item.id,
  commentable_type: "todo_item"
}
```

Polymorphic associations can be implemented using a combination of ID and type
fields. While Ecto doesn't have built-in polymorphic associations like some ORMs,
this pattern provides similar functionality.

## Schema with Virtual Fields

```elixir
defmodule MyApp.User do
  use Ecto.Schema

  schema "users" do
    field :first_name, :string
    field :last_name, :string
    field :email, :string

    # Virtual fields
    field :full_name, :string, virtual: true
    field :password, :string, virtual: true
    field :password_hash, :string

    timestamps()
  end

  def build_full_name(%__MODULE__{} = user) do
    %{user | full_name: "#{user.first_name} #{user.last_name}"}
  end
end
```

Virtual fields are not persisted to the database but can be useful for temporary
data like unhashed passwords or computed values like full names.

## Schema with Custom Source

```elixir
defmodule MyApp.LegacyUser do
  use Ecto.Schema

  @schema_prefix "legacy"
  schema "tbl_users" do
    field :user_name, :string, source: :username
    field :user_email, :string, source: :email
    field :create_date, :utc_datetime, source: :created_at

    timestamps()
  end
end
```

You can map schema fields to different column names using the `:source` option,
useful when working with legacy databases or following different naming conventions.

## Schema Prefix for Multi-Tenant Applications

```elixir
defmodule MyApp.Organization do
  use Ecto.Schema

  @schema_prefix "public"
  schema "organizations" do
    field :name, :string
    field :slug, :string

    timestamps()
  end
end

defmodule MyApp.Tenant.User do
  use Ecto.Schema

  schema "users" do
    field :name, :string
    field :email, :string

    timestamps()
  end
end

# Query with dynamic prefix
MyApp.Repo.all(MyApp.Tenant.User, prefix: "tenant_#{tenant_id}")
```

The `@schema_prefix` attribute and the `prefix` option enable multi-tenant
applications where each tenant has its own database schema or prefix.

## When to Use This Skill

Use ecto-schema-patterns when you need to:

- Define database-backed schemas for your application's domain models
- Create embedded schemas for nested or complex data structures
- Set up associations between different schemas (belongs_to, has_many, many_to_many)
- Model hierarchical or self-referential data
- Work with legacy databases using custom field mappings
- Implement multi-tenant applications with schema prefixes
- Define virtual fields for computed or temporary data
- Use custom primary keys or composite keys
- Store unstructured data using map or array fields
- Create polymorphic association patterns

## Best Practices

- Use descriptive schema and field names that reflect your domain
- Always define `timestamps()` for audit trails unless there's a specific reason not to
- Prefer embedded schemas over JSON columns when the structure is known
- Use Ecto.Enum for fields with a fixed set of values
- Keep schemas focused on data structure, put business logic elsewhere
- Use virtual fields for data that shouldn't be persisted
- Define proper associations to leverage Ecto's preloading capabilities
- Use `on_replace: :delete` for many_to_many associations that should cascade
- Extract complex embedded schemas into separate modules for reusability
- Use `belongs_to` with `define_field: false` when you need custom foreign key options
- Leverage schema metadata functions for metaprogramming sparingly
- Use `:source` option to bridge schema and database naming differences
- Set appropriate `@primary_key` for non-standard primary keys
- Use join schemas instead of join tables when you need extra attributes
- Document schema relationships and constraints in module documentation

## Common Pitfalls

- Forgetting to add `timestamps()` and losing audit information
- Not setting `on_replace` option for associations, causing unexpected behavior
- Confusing `embeds_one`/`embeds_many` with `has_one`/`has_many`
- Using `:map` type when an embedded schema would provide better structure
- Defining associations without corresponding database constraints
- Not marking virtual fields with `virtual: true`, causing database errors
- Mixing business logic with schema definitions
- Creating circular dependencies between schema modules
- Forgetting to set `@primary_key false` for join schemas
- Not using proper foreign key options in `belongs_to`
- Accessing associations without preloading them first
- Over-nesting embedded schemas, making them hard to maintain
- Not considering the difference between `has_one` and `belongs_to`
- Using polymorphic patterns without proper indexing
- Forgetting that embedded data is stored as JSON/map in a single column
- Not handling nil values properly in custom source mappings
- Creating too many associations, leading to N+1 query problems
- Not using join schemas when additional join table attributes are needed
- Hardcoding schema prefixes instead of making them configurable
- Not validating embedded schemas separately from parent schemas

## Resources

### Official Ecto Documentation

- [Ecto.Schema Module](https://hexdocs.pm/ecto/Ecto.Schema.html)
- [Schema Definition](https://hexdocs.pm/ecto/Ecto.Schema.html#module-schema-definition)
- [Field Types](https://hexdocs.pm/ecto/Ecto.Schema.html#module-types-and-casting)
- [Associations](https://hexdocs.pm/ecto/associations.html)
- [Embedded Schemas](https://hexdocs.pm/ecto/embedded-schemas.html)
- [Polymorphic Associations](https://hexdocs.pm/ecto/polymorphic-associations-with-many-to-many.html)
- [Self-Referencing Many to Many](https://hexdocs.pm/ecto/self-referencing-many-to-many.html)

### Guides and Patterns

- [Getting Started with Ecto](https://hexdocs.pm/ecto/getting-started.html)
- [Schema Metadata](https://hexdocs.pm/ecto/Ecto.Schema.html#module-reflection)
- [Multi-Tenancy Guide](https://hexdocs.pm/ecto/multi-tenancy-with-query-prefixes.html)
- [Ecto Best Practices](https://hexdocs.pm/ecto/Ecto.html)

### Community Resources

- [Elixir School - Ecto](https://elixirschool.com/en/lessons/ecto/basics)
- [Elixir Forum - Ecto Category](https://elixirforum.com/c/elixir-questions/ecto/15)
- [Programming Ecto Book](https://pragprog.com/titles/wmecto/programming-ecto/)
