---
name: plutonium-definition-query
description: Configure search, filters, scopes, and sorting for Plutonium resources
---

# Definition Query

Configure how users can search, filter, and sort resource collections.

## Overview

```ruby
class PostDefinition < ResourceDefinition
  # Search - global text search
  search do |scope, query|
    scope.where("title ILIKE ?", "%#{query}%")
  end

  # Filters - dropdown filter panel
  filter :title, with: :text, predicate: :contains
  filter :status, with: :select, choices: %w[draft published archived]
  filter :published, with: :boolean
  filter :created_at, with: :date_range
  filter :category, with: :association

  # Scopes - quick filter buttons
  scope :published
  scope :draft

  # Sorting - sortable columns
  sort :title
  sort :created_at

  # Default sort
  default_sort :created_at, :desc
end
```

## Search

Define global search across fields:

```ruby
# Single field
search do |scope, query|
  scope.where("title ILIKE ?", "%#{query}%")
end

# Multiple fields
search do |scope, query|
  scope.where(
    "title ILIKE :q OR content ILIKE :q OR author_name ILIKE :q",
    q: "%#{query}%"
  )
end

# With associations
search do |scope, query|
  scope.joins(:author).where(
    "posts.title ILIKE :q OR users.name ILIKE :q",
    q: "%#{query}%"
  ).distinct
end

# Split search terms
search do |scope, query|
  terms = query.split(/\s+/)
  terms.reduce(scope) do |current_scope, term|
    current_scope.where("title ILIKE ?", "%#{term}%")
  end
end
```

## Filters

Plutonium provides **6 built-in filter types**. Use shorthand symbols or full class names.

### Text Filter

String/text filtering with pattern matching.

```ruby
# Shorthand (recommended)
filter :title, with: :text, predicate: :contains
filter :status, with: :text, predicate: :eq

# Full class name
filter :title, with: Plutonium::Query::Filters::Text, predicate: :contains
```

**Predicates:**

| Predicate | SQL | Description |
|-----------|-----|-------------|
| `:eq` | `= value` | Exact match (default) |
| `:not_eq` | `!= value` | Not equal |
| `:contains` | `LIKE %value%` | Contains substring |
| `:not_contains` | `NOT LIKE %value%` | Does not contain |
| `:starts_with` | `LIKE value%` | Starts with |
| `:ends_with` | `LIKE %value` | Ends with |
| `:matches` | `LIKE value` | Pattern match (`*` becomes `%`) |
| `:not_matches` | `NOT LIKE value` | Does not match pattern |

### Boolean Filter

True/false filtering for boolean columns.

```ruby
# Basic
filter :active, with: :boolean

# Custom labels
filter :published, with: :boolean, true_label: "Published", false_label: "Draft"
```

Renders a select dropdown with "All", true label ("Yes"), and false label ("No").

### Date Filter

Single date filtering with comparison predicates.

```ruby
filter :created_at, with: :date, predicate: :gteq  # On or after
filter :due_date, with: :date, predicate: :lt      # Before
filter :published_at, with: :date, predicate: :eq  # On exact date
```

**Predicates:**

| Predicate | Description |
|-----------|-------------|
| `:eq` | On this date (default) |
| `:not_eq` | Not on this date |
| `:lt` | Before date |
| `:lteq` | On or before date |
| `:gt` | After date |
| `:gteq` | On or after date |

### Date Range Filter

Filter between two dates (from/to).

```ruby
# Basic
filter :created_at, with: :date_range

# Custom labels
filter :published_at, with: :date_range,
  from_label: "Published from",
  to_label: "Published to"
```

Renders two date pickers. Both are optional - users can filter with just "from" or just "to".

### Select Filter

Filter from predefined choices.

```ruby
# Static choices (array)
filter :status, with: :select, choices: %w[draft published archived]

# Dynamic choices (proc)
filter :category, with: :select, choices: -> { Category.pluck(:name) }

# Multiple selection
filter :tags, with: :select, choices: %w[ruby rails js], multiple: true
```

### Association Filter

Filter by associated record.

```ruby
# Basic - infers Category class from :category key
filter :category, with: :association

# Explicit class
filter :author, with: :association, class_name: User

# Multiple selection
filter :tags, with: :association, class_name: Tag, multiple: true
```

Renders a resource select dropdown. Converts filter key to foreign key (`:category` -> `:category_id`).

