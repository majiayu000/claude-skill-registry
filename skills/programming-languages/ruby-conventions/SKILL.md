---
name: ruby-conventions
description: |
  Ruby and Rails best practices for services, testing, and architecture. Use when:
  - Writing or reviewing Ruby/Rails code
  - Designing service objects or organizing business logic
  - Setting up RSpec tests with FactoryBot
  - Building APIs with JSON serialization
  - Optimizing Rails performance (N+1, caching)
  Keywords: Ruby, Rails, RSpec, FactoryBot, service object, strong params,
  N+1 query, Sidekiq, RuboCop, Thor CLI
---

# Ruby Conventions

Service objects, strong params, behavior-focused tests.

## Architecture

**Service objects for business logic:**
```ruby
# app/services/user_registration_service.rb
class UserRegistrationService
  def initialize(user_params:, mailer: UserMailer)
    @user_params = user_params
    @mailer = mailer
  end

  def call
    user = User.create!(@user_params)
    @mailer.welcome(user).deliver_later
    user
  end
end
```

**Thin controllers:**
```ruby
def create
  user = UserRegistrationService.new(user_params: user_params).call
  render json: UserSerializer.new(user), status: :created
rescue ActiveRecord::RecordInvalid => e
  render json: { errors: e.record.errors }, status: :unprocessable_entity
end
```

## Strong Parameters

**Always use strong params. Never mass-assign directly:**
```ruby
# Good
def user_params
  params.require(:user).permit(:email, :name, :password)
end

# Never
User.create(params[:user])  # SQL injection risk
```

## Query Safety

**Always parameterize queries:**
```ruby
# Good
User.where(email: email)
User.where("email = ?", email)

# Never
User.where("email = '#{email}'")  # SQL injection
```

**Prevent N+1 queries:**
```ruby
# Good
User.includes(:posts).each { |u| u.posts.count }

# Bad (N+1)
User.all.each { |u| u.posts.count }
```

## Testing with RSpec

```ruby
RSpec.describe UserRegistrationService do
  describe "#call" do
    it "creates active user with welcome email" do
      mailer = instance_double(UserMailer)
      allow(mailer).to receive(:welcome).and_return(double(deliver_later: true))

      service = described_class.new(
        user_params: { email: "test@example.com", name: "Test" },
        mailer: mailer
      )

      user = service.call

      expect(user).to be_persisted
      expect(user.email).to eq("test@example.com")
      expect(mailer).to have_received(:welcome).with(user)
    end
  end
end
```

**Use FactoryBot, not fixtures:**
```ruby
FactoryBot.define do
  factory :user do
    email { Faker::Internet.email }
    name { Faker::Name.name }
  end
end

let(:user) { create(:user) }
```

## API Design

```ruby
# Consistent serialization
class UserSerializer
  include JSONAPI::Serializer
  attributes :id, :email, :name, :created_at
end

# Versioned routes
namespace :api do
  namespace :v1 do
    resources :users
  end
end
```

## Language Patterns

```ruby
# Keyword arguments for 2+ params
def send_email(to:, subject:, body:)
  ...
end

# Safe navigation
user&.profile&.avatar_url

# Frozen strings (file header)
# frozen_string_literal: true
```

## Anti-Patterns

- Fat models (business logic in ActiveRecord)
- Business logic in controllers
- Fixtures instead of factories
- Testing implementation (mocking internals)
- String interpolation in SQL
- N+1 queries without includes
- Synchronous email in request cycle

## References

- [rails-performance.md](references/rails-performance.md) - Caching, background jobs, profiling
