---
name: ecto-changesets
description: Use when validating and casting data with Ecto changesets including field validation, constraints, nested changesets, and data transformation. Use for ensuring data integrity before database operations.
allowed-tools:
  - Bash
  - Read
---

# Ecto Changesets

Master Ecto changesets to validate, cast, and transform data before database operations.
This skill covers changeset creation, validation, constraints, handling associations,
and advanced patterns for maintaining data integrity.

## Basic Changeset

```elixir
defmodule MyApp.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :name, :string
    field :email, :string
    field :age, :integer

    timestamps()
  end

  def changeset(user, params \\ %{}) do
    user
    |> cast(params, [:name, :email, :age])
    |> validate_required([:name, :email])
  end
end

# Usage
changeset = MyApp.User.changeset(%MyApp.User{}, %{name: "John", email: "john@example.com"})
```

Changesets filter and validate parameters before they're applied to a struct.
The `cast/3` function specifies which fields can be changed, and `validate_required/2`
ensures specific fields are present.

## Creating and Validating Changesets

```elixir
defmodule MyApp.Person do
  use Ecto.Schema
  import Ecto.Changeset

  schema "people" do
    field :first_name, :string
    field :last_name, :string
    field :age, :integer

    timestamps()
  end

  def changeset(person, params \\ %{}) do
    person
    |> cast(params, [:first_name, :last_name, :age])
    |> validate_required([:first_name, :last_name])
    |> validate_number(:age, greater_than_or_equal_to: 0)
  end
end

# Create changeset
changeset = MyApp.Person.changeset(%MyApp.Person{}, %{first_name: "Jane"})

# Check validity
changeset.valid?  # false, last_name is missing

# Access errors
changeset.errors
# [first_name: {"can't be blank", [validation: :required]},
#  last_name: {"can't be blank", [validation: :required]}]
```

The `valid?` field indicates whether the changeset has any errors. The `errors`
field contains a keyword list of validation failures with error messages and metadata.

## Inserting with Changesets

```elixir
person = %MyApp.Person{}
changeset = MyApp.Person.changeset(person, %{
  first_name: "John",
  last_name: "Doe",
  age: 30
})

case MyApp.Repo.insert(changeset) do
  {:ok, person} ->
    # Successfully inserted
    IO.puts("Created person with ID: #{person.id}")

  {:error, changeset} ->
    # Validation or constraint errors
    IO.inspect(changeset.errors)
end
```

The `Repo.insert/1` function accepts a changeset and returns `{:ok, struct}` on
success or `{:error, changeset}` on failure. Pattern matching makes error handling
straightforward.

## Updating with Changesets

```elixir
person = MyApp.Repo.get!(MyApp.Person, 1)
changeset = MyApp.Person.changeset(person, %{age: 31})

case MyApp.Repo.update(changeset) do
  {:ok, updated_person} ->
    # Successfully updated
    IO.puts("Updated person age to: #{updated_person.age}")

  {:error, changeset} ->
    # Validation or constraint errors
    IO.inspect(changeset.errors)
end
```

Updates work similarly to inserts, but start with an existing struct from the
database. The changeset tracks which fields have changed.

## Type Casting

```elixir
changeset = Ecto.Changeset.cast(%MyApp.User{}, %{"age" => "25"}, [:age])
user = MyApp.Repo.insert!(changeset)
user.age  # 25 (integer, not string)
```

The `cast/3` function automatically converts parameter values to their schema-defined
types. Strings like "25" are converted to integers when the field type is `:integer`.

## Field Validations

```elixir
defmodule MyApp.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :email, :string
    field :username, :string
    field :age, :integer
    field :bio, :string
    field :website, :string

    timestamps()
  end

  def changeset(user, params \\ %{}) do
    user
    |> cast(params, [:email, :username, :age, :bio, :website])
    |> validate_required([:email, :username])
    |> validate_format(:email, ~r/@/)
    |> validate_length(:username, min: 3, max: 20)
    |> validate_length(:bio, max: 500)
    |> validate_number(:age, greater_than: 0, less_than: 150)
    |> validate_inclusion(:age, 18..100)
    |> validate_format(:website, ~r/^https?:\/\//)
  end
end
```

