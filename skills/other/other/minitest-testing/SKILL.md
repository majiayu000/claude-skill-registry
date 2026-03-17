---
name: minitest-testing
description: Write, review, and improve Minitest tests for Ruby on Rails applications. Covers model tests, controller tests, system tests, fixtures, and best practices from Rails Testing Guide.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Minitest Testing for Rails

Write comprehensive, maintainable Minitest tests following Rails conventions and best practices. This skill provides patterns for model tests, controller tests, system tests with Capybara, and fixture usage.

<when-to-use>
- Writing new tests for models, controllers, or system workflows
- Reviewing existing test coverage and improving quality
- Fixing failing tests or debugging test issues
- Setting up test fixtures and test helpers
- Writing system tests for end-to-end user workflows
- Testing Hotwire/Turbo behavior in system tests
</when-to-use>

<benefits>
- **Built-in Framework** - No additional gems needed, part of Rails
- **Fast Execution** - Lightweight and performant test suite
- **Rails Integration** - First-class support in Rails framework
- **Fixture Support** - Simple YAML-based test data
- **System Tests** - Built-in Capybara integration for browser testing
- **Parallel Testing** - Run tests in parallel with `bin/rails test:parallel`
</benefits>

<verification-checklist>
Before completing testing work:
- ✅ Tests follow Minitest naming convention: `test "descriptive name"`
- ✅ Fixtures used appropriately for test data
- ✅ System tests cover critical user workflows
- ✅ Assertions are specific and descriptive
- ✅ Tests are independent and can run in any order
- ✅ All tests passing: `bin/rails test`
</verification-checklist>

<standards>
- Use descriptive test names: `test "creates post with valid attributes"`
- One assertion concept per test (may use multiple assert calls)
- Use specific assertions: `assert_equal`, `assert_redirected_to`, not just `assert`
- Reference fixtures with symbols: `posts(:published_post)`
- Use `setup` and `teardown` for test lifecycle management
- Use `assert_difference` for counting changes
- System tests for critical workflows, controller/model tests for details
- Run tests before committing code
</standards>

---

## Core Testing Principles

### 1. Test Structure
Organize tests with clear phases:

```ruby
test "creates article with valid attributes" do
  # Arrange - set up test data
  user = users(:alice)

  # Act - perform the action
  article = Article.create(
    title: "Test Article",
    body: "Content here",
    user: user
  )

  # Assert - verify the outcome
  assert article.persisted?
  assert_equal "Test Article", article.title
end
```

### 2. Test Independence
Each test should be independent and able to run in any order. Use `setup` for common initialization:

```ruby
class ArticleTest < ActiveSupport::TestCase
  setup do
    @user = users(:alice)
    @article = articles(:published)
  end

  test "publishes article" do
    @article.publish!
    assert @article.published?
  end
end
```

### 3. Single Responsibility
Each test verifies one behavior, though it may use multiple assertions to fully verify that behavior.

---

## Test Types

### Model Tests (`test/models/`)
Test business logic, validations, associations, and custom methods.

**File location:** `test/models/article_test.rb`

```ruby
class ArticleTest < ActiveSupport::TestCase
  test "validates presence of title" do
    article = Article.new(body: "Content")
    assert_not article.valid?
    assert_includes article.errors[:title], "can't be blank"
  end

  test "belongs to user" do
    article = articles(:published)
    assert_instance_of User, article.user
  end

  test "#published? returns true when status is published" do
    article = articles(:published)
    assert article.published?
  end
end
```

### Controller Tests (`test/controllers/`)
Test HTTP responses, redirects, authentication, and parameter handling.

**File location:** `test/controllers/articles_controller_test.rb`

```ruby
class ArticlesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @user = users(:alice)
    sign_in_as(@user)  # helper method
  end

  test "GET index returns success" do
    get articles_path
    assert_response :success
  end

  test "POST create with valid params creates article" do
    assert_difference("Article.count", 1) do
      post articles_path, params: {
        article: { title: "New Article", body: "Content" }
      }
    end

    assert_redirected_to article_path(Article.last)
  end

  test "POST create with invalid params renders new" do
    assert_no_difference("Article.count") do
      post articles_path, params: {
        article: { title: "", body: "" }
      }
    end

    assert_response :unprocessable_entity
  end
end
```

### System Tests (`test/system/`)
Test end-to-end user workflows with browser simulation.

**File location:** `test/system/article_creation_test.rb`

