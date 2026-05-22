---
name: "ActiveRecord Query Patterns"
description: "Complete guide to ActiveRecord query optimization, associations, scopes, and PostgreSQL-specific patterns. Use when: (1) Writing database queries, (2) Designing model associations, (3) Creating migrations, (4) Optimizing query performance, (5) Debugging N+1 queries and GROUP BY errors. Trigger keywords: database, models, associations, validations, queries, ActiveRecord, scopes, migrations, N+1, PostgreSQL, indexes, eager loading"
version: 1.1.0
---

# ActiveRecord Query Patterns

## Query Decision Tree

```
What do I need?
│
├─ Find records by ID or attributes?
│   ├─ Single record: find(id), find_by(attrs)
│   └─ Multiple records: where(conditions)
│
├─ Access associated records?
│   ├─ Just filtering? → joins(:association)
│   └─ Loading data? → includes(:association)
│
├─ Aggregate data (count, sum, avg)?
│   └─ GROUP BY query
│       └─ REMEMBER: Every SELECT column must be in GROUP BY or aggregate
│
├─ Complex multi-step query?
│   └─ Query Object pattern (app/queries/)
│
├─ Hierarchical/recursive data?
│   └─ CTE (Common Table Expression)
│
└─ Full-text search?
    └─ pg_search gem with tsvector indexes
```

---

## NEVER Do This

**NEVER** use `includes` with `group`:
```ruby
# WRONG - PostgreSQL error
Task.includes(:carrier).group(:status).count

# RIGHT - Separate queries
status_counts = Task.group(:status).count
tasks = Task.where(status: status_counts.keys.first).includes(:carrier)
```

**NEVER** iterate without eager loading:
```ruby
# WRONG - N+1 queries
tasks = Task.all
tasks.each { |t| puts t.carrier.name }  # Query per task!

# RIGHT - Eager load
tasks = Task.includes(:carrier)
tasks.each { |t| puts t.carrier.name }  # Single query
```

**NEVER** load all records into memory:
```ruby
# WRONG - Memory explosion
Task.all.each { |task| process(task) }

# RIGHT - Batch processing
Task.find_each(batch_size: 1000) { |task| process(task) }
```

**NEVER** use `present?` to check existence:
```ruby
# WRONG - Loads all records
Task.where(status: 'pending').present?

# RIGHT - Efficient existence check
Task.where(status: 'pending').exists?
```

**NEVER** forget indexes on foreign keys:
```ruby
# WRONG - No index
t.references :merchant, foreign_key: true, index: false

# RIGHT - Always index foreign keys
t.references :merchant, null: false, foreign_key: true  # index: true is default
```

---

## Model Template

```ruby
class Task < ApplicationRecord
  # == Constants ==============================================================
  STATUSES = %w[pending in_progress completed].freeze

  # == Associations ===========================================================
  belongs_to :account
  belongs_to :merchant
  belongs_to :carrier, optional: true
  has_many :timelines, dependent: :destroy

  # == Validations ============================================================
  validates :status, presence: true, inclusion: { in: STATUSES }
  validates :tracking_number, presence: true, uniqueness: { scope: :account_id }

  # == Scopes =================================================================
  scope :active, -> { where.not(status: 'completed') }
  scope :for_carrier, ->(carrier) { where(carrier: carrier) }

  # == Callbacks ==============================================================
  before_validation :generate_tracking_number, on: :create

  # == Class Methods ==========================================================
  def self.search(query)
    where("tracking_number ILIKE ?", "%#{query}%")
  end

  # == Instance Methods =======================================================
  def complete!
    update!(status: 'completed', completed_at: Time.current)
  end

  private

  def generate_tracking_number
    self.tracking_number ||= SecureRandom.hex(8).upcase
  end
end
```

---

## Eager Loading Quick Reference

| Method | Query Type | Use Case |
|--------|-----------|----------|
| `includes` | Smart (auto-selects) | Default choice |
| `preload` | Separate queries | Can't filter on association |
| `eager_load` | LEFT JOIN | Need to filter on association |
| `joins` | INNER JOIN | Filtering only, no data loading |

