---
name: ecto-query-patterns
description: Use when querying data with Ecto.Query DSL including where clauses, joins, aggregates, preloading, and query composition. Use for building flexible database queries in Elixir applications.
allowed-tools:
  - Bash
  - Read
---

# Ecto Query Patterns

Master Ecto's powerful Query DSL to build efficient, composable database queries.
This skill covers the query syntax, filtering, joining, aggregation, preloading
associations, and advanced query composition patterns.

## Basic Query with from Macro

```elixir
import Ecto.Query, only: [from: 2]

# Basic query using keyword syntax
query = from u in "users",
          where: u.age > 18,
          select: u.name

# Execute the query
MyApp.Repo.all(query)
```

Queries are built using the `from/2` macro and only sent to the database when
passed to a `Repo` function like `all/1`, `one/1`, or `get/2`. The keyword syntax
provides a readable way to construct queries.

## Query with Schema Module

```elixir
query = from u in MyApp.User,
          where: u.age > 18,
          select: u.name

MyApp.Repo.all(query)
```

Using a schema module instead of a table name string provides better type safety
and allows Ecto to use the schema's field definitions for validation and casting.

## Bindingless Query Construction

```elixir
from MyApp.Post,
  where: [category: "fresh and new"],
  order_by: [desc: :published_at],
  select: [:id, :title, :body]
```

Bindingless syntax allows building queries without explicit variable bindings.
This works well for simple queries and when using keyword list syntax for conditions.

## Query with Explicit Bindings

```elixir
query = from p in MyApp.Post,
          where: p.category == "fresh and new",
          order_by: [desc: p.published_at],
          select: struct(p, [:id, :title, :body])

MyApp.Repo.all(query)
```

Explicit bindings (like `p` for posts) allow for more complex conditions and
selections. The `struct/2` function selects only specific fields from the schema.

## Dynamic Query Variables

```elixir
category = "fresh and new"
order_by = [desc: :published_at]
select_fields = [:id, :title, :body]

query = from MyApp.Post,
          where: [category: ^category],
          order_by: ^order_by,
          select: ^select_fields

MyApp.Repo.all(query)
```

The pin operator `^` allows interpolating Elixir values into queries. This is
essential for parameterized queries and prevents SQL injection.

## Where Clause with Expressions

```elixir
query = from u in MyApp.User,
          where: u.age > 0,
          select: u.name

# Multiple where clauses are combined with AND
query = from u in MyApp.User,
          where: u.age > 18,
          where: u.confirmed == true,
          select: u

MyApp.Repo.all(query)
```

Query expressions support field access, comparison operators, and literals.
Multiple `where` clauses are automatically combined with AND logic.

## Composable Queries

```elixir
# Create a base query
query = from u in MyApp.User, where: u.age > 18

# Extend the query
query = from u in query, select: u.name

MyApp.Repo.all(query)
```

Queries are composable - you can build on existing queries by using them in the
`in` clause. This enables powerful query abstraction and reusability.

## Query Composition Function Pattern

```elixir
def most_recent_from(query, minimum_date) do
  from p in query,
    where: p.published_at > ^minimum_date,
    order_by: [desc: p.published_at]
end

# Usage
MyApp.Post
|> most_recent_from(~N[2024-01-01 00:00:00])
|> MyApp.Repo.all()
```

Extracting query logic into functions creates reusable, testable query components.
This pattern is fundamental to building maintainable query code.

## Or Where Conditions

```elixir
from p in MyApp.Post,
  where: p.category == "elixir" or p.category == "phoenix",
  select: p
```

Use the `or` keyword for alternative conditions. For more complex OR logic,
consider using `Ecto.Query.dynamic/2`.

## IN Query with List

```elixir
categories = ["elixir", "phoenix", "ecto"]

query = from p in MyApp.Post,
          where: p.category in ^categories,
          select: p

MyApp.Repo.all(query)
```

