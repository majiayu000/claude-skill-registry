---
name: rspec-testing
description: RSpec BDD testing framework for Ruby
category: Testing BDD
---

# Skill: rspec-testing

## What I do

I provide RSpec BDD expertise: describe/context/it structure, matchers, mocking with doubles, shared examples, and factory patterns for clean, expressive Ruby tests.

## When to use me

- Writing BDD specs for Ruby classes or Rails apps
- Structuring tests with describe/context/it blocks
- Using matchers, doubles, and stubs effectively
- Setting up shared examples and shared contexts
- Configuring RSpec with FactoryBot, DatabaseCleaner, etc.

## Core principles

1. **Describe behaviour, not methods** - Test what it does, not how
2. **One expectation per example** - Each `it` tests one behaviour
3. **Context for conditions** - Use `context` to group by state/scenario
4. **Let over instance variables** - Lazy `let` for test data, `let!` when eager needed
5. **Factories over fixtures** - FactoryBot for flexible, minimal test data

## Patterns & examples

**BDD test structure:**
```ruby
RSpec.describe Order do
  subject(:order) { described_class.new(user: user, items: items) }
  let(:user) { build(:user) }
  let(:items) { [build(:item, price: 10.0)] }

  describe '#total' do
    context 'with single item' do
      it 'returns the item price' do
        expect(order.total).to eq(10.0)
      end
    end

    context 'with discount applied' do
      before { order.apply_discount(0.1) }

      it 'reduces total by discount percentage' do
        expect(order.total).to eq(9.0)
      end
    end
  end
end
```

**Matchers (expressive assertions):**
```ruby
# ✅ Correct: expressive matchers
expect(user).to be_valid
expect(users).to include(alice)
expect(order.total).to be_within(0.01).of(9.99)
expect { order.submit! }.to change(Order, :count).by(1)
expect { risky_op }.to raise_error(InsufficientFundsError)

# ❌ Wrong: boolean assertions lose context
expect(user.valid?).to eq(true)  # error message: "expected true, got false"
```

**Doubles and stubs:**
```ruby
# ✅ Correct: stub external dependency at boundary
let(:payment_gateway) { instance_double(PaymentGateway) }

before do
  allow(payment_gateway).to receive(:charge)
    .with(amount: 10.0)
    .and_return(PaymentResult.new(success: true))
end

it 'processes payment' do
  result = order.checkout(gateway: payment_gateway)
  expect(result).to be_successful
end

# ❌ Wrong: stubbing the object under test
allow(order).to receive(:calculate_total).and_return(10.0)
```

**Shared examples:**
```ruby
RSpec.shared_examples 'a timestamped record' do
  it { is_expected.to respond_to(:created_at) }
  it { is_expected.to respond_to(:updated_at) }

  it 'sets timestamps on create' do
    subject.save!
    expect(subject.created_at).to be_present
  end
end

RSpec.describe User do
  it_behaves_like 'a timestamped record'
end
```

## Anti-patterns to avoid

- ❌ Instance variables in tests (use `let` / `let!` instead)
- ❌ Mystery guests (test data defined far from assertion)
- ❌ Stubbing the object under test (defeats the purpose)
- ❌ Deeply nested contexts beyond 3 levels (extract shared examples)
- ❌ Using `before(:all)` with database state (leaks between tests)

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/RSpec Testing.md`

## Related skills

- `ruby` - Core Ruby idioms and patterns
- `bdd-workflow` - Red-Green-Refactor cycle
- `test-fixtures` - Factory patterns for test data
- `clean-code` - SOLID principles in test code
