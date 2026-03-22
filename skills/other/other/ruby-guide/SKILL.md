---
name: ruby-guide
description: |
  Ruby language guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Ruby files (.rb), Gemfile, Rakefile, or when the user mentions Ruby.
  Provides block/proc patterns, metaprogramming guidelines, Bundler conventions,
  and testing standards specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: ruby
  extensions: ".rb,.rake,.gemspec"
---

# Ruby Guide

> Applies to: Ruby 3.2+, Gems, APIs, CLIs, Web Applications

## Core Principles

1. **Least Surprise**: Code should behave as readers expect; prefer clarity over cleverness
2. **Everything is an Object**: Leverage Ruby's object model; primitives are objects with methods
3. **Convention Over Configuration**: Follow established naming and structure conventions
4. **Duck Typing with Confidence**: Rely on behavior, not class checks; validate at boundaries
5. **Blocks Everywhere**: Use blocks for resource management, iteration, and DSLs

## Guardrails

### Version & Dependencies

- Use Ruby 3.2+ with `# frozen_string_literal: true` in every `.rb` file
- Manage dependencies with Bundler (`Gemfile` + `Gemfile.lock`)
- Pin gem versions with pessimistic operator: `gem "rails", "~> 7.1"`
- Run `bundle audit` before merging to check for vulnerable gems
- Commit `Gemfile.lock` for applications; omit for gems
- Specify `required_ruby_version` in `.gemspec` files

### Code Style

- Run `rubocop` before every commit (no exceptions)
- `snake_case` for methods/variables/files, `PascalCase` for classes/modules, `SCREAMING_SNAKE_CASE` for constants
- Predicate methods end with `?`, dangerous methods end with `!`
- Two-space indentation, no tabs
- Prefer guard clauses over nested conditionals

```ruby
# frozen_string_literal: true

# Bad: deeply nested
def process(user)
  if user
    if user.active?
      do_something(user) if user.verified?
    end
  end
end

# Good: guard clauses
def process(user)
  return unless user
  return unless user.active?
  return unless user.verified?

  do_something(user)
end
```

### Blocks & Procs

- Use `{}` for single-line blocks, `do...end` for multi-line
- Prefer `block_given?` + `yield` over explicit `&block` parameter
- Use lambdas for strict arity checking; procs for flexible arity

```ruby
# Block for resource management
File.open("data.txt", "r") do |file|
  file.each_line { |line| process(line) }
end

# Lambda vs Proc
validator = ->(x) { x.positive? }  # strict arity, returns from lambda
transformer = proc { |x| x.to_s }  # flexible arity, returns from enclosing

# Point-free style
names = users.map(&:name)
```

### Error Handling

- Rescue specific exceptions, never bare `rescue`
- Define custom errors inheriting from `StandardError`
- Use `ensure` for cleanup (not `rescue` for flow control)
- Provide `#message` with actionable information in custom errors

```ruby
class PaymentError < StandardError; end
class InsufficientFundsError < PaymentError; end

def charge(account, amount)
  raise InsufficientFundsError, "account #{account.id} needs #{amount}" if account.balance < amount

  account.debit(amount)
rescue Stripe::CardError => e
  Rails.logger.error("Payment failed for account=#{account.id}: #{e.message}")
  raise PaymentError, "card declined: #{e.message}"
end
```

### Metaprogramming

- Use `define_method` sparingly; prefer explicit method definitions
- Always pair `method_missing` with `respond_to_missing?`
- Prefer `Module#prepend` over `alias_method` chains
- Avoid `eval` with string arguments (use block form of `class_eval`)
- Never use metaprogramming in hot paths

```ruby
class DynamicFinder
  def method_missing(method_name, *args)
    if method_name.to_s.start_with?("find_by_")
      attribute = method_name.to_s.delete_prefix("find_by_")
      find_by_attribute(attribute, args.first)
    else
      super
    end
  end

  def respond_to_missing?(method_name, include_private = false)
    method_name.to_s.start_with?("find_by_") || super
  end
end
```

## Project Structure

### Gem Layout

```
mygem/
├── lib/
│   ├── mygem.rb              # Entry point, require dependencies
│   └── mygem/
│       ├── version.rb        # VERSION constant
│       ├── client.rb         # Core logic
│       └── errors.rb         # Custom error classes
├── spec/
│   ├── spec_helper.rb
│   └── mygem/
│       └── client_spec.rb
├── Gemfile
├── mygem.gemspec
└── Rakefile
```

### Application Layout

```
myapp/
├── app/
│   ├── models/               # Domain objects
│   ├── services/             # Business logic (POROs)
│   └── validators/           # Input validation
├── config/
├── db/migrate/               # Database migrations
├── lib/tasks/                # Rake tasks
├── spec/
│   ├── spec_helper.rb
│   ├── models/
│   └── services/
├── Gemfile
├── Gemfile.lock
└── Rakefile
```

- Service objects for business logic (single public method: `#call`)
- One class per file, file name matches class name in snake_case
- No global mutable state; use dependency injection or configuration objects

## Key Patterns

### Enumerable & Lazy Evaluation

