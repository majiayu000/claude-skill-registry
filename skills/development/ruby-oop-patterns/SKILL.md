---
name: Ruby OOP Patterns
description: Comprehensive guide to Object-Oriented Programming in Ruby and Rails covering classes, modules, design patterns, SOLID principles, and modern Ruby 3.x features
version: 1.0.0
---

# Ruby OOP Patterns

Complete guide to Object-Oriented Programming in Ruby and Ruby on Rails, from fundamentals to advanced patterns.

## Ruby OOP Fundamentals

### Classes and Objects

```ruby
# Basic class definition
class User
  # Class variables (shared across all instances)
  @@user_count = 0

  # Constants
  DEFAULT_ROLE = 'member'

  # Constructor
  def initialize(name, email)
    @name = name           # Instance variable
    @email = email
    @role = DEFAULT_ROLE
    @@user_count += 1
  end

  # Instance method
  def greet
    "Hello, I'm #{@name}"
  end

  # Class method (alternative syntax)
  def self.count
    @@user_count
  end

  # Class method (using class << self)
  class << self
    def reset_count
      @@user_count = 0
    end
  end
end

user = User.new('Alice', 'alice@example.com')
user.greet # => "Hello, I'm Alice"
User.count # => 1
```

### Attribute Accessors

```ruby
class Product
  # Read and write
  attr_accessor :name, :price

  # Read only
  attr_reader :created_at

  # Write only
  attr_writer :internal_code

  def initialize(name, price)
    @name = name
    @price = price
    @created_at = Time.current
  end
end

# Equivalent to:
class Product
  def name
    @name
  end

  def name=(value)
    @name = value
  end

  def created_at
    @created_at
  end

  def internal_code=(value)
    @internal_code = value
  end
end
```

### Method Visibility

```ruby
class BankAccount
  def initialize(balance)
    @balance = balance
  end

  # Public methods (default visibility)
  def deposit(amount)
    validate_amount(amount)
    @balance += amount
  end

  # Protected methods (callable by instances of same class or subclasses)
  protected

  def compare_balance(other_account)
    @balance <=> other_account.balance
  end

  def balance
    @balance
  end

  # Private methods (only callable within instance)
  private

  def validate_amount(amount)
    raise ArgumentError, "Amount must be positive" unless amount > 0
  end
end

# Modern Ruby 3.x private syntax
class BankAccount
  def deposit(amount)
    validate_amount(amount) # OK - called on self
    @balance += amount
  end

  private

  # Can also use inline private
  private def validate_amount(amount)
    raise ArgumentError, "Amount must be positive" unless amount > 0
  end
end
```

### Self Keyword

```ruby
class Document
  attr_accessor :title

  def initialize(title)
    @title = title
  end

  # Instance method - self refers to instance
  def display_title
    self.title # same as @title
  end

  # Class method - self refers to class
  def self.create_default
    new("Untitled") # same as self.new("Untitled")
  end

  # Comparing self
  def same_as?(other)
    self == other
  end

  # Returning self for method chaining
  def set_title(title)
    @title = title
    self # Return self for chaining
  end
end

doc = Document.new("Report")
doc.set_title("Annual Report").display_title
```

### Singleton Methods

```ruby
# Define method on specific object instance
user = User.new("Alice", "alice@example.com")

def user.special_greeting
  "Special greeting for #{@name}"
end

user.special_greeting # Works
other_user = User.new("Bob", "bob@example.com")
other_user.special_greeting # NoMethodError
```

---

## Modules

### Modules as Mixins

```ruby
# Shared behavior across classes
module Timestampable
  def mark_created
    @created_at = Time.current
  end

  def mark_updated
    @updated_at = Time.current
  end

  def timestamps
    { created_at: @created_at, updated_at: @updated_at }
  end
end

class Article
  include Timestampable

  def initialize(title)
    @title = title
    mark_created
  end
end

class Comment
  include Timestampable

  def initialize(body)
    @body = body
    mark_created
  end
end

article = Article.new("Title")
article.timestamps
```

### Modules as Namespaces

```ruby
module Analytics
  class Report
    def generate
      "Analytics Report"
    end
  end

  class Dashboard
    def display
      "Analytics Dashboard"
    end
  end
end

report = Analytics::Report.new
dashboard = Analytics::Dashboard.new
```

