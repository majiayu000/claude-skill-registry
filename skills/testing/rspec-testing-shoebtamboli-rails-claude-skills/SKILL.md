---
name: rspec-testing
description: This skill should be used when writing, reviewing, or improving RSpec tests for Ruby on Rails applications. Use this skill for all testing tasks including model specs, controller specs, system specs, component specs, service specs, and integration tests. The skill provides comprehensive RSpec best practices from Better Specs and thoughtbot guides.
---

# RSpec Testing for Rails

## Overview

Write comprehensive, maintainable RSpec tests following industry best practices. This skill combines guidance from Better Specs and thoughtbot's testing guides to produce high-quality test coverage for Rails applications.

## Core Testing Principles

### 1. Test-Driven Development (TDD)
Follow the Red-Green-Refactor cycle:
- **Red**: Write failing tests that define expected behavior
- **Green**: Implement minimal code to make tests pass
- **Refactor**: Improve code while tests continue to pass

### 2. Test Structure (Arrange-Act-Assert)
Organize tests with clear phases separated by newlines:

```ruby
it 'creates a new article' do
  # Arrange - set up test data
  user = create(:user)
  attributes = {title: 'Test Article', body: 'Content here'}

  # Act - perform the action
  article = Article.create(attributes)

  # Assert - verify the outcome
  expect(article).to be_persisted
  expect(article.title).to eq('Test Article')
end
```

### 3. Single Responsibility
Each test should verify one behavior. For unit tests, use one expectation per test. For integration tests, multiple expectations are acceptable when testing a complete flow.

### 4. Test Real Behavior
Avoid over-mocking. Test actual application behavior when possible. Only stub external services, slow operations, and dependencies outside your control.

## Test Type Decision Tree

### When to Write Model Specs
Use model specs (`spec/models/`) for:
- Validations
- Associations
- Scopes
- Instance methods
- Class methods
- Enums and constants
- Database constraints

**Example:**
```ruby
# spec/models/article_spec.rb
RSpec.describe Article do
  describe 'validations' do
    it 'validates presence of title' do
      article = build(:article, title: nil)
      expect(article).not_to be_valid
      expect(article.errors[:title]).to include("can't be blank")
    end
  end

  describe 'associations' do
    it { is_expected.to belong_to(:user) }
    it { is_expected.to have_many(:comments) }
  end

  describe '#published?' do
    it 'returns true when status is published' do
      article = build(:article, status: :published)
      expect(article.published?).to be true
    end
  end
end
```

### When to Write Controller Specs
Use controller specs (`spec/controllers/`) for:
- Authorization checks (Pundit/CanCanCan)
- Request routing and parameter handling
- Response status codes
- Instance variable assignments
- Flash messages
- Redirects

**Example:**
```ruby
# spec/controllers/articles_controller_spec.rb
RSpec.describe ArticlesController do
  describe 'POST #create' do
    context 'with valid parameters' do
      it 'creates a new article and redirects' do
        user = create(:user)
        session[:user_id] = user.id

        valid_attributes = {
          title: 'Test Article',
          body: 'Article content'
        }

        expect do
          post :create, params: {article: valid_attributes}
        end.to change(Article, :count).by(1)

        expect(response).to redirect_to(Article.last)
      end
    end

    context 'with invalid parameters' do
      it 'does not create article and renders new template' do
        user = create(:user)
        session[:user_id] = user.id

        invalid_attributes = {title: '', body: ''}

        expect do
          post :create, params: {article: invalid_attributes}
        end.not_to change(Article, :count)

        expect(response).to render_template(:new)
      end
    end
  end
end
```

### When to Write System Specs
Use system specs (`spec/system/`) for:
- End-to-end user workflows
- Multi-step interactions
- JavaScript functionality
- Form submissions
- Navigation flows
- Real user scenarios

**Naming convention:** `user_action_spec.rb` or `feature_description_spec.rb`

**Example:**
```ruby
# spec/system/article_creation_spec.rb
RSpec.describe 'Article Creation' do
  it 'allows a user to create a new article' do
    user = create(:user)

    # Sign in
    visit '/login'
    fill_in 'Email', with: user.email
    fill_in 'Password', with: 'password'
    click_button 'Sign In'

    # Navigate to new article page
    click_link 'New Article'
    expect(page).to have_current_path(new_article_path)

    # Fill out the article form
    fill_in 'Title', with: 'My Test Article'
    fill_in 'Body', with: 'This is the article content'
    select 'Published', from: 'Status'

    # Submit the form
    click_button 'Create Article'

    expect(page).to have_content('Article created successfully!')
    expect(page).to have_content('My Test Article')
  end
end
```

