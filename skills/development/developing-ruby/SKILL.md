---
name: developing-ruby
description: Use when working with .rb files, Ruby gems, or implementing Ruby features. Covers Ruby idioms, naming conventions, enumerable patterns, service objects, error handling, and RSpec testing.
---

# Ruby Development

Apply these patterns when working with Ruby code.

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes, Modules | PascalCase | `UserService` |
| Methods, variables | snake_case | `find_user_by_id` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES` |
| Predicates | snake_case? | `active?` |
| Dangerous methods | snake_case! | `save!` |
| Files | snake_case | `user_service.rb` |

## Project Structure

```
lib/
├── my_app.rb
└── my_app/
    ├── version.rb
    └── services/
spec/
├── spec_helper.rb
└── services/
Gemfile
```

## Idioms

### Blocks and Lambdas

```ruby
users.map { |u| u.name }
users.map(&:name)  # Symbol to proc

double = ->(n) { n * 2 }
double.call(5)
```

### Enumerable

```ruby
users.select(&:active?)
users.reject(&:banned?)
users.find { |u| u.id == 5 }
users.group_by(&:country)
orders.sum(&:total)

users.select(&:active?).sort_by(&:created_at).first(10).map(&:email)
```

### Safe Navigation

```ruby
user&.profile&.avatar_url
name = user.name || "Anonymous"

def expensive_calculation
  @expensive_calculation ||= perform_calculation
end
```

### Pattern Matching (Ruby 3+)

```ruby
case response
in { status: 200, body: }
  process(body)
in { status: 404 }
  handle_not_found
end
```

## Classes

```ruby
class User
  attr_reader :id, :email
  attr_accessor :name

  def initialize(id:, email:, name: nil)
    @id = id
    @email = email
    @name = name
  end

  def active?
    @status == :active
  end

  private

  def save!
    # Persist changes
  end
end
```

### Modules for Composition

```ruby
module Timestampable
  def touch
    @updated_at = Time.current
  end
end

class User
  include Timestampable
end
```

### Service Objects

```ruby
class CreateUser
  def initialize(user_repository:, email_service:)
    @user_repository = user_repository
    @email_service = email_service
  end

  def call(email:, name:)
    user = @user_repository.create(email: email, name: name)
    @email_service.send_welcome(user)
    user
  end
end
```

## Error Handling

```ruby
module MyApp
  class Error < StandardError; end
  class NotFoundError < Error; end
  class ValidationError < Error
    attr_reader :errors
    def initialize(errors)
      @errors = errors
      super("Validation failed: #{errors.join(', ')}")
    end
  end
end

raise MyApp::NotFoundError, "User not found"
```

### Result Objects

```ruby
class Result
  attr_reader :value, :error

  def self.success(value) = new(value: value)
  def self.failure(error) = new(error: error)

  def success? = @error.nil?
  def failure? = !success?

  def then
    return self if failure?
    yield(value)
  end
end
```

## Testing with RSpec

```ruby
RSpec.describe UserService do
  subject(:service) { described_class.new(repository: repository) }
  let(:repository) { instance_double(UserRepository) }
  let(:user) { build(:user, id: 1, name: "John") }

  describe "#find_by_id" do
    context "when user exists" do
      before { allow(repository).to receive(:find).with(1).and_return(user) }

      it "returns the user" do
        expect(service.find_by_id(1)).to eq(user)
      end
    end
  end
end
```

### Matchers

```ruby
expect(result).to eq(expected)
expect(user).to be_nil
expect(list).to include(item)
expect { user.activate! }.to change(user, :status).to(:active)
expect { risky_op }.to raise_error(MyError)
```

### Doubles

```ruby
repository = instance_double(UserRepository)
allow(repository).to receive(:find).with(1).and_return(user)

mailer = instance_spy(UserMailer)
service.call
expect(mailer).to have_received(:send_welcome).with(user)
```

## Requirements

1. Use composition over inheritance
2. Use keyword arguments for methods with 2+ parameters
3. Return early with guard clauses
4. Add `# frozen_string_literal: true` to every file
5. Use symbols for hash keys
6. Use Enumerable methods over manual iteration
7. Name predicate methods with `?`
8. Raise exceptions only for exceptional cases; use Result objects for expected failures