## Custom Filters

### Custom Filter Class

```ruby
class PriceRangeFilter < Plutonium::Query::Filter
  def apply(scope, min: nil, max: nil)
    scope = scope.where("price >= ?", min) if min.present?
    scope = scope.where("price <= ?", max) if max.present?
    scope
  end

  def customize_inputs
    input :min, as: :number
    input :max, as: :number
    field :min, placeholder: "Min price..."
    field :max, placeholder: "Max price..."
  end
end

# Use in definition
filter :price, with: PriceRangeFilter
```

## Scopes

Scopes appear as quick filter buttons. They reference model scopes.

### Basic Usage

```ruby
class PostDefinition < ResourceDefinition
  scope :published    # Uses Post.published
  scope :draft        # Uses Post.draft
  scope :featured     # Uses Post.featured
end
```

### Inline Scope

Use block syntax with the scope passed as an argument:

```ruby
scope(:recent) { |scope| scope.where('created_at > ?', 1.week.ago) }
scope(:this_month) { |scope| scope.where(created_at: Time.current.all_month) }
```

### With Controller Context

Inline scopes have access to controller context like `current_user`:

```ruby
scope(:mine) { |scope| scope.where(author: current_user) }
scope(:my_team) { |scope| scope.where(team: current_user.team) }
```

### Default Scope

Set a scope as default to apply it when no scope is explicitly selected:

```ruby
class PostDefinition < ResourceDefinition
  scope :published, default: true  # Applied by default
  scope :draft
  scope :archived
end
```

When a default scope is set:
- The default scope is applied on initial page load
- The default scope button is highlighted (not "All")
- Clicking "All" shows all records without any scope filter
- URL without scope param uses the default; URL with `?q[scope]=` uses "All"

## Sorting

### Basic Sorting

```ruby
sort :title
sort :created_at
sort :view_count

# Multiple at once
sorts :title, :created_at, :view_count
```

### Default Sort

```ruby
# Field and direction
default_sort :created_at, :desc
default_sort :title, :asc

# Complex sorting with block
default_sort { |scope| scope.order(featured: :desc, created_at: :desc) }
```

**Note:** Default sort only applies when no sort params are provided.

## URL Parameters

Query parameters are structured under `q`:

```
/posts?q[search]=rails
/posts?q[title][query]=widget
/posts?q[status][value]=published
/posts?q[created_at][from]=2024-01-01&q[created_at][to]=2024-12-31
/posts?q[scope]=recent
/posts?q[sort_fields][]=created_at&q[sort_directions][created_at]=desc
```

## Filter Summary Table

| Type | Symbol | Input Params | Options |
|------|--------|--------------|---------|
| Text | `:text` | `query` | `predicate:` |
| Boolean | `:boolean` | `value` | `true_label:`, `false_label:` |
| Date | `:date` | `value` | `predicate:` |
| Date Range | `:date_range` | `from`, `to` | `from_label:`, `to_label:` |
| Select | `:select` | `value` | `choices:`, `multiple:` |
| Association | `:association` | `value` | `class_name:`, `multiple:` |

## Complete Example

```ruby
class ProductDefinition < ResourceDefinition
  # Full-text search
  search do |scope, query|
    scope.where(
      "name ILIKE :q OR description ILIKE :q",
      q: "%#{query}%"
    )
  end

  # Filters
  filter :name, with: :text, predicate: :contains
  filter :status, with: :select, choices: %w[draft active discontinued]
  filter :featured, with: :boolean
  filter :created_at, with: :date_range
  filter :price, with: :date, predicate: :gteq
  filter :category, with: :association

  # Quick scopes
  scope :active, default: true
  scope :featured
  scope(:recent) { |scope| scope.where('created_at > ?', 1.week.ago) }

  # Sortable columns
  sorts :name, :price, :created_at

  # Default sort
  default_sort :created_at, :desc
end
```

## Performance Tips

1. **Add indexes** for filtered/sorted columns
2. **Use `.distinct`** when joining associations in search
3. **Consider `pg_search`** for complex full-text search
4. **Limit search fields** to indexed columns
5. **Use scopes** instead of filters for common queries

## Related Skills

- `plutonium-definition` - Overview and structure
- `plutonium-definition-fields` - Fields, inputs, displays
- `plutonium-definition-actions` - Actions and interactions