Ecto provides many built-in validators including `validate_format/3` for regex
patterns, `validate_length/3` for string lengths, `validate_number/3` for numeric
constraints, and `validate_inclusion/3` for allowed values.

## Custom Validation Functions

```elixir
defmodule MyApp.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :email, :string
    field :password, :string, virtual: true
    field :password_hash, :string

    timestamps()
  end

  def changeset(user, params \\ %{}) do
    user
    |> cast(params, [:email, :password])
    |> validate_required([:email, :password])
    |> validate_email_format()
    |> validate_password_strength()
    |> hash_password()
  end

  defp validate_email_format(changeset) do
    changeset
    |> validate_format(:email, ~r/@/, message: "must be a valid email")
    |> validate_length(:email, max: 255)
  end

  defp validate_password_strength(changeset) do
    validate_change(changeset, :password, fn :password, password ->
      cond do
        String.length(password) < 8 ->
          [password: "must be at least 8 characters"]

        not String.match?(password, ~r/[A-Z]/) ->
          [password: "must contain at least one uppercase letter"]

        not String.match?(password, ~r/[0-9]/) ->
          [password: "must contain at least one number"]

        true ->
          []
      end
    end)
  end

  defp hash_password(changeset) do
    case changeset do
      %Ecto.Changeset{valid?: true, changes: %{password: password}} ->
        put_change(changeset, :password_hash, hash_password_value(password))

      _ ->
        changeset
    end
  end

  defp hash_password_value(password) do
    # Use a real hashing library like Argon2 or Bcrypt
    :crypto.hash(:sha256, password) |> Base.encode64()
  end
end
```

Custom validation functions use `validate_change/3` to add custom logic. The
`put_change/3` function modifies changeset values, useful for transformations
like password hashing.

## Constraint Validations

```elixir
defmodule MyApp.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :email, :string
    field :username, :string

    timestamps()
  end

  def changeset(user, params \\ %{}) do
    user
    |> cast(params, [:email, :username])
    |> validate_required([:email, :username])
    |> unique_constraint(:email)
    |> unique_constraint(:username)
  end
end

# Usage
case MyApp.Repo.insert(changeset) do
  {:ok, user} ->
    # Success

  {:error, changeset} ->
    # Will contain unique constraint error if email/username exists
    changeset.errors
end
```

Constraint validations check database-level constraints like unique indexes.
They only run when the changeset is inserted or updated, not during validation.

## Unique Constraint with Custom Error Message

```elixir
def changeset(user, params \\ %{}) do
  user
  |> cast(params, [:email])
  |> validate_required([:email])
  |> unique_constraint(:email,
       name: :users_email_index,
       message: "has already been taken")
end
```

The `unique_constraint/3` function accepts options to specify the constraint name
and customize the error message. This maps database constraint violations to
user-friendly errors.

## Foreign Key Constraints

```elixir
defmodule MyApp.Comment do
  use Ecto.Schema
  import Ecto.Changeset

  schema "comments" do
    field :body, :string
    belongs_to :post, MyApp.Post

    timestamps()
  end

  def changeset(comment, params \\ %{}) do
    comment
    |> cast(params, [:body, :post_id])
    |> validate_required([:body, :post_id])
    |> foreign_key_constraint(:post_id)
  end
end
```

The `foreign_key_constraint/3` function validates that foreign key relationships
are valid. If you try to create a comment with a non-existent post_id, the
constraint will catch it.

## Check Constraints

```elixir
def changeset(product, params \\ %{}) do
  product
  |> cast(params, [:price, :discount_price])
  |> validate_required([:price])
  |> check_constraint(:discount_price,
       name: :discount_price_must_be_less_than_price,
       message: "must be less than the regular price")
end
```

Check constraints validate arbitrary database-level rules. The constraint must
be defined in your migration with the same name.

## Changeset Composition

