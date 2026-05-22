---
name: rails-active-record-patterns
description: Use when active Record patterns including models, associations, queries, validations, and callbacks.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# Rails Active Record Patterns

Master Active Record patterns for building robust Rails models with proper
associations, validations, scopes, and query optimization.

## Overview

Active Record is Rails' Object-Relational Mapping (ORM) layer that connects
model classes to database tables. It implements the Active Record pattern,
where each object instance represents a row in the database and includes both
data and behavior.

## Installation and Setup

### Creating Models

```bash
# Generate a model with migrations
rails generate model User name:string email:string:uniq

# Generate model with associations
rails generate model Post title:string body:text user:references

# Run migrations
rails db:migrate
```

### Database Configuration

```yaml
# config/database.yml
default: &default
  adapter: postgresql
  encoding: unicode
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>

development:
  <<: *default
  database: myapp_development

test:
  <<: *default
  database: myapp_test

production:
  <<: *default
  database: myapp_production
  username: myapp
  password: <%= ENV['MYAPP_DATABASE_PASSWORD'] %>
```

## Core Patterns

### 1. Basic Model Definition

```ruby
# app/models/user.rb
class User < ApplicationRecord
  # Validations
  validates :email, presence: true, uniqueness: true,
    format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :name, presence: true, length: { minimum: 2, maximum: 50 }

  # Callbacks
  before_save :normalize_email
  after_create :send_welcome_email

  # Scopes
  scope :active, -> { where(active: true) }
  scope :recent, -> { order(created_at: :desc).limit(10) }

  private

  def normalize_email
    self.email = email.downcase.strip
  end

  def send_welcome_email
    UserMailer.welcome(self).deliver_later
  end
end
```

### 2. Associations

```ruby
# app/models/user.rb
class User < ApplicationRecord
  # One-to-many
  has_many :posts, dependent: :destroy
  has_many :comments, dependent: :destroy

  # Many-to-many through join table
  has_many :memberships, dependent: :destroy
  has_many :organizations, through: :memberships

  # Has-one
  has_one :profile, dependent: :destroy

  # Polymorphic association
  has_many :images, as: :imageable, dependent: :destroy
end

# app/models/post.rb
class Post < ApplicationRecord
  belongs_to :user
  has_many :comments, dependent: :destroy
  has_many :commenters, through: :comments, source: :user

  # Counter cache
  belongs_to :user, counter_cache: true
end

# app/models/organization.rb
class Organization < ApplicationRecord
  has_many :memberships, dependent: :destroy
  has_many :users, through: :memberships
end

# app/models/membership.rb
class Membership < ApplicationRecord
  belongs_to :user
  belongs_to :organization

  enum role: { member: 0, admin: 1, owner: 2 }
end
```

### 3. Advanced Queries

```ruby
# app/models/post.rb
class Post < ApplicationRecord
  # Scopes with arguments
  scope :by_author, ->(user_id) { where(user_id: user_id) }
  scope :published_after, ->(date) { where('published_at > ?', date) }
  scope :with_tag, ->(tag) { joins(:tags).where(tags: { name: tag }) }

  # Class methods for complex queries
  def self.popular(threshold = 100)
    where('views_count >= ?', threshold)
      .order(views_count: :desc)
  end

  def self.search(query)
    where('title ILIKE ? OR body ILIKE ?', "%#{query}%", "%#{query}%")
  end

  # Query with joins and includes
  def self.with_user_and_comments
    includes(:user, comments: :user)
      .order(created_at: :desc)
  end
end

# Usage
Post.published_after(1.week.ago)
  .by_author(current_user.id)
  .with_tag('rails')
  .popular(50)
```

### 4. Validations

