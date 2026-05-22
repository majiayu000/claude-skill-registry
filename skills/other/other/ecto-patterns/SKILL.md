---
name: ecto-patterns
description: "Ecto patterns — schemas, changesets, queries, migrations, Multi, associations, preloads, upserts. Use when editing Repo calls, Ecto.Query, or schema fields. Skip for Ash."
effort: medium
user-invocable: false
paths:
  - "**/migrations/*.exs"
  - "**/*_schema.ex"
  - "**/*changeset*.ex"
---

# Ecto Patterns Reference

Reference for working with Ecto schemas, queries, and migrations.

## Iron Laws — Never Violate These

1. **CHANGESETS ARE FOR EXTERNAL DATA** — Use `cast/4` for user/API input, `change/2` or `put_change/3` for internal trusted data
2. **NEVER USE `:float` FOR MONEY** — Always use `:decimal` or `:integer` (cents)
3. **NO RAILS-STYLE POLYMORPHIC ASSOCIATIONS** — They break foreign key constraints; use multiple nullable FKs or separate join tables
4. **ALWAYS PIN VALUES IN QUERIES** — `u.name == ^user_input` is safe, string interpolation causes SQL injection
5. **PRELOAD COLLECTIONS, NOT INDIVIDUALS** — Preloading in loops = N+1 queries
6. **CONSTRAINTS BEAT VALIDATIONS FOR RACE CONDITIONS** — Validations provide quick feedback, constraints provide DB-level safety
7. **SEPARATE QUERIES FOR `has_many`, JOIN FOR `belongs_to`** — Avoids row multiplication
8. **NO IMPLICIT CROSS JOINS** — `from(a in A, b in B)` without `on:` creates Cartesian product
9. **DEDUP BEFORE `cast_assoc` WITH SHARED DATA** — When multiple parents share child data, deduplicate child records BEFORE building changesets. Dedup only works within a single changeset

## Quick Schema Template

```elixir
defmodule MyApp.Context.Entity do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :binary_id, autogenerate: true}
  @foreign_key_type :binary_id

  schema "entities" do
    field :name, :string
    field :status, Ecto.Enum, values: [:draft, :active, :archived]
    field :amount_cents, :integer  # Never :float for money!
    belongs_to :user, MyApp.Accounts.User
    timestamps(type: :utc_datetime_usec)
  end

  def changeset(entity, attrs) do
    entity
    |> cast(attrs, [:name, :status, :amount_cents])
    |> validate_required([:name])
    |> foreign_key_constraint(:user_id)
  end
end
```

## Quick Decisions

### cast vs put_change vs change

| Function | Use When |
|----------|----------|
| `cast/4` | External data (user input, API) |
| `put_change/3` | Internal trusted data (timestamps, computed) |
| `change/2` | Internal data from existing struct |

### Preload Strategy

| Relationship | Strategy |
|--------------|----------|
| `belongs_to` | JOIN (single query) |
| `has_many` | Separate queries (avoid row multiplication) |

## Common Anti-patterns

| Wrong | Right |
|-------|-------|
| `field :amount, :float` | `field :amount_cents, :integer` |
| `"SELECT * WHERE name = '#{name}'"` | `from(u in User, where: u.name == ^name)` |
| `Repo.all(User) \|> Enum.filter(& &1.active)` | `from(u in User, where: u.active)` |
| Preloading in loops | `Repo.preload(posts, :comments)` |
| `Repo.get!(User, user_id)` with user input | `Repo.get(User, id)` + handle nil |

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/changesets.md` - cast vs put_change, custom validations, prepare_changes
- `${CLAUDE_SKILL_DIR}/references/queries.md` - Composable queries, dynamic, subqueries, preloading
- `${CLAUDE_SKILL_DIR}/references/migrations.md` - Safe migrations, concurrent indexes, NOT NULL
- `${CLAUDE_SKILL_DIR}/references/transactions.md` - Repo.transact, Ecto.Multi, upserts