The `in` operator checks if a field value exists in a list of values. Use the
pin operator to interpolate the list variable.

## Like and ILike for Pattern Matching

```elixir
search_term = "%elixir%"

query = from p in MyApp.Post,
          where: like(p.title, ^search_term),
          select: p

# Case-insensitive version
query = from p in MyApp.Post,
          where: ilike(p.title, ^search_term),
          select: p
```

Use `like/2` for case-sensitive pattern matching and `ilike/2` for case-insensitive
matching. Wildcards `%` match any characters.

## Selecting Specific Fields

```elixir
# Select multiple fields
query = from p in MyApp.Post,
          select: {p.id, p.title}

MyApp.Repo.all(query)  # Returns [{1, "Title 1"}, {2, "Title 2"}]

# Select as map
query = from p in MyApp.Post,
          select: %{id: p.id, title: p.title}

MyApp.Repo.all(query)  # Returns [%{id: 1, title: "Title 1"}, ...]

# Select struct with specific fields
query = from p in MyApp.Post,
          select: struct(p, [:id, :title, :body])

MyApp.Repo.all(query)  # Returns Post structs with only selected fields loaded
```

Selecting specific fields instead of entire records improves query performance
by reducing data transfer and memory usage.

## Aggregation Functions

```elixir
# Count records
query = from p in MyApp.Post,
          select: count(p.id)

MyApp.Repo.one(query)  # Returns integer count

# Average
query = from p in MyApp.Post,
          select: avg(p.rating)

# Sum
query = from o in MyApp.Order,
          select: sum(o.total)

# Min and Max
query = from p in MyApp.Product,
          select: {min(p.price), max(p.price)}
```

Ecto supports standard SQL aggregation functions including `count/1`, `avg/1`,
`sum/1`, `min/1`, and `max/1`.

## Group By and Having

```elixir
query = from p in MyApp.Post,
          group_by: p.category,
          select: {p.category, count(p.id)}

MyApp.Repo.all(query)  # Returns [{"elixir", 10}, {"phoenix", 5}]

# With having clause
query = from p in MyApp.Post,
          group_by: p.category,
          having: count(p.id) > 5,
          select: {p.category, count(p.id)}
```

Use `group_by` to group results by field values and `having` to filter groups
based on aggregate values.

## Order By

```elixir
# Single field ascending
query = from p in MyApp.Post,
          order_by: p.published_at

# Single field descending
query = from p in MyApp.Post,
          order_by: [desc: p.published_at]

# Multiple fields
query = from p in MyApp.Post,
          order_by: [desc: p.published_at, asc: p.title]

# With nulls positioning
query = from p in MyApp.Post,
          order_by: [desc_nulls_last: p.published_at]
```

The `order_by` option controls result ordering. You can specify ascending or
descending order, multiple fields, and null positioning.

## Limit and Offset for Pagination

```elixir
# Simple limit
query = from p in MyApp.Post,
          limit: 10

# With offset for pagination
page = 2
per_page = 10

query = from p in MyApp.Post,
          order_by: [desc: p.published_at],
          limit: ^per_page,
          offset: ^((page - 1) * per_page)

MyApp.Repo.all(query)
```

Use `limit` and `offset` for pagination. Always include an `order_by` clause
to ensure consistent pagination results.

## Inner Join

```elixir
query = from p in MyApp.Post,
          join: c in MyApp.Comment,
          on: c.post_id == p.id,
          select: {p.title, c.body}

MyApp.Repo.all(query)
```

Inner joins return only records that have matching records in both tables. The
`on` clause specifies the join condition.

## Join with assoc Helper

```elixir
query = from p in MyApp.Post,
          join: c in assoc(p, :comments),
          select: {p, c}

MyApp.Repo.all(query)
```

The `assoc/2` helper uses the association definition from your schema, making
joins more maintainable and less error-prone than manually specifying foreign keys.

## Left Join

