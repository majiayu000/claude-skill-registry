---
name: active-record-db
description: This skill should be used when the user asks about Active Record models,
  database migrations, queries, associations (belongs_to, has_many, has_one, has_and_belongs_to_many),
  validations, callbacks, sc
---

---
name: active-record-db
description: This skill should be used when the user asks about Active Record models, database migrations, queries, associations (belongs_to, has_many, has_one, has_and_belongs_to_many), validations, callbacks, scopes, database schema design, SQL optimization, N+1 queries, eager loading, joins, or database-specific features (PostgreSQL, MySQL, SQLite). Also use when discussing ORM patterns, data modeling, or database best practices. Examples:

<example>
Context: User wants to create a relationship between models
user: "How do I set up a one-to-many relationship between Users and Posts?"
assistant: "I'll explain has_many and belongs_to associations, including foreign keys and conventions."
<commentary>
This relates to Active Record associations and database relationships.
</commentary>
</example>

<example>
Context: User's queries are slow
user: "My product index page is really slow with hundreds of queries"
assistant: "This is the N+1 query problem. Let me show you eager loading with includes."
<commentary>
This involves query optimization and the N+1 problem.
</commentary>
</example>

<example>
Context: User needs to validate data
user: "How do I ensure emails are unique and properly formatted?"
assistant: "I'll demonstrate Active Record validations for uniqueness and format."
<commentary>
This relates to model validations and data integrity.
</commentary>
</example>
---

# Active Record & Databases: Rails ORM Mastery

## Overview

Active Record is Rails' Object-Relational Mapping (ORM) layer. It connects Ruby objects to database tables, providing an elegant API for creating, reading, updating, and deleting data without writing SQL.

Active Record embodies Rails philosophy:
- **Convention over configuration**: Table names, foreign keys, and primary keys follow conventions
- **DRY**: Schema drives model attributes; no redundant declarations
- **Object-oriented**: Work with Ruby objects, not raw SQL
- **Database agnostic**: Same code works with PostgreSQL, MySQL, SQLite

Master Active Record and you master data in Rails applications.

## Models and Conventions

### Basic Model

A model represents a table and provides domain logic:

```ruby
# app/models/product.rb
class Product < ApplicationRecord
  # Table: products
  # Primary key: id
  # Attributes: name, price, description, created_at, updated_at
end
```

Rails infers:
- Table name: `products` (pluralized)
- Primary key: `id`
- Attributes from schema
- Timestamps: `created_at`, `updated_at`

No configuration needed—just convention.

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Model | Singular, CamelCase | `Product`, `LineItem` |
| Table | Plural, snake_case | `products`, `line_items` |
| Foreign key | `model_id` | `user_id`, `category_id` |
| Join table | Alphabetical models | `orders_products` |
| Primary key | `id` | Auto-generated integer |

**Irregular pluralizations** work automatically:
- `Person` → `people`
- `Child` → `children`
- `Octopus` → `octopi`

Rails' inflector handles English pluralization rules.

### Schema Conventions

Special column names have automatic behavior:

- **`id`**: Primary key (auto-generated)
- **`created_at`**: Set when record created
- **`updated_at`**: Updated when record saved
- **`lock_version`**: Optimistic locking counter
- **`type`**: Single Table Inheritance discriminator
- **`{association}_id`**: Foreign key for associations
- **`{association}_type`**: Polymorphic association type

## Migrations

Migrations are Ruby scripts that modify database schema.

### Creating Migrations

```bash
# Generate migration
rails generate migration CreateProducts name:string price:decimal

# Generate model (includes migration)
rails generate model Product name:string price:decimal
```

Generates:

```ruby
# db/migrate/20240115100000_create_products.rb
class CreateProducts < ActiveRecord::Migration[8.0]
  def change
    create_table :products do |t|
      t.string :name
      t.decimal :price, precision: 10, scale: 2

      t.timestamps
    end
  end
end
```

### Running Migrations

```bash
rails db:migrate              # Run pending migrations
rails db:rollback             # Undo last migration
rails db:migrate:status       # Show migration status
rails db:migrate VERSION=20240115100000  # Migrate to specific version
```

### Migration Methods

**Creating tables:**

```ruby
create_table :products do |t|
  t.string :name, null: false
  t.text :description
  t.decimal :price, precision: 10, scale: 2
  t.integer :quantity, default: 0
  t.boolean :available, default: true
  t.references :category, foreign_key: true
  t.timestamps
end
```

**Modifying tables:**

```ruby
change_table :products do |t|
  t.rename :description, :details
  t.change :price, :decimal, precision: 12, scale: 2
  t.remove :quantity
  t.string :sku
  t.index :sku, unique: true
end
```

**Adding columns:**

```ruby
add_column :products, :featured, :boolean, default: false
add_index :products, :name
add_reference :products, :supplier, foreign_key: true
```

**Removing columns:**