### Module Include vs Prepend vs Extend

```ruby
module Greetable
  def greet
    "Hello from Greetable"
  end
end

class Person
  def greet
    "Hello from Person"
  end
end

# include - adds module methods as instance methods (after class methods in lookup chain)
class Person
  include Greetable
end
Person.new.greet # => "Hello from Person" (class method takes precedence)

# prepend - adds module methods BEFORE class methods in lookup chain
class Person
  prepend Greetable
end
Person.new.greet # => "Hello from Greetable" (module takes precedence)

# extend - adds module methods as CLASS methods
class Person
  extend Greetable
end
Person.greet # => "Hello from Greetable" (class method)
Person.new.greet # NoMethodError
```

### Method Lookup Chain

```ruby
module A
  def who_am_i
    "A"
  end
end

module B
  def who_am_i
    "B"
  end
end

class C
  prepend A
  include B

  def who_am_i
    "C"
  end
end

C.ancestors # => [A, C, B, Object, Kernel, BasicObject]
C.new.who_am_i # => "A" (prepended module wins)
```

---

## Advanced Ruby OOP

### Metaprogramming

#### define_method

```ruby
class DynamicMethods
  [:first_name, :last_name, :email].each do |attribute|
    define_method(attribute) do
      instance_variable_get("@#{attribute}")
    end

    define_method("#{attribute}=") do |value|
      instance_variable_set("@#{attribute}", value)
    end
  end
end

user = DynamicMethods.new
user.first_name = "Alice"
user.first_name # => "Alice"
```

#### method_missing

```ruby
class DynamicFinder
  def initialize(data)
    @data = data
  end

  def method_missing(method_name, *args)
    if method_name.to_s.start_with?('find_by_')
      attribute = method_name.to_s.sub('find_by_', '')
      @data.find { |item| item[attribute.to_sym] == args.first }
    else
      super
    end
  end

  def respond_to_missing?(method_name, include_private = false)
    method_name.to_s.start_with?('find_by_') || super
  end
end

users = DynamicFinder.new([
  { name: 'Alice', email: 'alice@example.com' },
  { name: 'Bob', email: 'bob@example.com' }
])

users.find_by_name('Alice') # => { name: 'Alice', email: 'alice@example.com' }
users.find_by_email('bob@example.com') # => { name: 'Bob', email: 'bob@example.com' }
```

#### class_eval and instance_eval

```ruby
# class_eval - evaluates code in context of class
User.class_eval do
  def new_method
    "defined dynamically"
  end
end

# instance_eval - evaluates code in context of instance
user = User.new
user.instance_eval do
  @secret = "secret value"
end
```

### Eigenclass (Singleton Class)

```ruby
class Person
  def self.species
    "Homo sapiens"
  end
end

# Equivalent using eigenclass
class Person
  class << self
    def species
      "Homo sapiens"
    end
  end
end

# Adding methods to eigenclass of instance
person = Person.new
class << person
  def special_ability
    "Can fly"
  end
end

person.special_ability # Works
Person.new.special_ability # NoMethodError
```

---

## Rails-Specific OOP

### ActiveSupport::Concern

```ruby
# Traditional module
module Taggable
  def self.included(base)
    base.extend(ClassMethods)
    base.class_eval do
      has_many :tags, as: :taggable
    end
  end

  module ClassMethods
    def with_tag(tag_name)
      joins(:tags).where(tags: { name: tag_name })
    end
  end

  def tag_names
    tags.pluck(:name)
  end
end

# Using ActiveSupport::Concern (cleaner)
module Taggable
  extend ActiveSupport::Concern

  included do
    has_many :tags, as: :taggable
  end

  class_methods do
    def with_tag(tag_name)
      joins(:tags).where(tags: { name: tag_name })
    end
  end

  def tag_names
    tags.pluck(:name)
  end
end

# Usage
class Article < ApplicationRecord
  include Taggable
end

Article.with_tag('ruby') # Class method
article.tag_names # Instance method
```

### Service Objects