```ruby
# Multiple associations
Task.includes(:carrier, :merchant, :recipient)

# Nested associations
Task.includes(merchant: :branches)

# Filter on association (requires references or use joins)
Task.joins(:carrier).where(carriers: { active: true })
```

---

## Scope Patterns

```ruby
# Simple scopes
scope :active, -> { where.not(status: 'completed') }
scope :recent, -> { order(created_at: :desc) }

# Parameterized scopes
scope :by_status, ->(status) { where(status: status) }
scope :created_after, ->(date) { where('created_at >= ?', date) }

# Conditional (always returns relation)
scope :by_status_if, ->(status) { where(status: status) if status.present? }

# Chainable
Task.active.recent.by_status('pending')
```

---

## GROUP BY (PostgreSQL Critical)

**Rule**: Every non-aggregated SELECT column must appear in GROUP BY.

```ruby
# CORRECT
Task.group(:status).count
Task.group(:status).sum(:amount)
Task.group(:status, :task_type).count

# CORRECT - Explicit select
Task.select(:status, 'COUNT(*) as count', 'AVG(amount) as avg')
    .group(:status)

# Date grouping
Task.group("DATE(created_at)").count
```

---

## Migration Quick Reference

```ruby
class CreateTasks < ActiveRecord::Migration[7.1]
  def change
    create_table :tasks do |t|
      t.references :account, null: false, foreign_key: true
      t.string :tracking_number, null: false
      t.string :status, null: false, default: 'pending'
      t.decimal :amount, precision: 10, scale: 2
      t.jsonb :metadata, default: {}
      t.timestamps

      t.index :tracking_number, unique: true
      t.index :status
      t.index [:account_id, :status]
      t.index :metadata, using: :gin
    end
  end
end

# Concurrent index (large tables)
class AddIndex < ActiveRecord::Migration[7.1]
  disable_ddl_transaction!
  def change
    add_index :tasks, :status, algorithm: :concurrently
  end
end
```

---

## Performance Checklist

```
Before writing any query:

[ ] Am I loading more columns than needed? → Use select/pluck
[ ] Am I iterating and accessing associations? → Use includes
[ ] Am I using GROUP BY? → Every SELECT column grouped or aggregated?
[ ] Am I using includes with GROUP BY? → DON'T! Separate queries
[ ] Will this query run on large table? → Check indexes exist
[ ] Am I loading all records? → Use find_each for batches
[ ] Am I checking existence? → Use exists? not present?
[ ] Do indexes exist for WHERE/ORDER columns?
```

---

## Enum Pattern

```ruby
class Task < ApplicationRecord
  enum status: {
    pending: 0,
    in_progress: 1,
    completed: 2
  }, _prefix: true

  # Generated methods:
  # task.status_pending?
  # task.status_completed!
  # Task.status_pending (scope)
  # Task.not_status_pending (scope)
end
```

---

## JSONB Quick Reference

```ruby
# Migration
add_column :tasks, :metadata, :jsonb, default: {}
add_index :tasks, :metadata, using: :gin

# Queries
Task.where("metadata @> ?", { priority: 1 }.to_json)  # Contains
Task.where("metadata ->> 'key' = ?", 'value')         # Extract as text
Task.where("metadata ? 'key'")                        # Key exists
```

---

## Debugging Queries

```ruby
# Enable logging
ActiveRecord::Base.logger = Logger.new(STDOUT)

# Explain query plan
Task.where(status: 'pending').explain(:analyze)

# Use Bullet gem for N+1 detection
# Gemfile: gem 'bullet', group: :development
```

---

## References

Detailed patterns and examples in `references/`:
- `associations.md` - Association types, options, polymorphic
- `query-patterns.md` - Basic queries, eager loading, subqueries
- `scopes-query-objects.md` - Scope patterns, query objects
- `migrations.md` - Create table, safe migrations, JSONB
- `performance.md` - Batch processing, counter caches, indexes
- `rails7-8-features.md` - Composite keys, encryption, multi-db
- `advanced-patterns.md` - Enums, database views, CTEs, STI
- `postgresql-features.md` - Full-text search, JSONB, arrays