```ruby
remove_column :products, :quantity
remove_index :products, :sku
remove_reference :products, :supplier
```

See `references/migrations.md` for comprehensive migration patterns.

## Associations

Associations define relationships between models.

### belongs_to

Declares a one-to-one or many-to-one relationship:

```ruby
class Product < ApplicationRecord
  belongs_to :category
  # Expects: category_id column in products table
  # Provides: product.category
end
```

### has_many

Declares a one-to-many relationship:

```ruby
class Category < ApplicationRecord
  has_many :products
  # Expects: category_id column in products table
  # Provides: category.products
end
```

### has_one

Declares a one-to-one relationship:

```ruby
class User < ApplicationRecord
  has_one :profile
  # Expects: user_id column in profiles table
  # Provides: user.profile
end
```

### has_many :through

Many-to-many with join model:

```ruby
class Order < ApplicationRecord
  has_many :line_items
  has_many :products, through: :line_items
end

class LineItem < ApplicationRecord
  belongs_to :order
  belongs_to :product
end

class Product < ApplicationRecord
  has_many :line_items
  has_many :orders, through: :line_items
end
```

### has_and_belongs_to_many

Many-to-many without join model:

```ruby
class Product < ApplicationRecord
  has_and_belongs_to_many :tags
  # Expects: products_tags join table (no id, no timestamps)
end

class Tag < ApplicationRecord
  has_and_belongs_to_many :products
end
```

### Polymorphic Associations

One model belongs to multiple model types:

```ruby
class Comment < ApplicationRecord
  belongs_to :commentable, polymorphic: true
  # Expects: commentable_type and commentable_id columns
end

class Post < ApplicationRecord
  has_many :comments, as: :commentable
end

class Product < ApplicationRecord
  has_many :comments, as: :commentable
end

# Usage:
post.comments.create(body: "Great post!")
product.comments.create(body: "Love this product!")
```

See `references/associations.md` for advanced association patterns.

## Querying

Active Record provides a rich query interface.

### Finding Records

```ruby
# Find by primary key
Product.find(1)
Product.find([1, 2, 3])

# Find by attributes
Product.find_by(name: "Widget")
Product.find_by!(name: "Widget")  # Raises if not found

# First, last, all
Product.first
Product.last
Product.all
```

### Where Queries

```ruby
# Simple conditions
Product.where(available: true)
Product.where("price < ?", 10)
Product.where("price BETWEEN ? AND ?", 10, 50)

# Hash conditions
Product.where(category_id: [1, 2, 3])
Product.where.not(category_id: 1)

# Ranges
Product.where(created_at: 1.week.ago..Time.now)

# Pattern matching
Product.where("name LIKE ?", "%widget%")
```

### Ordering and Limiting

```ruby
Product.order(created_at: :desc)
Product.order(price: :asc, name: :asc)
Product.limit(10)
Product.offset(20).limit(10)  # Pagination
```

### Selecting Specific Columns

```ruby
Product.select(:id, :name, :price)
Product.select("id, name, UPPER(name) as uppercase_name")
```

### Joining Tables

```ruby
# Inner join
Product.joins(:category)
Product.joins(:category, :tags)

# Left outer join
Product.left_outer_joins(:reviews)

# With conditions
Product.joins(:category).where(categories: { name: "Electronics" })
```

### Eager Loading (N+1 Prevention)

**Problem (N+1 queries):**

```ruby
products = Product.all
products.each do |product|
  puts product.category.name  # Fires query for EACH product!
end
# Fires: 1 query for products + N queries for categories = N+1 queries
```

**Solution (eager loading):**

```ruby
products = Product.includes(:category).all
products.each do |product|
  puts product.category.name  # Uses preloaded data
end
# Fires: 1 query for products + 1 query for categories = 2 queries total
```

Methods:
- `includes`: Preload associations (two queries)
- `eager_load`: Preload with LEFT OUTER JOIN (one query)
- `preload`: Always uses separate queries

### Scopes

Reusable query fragments:

```ruby
class Product < ApplicationRecord
  scope :available, -> { where(available: true) }
  scope :cheap, -> { where("price < ?", 10) }
  scope :expensive, -> { where("price > ?", 100) }
  scope :in_category, ->(category) { where(category: category) }
end

# Usage:
Product.available.cheap
Product.expensive.in_category("Electronics")
```

### Method Chaining

Build complex queries incrementally:

```ruby
products = Product.all

products = products.where(available: true) if params[:available]
products = products.where(category: params[:category]) if params[:category]
products = products.where("price < ?", params[:max_price]) if params[:max_price]

products = products.order(params[:sort] || :created_at)
products = products.page(params[:page])

products  # Execute query when enumerated
```

## Validations

Ensure data integrity before saving.

### Common Validations