```ruby
# Service object for complex business logic
class CreateOrderService
  def initialize(user, cart)
    @user = user
    @cart = cart
  end

  def call
    validate_cart!

    ActiveRecord::Base.transaction do
      @order = create_order
      create_order_items
      charge_payment
      send_confirmation
      clear_cart
    end

    Result.success(@order)
  rescue => e
    Result.failure(e.message)
  end

  private

  def validate_cart!
    raise "Cart is empty" if @cart.items.empty?
    raise "Cart total invalid" unless @cart.total_valid?
  end

  def create_order
    @user.orders.create!(total: @cart.total, status: 'pending')
  end

  def create_order_items
    @cart.items.each do |cart_item|
      @order.order_items.create!(
        product: cart_item.product,
        quantity: cart_item.quantity,
        price: cart_item.price
      )
    end
  end

  def charge_payment
    PaymentService.charge(@user, @cart.total)
  end

  def send_confirmation
    OrderMailer.confirmation(@order).deliver_later
  end

  def clear_cart
    @cart.clear!
  end
end

# Result object
class Result
  attr_reader :value, :error

  def initialize(success, value, error = nil)
    @success = success
    @value = value
    @error = error
  end

  def self.success(value)
    new(true, value)
  end

  def self.failure(error)
    new(false, nil, error)
  end

  def success?
    @success
  end

  def failure?
    !@success
  end
end

# Usage
result = CreateOrderService.new(user, cart).call
if result.success?
  redirect_to order_path(result.value)
else
  flash[:error] = result.error
  redirect_to cart_path
end
```

### Form Objects

```ruby
class UserRegistrationForm
  include ActiveModel::Model
  include ActiveModel::Attributes

  attribute :email, :string
  attribute :password, :string
  attribute :password_confirmation, :string
  attribute :first_name, :string
  attribute :last_name, :string
  attribute :accept_terms, :boolean

  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :password, presence: true, length: { minimum: 8 }
  validates :password_confirmation, presence: true
  validates :first_name, :last_name, presence: true
  validates :accept_terms, acceptance: true

  validate :passwords_match

  def save
    return false unless valid?

    ActiveRecord::Base.transaction do
      @user = User.create!(
        email: email,
        password: password,
        first_name: first_name,
        last_name: last_name
      )

      @profile = @user.create_profile!
      send_welcome_email
    end

    true
  rescue => e
    errors.add(:base, e.message)
    false
  end

  attr_reader :user

  private

  def passwords_match
    if password != password_confirmation
      errors.add(:password_confirmation, "doesn't match password")
    end
  end

  def send_welcome_email
    UserMailer.welcome(@user).deliver_later
  end
end

# Usage in controller
def create
  @form = UserRegistrationForm.new(registration_params)

  if @form.save
    redirect_to dashboard_path
  else
    render :new
  end
end
```

### Query Objects

```ruby
class ActiveUsersQuery
  def initialize(relation = User.all)
    @relation = relation
  end

  def call
    @relation
      .where(active: true)
      .where('last_login_at > ?', 30.days.ago)
      .order(last_login_at: :desc)
  end

  # Chainable query methods
  def with_subscription
    @relation = @relation.joins(:subscription).where.not(subscriptions: { expires_at: nil })
    self
  end

  def by_role(role)
    @relation = @relation.where(role: role)
    self
  end
end

# Usage
ActiveUsersQuery.new.call
ActiveUsersQuery.new.with_subscription.call
ActiveUsersQuery.new.by_role('admin').with_subscription.call
```

### Policy Objects (Pundit)

```ruby
# app/policies/post_policy.rb
class PostPolicy
  attr_reader :user, :post

  def initialize(user, post)
    @user = user
    @post = post
  end

  def index?
    true
  end

  def show?
    post.published? || post.author == user || user&.admin?
  end

  def create?
    user.present?
  end

  def update?
    post.author == user || user&.admin?
  end

  def destroy?
    post.author == user || user&.admin?
  end

  def publish?
    (post.author == user && post.draft?) || user&.admin?
  end

  class Scope
    attr_reader :user, :scope

    def initialize(user, scope)
      @user = user
      @scope = scope
    end

    def resolve
      if user&.admin?
        scope.all
      elsif user
        scope.where(published: true).or(scope.where(author: user))
      else
        scope.where(published: true)
      end
    end
  end
end

# Usage
authorize @post # Calls PostPolicy#show?
@posts = policy_scope(Post) # Calls PostPolicy::Scope#resolve
```