```ruby
class ArticleCreationTest < ApplicationSystemTestCase
  test "user creates new article" do
    visit root_path
    click_on "New Article"

    fill_in "Title", with: "My Test Article"
    fill_in "Body", with: "This is the content"
    select "Published", from: "Status"

    click_on "Create Article"

    assert_text "Article was successfully created"
    assert_text "My Test Article"
  end

  test "article updates with Turbo Frame" do
    article = articles(:draft)
    visit article_path(article)

    click_on "Edit"
    fill_in "Title", with: "Updated Title"
    click_on "Update Article"

    # Turbo Frame update - no full page reload
    assert_text "Updated Title"
    assert_no_text article.title
  end
end
```

---

## Detailed Patterns & Examples

For comprehensive Minitest patterns and examples, see **[examples.md](examples.md)**.

### Pattern Categories

**examples.md contains:**
- **Fixtures** - YAML fixtures, associations, and fixture access
- **Model Testing** - Validations, associations, scopes, callbacks, enums
- **Controller Testing** - CRUD actions, authentication, authorization
- **System Testing** - Capybara selectors, form interactions, JavaScript behavior
- **Turbo/Hotwire Testing** - Turbo Frames, Turbo Streams, Stimulus controllers
- **Background Jobs** - Testing ActiveJob and SolidQueue jobs
- **Mailers** - Testing ActionMailer delivery and content
- **Test Helpers** - Custom assertions and helper methods
- **Mocking/Stubbing** - When and how to use mocks with Minitest

Refer to examples.md for complete code examples.

---

## Common Assertions

```ruby
# Equality
assert_equal expected, actual
assert_not_equal unexpected, actual

# Truth/Falsehood
assert value
assert_not value
assert_nil value
assert_not_nil value

# Predicates
assert article.valid?
assert_not article.persisted?
assert articles.empty?

# Collections
assert_includes array, item
assert_empty collection
assert_not_empty collection

# Differences (counting changes)
assert_difference "Article.count", 1 do
  Article.create!(title: "New", body: "Content")
end

assert_no_difference "Article.count" do
  Article.create(title: "", body: "")  # invalid
end

# HTTP Responses
assert_response :success
assert_response :redirect
assert_response :not_found
assert_redirected_to articles_path

# Errors
assert_raises ActiveRecord::RecordInvalid do
  Article.create!(title: nil)
end
```

---

## Fixtures

### Fixture Files (`test/fixtures/*.yml`)

```yaml
# test/fixtures/users.yml
alice:
  email: alice@example.com
  name: Alice Smith
  role: admin

bob:
  email: bob@example.com
  name: Bob Jones
  role: member
```

```yaml
# test/fixtures/articles.yml
published:
  user: alice
  title: Published Article
  body: This article is live
  status: published
  published_at: <%= 1.day.ago %>

draft:
  user: bob
  title: Draft Article
  body: Work in progress
  status: draft
```

### Using Fixtures in Tests

```ruby
test "finds published articles" do
  published = articles(:published)
  draft = articles(:draft)

  results = Article.published

  assert_includes results, published
  assert_not_includes results, draft
end
```

---

## Test Helpers

### Authentication Helper

```ruby
# test/test_helper.rb
class ActionDispatch::IntegrationTest
  def sign_in_as(user)
    post login_path, params: { email: user.email, password: "password" }
  end
end
```

### Custom Assertions

```ruby
# test/test_helper.rb
module ActiveSupport
  class TestCase
    def assert_valid(record)
      assert record.valid?, "Expected #{record.class} to be valid, errors: #{record.errors.full_messages}"
    end
  end
end
```

---

<testing>

## Running Tests

```bash
# Run all tests
bin/rails test

# Run specific test file
bin/rails test test/models/article_test.rb

# Run specific test by line number
bin/rails test test/models/article_test.rb:12

# Run tests by pattern
bin/rails test test/models/*_test.rb

# Run system tests only
bin/rails test:system

# Run tests in parallel
bin/rails test:parallel

# Run with verbose output
bin/rails test -v

# Run and show coverage
COVERAGE=true bin/rails test
```

</testing>

---

<related-skills>
- rails-models - ActiveRecord patterns for database models
- rails-controllers - Controller patterns and RESTful design
- rails-hotwire - Testing Turbo Frames/Streams and Stimulus
- rails-jobs - Testing background jobs with SolidQueue
- rails-mailers - Testing email delivery with ActionMailer
</related-skills>

<resources>

**Official Documentation:**
- [Rails Testing Guide](https://guides.rubyonrails.org/testing.html) - Comprehensive Rails testing guide
- [Minitest Documentation](https://docs.seattlerb.org/minitest/) - Minitest framework docs
- [Capybara Cheat Sheet](https://devhints.io/capybara) - System test selectors

**Tools:**
- [SimpleCov](https://github.com/simplecov-ruby/simplecov) - Code coverage for Ruby
- [shoulda-matchers](https://github.com/thoughtbot/shoulda-matchers) - Additional matchers for Rails

</resources>