```ruby
class Product < ApplicationRecord
  validates :name, presence: true
  validates :price, numericality: { greater_than: 0 }
  validates :sku, uniqueness: true
  validates :email, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :description, length: { minimum: 10, maximum: 500 }
  validates :category, presence: true
  validates :terms, acceptance: true
end
```

### Conditional Validations

```ruby
validates :coupon_code, presence: true, if: :coupon_used?
validates :shipping_address, presence: true, unless: :pickup?
```

### Custom Validations

```ruby
validate :price_must_be_reasonable

private

def price_must_be_reasonable
  if price.present? && price > 10000
    errors.add(:price, "is unreasonably high")
  end
end
```

### Validation Helpers

```ruby
# Inline validation
product.valid?  # => false
product.errors.full_messages  # => ["Name can't be blank", "Price must be greater than 0"]

# Save with validation
product.save  # => false (doesn't save if invalid)
product.save!  # => raises ActiveRecord::RecordInvalid

# Skip validation (dangerous!)
product.save(validate: false)
```

## Callbacks

Run code at specific points in an object's lifecycle.

### Common Callbacks

```ruby
class Product < ApplicationRecord
  before_validation :normalize_name
  after_validation :log_errors
  before_save :calculate_discount
  after_save :clear_cache
  before_create :generate_sku
  after_create :notify_team
  before_update :track_price_changes
  after_update :reindex_search
  before_destroy :check_orders
  after_destroy :cleanup_images
  after_commit :sync_to_external_system

  private

  def normalize_name
    self.name = name.strip.titleize if name.present?
  end

  def generate_sku
    self.sku = SecureRandom.hex(8).upcase
  end

  def check_orders
    throw :abort if orders.exists?
  end
end
```

### Callback Order

1. `before_validation`
2. `after_validation`
3. `before_save`
4. `before_create` / `before_update`
5. Database operation
6. `after_create` / `after_update`
7. `after_save`
8. `after_commit` / `after_rollback`

### Skipping Callbacks

```ruby
product.update_columns(price: 9.99)  # Skips callbacks and validations
product.update_attribute(:price, 9.99)  # Skips validations only
product.increment!(:view_count)  # Skips validations, runs callbacks
```

## Advanced Patterns

### Single Table Inheritance (STI)

```ruby
class Vehicle < ApplicationRecord
  # type column required
end

class Car < Vehicle
end

class Truck < Vehicle
end

# Queries:
Car.all  # WHERE type = 'Car'
Vehicle.all  # All vehicles
```

### Enums

```ruby
class Order < ApplicationRecord
  enum status: [:pending, :processing, :shipped, :delivered, :cancelled]
end

order = Order.create!(status: :pending)
order.pending?  # => true
order.processing!  # Updates status to processing
order.processing?  # => true

Order.pending  # WHERE status = 0
Order.not_pending  # WHERE status != 0
```

### Composite Primary Keys (Rails 8)

```ruby
class BookOrder < ApplicationRecord
  self.primary_key = [:book_id, :order_id]

  belongs_to :book
  belongs_to :order
end

# Find by composite key
BookOrder.find([book_id, order_id])
```

## Database-Specific Features

### PostgreSQL

```ruby
# JSON columns
add_column :products, :metadata, :jsonb, default: {}

product.metadata = { color: "red", size: "large" }
Product.where("metadata->>'color' = ?", "red")

# Arrays
add_column :products, :tags, :string, array: true, default: []

product.tags = ["electronics", "sale"]
Product.where("? = ANY(tags)", "electronics")

# Full-text search
Product.where("to_tsvector('english', name) @@ to_tsquery(?)", "widget")
```

### MySQL-Specific

```ruby
# Case-insensitive queries (default)
Product.where("name = ?", "Widget")  # Matches "widget", "WIDGET"

# JSON columns (MySQL 5.7+)
add_column :products, :settings, :json
```

## Best Practices

1. **Use scopes** for reusable queries
2. **Eager load** to prevent N+1 queries
3. **Add indexes** for foreign keys and frequently queried columns
4. **Validate** before saving to maintain data integrity
5. **Use transactions** for multi-step operations
6. **Limit callbacks** - keep them simple and focused
7. **Use migrations** - never modify schema directly
8. **Test validations** and associations
9. **Profile queries** - use `explain` to optimize
10. **Use database constraints** (NOT NULL, UNIQUE, FOREIGN KEY)

## Further Reading

For deeper exploration:

- **`references/migrations.md`**: Complete migration guide with patterns
- **`references/associations.md`**: Advanced association techniques
- **`references/query-optimization.md`**: Performance tuning and N+1 prevention

For code examples:

- **`examples/active-record-patterns.rb`**: Common Active Record patterns

## Summary

Active Record provides:
- **Models** that represent database tables
- **Migrations** for schema changes
- **Associations** for relationships
- **Validations** for data integrity
- **Queries** without writing SQL
- **Callbacks** for lifecycle hooks
- **Conventions** that eliminate configuration

Master Active Record, and you master data in Rails.