```elixir
query = from p in MyApp.Post,
          left_join: c in assoc(p, :comments),
          select: {p, c}

MyApp.Repo.all(query)
```

Left joins return all records from the left table (posts) even if there are no
matching records in the right table (comments). Unmatched fields are nil.

## Preload Associations

```elixir
# Preload in separate query
MyApp.Repo.all(from p in MyApp.Post, preload: [:comments])

# Preload multiple associations
MyApp.Repo.all(from p in MyApp.Post, preload: [:comments, :author])

# Nested preload
MyApp.Repo.all(from p in MyApp.Post, preload: [:author, comments: :likes])
```

Preloading fetches associated data efficiently, preventing N+1 query problems.
Separate query preloading is simpler but may require more database round trips.

## Preload with Join

```elixir
query = from p in MyApp.Post,
          join: c in assoc(p, :comments),
          where: c.published_at > p.updated_at,
          preload: [comments: c]

MyApp.Repo.all(query)
```

When you join an association and want to filter it, you can preload the joined
data using the binding variable. This creates a single, more efficient query.

## Complex Nested Preload with Joins

```elixir
query = from p in MyApp.Post,
          join: c in assoc(p, :comments),
          join: l in assoc(c, :likes),
          where: l.inserted_at > c.updated_at,
          preload: [:author, comments: {c, likes: l}]

MyApp.Repo.all(query)
```

You can preload multiple levels of nested associations while maintaining join
filters. The nested tuple syntax preserves the join bindings.

## Preload After Query

```elixir
posts = MyApp.Repo.all(MyApp.Post)
posts_with_comments = MyApp.Repo.preload(posts, :comments)

# Preload with custom query
comments_query = from c in MyApp.Comment, order_by: [desc: c.inserted_at]
posts_with_recent_comments = MyApp.Repo.preload(posts, comments: comments_query)
```

The `preload/2` function can preload associations after fetching records. You
can also customize the preload query for fine-grained control.

## Subquery

```elixir
# Define subquery
subquery = from p in MyApp.Post,
             where: p.published == true,
             select: %{category: p.category, count: count(p.id)},
             group_by: p.category

# Use subquery
query = from s in subquery(subquery),
          where: s.count > 10,
          select: s.category

MyApp.Repo.all(query)
```

Subqueries allow using the result of one query as input to another, enabling
complex analytical queries.

## Fragment for Raw SQL

```elixir
# Use SQL fragment
query = from p in MyApp.Post,
          where: fragment("lower(?)", p.title) == "elixir",
          select: p

# Fragment with parameters
search = "elixir"
query = from p in MyApp.Post,
          where: fragment("lower(?) LIKE ?", p.title, ^"%#{search}%"),
          select: p
```

The `fragment/1` function allows embedding raw SQL in queries when Ecto's DSL
doesn't support a specific database feature. Use sparingly as it reduces portability.

## Query Hints

```elixir
query = from p in MyApp.Post,
          hints: ["USE INDEX FOO"],
          where: p.title == "title"

# Multiple hints
query = from p in MyApp.Post,
          hints: "TABLESAMPLE SYSTEM(1)"

# Dynamic hints
sample = "SYSTEM_ROWS(1)"
query = from p in MyApp.Post,
          hints: ["TABLESAMPLE", unsafe_fragment(^sample)]
```

Query hints provide database-specific optimization instructions like index usage
or table sampling. Hints are database-specific and may not be portable.

## Dynamic Query Building

```elixir
defmodule MyApp.PostQueries do
  import Ecto.Query

  def filter(query \\ MyApp.Post, filters) do
    query
    |> filter_by_category(filters[:category])
    |> filter_by_published(filters[:published])
    |> filter_by_search(filters[:search])
  end

  defp filter_by_category(query, nil), do: query
  defp filter_by_category(query, category) do
    from p in query, where: p.category == ^category
  end

  defp filter_by_published(query, nil), do: query
  defp filter_by_published(query, published) do
    from p in query, where: p.published == ^published
  end

  defp filter_by_search(query, nil), do: query
  defp filter_by_search(query, search) do
    from p in query, where: ilike(p.title, ^"%#{search}%")
  end
end

# Usage
filters = %{category: "elixir", published: true, search: "ecto"}
MyApp.PostQueries.filter(filters) |> MyApp.Repo.all()
```