```elixir
defmodule MyApp.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :email, :string
    field :password, :string, virtual: true
    field :password_hash, :string
    field :role, :string

    timestamps()
  end

  def registration_changeset(user, params \\ %{}) do
    user
    |> cast(params, [:email, :password])
    |> validate_required([:email, :password])
    |> validate_email()
    |> validate_password()
    |> hash_password()
    |> put_change(:role, "user")
  end

  def admin_changeset(user, params \\ %{}) do
    user
    |> cast(params, [:email, :password, :role])
    |> validate_required([:email, :role])
    |> validate_email()
    |> validate_inclusion(:role, ["user", "admin", "moderator"])
    |> maybe_hash_password()
  end

  defp validate_email(changeset) do
    changeset
    |> validate_format(:email, ~r/@/)
    |> unique_constraint(:email)
  end

  defp validate_password(changeset) do
    validate_length(changeset, :password, min: 8)
  end

  defp hash_password(changeset) do
    case get_change(changeset, :password) do
      nil -> changeset
      password -> put_change(changeset, :password_hash, hash(password))
    end
  end

  defp maybe_hash_password(changeset) do
    case get_change(changeset, :password) do
      nil -> changeset
      password -> hash_password(changeset)
    end
  end

  defp hash(password), do: :crypto.hash(:sha256, password)
end
```

Different changesets can be used for different contexts (registration vs. admin
updates). This keeps validation logic focused and prevents unintended changes.

## Embedded Changeset Validation

```elixir
defmodule MyApp.UserProfile do
  use Ecto.Schema
  import Ecto.Changeset

  embedded_schema do
    field :online, :boolean
    field :dark_mode, :boolean
    field :visibility, Ecto.Enum, values: [:public, :private, :friends_only]
  end

  def changeset(profile, attrs \\ %{}) do
    profile
    |> cast(attrs, [:online, :dark_mode, :visibility])
    |> validate_required([:online, :visibility])
  end
end

defmodule MyApp.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :full_name, :string
    field :email, :string

    embeds_one :profile, MyApp.UserProfile

    timestamps()
  end

  def changeset(user, attrs \\ %{}) do
    user
    |> cast(attrs, [:full_name, :email])
    |> cast_embed(:profile, required: true)
  end
end

# Usage
changeset = MyApp.User.changeset(%MyApp.User{}, %{
  full_name: "John Doe",
  email: "john@example.com",
  profile: %{online: true, visibility: :public}
})

changeset.valid?  # true
```

The `cast_embed/3` function validates embedded schemas using their own changeset
functions. Validation errors in embedded data propagate to the parent changeset.

## Custom Embedded Changeset Function

```elixir
defmodule MyApp.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :full_name, :string
    field :email, :string

    embeds_one :profile, Profile do
      field :online, :boolean
      field :dark_mode, :boolean
      field :visibility, Ecto.Enum, values: [:public, :private, :friends_only]
    end

    timestamps()
  end

  def changeset(user, attrs \\ %{}) do
    user
    |> cast(attrs, [:full_name, :email])
    |> cast_embed(:profile, required: true, with: &profile_changeset/2)
  end

  def profile_changeset(profile, attrs \\ %{}) do
    profile
    |> cast(attrs, [:online, :dark_mode, :visibility])
    |> validate_required([:online, :visibility])
  end
end
```

The `:with` option in `cast_embed/3` specifies a custom changeset function for
the embedded data, allowing specific validation logic.

## Embedded Many Validation

```elixir
defmodule MyApp.Order do
  use Ecto.Schema
  import Ecto.Changeset

  schema "orders" do
    field :customer_name, :string

    embeds_many :items, OrderItem do
      field :product_name, :string
      field :quantity, :integer
      field :price, :decimal
    end

    timestamps()
  end

  def changeset(order, attrs \\ %{}) do
    order
    |> cast(attrs, [:customer_name])
    |> cast_embed(:items, with: &item_changeset/2)
    |> validate_required([:customer_name])
    |> validate_length(:items, min: 1, message: "must have at least one item")
  end

  defp item_changeset(item, attrs) do
    item
    |> cast(attrs, [:product_name, :quantity, :price])
    |> validate_required([:product_name, :quantity, :price])
    |> validate_number(:quantity, greater_than: 0)
    |> validate_number(:price, greater_than: 0)
  end
end
```

