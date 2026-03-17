---
name: rails-models
description: ActiveRecord patterns, migrations, validations, callbacks, associations
version: 1.0.0
rails_version: ">= 7.0"
tags:
  - activerecord
  - models
  - database
  - orm
---

# Rails Models (ActiveRecord)

## Quick Reference

| Pattern | Example |
|---------|---------|
| **Model Generation** | `rails g model User name:string email:string` |
| **Migration** | `rails g migration AddAgeToUsers age:integer` |
| **Validation** | `validates :email, presence: true, uniqueness: true` |
| **Association** | `has_many :posts, dependent: :destroy` |
| **Callback** | `before_save :normalize_email` |
| **Scope** | `scope :active, -> { where(active: true) }` |
| **Query** | `User.where(active: true).order(created_at: :desc)` |

## Model Definition

```ruby
class User < ApplicationRecord
  # Constants
  ROLES = %w[admin user guest].freeze
  
  # Associations
  has_many :posts, dependent: :destroy
  has_many :comments
  belongs_to :organization, optional: true
  
  # Validations
  validates :email, presence: true, uniqueness: true
  validates :name, presence: true, length: { minimum: 2 }
  validates :role, inclusion: { in: ROLES }
  
  # Callbacks
  before_save :normalize_email
  after_create :send_welcome_email
  
  # Scopes
  scope :active, -> { where(active: true) }
  scope :recent, -> { order(created_at: :desc) }
  
  # Class methods
  def self.search(query)
    where("name ILIKE ?", "%#{query}%")
  end
  
  # Instance methods
  def full_name
    "#{first_name} #{last_name}"
  end
  
  private
  
  def normalize_email
    self.email = email.downcase.strip
  end
end
```

## Migrations

### Creating Tables

```ruby
class CreateUsers < ActiveRecord::Migration[7.0]
  def change
    create_table :users do |t|
      t.string :name, null: false
      t.string :email, null: false
      t.boolean :active, default: true
      t.integer :role, default: 0
      t.references :organization, foreign_key: true
      
      t.timestamps
    end
    
    add_index :users, :email, unique: true
  end
end
```

### Modifying Tables

```ruby
class AddFieldsToUsers < ActiveRecord::Migration[7.0]
  def change
    add_column :users, :bio, :text
    add_column :users, :avatar_url, :string
    add_reference :users, :manager, foreign_key: { to_table: :users }
    
    change_column_null :users, :email, false
    change_column_default :users, :active, from: nil, to: true
  end
end
```

## Validations

```ruby
class User < ApplicationRecord
  # Presence
  validates :email, presence: true
  
  # Uniqueness
  validates :email, uniqueness: { case_sensitive: false }
  validates :username, uniqueness: { scope: :organization_id }
  
  # Format
  validates :email, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :phone, format: { with: /\A\d{10}\z/ }
  
  # Length
  validates :name, length: { minimum: 2, maximum: 50 }
  validates :bio, length: { maximum: 500 }
  
  # Numericality
  validates :age, numericality: { greater_than: 0, less_than: 150 }
  
  # Inclusion/Exclusion
  validates :role, inclusion: { in: ROLES }
  validates :username, exclusion: { in: %w[admin root] }
  
  # Custom validation
  validate :email_domain_allowed
  
  private
  
  def email_domain_allowed
    return if email.blank?
    domain = email.split('@').last
    unless %w[example.com company.com].include?(domain)
      errors.add(:email, "must be from an allowed domain")
    end
  end
end
```

## Associations

```ruby
# One-to-Many
class Author < ApplicationRecord
  has_many :books, dependent: :destroy
  has_many :published_books, -> { where(published: true) }, class_name: 'Book'
end

class Book < ApplicationRecord
  belongs_to :author
end

# Many-to-Many (has_and_belongs_to_many)
class Student < ApplicationRecord
  has_and_belongs_to_many :courses
end

class Course < ApplicationRecord
  has_and_belongs_to_many :students
end

# Many-to-Many (has_many :through)
class Student < ApplicationRecord
  has_many :enrollments
  has_many :courses, through: :enrollments
end

class Enrollment < ApplicationRecord
  belongs_to :student
  belongs_to :course
end

class Course < ApplicationRecord
  has_many :enrollments
  has_many :students, through: :enrollments
end

# One-to-One
class User < ApplicationRecord
  has_one :profile, dependent: :destroy
end

class Profile < ApplicationRecord
  belongs_to :user
end

# Polymorphic
class Comment < ApplicationRecord
  belongs_to :commentable, polymorphic: true
end

class Post < ApplicationRecord
  has_many :comments, as: :commentable
end

class Photo < ApplicationRecord
  has_many :comments, as: :commentable
end
```

