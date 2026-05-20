---
name: active-record-model-best-practices
description: Best practices for Ruby on Rails models, splitting code into well-organized, maintainable code. Use when a model exceeds ~100 lines, has mixed responsibilities, or when the user asks to refactor, extract, clean up, or organize a Rails model. Applies patterns: concerns, service objects, query objects, form objects, and value objects.
---

# Rails Model Refactoring

When refactoring a Rails model, analyze the file and extract code into the appropriate pattern based on what the code does. The model itself should only contain associations, enums, basic validations, and concern includes.

## Decision Framework

Read the model file and classify each block of code:

| Code type | Extract to | Location |
|---|---|---|
| Related scopes + simple methods sharing a theme | Concern | `app/models/concerns/` |
| Business logic, multi-step operations, callbacks with side effects | Service object | `app/services/` |
| Complex queries, multi-join scopes, reporting queries | Query object | `app/queries/` |
| Context-specific validations (e.g. registration vs admin update) | Form object | `app/forms/` |
| Domain concepts beyond a primitive (money, coordinates, scores) | Value object | `app/models/` |
| Associations, enums, core validations, simple scopes | Keep on model | — |

## Patterns

### Concerns

Use for grouping related scopes, validations, callbacks, and simple instance methods that share a single theme. Name the concern after the capability it provides.

```ruby
# app/models/concerns/searchable.rb
module Searchable
  extend ActiveSupport::Concern

  included do
    scope :search, ->(query) { where("name ILIKE ?", "%#{query}%") }
  end

  def matching_terms(query)
    name.scan(/#{Regexp.escape(query)}/i)
  end
end
```

### Service Objects

Use for business logic, orchestration of multiple models, and anything triggered by a user action that involves more than a simple CRUD operation. Follow the single-responsibility principle — one service, one operation.

```ruby
# app/services/players/calculate_stats.rb
module Players
  class CalculateStats
    def initialize(player)
      @player = player
    end

    def call
      # complex logic here
    end
  end
end
```

Conventions:
- Namespace under the model name: `Players::CalculateStats`
- Single public method: `call`
- Accept dependencies via `initialize`
- Return a result or raise a domain-specific error

### Query Objects

Use for complex database queries that involve joins, subqueries, CTEs, or multi-condition filtering that would clutter a model with scopes.

```ruby
# app/queries/players/free_agent_query.rb
module Players
  class FreeAgentQuery
    def initialize(relation = Player.all)
      @relation = relation
    end

    def call(filters = {})
      @relation
        .where(contract_status: :expired)
        .where("age < ?", filters[:max_age])
        .joins(:stats)
        .order(war: :desc)
    end
  end
end
```

Conventions:
- Accept a base relation in `initialize` (default to `Model.all`)
- Return an ActiveRecord relation so it remains chainable
- Single public method: `call`

### Form Objects

Use when validations only apply in specific contexts, or when a form spans multiple models.

```ruby
# app/forms/player_registration_form.rb
class PlayerRegistrationForm
  include ActiveModel::Model
  include ActiveModel::Attributes

  attribute :name, :string
  attribute :email, :string
  attribute :team_id, :integer
  attribute :position, :string

  validates :name, :email, :position, presence: true
  validates :email, format: { with: URI::MailTo::EMAIL_REGEXP }

  def save
    return false unless valid?
    Player.create!(attributes)
  end
end
```

### Value Objects

Use for domain concepts that deserve their own identity beyond a raw primitive.

```ruby
# app/models/batting_average.rb
class BattingAverage
  include Comparable

  def initialize(hits, at_bats)
    @hits = hits
    @at_bats = at_bats
  end

  def value
    return 0.0 if @at_bats.zero?
    (@hits.to_f / @at_bats).round(3)
  end

  def elite?
    value >= 0.300
  end

  def <=>(other)
    value <=> other.value
  end
end
```

## Refactoring Process

1. **Read the entire model** and identify every method, scope, callback, and validation.
2. **Classify each block** using the decision framework table above.
3. **Extract in order**: value objects first, then query objects, then service objects, then concerns. Do concerns last because some may become unnecessary after other extractions.
4. **Update the model** to include concerns and delegate to new objects.
5. **Verify** that the slimmed-down model only contains: associations, enums, core validations, and concern includes.
6. **Create or update tests** for each extracted class. Each new class gets its own spec file mirroring the source path.

## What NOT to Do

- Don't extract everything — simple one-line scopes and basic validations belong on the model.
- Don't create a class for trivial logic just to hit a line count target.
- Don't use concerns as junk drawers — each concern should have a clear, single theme.
- Don't break ActiveRecord conventions (e.g. don't move associations into concerns).
- Don't introduce callback-heavy service objects — prefer explicit invocation over implicit hooks.