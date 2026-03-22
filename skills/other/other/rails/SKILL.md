---
name: rails
description: |
  Rails 7+ framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Rails projects, or when the user mentions Ruby on Rails.
  Provides ActiveRecord, Hotwire/Turbo, Action Cable, and convention-over-configuration guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: ruby
  extensions: ".rb,.erb"
---

# Ruby on Rails Guide

> Applies to: Rails 7+, Ruby 3.2+, Hotwire/Turbo, ActiveRecord, Action Cable

## Core Principles

1. **Convention over Configuration**: Follow Rails conventions -- naming, directory structure, RESTful routes
2. **Fat Models, Thin Controllers**: Business logic in models and service objects, controllers handle request/response only
3. **DRY**: Use concerns, partials, helpers, and shared services to avoid repetition
4. **RESTful by Default**: Design resources around standard CRUD actions before adding custom routes
5. **Security by Default**: CSRF, XSS protection, strong parameters, and parameterized queries are built in

## When to Use Rails

**Good fit:** Full-stack web apps, MVPs, CMS, e-commerce, SaaS, Hotwire/Turbo SPA-like UX, API backends.

**Consider alternatives:** Minimal microservices (Sinatra, Hanami), heavy real-time streaming, strict type safety needs (Rust, Go).

## Project Structure

```
myapp/
├── app/
│   ├── controllers/
│   │   ├── application_controller.rb
│   │   ├── concerns/              # Controller concerns (auth, pagination)
│   │   └── api/
│   │       └── v1/                # Versioned API controllers
│   ├── models/
│   │   ├── application_record.rb
│   │   └── concerns/              # Model concerns (searchable, sluggable)
│   ├── views/
│   │   ├── layouts/               # Application layouts
│   │   │   └── application.html.erb
│   │   ├── shared/                # Shared partials (_navbar, _footer)
│   │   └── posts/                 # Resource-specific views
│   ├── helpers/                   # View helpers
│   ├── jobs/                      # ActiveJob classes
│   ├── mailers/                   # Action Mailer classes
│   ├── channels/                  # Action Cable channels
│   └── services/                  # Service objects (custom directory)
├── config/
│   ├── routes.rb                  # Route definitions
│   ├── database.yml               # Database configuration
│   ├── environments/              # Per-environment settings
│   └── initializers/              # Boot-time configuration
├── db/
│   ├── migrate/                   # Migration files
│   ├── schema.rb                  # Current schema snapshot
│   └── seeds.rb                   # Seed data
├── lib/
│   └── tasks/                     # Custom Rake tasks
├── test/                          # Minitest (default) or spec/ for RSpec
│   ├── models/
│   ├── controllers/
│   ├── integration/
│   └── system/
├── Gemfile
└── Gemfile.lock
```

- Place business logic in `app/services/`; use concerns for shared model/controller behavior
- Namespace API controllers under `Api::V1`; keep shared partials in `views/shared/`

## Guardrails

### Controllers

- Keep controllers under 100 lines total
- Limit each action to 10 lines (delegate to services for complex logic)
- Always use `before_action` for authentication and resource loading
- Always use strong parameters via private `*_params` methods
- Return `status: :unprocessable_entity` for failed form submissions
- Use `status: :see_other` (303) for `redirect_to` after DELETE
- Use `respond_to` blocks when serving multiple formats

### Models

- Always add validations for required fields and constraints
- Always add `dependent:` option on `has_many`/`has_one` associations
- Use `scope` for reusable queries (never build queries in controllers)
- Use `enum` with explicit integer or string mappings
- Use `before_validation` for data normalization (downcase, strip)
- Avoid heavy logic in callbacks -- prefer service objects for side effects
- Always define `counter_cache: true` for belongs_to when parent displays counts

### Migrations

- Always add `null: false` for required columns
- Always add database indexes for foreign keys and frequently queried columns
- Always add unique indexes where uniqueness is required
- Use `references` with `foreign_key: true` for associations
- Set sensible defaults with `default:` for boolean and status columns
- Include both `up` and `down` methods for irreversible migrations
- Never modify a migration after it has been applied to production

### Security

- Strong parameters: never use `params.permit!` (permit all)
- CSRF protection: enabled by default, skip only for API controllers with token auth
- SQL injection: use ActiveRecord query methods, never string interpolation in queries
- XSS: ERB auto-escapes by default; never use `raw` or `html_safe` with user data
- Mass assignment: only permit explicitly needed attributes
- Secrets: use `Rails.application.credentials` or environment variables
- Set `force_ssl` in production
- Use `content_security_policy` configuration in production

### Performance

