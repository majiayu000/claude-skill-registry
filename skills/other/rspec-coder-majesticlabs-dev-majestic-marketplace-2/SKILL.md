---
name: rspec-coder
description: This skill guides writing comprehensive RSpec tests for Ruby and Rails applications. Use when creating spec files, writing test cases, or testing new features. Covers RSpec syntax, describe/context organization, subject/let patterns, fixtures, mocking with allow/expect, and shoulda matchers.
allowed-tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch
---

# RSpec Coder

## Core Philosophy

- **AAA Pattern**: Arrange-Act-Assert structure for clarity
- **Behavior over Implementation**: Test what code does, not how
- **Isolation**: Tests should be independent
- **Descriptive Names**: Blocks should clearly explain behavior
- **Coverage**: Test happy paths AND edge cases
- **Fast Tests**: Minimize database operations
- **Fixtures**: Use fixtures for common data setup
- **Shoulda Matchers**: Use for validations and associations

## Critical Conventions

### ❌ Don't Add `require 'rails_helper'`

RSpec imports via `.rspec` config. Adding manually is redundant.

```ruby
# ✅ GOOD - no require needed
RSpec.describe User do
  # ...
end
```

### ❌ Don't Add Redundant Spec Type

RSpec infers type from file location automatically.

```ruby
# ✅ GOOD - type inferred from spec/models/ location
RSpec.describe User do
  # ...
end
```

### ✅ Use Namespace WITHOUT Leading `::`

```ruby
# ✅ GOOD - no leading double colons
RSpec.describe DynamicsGp::ERPSynchronizer do
  # ...
end
```

## Test Organization

### File Structure

```
spec/
├── models/           # Model unit tests
├── services/         # Service object tests
├── controllers/      # Controller tests
├── requests/         # Request specs (API testing)
├── mailers/          # Mailer tests
├── jobs/             # Background job tests
├── fixtures/         # Test data
├── support/          # Helper modules and shared examples
└── rails_helper.rb   # Rails-specific configuration
```

### Using `describe` and `context`

| Block | Purpose | Example |
|-------|---------|---------|
| `describe` | Groups by method/class | `describe "#process"` |
| `context` | Groups by condition | `context "when user is admin"` |

```ruby
RSpec.describe OrderProcessor do
  describe "#process" do
    context "with valid payment" do
      # success tests
    end

    context "with invalid payment" do
      # failure tests
    end
  end
end
```

## Subject and Let

See [resources/patterns.md](resources/patterns.md) for detailed examples.

| Pattern | Use Case |
|---------|----------|
| `subject(:name) { ... }` | Primary object/method under test |
| `let(:name) { ... }` | Lazy-evaluated, memoized data |
| `let!(:name) { ... }` | Eager evaluation (before each test) |

```ruby
RSpec.describe User do
  describe "#full_name" do
    subject(:full_name) { user.full_name }
    let(:user) { users(:alice) }

    it { is_expected.to eq("Alice Smith") }
  end
end
```

## Fixtures

See [resources/patterns.md](resources/patterns.md) for detailed examples.

```yaml
# spec/fixtures/users.yml
alice:
  name: Alice Smith
  email: alice@example.com
  admin: false
```

```ruby
RSpec.describe User do
  fixtures :users

  it "validates email" do
    expect(users(:alice)).to be_valid
  end
end
```

## Mocking and Stubbing

See [resources/patterns.md](resources/patterns.md) for detailed examples.

| Method | Purpose |
|--------|---------|
| `allow(obj).to receive(:method)` | Stub return value |
| `expect(obj).to receive(:method)` | Verify call happens |

```ruby
# Stubbing external service
allow(PaymentGateway).to receive(:charge).and_return(true)

# Verifying method called
expect(UserMailer).to receive(:welcome_email).with(user)
```

## Matchers Quick Reference

See [resources/matchers.md](resources/matchers.md) for complete reference.

### Essential Matchers