### When to Write Component Specs
Use component specs (`spec/components/`) for:
- ViewComponent rendering
- Variant behavior
- Slot functionality
- Conditional rendering
- Component attributes

**Example:**
```ruby
# spec/components/button_component_spec.rb
RSpec.describe ButtonComponent, type: :component do
  describe 'variants' do
    it 'renders primary variant' do
      render_inline(described_class.new(variant: :primary)) { 'Click me' }

      button = page.find('button')
      expect(button[:class]).to include('btn-primary')
      expect(page).to have_button('Click me')
    end

    it 'renders secondary variant' do
      render_inline(described_class.new(variant: :secondary)) { 'Cancel' }

      button = page.find('button')
      expect(button[:class]).to include('btn-secondary')
    end
  end
end
```

### When to Write Service/Integration Specs
Use service/integration specs (`spec/services/`, `spec/integration/`) for:
- Complex business logic
- Multi-step workflows
- External API integrations
- Background job processing
- Data transformations

## RSpec Syntax & Style Guide

### Describe Blocks
Use Ruby documentation conventions:
- `.method_name` for class methods
- `#method_name` for instance methods

```ruby
describe '.find_by_title' do      # class method
describe '#publish' do              # instance method
describe 'validations' do           # grouping
```

### Context Blocks
Start with "when," "with," or "without":

```ruby
context 'when user is admin' do
context 'with valid parameters' do
context 'without authentication' do
```

### It Blocks
- Keep descriptions under 40 characters
- Use third-person present tense
- **Never** use "should" in descriptions

```ruby
# ✅ Good
it 'creates a new article' do
it 'validates presence of title' do
it 'redirects to dashboard' do

# ❌ Bad
it 'should create a new article' do
it 'should validate presence of title' do
```

### Expectations
Always use `expect` syntax (never `should`):

```ruby
# ✅ Good
expect(article).to be_valid
expect(response).to have_http_status(:success)
expect { action }.to change(Article, :count).by(1)

# ❌ Bad (deprecated)
article.should be_valid
response.should have_http_status(:success)
```

### One-Liners
Use `is_expected` for concise one-line specs:

```ruby
subject { article }

it { is_expected.to be_valid }
it { is_expected.to be_persisted }
```

## System Test Best Practices

### Authentication in System Tests

Test authentication flows directly without stubbing:

```ruby
# Good - test the actual login flow
visit '/login'
fill_in 'Email', with: user.email
fill_in 'Password', with: 'password'
click_button 'Sign In'

expect(page).to have_content('Dashboard')
```

### Controller Test Authentication

For controller tests, use direct session assignment rather than stubbing:

```ruby
# ✅ Good - direct session assignment
session[:user_id] = user.id

# ❌ Avoid - stubbing authentication
allow_any_instance_of(Controller).to receive(:logged_in?).and_return(true)
```

### Avoid CSS Class Testing

Don't test implementation details like CSS utility classes. Test semantic selectors and content:

```ruby
# ✅ Good - semantic selectors
expect(page).to have_selector(:test_id, 'user-modal')
expect(page).to have_css("[aria-hidden='false']")
expect(page).to have_content('Success message')
expect(page).to have_button('Submit')

# ❌ Bad - coupling to CSS implementation
expect(page).to have_css('.opacity-100')
expect(page).to have_css('.bg-red-500')
expect(page).to have_css('.rounded-lg')
```

## Factory Patterns

### Organization
1. Associations (implicit) first
2. Attributes (alphabetical)
3. Traits (alphabetical)

```ruby
FactoryBot.define do
  factory :article do
    # Associations
    user
    category

    # Attributes (alphabetical)
    body { 'Article content goes here...' }
    published_at { Time.current }
    status { :draft }
    title { 'Sample Article Title' }

    # Traits (alphabetical)
    trait :published do
      status { :published }
      published_at { 1.day.ago }
    end

    trait :with_tags do
      after(:create) do |article|
        create_list(:tag, 3, article: article)
      end
    end
  end
end
```

### Prefer Build Over Create
Use `build` and `build_stubbed` when database persistence isn't needed:

```ruby
# ✅ Good - fast, no database hit
it 'validates title format' do
  article = build(:article, title: '')
  expect(article).not_to be_valid
end

# Less optimal - unnecessary database hit
it 'validates title format' do
  article = create(:article, title: '')
  expect(article).not_to be_valid
end
```

## Common Testing Patterns

### Testing Validations
```ruby
describe 'validations' do
  it 'validates presence of title' do
    article = build(:article, title: nil)
    expect(article).not_to be_valid
    expect(article.errors[:title]).to include("can't be blank")
  end

  it 'validates length of title' do
    article = build(:article, title: 'a' * 256)
    expect(article).not_to be_valid
  end

  it 'allows valid titles' do
    article = build(:article, title: 'Valid Title')
    expect(article).to be_valid
  end
end
```

### Testing Enums
```ruby
describe 'enums' do
  it 'defines status enum' do
    expect(described_class.statuses).to eq({
      'draft' => 'draft',
      'published' => 'published',
      'archived' => 'archived'
    })
  end

  it 'has correct default' do
    article = described_class.new
    expect(article.status).to eq('draft')
  end
end
```

### Testing Authorization
```ruby
context 'when user is not admin' do
  it 'raises authorization error' do
    user = create(:user, role: :member)
    session[:user_id] = user.id

    expect do
      get :admin_dashboard
    end.to raise_error(Pundit::NotAuthorizedError)
  end
end
```

### Using Shoulda Matchers
```ruby
describe 'associations' do
  it { is_expected.to belong_to(:user) }
  it { is_expected.to have_many(:comments) }
end

describe 'validations' do
  it { is_expected.to validate_presence_of(:title) }
  it { is_expected.to validate_length_of(:title).is_at_most(255) }
end
```

## What to Avoid

### ❌ Don't Stub the System Under Test
Never mock or stub methods on the class being tested:

```ruby
# ❌ Bad
it 'processes payment' do
  order = Order.new
  allow(order).to receive(:calculate_total).and_return(100)
  expect(order.process_payment).to be true
end

# ✅ Good
it 'processes payment' do
  order = Order.new(line_items: [line_item])
  expect(order.process_payment).to be true
end
```

### ❌ Don't Test Private Methods
Test the public interface. Private methods are tested indirectly:

```ruby
# ❌ Bad
describe '#calculate_total (private)' do
  it 'sums line items' do
    order.send(:calculate_total)
  end
end

# ✅ Good
describe '#total' do
  it 'returns sum of line items' do
    expect(order.total).to eq(100)
  end
end
```

### ❌ Avoid `any_instance_of`
Use dependency injection instead:

```ruby
# ❌ Bad
allow_any_instance_of(PaymentService).to receive(:charge)

# ✅ Good
payment_service = instance_double(PaymentService)
allow(payment_service).to receive(:charge).and_return(success)
order = Order.new(payment_service: payment_service)
```

## Quick Reference

### Test Organization
```ruby
RSpec.describe ClassName do
  # Setup (let, before)
  let(:resource) { create(:resource) }

  before do
    # common setup
  end

  # Validations
  describe 'validations' do
  end

  # Associations
  describe 'associations' do
  end

  # Class methods
  describe '.class_method' do
  end

  # Instance methods
  describe '#instance_method' do
    context 'when condition' do
      it 'does something' do
      end
    end
  end
end
```

### Expectation Matchers
```ruby
# Equality
expect(value).to eq(expected)
expect(value).to be(expected)           # same object
expect(value).to match(/regex/)

# Predicates
expect(object).to be_valid
expect(object).to be_persisted
expect(collection).to be_empty

# Collections
expect(array).to include(item)
expect(array).to contain_exactly(1, 2, 3)
expect(hash).to have_key(:name)

# Changes
expect { action }.to change(Model, :count).by(1)
expect { action }.to change { object.attribute }.from(old).to(new)

# Errors
expect { action }.to raise_error(ErrorClass)
expect { action }.not_to raise_error
```

## Resources

This skill includes detailed reference documentation in the `references/` directory:

### `references/better_specs_guide.md`
Comprehensive patterns from Better Specs including:
- Describe/context/it block conventions
- Subject and let usage
- Mocking strategies
- Shared examples
- Factory patterns

### `references/thoughtbot_patterns.md`
thoughtbot's RSpec best practices covering:
- Modern RSpec syntax
- Test structure and organization
- What to avoid in tests
- Capybara patterns for system tests
- Factory organization

Load these references when you need detailed examples or are unsure about a specific pattern.