### Presenter/Decorator Objects

```ruby
class UserPresenter
  def initialize(user, view_context)
    @user = user
    @view = view_context
  end

  def full_name
    [@user.first_name, @user.last_name].join(' ')
  end

  def avatar_url
    @user.avatar.attached? ? @view.url_for(@user.avatar) : @view.asset_path('default_avatar.png')
  end

  def formatted_created_at
    @view.time_ago_in_words(@user.created_at) + " ago"
  end

  def profile_link
    @view.link_to(full_name, @view.user_path(@user))
  end

  # Delegate unknown methods to user
  def method_missing(method, *args, &block)
    @user.send(method, *args, &block)
  end

  def respond_to_missing?(method, include_private = false)
    @user.respond_to?(method, include_private) || super
  end
end

# Using Draper gem (recommended)
class UserDecorator < Draper::Decorator
  delegate_all

  def full_name
    [object.first_name, object.last_name].join(' ')
  end

  def avatar_url
    object.avatar.attached? ? h.url_for(object.avatar) : h.asset_path('default_avatar.png')
  end

  def formatted_created_at
    h.time_ago_in_words(object.created_at) + " ago"
  end
end

# Usage
@user = User.find(params[:id]).decorate
@user.full_name
@user.formatted_created_at
```

### Value Objects

```ruby
class Money
  include Comparable

  attr_reader :amount, :currency

  def initialize(amount, currency = 'USD')
    @amount = BigDecimal(amount.to_s)
    @currency = currency
  end

  def +(other)
    raise ArgumentError, "Currency mismatch" unless currency == other.currency
    Money.new(amount + other.amount, currency)
  end

  def -(other)
    raise ArgumentError, "Currency mismatch" unless currency == other.currency
    Money.new(amount - other.amount, currency)
  end

  def *(multiplier)
    Money.new(amount * multiplier, currency)
  end

  def <=>(other)
    return nil unless currency == other.currency
    amount <=> other.amount
  end

  def ==(other)
    other.is_a?(Money) && amount == other.amount && currency == other.currency
  end
  alias eql? ==

  def hash
    [amount, currency].hash
  end

  def to_s
    format("%.2f %s", amount, currency)
  end
end

# Usage
price = Money.new(29.99, 'USD')
tax = Money.new(2.10, 'USD')
total = price + tax # => Money object
total.to_s # => "32.09 USD"
```

---

## SOLID Principles in Ruby

### Single Responsibility Principle (SRP)

**Each class should have one reason to change.**

```ruby
# BAD - Multiple responsibilities
class User
  def create
    # Database logic
    ActiveRecord::Base.connection.execute("INSERT INTO users...")

    # Email logic
    send_welcome_email

    # Analytics logic
    track_signup_event
  end
end

# GOOD - Separated responsibilities
class User < ApplicationRecord
  after_create :send_welcome_email
  after_create :track_signup

  private

  def send_welcome_email
    UserMailer.welcome(self).deliver_later
  end

  def track_signup
    AnalyticsService.track_event(self, 'signup')
  end
end

class UserMailer < ApplicationMailer
  def welcome(user)
    # Email logic
  end
end

class AnalyticsService
  def self.track_event(user, event_name)
    # Analytics logic
  end
end
```

### Open/Closed Principle (OCP)

**Open for extension, closed for modification.**

```ruby
# BAD - Must modify class to add payment methods
class PaymentProcessor
  def process(payment_method, amount)
    case payment_method
    when 'credit_card'
      process_credit_card(amount)
    when 'paypal'
      process_paypal(amount)
    when 'bitcoin'
      process_bitcoin(amount)
    end
  end
end

# GOOD - Open for extension via polymorphism
class PaymentProcessor
  def process(payment_method, amount)
    payment_method.process(amount)
  end
end

class CreditCardPayment
  def process(amount)
    # Credit card processing
  end
end

class PaypalPayment
  def process(amount)
    # PayPal processing
  end
end

class BitcoinPayment
  def process(amount)
    # Bitcoin processing
  end
end

# Usage
processor = PaymentProcessor.new
processor.process(CreditCardPayment.new, 100)
processor.process(PaypalPayment.new, 100)
```