Building queries dynamically allows handling optional filters and complex search
criteria. Pattern matching on nil values keeps the code clean and readable.

## Ecto.Query.dynamic for Complex Conditions

```elixir
defmodule MyApp.PostQueries do
  import Ecto.Query

  def search(filters) do
    MyApp.Post
    |> where(^build_where_clause(filters))
    |> MyApp.Repo.all()
  end

  defp build_where_clause(filters) do
    Enum.reduce(filters, dynamic(true), fn
      {:category, value}, dynamic ->
        dynamic([p], ^dynamic and p.category == ^value)

      {:published, value}, dynamic ->
        dynamic([p], ^dynamic and p.published == ^value)

      {:min_rating, value}, dynamic ->
        dynamic([p], ^dynamic and p.rating >= ^value)

      _, dynamic ->
        dynamic
    end)
  end
end
```

The `dynamic/2` macro builds query fragments that can be composed at runtime.
This is more flexible than string-based query building and prevents SQL injection.

## Distinct Queries

```elixir
# Distinct on all selected fields
query = from p in MyApp.Post,
          distinct: true,
          select: p.category

# Distinct on specific fields
query = from p in MyApp.Post,
          distinct: [desc: p.published_at],
          select: p
```

The `distinct` option removes duplicate rows from results. You can specify which
fields to use for determining uniqueness.

## Union Queries

```elixir
posts_query = from p in MyApp.Post,
                where: p.published == true,
                select: %{type: "post", title: p.title}

pages_query = from p in MyApp.Page,
                where: p.active == true,
                select: %{type: "page", title: p.title}

# Union
query = posts_query |> union(^pages_query)
MyApp.Repo.all(query)

# Union all (includes duplicates)
query = posts_query |> union_all(^pages_query)
```

Union combines results from multiple queries. Use `union/2` to remove duplicates
or `union_all/2` to keep them.

## Locking for Concurrency Control

```elixir
# Pessimistic locking
query = from p in MyApp.Post,
          where: p.id == ^post_id,
          lock: "FOR UPDATE"

post = MyApp.Repo.one(query)

# Optimistic locking (using version field in schema)
changeset = MyApp.Post.changeset(post, params)
case MyApp.Repo.update(changeset) do
  {:ok, updated_post} -> # Success
  {:error, changeset} -> # Failed, possibly due to concurrent update
end
```

Locking prevents race conditions in concurrent operations. Pessimistic locking
uses database locks, while optimistic locking uses version fields.

## Lateral Joins for Correlated Subqueries

```elixir
defp newest_records(parent_ids, assoc, n) do
  %{related_key: related_key, queryable: queryable} = assoc

  squery = from q in queryable,
             where: field(q, ^related_key) == parent_as(:parent_ids).id,
             order_by: {:desc, :created_at},
             limit: ^n

  query = from f in fragment("SELECT id from UNNEST(?::int[]) AS id", ^parent_ids),
             as: :parent_ids,
             inner_lateral_join: s in subquery(squery),
             on: true,
             select: s

  MyApp.Repo.all(query)
end
```

Lateral joins allow subqueries that reference columns from the outer query,
enabling complex correlated queries like "top N per group."

## Named Bindings

```elixir
query = from p in MyApp.Post, as: :posts
query = from [posts: p] in query,
          join: c in assoc(p, :comments), as: :comments
query = from [posts: p, comments: c] in query,
          where: c.score > 10,
          select: {p.title, c.body}
```

Named bindings make complex queries more readable by giving explicit names to
each table or subquery in the query.