```ruby
# app/models/user.rb
class User < ApplicationRecord
  # Presence validation
  validates :email, :name, presence: true

  # Uniqueness validation
  validates :email, uniqueness: { case_sensitive: false }

  # Format validation
  validates :username, format: {
    with: /\A[a-z0-9_]+\z/,
    message: "only allows lowercase letters, numbers, and underscores"
  }

  # Length validation
  validates :bio, length: { maximum: 500 }
  validates :password, length: { minimum: 8 }, if: :password_required?

  # Numericality validation
  validates :age, numericality: {
    only_integer: true,
    greater_than_or_equal_to: 18,
    less_than: 120
  }

  # Custom validation
  validate :email_domain_allowed

  private

  def email_domain_allowed
    return if email.blank?

    domain = email.split('@').last
    unless ALLOWED_DOMAINS.include?(domain)
      errors.add(:email, "domain #{domain} is not allowed")
    end
  end

  def password_required?
    new_record? || password.present?
  end
end
```

### 5. Callbacks

```ruby
# app/models/post.rb
class Post < ApplicationRecord
  # Before callbacks
  before_validation :normalize_title
  before_save :calculate_reading_time
  before_create :generate_slug

  # After callbacks
  after_create :notify_followers
  after_update :clear_cache, if: :saved_change_to_body?
  after_destroy :cleanup_attachments

  # Around callbacks
  around_save :log_save_time

  private

  def normalize_title
    self.title = title.strip.titleize if title.present?
  end

  def calculate_reading_time
    return unless body_changed?
    words = body.split.size
    self.reading_time = (words / 200.0).ceil
  end

  def generate_slug
    self.slug = title.parameterize
  end

  def notify_followers
    NotifyFollowersJob.perform_later(self)
  end

  def clear_cache
    Rails.cache.delete("post/#{id}")
  end

  def cleanup_attachments
    attachments.purge_later
  end

  def log_save_time
    start = Time.current
    yield
    duration = Time.current - start
    Rails.logger.info "Post #{id} saved in #{duration}s"
  end
end
```

### 6. Enum Patterns

```ruby
# app/models/post.rb
class Post < ApplicationRecord
  # Basic enum
  enum status: {
    draft: 0,
    published: 1,
    archived: 2
  }

  # Enum with prefix/suffix
  enum visibility: {
    public: 0,
    private: 1,
    unlisted: 2
  }, _prefix: :visibility

  # Multiple enums
  enum content_type: {
    article: 0,
    video: 1,
    podcast: 2
  }, _suffix: :content

  # Scopes automatically created
  # Post.draft, Post.published, Post.archived
  # Post.visibility_public, Post.visibility_private
  # Post.article_content, Post.video_content

  # Query methods
  # post.draft?, post.published?, post.archived?
  # post.visibility_public?, post.visibility_private?

  # State transitions
  def publish!
    published! if draft?
  end
end
```

### 7. Query Optimization

```ruby
# app/models/post.rb
class Post < ApplicationRecord
  # Eager loading to avoid N+1
  scope :with_associations, -> {
    includes(:user, :tags, comments: :user)
  }

  # Select specific columns
  scope :title_and_author, -> {
    select('posts.id, posts.title, users.name as author_name')
      .joins(:user)
  }

  # Batch processing
  def self.process_in_batches
    find_each(batch_size: 1000) do |post|
      post.process
    end
  end

  # Pluck for arrays
  def self.recent_titles
    order(created_at: :desc)
      .limit(10)
      .pluck(:title)
  end

  # Exists check (efficient)
  def self.has_recent_posts?(user_id)
    where(user_id: user_id)
      .where('created_at > ?', 1.day.ago)
      .exists?
  end

  # Count with joins
  def self.popular_authors
    joins(:user)
      .group('users.id', 'users.name')
      .select('users.id, users.name, COUNT(posts.id) as posts_count')
      .having('COUNT(posts.id) >= ?', 10)
      .order('posts_count DESC')
  end
end
```

### 8. Transactions

```ruby
# app/services/post_publisher.rb
class PostPublisher
  def self.publish(post, user)
    ActiveRecord::Base.transaction do
      post.update!(status: :published, published_at: Time.current)
      user.increment!(:posts_count)
      NotificationService.notify_followers(post)

      # If any operation fails, entire transaction is rolled back
    end
  rescue ActiveRecord::RecordInvalid => e
    Rails.logger.error "Failed to publish post: #{e.message}"
    false
  end

  # Nested transactions with savepoints
  def self.complex_operation(post)
    ActiveRecord::Base.transaction do
      post.update!(featured: true)

      ActiveRecord::Base.transaction(requires_new: true) do
        # This creates a savepoint
        post.tags.create!(name: 'featured')
      end
    end
  end
end
```