### Liskov Substitution Principle (LSP)

**Subclasses should be substitutable for their base classes.**

```ruby
# BAD - Breaks LSP
class Rectangle
  attr_accessor :width, :height

  def area
    width * height
  end
end

class Square < Rectangle
  def width=(value)
    super
    @height = value
  end

  def height=(value)
    super
    @width = value
  end
end

# This breaks expectations:
rect = Square.new
rect.width = 5
rect.height = 10
rect.area # => 100 (expected 50)

# GOOD - Composition over inheritance
class Rectangle
  attr_accessor :width, :height

  def area
    width * height
  end
end

class Square
  attr_reader :side

  def initialize(side)
    @side = side
  end

  def area
    side * side
  end
end
```

### Interface Segregation Principle (ISP)

**Clients shouldn't depend on interfaces they don't use.**

```ruby
# BAD - Fat interface
module Worker
  def work
    raise NotImplementedError
  end

  def eat
    raise NotImplementedError
  end

  def sleep
    raise NotImplementedError
  end
end

class Human
  include Worker

  def work; end
  def eat; end
  def sleep; end
end

class Robot
  include Worker

  def work; end
  def eat; raise "Robots don't eat"; end
  def sleep; raise "Robots don't sleep"; end
end

# GOOD - Segregated interfaces
module Workable
  def work
    raise NotImplementedError
  end
end

module Eatable
  def eat
    raise NotImplementedError
  end
end

module Sleepable
  def sleep
    raise NotImplementedError
  end
end

class Human
  include Workable
  include Eatable
  include Sleepable

  def work; end
  def eat; end
  def sleep; end
end

class Robot
  include Workable

  def work; end
end
```

### Dependency Inversion Principle (DIP)

**Depend on abstractions, not concretions.**

```ruby
# BAD - Direct dependency on concrete class
class OrderProcessor
  def process(order)
    notifier = EmailNotifier.new
    notifier.send(order.customer.email, "Order processed")
  end
end

# GOOD - Dependency injection
class OrderProcessor
  def initialize(notifier)
    @notifier = notifier
  end

  def process(order)
    @notifier.send(order.customer.email, "Order processed")
  end
end

class EmailNotifier
  def send(email, message)
    # Send email
  end
end

class SmsNotifier
  def send(phone, message)
    # Send SMS
  end
end

# Usage
email_processor = OrderProcessor.new(EmailNotifier.new)
sms_processor = OrderProcessor.new(SmsNotifier.new)
```

---

## Inheritance Patterns

### Single Table Inheritance (STI)

```ruby
# app/models/vehicle.rb
class Vehicle < ApplicationRecord
  # Table: vehicles
  # Columns: id, type, name, max_speed, max_altitude, max_depth
end

class Car < Vehicle
  def drive
    "Driving at #{max_speed} mph"
  end
end

class Airplane < Vehicle
  def fly
    "Flying at #{max_altitude} ft"
  end
end

class Submarine < Vehicle
  def dive
    "Diving to #{max_depth} ft"
  end
end

# Usage
car = Car.create(name: 'Tesla', max_speed: 150)
airplane = Airplane.create(name: 'Boeing 747', max_altitude: 45000)

Vehicle.all # Returns mix of Cars, Airplanes, Submarines
Car.all # Returns only Cars
```

**When to use STI:**
- Subclasses share most attributes
- Subclasses have similar behavior
- Need to query across all types

**STI Anti-patterns:**
- Too many type-specific columns (use delegated_type instead)
- Vastly different behavior between types
- Deep inheritance hierarchies

### Delegated Type (Rails 6.1+)

```ruby
# Better than STI when types have different attributes
class Entry < ApplicationRecord
  delegated_type :entryable, types: %w[Message Comment]
end

class Message < ApplicationRecord
  has_one :entry, as: :entryable, touch: true
end

class Comment < ApplicationRecord
  has_one :entry, as: :entryable, touch: true
end

# Usage
entry = Entry.find(1)
entry.entryable # Returns Message or Comment
entry.message? # true if type is Message
entry.comment? # true if type is Comment
```

### Polymorphic Associations