Collections of embedded schemas are validated using `cast_embed/3` with `embeds_many`.
Each item in the collection is validated independently using its changeset function.

## Association Changesets with put_assoc

```elixir
defmodule MyApp.Post do
  use Ecto.Schema
  import Ecto.Changeset

  schema "posts" do
    field :title, :string
    field :body, :string

    many_to_many :tags, MyApp.Tag,
      join_through: "posts_tags",
      on_replace: :delete

    timestamps()
  end

  def changeset(post, params \\ %{}) do
    post
    |> cast(params, [:title, :body])
    |> validate_required([:title, :body])
    |> put_assoc(:tags, parse_tags(params))
  end

  defp parse_tags(params) do
    (params["tags"] || "")
    |> String.split(",")
    |> Enum.map(&String.trim/1)
    |> Enum.reject(&(&1 == ""))
    |> Enum.map(&get_or_insert_tag/1)
  end

  defp get_or_insert_tag(name) do
    MyApp.Repo.get_by(MyApp.Tag, name: name) ||
      MyApp.Repo.insert!(%MyApp.Tag{name: name})
  end
end
```

The `put_assoc/3` function sets association data on a changeset. When combined
with `on_replace: :delete`, it properly handles adding and removing associations.

## Upsert Pattern with Unique Constraints

```elixir
defmodule MyApp.Tag do
  use Ecto.Schema
  import Ecto.Changeset

  schema "tags" do
    field :name, :string

    timestamps()
  end

  def changeset(tag, params \\ %{}) do
    tag
    |> cast(params, [:name])
    |> validate_required([:name])
    |> unique_constraint(:name)
  end
end

defp get_or_insert_tag(name) do
  %MyApp.Tag{}
  |> MyApp.Tag.changeset(%{name: name})
  |> MyApp.Repo.insert()
  |> case do
    {:ok, tag} -> tag
    {:error, _} -> MyApp.Repo.get_by!(MyApp.Tag, name: name)
  end
end
```

This pattern handles race conditions when inserting records with unique constraints.
If the insert fails due to a duplicate, it fetches the existing record.

## Batch Upsert with insert_all

```elixir
defmodule MyApp.Post do
  use Ecto.Schema
  import Ecto.Changeset
  import Ecto.Query

  schema "posts" do
    field :title, :string
    field :body, :string

    many_to_many :tags, MyApp.Tag,
      join_through: "posts_tags",
      on_replace: :delete

    timestamps()
  end

  def changeset(struct, params \\ %{}) do
    struct
    |> cast(params, [:title, :body])
    |> put_assoc(:tags, parse_tags(params))
  end

  defp parse_tags(params) do
    (params["tags"] || "")
    |> String.split(",")
    |> Enum.map(&String.trim/1)
    |> Enum.reject(&(&1 == ""))
    |> insert_and_get_all()
  end

  defp insert_and_get_all([]), do: []

  defp insert_and_get_all(names) do
    timestamp = NaiveDateTime.utc_now() |> NaiveDateTime.truncate(:second)
    placeholders = %{timestamp: timestamp}

    maps = Enum.map(names, fn name ->
      %{
        name: name,
        inserted_at: {:placeholder, :timestamp},
        updated_at: {:placeholder, :timestamp}
      }
    end)

    MyApp.Repo.insert_all(
      MyApp.Tag,
      maps,
      placeholders: placeholders,
      on_conflict: :nothing
    )

    MyApp.Repo.all(from t in MyApp.Tag, where: t.name in ^names)
  end
end
```

The `insert_all/3` function with `on_conflict: :nothing` performs bulk upserts
efficiently, minimizing database round trips when handling multiple associations.

## Traversing Changeset Errors

```elixir
defmodule MyApp.ErrorHelpers do
  def error_messages(changeset) do
    Ecto.Changeset.traverse_errors(changeset, fn {msg, opts} ->
      Enum.reduce(opts, msg, fn {key, value}, acc ->
        String.replace(acc, "%{#{key}}", to_string(value))
      end)
    end)
  end
end

# Usage
changeset = MyApp.User.changeset(%MyApp.User{}, %{})
errors = MyApp.ErrorHelpers.error_messages(changeset)
# %{
#   email: ["can't be blank"],
#   username: ["can't be blank"]
# }
```

