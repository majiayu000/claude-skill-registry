---
name: aasm-coder
description: Implement state machines with AASM for workflow management. Covers state transitions, guards, callbacks, and testing.
---

# AASM Coder

State machine patterns for managing workflow states in Rails.

## Setup

```ruby
# Gemfile
gem "aasm", "~> 5.5"
```

## Basic State Machine

```ruby
class Order < ApplicationRecord
  include AASM

  aasm column: :status do
    state :pending, initial: true
    state :paid
    state :processing
    state :shipped
    state :cancelled

    event :pay do
      transitions from: :pending, to: :paid

      after do
        OrderMailer.payment_received(self).deliver_later
      end
    end

    event :process do
      transitions from: :paid, to: :processing
    end

    event :ship do
      transitions from: :processing, to: :shipped
    end

    event :cancel do
      transitions from: [:pending, :paid], to: :cancelled

      before do
        refund_payment if paid?
      end
    end
  end
end
```

## Usage

```ruby
order = Order.create!
order.pending?      # => true
order.may_pay?      # => true
order.pay!          # Transition + callbacks
order.paid?         # => true

order.may_ship?     # => false (must process first)
order.aasm.events   # => [:process, :cancel]

# Scopes created automatically
Order.pending
Order.paid.where(user: current_user)
```

## Guards

```ruby
event :pay do
  transitions from: :pending, to: :paid, guard: :payment_valid?
end

def payment_valid?
  payment_method.present? && total > 0
end

# Usage
order.pay!  # Raises AASM::InvalidTransition if guard fails
order.pay   # Returns false (no exception)
```

## Callbacks

```ruby
aasm do
  # State callbacks
  state :paid, before_enter: :validate_payment,
               after_enter: :send_receipt

  # Event callbacks
  event :ship do
    before do
      generate_tracking_number
    end

    after do
      notify_customer
    end

    transitions from: :processing, to: :shipped
  end
end
```

**Callback order:**
1. `before` (event)
2. `before_exit` (old state)
3. `before_enter` (new state)
4. State change persisted
5. `after_exit` (old state)
6. `after_enter` (new state)
7. `after` (event)

## Multiple Transitions

```ruby
event :approve do
  transitions from: :pending, to: :approved, guard: :auto_approvable?
  transitions from: :pending, to: :review, guard: :needs_review?
  transitions from: :pending, to: :rejected  # fallback
end
```

First matching guard wins.

## Error Handling

```ruby
# Safe (returns false on failure)
order.pay  # => false if invalid

# Raises exception
begin
  order.pay!
rescue AASM::InvalidTransition => e
  Rails.logger.error("Invalid transition: #{e.message}")
end

# Check before transition
if order.may_pay?
  order.pay!
end
```

## Testing State Machines

```ruby
RSpec.describe Order do
  let(:order) { create(:order) }

  it "starts in pending state" do
    expect(order).to be_pending
  end

  describe "pay event" do
    it "transitions to paid" do
      expect { order.pay! }
        .to change(order, :status).from("pending").to("paid")
    end

    it "sends payment received email" do
      expect(OrderMailer).to receive_message_chain(:payment_received, :deliver_later)
      order.pay!
    end
  end

  describe "ship event" do
    context "when pending" do
      it "raises error" do
        expect { order.ship! }.to raise_error(AASM::InvalidTransition)
      end
    end

    context "when processing" do
      before { order.update!(status: :processing) }

      it "transitions to shipped" do
        expect { order.ship! }
          .to change(order, :status).to("shipped")
      end
    end
  end
end
```

## Advanced Patterns

For multiple state machines, persistence options, and history tracking see:
- `references/aasm-patterns.md`

## Related Skills

- **`event-sourcing-coder`** - For recording domain events when state transitions should trigger notifications, webhooks, or audit trails.