```ruby
class Comment < ApplicationRecord
  belongs_to :commentable, polymorphic: true
end

class Article < ApplicationRecord
  has_many :comments, as: :commentable
end

class Video < ApplicationRecord
  has_many :comments, as: :commentable
end

# Usage
article = Article.find(1)
article.comments.create(body: "Great article!")

video = Video.find(1)
video.comments.create(body: "Great video!")
```

---

## Composition Over Inheritance

### Delegation with Forwardable

```ruby
require 'forwardable'

class Order
  extend Forwardable

  def_delegators :@customer, :name, :email, :phone
  def_delegators :@line_items, :<<, :each, :size

  def initialize(customer)
    @customer = customer
    @line_items = []
  end
end

order = Order.new(customer)
order.name # Delegates to customer.name
order << line_item # Delegates to line_items.<<
```

### SimpleDelegator

```ruby
require 'delegate'

class UserDecorator < SimpleDelegator
  def full_name
    "#{first_name} #{last_name}"
  end

  def greeting
    "Hello, #{full_name}!"
  end
end

user = User.new(first_name: 'Alice', last_name: 'Smith')
decorated = UserDecorator.new(user)
decorated.full_name # => "Alice Smith"
decorated.email # Delegates to user.email
```

### ActiveSupport::Delegation

```ruby
class Order
  delegate :name, :email, to: :customer, prefix: true
  delegate :total_price, to: :calculator

  def initialize(customer, items)
    @customer = customer
    @items = items
  end

  private

  def calculator
    @calculator ||= PriceCalculator.new(@items)
  end
end

order.customer_name # => customer.name
order.customer_email # => customer.email
order.total_price # => calculator.total_price
```

---

## Modern Ruby Features

### Pattern Matching (Ruby 3.x)

```ruby
def process_response(response)
  case response
  in { status: 200, body: }
    puts "Success: #{body}"
  in { status: 404 }
    puts "Not found"
  in { status: 500..599, error: }
    puts "Server error: #{error}"
  else
    puts "Unknown response"
  end
end

# Array pattern matching
def process_coordinates(point)
  case point
  in [0, 0]
    "Origin"
  in [x, 0]
    "On X axis at #{x}"
  in [0, y]
    "On Y axis at #{y}"
  in [x, y]
    "Point at (#{x}, #{y})"
  end
end
```

### Endless Methods (Ruby 3.x)

```ruby
# Traditional
def full_name
  "#{first_name} #{last_name}"
end

# Endless method
def full_name = "#{first_name} #{last_name}"

# With arguments
def greet(name) = "Hello, #{name}!"

# Useful for simple one-liners
def adult? = age >= 18
def total = items.sum(&:price)
```

### Keyword Arguments

```ruby
# Required keyword arguments
def create_user(email:, password:, role: 'member')
  User.create(email: email, password: password, role: role)
end

create_user(email: 'user@example.com', password: 'secret')

# **kwargs for flexibility
def build_query(**options)
  options.each do |key, value|
    puts "#{key}: #{value}"
  end
end

build_query(name: 'Alice', age: 30, city: 'NYC')
```

### Numbered Parameters

```ruby
# Traditional
users.map { |user| user.name.upcase }

# Numbered parameters (Ruby 2.7+)
users.map { _1.name.upcase }

# Multiple parameters
users.zip(posts).map { "#{_1.name}: #{_2.title}" }
```

---

## Testing OOP Code

### Testing Private Methods

```ruby
# Generally, don't test private methods directly
# Test through public interface instead

class Calculator
  def calculate(numbers)
    validate_input(numbers)
    sum(numbers)
  end

  private

  def validate_input(numbers)
    raise ArgumentError unless numbers.is_a?(Array)
  end

  def sum(numbers)
    numbers.sum
  end
end

# Test public method (which exercises private methods)
RSpec.describe Calculator do
  describe '#calculate' do
    it 'calculates sum' do
      expect(subject.calculate([1, 2, 3])).to eq(6)
    end

    it 'validates input' do
      expect { subject.calculate("invalid") }.to raise_error(ArgumentError)
    end
  end
end

# If you MUST test private method
RSpec.describe Calculator do
  describe '#sum' do
    it 'sums numbers' do
      expect(subject.send(:sum, [1, 2, 3])).to eq(6)
    end
  end
end
```