The `traverse_errors/2` function walks through all errors in a changeset,
including nested changesets, allowing you to format error messages for display.

## Conditional Validations

```elixir
defmodule MyApp.Product do
  use Ecto.Schema
  import Ecto.Changeset

  schema "products" do
    field :name, :string
    field :price, :decimal
    field :discount_price, :decimal
    field :is_on_sale, :boolean

    timestamps()
  end

  def changeset(product, params \\ %{}) do
    product
    |> cast(params, [:name, :price, :discount_price, :is_on_sale])
    |> validate_required([:name, :price])
    |> validate_discount_price()
  end

  defp validate_discount_price(changeset) do
    case get_field(changeset, :is_on_sale) do
      true ->
        changeset
        |> validate_required([:discount_price])
        |> validate_number(:discount_price, less_than: get_field(changeset, :price))

      _ ->
        changeset
    end
  end
end
```

Conditional validations apply different rules based on changeset data. Use
`get_field/2` to access current field values including changes and existing data.

## Optimistic Locking with Version Fields

```elixir
defmodule MyApp.Document do
  use Ecto.Schema
  import Ecto.Changeset

  schema "documents" do
    field :title, :string
    field :content, :string
    field :version, :integer, default: 1

    timestamps()
  end

  def changeset(document, params \\ %{}) do
    document
    |> cast(params, [:title, :content])
    |> validate_required([:title, :content])
    |> optimistic_lock(:version)
  end
end

# Update with version check
document = MyApp.Repo.get!(MyApp.Document, 1)
changeset = MyApp.Document.changeset(document, %{title: "Updated Title"})

case MyApp.Repo.update(changeset) do
  {:ok, updated_document} ->
    # Success, version incremented

  {:error, changeset} ->
    # Stale object error if version doesn't match
    IO.puts("Document was modified by another process")
end
```

The `optimistic_lock/3` function adds version checking to prevent lost updates
in concurrent scenarios. The update fails if the version has changed since reading.

## Changeset Pipelines for Complex Workflows

```elixir
defmodule MyApp.UserRegistration do
  import Ecto.Changeset

  def changeset(params) do
    %MyApp.User{}
    |> MyApp.User.changeset(params)
    |> validate_terms_accepted()
    |> validate_email_verification()
    |> set_initial_role()
    |> send_welcome_email()
  end

  defp validate_terms_accepted(changeset) do
    if get_change(changeset, :terms_accepted) == true do
      changeset
    else
      add_error(changeset, :terms_accepted, "must be accepted")
    end
  end

  defp validate_email_verification(changeset) do
    # Custom email verification logic
    changeset
  end

  defp set_initial_role(changeset) do
    put_change(changeset, :role, "user")
  end

  defp send_welcome_email(changeset) do
    if changeset.valid? do
      # Send email in a separate process
      email = get_change(changeset, :email)
      Task.start(fn -> MyApp.Mailer.send_welcome(email) end)
    end

    changeset
  end
end
```

Complex workflows can be built as changeset pipelines. Each step validates or
transforms data, and the pipeline short-circuits if validation fails.

## When to Use This Skill

Use ecto-changesets when you need to:

- Validate user input before database operations
- Cast external data to appropriate types
- Enforce database constraints at the application level
- Transform data before persistence (e.g., hashing passwords)
- Handle nested or embedded data validation
- Manage associations when creating or updating records
- Provide user-friendly error messages for validation failures
- Implement different validation rules for different contexts
- Prevent race conditions with unique constraints
- Track changes to records for audit purposes
- Implement optimistic locking for concurrent updates
- Build complex multi-step data validation workflows

## Best Practices