### 9. STI (Single Table Inheritance)

```ruby
# app/models/vehicle.rb
class Vehicle < ApplicationRecord
  validates :make, :model, presence: true

  def max_speed
    raise NotImplementedError
  end
end

# app/models/car.rb
class Car < Vehicle
  validates :doors, presence: true

  def max_speed
    120
  end
end

# app/models/motorcycle.rb
class Motorcycle < Vehicle
  validates :engine_size, presence: true

  def max_speed
    180
  end
end

# Usage
car = Car.create(make: 'Toyota', model: 'Camry', doors: 4)
car.type # => "Car"
Vehicle.all # Returns both cars and motorcycles
Car.all # Returns only cars
```

### 10. Concerns

```ruby
# app/models/concerns/sluggable.rb
module Sluggable
  extend ActiveSupport::Concern

  included do
    before_validation :generate_slug
    validates :slug, presence: true, uniqueness: true
  end

  class_methods do
    def find_by_slug(slug)
      find_by(slug: slug)
    end
  end

  private

  def generate_slug
    return if slug.present?
    base_slug = title.parameterize
    self.slug = unique_slug(base_slug)
  end

  def unique_slug(base_slug)
    slug_candidate = base_slug
    counter = 1

    while self.class.exists?(slug: slug_candidate)
      slug_candidate = "#{base_slug}-#{counter}"
      counter += 1
    end

    slug_candidate
  end
end

# app/models/post.rb
class Post < ApplicationRecord
  include Sluggable
end
```

## Best Practices

1. **Use scopes for reusable queries** - Keep query logic in the model
2. **Eager load associations** - Prevent N+1 queries with includes/preload
3. **Add database indexes** - Index foreign keys and frequently queried columns
4. **Use counter caches** - Optimize count queries for associations
5. **Validate at model level** - Ensure data integrity with validations
6. **Keep callbacks simple** - Extract complex logic to service objects
7. **Use transactions** - Ensure data consistency for multi-step operations
8. **Leverage concerns** - Share common behavior across models
9. **Use enums for state** - Type-safe state management with enums
10. **Write efficient queries** - Use select, pluck, and exists appropriately

## Common Pitfalls

1. **N+1 queries** - Forgetting to eager load associations
2. **Callback hell** - Too many callbacks making flow hard to follow
3. **Fat models** - Putting too much business logic in models
4. **Missing indexes** - Slow queries due to unindexed columns
5. **Unsafe updates** - Not using transactions for related operations
6. **Validation bypass** - Using update_attribute or save(validate: false)
7. **Memory bloat** - Loading all records instead of batching
8. **SQL injection** - Using string interpolation in where clauses
9. **Counter cache mismatches** - Manual updates breaking counter caches
10. **Ignoring database constraints** - Not adding DB-level validations

## When to Use

- Building data-backed Rails applications
- Implementing business logic tied to database models
- Creating REST APIs with Rails
- Developing CRUD interfaces
- Managing complex data relationships
- Building multi-tenant applications
- Creating admin interfaces with Active Admin
- Implementing soft deletes and audit trails
- Building reporting and analytics features
- Creating content management systems

## Resources

- [Active Record Basics Guide](https://guides.rubyonrails.org/active_record_basics.html)
- [Active Record Associations](https://guides.rubyonrails.org/association_basics.html)
- [Active Record Validations](https://guides.rubyonrails.org/active_record_validations.html)
- [Active Record Callbacks](https://guides.rubyonrails.org/active_record_callbacks.html)
- [Active Record Query Interface](https://guides.rubyonrails.org/active_record_querying.html)
- [Rails API Documentation](https://api.rubyonrails.org/)
- [The Rails Way Book](https://www.amazon.com/Rails-Way-Addison-Wesley-Professional-Ruby/dp/0321944275)
