---
name: rails-business-logic
description: Specialized skill for Rails business logic with ActiveInteraction, AASM state machines, and ActiveDecorator. Use when implementing complex operations, state transitions, or presentation logic. Enforces interaction pattern over service objects.
---

# Rails Business Logic

Implement business logic with ActiveInteraction, state machines, and decorators.

## When to Use This Skill

- Creating business operations with ActiveInteraction
- Implementing state machines with AASM
- Adding presentation logic with ActiveDecorator
- Refactoring service objects to interactions
- Managing complex workflows
- Handling state transitions
- Composing business operations

## Core Principle: Use Interactions, NOT Service Objects

**Why ActiveInteraction over service objects?**

- ✓ Built-in type checking
- ✓ Automatic validation
- ✓ Explicit contracts (inputs/outputs)
- ✓ Composable
- ✓ Testable
- ✓ Self-documenting

```ruby
# Gemfile
gem "active_interaction", "~> 5.3"
gem "aasm", "~> 5.5"
gem "active_decorator", "~> 1.4"
```

## ActiveInteraction Basics

### Simple Interaction

```ruby
# app/interactions/users/create.rb
module Users
  class Create < ActiveInteraction::Base
    # Define inputs with types
    string :email
    string :name
    string :password, default: nil

    # Validations
    validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
    validates :name, presence: true

    # Main logic
    def execute
      user = User.create!(
        email: email,
        name: name,
        password: password || generate_password
      )

      UserMailer.welcome(user).deliver_later

      user  # Return value becomes outcome.result
    end

    private

    def generate_password
      SecureRandom.alphanumeric(32)
    end
  end
end
```

### Running Interactions

```ruby
# In controller
def create
  outcome = Users::Create.run(
    email: params[:email],
    name: params[:name],
    password: params[:password]
  )

  if outcome.valid?
    @user = outcome.result
    redirect_to @user, notice: "User created"
  else
    @errors = outcome.errors
    render :new, status: :unprocessable_entity
  end
end

# With bang method (raises on error)
user = Users::Create.run!(email: "user@example.com", name: "John")
```

### Input Types

```ruby
class MyInteraction < ActiveInteraction::Base
  # Primitives
  string :name
  integer :age
  float :price
  boolean :active
  symbol :status

  # Objects
  date :birthday
  time :created_at
  date_time :scheduled_at

  # Complex types
  array :tags
  hash :metadata

  # Model instances
  object :user, class: User

  # Arrays of specific types
  array :emails, default: [] do
    string
  end

  # Optional (nilable)
  string :optional_field, default: nil

  # Custom default
  integer :count, default: 0
end
```

### Composing Interactions

```ruby
module Users
  class Register < ActiveInteraction::Base
    string :email
    string :name
    string :password

    def execute
      # Compose other interactions
      user = compose(Users::Create,
        email: email,
        name: name,
        password: password
      )

      # compose raises if nested interaction fails
      # errors are merged automatically

      compose(Users::SendWelcomeEmail, user: user)

      user
    end
  end
end
```

### Testing Interactions

```ruby
RSpec.describe Users::Create do
  let(:valid_params) do
    { email: "user@example.com", name: "John", password: "SecurePass123" }
  end

  context "with valid parameters" do
    it "creates user" do
      expect { described_class.run(valid_params) }
        .to change(User, :count).by(1)
    end

    it "returns valid outcome" do
      outcome = described_class.run(valid_params)
      expect(outcome).to be_valid
    end

    it "returns created user" do
      outcome = described_class.run(valid_params)
      expect(outcome.result).to be_a(User)
    end
  end

  context "with invalid parameters" do
    it "returns invalid outcome" do
      outcome = described_class.run(valid_params.merge(email: nil))
      expect(outcome).not_to be_valid
    end
  end
end
```

## State Machines (AASM)

### Basic State Machine

```ruby
# app/models/order.rb
class Order < ApplicationRecord
  include AASM

  aasm column: :status do
    state :pending, initial: true
    state :paid
    state :processing
    state :shipped
    state :delivered
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

      after do
        TrackingService.create_shipment(self)
      end
    end

    event :deliver do
      transitions from: :shipped, to: :delivered
    end

    event :cancel do
      transitions from: [:pending, :paid], to: :cancelled

      before do
        refund_payment if paid?
      end
    end
  end

  private

  def refund_payment
    PaymentService.refund(self)
  end
end
```

### Usage