```ruby
# Equality
expect(value).to eq(expected)

# Truthiness
expect(obj).to be_valid
expect(obj).to be_truthy

# Change
expect { action }.to change { obj.status }.to("completed")
expect { action }.to change(Model, :count).by(1)

# Errors
expect { action }.to raise_error(SomeError)

# Collections
expect(array).to include(item)
expect(array).to be_empty
```

### Shoulda Matchers

```ruby
# Validations
it { is_expected.to validate_presence_of(:name) }
it { is_expected.to validate_uniqueness_of(:email) }

# Associations
it { is_expected.to have_many(:posts) }
it { is_expected.to belong_to(:account) }
```

## AAA Pattern

Structure all tests as Arrange-Act-Assert:

```ruby
describe "#process_refund" do
  subject(:process_refund) { processor.process_refund }

  let(:order) { orders(:completed_order) }
  let(:processor) { described_class.new(order) }

  it "updates order status" do
    process_refund  # Act
    expect(order.reload.status).to eq("refunded")  # Assert
  end

  it "credits user account" do
    expect { process_refund }  # Act
      .to change { order.user.reload.account_balance }  # Assert
      .by(order.total)
  end
end
```

## Test Coverage Standards

### What to Test

| Type | Test For |
|------|----------|
| Models | Validations, associations, scopes, callbacks, methods |
| Services | Happy path, sad path, edge cases, external integrations |
| Controllers | Status codes, response formats, auth, redirects |
| Jobs | Execution, retry logic, error handling, idempotency |

### Coverage Example

```ruby
RSpec.describe User do
  fixtures :users

  describe "validations" do
    subject(:user) { users(:valid_user) }

    it { is_expected.to validate_presence_of(:name) }
    it { is_expected.to validate_presence_of(:email) }
    it { is_expected.to validate_uniqueness_of(:email).case_insensitive }
  end

  describe "associations" do
    it { is_expected.to have_many(:posts).dependent(:destroy) }
  end

  describe "#full_name" do
    subject(:full_name) { user.full_name }
    let(:user) { User.new(first_name: "Alice", last_name: "Smith") }

    it { is_expected.to eq("Alice Smith") }

    context "when last name is missing" do
      let(:user) { User.new(first_name: "Alice") }
      it { is_expected.to eq("Alice") }
    end
  end
end
```

## Anti-Patterns

See [resources/anti-patterns.md](resources/anti-patterns.md) for detailed examples.

| Anti-Pattern | Why Bad |
|--------------|---------|
| `require 'rails_helper'` | Redundant, loaded via .rspec |
| `type: :model` | Redundant, inferred from location |
| Leading `::` in namespace | Violates RuboCop style |
| Empty test bodies | False confidence |
| Testing private methods | Couples to implementation |
| Not using fixtures | Slow tests |
| Not using shoulda | Verbose validation tests |

## Best Practices Checklist

**Critical Conventions**:
- [ ] NOT adding `require 'rails_helper'`
- [ ] NOT adding redundant spec type
- [ ] Using namespace WITHOUT leading `::`

**Test Organization**:
- [ ] `describe` for methods/classes
- [ ] `context` for conditions
- [ ] Max 3 levels nesting

**Test Data**:
- [ ] Using fixtures (not factories)
- [ ] Using `let` for lazy data
- [ ] Using `subject` for method under test

**Assertions**:
- [ ] Shoulda matchers for validations
- [ ] Shoulda matchers for associations
- [ ] `change` matcher for state changes

**Coverage**:
- [ ] Happy path tested
- [ ] Sad path tested
- [ ] Edge cases covered

## Quick Reference

```ruby
# Minimal spec file
RSpec.describe User do
  fixtures :users

  describe "#full_name" do
    subject(:full_name) { user.full_name }
    let(:user) { users(:alice) }

    it { is_expected.to eq("Alice Smith") }
  end

  describe "validations" do
    subject(:user) { users(:alice) }

    it { is_expected.to validate_presence_of(:name) }
    it { is_expected.to have_many(:posts) }
  end
end
```