- Always use changesets for external data, never directly create structs
- Define multiple changeset functions for different contexts (create, update, admin)
- Keep changesets focused on validation and casting, not business logic
- Use `validate_required/2` before other validations to provide clear errors
- Leverage database constraints and map them with constraint functions
- Use virtual fields for data that shouldn't be persisted
- Compose changesets using private helper functions
- Return changesets from failed operations for better error handling
- Use `traverse_errors/2` to format errors for API responses
- Document why specific validations exist, especially complex custom ones
- Test changesets independently from database operations
- Use `get_change/2` for conditional logic on modified fields
- Use `get_field/2` when you need current value (changed or existing)
- Keep embedded changeset functions close to the parent schema
- Use `on_replace` option appropriately for association changesets

## Common Pitfalls

- Forgetting to include fields in the `cast/3` allowed list
- Not checking `changeset.valid?` before calling Repo functions
- Mixing validation logic with business logic in changeset functions
- Using `put_change/3` instead of validations for constraints
- Forgetting to add constraint validations for database constraints
- Not handling race conditions with unique constraints properly
- Overusing custom validations when built-in validators suffice
- Mutating changesets instead of returning new ones
- Not using virtual fields for temporary data like passwords
- Calling Repo functions inside changeset functions
- Using `change/2` when you need validation with `cast/3`
- Forgetting `on_replace: :delete` for many_to_many associations
- Not validating embedded schemas separately
- Hardcoding error messages instead of using metadata
- Not testing edge cases in custom validations
- Using `get_change/2` when you need `get_field/2` (or vice versa)
- Not setting appropriate constraint names in migrations
- Ignoring changeset errors in insert/update pipelines
- Performing side effects in validation functions
- Not documenting expected params shape for changesets

## Resources

### Official Ecto Documentation

- [Ecto.Changeset Module](https://hexdocs.pm/ecto/Ecto.Changeset.html)
- [Changeset API Reference](https://hexdocs.pm/ecto/Ecto.Changeset.html#summary)
- [Data Validation Guide](https://hexdocs.pm/ecto/data-mapping-and-validation.html)
- [Constraints and Upserts](https://hexdocs.pm/ecto/constraints-and-upserts.html)

### Validation Functions

- [validate_required/3](https://hexdocs.pm/ecto/Ecto.Changeset.html#validate_required/3)
- [validate_format/4](https://hexdocs.pm/ecto/Ecto.Changeset.html#validate_format/4)
- [validate_length/3](https://hexdocs.pm/ecto/Ecto.Changeset.html#validate_length/3)
- [validate_number/3](https://hexdocs.pm/ecto/Ecto.Changeset.html#validate_number/3)
- [validate_inclusion/4](https://hexdocs.pm/ecto/Ecto.Changeset.html#validate_inclusion/4)
- [validate_change/3](https://hexdocs.pm/ecto/Ecto.Changeset.html#validate_change/3)

### Constraint Functions

- [unique_constraint/3](https://hexdocs.pm/ecto/Ecto.Changeset.html#unique_constraint/3)
- [foreign_key_constraint/3](https://hexdocs.pm/ecto/Ecto.Changeset.html#foreign_key_constraint/3)
- [check_constraint/3](https://hexdocs.pm/ecto/Ecto.Changeset.html#check_constraint/3)
- [optimistic_lock/3](https://hexdocs.pm/ecto/Ecto.Changeset.html#optimistic_lock/3)

### Association and Embedded Functions

- [cast_assoc/3](https://hexdocs.pm/ecto/Ecto.Changeset.html#cast_assoc/3)
- [cast_embed/3](https://hexdocs.pm/ecto/Ecto.Changeset.html#cast_embed/3)
- [put_assoc/4](https://hexdocs.pm/ecto/Ecto.Changeset.html#put_assoc/4)

### Community Resources

- [Elixir School - Changesets](https://elixirschool.com/en/lessons/ecto/changesets)
- [Programming Ecto Book](https://pragprog.com/titles/wmecto/programming-ecto/)
- [Ecto Changeset Best Practices](https://hexdocs.pm/ecto/Ecto.Changeset.html#module-changeset-actions)
- [Error Handling in Ecto](https://hexdocs.pm/ecto/Ecto.Changeset.html#module-error-messages)