### Testing Modules

```ruby
module Taggable
  def add_tag(tag)
    @tags ||= []
    @tags << tag
  end

  def tags
    @tags || []
  end
end

# Create dummy class for testing
RSpec.describe Taggable do
  let(:dummy_class) { Class.new { include Taggable } }
  let(:instance) { dummy_class.new }

  describe '#add_tag' do
    it 'adds tag' do
      instance.add_tag('ruby')
      expect(instance.tags).to include('ruby')
    end
  end
end
```

### Mocking and Stubbing

```ruby
RSpec.describe OrderProcessor do
  describe '#process' do
    let(:order) { double('Order', id: 1, total: 100) }
    let(:payment_gateway) { double('PaymentGateway') }
    subject { OrderProcessor.new(payment_gateway) }

    it 'charges payment' do
      expect(payment_gateway).to receive(:charge).with(100)
      subject.process(order)
    end

    it 'handles payment failure' do
      allow(payment_gateway).to receive(:charge).and_raise(PaymentError)
      expect { subject.process(order) }.to raise_error(PaymentError)
    end
  end
end
```

---

## Rails Anti-Patterns

### Fat Models

```ruby
# BAD - Fat model with too many responsibilities
class User < ApplicationRecord
  def create_with_profile(params)
    # Creation logic
  end

  def send_welcome_email
    # Email logic
  end

  def calculate_statistics
    # Analytics logic
  end

  def export_to_csv
    # Export logic
  end
end

# GOOD - Thin model with extracted services
class User < ApplicationRecord
  # Only model-specific logic and validations
  validates :email, presence: true, uniqueness: true
  has_many :posts
end

class UserCreationService
  def call(params)
    # Creation logic
  end
end

class UserStatisticsService
  def call(user)
    # Analytics logic
  end
end

class UserCsvExporter
  def export(users)
    # Export logic
  end
end
```

### Callback Hell

```ruby
# BAD - Too many callbacks
class Order < ApplicationRecord
  before_validation :set_defaults
  after_validation :check_inventory
  before_create :generate_order_number
  after_create :send_confirmation
  after_create :update_inventory
  after_create :create_invoice
  after_create :notify_warehouse
  after_update :log_changes
  before_destroy :cancel_pending_shipments
end

# GOOD - Explicit service object
class CreateOrderService
  def call(params)
    order = Order.new(params)
    order.set_defaults

    return Result.failure(order.errors) unless order.valid?

    ActiveRecord::Base.transaction do
      order.generate_order_number
      order.save!

      send_confirmation(order)
      update_inventory(order)
      create_invoice(order)
      notify_warehouse(order)
    end

    Result.success(order)
  end
end
```

### God Objects

```ruby
# BAD - One object does everything
class ApplicationController < ActionController::Base
  def current_user
    # User logic
  end

  def authorize_admin
    # Authorization logic
  end

  def log_action(action)
    # Logging logic
  end

  def send_notification(message)
    # Notification logic
  end

  def format_date(date)
    # Formatting logic
  end
end

# GOOD - Separated concerns
class ApplicationController < ActionController::Base
  include Authentication
  include Authorization
  include Logging
end

module Authentication
  def current_user
    @current_user ||= User.find_by(id: session[:user_id])
  end
end

module Authorization
  def authorize_admin
    redirect_to root_path unless current_user&.admin?
  end
end
```

---

## Summary Checklist

**Good OOP Practices:**

- [ ] Use meaningful class and method names
- [ ] Keep classes focused (Single Responsibility Principle)
- [ ] Prefer composition over inheritance
- [ ] Use modules for shared behavior
- [ ] Make dependencies explicit (dependency injection)
- [ ] Write tests for public interfaces
- [ ] Use service objects for complex business logic
- [ ] Use form objects for complex forms
- [ ] Use query objects for complex queries
- [ ] Use presenters/decorators for view logic
- [ ] Follow SOLID principles
- [ ] Avoid callback hell - use service objects
- [ ] Avoid fat models - extract to services
- [ ] Use value objects for domain concepts

This skill provides comprehensive OOP patterns for Ruby and Rails development!