- Always use `includes` (or `preload`/`eager_load`) to prevent N+1 queries
- Add database indexes for all foreign keys and commonly filtered columns
- Use `counter_cache` for association counts displayed in views
- Use pagination for all list endpoints (Kaminari or Pagy)
- Use fragment caching (`cache @record do`) for expensive view rendering
- Use background jobs (ActiveJob + Sidekiq) for slow operations
- Use `find_each` instead of `each` when iterating over large datasets

## MVC Conventions

### Models

```ruby
# app/models/post.rb
class Post < ApplicationRecord
  # 1. Associations
  belongs_to :user
  belongs_to :category, optional: true
  has_many :comments, dependent: :destroy
  has_many :taggings, dependent: :destroy
  has_many :tags, through: :taggings
  has_one_attached :featured_image

  # 2. Validations
  validates :title, presence: true, length: { maximum: 255 }
  validates :body, presence: true

  # 3. Enums
  enum :status, { draft: 0, published: 1, archived: 2 }

  # 4. Scopes
  scope :published, -> { where(status: :published) }
  scope :recent, -> { order(created_at: :desc) }
  scope :by_category, ->(cat) { where(category: cat) }
  scope :search, ->(q) {
    where("title ILIKE :q OR body ILIKE :q", q: "%#{sanitize_sql_like(q)}%")
  }

  # 5. Callbacks (keep minimal)
  before_validation :normalize_title

  # 6. Instance methods
  def publish!
    update!(status: :published, published_at: Time.current)
  end

  private

  def normalize_title
    self.title = title&.strip
  end
end
```

**Model ordering convention**: Associations, validations, enums, scopes, callbacks, class methods, instance methods, private methods.

### Controllers

```ruby
# app/controllers/posts_controller.rb
class PostsController < ApplicationController
  before_action :authenticate_user!, except: [:index, :show]
  before_action :set_post, only: [:show, :edit, :update, :destroy]
  before_action :authorize_post!, only: [:edit, :update, :destroy]

  def index
    @posts = Post.published
                 .includes(:user, :category)
                 .recent
                 .page(params[:page])
                 .per(20)
  end

  def show; end

  def new
    @post = current_user.posts.build
  end

  def create
    @post = current_user.posts.build(post_params)
    if @post.save
      redirect_to @post, notice: "Post created."
    else
      render :new, status: :unprocessable_entity
    end
  end

  def edit; end

  def update
    if @post.update(post_params)
      redirect_to @post, notice: "Post updated."
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def destroy
    @post.destroy
    redirect_to posts_url, notice: "Post deleted.", status: :see_other
  end

  private

  def set_post
    @post = Post.find(params[:id])
  end

  def authorize_post!
    redirect_to posts_url, alert: "Not authorized." unless @post.user == current_user
  end

  def post_params
    params.require(:post).permit(:title, :body, :category_id, :status, :featured_image, tag_ids: [])
  end
end
```

### Views and Partials

- Use `_form.html.erb` partial shared between `new` and `edit`
- Use collection rendering: `render @posts` (auto-maps to `_post.html.erb`)
- Use locals: `render partial: "post", locals: { post: @post }`
- Use `content_for :title` for page-specific titles
- Use helpers for complex view logic (not inline ERB conditionals)

## Routing

```ruby
# config/routes.rb
Rails.application.routes.draw do
  root "home#index"

  # Authentication
  get "login", to: "sessions#new"
  post "login", to: "sessions#create"
  delete "logout", to: "sessions#destroy"

  # RESTful resources
  resources :posts do
    resources :comments, only: [:create, :destroy]
    member do
      post :publish
      post :unpublish
    end
  end

  resources :categories, only: [:index, :show] do
    resources :posts, only: [:index]
  end

  # Admin namespace
  namespace :admin do
    root "dashboard#index"
    resources :users
    resources :posts
  end

  # API namespace
  namespace :api do
    namespace :v1 do
      resources :posts, only: [:index, :show, :create, :update, :destroy]
    end
  end

  # Health check
  get "health", to: "health#show"
end
```

**Route conventions:**
- Use `resources` for standard CRUD (generates 7 RESTful routes)
- Use `only:` or `except:` to limit generated routes
- Use `member` for actions on a specific record, `collection` for actions on the set
- Nest resources only one level deep; use `shallow: true` for deeper nesting
- Namespace admin and API routes separately

## Migrations

```ruby
# db/migrate/20240115000000_create_posts.rb
class CreatePosts < ActiveRecord::Migration[7.1]
  def change
    create_table :posts do |t|
      t.references :user, null: false, foreign_key: true
      t.references :category, foreign_key: true
      t.string :title, null: false
      t.text :body, null: false
      t.integer :status, default: 0, null: false
      t.datetime :published_at
      t.integer :comments_count, default: 0, null: false

      t.timestamps
    end

    add_index :posts, [:user_id, :status]
    add_index :posts, :published_at
  end
end
```