```ruby
order = Order.create!
order.pending?  # => true
order.status    # => "pending"

# Trigger transitions
order.pay!
order.paid?  # => true

# Check if transition allowed
order.may_ship?  # => false (must process first)
order.may_process?  # => true

order.process!
order.ship!
order.shipped?  # => true

# Get available events
order.aasm.events  # => [:deliver, :cancel]
```

### Guards

```ruby
class Order < ApplicationRecord
  include AASM

  aasm do
    state :pending, initial: true
    state :paid

    event :pay do
      transitions from: :pending, to: :paid, guard: :payment_valid?
    end
  end

  def payment_valid?
    payment_method.present? && total > 0
  end
end

# Usage
order.pay!  # Raises AASM::InvalidTransition if guard fails
order.pay   # Returns false if guard fails (no exception)
```

### Scopes

AASM automatically creates scopes:

```ruby
Order.pending    # All pending orders
Order.paid       # All paid orders
Order.shipped    # All shipped orders

# Combine with other scopes
Order.paid.where(user: current_user)
```

### Testing State Machines

```ruby
RSpec.describe Order do
  let(:order) { create(:order) }

  it "starts in pending state" do
    expect(order).to be_pending
  end

  describe "pay event" do
    it "transitions from pending to paid" do
      expect { order.pay! }
        .to change(order, :status).from("pending").to("paid")
    end

    it "sends payment receipt" do
      expect { order.pay! }
        .to have_enqueued_mail(OrderMailer, :payment_received)
    end
  end

  describe "ship event" do
    context "when order is paid" do
      before { order.pay!; order.process! }

      it "allows shipping" do
        expect(order.may_ship?).to be true
      end
    end

    context "when order is pending" do
      it "raises error" do
        expect { order.ship! }.to raise_error(AASM::InvalidTransition)
      end
    end
  end
end
```

## Decorators (ActiveDecorator)

### Basic Decorator

```ruby
# app/decorators/user_decorator.rb
module UserDecorator
  def full_name
    "#{first_name} #{last_name}"
  end

  def avatar_url(size: :medium)
    if avatar.attached?
      helpers.url_for(avatar.variant(resize_to_limit: avatar_size(size)))
    else
      helpers.image_url("default-avatar.png")
    end
  end

  def formatted_created_at
    created_at.strftime("%B %d, %Y")
  end

  def status_badge
    case status
    when "active"
      helpers.content_tag(:span, "Active", class: "badge badge-success")
    when "inactive"
      helpers.content_tag(:span, "Inactive", class: "badge badge-secondary")
    end
  end

  private

  def avatar_size(size)
    { small: [50, 50], medium: [100, 100], large: [200, 200] }[size]
  end

  def helpers
    ActionController::Base.helpers
  end
end
```

### Usage in Views

```erb
<%# Automatically decorated in views %>
<%= @user.full_name %>
<%= image_tag @user.avatar_url(size: :large) %>
<%= @user.formatted_created_at %>
<%= @user.status_badge %>

<%# Collections decorated automatically %>
<% @users.each do |user| %>
  <p><%= user.full_name %></p>
<% end %>
```

### Testing Decorators

```ruby
RSpec.describe UserDecorator do
  let(:user) { create(:user, first_name: "John", last_name: "Doe") }

  describe "#full_name" do
    it "combines first and last name" do
      expect(user.full_name).to eq("John Doe")
    end
  end

  describe "#formatted_created_at" do
    it "formats date" do
      user.update(created_at: Date.new(2025, 1, 15))
      expect(user.formatted_created_at).to eq("January 15, 2025")
    end
  end
end
```

## Service Objects vs Interactions

### DON'T Use Service Objects

```ruby
# AVOID - Verbose service object
class UserCreationService
  def initialize(params)
    @params = params
    @errors = []
  end

  def call
    validate_params
    return false if errors.any?
    create_user
  end

  # ... lots of boilerplate
end
```

### DO Use Interactions

```ruby
# PREFER - Clean interaction
class Users::Create < ActiveInteraction::Base
  string :email
  string :name

  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }

  def execute
    User.create!(email: email, name: name)
  end
end
```

## Controller Pattern

```ruby
class ArticlesController < ApplicationController
  def create
    outcome = Articles::Create.run(
      title: params[:article][:title],
      body: params[:article][:body],
      author: current_user
    )

    if outcome.valid?
      redirect_to article_path(outcome.result), notice: "Article created"
    else
      @article = Article.new(params[:article])
      @article.errors.merge!(outcome.errors)
      render :new, status: :unprocessable_entity
    end
  end
end
```

## Reference Documentation

For comprehensive business logic patterns:
- Business logic guide: `business-logic.md` (detailed examples and advanced patterns)
