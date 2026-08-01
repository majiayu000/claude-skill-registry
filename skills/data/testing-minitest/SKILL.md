---
name: testing-minitest
description: This skill should be used when the user asks about testing Rails applications,
  Minitest, test-driven development (TDD), unit tests, integration tests, system tests,
  fixtures, factories, mocking, stubb
---

---
name: testing-minitest
description: This skill should be used when the user asks about testing Rails applications, Minitest, test-driven development (TDD), unit tests, integration tests, system tests, fixtures, factories, mocking, stubbing, test coverage, continuous integration, test organization, or Rails testing best practices. Also use when discussing testing philosophy, test speed, or debugging failing tests. Examples:

<example>
Context: User wants to test a model
user: "How do I write tests for my Product model validations?"
assistant: "I'll show you how to write Minitest unit tests for model validations."
<commentary>
This relates to model testing and Minitest assertions.
</commentary>
</example>

<example>
Context: User needs to test user flows
user: "How do I test the complete checkout process?"
assistant: "System tests are perfect for end-to-end workflows. Let me show you."
<commentary>
This involves system tests with browser simulation.
</commentary>
</example>

<example>
Context: User asks about testing philosophy
user: "Should I write tests first or after implementing features?"
assistant: "Rails embraces TDD—write tests first. Let me explain the workflow."
<commentary>
This relates to TDD philosophy and Rails testing culture.
</commentary>
</example>
---

# Testing with Minitest: Rails Testing Philosophy

## Overview

Rails includes a comprehensive testing framework based on Minitest. Testing is baked into Rails from the start—every generated model, controller, and mailer includes a test file.

**Rails testing philosophy:**
- Write tests early and often
- Test-driven development (TDD) is encouraged
- Tests are documentation
- Fast test suite enables confidence
- Test coverage prevents regressions

Rails provides several test types:
- **Model tests**: Business logic and validations
- **Controller tests**: Request handling
- **Integration tests**: Multi-controller workflows
- **System tests**: Full browser simulation
- **Mailer tests**: Email content and delivery
- **Job tests**: Background job behavior

## Minitest vs RSpec

Rails uses **Minitest** by default. It's simple, fast, and built into Ruby.

**Minitest:**
```ruby
test "product must have a name" do
  product = Product.new(price: 9.99)
  assert_not product.valid?
  assert_includes product.errors[:name], "can't be blank"
end
```

**RSpec (alternative):**
```ruby
it "must have a name" do
  product = Product.new(price: 9.99)
  expect(product).not_to be_valid
  expect(product.errors[:name]).to include("can't be blank")
end
```

Rails philosophy: Use Minitest unless you have strong RSpec preference. Minitest is simpler, faster, and requires no extra gems.

## Test Structure

### Test File Organization

```
test/
├── models/              # Model tests
├── controllers/         # Controller tests
├── integration/         # Integration tests
├── system/              # System tests (browser)
├── mailers/             # Mailer tests
├── jobs/                # Job tests
├── helpers/             # Helper tests
├── fixtures/            # Test data
└── test_helper.rb       # Test configuration
```

### Basic Test Structure

```ruby
require "test_helper"

class ProductTest < ActiveSupport::TestCase
  test "should not save product without name" do
    product = Product.new
    assert_not product.save, "Saved product without name"
  end

  test "should save valid product" do
    product = Product.new(name: "Widget", price: 9.99)
    assert product.save, "Failed to save valid product"
  end
end
```

## Fixtures

Test data defined in YAML files.

### Defining Fixtures

```yaml
# test/fixtures/products.yml
widget:
  name: Widget
  price: 9.99
  available: true
  category: electronics

gadget:
  name: Gadget
  price: 14.99
  available: false
  category: electronics
```

### Using Fixtures

```ruby
test "finds widget by name" do
  widget = products(:widget)  # Loads from fixtures
  assert_equal "Widget", widget.name
  assert_equal 9.99, widget.price
end

test "associates with category" do
  widget = products(:widget)
  assert_equal categories(:electronics), widget.category
end
```

### ERB in Fixtures

```yaml
# test/fixtures/products.yml
<% 10.times do |n| %>
product_<%= n %>:
  name: <%= "Product #{n}" %>
  price: <%= (n + 1) * 10 %>
<% end %>
```