## Callbacks

```ruby
class User < ApplicationRecord
  # Order of execution:
  before_validation :normalize_data
  after_validation :log_validation_errors
  
  before_save :encrypt_password
  around_save :log_save_time
  after_save :clear_cache
  
  before_create :set_default_role
  after_create :send_welcome_email
  
  before_update :check_changes
  after_update :notify_changes
  
  before_destroy :check_dependencies
  after_destroy :cleanup_files
  
  private
  
  def normalize_data
    self.email = email.downcase if email.present?
  end
  
  def around_save
    start_time = Time.current
    yield
    Rails.logger.info "Save took #{Time.current - start_time}s"
  end
end
```

## Scopes and Queries

```ruby
class Post < ApplicationRecord
  # Scopes
  scope :published, -> { where(published: true) }
  scope :recent, -> { order(created_at: :desc) }
  scope :by_author, ->(author_id) { where(author_id: author_id) }
  scope :created_between, ->(start_date, end_date) {
    where(created_at: start_date..end_date)
  }
  
  # Chaining scopes
  # Post.published.recent.limit(10)
end

# Query methods
Post.where(published: true)
Post.where("views > ?", 100)
Post.where(author_id: [1, 2, 3])
Post.where.not(category: 'draft')

# Ordering
Post.order(created_at: :desc)
Post.order(views: :desc, created_at: :asc)

# Limiting
Post.limit(10)
Post.offset(20).limit(10)

# Joins
Post.joins(:author)
Post.joins(:author, :comments)
Post.left_joins(:comments)

# Includes (eager loading)
Post.includes(:author, :comments)
Post.includes(author: :profile)

# Selecting specific fields
Post.select(:id, :title, :created_at)
Post.pluck(:title)
Post.pluck(:id, :title)

# Aggregations
Post.count
Post.average(:views)
Post.maximum(:views)
Post.minimum(:views)
Post.sum(:views)

# Group
Post.group(:category).count
Post.group(:author_id).average(:views)
```

## Enums

```ruby
class Post < ApplicationRecord
  enum status: {
    draft: 0,
    published: 1,
    archived: 2
  }
  
  # Or with prefix/suffix
  enum visibility: {
    public: 0,
    private: 1
  }, _prefix: :visibility
  
  # Usage:
  # post.draft!
  # post.published?
  # Post.published
  # post.visibility_public!
end
```

## Model Concerns

```ruby
# app/models/concerns/taggable.rb
module Taggable
  extend ActiveSupport::Concern
  
  included do
    has_many :taggings, as: :taggable
    has_many :tags, through: :taggings
  end
  
  class_methods do
    def tagged_with(tag_name)
      joins(:tags).where(tags: { name: tag_name })
    end
  end
  
  def tag_list
    tags.pluck(:name).join(', ')
  end
end

# Usage in model
class Post < ApplicationRecord
  include Taggable
end
```

## Best Practices

1. **Fat models, skinny controllers** - Business logic belongs in models
2. **Use scopes** for common queries
3. **Validate at database level** with constraints when possible
4. **Use indexes** for frequently queried columns
5. **Eager load associations** to avoid N+1 queries
6. **Use concerns** to share behavior across models
7. **Keep callbacks simple** - avoid complex logic
8. **Use transactions** for multi-step operations
9. **Avoid callbacks for cross-cutting concerns** - use service objects instead

## Common Pitfalls

- **N+1 queries**: Use `includes`, `preload`, or `eager_load`
- **Callback hell**: Keep callbacks simple, use service objects for complex logic
- **Mass assignment vulnerabilities**: Use strong parameters in controllers
- **Missing indexes**: Add indexes for foreign keys and frequently queried columns
- **Ignoring database constraints**: Add NOT NULL, unique constraints in migrations

## References

- [Rails Guides - Active Record](https://guides.rubyonrails.org/active_record_basics.html)
- [Rails Guides - Validations](https://guides.rubyonrails.org/active_record_validations.html)
- [Rails Guides - Associations](https://guides.rubyonrails.org/association_basics.html)
- [Rails Guides - Migrations](https://guides.rubyonrails.org/active_record_migrations.html)
- [Rails Guides - Queries](https://guides.rubyonrails.org/active_record_querying.html)