```ruby
# Chain Enumerable methods over manual loops
users.select(&:active?).map(&:email).sort

# Lazy evaluation for large collections
File.open("huge.log").each_line.lazy
  .select { |line| line.include?("ERROR") }
  .map { |line| parse_error(line) }
  .first(10)

# each_with_object for building hashes
totals = orders.each_with_object(Hash.new(0)) do |order, sums|
  sums[order.category] += order.amount
end
```

### Pattern Matching (Ruby 3.x)

```ruby
case response
in { status: 200, body: { data: Array => items } }
  process_items(items)
in { status: 404 }
  handle_not_found
in { status: (500..) }
  handle_server_error
end

# Pin operator for variable binding
expected_id = 42
case record
in { id: ^expected_id, name: String => name }
  puts "Found: #{name}"
end
```

### Frozen String Literals & Immutability

```ruby
# frozen_string_literal: true

name = "hello"
name << " world"  # => FrozenError

# Use +"" or .dup when mutation is needed
mutable = +"hello"
mutable << " world"  # => "hello world"

VALID_STATUSES = %w[pending active suspended].freeze
CONFIG_DEFAULTS = { timeout: 30, retries: 3 }.freeze
```

### Ractor (Ruby 3.x Parallelism)

```ruby
workers = 4.times.map do
  Ractor.new do
    loop do
      task = Ractor.receive
      Ractor.yield expensive_computation(task)
    end
  end
end

tasks.each_with_index { |task, i| workers[i % workers.size].send(task) }
results = workers.map(&:take)
```

## Testing

### RSpec

```ruby
RSpec.describe PaymentService do
  subject(:service) { described_class.new(gateway: gateway) }

  let(:gateway) { instance_double(PaymentGateway) }
  let(:account) { build(:account, balance: 100.0) }

  describe "#charge" do
    context "when account has sufficient funds" do
      before { allow(gateway).to receive(:process).and_return(true) }

      it "debits the account" do
        expect { service.charge(account, 50.0) }
          .to change { account.balance }.from(100.0).to(50.0)
      end
    end

    context "when account has insufficient funds" do
      it "raises InsufficientFundsError" do
        expect { service.charge(account, 200.0) }
          .to raise_error(InsufficientFundsError, /needs 200/)
      end
    end
  end
end
```

### RSpec Conventions

- `describe` for class/method, `context` for scenario (prefix with "when" or "with")
- `let` for lazy data, `let!` only when eager evaluation is needed
- `subject` for the object under test, `described_class` over hardcoded class names
- Prefer `instance_double` over generic `double` for type safety
- Use shared examples for behavior shared across classes

### FactoryBot

```ruby
FactoryBot.define do
  factory :user do
    sequence(:email) { |n| "user#{n}@example.com" }
    name { "Test User" }
    active { true }
    trait(:admin) { role { "admin" } }
    trait(:inactive) { active { false } }
  end
end
```

### Testing Standards

- Test files mirror source: `lib/foo/bar.rb` -> `spec/foo/bar_spec.rb`
- Coverage target: >80% for business logic, >60% overall (use `simplecov`)
- All bug fixes include a regression test
- Test edge cases: nil, empty string, empty array, boundary values
- Use `webmock` or `vcr` for HTTP stubbing (no real network in unit tests)

## Tooling

### Essential Commands

```bash
bundle install              # Install dependencies
bundle exec rspec           # Run tests through Bundler
bundle exec rubocop         # Lint
bundle exec rubocop -a      # Auto-fix safe cops
bundle exec rake            # Default task (usually tests)
bundle audit                # Check for vulnerable gems
bundle outdated             # Show outdated gems
```

### RuboCop Configuration

```yaml
# .rubocop.yml
require:
  - rubocop-rspec
  - rubocop-performance
AllCops:
  NewCops: enable
  TargetRubyVersion: 3.2
Style/FrozenStringLiteralComment:
  Enabled: true
  EnforcedStyle: always
Metrics/MethodLength:
  Max: 20
Metrics/CyclomaticComplexity:
  Max: 10
```

### Bundler Best Practices

```ruby
# Gemfile
source "https://rubygems.org"
ruby "~> 3.2"

gem "dry-struct", "~> 1.6"
gem "zeitwerk", "~> 2.6"

group :development, :test do
  gem "rspec", "~> 3.13"
  gem "rubocop", "~> 1.60", require: false
  gem "factory_bot", "~> 6.4"
end

group :test do
  gem "simplecov", require: false
  gem "webmock", "~> 3.19"
end
```

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Enumerable patterns, metaprogramming examples, RSpec matchers

## External References

- [Ruby Style Guide](https://rubystyle.guide/)
- [RSpec Documentation](https://rspec.info/documentation/)
- [RuboCop Documentation](https://docs.rubocop.org/)
- [Ruby 3.x Pattern Matching](https://docs.ruby-lang.org/en/3.3/syntax/pattern_matching_rdoc.html)
- [Bundler Best Practices](https://bundler.io/guides/best_practices.html)
- [RBS Type Signatures](https://github.com/ruby/rbs)
- [Zeitwerk Autoloading](https://github.com/fxn/zeitwerk)
- [Ruby on Rails Guides](https://guides.rubyonrails.org/) (for Rails projects)