- Use `t.references` for foreign keys (adds index automatically)
- Use `t.timestamps` for `created_at` and `updated_at`
- Add composite indexes for common query patterns
- Use `comments_count` with `counter_cache: true` on the association

## Service Objects

```ruby
# app/services/application_service.rb
class ApplicationService
  def self.call(...)
    new(...).call
  end
end

# app/services/posts/publish_service.rb
module Posts
  class PublishService < ApplicationService
    def initialize(post:, user:)
      @post = post
      @user = user
    end

    def call
      return ServiceResult.failure(["Not authorized"]) unless @user == @post.user

      ActiveRecord::Base.transaction do
        @post.update!(status: :published, published_at: Time.current)
        notify_subscribers
      end

      ServiceResult.success(@post)
    rescue ActiveRecord::RecordInvalid => e
      ServiceResult.failure(e.record.errors.full_messages)
    end

    private

    def notify_subscribers
      PostMailer.published(@post).deliver_later
    end
  end
end
```

- Use `self.call(...)` class method pattern for clean invocation
- Wrap multi-step operations in `ActiveRecord::Base.transaction`
- Return a result object (success/failure) instead of raising
- Namespace services by domain: `Posts::PublishService`, `Users::CreateService`

## Rails Commands

```bash
# Application
rails new myapp --database=postgresql --css=tailwind
rails new myapp --api                    # API-only mode
rails server                             # Start dev server
rails console                            # Interactive console
rails routes                             # List all routes

# Generators
rails generate model User name:string email:string
rails generate controller Posts index show new create
rails generate scaffold Article title:string body:text
rails generate migration AddStatusToPosts status:integer

# Database
rails db:create                          # Create database
rails db:migrate                         # Run pending migrations
rails db:rollback                        # Undo last migration
rails db:seed                            # Run seeds.rb
rails db:reset                           # Drop, create, migrate, seed

# Testing
rails test                               # Run all tests
rails test:models                        # Model tests only
rails test:system                        # System tests only

# Assets and dependencies
bundle install                           # Install gems
rails assets:precompile                  # Compile assets for production
```

## Testing

### Minitest (Default)

```ruby
# test/models/post_test.rb
require "test_helper"

class PostTest < ActiveSupport::TestCase
  def setup
    @post = posts(:first_post)
  end

  test "valid post" do
    assert @post.valid?
  end

  test "invalid without title" do
    @post.title = nil
    assert_not @post.valid?
    assert_includes @post.errors[:title], "can't be blank"
  end

  test "publish! sets status and timestamp" do
    @post.publish!
    assert @post.published?
    assert_not_nil @post.published_at
  end
end
```

### Testing Standards

- Use fixtures (default) or `factory_bot` for test data
- Test validations, associations, scopes, and instance methods on models
- Test authentication, authorization, and response codes on controllers
- Use system tests (Capybara) for critical user flows
- Coverage target: >80% for models and services, >60% overall
- Test names describe behavior: `test "user cannot edit others' posts"`
- See [references/patterns.md](references/patterns.md) for controller and system test examples

## Dependencies

**Core**: `rails ~> 7.1`, `pg`, `puma`, `redis`, `turbo-rails`, `stimulus-rails`, `importmap-rails`

**Auth**: `bcrypt` (has_secure_password)

**Background**: `sidekiq`

**Pagination**: `kaminari` or `pagy`

**Dev/Test**: `debug`, `capybara`, `selenium-webdriver`, `web-console`, `rack-mini-profiler`

**Optional**: `rspec-rails`, `factory_bot_rails`, `faker`, `shoulda-matchers`, `webmock`

## Best Practices

### Do

- Follow RESTful conventions for routes and controllers
- Use `includes`/`preload` on every association accessed in views
- Extract business logic to service objects
- Use scopes for all reusable query patterns
- Use `find_each` for batch operations on large datasets
- Use background jobs for email, notifications, and heavy processing
- Use fragment caching for expensive view partials
- Keep secrets in credentials or environment variables

### Don't

- Put business logic in controllers or views
- Use `params.permit!` (mass-assignment vulnerability)
- Use string interpolation in SQL queries
- Skip database indexes on foreign keys
- Use `Model.all` without pagination or limits
- Modify migrations after they have been applied to production
- Use `raw`/`html_safe` with user-provided data
- Rely heavily on callbacks for business logic (use services)

## Advanced Topics

For detailed code examples and advanced patterns, see:

- [references/patterns.md](references/patterns.md) -- ActiveRecord advanced patterns, Hotwire/Turbo, Action Cable, ActiveJob, API mode, deployment, and testing strategies

## External References

- [Rails Guides](https://guides.rubyonrails.org/)
- [Rails API Documentation](https://api.rubyonrails.org/)
- [Hotwire Documentation](https://hotwired.dev/)
- [Rails Tutorial](https://www.railstutorial.org/)