## When to Use This Skill

Use ecto-query-patterns when you need to:

- Query database records with filtering, sorting, and pagination
- Join multiple tables to fetch related data
- Preload associations to avoid N+1 query problems
- Aggregate data using count, sum, average, or other functions
- Build dynamic queries based on user input or application logic
- Perform complex analytical queries with subqueries and grouping
- Optimize query performance with hints and indexes
- Handle concurrent updates with locking mechanisms
- Create reusable query components through composition
- Implement search functionality with pattern matching

## Best Practices

- Always use the pin operator `^` for external values to prevent SQL injection
- Compose queries into small, reusable functions
- Use `preload` to avoid N+1 query problems with associations
- Select only the fields you need to reduce data transfer
- Add `order_by` when using `limit` and `offset` for consistent pagination
- Use `assoc/2` helper instead of manual foreign key joins
- Leverage `Ecto.Query.dynamic/2` for complex conditional queries
- Keep query logic in dedicated query modules, not controllers
- Use subqueries for complex aggregations and analytical queries
- Profile queries in development to identify performance issues
- Use database indexes for frequently queried fields
- Prefer preloading with joins when filtering associated data
- Use named bindings for complex multi-join queries
- Test query functions independently from your business logic
- Document complex queries with comments explaining the logic

## Common Pitfalls

- Forgetting the pin operator `^`, causing compilation errors
- Not preloading associations, leading to N+1 query problems
- Selecting entire structs when only a few fields are needed
- Using `Repo.all/1` in loops instead of batch operations
- Building queries with string concatenation (SQL injection risk)
- Not adding `order_by` when using pagination
- Joining tables without filtering, causing cartesian products
- Using fragments excessively, reducing query portability
- Not handling nil values in dynamic query building
- Performing aggregations in application code instead of database
- Forgetting to wrap updates in transactions when necessary
- Using `Repo.preload/2` in loops instead of batch preloading
- Not utilizing query composition for reusable logic
- Mixing business logic with query construction
- Over-optimizing queries prematurely without profiling
- Using distinct without understanding its performance impact
- Not leveraging database-specific features when appropriate
- Creating overly complex queries that are hard to maintain
- Ignoring database query logs during development
- Not testing edge cases like empty results or nil values

## Resources

### Official Ecto Documentation

- [Ecto.Query Module](https://hexdocs.pm/ecto/Ecto.Query.html)
- [Query Syntax](https://hexdocs.pm/ecto/Ecto.Query.html#module-query-expressions)
- [Dynamic Queries](https://hexdocs.pm/ecto/dynamic-queries.html)
- [Associations Guide](https://hexdocs.pm/ecto/associations.html)
- [Query Composition](https://hexdocs.pm/ecto/Ecto.Query.html#module-composition)

### Query Operators and Functions

- [Comparison Operators](https://hexdocs.pm/ecto/Ecto.Query.html#module-comparison-operators)
- [Aggregation Functions](https://hexdocs.pm/ecto/Ecto.Query.API.html)
- [Fragment Function](https://hexdocs.pm/ecto/Ecto.Query.API.html#fragment/1)
- [Dynamic Macro](https://hexdocs.pm/ecto/Ecto.Query.html#dynamic/2)

### Performance and Optimization

- [Preloading Associations](https://hexdocs.pm/ecto/Ecto.html#module-preloading)
- [Query Optimization Tips](https://hexdocs.pm/ecto/Ecto.Query.html#module-query-optimization)
- [Database Constraints](https://hexdocs.pm/ecto/constraints-and-upserts.html)

### Community Resources

- [Elixir School - Ecto Queries](https://elixirschool.com/en/lessons/ecto/querying)
- [Programming Ecto Book](https://pragprog.com/titles/wmecto/programming-ecto/)
- [Ecto Query Examples](https://hexdocs.pm/ecto/Ecto.Query.html#module-examples)