### Associations in Fixtures

```yaml
# test/fixtures/categories.yml
electronics:
  name: Electronics

# test/fixtures/products.yml
widget:
  name: Widget
  category: electronics  # References category fixture
```

## Model Tests

Test business logic, validations, associations, and instance methods.

### Validation Tests

```ruby
require "test_helper"

class ProductTest < ActiveSupport::TestCase
  test "requires name" do
    product = Product.new(price: 9.99)
    assert_not product.valid?
    assert_includes product.errors[:name], "can't be blank"
  end

  test "requires positive price" do
    product = Product.new(name: "Widget", price: -1)
    assert_not product.valid?
    assert_includes product.errors[:price], "must be greater than 0"
  end

  test "requires unique SKU" do
    existing = products(:widget)
    product = Product.new(name: "New", sku: existing.sku)
    assert_not product.valid?
    assert_includes product.errors[:sku], "has already been taken"
  end
end
```

### Association Tests

```ruby
test "belongs to category" do
  product = products(:widget)
  assert_instance_of Category, product.category
end

test "has many reviews" do
  product = products(:widget)
  assert_respond_to product, :reviews
  assert_kind_of ActiveRecord::Associations::CollectionProxy, product.reviews
end
```

### Method Tests

```ruby
test "calculates discount price" do
  product = products(:widget)
  product.discount_percentage = 10
  assert_equal 8.99, product.discounted_price.round(2)
end

test "checks if in stock" do
  product = products(:widget)
  product.quantity = 5
  assert product.in_stock?

  product.quantity = 0
  assert_not product.in_stock?
end
```

## Controller Tests

Test request handling, rendering, and redirects.

```ruby
require "test_helper"

class ProductsControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get products_url
    assert_response :success
    assert_dom "h1", "Products"
  end

  test "should show product" do
    get product_url(products(:widget))
    assert_response :success
    assert_dom "h2", "Widget"
  end

  test "should create product" do
    assert_difference("Product.count", 1) do
      post products_url, params: { product: { name: "New Widget", price: 9.99 } }
    end

    assert_redirected_to product_path(Product.last)
    follow_redirect!
    assert_response :success
  end

  test "should not create invalid product" do
    assert_no_difference("Product.count") do
      post products_url, params: { product: { price: 9.99 } }  # Missing name
    end

    assert_response :unprocessable_entity
  end

  test "should update product" do
    product = products(:widget)
    patch product_url(product), params: { product: { name: "Updated" } }

    assert_redirected_to product_path(product)
    assert_equal "Updated", product.reload.name
  end

  test "should destroy product" do
    product = products(:widget)

    assert_difference("Product.count", -1) do
      delete product_url(product)
    end

    assert_redirected_to products_path
  end
end
```

## System Tests

Full browser simulation using Capybara.

```ruby
require "application_system_test_case"

class ProductsTest < ApplicationSystemTestCase
  test "creating a product" do
    visit products_path
    click_on "New Product"

    fill_in "Name", with: "Widget"
    fill_in "Price", with: "9.99"
    select "Electronics", from: "Category"

    click_on "Create Product"

    assert_text "Product created successfully"
    assert_text "Widget"
  end

  test "editing a product" do
    product = products(:widget)
    visit product_path(product)

    click_on "Edit"

    fill_in "Name", with: "Updated Widget"
    click_on "Update Product"

    assert_text "Product updated successfully"
    assert_text "Updated Widget"
  end

  test "searching products" do
    visit products_path

    fill_in "Search", with: "Widget"
    click_on "Search"

    assert_text "Widget"
    assert_no_text "Gadget"
  end
end
```

## Assertions

### Basic Assertions

```ruby
assert true
assert_not false
assert_nil nil
assert_not_nil "value"
assert_empty []
assert_not_empty [1, 2, 3]
assert_equal 5, 2 + 3
assert_not_equal 5, 2 + 2
assert_match /widget/i, "Widget"
assert_no_match /foo/, "bar"
assert_includes [1, 2, 3], 2
assert_instance_of String, "hello"
assert_kind_of Numeric, 42
assert_respond_to product, :name
assert_raises(ActiveRecord::RecordInvalid) { product.save! }
```

