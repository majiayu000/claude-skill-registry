---
name: definition-query
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

  # Filters - sidebar filter inputs
  filter :status, with: Plutonium::Query::Filters::Text, predicate: :eq

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

Currently Plutonium provides the **Text filter** with various predicates.

### Text Filter Predicates

```ruby
# Exact match
filter :status, with: Plutonium::Query::Filters::Text, predicate: :eq

# Not equal
filter :status, with: Plutonium::Query::Filters::Text, predicate: :not_eq

# Contains (LIKE %value%)
filter :title, with: Plutonium::Query::Filters::Text, predicate: :contains

# Not contains
filter :title, with: Plutonium::Query::Filters::Text, predicate: :not_contains

# Starts with (LIKE value%)
filter :slug, with: Plutonium::Query::Filters::Text, predicate: :starts_with

# Ends with (LIKE %value)
filter :email, with: Plutonium::Query::Filters::Text, predicate: :ends_with

# Pattern match (* becomes %)
filter :title, with: Plutonium::Query::Filters::Text, predicate: :matches

# Not matching pattern
filter :title, with: Plutonium::Query::Filters::Text, predicate: :not_matches
```

### Custom Filter with Lambda

```ruby
filter :published, with: ->(scope, value) {
  value == "true" ? scope.where.not(published_at: nil) : scope.where(published_at: nil)
}
```

### Custom Filter Class

```ruby
# Define custom filter
class DateRangeFilter < Plutonium::Query::Filter
  def apply(scope, start_date: nil, end_date: nil)
    scope = scope.where("#{key} >= ?", start_date.beginning_of_day) if start_date.present?
    scope = scope.where("#{key} <= ?", end_date.end_of_day) if end_date.present?
    scope
  end

  def customize_inputs
    input :start_date, as: :date
    input :end_date, as: :date
  end
end

# Use in definition
filter :created_at, with: DateRangeFilter
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
/posts?q[status][query]=published
/posts?q[scope]=recent
/posts?q[sort_fields][]=created_at&q[sort_directions][created_at]=desc
```

Combined:
```
/posts?q[search]=rails&q[scope]=published&q[sort_fields][]=created_at&q[sort_directions][created_at]=desc
```

## Common Patterns

### Status Filter

```ruby
class PostDefinition < ResourceDefinition
  filter :status, with: Plutonium::Query::Filters::Text, predicate: :eq

  scope :draft
  scope :published
  scope :archived
end
```

### Date-Based Scopes

```ruby
class PostDefinition < ResourceDefinition
  scope(:today) { |scope| scope.where(created_at: Time.current.all_day) }
  scope(:this_week) { |scope| scope.where(created_at: Time.current.all_week) }
  scope(:this_month) { |scope| scope.where(created_at: Time.current.all_month) }
end
```

### Archive State Scopes

```ruby
class PostDefinition < ResourceDefinition
  scope :active
  scope :archived

  # Default to showing only active
  default_sort { |scope| scope.active.order(created_at: :desc) }
end
```

### Full-Text Search with pg_search

```ruby
# Model
class Post < ApplicationRecord
  include PgSearch::Model
  pg_search_scope :search_content, against: [:title, :content]
end

# Definition
class PostDefinition < ResourceDefinition
  search do |scope, query|
    scope.search_content(query)
  end
end
```

### Association Filtering

```ruby
class PostDefinition < ResourceDefinition
  filter :author_name, with: Plutonium::Query::Filters::Text, predicate: :contains

  search do |scope, query|
    scope.joins(:author).where(
      "posts.title ILIKE :q OR users.name ILIKE :q",
      q: "%#{query}%"
    ).distinct
  end
end
```

## Complete Example

```ruby
class PostDefinition < ResourceDefinition
  # Full-text search
  search do |scope, query|
    scope.where(
      "title ILIKE :q OR content ILIKE :q",
      q: "%#{query}%"
    )
  end

  # Filters
  filter :status, with: Plutonium::Query::Filters::Text, predicate: :eq
  filter :category, with: Plutonium::Query::Filters::Text, predicate: :eq
  filter :title, with: Plutonium::Query::Filters::Text, predicate: :contains

  # Quick scopes (reference model scopes)
  scope :published
  scope :draft
  scope :featured
  scope(:recent) { |scope| scope.where('created_at > ?', 1.week.ago) }

  # Sortable columns
  sorts :title, :created_at, :view_count, :published_at

  # Default: newest first
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

- `definition` - Overview and structure
- `definition-fields` - Fields, inputs, displays
- `definition-actions` - Actions and interactions
