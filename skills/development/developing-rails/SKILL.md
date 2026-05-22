---
name: developing-rails
description: Use when working with Rails projects, ActiveRecord models, controllers, routes, or Rails-specific patterns. Covers naming conventions, models, migrations, service objects, and testing with RSpec.
---

# Rails Development

Follow these conventions when working with Rails. Rails conventions take precedence over conflicting ruby patterns.

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Models | singular PascalCase | `User`, `OrderItem` |
| Tables | plural snake_case | `users`, `order_items` |
| Controllers | plural PascalCase | `UsersController` |
| Foreign keys | singular_id | `user_id` |
| Join tables | alphabetical | `categories_products` |

## File Locations

| Type | Location |
|------|----------|
| Models | `app/models/` |
| Controllers | `app/controllers/` |
| Views | `app/views/{resource}/` |
| Services | `app/services/` |
| Jobs | `app/jobs/` |
| Mailers | `app/mailers/` |
| Migrations | `db/migrate/` |

## Models

```ruby
class User < ApplicationRecord
  belongs_to :organization
  has_many :posts, dependent: :destroy

  validates :email, presence: true, uniqueness: true

  scope :active, -> { where(active: true) }

  def full_name
    "#{first_name} #{last_name}"
  end
end
```

### Queries

```ruby
User.find(1)                    # Raises if not found
User.find_by(email: "a@b.com")  # Returns nil if not found
User.includes(:posts, :profile) # Eager load to prevent N+1
User.find_each(batch_size: 1000) { |u| process(u) }
```

## Controllers

```ruby
class UsersController < ApplicationController
  before_action :set_user, only: [:show, :edit, :update, :destroy]

  def create
    @user = User.new(user_params)
    if @user.save
      redirect_to @user, notice: "User created."
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def set_user
    @user = User.find(params[:id])
  end

  def user_params
    params.require(:user).permit(:name, :email)
  end
end
```

## Routes

```ruby
Rails.application.routes.draw do
  resources :users
  resources :posts, only: [:index, :show]

  resources :users do
    resources :posts, shallow: true
  end

  namespace :api do
    namespace :v1 do
      resources :users, only: [:index, :show, :create]
    end
  end

  root "home#index"
end
```

## Migrations

```ruby
class CreateUsers < ActiveRecord::Migration[7.1]
  def change
    create_table :users do |t|
      t.string :email, null: false
      t.string :name, null: false
      t.references :organization, foreign_key: true
      t.timestamps
    end
    add_index :users, :email, unique: true
  end
end
```

## Service Objects

Use Result pattern for service objects:

```ruby
class CreateUser
  def initialize(user_repository: User, mailer: UserMailer)
    @user_repository = user_repository
    @mailer = mailer
  end

  def call(params)
    user = @user_repository.new(params)
    if user.save
      @mailer.welcome(user).deliver_later
      Result.success(user)
    else
      Result.failure(user.errors.full_messages)
    end
  end
end
```

## Background Jobs

```ruby
class SendWelcomeEmailJob < ApplicationJob
  queue_as :default
  retry_on Net::SMTPError, wait: 5.minutes, attempts: 3

  def perform(user_id)
    user = User.find(user_id)
    UserMailer.welcome(user).deliver_now
  end
end

SendWelcomeEmailJob.perform_later(user.id)
```

## Testing

```ruby
RSpec.describe User, type: :model do
  describe "validations" do
    it { is_expected.to validate_presence_of(:email) }
  end

  describe "#full_name" do
    let(:user) { build(:user, first_name: "John", last_name: "Doe") }
    it { expect(user.full_name).to eq("John Doe") }
  end
end

RSpec.describe "Users", type: :request do
  describe "POST /users" do
    let(:valid_params) { { user: { name: "John", email: "john@example.com" } } }

    it "creates a user" do
      expect { post users_path, params: valid_params }.to change(User, :count).by(1)
    end
  end
end
```

## Requirements

1. Keep controllers thin—extract business logic to services
2. Use strong parameters for all user input
3. Do not use callbacks for business logic; use services instead
4. Use `includes`, `preload`, or `eager_load` to prevent N+1 queries
5. Define scopes in models for reusable queries
6. Use background jobs for emails, external APIs, and slow operations
7. Follow REST conventions; custom actions are rare
8. Prefer service objects over concerns for business logic