### Rails-Specific Assertions

```ruby
assert_difference('Product.count', 1) { Product.create!(name: "Test") }
assert_no_difference('Product.count') { Product.new.save }
assert_changes -> { product.reload.price }, from: 9.99, to: 14.99
assert_no_changes -> { product.reload.price }
assert_response :success
assert_response :redirect
assert_redirected_to product_path(product)
assert_dom "h1", "Products"
assert_dom "div.product", count: 5
```

### SQL Query Assertions

Test database query behavior:

```ruby
# Assert exact query count
assert_queries_count(2) do
  User.find(1)
  User.find(2)
end

# Assert no queries (useful for caching tests)
assert_no_queries { cached_value }

# Match query patterns
assert_queries_match(/SELECT.*users/) { User.first }
assert_no_queries_match(/UPDATE/) { User.first }
```

### Error Reporter Assertions

Test error reporting behavior:

```ruby
assert_error_reported(CustomError) do
  Rails.error.report(CustomError.new("test"))
end

assert_no_error_reported do
  safe_operation
end
```

## Test-Driven Development (TDD)

Rails encourages TDD: write tests first, then implement.

### TDD Workflow

1. **Red**: Write failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code while keeping tests green

**Example:**

```ruby
# 1. RED - Write failing test
test "calculates discount price" do
  product = Product.new(price: 100, discount_percentage: 10)
  assert_equal 90, product.discounted_price
end

# Run test - FAILS (method doesn't exist)

# 2. GREEN - Minimal implementation
class Product < ApplicationRecord
  def discounted_price
    price - (price * discount_percentage / 100.0)
  end
end

# Run test - PASSES

# 3. REFACTOR - Improve code
class Product < ApplicationRecord
  def discounted_price
    return price unless discount_percentage.present?
    (price * (1 - discount_percentage / 100.0)).round(2)
  end
end

# Run test - Still PASSES
```

See `references/tdd-workflow.md` for comprehensive TDD guidance.

## Running Tests

```bash
# All tests
rails test

# Specific file
rails test test/models/product_test.rb

# Specific test
rails test test/models/product_test.rb:14

# By pattern
rails test test/models/*_test.rb

# Failed tests only
rails test --fail-fast

# Verbose output
rails test --verbose
```

## Parallel Testing

Rails can run tests in parallel to speed up large test suites:

```ruby
# test/test_helper.rb
class ActiveSupport::TestCase
  parallelize(workers: :number_of_processors)
end
```

Run with custom worker count:

```bash
PARALLEL_WORKERS=4 rails test
```

Use threads instead of processes for lighter parallelization:

```ruby
parallelize(workers: :number_of_processors, with: :threads)
```

See `references/parallel-testing.md` for comprehensive parallel testing guidance including setup/teardown hooks and debugging flaky tests.

## Time Helpers

Test time-sensitive code with `ActiveSupport::Testing::TimeHelpers`:

```ruby
test "subscription expires after one year" do
  user = users(:subscriber)
  user.update!(subscribed_at: Time.current)

  travel_to 1.year.from_now do
    assert user.subscription_expired?
  end
end

test "discount valid during sale period" do
  travel_to Date.new(2024, 12, 25) do
    assert Product.christmas_sale_active?
  end
end
```

Available helpers:

```ruby
travel_to(date_or_time)     # Set current time within block
travel(duration)            # Move time forward by duration
freeze_time                 # Freeze at current time
travel_back                 # Return to real time (automatic after block)
```

## Further Reading

For deeper exploration:

- **`references/tdd-workflow.md`**: Test-driven development in Rails
- **`references/test-types.md`**: Model, controller, integration, system test patterns
- **`references/parallel-testing.md`**: Parallel testing configuration and troubleshooting

For code examples:

- **`examples/minitest-patterns.rb`**: Common testing patterns

## Summary

Rails testing provides:
- **Minitest framework** built into Rails
- **Multiple test types** for different layers
- **Fixtures** for test data
- **System tests** for browser simulation
- **TDD workflow** for confident development
- **Fast test suite** for rapid feedback

Master testing and you'll ship features with confidence.
